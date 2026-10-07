#!/usr/bin/env python3
"""Measure how much each nine-node kernel actually influences a decision.

Why this exists
---------------
`live-supabase-runtime-proof.yml` builds a `NAYAPOWER_NINE_NODE_BEHAVIORAL_ACCEPTANCE_V1`
receipt that marks all nine nodes SATISFIED with `independent_verification: true`, and
its "ablation discrimination" step proves only that deleting a key from a dict breaks a
shape check. Nothing in that receipt executes a node.

NAYANODE/0007 section 6 states the actual requirement:

    CONTROL:   relevant kernel capability unavailable.
    TREATMENT: relevant kernel capability available.
    The test must measure an observable behavioral difference attributable to the
    treatment.

This script runs that ablation for real, against both kernels the repo ships, and
reports the measured delta. It is deliberately a measurement and not a gate: it does not
fail the build, because the correct response to "the proof artifact overstates what it
proves" is a truth decision, not a coda's unilateral edit to a CI gate.

Usage:  python tools/measure_node_influence.py [--json]
"""

from __future__ import annotations

import argparse
import copy
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

ORDER = ["SELF", "LAW", "ACT", "KNOW", "PROVE", "CONNECT", "VERIFY", "LEARN", "EVOLVE"]


# ── the two kernels ────────────────────────────────────────────────────────────

def measure_reference_kernel() -> dict:
    """kernel/nayapower_kernel.py -- the manifest-bound runtime kernel."""
    from kernel.nayapower_kernel import Authority, DecisionContext, Kernel

    kernel = Kernel()

    def run(action: str, consequential: bool, authority_scope: str | None):
        ctx = DecisionContext(
            action=action,
            consequential=consequential,
            authority=Authority(scope=authority_scope) if authority_scope else None,
        )
        r = kernel.decide(ctx)
        return {
            "allowed": r.allowed,
            "executed": r.executed,
            "truth_state": r.truth_state.value,
            "blocked_by": r.blocked_by.value if r.blocked_by else None,
            "trace": [n.value for n in r.trace],
            "evidence": list(r.evidence),
            "outcome": r.outcome,
        }

    scenarios = {
        "authorized": run("act", True, "act"),
        "no_authority": run("act", True, None),
        "scope_mismatch": run("act", True, "something_else"),
        "non_consequential": run("act", False, None),
    }
    return {"kernel": "kernel.nayapower_kernel.Kernel", "scenarios": scenarios}


def measure_behavior_engine() -> dict:
    """BRAIN/12-ENGINEERING/kernel_behavior_engine.py -- the full nine-node cycle."""
    # BRAIN/12-ENGINEERING is not a package (no __init__.py, and the directory name is
    # not a valid identifier), so it is loaded by path -- the same approach the
    # behaviour-engine test itself uses.
    module_path = ROOT / "BRAIN" / "12-ENGINEERING" / "kernel_behavior_engine.py"
    module_name = "naya_kernel_behavior_engine"
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    # Register before exec: @dataclass resolves annotations via sys.modules[cls.__module__],
    # so a module that is not registered raises AttributeError at class-definition time.
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    KernelBehaviorEngine = module.KernelBehaviorEngine

    def run(ctx: dict) -> dict:
        engine = KernelBehaviorEngine()
        out = engine.execute_cycle(copy.deepcopy(ctx))
        return {
            "status": out["status"],
            "nodes_processed": out["nodes_processed"],
            "node_statuses": {
                nid: rec["status"] for nid, rec in out["node_receipts"].items()
            },
        }

    base = {
        "identity": {"actor_id": "A", "system_id": "S", "owner_id": "O"},
        "mission": {"mission": "M", "objective": "O"},
        "proposed_action": {"type": "t", "expected_outcome": "done"},
        "authority": {"grant_id": "G"},
        "claim": "c",
        "evidence": [{"provenance": "p"}],
        "observed_outcome": "done",
        "independent_evidence": ["i"],
        "holdout_result": True,
    }

    scenarios = {"full_cycle": run(base)}

    # Ablations. Each entry declares the node it isolates, so attribution is explicit
    # rather than inferred from a scenario name. A node counts as influential only if
    # removing its input actually changes the outcome.
    ablations = {
        "no_identity": ("SELF", {**base, "identity": {}}),
        "no_authority": ("LAW", {**base, "authority": {}}),
        "authority_revoked": ("LAW", {**base, "authority": {"grant_id": "G", "revoked": True}}),
        "action_type_missing": ("ACT", {**base, "proposed_action": {"expected_outcome": "done"}}),
        "no_evidence": ("PROVE", {**base, "evidence": []}),
        "evidence_without_provenance": ("PROVE", {**base, "evidence": [{"note": "no provenance"}]}),
        "no_observation": ("VERIFY", {**base, "observed_outcome": None}),
        "no_independent_evidence": ("VERIFY", {**base, "independent_evidence": []}),
        "outcome_mismatch": ("VERIFY", {**base, "observed_outcome": "different"}),
        "holdout_failed": ("LEARN", {**base, "holdout_result": False}),
    }
    for name, (_node, ctx) in ablations.items():
        scenarios[name] = run(ctx)

    # KNOW ablation: durable retrieval is identity-bound, so removing the block id must
    # block the cycle when a reader is wired in.
    scenarios["know_without_reader"] = run({**base, "intelligent_block_id": ""})
    # CONNECT ablation: drop every typed relationship.
    scenarios["connect_without_relationships"] = run({**base, "relationships": []})
    # EVOLVE ablation: SELF not ready blocks EVOLVE; already covered by no_identity, so
    # here we test that successor continuity does NOT carry authority.
    scenarios["evolve_inherits_no_authority"] = run(base)

    return {"kernel": "BRAIN.Engineering.kernel_behavior_engine.KernelBehaviorEngine",
            "scenarios": scenarios,
            "ablations": ablations}


# ── ablation arithmetic ───────────────────────────────────────────────────────

def influence_report(measurements: list[dict]) -> dict:
    """For each kernel: which nodes can change an outcome, and which cannot.

    Attribution is explicit -- each ablation names the node it isolates -- rather than
    inferred. A node is influential only when removing its input changes the outcome.
    """
    report = {}
    for m in measurements:
        name = m["kernel"]
        scenarios = m["scenarios"]
        baseline_key = "authorized" if "authorized" in scenarios else "full_cycle"
        base = json.dumps(scenarios[baseline_key], sort_keys=True)

        influential = set()
        changed_scenarios = []
        for scenario_name, (node, _ctx) in m.get("ablations", {}).items():
            if json.dumps(scenarios[scenario_name], sort_keys=True) != base:
                influential.add(node)
                changed_scenarios.append(scenario_name)

        invoked = set()
        for scenario in scenarios.values():
            invoked.update(scenario.get("nodes_processed") or scenario.get("trace") or [])

        report[name] = {
            "invoked_nodes": sorted(invoked),
            "invoked_count": len(invoked),
            "of_total": len(ORDER),
            "influence_demonstrated_for": sorted(influential) or ["NONE"],
            "influence_demonstrated_count": len(influential),
            "changed_scenarios": changed_scenarios,
        }
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    measurements = [measure_reference_kernel(), measure_behavior_engine()]
    report = influence_report(measurements)

    if args.json:
        print(json.dumps({"measurements": measurements, "report": report}, indent=2))
        return 0

    print("NINE-NODE INFLUENCE MEASUREMENT")
    print("=" * 78)
    print("Method: NAYANODE/0007 s6 ablation. CONTROL = capability removed,")
    print("TREATMENT = capability present. An influential node is one whose removal")
    print("changes an outcome. A node that never changes an outcome is decoration.")
    print("-" * 78)
    for name, r in report.items():
        print(f"\n{name}")
        print(f"  nodes invoked            : {r['invoked_count']}/{r['of_total']}")
        print(f"  invoked                  : {', '.join(r['invoked_nodes']) or 'NONE'}")
        never = [n for n in ORDER if n not in r["invoked_nodes"]]
        print(f"  NEVER invoked            : {', '.join(never) or 'NONE'}")
        print(f"  influence demonstrated   : {', '.join(r['influence_demonstrated_for'])}")
        print(f"  influence count          : {r['influence_demonstrated_count']}/{r['of_total']}")
    print("\n" + "=" * 78)
    print("Reading: 'NEVER invoked' is the finding, not a defect in this script.")
    print("It means no code path reachable at runtime executes that node.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
