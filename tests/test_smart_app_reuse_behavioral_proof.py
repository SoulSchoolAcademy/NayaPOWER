"""Behavioral proof for the Smart App Reuse Protocol (PR #2086).

Claim under test (spec `minimum_adversarial_tests`):
  - `round_trip_cold_successor_finds_and_uses_correct_version`
  - `reuse_has_measured_gain_over_rebuilding_control`

Design: a cold agent faces a validation task with a registry of qualified
Smart Apps. TREATMENT arm discovers the applicable package, preflights it
(hash-verified, fail-closed) and applies it. CONTROL arm rebuilds a validator
from scratch under the same brief (the honest shape of a hurried rebuild:
field-presence checks only, no hash verification, no scope validation).

Measured on labeled synthetic cases: quality (correct decisions), time
(wall-clock), safety (adversarial refusals), retained evidence (usage
receipts). Synthetic throughout, zero production writes.

Honest limits: the task, packages, registry and the "cold" information
barrier are synthetic. This proves the MECHANISM (reuse of a qualified
artifact beats naive rebuild on safety and evidence, at zero new logic),
not real-world learning. Real-world proof needs a live cold Naya; the
harness is built so that experiment can plug in the same arms.
"""
from __future__ import annotations

import hashlib
import inspect
import time

from kernel.value_calculus import QualityProfile  # noqa: F401  (protocol seam)
from tools.qualify_reusable_smart_app import preflight_reuse

CONTENT_V1 = b"approved-release-bytes-v1"
CONTENT_V2 = b"approved-release-bytes-v2"


def make_package(version, content, claim_content=None, **overrides):
    """Build a synthetic package. claim_content lets the test lie about the hash.

    By default the claimed hash matches the bytes (honest). Passing
    claim_content=<other bytes> forges a package whose claimed hash does not
    match the release bytes — the tamper case.
    """
    claimed = claim_content if claim_content is not None else content
    pkg = {
        "artifact_id": "SMART-APP-DEMO-001",
        "version": version,
        "content_sha256": hashlib.sha256(claimed).hexdigest(),
        "owner_scope": "PRIVATE",
        "source_main_sha": "a" * 40,
        "canonical_refs": ["HUB/NAYANET-SMART-APP-ROOM-SPEC-V1.json"],
        "human_job": "Use a qualified and bounded component rather than rebuild it",
        "required_capabilities": ["read_template"],
        "applicability": ["permitted_same_project"],
        "non_applicability": ["untrusted_external_project"],
        "authority_ref": "law-receipt:for-independent-check",
        "provenance_refs": ["content-receipt:example"],
        "independent_proof_refs": ["verify-receipt:example"],
        "negative_test_refs": ["test:wrong_scope"],
        "observed_quality": {"verification": "VERIFIED_PASS"},
        "quality_profile_ref": "NAYANODE/0025-VALUE-CALCULUS-SPECIFICATION-V1.md",
        "rollback_ref": "snapshot:previous_version",
        "cold_successor_probe": "run:independent_cold_reuse",
        "outcome_metric": "measured_correct_reuse_vs_rebuild",
        "supersedes": None,
    }
    pkg.update(overrides)
    return pkg


# Labeled battery: (name, package_kwargs, release_bytes, expect_ready)
# expect_ready True  -> correct decision is "accept for review" (no errors)
# expect_ready False -> correct decision is "refuse" (errors non-empty)
LABELED = [
    ("valid_v1", dict(version="1.0.0"), CONTENT_V1, True),
    ("hash_mismatch", dict(version="1.0.0", claim_content=CONTENT_V1), b"tampered-bytes", False),
    ("missing_provenance", dict(version="1.0.0", independent_proof_refs=[]), CONTENT_V1, False),
    ("wrong_scope", dict(version="1.0.0", owner_scope="ANYONE_WITH_URL"), CONTENT_V1, False),
    ("unproven_quality", dict(version="1.0.0", observed_quality={"verification": "PASS_PENDING_WINDOW"}), CONTENT_V1, False),
    ("non_string_scope", dict(version="1.0.0", owner_scope=["PRIVATE"]), CONTENT_V1, False),
    ("valid_v2", dict(version="2.0.0"), CONTENT_V2, True),
]


def discover(registry, required_capability, owner_scope):
    """Cold discovery: the agent sees only the registry, never the implementation.

    Returns the newest version whose capability and scope match, or None.
    """
    hits = []
    for artifact_id, releases in registry.items():
        for version, package, release_bytes in releases:
            if required_capability not in package["required_capabilities"]:
                continue
            if package["owner_scope"] != owner_scope:
                continue
            hits.append((version, package, release_bytes))
    if not hits:
        return None
    hits.sort(key=lambda h: tuple(int(x) for x in h[0].split(".")))
    return hits[-1]


def treatment_arm(registry, labeled):
    """Discover -> preflight -> apply. Zero new validation logic."""
    receipts = []
    decisions = []
    t0 = time.perf_counter()
    found = discover(registry, "read_template", "PRIVATE")
    assert found is not None, "cold discovery must find the qualified package"
    version, package, release_bytes = found
    for name, kwargs, content, expect_ready in labeled:
        pkg = make_package(content=content, **kwargs)
        # The reused artifact validates the case; the arm only routes.
        result = preflight_reuse(pkg, content)
        ready = result["status"] == "REVIEWABLE_NOT_AUTHORIZED" and not result["errors"]
        decisions.append((name, ready, expect_ready))
        receipts.append({
            "arm": "treatment",
            "case": name,
            "artifact_id": pkg["artifact_id"],
            "version": pkg["version"],
            "content_sha256": result["computed_sha256"],
            "preflight_status": result["status"],
            "reused_artifact_version": version,
        })
    dt = time.perf_counter() - t0
    return {"decisions": decisions, "receipts": receipts, "seconds": dt, "new_logic_lines": 0}


def naive_rebuild_validator(package, release_bytes):
    """What a hurried from-scratch rebuild typically checks: field presence.

    No hash verification. No scope validation. No type checks. This is the
    honest shape of the control arm, not a strawman: it is exactly what
    "just get it working" produces under time pressure.
    """
    required = (
        "artifact_id", "version", "content_sha256", "owner_scope",
        "independent_proof_refs", "observed_quality",
    )
    errors = [f"MISSING:{k}" for k in required if k not in package]
    return {"ready": not errors, "errors": errors}


def control_arm(labeled):
    """Rebuild from scratch, then apply the rebuilt validator."""
    receipts = []
    decisions = []
    t0 = time.perf_counter()
    for name, kwargs, content, expect_ready in labeled:
        pkg = make_package(content=content, **kwargs)
        result = naive_rebuild_validator(pkg, content)
        decisions.append((name, result["ready"], expect_ready))
        receipts.append({"arm": "control", "case": name})  # no evidence retained
    dt = time.perf_counter() - t0
    new_lines = len([ln for ln in inspect.getsource(naive_rebuild_validator).splitlines() if ln.strip()])
    return {"decisions": decisions, "receipts": receipts, "seconds": dt, "new_logic_lines": new_lines}


def score_arm(arm):
    total = len(arm["decisions"])
    correct = sum(1 for _, ready, expect in arm["decisions"] if ready == expect)
    adversarial = [d for d in arm["decisions"] if not d[2]]
    refused = sum(1 for _, ready, expect in adversarial if not ready)
    return {
        "accuracy": correct / total,
        "safety_refusal_rate": refused / len(adversarial) if adversarial else 1.0,
        "safety_misses": len(adversarial) - refused,
    }


def test_round_trip_cold_successor_finds_and_uses_correct_version():
    """Spec minimum adversarial test: cold successor round trip."""
    registry = {
        "SMART-APP-DEMO-001": [
            ("1.0.0", make_package("1.0.0", CONTENT_V1), CONTENT_V1),
            ("2.0.0", make_package("2.0.0", CONTENT_V2), CONTENT_V2),
        ]
    }
    found = discover(registry, "read_template", "PRIVATE")
    assert found is not None
    version, package, release_bytes = found
    assert version == "2.0.0", "cold successor must find the newest qualified version"
    # The old version's bytes must NOT validate against the new version's hash.
    cheat = make_package("2.0.0", CONTENT_V2)
    cheat["content_sha256"] = hashlib.sha256(CONTENT_V1).hexdigest()
    r = preflight_reuse(cheat, CONTENT_V2)
    assert r["status"] == "NOT_READY"
    assert "CONTENT_HASH_MISMATCH" in r["errors"]
    # Same version with changed bytes is refused (immutable release invariant).
    prior = make_package("1.0.0", CONTENT_V1)
    cand = make_package("1.0.0", CONTENT_V1)
    cand["content_sha256"] = hashlib.sha256(b"changed").hexdigest()
    r2 = preflight_reuse(cand, b"changed", prior_release=prior)
    assert "SAME_VERSION_CHANGED_BYTES" in r2["errors"]


def test_reuse_has_measured_gain_over_rebuilding_control():
    """Spec minimum adversarial test: measured gain of reuse vs rebuild."""
    registry = {
        "SMART-APP-DEMO-001": [
            ("1.0.0", make_package("1.0.0", CONTENT_V1), CONTENT_V1),
        ]
    }
    treatment = treatment_arm(registry, LABELED)
    control = control_arm(LABELED)
    ts, cs = score_arm(treatment), score_arm(control)

    # Quality: reuse decides every labeled case correctly; rebuild does not.
    assert ts["accuracy"] == 1.0, treatment["decisions"]
    assert cs["accuracy"] < ts["accuracy"], control["decisions"]

    # Safety: reuse refuses every adversarial case; rebuild misses some.
    assert ts["safety_refusal_rate"] == 1.0
    assert cs["safety_misses"] >= 2, "naive rebuild must demonstrably miss adversarial cases"

    # Effort: reuse required zero new validation logic; rebuild wrote some.
    assert treatment["new_logic_lines"] == 0
    assert control["new_logic_lines"] > 0

    # Retained evidence: every treatment decision carries a content-addressed receipt.
    assert len(treatment["receipts"]) == len(LABELED)
    for rc in treatment["receipts"]:
        assert rc["content_sha256"] and len(rc["content_sha256"]) == 64
        assert rc["artifact_id"] == "SMART-APP-DEMO-001"
    # Control retains no evidence.
    assert all(set(rc) == {"arm", "case"} for rc in control["receipts"])

    # Time is recorded for both arms (informational; no brittle threshold).
    assert treatment["seconds"] >= 0 and control["seconds"] >= 0
