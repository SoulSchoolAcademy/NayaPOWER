import json
import os
import re
from pathlib import Path
from textwrap import dedent

import pytest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/governed-supabase-production-deploy.yml"


def receipt_program():
    source = WORKFLOW.read_text(encoding="utf-8")
    block = re.search(
        r'      - name: Write durable production promotion receipt\n'
        r'        shell: bash\n'
        r'        run: \|\n'
        r'(?P<body>.*?)(?=\n      - uses: actions/upload-artifact@v4)',
        source,
        re.S,
    )
    assert block
    body = block.group("body")
    start = body.index("          python - <<'PY'") + len("          python - <<'PY'\n")
    end = body.index("\n          PY", start)
    return dedent(body[start:end])


def run_receipt(tmp_path, source_sha="a" * 40, producer_sha=None, proof_sha=None, producer_conclusion="success", proof_conclusion="success", act_sha=None, act_conclusion="success", connect_sha=None, connect_conclusion="success"):
    (tmp_path / "supabase-production-check.json").write_text(
        json.dumps({"id": 10, "name": "Supabase", "conclusion": "success"})
    )
    (tmp_path / "producer-run.json").write_text(
        json.dumps({"databaseId": 20, "conclusion": producer_conclusion, "headSha": producer_sha or source_sha})
    )
    (tmp_path / "proof-run.json").write_text(
        json.dumps({"databaseId": 30, "conclusion": proof_conclusion, "headSha": proof_sha or source_sha})
    )
    (tmp_path / "act-proof-run.json").write_text(
        json.dumps({"databaseId": 35, "conclusion": act_conclusion, "headSha": act_sha or source_sha})
    )
    (tmp_path / "connect-proof-run.json").write_text(
        json.dumps({"databaseId": 36, "conclusion": connect_conclusion, "headSha": connect_sha or source_sha})
    )
    env = {
        "GITHUB_SHA": source_sha,
        "PRODUCTION_BRANCH": "production",
        "PROMOTION_MODE": "EXPLICIT_HUMAN",
        "GITHUB_ACTOR": "test",
        "GITHUB_RUN_ID": "40",
        "DEPLOYMENT_SHA": "b" * 40,
        "SOURCE_TREE_SHA": "c" * 40,
        "DEPLOYMENT_TREE_SHA": "d" * 40,
    }
    old = Path.cwd()
    try:
        os.chdir(tmp_path)
        os.environ.update(env)
        exec(compile(receipt_program(), "governed-production-receipt", "exec"), {})
    finally:
        os.chdir(old)
    return json.loads((tmp_path / "production-promotion-receipt.json").read_text())


def test_parent_receipt_binds_both_child_proofs_to_authorized_source(tmp_path):
    receipt = run_receipt(tmp_path)
    assert receipt["source_sha"] == "a" * 40
    assert receipt["canonical_proof"]["producer_run_id"] == 20
    assert receipt["canonical_proof"]["runtime_proof_run_id"] == 30
    assert receipt["canonical_proof"]["act_proof_run_id"] == 35
    assert receipt["canonical_proof"]["connect_proof_run_id"] == 36


@pytest.mark.parametrize("bad", ["producer", "proof", "act", "connect"])
def test_parent_receipt_fails_closed_on_child_source_mismatch(tmp_path, bad):
    kwargs = ({"producer_sha": "z" * 40} if bad == "producer" else {"proof_sha": "z" * 40} if bad == "proof" else {"act_sha": "z" * 40} if bad == "act" else {"connect_sha": "z" * 40})
    with pytest.raises(AssertionError):
        run_receipt(tmp_path, **kwargs)


@pytest.mark.parametrize("bad", ["producer", "proof", "act", "connect"])
def test_parent_receipt_fails_closed_when_a_child_is_not_successful(tmp_path, bad):
    kwargs = ({f"{bad}_conclusion": "failure"})
    with pytest.raises(AssertionError):
        run_receipt(tmp_path, **kwargs)
