"""Candidate-only preflight for reusable Smart App packages.

No publication, LAW grants, Smart Note writes, score promotion or independent
VERIFICATION occur here. Quality decisions delegate to the ONE canonical
kernel.value_calculus implementation.
"""
from __future__ import annotations

import hashlib
import re
from typing import Any, Mapping, Sequence

from kernel.value_calculus import Candidate, QualityProfile, RiskPolicy, evaluate_candidates

SHA256 = re.compile(r"[0-9a-f]{64}\Z")
SHA40 = re.compile(r"[0-9a-f]{40}\Z")
VERSION = re.compile(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\Z")
REQUIRED = (
    "artifact_id", "version", "content_sha256", "owner_scope", "source_main_sha",
    "canonical_refs", "human_job", "required_capabilities", "applicability",
    "non_applicability", "authority_ref", "provenance_refs",
    "independent_proof_refs", "negative_test_refs", "observed_quality",
    "quality_profile_ref", "rollback_ref", "cold_successor_probe",
    "outcome_metric", "supersedes",
)
NONEMPTY_REFS = (
    "canonical_refs", "required_capabilities", "provenance_refs",
    "independent_proof_refs", "negative_test_refs",
)
SCOPES = {"PRIVATE", "SHARED", "COLLECTIVE", "PUBLIC"}


def rank_repair_options(
    candidates: Sequence[Candidate], baseline_id: str, profile: QualityProfile,
    risk_policy: RiskPolicy = RiskPolicy()
) -> dict:
    """No substitute scoring function: run the established hard-gate calculus."""
    return evaluate_candidates(candidates, baseline_id, profile, risk_policy)


def preflight_reuse(
    package: Mapping[str, Any], release_bytes: bytes,
    *, prior_release: Mapping[str, Any] | None = None,
) -> dict:
    """Check local package consistency. The result NEVER grants publication.

    This function cannot attest external proof or authenticated LAW grants. A
    clean preflight means 'send to real owner/independent verifier', NOT ACTIVE.
    """
    errors: list[str] = []
    if not isinstance(package, Mapping):
        return {"status": "NOT_READY", "errors": ["PACKAGE_MUST_BE_OBJECT"], "publishing_authorized": False}
    missing = [key for key in REQUIRED if key not in package]
    errors.extend("REQUIRED_FIELD_MISSING:" + key for key in missing)
    if missing:
        return {"status": "NOT_READY", "errors": errors, "publishing_authorized": False}

    ident = package["artifact_id"]
    if not isinstance(ident, str) or not ident.strip():
        errors.append("ARTIFACT_ID_INVALID")
    version = package["version"]
    if not isinstance(version, str) or not VERSION.fullmatch(version):
        errors.append("SEMANTIC_VERSION_INVALID")
    hash_value = package["content_sha256"]
    if not isinstance(hash_value, str) or not SHA256.fullmatch(hash_value):
        errors.append("CONTENT_HASH_INVALID")
    elif hashlib.sha256(release_bytes).hexdigest() != hash_value:
        errors.append("CONTENT_HASH_MISMATCH")
    source = package["source_main_sha"]
    if not isinstance(source, str) or not SHA40.fullmatch(source):
        errors.append("SOURCE_SHA_INVALID")
    scope = package["owner_scope"]
    if not isinstance(scope, str) or scope not in SCOPES:
        errors.append("SCOPE_INVALID")
    for key in NONEMPTY_REFS:
        value = package[key]
        if not isinstance(value, list) or not value or any(not isinstance(v, str) or not v.strip() for v in value):
            errors.append("REQUIRED_REFERENCES_MISSING:" + key)
    for key in ("human_job", "authority_ref", "quality_profile_ref", "rollback_ref", "cold_successor_probe", "outcome_metric"):
        value = package[key]
        if not isinstance(value, str) or not value.strip():
            errors.append("FIELD_EMPTY:" + key)
    for key in ("applicability", "non_applicability"):
        if not isinstance(package[key], list) or not package[key]:
            errors.append("SCOPE_CONDITIONS_MISSING:" + key)
    quality = package["observed_quality"]
    if not isinstance(quality, Mapping) or quality.get("verification") != "VERIFIED_PASS":
        errors.append("INDEPENDENT_OUTCOME_UNPROVEN")
    if prior_release is not None:
        if prior_release.get("artifact_id") == ident and prior_release.get("version") == version:
            if prior_release.get("content_sha256") != hash_value:
                errors.append("SAME_VERSION_CHANGED_BYTES")
        if prior_release.get("artifact_id") == ident and prior_release.get("version") != version:
            if prior_release.get("content_sha256") == hash_value:
                errors.append("UNNECESSARY_VERSION_WITH_IDENTICAL_BYTES")
    return {
        "status": "NOT_READY" if errors else "REVIEWABLE_NOT_AUTHORIZED",
        "errors": errors,
        "computed_sha256": hashlib.sha256(release_bytes).hexdigest(),
        "publishing_authorized": False,
        "independent_proof_verified_here": False,
        "next_gate": "EXTERNAL_VERIFIER_AND_LAW_AUTHORITY_CHECK" if not errors else "REPAIR_PACKAGE_EVIDENCE",
    }
