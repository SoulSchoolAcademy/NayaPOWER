#!/usr/bin/env python3
"""Pricing Free: Taken-State Certificate Fix (2026-11-17).

BASE (verified first, fail-stop if moved): the Marcellus-swap tip —
  walk 3,292,257 B sha 2370eae2... | entry 310,212 B sha dfe70a8c... |
  worker 3,622,208 B sha 29c859f2... (branch pricing-f4-free-entry-20261116).
Regenerates the tip in memory (F4 builder + F4 fix + follow-on + Marcellus
swap) and asserts the base shas before patching anything. Also verifies
the LIVE staged /free still serves the tip entry before staging over it.

THE TAKEN STATE (proven live, Chromium 390/635/1440, alias
alexanderchristopherbennett cert 753): the plaque is NOT .is-certified,
so NONE of the follow-on narrow fixes apply to it:
  (1) the echo name (.cert-name) is ABSOLUTE above the input and grows
      UPWARD as it wraps — a 29-char name paints straight over
      "CERTIFICATE OF SMART IDENTITY" and "This certifies that" (desktop)
      and strikes through "This certifies that" (390); at 635 it climbs
      to viewport y=7, over the seal and top bar.
  (2) the base .cert-name carries NO text-shadow — only the certified
      rule has the layered glow (SN-2922).
  (3) #startOverBtn is display:none except under .is-certified — the
      taken state has no way out.
  (4) the plaque scroll rule is .is-certified-gated — the taken page
      cannot scroll at 635x349 (overflow:hidden) and ENTER strands
      below the fold (user scroll does nothing; programmatic scrollTop
      is not a user path).
  (5) console: "A bad HTTP response code (404) was received when
      fetching the script." — the entry registers sw.js and links
      manifest.webmanifest; the free worker 404s both (curl-proven:
      /sw.js 404, /manifest.webmanifest 404, /icons/apple-touch-icon.png
      404). The script IS sw.js.

THE FIX — taken state only, the fresh certificate UNTOUCHED (its rules
are extracted before/after and asserted byte-identical; the diff is
additions only). The taken document takes the fresh certificate's OWN
presentation, using its own proven mechanism (the follow-on's flow +
scroll cure for short viewports), gated on the taken state:
  (1) the taken name goes STATIC IN FLOW, exactly as the certified
      name sits (position:static; transform:none; width:auto) — inside
      the center row, below the head band, so it can never overlap the
      title or "This certifies that" at any width.
  (2) the taken name carries the certified name's layered glow VERBATIM:
      text-shadow: 0 0 38px rgba(160,107,255,0.16), 0 3px 30px
      rgba(0,0,0,0.55).
  (3) #startOverBtn shows in the taken state too (same ghost button,
      same handler — clears the six identity/walk keys + two session
      keys and reloads into composing).
  (4) the taken plaque scrolls and its face flows (position:static
      flex column, min-height:100%, centered) at EVERY height — the
      taken document is taller than the certified one (benefit +
      privacy + hubNote ride in the foot), so a height gate would still
      strand ENTER at desktop with a long name; overflow-y:auto means
      it scrolls exactly when it doesn't fit and centers when it does.
  (5) the worker serves the page's own PWA assets: /sw.js and
      /manifest.webmanifest, harvested VERBATIM from the live site
      (https://nayanet.app/sw.js — the self-retiring cure, 567 B;
      manifest 581 B). The live sw.js was proven benign on localhost
      first (swtest.py: registers ok, self-unregisters, NO page reload
      in 8s, zero console errors) — it is the file that ships next to
      the live identity page. Both routes return 200 with the correct
      MIME type. /icons/apple-touch-icon.png still 404s (only fetched
      on iOS add-to-home-screen, never on desktop load) — noted, not
      fixed: its bytes are not harvested anywhere in scope.

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


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_bf = load("bfree", os.path.join(F4, "build-free-staging-worker.py"))
_fix = load("ffix", os.path.join(F4FIX, "build-fix.py"))
_fo = load("fo", os.path.join(FO, "build-followon.py"))
_marc = load("marc", os.path.join(MARC, "build-marcellus.py"))
_sim = load("sim", os.path.join(F4, "stage-in-memory.py"))
replace_once = _bf.replace_once

FREE_HOST = "https://naya-pricing-free-staging.nayapower.workers.dev"
PRICING_HOST = "https://naya-pricing-f4-staging.nayapower.workers.dev"
LIVE = "https://nayanet.app"

BASE_WALK_SHA = "2370eae2f9ae9e281d1c3f3b35d99f8699c7df6a2fe4f73328e2877c3b6453ea"
BASE_ENTRY_SHA = "dfe70a8c8a4d89aa49a31aa56d077b51867ef4e42f276ce28bc39d23fa6370b2"
BASE_WORKER_SHA = "29c859f2bf7201e239ec9a11be1290f9e69637bb0da1f915480077ae5df29121"
PRICING_V78_SHA = "ca2eafeb896c763ae2459b4a10b8715e726765ced607c0aab3640d27e6c39ae2"

CERT_GLOW = "0 0 38px rgba(160,107,255,0.16), 0 3px 30px rgba(0,0,0,0.55)"

TAKEN_CSS = (
    "/* TAKEN STATE (2026-11-17): the taken document takes the fresh "
    "certificate's own presentation — the name sits IN FLOW in the "
    "center (as the certified name does), carries the certified glow, "
    "the face flows and the plaque scrolls when the document is taller "
    "than the viewport, and the start-over control shows. Gated on the "
    "taken state only — the fresh certificate is untouched. */\n    "
    ".cert-plaque:has(.alias-status[data-state=\"taken\"]) .cert-name{"
    "position:static;transform:none;width:auto;pointer-events:auto;"
    "text-shadow:" + CERT_GLOW + ";}\n    "
    ".cert-plaque:has(.alias-status[data-state=\"taken\"]){overflow-y:auto}\n    "
    ".cert-plaque:has(.alias-status[data-state=\"taken\"]) .identity-face{"
    "position:static;display:flex;flex-direction:column;justify-content:center;"
    "min-height:100%;box-sizing:border-box}\n    "
    ".cert-plaque:has(.alias-status[data-state=\"taken\"]) .face-head,"
    ".cert-plaque:has(.alias-status[data-state=\"taken\"]) .face-foot{align-self:auto}\n    "
    ".cert-plaque:has(.alias-status[data-state=\"taken\"]) .face-foot{margin-top:16px}\n    "
    ".cert-plaque:has(.alias-status[data-state=\"taken\"]) #startOverBtn{"
    "display:inline-flex;align-items:center;justify-content:center}\n    "
)


def sha(b):
    return hashlib.sha256(b if isinstance(b, bytes) else b.encode()).hexdigest()


def apply_taken_fix(d):
    """The taken-state fix: one appended CSS block, additions only."""
    assert d.count("</style>") == 1, "entry must have exactly one </style>"
    assert ".cert-plaque.is-certified{overflow-y:auto}" in d, \
        "follow-on certified scroll rule missing — base moved"
    assert TAKEN_CSS.strip().split("\n")[0] not in d, "taken block already present"
    new = d.replace("</style>", TAKEN_CSS + "</style>", 1)
    # Placement: the taken block must come AFTER the follow-on CERT_CSS.
    assert new.find(TAKEN_CSS.strip().split("\n")[0]) > \
        new.find(".cert-plaque.is-certified{overflow-y:auto}"), \
        "taken block landed before the follow-on block — STOP"
    return new


def main():
    # 0. Regenerate the Marcellus-tip base in memory; fail-stop if moved.
    walk_f4 = _fix.apply_walk_fixes(_bf.build_walk_free())
    entry_f4 = _bf.build_free_entry()
    walk = _fo.apply_item1_walk(walk_f4)
    entry_fo = _fo.apply_entry_followon(entry_f4)
    entry = _marc.apply_marcellus_swap(entry_fo)
    worker = _fix.apply_worker_fix(_bf.build_worker(walk, entry))
    assert sha(walk) == BASE_WALK_SHA, f"base walk moved: {sha(walk)}"
    assert sha(entry) == BASE_ENTRY_SHA, f"base entry moved: {sha(entry)}"
    assert sha(worker) == BASE_WORKER_SHA, f"base worker moved: {sha(worker)}"
    print(f"base verified: walk {len(walk.encode())} B sha={sha(walk)[:8]}... "
          f"entry {len(entry.encode())} B sha={sha(entry)[:8]}... "
          f"worker {len(worker.encode())} B sha={sha(worker)[:8]}...")

    # 0b. The live staged /free must still serve the tip entry.
    st, _, live_entry = _sim.http_get(FREE_HOST + "/free")
    assert st == 200 and sha(live_entry) == BASE_ENTRY_SHA, \
        f"live staged /free moved: {st} {sha(live_entry)[:8]}... — STOP"
    print("live staged /free == tip entry MATCH")

    # 0c. Harvest the page's own PWA assets verbatim from the live site.
    st, _, sw = _sim.http_get(LIVE + "/sw.js")
    assert st == 200, f"live sw.js: {st}"
    sw = sw.decode("utf-8")
    assert "self-retiring" in sw and "skipWaiting" in sw and "unregister" in sw, \
        "live sw.js is not the self-retiring cure — STOP"
    st, _, mani = _sim.http_get(LIVE + "/manifest.webmanifest")
    assert st == 200, f"live manifest: {st}"
    mani = mani.decode("utf-8")
    mj = json.loads(mani)
    assert "NayaNET" in mj.get("name", ""), "live manifest name wrong — STOP"
    print(f"harvested live PWA assets: sw.js {len(sw.encode())} B sha={sha(sw)[:8]}... "
          f"manifest {len(mani.encode())} B sha={sha(mani)[:8]}...")

    # 1. Apply the taken fix to the entry.
    old_certname = re.findall(r'\.cert-name[^{]*\{[^}]*\}', entry)
    old_certified = re.findall(r'\.cert-plaque\.is-certified[^{]*\{[^}]*\}', entry)
    old_shadows = re.findall(r'text-shadow:[^;]*;', entry)
    new_entry = apply_taken_fix(entry)
    # Fresh certificate untouched: every old .cert-name rule is still
    # present byte-identical (the taken block ADDS one new .cert-name
    # rule); every certified rule byte-identical.
    new_certname = re.findall(r'\.cert-name[^{]*\{[^}]*\}', new_entry)
    assert len(new_certname) == len(old_certname) + 1, \
        f".cert-name rule count moved by {len(new_certname) - len(old_certname)} — STOP"
    for r in old_certname:
        assert r in new_certname, f"old .cert-name rule changed — STOP: {r[:120]}"
    assert re.findall(r'\.cert-plaque\.is-certified[^{]*\{[^}]*\}', new_entry) == old_certified, \
        "certified rules changed — STOP"
    assert re.findall(r'text-shadow:[^;]*;', new_entry) == old_shadows + \
        [f"text-shadow:{CERT_GLOW};"], "text-shadows changed beyond the one taken glow — STOP"
    # The diff must be additions ONLY, all inside the taken block.
    diff = list(difflib.unified_diff(entry.splitlines(), new_entry.splitlines(),
                                     lineterm="", n=0))
    removed = [ln for ln in diff if ln.startswith("-") and not ln.startswith("---")]
    added = [ln for ln in diff if ln.startswith("+") and not ln.startswith("+++")]
    assert not removed, f"diff REMOVES lines — STOP: {removed[:3]}"
    assert all("taken" in ln or ln.startswith("+    ") or ln.startswith("+.cert-plaque:has")
               for ln in added), f"diff adds a non-taken line — STOP: {added[:3]}"
    print(f"taken fix applied: +{len(added)} lines, -{len(removed)} lines "
          f"(additions only, taken block only)")
    for ln in added:
        print("   ", ln[:200])
    print(f"new entry: {len(new_entry.encode())} B sha256={sha(new_entry)}")

    # 2. Worker patch (item 5): serve /sw.js + /manifest.webmanifest.
    from importlib.util import spec_from_file_location as _sfl, module_from_spec as _mfs
    _dn_spec = _sfl("deploy_ninaya", os.path.expanduser(
        "~/workspace/ninaya/integration/deploy-ninaya.py"))
    _dn = _mfs(_dn_spec)
    _dn_spec.loader.exec_module(_dn)
    js_encode = _dn.js_encode

    free_index = _bf.FREE_INDEX.replace(
        "__PRICING_STAGED__", "https://naya-pricing-f4-staging.nayapower.workers.dev/")
    new_worker = _fix.apply_worker_fix(_bf.build_worker(walk, new_entry))
    # (a) the asset consts, ahead of SB_URL.
    anchor_const = 'const SB_URL = "https://dahisasgpfvziswqvmvm.supabase.co/rest/v1/nayanet_identities";'
    consts = ('const TAKEN_SW = "' + js_encode(sw) + '";\n'
              'const TAKEN_MANIFEST = "' + js_encode(mani) + '";\n')
    new_worker = replace_once(new_worker, anchor_const, consts + anchor_const,
                              "PWA asset consts")
    # (b) the routes, ahead of the /free/hub branch.
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
    assert new_entry.count("Newsreader") == 0 and "Marcellus" in new_entry
    print(f"new worker: {len(new_worker.encode())} B sha256={sha(new_worker)}")
    gz = gzip.compress(new_worker.encode("utf-8"))
    print(f"worker gzip: {len(gz)} B (limit 10,485,760)")
    assert len(gz) < 10485760

    # 3. Node driver: the real fetch handler serves the new entry + walk +
    # the PWA assets with the right bytes.
    _sim.node_check(new_worker, FREE_HOST + "/free", sha(new_entry),
                    ['.cert-plaque:has(.alias-status[data-state="taken"]) .cert-name{position:static',
                     "text-shadow:" + CERT_GLOW,
                     '.cert-plaque:has(.alias-status[data-state="taken"]){overflow-y:auto}',
                     '.cert-plaque:has(.alias-status[data-state="taken"]) #startOverBtn{display:inline-flex',
                     "--serif: Marcellus, Georgia, serif;",
                     "id=\"startOverBtn\"", "Use a different alias",
                     ".cert-plaque.is-certified{overflow-y:auto}",
                     "Enter free &mdash; no payment, no card.",
                     'id="freeEye"', "WALKTHROUGH_URL = '/free/walk'"],
                    ["Newsreader"])
    _sim.node_check(new_worker, FREE_HOST + "/free/walk", sha(walk),
                    ["fonts.googleapis.com/css2?family=Marcellus",
                     "font-family:Marcellus,Georgia,serif",
                     ".p3-congrats{font-family:Marcellus",
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
    print("node driver: PASS (new entry + unchanged walk + index + sw.js + manifest + hub)")

    # 4. Stage the new free worker (STAGING ONLY — pricing untouched).
    kv = [{"type": "kv_namespace", "name": "WELCOME_ASSETS",
           "namespace_id": "1cf80db6183245d19dd5296645a12bd0"}]
    _sim.put_worker("naya-pricing-free-staging", new_worker.encode(), kv)
    status, raw = _sim.api("GET", "/naya-pricing-free-staging")
    assert status == 200
    _, wb, _ = _sim.split_multipart(raw)
    assert wb == new_worker.encode(), "read-back differs from PUT — STOP"
    print(f"read-back sha256={sha(wb)} — MATCH")

    # 5. Live HTTP verification of the staged routes.
    for path, want in [("/", free_index), ("/free", new_entry),
                       ("/free/walk", walk)]:
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

    # 6. Pricing v78 still byte-exact on its own staging worker (untouched).
    st, _, v78 = _sim.http_get(PRICING_HOST + "/")
    assert st == 200 and sha(v78) == PRICING_V78_SHA, "pricing v78 MOVED — STOP"
    print(f"pricing v78: {len(v78)} B sha={sha(v78)[:8]}... UNCHANGED")

    print("BUILD+STAGE OK")
    print(f"  walk sha256={sha(walk)} (UNCHANGED)")
    print(f"  entry sha256={sha(new_entry)}")
    print(f"  worker sha256={sha(new_worker)}")
    print(f"  sw.js sha256={sha(sw)} ({len(sw.encode())} B, live verbatim)")
    print(f"  manifest sha256={sha(mani)} ({len(mani.encode())} B, live verbatim)")
    return {"walk": walk, "entry": new_entry, "free_index": free_index,
            "worker": new_worker, "sw": sw, "manifest": mani}


if __name__ == "__main__":
    main()
