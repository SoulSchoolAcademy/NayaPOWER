"""UD-03 — CHANGING OUR MIND TAKES EVIDENCE AND GUARDS.

What we believe can change — but never silently, never cheaply, and never
from thin evidence. A settled interpretation stays settled until real new
evidence challenges it, and the challenge travels a versioned path:
challenged -> reopened -> requalified (or returned to unresolved), with
history intact and unaffected work continuing.

Three thresholds govern the path (easy to listen, hard to change truth,
quick to protect people):
  LISTEN          low bar  — new evidence is noted and may open a challenge.
  CHANGE_TRUTH    high bar — only strong evidence rewrites a settled belief.
  PROTECT_PEOPLE  low bar  — harm-suggesting evidence triggers protective
                  action quickly, even before truth changes.

Every threshold is bound to the policy/model/evaluator/environment it was
qualified under. When that context drifts, thresholds must be requalified
before consequential reliance — the ledger refuses otherwise.

Uncertainty-interval arithmetic: confidence is an interval [lo, hi].
Absence of observed harm never counts as proof of safety — it moves no
bound toward "safe".

Evidence is append-only: contradicting evidence is recorded, never deleted.
A belief is never rewritten in place; it is superseded by a new version
that cites the evidence that caused the change.

Stdlib only. No I/O, no network.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib
import json
from typing import Dict, List, Optional, Sequence, Tuple


# ---------------------------------------------------------------------------
# Refusals
# ---------------------------------------------------------------------------

class Refusal(Exception):
    """A refused belief-ledger operation. The code is machine-readable."""

    def __init__(self, code: str, detail: str = ""):
        self.code = code
        self.detail = detail
        super().__init__(f"{code}: {detail}" if detail else code)


NO_EVIDENCE = "NO_EVIDENCE"
WEAK_EVIDENCE = "WEAK_EVIDENCE"
EVIDENCE_IMMUTABLE = "EVIDENCE_IMMUTABLE"
CONFIDENCE_EXCEEDS_EVIDENCE = "CONFIDENCE_EXCEEDS_EVIDENCE"
DRIFT_UNREQUALIFIED = "DRIFT_UNREQUALIFIED"
SAFETY_FROM_ABSENCE = "SAFETY_FROM_ABSENCE"
SILENT_REWRITE = "SILENT_REWRITE"


# ---------------------------------------------------------------------------
# Core records (frozen: the ledger is append-only)
# ---------------------------------------------------------------------------

SUPPORTS = "SUPPORTS"
REFUTES = "REFUTES"

SETTLED = "SETTLED"
CHALLENGED = "CHALLENGED"
REOPENED = "REOPENED"
REQUALIFIED = "REQUALIFIED"
UNRESOLVED = "UNRESOLVED"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _hash(payload: str) -> str:
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


@dataclass(frozen=True)
class Evidence:
    """One recorded observation. Immutable once recorded; never deleted."""
    id: str
    statement: str
    weight: float          # 0..1 — strength of this evidence
    source: str
    direction: str         # SUPPORTS or REFUTES (relative to a belief version)
    recorded_at: str = field(default_factory=_now)

    def __post_init__(self):
        if not (0.0 <= self.weight <= 1.0):
            raise ValueError(f"weight must be 0..1, got {self.weight}")
        if self.direction not in (SUPPORTS, REFUTES):
            raise ValueError(f"direction must be SUPPORTS/REFUTES, got {self.direction}")


@dataclass(frozen=True)
class BeliefVersion:
    """One version of a belief's interpretation. Never mutated in place."""
    n: int
    interpretation: str
    evidence_ids: Tuple[str, ...]
    conf_lo: float
    conf_hi: float
    prev_hash: str
    caused_by: str         # receipt id of the transition that created it
    created_at: str = field(default_factory=_now)

    @property
    def version_hash(self) -> str:
        return _hash(json.dumps({
            "n": self.n, "interpretation": self.interpretation,
            "evidence": sorted(self.evidence_ids),
            "conf": [self.conf_lo, self.conf_hi],
            "prev": self.prev_hash, "cause": self.caused_by,
        }, sort_keys=True))


@dataclass(frozen=True)
class Receipt:
    """Immutable record of one ledger transition."""
    id: str
    belief_id: str
    transition: str        # e.g. "SETTLED->CHALLENGED"
    evidence_ids: Tuple[str, ...]
    reason: str
    at: str = field(default_factory=_now)


@dataclass(frozen=True)
class ContextFingerprint:
    """What the thresholds were qualified under."""
    policy: str
    model: str
    evaluator: str
    environment: str

    def digest(self) -> str:
        return _hash("|".join([self.policy, self.model, self.evaluator, self.environment]))


# ---------------------------------------------------------------------------
# Uncertainty-interval arithmetic
# ---------------------------------------------------------------------------

def max_supported_confidence(supporting_weights: Sequence[float]) -> float:
    """Noisy-OR cap: confidence can never exceed what the evidence supports.

    One strong source (0.9) supports 0.9. Two independent 0.5 sources
    support 0.75. Ten weak 0.1 sources support only 0.65 — quantity is not
    proof (UD-06 consonance).
    """
    cap = 1.0
    for w in supporting_weights:
        cap *= (1.0 - w)
    return round(1.0 - cap, 6)


def confidence_interval(supporting: Sequence[float],
                        refuting: Sequence[float]) -> Tuple[float, float]:
    """[lo, hi] from the evidence. Absence of evidence moves nothing.

    lo rises only with supporting evidence; hi falls only with refuting
    evidence. A belief with no evidence at all sits at [0.0, 1.0]:
    total uncertainty, honestly stated.
    """
    lo = max_supported_confidence(supporting) if supporting else 0.0
    hi = 1.0 - max_supported_confidence(refuting) if refuting else 1.0
    lo, hi = round(lo, 6), round(hi, 6)
    if lo > hi:  # conflicting evidence: interval collapses to the conflict point
        mid = round((lo + hi) / 2, 6)
        return (mid, mid)
    return (lo, hi)


# ---------------------------------------------------------------------------
# The ledger
# ---------------------------------------------------------------------------

class BeliefLedger:
    """Append-only belief ledger with evidence-weighted updates."""

    def __init__(self,
                 listen: float = 0.25,
                 change_truth: float = 0.70,
                 protect_people: float = 0.30,
                 context: Optional[ContextFingerprint] = None):
        if not (0 <= listen < change_truth <= 1):
            raise ValueError("require 0 <= listen < change_truth <= 1")
        self._beliefs: Dict[str, dict] = {}
        self._evidence: Dict[str, Evidence] = {}
        self._receipts: List[Receipt] = []
        self._thresholds = {"listen": listen, "change_truth": change_truth,
                            "protect": protect_people}
        self._qualified_under = (context or ContextFingerprint(
            policy="default", model="default",
            evaluator="default", environment="default")).digest()
        self._requalified = True
        self._seq = 0

    # -- internal ---------------------------------------------------------
    def _next_id(self, prefix: str) -> str:
        self._seq += 1
        return f"{prefix}-{self._seq:04d}"

    def _receipt(self, belief_id: str, transition: str,
                 evidence_ids: Sequence[str], reason: str) -> Receipt:
        r = Receipt(id=self._next_id("rcpt"), belief_id=belief_id,
                    transition=transition, evidence_ids=tuple(evidence_ids),
                    reason=reason)
        self._receipts.append(r)
        return r

    def _belief(self, belief_id: str) -> dict:
        try:
            return self._beliefs[belief_id]
        except KeyError:
            raise Refusal("UNKNOWN_BELIEF", belief_id)

    def _check_requalified(self):
        if not self._requalified:
            raise Refusal(DRIFT_UNREQUALIFIED,
                          "context drifted; thresholds must be requalified "
                          "before consequential reliance")

    # -- beliefs ----------------------------------------------------------
    def register_belief(self, belief_id: str, interpretation: str,
                        evidence_ids: Sequence[str],
                        confidence: Optional[float] = None) -> str:
        """Register a new belief at version 1. Initial evidence required."""
        if belief_id in self._beliefs:
            raise Refusal("BELIEF_EXISTS", belief_id)
        if not evidence_ids:
            raise Refusal(NO_EVIDENCE, "a belief cannot be registered on no evidence")
        missing = [e for e in evidence_ids if e not in self._evidence]
        if missing:
            raise Refusal(NO_EVIDENCE, f"cites unrecorded evidence: {missing}")
        evs = [self._evidence[e] for e in evidence_ids]
        lo, hi = confidence_interval(
            [e.weight for e in evs if e.direction == SUPPORTS],
            [e.weight for e in evs if e.direction == REFUTES])
        cap = max_supported_confidence(
            [e.weight for e in evs if e.direction == SUPPORTS])
        if confidence is not None and confidence > cap + 1e-9:
            raise Refusal(CONFIDENCE_EXCEEDS_EVIDENCE,
                          f"claims {confidence} on evidence supporting {cap}")
        r = self._receipt(belief_id, "NONE->SETTLED", evidence_ids,
                          "initial registration")
        v = BeliefVersion(n=1, interpretation=interpretation,
                          evidence_ids=tuple(evidence_ids),
                          conf_lo=lo, conf_hi=hi, prev_hash="GENESIS",
                          caused_by=r.id)
        self._beliefs[belief_id] = {
            "versions": [v], "status": SETTLED,
            "applicable": {"version": 1, "context": self._qualified_under},
        }
        return v.version_hash

    # -- evidence (append-only) -------------------------------------------
    def record_evidence(self, statement: str, weight: float, source: str,
                        direction: str) -> str:
        ev = Evidence(id=self._next_id("ev"), statement=statement,
                      weight=weight, source=source, direction=direction)
        self._evidence[ev.id] = ev
        # A new refuting observation may open a challenge on affected beliefs.
        return ev.id

    def retract_evidence(self, evidence_id: str):
        """There is no such operation. Contradicting evidence is recorded,
        never deleted — attempting it is refused, loudly."""
        raise Refusal(EVIDENCE_IMMUTABLE,
                      f"{evidence_id} stays in history; record counter-evidence instead")

    # -- the versioned challenge path -------------------------------------
    def challenge(self, belief_id: str, evidence_ids: Sequence[str]) -> str:
        """Present new evidence against the current interpretation.

        Below LISTEN: noted, belief stays SETTLED (easy to listen).
        At/above LISTEN: SETTLED -> CHALLENGED.
        """
        b = self._belief(belief_id)
        missing = [e for e in evidence_ids if e not in self._evidence]
        if missing:
            raise Refusal(NO_EVIDENCE, f"cites unrecorded evidence: {missing}")
        refuting = sum(self._evidence[e].weight for e in evidence_ids
                       if self._evidence[e].direction == REFUTES)
        r = self._receipt(belief_id, "EVIDENCE_NOTED", evidence_ids,
                          f"refuting weight {refuting:.3f} presented")
        if refuting >= self._thresholds["listen"] and b["status"] == SETTLED:
            b["status"] = CHALLENGED
            self._receipt(belief_id, "SETTLED->CHALLENGED", evidence_ids,
                          f"refuting weight {refuting:.3f} >= listen "
                          f"{self._thresholds['listen']}")
            return CHALLENGED
        return b["status"]

    def update_belief(self, belief_id: str, new_interpretation: str,
                      evidence_ids: Sequence[str],
                      confidence: Optional[float] = None) -> str:
        """Supersede the current interpretation with a new version.

        Refused: no evidence, weak evidence (below CHANGE_TRUTH), confidence
        beyond what the evidence supports, drifted-unrequalified context.
        The old version is retained; the new version cites its cause.
        """
        self._check_requalified()
        b = self._belief(belief_id)
        if not evidence_ids:
            raise Refusal(NO_EVIDENCE,
                          "changing our mind takes evidence; none was cited")
        missing = [e for e in evidence_ids if e not in self._evidence]
        if missing:
            raise Refusal(NO_EVIDENCE, f"cites unrecorded evidence: {missing}")
        evs = [self._evidence[e] for e in evidence_ids]
        # Weight behind the NEW interpretation must clear CHANGE_TRUTH.
        for_new = sum(e.weight for e in evs if e.direction == SUPPORTS)
        if for_new < self._thresholds["change_truth"]:
            raise Refusal(WEAK_EVIDENCE,
                          f"weight {for_new:.3f} < change-truth "
                          f"{self._thresholds['change_truth']}: truth does not "
                          f"change on thin evidence")
        cap = max_supported_confidence(
            [e.weight for e in evs if e.direction == SUPPORTS])
        if confidence is not None and confidence > cap + 1e-9:
            raise Refusal(CONFIDENCE_EXCEEDS_EVIDENCE,
                          f"claims {confidence} on evidence supporting {cap}")
        lo, hi = confidence_interval(
            [e.weight for e in evs if e.direction == SUPPORTS],
            [e.weight for e in evs if e.direction == REFUTES])
        prev = b["versions"][-1]
        r = self._receipt(
            belief_id, f"{b['status']}->REOPENED->REQUALIFIED", evidence_ids,
            f"new interpretation supersedes v{prev.n} on evidence weight "
            f"{for_new:.3f}")
        v = BeliefVersion(n=prev.n + 1, interpretation=new_interpretation,
                          evidence_ids=tuple(evidence_ids),
                          conf_lo=lo, conf_hi=hi,
                          prev_hash=prev.version_hash, caused_by=r.id)
        b["versions"].append(v)  # old versions retained — history intact
        b["status"] = REQUALIFIED
        b["applicable"] = {"version": v.n, "context": self._qualified_under}
        return v.version_hash

    def return_to_unresolved(self, belief_id: str, evidence_ids: Sequence[str],
                             reason: str) -> str:
        """The honest alternative to a forced update: admit we don't know."""
        b = self._belief(belief_id)
        r = self._receipt(belief_id, f"{b['status']}->UNRESOLVED", evidence_ids,
                          reason)
        b["status"] = UNRESOLVED
        return r.id

    # -- guards ------------------------------------------------------------
    def protective_check(self, belief_id: str) -> str:
        """Quick to protect people: harm-suggesting evidence at/above the
        protect threshold recommends protective action even when truth
        has not (yet) changed. This is a tripwire, not a truth claim, so
        all recorded harm-suggesting refuting evidence counts. Returns
        PROTECT or NO_ACTION."""
        self._belief(belief_id)  # unknown belief -> Refusal
        harm = sum(e.weight for e in self._evidence.values()
                   if e.direction == REFUTES
                   and "harm" in e.statement.lower())
        harm = round(harm, 6)
        if harm >= self._thresholds["protect"]:
            self._receipt(belief_id, "PROTECTIVE_CHECK->PROTECT", (),
                          f"harm-suggesting weight {harm:.3f} >= protect "
                          f"{self._thresholds['protect']}")
            return "PROTECT"
        return "NO_ACTION"

    def assess_safety_from_observations(self, belief_id: str,
                                        observed_harm_count: int) -> str:
        """Absence of observed harm never counts as proof of safety.

        Claiming safety from zero observations is refused. Safety must be
        established by positive evidence, not by an empty incident log.
        """
        if observed_harm_count == 0:
            raise Refusal(SAFETY_FROM_ABSENCE,
                          "zero observed harms is not evidence of safety; "
                          "uncertainty interval unchanged")
        return "RECORDED"

    # -- drift --------------------------------------------------------------
    def note_context_drift(self, context: ContextFingerprint):
        """Bind calibration to a new policy/model/evaluator/environment.

        After drift, thresholds are unqualified: consequential reliance is
        refused until requalified.
        """
        if context.digest() != self._qualified_under:
            self._requalified = False
            self._receipt("THRESHOLDS", "QUALIFIED->REQUALIFICATION_REQUIRED",
                          (), f"context drifted to {context.digest()}")

    def requalify_thresholds(self, context: ContextFingerprint,
                             calibration_note: str):
        self._qualified_under = context.digest()
        self._requalified = True
        self._receipt("THRESHOLDS", "REQUALIFICATION_REQUIRED->QUALIFIED", (),
                      calibration_note)

    def rely(self, belief_id: str) -> dict:
        """Consequential reliance on the current interpretation.

        Refused when thresholds are drifted-unrequalified or the belief is
        UNRESOLVED. Returns the applicable version otherwise.
        """
        self._check_requalified()
        b = self._belief(belief_id)
        if b["status"] == UNRESOLVED:
            raise Refusal("UNRESOLVED_BELIEF",
                          "consequential reliance on an unresolved belief is refused")
        v = b["versions"][-1]
        return {"belief": belief_id, "version": v.n,
                "interpretation": v.interpretation,
                "confidence": [v.conf_lo, v.conf_hi],
                "context": b["applicable"]["context"]}

    # -- history (read-only views; versions are tuples — no in-place edit) --
    def history(self, belief_id: str) -> Tuple[BeliefVersion, ...]:
        return tuple(self._belief(belief_id)["versions"])

    def status(self, belief_id: str) -> str:
        return self._belief(belief_id)["status"]

    def receipts(self, belief_id: Optional[str] = None) -> Tuple[Receipt, ...]:
        if belief_id is None:
            return tuple(self._receipts)
        return tuple(r for r in self._receipts if r.belief_id == belief_id)

    def get_evidence(self, evidence_id: str) -> Evidence:
        return self._evidence[evidence_id]
