#!/usr/bin/env python3
"""EVOLVE proposal-lifecycle ledger — governed, auditable evolution state.

The EVOLVE node contract (BRAIN/03-KERNEL/NODES/EVOLVE/0001-CONTRACT.md) lists
"Evolution state (what changed, what was rejected)" as a node OUTPUT and
"Evolution state is auditable" as an acceptance criterion. Until this tool,
that state lived only in prose on the area feed. This tool makes it machine
form: every improvement proposal moves through the contract's governed state
machine, and every transition is appended to an immutable per-proposal ledger.

State machine (from the contract's ultimate lock state axes):

    OBSERVED_GAP -> PROPOSED -> ANALYZED -> NEEDS_EVIDENCE -+
         |              |           |                       |
         v              v           v                       v
      REJECTED      NEEDS_AUTHORITY -> AUTHORIZED -> IMPLEMENTED -> VERIFIED -> ADOPTED
                           |                            |             |
                           v                            v             v
                        REJECTED                    ROLLED_BACK -> PROPOSED (re-propose)
                                                          |
                                                          v
                                                      SUPERSEDED

ADOPTED -> SUPERSEDED (a newer proposal takes its place).
Terminal states REJECTED and SUPERSEDED accept no further transitions.

ADOPT GATE (measured improvement, not asserted):
  VERIFIED -> ADOPTED is the only transition that changes what the system
  treats as its improved state — so it is the only transition that must
  prove the improvement was MEASURED. The transition requires
  --receipt <file>: a JSON improvement receipt with this shape:

    {
      "proposal_id": "<the proposal being adopted>",
      "verdict": "improved",          # exactly this; anything else refuses
      "measured": [                   # non-empty; every delta was measured
        {"metric": "<name>", "before": <v>, "after": <v>, "method": "<how>"}
      ],
      "measured_at": "<ISO-8601 timestamp>"
    }

  The tool fail-closes (exit 2) when the receipt is missing, unreadable,
  malformed, bound to another proposal, verdict != "improved", or carries
  no measured deltas. The receipt's sha256 is sealed into the ledger entry,
  so the audit trail names the exact bytes that justified the adoption.
  Passing --receipt on any other transition is refused — it signals a
  mistyped target state. Contract invariant enforced as machinery:
  never promote speculative improvements as facts.

Fail-closed contract:
  exit 0 — the command did what it said.
  exit 1 — operational refusal: proposal already exists / not found.
  exit 2 — fail-closed: invalid id, unknown state, or a transition the
           machine does not allow. The error names the allowed targets.

Storage: <root>/.naya/evolve/proposals/<proposal-id>/ledger.jsonl
(append-only; current state is always derived from the ledger tail —
there is no separate index to drift.)

Stdlib only. Every command takes --root so tests run hermetically.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import NoReturn

# ---------------------------------------------------------------------------
# The governed state machine
# ---------------------------------------------------------------------------

OBSERVED_GAP = "OBSERVED_GAP"
PROPOSED = "PROPOSED"
ANALYZED = "ANALYZED"
NEEDS_EVIDENCE = "NEEDS_EVIDENCE"
NEEDS_AUTHORITY = "NEEDS_AUTHORITY"
AUTHORIZED = "AUTHORIZED"
IMPLEMENTED = "IMPLEMENTED"
VERIFIED = "VERIFIED"
ADOPTED = "ADOPTED"
REJECTED = "REJECTED"
ROLLED_BACK = "ROLLED_BACK"
SUPERSEDED = "SUPERSEDED"

STATES = frozenset(
    {
        OBSERVED_GAP,
        PROPOSED,
        ANALYZED,
        NEEDS_EVIDENCE,
        NEEDS_AUTHORITY,
        AUTHORIZED,
        IMPLEMENTED,
        VERIFIED,
        ADOPTED,
        REJECTED,
        ROLLED_BACK,
        SUPERSEDED,
    }
)

TERMINAL = frozenset({REJECTED, SUPERSEDED})

# current state -> allowed next states. Anything not listed is refused.
TRANSITIONS: dict[str, frozenset[str]] = {
    OBSERVED_GAP: frozenset({PROPOSED, REJECTED}),
    PROPOSED: frozenset({ANALYZED, NEEDS_AUTHORITY, REJECTED}),
    ANALYZED: frozenset({NEEDS_EVIDENCE, NEEDS_AUTHORITY, AUTHORIZED, REJECTED}),
    NEEDS_EVIDENCE: frozenset({ANALYZED, REJECTED}),
    NEEDS_AUTHORITY: frozenset({AUTHORIZED, REJECTED}),
    AUTHORIZED: frozenset({IMPLEMENTED, REJECTED}),
    IMPLEMENTED: frozenset({VERIFIED, ROLLED_BACK}),
    VERIFIED: frozenset({ADOPTED, ROLLED_BACK, NEEDS_AUTHORITY}),
    ADOPTED: frozenset({SUPERSEDED}),
    ROLLED_BACK: frozenset({PROPOSED, SUPERSEDED}),
    REJECTED: frozenset(),
    SUPERSEDED: frozenset(),
}

PROPOSAL_ID_RE = re.compile(r"^[a-z0-9][a-z0-9_-]{0,63}$")

EXIT_OK = 0
EXIT_OPERATIONAL = 1  # already exists / not found
EXIT_FAIL_CLOSED = 2  # invalid input or forbidden transition


def die(code: int, message: str) -> NoReturn:
    print(f"evolve_proposals: {message}", file=sys.stderr)
    raise SystemExit(code)


def store_dir(root: Path) -> Path:
    return root / ".naya" / "evolve" / "proposals"


def ledger_path(root: Path, proposal_id: str) -> Path:
    return store_dir(root) / proposal_id / "ledger.jsonl"


def check_id(proposal_id: str) -> None:
    if not PROPOSAL_ID_RE.match(proposal_id):
        die(
            EXIT_FAIL_CLOSED,
            f"invalid proposal id {proposal_id!r}: must match {PROPOSAL_ID_RE.pattern}",
        )


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_ledger(path: Path) -> list[dict]:
    entries = []
    with path.open("r", encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                die(
                    EXIT_FAIL_CLOSED,
                    f"ledger corrupt at {path}:{lineno} — refusing to derive state",
                )
    return entries


def append_entry(path: Path, entry: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, sort_keys=True) + "\n")


def current_state(entries: list[dict]) -> str:
    return entries[-1]["to"]


# ---------------------------------------------------------------------------
# ADOPT gate — measured improvement proof
# ---------------------------------------------------------------------------

#: The only receipt verdict that permits adoption. Anything else (no_change,
#: regressed, unknown, missing) fail-closes the ADOPTED transition.
ADOPT_REQUIRED_VERDICT = "improved"


def validate_receipt(proposal_id: str, raw: bytes) -> dict:
    """Parse and validate an improvement receipt; fail-closed.

    Returns the parsed receipt dict on success. Dies with EXIT_FAIL_CLOSED,
    naming the exact defect, on any violation — a receipt that cannot be
    trusted is not a receipt.
    """
    try:
        receipt = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        die(EXIT_FAIL_CLOSED, f"receipt is not valid JSON: {exc}")
    if not isinstance(receipt, dict):
        die(EXIT_FAIL_CLOSED, "receipt must be a JSON object")
    if receipt.get("proposal_id") != proposal_id:
        die(
            EXIT_FAIL_CLOSED,
            f"receipt proposal_id {receipt.get('proposal_id')!r} does not match "
            f"proposal {proposal_id!r} — refusing cross-proposal adoption",
        )
    if receipt.get("verdict") != ADOPT_REQUIRED_VERDICT:
        die(
            EXIT_FAIL_CLOSED,
            f"receipt verdict is {receipt.get('verdict')!r}; ADOPTED requires "
            f"verdict {ADOPT_REQUIRED_VERDICT!r} — speculative adoption refused",
        )
    measured = receipt.get("measured")
    if not isinstance(measured, list) or not measured:
        die(
            EXIT_FAIL_CLOSED,
            "receipt has no measured deltas — improvement must be measured, not asserted",
        )
    for i, delta in enumerate(measured):
        if not isinstance(delta, dict):
            die(EXIT_FAIL_CLOSED, f"receipt measured[{i}] must be an object")
        for key in ("metric", "before", "after", "method"):
            if key not in delta:
                die(EXIT_FAIL_CLOSED, f"receipt measured[{i}] missing {key!r}")
        if not delta["metric"] or not delta["method"]:
            die(
                EXIT_FAIL_CLOSED,
                f"receipt measured[{i}] needs a named metric and method",
            )
    if not receipt.get("measured_at"):
        die(EXIT_FAIL_CLOSED, "receipt missing measured_at timestamp")
    return receipt


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------


def cmd_record(args: argparse.Namespace) -> int:
    check_id(args.id)
    path = ledger_path(args.root, args.id)
    if path.exists():
        die(EXIT_OPERATIONAL, f"proposal {args.id!r} already recorded")
    entry = {
        "ts": utc_now(),
        "actor": args.actor,
        "from": None,
        "to": OBSERVED_GAP,
        "title": args.title,
        "gap": args.gap,
        "reason": "observed gap recorded",
    }
    append_entry(path, entry)
    print(json.dumps({"id": args.id, "state": OBSERVED_GAP}))
    return EXIT_OK


def cmd_transition(args: argparse.Namespace) -> int:
    check_id(args.id)
    target = args.to
    if target not in STATES:
        die(
            EXIT_FAIL_CLOSED,
            f"unknown state {target!r}; known states: {sorted(STATES)}",
        )
    path = ledger_path(args.root, args.id)
    if not path.exists():
        die(EXIT_OPERATIONAL, f"proposal {args.id!r} not found — record it first")
    entries = read_ledger(path)
    if not entries:
        die(EXIT_FAIL_CLOSED, f"ledger for {args.id!r} is empty — refusing")
    cur = current_state(entries)
    allowed = TRANSITIONS[cur]
    if target not in allowed:
        if cur in TERMINAL:
            die(
                EXIT_FAIL_CLOSED,
                f"proposal {args.id!r} is terminal ({cur}) — no transitions allowed",
            )
        die(
            EXIT_FAIL_CLOSED,
            f"forbidden transition {cur} -> {target} for {args.id!r}; "
            f"allowed: {sorted(allowed) if allowed else 'none'}",
        )
    entry = {
        "ts": utc_now(),
        "actor": args.actor,
        "from": cur,
        "to": target,
        "reason": args.reason,
    }
    if args.evidence:
        entry["evidence"] = args.evidence
    if target == ADOPTED:
        # The ADOPT gate: adoption without measured improvement proof is
        # speculative promotion — the contract forbids it, so the machine
        # refuses it. The receipt's hash is sealed into the ledger entry.
        if not args.receipt:
            die(
                EXIT_FAIL_CLOSED,
                f"ADOPTED requires a measured-improvement receipt "
                f"(--receipt <path>) for {args.id!r}; speculative adoption refused",
            )
        receipt_path = Path(args.receipt)
        try:
            raw = receipt_path.read_bytes()
        except OSError as exc:
            die(EXIT_FAIL_CLOSED, f"cannot read receipt {receipt_path}: {exc}")
        receipt = validate_receipt(args.id, raw)
        entry["receipt_sha256"] = hashlib.sha256(raw).hexdigest()
        entry["receipt_verdict"] = receipt["verdict"]
    elif args.receipt:
        die(
            EXIT_FAIL_CLOSED,
            f"--receipt is only meaningful on the ADOPTED transition "
            f"(got {cur} -> {target})",
        )
    append_entry(path, entry)
    print(json.dumps({"id": args.id, "from": cur, "to": target}))
    return EXIT_OK


def summarize(root: Path, proposal_id: str) -> dict:
    entries = read_ledger(ledger_path(root, proposal_id))
    first = entries[0]
    return {
        "id": proposal_id,
        "title": first.get("title"),
        "state": current_state(entries),
        "transitions": len(entries) - 1,
        "last_ts": entries[-1]["ts"],
        "last_actor": entries[-1]["actor"],
    }


def cmd_status(args: argparse.Namespace) -> int:
    check_id(args.id)
    path = ledger_path(args.root, args.id)
    if not path.exists():
        die(EXIT_OPERATIONAL, f"proposal {args.id!r} not found")
    print(json.dumps(summarize(args.root, args.id), indent=2, sort_keys=True))
    return EXIT_OK


def cmd_list(args: argparse.Namespace) -> int:
    base = store_dir(args.root)
    wanted = args.state
    if wanted is not None and wanted not in STATES:
        die(EXIT_FAIL_CLOSED, f"unknown state {wanted!r}")
    out = []
    if base.is_dir():
        for child in sorted(base.iterdir()):
            if not child.is_dir():
                continue
            if not (child / "ledger.jsonl").exists():
                continue
            summary = summarize(args.root, child.name)
            if wanted is None or summary["state"] == wanted:
                out.append(summary)
    print(json.dumps(out, indent=2, sort_keys=True))
    return EXIT_OK


def cmd_audit(args: argparse.Namespace) -> int:
    check_id(args.id)
    path = ledger_path(args.root, args.id)
    if not path.exists():
        die(EXIT_OPERATIONAL, f"proposal {args.id!r} not found")
    print(json.dumps(read_ledger(path), indent=2, sort_keys=True))
    return EXIT_OK


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def default_root() -> Path:
    # tools/evolve_proposals.py -> repo root
    return Path(__file__).resolve().parents[1]


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="EVOLVE proposal-lifecycle ledger: governed, auditable evolution state."
    )
    p.add_argument(
        "--root",
        type=Path,
        default=default_root(),
        help="workdir root holding .naya/evolve/proposals/ (default: repo root)",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("record", help="record a new observed gap (state OBSERVED_GAP)")
    r.add_argument("--id", required=True)
    r.add_argument("--title", required=True)
    r.add_argument("--gap", required=True, help="the observed gap, in plain words")
    r.add_argument("--actor", required=True)
    r.set_defaults(func=cmd_record)

    t = sub.add_parser("transition", help="move a proposal to its next governed state")
    t.add_argument("--id", required=True)
    t.add_argument("--to", required=True, help="target state")
    t.add_argument("--actor", required=True)
    t.add_argument("--reason", required=True)
    t.add_argument("--evidence", default=None, help="link to the evidence, if any")
    t.add_argument(
        "--receipt",
        default=None,
        help="path to a JSON improvement receipt (REQUIRED for --to ADOPTED)",
    )
    t.set_defaults(func=cmd_transition)

    s = sub.add_parser("status", help="current state of one proposal")
    s.add_argument("--id", required=True)
    s.set_defaults(func=cmd_status)

    l = sub.add_parser("list", help="all proposals, optionally filtered by state")
    l.add_argument("--state", default=None)
    l.set_defaults(func=cmd_list)

    a = sub.add_parser("audit", help="full transition history of one proposal")
    a.add_argument("--id", required=True)
    a.set_defaults(func=cmd_audit)

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
