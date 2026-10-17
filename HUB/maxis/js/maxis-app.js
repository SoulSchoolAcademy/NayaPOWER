/* =========================================================
   MAXIS APP GLUE — history, score count-up, CTA config.
   The assessment engine (maxis-engine.js) is untouched;
   this layer only observes and extends.
   ========================================================= */

/* ---------- Configurable destinations ----------
   enterNayanetUrl: where "Enter NayaNET" goes.
   orderUrl:       where "Order Naya Power" goes.
                   Leave "" until a real checkout exists —
                   the button then shows "Coming soon".   */
window.MAXIS_CONFIG = Object.assign({
  enterNayanetUrl: "../app/index.html",
  orderUrl: ""
}, window.MAXIS_CONFIG || {});

/* ---------- History (internal app) ---------- */
const MaxisHistory = (() => {
  const KEY = "maxis_history_v1";
  const load = () => {
    try { return JSON.parse(localStorage.getItem(KEY) || "[]"); }
    catch (e) { return []; }
  };
  const persist = (rows) => {
    try { localStorage.setItem(KEY, JSON.stringify(rows.slice(0, 24))); } catch (e) {}
  };
  function save(entry) {
    const rows = load();
    rows.unshift(Object.assign({ id: "r" + Date.now(), at: new Date().toISOString() }, entry));
    persist(rows);
    render();
  }
  function remove(id) {
    persist(load().filter(r => r.id !== id));
    render();
  }
  function render() {
    const strip = document.getElementById("historyStrip");
    const list = document.getElementById("historyList");
    if (!strip || !list) return;
    const rows = load();
    if (!rows.length) { strip.style.display = "none"; return; }
    strip.style.display = "block";
    list.innerHTML = "";
    rows.forEach(r => {
      const d = new Date(r.at);
      const when = d.toLocaleDateString(undefined, { month: "short", day: "numeric" }) +
        " " + d.toLocaleTimeString(undefined, { hour: "numeric", minute: "2-digit" });
      const row = document.createElement("div");
      row.className = "history-row";
      row.innerHTML =
        '<div class="history-score" style="color:' + r.bandColor + '">' + Math.round(r.overall) + "</div>" +
        '<div class="history-meta"><b>' + escapeHtml(r.bankTitle) + " · " + escapeHtml(r.bandLabel) + "</b>" +
        "<span>" + escapeHtml(when) + "</span></div>" +
        '<button class="history-del" type="button" aria-label="Delete this result">×</button>';
      row.querySelector(".history-del").addEventListener("click", (e) => {
        e.stopPropagation(); remove(r.id);
      });
      list.appendChild(row);
    });
  }
  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, c =>
      ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
  }
  return { load, save, remove, render };
})();

/* ---------- Score count-up + history capture ----------
   Watches for the results view; animates the orb number
   and stores the completed run. Engine untouched. */
(() => {
  let captured = null;
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function onResultsVisible() {
    const num = document.getElementById("overallScore");
    const view = document.getElementById("resultsView");
    if (!num || !view) return;
    const target = Math.round(parseFloat(num.textContent) || 0);

    // Count-up the orb number
    if (!reduce && target > 0) {
      const t0 = performance.now(), dur = 1500;
      (function tick(t) {
        const p = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - p, 3);
        num.textContent = Math.round(target * e);
        if (p < 1) requestAnimationFrame(tick);
      })(t0);
    }

    // Capture history once per completion
    const stamp = view.dataset.captureStamp;
    const now = target + "|" + (document.getElementById("resultLevelText") || {}).textContent;
    if (captured !== now && target > 0) {
      captured = now;
      const bank = window.MAXIS_BANK || {};
      const lvl = document.getElementById("resultLevelText");
      const dot = document.querySelector("#resultLevel .result-level-dot");
      MaxisHistory.save({
        bankId: bank.id || "maxis",
        bankTitle: bank.title || "Assessment",
        overall: target,
        bandLabel: (lvl ? lvl.textContent.split("·")[0].trim() : ""),
        bandColor: bank.scoreBands ? "" : ""
      });
      // band color from the level dot's computed style is unreliable;
      // re-derive from the bank via the stored rows is skipped — color set below.
      void stamp;
    }
  }

  // Fix band color on the saved row: read it from the visible level badge.
  const origSave = MaxisHistory.save;
  MaxisHistory.save = function (entry) {
    const stage = document.getElementById("scoreStage");
    if (stage) {
      const c = stage.style.getPropertyValue("--scoreColor").trim();
      if (c) entry.bandColor = c;
    }
    if (!entry.bandColor) entry.bandColor = "#b895ff";
    origSave(entry);
  };

  const view = document.getElementById("resultsView");
  if (view) {
    new MutationObserver(() => {
      if (view.classList.contains("visible")) onResultsVisible();
    }).observe(view, { attributes: true, attributeFilter: ["class"] });
    if (view.classList.contains("visible")) onResultsVisible();
  }
  document.addEventListener("DOMContentLoaded", () => MaxisHistory.render());
  if (document.readyState !== "loading") MaxisHistory.render();
})();

/* ---------- Public-page CTAs ---------- */
(() => {
  // "Order Naya Power" shows "Coming soon" until MAXIS_CONFIG.orderUrl
  // is set to a real checkout. The engine's openFreeTrial() no-ops
  // without it — never a fake checkout.
  function wire() {
    const cfg = window.MAXIS_CONFIG || {};
    const order = document.getElementById("freeTrialButton");
    if (order && !cfg.orderUrl) {
      order.setAttribute("aria-disabled", "true");
      const tag = order.querySelector(".cta-tag");
      if (tag) tag.textContent = " · Coming soon";
    }
  }
  document.addEventListener("DOMContentLoaded", wire);
  if (document.readyState !== "loading") wire();
})();

/* ---------- Result action buttons ---------- */
(() => {
  function wire() {
    const pdf = document.getElementById("pdfButton");
    // restartButton is wired by the engine (resetAssessment).
    if (pdf) pdf.addEventListener("click", () => window.print());
  }
  document.addEventListener("DOMContentLoaded", wire);
  if (document.readyState !== "loading") wire();
})();
