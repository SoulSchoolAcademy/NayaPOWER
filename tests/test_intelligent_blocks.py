"""Tests for the canonical Intelligent Blocks substrate.

intelligence/blocks/ is the single canonical home for distilled lessons.
These tests pin the schema, the seed data, and the registry consistency —
so the brain's atomic units can't silently rot.
"""
import json
import os
import re

BLOCKS_DIR = os.path.join(os.path.dirname(__file__), "..", "intelligence", "blocks")
REGISTRY_PATH = os.path.join(BLOCKS_DIR, "REGISTRY.json")
ID_RE = re.compile(r"^IB-(\d{4})$")
STATUSES = {"UNVERIFIED", "APPLIED", "BEHAVIOR-CHANGE-PROVEN", "COMPOUNDED"}
STAGES = {"text", "briefing", "code-gate"}
KINDS = {"receipt", "observation", "code", "test", "direct-word"}
REQUIRED = ["id", "schema_version", "title", "principle", "source", "evidence",
            "applicability", "verification_status", "status_history",
            "graduation", "supersedes", "superseded_by",
            "created_at", "updated_at"]


def load_blocks():
    blocks = []
    for name in sorted(os.listdir(BLOCKS_DIR)):
        if name.endswith(".json") and name != "REGISTRY.json" and ID_RE.match(name[:-5]):
            with open(os.path.join(BLOCKS_DIR, name), encoding="utf-8") as f:
                blocks.append((name, json.load(f)))
    return blocks


def test_blocks_directory_exists():
    assert os.path.isdir(BLOCKS_DIR), "intelligence/blocks/ is the canonical home"


def test_seed_count_at_least_twenty():
    assert len(load_blocks()) >= 20, "the 20 seed laws must all be present"


def test_all_blocks_valid_json_and_schema():
    for name, b in load_blocks():
        for field in REQUIRED:
            assert field in b, f"{name}: missing required field {field}"
        assert b["schema_version"] == "1.0", f"{name}: bad schema_version"
        assert ID_RE.match(b["id"]), f"{name}: bad id format"
        assert b["id"] == name[:-5], f"{name}: filename must match block id"


def test_ids_unique_and_sequential():
    blocks = load_blocks()
    ids = [b["id"] for _, b in blocks]
    assert len(ids) == len(set(ids)), "block IDs must be unique"
    nums = sorted(int(ID_RE.match(i).group(1)) for i in ids)
    assert nums == list(range(1, len(nums) + 1)), \
        "seed IDs must be sequential IB-0001.. with no gaps"


def test_principle_is_one_distilled_sentence():
    for name, b in load_blocks():
        p = b["principle"]
        assert p and "\n" not in p.strip(), f"{name}: principle must be one line"
        assert len(p) <= 400, f"{name}: principle too long — distill it"
        assert len(p.split()) >= 8, f"{name}: principle suspiciously short"


def test_source_complete():
    for name, b in load_blocks():
        for k in ["who", "when", "context"]:
            assert b["source"].get(k), f"{name}: source.{k} missing"


def test_evidence_kinds_and_refs():
    for name, b in load_blocks():
        for i, e in enumerate(b["evidence"]):
            assert e.get("kind") in KINDS, f"{name}: evidence[{i}] bad kind"
            assert e.get("ref"), f"{name}: evidence[{i}] missing ref"


def test_status_requires_evidence():
    for name, b in load_blocks():
        assert b["verification_status"] in STATUSES, f"{name}: bad status"
        if b["verification_status"] != "UNVERIFIED":
            assert b["evidence"], f"{name}: non-UNVERIFIED status needs evidence"


def test_status_history_ends_at_current():
    for name, b in load_blocks():
        hist = b["status_history"]
        assert hist, f"{name}: status_history empty"
        assert hist[-1]["status"] == b["verification_status"], \
            f"{name}: history must end at current status"


def test_applicability_complete():
    for name, b in load_blocks():
        app = b["applicability"]
        assert app.get("topics"), f"{name}: topics must be non-empty"
        assert all(t == t.lower() for t in app["topics"]), \
            f"{name}: topics must be lowercase tags"
        assert app.get("situations"), f"{name}: situations missing"
        assert app.get("decisions"), f"{name}: decisions missing"


def test_graduation_valid():
    for name, b in load_blocks():
        g = b["graduation"]
        assert g.get("stage") in STAGES, f"{name}: bad graduation stage"
        assert g.get("next_step"), f"{name}: graduation.next_step missing"
        assert "enforced_by" in g, f"{name}: graduation.enforced_by missing"


def test_registry_exists_and_consistent():
    assert os.path.exists(REGISTRY_PATH), "REGISTRY.json must exist"
    with open(REGISTRY_PATH, encoding="utf-8") as f:
        reg = json.load(f)
    blocks = load_blocks()
    assert reg["count"] == len(blocks), "registry count must match blocks dir"
    reg_ids = {e["id"] for e in reg["blocks"]}
    block_ids = {b["id"] for _, b in blocks}
    assert reg_ids == block_ids, "registry must cover exactly the blocks on disk"
    for e in reg["blocks"]:
        assert e["path"] == f"intelligence/blocks/{e['id']}.json"


def test_no_parallel_block_stores():
    # The canonical home is intelligence/blocks/. A second *.json block store
    # elsewhere in intelligence/ would be a fork — forbidden.
    for root, dirs, files in os.walk(os.path.join(os.path.dirname(__file__),
                                                  "..", "intelligence")):
        if os.path.basename(root) == "blocks":
            dirs[:] = []
            continue
        for fn in files:
            assert not (fn.startswith("IB-") and fn.endswith(".json")), \
                f"parallel block store found: {os.path.join(root, fn)}"


# ---------------------------------------------------------------------------
# CLI end-to-end: the ib tool must work, not just exist.
# ---------------------------------------------------------------------------

import shutil
import subprocess
import sys
import tempfile

IB_CLI = os.path.join(os.path.dirname(__file__), "..", "intelligence", "tools", "ib.py")


def _cli_tree():
    """Isolated intelligence/ tree with a fresh copy of the ib CLI."""
    tmp = tempfile.mkdtemp(prefix="ib-cli-test-")
    tools = os.path.join(tmp, "intelligence", "tools")
    os.makedirs(os.path.join(tools, "..", "blocks"))
    shutil.copy(os.path.abspath(IB_CLI), tools)
    return tmp


def _run(tmp, *argv):
    cli = os.path.join(tmp, "intelligence", "tools", "ib.py")
    return subprocess.run([sys.executable, cli, *argv],
                          capture_output=True, text=True, cwd=tmp)


def test_cli_full_lifecycle():
    tmp = _cli_tree()
    try:
        r = _run(tmp, "create", "--title", "T", "--principle",
                 "One plain sentence for the test block lifecycle.",
                 "--who", "tester", "--when", "2026-10-11",
                 "--context", "cli test", "--topics", "test",
                 "--situations", "s", "--decisions", "d")
        assert r.returncode == 0, r.stderr
        assert "IB-0001" in r.stdout

        r = _run(tmp, "evidence", "IB-0001", "--kind", "receipt",
                 "--ref", "cli-test", "--note", "n")
        assert r.returncode == 0, r.stderr

        r = _run(tmp, "update", "IB-0001", "--status", "APPLIED", "--note", "n")
        assert r.returncode == 0, r.stderr

        r = _run(tmp, "graduate", "IB-0001", "--stage", "briefing",
                 "--next", "n")
        assert r.returncode == 0, r.stderr

        r = _run(tmp, "get", "IB-0001")
        assert r.returncode == 0, r.stderr
        got = json.loads(r.stdout)
        assert got["verification_status"] == "APPLIED"
        assert got["graduation"]["stage"] == "briefing"
        assert len(got["evidence"]) == 1

        r = _run(tmp, "list", "--topic", "test")
        assert r.returncode == 0 and "IB-0001" in r.stdout

        r = _run(tmp, "reindex")
        assert r.returncode == 0, r.stderr
        r = _run(tmp, "validate")
        assert r.returncode == 0, r.stderr + r.stdout
        assert "1/1 blocks valid" in r.stdout
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_cli_refuses_status_without_evidence():
    tmp = _cli_tree()
    try:
        r = _run(tmp, "create", "--title", "T", "--principle",
                 "One plain sentence with no evidence attached yet here.",
                 "--who", "tester", "--when", "2026-10-11",
                 "--context", "cli test", "--topics", "test",
                 "--situations", "s", "--decisions", "d")
        assert r.returncode == 0, r.stderr
        r = _run(tmp, "update", "IB-0001", "--status", "APPLIED",
                 "--note", "should fail")
        assert r.returncode != 0
        assert "requires non-empty evidence" in r.stdout
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_cli_refuses_downgrade():
    tmp = _cli_tree()
    try:
        r = _run(tmp, "create", "--title", "T", "--principle",
                 "One plain sentence for the downgrade refusal test case.",
                 "--who", "tester", "--when", "2026-10-11",
                 "--context", "cli test", "--topics", "test",
                 "--situations", "s", "--decisions", "d")
        assert r.returncode == 0, r.stderr
        _run(tmp, "evidence", "IB-0001", "--kind", "receipt",
             "--ref", "x", "--note", "n")
        _run(tmp, "update", "IB-0001", "--status", "APPLIED", "--note", "n")
        r = _run(tmp, "update", "IB-0001", "--status", "UNVERIFIED",
                 "--note", "downgrade")
        assert r.returncode != 0
        assert "refusing downgrade" in r.stdout
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_cli_list_json_format():
    tmp = _cli_tree()
    try:
        r = _run(tmp, "create", "--title", "T", "--principle",
                 "One plain sentence for the json list format test case.",
                 "--who", "tester", "--when", "2026-10-11",
                 "--context", "cli test", "--topics", "alpha,beta",
                 "--situations", "s", "--decisions", "d")
        assert r.returncode == 0, r.stderr
        r = _run(tmp, "list", "--format", "json")
        assert r.returncode == 0, r.stderr
        rows = json.loads(r.stdout)
        assert len(rows) == 1
        assert rows[0]["id"] == "IB-0001"
        assert rows[0]["topics"] == ["alpha", "beta"]
        assert rows[0]["verification_status"] == "UNVERIFIED"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_cli_reindex_idempotent():
    tmp = _cli_tree()
    try:
        r = _run(tmp, "create", "--title", "T", "--principle",
                 "One plain sentence for the idempotent reindex test case.",
                 "--who", "tester", "--when", "2026-10-11",
                 "--context", "cli test", "--topics", "test",
                 "--situations", "s", "--decisions", "d")
        assert r.returncode == 0, r.stderr
        _run(tmp, "reindex")
        reg_path = os.path.join(tmp, "intelligence", "blocks", "REGISTRY.json")
        with open(reg_path, "rb") as f:
            first = f.read()
        r = _run(tmp, "reindex")
        assert r.returncode == 0, r.stderr
        assert "unchanged" in r.stdout
        with open(reg_path, "rb") as f:
            second = f.read()
        assert first == second, "no-op reindex must be byte-identical"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
