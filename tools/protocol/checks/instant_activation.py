#!/usr/bin/env python3
"""The Verification Law (Shawn, 2026-10-09).

"When Shawn says 'smart note this,' THAT IS THE VERIFICATION.
He verified it when he said it. It activates INSTANTLY — no queue,
no second verification, no 11-day wait. Same for any user's direct
capture request: the ask is the verification."

Validates a capture-request record. The hard line: treating Shawn's
verified word as unverified input — queuing a direct capture request
for verification — fails, no matter how careful the queue is.

Input record:
    {
      "request": "<the words, e.g. 'smart note this'>",
      "requester": "shawn" | "user",        # the human director / a user
      "request_type": "capture",            # a direct capture request
      "disposition": "activated",           # must be instant
      "queued_for_verification": false,
      "activated_at": "<ISO-8601 UTC>"
    }

Checks:
  1. request_type == "capture" with requester shawn/user: the ask IS the
     verification — queued_for_verification must be false.
  2. disposition must be "activated" (the only lawful instant state).
  3. activated_at present — activation happened, not promised.

Note: ratified by Shawn's own words (#1354). This check verifies the
law's compliance; it never grants authority.

Usage:
    python3 tools/protocol/checks/instant_activation.py \
        --record '{"request": "smart note this", ...}' [--json]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks import emit, fail, load_record, result  # noqa: E402

DIRECT_REQUESTERS = {"shawn", "user", "human_director"}


def check(record: dict) -> dict:
    reasons: list[str] = []
    details: dict = {"law": "VERIFICATION-LAW", "law_status": "RATIFIED"}

    if not isinstance(record, dict):
        return fail("record is not a JSON object", details)

    request = str(record.get("request") or "").strip()
    requester = str(record.get("requester") or "").strip().lower()
    request_type = str(record.get("request_type") or "").strip().lower()
    disposition = str(record.get("disposition") or "").strip().lower()
    queued = record.get("queued_for_verification", False)
    activated_at = str(record.get("activated_at") or "").strip()

    details.update({"request": request, "requester": requester,
                    "request_type": request_type})

    is_direct_capture = (
        request_type == "capture" and requester in DIRECT_REQUESTERS and bool(request)
    )
    details["is_direct_capture_request"] = is_direct_capture

    if is_direct_capture:
        if queued:
            return fail(
                "queued_for_verification is true on a direct capture request — "
                "treating Shawn's verified word as unverified input. "
                "The ask IS the verification; activate instantly, never queue.",
                details,
            )
        reasons.append("direct capture request not queued for verification")
        if disposition != "activated":
            return fail(
                f"disposition is {disposition!r}, not 'activated' — "
                "the Verification Law demands INSTANT activation, no queue, no wait",
                details,
            )
        reasons.append("disposition is 'activated'")
    else:
        # Non-direct requests fall back to the normal capture contract:
        # they must at least record a disposition.
        if not disposition:
            return fail("disposition missing — record states nothing verifiable",
                        details)
        reasons.append(f"non-direct request, disposition {disposition!r} recorded")

    if not activated_at:
        return fail("activated_at missing — activation happened, not promised",
                    details)
    reasons.append("activated_at present")

    reasons.append("Verification Law honored: the ask was the verification")
    return result(True, reasons, details)


def main() -> int:
    parser = argparse.ArgumentParser(description="Verification Law check")
    parser.add_argument("--record", required=True,
                        help="JSON capture-request record (or @file)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()
    try:
        record = load_record(args.record)
    except Exception as e:
        return emit(fail(f"unparseable record: {e}", {"law": "VERIFICATION-LAW"}),
                    args.json)
    return emit(check(record), args.json)


if __name__ == "__main__":
    sys.exit(main())
