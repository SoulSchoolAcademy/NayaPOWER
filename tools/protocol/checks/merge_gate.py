#!/usr/bin/env python3
"""Merge-path executor for Delegated Merge Authority check #4.

Naya Delta's recommendation A (2026-10-12): check #4 ("no merge to main
without independent validation by a different seat") EXISTS in
merge_authority.py but NOTHING executes it before a merge. This module is
the executor: call enforce() (or the CLI) with the ref about to be updated
and the merge packet; it runs merge_authority.check() and FAILS CLOSED
unless the packet passes.

The five conditions executed are EXACTLY the five ratified ones — this
executor adds no conditions. It never grants authority; it verifies the
packet that claims it, with the same fail-closed semantics as the check.

The #1354 wrinkle: the ratified packet field is `posted_to_1354`, but #1354
is comment-locked and team coordination moved to #2154 (2026-10-12). The
executor keeps the ratified field name and binds the boolean to the live
team feed, saying so in the receipt — the ratified INTENT is "team
consensus on the team feed".

Scope pinning: the check's own scope rule passes any packet whose target
is not "main". The executor pins target="main" before calling the check so
a packet cannot smuggle a different target past the gate — that is scope
enforcement, not a new condition.

Honest limit (stated in every refusal and receipt): a script-level gate
binds the team's merge path. A seat with raw API access could still update
the ref directly; the ledger (#2154 receipts) remains the audit surface.
This gate makes unauthorized merges impossible through the team's scripts,
not impossible in principle.

Wiring (the live operator copies in ~/workspace/naya/bin — the actual
merge path; this repo file is the canonical version, synced byte-identical):
  - merge_branch_api.py, merge_pr_api.py: these only ever update
    refs/heads/main, so the gate fires on every invocation. Top of
    main(), before any verification or API call:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from merge_gate import gate_from_argv
        gate_from_argv(sys.argv, ref="refs/heads/main")
  - push_branch_api.py: can push any branch; the gate fires only when the
    target ref is refs/heads/main (feature branches pass by scope). Top of
    main(), packet stripped before positional parsing:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from merge_gate import take_packet, enforce_gate
        _packet, _stripped = take_packet(sys.argv)
        sys.argv[:] = _stripped
        ...
        enforce_gate(f"refs/heads/{branch}", _packet)
  - push_branch_preserve.py: NOT wired — it already refuses branch "main"
    outright (fail-closed, stricter than the gate), so the gate is vacuous
    there. If that refusal is ever relaxed, the gate must be wired in.

The merge packet: --packet <json-file> on any wired script. Without a
passing packet the script exits 1 before any API call — the merge still
needs Shawn's word, exactly as the delegation says.

Usage:
    python3 tools/protocol/checks/merge_gate.py \\
        --ref refs/heads/main --record '{"branch": "...", ...}' [--json]

Exit codes: 0 = gate PASSED (ref update may proceed); 1 = gate REFUSED
(the ref update must NOT proceed — under the delegation this merge still
needs Shawn's word); 2 = usage / malformed input (also a refusal).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


def _checks_roots():
    """Where the `checks` package (merge_authority.py) can live.

    The repo copy of this file sits at tools/protocol/checks/merge_gate.py
    (parents[1] is tools/protocol). The live operator copy sits in
    ~/workspace/naya/bin and must resolve the canonical repo clone.
    NAYAPOWER_REPO overrides everything.
    """
    roots = []
    env = os.environ.get("NAYAPOWER_REPO")
    if env:
        roots.append(Path(env) / "tools" / "protocol")
    roots.append(Path.home() / "workspace" / "nayapower-work" / "tools" / "protocol")
    roots.append(Path(__file__).resolve().parents[1])
    return roots


for _root in _checks_roots():
    if (_root / "checks" / "merge_authority.py").is_file():
        sys.path.insert(0, str(_root))
        break

try:
    from checks import merge_authority  # noqa: E402
    _CHECK_AVAILABLE = True
    _CHECK_IMPORT_ERROR: Exception | None = None
except Exception as e:  # fail closed: a missing check never means "allowed"
    merge_authority = None  # type: ignore[assignment]
    _CHECK_AVAILABLE = False
    _CHECK_IMPORT_ERROR = e

MAIN_REF = "refs/heads/main"

# The ratified field name stays `posted_to_1354`; the boolean binds to the
# live team feed (#2154) because #1354 is comment-locked. Said plainly in
# every receipt so no operator mistakes the field name for the venue.
LIVE_FEED_BINDING = (
    "posted_to_1354 binds to the LIVE team feed (#2154 — #1354 is "
    "comment-locked): the ratified intent is 'intent + scorecard + "
    "validation posted, team consensus, no seat objects'"
)

RAW_API_RESIDUAL = (
    "Honest limit: this gate binds the team's merge scripts. A seat with "
    "raw API access could update the ref directly; #2154 receipts remain "
    "the audit surface."
)


class GateRefused(Exception):
    """The gate refused a main-ref update. reasons are plain words."""

    def __init__(self, reasons):
        self.reasons = list(reasons)
        super().__init__("; ".join(self.reasons))


def enforce(ref: str, record) -> dict:
    """Run the merge-authority gate for an intended ref update.

    Returns {"allowed": True, "reasons": [...], "details": {...}} when the
    ref update may proceed. Raises GateRefused when it must not.
    """
    ref = (ref or "").strip()

    # Scope: the delegation covers merges to main ONLY. Anything else
    # passes by scope — the law's own boundary, not a loophole.
    if ref != MAIN_REF:
        return {
            "allowed": True,
            "reasons": [
                f"{ref or '(unnamed ref)'} is not {MAIN_REF} — the "
                "delegated merge authority covers main only; PASS by "
                "scope, not by permission"
            ],
            "details": {"ref": ref, "scope": "not-main"},
        }

    # The check itself must be loadable. A missing check is a refusal,
    # never a permission — erasing the gate is not passing it.
    if not _CHECK_AVAILABLE:
        raise GateRefused([
            "merge_authority check #4 could not be loaded "
            f"({_CHECK_IMPORT_ERROR}); the gate cannot verify the packet, "
            "so the ref update is REFUSED. A missing check never means "
            "'allowed'.",
            RAW_API_RESIDUAL,
        ])

    if not isinstance(record, dict):
        raise GateRefused([
            "no merge packet supplied — the delegated merge authority "
            "requires all five conditions verified before a main-ref "
            "update. Absence fails closed, never defaults to permitted. "
            "Supply the packet (--packet <file>) or get Shawn's word. "
            "This merge still needs Shawn's word.",
            RAW_API_RESIDUAL,
        ])

    # Pin the scope: the check passes packets whose target is not "main",
    # so the executor sets target="main" itself. Scope enforcement, not a
    # new condition — the delegation's boundary is main, full stop.
    packet = dict(record)
    packet["target"] = "main"

    res = merge_authority.check(packet)
    if not res.get("pass"):
        reasons = list(res.get("reasons", ["packet did not pass"]))
        reasons.append(
            "Under the Delegated Merge Authority this merge still needs "
            "Shawn's word."
        )
        reasons.append(RAW_API_RESIDUAL)
        raise GateRefused(reasons)

    reasons = list(res.get("reasons", []))
    reasons.append(LIVE_FEED_BINDING)
    reasons.append(RAW_API_RESIDUAL)
    return {
        "allowed": True,
        "reasons": reasons,
        "details": dict(res.get("details", {}), ref=ref,
                        live_feed_binding=LIVE_FEED_BINDING),
    }


def take_packet(argv):
    """Parse an optional --packet <json-file> out of argv.

    Returns (packet_or_None, stripped_argv). The --packet pair is removed
    so the caller's own positional parsing is unaffected. A missing path
    or unreadable file is a usage error (exit 2) — never a silent skip.
    """
    args = list(argv)
    if "--packet" not in args:
        return None, args
    i = args.index("--packet")
    try:
        packet_path = args[i + 1]
    except IndexError:
        print("merge gate: --packet needs a file path", file=sys.stderr)
        sys.exit(2)
    del args[i:i + 2]
    try:
        packet = json.loads(Path(packet_path).read_text())
    except Exception as e:
        print(f"merge gate: cannot read packet file {packet_path}: {e}",
              file=sys.stderr)
        sys.exit(2)
    return packet, args


def enforce_gate(ref, packet):
    """Enforce the gate for `ref` with an already-parsed packet.

    Prints the receipt. On refusal prints plain-words reasons and exits 1;
    on pass returns the packet (None when the ref is not main).
    """
    try:
        res = enforce(ref, packet)
    except GateRefused as e:
        print("MERGE GATE REFUSED — no ref update will happen:", file=sys.stderr)
        for r in e.reasons:
            print(f"  - {r}", file=sys.stderr)
        sys.exit(1)
    for r in res["reasons"]:
        print(f"merge gate: {r}")
    return packet


def gate_from_argv(argv, ref):
    """Drop-in for the team's merge scripts.

    Parses an optional --packet <json-file> out of argv (removing it so the
    script's own positional parsing is unaffected), then enforces the gate
    for `ref`. On refusal prints plain-words reasons and exits 1; on pass
    returns the packet (or None when the ref is not main).
    """
    packet, stripped = take_packet(argv)
    argv[:] = stripped
    return enforce_gate(ref, packet)


def main() -> int:
    parser = argparse.ArgumentParser(description="Merge-authority check #4 executor")
    parser.add_argument("--ref", required=True,
                        help="ref about to be updated, e.g. refs/heads/main")
    parser.add_argument("--record", required=True,
                        help="JSON merge packet (or @file)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()
    try:
        record = json.loads(Path(args.record[1:]).read_text()
                            if args.record.startswith("@")
                            else args.record)
    except Exception as e:
        print(f"merge gate: unparseable packet: {e}", file=sys.stderr)
        return 2
    try:
        res = enforce(args.ref, record)
    except GateRefused as e:
        if args.json:
            print(json.dumps({"allowed": False, "reasons": e.reasons}, indent=2))
        else:
            print("REFUSED — no ref update may proceed:")
            for r in e.reasons:
                print(f"  - {r}")
        return 1
    if args.json:
        print(json.dumps(res, indent=2))
    else:
        print("PASSED — ref update may proceed:")
        for r in res["reasons"]:
            print(f"  - {r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
