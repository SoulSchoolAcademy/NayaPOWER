#!/usr/bin/env python3
"""Work-honesty tracker (UD-08): authorized work must actually move, and every
progress claim must be honest. No motion mistaken for movement.

State machine per work item:
    AUTHORIZED -> IN_PROGRESS -> CLAIMED_DONE -> VERIFIED_DONE
    any live state -> BLOCKED -> IN_PROGRESS   (on unblock with evidence)

STALLED / STARVED / UNVERIFIED_CLAIM / DEADLOCK_CYCLE / LIVELOCK_SUSPECT are
computed audit flags, never worker-set states. A correct refusal (BLOCKED) is
never a stall, and WAITING_AUTHORITY is never reclassified as COMPLETED.

Every transition requires evidence. Activity alone earns no progress credit:
only obligation-state changes backed by artifacts or verifications count.
A thousand logged actions with no discharged obligation is zero progress.

Independence (UD-02 principle, enforced inline): the verifier's identity
(seat AND session) must differ from the doer's. Self-verification is refused
structurally, not by policy text.

DOES NOT CLAIM:
  - This does not detect collusion between distinct seats/sessions (no
    back-channel detection); it judges declared identity, not intent.
  - This does not schedule work or prove scheduler fairness properties; it
    tracks item-level honesty (states, evidence, stalls, deadlock cycles).
    The full D22-D28 fairness machinery (model checker, assumption audit)
    is explicitly out of scope for this module.
  - Timestamps are supplied by the caller (injectable clock for tests); this
    module does not secure time.

Stdlib only.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

# ---------------------------------------------------------------- states ---
AUTHORIZED = "AUTHORIZED"
IN_PROGRESS = "IN_PROGRESS"
CLAIMED_DONE = "CLAIMED_DONE"
VERIFIED_DONE = "VERIFIED_DONE"
BLOCKED = "BLOCKED"

TERMINAL = {VERIFIED_DONE}
LIVE = {AUTHORIZED, IN_PROGRESS, CLAIMED_DONE, BLOCKED}

# --------------------------------------------------------------- evidence ---
AUTHORIZATION = "AUTHORIZATION"
START = "START"
ARTIFACT = "ARTIFACT"
VERIFICATION = "VERIFICATION"
BLOCKER = "BLOCKER"
UNBLOCK = "UNBLOCK"
NOTE = "NOTE"  # earns nothing; activity theater detector ignores it too

# ---------------------------------------------------------- refusal codes ---
NO_AUTHORITY = "NO_AUTHORITY"
NO_START_EVIDENCE = "NO_START_EVIDENCE"
NO_ARTIFACT = "NO_ARTIFACT"
SELF_VERIFICATION = "SELF_VERIFICATION"
NO_VERIFICATION_EVIDENCE = "NO_VERIFICATION_EVIDENCE"
NO_BLOCKER_RECORD = "NO_BLOCKER_RECORD"
NO_UNBLOCK_EVIDENCE = "NO_UNBLOCK_EVIDENCE"
BLOCKED_CANNOT_COMPLETE = "BLOCKED_CANNOT_COMPLETE"
INVALID_TRANSITION = "INVALID_TRANSITION"
UNKNOWN_ITEM = "UNKNOWN_ITEM"
TERMINAL_STATE = "TERMINAL_STATE"


class TransitionRefused(Exception):
    """Raised whenever a state transition is refused, with a machine-readable
    reason code. A refusal is a verdict, not an exception to hide."""

    def __init__(self, code: str, detail: str = ""):
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.detail = detail


@dataclass
class Identity:
    seat: str
    session: str

    def same_agent_as(self, other: "Identity") -> bool:
        # Same seat, or same session under a renamed seat: not independent.
        return self.seat == other.seat or self.session == other.session


@dataclass
class Evidence:
    kind: str
    at: float
    by: Optional[Identity] = None
    detail: str = ""
    artifact_handle: Optional[str] = None   # content hash / pointer
    artifact_pointer: Optional[str] = None  # where the artifact lives
    verdict: Optional[str] = None           # PASS / FAIL for VERIFICATION
    blocked_by_item: Optional[str] = None   # for BLOCKER: waits-for edge


@dataclass
class WorkItem:
    item_id: str
    title: str
    state: str = AUTHORIZED
    doer: Optional[Identity] = None
    authority: str = ""
    evidence: List[Evidence] = field(default_factory=list)
    transitions: List[Tuple[str, str, float]] = field(default_factory=list)
    # (from_state, to_state, at) — the ONLY progress record. Activity logs
    # alone never appear here.
    selections: int = 0          # times chosen for service (fairness input)
    failed_verifications: int = 0
    last_evidence_at: float = 0.0
    blocker_detail: str = ""


class WorkHonestyTracker:
    """Tracks authorized work items with evidence-gated transitions."""

    def __init__(self, clock=None):
        self._items: Dict[str, WorkItem] = {}
        self._clock = clock or time.time
        self.ledger: List[Dict[str, Any]] = []  # append-only transition log

    # ------------------------------------------------------------ helpers ---
    def _now(self) -> float:
        return self._clock()

    def _get(self, item_id: str) -> WorkItem:
        try:
            return self._items[item_id]
        except KeyError:
            raise TransitionRefused(UNKNOWN_ITEM, f"no such item: {item_id}")

    def _record(self, item: WorkItem, frm: str, to: str, ev: Evidence):
        at = self._now()
        ev.at = at
        item.evidence.append(ev)
        item.transitions.append((frm, to, at))
        item.last_evidence_at = at
        self.ledger.append({
            "item": item.item_id, "from": frm, "to": to, "at": at,
            "kind": ev.kind,
            "by": f"{ev.by.seat}/{ev.by.session}" if ev.by else None,
        })
        item.state = to

    def _note(self, item: WorkItem, ev: Evidence):
        # Activity without a state change: logged, earns zero progress credit.
        ev.at = self._now()
        item.evidence.append(ev)
        item.last_evidence_at = ev.at

    # ---------------------------------------------------------- lifecycle ---
    def authorize(self, item_id: str, title: str, authority: str,
                  by: Identity) -> WorkItem:
        if not authority:
            raise TransitionRefused(NO_AUTHORITY, "authorization needs a source")
        item = WorkItem(item_id=item_id, title=title, authority=authority)
        now = self._now()
        item.last_evidence_at = now
        item.evidence.append(Evidence(AUTHORIZATION, now, by,
                                     f"authorized under {authority}"))
        self._items[item_id] = item
        self.ledger.append({"item": item_id, "from": None, "to": AUTHORIZED,
                            "at": now, "kind": AUTHORIZATION,
                            "by": f"{by.seat}/{by.session}"})
        return item

    def start(self, item_id: str, doer: Identity, first_action: str) -> WorkItem:
        item = self._get(item_id)
        if item.state != AUTHORIZED:
            raise TransitionRefused(INVALID_TRANSITION,
                                    f"start requires AUTHORIZED, is {item.state}")
        if not first_action.strip():
            raise TransitionRefused(NO_START_EVIDENCE,
                                    "starting needs a first action, not a pulse")
        item.doer = doer
        self._record(item, AUTHORIZED, IN_PROGRESS,
                     Evidence(START, 0, doer, first_action))
        return item

    def heartbeat(self, item_id: str, by: Identity, note: str = ""):
        # Explicitly earns NOTHING. A heartbeat is not proof of anything.
        item = self._get(item_id)
        self._note(item, Evidence(NOTE, 0, by, note or "heartbeat"))

    def claim_done(self, item_id: str, by: Identity, artifact_handle: str,
                   artifact_pointer: str = "") -> WorkItem:
        item = self._get(item_id)
        if item.state == BLOCKED:
            raise TransitionRefused(BLOCKED_CANNOT_COMPLETE,
                                    "blocked work cannot be marked done; unblock first")
        if item.state != IN_PROGRESS:
            raise TransitionRefused(INVALID_TRANSITION,
                                    f"claim_done requires IN_PROGRESS, is {item.state}")
        if not artifact_handle or not artifact_handle.strip():
            raise TransitionRefused(NO_ARTIFACT,
                                    "a done-claim without the artifact is refused")
        self._record(item, IN_PROGRESS, CLAIMED_DONE,
                     Evidence(ARTIFACT, 0, by, "done claimed",
                              artifact_handle=artifact_handle,
                              artifact_pointer=artifact_pointer))
        return item

    def verify(self, item_id: str, verifier: Identity, verdict: str,
               evidence_detail: str = "") -> WorkItem:
        item = self._get(item_id)
        if item.state != CLAIMED_DONE:
            raise TransitionRefused(INVALID_TRANSITION,
                                    f"verify requires CLAIMED_DONE, is {item.state}")
        if item.doer is not None and verifier.same_agent_as(item.doer):
            raise TransitionRefused(SELF_VERIFICATION,
                                    f"verifier {verifier.seat}/{verifier.session} "
                                    f"is not independent of doer "
                                    f"{item.doer.seat}/{item.doer.session}")
        if not evidence_detail.strip():
            raise TransitionRefused(NO_VERIFICATION_EVIDENCE,
                                    "a verdict without verification evidence is refused")
        verdict = verdict.upper()
        if verdict == "PASS":
            self._record(item, CLAIMED_DONE, VERIFIED_DONE,
                         Evidence(VERIFICATION, 0, verifier, evidence_detail,
                                  verdict="PASS"))
        elif verdict == "FAIL":
            item.failed_verifications += 1
            self._record(item, CLAIMED_DONE, IN_PROGRESS,
                         Evidence(VERIFICATION, 0, verifier, evidence_detail,
                                  verdict="FAIL"))
        else:
            raise TransitionRefused(INVALID_TRANSITION,
                                    f"verdict must be PASS or FAIL, got {verdict!r}")
        return item

    def block(self, item_id: str, by: Identity, blocker_detail: str,
              owner: str = "", blocked_by_item: Optional[str] = None) -> WorkItem:
        item = self._get(item_id)
        if item.state == VERIFIED_DONE:
            raise TransitionRefused(TERMINAL_STATE, "verified work is terminal")
        if not blocker_detail.strip():
            raise TransitionRefused(NO_BLOCKER_RECORD,
                                    "blocking needs a named blocker and owner")
        item.blocker_detail = blocker_detail
        self._record(item, item.state, BLOCKED,
                     Evidence(BLOCKER, 0, by,
                              f"blocked: {blocker_detail} (owner: {owner or 'unassigned'})",
                              blocked_by_item=blocked_by_item))
        return item

    def unblock(self, item_id: str, by: Identity, unblock_evidence: str) -> WorkItem:
        item = self._get(item_id)
        if item.state != BLOCKED:
            raise TransitionRefused(INVALID_TRANSITION,
                                    f"unblock requires BLOCKED, is {item.state}")
        if not unblock_evidence.strip():
            raise TransitionRefused(NO_UNBLOCK_EVIDENCE,
                                    "unblocking needs evidence the blocker is gone")
        item.blocker_detail = ""
        self._record(item, BLOCKED, IN_PROGRESS,
                     Evidence(UNBLOCK, 0, by, unblock_evidence))
        return item

    def record_selection(self, item_id: str):
        # Fairness input: the item was chosen for service. Reported
        # independently from progress; selections earn no proof credit.
        self._get(item_id).selections += 1

    # --------------------------------------------------------------- audit ---
    def progress_credit(self, item_id: str) -> int:
        """Forward state changes only. Activity, heartbeats, and notes count
        for exactly zero."""
        item = self._get(item_id)
        forward = {(AUTHORIZED, IN_PROGRESS), (IN_PROGRESS, CLAIMED_DONE),
                   (CLAIMED_DONE, VERIFIED_DONE), (BLOCKED, IN_PROGRESS)}
        return sum(1 for frm, to, _ in item.transitions if (frm, to) in forward)

    def audit(self, stall_window_s: float = 86400.0,
              starve_window_s: float = 172800.0,
              livelock_threshold: int = 3) -> Dict[str, Any]:
        """Independent audit. Returns progress and fairness as separate
        sections — a fair scheduler with broken workers and a broken
        scheduler with lucky workers must not be confusable."""
        now = self._now()
        progress, fairness, flags = [], [], {}

        # Deadlock: cycle in the waits-for graph built from BLOCKER evidence.
        waits: Dict[str, str] = {}
        for item in self._items.values():
            if item.state == BLOCKED:
                for ev in reversed(item.evidence):
                    if ev.kind == BLOCKER and ev.blocked_by_item:
                        if ev.blocked_by_item in self._items:
                            waits[item.item_id] = ev.blocked_by_item
                        break
        deadlocked = self._find_cycle(waits)

        for item in self._items.values():
            age = now - item.last_evidence_at
            item_flags: List[str] = []
            if item.state == IN_PROGRESS and age > stall_window_s:
                item_flags.append("STALLED")
            if item.state == AUTHORIZED and age > starve_window_s:
                item_flags.append("STARVED")
            if item.state == CLAIMED_DONE and age > stall_window_s:
                item_flags.append("UNVERIFIED_CLAIM")
            if item.item_id in deadlocked:
                item_flags.append("DEADLOCK_CYCLE")
            if item.failed_verifications >= livelock_threshold:
                item_flags.append("LIVELOCK_SUSPECT")
            # BLOCKED is never STALLED: a correct refusal is not a stall.
            if item_flags:
                flags[item.item_id] = item_flags
            progress.append({
                "item": item.item_id, "state": item.state,
                "progress_credit": self.progress_credit(item.item_id),
                "transitions": len(item.transitions),
                "evidence_age_s": round(age, 1),
            })
            fairness.append({
                "item": item.item_id,
                "selections": item.selections,
                "advancements": self.progress_credit(item.item_id),
                # selections and advancements reported side by side, never
                # merged: service opportunity is not progress.
            })

        return {"at": now, "progress": progress, "fairness": fairness,
                "flags": flags,
                "does_not_claim": (
                    "STALLED/STARVED are evidence-age heuristics, not proof of "
                    "fault. DEADLOCK_CYCLE covers item-level waits-for edges only. "
                    "LIVELOCK_SUSPECT is a threshold trip, not a diagnosis.")}

    @staticmethod
    def _find_cycle(waits: Dict[str, str]) -> List[str]:
        seen_in_cycle: List[str] = []
        for start in waits:
            path, cur = [], start
            while cur in waits and cur not in path:
                path.append(cur)
                cur = waits[cur]
            if cur in path:
                cyc = path[path.index(cur):]
                for node in cyc:
                    if node not in seen_in_cycle:
                        seen_in_cycle.append(node)
        return seen_in_cycle
