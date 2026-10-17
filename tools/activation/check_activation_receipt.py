#!/usr/bin/env python3
"""Activation receipt check — Law 4.1 (The Drink-First Law).

Law: "Before you serve me you must drink the water. Either do your job right
and send me what's right, or don't send me anything at all."
REQUIRES: Activation before service. No Naya serves anyone unactivated.

What this check does (the machinable core of the law):
  A work artifact directory must contain a valid activation receipt
  (ACTIVATION-RECEIPT*.json, schema naya.activation.receipt.v1, matching
  NAYA-ACTIVATION/ACTIVATION-RECEIPT-TEMPLATE.json). The receipt must say
  ACTIVATED — not UNACTIVATED — name who was activated, who the human
  director is, under what authority, when it happened, and carry verification
  evidence. Anything less means the ritual was not completed.

What it does NOT check (honest limit): it cannot tell whether the activation
was genuine. A seat can write a truthful-looking receipt without doing the
work. Receipt honesty is Law 5.5 (the Honesty Covenant) — judgment-only.
This check enforces that the receipt EXISTS and is COMPLETE. An absent or
incomplete receipt can never pass.

Usage:
    python3 check_activation_receipt.py --workdir <artifact-directory>

Exit code 0: a valid ACTIVATED receipt is present.
Exit code 1: missing, unparsable, UNACTIVATED, or incomplete receipt.
Exit code 2: usage error.

Stdlib only.
"""

import argparse
import glob
import json
import os
import sys

SCHEMA = "naya.activation.receipt.v1"

# Fields the template requires to be non-null for an activation to be real.
REQUIRED_FIELDS = (
    "naya_identity",
    "human_director",
    "authority",
    "repository",
    "timestamp",
)


def fail(msg):
    print(f"ACTIVATION RECEIPT CHECK FAILED — {msg}")
    print("Law 4.1 (Drink-First Law): no work ships unactivated.")
    print("Fix: complete the activation ritual, then write a truthful")
    print("ACTIVATION-RECEIPT.json (schema naya.activation.receipt.v1).")


def main(argv):
    ap = argparse.ArgumentParser(description="Law 4.1 activation receipt check")
    ap.add_argument("--workdir", required=True,
                    help="work artifact directory that must contain a receipt")
    args = ap.parse_args(argv)

    workdir = args.workdir
    if not os.path.isdir(workdir):
        print(f"USAGE ERROR: not a directory: {workdir}")
        return 2

    matches = sorted(glob.glob(os.path.join(workdir, "ACTIVATION-RECEIPT*.json")))
    if not matches:
        fail(f"no activation receipt found in {workdir}. "
             "A work artifact must carry proof that activation happened first.")
        return 1

    path = matches[0]
    try:
        with open(path, encoding="utf-8") as f:
            receipt = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        fail(f"receipt {os.path.basename(path)} is not valid JSON: {e}")
        return 1

    if not isinstance(receipt, dict):
        fail(f"receipt {os.path.basename(path)} is not a JSON object.")
        return 1

    if receipt.get("schema") != SCHEMA:
        fail(f"receipt schema is {receipt.get('schema')!r}, expected {SCHEMA!r}.")
        return 1

    status = receipt.get("status")
    if status != "ACTIVATED":
        fail(f"receipt status is {status!r} — the ritual was not completed. "
             "An UNACTIVATED receipt never authorizes work.")
        return 1

    missing = [f for f in REQUIRED_FIELDS if not receipt.get(f)]
    if missing:
        fail(f"receipt is incomplete — missing: {', '.join(missing)}. "
             "An activation receipt that doesn't name who, for whom, under "
             "what authority, and when, proves nothing.")
        return 1

    verification = receipt.get("verification") or {}
    if not isinstance(verification, dict) or not verification.get("evidence"):
        fail("receipt carries no verification evidence. "
             "An activation receipt without evidence is theater — "
             "add what was actually verified, with sources.")
        return 1

    print(f"ACTIVATION RECEIPT CHECK PASSED — {os.path.basename(path)}: "
          f"{receipt.get('naya_identity')} activated for "
          f"{receipt.get('human_director')} at {receipt.get('timestamp')}.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
