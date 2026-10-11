#!/usr/bin/env python3
"""Assumption-guarantee boundary for the fairness machinery — D27.

Directive D27 (directive-register wave 6, owner naya2): every guarantee the
fairness gate makes must name the assumptions it rests on, and every
assumption must be REGISTERED — never free text. A verdict that rests on a
phantom (unregistered) assumption is not a verdict: the prover refuses to
emit one.

The boundary table
------------------
GUARANTEES (what the machinery promises):
  FG-G1  No silent green — scanner errors exit 2, never 0.
  FG-G2  Unknown is unknown — missing evidence widens the debt bound; it
         never manufactures a violation and never manufactures a pass.
  FG-G3  Every verdict names one of D26's four explicit verdict levels.
  FG-G4  The scheduler's claim is recorded but never trusted; evidence
         contradictions are named.
  FG-G5  Debt accrues only for eligible, unblocked, unparked items whose
         ready_since is provable from evidence timestamps.
  FG-G6  Cross-seat predicates treat an undeclared author seat per the
         registered inference rule.

ASSUMPTIONS (what the guarantees rest on):
  FA-A1  Author-seat inference — when the author seat is undeclared,
         cross-seat predicates accept any named reviewer seat
         (branch-prefix fallback for author inference).
  FA-A2  blocked_by deferral is legitimate queue ordering, not starvation;
         accrues no debt.
  FA-A3  Parked items (awaiting Shawn's word, the human gate) are not
         starvation; accrue no debt.
  FA-A4  ready_since unprovable from evidence timestamps -> the bound is
         widened per the missing-evidence rule and no debt accrues.

Fail-closed rules
-----------------
  - resolve() of an unknown id or statement raises UnknownAssumptionError.
    Callers (notably EligibilityProver.prove) resolve BEFORE emitting any
    verdict, so a phantom assumption can never be silently named.
  - Duplicate registration raises BoundaryError; the canonical registration
    is never mutated by a rejected write.
  - Import-time self-check: the boundary table must be CLOSED — every
    guarantee names only registered assumptions, every assumption is relied
    upon by at least one component and at least one guarantee, and every
    legacy spelling maps to exactly one registered id. A broken boundary
    fails at import; it never ships silently.

Note on the directive register: the machine-readable register lives on the
#2225 chain (unmerged at the time of writing). This module references D27 by
its stable directive id and does NOT import the unmerged register — no
phantom dependency. When #2225 merges, the promotion mechanism (PR #2294)
is the honest path that flips D27 to BUILT_AS_CODE with this module as
evidence.

Stdlib only.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Tuple


class UnknownAssumptionError(LookupError):
    """An assumption reference that resolves to no registered assumption.

    Raised fail-closed: the caller must not emit a verdict resting on it.
    """


class BoundaryError(Exception):
    """The assumption registry or the boundary table is structurally broken."""


# Canonical assumption ids. Import these; never hand-spell the strings.
FA_A1 = "FA-A1"
FA_A2 = "FA-A2"
FA_A3 = "FA-A3"
FA_A4 = "FA-A4"


@dataclass(frozen=True)
class Assumption:
    """One registered operating assumption.

    id: canonical id (FA-A<n>).
    statement: the exact human-readable meaning. Frozen: the statement is the
        contract; changing the meaning means registering a new id.
    relied_upon_by: dotted component paths that rest behavior on this
        assumption (documentation + the closure check, not runtime hooks).
    legacy_spellings: free-text forms used before registration (old snapshots,
        old code). They keep resolving so history does not silently break.
    """
    id: str
    statement: str
    relied_upon_by: Tuple[str, ...] = ()
    legacy_spellings: Tuple[str, ...] = ()


ASSUMPTIONS: Dict[str, Assumption] = {
    FA_A1: Assumption(
        id=FA_A1,
        statement=(
            "Author seat undeclared: cross-seat predicates accept any named "
            "reviewer seat (branch-prefix fallback is used for author "
            "inference)."
        ),
        relied_upon_by=(
            "snapshot_merge_queue.build_queue",
            "merge_queue_fairness.scan_queue",
        ),
        legacy_spellings=(
            "author seat undeclared; branch prefix fallback used",
            "author seat not declared (no 'Seat: Naya N' in PR body and "
            "no nayaN/ branch prefix); cross-seat predicates accept any "
            "named reviewer seat",
        ),
    ),
    FA_A2: Assumption(
        id=FA_A2,
        statement=(
            "Service deferred: the PR is queued behind another queue item "
            "(blocked_by) — legitimate queue ordering, not starvation; "
            "accrues no debt."
        ),
        relied_upon_by=("merge_queue_fairness.scan_queue",),
    ),
    FA_A3: Assumption(
        id=FA_A3,
        statement=(
            "Service deferred: the PR is parked awaiting Shawn's word (the "
            "human gate) — not starvation; accrues no debt."
        ),
        relied_upon_by=("merge_queue_fairness.scan_queue",),
    ),
    FA_A4: Assumption(
        id=FA_A4,
        statement=(
            "ready_since unprovable from evidence timestamps: the debt bound "
            "is widened per the missing-evidence rule and no debt accrues; "
            "unknown is unknown."
        ),
        relied_upon_by=("merge_queue_fairness.scan_queue",),
    ),
}

# The assumption-guarantee boundary: guarantee id -> statement + the
# assumption ids it rests on. Empty rests_on = unconditional (enforced
# structurally, e.g. by __post_init__ or by construction).
BOUNDARY: Dict[str, Dict[str, object]] = {
    "FG-G1": {
        "statement": "No silent green: scanner errors exit 2, never 0.",
        "rests_on": (),
    },
    "FG-G2": {
        "statement": (
            "Unknown is unknown: missing evidence widens the debt bound; "
            "it never manufactures a violation and never manufactures a pass."
        ),
        "rests_on": (FA_A4,),
    },
    "FG-G3": {
        "statement": "Every verdict names one of D26's four explicit levels.",
        "rests_on": (),
    },
    "FG-G4": {
        "statement": (
            "The scheduler's claim is recorded but never trusted; evidence "
            "contradictions are named."
        ),
        "rests_on": (),
    },
    "FG-G5": {
        "statement": (
            "Debt accrues only for eligible, unblocked, unparked items whose "
            "ready_since is provable from evidence timestamps."
        ),
        "rests_on": (FA_A2, FA_A3),
    },
    "FG-G6": {
        "statement": (
            "Cross-seat predicates treat an undeclared author seat per the "
            "registered inference rule."
        ),
        "rests_on": (FA_A1,),
    },
}


def _legacy_map(assumptions: Dict[str, Assumption]) -> Dict[str, str]:
    m: Dict[str, str] = {}
    for aid, asm in assumptions.items():
        for spelling in asm.legacy_spellings:
            if spelling in m:
                raise BoundaryError(
                    f"legacy spelling {spelling!r} maps to both "
                    f"{m[spelling]!r} and {aid!r}")
            if spelling in assumptions:
                raise BoundaryError(
                    f"legacy spelling {spelling!r} collides with a "
                    f"canonical assumption id")
            m[spelling] = aid
    return m


_LEGACY: Dict[str, str] = _legacy_map(ASSUMPTIONS)


def _check_tables_closed(assumptions: Dict[str, Assumption],
                         boundary: Dict[str, Dict[str, object]]) -> Dict[str, object]:
    """Verify the boundary is closed. Raises BoundaryError on any defect."""
    for aid, asm in assumptions.items():
        if not isinstance(asm, Assumption):
            raise BoundaryError(f"{aid!r} is not an Assumption")
        if asm.id != aid:
            raise BoundaryError(
                f"registry key {aid!r} != assumption.id {asm.id!r}")
        if not asm.statement or len(asm.statement) < 20:
            raise BoundaryError(f"{aid}: statement too short to be a contract")
        if not asm.relied_upon_by:
            raise BoundaryError(
                f"{aid}: no relying component — dead registry entry")
    relied_on = set()
    for gid, g in boundary.items():
        stmt = g.get("statement")
        rests = g.get("rests_on")
        if not stmt or not isinstance(rests, tuple):
            raise BoundaryError(f"{gid}: malformed boundary entry")
        for aid in rests:
            if aid not in assumptions:
                raise BoundaryError(
                    f"guarantee {gid} rests on unregistered assumption {aid!r}")
            relied_on.add(aid)
    orphaned = set(assumptions) - relied_on
    if orphaned:
        raise BoundaryError(
            f"assumptions relied on by no guarantee: {sorted(orphaned)}")
    return {"closed": True, "guarantees": len(boundary),
            "assumptions": len(assumptions)}


def check_boundary() -> Dict[str, object]:
    """Check the canonical tables. Raises BoundaryError on any defect."""
    return _check_tables_closed(ASSUMPTIONS, BOUNDARY)


def resolve(ref: object) -> Assumption:
    """Resolve an assumption id or legacy spelling to its registration.

    Fail-closed: unknown, empty, or non-string refs raise
    UnknownAssumptionError. Never returns a default.
    """
    if not isinstance(ref, str) or not ref:
        raise UnknownAssumptionError(f"unresolvable assumption ref: {ref!r}")
    if ref in ASSUMPTIONS:
        return ASSUMPTIONS[ref]
    aid = _LEGACY.get(ref)
    if aid is not None:
        return ASSUMPTIONS[aid]
    raise UnknownAssumptionError(
        f"unregistered assumption {ref!r}: register it in "
        f"fairness_assumptions.py before any verdict may rest on it")


def register_assumption(asm: Assumption) -> Assumption:
    """Register a new assumption. Duplicate ids raise BoundaryError.

    The canonical registry is append-only in practice: Assumption is frozen,
    so changing a meaning means a new id. A rejected duplicate never mutates
    the registry.
    """
    if not isinstance(asm, Assumption):
        raise BoundaryError(f"not an Assumption: {asm!r}")
    if asm.id in ASSUMPTIONS:
        raise BoundaryError(f"duplicate assumption id: {asm.id!r}")
    ASSUMPTIONS[asm.id] = asm
    global _LEGACY
    _LEGACY = _legacy_map(ASSUMPTIONS)
    check_boundary()  # the new entry must keep the boundary closed
    return asm


def guarantees_resting_on(assumption_id: str) -> List[str]:
    """Guarantee ids whose rests_on names the assumption. Fail-closed."""
    resolve(assumption_id)  # unknown id -> UnknownAssumptionError
    return [gid for gid, g in BOUNDARY.items()
            if assumption_id in g["rests_on"]]


# Import-time self-check: a broken boundary fails at import, never ships
# silently. This is the D27 enforcement point for the registry itself.
check_boundary()
