#!/usr/bin/env python3
"""
PROTOCOL PIN + DECLARATION RECEIPT — the ratified protocol, byte-pinned.

PROTOCOL.md is the canonical operating law (ratified by Shawn Vibert,
2026-10-20, with the Declaration & Value Loop amendment). Until now
nothing machine-verified the protocol's own bytes: the boot gate pinned
the 14 thinking lessons and Operating Code V2, while the protocol itself
could drift silently — and did (the manifest claimed a 2026-10-08
ratification for ten days after the document had already changed).

This module is the pin source, mirroring the pin pattern in
tools/activation_checklist.py (content-addressed trust roots; a drift
is a deliberate re-pin via code change, never a silent pass):

  1. PROTOCOL PIN — sha256 of PROTOCOL.md and of its Step 0 declaration
     section specifically (the declaration is the load-bearing text:
     Step 0 is spoken as written, so its bytes are pinned separately —
     a re-pin of the whole document that quietly edits the declaration
     still trips the Step 0 pin).
  2. DECLARATION RECEIPT — Step 0 made provable. Activation writes a
     receipt {agent_id, declared_at, protocol_sha256, step0_sha256,
     protocol_version} computed from live canonical bytes. Verification
     recomputes the fingerprints from the repo and rejects forged,
     stale, or agent-less receipts. The activation checklist fails
     without a valid receipt when run with --require-declaration.

Honest boundary: the receipt proves the declaration was issued against
the current pinned protocol bytes at a stated time by a named agent.
It cannot prove the agent internalized the declaration — that is
behavioral, and the protocol's own scorecard loop is where behavior is
judged. What the machine can do — refuse to boot on drifted law, and
refuse activation without the declaration step — it now does.

Usage:
    python3 tools/protocol_pin.py --check [--json]
    python3 tools/protocol_pin.py --issue --agent-id <id> [--out PATH]
    python3 tools/protocol_pin.py --verify <receipt.json> \
        [--max-age-hours N] [--json]

Exit codes: 0 = ok | 1 = pin mismatch / receipt violations |
            2 = tool error (canonical bytes unreadable — fail closed).
"""

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# Canonical location + pins (content-addressed trust roots)
# ---------------------------------------------------------------------------

PROTOCOL_MD = "PROTOCOL.md"

PIN_SOURCE = (
    "origin/main @ d986404acac7b3e1be6a4eb253bbc5f34460729f "
    "(PROTOCOL.md ratified 2026-10-20; pinned at operationalization, "
    "2026-10-20). A drift in protocol bytes is a deliberate re-pin "
    "(code change), never a silent pass.")
PROTOCOL_FILE_PIN = \
    "cb7bc9e78b3ac86b939c475f79ae00d0f390fc0a70727b9717a08524190be84c"
STEP0_PIN = \
    "588cac59b390cccae7443cc406f5b0f37b61bec81d74fcd1d635ea3fb66f40da"

STEP0_START = "**0. DECLARE"
STEP0_END = "**1. WAKE"
RATIFIED_RE = re.compile(
    r"Ratified and amended by Shawn Vibert, (\d{4}-\d{2}-\d{2})")
SHA64_RE = re.compile(r"^[a-fA-F0-9]{64}$")

RECEIPT_SCHEMA = "naya.declaration-receipt.v1"


def _sha256_hex(data):
    return hashlib.sha256(bytes(data)).hexdigest()


def extract_step0(text):
    """The Step 0 declaration section: from its header line to Step 1's.

    Deterministic slice of the canonical text — the declaration is
    spoken as written, so these exact bytes are what a Naya declares.
    Raises ValueError when the markers are absent (structure drift is
    a pin failure, never a silent empty section)."""
    try:
        start = text.index(STEP0_START)
        end = text.index(STEP0_END)
    except ValueError:
        raise ValueError(
            "Step 0 declaration markers not found in PROTOCOL.md "
            "(%r .. %r) — document structure drifted" % (STEP0_START, STEP0_END))
    if end <= start:
        raise ValueError("Step 0 section is empty or out of order")
    return text[start:end]


def protocol_fingerprints(repo_root):
    """Recompute the protocol fingerprints from live bytes.

    Returns {"sha256", "step0_sha256", "version", "bytes"}.
    Raises OSError/ValueError when the canonical bytes are unreadable
    or structurally drifted — callers fail closed."""
    path = os.path.join(str(repo_root), PROTOCOL_MD)
    with open(path, "rb") as f:
        blob = f.read()
    text = blob.decode("utf-8")
    m = RATIFIED_RE.search(text)
    if not m:
        raise ValueError("ratification line not found in PROTOCOL.md")
    return {
        "sha256": _sha256_hex(blob),
        "step0_sha256": _sha256_hex(extract_step0(text).encode("utf-8")),
        "version": m.group(1),
        "bytes": len(blob),
    }


def check_protocol_pin(repo_root):
    """Boot-gate predicate: (passed, detail). Never raises."""
    try:
        fp = protocol_fingerprints(repo_root)
    except Exception as e:
        return False, ("protocol unreadable or structurally drifted "
                       "(%s) — boot refused (fail closed)" % e)
    if fp["sha256"].lower() != PROTOCOL_FILE_PIN.lower():
        return False, (
            "PROTOCOL.md bytes differ from the pinned fingerprint "
            "(pin source: %s) — re-pin deliberately or restore canonical "
            "bytes — boot refused (fail closed)" % PIN_SOURCE)
    if fp["step0_sha256"].lower() != STEP0_PIN.lower():
        return False, (
            "Step 0 declaration text differs from its pinned fingerprint "
            "(pin source: %s) — the declaration is spoken as written; "
            "its drift is never silent — boot refused (fail closed)"
            % PIN_SOURCE)
    return True, ("protocol pinned: PROTOCOL.md + Step 0 declaration "
                  "match canonical bytes (ratified %s)" % fp["version"])


# ---------------------------------------------------------------------------
# Declaration receipt — Step 0, made provable
# ---------------------------------------------------------------------------

def issue_declaration_receipt(repo_root, agent_id):
    """Write the activation receipt: Step 0 declared against the
    current pinned protocol, by a named agent, at a stated time.
    Raises ValueError on an empty agent id or unreadable protocol."""
    if not isinstance(agent_id, str) or not agent_id.strip():
        raise ValueError("agent_id is required — an anonymous declaration "
                         "is not a declaration")
    fp = protocol_fingerprints(repo_root)
    return {
        "schema": RECEIPT_SCHEMA,
        "agent_id": agent_id.strip(),
        "declared_at": datetime.now(timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ"),
        "protocol_sha256": fp["sha256"],
        "step0_sha256": fp["step0_sha256"],
        "protocol_version": fp["version"],
    }


def check_declaration_receipt(repo_root, receipt, max_age_hours=None):
    """Verify an untrusted declaration receipt against live bytes.
    Returns a list of violations ([] = valid)."""
    v = []
    if not isinstance(receipt, dict):
        return ["DECLARATION_MALFORMED: receipt is not an object"]
    if receipt.get("schema") != RECEIPT_SCHEMA:
        v.append("DECLARATION_MALFORMED: schema is %r, expected %r"
                 % (receipt.get("schema"), RECEIPT_SCHEMA))
    agent = receipt.get("agent_id")
    if not isinstance(agent, str) or not agent.strip():
        v.append("DECLARATION_AGENT_MISSING: receipt names no agent — "
                 "Step 0 is declared by someone, or it did not happen")
    try:
        fp = protocol_fingerprints(repo_root)
    except Exception as e:
        return v + ["DECLARATION_UNVERIFIABLE: canonical protocol "
                    "unreadable (%s) — fail closed" % e]
    got = receipt.get("protocol_sha256", "")
    if not isinstance(got, str) or not SHA64_RE.match(got):
        v.append("DECLARATION_MALFORMED: protocol_sha256 is not 64-hex")
    elif got.lower() != fp["sha256"].lower():
        v.append("DECLARATION_PROTOCOL_MISMATCH: receipt was issued "
                 "against different protocol bytes than the current "
                 "canonical PROTOCOL.md (stale or forged declaration)")
    got0 = receipt.get("step0_sha256", "")
    if not isinstance(got0, str) or not SHA64_RE.match(got0):
        v.append("DECLARATION_MALFORMED: step0_sha256 is not 64-hex")
    elif got0.lower() != fp["step0_sha256"].lower():
        v.append("DECLARATION_STEP0_MISMATCH: receipt's Step 0 "
                 "fingerprint does not match the current declaration "
                 "text")
    if receipt.get("protocol_version") != fp["version"]:
        v.append("DECLARATION_VERSION_MISMATCH: receipt protocol "
                 "version %r != canonical %r"
                 % (receipt.get("protocol_version"), fp["version"]))
    stamp = receipt.get("declared_at")
    when = None
    if isinstance(stamp, str):
        try:
            when = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
        except ValueError:
            when = None
    if when is None:
        v.append("DECLARATION_MALFORMED: declared_at %r is not an "
                 "ISO-8601 timestamp" % (stamp,))
    elif max_age_hours is not None:
        age_h = (datetime.now(timezone.utc) - when).total_seconds() / 3600.0
        if age_h > max_age_hours:
            v.append("DECLARATION_STALE: declared %.1fh ago, limit is "
                     "%sh — re-declare for this shift" % (age_h, max_age_hours))
        elif age_h < -0.25:
            v.append("DECLARATION_MALFORMED: declared_at is in the "
                     "future — a receipt from the future proves nothing")
    return v


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _default_repo_root():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(here)  # tools/ -> repo root


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Protocol pin + Step 0 declaration receipt: the "
                    "ratified protocol, byte-pinned and provable.")
    ap.add_argument("--repo-root", default=_default_repo_root())
    ap.add_argument("--check", action="store_true",
                    help="verify PROTOCOL.md + Step 0 against the pins")
    ap.add_argument("--issue", action="store_true",
                    help="issue a declaration receipt")
    ap.add_argument("--agent-id", default="",
                    help="agent id for --issue")
    ap.add_argument("--out", default="",
                    help="write the issued receipt here (default: stdout)")
    ap.add_argument("--verify", default="",
                    help="declaration receipt JSON file to verify")
    ap.add_argument("--max-age-hours", type=float, default=None,
                    help="with --verify: reject receipts older than this")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    if args.issue:
        try:
            receipt = issue_declaration_receipt(args.repo_root, args.agent_id)
        except Exception as e:
            print("TOOL-ERROR: %s" % e, file=sys.stderr)
            return 2
        payload = json.dumps(receipt, indent=2, sort_keys=True)
        if args.out:
            with open(args.out, "w", encoding="utf-8") as f:
                f.write(payload + "\n")
            print("declaration receipt written: %s" % args.out)
        else:
            print(payload)
        return 0

    if args.verify:
        try:
            with open(args.verify, encoding="utf-8") as f:
                receipt = json.load(f)
        except (OSError, ValueError) as e:
            print("TOOL-ERROR: cannot read receipt: %s" % e, file=sys.stderr)
            return 2
        violations = check_declaration_receipt(
            args.repo_root, receipt, args.max_age_hours)
        if args.json:
            print(json.dumps({"valid": not violations,
                              "violations": violations,
                              "receipt": receipt}, indent=2))
        else:
            print("DECLARATION-%s: %s" % (
                "VALID" if not violations else "REJECT",
                "; ".join(violations) if violations else "ok"))
        return 0 if not violations else 1

    # default: the pin check
    passed, detail = check_protocol_pin(args.repo_root)
    if args.json:
        print(json.dumps({"pass": passed, "detail": detail,
                          "pin_source": PIN_SOURCE}, indent=2))
    else:
        print("%s: %s" % ("PIN-VERIFIED" if passed else "PIN-REJECT", detail))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
