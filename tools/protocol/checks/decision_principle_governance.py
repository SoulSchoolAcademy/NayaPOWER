#!/usr/bin/env python3
"""Decision Principle Governance (mechanical gate).

Shawn's principle, as code that fails:

    FIRST — HARD GATES
        Protect people · Tell the truth · Respect authority
    THEN — INTELLIGENT OPTIMIZATION
        a* = argmax over A_admissible of V_verified(a)

The critical distinction this gate enforces: an action that violates a
non-negotiable human protection is DISQUALIFIED from the competition
entirely — not scored zero. Disqualification is exclusion, not a score.
A disqualified action cannot win on other dimensions, no matter how high
its verified value.

This gate does NOT make decisions. It proves the decision machinery
honors the principle. Three proofs, every run:

  1. CROSS-IMPLEMENTATION AGREEMENT — the DecisionEngine and an
     independently written implementation (sharing no code paths) must
     agree on the disqualified set, the admissible set, the chosen action,
     and the outcome, across a hand-built edge-case battery AND
     deterministic randomized scenarios. If two independent readings of
     the principle diverge, the principle is ambiguous — fail.

  2. PIPELINE EXCLUSION — the live value_calculus pipeline
     (gate_candidate + evaluate_candidates, the actual code that decides)
     must exclude every PROHIBITED candidate from the ranked set, the
     top-3, and the final decision. Scoring must never happen before
     gating. A PROHIBITED candidate appearing anywhere in the optimized
     output is a fail.

  3. VERDICT MAPPING — the value_calculus gate verdicts must map
     correctly into the decision-principle verdict space:
     PROHIBITED -> DISQUALIFIED, NEEDS_AUTHORITY/NEEDS_EVIDENCE ->
     DEFERRED, ADMISSIBLE -> ADMISSIBLE. Unknown verdicts fail closed.

What it does NOT prove (said out loud): that the gate thresholds
(severity 7.0, probability 0.05) are the right values — those are policy,
set by the director, reviewed by humans. That the evidence feeding the
gates is true — garbage in, garbage out is a different exploit class.
This gate proves the ARCHITECTURE: gates run before optimization, always,
and disqualification is exclusion, never a score.

Fail-closed: any import error, any proof raising AssertionError, any
unexpected exception fails the check — never silently passes.

Usage:
    python3 tools/protocol/checks/decision_principle_governance.py [--record '{}']

Input record: {} (no inputs required; the gate is self-contained).
Exit 0: all three proofs pass. Exit 1: any proof fails, with the
divergence or violation named.
"""

from __future__ import annotations

import json
import sys


def _repo_root() -> str:
    import os
    here = os.path.abspath(__file__)
    # tools/protocol/checks/decision_principle_governance.py -> repo root
    for _ in range(4):
        here = os.path.dirname(here)
    return here


def run_governance() -> dict:
    """Run all three governance proofs. Returns evidence; raises on failure."""
    sys.path.insert(0, _repo_root())

    from kernel.decision_principle import (
        cross_verify,
        random_scenarios,
        scenario_battery,
        verdict_from_calculus_gate,
        verify_pipeline_excludes_first,
        ADMISSIBLE,
        DISQUALIFIED,
        DEFERRED,
    )

    evidence: dict = {"proofs": {}}

    # ---- Proof 1: cross-implementation agreement --------------------------
    battery = scenario_battery()
    cross_verify(battery)
    evidence["proofs"]["handbuilt_battery"] = {
        "scenarios": len(battery), "agreed": True,
    }

    for seed in (7, 20261011):
        scenarios = random_scenarios(seed, 60)
        cross_verify(scenarios)
        evidence["proofs"][f"randomized_seed_{seed}"] = {
            "scenarios": len(scenarios), "agreed": True,
        }

    # ---- Proof 2: live pipeline excludes prohibited before optimizing -----
    from kernel.value_calculus import (
        Candidate,
        PVEstimate,
        QualityProfile,
        RiskPolicy,
        gate_candidate,
    )

    profile = QualityProfile(
        profile_id="DECISION-PRINCIPLE-GOVERNANCE",
        version="1.0",
        objective="prove the decision principle governs the pipeline",
    )
    policy = RiskPolicy()

    def cand(cid: str, **kw) -> Candidate:
        base_value = kw.pop("base_value", 5.0)
        d = dict(
            candidate_id=cid,
            quality={},
            confidence={},
            pv=PVEstimate(B=base_value, H=0.0, C=0.0, R=0.0, confidence={},
                          evidence_count=10),
            authorized=True,
            human_authorized=True,
            lawful=True,
            rights_safe=True,
            privacy_safe=True,
            safety_safe=True,
        )
        d.update(kw)
        return Candidate(**d)

    baseline = cand("baseline", is_baseline=True, base_value=0.0)
    admissible = cand("admissible-modest", base_value=3.0)

    # Multiple prohibition triggers — each must be excluded. A high value
    # must never rescue a prohibited candidate through ANY gate path.
    prohibited_variants = [
        ("prohibited-hard-violation", dict(base_value=1000000.0,
                                           hard_violation=True)),
        ("prohibited-unlawful", dict(base_value=999999.0, lawful=False)),
        ("prohibited-rights", dict(base_value=999998.0, rights_safe=False)),
        ("prohibited-safety", dict(base_value=999997.0, safety_safe=False)),
    ]
    for cid, kwargs in prohibited_variants:
        prohibited = cand(cid, **kwargs)
        gate, reasons, _ = gate_candidate(prohibited, profile, policy)
        if gate != "PROHIBITED":
            raise AssertionError(
                f"expected PROHIBITED for {cid}, got {gate} ({reasons})"
            )
        candidates = [baseline, prohibited, admissible]
        exclusion_evidence = verify_pipeline_excludes_first(
            candidates, "baseline", profile, policy
        )
        if exclusion_evidence["violations"]:
            raise AssertionError(
                f"pipeline optimized over prohibited candidate {cid}: "
                f"{exclusion_evidence['violations']}"
            )

    evidence["proofs"]["pipeline_exclusion"] = {
        "prohibition_paths_tested": len(prohibited_variants),
        "paths": [cid for cid, _ in prohibited_variants],
        "violations": [],
        "passed": True,
    }

    # ---- Proof 3: verdict mapping -----------------------------------------
    mapping_cases = {
        "PROHIBITED": DISQUALIFIED,
        "NEEDS_AUTHORITY": DEFERRED,
        "NEEDS_EVIDENCE": DEFERRED,
        "ADMISSIBLE": ADMISSIBLE,
    }
    for calculus_verdict, expected in mapping_cases.items():
        actual = verdict_from_calculus_gate(calculus_verdict)
        if actual != expected:
            raise AssertionError(
                f"verdict mapping wrong: {calculus_verdict} -> {actual}, "
                f"expected {expected}"
            )
    # Unknown verdicts must fail closed.
    try:
        verdict_from_calculus_gate("SOMETHING_ELSE")
        raise AssertionError(
            "verdict_from_calculus_gate did not fail closed on unknown verdict"
        )
    except ValueError:
        pass  # correct: fail closed
    evidence["proofs"]["verdict_mapping"] = {
        "cases": len(mapping_cases), "fail_closed_on_unknown": True,
    }

    evidence["passed"] = True
    return evidence


def main(argv: list[str]) -> int:
    record: dict = {}
    args = list(argv)
    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "--record":
            if i + 1 < len(args):
                raw = args[i + 1]
                try:
                    record = json.loads(raw)
                except json.JSONDecodeError:
                    print(f"FAIL: input record is not valid JSON: {raw[:80]}")
                    return 1
                i += 2
            else:
                print("WARN: --record given with no following value; ignored",
                      file=sys.stderr)
                i += 1
            continue
        i += 1
    if not isinstance(record, dict):
        print("FAIL: input record must be a JSON object")
        return 1

    try:
        evidence = run_governance()
    except AssertionError as e:
        print(f"FAIL: decision principle governance violated: {e}")
        return 1
    except Exception as e:  # noqa: BLE001 — fail closed on anything unexpected
        print(f"FAIL: governance check errored (fail-closed): {type(e).__name__}: {e}")
        return 1

    proofs = evidence["proofs"]
    total_scenarios = (
        proofs["handbuilt_battery"]["scenarios"]
        + proofs["randomized_seed_7"]["scenarios"]
        + proofs["randomized_seed_20261011"]["scenarios"]
    )
    print(
        "OK: decision principle governs the pipeline — "
        f"{total_scenarios} cross-implementation scenarios agree, "
        "live pipeline excludes prohibited before optimizing, "
        "verdict mapping correct and fail-closed."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
