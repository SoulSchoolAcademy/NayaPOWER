/* ============================================================================
   SMART BAR — two-bar navigation component (Smart Bar standard, Shawn
   2026-10-28). ONE self-contained file: vanilla JS, injects its own CSS,
   zero dependencies, no build step. Drop into any page with a <script> tag
   AFTER setting the two config objects:

     window.SMARTBAR_TOP    = [{id, label, tabKey?, target?}, ...]
        The host app's organization. tabKey: the key the host's own tab
        function expects (on the PI face: window.showTab(key)). target: a
        CSS selector used with scrollIntoView when no tabKey/showTab path
        exists. The top bar is NOT user-editable by law — this file gives
        it no edit, remove, reorder, heart, or star control. None.

     window.SMARTBAR_BOTTOM = [{id, label, url}, ...]
        The whole network. url may be null: the tab then says so on tap
        ("No destination yet — never a dead link") instead of navigating.
        Editable by law: every tab carries a ⋯ menu (Edit / Set Purple
        Heart 💜 / Set Gold Star ⭐ / Remove) plus a ＋ Add control.
        Hearts sort first, then stars, then the rest (stable). State
        persists on the device under localStorage key "naya.smarttabs.v1",
        shared across pages; once a saved state exists it wins over the
        seed config on later loads.

   SETTLED RULES IMPLEMENTED (see verification.md for the rule→code map):
   top bar at the very top, bottom bar at the very bottom, both fixed;
   top drifts slowly RIGHT, bottom drifts slowly LEFT; bars load AT REST
   (no drift for the first ~5s); drift pauses on touch/hover/focus/wheel
   and resumes after ~6s idle; drift fully disabled under
   prefers-reduced-motion; dark pills, bold labels, white light at rest,
   each tab ignites in its OWN spectrum color by position (purple, blue,
   green, gold, orange, red, magenta, cycling) with lift + glow; edge
   fades; hidden scrollbars; the bars are navigation chrome only — they
   reserve space via body padding and never restyle page content.

   CANDIDATE, NOT SETTLED: drift speed. The standard says "slowly"
   (qualitative). This file picks ONE FULL TRAVERSE IN ~90 SECONDS
   (inside the 60–120s candidate band) — a chosen candidate value, to be
   replaced the day a speed is settled. Drift pattern is one-way wrap.
   ========================================================================== */
(function () {
  "use strict";

  /* ---------- constants ---------- */
  var STORAGE_KEY = "naya.smarttabs.v1"; // settled persistence key (bottom bar)
  var SPECTRUM = ["#a06bff", "#3fb8ff", "#2fe89e", "#ffbf3d", "#ff9a5a", "#ff5e6c", "#e84fff"];
  // spectrum by position: purple, blue, green, gold, orange, red, magenta, cycling
  var REST_MS = 5000;          // bars load at rest: no drift for the first ~5s
  var RESUME_MS = 6000;        // drift resumes ~6s after the last interaction
  var TRAVERSE_SECONDS = 90;   // CANDIDATE speed: one full traverse in ~90s (band 60–120s)
  var BAR_H = 52;              // px, matches the CSS bar height below

  if (document.getElementById("smartbar-top")) return; // never mount twice

  var reduceMotion = window.matchMedia &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- CSS (injected; the component owns no other styles) ---------- */
  var CSS = [
    ".smartbar{position:fixed;left:0;right:0;height:" + BAR_H + "px;z-index:99990;",
    "background:rgba(2,2,3,.92);backdrop-filter:blur(6px);display:flex;align-items:center;",
    "overflow:hidden;font-family:system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;",
    "-webkit-mask-image:linear-gradient(to right,transparent 0,#000 28px,#000 calc(100% - 28px),transparent 100%);",
    "mask-image:linear-gradient(to right,transparent 0,#000 28px,#000 calc(100% - 28px),transparent 100%)}",
    "#smartbar-top{top:0;border-bottom:1px solid rgba(255,255,255,.14)}",
    "#smartbar-bottom{bottom:0;border-top:1px solid rgba(255,255,255,.14)}",
    ".smartbar .sb-track{display:flex;align-items:center;gap:10px;padding:0 14px;",
    "white-space:nowrap;will-change:transform;scrollbar-width:none}",
    ".smartbar .sb-track::-webkit-scrollbar{display:none}",
    ".smartbar .sb-set{display:flex;align-items:center;gap:10px}",
    ".sb-pill{display:inline-flex;align-items:center;gap:6px;border:1px solid rgba(255,255,255,.22);",
    "background:#0b0b10;color:#fff;font-weight:700;font-size:15px;line-height:1;",
    "padding:9px 14px;border-radius:999px;cursor:pointer;--tc:#fff;",
    "box-shadow:0 0 6px rgba(255,255,255,.35),inset 0 0 4px rgba(255,255,255,.25);",
    "transition:transform .18s ease,box-shadow .18s ease,border-color .18s ease,color .18s ease}",
    ".sb-pill:hover,.sb-pill:focus-visible{color:var(--tc);border-color:var(--tc);outline:none;",
    "transform:translateY(-3px);",
    "box-shadow:0 0 14px var(--tc),inset 0 0 8px var(--tc),0 6px 14px rgba(0,0,0,.5);",
    "text-shadow:0 0 8px var(--tc)}",
    ".sb-pill[aria-current='true']{border-color:var(--tc);color:var(--tc)}",
    ".sb-more{border:1px solid rgba(255,255,255,.22);background:#0b0b10;color:#fff;",
    "border-radius:999px;width:26px;height:26px;font-size:15px;line-height:1;cursor:pointer;padding:0}",
    ".sb-more:hover,.sb-more:focus-visible{color:#3fb8ff;border-color:#3fb8ff;outline:none}",
    ".sb-flag{font-size:13px}",
    /* menu + editor + toast */
    ".sb-menu{position:fixed;z-index:99999;background:#0b0b10;border:1px solid rgba(255,255,255,.3);",
    "border-radius:12px;padding:6px;min-width:210px;box-shadow:0 10px 30px rgba(0,0,0,.6)}",
    ".sb-menu button{display:block;width:100%;text-align:left;background:none;border:0;color:#fff;",
    "font-size:15px;font-weight:600;padding:9px 10px;border-radius:8px;cursor:pointer}",
    ".sb-menu button:hover,.sb-menu button:focus-visible{background:rgba(255,255,255,.12);outline:none}",
    ".sb-editor{position:fixed;z-index:99999;left:50%;transform:translateX(-50%);bottom:" + (BAR_H + 12) + "px;",
    "background:#0b0b10;border:1px solid rgba(255,255,255,.3);border-radius:12px;padding:14px;",
    "box-shadow:0 10px 30px rgba(0,0,0,.6);color:#fff;min-width:min(420px,92vw)}",
    ".sb-editor label{display:block;font-size:13px;font-weight:700;margin:8px 0 4px}",
    ".sb-editor input{width:100%;box-sizing:border-box;background:#020203;color:#fff;",
    "border:1px solid rgba(255,255,255,.35);border-radius:8px;padding:9px 10px;font-size:15px}",
    ".sb-editor .sb-row{display:flex;gap:8px;margin-top:12px;justify-content:flex-end}",
    ".sb-editor .sb-row button{border:1px solid rgba(255,255,255,.35);background:#16161d;color:#fff;",
    "border-radius:8px;padding:8px 14px;font-size:14px;font-weight:700;cursor:pointer}",
    ".sb-toast{position:fixed;z-index:99999;left:50%;transform:translateX(-50%);bottom:" + (BAR_H + 12) + "px;",
    "background:#0b0b10;color:#fff;border:1px solid #ffbf3d;border-radius:999px;",
    "padding:9px 16px;font-size:14px;font-weight:700;box-shadow:0 8px 24px rgba(0,0,0,.6)}",
    "@media (prefers-reduced-motion: reduce){.sb-pill{transition:none}}"
  ].join("");

  var style = document.createElement("style");
  style.id = "smartbar-style";
  style.textContent = CSS;
  document.head.appendChild(style);

  /* ---------- helpers ---------- */
  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  function spectrum(i) { return SPECTRUM[i % SPECTRUM.length]; }

  var toastTimer = null;
  function toast(msg) {
    closePopups();
    var t = document.createElement("div");
    t.className = "sb-toast";
    t.setAttribute("role", "status");
    t.textContent = msg;
    document.body.appendChild(t);
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { t.remove(); }, 2600);
  }

  function closePopups() {
    var m = document.querySelector(".sb-menu"); if (m) m.remove();
    var e = document.querySelector(".sb-editor"); if (e) e.remove();
  }
  document.addEventListener("keydown", function (ev) {
    if (ev.key === "Escape") closePopups();
  });
  document.addEventListener("pointerdown", function (ev) {
    var m = document.querySelector(".sb-menu");
    if (m && !m.contains(ev.target) && !ev.target.classList.contains("sb-more")) m.remove();
  });

  /* ======================================================================
     DRIFT — one mechanism for both bars. offset is the single source of
     truth; drift moves it each frame while active, drag/wheel move it by
     hand. Direction: +1 drifts LEFT (bottom bar), -1 drifts RIGHT (top).
     ====================================================================== */
  function makeDrift(track, direction) {
    var offset = 0, setWidth = 0, holdUntil = 0, last = null;
    var born = performance.now();

    function measure() {
      var set = track.querySelector(".sb-set");
      setWidth = set ? set.offsetWidth + 10 : 0; // + gap
    }
    function frame(now) {
      if (last == null) last = now;
      var dt = Math.min(100, now - last); last = now;
      var active = !reduceMotion && setWidth > 0 &&
        now - born > REST_MS && now > holdUntil && !document.hidden;
      if (active) offset += direction * (setWidth / (TRAVERSE_SECONDS * 1000)) * dt;
      var shift = setWidth > 0 ? ((offset % setWidth) + setWidth) % setWidth : 0;
      track.style.transform = "translateX(" + (-shift) + "px)";
      requestAnimationFrame(frame);
    }
    function poke() { holdUntil = performance.now() + RESUME_MS; }

    ["pointerenter", "pointerdown", "focusin", "touchstart", "wheel"].forEach(function (name) {
      track.parentElement.addEventListener(name, poke, { passive: true });
    });
    /* drag / wheel scroll the running bar by hand (offset is the truth) */
    var dragX = null, dragOffset = 0;
    track.parentElement.addEventListener("pointerdown", function (ev) {
      dragX = ev.clientX; dragOffset = offset;
    });
    window.addEventListener("pointermove", function (ev) {
      if (dragX == null) return;
      offset = dragOffset - (ev.clientX - dragX);
      poke();
    });
    window.addEventListener("pointerup", function () { dragX = null; });
    track.parentElement.addEventListener("wheel", function (ev) {
      offset += (Math.abs(ev.deltaX) > Math.abs(ev.deltaY) ? ev.deltaX : ev.deltaY);
      poke();
    }, { passive: true });

    measure();
    window.addEventListener("resize", measure);
    requestAnimationFrame(frame);
    return { remeasure: measure };
  }

  function buildTrack(bar, pillsHTML) {
    // two copies of the set => seamless wrap at one set width
    var track = document.createElement("div");
    track.className = "sb-track";
    track.innerHTML = '<div class="sb-set">' + pillsHTML + '</div>' +
                      '<div class="sb-set" aria-hidden="true">' + pillsHTML + "</div>";
    bar.appendChild(track);
    return track;
  }

  /* ======================================================================
     TOP BAR — the host app's organization. NOT editable: this function
     creates no ⋯ menu, no Add, no remove, no reorder control. None, by law.
     ====================================================================== */
  function renderTop() {
    var cfg = Array.isArray(window.SMARTBAR_TOP) ? window.SMARTBAR_TOP : [];
    var bar = document.createElement("nav");
    bar.className = "smartbar";
    bar.id = "smartbar-top";
    bar.setAttribute("aria-label", "This app — sections");
    var html = cfg.map(function (tab, i) {
      return '<button type="button" class="sb-pill" data-sb-top="' + i + '"' +
        ' style="--tc:' + spectrum(i) + '">' + esc(tab.label) + "</button>";
    }).join("");
    var track = buildTrack(bar, html);
    document.body.appendChild(bar);

    bar.addEventListener("click", function (ev) {
      var btn = ev.target.closest("[data-sb-top]");
      if (!btn) return;
      var tab = cfg[Number(btn.getAttribute("data-sb-top"))];
      if (!tab) return;
      bar.querySelectorAll(".sb-pill").forEach(function (p) { p.removeAttribute("aria-current"); });
      btn.setAttribute("aria-current", "true");
      // Pull into the section: the host's own tab function wins when present.
      if (tab.tabKey && typeof window.showTab === "function") {
        window.showTab(tab.tabKey);
      } else if (tab.target) {
        var el = document.querySelector(tab.target);
        if (el && el.scrollIntoView) el.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth" });
      }
    });
    return makeDrift(track, -1); // top drifts RIGHT
  }

  /* ======================================================================
     BOTTOM BAR — the whole network. Editable by law: ⋯ menu + Add,
     hearts first then stars, persisted under naya.smarttabs.v1.
     ====================================================================== */
  var bottomState = null; // {tabs:[{id,label,url,heart,star}], }

  function loadBottom() {
    var seed = (Array.isArray(window.SMARTBAR_BOTTOM) ? window.SMARTBAR_BOTTOM : [])
      .map(function (t) {
        return { id: String(t.id), label: String(t.label), url: t.url ? String(t.url) : null, heart: false, star: false };
      });
    try {
      var raw = window.localStorage.getItem(STORAGE_KEY);
      if (raw) {
        var saved = JSON.parse(raw);
        if (saved && Array.isArray(saved.tabs) && saved.tabs.length) {
          bottomState = { tabs: saved.tabs };
          return;
        }
      }
    } catch (e) { /* storage unavailable: run on the seed, save nothing */ }
    bottomState = { tabs: seed };
  }
  function saveBottom() {
    try { window.localStorage.setItem(STORAGE_KEY, JSON.stringify(bottomState)); } catch (e) { /* see loadBottom */ }
  }
  function sortedTabs() {
    // hearts first, then stars, then the rest — stable inside each class
    return bottomState.tabs
      .map(function (t, i) { return { t: t, i: i }; })
      .sort(function (a, b) {
        var ra = a.t.heart ? 0 : (a.t.star ? 1 : 2);
        var rb = b.t.heart ? 0 : (b.t.star ? 1 : 2);
        return ra - rb || a.i - b.i;
      })
      .map(function (x) { return x.t; });
  }

  var bottomBar = null, bottomDrift = null;
  function renderBottom() {
    if (bottomBar) bottomBar.remove();
    bottomBar = document.createElement("nav");
    bottomBar.className = "smartbar";
    bottomBar.id = "smartbar-bottom";
    bottomBar.setAttribute("aria-label", "The whole network — apps");
    var tabs = sortedTabs();
    var html = tabs.map(function (tab, i) {
      var flags = (tab.heart ? ' <span class="sb-flag" aria-label="purple heart">💜</span>' : "") +
                  (tab.star ? ' <span class="sb-flag" aria-label="gold star">⭐</span>' : "");
      return '<span style="display:inline-flex;align-items:center;gap:4px">' +
        '<button type="button" class="sb-pill" data-sb-tab="' + esc(tab.id) + '"' +
        ' style="--tc:' + spectrum(i) + '">' + esc(tab.label) + flags + "</button>" +
        '<button type="button" class="sb-more" data-sb-more="' + esc(tab.id) + '"' +
        ' aria-label="Edit tab ' + esc(tab.label) + '">⋯</button></span>';
    }).join("") +
      '<button type="button" class="sb-pill" data-sb-add="1" style="--tc:#2fe89e">＋ Add</button>';
    var track = buildTrack(bottomBar, html);
    document.body.appendChild(bottomBar);
    bottomDrift = makeDrift(track, +1); // bottom drifts LEFT

    bottomBar.onclick = function (ev) {
      var more = ev.target.closest("[data-sb-more]");
      if (more) { openMenu(more.getAttribute("data-sb-more"), more); return; }
      if (ev.target.closest("[data-sb-add]")) { openEditor(null); return; }
      var pill = ev.target.closest("[data-sb-tab]");
      if (!pill) return;
      var tab = bottomState.tabs.filter(function (t) { return t.id === pill.getAttribute("data-sb-tab"); })[0];
      if (!tab) return;
      if (tab.url) { window.location.href = tab.url; }
      else { toast("No destination yet — never a dead link"); }
    };
  }

  function openMenu(tabId, anchor) {
    closePopups();
    var tab = bottomState.tabs.filter(function (t) { return t.id === tabId; })[0];
    if (!tab) return;
    var menu = document.createElement("div");
    menu.className = "sb-menu";
    menu.setAttribute("role", "menu");
    menu.innerHTML =
      '<button type="button" role="menuitem" data-act="edit">Edit</button>' +
      '<button type="button" role="menuitem" data-act="heart">Set Purple Heart 💜</button>' +
      '<button type="button" role="menuitem" data-act="star">Set Gold Star ⭐</button>' +
      '<button type="button" role="menuitem" data-act="remove">Remove</button>';
    document.body.appendChild(menu);
    var r = anchor.getBoundingClientRect();
    menu.style.left = Math.max(8, Math.min(r.left, window.innerWidth - 230)) + "px";
    menu.style.bottom = (window.innerHeight - r.top + 8) + "px"; // opens upward, above the bottom bar
    menu.addEventListener("click", function (ev) {
      var btn = ev.target.closest("[data-act]");
      if (!btn) return;
      var act = btn.getAttribute("data-act");
      closePopups();
      if (act === "edit") { openEditor(tab); return; }
      if (act === "heart") { tab.heart = !tab.heart; }
      if (act === "star") { tab.star = !tab.star; }
      if (act === "remove") {
        bottomState.tabs = bottomState.tabs.filter(function (t) { return t.id !== tab.id; });
      }
      saveBottom();
      renderBottom();
    });
  }

  function openEditor(tab) {
    closePopups();
    var isNew = !tab;
    var ed = document.createElement("div");
    ed.className = "sb-editor";
    ed.setAttribute("role", "dialog");
    ed.setAttribute("aria-label", isNew ? "Add a smart tab" : "Edit smart tab");
    ed.innerHTML =
      "<strong>" + (isNew ? "Add a smart tab" : "Edit smart tab") + "</strong>" +
      '<label for="sb-ed-label">Name</label>' +
      '<input id="sb-ed-label" type="text" value="' + (isNew ? "" : esc(tab.label)) + '">' +
      '<label for="sb-ed-url">URL (any website — saved as a smart tab)</label>' +
      '<input id="sb-ed-url" type="url" placeholder="https://…" value="' + (isNew ? "" : esc(tab.url || "")) + '">' +
      '<div class="sb-row"><button type="button" data-ed="cancel">Cancel</button>' +
      '<button type="button" data-ed="save">Save</button></div>';
    document.body.appendChild(ed);
    var labelIn = ed.querySelector("#sb-ed-label");
    var urlIn = ed.querySelector("#sb-ed-url");
    labelIn.focus();
    ed.addEventListener("click", function (ev) {
      var btn = ev.target.closest("[data-ed]");
      if (!btn) return;
      if (btn.getAttribute("data-ed") === "cancel") { closePopups(); return; }
      var label = labelIn.value.trim();
      if (!label) { toast("A tab needs a name"); return; }
      var url = urlIn.value.trim() || null;
      if (isNew) {
        bottomState.tabs.push({ id: "custom-" + Date.now(), label: label, url: url, heart: false, star: false });
      } else {
        tab.label = label; tab.url = url;
      }
      saveBottom();
      closePopups();
      renderBottom();
    });
  }

  /* ---------- reserve space: chrome only, content is never restyled ------ */
  function reserveSpace() {
    var cs = window.getComputedStyle(document.body);
    var pt = parseFloat(cs.paddingTop) || 0;
    var pb = parseFloat(cs.paddingBottom) || 0;
    document.body.style.paddingTop = (pt + BAR_H) + "px";
    document.body.style.paddingBottom = (pb + BAR_H) + "px";
  }

  /* ---------- mount ---------- */
  function mount() {
    loadBottom();
    renderTop();
    renderBottom();
    reserveSpace();
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", mount);
  } else {
    mount();
  }
})();
