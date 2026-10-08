"""Falsifier tests for the Naya Design Calculator.

Each test asserts the calculator's JUDGMENT layer — where it must agree
with Shawn, not just count mechanical violations. A test that fails here
is a place where the math disagrees with the taste.
"""
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools", "design_law"))
from design_calculator import DesignCalculator  # noqa: E402

BASE = """<!doctype html><html><head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
:root{--bg:#0B0D12;--ink:#F5F7FB;}
body{background:#0B0D12;color:#F5F7FB;font-size:18px;font-family:Inter,system-ui,sans-serif;}
h1{font-size:24px;}
.btn{background:#050505;color:#fff;border:1.5px solid #fff;border-radius:999px;min-height:52px;
 box-shadow:0 0 22px rgba(157,117,255,.35);}
.btn:hover{box-shadow:0 0 42px #9d75ff;}
.btn:focus{outline:2px solid #9d75ff;}
@media (prefers-reduced-motion: reduce){*{animation:none;}}
</style></head><body><h1>Title</h1><button class="btn">Go</button></body></html>"""


def calc(html=BASE, **kw):
    return DesignCalculator(html, **kw).run()


def cat(result, key):
    return result["categories"][key]


def test_compliant_page_scores_high():
    r = calc()
    assert r["total"] >= 85, r["total"]


def test_richened_tokens_sanctioned():
    # Shawn: "make them richer" — richened variants are not violations.
    html = BASE.replace("</style>",
                        ".rich{background:#e84fff;}.rich2{color:#ffbf3d;}</style>")
    r = calc(html)
    assert cat(r, "spectrum_law")["score"] == 20, cat(r, "spectrum_law")["findings"]


def test_white_buttons_not_lightbg():
    # Shawn 2026-10-08: buttons should be white at rest.
    html = BASE.replace(".btn{background:#050505;",
                        ".btn{background:linear-gradient(180deg,#ffffff,#dbe0ef);color:#0b0d14;")
    r = calc(html)
    lightbg = [f for f in cat(r, "color_identity")["findings"] if f["check"] == "LIGHTBG"]
    assert not lightbg, lightbg


def test_swatch_exempt():
    html = BASE.replace("</body>",
                        '<div class="swatch" style="background:#9d75ff"></div></body>')
    r = calc(html)
    pf = [f for f in cat(r, "spectrum_law")["findings"] if f["check"] == "PURPLEFILL"]
    assert not pf, pf


def test_selection_exempt():
    html = BASE.replace("</style>", "::selection{background:#9d75ff;}</style>")
    r = calc(html)
    pf = [f for f in cat(r, "spectrum_law")["findings"] if f["check"] == "PURPLEFILL"]
    assert not pf, pf


def test_gold_token_not_amberrose():
    # The token set INCLUDES gold/yellow — amber band must not flag them.
    html = BASE.replace("</style>", ".g{color:#e8b64c;}.y{background:#f1d75a;}</style>")
    r = calc(html)
    ar = [f for f in cat(r, "spectrum_law")["findings"] if f["check"] == "AMBERROSE"]
    assert not ar, ar


def test_var_body_resolves():
    html = BASE.replace("font-size:18px;", "font-size:var(--body);").replace(
        ":root{", ":root{--body:18px;")
    r = calc(html)
    d9 = [f for f in cat(r, "typography")["findings"] if f["check"] == "D9"]
    assert not d9, d9


def test_pr_number_flagged():
    html = BASE.replace("</body>", "<p>See PR #1858 for details.</p></body>")
    r = calc(html)
    pr = [f for f in cat(r, "truth_language")["findings"] if f["check"] == "TRUTH-PR"]
    assert pr, "PR number in UI text must be flagged"


def test_jargon_flagged():
    html = BASE.replace("</body>", "<p>Our pre-ship harness is ready.</p></body>")
    r = calc(html)
    j = [f for f in cat(r, "truth_language")["findings"] if f["check"] == "TRUTH-JARGON"]
    assert j, "jargon in human text must be flagged"


def test_adjacent_dupes_flagged():
    html = BASE.replace("</body>", (
        '<span class="jewel" style="color:#e8b64c"></span>'
        '<span class="jewel" style="color:#e8b64c"></span>'
        '<span class="jewel" style="color:#e8b64c"></span></body>'))
    r = calc(html)
    d = [f for f in cat(r, "spectrum_law")["findings"] if f["check"] == "ADJ-DUPE"]
    assert d, "three adjacent gold jewels must be flagged"


def test_valid_flow_passes():
    html = BASE.replace("</body>", (
        '<span class="jewel" style="color:#d86cff"></span>'
        '<span class="jewel" style="color:#9d75ff"></span>'
        '<span class="jewel" style="color:#55b9ee"></span></body>'))
    r = calc(html)
    bad = [f for f in cat(r, "spectrum_law")["findings"]
           if f["check"] in ("ADJ-DUPE", "FLOW-ORDER")]
    assert not bad, bad


def test_light_root_penalized():
    html = BASE.replace("#0B0D12", "#eef0f6").replace("#F5F7FB", "#11141f")
    r = calc(html)
    assert cat(r, "color_identity")["score"] <= 9, cat(r, "color_identity")["findings"]


def test_body_under_18_penalized():
    html = BASE.replace("font-size:18px;", "font-size:16px;")
    r = calc(html)
    d9 = [f for f in cat(r, "typography")["findings"] if f["check"] == "D9"]
    assert d9, "16px body must be flagged"


def test_no_hover_penalized():
    html = BASE.replace(".btn:hover{box-shadow:0 0 42px #9d75ff;}\n", "")
    r = calc(html)
    h = [f for f in cat(r, "buttons_dimensional")["findings"] if f["check"] == "NO-HOVER"]
    assert h, "buttons without hover must be flagged"


def test_gate_mode():
    import subprocess
    calc_path = os.path.join(os.path.dirname(__file__), "..", "tools",
                             "design_law", "design_calculator.py")
    good = os.path.join(os.path.dirname(__file__), "test_fixtures", "good.html")
    os.makedirs(os.path.dirname(good), exist_ok=True)
    with open(good, "w") as f:
        f.write(BASE)
    try:
        ok = subprocess.run([sys.executable, calc_path, good, "--gate", "90"],
                            capture_output=True, text=True, timeout=60)
        assert ok.returncode == 0, ok.stdout + ok.stderr
        bad = subprocess.run([sys.executable, calc_path, good, "--gate", "101"],
                             capture_output=True, text=True, timeout=60)
        assert bad.returncode == 1, bad.stdout + bad.stderr
    finally:
        os.remove(good)
        os.rmdir(os.path.dirname(good))


def test_json_structure():
    import json
    import subprocess
    calc_path = os.path.join(os.path.dirname(__file__), "..", "tools",
                             "design_law", "design_calculator.py")
    good = "/tmp/calc_json_test.html"
    with open(good, "w") as f:
        f.write(BASE)
    try:
        out = subprocess.run([sys.executable, calc_path, good, "--json"],
                             capture_output=True, text=True, timeout=60)
        d = json.loads(out.stdout)
        assert d["max"] == 100
        assert len(d["categories"]) == 7
        assert all("score" in c and "findings" in c for c in d["categories"].values())
    finally:
        os.remove(good)
