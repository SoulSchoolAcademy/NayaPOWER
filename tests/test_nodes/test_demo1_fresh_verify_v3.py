"""Demo-1 P3: fresh_verify V3 must separate the three questions.

V1 (receipt bytes intact?) and V2 (historical effect occurred?) are the
historical verification. V3 (is another action authorized NOW?) resolves
the referenced DECISION receipt and the CURRENT grant file — never the
execution receipt's frozen authority_basis.

Pinned behavior:
- honest layout + live grant            -> V1/V2/V3 PASS, exit 0
- grant revoked after the effect        -> V3 FAIL, V1/V2 PASS (history stands)
- grant expired                         -> V3 FAIL
- grant file absent                      -> V3 FAIL (fail closed)
- decision receipt missing               -> V3 UNKNOWN (never a silent PASS)

Every case runs fresh_verify in a FRESH process against receipts produced
by the real act_run.py — no fabricated receipts.
"""

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
VERIFY = REPO_ROOT / "scripts" / "demo1" / "fresh_verify.py"
ACT_RUN = REPO_ROOT / "scripts" / "demo1" / "act_run.py"
REAL_GRANT = REPO_ROOT / "scripts" / "demo1" / "demo_grant.json"


@pytest.fixture(scope="module")
def honest_run(tmp_path_factory):
    """One genuine Demo-1 execution; tests copy and mutate the layout."""
    root = tmp_path_factory.mktemp("honest-run")
    proc = subprocess.run(
        [sys.executable, str(ACT_RUN), "--root", str(root)],
        cwd=REPO_ROOT, capture_output=True, text=True, timeout=120)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    staging = root / "demo-staging"
    receipts = list((staging / "receipts").glob("exec-*.json"))
    assert len(receipts) == 1, "one execution receipt expected"
    assert list((staging / "receipts").glob("decision-*.json")), \
        "decision receipt expected"
    return staging


def _layout_copy(honest_run, tmp_path):
    dest = tmp_path / "demo-staging"
    shutil.copytree(honest_run, dest)
    return dest


def _verify(receipt_path, grant_path=None):
    cmd = [sys.executable, str(VERIFY), str(receipt_path)]
    if grant_path is not None:
        cmd += ["--grant-path", str(grant_path)]
    proc = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True,
                          text=True, timeout=120)
    verdicts = None
    for line in proc.stdout.splitlines():
        if line.startswith("VERDICTS:"):
            verdicts = json.loads(line.split("VERDICTS:", 1)[1].strip())
    assert verdicts is not None, "no VERDICTS line:\n" + proc.stdout
    return proc.returncode, verdicts, proc.stdout


def _exec_receipt(staging):
    receipts = list((staging / "receipts").glob("exec-*.json"))
    assert len(receipts) == 1
    return receipts[0]


def _mutated_grant(tmp_path, **changes):
    grant = json.loads(REAL_GRANT.read_text(encoding="utf-8"))
    for key, value in changes.items():
        grant[key] = value
    path = tmp_path / "grant-test.json"
    path.write_text(json.dumps(grant), encoding="utf-8")
    return path


def test_honest_layout_all_verdicts_pass(honest_run, tmp_path):
    staging = _layout_copy(honest_run, tmp_path)
    code, verdicts, _ = _verify(_exec_receipt(staging))
    assert verdicts == {"V1": "PASS", "V2": "PASS", "V3": "PASS"}, verdicts
    assert code == 0


def test_revoked_grant_v3_fails_history_stands(honest_run, tmp_path):
    """The coordinator's repro: revoking the grant file must flip V3 to
    FAIL while V1/V2 keep standing — history is not erased, reuse is dead."""
    staging = _layout_copy(honest_run, tmp_path)
    grant = _mutated_grant(tmp_path, revoked=True)
    code, verdicts, out = _verify(_exec_receipt(staging), grant)
    assert verdicts["V1"] == "PASS", verdicts
    assert verdicts["V2"] == "PASS", verdicts
    assert verdicts["V3"] == "FAIL", verdicts
    assert code == 0  # historical verification succeeded; V3 is separate
    assert "revoked" in out


def test_expired_grant_v3_fails(honest_run, tmp_path):
    staging = _layout_copy(honest_run, tmp_path)
    grant = _mutated_grant(tmp_path, expiry="2026-09-01T00:00:00+00:00")
    code, verdicts, _ = _verify(_exec_receipt(staging), grant)
    assert verdicts["V3"] == "FAIL", verdicts
    assert verdicts["V1"] == "PASS" and verdicts["V2"] == "PASS"
    assert code == 0


def test_missing_grant_file_v3_fails_closed(honest_run, tmp_path):
    staging = _layout_copy(honest_run, tmp_path)
    code, verdicts, _ = _verify(
        _exec_receipt(staging), tmp_path / "no-such-grant.json")
    assert verdicts["V3"] == "FAIL", verdicts
    assert code == 0


def test_missing_decision_receipt_v3_unknown(honest_run, tmp_path):
    """Without the decision receipt, current authority cannot be resolved:
    UNKNOWN — never a silent PASS."""
    staging = _layout_copy(honest_run, tmp_path)
    for p in (staging / "receipts").glob("decision-*.json"):
        p.unlink()
    code, verdicts, out = _verify(_exec_receipt(staging))
    assert verdicts["V1"] == "PASS", verdicts
    assert verdicts["V2"] == "PASS", verdicts
    assert verdicts["V3"] == "UNKNOWN", verdicts
    assert code == 0
    assert "UNKNOWN [V3]" in out
