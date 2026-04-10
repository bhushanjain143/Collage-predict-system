"""Optional LLM calls (OpenAI or Gemini) for counselling explanations. Uses stdlib only."""
from __future__ import annotations

import json
import os
import ssl
import urllib.error
import urllib.parse
import urllib.request
from typing import Any


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
        "tasks": ["explain_list", "compare", "guidance"],
    }


def _post_json(url: str, headers: dict[str, str], payload: dict, timeout: int = 55) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _openai_complete(system: str, user: str) -> str:
    api_key = os.environ["OPENAI_API_KEY"].strip()
    model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini").strip()
    url = "https://api.openai.com/v1/chat/completions"
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.4,
        "max_tokens": 1200,
    }
    out = _post_json(
        url,
        {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        body,
    )
    return (out.get("choices") or [{}])[0].get("message", {}).get("content") or ""


def _gemini_complete(system: str, user: str) -> str:
    api_key = os.environ["GEMINI_API_KEY"].strip()
    model = os.environ.get("GEMINI_MODEL", "gemini-1.5-flash").strip()
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{model}:generateContent?key={urllib.parse.quote(api_key, safe='')}"
    )
    body = {
        "contents": [{"role": "user", "parts": [{"text": system + "\n\n" + user}]}],
        "generationConfig": {"temperature": 0.4, "maxOutputTokens": 1200},
    }
    out = _post_json(url, {"Content-Type": "application/json"}, body)
    parts = (
        (out.get("candidates") or [{}])[0]
        .get("content", {})
        .get("parts")
        or []
    )
    return "".join(p.get("text", "") for p in parts)


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

    system = (
        "You are a concise Maharashtra engineering admissions counsellor. "
        "Use MHT-CET / CAP terminology. Never guarantee a seat; remind users to verify on official CET Cell notices. "
        "Keep answers under 400 words, structured with short bullets where helpful."
    )

    user_parts: list[str] = []
    pct = context.get("percentile")
    cat = context.get("category")
    city = context.get("city")
    user_parts.append(f"Student context: percentile={pct}, category={cat}, preferred city filter={city}.")

    if task == "compare" and compare_pair and len(compare_pair) == 2:
        user_parts.append("Compare these two college+branch options for fit, risk, and typical next steps:")
        user_parts.append(json.dumps(compare_pair, ensure_ascii=False)[:6000])
    elif task == "guidance":
        user_parts.append(
            "Give practical next-step career/counselling guidance for this student "
            "(document checklist mindset, how to order preferences, backups) without naming unverified placements."
        )
        if colleges:
            user_parts.append("Their shortlist (top rows):\n" + json.dumps(colleges[:15], ensure_ascii=False))
    else:
        user_parts.append(
            "Explain why this shortlist is reasonable given typical cutoff logic (High/Medium/Low chance labels). "
            "Highlight how to read risk and backups."
        )
        if colleges:
            user_parts.append("Colleges:\n" + json.dumps(colleges[:25], ensure_ascii=False))

    user_msg = "\n".join(user_parts)

    try:
        if os.environ.get("OPENAI_API_KEY", "").strip():
            text = _openai_complete(system, user_msg)
            prov = "openai"
        else:
            text = _gemini_complete(system, user_msg)
            prov = "gemini"
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
    except Exception as exc:  # noqa: BLE001 — return safe fallback for API users
        return {
            "status": "error",
            "text": _fallback_text(task, context, colleges, compare_pair),
            "provider": cfg.get("provider"),
            "error": str(exc)[:300],
        }


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
