#!/usr/bin/env python3
"""D55 — Safe Recovery Holds vs. Liveness Failures (AER-LIVE-001).

Canonical rule: never classify a legitimately prohibited action as a liveness
failure just because it stays blocked. Classify safety and liveness
independently. Every recovery obligation separately establishes eligibility,
usable service, and independently verified progress — or a governed
disposition. Escalation changes who investigates; it never changes the safety
predicate, never manufactures authority, and never manufactures proof.

The tri-fact (E_o / S_o / P_o), tracked as three separate facts:
  enabled    (E_o) — legally permitted to execute (authorization granted)
  serviced   (S_o) — the scheduler gave the obligation attention
  progressed (P_o) — verifiable state advance

A heartbeat is service, never progress: heartbeats set S_o only. P_o is
established exclusively by progress events carrying verifiable state advance.

Vocabulary aligned with SN-0807 / AER-LIVE-1 (prior art on the held #2161
branch — branch-state, cited as input, not a second live mechanism).

Directive: D55, wave 5, owner naya2. Source: issue comment 6102257048.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Callable, Dict, List, Optional


# ---------------------------------------------------------------------------
# Event model: service signals and progress evidence are different types.
# ---------------------------------------------------------------------------

SERVICE = "service"    # scheduler attention: heartbeats, worker polls, retries
PROGRESS = "progress"  # verifiable state advance: projection moved, replay applied


@dataclass
class Event:
    kind: str  # SERVICE | PROGRESS
    detail: str = ""


@dataclass
class Obligation:
    """One recovery obligation under governance."""
    name: str
    auth: "AuthState"
    events: List[Event] = field(default_factory=list)
    # The authorized repair/reconciliation task governed alongside this one.
    reconciliation: Optional["Obligation"] = None
    responsible: str = "unassigned"
    disposition: Optional["ValidDisposition"] = None


class AuthState(str, Enum):
    WITHDRAWN = "withdrawn"              # legitimately prohibited — hold is correct
    GRANTED = "granted"                  # permitted to execute
    MISSING_DECISION = "missing_decision"  # no LAW decision exists yet


class Classification(str, Enum):
    HEALTHY = "healthy"
    # Correct hold. NOT a liveness failure, NOT starvation.
    VALID_HOLD = "valid_hold"
    # Genuine recovery failure: serviced, never progressed.
    RECOVERY_DEFECT = "recovery_defect"
    # Missing LAW decision: waiting on authority — never starvation.
    WAITING_AUTHORITY = "waiting_authority"
    # Permitted and runnable, but the scheduler never gave it attention.
    SCHEDULER_DEFECT = "scheduler_defect"


@dataclass(frozen=True)
class TriFact:
    enabled: bool     # E_o
    serviced: bool    # S_o
    progressed: bool  # P_o


@dataclass
class ValidDisposition:
    """Terminal dispositions require evidence or an explicit reason.

    Mirrors the learning-envelope NONE_WITH_REASON contract: a disposition
    with neither evidence nor reason is not a governed disposition.
    """
    disposition: str
    evidence: str = ""
    reason: str = ""

    def is_valid(self) -> bool:
        return bool(self.evidence.strip() or self.reason.strip())


@dataclass
class Diagnosis:
    obligation: str
    classification: Classification
    tri_fact: TriFact
    auth: AuthState
    # True when the hold is valid AND the authorized reconciliation task sits
    # runnable and ignored — the directive's "scheduler needs investigation".
    scheduler_defect: bool = False
    note: str = ""


# ---------------------------------------------------------------------------
# Tri-fact derivation and classification
# ---------------------------------------------------------------------------

def trifacts(ob: Obligation) -> TriFact:
    """Derive E_o/S_o/P_o. Progress events are the ONLY source of P_o."""
    return TriFact(
        enabled=ob.auth == AuthState.GRANTED,
        serviced=any(e.kind == SERVICE for e in ob.events),
        progressed=any(e.kind == PROGRESS for e in ob.events),
    )


def classify(ob: Obligation) -> Diagnosis:
    """Classify safety and liveness independently for one obligation."""
    tf = trifacts(ob)

    if ob.auth == AuthState.MISSING_DECISION:
        # A task that cannot legally execute is not starved — it waits.
        return Diagnosis(ob.name, Classification.WAITING_AUTHORITY, tf,
                         ob.auth, note="missing LAW decision; not starvation")

    if ob.auth == AuthState.WITHDRAWN:
        # Legitimately prohibited: the hold is correct. This is never a
        # liveness failure and never starvation — but the hold does not excuse
        # ignoring an authorized, runnable reconciliation task.
        sched_defect = False
        note = "authorization withdrawn; hold is valid"
        rec = ob.reconciliation
        if rec is not None:
            rtf = trifacts(rec)
            if rtf.enabled and not rtf.serviced:
                sched_defect = True
                note += "; authorized reconciliation runnable and ignored"
        return Diagnosis(ob.name, Classification.VALID_HOLD, tf,
                         ob.auth, scheduler_defect=sched_defect, note=note)

    # GRANTED
    if tf.progressed:
        return Diagnosis(ob.name, Classification.HEALTHY, tf, ob.auth,
                         note="verifiable state advance observed")
    if tf.serviced:
        # Served repeatedly, never advanced: genuine recovery defect.
        return Diagnosis(ob.name, Classification.RECOVERY_DEFECT, tf, ob.auth,
                         note="serviced without progress")
    return Diagnosis(ob.name, Classification.SCHEDULER_DEFECT, tf, ob.auth,
                     note="permitted and runnable, never serviced")


def escalate(diag: Diagnosis, new_responsible: str) -> Diagnosis:
    """Escalation changes who investigates — never the safety predicate.

    The authorization state, classification, and tri-fact are immutable under
    escalation. Returns a new Diagnosis; the input is untouched.
    """
    out = Diagnosis(
        obligation=diag.obligation,
        classification=diag.classification,
        tri_fact=diag.tri_fact,
        auth=diag.auth,
        scheduler_defect=diag.scheduler_defect,
        note=diag.note + f" [escalated to {new_responsible}]",
    )
    return out


# ---------------------------------------------------------------------------
# AER-LIVE-001: the directive's three-history experiment
# ---------------------------------------------------------------------------
#
# H1 control   — outbox event applies cleanly; reconciliation progressed.
# H2 defective  — worker served repeatedly, projection never advances.
# H3 missing    — genuinely missing LAW decision.
#
# In all three, the prohibited retry's authorization stays WITHDRAWN; the
# verifier must show it. Only H2 fails the progress requirement. H3 classifies
# as waiting-authority — not starvation.

def _history_control() -> List[Obligation]:
    retry = Obligation(
        name="retry-blocked-action", auth=AuthState.WITHDRAWN,
        events=[Event(SERVICE, "hold re-evaluated")],
        responsible="ops",
        disposition=ValidDisposition("held", evidence="LAW decision L-118 prohibits retry during incident"),
    )
    repair = Obligation(
        name="reconciliation-task", auth=AuthState.GRANTED,
        events=[Event(SERVICE, "worker poll"), Event(PROGRESS, "outbox event applied; projection advanced to v42")],
        responsible="ops",
        disposition=ValidDisposition("completed", evidence="projection v42 == authoritative source"),
    )
    retry.reconciliation = repair
    return [retry, repair]


def _history_defective() -> List[Obligation]:
    # The directive's three-simultaneous-truths case:
    #  (1) the retry is correctly blocked (valid hold);
    #  (2) the authorized reconciliation task sits runnable and ignored;
    #  (3) the committed publication's replay is repeatedly lost.
    retry = Obligation(
        name="retry-blocked-action", auth=AuthState.WITHDRAWN,
        events=[Event(SERVICE, "hold re-evaluated")],
        responsible="ops",
        disposition=ValidDisposition("held", evidence="LAW decision L-118 prohibits retry during incident"),
    )
    repair = Obligation(
        name="reconciliation-task", auth=AuthState.GRANTED,
        events=[],  # runnable, ignored: zero service events
        responsible="ops",
        disposition=ValidDisposition("pending", reason="awaiting scheduler attention; hold remains valid"),
    )
    publication = Obligation(
        name="committed-publication-replay", auth=AuthState.GRANTED,
        events=[Event(SERVICE, f"worker poll #{i} (heartbeat only)") for i in range(1, 6)],
        responsible="ops",
        disposition=ValidDisposition("defective", evidence="5 service rounds, projection stuck at v41"),
    )
    retry.reconciliation = repair
    return [retry, repair, publication]


def _history_missing_decision() -> List[Obligation]:
    retry = Obligation(
        name="retry-blocked-action", auth=AuthState.WITHDRAWN,
        events=[Event(SERVICE, "hold re-evaluated")],
        responsible="ops",
        disposition=ValidDisposition("held", evidence="LAW decision L-118 prohibits retry during incident"),
    )
    repair = Obligation(
        name="reconciliation-task", auth=AuthState.MISSING_DECISION,
        events=[],
        responsible="ops",
        disposition=ValidDisposition("waiting", reason="no LAW decision exists for this repair path"),
    )
    retry.reconciliation = repair
    return [retry, repair]


HISTORIES: Dict[str, Callable[[], List[Obligation]]] = {
    "H1": _history_control,
    "H2": _history_defective,
    "H3": _history_missing_decision,
}

# The directive names each history's primary obligation for acceptance.
PRIMARY = {"H1": "reconciliation-task", "H2": "committed-publication-replay",
           "H3": "reconciliation-task"}


@dataclass
class HistoryVerdict:
    history_id: str
    diagnoses: List[Diagnosis]
    authorization_proof: Dict[str, str]  # obligation -> auth state, verbatim
    primary: str


def run_history(history_id: str,
                classifier: Callable[[Obligation], Diagnosis] = classify
                ) -> HistoryVerdict:
    obligations = HISTORIES[history_id]()
    diagnoses = [classifier(ob) for ob in obligations]
    proof = {ob.name: ob.auth.value for ob in obligations}
    return HistoryVerdict(history_id, diagnoses, proof, PRIMARY[history_id])


def run_aer_live_001(
        classifier: Callable[[Obligation], Diagnosis] = classify
) -> Dict[str, HistoryVerdict]:
    return {hid: run_history(hid, classifier) for hid in ("H1", "H2", "H3")}


def _diag(verdict: HistoryVerdict, name: str) -> Diagnosis:
    for d in verdict.diagnoses:
        if d.obligation == name:
            return d
    raise KeyError(name)


def verify_aer_live_001(
        results: Dict[str, HistoryVerdict],
        classifier: Callable[[Obligation], Diagnosis] = classify,
) -> List[str]:
    """Verify the directive's acceptance criteria. Empty list = PASS."""
    violations: List[str] = []

    for hid in ("H1", "H2", "H3"):
        if hid not in results:
            violations.append(f"missing history {hid}")
    if violations:
        return violations

    # (1) The authorization stays withdrawn in all three histories: no history
    # may manufacture authority. GRANTED anywhere in the proof is a violation —
    # and a missing proof is a violation too (the verifier must SHOW it).
    for hid, v in results.items():
        proof = v.authorization_proof
        if "retry-blocked-action" not in proof:
            violations.append(f"{hid}: authorization proof missing for retry-blocked-action")
            continue
        for name, auth in proof.items():
            if auth == AuthState.GRANTED.value and name == "retry-blocked-action":
                violations.append(f"{hid}: prohibited action shows GRANTED — authority manufactured")

    # (2) Control is healthy.
    if _diag(results["H1"], "reconciliation-task").classification != Classification.HEALTHY:
        violations.append("H1: control reconciliation-task is not HEALTHY")

    # (3) Only the defective history fails the progress requirement.
    h2_primary = _diag(results["H2"], "committed-publication-replay").classification
    if h2_primary != Classification.RECOVERY_DEFECT:
        violations.append(f"H2: defective publication is {h2_primary}, not RECOVERY_DEFECT")
    for hid, pname in (("H1", "reconciliation-task"), ("H3", "reconciliation-task")):
        if _diag(results[hid], pname).classification == Classification.RECOVERY_DEFECT:
            violations.append(f"{hid}: non-defective history wrongly classified RECOVERY_DEFECT")

    # (4) Missing decision classifies as waiting-authority — not starvation.
    h3_cls = _diag(results["H3"], "reconciliation-task").classification
    if h3_cls != Classification.WAITING_AUTHORITY:
        violations.append(f"H3: missing decision is {h3_cls}, not WAITING_AUTHORITY")

    # (5) Three simultaneous truths visible in H2: valid hold on the retry,
    # scheduler defect flagged on the ignored reconciliation, recovery defect
    # on the publication — independently classified, none collapsed together.
    h2_retry = _diag(results["H2"], "retry-blocked-action")
    if h2_retry.classification != Classification.VALID_HOLD:
        violations.append(f"H2: retry is {h2_retry.classification}, not VALID_HOLD")
    if not h2_retry.scheduler_defect:
        violations.append("H2: ignored runnable reconciliation not flagged (scheduler_defect)")
    if _diag(results["H2"], "reconciliation-task").classification != Classification.SCHEDULER_DEFECT:
        violations.append("H2: ignored reconciliation not classified SCHEDULER_DEFECT")

    # (6) Heartbeat-only service never counts as progress: any obligation with
    # zero PROGRESS events must not classify HEALTHY under the real classifier.
    if classifier is classify:
        for hid, v in results.items():
            for d in v.diagnoses:
                if d.classification == Classification.HEALTHY and not d.tri_fact.progressed:
                    violations.append(f"{hid}/{d.obligation}: HEALTHY without P_o — heartbeat fraud")

    # (7) ValidDisposition contract: terminal dispositions carry evidence or
    # an explicit reason. (Checked against the fixture obligations.)
    for hid in ("H1", "H2", "H3"):
        for ob in HISTORIES[hid]():
            if ob.disposition is not None and not ob.disposition.is_valid():
                violations.append(f"{hid}/{ob.name}: disposition lacks evidence and reason")

    return violations


# ---------------------------------------------------------------------------
# Machine-readable output + CLI
# ---------------------------------------------------------------------------

def _jsonable(obj: Any) -> Any:
    if isinstance(obj, Enum):
        return obj.value
    if isinstance(obj, (Diagnosis, TriFact, HistoryVerdict, Event, ValidDisposition)):
        d = asdict(obj)
        return {k: _jsonable(v) for k, v in d.items()}
    if isinstance(obj, dict):
        return {k: _jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_jsonable(v) for v in obj]
    return obj


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="D55 safety/liveness classifier + AER-LIVE-001")
    ap.add_argument("--run-experiment", action="store_true",
                    help="run AER-LIVE-001 and verify; exit 2 on failure")
    ap.add_argument("--history", choices=["H1", "H2", "H3"],
                    help="print one history's verdict as JSON")
    ap.add_argument("--verify", action="store_true",
                    help="verify AER-LIVE-001 and print violations")
    args = ap.parse_args(argv)

    if args.history:
        print(json.dumps(_jsonable(run_history(args.history)), indent=2))
        return 0

    results = run_aer_live_001()
    violations = verify_aer_live_001(results)

    if args.verify or args.run_experiment:
        payload = {
            "experiment": "AER-LIVE-001",
            "directive": "D55",
            "verdicts": {hid: _jsonable(v) for hid, v in results.items()},
            "violations": violations,
            "pass": not violations,
        }
        print(json.dumps(payload, indent=2))
        return 0 if not violations else 2

    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
