#!/usr/bin/env python3
"""Pricing Fix round (2026-11-17) — six items, entry + walk.

BASE (reproduced first, fail-stop if moved): the taken-fix tip —
  walk 3,292,257 B sha 2370eae2... | entry 311,426 B sha 3d5b913f... |
  live staged /free must still serve that entry before anything is staged.
Regenerates the tip in memory (F4 builder + F4 fix + follow-on +
Marcellus swap + taken fix) and asserts the base shas before patching.

ITEM 1 — long taken name wraps mid-word at 635. Taken name goes
  nowrap + a narrow-width font cap (max-width:700px) + a JS shrink-to-fit
  (fitTakenName) that steps the size down until the one-line name fits
  its row. Gated on the taken state only; the fresh certificate is
  untouched (its CSS rules are asserted byte-identical).
ITEM 2 — descender overlap at desktop. Taken name gets line-height 1.14
  + padding-bottom .14em + margin-bottom 10px, so Marcellus descenders
  (p, g, y, j) clear the alias-box top border below at BOTH widths.
ITEM 3 — fresh-cert name echo. Root cause, proven in the worker code:
  the claim POSTs name = rawName || prettyName(alias); at a fresh entry
  rawName is empty, so the registry row's name IS the alias echo, and
  /api/welcome/complete only stores the completion record in KV — it
  never updates the identity row. The walk never saved its typed name
  anywhere the entry reads: step-1 answers live only in S.answers.about
  and the names-page title only in S.pageNames. On reload the 'own'
  restore preferred certRegalia.name (registry echo) over localStorage.
  Fix, both ends: (a) the walk adopts a name-like typed answer — step 1
  ("Tell me who you are") and the names-page personal title — into
  ID.name + localStorage nayanet_smart_name (so the completion payload
  carries it too); (b) the entry's 'own' restore prefers the walk-saved
  local name over the registry echo whenever it differs from the echo.
  A name-like answer is 1-4 words, <=40 chars, letters/spaces/hyphen/
  apostrophe/period only — a sentence stays an answer, never a name.
ITEM 4 — install veil. The veil auto-showed 5s after load, covered the
  whole page, intercepted ALL pointer events and locked body scroll.
  Fix: (a) the auto-show never fires over a finished (is-certified) or
  taken document; (b) stampCertificate and the own/taken state change
  close an open veil at once; (c) the veil is pointer-transparent (CSS)
  and ANY first interaction dismisses it (pointerdown / keydown) —
  only the card's own BUTTONS are exempt, so Install App / Not now /
  the X still work; a click on the card's dead space dismisses too,
  which matters because the centered card sits over ENTER. The
  dismissing click does not also fire the control beneath it; the next
  click acts — the brief's 'dismiss on first interaction' shape;
  (d) opening the veil no
  longer locks body scroll. The invite itself is unchanged (same card,
  same 3-lifetime-auto-show cap, same dismiss keys, manual open via the
  corner button still works).
ITEM 5 — duplicate id="enterBtn-14" on the naming page. The walk's
  step-names section reused step-14's ids (enterBtn-14, playBtn-14,
  enterNote-14 — all three duplicated). The names section's ids become
  enterBtn-names / playBtn-names / enterNote-names, and wireNames +
  resetNamesEnter use the new ids. Step 14 keeps enterBtn-14.
ITEM 6 — FILE the fixed bytes to branch pricing-f4-free-entry-20261116
  (see file-fix-to-github.py): the fixed entry bytes + fixed walk bytes
  + this build script + probe + report. No more "bytes only on staging".

Builds entirely in memory (EPERM flake) and stages to
naya-pricing-free-staging ONLY. Pricing worker NOT touched.
"""
import difflib
import gzip
import hashlib
import importlib.util
import json
import os
import re
import sys

sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
sys.path.insert(0, os.path.expanduser("~/workspace/ninaya/integration"))

F4 = os.path.expanduser("~/workspace/team-nitro/pricing-free-entry-20261116")
F4FIX = os.path.expanduser("~/workspace/team-nitro/pricing-f4-fix-20261117")
FO = os.path.expanduser("~/workspace/team-nitro/pricing-f4-followon-20261117")
MARC = os.path.expanduser("~/workspace/team-nitro/free-cert-marcellus-20261117")
TAKEN = os.path.expanduser("~/workspace/team-nitro/pricing-taken-state-fix-20261117")
HERE = os.path.expanduser("~/workspace/team-nitro/pricing-fix-20261117")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_bt = load("btaken", os.path.join(TAKEN, "build-taken-fix.py"))
_bf = _bt._bf
_fix = _bt._fix
_fo = _bt._fo
_marc = _bt._marc
_sim = _bt._sim
replace_once = _bf.replace_once

FREE_HOST = "https://naya-pricing-free-staging.nayapower.workers.dev"
PRICING_HOST = "https://naya-pricing-f4-staging.nayapower.workers.dev"
LIVE = "https://nayanet.app"

BASE_WALK_SHA = "2370eae2f9ae9e281d1c3f3b35d99f8699c7df6a2fe4f73328e2877c3b6453ea"
BASE_ENTRY_SHA = "3d5b913f117b90a1fdd3e72347f8458c4de4429972eb05a38c6fb118f7fbf285"
BASE_WORKER_SHA = "b70538d6ec32cba95d280a3e33f5e73bde24698112dafc1f97f90b338376d66a"
PRICING_V78_SHA = "ca2eafeb896c763ae2459b4a10b8715e726765ced607c0aab3640d27e6c39ae2"

CERT_GLOW = "0 0 38px rgba(160,107,255,0.16), 0 3px 30px rgba(0,0,0,0.55)"

# ---------------------------------------------------------------- entry fix
FIX_CSS = (
    "/* PRICING FIX (2026-11-17, items 1+2+4): taken name one line at every "
    "width, descenders clear of the alias box, veil never blocks. */\n    "
    ".cert-plaque:has(.alias-status[data-state=\"taken\"]) .cert-name{"
    "white-space:nowrap;overflow:visible;line-height:1.14;"
    "padding-bottom:.14em;margin-bottom:10px;}\n    "
    "@media (max-width:700px){\n      "
    ".cert-plaque:has(.alias-status[data-state=\"taken\"]) .cert-name{"
    "font-size:clamp(1.65rem,6.2vw,2.5rem);}\n    }\n    "
    ".install-veil{pointer-events:none;}\n    "
    ".install-veil .install-card{pointer-events:auto;}\n    "
)

FIT_JS = (
    "/* PRICING FIX (2026-11-17, item 1): shrink-to-fit for the taken "
    "name — the one-line rule must hold for the longest realistic alias "
    "at 635 AND desktop. Only ever shrinks, never grows; only runs in "
    "the taken state, so composing and the fresh certificate are "
    "untouched. */\n    "
    "function fitTakenName() {\n      "
    "try {\n        "
    "var _st = document.getElementById('aliasStatus');\n        "
    "if (!_st || _st.getAttribute('data-state') !== 'taken') return;\n        "
    "var _nm = document.getElementById('displayName');\n        "
    "if (!_nm || _nm.hidden || !_nm.textContent) return;\n        "
    "var _av = _nm.parentNode ? _nm.parentNode.clientWidth : 0;\n        "
    "if (!_av) return;\n        "
    "_nm.style.fontSize = '';\n        "
    "var _sz = parseFloat(window.getComputedStyle(_nm).fontSize) || 0;\n        "
    "var _g = 0;\n        "
    "while (_sz > 22 && _nm.scrollWidth > _av + 1 && _g < 40) { _sz -= 2; _nm.style.fontSize = _sz + 'px'; _g++; }\n      "
    "} catch (e) {}\n    }\n    "
    "window.fitTakenName = fitTakenName;\n    "
    "var _fitT = null;\n    "
    "window.addEventListener('resize', function(){ if (_fitT) clearTimeout(_fitT); _fitT = setTimeout(fitTakenName, 120); });\n    "
    "if (document.fonts && document.fonts.ready) { try { document.fonts.ready.then(function(){ fitTakenName(); }); } catch(e){} }\n    "
)


def sha(b):
    return hashlib.sha256(b if isinstance(b, bytes) else b.encode()).hexdigest()


def apply_entry_fix(d):
    """Items 1-4 on the entry. CSS additions + targeted JS edits only."""
    assert d.count("</style>") == 1, "entry must have exactly one </style>"
    assert ".cert-plaque:has(.alias-status[data-state=\"taken\"]) .cert-name{" in d, \
        "taken block missing — base moved"
    assert "PRICING FIX (2026-11-17" not in d, "fix block already present"
    new = d.replace("</style>", FIX_CSS + "</style>", 1)

    # --- item 1: fit function, right after prettyName (before first use).
    anchor = "const prettyName = s => s ? s.charAt(0).toUpperCase() + s.slice(1) : '';"
    assert new.count(anchor) == 1, "prettyName anchor moved"
    new = replace_once(new, anchor, anchor + "\n    " + FIT_JS, "fitTakenName def")
    # --- item 1: run the fit on every input (state-gated inside) and on
    # every state change.
    anchor = "updateSmartCredentials = function(){ _origUpdate(); scheduleAliasCheck(false); };"
    assert new.count(anchor) == 1, "update wrapper anchor moved"
    new = replace_once(new, anchor,
                       "updateSmartCredentials = function(){ _origUpdate(); fitTakenName(); scheduleAliasCheck(false); };",
                       "fit on input")
    anchor = "      renderCertRegalia(state);"
    assert new.count(anchor) == 1, "setAliasState anchor moved"
    new = replace_once(new, anchor,
                       anchor + "\n      fitTakenName();"
                       "\n      /* PRICING FIX (item 4): a result document never sits behind the veil. */"
                       "\n      if ((state === 'own' || state === 'taken') && window.__nayaCloseInstallVeil) { try { window.__nayaCloseInstallVeil(); } catch(e){} }",
                       "fit + veil-close on state change")

    # --- item 3: 'own' restore prefers the walk-saved local name over the
    # registry echo (claim-time name, written before the walk existed).
    anchor = "var certName = certRegalia.name || rawName || prettyName(certRegalia.alias || alias);"
    assert new.count(anchor) == 1, "own-restore anchor moved"
    new = replace_once(new, anchor,
                       "/* PRICING FIX (item 3): the registry name is the claim-time name — the alias echo when no ?name= rode in — and the walk never corrected it. The walk's typed name lives in localStorage; when it differs from the echo, IT is the certificate name. */\n        "
                       "var typedName = (rawName && rawName.toLowerCase() !== (certRegalia.alias || alias) && rawName !== prettyName(certRegalia.alias || alias)) ? rawName : '';\n        "
                       "var certName = typedName || certRegalia.name || rawName || prettyName(certRegalia.alias || alias);",
                       "own-restore name priority")

    # --- item 4: stamp closes an open veil (fresh cert never behind it).
    anchor = "        certStamped = true;"
    assert new.count(anchor) == 1, "stamp anchor moved"
    new = replace_once(new, anchor,
                       anchor + "\n        try { if (window.__nayaCloseInstallVeil) window.__nayaCloseInstallVeil(); } catch(e){}",
                       "stamp closes veil")

    # --- item 4: veil IIFE — no scroll lock; dismiss on first interaction
    # outside the card; never auto-show over a result document; expose dismiss.
    anchor = "        veil.hidden = false;\n        document.body.style.overflow = 'hidden';"
    assert new.count(anchor) == 1, "openModal anchor moved"
    new = replace_once(new, anchor,
                       "        veil.hidden = false;\n        /* PRICING FIX (item 4): never lock the page scroll behind the veil — a locked page strands ENTER/start-over below the fold. */",
                       "no scroll lock")
    anchor = "      document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !veil.hidden) dismiss(); });"
    assert new.count(anchor) == 1, "veil keydown anchor moved"
    new = replace_once(new, anchor,
                       anchor + "\n      /* PRICING FIX (2026-11-17, item 4): the veil must never block the page. It is pointer-transparent (CSS) and ANY first interaction dismisses it — a click on ENTER, start-over, the input, or the card's own dead space all dismiss; only the card's BUTTONS are exempt, so Install App / Not now / the X still work. (Exempting the whole card was the first shape's bug: the centered card sits over ENTER, so an ENTER click landed on the card and was exempted — the veil never dismissed.) The click that dismisses does not also fire the control beneath it; the next click acts — that is the brief's 'dismiss on first interaction' shape. */"
                       "\n      document.addEventListener('pointerdown', function (e) { if (veil.hidden) return; if (e.target && e.target.closest && e.target.closest('button')) return; dismiss(); }, true);"
                       "\n      document.addEventListener('keydown', function (e) { if (veil.hidden) return; if (e.target && e.target.closest && e.target.closest('button')) return; if (e.key !== 'Escape') dismiss(); }, true);"
                       "\n      /* The stamp path and the result states close the veil too: a fresh certificate must never sit behind it. */"
                       "\n      /* Automatic closes (stamp / result state) hide without recording a user dismissal — that key stays the user's own tap. */"
                       "\n      window.__nayaCloseInstallVeil = closeModal;",
                       "veil first-interaction dismiss")
    anchor = "          if (!h && !d && n < 3) {"
    assert new.count(anchor) == 1, "veil auto-show anchor moved"
    new = replace_once(new, anchor,
                       "          /* PRICING FIX (item 4): never auto-show over a finished or taken document — the certificate a citizen just earned, and the taken document with its ENTER/start-over, are never covered. */\n"
                       "          var _pl = document.getElementById('certPlaque');\n"
                       "          var _tk = document.getElementById('aliasStatus');\n"
                       "          var _isResult = (_pl && _pl.classList.contains('is-certified')) || (_tk && _tk.getAttribute('data-state') === 'taken');\n"
                       "          if (!h && !d && n < 3 && !_isResult) {",
                       "veil auto-show gate")
    return new


# ----------------------------------------------------------------- walk fix
ADOPT_JS = (
    "/* PRICING FIX (2026-11-17, item 3): the walk's typed name IS the "
    "certificate name. The claim posted the alias echo as the registry "
    "name (the entry had no typed name yet), and nothing ever corrected "
    "it — so a reload showed the echo instead of the name typed here. "
    "When an answer looks like a person's name (a few words, letters/"
    "spaces/hyphen/apostrophe/period only), adopt it as the identity "
    "name at once: localStorage (the entry reads it on reload) and "
    "ID.name (the completion payload carries it). A sentence stays an "
    "answer, never a name. */\n"
    "function looksLikeName(t){\n"
    "  if (!t) return false;\n"
    "  var s = String(t).trim().replace(/\\s+/g, ' ');\n"
    "  if (!s || s.length > 40) return false;\n"
    "  var words = s.split(' ');\n"
    "  if (words.length < 1 || words.length > 4) return false;\n"
    "  if (/[^A-Za-z'\\u2019\\-.\\s]/.test(s)) return false;\n"
    "  if (/[.!?,:;]$/.test(s)) return false;\n"
    "  return true;\n"
    "}\n"
    "function adoptWalkName(t){\n"
    "  try {\n"
    "    if (!looksLikeName(t)) return;\n"
    "    var s = String(t).trim().replace(/\\s+/g, ' ');\n"
    "    if (ID.alias && s.toLowerCase() === ID.alias.toLowerCase()) return;\n"
    "    ID.name = s;\n"
    "    lsSet('nayanet_smart_name', s);\n"
    "  } catch(e){}\n"
    "}\n"
)


def apply_walk_fix(w):
    """Items 3 + 5 on the walk."""
    assert "PRICING FIX (2026-11-17" not in w, "walk fix already present"
    # --- item 3: adoptWalkName helper, after save().
    anchor = "function save(){ try { lsSet(SKEY, JSON.stringify({ alias: ID.alias, answers: S.answers, topics: S.topics, reveal: S.reveal, pageNames: S.pageNames })); } catch(e){} }"
    assert w.count(anchor) == 1, "walk save anchor moved"
    new = replace_once(w, anchor, anchor + "\n" + ADOPT_JS, "adoptWalkName def")
    # --- item 3: step 1 ("Tell me who you are") adopts its typed name.
    anchor = "      S.answers[key] = answer.value; save();\n      hideStatus(speakNote);"
    assert new.count(anchor) == 1, "submitAnswer anchor moved"
    new = replace_once(new, anchor,
                       "      S.answers[key] = answer.value; save();\n      if (key === 'about') adoptWalkName(answer.value);\n      hideStatus(speakNote);",
                       "step-1 name adopt")
    # --- item 3: names-page personal title adopts its typed name.
    anchor = "    S.pageNames = {\n      personal: { title: pTitle, slug: alias },"
    assert new.count(anchor) == 1, "wireNames pageNames anchor moved"
    # insert after the closing of the S.pageNames assignment + save();
    anchor2 = "    };\n    save();\n  }"
    assert new.count(anchor2) == 1, "wireNames refresh anchor moved"
    new = replace_once(new, anchor2,
                       "    };\n    save();\n    if (pTitle && pTitle.toLowerCase() !== alias) adoptWalkName(pTitle);\n  }",
                       "names-page name adopt")
    # --- item 5: the names section reuses step-14's ids — rename in-section.
    start = new.find('id="step-names"')
    assert start > 0, "step-names section missing"
    end = new.find("</section>", start)
    assert end > start, "step-names section end missing"
    sec = new[start:end]
    assert sec.count('id="enterBtn-14"') == 1, "names enterBtn count moved"
    assert sec.count('id="playBtn-14"') == 1, "names playBtn count moved"
    assert sec.count('id="enterNote-14"') == 1, "names enterNote count moved"
    sec = sec.replace('id="enterBtn-14"', 'id="enterBtn-names"')
    sec = sec.replace('id="playBtn-14"', 'id="playBtn-names"')
    sec = sec.replace('id="enterNote-14"', 'id="enterNote-names"')
    new = new[:start] + sec + new[end:]
    # --- item 5: wireNames + resetNamesEnter use the new ids.
    anchor = "NAMESSEC.querySelector('#enterBtn-14')"
    assert new.count(anchor) == 1, "resetNamesEnter anchor moved"
    new = replace_once(new, anchor, "NAMESSEC.querySelector('#enterBtn-names')", "resetNamesEnter id")
    anchor = "var playBtn = sec.querySelector('#playBtn-14');"
    assert new.count(anchor) == 1, "wireNames playBtn anchor moved"
    new = replace_once(new, anchor, "var playBtn = sec.querySelector('#playBtn-names');", "wireNames playBtn id")
    anchor = "var enterBtn = sec.querySelector('#enterBtn-14');"
    assert new.count(anchor) == 1, "wireNames enterBtn anchor moved"
    new = replace_once(new, anchor, "var enterBtn = sec.querySelector('#enterBtn-names');", "wireNames enterBtn id")
    anchor = "var enterNote = sec.querySelector('#enterNote-14');"
    assert new.count(anchor) == 1, "wireNames enterNote anchor moved"
    new = replace_once(new, anchor, "var enterNote = sec.querySelector('#enterNote-names');", "wireNames enterNote id")
    # --- item 5 proof: no duplicate ids left in the walk at all.
    ids = re.findall(r'id="([^"]+)"', new)
    dupes = sorted({k for k, v in ((k, ids.count(k)) for k in set(ids)) if v > 1})
    assert not dupes, f"walk still has duplicate ids: {dupes}"
    assert new.count('id="enterBtn-14"') == 1, "enterBtn-14 must occur exactly once (step 14)"
    return new


def main():
    # 0. Regenerate the taken-fix tip base in memory; fail-stop if moved.
    walk_f4 = _fix.apply_walk_fixes(_bf.build_walk_free())
    entry_f4 = _bf.build_free_entry()
    walk_base = _fo.apply_item1_walk(walk_f4)
    entry_fo = _fo.apply_entry_followon(entry_f4)
    entry_marc = _marc.apply_marcellus_swap(entry_fo)
    entry_base = _bt.apply_taken_fix(entry_marc)
    worker_base = _fix.apply_worker_fix(_bf.build_worker(walk_base, entry_base))
    assert sha(walk_base) == BASE_WALK_SHA, f"base walk moved: {sha(walk_base)}"
    assert sha(entry_base) == BASE_ENTRY_SHA, f"base entry moved: {sha(entry_base)}"
    print(f"base verified: walk {len(walk_base.encode())} B sha={sha(walk_base)[:8]}... "
          f"entry {len(entry_base.encode())} B sha={sha(entry_base)[:8]}...")

    # 0b. Live staged /free must still serve the tip entry — or, on a
    # rebuild, this round's own previous fixed entry (same base, same
    # chain; the fix is re-applied from the base in memory either way).
    st, _, live_entry = _sim.http_get(FREE_HOST + "/free")
    prev_fixed = "c059deff194c1395976879c37195e3486727f22db8678304cb8dc8512e00fa95"
    assert st == 200 and sha(live_entry) in (BASE_ENTRY_SHA, prev_fixed), \
        f"live staged /free moved: {st} {sha(live_entry)[:8]}... — STOP"
    print(f"live staged /free == {'tip entry' if sha(live_entry) == BASE_ENTRY_SHA else 'previous fixed entry'} MATCH")

    # 0c. Harvest the page's own PWA assets verbatim from the live site.
    st, _, sw = _sim.http_get(LIVE + "/sw.js")
    assert st == 200, f"live sw.js: {st}"
    sw = sw.decode("utf-8")
    assert "self-retiring" in sw and "skipWaiting" in sw and "unregister" in sw
    st, _, mani = _sim.http_get(LIVE + "/manifest.webmanifest")
    assert st == 200, f"live manifest: {st}"
    mani = mani.decode("utf-8")
    assert "NayaNET" in json.loads(mani).get("name", "")
    print(f"harvested live PWA assets: sw.js {len(sw.encode())} B sha={sha(sw)[:8]}... "
          f"manifest {len(mani.encode())} B sha={sha(mani)[:8]}...")

    # 1. Apply the fixes.
    old_certified = re.findall(r'\.cert-plaque\.is-certified[^{]*\{[^}]*\}', entry_base)
    old_certname = re.findall(r'\.cert-name[^{]*\{[^}]*\}', entry_base)
    new_entry = apply_entry_fix(entry_base)
    new_walk = apply_walk_fix(walk_base)
    # Fresh certificate CSS untouched: every old certified rule and every
    # old .cert-name rule still present byte-identical.
    assert re.findall(r'\.cert-plaque\.is-certified[^{]*\{[^}]*\}', new_entry) == old_certified, \
        "certified CSS rules changed — STOP"
    for r in old_certname:
        assert r in new_entry, f"old .cert-name rule changed — STOP: {r[:120]}"
    # Marcellus still the cert serif; no Newsreader anywhere.
    assert "Marcellus" in new_entry and new_entry.count("Newsreader") == 0
    assert new_walk.count("Newsreader") == 0
    # Diff shape: print it.
    for label, old, new in [("entry", entry_base, new_entry), ("walk", walk_base, new_walk)]:
        diff = list(difflib.unified_diff(old.splitlines(), new.splitlines(), lineterm="", n=0))
        removed = [ln for ln in diff if ln.startswith("-") and not ln.startswith("---")]
        added = [ln for ln in diff if ln.startswith("+") and not ln.startswith("+++")]
        print(f"{label} diff: +{len(added)} lines, -{len(removed)} lines")
        for ln in removed:
            print("   -", ln[:220])
        for ln in added:
            print("   +", ln[:220])
    print(f"new entry: {len(new_entry.encode())} B sha256={sha(new_entry)}")
    print(f"new walk: {len(new_walk.encode())} B sha256={sha(new_walk)}")

    # 2. Worker rebuild (taken-fix PWA patch, same shape) + node driver.
    from importlib.util import spec_from_file_location as _sfl, module_from_spec as _mfs
    _dn_spec = _sfl("deploy_ninaya", os.path.expanduser(
        "~/workspace/ninaya/integration/deploy-ninaya.py"))
    _dn = _mfs(_dn_spec)
    _dn_spec.loader.exec_module(_dn)
    js_encode = _dn.js_encode

    free_index = _bf.FREE_INDEX.replace(
        "__PRICING_STAGED__", "https://naya-pricing-f4-staging.nayapower.workers.dev/")
    new_worker = _fix.apply_worker_fix(_bf.build_worker(new_walk, new_entry))
    anchor_const = 'const SB_URL = "https://dahisasgpfvziswqvmvm.supabase.co/rest/v1/nayanet_identities";'
    consts = ('const TAKEN_SW = "' + js_encode(sw) + '";\n'
              'const TAKEN_MANIFEST = "' + js_encode(mani) + '";\n')
    new_worker = replace_once(new_worker, anchor_const, consts + anchor_const,
                              "PWA asset consts")
    anchor_route = '    if (p === "/free/hub") {'
    routes = (
        '    if (p === "/sw.js") {\n'
        '      return new Response(TAKEN_SW, { headers: { "content-type": '
        '"application/javascript;charset=utf-8", "cache-control": "no-store" } });\n'
        '    }\n'
        '    if (p === "/manifest.webmanifest") {\n'
        '      return new Response(TAKEN_MANIFEST, { headers: { "content-type": '
        '"application/manifest+json;charset=utf-8", "cache-control": "no-store" } });\n'
        '    }\n')
    new_worker = replace_once(new_worker, anchor_route, routes + anchor_route,
                              "PWA asset routes")
    print(f"new worker: {len(new_worker.encode())} B sha256={sha(new_worker)}")
    gz = gzip.compress(new_worker.encode("utf-8"))
    print(f"worker gzip: {len(gz)} B (limit 10,485,760)")
    assert len(gz) < 10485760

    _sim.node_check(new_worker, FREE_HOST + "/free", sha(new_entry),
                    ["PRICING FIX (2026-11-17",
                     "function fitTakenName()",
                     "white-space:nowrap;overflow:visible;line-height:1.14",
                     ".install-veil{pointer-events:none;}",
                     "var typedName = (rawName",
                     "__nayaCloseInstallVeil",
                     "never auto-show over a finished or taken document",
                     ".cert-plaque:has(.alias-status[data-state=\"taken\"]) .cert-name{position:static",
                     "text-shadow:" + CERT_GLOW,
                     "--serif: Marcellus, Georgia, serif;",
                     "id=\"startOverBtn\"", "Use a different alias",
                     ".cert-plaque.is-certified{overflow-y:auto}",
                     "Enter free &mdash; no payment, no card.",
                     'id="freeEye"', "WALKTHROUGH_URL = '/free/walk'"],
                    ["Newsreader"])
    _sim.node_check(new_worker, FREE_HOST + "/free/walk", sha(new_walk),
                    ["fonts.googleapis.com/css2?family=Marcellus",
                     "font-family:Marcellus,Georgia,serif",
                     ".p3-congrats{font-family:Marcellus",
                     "function adoptWalkName",
                     'id="enterBtn-names"',
                     'id="playBtn-names"',
                     'id="enterNote-names"',
                     "if (key === 'about') adoptWalkName(answer.value);",
                     "buildBarFill", "showStep(16)"],
                    ["Newsreader"])
    _sim.node_check(new_worker, FREE_HOST + "/", sha(free_index),
                    ["Enter free — the route, staged"], [])
    _sim.node_check(new_worker, FREE_HOST + "/sw.js", sha(sw),
                    ["self-retiring", "skipWaiting", "unregister"], [])
    _sim.node_check(new_worker, FREE_HOST + "/manifest.webmanifest", sha(mani),
                    ["NayaNET", "start_url"], [])
    _sim.node_redirect_check(new_worker, FREE_HOST + "/free/hub",
                             "https://nayanet.app/")
    print("node driver: PASS (fixed entry + fixed walk + index + sw.js + manifest + hub)")

    # 3. Stage the new free worker (STAGING ONLY — pricing untouched).
    kv = [{"type": "kv_namespace", "name": "WELCOME_ASSETS",
           "namespace_id": "1cf80db6183245d19dd5296645a12bd0"}]
    _sim.put_worker("naya-pricing-free-staging", new_worker.encode(), kv)
    status, raw = _sim.api("GET", "/naya-pricing-free-staging")
    assert status == 200
    _, wb, _ = _sim.split_multipart(raw)
    assert wb == new_worker.encode(), "read-back differs from PUT — STOP"
    print(f"read-back sha256={sha(wb)} — MATCH")

    # 4. Live HTTP verification of the staged routes.
    for path, want in [("/", free_index), ("/free", new_entry),
                       ("/free/walk", new_walk)]:
        st, _, got = _sim.http_get(FREE_HOST + path)
        assert st == 200, f"GET {path}: {st}"
        assert got.decode("utf-8") == want, f"GET {path}: bytes != source — STOP"
        print(f"GET {FREE_HOST}{path}: 200, {len(got)} B == source MATCH")
    for path, want_bytes, want_ct in [
            ("/sw.js", sw.encode(), "application/javascript"),
            ("/manifest.webmanifest", mani.encode(), "application/manifest+json")]:
        st, hdrs, got = _sim.http_get(FREE_HOST + path)
        assert st == 200, f"GET {path}: {st}"
        assert got == want_bytes, f"GET {path}: bytes != harvested — STOP"
        assert want_ct in hdrs.get("Content-Type", ""), \
            f"GET {path}: content-type {hdrs.get('Content-Type')} — STOP"
        print(f"GET {FREE_HOST}{path}: 200, {len(got)} B == harvested MATCH "
              f"({hdrs.get('Content-Type')})")
    st, hdrs, _ = _sim.http_get(FREE_HOST + "/free/hub")
    assert st in (301, 302) and hdrs.get("Location") == "https://nayanet.app/"
    print("GET /free/hub: 302 -> https://nayanet.app/ MATCH")

    # 5. Pricing v78 still byte-exact on its own staging worker (untouched).
    st, _, v78 = _sim.http_get(PRICING_HOST + "/")
    assert st == 200 and sha(v78) == PRICING_V78_SHA, "pricing v78 MOVED — STOP"
    print(f"pricing v78: {len(v78)} B sha={sha(v78)[:8]}... UNCHANGED")

    # 6. Save the fixed bytes locally (filing + checker source of truth).
    with open(os.path.join(HERE, "fixed-entry.html"), "w") as f:
        f.write(new_entry)
    with open(os.path.join(HERE, "fixed-walk.html"), "w") as f:
        f.write(new_walk)
    print("BUILD+STAGE OK")
    print(f"  walk sha256={sha(new_walk)}")
    print(f"  entry sha256={sha(new_entry)}")
    print(f"  worker sha256={sha(new_worker)}")
    print(f"  sw.js sha256={sha(sw)} ({len(sw.encode())} B, live verbatim)")
    print(f"  manifest sha256={sha(mani)} ({len(mani.encode())} B, live verbatim)")
    return {"walk": new_walk, "entry": new_entry, "free_index": free_index,
            "worker": new_worker, "sw": sw, "manifest": mani}


if __name__ == "__main__":
    main()
