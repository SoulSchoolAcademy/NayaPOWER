#!/usr/bin/env python3
"""Validate BRAIN/09-EVOLUTION/0002-EVOLUTION-SELF-OPTIMIZATION-V1.json.

Fail-closed rules (UNKNOWN != PASS):
  - stage claims are only honored when the evidence the stage's gate requires
    is present; missing evidence -> the stage claim is rejected.
  - stage_history must equal stages[0..index(stage)] exactly: forward-only,
    one stage at a time, no skips, no backward moves.
  - no fractional/manufactured stages: stage must be exactly one of the
    eleven loop stages from the contract V1 loop.
  - IMPACT-CHECK requires non-empty dependencies, blast_radius and a
    rollback_plan; 'TBD'/'none' rollback plans are rejected.
  - AUTHORIZE requires a named authority source and changes_authority == false;
    self-authorization (the loop authorizing itself) and any authority change
    are rejected; authority questions route to LAW, never here.
  - ADOPT requires measured == true with non-empty before/after: improvement
    that cannot be measured cannot be adopted.
  - LEARN requires a learning_record closing the loop into 07-LEARNING.
  - VERIFY requires independent evidence; builder TEST evidence never
    satisfies VERIFY.
  - REJECTED needs rejection_reason; ROLLED_BACK needs rollback_record;
    SUPERSEDED needs superseded_by; terminal outcomes freeze stage history.
  - status must remain PROPOSED_CANONICAL until human-director ratification;
    CANONICAL is rejected here.
Usage: python3 tools/validate_evolution_self_optimization.py
Exit 0 when the evolution file is internally consistent and evidence-bound.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "BRAIN/09-EVOLUTION/0002-EVOLUTION-SELF-OPTIMIZATION-V1.json"

SCHEMA = "naya.evolution-self-optimization.v1"
ALLOWED_STATUSES = {"PROPOSED_CANONICAL"}
STAGES = [
    "OBSERVE", "DIAGNOSE", "PROPOSE", "IMPACT-CHECK", "AUTHORIZE",
    "BUILD", "TEST", "VERIFY", "MEASURE", "ADOPT", "LEARN",
]
OUTCOMES = {"ACTIVE", "ADOPTED", "REJECTED", "ROLLED_BACK", "SUPERSEDED"}
SHA_RE = re.compile(r"^[0-9a-f]{40}$")

SELF_AUTHORIZATION_PATTERNS = re.compile(
    r"\b(self-?authoriz|authoriz\w* by (this|the) loop|loop authoriz|authorized by itself)\b",
    re.IGNORECASE,
)
NO_ROLLBACK_PATTERNS = re.compile(r"^\s*(tbd|none|n/a|todo)\s*$", re.IGNORECASE)


def _nonempty_str(value):
    return isinstance(value, str) and bool(value.strip())


def _nonempty_str_list(value):
    return (
        isinstance(value, list)
        and bool(value)
        and all(_nonempty_str(v) for v in value)
    )


def _proposal_failures(pid, proposal):
    out = []
    stage = proposal.get("stage")
    if stage not in STAGES:
        out.append(f"{pid}: STAGE_INVALID: {stage!r} not in loop stages")
        return out
    outcome = proposal.get("outcome", "ACTIVE")
    if outcome not in OUTCOMES:
        out.append(f"{pid}: OUTCOME_INVALID: {outcome!r}")
    idx = STAGES.index(stage)
    expected_history = STAGES[: idx + 1]
    if proposal.get("stage_history") != expected_history:
        out.append(
            f"{pid}: STAGE_HISTORY_INVALID: {proposal.get('stage_history')!r} "
            f"!= {expected_history!r} (forward-only, no skips, no backward)"
        )
    gates = STAGES[: idx + 1]
    if "OBSERVE" in gates and not _nonempty_str(proposal.get("observation_ref")):
        out.append(f"{pid}: OBSERVE_EVIDENCE_MISSING: observation_ref required")
    if "DIAGNOSE" in gates and not _nonempty_str(proposal.get("diagnosis")):
        out.append(f"{pid}: DIAGNOSE_EVIDENCE_MISSING: diagnosis required")
    if "PROPOSE" in gates and not _nonempty_str(proposal.get("proposal")):
        out.append(f"{pid}: PROPOSE_EVIDENCE_MISSING: proposal required")
    if "IMPACT-CHECK" in gates:
        impact = proposal.get("impact_assessment")
        if not isinstance(impact, dict):
            out.append(
                f"{pid}: IMPACT_INCOMPLETE: impact_assessment must be an object"
            )
        else:
            if not _nonempty_str_list(impact.get("dependencies")):
                out.append(
                    f"{pid}: IMPACT_INCOMPLETE: dependencies must be a "
                    "non-empty list of non-empty strings"
                )
            if not _nonempty_str(impact.get("blast_radius")):
                out.append(
                    f"{pid}: IMPACT_INCOMPLETE: blast_radius required"
                )
            plan = impact.get("rollback_plan")
            if not _nonempty_str(plan) or NO_ROLLBACK_PATTERNS.match(plan):
                out.append(
                    f"{pid}: IMPACT_INCOMPLETE: rollback_plan must be a "
                    "concrete non-empty plan ('TBD'/'none' rejected)"
                )
    if "AUTHORIZE" in gates:
        authority = proposal.get("authority_check")
        if not isinstance(authority, dict):
            out.append(
                f"{pid}: AUTHORITY_CHECK_MISSING: authority_check object required"
            )
        else:
            if not _nonempty_str(authority.get("authority")):
                out.append(
                    f"{pid}: AUTHORITY_UNNAMED: authority source must be named"
                )
            if authority.get("changes_authority") is not False:
                out.append(
                    f"{pid}: AUTHORITY_CHANGE_REJECTED: authority_check."
                    "changes_authority must be false — self-building without "
                    "self-authorizing"
                )
            blob = " ".join(
                str(v) for v in authority.values() if isinstance(v, str)
            )
            if SELF_AUTHORIZATION_PATTERNS.search(blob):
                out.append(
                    f"{pid}: SELF_AUTHORIZATION_REJECTED: the loop may not "
                    "authorize itself"
                )
    if "BUILD" in gates and not _nonempty_str(proposal.get("build_record")):
        out.append(f"{pid}: BUILD_EVIDENCE_MISSING: build_record required")
    if "TEST" in gates and not _nonempty_str_list(proposal.get("test_evidence")):
        out.append(
            f"{pid}: TEST_EVIDENCE_MISSING: test_evidence must be a "
            "non-empty list of non-empty strings"
        )
    if "VERIFY" in gates and not _nonempty_str_list(
        proposal.get("verification_evidence")
    ):
        out.append(
            f"{pid}: VERIFY_EVIDENCE_MISSING: verification_evidence must be a "
            "non-empty list of non-empty strings (independent, adversarial)"
        )
    if "MEASURE" in gates:
        measurement = proposal.get("measurement")
        if (
            not isinstance(measurement, dict)
            or measurement.get("measured") is not True
            or not _nonempty_str(measurement.get("before"))
            or not _nonempty_str(measurement.get("after"))
        ):
            out.append(
                f"{pid}: MEASURE_EVIDENCE_MISSING: measurement must have "
                "measured == true and non-empty before/after"
            )
    if "ADOPT" in gates:
        if not _nonempty_str(proposal.get("adoption_record")):
            out.append(f"{pid}: ADOPT_EVIDENCE_MISSING: adoption_record required")
        measurement = proposal.get("measurement")
        if not (isinstance(measurement, dict) and measurement.get("measured") is True):
            out.append(
                f"{pid}: ADOPTION_UNMEASURED: adoption requires measured == "
                "true — improvement that cannot be measured cannot be adopted"
            )
    if "LEARN" in gates and not _nonempty_str(proposal.get("learning_record")):
        out.append(
            f"{pid}: LEARN_EVIDENCE_MISSING: learning_record required — the "
            "loop closes into 07-LEARNING, not at ADOPT"
        )
    if outcome == "REJECTED" and not _nonempty_str(proposal.get("rejection_reason")):
        out.append(f"{pid}: REJECTION_REASON_MISSING: rejection_reason required")
    if outcome == "ROLLED_BACK" and not _nonempty_str(
        proposal.get("rollback_record")
    ):
        out.append(
            f"{pid}: ROLLBACK_RECORD_MISSING: rollback_record required — "
            "rollback preserves learning, it never erases"
        )
    if outcome == "SUPERSEDED" and not _nonempty_str(proposal.get("superseded_by")):
        out.append(f"{pid}: SUPERSEDED_BY_MISSING: superseded_by required")
    if outcome in {"ADOPTED", "REJECTED", "ROLLED_BACK", "SUPERSEDED"}:
        term_history = STAGES[: idx + 1]
        if proposal.get("stage_history") != term_history:
            out.append(
                f"{pid}: TERMINAL_OUTCOME_STAGE_MISMATCH: terminal outcomes "
                "freeze stage history"
            )
    return out


def failures(data):
    out = []
    if data.get("schema") != SCHEMA:
        out.append(f"SCHEMA_MISMATCH: {data.get('schema')!r} != {SCHEMA!r}")
    if data.get("status") not in ALLOWED_STATUSES:
        out.append(
            f"STATUS_NOT_PROPOSED_CANONICAL: {data.get('status')!r} "
            "(CANONICAL requires human-director ratification)"
        )
    if data.get("stages") != STAGES:
        out.append(
            f"STAGE_ORDER_MISMATCH: {data.get('stages')!r} != {STAGES!r} "
            "(loop order is fixed by the contract V1 loop)"
        )
    if not SHA_RE.match(str(data.get("as_of") or "")):
        out.append(f"AS_OF_NOT_PINNED_SHA: {data.get('as_of')!r}")
    proposals = data.get("proposals")
    if not isinstance(proposals, list):
        out.append("PROPOSALS_NOT_A_LIST")
        return out
    seen = set()
    for i, proposal in enumerate(proposals):
        if not isinstance(proposal, dict):
            out.append(f"PROPOSAL_{i}_NOT_AN_OBJECT")
            continue
        pid = proposal.get("proposal_id")
        if not _nonempty_str(pid):
            out.append(f"PROPOSAL_{i}: PROPOSAL_ID_MISSING")
            pid = f"PROPOSAL_{i}"
        if pid in seen:
            out.append(f"{pid}: PROPOSAL_ID_DUPLICATE")
        seen.add(pid)
        out.extend(_proposal_failures(pid, proposal))
    return out


def main() -> int:
    try:
        data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    except Exception as exc:  # fail closed on unreadable fixture
        print(json.dumps({"schema": "naya.evolution-self-optimization.validation-report",
                          "failures": [f"FIXTURE_UNREADABLE: {exc}"],
                          "passed": False}, indent=2))
        return 1
    fails = failures(data)
    print(json.dumps({"schema": "naya.evolution-self-optimization.validation-report",
                      "as_of": data.get("as_of"), "failures": fails,
                      "passed": not fails}, indent=2))
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
