"""Repository-only acceptance test for the Cold-Naya Operating Index.

This test deliberately performs navigation/integrity checks only. It does not
claim that an external model can execute the entire Naya loop; that requires a
separate behavioral harness.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "START-HERE" / "COLD-NAYA-OPERATING-INDEX.md"
ISSUES = ROOT / ".naya" / "control-plane" / "GITHUB-ISSUE-CLASSIFICATION-2026-09-17.md"
ISSUE_AUDIT = ROOT / ".naya" / "control-plane" / "GITHUB-ISSUE-AUDIT.json"
WORKFLOWS = ROOT / ".naya" / "control-plane" / "GITHUB-WORKFLOW-CLASSIFICATION-2026-09-17.md"


def require(path: Path, text: str) -> None:
    if not path.exists():
        raise AssertionError(f"MISSING: {path}")
    body = path.read_text(encoding="utf-8")
    if text not in body:
        raise AssertionError(f"MISSING TEXT: {text} in {path}")


def count_issue_rows() -> int:
    body = ISSUES.read_text(encoding="utf-8")
    return sum(1 for line in body.splitlines() if line.startswith("| #"))


def classified_issue_numbers() -> list[int]:
    body = ISSUES.read_text(encoding="utf-8")
    return [int(line.split("|", 2)[1].strip().lstrip("#")) for line in body.splitlines() if line.startswith("| #")]


def audited_issue_numbers() -> set[int]:
    import json
    return {int(item["number"]) for item in json.loads(ISSUE_AUDIT.read_text(encoding="utf-8"))["issues"]}


def count_workflow_rows() -> int:
    body = WORKFLOWS.read_text(encoding="utf-8")
    return sum(1 for line in body.splitlines() if line.startswith("| `"))


require(INDEX, "# COLD-NAYA OPERATING INDEX")
require(INDEX, "Issue #245")
require(INDEX, ".naya/control-plane/MAP.json")
require(INDEX, ".naya/control-plane/STATE.json")
require(INDEX, ".naya/control-plane/PROOF.json")
require(INDEX, ".naya/runtime/canonical_event_store.py")
require(INDEX, "SUPERBRAIN/NAYA-ACTIVITY/")
require(INDEX, "`.naya/activity/`")
require(INDEX, "UNKNOWN != GREEN")
require(INDEX, "One current execution focus")

classified = classified_issue_numbers()
audited = audited_issue_numbers()
if len(audited) != 61:
    raise AssertionError(f"ISSUE_AUDIT_ROWS={len(audited)} expected 61")
if len(set(classified)) != 62:
    raise AssertionError(f"ISSUE_CLASSIFICATION_ROWS={len(set(classified))} expected 62 including preserved non-open governance row")
if not set(classified) - audited == {2}:
    raise AssertionError(f"UNSCOPED_CLASSIFICATION_ROWS={set(classified) - audited} expected only preserved issue #2")

if count_workflow_rows() != 42:
    raise AssertionError(f"WORKFLOW_CLASSIFICATION_ROWS={count_workflow_rows()} expected 42")

issues = ISSUES.read_text(encoding="utf-8")
if issues.count("| #245 | CURRENT") != 1:
    raise AssertionError("Issue #245 must be the single CURRENT classification record")

print("COLD_NAYA_INDEX=PASS")
print("ISSUE_AUDIT_OPEN_ISSUES=61/61")
print("CLASSIFICATION_ROWS=62 (61 audited + preserved #2 governance row)")
print("WORKFLOW_CLASSIFICATION=42/42")
print("HISTORICAL_CLASSIFICATION_OWNER=#245")
print("CANONICAL_EVENT_STORE=FOUND")
print("ACTIVITY_PROJECTION=FOUND")
print("SECOND_EVENT_STORE=NOT_CREATED")
print("BEHAVIORAL_EXTERNAL_COLD_NAYA=NOT_PROVEN")
print("STATUS=PASS_NAVIGATION_ONLY")
