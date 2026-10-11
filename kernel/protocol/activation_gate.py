"""activation_gate.py — Fail-closed activation gate (session admission).

A worker may not begin governed work unless it presents all four:
  1. IDENTITY       — who is acting (seat/lane), under whose dispatch
  2. SOURCE_VERSIONS — exact SHAs of the official knowledge it read
                       (root PROTOCOL.md, mission state, activation sources)
  3. QUALIFICATION  — activation qualification record (e.g. Cold-14 pass),
                       bound to the same protocol version it claims to have read
  4. READINESS      — environment + tooling + preconditions verified

Missing ANY of these -> fail-closed: no governed work. The gate returns a
structured Refusal record (code, missing evidence, remediation) INSTEAD OF
output, suitable for writing into the worker receipt.

This is the session/cycle-level admission check in the
WAKE -> UNDERSTAND -> GATE spine: it runs between WAKE (step 1) and
RESTORE TRUTH (step 2). Step-5 GATE (authority_gate.py) is UNCHANGED and still
classifies every consequential action. Admission verifies preconditions;
authority classification still runs before every action.

SHA resolution is injected via a `resolver` callable so unit tests never touch
the network. In production the resolver is `git cat-file -e <sha>`: the claimed
SHA must be a REAL object, not a well-formed-looking string.

Refusal codes: IDENTITY_MISSING | VERSION_UNRESOLVABLE | VERSION_MISMATCH
  | QUALIFICATION_MISSING | QUALIFICATION_FAILED | QUALIFICATION_STALE
  | READINESS_FAILED

Design: receipts/t2252-a-design.md (night shift, t2252-a).
Tests: tests/test_activation_gate.py (positive + negative controls).
Manifest: kernel/protocol/protocol_manifest.json, id SN-ACTIVATION-GATE.
"""

from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone


# ---------------------------------------------------------------------------
# Evidence contract
# ---------------------------------------------------------------------------

SHA40 = re.compile(r"^[0-9a-f]{40}$")


@dataclass
class SourceVersion:
    """One official knowledge source the worker claims to have read."""

    path: str            # repo-relative path, e.g. "PROTOCOL.md"
    sha: str             # exact blob/commit SHA it claims to have read
    kind: str = "blob"   # "blob" | "commit" | "tree"


@dataclass
class Qualification:
    """Activation qualification evidence (e.g. Cold-14 pass record)."""

    test_id: str              # e.g. "cold-14"
    protocol_version: str      # SHA of the PROTOCOL.md version it was graded against
    passed: bool
    graded_at: str            # ISO-8601 UTC timestamp
    grader: str               # who graded: seat id or "self-test"


@dataclass
class Readiness:
    """Environment + tooling + preconditions, verified by the worker."""

    git_available: bool
    remote_reachable: bool
    tip_sha: str               # tip the worker resolved at readiness time
    tip_fresh: bool            # tip resolved fresh (SN-0493: decision expires when tip moves)
    workspace_writable: bool


@dataclass
class Identity:
    seat_id: str        # e.g. "naya-4-worker-t2312-a"
    lane: str           # lane/team owning the work
    dispatcher: str     # who briefed this worker
    human_director: str = "Shawn"


@dataclass
class ActivationEvidence:
    identity: Identity | None = None
    sources: list[SourceVersion] = field(default_factory=list)
    qualification: Qualification | None = None
    readiness: Readiness | None = None


# ---------------------------------------------------------------------------
# Adjudication contract
# ---------------------------------------------------------------------------

@dataclass
class Refusal:
    """Structured refusal record — written to the receipt instead of output."""

    code: str
    missing_evidence: list[str]
    remediation: str
    recorded_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)


@dataclass
class Admission:
    """The worker may begin governed work. Authority still comes from grants."""

    seat_id: str
    verified_sources: list[str]
    recorded_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat())
    note: str = ("Admission verifies preconditions, not authority. "
                 "Protected gates (authority_gate.py) still apply per action.")

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)


# Sources that MUST be version-bound. A worker claiming activation without
# these is claiming it "read" nothing verifiable.
REQUIRED_SOURCE_PATHS = frozenset({"PROTOCOL.md"})

MAX_TIP_STALENESS_NOTE = ("Tip freshness is a boolean here (SN-0493): the worker "
                          "must re-resolve the tip at readiness time. Stale = fail.")


# ---------------------------------------------------------------------------
# The gate
# ---------------------------------------------------------------------------

def refuse(code: str, missing: list[str], remediation: str) -> Refusal:
    return Refusal(code=code, missing_evidence=missing, remediation=remediation)


def run_gate(evidence: ActivationEvidence, resolver) -> Admission | Refusal:
    """Adjudicate. Fail-closed: the FIRST missing category ends evaluation.

    `resolver(sha) -> bool`: True iff sha is a real object (git cat-file -e).
    Never consult memory, never accept a SHA on format alone.
    """

    # 1. IDENTITY -----------------------------------------------------------
    ident = evidence.identity
    if ident is None:
        return refuse("IDENTITY_MISSING", ["identity"],
                      "Present seat_id, lane, dispatcher, and human director before retry.")
    missing_id = [f for f in ("seat_id", "lane", "dispatcher")
                  if not getattr(ident, f, "").strip()]
    if missing_id:
        return refuse("IDENTITY_MISSING", [f"identity.{f}" for f in missing_id],
                      "Identity must name seat, lane, and dispatcher.")
    if "shawn" not in ident.human_director.lower():
        return refuse("IDENTITY_MISSING", ["identity.human_director"],
                      "Human director must be identified as Shawn.")

    # 2. SOURCE VERSIONS ----------------------------------------------------
    if not evidence.sources:
        return refuse("VERSION_UNRESOLVABLE", ["sources"],
                      "Bind exact SHAs of the official knowledge you read; none were presented.")
    claimed = {s.path for s in evidence.sources}
    missing_req = sorted(REQUIRED_SOURCE_PATHS - claimed)
    if missing_req:
        return refuse("VERSION_UNRESOLVABLE", [f"sources.{p}" for p in missing_req],
                      f"Required sources not version-bound: {', '.join(missing_req)}.")
    unresolvable: list[str] = []
    for s in evidence.sources:
        if not SHA40.match(s.sha or ""):
            unresolvable.append(f"{s.path}: malformed SHA")
            continue
        try:
            ok = resolver(s.sha)
        except Exception:
            ok = False
        if not ok:
            unresolvable.append(f"{s.path}@{s.sha[:12]}")
    if unresolvable:
        return refuse("VERSION_UNRESOLVABLE", unresolvable,
                      "Every claimed SHA must resolve to a real object (git cat-file -e). "
                      "A well-formed string that resolves nowhere is a forged version.")

    # 3. QUALIFICATION ------------------------------------------------------
    qual = evidence.qualification
    if qual is None:
        return refuse("QUALIFICATION_MISSING", ["qualification"],
                      "Present an activation qualification record (e.g. Cold-14 pass). "
                      "No qualification, no governed work.")
    if not qual.passed:
        return refuse("QUALIFICATION_FAILED", ["qualification.passed"],
                      "Qualification did not pass. Re-qualify before retry.")
    # The qualification must be bound to the SAME protocol version claimed.
    proto_shas = {s.sha for s in evidence.sources if s.path == "PROTOCOL.md"}
    if qual.protocol_version not in proto_shas:
        return refuse("VERSION_MISMATCH", ["qualification.protocol_version"],
                      "Qualification was graded against a different PROTOCOL.md version "
                      "than the one presented. Re-qualify against the current version.")

    # 4. READINESS ----------------------------------------------------------
    ready = evidence.readiness
    if ready is None:
        return refuse("READINESS_FAILED", ["readiness"],
                      "Verify environment, tooling, and preconditions before retry.")
    failed_checks = [name for name, val in
                     (("git_available", ready.git_available),
                      ("remote_reachable", ready.remote_reachable),
                      ("tip_fresh", ready.tip_fresh),
                      ("workspace_writable", ready.workspace_writable))
                     if not val]
    if failed_checks:
        return refuse("READINESS_FAILED", [f"readiness.{c}" for c in failed_checks],
                      f"{MAX_TIP_STALENESS_NOTE} Fix and re-verify.")
    if not SHA40.match(ready.tip_sha or ""):
        return refuse("READINESS_FAILED", ["readiness.tip_sha"],
                      "tip_sha must be a 40-hex SHA.")

    return Admission(seat_id=ident.seat_id,
                     verified_sources=[f"{s.path}@{s.sha[:12]}" for s in evidence.sources])


# ---------------------------------------------------------------------------
# Production resolver (real SHA check, read-only git protocol)
# ---------------------------------------------------------------------------

def git_resolver(sha: str) -> bool:
    """True iff sha resolves to a real object in the local repo."""
    try:
        r = subprocess.run(["git", "cat-file", "-e", sha],
                           capture_output=True, timeout=15)
        return r.returncode == 0
    except Exception:
        return False
