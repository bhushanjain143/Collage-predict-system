"""Optional LLM calls (OpenAI or Gemini) for counselling. Uses stdlib only."""
from __future__ import annotations

import json
import os
import ssl
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

from counselor_prompts import (
    BATCH_CARD_SYSTEM,
    COMPARE_SYSTEM,
    COUNSELOR_CHAT_SYSTEM,
    GUIDANCE_NEXT_STEPS_SYSTEM,
    LIST_EXPLAIN_SYSTEM,
    SCHOLARSHIP_APPLY_SYSTEM,
    build_batch_card_user_message,
    build_counselor_user_message,
    build_scholarship_apply_user_message,
    wrap_system,
)


def get_ai_public_config() -> dict[str, Any]:
    key_o = bool(os.environ.get("OPENAI_API_KEY", "").strip())
    key_g = bool(os.environ.get("GEMINI_API_KEY", "").strip())
    if key_o:
        provider = "openai"
    elif key_g:
        provider = "gemini"
    else:
        provider = None
    return {
        "ai_enabled": provider is not None,
        "provider": provider,
        "tasks": [
            "chat",
            "card_insights",
            "scholarship_guide",
            "explain_list",
            "compare",
            "guidance",
        ],
    }


def _post_json(url: str, headers: dict[str, str], payload: dict, timeout: int = 75) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _openai_messages_completion(messages: list[dict[str, str]], max_tokens: int = 1200) -> str:
    api_key = os.environ["OPENAI_API_KEY"].strip()
    model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini").strip()
    url = "https://api.openai.com/v1/chat/completions"
    body = {
        "model": model,
        "messages": messages,
        "temperature": 0.45,
        "max_tokens": max_tokens,
    }
    out = _post_json(
        url,
        {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        body,
    )
    return (out.get("choices") or [{}])[0].get("message", {}).get("content") or ""


def _openai_complete(system: str, user: str, max_tokens: int = 1200) -> str:
    return _openai_messages_completion(
        [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        max_tokens=max_tokens,
    )


def _gemini_complete(system: str, user: str, max_out: int = 2048) -> str:
    api_key = os.environ["GEMINI_API_KEY"].strip()
    model = os.environ.get("GEMINI_MODEL", "gemini-1.5-flash").strip()
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{model}:generateContent?key={urllib.parse.quote(api_key, safe='')}"
    )
    body = {
        "contents": [{"role": "user", "parts": [{"text": system + "\n\n" + user}]}],
        "generationConfig": {"temperature": 0.45, "maxOutputTokens": max_out},
    }
    out = _post_json(url, {"Content-Type": "application/json"}, body)
    parts = (
        (out.get("candidates") or [{}])[0]
        .get("content", {})
        .get("parts")
        or []
    )
    return "".join(p.get("text", "") for p in parts)


def _gemini_history_block(history: list[dict[str, str]] | None) -> str:
    if not history:
        return ""
    lines: list[str] = ["Previous conversation (most recent last):"]
    for h in history[-12:]:
        r = (h.get("role") or "user").strip().lower()
        c = (h.get("content") or "").strip()
        if not c:
            continue
        if r not in ("user", "assistant"):
            r = "user"
        lines.append(f"{r.upper()}: {c[:3500]}")
    return "\n".join(lines) + "\n\n"


def _complete(system_wrapped: str, user: str, *, openai_max_tokens: int = 1200, gemini_max: int = 2048) -> tuple[str, str]:
    if os.environ.get("OPENAI_API_KEY", "").strip():
        return _openai_complete(system_wrapped, user, max_tokens=openai_max_tokens), "openai"
    return _gemini_complete(system_wrapped, user, max_out=gemini_max), "gemini"


def _complete_openai_messages(messages: list[dict[str, str]], max_tokens: int) -> tuple[str, str]:
    if os.environ.get("OPENAI_API_KEY", "").strip():
        return _openai_messages_completion(messages, max_tokens=max_tokens), "openai"
    # Gemini: flatten
    sys = messages[0]["content"] if messages and messages[0].get("role") == "system" else ""
    rest = []
    for m in messages[1:]:
        rest.append(f"{m.get('role', 'user').upper()}: {m.get('content', '')}")
    user_block = "\n\n".join(rest)
    return _gemini_complete(sys, user_block, max_out=max(2048, max_tokens)), "gemini"


def run_counselor_chat(
    percentile: Any,
    category: Any,
    top_colleges: list[dict[str, Any]],
    user_question: str,
    history: list[dict[str, str]] | None,
    city: str | None = None,
) -> dict[str, Any]:
    cfg = get_ai_public_config()
    if not cfg["ai_enabled"]:
        return {
            "status": "disabled",
            "text": _chat_fallback(percentile, category, user_question),
            "provider": None,
        }
    system = wrap_system(COUNSELOR_CHAT_SYSTEM)
    user_msg = build_counselor_user_message(percentile, category, top_colleges, user_question, city=city)
    messages: list[dict[str, str]] = [{"role": "system", "content": system}]
    for h in (history or [])[-10:]:
        r = h.get("role", "user")
        c = (h.get("content") or "").strip()
        if r not in ("user", "assistant") or not c:
            continue
        messages.append({"role": r, "content": c[:6000]})
    messages.append({"role": "user", "content": user_msg[:12000]})
    try:
        text, prov = _complete_openai_messages(messages, max_tokens=900)
        text = (text or "").strip()
        if not text:
            raise ValueError("empty model response")
        return {"status": "ok", "text": text[:8000], "provider": prov}
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")[:500]
        return {
            "status": "error",
            "text": _chat_fallback(percentile, category, user_question),
            "provider": cfg.get("provider"),
            "error": f"HTTP {e.code}: {err_body}",
        }
    except Exception as exc:  # noqa: BLE001
        return {
            "status": "error",
            "text": _chat_fallback(percentile, category, user_question),
            "provider": cfg.get("provider"),
            "error": str(exc)[:300],
        }


def run_batch_card_insights(
    percentile: Any,
    category: Any,
    colleges: list[dict[str, Any]],
) -> dict[str, Any]:
    cfg = get_ai_public_config()
    if not cfg["ai_enabled"]:
        return {
            "status": "disabled",
            "text": _batch_fallback(percentile, category, colleges),
            "provider": None,
        }
    system = wrap_system(BATCH_CARD_SYSTEM)
    user_msg = build_batch_card_user_message(percentile, category, colleges)
    try:
        text, prov = _complete(system, user_msg, openai_max_tokens=2500, gemini_max=4096)
        text = (text or "").strip()
        if not text:
            raise ValueError("empty model response")
        return {"status": "ok", "text": text[:12000], "provider": prov}
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")[:500]
        return {
            "status": "error",
            "text": _batch_fallback(percentile, category, colleges),
            "provider": cfg.get("provider"),
            "error": f"HTTP {e.code}: {err_body}",
        }
    except Exception as exc:  # noqa: BLE001
        return {
            "status": "error",
            "text": _batch_fallback(percentile, category, colleges),
            "provider": cfg.get("provider"),
            "error": str(exc)[:300],
        }


def run_scholarship_apply_guide(
    name: str,
    url: str,
    documents: list[str],
    category: str,
) -> dict[str, Any]:
    cfg = get_ai_public_config()
    if not cfg["ai_enabled"]:
        return {
            "status": "disabled",
            "text": _scholar_fallback(name, url),
            "provider": None,
        }
    system = wrap_system(SCHOLARSHIP_APPLY_SYSTEM)
    user_msg = build_scholarship_apply_user_message(name, url, documents, category)
    try:
        text, prov = _complete(system, user_msg, openai_max_tokens=1200, gemini_max=2048)
        text = (text or "").strip()
        if not text:
            raise ValueError("empty model response")
        return {"status": "ok", "text": text[:8000], "provider": prov}
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")[:500]
        return {
            "status": "error",
            "text": _scholar_fallback(name, url),
            "provider": cfg.get("provider"),
            "error": f"HTTP {e.code}: {err_body}",
        }
    except Exception as exc:  # noqa: BLE001
        return {
            "status": "error",
            "text": _scholar_fallback(name, url),
            "provider": cfg.get("provider"),
            "error": str(exc)[:300],
        }


def run_llm_task(
    task: str,
    context: dict[str, Any],
    colleges: list[dict[str, Any]] | None,
    compare_pair: list[dict[str, Any]] | None,
) -> dict[str, Any]:
    cfg = get_ai_public_config()
    if not cfg["ai_enabled"]:
        return {
            "status": "disabled",
            "text": _fallback_text(task, context, colleges, compare_pair),
            "provider": None,
        }

    pct = context.get("percentile")
    cat = context.get("category")
    city = context.get("city")

    if task == "compare" and compare_pair and len(compare_pair) == 2:
        system = wrap_system(COMPARE_SYSTEM)
        user_msg = (
            f"Student: percentile={pct}, category={cat}.\n\n"
            "Compare these two options:\n"
            + json.dumps(compare_pair, ensure_ascii=False)[:8000]
        )
    elif task == "guidance":
        system = wrap_system(GUIDANCE_NEXT_STEPS_SYSTEM)
        user_msg = (
            f"Student: percentile={pct}, category={cat}, city filter={city}.\n"
            "Top colleges (summary):\n"
            + json.dumps((colleges or [])[:18], ensure_ascii=False)[:10000]
        )
    else:
        system = wrap_system(LIST_EXPLAIN_SYSTEM)
        user_msg = (
            f"Student: percentile={pct}, category={cat}, city filter={city}.\n\n"
            "Predicted colleges (JSON):\n"
            + json.dumps((colleges or [])[:28], ensure_ascii=False)[:12000]
        )

    try:
        text, prov = _complete(system, user_msg, openai_max_tokens=1200, gemini_max=2048)
        text = (text or "").strip()
        if not text:
            raise ValueError("empty model response")
        return {"status": "ok", "text": text[:8000], "provider": prov}
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")[:500]
        return {
            "status": "error",
            "text": _fallback_text(task, context, colleges, compare_pair),
            "provider": cfg.get("provider"),
            "error": f"HTTP {e.code}: {err_body}",
        }
    except Exception as exc:  # noqa: BLE001
        return {
            "status": "error",
            "text": _fallback_text(task, context, colleges, compare_pair),
            "provider": cfg.get("provider"),
            "error": str(exc)[:300],
        }


def _chat_fallback(percentile: Any, category: Any, question: str) -> str:
    return (
        "**Offline** — add `OPENAI_API_KEY` or `GEMINI_API_KEY` on the server for the AI counselor.\n\n"
        f"Your context: percentile **{percentile}**, category **{category}**.\n"
        f"Question was: {(question or '')[:200]}\n\n"
        "Tip: verify every cutoff and document on the official CET Cell / college portals."
    )


def _batch_fallback(percentile: Any, category: Any, colleges: list[dict[str, Any]] | None) -> str:
    lines = [
        "**Offline** — configure an API key for per-college AI lines.",
        f"Student: {percentile} percentile, {category}.",
    ]
    for c in (colleges or [])[:8]:
        nm = c.get("college_name") or "—"
        br = c.get("branch") or "—"
        lines.append(f"- {nm} ({br}): compare your percentile to the shown cutoff; tier = {c.get('chance', '—')}.")
    return "\n".join(lines)


def _scholar_fallback(name: str, url: str) -> str:
    u = url or "official portal (search by exact scheme name)"
    return (
        "**Offline** — add an API key for AI apply steps.\n\n"
        f"**{name}**: open **{u}**, register, fill the form, upload listed documents, submit before the deadline, "
        "and download a copy of your application."
    )


def _fallback_text(
    task: str,
    context: dict[str, Any],
    colleges: list[dict[str, Any]] | None,
    compare_pair: list[dict[str, Any]] | None,
) -> str:
    pct = context.get("percentile", "—")
    lines = [
        "**Offline explanation** (add `OPENAI_API_KEY` or `GEMINI_API_KEY` on the server for full AI text.)",
        f"- Your inputs: percentile **{pct}**, category **{context.get('category', '—')}**, city filter **{context.get('city', '—')}**.",
    ]
    if task == "compare" and compare_pair and len(compare_pair) == 2:
        lines.append("- Compare: weigh branch strength, commute, fees (verify on college sites), and keep one safer backup in CAP.")
    elif task == "guidance":
        lines.append(
            "- Next steps: download latest CAP PDFs from CET Cell, freeze a preference list with highs/mediums/lows, "
            "and parallel-track scholarships on MahaDBT / NSP."
        )
    else:
        n = len(colleges or [])
        lines.append(
            f"- Your list has **{n}** suggestions. **High** = at/above last published cutoff; **Medium** = close; **Low** = reach — cutoffs shift yearly."
        )
    return "\n".join(lines)
