"""Evidence access & authority governance (spec). Enforcement layer for
uncertain-scope work.

Core rule: "Undetermined evidence may be investigated, but it must never
silently become independently verified evidence or authority to act."

Principle: "Evidence access, evidence credibility, independent qualification
and execution authority are four different things."

Composes with uncertainty.py and revocation.py:
  - uncertainty.py decides WHICH evidence may certify (cleared vs undetermined).
  - this module decides WHO may do WHAT with it, for WHICH purpose, and
    re-checks at the moment of consequential use. Inspect != certify != act.
"""
from __future__ import annotations

from dataclasses import dataclass, field

# Five capabilities, not two. Scoped to evidence object + version + purpose +
# project + operation + expiration.
CAPABILITIES = (
    "inspect",   # examine the evidence object
    "analyze",   # form hypotheses, run diagnostics
    "test",      # sandbox experiments — never as a blind holdout
    "certify",   # support a qualification claim — requires independent admissibility
    "act",       # execute under LAW authorization
)

# Roles in the purpose-bound authorization function.
ROLES = (
    "researcher",
    "builder",
    "independent_verifier",
    "executor",   # ACT seat under LAW
)

# Key separation: no node grants itself authority by generating a plausible
# explanation. KNOW exposes uncertainty; VERIFY investigates and qualifies;
# LAW determines permission; ACT enforces.
NODE_AUTHORITY = {
    "KNOW": "expose uncertainty to investigators — never clears it",
    "VERIFY": "investigate, build clearance packets, qualify — never authorize acts",
    "LAW": "determine permission for an operation — never certify evidence",
    "ACT": "enforce current eligibility at execution time — never re-decide law",
}

# Default role × capability matrix for UNDETERMINED evidence. None of these
# ever silently becomes independent proof.
UNDETERMINED_CAPABILITY_POLICY = {
    "researcher": {
        "inspect": "PERMIT", "analyze": "PERMIT", "test": "PERMIT",
        "certify": "DENY", "act": "DENY"},
    "builder": {
        "inspect": "PERMIT", "analyze": "PERMIT", "test": "PERMIT_SANDBOX_ONLY",
        "certify": "DENY", "act": "DENY"},
    "independent_verifier": {
        "inspect": "PERMIT", "analyze": "PERMIT", "test": "PERMIT",
        "certify": "DENY_AS_INDEPENDENT_PROOF", "act": "DENY"},
    "executor": {
        "inspect": "PERMIT_LABELED_ONLY", "analyze": "DENY", "test": "DENY",
        "certify": "DENY",
        "act": "PERMIT_ONLY_WITH_LAW_RECEIPT_AND_CURRENT_ELIGIBILITY"},
}

# Role × capability for INDEPENDENTLY CLEARED evidence (certify opens, act
# still needs LAW).
CLEARED_CAPABILITY_POLICY = {
    "researcher": {
        "inspect": "PERMIT", "analyze": "PERMIT", "test": "PERMIT",
        "certify": "PERMIT", "act": "DENY"},
    "builder": {
        "inspect": "PERMIT", "analyze": "PERMIT", "test": "PERMIT_SANDBOX_ONLY",
        "certify": "PERMIT_WITH_VERIFIER", "act": "DENY"},
    "independent_verifier": {
        "inspect": "PERMIT", "analyze": "PERMIT", "test": "PERMIT",
        "certify": "PERMIT", "act": "DENY"},
    "executor": {
        "inspect": "PERMIT", "analyze": "DENY", "test": "DENY",
        "certify": "DENY",
        "act": "PERMIT_ONLY_WITH_LAW_RECEIPT_AND_CURRENT_ELIGIBILITY"},
}


@dataclass(frozen=True)
class CapabilityGrant:
    """One scoped permission. Narrow by construction: same evidence, different
    purpose or operation, is a different grant."""
    grant_id: str
    identity: str
    role: str                 # one of ROLES
    capability: str           # one of CAPABILITIES
    evidence_ref: str
    evidence_version: str     # versioned eligibility — stale versions do not grant
    purpose: str
    project: str
    operation: str
    expires_at: str = ""      # ISO timestamp; expired grants are dead

    def __post_init__(self):
        assert self.role in ROLES, self.role
        assert self.capability in CAPABILITIES, self.capability

    def scope_key(self) -> tuple:
        return (self.identity, self.role, self.capability, self.evidence_ref,
                self.evidence_version, self.purpose, self.project,
                self.operation)


@dataclass
class AccessDecision:
    """Access-time checkpoint: may this identity exercise this capability on
    this evidence, for this purpose, right now?"""
    grant: CapabilityGrant
    evidence_assessment: str   # confirmed_compromised | possibly_compromised |
                               # independently_cleared | unassessed
    decision: str = ""         # PERMIT | DENY (+ qualifiers)
    reason: str = ""

    def evaluate(self, now_iso: str) -> "AccessDecision":
        policy = (UNDETERMINED_CAPABILITY_POLICY
                  if self.evidence_assessment in ("possibly_compromised", "unassessed")
                  else CLEARED_CAPABILITY_POLICY
                  if self.evidence_assessment == "independently_cleared"
                  else UNDETERMINED_CAPABILITY_POLICY)
        # Confirmed-compromised evidence gets no investigative access beyond
        # labeled historical reading.
        if self.evidence_assessment == "confirmed_compromised":
            if (self.grant.role == "researcher"
                    and self.grant.capability == "inspect"):
                self.decision = "PERMIT_LABELED_HISTORICAL"
                self.reason = "historical research only; uncertainty labels mandatory"
            else:
                self.decision = "DENY"
                self.reason = "confirmed compromised — contribution disqualified"
            return self
        if self.grant.expires_at and self.grant.expires_at < now_iso:
            self.decision = "DENY"
            self.reason = "grant expired — expired grants are dead"
            return self
        self.decision = policy[self.grant.role][self.grant.capability]
        self.reason = (
            f"purpose-bound decision: {self.grant.role} × "
            f"{self.grant.capability} × {self.evidence_assessment}"
        )
        return self


@dataclass
class UndeterminedProvenance:
    """Purpose-laundering prevention. Every artifact derived from undetermined
    evidence carries the marker through EVERY transformation: summaries,
    notes, successor packages, retrained prompts. The marker does not mean
    'false' — it means the source cannot count as independent proof. If later
    evidence independently supports the claim, VERIFY reassesses; the marker
    is lifted only by a clearance event, never by rewriting."""
    artifact_ref: str
    derived_from_undetermined: bool = True
    derivation_chain: tuple = ()   # ordered artifact_refs, source → this artifact
    original_incident: str = ""

    def transform(self, new_ref: str) -> "UndeterminedProvenance":
        """Any transformation preserves the marker. There is no wash cycle."""
        return UndeterminedProvenance(
            artifact_ref=new_ref,
            derived_from_undetermined=True,
            derivation_chain=self.derivation_chain + (self.artifact_ref,),
            original_incident=self.original_incident,
        )

    def clear(self, clearance_verdict: str) -> "UndeterminedProvenance":
        """Marker lifts only via a recorded clearance event (CLEARED packet),
        never by rewriting or summarizing."""
        assert clearance_verdict == "CLEARED", \
            "only a CLEARED packet lifts the marker"
        return UndeterminedProvenance(
            artifact_ref=self.artifact_ref,
            derived_from_undetermined=False,
            derivation_chain=self.derivation_chain,
            original_incident=self.original_incident,
        )

    def may_serve_as_independent_proof(self) -> bool:
        return not self.derived_from_undetermined


@dataclass
class UseTimeCheck:
    """Use-time checkpoint: may THIS claim support THIS decision, NOW?

    Re-verifies at the moment of consequential use: current eligibility
    version, revocation state, lineage markers, LAW receipt, and scope.
    Fail closed — if mandatory proof cannot be established, the action
    does not proceed."""
    claim_id: str
    evidence_refs: tuple
    evidence_eligibility_version: str
    law_receipt: str            # "" = no LAW authorization
    current_eligibility_version: str
    revocation_state: str       # eligibility verdict from uncertainty.py
    undetermined_markers: tuple = ()  # UndeterminedProvenance refs in lineage

    def evaluate(self) -> dict:
        if self.evidence_eligibility_version != self.current_eligibility_version:
            return {"permitted": False,
                    "reason": "stale eligibility version — re-derive from current certificates"}
        if self.undetermined_markers:
            return {"permitted": False,
                    "reason": "undetermined evidence in lineage cannot certify this decision"}
        if not self.law_receipt:
            return {"permitted": False,
                    "reason": "no LAW receipt — execution authority not established"}
        if self.revocation_state not in ("UNAFFECTED", "REQUALIFIED"):
            return {"permitted": False,
                    "reason": f"eligibility verdict is {self.revocation_state} — "
                              "independent qualification not established"}
        return {"permitted": True, "reason": "current eligibility confirmed at use time"}


# Adversarial test contracts. Each names the attack and the required result.
ADVERSARIAL_TESTS = (
    "purpose_laundering_via_summary: a summary of undetermined evidence must "
    "retain derived_from_undetermined through the transformation; presenting "
    "it as fresh blind proof is denied",
    "role_switching_for_broader_permissions: an identity holding builder and "
    "verifier roles gets the STRICTEST bound of (identity, purpose) pairs — "
    "the verifier hat never widens builder permissions",
    "stale_cache_at_act: a certificate cached before a revocation fails the "
    "use-time eligibility-version check — ACT fails closed",
    "debug_submitted_as_blind_proof: a diagnostic run labeled test/sandbox "
    "cannot be submitted as independent qualification evidence — certify denied",
)
