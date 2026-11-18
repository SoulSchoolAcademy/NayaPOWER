#!/usr/bin/env python3
"""Pricing F4-FIX (2026-11-17): make the free walk finish.

ROOT CAUSE (proven, not guessed — see MAKER-REPORT.md):
  The backend POST /api/welcome/complete works live (200, reveal pages,
  ~0.9s, re-proven this round). The stall is CLIENT-SIDE, in the walk:
  (a) the naming Enter calls showStep(14) — the NAMES step itself — so the
      click changes nothing visible (silent Enter); completeWalk() then runs
      in the background and showBuildDone()/showBuildError() unhide panels
      inside #step-building, which is still hidden — so success AND failure
      are both invisible;
  (b) on reload, boot() sees the saved S.reveal and calls showStep(15) —
      the BUILDING step with #buildWorking visible and #buildDone hidden —
      so the citizen sits on "Building it — wait a minute…" FOREVER, with
      the reveal already saved. That is the eye's ~6-minute stall, exactly.
  (c) api() has no timeout: a hanging POST hangs forever.
  (d) "See your pages" calls showStep(15) (building again) not showStep(16)
      (the end slide) — it would loop even after a good build.
  The eye's GET /api/welcome/me -> {"ok":false,"error":"unknown api"} is a
  red herring with a real edge: the endpoint exists but is POST-only, and
  the walk never calls it. W1 adds the GET branch anyway, so the endpoint
  answers as probed.

FIXES (free copy ONLY — the source walk walk-beginning-fixed.html carries
the same four bugs; fixing the live walk source is a walk-round follow-on,
NOT this round — this script touches only the free worker):
  F1 CSS: build progress bar + busy-Enter + error message styles.
  F2 HTML: progress bar + live status line in #buildWorking; error message
     line + "Back to your names" button in #buildError.
  F3 api(): 25 s AbortController timeout -> {ok:false, timedOut:true}.
  F4 completeWalk(): in-flight guard; starts visible progress; stops it on
     done/error; loud error with the reason.
  F5 showBuildDone/showBuildError(): stop progress, reset the naming Enter.
  F6 naming Enter: immediate pressed feedback (disabled + "Building…"),
     then showStep(15) (the BUILDING step, visible) + completeWalk().
  F7 "See your pages" -> showStep(16) (the end slide, five doors);
     "Back to your names" -> showStep(14).
  F8 boot resume with a saved reveal -> the end slide directly (doors),
     never the building screen.
  W1 worker: GET /api/welcome/me (alias from query) mirrors the POST read.

Builds entirely in memory (EPERM flake blocks big disk writes) and stages
to naya-pricing-free-staging ONLY. The pricing worker is NOT touched.
"""
import hashlib
import importlib.util
import json
import os
import random
import string
import sys

sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
sys.path.insert(0, os.path.expanduser("~/workspace/ninaya/integration"))

F4 = os.path.expanduser("~/workspace/team-nitro/pricing-free-entry-20261116")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_bf = load("bfree", os.path.join(F4, "build-free-staging-worker.py"))
_sim = load("sim", os.path.join(F4, "stage-in-memory.py"))
replace_once = _bf.replace_once

FREE_HOST = "https://naya-pricing-free-staging.nayapower.workers.dev"


def sha(b):
    return hashlib.sha256(b if isinstance(b, bytes) else b.encode()).hexdigest()


# ---------------------------------------------------------------- F1: CSS
FIX_CSS = (
    "/* FREE-WALK FIX (F4-FIX 2026-11-17): visible build progress, pressed "
    "Enter, loud build error. Green = free/positive, the Enter-free colour. */\n    "
    ".p3-buildbar{width:min(320px,80%);height:12px;margin:16px auto 0;"
    "border-radius:999px;background:#0a0a10;border:1.5px solid "
    "rgba(255,255,255,.9);box-shadow:inset 0 1px 0 rgba(255,255,255,.15),"
    "0 4px 12px rgba(0,0,0,.5);overflow:hidden}\n    "
    ".p3-buildbar span{display:block;height:100%;width:8%;border-radius:999px;"
    "background:linear-gradient(135deg,#2fe89e,#0e9f6e);"
    "transition:width .6s ease}\n    "
    ".p3-enter.is-busy{opacity:.75;pointer-events:none}\n    "
    "#buildStatus{margin-top:12px}\n    "
    "#buildErrorMsg{margin-top:8px}\n    "
)


def apply_walk_fixes(w):
    # F1: CSS before the first </style>.
    assert w.count("</style>") >= 1
    w = w.replace("</style>", FIX_CSS + "</style>", 1)
    assert "p3-buildbar" in w

    # F2a: progress bar + live status line in #buildWorking.
    w = replace_once(
        w,
        '<p class="p3-note">Your answers are going into your Smart Box, and your pages are being built from your own words.</p>\n</div>',
        '<p class="p3-note">Your answers are going into your Smart Box, and your pages are being built from your own words.</p>\n'
        '<div class="p3-buildbar" aria-hidden="true"><span id="buildBarFill"></span></div>\n'
        '<p class="p3-note" id="buildStatus">Saving your answers&hellip;</p>\n</div>',
        "F2a build progress")
    # F2b: error message line + way back in #buildError.
    w = replace_once(
        w,
        '<p class="p3-note">Your answers are saved here. Try once more.</p>\n<button class="p3-enter" id="buildRetry" type="button">Try again</button>',
        '<p class="p3-note">Your answers are saved here. Try once more.</p>\n'
        '<p class="p3-note" id="buildErrorMsg" hidden></p>\n'
        '<button class="p3-enter" id="buildRetry" type="button">Try again</button>\n'
        '<button class="p3-enter" id="buildBack" type="button">Back to your names</button>',
        "F2b build error")

    # F3: api() with a 25 s timeout — a hanging POST must fail, never hang.
    w = replace_once(
        w,
        "async function api(path, body){ var r; try { r = await fetch(path, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) }); } catch(e){ return { ok: false, d: {} }; } var d = {}; try { d = await r.json(); } catch(e){} return { ok: r.ok, d: d }; }",
        "async function api(path, body){ var r; var ctrl = (typeof AbortController !== 'undefined') ? new AbortController() : null; var to = null; try { if (ctrl) to = setTimeout(function(){ ctrl.abort(); }, 25000); r = await fetch(path, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body), signal: ctrl ? ctrl.signal : undefined }); } catch(e){ if (to) clearTimeout(to); return { ok: false, d: {}, timedOut: (e && e.name === 'AbortError') }; } if (to) clearTimeout(to); var d = {}; try { d = await r.json(); } catch(e){} return { ok: r.ok, d: d }; }",
        "F3 api timeout")

    # F4: progress helpers + completeWalk with guard, progress, loud error.
    w = replace_once(
        w,
        "async function completeWalk(){\n"
        "  var payload = cred({ answers: S.answers, topics: S.topics, pageNames: S.pageNames });\n"
        "  window.__lastCompletionPayload = payload;\n"
        "  var r = await api('/api/welcome/complete', payload);\n"
        "  if (!r.ok || !r.d || !r.d.pages) { showBuildError(); return; }\n"
        "  S.reveal = r.d;\n"
        "  save();\n"
        "  renderEnd();\n"
        "  showBuildDone();\n"
        "}",
        "/* FREE-WALK FIX (F4-FIX): visible progress while the build runs, a "
        "25 s timeout, and a loud error with a way back — never a silent hang. */\n"
        "var buildTimer = null, buildPct = 8;\n"
        "var BUILD_STAGES = ['Saving your answers\\u2026', 'Building your pages from your own words\\u2026', 'Wiring up your Hub, Dashboard and pages\\u2026', 'Almost there \\u2014 putting the doors on\\u2026'];\n"
        "function buildProgressStart(){ buildProgressStop(false); var bar = document.getElementById('buildBarFill'); var st = document.getElementById('buildStatus'); var i = 0; buildPct = 8; if (bar) bar.style.width = '8%'; if (st) st.textContent = BUILD_STAGES[0]; buildTimer = setInterval(function(){ i = (i + 1) % BUILD_STAGES.length; if (st) st.textContent = BUILD_STAGES[i]; buildPct = Math.min(92, buildPct + 14); if (bar) bar.style.width = buildPct + '%'; }, 2500); }\n"
        "function buildProgressStop(done){ if (buildTimer) { clearInterval(buildTimer); buildTimer = null; } var bar = document.getElementById('buildBarFill'); var st = document.getElementById('buildStatus'); if (bar) bar.style.width = done ? '100%' : '8%'; }\n"
        "function resetNamesEnter(){ var b = NAMESSEC.querySelector('#enterBtn-14'); if (b) { b.disabled = false; b.classList.remove('is-busy'); b.textContent = 'Enter'; } }\n"
        "async function completeWalk(){\n"
        "  if (completeWalk._busy) return;\n"
        "  completeWalk._busy = true;\n"
        "  buildProgressStart();\n"
        "  var payload = cred({ answers: S.answers, topics: S.topics, pageNames: S.pageNames });\n"
        "  window.__lastCompletionPayload = payload;\n"
        "  var r = await api('/api/welcome/complete', payload);\n"
        "  if (!r.ok || !r.d || !r.d.pages) { completeWalk._busy = false; showBuildError(r && r.timedOut ? 'The build timed out after 25 seconds \\u2014 the server did not answer. Your answers are saved here. Try once more, or go back to your names.' : 'The build did not answer. Your answers are saved here. Try once more, or go back to your names.'); return; }\n"
        "  S.reveal = r.d;\n"
        "  save();\n"
        "  renderEnd();\n"
        "  completeWalk._busy = false;\n"
        "  showBuildDone();\n"
        "}",
        "F4 completeWalk")

    # F5: showBuildDone / showBuildError stop progress, reset Enter, say why.
    w = replace_once(
        w,
        "function showBuildDone(){\n"
        "  var w = document.getElementById('buildWorking'); if (w) w.hidden = true;\n"
        "  var e = document.getElementById('buildError'); if (e) e.hidden = true;\n"
        "  var d = document.getElementById('buildDone'); if (d) d.hidden = false;\n"
        "}\n"
        "function showBuildError(){\n"
        "  var w = document.getElementById('buildWorking'); if (w) w.hidden = true;\n"
        "  var d = document.getElementById('buildDone'); if (d) d.hidden = true;\n"
        "  var e = document.getElementById('buildError'); if (e) e.hidden = false;\n"
        "}",
        "function showBuildDone(){\n"
        "  buildProgressStop(true); resetNamesEnter();\n"
        "  var w = document.getElementById('buildWorking'); if (w) w.hidden = true;\n"
        "  var e = document.getElementById('buildError'); if (e) e.hidden = true;\n"
        "  var d = document.getElementById('buildDone'); if (d) d.hidden = false;\n"
        "}\n"
        "function showBuildError(reason){\n"
        "  buildProgressStop(false); resetNamesEnter();\n"
        "  var w = document.getElementById('buildWorking'); if (w) w.hidden = true;\n"
        "  var d = document.getElementById('buildDone'); if (d) d.hidden = true;\n"
        "  var e = document.getElementById('buildError'); if (e) e.hidden = false;\n"
        "  var m = document.getElementById('buildErrorMsg'); if (m) { m.textContent = reason || 'The build did not answer. Your answers are saved here. Try once more, or go back to your names.'; m.hidden = false; }\n"
        "}",
        "F5 build done/error")

    # F6: naming Enter — immediate pressed feedback, then the BUILDING step.
    w = replace_once(
        w,
        "  enterBtn.addEventListener('click', function(){\n"
        "    refresh(); save();\n"
        "    if (!bIn.value.trim() || !sIn.value.trim()) showNote('Tip: name your business and space — or leave them and we\\'ll set sensible defaults.');\n"
        "    setTimeout(function(){ showStep(14); completeWalk(); }, 350);\n"
        "  });",
        "  enterBtn.addEventListener('click', function(){\n"
        "    if (enterBtn.disabled) return;\n"
        "    refresh(); save();\n"
        "    if (!bIn.value.trim() || !sIn.value.trim()) showNote('Tip: name your business and space — or leave them and we\\'ll set sensible defaults.');\n"
        "    enterBtn.disabled = true; enterBtn.classList.add('is-busy'); enterBtn.textContent = 'Building\\u2026';\n"
        "    setTimeout(function(){ showStep(15); completeWalk(); }, 150);\n"
        "  });",
        "F6 naming Enter")

    # F7: "See your pages" goes to the END slide (16), not building (15);
    # "Back to your names" is the way back from a failed build.
    w = replace_once(
        w,
        "  if (go) go.addEventListener('click', function(){ showStep(15); });",
        "  if (go) go.addEventListener('click', function(){ showStep(16); });",
        "F7a see your pages")
    w = replace_once(
        w,
        "    var w = document.getElementById('buildWorking'); if (w) w.hidden = false;\n"
        "    completeWalk();\n"
        "  });",
        "    var w = document.getElementById('buildWorking'); if (w) w.hidden = false;\n"
        "    completeWalk();\n"
        "  });\n"
        "  var back = document.getElementById('buildBack');\n"
        "  if (back) back.addEventListener('click', function(){ showStep(14); });",
        "F7b back to names")

    # F8: resume with a saved reveal lands on the END slide (five doors),
    # never on the building screen.
    w = replace_once(
        w,
        "  if (S.reveal) { renderEnd(); showStep(15); return; }",
        "  if (S.reveal) { renderEnd(); showStep(16); return; }",
        "F8 boot resume")
    return w


def apply_worker_fix(worker):
    # W1: GET /api/welcome/me mirrors the POST read (alias from the query).
    w = replace_once(
        worker,
        '    // ---- welcome me: name for the walk\'s background verify ----\n'
        '    if (p === "/api/welcome/me" && req.method === "POST") {',
        '    // ---- welcome me: name for the walk\'s background verify (GET + POST) ----\n'
        '    if (p === "/api/welcome/me" && req.method === "GET") {\n'
        '      const alias = cleanAlias(u.searchParams.get("alias"));\n'
        '      if (!alias) return j({ ok: false, error: "alias required" }, 400);\n'
        '      const row = await sbGetRow(alias);\n'
        '      if (!row) return j({ ok: false, error: "unknown alias" }, 404);\n'
        '      return j({ alias: row.alias, name: row.name });\n'
        '    }\n'
        '    if (p === "/api/welcome/me" && req.method === "POST") {',
        "W1 GET welcome/me")
    return w


def main():
    walk_free = apply_walk_fixes(_bf.build_walk_free())
    free_entry = _bf.build_free_entry()
    free_index = _bf.FREE_INDEX.replace(
        "__PRICING_STAGED__", "https://naya-pricing-f4-staging.nayapower.workers.dev/")
    worker = apply_worker_fix(_bf.build_worker(walk_free, free_entry))
    print(f"walk-free fixed: {len(walk_free.encode())} B sha256={sha(walk_free)}")
    print(f"free-entry (unchanged): {len(free_entry.encode())} B sha256={sha(free_entry)}")
    print(f"free worker fixed: {len(worker.encode())} B sha256={sha(worker)}")
    import gzip
    gz = gzip.compress(worker.encode("utf-8"))
    print(f"worker gzip: {len(gz)} B (limit 10,485,760)")
    assert len(gz) < 10485760

    # Old code must be gone from the fixed walk; new markers present.
    for bad in ["setTimeout(function(){ showStep(14); completeWalk(); }, 350);",
                "if (S.reveal) { renderEnd(); showStep(15); return; }",
                "function(){ showStep(15); });"]:
        assert bad not in walk_free, f"old code still present: {bad[:50]}"
    for good in ["buildBarFill", "buildStatus", "buildErrorMsg", "buildBack",
                 "is-busy", "BUILD_STAGES", "25000", "showStep(16)",
                 "The build timed out after 25 seconds",
                 "enterBtn.disabled = true"]:
        assert good in walk_free, f"fix marker missing: {good}"
    assert "showStep(15); completeWalk()" in walk_free
    print("fix markers: HAVE all, old code: GONE all")

    # Node driver: the real fetch handler serves the fixed walk + entry.
    _sim.node_check(worker, FREE_HOST + "/free/walk", sha(walk_free),
                    ["nayanet_free_entry", "data-door=\"Hub\"",
                     "You&rsquo;re in on Naya Free",
                     "buildBarFill", "buildStatus", "buildErrorMsg",
                     "The build timed out after 25 seconds",
                     "showStep(16)"],
                    ["setTimeout(function(){ showStep(14); completeWalk(); }, 350);"])
    _sim.node_check(worker, FREE_HOST + "/free", sha(free_entry),
                    ["Enter free &mdash; no payment, no card.", 'id="freeEye"',
                     "WALKTHROUGH_URL = '/free/walk'"], [])
    _sim.node_check(worker, FREE_HOST + "/", sha(free_index),
                    ["Enter free — the route, staged"], [])
    _sim.node_redirect_check(worker, FREE_HOST + "/free/hub",
                             "https://nayanet.app/")
    print("node driver: PASS (fixed walk + unchanged entry + index + hub)")

    # Stage the fixed free worker (STAGING ONLY — pricing worker untouched).
    kv = [{"type": "kv_namespace", "name": "WELCOME_ASSETS",
           "namespace_id": "1cf80db6183245d19dd5296645a12bd0"}]
    _sim.put_worker("naya-pricing-free-staging", worker.encode(), kv)
    status, raw = _sim.api("GET", "/naya-pricing-free-staging")
    assert status == 200
    _, wb, _ = _sim.split_multipart(raw)
    assert wb == worker.encode(), "read-back differs from PUT — STOP"
    print(f"read-back sha256={sha(wb)} — MATCH")

    # Live HTTP verification of the staged routes.
    for path, want in [("/", free_index), ("/free", free_entry),
                       ("/free/walk", walk_free)]:
        st, _, got = _sim.http_get(FREE_HOST + path)
        assert st == 200, f"GET {path}: {st}"
        assert got.decode("utf-8") == want, f"GET {path}: bytes != source — STOP"
        print(f"GET {FREE_HOST}{path}: 200, {len(got)} B == source MATCH")
    st, hdrs, _ = _sim.http_get(FREE_HOST + "/free/hub")
    assert st in (301, 302) and hdrs.get("Location") == "https://nayanet.app/"
    print("GET /free/hub: 302 -> https://nayanet.app/ MATCH")

    # API: GET /api/welcome/me now answers (was 404 unknown api).
    st, _, out = _sim.http_get(FREE_HOST + "/api/welcome/me?alias=f4captaincheck")
    print(f"GET /api/welcome/me?alias=f4captaincheck: {st} {out[:160].decode()}")
    assert st == 200, "GET /api/welcome/me still failing — STOP"
    # API: POST complete with a fresh test alias, then read-back + redirect.
    alias = "f4fix" + "".join(random.choices(string.ascii_lowercase, k=8))
    st, out = _sim.http_post_json(
        FREE_HOST + "/api/welcome/complete",
        {"alias": alias, "name": "F4 Fix Test",
         "answers": {"about": "free-walk fix verification"}, "topics": ["test"],
         "pageNames": {"personal": {"title": "F4 Fix Test"}}})
    assert st == 200, f"POST complete: {st} {out[:200]}"
    rev = json.loads(out.decode())
    assert rev.get("pages", {}).get("personal") == "/" + alias
    assert rev["pages"]["dashboard"].startswith("https://nayanet.app/dashboard")
    assert rev["pages"]["space"] == "/" + alias + "/space"
    print(f"POST /api/welcome/complete ({alias}): 200, reveal pages OK")
    st, _, out = _sim.http_get(FREE_HOST + f"/api/welcome/complete?alias={alias}")
    assert st == 200 and json.loads(out.decode())["alias"] == alias
    print("GET /api/welcome/complete: stored record reads back MATCH")
    st, hdrs, _ = _sim.http_get(FREE_HOST + "/" + alias)
    assert st in (301, 302)
    print(f"GET /{alias}: {st} -> {hdrs.get('Location')} MATCH")

    print("BUILD+STAGE OK")
    print(f"  walk-free sha256={sha(walk_free)}")
    print(f"  worker sha256={sha(worker)}")
    print(f"  test alias (KV, to clean): complete_{alias}")
    return {"walk_free": walk_free, "free_entry": free_entry,
            "free_index": free_index, "worker": worker, "alias": alias}


if __name__ == "__main__":
    main()
