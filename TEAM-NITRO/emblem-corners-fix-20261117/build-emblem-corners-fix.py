#!/usr/bin/env python3
"""Emblem Corners Fix — CERTIFICATE (2026-11-17, eye 21:53-21:57Z).

Fixes the four corner emblems on the staged /free certificate, and
nothing else. Base: emblem/certificate-20261117 tip f23b6202, PR #3440
open unmerged, entry 3,801,588 B sha fbe04202... (the emblem placement
round — emblem verbatim in all four corners, on the angle).

THE EYE'S DEFECTS (each fixed, each asserted):
  D1 CLIPPED. The corner slots straddled the frame edge (20px inset +
      translate +/-50%) on a card that fills the screen edge to edge
      (overflow:hidden), so the rotated emblems were cut by the screen
      edges top-left / top-right, and the bottom pair sat partly below
      the fold. Fix (F1/F2): move the emblem CENTERS fully inside the
      card, by the measured rotated bounding box, at both sizes.
      Desktop box 100x122 -> 132x161, centers 20px -> 112px from each
      edge. Rotated bbox at 59 deg: halfW 103.0, halfH 98.0, so a 112px
      center leaves the emblem 9px inside the left/right edges and
      14px inside the top/bottom edges of the card. The card itself
      sits 52px below the top bar and 50px above the bottom bar, so
      the emblems are whole in the viewport at 1920x999 too.
      Mobile box 54x54 -> 64x64, centers 15px -> 56px. Rotated bbox
      at 35 deg: halfW = halfH = 44.6, so a 56px center leaves the
      emblem 11.4px inside every card edge at 635 and at 390.
  D2 THE BLACK SQUARE SHOWS AS A DIAMOND. NAYA_ICON.png is RGBA with
      0 transparent pixels and a pure-black background, so the rotated
      square read as a dark diamond against the near-black card. The
      file stays VERBATIM (never redrawn, never re-derived) — the cut
      is presentation-only (F3): an inline SVG filter (#crestCut)
      turns the artwork's own luminance into alpha with a steep ramp
      (alpha = clamp(6*lum - 0.15)): pure black (lum 0) goes fully
      transparent, the gem's median luminance (0.26) stays fully
      opaque, and the anti-aliased edge feathers instead of clipping.
      Chained after it, the same drop-shadow as before now follows
      the die-cut silhouette instead of the square, so the seal keeps
      its elevation. The mobile rule carries the same filter chain —
      a plain drop-shadow there would have undone the cut at <=640px.
  D3 THE SILVER SURROUND READS SMALL AND BUSY at desktop size; the
      teardrop barely legible. The purple diamond gem itself reads.
      Fix (F1): the emblem renders 132x147 desktop (was 100x111,
      +32%) and 58x64 mobile (was 48x54, +20%), same artwork, same
      angles. The surround and the teardrop get a third more pixels
      to read in.
  D4 THE CENTER SEAL IS THE MODEL — UNTOUCHED. The crystal-N seal,
      the heading, name, pills, number/date, ENTER button, agreement
      note and "USE A DIFFERENT ALIAS" do not change. Angles are the
      page's own corner law, byte-identical: desktop -59/+59/-121/
      +121 deg, mobile +/-35/+/-145 deg.
  F4 (found by the maker's own live probe, 22:10Z — see the report):
      at phone widths the foot text runs the full width down to 34px
      above the card bottom, so a whole bottom emblem would sit ON
      the foot's last lines. The clearance comes in two parts: the
      ROWS (auto auto 1fr at <=640px — the head keeps its row, the
      name keeps its row, and the foot pins to the top of its row
      instead of chasing the card height) and the CARD (min-height
      798px on tall phones — the foot does not move when the card
      grows, only the emblems move down, so the bottom emblems' top
      edge lands 7px below the foot's bottom). Padding alone cannot
      buy it — past ~179px it pushes the head down onto the name
      input (seen live at 280px). The old emblems overlapped the
      privacy line the same way (only half-clipped, so less visible)
      — this is a pre-existing overlap made fully visible by making
      the emblems whole, and F4 clears it rather than shipping it.

EMBLEM SOURCE: ~/workspace/user/media_library/image/NAYA_ICON.png,
2,654,505 B, 1800x2000 PNG, sha256
1e3deb55ae00552a2cbe26baaa610e04dc91812b6bc68c3532a061be020c8bf4.
Read from disk, base64-encoded in memory, hash-proven on decode.
The file is NOT re-encoded, NOT re-derived: the staged entry still
carries the exact bytes (the checker proves it from live bytes).

Builds entirely in memory and stages to naya-pricing-free-staging ONLY.
Walk unchanged. Pricing v78 untouched. Identity + unfold stay
SEQUENCED (do NOT stage them here). Nothing live, no merge.
"""
import base64
import difflib
import gzip
import hashlib
import importlib.util
import math
import os
import re
import sys

sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
sys.path.insert(0, os.path.expanduser("~/workspace/ninaya/integration"))

PREVDIR = os.path.expanduser("~/workspace/team-nitro/emblem-placement-20261117")
CURDIR = os.path.expanduser("~/workspace/team-nitro/pricing-certificate-current-20261117")
FIXDIR = os.path.expanduser("~/workspace/team-nitro/pricing-certificate-fix-20261117")
HERE = os.path.expanduser("~/workspace/team-nitro/emblem-corners-fix-20261117")


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

_fixmod = load("certfix", os.path.join(FIXDIR, "build-fix.py"))
_emb = load("embcert", os.path.join(PREVDIR, "build-emblem-certificate.py"))

FREE_HOST = "https://naya-pricing-free-staging.nayapower.workers.dev"
PRICING_HOST = "https://naya-pricing-f4-staging.nayapower.workers.dev"
LIVE = "https://nayanet.app"
IDENTITY_HOST = "https://naya-walk-beginning-staging.nayapower.workers.dev"

BASE_WALK_SHA = "46bc52e54ac02e87cdad0ae2924ce35555671333ce3c7cd96676f17d86253fa1"
BASE_ENTRY_SHA = "fbe042022c5d88559fa37317bed67aff89ea092929a65923d1688177a3d404ac"
BASE_WORKER_SHA = "d3d75854fdb791fb739c5cf53af9605a1515ba4aa12275c230f2578e6b6a43f6"
# v5 of THIS round (staged 22:31Z, rows auto auto 1fr + padding 160px):
# re-running the build must accept it as the live state, since the new
# bytes are re-derived from the base.
PREV_STAGED_SHA = "3860b7b66b8389c96f4ae7456e817339e004226267e6aa9404b83f3181aeee9b"
PREV_WORKER_SHA = "97f668369cae3e85dd955fe861891c9d3a82db7e69ef32f1cc16dcaf07ee0bbe"
IDENTITY_SHA = "8c641f96d31818b610d1a243d945dfb5c68e6016e036b7afb11b72445330013d"
PRICING_V78_SHA = "ca2eafeb896c763ae2459b4a10b8715e726765ced607c0aab3640d27e6c39ae2"
SW_SHA = "abac2ab507fc162788d9bdcd60f895049222e125d1445a4870be71342625d6a3"
MANI_SHA = "b4abd81c41e85f4149be355f740dd8ff9b136f6ea85e8b5874073a0686c67e81"

EMBLEM_PATH = os.path.expanduser("~/workspace/user/media_library/image/NAYA_ICON.png")
EMBLEM_SHA = "1e3deb55ae00552a2cbe26baaa610e04dc91812b6bc68c3532a061be020c8bf4"
EMBLEM_BYTES = 2654505

# Geometry (measured from the staged CSS, asserted in geometry_proof):
#   desktop box 132x161 at 59 deg -> halfW 103.0, halfH 98.0, center 112
#   mobile  box  64x64  at 35 deg -> halfW = halfH 44.6, center 56
#   top bar 52px, bottom bar 50px (the card fills the rest of the viewport)
DESK_BOX = (132, 161)
DESK_CENTER = 112
MOB_BOX = (64, 64)
MOB_CENTER = 56
TOP_BAR = 52
BOTTOM_BAR = 50

# The die-cut filter: luminance -> alpha, steep ramp.
#   alpha = clamp(6 * lum - 0.15): lum 0 -> 0 (the pure-black background
#   is cut away entirely); lum 0.025 -> 0; lum 0.26 (the purple gem's
#   median) -> 1 (fully opaque); the anti-aliased edge feathers.
FILTER_ID = "crestCut"
FILTER_SVG = (
    '      <!-- EMBLEM CORNERS FIX (2026-11-17, eye 21:53-21:57Z): the die-cut\n'
    '           filter for the corner emblems. The emblem file itself stays\n'
    '           verbatim — its pure-black background is cut away here, in\n'
    '           presentation only, by its own luminance: the filter turns\n'
    '           luminance into alpha (steep ramp, pure black fully\n'
    '           transparent, the gem fully opaque, the edge feathered),\n'
    '           so no square edge can read as a diamond. The drop-shadow\n'
    '           chained after it follows the cut silhouette, not the square. -->\n'
    '      <svg aria-hidden="true" focusable="false" width="0" height="0" '
    'style="position:absolute;width:0;height:0;overflow:hidden"><defs>'
    '<filter id="crestCut" x="-20%" y="-20%" width="140%" height="140%" '
    'color-interpolation-filters="sRGB"><feColorMatrix in="SourceGraphic" '
    'type="matrix" values="1 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0.2126 0.7152 0.0722 0 0"/>'
    '<feComponentTransfer><feFuncA type="linear" slope="6" intercept="-0.15"/>'
    '</feComponentTransfer></filter></defs></svg>\n'
)
FILTER_CHAIN = "filter: url(#crestCut) drop-shadow(0 6px 12px rgba(0,0,0,0.60));"
FILTER_PLAIN = "filter: drop-shadow(0 6px 12px rgba(0,0,0,0.60));"


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


def apply_corners_fix(base_entry, b64):
    """F1+F2+F3 on the staged emblem entry. Every replacement asserted."""
    new = base_entry
    # --- F0: the stale v2.3 comment claims a baked alpha melt and "no CSS
    # mask" — that was never true of the emblem (0 transparent pixels) and
    # the cut below is now exactly a presentation mask. Say so honestly.
    old_note = (
        "    /* The crest artwork carries its own baked alpha melt (radial +\n"
        "       luminance feather, pressed into the image itself) — no CSS mask,\n"
        "       no rectangle, in any browser. */\n"
    )
    assert old_note in new, "v2.3 crest comment NOT FOUND — STOP"
    new = new.replace(old_note, (
        "    /* The crest artwork is the official emblem, verbatim, on a\n"
        "       pure-black background with no baked transparency — so the cut\n"
        "       is done here, in presentation only, by the #crestCut filter\n"
        "       below (the emblem's own luminance becomes its alpha). No\n"
        "       rectangle edge can read, in any browser that honors the\n"
        "       filter; the file itself is never redrawn. */\n"
    ), 1)
    # --- F1: desktop geometry — bigger box, centers fully inside the card.
    old_slot = (".corner-crest { position: absolute; z-index: 5; "
                "width: 100px; height: 122px;")
    assert old_slot in new, "desktop corner slot NOT FOUND — STOP"
    new = new.replace(old_slot,
                      ".corner-crest { position: absolute; z-index: 5; "
                      "width: 132px; height: 161px;", 1)
    for old, new_rule in [
        (".cm-tl { top: 20px; left: 20px; transform: translate(-50%, -50%) rotate(-59deg); }",
         ".cm-tl { top: 112px; left: 112px; transform: translate(-50%, -50%) rotate(-59deg); }"),
        (".cm-tr { top: 20px; right: 20px; transform: translate(50%, -50%) rotate(59deg); }",
         ".cm-tr { top: 112px; right: 112px; transform: translate(50%, -50%) rotate(59deg); }"),
        (".cm-bl { bottom: 20px; left: 20px; transform: translate(-50%, 50%) rotate(-121deg); }",
         ".cm-bl { bottom: 112px; left: 112px; transform: translate(-50%, 50%) rotate(-121deg); }"),
        (".cm-br { bottom: 20px; right: 20px; transform: translate(50%, 50%) rotate(121deg); }",
         ".cm-br { bottom: 112px; right: 112px; transform: translate(50%, 50%) rotate(121deg); }"),
    ]:
        assert old in new, f"desktop corner rule NOT FOUND: {old[:60]} — STOP"
        new = new.replace(old, new_rule, 1)
    # --- F2: mobile geometry — bigger box, centers fully inside the card.
    old_mob_slot = ".corner-crest { width: 54px; height: 54px; }"
    assert old_mob_slot in new, "mobile corner slot NOT FOUND — STOP"
    new = new.replace(old_mob_slot, ".corner-crest { width: 64px; height: 64px; }", 1)
    for old, new_rule in [
        (".cm-tl { top: 15px; left: 15px; transform: translate(-50%, -50%) rotate(-35deg); }",
         ".cm-tl { top: 56px; left: 56px; transform: translate(-50%, -50%) rotate(-35deg); }"),
        (".cm-tr { top: 15px; right: 15px; transform: translate(50%, -50%) rotate(35deg); }",
         ".cm-tr { top: 56px; right: 56px; transform: translate(50%, -50%) rotate(35deg); }"),
        (".cm-bl { bottom: 15px; left: 15px; transform: translate(-50%, 50%) rotate(-145deg); }",
         ".cm-bl { bottom: 56px; left: 56px; transform: translate(-50%, 50%) rotate(-145deg); }"),
        (".cm-br { bottom: 15px; right: 15px; transform: translate(50%, 50%) rotate(145deg); }",
         ".cm-br { bottom: 56px; right: 56px; transform: translate(50%, 50%) rotate(145deg); }"),
    ]:
        assert old in new, f"mobile corner rule NOT FOUND: {old[:60]} — STOP"
        new = new.replace(old, new_rule, 1)
    # The stale mobile comment says the phone crest is a medallion alone —
    # since the emblem round the medal carries the whole emblem. Say so.
    old_mob_note = (
        "      /* Phone: the full crest turns to mush — the crest's diamond-heart\n"
        "         medallion alone carries the corners, same rotation law. */\n"
    )
    assert old_mob_note in new, "mobile crest comment NOT FOUND — STOP"
    new = new.replace(old_mob_note, (
        "      /* Phone: the whole emblem carries the corners, same rotation\n"
        "         law — 64px, centers 56px inside the card, so the emblem is\n"
        "         seen whole at 635 and at 390, with the same die-cut. */\n"
    ), 1)
    # --- F4: mobile foot clearance — the foot must end above the bottom
    # emblems, or a whole bottom emblem sits on the foot's last lines.
    # The bottom emblems' top edge is 56 + 44.6 = 100.6px above the card
    # bottom. Padding alone cannot buy the clearance: the foot is ~370px
    # tall in a ~233px grid row and moves up only about half as fast as
    # the padding grows — and past ~179px of padding the shrunken top
    # row pushes the head down onto the name input (seen live at 280px:
    # the title hid behind the input box). So the clearance comes from
    # the ROWS, not the padding: at <=640px the face's rows become
    # auto auto 1fr — the head keeps its own row, the name keeps its
    # row, and the foot pins to the top of its row (measured: the foot
    # top-aligns, its bottom then sits at a fixed 739px in the viewport
    # at 390x844 and does NOT move when the card grows). Padding stays
    # at 160px. The certified face keeps its own more-specific rows
    # (0.74fr auto 1.26fr, later in the same block), and the
    # short-viewport flex face ignores rows entirely. One rule, two
    # values — plus F4b below, which moves the emblems, not the foot.
    old_pad = ".identity-face { padding: 22px 18px 34px; }"
    assert new.count(old_pad) == 1, f"mobile face padding count wrong: {new.count(old_pad)} — STOP"
    new = new.replace(old_pad, (
        "      /* EMBLEM CORNERS FIX (2026-11-17): the foot clears the\n"
        "         bottom corner emblems — their top edge sits 101px above\n"
        "         the card bottom. The rows do the work: auto auto 1fr\n"
        "         gives the head its own row, the name its row, and the\n"
        "         foot the top of its row, so the foot pins and no foot\n"
        "         line ever runs under a seal; the 160px bottom padding\n"
        "         is the head-safe margin. Desktop needs none of this:\n"
        "         the foot there is narrow and centered, far from the\n"
        "         corners. */\n"
        "      .identity-face { padding: 22px 18px 160px; grid-template-rows: auto auto 1fr; }"
    ), 1)
    # --- F4b: tall phones — the card must be tall enough that the
    # bottom emblems (top edge 103px above the card bottom, probe-
    # measured) clear the foot, whose bottom is pinned at 739px in
    # the viewport by the auto rows (the foot does not move when the
    # card grows; only the emblems move down). min-height 798px puts
    # the emblems' top edge 7px below the foot and their bottom edge
    # 8px above the viewport bottom at 390x844 — the whole slack
    # there is 15px, split 7/8 (verified live by injecting the rule
    # into the staged v5 page before staging it: foot 396..739
    # unmoved, emblems 746..836). The card is in flow (the bottom
    # system bar is position:relative, the top bar sticky), so the
    # document scrolls ~90px and the bottom bar rides below the
    # fold; the certificate itself fits the first viewport. Scoped
    # to (max-width:640px) and (min-height:701px): at <=700px tall
    # the face is flex and the card must stay viewport-sized (the
    # flex content would chase the emblems down). Both the card and
    # the plaque carry it — the plaque fills the card, and the
    # emblems anchor to the plaque.
    anchor = "      .bottom-system-bar { font-size: 0.64rem; letter-spacing: 0.06em; padding: 0 10px; }\n    }"
    assert new.count(anchor) == 1, f"mobile block end anchor count wrong: {new.count(anchor)} — STOP"
    new = new.replace(anchor, anchor + (
        "\n    @media (max-width: 640px) and (min-height: 701px) {\n"
        "      /* EMBLEM CORNERS FIX (2026-11-17): tall phones — the card\n"
        "         is 798px tall at minimum so the bottom corner emblems\n"
        "         (top edge 103px above the card bottom) clear the foot,\n"
        "         whose bottom is pinned by the auto rows above. The foot\n"
        "         does not move when the card grows; only the emblems move\n"
        "         down. Short viewports are excluded: there the face is\n"
        "         flex and the card must stay viewport-sized. */\n"
        "      .identity-pro-card, #certPlaque { min-height: 798px; }\n"
        "    }"
    ), 1)
    # --- F3: the die-cut — the filter chain on BOTH medal rules (desktop
    # and mobile carry the identical plain drop-shadow text; both must
    # change, or the cut would silently vanish at <=640px).
    assert new.count(FILTER_PLAIN) == 2, \
        f"plain drop-shadow count wrong: {new.count(FILTER_PLAIN)} (want 2) — STOP"
    new = new.replace(FILTER_PLAIN, FILTER_CHAIN)
    assert new.count(FILTER_CHAIN) == 2, "filter chain count wrong — STOP"
    assert FILTER_PLAIN not in new, "plain drop-shadow left behind — STOP"
    # The filter defs themselves, right before the first corner slot.
    anchor = '      <div class="corner-crest cm-tl" aria-hidden="true">'
    assert anchor in new, "corner markup anchor NOT FOUND — STOP"
    assert 'id="crestCut"' not in new, "crestCut already present — STOP"
    new = new.replace(anchor, FILTER_SVG + anchor, 1)
    return new


def geometry_proof():
    """Rotated-bbox arithmetic for the new geometry (CSS-derived, not a
    render measurement — the live eye still judges the render)."""
    def bbox(w, h, deg):
        th = math.radians(abs(deg))
        return ((w * abs(math.cos(th)) + h * abs(math.sin(th))) / 2,
                (w * abs(math.sin(th)) + h * abs(math.cos(th))) / 2)
    # Desktop: 132x161 at 59 deg (121 deg has the same |cos|/|sin|).
    hw, hh = bbox(*DESK_BOX, 59)
    print(f"geometry desktop: box {DESK_BOX[0]}x{DESK_BOX[1]} at 59deg -> "
          f"halfW {hw:.1f} halfH {hh:.1f}; center {DESK_CENTER}px -> "
          f"clearance left/right {DESK_CENTER - hw:.1f}px, top/bottom "
          f"{DESK_CENTER - hh:.1f}px inside the card")
    assert DESK_CENTER - hw >= 8 and DESK_CENTER - hh >= 8, "desktop emblem not whole — STOP"
    # The pooled ::before shadow reaches 6% past the box sideways.
    assert DESK_CENTER - hw - 0.06 * DESK_BOX[0] >= 0, "pooled shadow past the card edge — STOP"
    # Viewport at 1920x999: card top = top bar, card bottom = viewport - bottom bar.
    assert TOP_BAR + (DESK_CENTER - hh) >= 0
    assert 999 - BOTTOM_BAR - (DESK_CENTER - hh) <= 999
    print(f"geometry desktop viewport 1920x999: emblem top edge at "
          f"y={TOP_BAR + DESK_CENTER - hh:.0f}, bottom edge at "
          f"y={999 - BOTTOM_BAR - (DESK_CENTER - hh):.0f} — whole in the first viewport")
    # Mobile: 64x64 at 35 deg (145 deg has the same |cos|/|sin|).
    hw, hh = bbox(*MOB_BOX, 35)
    print(f"geometry mobile: box {MOB_BOX[0]}x{MOB_BOX[1]} at 35deg -> "
          f"halfW {hw:.1f} halfH {hh:.1f}; center {MOB_CENTER}px -> "
          f"clearance {MOB_CENTER - hw:.1f}px inside the card on every side")
    assert MOB_CENTER - hw >= 8 and MOB_CENTER - hh >= 8, "mobile emblem not whole — STOP"
    for vw, vh in [(635, 390), (390, 844)]:
        print(f"geometry mobile viewport {vw}x{vh}: emblem left edge at "
              f"x={MOB_CENTER - hw:.1f}, right edge at x={vw - (MOB_CENTER - hw):.1f}, "
              f"top edge at y={TOP_BAR + MOB_CENTER - hh:.1f}, bottom edge at "
              f"y={vh - BOTTOM_BAR - (MOB_CENTER - hh):.1f} — whole in the card")
        assert MOB_CENTER - hw >= 0 and TOP_BAR + MOB_CENTER - hh >= 0
        assert vh - BOTTOM_BAR - (MOB_CENTER - hh) <= vh
    # Foot clearance (F4 + F4b): the foot pins at 739px in the viewport
    # at 390x844 (auto rows; measured live, it does not move when the
    # card grows), and the bottom emblems' top edge sits 103px above
    # the card bottom (probe-measured). With the card at min-height
    # 798px the emblem top lands at 51 + 798 - 103 = 746, 7px below
    # the foot, and the emblem bottom at 51 + 798 - 13 = 836, 8px
    # above the viewport bottom. The live probe measures the real
    # gap; this arithmetic is only the sanity floor.
    mob_half = bbox(*MOB_BOX, 35)[1]
    print(f"geometry mobile foot clearance: foot pinned at 739px, card "
          f"min-height 798px -> emblem top 746 (gap 7px), emblem bottom "
          f"836 (margin 8px); real gap probe-measured")
    assert 798 - 103 - (739 - 51) >= 0, "foot clearance too small — STOP"
    print("geometry_proof: PASS (desktop + mobile, 1920/635/390, CSS-derived)")


def check_invariants(base, new, b64):
    # The emblem is in, exactly once (one shared rule), byte-identical.
    assert new.count("data:image/png;base64," + b64[:120]) == 1, "emblem b64 not exactly x1"
    assert new.count("data:image/png;base64,") == 1, "more than one png data URI — STOP"
    assert sha(base64.b64decode(re.search(
        r'data:image/png;base64,([A-Za-z0-9+/=]+)', new).group(1))) == EMBLEM_SHA, \
        "emblem in new bytes != NAYA_ICON.png — STOP"
    # The die-cut is in, exactly once as defs, twice as the filter chain.
    assert new.count('id="crestCut"') == 1, "crestCut defs not exactly x1 — STOP"
    assert new.count(FILTER_CHAIN) == 2, "filter chain not on both medal rules — STOP"
    assert FILTER_PLAIN not in new, "plain drop-shadow left behind — STOP"
    assert 'feFuncA type="linear" slope="6" intercept="-0.15"' in new
    assert "no CSS mask" not in new, "stale 'no CSS mask' comment left behind — STOP"
    # New geometry in, old geometry out (exact rule strings).
    for frag in [
        ".corner-crest { position: absolute; z-index: 5; width: 132px; height: 161px;",
        ".cm-tl { top: 112px; left: 112px; transform: translate(-50%, -50%) rotate(-59deg); }",
        ".cm-tr { top: 112px; right: 112px; transform: translate(50%, -50%) rotate(59deg); }",
        ".cm-bl { bottom: 112px; left: 112px; transform: translate(-50%, 50%) rotate(-121deg); }",
        ".cm-br { bottom: 112px; right: 112px; transform: translate(50%, 50%) rotate(121deg); }",
        ".corner-crest { width: 64px; height: 64px; }",
        ".cm-tl { top: 56px; left: 56px; transform: translate(-50%, -50%) rotate(-35deg); }",
        ".cm-tr { top: 56px; right: 56px; transform: translate(50%, -50%) rotate(35deg); }",
        ".cm-bl { bottom: 56px; left: 56px; transform: translate(-50%, 50%) rotate(-145deg); }",
        ".cm-br { bottom: 56px; right: 56px; transform: translate(50%, 50%) rotate(145deg); }",
        ".crest-full { display: none; }",
        ".crest-medal { display: block; width: 100%; height: 100%;",
        ".corner-crest::before { content: \"\"; position: absolute; inset: 10% -6%;",
    ]:
        assert frag in new, f"new corner piece missing: {frag[:70]} — STOP"
    for frag in [
        "width: 100px; height: 122px;",
        ".corner-crest { width: 54px; height: 54px; }",
        "top: 20px; left: 20px;", "top: 20px; right: 20px;",
        "bottom: 20px; left: 20px;", "bottom: 20px; right: 20px;",
        "top: 15px; left: 15px;", "top: 15px; right: 15px;",
        "bottom: 15px; left: 15px;", "bottom: 15px; right: 15px;",
    ]:
        assert frag not in new, f"old corner geometry left behind: {frag} — STOP"
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
    assert 'class="cert-seal"' in new and 'class="logo-hero"' in new
    # F4: the mobile face carries the foot clearance; the old padding is gone.
    assert ".identity-face { padding: 22px 18px 160px; grid-template-rows: auto auto 1fr; }" in new, \
        "mobile foot clearance padding missing — STOP"
    assert "padding: 22px 18px 34px;" not in new, "old mobile face padding left — STOP"
    # F4b: tall phones — the card carries the min-height that moves the
    # emblems below the pinned foot; scoped away from short viewports.
    assert ".identity-pro-card, #certPlaque { min-height: 798px; }" in new, \
        "tall-phone card min-height missing — STOP"
    assert "@media (max-width: 640px) and (min-height: 701px)" in new, \
        "tall-phone media scope missing — STOP"
    print("invariants: PASS (emblem x1 verbatim, die-cut x1+x2, geometry new, certificate untouched)")


def main():
    b64 = emblem_b64()

    # 0a. Reproduce the emblem-placement tip in memory (the base of this round).
    walk_pf, entry_pf = _cur.regen_pricing_fix_tip()
    h = _cur.harvest_identity()
    base_entry = _cur.apply_certificate(entry_pf, h)
    assert sha(base_entry) == "1e1bb4894b3e4bffed026781ac08976e8353b0e2bb020652357f567a711b16a3", \
        f"certificate-current tip NOT reproduced: {sha(base_entry)} — STOP"
    fix_entry = _fixmod.apply_fix(base_entry, h)
    _fixmod.check_invariants(base_entry, fix_entry)
    assert sha(fix_entry) == _emb.BASE_ENTRY_SHA, \
        f"certificate-fix tip NOT reproduced: {sha(fix_entry)} — STOP"
    emb_entry = _emb.apply_emblem(fix_entry, b64)
    _emb.check_invariants(fix_entry, emb_entry, b64)
    assert sha(emb_entry) == BASE_ENTRY_SHA, \
        f"emblem-placement tip NOT reproduced: {sha(emb_entry)} — STOP"
    print(f"base reproduced: entry {len(emb_entry.encode())} B sha={sha(emb_entry)[:8]}... MATCH")

    # 0b. Live staged guards: /free must serve the tip (or this round's
    # v1 staging, when the build is re-run after staging v1) + /free/walk.
    st, _, live_entry = _sim.http_get(FREE_HOST + "/free")
    assert st == 200 and sha(live_entry) in (BASE_ENTRY_SHA, PREV_STAGED_SHA), \
        f"live staged /free moved: {st} {sha(live_entry)[:8]}... — STOP"
    print(f"live staged /free == {'tip' if sha(live_entry) == BASE_ENTRY_SHA else 'this round v1'} MATCH")
    st, _, live_walk = _sim.http_get(FREE_HOST + "/free/walk")
    assert st == 200 and sha(live_walk) == BASE_WALK_SHA, \
        f"live staged /free/walk moved: {st} {sha(live_walk)[:8]}... — STOP"
    print("live staged /free + /free/walk == tip MATCH")
    # Identity is OUT OF SCOPE for this round (sequenced, do NOT stage it
    # here) — observe it, do not guard on it: it has moved since the
    # emblem round (was 8c641f96...), which is another round's doing, not
    # this round's (nothing has been staged yet at this point).
    st, _, live_id = _sim.http_get(IDENTITY_HOST + "/identity.html")
    print(f"live staged identity: {st} sha={sha(live_id)[:8]}... "
          f"(base 8c641f96... — MOVED by another round, observed not touched)")

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
    assert sha(wb) in (BASE_WORKER_SHA, PREV_WORKER_SHA), \
        f"live staged worker moved: {sha(wb)[:8]}... — STOP"
    free_index = _bf.FREE_INDEX.replace(
        "__PRICING_STAGED__", "https://naya-pricing-f4-staging.nayapower.workers.dev/")
    worker_cur = _cur.build_worker_for(walk_pf, emb_entry, sw, mani)
    assert sha(worker_cur) == BASE_WORKER_SHA, \
        f"current worker NOT reproduced: {sha(worker_cur)} — STOP"
    print(f"current worker reproduced: {len(worker_cur.encode())} B sha={sha(worker_cur)[:8]}... MATCH")

    # 1. Apply the corners fix.
    geometry_proof()
    new_entry = apply_corners_fix(emb_entry, b64)
    check_invariants(emb_entry, new_entry, b64)
    diff = list(difflib.unified_diff(emb_entry.splitlines(), new_entry.splitlines(), lineterm="", n=0))
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
                    ["EMBLEM CORNERS FIX (2026-11-17",
                     'id="crestCut"',
                     "filter: url(#crestCut) drop-shadow(0 6px 12px rgba(0,0,0,0.60));",
                     ".corner-crest { position: absolute; z-index: 5; width: 132px; height: 161px;",
                     ".cm-tl { top: 112px; left: 112px; transform: translate(-50%, -50%) rotate(-59deg); }",
                     ".cm-tr { top: 112px; right: 112px; transform: translate(50%, -50%) rotate(59deg); }",
                     ".cm-bl { bottom: 112px; left: 112px; transform: translate(-50%, 50%) rotate(-121deg); }",
                     ".cm-br { bottom: 112px; right: 112px; transform: translate(50%, 50%) rotate(121deg); }",
                     ".corner-crest { width: 64px; height: 64px; }",
                     ".cm-tl { top: 56px; left: 56px; transform: translate(-50%, -50%) rotate(-35deg); }",
                     ".cm-br { bottom: 56px; right: 56px; transform: translate(50%, 50%) rotate(145deg); }",
                     ".identity-face { padding: 22px 18px 160px; grid-template-rows: auto auto 1fr; }",
                     ".identity-pro-card, #certPlaque { min-height: 798px; }",
                     "@media (max-width: 640px) and (min-height: 701px)",
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
                     "width: 100px; height: 122px;",
                     ".corner-crest { width: 54px; height: 54px; }",
                     "padding: 22px 18px 34px;",
                     "top: 20px; left: 20px;", "top: 15px; left: 15px;",
                     "no CSS mask",
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
