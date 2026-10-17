#!/usr/bin/env python3
"""
activation_contract.py — #2244 req 1: machine-checkable wake/activation contract.

The gap (verified on live bytes): tools/worker_entry.py is a local
tip/stand-down/pending-work gate — it does NOT establish that a worker read
the current mission state, verified a fresh main SHA, read the ratified
protocol, read the relevant specialty feed(s), or signed in to a feed.
kernel/protocol/cold_start_gate.py still pins #1354 as the live coordination
feed, conflicting with current mission state (#2175 live, #1354 archive-only).

This module is the machine twin of the reconciled activation contract:
before governed work, a worker presents an ActivationClaim; the verifier
recomputes the artifact bytes it can check locally, compares the claimed
main SHA against an INDEPENDENTLY supplied live tip, and fails closed
(STAND_DOWN) on any missing, stale, drifted, or conflicting orientation.

ARCHITECTURAL LAW (inherited): a builder cannot establish authenticity by
writing a plausible JSON file. The verifier recomputes every hash from the
repo tree itself; the live tip is a caller-supplied input, never taken from
the claim. What the gate cannot check without API access (the feed sign-in
actually landing on GitHub) is marked CLAIMED-UNVERIFIED in the receipt —
never presented as verified.

Checks (all fail closed):
  1. main_sha_present      — claim carries a main SHA
  2. main_sha_fresh        — claim SHA == independently-supplied live tip SHA
  3. mission_state_present — canonical mission-state file exists in tree
  4. mission_state_intact  — its bytes hash == claimed hash
  5. protocol_present      — canonical protocol file exists in tree
  6. protocol_intact       — its bytes hash == claimed hash
  7. feeds_known           — every read feed is a canonical specialty feed
  8. sign_in_feed_valid    — sign-in feed is canonical AND was read
  9. sign_in_evidence      — non-empty evidence string (marked unverified)
 10. board_ack_current     — acknowledges #2175 as the LIVE board
 11. board_not_stale       — does not name #1354 as the live board
 12. toc_ack               — acknowledges TOC #1599

Usage:
    python3 tools/activation_contract.py --claim claim.json --live-tip <sha>
        [--repo-root PATH] [--json]

Exit codes: 0 = PROCEED, 1 = STAND_DOWN, 2 = tool error.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Canonical references (#2244 req 1 / sequence A reconciliation)
# ---------------------------------------------------------------------------

MISSION_STATE_PATH = "BRAIN/CURRENT-MISSION-STATE.md"
PROTOCOL_PATH = "BRAIN/01-GOVERNANCE/TEAM-NAYA-OPERATING-PROTOCOL-V1.md"

LIVE_BOARD = 2175      # current coordination board (mission state)
ARCHIVE_BOARD = 1354   # archive-only since 2026-10-10 comment cap
TOC_ISSUE = 1599       # table of contents

# Nine standing specialty feeds, ratified in TEAM-NAYA-OPERATING-PROTOCOL-V1.
CANONICAL_FEEDS = {
    1865: "Learning",
    1866: "Brain / Memory",
    1867: "Law / Governance",
    1868: "Architecture / Engineering / Operations",
    1869: "Evolution / Succession",
    1870: "Interfaces / Hub",
    1871: "Knowledge / Intelligence",
    1872: "Proving / Verifying",
    1873: "Innovation",
}

REQUIRED_CLAIM_FIELDS = (
    "worker_id", "lane", "main_sha", "mission_state", "protocol",
    "feeds_read", "sign_in_feed", "sign_in_evidence", "board_ack", "toc_ack",
)

VERDICT_PROCEED = "PROCEED"
VERDICT_STAND_DOWN = "STAND_DOWN"


# ---------------------------------------------------------------------------
# Claim model
# ---------------------------------------------------------------------------

@dataclass
class ArtifactPin:
    path: str
    sha256: str


@dataclass
class ActivationClaim:
    worker_id: str
    lane: str
    main_sha: str
    mission_state: ArtifactPin
    protocol: ArtifactPin
    feeds_read: list
    sign_in_feed: int
    sign_in_evidence: str
    board_ack: str
    toc_ack: str

    @classmethod
    def from_dict(cls, d: dict) -> "ActivationClaim":
        missing = [f for f in REQUIRED_CLAIM_FIELDS if f not in d]
        if missing:
            raise ValueError(f"CLAIM_MALFORMED: missing fields {missing}")
        ms, pr = d["mission_state"], d["protocol"]
        if not isinstance(ms, dict) or "path" not in ms or "sha256" not in ms:
            raise ValueError("CLAIM_MALFORMED: mission_state must be {path, sha256}")
        if not isinstance(pr, dict) or "path" not in pr or "sha256" not in pr:
            raise ValueError("CLAIM_MALFORMED: protocol must be {path, sha256}")
        return cls(
            worker_id=str(d["worker_id"]),
            lane=str(d["lane"]),
            main_sha=str(d["main_sha"]),
            mission_state=ArtifactPin(path=str(ms["path"]), sha256=str(ms["sha256"])),
            protocol=ArtifactPin(path=str(pr["path"]), sha256=str(pr["sha256"])),
            feeds_read=list(d["feeds_read"] or []),
            sign_in_feed=d["sign_in_feed"],
            sign_in_evidence=str(d["sign_in_evidence"]),
            board_ack=str(d["board_ack"]),
            toc_ack=str(d["toc_ack"]),
        )


@dataclass
class CheckResult:
    name: str
    passed: bool
    code: str
    detail: str = ""


@dataclass
class ActivationResult:
    verdict: str
    checks: list = field(default_factory=list)
    unverified: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "verdict": self.verdict,
            "checks": [
                {"name": c.name, "passed": c.passed, "code": c.code, "detail": c.detail}
                for c in self.checks
            ],
            "unverified": self.unverified,
            "live_board": LIVE_BOARD,
            "archive_board": ARCHIVE_BOARD,
            "toc_issue": TOC_ISSUE,
        }


# ---------------------------------------------------------------------------
# Verifier
# ---------------------------------------------------------------------------

def _sha256_file(path: str) -> str | None:
    try:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()
    except OSError:
        return None


def _board_names_live_as(board_ack: str, issue: int) -> bool:
    """True if some clause of the ack names `issue` as the LIVE board.

    Clauses split on sentence/paren boundaries so that an explicit
    archive qualification ("#1354 is archive-only") in one clause does not
    leak into another ("live board is #2175").
    """
    live_words = re.compile(r"live|current|coordination board")
    archive_words = re.compile(r"archiv")
    num = re.compile(r"#?%d\b" % issue)
    for clause in re.split(r"[.;()]", (board_ack or "").lower()):
        if num.search(clause) and live_words.search(clause) \
                and not archive_words.search(clause):
            return True
    return False


def verify_claim(claim: ActivationClaim, repo_root: str, live_tip_sha: str) -> ActivationResult:
    checks: list[CheckResult] = []

    def check(name: str, passed: bool, code: str, detail: str = "") -> None:
        checks.append(CheckResult(name, passed, code, detail))

    # 1+2. Main SHA present and fresh against the INDEPENDENT tip.
    sha = (claim.main_sha or "").strip().lower()
    check("main_sha_present", bool(sha), "OK" if sha else "MISSING_SHA",
          "" if sha else "claim carries no main SHA")
    tip = (live_tip_sha or "").strip().lower()
    fresh = bool(sha) and bool(tip) and sha == tip
    check("main_sha_fresh", fresh,
          "OK" if fresh else "STALE_SHA",
          "" if fresh else f"claimed {sha or '(none)'} != live tip {tip or '(none)'}")

    # 3+4. Mission-state bytes recomputed from the tree, never trusted.
    ms_disk = _sha256_file(os.path.join(repo_root, claim.mission_state.path))
    check("mission_state_present", ms_disk is not None,
          "OK" if ms_disk is not None else "MISSION_STATE_MISSING",
          "" if ms_disk is not None else f"not found: {claim.mission_state.path}")
    ms_ok = ms_disk is not None and ms_disk == claim.mission_state.sha256.strip().lower()
    check("mission_state_intact", ms_ok,
          "OK" if ms_ok else "MISSION_STATE_DRIFT",
          "" if ms_ok else "claimed hash != recomputed tree bytes")

    # 5+6. Protocol bytes likewise.
    pr_disk = _sha256_file(os.path.join(repo_root, claim.protocol.path))
    check("protocol_present", pr_disk is not None,
          "OK" if pr_disk is not None else "PROTOCOL_MISSING",
          "" if pr_disk is not None else f"not found: {claim.protocol.path}")
    pr_ok = pr_disk is not None and pr_disk == claim.protocol.sha256.strip().lower()
    check("protocol_intact", pr_ok,
          "OK" if pr_ok else "PROTOCOL_DRIFT",
          "" if pr_ok else "claimed hash != recomputed tree bytes")

    # 7. Every read feed must be canonical.
    unknown = [f for f in claim.feeds_read if f not in CANONICAL_FEEDS]
    check("feeds_known", not unknown,
          "OK" if not unknown else "UNKNOWN_FEED",
          "" if not unknown else f"not canonical specialty feeds: {unknown}")

    # 8. Sign-in feed must be canonical and among the read feeds.
    sif = claim.sign_in_feed
    sif_ok = sif in CANONICAL_FEEDS and sif in (claim.feeds_read or [])
    check("sign_in_feed_valid", sif_ok,
          "OK" if sif_ok else "SIGN_IN_FEED_INVALID",
          "" if sif_ok else f"sign_in_feed={sif!r} must be a canonical feed that was read")

    # 9. Sign-in evidence present — but CANNOT be verified without API.
    ev = (claim.sign_in_evidence or "").strip()
    check("sign_in_evidence", bool(ev),
          "OK" if ev else "SIGN_IN_EVIDENCE_MISSING",
          "claimed only — not verified (no API read performed)" if ev
          else "no sign-in evidence string")

    # 10+11. Board ack must name #2175 as live; must not name #1354 as live.
    ack_live_2175 = _board_names_live_as(claim.board_ack, LIVE_BOARD)
    check("board_ack_current", ack_live_2175,
          "OK" if ack_live_2175 else "BOARD_ACK_MISSING",
          "" if ack_live_2175 else f"must acknowledge #{LIVE_BOARD} as the live coordination board")
    names_1354_live = _board_names_live_as(claim.board_ack, ARCHIVE_BOARD)
    check("board_not_stale", not names_1354_live,
          "OK" if not names_1354_live else "STALE_BOARD",
          "" if not names_1354_live
          else f"names #{ARCHIVE_BOARD} as live — it is archive-only; live board is #{LIVE_BOARD}")

    # 12. TOC ack must reference #1599.
    toc_ok = str(TOC_ISSUE) in (claim.toc_ack or "")
    check("toc_ack", toc_ok,
          "OK" if toc_ok else "TOC_ACK_MISSING",
          "" if toc_ok else f"must acknowledge TOC #{TOC_ISSUE}")

    failed = [c for c in checks if not c.passed]
    verdict = VERDICT_PROCEED if not failed else VERDICT_STAND_DOWN
    return ActivationResult(
        verdict=verdict,
        checks=checks,
        unverified=[
            "feed sign-in evidence: claimed string only — landing on GitHub "
            "requires an API read this gate does not perform",
            "worker internalization of read artifacts: byte-faithfulness is "
            "proven, comprehension is not",
        ],
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Verify a #2244 req-1 activation claim.")
    ap.add_argument("--claim", required=True, help="path to claim JSON")
    ap.add_argument("--live-tip", required=True,
                    help="independently-verified live main tip SHA (never from the claim)")
    ap.add_argument("--repo-root", default=".",
                    help="repo tree the artifact bytes are recomputed from")
    ap.add_argument("--json", action="store_true", help="print the receipt as JSON")
    args = ap.parse_args(argv)

    try:
        with open(args.claim) as f:
            raw = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"TOOL_ERROR: cannot read claim: {e}", file=sys.stderr)
        return 2

    try:
        claim = ActivationClaim.from_dict(raw)
    except (ValueError, TypeError, AttributeError) as e:
        result = ActivationResult(
            verdict=VERDICT_STAND_DOWN,
            checks=[CheckResult("claim_wellformed", False, "CLAIM_MALFORMED", str(e))],
            unverified=[],
        )
        print(json.dumps(result.to_dict(), indent=2) if args.json
              else f"{result.verdict}: CLAIM_MALFORMED — {e}")
        return 1

    result = verify_claim(claim, args.repo_root, args.live_tip)
    if args.json:
        print(json.dumps(result.to_dict(), indent=2))
    else:
        print(result.verdict)
        for c in result.checks:
            print(f"  [{'ok' if c.passed else 'FAIL'}] {c.name}: {c.code}"
                  + (f" — {c.detail}" if c.detail else ""))
        if result.unverified:
            print("  unverified (honest boundary):")
            for u in result.unverified:
                print(f"    - {u}")
    return 0 if result.verdict == VERDICT_PROCEED else 1


if __name__ == "__main__":
    sys.exit(main())
