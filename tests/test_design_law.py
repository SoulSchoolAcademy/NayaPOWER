"""Falsifier tests for the Naya Design Law checker (Contract V1, CANDIDATE).

Each test feeds a violating snippet and asserts FAIL, and a compliant snippet
and asserts PASS. The checker is the executable form of the contract; a test
that fails here is a hole in the machine law.
"""
import os
import subprocess
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools", "design_law"))
from check_design import check  # noqa: E402

CHECKER = os.path.join(os.path.dirname(__file__), "..", "tools", "design_law", "check_design.py")

# A fully compliant base snippet: token colors only, 18px body, white text,
# black button, reduced-motion present, zoom allowed.
COMPLIANT_BASE = """<!doctype html><html><head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
:root{--bg:#0B0D12;--ink:#F5F7FB;--purple:#9d75ff;--lime:#b8ee57;--teal:#40d3bb;}
body{background:#0B0D12;color:#F5F7FB;font-size:18px;font-family:Inter,system-ui,sans-serif;}
.btn{background:#050505;color:#fff;border:1.5px solid #fff;border-radius:999px;min-height:52px;}
.jewel{clip-path:polygon(50% 0%, 86% 28%, 74% 82%, 50% 100%, 26% 82%, 14% 28%);}
@keyframes breathe{to{opacity:.2}}
.card{animation:breathe 6s ease-in-out infinite;}
@media (prefers-reduced-motion: reduce){*{animation:none;}}
</style></head><body></body></html>"""


def ids(violations, severity="FAIL"):
    return {x["id"] for x in violations if x["severity"] == severity}


def fails_with(snippet, check_id, room=None):
    v = check(snippet, room=room)
    assert check_id in ids(v), "expected FAIL %s, got %s" % (check_id, v)
    assert any(x["severity"] == "FAIL" for x in v)


def passes(snippet, room=None):
    v = check(snippet, room=room)
    assert not any(x["severity"] == "FAIL" for x in v), "expected PASS, got %s" % (v,)


# ---- D1: pinch zoom -------------------------------------------------------
def test_d1_user_scalable_no_fails():
    html = COMPLIANT_BASE.replace(
        'content="width=device-width, initial-scale=1"',
        'content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no"')
    fails_with(html, "D1")


def test_d1_maximum_scale_1_fails():
    html = COMPLIANT_BASE.replace(
        'content="width=device-width, initial-scale=1"',
        'content="width=device-width, maximum-scale=1"')
    fails_with(html, "D1")


def test_d1_zoom_allowed_passes():
    passes(COMPLIANT_BASE)


# ---- D2/D3/D4: wrong room accents -----------------------------------------
def test_mail_blue_accent_passes():
    # SYNTHESIS 2026-10-08: mail's accent is blue #3ca8ff (bespoke "Blue identity").
    css = COMPLIANT_BASE.replace("--lime:#b8ee57", "--ml-blue:#3ca8ff")
    passes(css, room="mail")


def test_d3_spaces_wrong_accent_fails():
    css = COMPLIANT_BASE.replace("--lime:#b8ee57", "--sc:#7c3aed")
    fails_with(css, "D3", room="spaces")


def test_d3_spaces_prefixed_accent_fails():
    css = COMPLIANT_BASE.replace("--lime:#b8ee57", "--sc-accent:#7c3aed")
    fails_with(css, "D3", room="spaces")


def test_d3_spaces_correct_accent_passes():
    css = COMPLIANT_BASE.replace("--lime:#b8ee57", "--sp-coral:#ff5e6c")
    passes(css, room="spaces")  # coral #ff5e6c is the assigned accent


def test_connections_purple_accent_passes():
    # SYNTHESIS 2026-10-08: connections' accent is purple #9d75ff (bespoke --cx-purple).
    css = COMPLIANT_BASE.replace("--lime:#b8ee57", "--cx-purple:#9d75ff")
    passes(css, room="connections")


def test_room_accent_missing_fails():
    css = COMPLIANT_BASE.replace("--lime:#b8ee57", "")
    v = check(css, room="spaces")  # no coral accent -> FAIL
    assert "D3" in ids(v)


# ---- D9: 18px body law -----------------------------------------------------
def test_d9_body_16_fails():
    fails_with(COMPLIANT_BASE.replace("font-size:18px", "font-size:16px"), "D9")


def test_d9_body_11_fails():
    fails_with(COMPLIANT_BASE.replace("font-size:18px", "font-size:11px"), "D9")


def test_d9_body_missing_fails():
    fails_with(COMPLIANT_BASE.replace("font-size:18px;", ""), "D9")


def test_d9_body_18_passes():
    v = check(COMPLIANT_BASE)
    assert "D9" not in ids(v)


def test_d9_presentation_variant_14_passes():
    # Code-sanctioned presentation variant: 24/18/14 with variant markers
    css = COMPLIANT_BASE.replace(
        ":root{--bg:#0B0D12;",
        ":root{--fs-headline:24px;--fs-sub:18px;--fs-body:14px;--bg:#0B0D12;")
    css = css.replace("font-size:18px", "font-size:14px")
    v = check(css)
    assert "D9" not in ids(v), v


# ---- SPECTRUM: non-token chromatic colors ----------------------------------
def test_spectrum_nontoken_hex_fails():
    fails_with(COMPLIANT_BASE + "<style>.x{color:#a020f0;}</style>", "SPECTRUM")


def test_spectrum_token_hex_passes():
    v = check(COMPLIANT_BASE + "<style>.x{color:#55b9ee;border:1px solid #e8b64c;}</style>")
    assert "SPECTRUM" not in ids(v), v


def test_spectrum_gray_passes():
    v = check(COMPLIANT_BASE + "<style>.x{color:#888888;background:#161618;}</style>")
    assert "SPECTRUM" not in ids(v), v


# ---- LIGHTBG ----------------------------------------------------------------
def test_lightbg_white_fails():
    fails_with(COMPLIANT_BASE.replace("background:#0B0D12", "background:#ffffff"), "LIGHTBG")


def test_lightbg_gray_bg_fails():
    fails_with(COMPLIANT_BASE.replace("background:#0B0D12", "background:#cccccc"), "LIGHTBG")


def test_lightbg_sheen_gradient_passes():
    # Avatar sheen / jewel-core glows mix light stops with dark/transparent: legitimate
    v = check(COMPLIANT_BASE +
              "<style>.ava{background:radial-gradient(circle at 35% 30%, #ffffff, #0a0a0e 70%);}</style>")
    assert "LIGHTBG" not in ids(v), v


def test_lightbg_all_light_gradient_fails():
    fails_with(COMPLIANT_BASE.replace(
        "background:#0B0D12", "background:linear-gradient(#ffffff, #eeeeee)"), "LIGHTBG")


# ---- BTN: button law -----------------------------------------------------------
def test_btn_colored_text_fails():
    fails_with(COMPLIANT_BASE.replace(".btn{background:#050505;color:#fff;",
                                     ".btn{background:#050505;color:#9d75ff;"), "BTN")


def test_btn_solid_purple_fill_fails():
    v = check(COMPLIANT_BASE.replace(".btn{background:#050505;", ".btn{background:#9d75ff;"))
    assert "BTN" in ids(v) or "PURPLEFILL" in ids(v), v


def test_btn_solid_blue_fill_fails():
    fails_with(COMPLIANT_BASE.replace(".btn{background:#050505;", ".btn{background:#3ca8ff;"), "BTN")


def test_btn_compliant_passes():
    v = check(COMPLIANT_BASE)
    assert "BTN" not in ids(v), v


# ---- misc hard checks -----------------------------------------------------------
def test_clickable_div_fails():
    fails_with(COMPLIANT_BASE.replace("</body>", '<div onclick="go()">x</div></body>'), "DIVBTN")


def test_maxis_link_fails():
    fails_with(COMPLIANT_BASE.replace("</body>", '<a href="https://app.nayanet.technology/x">x</a></body>'),
               "MAXIS")


def test_maxwidth_chassis_fails():
    fails_with(COMPLIANT_BASE + "<style>body{max-width:1200px;}</style>", "MAXW")


def test_maxwidth_card_passes():
    v = check(COMPLIANT_BASE + "<style>.card{max-width:300px;}</style>")
    assert "MAXW" not in ids(v), v


def test_amber_rose_fails():
    v = check(COMPLIANT_BASE + "<style>.x{color:#f2c94c;}</style>")  # ledger D6 near-miss
    assert "AMBERROSE" in ids(v), v


def test_token_gold_passes_amber():
    v = check(COMPLIANT_BASE + "<style>.x{color:#e8b64c;}</style>")  # token gold is fine
    assert "AMBERROSE" not in ids(v), v


def test_gray_body_text_fails():
    fails_with(COMPLIANT_BASE.replace("color:#F5F7FB", "color:#8a8a96"), "BODYCOLOR")


def test_reduced_motion_missing_fails():
    css = COMPLIANT_BASE.replace("@media (prefers-reduced-motion: reduce){*{animation:none;}}", "")
    fails_with(css, "RM")


def test_reduced_motion_present_passes():
    v = check(COMPLIANT_BASE)
    assert "RM" not in ids(v), v


# ---- warnings do not fail ---------------------------------------------------------
def test_jewel_clip_drift_warns_only():
    css = COMPLIANT_BASE.replace("86% 28%", "88% 26%").replace("14% 28%", "12% 26%")
    v = check(css)
    assert "JEWEL" in ids(v, "WARN")
    assert not any(x["severity"] == "FAIL" for x in v), v


def test_missing_bottombar_warns_only():
    css = COMPLIANT_BASE.replace("--lime:#b8ee57", "--sp-coral:#ff5e6c")
    v = check(css, room="spaces")  # coral #ff5e6c satisfies the accent
    assert "BOTTOMBAR" in ids(v, "WARN")
    assert not any(x["severity"] == "FAIL" for x in v), v


# ---- full compliant page passes ----------------------------------------------------
def test_fully_compliant_page_passes():
    passes(COMPLIANT_BASE)


# ---- CLI exit codes -----------------------------------------------------------------
def _run_cli(argv):
    p = subprocess.run([sys.executable, CHECKER] + argv,
                       capture_output=True, text=True, timeout=30)
    return p.returncode, p.stdout


def test_cli_exit_1_on_violation():
    code, out = _run_cli([COMPLIANT_BASE.replace("font-size:18px", "font-size:16px")])
    assert code == 1, out
    assert "D9" in out


def test_cli_exit_0_on_compliant():
    code, out = _run_cli([COMPLIANT_BASE])
    assert code == 0, out
    assert "PASS" in out


def test_cli_room_flag():
    css = COMPLIANT_BASE.replace("--lime:#b8ee57", "--sc:#7c3aed")
    code, out = _run_cli(["--room", "spaces", css])
    assert code == 1, out
    assert "D3" in out


# ---- synthesis 2026-10-08: team colors + headline 24 -------------------------------
def test_team_colors_exempt_from_spectrum():
    # Shawn's nine team colors (provisional hexes) must not trip SPECTRUM.
    for hx in ["#FF00FF", "#800080", "#4B0082", "#228B22",
               "#FFFF00", "#FFD700", "#FFA500", "#FF0000"]:
        snippet = COMPLIANT_BASE.replace(
            "</style>",
            ".team-tag{color:%s;}</style>" % hx)
        v = check(snippet)
        assert "SPECTRUM" not in ids(v), "team color %s tripped SPECTRUM: %s" % (hx, v)


def test_headline_24_fail():
    fails_with(
        COMPLIANT_BASE.replace("</style>", "h1{font-size:82px;}</style>"),
        "SYN-H24")


def test_headline_24_pass():
    passes(COMPLIANT_BASE.replace("</style>", "h1{font-size:24px;}</style>"))
