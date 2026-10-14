#!/usr/bin/env python3
"""validate_ratified_pins.py — NO-WORD RATIFICATION pin enforcement (2026-10-14).

Standing law (Shawn, 2026-10-14): a governance JSON claiming
`"status": "RATIFIED"` without scorecard pins (scorecard IDs + content hash
+ reviewer seats) is CLAIMED-UNVERIFIED, never ratified. Authorization comes
from the scoring matrix alone — no word can ratify.

Every `*.json` under the governance dir whose top-level "status" is
"RATIFIED" must carry ALL of the following:

  ratification.authority == "SCORING_MATRIX"
  ratification.ratified_at            (ISO date or datetime string)
  ratification.pins.scorecards        (non-empty list), each entry:
    scorecard_id            non-empty string
    reviewer_seat           non-empty string
    scored_at               non-empty string (ISO date/datetime)
    score                   number
    ratification_threshold  number
    score >= ratification_threshold
        (a below-bar scorecard can never pin a RATIFIED claim)
    reviewed_content_sha256 64 lowercase hex chars
    artifact_sha256         64 lowercase hex chars
  activation.record_content_sha256    64 lowercase hex chars, and it must
    recompute over the canonical activation record (canonical_record):
    json.dumps(record-minus-the-hash-field, sort_keys=True,
               separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    hashed with sha256.

Any other status (CANDIDATE, DRAFT, EXPIRED, REVOKED, ...) carries NO pin
requirement — pins are only enforced where a RATIFIED claim exists.

Fail-closed: a missing governance dir, an unreadable/invalid JSON file, or
any RATIFIED claim missing or failing a pin check exits non-zero.

This is NOT a duplicate of tools/ratification_gate.py (PR #2557), which
decides ratification FROM scores, nor of tools/ratified_guard.py, which
guards DELETION of ratified objects. This validator scans STORED governance
JSON for the presence and validity of ratification pins on existing claims.
"""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

GOVERNANCE_DIR_DEFAULT = ".naya/governance"
SCORE_DERIVED_AUTHORITY = "SCORING_MATRIX"
HEX64 = re.compile(r"^[0-9a-f]{64}$")
HASH_FIELD = "record_content_sha256"


def canonical_record(record):
    """Canonical bytes of an activation record for content-hash pinning.

    The hash field itself is excluded so the record can carry its own pin.
    """
    scrubbed = {k: v for k, v in record.items() if k != HASH_FIELD}
    return json.dumps(
        scrubbed, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def record_content_sha256(record):
    """sha256 of the canonical activation record (generator + verifier)."""
    return hashlib.sha256(canonical_record(record)).hexdigest()


def _failures_for_status_ratified(doc, path):
    failures = []
    rat = doc.get("ratification")
    if not isinstance(rat, dict):
        return [f"{path}: status RATIFIED but 'ratification' block missing"]
    if rat.get("authority") != SCORE_DERIVED_AUTHORITY:
        failures.append(
            f"{path}: ratification.authority must be "
            f"{SCORE_DERIVED_AUTHORITY!r}, got {rat.get('authority')!r} "
            "-- word-based authority can never ratify"
        )
    ratified_at = rat.get("ratified_at")
    if not isinstance(ratified_at, str) or not ratified_at.strip():
        failures.append(f"{path}: ratification.ratified_at missing or empty")
    pins = rat.get("pins")
    scorecards = pins.get("scorecards") if isinstance(pins, dict) else None
    if not isinstance(scorecards, list) or not scorecards:
        failures.append(
            f"{path}: ratification.pins.scorecards must be a non-empty list"
        )
    else:
        for i, sc in enumerate(scorecards):
            where = f"{path}: ratification.pins.scorecards[{i}]"
            if not isinstance(sc, dict):
                failures.append(f"{where}: not an object")
                continue
            for field in ("scorecard_id", "reviewer_seat", "scored_at"):
                v = sc.get(field)
                if not isinstance(v, str) or not v.strip():
                    failures.append(f"{where}: {field} missing or empty")
            score = sc.get("score")
            bar = sc.get("ratification_threshold")
            if isinstance(score, bool) or not isinstance(score, (int, float)):
                failures.append(f"{where}: score must be a number")
            if isinstance(bar, bool) or not isinstance(bar, (int, float)):
                failures.append(f"{where}: ratification_threshold must be a number")
            elif isinstance(score, (int, float)) and score < bar:
                failures.append(
                    f"{where}: score {score} < ratification_threshold {bar} "
                    "-- a below-bar scorecard can never pin RATIFIED"
                )
            for hfield in ("reviewed_content_sha256", "artifact_sha256"):
                hv = sc.get(hfield)
                if not isinstance(hv, str) or not HEX64.match(hv):
                    failures.append(
                        f"{where}: {hfield} must be 64 lowercase hex chars"
                    )
    act = doc.get("activation")
    if not isinstance(act, dict):
        failures.append(f"{path}: status RATIFIED but 'activation' block missing")
    else:
        pinned = act.get(HASH_FIELD)
        if not isinstance(pinned, str) or not HEX64.match(pinned):
            failures.append(f"{path}: activation.{HASH_FIELD} missing or malformed")
        elif record_content_sha256(act) != pinned:
            failures.append(
                f"{path}: activation.{HASH_FIELD} does not recompute over the "
                "canonical activation record -- record was altered after pinning"
            )
    return failures


def validate_file(path):
    """Return a list of failure strings; empty list means PASS."""
    try:
        doc = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"{path}: FAIL CLOSED -- unreadable or invalid JSON ({exc})"]
    if not isinstance(doc, dict):
        return [f"{path}: FAIL CLOSED -- top-level JSON is not an object"]
    if doc.get("status") != "RATIFIED":
        return []
    return _failures_for_status_ratified(doc, path)


def validate_dir(governance_dir):
    """Map of path -> failure list for every *.json in the governance dir."""
    gdir = Path(governance_dir)
    if not gdir.is_dir():
        return {
            "__dir__": [
                f"{gdir}: FAIL CLOSED -- governance dir missing or not a directory"
            ]
        }
    return {str(f): validate_file(f) for f in sorted(gdir.glob("*.json"))}


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Fail any status:RATIFIED governance JSON lacking "
                    "scorecard pins (NO-WORD RATIFICATION)."
    )
    ap.add_argument("--governance-dir", default=GOVERNANCE_DIR_DEFAULT)
    ap.add_argument("--json", action="store_true",
                    help="emit machine-readable JSON report")
    args = ap.parse_args(argv)
    results = validate_dir(args.governance_dir)
    failed = {k: v for k, v in results.items() if v}
    if args.json:
        print(json.dumps({
            "governance_dir": str(args.governance_dir),
            "files_checked": len(results),
            "failed": failed,
            "ok": not failed,
        }, indent=2, sort_keys=True))
    else:
        for path in sorted(results):
            errs = results[path]
            print(("FAIL " if errs else "PASS ") + path)
            for e in errs:
                print("  - " + e)
        if not results:
            print(f"NOTE: no governance JSON files under {args.governance_dir}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
