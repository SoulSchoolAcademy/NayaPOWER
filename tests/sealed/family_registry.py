#!/usr/bin/env python3
"""Machine-readable blind-family registry (Phase 3A activation).

Law sources:
  - tests/sealed/README.md — the sealed-fixture convention (SHA commitments
    in-repo, raw keys outside).
  - Drift-canary exposure audit, 2026-10-10 — 218 test files expose answer
    keys inline; T11 retired from blind use.
  - Shawn, 2026-10-10 — key custody = the math (Wisest Choice Law).

Integrity lifecycle (from drift_canary/integrity.py):
    sealed -> suspect -> compromised -> retired -> replaced
Never backwards. A family whose answers touched the repo (or any shared
readable surface) is compromised, full stop; the replacement must be
disjoint (fresh tasks, fresh lesson, fresh seed).

This registry is what the CI gates in test_blind_family_gate.py enforce.
"""

# States a family may hold, in lifecycle order. Transitions only move
# forward; "replaced" points at the successor family.
LIFECYCLE = ("sealed", "suspect", "compromised", "retired", "replaced")

FAMILIES = {
    "QUAL-20261010-CIQ-001": {
        "code": "T11",
        "name": "The Reserve Rule",
        "state": "retired",
        "blind_eligible": False,
        "retirement_reason": (
            "Answers exposed in the database and local JSON receipts "
            "(2026-10-10). Retired from blind use; useful for regression, "
            "never for fresh blind qualification."
        ),
        "replaced_by": "QUAL-20261010-CIQ-012",
        "manifest": None,  # retired before the sealed convention existed
    },
    "QUAL-20261010-CIQ-012": {
        "code": "T12",
        "name": "The Second-Read Rule",
        "state": "sealed",
        "blind_eligible": True,
        "manifest": "manifests/QUAL-20261010-CIQ-012-t12.json",
        "task_id_prefix": "T12-",
    },
}


def get_family(qualification_id: str) -> dict | None:
    """Return the registry record, or None if the family is unknown."""
    return FAMILIES.get(qualification_id)


def blind_eligible(qualification_id: str) -> bool:
    """Fail-closed: unknown families are NOT blind-eligible."""
    fam = FAMILIES.get(qualification_id)
    return bool(fam and fam["state"] == "sealed" and fam["blind_eligible"])


def assert_valid_lifecycle() -> list:
    """Registry self-check: every family sits on the lifecycle, retired
    families name their replacement, sealed families have manifests."""
    problems = []
    for qid, fam in FAMILIES.items():
        if fam["state"] not in LIFECYCLE:
            problems.append(f"{qid}: unknown state {fam['state']!r}")
        if fam["state"] == "retired" and not fam.get("replaced_by"):
            problems.append(f"{qid}: retired but names no replacement")
        if fam["state"] == "sealed":
            if not fam.get("blind_eligible"):
                problems.append(f"{qid}: sealed but not blind-eligible")
            if not fam.get("manifest"):
                problems.append(f"{qid}: sealed but has no manifest")
    return problems
