"""Pytest suite for the fused Naya delivery gate (tools/naya_gate.py).

Run: python3 -m pytest tools/test_naya_gate.py -v
The network-dependent enforce-mode e2e is marked e2e; skip with -m "not e2e".
"""
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import naya_gate as G

CANON = "SoulSchoolAcademy/NayaPOWER"
GIT_URL = "https://github.com/SoulSchoolAcademy/NayaPOWER.git"


@pytest.fixture()
def ctx(tmp_path):
    mf = tmp_path / "manifest.json"
    mf.write_text(json.dumps({"blocks": [{"css_classes": [".naya-btn"]}]}))
    pg = tmp_path / "page.html"
    return tmp_path, mf, pg


def good_html(marker=""):
    return ("<!DOCTYPE html><html><head>"
            '<meta name="viewport" content="width=device-width, initial-scale=1">'
            '<meta name="color-scheme" content="dark">'
            "<style>html{background:#050507}body{background:#050507;color:#f8f7fb}"
            ".naya-btn{color:#fff}</style></head>"
            '<body class="naya-page"><button class="naya-btn">Go</button>'
            f"{marker}</body></html>")


def bad_html():
    return ('<!DOCTYPE html><html><head><link rel="stylesheet" href="x.css">'
            "<style>body{background:#fff;color:#111}</style></head>"
            '<body><div class="naya-frobnicate">hi</div></body></html>')


def make_receipt(tmp_path, name="r.json", **kw):
    r = {"schema": "naya.activation.receipt.v2", "status": "ACTIVATED",
         "session_id": "t1", "naya_identity": "Naya QA",
         "human_authority": "Shawn", "repository": CANON,
         "job": "test", "gates": ["law"], "proof_plan": "test",
         "main_sha": "a" * 40,
         "activated_at": datetime.now(timezone.utc).isoformat()}
    r.update(kw)
    rp = tmp_path / name
    rp.write_bytes(json.dumps(r).encode())
    return rp


def marked(html, rp):
    digest = hashlib.sha256(rp.read_bytes()).hexdigest()
    return html.replace("</body>",
                        f"<!-- NAYA-ACTIVATION-RECEIPT-SHA256:{digest} --></body>")


def act(html_text, rp, **kw):
    return G.run_activation_stage(html_text, rp, enforce=False,
                                  caller_tip="a" * 40, trust_caller=True, **kw)


# ---------------- STAGE 1: design ----------------

def test_design_rejects_forbidden_html(ctx):
    tmp_path, mf, pg = ctx
    pg.write_text(bad_html())
    v = G.run_design_stage(pg, mf)
    assert len(v) >= 4, f"expected multiple violations, got {v}"
    joined = " ".join(v)
    assert "SELF-CONTAINED" in joined
    assert "BLACK ROOT" in joined or "NO LIGHT SURFACES" in joined
    assert "NO FREESTYLE" in joined


def test_design_accepts_valid_canonical_component(ctx):
    tmp_path, mf, pg = ctx
    pg.write_text(good_html())
    assert G.run_design_stage(pg, mf) == []


def test_design_rejects_undocumented_class_without_prefix(ctx):
    """Closed-world (Naya 1): an unregistered class fails even with no naya-
    prefix. Undocumented must not mean escapes-the-rules."""
    tmp_path, mf, pg = ctx
    pg.write_text(good_html().replace(
        "</body>", '<div class="widget">x</div></body>'))
    v = G.run_design_stage(pg, mf)
    assert any("NO FREESTYLE" in x and ".widget" in x for x in v), v


def test_design_permits_bem_modifier_of_registered_block(ctx):
    tmp_path, mf, pg = ctx
    pg.write_text(good_html().replace(
        'class="naya-btn"', 'class="naya-btn naya-btn--large"'))
    assert G.run_design_stage(pg, mf) == []


# ---------------- STAGE 2: activation (advisory) ----------------

def test_activation_rejects_missing_marker(ctx):
    tmp_path, mf, pg = ctx
    rp = make_receipt(tmp_path)
    v, _ = act(good_html(), rp)
    assert any("no activation citation marker" in x for x in v)


def test_activation_accepts_valid_receipt(ctx):
    tmp_path, mf, pg = ctx
    rp = make_receipt(tmp_path)
    v, advisory = act(marked(good_html(), rp), rp)
    assert v == [], f"unexpected violations: {v}"
    assert advisory is True  # caller-supplied tip => advisory, never enforcement


def test_activation_rejects_forged_marker(ctx):
    tmp_path, mf, pg = ctx
    rp = make_receipt(tmp_path)
    forged = good_html("<!-- NAYA-ACTIVATION-RECEIPT-SHA256:" + "0" * 64 + " -->")
    v, _ = act(forged, rp)
    assert any("FAIL-CITATION" in x for x in v)


def test_activation_rejects_stale_receipt(ctx):
    tmp_path, mf, pg = ctx
    old_ts = (datetime.now(timezone.utc) - timedelta(hours=5)).isoformat()
    rp = make_receipt(tmp_path, activated_at=old_ts)
    v, _ = act(marked(good_html(), rp), rp)
    assert any("FAIL-STALE" in x for x in v)


def test_activation_rejects_wrong_repository(ctx):
    tmp_path, mf, pg = ctx
    rp = make_receipt(tmp_path, repository="EvilCorp/OtherRepo")
    v, _ = act(marked(good_html(), rp), rp)
    assert any("FAIL-WRONG-REPO" in x for x in v)


def test_activation_rejects_unactivated_status(ctx):
    tmp_path, mf, pg = ctx
    rp = make_receipt(tmp_path, status="DRAFT")
    v, _ = act(marked(good_html(), rp), rp)
    assert any("FAIL-UNACTIVATED" in x for x in v)


def test_activation_rejects_tip_mismatch_advisory(ctx):
    tmp_path, mf, pg = ctx
    rp = make_receipt(tmp_path)
    v, _ = G.run_activation_stage(marked(good_html(), rp), rp, enforce=False,
                                   caller_tip="b" * 40, trust_caller=True)
    assert v, "tip mismatch should fail even in advisory mode"


def test_activation_rejects_untrusted_caller_tip(ctx):
    tmp_path, mf, pg = ctx
    rp = make_receipt(tmp_path)
    v, _ = G.run_activation_stage(marked(good_html(), rp), rp, enforce=False,
                                   caller_tip="a" * 40, trust_caller=False)
    assert any("SN-0787" in x for x in v)


def test_activation_accepts_v1_schema(ctx):
    tmp_path, mf, pg = ctx
    r = {"schema": "naya.activation.receipt.v1", "status": "ACTIVATED",
         "session_id": "t1", "repository": CANON, "main_sha": "a" * 40,
         "timestamp": datetime.now(timezone.utc).isoformat(),
         "activation_protocol": "v2", "loaded": ["design-doctrine"]}
    rp = tmp_path / "r1.json"
    rp.write_bytes(json.dumps(r).encode())
    v, _ = act(marked(good_html(), rp), rp)
    assert v == [], f"v1 receipt should pass: {v}"


# ---------------- STAGE 3: workflow proof (needs network) ----------------

def _live_tip():
    r = subprocess.run(["git", "ls-remote", GIT_URL, "HEAD"],
                       capture_output=True, text=True, timeout=60)
    assert r.returncode == 0, "trusted fetch failed"
    return r.stdout.strip().split()[0]


@pytest.mark.e2e
def test_enforce_mode_passes_on_real_live_tip(ctx):
    tmp_path, mf, pg = ctx
    tip = _live_tip()
    rp = make_receipt(tmp_path, main_sha=tip)
    pg.write_text(marked(good_html(), rp))
    res = subprocess.run(
        [sys.executable, str(Path(G.__file__)), str(pg),
         "--manifest", str(mf), "--require-activation",
         "--receipt", str(rp)],
        capture_output=True, text=True, timeout=120)
    assert res.returncode == 0, f"enforce PASS failed:\n{res.stdout[-800:]}"
    assert "ADVISORY" not in res.stdout


@pytest.mark.e2e
def test_enforce_mode_fails_on_tampered_tip(ctx):
    tmp_path, mf, pg = ctx
    tip = _live_tip()
    tampered = "0" + tip[1:]
    rp = make_receipt(tmp_path, main_sha=tampered)
    pg.write_text(marked(good_html(), rp))
    res = subprocess.run(
        [sys.executable, str(Path(G.__file__)), str(pg),
         "--manifest", str(mf), "--require-activation",
         "--receipt", str(rp)],
        capture_output=True, text=True, timeout=120)
    assert res.returncode == 1
    assert "FAIL-TIP-MOVED" in res.stdout


def _live_component_shas():
    """Resolve true blob SHAs via the gate's own trusted path (test uses the
    mechanism under test to obtain ground truth — proves the round trip)."""
    live, err = G.fetch_live_tree_blob_shas(["HUB/DESIGN-CONTRACT.md", "AGENTS.md"])
    assert err is None, f"trusted component fetch failed: {err}"
    return live


@pytest.mark.e2e
def test_enforce_mode_components_live_pass(ctx):
    tmp_path, mf, pg = ctx
    tip = _live_tip()
    live = _live_component_shas()
    comps = [{"path": p, "sha": s} for p, s in sorted(live.items())]
    rp = make_receipt(tmp_path, main_sha=tip, components=comps)
    pg.write_text(marked(good_html(), rp))
    res = subprocess.run(
        [sys.executable, str(Path(G.__file__)), str(pg),
         "--manifest", str(mf), "--require-activation",
         "--receipt", str(rp)],
        capture_output=True, text=True, timeout=180)
    assert res.returncode == 0, f"COMPONENTS_LIVE pass failed:\n{res.stdout[-800:]}"
    assert "FAIL-COMPONENT-MISMATCH" not in res.stdout


@pytest.mark.e2e
def test_enforce_mode_components_live_rejects_forged_sha(ctx):
    tmp_path, mf, pg = ctx
    tip = _live_tip()
    live = _live_component_shas()
    comps = [{"path": p, "sha": s} for p, s in sorted(live.items())]
    comps[0] = {"path": comps[0]["path"], "sha": "0" * 40}  # forged component
    rp = make_receipt(tmp_path, main_sha=tip, components=comps)
    pg.write_text(marked(good_html(), rp))
    res = subprocess.run(
        [sys.executable, str(Path(G.__file__)), str(pg),
         "--manifest", str(mf), "--require-activation",
         "--receipt", str(rp)],
        capture_output=True, text=True, timeout=180)
    assert res.returncode == 1
    assert "FAIL-COMPONENT-MISMATCH" in res.stdout


@pytest.mark.e2e
def test_enforce_mode_components_live_rejects_missing_path(ctx):
    tmp_path, mf, pg = ctx
    tip = _live_tip()
    comps = [{"path": "NOPE/nonexistent-xyz.md", "sha": "a" * 40}]
    rp = make_receipt(tmp_path, main_sha=tip, components=comps)
    pg.write_text(marked(good_html(), rp))
    res = subprocess.run(
        [sys.executable, str(Path(G.__file__)), str(pg),
         "--manifest", str(mf), "--require-activation",
         "--receipt", str(rp)],
        capture_output=True, text=True, timeout=180)
    assert res.returncode == 1
    assert "FAIL-TRUSTED-FETCH" in res.stdout or "no blob in tip tree" in res.stdout


@pytest.mark.e2e
def test_enforce_mode_notes_not_bound_without_components(ctx):
    tmp_path, mf, pg = ctx
    tip = _live_tip()
    rp = make_receipt(tmp_path, main_sha=tip)  # no components recorded
    pg.write_text(marked(good_html(), rp))
    res = subprocess.run(
        [sys.executable, str(Path(G.__file__)), str(pg),
         "--manifest", str(mf), "--require-activation",
         "--receipt", str(rp)],
        capture_output=True, text=True, timeout=180)
    assert res.returncode == 0  # note, not fail
    assert "COMPONENTS_LIVE NOT_BOUND" in res.stdout
