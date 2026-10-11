"""
UD-05 — UNRESOLVED MEANS UNRESOLVED (absorbs D12, D13).

Unknown is unknown. It is never converted into a pass, a clean bill, or a
quiet default. Anything unresolved stays visibly unresolved until real
evidence resolves it.

Three-valued evidence logic: CONFIRMED / EXCLUDED / UNDETERMINED.
Undetermined is a supported outcome, never an error — but it can never
silently become verified evidence or permission to act.

Doctrine: SN-083 — "Resolve what evidence can reach; retain exactly one
UNKNOWN naming the precise missing evidence and its owner — and change
nothing against an unresolved target."

Stdlib only.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


# ---------------------------------------------------------------------------
# Three-valued evidence logic
# ---------------------------------------------------------------------------

class EvidenceState(str, Enum):
    CONFIRMED = "CONFIRMED"       # trustworthy, demonstrated
    EXCLUDED = "EXCLUDED"         # proven untrustworthy — can never support
    UNDETERMINED = "UNDETERMINED" # genuinely not known — a supported outcome


class Operation(str, Enum):
    INSPECT = "INSPECT"
    ANALYZE = "ANALYZE"
    TEST = "TEST"
    CERTIFY = "CERTIFY"
    ACT = "ACT"


# Operations that need certainty on every load-bearing dimension.
_HARD_OPERATIONS = {Operation.CERTIFY, Operation.ACT}


# ---------------------------------------------------------------------------
# Refusals
# ---------------------------------------------------------------------------

class UnknownGuardRefusal(Exception):
    """Raised whenever unknown would be laundered into certainty or action."""

    def __init__(self, code: str, message: str, items: Optional[List[str]] = None):
        super().__init__(message)
        self.code = code
        self.items = items or []


# Laundering-pattern codes emitted by scan_report / guard_certify.
LAUNDER_UNKNOWN_TO_PASS = "LAUNDER_UNKNOWN_TO_PASS"
LAUNDER_UNKNOWN_TO_ALLOW = "LAUNDER_UNKNOWN_TO_ALLOW"
LAUNDER_DROPPED_UNKNOWN = "LAUNDER_DROPPED_UNKNOWN"
LAUNDER_ABSENCE_AS_SAFETY = "LAUNDER_ABSENCE_AS_SAFETY"
LAUNDER_ACCESS_AS_CREDIBILITY = "LAUNDER_ACCESS_AS_CREDIBILITY"
LAUNDER_EXCLUDED_AS_SUPPORT = "LAUNDER_EXCLUDED_AS_SUPPORT"
PERMIT_DENIED_UNKNOWN = "PERMIT_DENIED_UNKNOWN"
PERMIT_DENIED_EXCLUDED = "PERMIT_DENIED_EXCLUDED"
USE_BINDING_VIOLATION = "USE_BINDING_VIOLATION"
RESOLUTION_WITHOUT_EVIDENCE = "RESOLUTION_WITHOUT_EVIDENCE"


# ---------------------------------------------------------------------------
# Records
# ---------------------------------------------------------------------------

@dataclass
class EvidenceItem:
    """One piece of evidence with its trust state."""
    id: str
    state: EvidenceState
    load_bearing: bool = True      # does a verdict/decision rest on this?
    note: str = ""
    # D13: access is not credibility. Merely having accessed the evidence
    # (opened the file, fetched the page) is not evaluation.
    evaluated: bool = True


@dataclass
class UnresolvedItem:
    """A retained unknown. 'Unknown, and here's exactly what would resolve
    it' is a complete verdict; 'unknown, moving on' is not."""
    id: str
    what_unknown: str
    why_matters: str
    what_would_resolve: str
    owner: str                    # who is responsible for resolving it
    status: str = "OPEN"          # OPEN | RESOLVED
    resolved_by: str = ""         # evidence reference — required to close


@dataclass
class CertificationReceipt:
    subject: str
    verdict: str
    evidence_ids: List[str]
    note: str = "certified with zero open unknowns on load-bearing dimensions"


# ---------------------------------------------------------------------------
# The guard
# ---------------------------------------------------------------------------

def _open_unknowns(evidence: Dict[str, EvidenceItem],
                   unresolved: List[UnresolvedItem]) -> List[str]:
    """Names of every unresolved thing: UNDETERMINED load-bearing evidence
    plus OPEN unresolved items."""
    names = [e.id for e in evidence.values()
             if e.state == EvidenceState.UNDETERMINED and e.load_bearing]
    names += [u.id for u in unresolved if u.status == "OPEN"]
    return names


def guard_certify(subject: str, claimed_verdict: str,
                  evidence: Dict[str, EvidenceItem],
                  unresolved: List[UnresolvedItem]) -> CertificationReceipt:
    """Refuse to certify anything with open unknowns as resolved.

    claimed_verdict in {"PASS", "CERTIFIED", "VERIFIED", "RESOLVED", "SAFE"}.
    """
    claimed = claimed_verdict.strip().upper()
    certifying_claims = {"PASS", "CERTIFIED", "VERIFIED", "RESOLVED", "SAFE",
                         "SAFETY_ESTABLISHED"}
    open_names = _open_unknowns(evidence, unresolved)

    # EXCLUDED evidence cited as support is its own laundering.
    excluded_support = [e.id for e in evidence.values()
                        if e.state == EvidenceState.EXCLUDED]

    if claimed in certifying_claims:
        if open_names:
            raise UnknownGuardRefusal(
                LAUNDER_UNKNOWN_TO_PASS,
                "Refusing to certify '%s' as %s with open unknowns: %s. "
                "Unknown is not a pass." % (subject, claimed,
                                             ", ".join(open_names)),
                items=open_names)
        if excluded_support:
            raise UnknownGuardRefusal(
                LAUNDER_EXCLUDED_AS_SUPPORT,
                "Refusing to certify '%s': excluded evidence cannot support "
                "a verdict: %s." % (subject, ", ".join(excluded_support)),
                items=excluded_support)
    # D13: merely accessed evidence is not evaluated evidence.
    unevaluated = [e.id for e in evidence.values() if not e.evaluated]
    if claimed in certifying_claims and unevaluated:
        raise UnknownGuardRefusal(
            LAUNDER_ACCESS_AS_CREDIBILITY,
            "Refusing to certify '%s': evidence accessed but not evaluated "
            "is not credibility: %s." % (subject, ", ".join(unevaluated)),
            items=unevaluated)

    return CertificationReceipt(
        subject=subject, verdict=claimed,
        evidence_ids=[e.id for e in evidence.values()
                      if e.state == EvidenceState.CONFIRMED])


def guard_allow(subject: str, evidence: Dict[str, EvidenceItem],
                unresolved: List[UnresolvedItem]) -> str:
    """Default-allow is refused on unknown: a PROCEED/ACT decision with
    UNDETERMINED load-bearing evidence or OPEN unresolved items is denied."""
    open_names = _open_unknowns(evidence, unresolved)
    if open_names:
        raise UnknownGuardRefusal(
            LAUNDER_UNKNOWN_TO_ALLOW,
            "Refusing default-allow for '%s' with open unknowns: %s. "
            "Unknown is not permission." % (subject, ", ".join(open_names)),
            items=open_names)
    return "ALLOWED"


def resolve_unknown(item: UnresolvedItem, evidence_ref: str) -> UnresolvedItem:
    """Close an unresolved item — only with a real evidence reference.
    Resolving without evidence is laundering."""
    if not evidence_ref or not evidence_ref.strip():
        raise UnknownGuardRefusal(
            RESOLUTION_WITHOUT_EVIDENCE,
            "Refusing to resolve '%s' without an evidence reference. "
            "Naming the missing evidence is not the same as supplying it."
            % item.id,
            items=[item.id])
    item.status = "RESOLVED"
    item.resolved_by = evidence_ref.strip()
    return item


# ---------------------------------------------------------------------------
# Five-permission purpose-bound gate (D13)
# ---------------------------------------------------------------------------

@dataclass
class UseBinding:
    """Every use is bound to who is using it, why, and what it will
    influence — checked at the moment of use, not just at access."""
    identity: str
    purpose: str
    influences: str


def request_permission(identity: str, purpose: str, operation: Operation,
                       evidence: Dict[str, EvidenceItem],
                       influences: str) -> UseBinding:
    """Permit = f(identity, purpose, evidence, operation, context, LAW).

    CERTIFY and ACT fail closed on any UNDETERMINED or EXCLUDED
    load-bearing evidence. INSPECT / ANALYZE / TEST may proceed with
    undetermined evidence, but derived outputs carry the marker.
    """
    unknown_lb = [e.id for e in evidence.values()
                  if e.state == EvidenceState.UNDETERMINED and e.load_bearing]
    excluded_lb = [e.id for e in evidence.values()
                   if e.state == EvidenceState.EXCLUDED and e.load_bearing]
    if operation in _HARD_OPERATIONS:
        if unknown_lb:
            raise UnknownGuardRefusal(
                PERMIT_DENIED_UNKNOWN,
                "Denied %s for %s: undetermined on load-bearing evidence: "
                "%s." % (operation.value, identity, ", ".join(unknown_lb)),
                items=unknown_lb)
        if excluded_lb:
            raise UnknownGuardRefusal(
                PERMIT_DENIED_EXCLUDED,
                "Denied %s for %s: excluded load-bearing evidence: %s."
                % (operation.value, identity, ", ".join(excluded_lb)),
                items=excluded_lb)
    return UseBinding(identity=identity, purpose=purpose, influences=influences)


def check_use(binding: UseBinding, identity: str, purpose: str,
              influences: str) -> bool:
    """Use-time check: the binding granted at access is re-checked at the
    moment of use. Any drift fails closed."""
    if (binding.identity != identity or binding.purpose != purpose
            or binding.influences != influences):
        raise UnknownGuardRefusal(
            USE_BINDING_VIOLATION,
            "Use-time binding violation: granted to %s for '%s' influencing "
            "'%s', used by %s for '%s' influencing '%s'. Fail closed."
            % (binding.identity, binding.purpose, binding.influences,
               identity, purpose, influences))
    return True


# ---------------------------------------------------------------------------
# Derived-from-undetermined markers (provenance survives projection)
# ---------------------------------------------------------------------------

@dataclass
class DerivedArtifact:
    id: str
    derived_from_undetermined: bool = False
    undetermined_sources: List[str] = field(default_factory=list)


def derive(artifact_id: str,
           inputs: List[EvidenceItem]) -> DerivedArtifact:
    """Summaries, lessons, and successor packages inherit the marker from
    anything undetermined they were derived from."""
    sources = [i.id for i in inputs
               if i.state == EvidenceState.UNDETERMINED]
    return DerivedArtifact(
        id=artifact_id,
        derived_from_undetermined=bool(sources),
        undetermined_sources=sources)


# ---------------------------------------------------------------------------
# Report scanner — the laundering patterns
# ---------------------------------------------------------------------------

_ABSENCE_PHRASES = (
    "no evidence of", "no issues found", "nothing found", "no sign of",
    "could not find", "failed to find", "no indication of",
    "no problems found", "zero findings",
)
_SAFETY_CONCLUSIONS = (
    "safe", "safety established", "no risk", "cleared", "verified safe",
    "proven safe", "risk-free",
)


@dataclass
class ScanFinding:
    code: str
    detail: str
    items: List[str] = field(default_factory=list)


def scan_report(report: dict) -> List[ScanFinding]:
    """Scan a verdict/report dict for unknown-laundering patterns.

    report keys:
      subject: str
      claimed: str — the headline verdict ("PASS", "SAFE", ...)
      evidence: {id: EvidenceState}
      unresolved_declared: [ids] — every unknown the scope declared
      unresolved_in_report: [ids] — unknowns actually present in the report
      statements: [{text: str, cites_positive_evidence: bool}]
    """
    findings: List[ScanFinding] = []
    evidence: Dict[str, EvidenceItem] = {
        k: EvidenceItem(id=k, state=v)
        for k, v in report.get("evidence", {}).items()
    }
    claimed = str(report.get("claimed", "")).strip().upper()
    certifying = {"PASS", "CERTIFIED", "VERIFIED", "RESOLVED", "SAFE",
                  "SAFETY_ESTABLISHED"}

    # 1. unknown -> PASS
    if claimed in certifying:
        unknowns = [k for k, e in evidence.items()
                    if e.state == EvidenceState.UNDETERMINED]
        if unknowns:
            findings.append(ScanFinding(
                LAUNDER_UNKNOWN_TO_PASS,
                "Report claims %s while evidence is undetermined: %s."
                % (claimed, ", ".join(unknowns)),
                items=unknowns))

    # 2. unknown silently dropped from the report
    declared = set(report.get("unresolved_declared", []))
    in_report = set(report.get("unresolved_in_report", []))
    dropped = sorted(declared - in_report)
    undetermined_unreported = [
        k for k, e in evidence.items()
        if e.state == EvidenceState.UNDETERMINED and k not in in_report
    ]
    missing = sorted(set(dropped) | set(undetermined_unreported))
    if missing:
        findings.append(ScanFinding(
            LAUNDER_DROPPED_UNKNOWN,
            "Unresolved items declared but absent from the report: %s. "
            "Dropped unknowns are laundered unknowns." % ", ".join(missing),
            items=missing))

    # 3. "no evidence of harm" presented as "evidence of safety"
    for st in report.get("statements", []):
        text = str(st.get("text", "")).lower()
        has_absence = any(p in text for p in _ABSENCE_PHRASES)
        has_safety = any(p in text for p in _SAFETY_CONCLUSIONS)
        if has_absence and has_safety and not st.get("cites_positive_evidence"):
            findings.append(ScanFinding(
                LAUNDER_ABSENCE_AS_SAFETY,
                "Absence of evidence presented as evidence of safety: %r. "
                "'No evidence of harm' is not 'evidence of safety'."
                % st.get("text", "")[:120]))

    # 4. excluded evidence cited as support
    excluded = [k for k, e in evidence.items()
                if e.state == EvidenceState.EXCLUDED]
    if excluded and claimed in certifying:
        findings.append(ScanFinding(
            LAUNDER_EXCLUDED_AS_SUPPORT,
            "Excluded evidence cannot support a %s verdict: %s."
            % (claimed, ", ".join(excluded)),
            items=excluded))

    return findings


# ---------------------------------------------------------------------------
# Honest boundary
# ---------------------------------------------------------------------------

def does_not_claim() -> str:
    return ("This guard judges the evidence states it is given; it does not "
            "discover unknowns on its own. A report that never declares its "
            "unknowns can only be caught on the unknowns it declares — "
            "honest declaration is a prerequisite, enforced by requiring "
            "the unresolved section to exist whenever undetermined evidence "
            "is in scope.")
