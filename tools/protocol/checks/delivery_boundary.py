#!/usr/bin/env python3
"""SN-0733 — Enforcement lives at the delivery boundary (Shawn ratified 2026-10-09).

A gate mechanism is ENFORCED only when it is wired into a real delivery
path — the path code actually travels to reach Shawn: a required check on
pull requests, or a workflow that runs on push to main. A mechanism that
exists on a branch, in a document, or in a draft workflow that never runs
on the delivery path is a CANDIDATE, never ENFORCED.

This is the machine form of the lesson from the activation-gate arc:
three deep verifiers on main, zero of them invoked by any main delivery
path — the ADOPTION GAP. The gate existed; enforcement did not.

Validates a mechanism record. The hard line: claiming "enforced" for a
mechanism with no delivery binding fails — the binding is the enforcement.

Input record:
    {
      "mechanism": "tools/activation_gate.py",
      "claimed_status": "enforced" | "candidate",
      "delivery_binding": {
        "workflow_file": ".github/workflows/x.yml",
        "triggers_on": ["pull_request_required", "push_to_main"],
        "invokes_gate": true,
        "binding_verified_at": "<ISO-8601 UTC>"
      }
    }

Checks:
  1. claimed_status == "enforced" requires a complete delivery_binding:
     workflow_file non-empty; triggers_on includes a real delivery path
     ("pull_request_required" or "push_to_main"); invokes_gate true;
     binding_verified_at present (the binding was observed, not assumed).
  2. A branch-scoped or binding-less "enforced" claim fails closed.
  3. claimed_status == "candidate" passes structurally (honest state).

Note: SN-0733 is the mechanism-side law; predicate_vs_perimeter.py is
the claim-side law (a predicate passing is not a perimeter holding).
Both must pass for a mechanism to be honestly called enforced.

Usage:
    python3 tools/protocol/checks/delivery_boundary.py \
        --record '{"mechanism": "...", ...}' [--json]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks import emit, fail, load_record, result  # noqa: E402

DELIVERY_PATHS = {"pull_request_required", "push_to_main"}


def check(record: dict) -> dict:
    reasons: list[str] = []
    details: dict = {"law": "SN-0733", "law_status": "RATIFIED"}

    if not isinstance(record, dict):
        return fail("record is not a JSON object", details)

    mechanism = str(record.get("mechanism") or "(unnamed)").strip()
    claimed = str(record.get("claimed_status") or "").strip().lower()
    binding = record.get("delivery_binding")

    details["mechanism"] = mechanism
    details["claimed_status"] = claimed

    if claimed not in {"enforced", "candidate"}:
        return fail(
            f"{mechanism}: claimed_status {claimed!r} — honest states are "
            "'enforced' or 'candidate'; nothing else may be claimed",
            details,
        )
    reasons.append(f"claimed '{claimed}' (an honest state)")

    if claimed == "candidate":
        reasons.append(
            f"{mechanism}: CANDIDATE is an honest state — the gate exists, "
            "enforcement is not yet wired; this is the ADOPTION GAP made visible"
        )
        return result(True, reasons, details)

    # claimed == "enforced": the binding IS the enforcement.
    if not isinstance(binding, dict):
        return fail(
            f"{mechanism}: claimed 'enforced' with no delivery_binding — "
            "a mechanism that exists but is never invoked on the delivery path "
            "is a CANDIDATE, never ENFORCED. Enforcement lives at the delivery boundary.",
            details,
        )

    wf = str(binding.get("workflow_file") or "").strip()
    triggers = binding.get("triggers_on") or []
    invokes = binding.get("invokes_gate", False)
    verified_at = str(binding.get("binding_verified_at") or "").strip()

    if not wf:
        return fail(
            f"{mechanism}: 'enforced' claim without a workflow_file — name the "
            "delivery-path workflow or retract the claim",
            details,
        )
    if not isinstance(triggers, list) or not (set(triggers) & DELIVERY_PATHS):
        return fail(
            f"{mechanism}: workflow {wf} triggers on {triggers!r} — not a real "
            "delivery path. Enforcement requires 'pull_request_required' and/or "
            "'push_to_main'. A branch-only workflow is the ADOPTION GAP.",
            details,
        )
    if invokes is not True:
        return fail(
            f"{mechanism}: workflow {wf} does not invoke the gate — presence "
            "on the path without invocation is decoration, not enforcement",
            details,
        )
    if not verified_at:
        return fail(
            f"{mechanism}: binding_verified_at missing — the binding must be "
            "OBSERVED (a real run), not assumed from file presence",
            details,
        )

    reasons.append(f"bound to {wf} on {sorted(set(triggers) & DELIVERY_PATHS)}")
    reasons.append(f"gate invoked; binding observed at {verified_at}")
    details["delivery_binding"] = {
        "workflow_file": wf,
        "triggers_on": sorted(set(triggers) & DELIVERY_PATHS),
        "invokes_gate": True,
        "binding_verified_at": verified_at,
    }
    reasons.append(f"{mechanism}: ENFORCED — enforcement lives at the delivery boundary")
    return result(True, reasons, details)


def main() -> int:
    parser = argparse.ArgumentParser(description="SN-0733 delivery-boundary check")
    parser.add_argument("--record", required=True,
                        help="JSON mechanism record (or @file)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()
    try:
        record = load_record(args.record)
    except Exception as e:
        return emit(fail(f"unparseable record: {e}", {"law": "SN-0733"}), args.json)
    return emit(check(record), args.json)


if __name__ == "__main__":
    sys.exit(main())
