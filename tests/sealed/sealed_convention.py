#!/usr/bin/env python3
"""Sealed-fixture convention machinery (spec + enforcement).

Law source: drift-canary audit 2026-10-10 — 218 test files expose answer keys
inline, the in-repo qualification receipts are compromised FOR BLIND USE, and
the T11 fixture family (QUAL-20261010-CIQ-001) was RETIRED from blind use. The
convention below is the "smallest safe separation": answer keys live OUTSIDE
the repo; only SHA-256 commitments appear in-repo.

The one good prior example: QUAL-20261010-CIQ-001's sealed key — SHA-256 only
in the plan appendix, raw key held outside the repo (qualification-plan
Appendix A: sha256 109f6c30...05217). This module makes that pattern the law.

Roles (separation of duties):
  - FIXTURE AUTHOR: designs task families, generates tasks, seals keys. Never
    runs a qualification against the fixtures, never certifies anything.
  - EVALUATOR: holds the keys, runs the blind trial, scores, reports. The
    author and the evaluator are different seats (Naya 2 / Coda 1's seat for
    the qualification program).

Custody pattern (interim, matches the T11 precedent):
  - Raw answer keys are written ONLY outside the repo — currently the
    director's hidden_files (~/workspace/goals/<goal>/hidden_files/).
  - The permanent evaluation-service-held store needs Shawn's word
    (drift-canary §4, "Needs Shawn's word").
  - Keys files MUST carry the sentinel first line
    "SEALED-ANSWER-KEY" + "-DO-NOT-COMMIT" so the repo gate catches
    accidental commits.

Integrity states (from drift-canary integrity.py):
  sealed -> suspect -> compromised -> retired -> replaced. Never back to
  sealed. A family that touches the repo in raw form is compromised, full
  stop; the replacement must be disjoint (see the T12 design rationale).
"""

import hashlib
import json
import re
from pathlib import Path

# ---------------------------------------------------------------------------
# Sentinel and manifest schema
# ---------------------------------------------------------------------------

# Built by concatenation so this module's own source never carries the literal
# sentinel (the repo gate scans for the literal and self-excludes this file).
SENTINEL = "SEALED-ANSWER-KEY" + "-DO-NOT-COMMIT"

COMMITMENT_RE = re.compile(r"^[0-9a-f]{64}$")

# Fields that may never appear anywhere inside tests/sealed/manifests/*.json.
# They signal raw answer material leaked into a commitment record.
FORBIDDEN_MANIFEST_FIELDS = {
    "answer",
    "answers",
    "expected",
    "expected_decision",
    "expected_source_kind",
    "correct",
    "label",
    "labels",
    "answer_key",
    "key_material",
    "rationale",
}

REQUIRED_MANIFEST_TOP_LEVEL = {"family_id", "schema_version", "tasks"}


# ---------------------------------------------------------------------------
# Commitment machinery
# ---------------------------------------------------------------------------

def canonical_answer_record(task_id: str, expected_decision: str,
                            expected_source_kind: str) -> str:
    """The canonical byte string that a commitment is taken over.

    Sort-keys, no whitespace: the same logical record always hashes the same,
    whatever tooling produced it. The evaluator recomputes this from the held
    key file and compares against the in-repo commitment.
    """
    record = {
        "task_id": task_id,
        "expected_decision": expected_decision,
        "expected_source_kind": expected_source_kind,
    }
    return json.dumps(record, sort_keys=True, separators=(",", ":"))


def commit_answer(task_id: str, expected_decision: str,
                  expected_source_kind: str) -> str:
    """SHA-256 commitment for one task's answer. Answers never enter the repo;
    this hex digest is what gets committed instead."""
    payload = canonical_answer_record(task_id, expected_decision,
                                      expected_source_kind)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def verify_commitment(commitment: str, task_id: str, expected_decision: str,
                      expected_source_kind: str) -> bool:
    """Evaluator-side: does the held answer match the in-repo commitment?"""
    if not COMMITMENT_RE.match(commitment or ""):
        return False
    return commit_answer(task_id, expected_decision,
                         expected_source_kind) == commitment


def seal_answer_key(key_records: list) -> tuple:
    """Seal a full key file's worth of records.

    key_records: list of (task_id, expected_decision, expected_source_kind).
    Returns (key_sha256, {task_id: commitment}). The key_sha256 authenticates
    the whole key file; the per-task map is what lands in the manifest.
    """
    canonical = "\n".join(
        canonical_answer_record(t, d, s) for (t, d, s) in key_records
    )
    key_sha256 = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    commitments = {
        task_id: commit_answer(task_id, dec, kind)
        for (task_id, dec, kind) in key_records
    }
    return key_sha256, commitments


# ---------------------------------------------------------------------------
# Manifest schema validation (used by the CI gate)
# ---------------------------------------------------------------------------

def validate_manifest(manifest: dict) -> list:
    """Return a list of violation strings; empty means the manifest is clean.

    A clean manifest contains commitments ONLY — no answer material.
    """
    violations = []
    if not isinstance(manifest, dict):
        return ["manifest root is not an object"]
    missing = REQUIRED_MANIFEST_TOP_LEVEL - set(manifest)
    if missing:
        violations.append(f"missing top-level fields: {sorted(missing)}")
    tasks = manifest.get("tasks")
    if not isinstance(tasks, dict) or not tasks:
        violations.append("tasks must be a non-empty object")
        tasks = {}
    for task_id, rec in tasks.items():
        if not isinstance(rec, dict):
            violations.append(f"task {task_id}: record is not an object")
            continue
        if set(rec.keys()) != {"task_id", "commitment"}:
            violations.append(
                f"task {task_id}: record keys must be exactly "
                f"{{task_id, commitment}}, got {sorted(rec.keys())}"
            )
        if rec.get("task_id") != task_id:
            violations.append(f"task {task_id}: task_id mismatch inside record")
        if not COMMITMENT_RE.match(str(rec.get("commitment") or "")):
            violations.append(f"task {task_id}: commitment is not a sha256 hex")
    _walk_for_forbidden(manifest, "$", violations)
    return violations


def _walk_for_forbidden(node, path: str, violations: list):
    if isinstance(node, dict):
        for k, v in node.items():
            if k in FORBIDDEN_MANIFEST_FIELDS:
                violations.append(
                    f"forbidden answer-material field '{k}' at {path}"
                )
            _walk_for_forbidden(v, f"{path}.{k}", violations)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            _walk_for_forbidden(v, f"{path}[{i}]", violations)


def validate_manifest_file(path: Path) -> list:
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"{path}: unreadable or not JSON: {exc}"]
    return [f"{path}: {v}" for v in validate_manifest(manifest)]
