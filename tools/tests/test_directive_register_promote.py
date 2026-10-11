"""Directive register status-promotion tests.

Tests the promotion authority (tools/directive_register_promote.py) and the
status-change gate (tools/directive_register_status_check.py).

These are REAL asserts with REAL negative controls: skip-level jumps,
demotions, phantom ids, missing evidence, corrupt registers, and audit
mismatches must all be refused. If the mechanism can be lied to, the tests
fail. No theater.
"""
import json
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from directive_register_promote import (  # noqa: E402
    AUDIT_KEYS,
    promote,
)
from directive_register_status_check import run as status_check_run  # noqa: E402

TOOLS_DIR = Path(__file__).resolve().parent.parent
REAL_REGISTER = (
    TOOLS_DIR.parent / "BRAIN" / "01-GOVERNANCE" / "directive-register.json"
)


def make_register(tmp_path: Path, statuses: dict | None = None) -> Path:
    """A tiny valid register fixture. statuses maps id -> status."""
    statuses = statuses or {}
    entries = []
    for i, did in enumerate(["D8", "D9", "D10"]):
        entries.append(
            {
                "id": did,
                "title": f"Test directive {did}",
                "source_issue": 2175,
                "source_comment": "6108170419",
                "owner": "naya2",
                "status": statuses.get(did, "NOT_STARTED"),
                "evidence_pr": None,
                "wave": 6,
            }
        )
    reg = tmp_path / "directive-register.json"
    reg.write_text(json.dumps(entries, indent=2) + "\n", encoding="utf-8")
    return reg


def audit_lines(audit_path: Path) -> list[dict]:
    if not audit_path.exists():
        return []
    return [
        json.loads(line)
        for line in audit_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def register_status(reg: Path, did: str) -> str:
    data = json.loads(reg.read_text(encoding="utf-8"))
    return next(e["status"] for e in data if e["id"] == did)


# ---------------------------------------------------------------- promote()


def test_promote_building_happy_path(tmp_path):
    reg = make_register(tmp_path)
    audit = tmp_path / "audit.log"
    rc = promote(
        "D8", "BUILDING", evidence_comment=6108170419, actor="naya2",
        register_path=reg, audit_path=audit,
    )
    assert rc == 0
    assert register_status(reg, "D8") == "BUILDING"
    lines = audit_lines(audit)
    assert len(lines) == 1
    rec = lines[0]
    assert set(rec.keys()) == AUDIT_KEYS
    assert rec["directive_id"] == "D8"
    assert rec["from"] == "NOT_STARTED" and rec["to"] == "BUILDING"
    assert rec["evidence_pr"] is None
    assert rec["evidence_comment"] == 6108170419
    assert rec["actor"] == "naya2"


def test_promote_built_as_code_sets_evidence_pr(tmp_path):
    reg = make_register(tmp_path, {"D8": "BUILDING"})
    audit = tmp_path / "audit.log"
    rc = promote(
        "D8", "BUILT_AS_CODE", evidence_pr=2315, evidence_comment=6107942578,
        actor="naya2", register_path=reg, audit_path=audit,
    )
    assert rc == 0
    data = json.loads(reg.read_text(encoding="utf-8"))
    entry = next(e for e in data if e["id"] == "D8")
    assert entry["status"] == "BUILT_AS_CODE"
    assert entry["evidence_pr"] == 2315


def test_promote_enforced_happy_path(tmp_path):
    reg = make_register(tmp_path, {"D8": "BUILT_AS_CODE"})
    audit = tmp_path / "audit.log"
    rc = promote(
        "D8", "ENFORCED", evidence_pr=2328, evidence_comment=6107921353,
        actor="naya2", register_path=reg, audit_path=audit,
    )
    assert rc == 0
    assert register_status(reg, "D8") == "ENFORCED"
    assert len(audit_lines(audit)) == 1


def test_promote_audit_sha256_matches_pre_write_bytes(tmp_path):
    reg = make_register(tmp_path)
    before = reg.read_bytes()
    import hashlib

    audit = tmp_path / "audit.log"
    rc = promote(
        "D9", "BUILDING", evidence_comment=6108170419, actor="naya2",
        register_path=reg, audit_path=audit,
    )
    assert rc == 0
    rec = audit_lines(audit)[0]
    assert rec["register_sha256"] == hashlib.sha256(before).hexdigest()


def test_promote_skip_level_refused(tmp_path):
    """NOT_STARTED -> BUILT_AS_CODE is a lie. Refuse it."""
    reg = make_register(tmp_path)
    audit = tmp_path / "audit.log"
    rc = promote(
        "D8", "BUILT_AS_CODE", evidence_pr=2315, evidence_comment=6107942578,
        actor="naya2", register_path=reg, audit_path=audit,
    )
    assert rc == 1
    assert register_status(reg, "D8") == "NOT_STARTED"
    assert not audit.exists() or audit_lines(audit) == []


def test_promote_demotion_refused(tmp_path):
    """ENFORCED -> BUILDING is never a promotion. Refuse it."""
    reg = make_register(tmp_path, {"D8": "ENFORCED"})
    audit = tmp_path / "audit.log"
    rc = promote(
        "D8", "BUILDING", evidence_comment=6108170419, actor="naya2",
        register_path=reg, audit_path=audit,
    )
    assert rc == 1
    assert register_status(reg, "D8") == "ENFORCED"
    assert audit_lines(audit) == []


def test_promote_unknown_id_refused(tmp_path):
    reg = make_register(tmp_path)
    audit = tmp_path / "audit.log"
    rc = promote(
        "D999", "BUILDING", evidence_comment=6108170419, actor="naya2",
        register_path=reg, audit_path=audit,
    )
    assert rc == 1
    assert audit_lines(audit) == []


def test_promote_missing_evidence_refused(tmp_path):
    reg = make_register(tmp_path, {"D8": "BUILDING"})
    audit = tmp_path / "audit.log"
    # BUILT_AS_CODE without the build PR number
    rc = promote(
        "D8", "BUILT_AS_CODE", evidence_comment=6107942578, actor="naya2",
        register_path=reg, audit_path=audit,
    )
    assert rc == 1
    assert register_status(reg, "D8") == "BUILDING"
    # BUILDING without the sign-in comment
    rc = promote(
        "D9", "BUILDING", actor="naya2", register_path=reg, audit_path=audit
    )
    assert rc == 1
    assert register_status(reg, "D9") == "NOT_STARTED"


def test_promote_malformed_evidence_refused(tmp_path):
    reg = make_register(tmp_path, {"D8": "BUILDING"})
    audit = tmp_path / "audit.log"
    rc = promote(
        "D8", "BUILT_AS_CODE", evidence_pr="not-a-number",
        evidence_comment=6107942578, actor="naya2",
        register_path=reg, audit_path=audit,
    )
    assert rc == 1
    assert register_status(reg, "D8") == "BUILDING"


def test_promote_idempotent_rerun_is_noop(tmp_path):
    """Promoting to the status it already holds writes nothing."""
    reg = make_register(tmp_path, {"D8": "BUILDING"})
    audit = tmp_path / "audit.log"
    before = reg.read_bytes()
    rc = promote(
        "D8", "BUILDING", evidence_comment=6108170419, actor="naya2",
        register_path=reg, audit_path=audit,
    )
    assert rc == 0
    assert reg.read_bytes() == before
    assert audit_lines(audit) == []


def test_promote_corrupt_register_fail_closed(tmp_path):
    reg = tmp_path / "directive-register.json"
    reg.write_text("{ this is not json", encoding="utf-8")
    audit = tmp_path / "audit.log"
    rc = promote(
        "D8", "BUILDING", evidence_comment=6108170419, actor="naya2",
        register_path=reg, audit_path=audit,
    )
    assert rc == 2


def test_promote_missing_actor_refused(tmp_path):
    reg = make_register(tmp_path)
    audit = tmp_path / "audit.log"
    rc = promote(
        "D8", "BUILDING", evidence_comment=6108170419, actor="",
        register_path=reg, audit_path=audit,
    )
    assert rc == 1
    assert register_status(reg, "D8") == "NOT_STARTED"


def test_promote_dry_run_writes_nothing(tmp_path):
    reg = make_register(tmp_path)
    audit = tmp_path / "audit.log"
    before = reg.read_bytes()
    rc = promote(
        "D8", "BUILDING", evidence_comment=6108170419, actor="naya2",
        register_path=reg, audit_path=audit, dry_run=True,
    )
    assert rc == 0
    assert reg.read_bytes() == before
    assert not audit.exists()


# ------------------------------------------------------- status check gate


def git_repo_with_register(tmp_path: Path, entries: list[dict]) -> Path:
    repo = tmp_path / "repo"
    (repo / "BRAIN" / "01-GOVERNANCE").mkdir(parents=True)
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.email", "test@naya"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.name", "test"], cwd=repo, check=True)
    (repo / "BRAIN" / "01-GOVERNANCE" / "directive-register.json").write_text(
        json.dumps(entries, indent=2) + "\n", encoding="utf-8"
    )
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-qm", "base"], cwd=repo, check=True)
    return repo


def tiny_entries(status="NOT_STARTED"):
    return [
        {
            "id": "D8",
            "title": "t",
            "source_issue": 2175,
            "source_comment": "1",
            "owner": "naya2",
            "status": status,
            "evidence_pr": None,
            "wave": 6,
        }
    ]


def commit_all(repo: Path, msg: str):
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-qm", msg], cwd=repo, check=True)


def base_sha(repo: Path) -> str:
    return subprocess.run(
        ["git", "rev-list", "--max-parents=0", "HEAD"],
        cwd=repo, capture_output=True, text=True, check=True,
    ).stdout.strip()


def test_status_check_clean_promotion_passes(tmp_path):
    repo = git_repo_with_register(tmp_path, tiny_entries())
    base = base_sha(repo)
    # Promote D8 with a matching audit line, committed together.
    reg_path = repo / "BRAIN" / "01-GOVERNANCE" / "directive-register.json"
    audit_path = repo / "BRAIN" / "01-GOVERNANCE" / "directive-register-audit.log"
    rc = promote(
        "D8", "BUILDING", evidence_comment=6108170419, actor="naya2",
        register_path=reg_path, audit_path=audit_path,
    )
    assert rc == 0
    commit_all(repo, "promote D8")
    assert status_check_run(repo, base, "HEAD") == 0


def test_status_check_change_without_audit_fails(tmp_path):
    repo = git_repo_with_register(tmp_path, tiny_entries())
    base = base_sha(repo)
    reg_path = repo / "BRAIN" / "01-GOVERNANCE" / "directive-register.json"
    data = json.loads(reg_path.read_text(encoding="utf-8"))
    data[0]["status"] = "BUILDING"
    reg_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    commit_all(repo, "silent hand-edit")
    assert status_check_run(repo, base, "HEAD") == 1


def test_status_check_audit_without_change_fails(tmp_path):
    repo = git_repo_with_register(tmp_path, tiny_entries())
    base = base_sha(repo)
    audit_path = repo / "BRAIN" / "01-GOVERNANCE" / "directive-register-audit.log"
    audit_path.write_text(
        json.dumps(
            {
                "directive_id": "D8",
                "from": "NOT_STARTED",
                "to": "BUILDING",
                "evidence_pr": None,
                "evidence_comment": 6108170419,
                "actor": "naya2",
                "at": "2026-10-11T11:00:00Z",
                "register_sha256": "abc",
            }
        )
        + "\n",
        encoding="utf-8",
    )
    commit_all(repo, "orphan audit line")
    assert status_check_run(repo, base, "HEAD") == 1


def test_status_check_audit_mismatch_fails(tmp_path):
    repo = git_repo_with_register(tmp_path, tiny_entries())
    base = base_sha(repo)
    reg_path = repo / "BRAIN" / "01-GOVERNANCE" / "directive-register.json"
    audit_path = repo / "BRAIN" / "01-GOVERNANCE" / "directive-register-audit.log"
    # Register says NOT_STARTED -> BUILDING, audit claims a different jump.
    data = json.loads(reg_path.read_text(encoding="utf-8"))
    data[0]["status"] = "BUILDING"
    reg_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    audit_path.write_text(
        json.dumps(
            {
                "directive_id": "D8",
                "from": "NOT_STARTED",
                "to": "ENFORCED",  # lies about the landing status
                "evidence_pr": 9999,
                "evidence_comment": 6108170419,
                "actor": "naya2",
                "at": "2026-10-11T11:00:00Z",
                "register_sha256": "abc",
            }
        )
        + "\n",
        encoding="utf-8",
    )
    commit_all(repo, "mismatched audit")
    assert status_check_run(repo, base, "HEAD") == 1


def test_status_check_malformed_audit_line_fails(tmp_path):
    repo = git_repo_with_register(tmp_path, tiny_entries())
    base = base_sha(repo)
    audit_path = repo / "BRAIN" / "01-GOVERNANCE" / "directive-register-audit.log"
    audit_path.write_text("{ not json\n", encoding="utf-8")
    commit_all(repo, "broken audit")
    assert status_check_run(repo, base, "HEAD") == 1


def test_status_check_no_register_at_base_skips_transitions(tmp_path):
    """The initial-registration PR has no base register: validate, don't block."""
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.email", "test@naya"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.name", "test"], cwd=repo, check=True)
    (repo / "x.txt").write_text("base\n")
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-qm", "base"], cwd=repo, check=True)
    base = base_sha(repo)
    (repo / "BRAIN" / "01-GOVERNANCE").mkdir(parents=True)
    (repo / "BRAIN" / "01-GOVERNANCE" / "directive-register.json").write_text(
        json.dumps(tiny_entries(), indent=2) + "\n", encoding="utf-8"
    )
    commit_all(repo, "initial register")
    assert status_check_run(repo, base, "HEAD") == 0


# ------------------------------------------------- live-register dogfood


def test_promote_dry_run_against_live_register():
    """The real register loads through the authority; a dry-run promotes cleanly."""
    assert REAL_REGISTER.exists()
    rc = promote(
        "D8", "BUILDING", evidence_comment=6108170419, actor="naya2",
        register_path=REAL_REGISTER, dry_run=True,
    )
    assert rc == 0
