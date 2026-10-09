#!/usr/bin/env python3
"""Pre-delivery gate — the one enforceable path.

Runs the full delivery boundary in order:
  1. DRINK-FIRST (Naya 4): activation receipt valid, fresh, correct repo.
     If this fails, we STOP — no design check, no delivery.
  2. DESIGN GATE (Naya 5): structural design laws enforced.
     If this fails, we STOP — no delivery.

Both pass → CLEARED FOR DELIVERY.

This is the composition Naya 1's integration directive calls for:
"the system should refuse work that fails required checks, not simply
remind an agent to follow the rules."

Usage:
    python3 tools/pre_delivery_gate.py <page.html> --receipt <receipt.json> \
        --live-tip <sha> [--manifest <manifest.json>] [--expected-repo <slug>]

Exit codes: 0 = cleared for delivery, 1 = blocked (named stage), 2 = tool error.

The gate never touches the network — the caller resolves --live-tip from
the refs API. All verdicts are deterministic.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DRINK_FIRST = REPO_ROOT / "NAYA-ACTIVATION" / "tools" / "drink_first_gate.py"
DESIGN_GATE = REPO_ROOT / "tools" / "design_gate.py"


def run(cmd: list[str]) -> tuple[int, str]:
    """Run a gate, return (exit_code, combined output)."""
    try:
        p = subprocess.run(
            cmd, capture_output=True, text=True, timeout=120,
        )
    except FileNotFoundError as e:
        return 2, f"TOOL ERROR: gate script not found: {e}"
    except subprocess.TimeoutExpired:
        return 2, "TOOL ERROR: gate timed out after 120s"
    out = (p.stdout or "") + (p.stderr or "")
    return p.returncode, out.strip()


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(
        description="Pre-delivery gate: activation THEN design, fail closed.")
    ap.add_argument("page", help="work product HTML path")
    ap.add_argument("--receipt", required=True,
                    help="activation receipt JSON path")
    ap.add_argument("--live-tip", required=True,
                    help="live main tip SHA (caller resolves via refs API)")
    ap.add_argument("--manifest", default=None,
                    help="smart-blocks manifest for the design gate")
    ap.add_argument("--expected-repo", default="SoulSchoolAcademy/NayaPOWER",
                    help="repository the receipt must be bound to")
    ap.add_argument("--max-age-hours", type=float, default=4)
    args = ap.parse_args(argv)

    page = Path(args.page)
    receipt = Path(args.receipt)
    if not page.exists():
        print(f"TOOL ERROR: page not found: {page}")
        return 2
    if not receipt.exists():
        print(f"TOOL ERROR: receipt not found: {receipt}")
        return 2

    # ---- Stage 1: DRINK-FIRST (activation) ----
    if not DRINK_FIRST.exists():
        print(f"TOOL ERROR: drink-first gate missing: {DRINK_FIRST}")
        print("  (Naya 4's PR #1979 not yet merged — activation cannot be enforced)")
        return 2
    code, out = run([
        sys.executable, str(DRINK_FIRST),
        "--receipt", str(receipt),
        "--live-tip", args.live_tip,
        "--max-age-hours", str(args.max_age_hours),
        "--product", str(page),
        "--require-citation",
    ])
    if code != 0:
        print("BLOCKED AT STAGE 1 — DRINK-FIRST (activation)")
        print(out)
        print()
        print("No Naya serves unactivated. Fix the receipt, then re-run.")
        return 1
    print("STAGE 1 PASS — drink-first: activation valid, fresh, cited.")

    # ---- Stage 2: DESIGN GATE (structural laws) ----
    if not DESIGN_GATE.exists():
        print(f"TOOL ERROR: design gate missing: {DESIGN_GATE}")
        print("  (Naya 5's ship-design-gate not yet merged — design cannot be enforced)")
        return 2
    dcmd = [
        sys.executable, str(DESIGN_GATE), str(page),
        "--require-activation", f"--receipt={receipt}",
        f"--expected-repo={args.expected_repo}",
    ]
    if args.manifest:
        dcmd += ["--manifest", args.manifest]
    code, out = run(dcmd)
    if code != 0:
        print("BLOCKED AT STAGE 2 — DESIGN GATE (structural laws)")
        print(out)
        print()
        print("Fix the violations, then re-run from Stage 1.")
        return 1
    print("STAGE 2 PASS — design gate: structural laws hold.")

    print()
    print("CLEARED FOR DELIVERY — activation + design verified.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
