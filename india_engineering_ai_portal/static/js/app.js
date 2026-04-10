(() => {
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];

  const state = {
    colleges: [],
    allColleges: null,
    selected: new Set(),
  };

  async function loadColleges() {
    const params = new URLSearchParams({
      q: $("#q").value.trim(),
      type: $("#ftype").value,
      state: $("#fstate").value,
      branch: $("#fbranch").value,
    });
    const r = await fetch(`/api/colleges?${params}`);
    state.colleges = await r.json();
    renderGrid();
    fillPredictSelect();
  }

  async function bootstrap() {
    const r = await fetch("/api/colleges");
    state.allColleges = await r.json();
    const sel = $("#fstate");
    const cur = sel.value;
    sel.innerHTML = '<option value="all">All states</option>';
    [...new Set(state.allColleges.map((c) => c.state))].sort().forEach((s) => {
      const o = document.createElement("option");
      o.value = s;
      o.textContent = s;
      sel.appendChild(o);
    });
    if ([...sel.options].some((o) => o.value === cur)) sel.value = cur;
    await loadColleges();
  }

  function renderGrid() {
    const grid = $("#grid");
    grid.innerHTML = "";
    state.colleges.forEach((c) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "college-card" + (state.selected.has(c.id) ? " selected" : "");
      btn.dataset.id = c.id;
      btn.innerHTML = `
        <div class="type">${escapeHtml(c.college_type)}</div>
        <h3>${escapeHtml(c.college_name)}</h3>
        <div class="meta">${escapeHtml(c.city)}, ${escapeHtml(c.state)} · ${escapeHtml(c.branch)}</div>
        <div class="tag-row">
          <span class="tag">Cutoff ~${c.cutoff_score}</span>
          <span class="tag">₹${c.fees_per_year.toLocaleString("en-IN")}/yr</span>
          <span class="tag">${c.placement_percent}% placed</span>
        </div>
      `;
      btn.addEventListener("click", () => {
        if (state.selected.has(c.id)) state.selected.delete(c.id);
        else state.selected.add(c.id);
        btn.classList.toggle("selected", state.selected.has(c.id));
      });
      grid.appendChild(btn);
    });
  }

  function fillPredictSelect() {
    const list = state.allColleges || state.colleges;
    const sel = $("#predict-college");
    const v = sel.value;
    sel.innerHTML = "";
    list.forEach((c) => {
      const o = document.createElement("option");
      o.value = c.id;
      o.textContent = `${c.college_name} — ${c.branch}`;
      sel.appendChild(o);
    });
    if (v && [...sel.options].some((o) => o.value === v)) sel.value = v;
  }

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function syncWeights() {
    let a = +$("#rwpl").value;
    let b = +$("#rwpk").value;
    let c = +$("#rwfe").value;
    const t = a + b + c || 1;
    $("#wpl").value = (a / t).toFixed(3);
    $("#wpk").value = (b / t).toFixed(3);
    $("#wfe").value = (c / t).toFixed(3);
  }

  $("#rec-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    syncWeights();
    const fd = new FormData(e.target);
    const body = Object.fromEntries(fd.entries());
    body.jee_percentile = parseFloat(body.jee_percentile || "0");
    body.max_fee_per_year = parseInt(body.max_fee_per_year || "600000", 10);
    body.weight_placement = parseFloat($("#wpl").value);
    body.weight_package = parseFloat($("#wpk").value);
    body.weight_affordability = parseFloat($("#wfe").value);
    const r = await fetch("/api/recommend", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const rows = await r.json();
    const out = $("#rec-out");
    out.innerHTML = "";
    rows.forEach((c) => {
      const div = document.createElement("article");
      div.className = "college-card";
      div.style.cursor = "default";
      div.innerHTML = `
        <div class="type">match ${c.match_score}</div>
        <h3>${escapeHtml(c.college_name)}</h3>
        <div class="meta">${escapeHtml(c.branch)} · ${escapeHtml(c.city)}</div>
        <div class="tag-row">
          <span class="tag">${escapeHtml(c.college_type)}</span>
          <span class="tag">₹${c.fees_per_year.toLocaleString("en-IN")}</span>
          <span class="tag">${c.avg_package_lpa} LPA avg</span>
        </div>
      `;
      out.appendChild(div);
    });
  });

  ["rwpl", "rwpk", "rwfe"].forEach((id) => $("#" + id).addEventListener("input", syncWeights));

  $("#predict-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const fd = new FormData(e.target);
    const body = Object.fromEntries(fd.entries());
    body.jee_percentile = parseFloat(body.jee_percentile || "0");
    body.mht_percentile = parseFloat(body.mht_percentile || "0");
    body.college_id = parseInt(body.college_id, 10);
    const r = await fetch("/api/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const j = await r.json();
    const el = $("#predict-out");
    if (j.error) {
      el.innerHTML = `<p class="muted">${escapeHtml(j.error)}</p>`;
      return;
    }
    const cls =
      j.result === "High Chance" ? "badge-high" : j.result === "Medium Chance" ? "badge-med" : "badge-low";
    el.innerHTML = `
      <div class="badge ${cls}">${escapeHtml(j.result)}</div>
      <p><strong>${(j.probability * 100).toFixed(1)}%</strong> demo confidence · used percentile <strong>${j.used_percentile}</strong>
      (incl. category bump +${j.category_adjustment})</p>
      <p>${escapeHtml(j.detail)}</p>
      <p class="muted">${escapeHtml(j.disclaimer)}</p>
    `;
  });

  $("#sch-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const body = Object.fromEntries(new FormData(e.target).entries());
    const r = await fetch("/api/scholarships", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const j = await r.json();
    $("#sch-out").innerHTML = "<ul>" + j.matches.map((m) => `<li>${escapeHtml(m)}</li>`).join("") + "</ul>";
  });

  $("#cap-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const body = Object.fromEntries(new FormData(e.target).entries());
    const r = await fetch("/api/cap-hint", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const j = await r.json();
    $("#cap-out").innerHTML = `<p>${escapeHtml(j.hint)}</p><p class="muted">${escapeHtml(j.disclaimer)}</p>`;
  });

  $("#btn-compare").addEventListener("click", async () => {
    const ids = [...state.selected];
    if (ids.length < 2) {
      $("#compare-out").innerHTML = "<p class='muted'>Select at least two college cards in Explore (click to highlight).</p>";
      return;
    }
    const r = await fetch("/api/compare", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ids }),
    });
    const j = await r.json();
    if (j.error) {
      $("#compare-out").innerHTML = `<p class="muted">${escapeHtml(j.error)}</p>`;
      return;
    }
    const keys = ["college_name", "city", "state", "college_type", "branch", "cutoff_score", "fees_per_year", "placement_percent", "avg_package_lpa"];
    let html = "<p>" + escapeHtml(j.suggestion) + "</p><table><thead><tr><th>Field</th>";
    j.colleges.forEach((c) => {
      html += `<th>${escapeHtml(c.college_name)}</th>`;
    });
    html += "</tr></thead><tbody>";
    keys.forEach((k) => {
      html += `<tr><th>${k}</th>`;
      j.colleges.forEach((c) => {
        html += `<td>${escapeHtml(String(c[k] ?? ""))}</td>`;
      });
      html += "</tr>";
    });
    html += "</tbody></table>";
    $("#compare-out").innerHTML = html;
  });

  $("#chat-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const msg = $("#chat-msg").value.trim();
    if (!msg) return;
    $("#chat-msg").value = "";
    const log = $("#chat-log");
    const u = document.createElement("div");
    u.className = "bubble user";
    u.textContent = msg;
    log.appendChild(u);
    const r = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: msg }),
    });
    const j = await r.json();
    const b = document.createElement("div");
    b.className = "bubble bot";
    b.textContent = j.reply;
    log.appendChild(b);
    log.scrollTop = log.scrollHeight;
  });

  let t;
  ["#q", "#ftype", "#fstate", "#fbranch"].forEach((sel) => {
    $(sel).addEventListener("input", () => {
      clearTimeout(t);
      t = setTimeout(loadColleges, 200);
    });
    $(sel).addEventListener("change", loadColleges);
  });

  bootstrap();
  syncWeights();
})();
