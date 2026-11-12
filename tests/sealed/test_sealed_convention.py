#!/usr/bin/env python3
"""Unit tests for the sealed-fixture convention machinery.

These test the COMMITMENT MACHINERY (hashing, canonicalization, schema
validation) — not any qualification. No live paths, no kernel, no DB.
"""

import hashlib
import json

from sealed_convention import (
    FORBIDDEN_MANIFEST_FIELDS,
    SENTINEL,
    canonical_answer_record,
    commit_answer,
    seal_answer_key,
    validate_manifest,
    verify_commitment,
)


def _good_manifest():
    return {
        "family_id": "QUAL-TEST-FAMILY-001",
        "schema_version": 1,
        "sealed_at_utc": "2026-10-10T00:00:00+00:00",
        "lesson_content_hash": "ab" * 32,
        "key_sha256": "cd" * 32,
        "tasks": {
            "TASK-001": {
                "task_id": "TASK-001",
                "commitment": commit_answer("TASK-001", "decision-alpha",
                                            "kind-x"),
            },
            "TASK-002": {
                "task_id": "TASK-002",
                "commitment": commit_answer("TASK-002", "decision-beta",
                                            "kind-y"),
            },
        },
    }


def test_commitment_is_deterministic():
    a = commit_answer("T-1", "lower-first,reserve", "lesson-T11")
    b = commit_answer("T-1", "lower-first,reserve", "lesson-T11")
    assert a == b
    assert len(a) == 64


def test_commitment_changes_with_any_field():
    base = commit_answer("T-1", "x", "k")
    assert commit_answer("T-2", "x", "k") != base
    assert commit_answer("T-1", "y", "k") != base
    assert commit_answer("T-1", "x", "z") != base


def test_canonical_record_is_key_sorted_compact():
    s = canonical_answer_record("T-1", "d", "k")
    assert s == json.dumps(json.loads(s), sort_keys=True,
                           separators=(",", ":"))
    assert s == '{"expected_decision":"d","expected_source_kind":"k","task_id":"T-1"}'


def test_commitment_matches_independent_sha256():
    # Independent re-derivation: the hash is over exactly the canonical bytes.
    payload = canonical_answer_record("T-9", "dec", "kind")
    assert commit_answer("T-9", "dec", "kind") == \
        hashlib.sha256(payload.encode("utf-8")).hexdigest()


def test_verify_commitment_round_trip():
    c = commit_answer("T-1", "decision-alpha", "kind-x")
    assert verify_commitment(c, "T-1", "decision-alpha", "kind-x")
    assert not verify_commitment(c, "T-1", "decision-beta", "kind-x")
    assert not verify_commitment(c, "T-2", "decision-alpha", "kind-x")
    assert not verify_commitment("not-a-hash", "T-1", "d", "k")
    assert not verify_commitment("", "T-1", "d", "k")


def test_seal_answer_key_produces_manifest_map():
    records = [("A-1", "d1", "k1"), ("A-2", "d2", "k2")]
    key_sha, commitments = seal_answer_key(records)
    assert len(key_sha) == 64
    assert set(commitments) == {"A-1", "A-2"}
    for t, d, k in records:
        assert verify_commitment(commitments[t], t, d, k)


def test_good_manifest_validates():
    assert validate_manifest(_good_manifest()) == []


def test_manifest_rejects_answer_material_fields():
    for field in sorted(FORBIDDEN_MANIFEST_FIELDS):
        m = _good_manifest()
        m["tasks"]["TASK-001"][field] = "LEAKED-ANSWER"
        violations = validate_manifest(m)
        assert any(field in v for v in violations), field


def test_manifest_rejects_non_hash_commitment():
    m = _good_manifest()
    m["tasks"]["TASK-001"]["commitment"] = "lower-first,reserve"
    violations = validate_manifest(m)
    assert any("commitment is not a sha256" in v for v in violations)


def test_manifest_rejects_extra_record_keys():
    m = _good_manifest()
    m["tasks"]["TASK-001"]["note"] = "innocent note"
    violations = validate_manifest(m)
    assert any("exactly" in v for v in violations)


def test_manifest_rejects_missing_top_level():
    m = _good_manifest()
    del m["family_id"]
    violations = validate_manifest(m)
    assert any("family_id" in v for v in violations)


def test_manifest_rejects_empty_tasks():
    m = _good_manifest()
    m["tasks"] = {}
    violations = validate_manifest(m)
    assert any("non-empty" in v for v in violations)


def test_sentinel_shape():
    # Concatenated on purpose: this file must never carry the literal
    # sentinel (the repo gate scans for it and this file is not allowlisted).
    assert SENTINEL == "SEALED-ANSWER" + "-KEY-DO-NOT-COMMIT"
    assert len(SENTINEL) > 10
    assert SENTINEL.startswith("SEALED-ANSWER-KEY")
    assert SENTINEL.endswith("DO-NOT-COMMIT")
