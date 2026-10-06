#!/usr/bin/env python3
"""Issue an elevation grant authorizing VERIFIED->RATIFIED for one note.

Shawn (Human Director) runs this to create a bounded capability grant.
The grant is written as JSON to BRAIN/01-GOVERNANCE/elevation-grants/
and printed for confirmation. Grants land via normal PR review.

Usage:
    python3 tools/issue_elevation_grant.py --note-id SN-0471 \
        --expires-days 7 --scope-note "Ratify per director directive"

    python3 tools/issue_elevation_grant.py --note-id SN-0472 \
        --issuer "Naya 4" --issuer-role Delegate --delegated-by "Shawn Vibert" \
        --expires-days 3 --scope-note "Delegated ratification"
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GRANTS_DIR = ROOT / "BRAIN" / "01-GOVERNANCE" / "elevation-grants"


def load_guard():
    spec = importlib.util.spec_from_file_location(
        "truth_state_guard", ROOT / "tools" / "truth_state_guard.py")
    g = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(g)
    return g


def main():
    ap = argparse.ArgumentParser(description="Issue a VERIFIED->RATIFIED elevation grant.")
    ap.add_argument("--note-id", required=True, help="Smart Note ID, e.g. SN-0471")
    ap.add_argument("--target-state", default="RATIFIED",
                    help="Target truth state (default: RATIFIED)")
    ap.add_argument("--issuer", default="Shawn Vibert",
                    help="Grant issuer (default: Shawn Vibert)")
    ap.add_argument("--issuer-role", default="Human Director",
                    choices=["Human Director", "Delegate"],
                    help="Issuer role (default: Human Director)")
    ap.add_argument("--delegated-by", default=None,
                    help="For Delegate role: who delegated (must name the Director)")
    ap.add_argument("--expires-days", type=int, default=7,
                    help="Grant validity in days (default: 7)")
    ap.add_argument("--scope-note", default="",
                    help="Why this elevation is authorized")
    ap.add_argument("--grants-dir", default=str(GRANTS_DIR),
                    help="Directory to write the grant JSON")
    ap.add_argument("--dry-run", action="store_true",
                    help="Print the grant without writing")
    args = ap.parse_args()

    if args.issuer_role == "Delegate" and not args.delegated_by:
        ap.error("--issuer-role Delegate requires --delegated-by naming the Director")
    if args.expires_days < 1:
        ap.error("--expires-days must be >= 1")

    g = load_guard()
    grant = g.make_grant(
        note_id=args.note_id,
        target_state=args.target_state,
        issuer=args.issuer,
        issuer_role=args.issuer_role,
        expires_days=args.expires_days,
        scope_note=args.scope_note,
        delegated_by=args.delegated_by,
    )

    # Self-verify before writing.
    ok, rec = g.validate_grant(grant, args.note_id, args.target_state)
    if not ok:
        print(f"SELF-CHECK FAILED: {rec['reason_code']}: {rec['detail']}", file=sys.stderr)
        sys.exit(1)

    if args.dry_run:
        print(json.dumps(grant, indent=2))
        return

    out_dir = Path(args.grants_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{grant['grant_id']}.json"
    if out_path.exists():
        print(f"REFUSED: {out_path} already exists — grants are immutable", file=sys.stderr)
        sys.exit(1)
    out_path.write_text(json.dumps(grant, indent=2) + "\n", encoding="utf-8")

    print(f"Grant issued: {grant['grant_id']}")
    print(f"  note:    {grant['note_id']} -> {grant['target_state']}")
    print(f"  issuer:  {grant['issuer']} ({grant['issuer_role']})")
    print(f"  valid:   {grant['issued_at']} to {grant['expires_at']}")
    print(f"  file:    {out_path}")
    print(f"  hash:    {grant['grant_hash'][:16]}...")


if __name__ == "__main__":
    main()
