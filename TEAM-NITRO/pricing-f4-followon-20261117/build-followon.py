#!/usr/bin/env python3
"""Pricing F4-FOLLOWON (2026-11-17): Marcellus font + certificate narrow +
start over + certificate layered type (Newsreader).

BASE (verified first, fail-stop if moved): the F4-fix staged bytes —
  walk 3,291,949 B sha 04ec6218… · entry 307,918 B sha e0534a61… ·
  worker 3,619,556 B sha 83aa4090… · pricing v78 UNCHANGED (never touched).
Regenerates the base in memory (F4 builder + F4 fix functions) and asserts
the base shas before patching anything.

ITEM 1 — MARCELLUS ON THE WALK. Finding (proven, not guessed): the live
walk's /welcome names Marcellus,Georgia,serif 7 times but loads it NOWHERE
(0 @font-face, 0 Google Fonts links, 0 @import on /welcome itself). The
loading lives on the walk worker's MAIN ENTRANCE (/): a verbatim Google
Fonts link — preconnect + css2?family=Marcellus&family=Outfit:wght@... —
so /welcome renders Marcellus from that page's load/cache. The staged free
walk lost both the family AND the loading in the F4 regeneration. Restore:
  (a) the entrance's link tag, VERBATIM, into the free walk's <head>;
  (b) font-family:Marcellus,Georgia,serif on the walk's display type —
      .p3-question (headlines), .p3-congrats (end-slide headline),
      .p3-welcome (intro paragraphs) — the live walk's Marcellus uses are
      headlines (30/24px) + intro/letter beats (19px), so these three base
      rules are the faithful mapping (the live walk's .deal-*/.letter-beat
      classes do not exist in the free walk's older source).
  No new font treatment invented: same stack string, same loading URL.

ITEM 2 — /free CERTIFICATE AT NARROW WIDTHS. Root cause (from the served
bytes): the certified document is a fixed 3-row grid
(.identity-face absolute, rows 0.84fr/auto/1.16fr, plaque overflow:hidden).
At 635x349 the face is ~235px tall while the certified content is ~460px:
the head row (0.74fr ≈ 66px) cannot hold seal 94px + title + certifies, so
the head's overflowing content paints down over the giant name; the foot
row (1.26fr ≈ 113px) cannot hold status + 2 boxes + regalia + ENTER
(~230px), so ENTER is pushed below the plaque edge and clipped — invisible.
The regalia line (Nº + date ≈ 570px at desktop spacing) is a single flex
row that cannot fit 354px at 390px wide. Fix, certified state only,
desktop untouched (every rule below is gated on narrow width or short
viewport — 1919x998 matches neither):
  (a) max-width:640px — the regalia stacks (column, dot hidden), each line
      centered, letter-spacing tightened; no side-by-side collision possible.
  (b) max-height:700px — the certified face leaves the fixed grid and
      becomes normal flow (static flex column, centered, min-height:100%)
      inside a scrolling plaque (overflow-y:auto); seal steps down to 72px.
      Content that cannot fit scrolls instead of overlapping; ENTER stays
      in flow and reachable. When content fits, nothing scrolls and the
      composition reads the same.
  Nothing else moves: same copy, same boxes, same seal, same ENTER.

ITEM 3 — START OVER. Finding (proven): the walk persists in localStorage —
  nayanet_smart_alias / nayanet_smart_name / nayanet_vault_key (identity),
  naya_welcome_right_v1 (answers + reveal), nayanet_free_entry (flag);
  sessionStorage nayanet_user_name + nayanet_pending_route. Boot with a
  saved reveal jumps to the end slide; ?reset=1 does nothing (no reset
  handling anywhere — the only 'reset' hits are the F4 resetNamesEnter).
  The control: a small quiet "Use a different alias" ghost button under
  ENTER on /free, visible ONLY in the certified state (CSS-gated on
  .cert-plaque.is-certified — no JS hook into the stamp/restore paths, so
  it is correct in both). Click clears exactly the six identity/walk keys
  + the two session keys and reloads: /free boots back to the composing
  claim form, a new alias can be claimed, ENTER hands a fresh walk at
  step 1. The old alias stays claimed in the registry (its row is never
  deleted); this device simply forgets it — the device key is minted fresh
  on the next claim, as activateAndRedirect already does for a missing key.

ITEM 4 — CERTIFICATE LAYERED TYPE (amendment 02:08Z). Findings (proven):
  (a) /free's --serif is 'Newsreader', Georgia, 'Times New Roman', serif
      (9 var(--serif) uses) — but Newsreader is NOT web-loaded anywhere
      (0 @font-face, 0 webfont links on /free AND on the walk worker's
      /identity.html); the certificate renders in Georgia today. Memory
      already recorded this on 2026-10-21 ("Newsreader not web-loaded —
      Georgia renders"). Load it properly: preconnect + Google Fonts css2
      for Newsreader (ital,opsz,wght ranges covering 400-700 + italic,
      which the certificate uses) into /free's <head>. Verified live:
      css2 200 (6 @font-face blocks, italic included), latin woff2 200,
      146,872 B, wOF2 magic.
  (b) ONE serif for the certificate: the canonical layered certificate is
      /free (identity v2.4, Shawn-accepted 2026-10-20, SN-2922 bar:
      official, glowing, solid) — its serif is Newsreader. The walk
      worker's /identity.html defines the SAME --serif (verified read-only,
      out of scope, already aligned). The staged walk holds NO certificate
      card (0 cert-* classes; the live walk's Marcellus lives on the
      DEAL/agreement presentation, not a certificate), so there is no
      second certificate serif in scope to align — the walk's display type
      stays Marcellus per item 1, the certificate's type stays Newsreader
      per this item, each canonical in its own file. If the captain wants
      the walk's end-slide headline in Newsreader too, that is one line;
      it is flagged, not silently decided.

Builds entirely in memory (EPERM flake) and stages to
naya-pricing-free-staging ONLY. Pricing worker NOT touched.
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
F4FIX = os.path.expanduser("~/workspace/team-nitro/pricing-f4-fix-20261117")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_bf = load("bfree", os.path.join(F4, "build-free-staging-worker.py"))
_fix = load("ffix", os.path.join(F4FIX, "build-fix.py"))
_sim = load("sim", os.path.join(F4, "stage-in-memory.py"))
replace_once = _bf.replace_once

FREE_HOST = "https://naya-pricing-free-staging.nayapower.workers.dev"
PRICING_HOST = "https://naya-pricing-f4-staging.nayapower.workers.dev"

BASE_WALK_SHA = "04ec6218783e949690cb832c57e5d02e38ed304e7f2f164ddea8b67167c6ba78"
BASE_ENTRY_SHA = "e0534a61441dd6f4f643b79a74a9d1a8479c8c41cb2d6abf126d3b7fd87eb1ab"
BASE_WORKER_SHA = "83aa4090852cb3fd58dfaaaccb337d428662a2b88ff9314caf803d1ec1678cbc"
PRICING_V78_SHA = "ca2eafeb896c763ae2459b4a10b8715e726765ced607c0aab3640d27e6c39ae2"


def sha(b):
    return hashlib.sha256(b if isinstance(b, bytes) else b.encode()).hexdigest()


# ---------------------------------------------------------------- ITEM 1
# Verbatim harvest: the live walk worker's main entrance (/) loads Marcellus
# (+ Outfit, unused by the walk — rides along verbatim, its woff2 never
# downloads since no rule names it).
MARCELLUS_LINKS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    ' <link href="https://fonts.googleapis.com/css2?family=Marcellus'
    '&family=Outfit:wght@300;400;600;700;800;900&display=swap" rel="stylesheet">\n '
)


def apply_item1_walk(w):
    # (a) the loading, verbatim, into <head>.
    w = replace_once(w, "</head>", MARCELLUS_LINKS + "</head>", "I1a font links")
    # (b) the family on the display type — base rules only; the media rules
    # only change size/margin, so the family carries through them.
    w = replace_once(w, ".p3-question{font-size:clamp(1.7rem,5.5vw,2.3rem);",
                     ".p3-question{font-family:Marcellus,Georgia,serif;"
                     "font-size:clamp(1.7rem,5.5vw,2.3rem);", "I1b question")
    w = replace_once(w, ".p3-congrats{font-size:26px;",
                     ".p3-congrats{font-family:Marcellus,Georgia,serif;font-size:26px;",
                     "I1b congrats")
    w = replace_once(w, ".p3-welcome{font-size:15px;",
                     ".p3-welcome{font-family:Marcellus,Georgia,serif;font-size:15px;",
                     "I1b welcome")
    return w


# ---------------------------------------------------------------- ITEMS 2+3+4 (entry)
CERT_CSS = (
    "/* FREE CERT (F4-FOLLOWON 2026-11-17): certified document reads clean "
    "at 390/635px. Desktop untouched — every rule is gated on narrow width "
    "or a short viewport, certified state only. */\n    "
    "#startOverBtn{display:none;margin:10px auto 0;padding:10px 18px;"
    "min-height:40px;border-radius:999px;background:transparent;"
    "border:1.5px solid rgba(255,255,255,.55);color:#fff;"
    "font-family:var(--sans);font-size:.8rem;font-weight:700;"
    "letter-spacing:.12em;text-transform:uppercase;cursor:pointer}\n    "
    "#startOverBtn:hover{border-color:#fff}\n    "
    "#startOverBtn:active{transform:scale(.97)}\n    "
    ".cert-plaque.is-certified #startOverBtn{display:inline-flex;"
    "align-items:center;justify-content:center}\n    "
    "@media (max-width:640px){\n    "
    "  .cert-plaque.is-certified .cert-regalia{flex-direction:column;gap:2px 0}\n    "
    "  .cert-plaque.is-certified .cert-regalia .regalia-dot{display:none}\n    "
    "  .cert-plaque.is-certified .cert-no{letter-spacing:.18em;text-indent:.18em}\n    "
    "  .cert-plaque.is-certified .cert-date{letter-spacing:.14em;text-indent:.14em}\n    "
    "}\n    "
    "@media (max-height:700px){\n    "
    "  .cert-plaque.is-certified{overflow-y:auto}\n    "
    "  .cert-plaque.is-certified .identity-face{position:static;display:flex;"
    "flex-direction:column;justify-content:center;min-height:100%;"
    "box-sizing:border-box}\n    "
    "  .cert-plaque.is-certified .face-head,.cert-plaque.is-certified "
    ".face-foot{align-self:auto}\n    "
    "  .cert-plaque.is-certified .face-foot{margin-top:16px}\n    "
    "  .cert-plaque.is-certified .cert-seal{width:72px;height:72px}\n    "
    "  .cert-plaque.is-certified .cert-jewels{margin-top:6px}\n    "
    "}\n    "
)

# Item 3: the control. Sits under ENTER (before the free-line, which is
# hidden in the certified state, so visually it is directly under ENTER).
# Clears exactly the identity + walk state, then reloads into composing.
START_OVER_HTML = (
    '<button type="button" class="start-over-btn" id="startOverBtn">'
    'Use a different alias</button>\n        '
    '<script>(function(){var b=document.getElementById(\'startOverBtn\');'
    'if(!b)return;b.addEventListener(\'click\',function(){try{'
    '[\'nayanet_smart_alias\',\'nayanet_smart_name\',\'nayanet_vault_key\','
    '\'naya_welcome_right_v1\',\'nayanet_free_entry\'].forEach(function(k)'
    '{localStorage.removeItem(k);});'
    'sessionStorage.removeItem(\'nayanet_user_name\');'
    'sessionStorage.removeItem(\'nayanet_pending_route\');}catch(e){}'
    'window.location.reload();});})();</script>\n        '
)

# Item 4: Newsreader, properly web-loaded (ital + opsz + wght cover the
# certificate's 400-700 + italic). --serif itself is UNCHANGED.
NEWSREADER_LINKS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '   <link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400..700;1,6..72,400..700&display=swap" rel="stylesheet">\n   '
)


def apply_entry_followon(d):
    # Item 4: the loading, before </head> (anchor: the apple-touch-icon line).
    d = replace_once(
        d,
        '<link rel="apple-touch-icon" href="icons/apple-touch-icon.png" />',
        '<link rel="apple-touch-icon" href="icons/apple-touch-icon.png" />\n   '
        + NEWSREADER_LINKS.rstrip(),
        "I4 Newsreader links")
    # Items 2+3: CSS before the single </style>.
    assert d.count("</style>") == 1
    d = d.replace("</style>", CERT_CSS + "</style>", 1)
    assert "startOverBtn" in d and "max-height:700px" in d
    # Item 3: the control under ENTER.
    d = replace_once(d, '<p class="cert-claim free-line">',
                     START_OVER_HTML + '<p class="cert-claim free-line">',
                     "I3 start-over control")
    return d


def main():
    # 0. Regenerate the F4-fix base in memory; fail-stop if it moved.
    walk_f4 = _fix.apply_walk_fixes(_bf.build_walk_free())
    entry_f4 = _bf.build_free_entry()
    worker_f4 = _fix.apply_worker_fix(_bf.build_worker(walk_f4, entry_f4))
    assert sha(walk_f4) == BASE_WALK_SHA, f"base walk moved: {sha(walk_f4)}"
    assert sha(entry_f4) == BASE_ENTRY_SHA, f"base entry moved: {sha(entry_f4)}"
    assert sha(worker_f4) == BASE_WORKER_SHA, f"base worker moved: {sha(worker_f4)}"
    print(f"base verified: walk {len(walk_f4.encode())} B sha={sha(walk_f4)[:8]}… "
          f"entry {len(entry_f4.encode())} B sha={sha(entry_f4)[:8]}… "
          f"worker {len(worker_f4.encode())} B sha={sha(worker_f4)[:8]}…")

    walk = apply_item1_walk(walk_f4)
    entry = apply_entry_followon(entry_f4)
    free_index = _bf.FREE_INDEX.replace(
        "__PRICING_STAGED__", "https://naya-pricing-f4-staging.nayapower.workers.dev/")
    worker = _fix.apply_worker_fix(_bf.build_worker(walk, entry))
    print(f"walk follow-on: {len(walk.encode())} B sha256={sha(walk)}")
    print(f"entry follow-on: {len(entry.encode())} B sha256={sha(entry)}")
    print(f"worker follow-on: {len(worker.encode())} B sha256={sha(worker)}")
    import gzip
    gz = gzip.compress(worker.encode("utf-8"))
    print(f"worker gzip: {len(gz)} B (limit 10,485,760)")
    assert len(gz) < 10485760

    # Markers: new present, old-code intact where it must be.
    for good in ["fonts.googleapis.com/css2?family=Marcellus",
                 "font-family:Marcellus,Georgia,serif",
                 ".p3-question{font-family:Marcellus",
                 ".p3-congrats{font-family:Marcellus",
                 ".p3-welcome{font-family:Marcellus",
                 "css2?family=Newsreader:ital,opsz,wght",
                 "--serif: 'Newsreader', Georgia, 'Times New Roman', serif",
                 "id=\"startOverBtn\"", "Use a different alias",
                 "naya_welcome_right_v1", "nayanet_pending_route",
                 ".cert-plaque.is-certified .cert-regalia{flex-direction:column",
                 ".cert-plaque.is-certified{overflow-y:auto}",
                 "position:static;display:flex;flex-direction:column"]:
        assert good in (walk + entry), f"marker missing: {good}"
    for keep in ["buildBarFill", "25000", "showStep(16)",
                 "The build timed out after 25 seconds",
                 "WALKTHROUGH_URL = '/free/walk'",
                 "Enter free &mdash; no payment, no card."]:
        assert keep in (walk + entry), f"F4 marker lost: {keep}"
    # No Marcellus on the certificate, no Newsreader on the walk: each file
    # keeps its own canonical serif.
    assert "Marcellus" not in entry, "Marcellus leaked onto the certificate"
    assert "Newsreader" not in walk, "Newsreader leaked onto the walk"
    assert entry.count("var(--serif)") == 9, "cert serif uses changed"
    print("markers: HAVE all; serif separation holds (walk Marcellus only, "
          "cert Newsreader only); F4 markers intact")

    # Newsreader actually loads: css2 + latin woff2, live, right now.
    st, _, css = _sim.http_get(
        "https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400..700;1,6..72,400..700&display=swap")
    assert st == 200 and b"font-family: 'Newsreader'" in css
    import re
    m = re.search(rb"/\* latin \*/\s*@font-face \{[^}]*src: url\((https://[^)]+\.woff2)\)", css)
    assert m, "no latin Newsreader woff2 in css2"
    st2, _, woff = _sim.http_get(m.group(1).decode())
    assert st2 == 200 and woff[:4] == b"wOF2", f"woff2 fetch: {st2}"
    print(f"Newsreader loads: css2 200 ({len(css)} B, {css.count(b'@font-face')} faces), "
          f"latin woff2 200 ({len(woff)} B, wOF2 magic)")

    # Node driver: the real fetch handler serves the new walk + entry.
    _sim.node_check(worker, FREE_HOST + "/free/walk", sha(walk),
                    ["fonts.googleapis.com/css2?family=Marcellus",
                     "font-family:Marcellus,Georgia,serif",
                     ".p3-congrats{font-family:Marcellus",
                     "buildBarFill", "showStep(16)"],
                    ["font-family:Marcellus,Georgia,serif;font-size:26px;font-weight:800;letter-spacing:.01em;text-align:center;margin:14px 0 10px;color:#fff;text-shadow:0 2px 6px rgba(0,0,0,.85),0 0 18px rgba(160,107,255,.45),0 1px 0 rgba(0,0,0,.9),0 -1px 0 rgba(255,255,255,.10)}"])
    _sim.node_check(worker, FREE_HOST + "/free", sha(entry),
                    ["css2?family=Newsreader:ital,opsz,wght",
                     "id=\"startOverBtn\"", "Use a different alias",
                     ".cert-plaque.is-certified .cert-regalia{flex-direction:column",
                     ".cert-plaque.is-certified{overflow-y:auto}",
                     "Enter free &mdash; no payment, no card.",
                     'id="freeEye"', "WALKTHROUGH_URL = '/free/walk'"],
                    ["Marcellus"])
    _sim.node_check(worker, FREE_HOST + "/", sha(free_index),
                    ["Enter free — the route, staged"], [])
    _sim.node_redirect_check(worker, FREE_HOST + "/free/hub",
                             "https://nayanet.app/")
    print("node driver: PASS (new walk + new entry + index + hub)")

    # Stage the follow-on free worker (STAGING ONLY — pricing untouched).
    kv = [{"type": "kv_namespace", "name": "WELCOME_ASSETS",
           "namespace_id": "1cf80db6183245d19dd5296645a12bd0"}]
    _sim.put_worker("naya-pricing-free-staging", worker.encode(), kv)
    status, raw = _sim.api("GET", "/naya-pricing-free-staging")
    assert status == 200
    _, wb, _ = _sim.split_multipart(raw)
    assert wb == worker.encode(), "read-back differs from PUT — STOP"
    print(f"read-back sha256={sha(wb)} — MATCH")

    # Live HTTP verification of the staged routes.
    for path, want in [("/", free_index), ("/free", entry),
                       ("/free/walk", walk)]:
        st, _, got = _sim.http_get(FREE_HOST + path)
        assert st == 200, f"GET {path}: {st}"
        assert got.decode("utf-8") == want, f"GET {path}: bytes != source — STOP"
        print(f"GET {FREE_HOST}{path}: 200, {len(got)} B == source MATCH")
    st, hdrs, _ = _sim.http_get(FREE_HOST + "/free/hub")
    assert st in (301, 302) and hdrs.get("Location") == "https://nayanet.app/"
    print("GET /free/hub: 302 -> https://nayanet.app/ MATCH")

    # Pricing v78 still byte-exact on its own staging worker (untouched).
    st, _, v78 = _sim.http_get(PRICING_HOST + "/")
    assert st == 200 and sha(v78) == PRICING_V78_SHA, "pricing v78 MOVED — STOP"
    print(f"pricing v78: {len(v78)} B sha={sha(v78)[:8]}… UNCHANGED")

    # API: fresh test alias through the real claim (like /free does:
    # {alias, name, device_key}).
    alias = "f4followon" + "".join(random.choices(string.ascii_lowercase, k=8))
    device_key = "nayanet_key_" + "".join(random.choices(string.ascii_lowercase + string.digits, k=13))
    st, out = _sim.http_post_json(
        FREE_HOST + "/api/claim",
        {"alias": alias, "name": "F4 Followon Test", "device_key": device_key})
    assert st in (200, 201), f"POST claim: {st} {out[:200]}"
    claim = json.loads(out.decode())
    print(f"POST /api/claim ({alias}): {st} {out[:200].decode()}")
    st, _, out = _sim.http_get(FREE_HOST + f"/api/claim?alias={alias}")
    assert st == 200
    row = json.loads(out.decode())
    assert row.get("exists") is True
    print(f"claim read-back: exists, cert_no={row.get('cert_no')}, "
          f"created={row.get('created_at')}")

    print("BUILD+STAGE OK")
    print(f"  walk sha256={sha(walk)}")
    print(f"  entry sha256={sha(entry)}")
    print(f"  worker sha256={sha(worker)}")
    print(f"  test alias (KV + Supabase row, to clean): {alias} "
          f"cert_no={row.get('cert_no')}")
    return {"walk": walk, "entry": entry, "free_index": free_index,
            "worker": worker, "alias": alias,
            "cert_no": row.get("cert_no")}


if __name__ == "__main__":
    main()
