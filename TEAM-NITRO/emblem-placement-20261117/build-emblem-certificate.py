#!/usr/bin/env python3
"""Emblem Placement — CERTIFICATE (2026-11-17, Shawn's word 21:08Z).

Places the official emblem (NAYA_ICON.png, verbatim) in the four corners
of the staged /free certificate, each corner ON AN ANGLE — the settled
corner law (Shawn 2026-11-17 20:57Z, AGENTS.md: "The corner jewels don't
look super clear — use the original in the spots so you get the clear nice
icon... in each corner ON AN ANGLE"; the emblem "goes on certificates,
documents, and official areas").

BASE (reproduced in memory first, fail-stop if moved): the
certificate-fix tip — entry 335,915 B sha fbd6477f... (branch
pricing/certificate-fix-20261117, tip 7299a57c, PR #3429 open, UNMERGED).

THE CHANGE (one idea: the emblem IS the corner seal):
  E1  .crest-full (the desktop filigree webp) -> display:none at all sizes.
      The emblem itself is a complete crest (crown + wings + diamond +
      star + teardrop); showing the filigree AND the emblem would be two
      crests stacked — doubling up, against the sense check.
  E2  .crest-medal (the mobile JPEG medal, display:none on desktop) ->
      display:block at ALL sizes, background = the emblem PNG verbatim
      (base64 data URI, center / contain), border-radius REMOVED (the
      emblem is not circular — a 50% radius would clip the crown wings,
      the star above and the teardrop below), drop-shadow elevation
      (harvested from the mobile rule) at all sizes.
  Kept byte-identical: the four .corner-crest slots, their positions
  (20px desktop / 15px mobile) and their rotations (desktop tl -59deg,
  tr 59deg, bl -121deg, br 121deg; mobile +-35deg / +-145deg) — the
  emblem inherits the angle; the ::before pooled shadow beneath each
  corner (seats the emblem as a real object); the mobile @media block
  (its display:none / display:block lines are now redundant but kept,
  untouched); the crystal-N seal, the five stones, the title, the
  certifies line, the solid white name, the agreement line + reader,
  the ENTER claim path — NOTHING else moves. No rendered word changes.
  No orbit ring on the corners: a seal is stamped, not spun (the
  existing crest never orbited); the angle + elevation carry the life.

EMBLEM SOURCE: ~/workspace/user/media_library/image/NAYA_ICON.png,
2,654,505 B, 1800x2000 PNG, sha256
1e3deb55ae00552a2cbe26baaa610e04dc91812b6bc68c3532a061be020c8bf4.
Read from disk, base64-encoded in memory, hash-proven on decode.
ICON_LOGO.png is a different, earlier render — NOT used.

Builds entirely in memory and stages to naya-pricing-free-staging ONLY.
Walk unchanged. Pricing v78 untouched. Identity page untouched (its own
branch). Nothing live, no merge.
"""
import base64
import difflib
import gzip
import hashlib
import importlib.util
import os
import re
import sys

sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
sys.path.insert(0, os.path.expanduser("~/workspace/ninaya/integration"))

CURDIR = os.path.expanduser("~/workspace/team-nitro/pricing-certificate-current-20261117")
FIXDIR = os.path.expanduser("~/workspace/team-nitro/pricing-certificate-fix-20261117")
HERE = os.path.expanduser("~/workspace/team-nitro/emblem-placement-20261117")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_cur = load("certcurrent", os.path.join(CURDIR, "build-certificate.py"))
_bt = _cur._bt
_bf = _bt._bf
_fix = _bt._fix
_fo = _bt._fo
_marc = _bt._marc
_sim = _bt._sim
replace_once = _bf.replace_once

# The certificate-fix round's build module, for the fixed entry chain.
_fixmod = load("certfix", os.path.join(FIXDIR, "build-fix.py"))

FREE_HOST = "https://naya-pricing-free-staging.nayapower.workers.dev"
PRICING_HOST = "https://naya-pricing-f4-staging.nayapower.workers.dev"
LIVE = "https://nayanet.app"
IDENTITY_HOST = "https://naya-walk-beginning-staging.nayapower.workers.dev"

BASE_WALK_SHA = "46bc52e54ac02e87cdad0ae2924ce35555671333ce3c7cd96676f17d86253fa1"
BASE_ENTRY_SHA = "fbd6477f348ab50b8b0eb278fb36e475c25eb55ae27a4d79ca416942161f16fd"
BASE_WORKER_SHA = "041c8a5944f3b52f017185ca522498b0df12aafe246f3baa0bcdd27efc9eb2f3"
IDENTITY_SHA = "8c641f96d31818b610d1a243d945dfb5c68e6016e036b7afb11b72445330013d"
PRICING_V78_SHA = "ca2eafeb896c763ae2459b4a10b8715e726765ced607c0aab3640d27e6c39ae2"
SW_SHA = "abac2ab507fc162788d9bdcd60f895049222e125d1445a4870be71342625d6a3"
MANI_SHA = "b4abd81c41e85f4149be355f740dd8ff9b136f6ea85e8b5874073a0686c67e81"

EMBLEM_PATH = os.path.expanduser("~/workspace/user/media_library/image/NAYA_ICON.png")
EMBLEM_SHA = "1e3deb55ae00552a2cbe26baaa610e04dc91812b6bc68c3532a061be020c8bf4"
EMBLEM_BYTES = 2654505


def sha(b):
    return hashlib.sha256(b if isinstance(b, bytes) else b.encode()).hexdigest()


def emblem_b64():
    raw = open(EMBLEM_PATH, "rb").read()
    assert len(raw) == EMBLEM_BYTES, f"emblem moved: {len(raw)} B"
    assert sha(raw) == EMBLEM_SHA, f"emblem sha moved: {sha(raw)}"
    b64 = base64.b64encode(raw).decode("ascii")
    assert sha(base64.b64decode(b64)) == EMBLEM_SHA, "emblem b64 round-trip FAILED"
    print(f"emblem: {len(raw)} B sha={EMBLEM_SHA[:8]}... b64 {len(b64)} chars, round-trip MATCH")
    return b64


def apply_emblem(base_entry, b64):
    """E1+E2 on the certificate entry. Every replacement asserted."""
    new = base_entry
    # --- E1: the desktop filigree crest goes dark at all sizes.
    m = re.search(
        r"    \.crest-full \{ position: absolute; inset: 0; display: block;\n"
        r"      background: url\(\"data:image/webp;base64,[^\"]+\"\) center / contain no-repeat; \}",
        new)
    assert m, "crest-full rule NOT FOUND — STOP"
    new = new[:m.start()] + (
        "    /* EMBLEM PLACEMENT (2026-11-17, Shawn 21:08Z + the corner law\n"
        "       20:57Z): the official emblem sits in each corner, ON AN ANGLE.\n"
        "       The filigree crest-full goes dark — the emblem itself is a\n"
        "       complete crest (crown + wings + diamond + star + teardrop);\n"
        "       filigree AND emblem would be two crests stacked. The medal\n"
        "       below carries the emblem at all sizes, on the corner's own\n"
        "       rotation (desktop +-59deg / +-121deg, mobile +-35deg / +-145deg). */\n"
        "    .crest-full { display: none; }"
    ) + new[m.end():]
    # --- E2: the medal carries the emblem verbatim, at all sizes.
    m = re.search(
        r"    \.crest-medal \{ display: none; width: 100%; height: 100%; border-radius: 50%;\n"
        r"      background: url\(\"data:image/jpeg;base64,[^\"]+\"\) center / cover no-repeat; \}",
        new)
    assert m, "crest-medal rule NOT FOUND — STOP"
    new = new[:m.start()] + (
        "    .crest-medal { display: block; width: 100%; height: 100%;\n"
        "      background: url(\"data:image/png;base64," + b64 + "\") center / contain no-repeat;\n"
        "      filter: drop-shadow(0 6px 12px rgba(0,0,0,0.60)); }"
        " /* EMBLEM PLACEMENT (2026-11-17): NAYA_ICON.png verbatim —\n"
        "       never redrawn, never re-derived. border-radius removed: the\n"
        "       emblem is not circular, a 50% radius would clip the crown\n"
        "       wings, the star above and the teardrop below. contain shows\n"
        "       the whole emblem; the drop-shadow (harvested from the mobile\n"
        "       rule) seats it as a real object. */"
    ) + new[m.end():]
    return new


def check_invariants(base, new, b64):
    # The emblem is in, exactly once per corner slot (one shared rule).
    assert new.count("data:image/png;base64," + b64[:120]) == 1, "emblem b64 not exactly x1"
    assert "data:image/png;base64," in new
    assert new.count("data:image/png;base64,") == 1, "more than one png data URI — STOP"
    # Old corner art gone from its rules.
    assert ".crest-full { display: none; }" in new
    assert ".crest-medal { display: block; width: 100%; height: 100%;" in new
    assert "border-radius: 50%;" not in new.split(".crest-medal")[1].split("}")[0], \
        "medal still circular — STOP"
    # The corner slots, positions and rotations are untouched.
    for frag in [
        ".corner-crest { position: absolute; z-index: 5; width: 100px; height: 122px;",
        ".cm-tl { top: 20px; left: 20px; transform: translate(-50%, -50%) rotate(-59deg); }",
        ".cm-tr { top: 20px; right: 20px; transform: translate(50%, -50%) rotate(59deg); }",
        ".cm-bl { bottom: 20px; left: 20px; transform: translate(-50%, 50%) rotate(-121deg); }",
        ".cm-br { bottom: 20px; right: 20px; transform: translate(50%, 50%) rotate(121deg); }",
        ".corner-crest { width: 54px; height: 54px; }",
        ".cm-tl { top: 15px; left: 15px; transform: translate(-50%, -50%) rotate(-35deg); }",
        ".cm-tr { top: 15px; right: 15px; transform: translate(50%, -50%) rotate(35deg); }",
        ".cm-bl { bottom: 15px; left: 15px; transform: translate(-50%, 50%) rotate(-145deg); }",
        ".cm-br { bottom: 15px; right: 15px; transform: translate(50%, 50%) rotate(145deg); }",
        ".corner-crest::before { content: \"\"; position: absolute; inset: 10% -6%;",
    ]:
        assert frag in new, f"corner slot moved: {frag[:70]} — STOP"
    # The certificate itself is untouched: title, certifies, name, agree, claim.
    for frag in [
        '<div class="cert-title">Certificate of the Collective Agreement</div>',
        "This certificate of the Collective Agreement certifies that",
        "color: #ffffff; /* CERTIFICATE FIX",
        "the Enter KEY claims",
        ".cert-plaque.is-certified .cert-agree { display: block;",
        "By entering your name, you make it official",
        'id="certInfoReader"',
        "paintHeroName",
        "--serif: Marcellus, Georgia, serif;",
        "WALKTHROUGH_URL = '/free/walk'",
    ]:
        assert frag in new, f"certificate piece moved: {frag[:60]} — STOP"
    # No other data-URI art touched: the seal JPEG and the crest webp are gone
    # only where the rules say (crest-full rule retired); the seal stays.
    assert new.count("data:image/jpeg;base64,") == base.count("data:image/jpeg;base64,") - 1, \
        "jpeg data-URI count wrong — the medal jpeg (x1) should be the only jpeg gone"
    assert 'class="cert-seal"' in new and 'class="logo-hero"' in new
    print("invariants: PASS (emblem x1, corners kept, certificate untouched)")


def main():
    b64 = emblem_b64()

    # 0a. Reproduce the certificate-fix tip in memory.
    walk_pf, entry_pf = _cur.regen_pricing_fix_tip()
    h = _cur.harvest_identity()
    base_entry = _cur.apply_certificate(entry_pf, h)
    assert sha(base_entry) == "1e1bb4894b3e4bffed026781ac08976e8353b0e2bb020652357f567a711b16a3", \
        f"certificate-current tip NOT reproduced: {sha(base_entry)} — STOP"
    fix_entry = _fixmod.apply_fix(base_entry, h)
    _fixmod.check_invariants(base_entry, fix_entry)
    assert sha(fix_entry) == BASE_ENTRY_SHA, \
        f"certificate-fix tip NOT reproduced: {sha(fix_entry)} — STOP"
    print(f"base reproduced: entry {len(fix_entry.encode())} B sha={sha(fix_entry)[:8]}... MATCH")

    # 0b. Live staged guards: /free + /free/walk + identity must serve the tip.
    st, _, live_entry = _sim.http_get(FREE_HOST + "/free")
    assert st == 200 and sha(live_entry) == BASE_ENTRY_SHA, \
        f"live staged /free moved: {st} {sha(live_entry)[:8]}... — STOP"
    st, _, live_walk = _sim.http_get(FREE_HOST + "/free/walk")
    assert st == 200 and sha(live_walk) == BASE_WALK_SHA, \
        f"live staged /free/walk moved: {st} {sha(live_walk)[:8]}... — STOP"
    st, _, live_id = _sim.http_get(IDENTITY_HOST + "/identity.html")
    assert st == 200 and sha(live_id) == IDENTITY_SHA, \
        f"live staged identity moved: {st} {sha(live_id)[:8]}... — STOP"
    print("live staged /free + /free/walk + identity == tip MATCH")

    # 0c. Harvest live PWA assets verbatim.
    st, _, sw = _sim.http_get(LIVE + "/sw.js")
    assert st == 200, f"live sw.js: {st}"
    sw = sw.decode("utf-8")
    assert sha(sw) == SW_SHA, f"sw.js moved: {sha(sw)}"
    st, _, mani = _sim.http_get(LIVE + "/manifest.webmanifest")
    assert st == 200, f"live manifest: {st}"
    mani = mani.decode("utf-8")
    assert sha(mani) == MANI_SHA, f"manifest moved: {sha(mani)}"
    print(f"harvested live PWA assets: sw.js {len(sw.encode())} B, manifest {len(mani.encode())} B")

    # 0d. Reproduce the CURRENT staged worker byte-exact before changing anything.
    st, raw = _sim.api("GET", "/naya-pricing-free-staging")
    assert st == 200, f"worker GET failed: {st}"
    _, wb, _ = _sim.split_multipart(raw)
    assert sha(wb) == BASE_WORKER_SHA, \
        f"live staged worker moved: {sha(wb)[:8]}... — STOP"
    free_index = _bf.FREE_INDEX.replace(
        "__PRICING_STAGED__", "https://naya-pricing-f4-staging.nayapower.workers.dev/")
    worker_cur = _cur.build_worker_for(walk_pf, fix_entry, sw, mani)
    assert sha(worker_cur) == BASE_WORKER_SHA, \
        f"current worker NOT reproduced: {sha(worker_cur)} — STOP"
    print(f"current worker reproduced: {len(worker_cur.encode())} B sha={sha(worker_cur)[:8]}... MATCH")

    # 1. Apply the emblem.
    new_entry = apply_emblem(fix_entry, b64)
    check_invariants(fix_entry, new_entry, b64)
    diff = list(difflib.unified_diff(fix_entry.splitlines(), new_entry.splitlines(), lineterm="", n=0))
    removed = [ln for ln in diff if ln.startswith("-") and not ln.startswith("---")]
    added = [ln for ln in diff if ln.startswith("+") and not ln.startswith("+++")]
    print(f"entry diff: +{len(added)} lines, -{len(removed)} lines")
    for ln in removed:
        print("   -", ln[:160])
    for ln in added:
        print("   +", ln[:160])
    print(f"new entry: {len(new_entry.encode())} B sha256={sha(new_entry)}")
    _cur.js_syntax_check(new_entry)

    # 2. Worker rebuild with the new entry (walk unchanged) + node driver.
    new_worker = _cur.build_worker_for(walk_pf, new_entry, sw, mani)
    print(f"new worker: {len(new_worker.encode())} B sha256={sha(new_worker)}")
    gz = gzip.compress(new_worker.encode("utf-8"))
    print(f"worker gzip: {len(gz)} B (limit 10,485,760)")
    assert len(gz) < 10485760

    _sim.node_check(new_worker, FREE_HOST + "/free", sha(new_entry),
                    ["EMBLEM PLACEMENT (2026-11-17",
                     ".crest-full { display: none; }",
                     ".crest-medal { display: block; width: 100%; height: 100%;",
                     "center / contain no-repeat",
                     "data:image/png;base64,",
                     "Certificate of the Collective Agreement",
                     "This certificate of the Collective Agreement certifies that",
                     "color: #ffffff; /* CERTIFICATE FIX",
                     "the Enter KEY claims",
                     ".cert-plaque.is-certified .cert-agree { display: block;",
                     "By entering your name, you make it official",
                     'id="certInfoReader"', 'id="certInfoBtn"',
                     "paintHeroName", "paintValues", "settleHeroName",
                     "--serif: Marcellus, Georgia, serif;",
                     'id="startOverBtn"',
                     "WALKTHROUGH_URL = '/free/walk'"],
                    [".crest-medal { display: none;",
                     "<div class=\"cert-title\">Certificate of Smart Identity</div>",
                     "Newsreader", "#f2f2f6", "#a8dcff", "#ffd97a",
                     "#163a56", "#0a1c2e", "#3a2a09", "#1c1204"])
    _sim.node_check(new_worker, FREE_HOST + "/free/walk", sha(walk_pf),
                    ["fonts.googleapis.com/css2?family=Marcellus",
                     "font-family:Marcellus,Georgia,serif",
                     ".p3-congrats{font-family:Marcellus",
                     "function adoptWalkName",
                     'id="enterBtn-names"',
                     "buildBarFill", "showStep(16)"],
                    ["Newsreader", "data:image/png;base64,"])
    _sim.node_check(new_worker, FREE_HOST + "/", sha(free_index),
                    ["Enter free — the route, staged"], [])
    _sim.node_check(new_worker, FREE_HOST + "/sw.js", sha(sw),
                    ["self-retiring", "skipWaiting", "unregister"], [])
    _sim.node_check(new_worker, FREE_HOST + "/manifest.webmanifest", sha(mani),
                    ["NayaNET", "start_url"], [])
    _sim.node_redirect_check(new_worker, FREE_HOST + "/free/hub",
                             "https://nayanet.app/")
    print("node driver: PASS (new entry + walk + index + sw.js + manifest + hub)")

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
                       ("/free/walk", walk_pf)]:
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

    # 6. No disk save (EPERM flake: truncate-first writes destroy files;
    # bytes live in memory + on the staged worker; the filing script
    # re-derives them in memory, never from disk).
    print("SKIP disk save (EPERM flake rule)")
    print("BUILD+STAGE OK")
    print(f"  walk sha256={sha(walk_pf)} (UNCHANGED)")
    print(f"  entry sha256={sha(new_entry)}")
    print(f"  worker sha256={sha(new_worker)}")
    print(f"  sw.js sha256={sha(sw)} ({len(sw.encode())} B, live verbatim)")
    print(f"  manifest sha256={sha(mani)} ({len(mani.encode())} B, live verbatim)")
    return {"walk": walk_pf, "entry": new_entry, "free_index": free_index,
            "worker": new_worker, "sw": sw, "manifest": mani}


if __name__ == "__main__":
    main()
