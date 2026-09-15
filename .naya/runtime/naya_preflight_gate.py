#!/usr/bin/env python3
"""Naya Power repository preflight guard.

This validates structural prerequisites for substantive Naya work. It cannot prove
that a model actually understood a document; it only prevents missing/invalid
repository governance evidence from being treated as ready.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
REQUIRED = {
    "read_first": ROOT / "NAYA-READ-FIRST.md",
    "preflight": ROOT / ".naya" / "00-NAYA-PREFLIGHT-GOVERNANCE-EXECUTION-GATE.md",
    "lead_mode": ROOT / ".naya" / "2026-09-14-NAYAPOWER-LEAD-MODE-AND-TEN-STAR-OPERATING-PROTOCOL.md",
}


def fail(message: str) -> int:
    print(f"PREFLIGHT: BLOCKED — {message}")
    return 2


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", default=".naya/PREFLIGHT-RECEIPT.json")
    parser.add_argument("--require-receipt", action="store_true")
    args = parser.parse_args()

    for name, path in REQUIRED.items():
        if not path.is_file():
            return fail(f"missing required {name}: {path.relative_to(ROOT)}")

    activation_candidates = [
        p for p in ROOT.iterdir()
        if p.is_file() and "ACTIVATION 00" in p.name and "NAYA POWER" in p.name
    ]
    if not activation_candidates:
        return fail("Activation 00 initialization contract was not found")

    preflight_text = REQUIRED["preflight"].read_text(encoding="utf-8")
    for marker in ("NO PREFLIGHT = NO SUBSTANTIVE EXECUTION", "SOURCE-LOCK", "POST-ACTION VERIFICATION GATE"):
        if marker not in preflight_text:
            return fail(f"preflight gate is missing mandatory marker: {marker}")

    if args.require_receipt:
        receipt = ROOT / args.receipt
        if not receipt.is_file():
            return fail(f"required preflight receipt is missing: {receipt.relative_to(ROOT)}")
        try:
            data = json.loads(receipt.read_text(encoding="utf-8"))
        except Exception as exc:
            return fail(f"preflight receipt is not valid JSON: {exc}")
        required_fields = {
            "status", "mission", "scope", "source_of_truth", "authority",
            "current_state", "protected_baseline", "recommendation",
            "authorized_action", "pass_condition", "verification_plan",
        }
        missing = sorted(required_fields - set(data))
        if missing:
            return fail("preflight receipt missing fields: " + ", ".join(missing))
        if data.get("status") not in {"READY", "BLOCKED", "HUMAN_REVIEW_REQUIRED"}:
            return fail("preflight receipt status is invalid")

    print("PREFLIGHT: READY")
    print("Required governance surfaces are present and structurally valid.")
    print("Reminder: structural readiness is not proof of model comprehension or runtime success.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
