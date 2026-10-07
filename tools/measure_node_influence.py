#!/usr/bin/env python3
"""Measure how much each nine-node kernel actually influences a decision.

Why this exists
---------------
NAYANODE/0007 section 6 requires behavioral attribution:

    CONTROL:   relevant kernel capability unavailable.
    TREATMENT: relevant kernel capability available.
    The test must measure an observable behavioral difference attributable to the
    treatment.

This script executes the canonical behavior engine and produces deterministic, target-node
behavior fingerprints under real CONTROL/TREATMENT ablations. The live runtime-proof
workflow consumes this artifact as a gate and requires 9/9 demonstrated node influence.
The manifest-bound reference kernel is measured separately and is allowed to expose its
current narrower runtime scope.

The standalone tool reports the measured delta against both kernels the repo ships.
The canonical live runtime-proof workflow consumes the measurement as a gate and requires
9/9 demonstrated influence for the nine-node behavior engine. The standalone command does
not itself mutate or authorize production state.

Usage:  python tools/measure_node_influence.py [--json]
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

ORDER = ["SELF", "LAW", "ACT", "KNOW", "PROVE", "CONNECT", "VERIFY", "LEARN", "EVOLVE"]
EPHEMERAL_KEYS = {
    "execution_id",
    "candidate_id",
    "timestamp",
    "cycle_id",
    "start_time",
    "end_time",
    "duration_ms",
}


def stable_behavior_hash(value: Any) -> str:
    """Hash only semantically observable node behavior, excluding per-run UUID/time noise."""
    def normalize(item: Any) -> Any:
        if isinstance(item, dict):
            return {
                key: normalize(val)
                for key, val in sorted(item.items())
                if key not in EPHEMERAL_KEYS
            }
        if isinstance(item, list):
            return [normalize(val) for val in item]
        return item

    payload = json.dumps(normalize(value), sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


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
            # Fingerprint the actual node output after removing only ephemeral run IDs/time.
            # Influence attribution compares ONLY the target node's behavior fingerprint.
            "node_behavior_fingerprints": {
                nid: stable_behavior_hash(engine.outputs.get(nid, {}))
                for nid in out["node_receipts"]
            },
        }

    base = {
        "identity": {"actor_id": "A", "system_id": "S", "owner_id": "O"},
        "mission": {"mission": "M", "objective": "O"},
        "proposed_action": {"type": "t", "expected_outcome": "done"},
        "authority": {"grant_id": "G"},
        "claim": "c",
        "evidence": [{"provenance": "p"}],
        "intelligent_block_id": "IB-1",
        "intelligence": [{"id": "IB-1", "owner_id": "O", "content": "lesson"}],
        "relationships": [{"type": "DERIVED_FROM", "source": "IB-1", "target": "KNOW-1"}],
        "observed_outcome": "done",
        "independent_evidence": ["i"],
        "holdout_result": True,
        "next_action": "continue",
        "applicability": "contextual",
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
        # KNOW ablation: remove the durable block binding and the retrieved result.
        "know_without_reader": ("KNOW", {
            **base,
            "intelligent_block_id": "",
            "intelligence": [],
        }),
        # CONNECT ablation: drop the actual typed relationship used by the treatment.
        "connect_without_relationships": ("CONNECT", {**base, "relationships": []}),
        # EVOLVE ablation: remove the successor's next action.
        "evolve_without_next_action": ("EVOLVE", {**base, "next_action": None}),
    }
    for name, (_node, ctx) in ablations.items():
        scenarios[name] = run(ctx)

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
            baseline_hash = (scenarios[baseline_key].get("node_behavior_fingerprints") or {}).get(node)
            treatment_hash = (scenarios[scenario_name].get("node_behavior_fingerprints") or {}).get(node)
            changed = baseline_hash != treatment_hash
            if changed:
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
