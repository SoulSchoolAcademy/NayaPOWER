"""NAYA-KERNEL-CONNECT — CANDIDATE implementation (NOT RATIFIED — NOT MERGED).

Implements the CONNECT node contract from CONNECT-NODE-SPEC-CANDIDATE.md
(draft) against the NodeBase interface. Candidate code on a feature branch:
it proves the spec is implementable; it grants nothing, merges nothing,
deploys nothing.

Contractual responsibility (spec §0): CONNECT decides what may be connected
to what, under whose consent, and what context becomes relevant because of
it — for knowledge inside one mind and for minds reaching each other across
NayaNET, under one boundary law. It owns the connection boundary: the rules
of what crosses and what never does.

Gate input contract (`state` dict keys; all reads explicit, nothing inferred):
  connection_request {
    id: str, kind: GRAPH_EDGE|MIND_LINK|SPACE_JOIN|INTERFACE_OPEN,
    parties: [{identity, owner_scope, role}],   # identity must be authenticated
    purpose: str,                                # binding (§3.3)
    scope: [{owner_scope, content_classes: [...]}]  # explicit allow-list (§3.2)
    consentRefs: [str],                           # ≥1 per party (§3.1)
    evidenceRefs: [str],
    boundaryPolicy: {version, forbidden_classes: [...], strictness: int},
    expiresAt: str | None,
    reversibility: float,                          # 0..10
    consentLadder: PRIVATE|SHARED|COLLECTIVE|PUBLIC,
    carry_authority: bool,                         # must be False (§4.4)
    door_proposal: {...} | None,                   # INTERFACE_OPEN only (§5.4)
  }
  consent_registry: {consent_id: {party, purpose, scope, expires_at,
                                 revoked: bool, consent_hash: str}}
  identity_bindings: {identity: {authenticated: bool, owner_scope,
                                 binding_ref}}
  evidence_registry: {ref: {content_hash, valid: bool}}
  boundary_policy: {version, forbidden_classes: [...], strictness: int}
  now: str | None

Gate outcomes map onto NodeBase.GateVerdict as:
  ADMITTED (all §4 refusal checks clear; sync path)              -> PASS
  async handshake pending (MIND_LINK/SPACE_JOIN multi-party)     -> NEED_EVIDENCE
  REFUSED (any §4.1–§4.8 or §2.3 condition)                       -> FAIL

CONNECT never grants, infers, or transmits authority (§1.3, §4.4);
authority_checks() declares validations only. Consent cannot be
manufactured by authority, urgency, or calculus score (§4.2).
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple

from naya_kernel.node_base import GateResult, GateVerdict, ManifestEntry, NodeBase

NODE_ID = "NAYA-KERNEL-CONNECT"
NODE_VERSION = "0.1.0-candidate"
PIPELINE_POSITION = 6

# §2 — the four connection kinds.
KIND_GRAPH_EDGE = "GRAPH_EDGE"
KIND_MIND_LINK = "MIND_LINK"
KIND_SPACE_JOIN = "SPACE_JOIN"
KIND_INTERFACE_OPEN = "INTERFACE_OPEN"
KINDS = frozenset({KIND_GRAPH_EDGE, KIND_MIND_LINK, KIND_SPACE_JOIN,
                   KIND_INTERFACE_OPEN})

# §2.1 — the consent ladder. Movement upward needs every affected owner's
# consent; no majority vote moves another owner's private context.
LADDER_PRIVATE = "PRIVATE"
LADDER_SHARED = "SHARED"
LADDER_COLLECTIVE = "COLLECTIVE"
LADDER_PUBLIC = "PUBLIC"
LADDER_ORDER = [LADDER_PRIVATE, LADDER_SHARED, LADDER_COLLECTIVE, LADDER_PUBLIC]
LADDER_RANK = {level: i for i, level in enumerate(LADDER_ORDER)}

# §2.3 — content categories that NEVER cross a boundary. No consent, no
# authority, no calculus score can authorize these (refused as PROHIBITED).
NEVER_CROSS = frozenset({
    "RAW_PRIVATE_MEMORY",
    "AUTHORITY_GRANTS",
    "IDENTITY_CREDENTIALS",
    "GOVERNANCE_INTERNALS",
    "BEYOND_PURPOSE_CONTENT",
    "POLICY_FORBIDDEN",
})

# §8.1 — connection lifecycle states.
C_PROPOSED = "PROPOSED"
C_CONSENT_PENDING = "CONSENT_PENDING"
C_VALIDATED = "VALIDATED"
C_ACTIVE = "ACTIVE"
C_SUSPENDED = "SUSPENDED"
C_REVOKED = "REVOKED"
C_SUPERSEDED = "SUPERSEDED"
C_REJECTED = "REJECTED"
C_INVALID = "INVALID"

# Space states (§6).
SPACE_ACTIVE = "ACTIVE"
SPACE_SUSPENDED = "SUSPENDED"
SPACE_DISSOLVED = "DISSOLVED"

# Legal connection transitions (from -> set(to)); everything else fails
# closed (§8.1). Note REJECTED/INVALID are terminal.
LEGAL_TRANSITIONS: Dict[str, frozenset] = {
    C_PROPOSED: frozenset({C_CONSENT_PENDING, C_VALIDATED, C_REJECTED,
                           C_INVALID}),
    C_CONSENT_PENDING: frozenset({C_VALIDATED, C_REJECTED, C_INVALID}),
    C_VALIDATED: frozenset({C_ACTIVE, C_REJECTED}),
    C_ACTIVE: frozenset({C_SUSPENDED, C_REVOKED, C_SUPERSEDED, C_INVALID}),
    C_SUSPENDED: frozenset({C_ACTIVE, C_REVOKED}),
    C_REVOKED: frozenset(),
    C_SUPERSEDED: frozenset(),
    C_REJECTED: frozenset(),
    C_INVALID: frozenset(),
}

# §4 refusal codes.
E_MALFORMED = "E_MALFORMED"
E_UNAUTHENTICATED_IDENTITY = "E_UNAUTHENTICATED_IDENTITY"   # §4.3
E_PROHIBITED_CROSSING = "E_PROHIBITED_CROSSING"             # §2.3
E_AUTHORITY_SMUGGLING = "E_AUTHORITY_SMUGGLING"             # §4.4
E_NO_EVIDENCE = "E_NO_EVIDENCE"                             # §4.1
E_CONSENT_MISSING = "E_CONSENT_MISSING"                     # §4.2
E_CROSS_OWNER_LEAKAGE = "E_CROSS_OWNER_LEAKAGE"              # §4.5
E_PURPOSE_DRIFT = "E_PURPOSE_DRIFT"                         # §4.6
E_SCOPE_CREEP = "E_SCOPE_CREEP"                             # §4.6
E_DOOR_RULE = "E_DOOR_RULE"                                 # §4.7
E_GOVERNANCE_EXPORT = "E_GOVERNANCE_EXPORT"                 # §4.8

# The §4.2/§4.4/§2.3 family is PROHIBITED: no one can authorize a cure.
# Missing evidence, identity, leakage, door-rule, and governance issues can
# be repaired with new evidence/consent (refusal, not prohibition).
PROHIBITED_CODES = frozenset({
    E_CONSENT_MISSING,
    E_AUTHORITY_SMUGGLING,
    E_PROHIBITED_CROSSING,
})

# §10 — edge semantics for the V2 graph binding.
EDGE_CONNECTED_TO = "CONNECTED_TO"
EDGE_MEMBER_OF = "MEMBER_OF"
EDGE_SHARED_WITH = "SHARED_WITH"
EDGE_SUPPORTS = "SUPPORTS"
EDGE_REFUTES = "REFUTES"
EDGE_CONTRADICTS = "CONTRADICTS"
EDGE_SUPERSEDES = "SUPERSEDES"
EDGE_INVALIDATES = "INVALIDATES"

CALCULUS_CANDIDATE_NOTE = (
    "Decision Value Calculus V2.1 is CANDIDATE (draft PR #1185), not ratified "
    "law. Scores recorded on receipts are aspirational; the mechanical §4 "
    "gates above are what refuse."
)


def _canonical(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str)


def _sha256(obj: Any) -> str:
    return hashlib.sha256(_canonical(obj).encode("utf-8")).hexdigest()


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _deepcopy_json(obj: Any) -> Any:
    return json.loads(_canonical(obj))


def _parse_ts(value: Any) -> Optional[datetime]:
    if not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value)
    except (ValueError, TypeError):
        return None


class ConnectNode(NodeBase):
    """NAYA-KERNEL-CONNECT. Owns the connection boundary (§1.4).

    Two surfaces, one boundary law: internal knowledge relationships
    (edges, traversal, relevance) and NayaNET connections between minds.
    Consent-gated, purpose-bound, scope-limited, receipted, revocable.
    """

    def __init__(self) -> None:
        # connection_id -> connection record (lifecycle state + inputs).
        self.connections: Dict[str, Dict[str, Any]] = {}
        # connection_id -> active edge ledger entries for the internal surface.
        self.edge_ledger: Dict[str, Dict[str, Any]] = {}
        # space_id -> connection space record (§6).
        self.spaces: Dict[str, Dict[str, Any]] = {}
        # interface_id -> door record (§5.4).
        self.interfaces: Dict[str, Dict[str, Any]] = {}
        # execution_id -> idempotent mutation result (§3.4, §11 replay).
        self.mutations: Dict[str, Dict[str, Any]] = {}
        # Boundary policy history: version -> {forbidden_classes, strictness}.
        self.policy_history: Dict[str, Dict[str, Any]] = {}
        # The full connection ledger: every receipt (establish, share,
        # suspend, revoke, dissolve, rejection) in issuance order (§13).
        self.ledger: List[Dict[str, Any]] = []
        self.last_receipt: Optional[Dict[str, Any]] = None

    # ------------------------------------------------------------------
    # NodeBase interface
    # ------------------------------------------------------------------
    def manifest_entry(self) -> ManifestEntry:
        return ManifestEntry(
            node_id=NODE_ID,
            version=NODE_VERSION,
            responsibilities=[
                "admit or refuse connections at the boundary (§4)",
                "enforce consent ladder, purpose binding, scope allow-lists",
                "govern NayaNET handshakes, leases, and the door rule",
                "maintain connection spaces and shared-manifest ledgers",
                "bind validated connections to V2 graph edges",
                "emit hash-bound connection receipts for cold reconstruction",
            ],
        )

    def gate(self, state: Dict[str, Any]) -> GateResult:
        """Admission intake for a connection proposal (spec §4).

        Runs the §4 refusal ladder in precedence order: malformed intake,
        unauthenticated identity, prohibited crossings, authority smuggling,
        no evidence, consent, cross-owner leakage, door rule, governance
        export. Async handshakes (MIND_LINK/SPACE_JOIN) return NEED_EVIDENCE
        until the handshake completes; completed handshakes PASS.
        """
        request = state.get("connection_request") or {}
        consent_registry = state.get("consent_registry") or {}
        identity_bindings = state.get("identity_bindings") or {}
        evidence_registry = state.get("evidence_registry") or {}
        boundary_policy = state.get("boundary_policy") or {}
        now = state.get("now") or _now_iso()
        verdict, reasons = self._admit(request, consent_registry,
                                       identity_bindings, evidence_registry,
                                       boundary_policy, now)
        return GateResult(verdict=verdict, reasons=reasons)

    def persisted_transitions(self) -> List[str]:
        base = [f"{frm} -> {to}" for frm, tos in LEGAL_TRANSITIONS.items()
                for to in sorted(tos)]
        return base + [
            "space create -> active -> suspended -> dissolved",
            "lease expiry -> revoked (automatic)",
            "consent revoked -> connection revoked + edges STALE",
        ]

    def evidence_hooks(self) -> List[str]:
        return [
            "smartledger.connections (ConnectionReceipt stream, proposed)",
            "consent receipts (content-addressed, re-derivable)",
            "shared manifests (hashes of crossed content, per crossing)",
            "boundary policy history (versioned floor)",
            "VERIFY findings on crossings (PURPOSE_DRIFT, leakage alerts)",
            "handshake records (mutual auth + policy exchange + consent)",
        ]

    def authority_checks(self) -> List[str]:
        return [
            "identity authenticated binding per party (§4.3)",
            "consent receipt validity per party, per purpose, per scope (§4.2)",
            "authority smuggling scan: connection carries context, never power (§4.4)",
            "never-cross categories enforced against boundary policy (§2.3)",
            "door-rule: no competing source of truth at new interfaces (§4.7)",
            "no authority grant/inference/expansion/persistence — declared only",
        ]

    # ------------------------------------------------------------------
    # §4 — the refusal ladder (precedence order)
    # ------------------------------------------------------------------
    def _admit(
        self,
        request: Dict[str, Any],
        consent_registry: Dict[str, Any],
        identity_bindings: Dict[str, Any],
        evidence_registry: Dict[str, Any],
        boundary_policy: Dict[str, Any],
        now: str,
    ) -> Tuple[GateVerdict, List[str]]:
        """Return (verdict, reasons) for a connection proposal."""
        missing = self._missing_fields(request)
        if missing:
            return (GateVerdict.FAIL,
                    [f"CONNECT REFUSED: {E_MALFORMED} missing={missing}"])

        unauth = self._unauthenticated_parties(request, identity_bindings)
        if unauth:
            return (GateVerdict.FAIL,
                    [f"CONNECT PROHIBITED: {E_UNAUTHENTICATED_IDENTITY} "
                     f"parties={unauth} (§4.3: unauthenticated counterpart is "
                     f"indistinguishable from an attacker)"])

        prohibited = self._prohibited_crossing(request, boundary_policy)
        if prohibited:
            return (GateVerdict.FAIL,
                    [f"CONNECT PROHIBITED: {E_PROHIBITED_CROSSING} "
                     f"categories={sorted(prohibited)} (§2.3: no consent, "
                     f"authority, or score can authorize these)"])

        smuggled = self._authority_smuggling(request)
        if smuggled:
            return (GateVerdict.FAIL,
                    [f"CONNECT PROHIBITED: {E_AUTHORITY_SMUGGLING} "
                     f"detail={smuggled} (§4.4: a connection carries context, "
                     f"never power)"])

        ok_evidence, evidence_gap = self._evidence_valid(request,
                                                         evidence_registry)
        if not ok_evidence:
            return (GateVerdict.FAIL,
                    [f"CONNECT REFUSED: {E_NO_EVIDENCE} missing={evidence_gap} "
                     f"(§4.1: never create trust from proximity or semantic "
                     f"similarity alone)"])

        ok_consent, consent_gap = self._consents_valid(
            request, consent_registry, now)
        if not ok_consent:
            return (GateVerdict.FAIL,
                    [f"CONNECT PROHIBITED: {E_CONSENT_MISSING} "
                     f"detail={consent_gap} (§4.2: consent cannot be "
                     f"manufactured by authority, urgency, or calculus "
                     f"score)"])

        leaked = self._cross_owner_leakage(request, consent_registry, now)
        if leaked:
            return (GateVerdict.FAIL,
                    [f"CONNECT REFUSED: {E_CROSS_OWNER_LEAKAGE} "
                     f"detail={leaked} (§4.5: critical failure, affected "
                     f"owner's VERIFY must be notified)"])

        if request.get("kind") == KIND_INTERFACE_OPEN:
            ok_door, door_gap = self._door_rule(request)
            if not ok_door:
                return (GateVerdict.FAIL,
                        [f"CONNECT REFUSED: {E_DOOR_RULE} detail={door_gap} "
                         f"(§4.7: no competing source of truth)"])

        gov = self._governance_export(request)
        if gov:
            return (GateVerdict.FAIL,
                    [f"CONNECT REFUSED: {E_GOVERNANCE_EXPORT} "
                     f"detail={gov} (§4.8: control planes stay home)"])

        if request.get("kind") in (KIND_MIND_LINK, KIND_SPACE_JOIN):
            handshake = request.get("handshake") or {}
            if not handshake.get("complete"):
                return (GateVerdict.NEED_EVIDENCE,
                        [f"CONNECT NEED_EVIDENCE: async handshake incomplete "
                         f"(§8.3: §5.3 steps 1-5 not all recorded); "
                         f"proposal held inert, never half-trusted"])

        return (GateVerdict.PASS,
                [f"CONNECT ADMITTED: kind={request['kind']} "
                 f"parties={len(request['parties'])} ladder="
                 f"{request.get('consentLadder', LADDER_SHARED)}"])
    # ------------------------------------------------------------------
    # Refusal-ladder helpers (§2.3, §3, §4)
    # ------------------------------------------------------------------
    @staticmethod
    def _missing_fields(request: Dict[str, Any]) -> List[str]:
        required = ["id", "kind", "parties", "purpose", "scope",
                    "consentRefs", "evidenceRefs", "boundaryPolicy",
                    "reversibility"]
        missing = [f for f in required if request.get(f) in (None, "", [])]
        if request.get("kind") not in KINDS and "kind" not in missing:
            missing.append("kind(unknown)")
        parties = request.get("parties")
        if isinstance(parties, list) and len(parties) == 0:
            missing.append("parties(empty)")
        return missing

    @staticmethod
    def _unauthenticated_parties(
        request: Dict[str, Any],
        identity_bindings: Dict[str, Any],
    ) -> List[str]:
        bad = []
        for party in request.get("parties") or []:
            identity = party.get("identity")
            binding = (identity_bindings or {}).get(identity) or {}
            if not binding.get("authenticated"):
                bad.append(str(identity))
        return bad

    @staticmethod
    def _prohibited_crossing(
        request: Dict[str, Any],
        boundary_policy: Dict[str, Any],
    ) -> List[str]:
        """§2.3: the never-cross categories in the requested scope."""
        flagged: List[str] = []
        classes: List[str] = []
        for entry in request.get("scope") or []:
            classes.extend(entry.get("content_classes") or [])
        upper = {str(c).upper() for c in classes}
        for category in NEVER_CROSS:
            if category in upper:
                flagged.append(category)
        forbidden = set(boundary_policy.get("forbidden_classes") or [])
        if upper & {str(f).upper() for f in forbidden}:
            flagged.append("POLICY_FORBIDDEN")
        return sorted(set(flagged))

    @staticmethod
    def _authority_smuggling(request: Dict[str, Any]) -> Optional[str]:
        """§4.4: any attempt to carry, imply, or enable authority."""
        if request.get("carry_authority"):
            return "carry_authority=True on the request"
        purpose = str(request.get("purpose") or "").lower()
        for marker in ("bypass law gate", "bypass the law gate",
                       "inherit upstream grant", "act with another mind's",
                       "escalate permission", "impersonate"):
            if marker in purpose:
                return f"purpose implies authority routing: '{marker}'"
        scope_classes = [str(c).lower() for entry in request.get("scope") or []
                         for c in (entry.get("content_classes") or [])]
        for marker in ("capabilities", "permissions", "tokens",
                       "credentials", "authority"):
            if marker in scope_classes:
                return f"scope names authority carrier '{marker}'"
        return None

    @staticmethod
    def _evidence_valid(
        request: Dict[str, Any],
        evidence_registry: Dict[str, Any],
    ) -> Tuple[bool, List[str]]:
        missing = []
        for ref in request.get("evidenceRefs") or []:
            record = (evidence_registry or {}).get(ref)
            if not record or not record.get("valid"):
                missing.append(str(ref))
        # GRAPH_EDGE and MIND_LINK require ≥1 valid evidence ref (§4.1).
        if request.get("kind") in (KIND_GRAPH_EDGE, KIND_MIND_LINK) and \
                not request.get("evidenceRefs"):
            missing.append("(none supplied)")
        return (len(missing) == 0, missing)

    def _consent_hash(self, consent: Dict[str, Any]) -> str:
        body = {k: v for k, v in consent.items()
                if k not in ("consent_hash",)}
        return _sha256(body)

    def _consents_valid(
        self,
        request: Dict[str, Any],
        consent_registry: Dict[str, Any],
        now: str,
    ) -> Tuple[bool, List[str]]:
        """§3.1/§4.2: explicit, per-party, per-purpose, re-derivable consent."""
        problems: List[str] = []
        refs = request.get("consentRefs") or []
        by_party: Dict[str, List[str]] = {}
        for ref in refs:
            record = (consent_registry or {}).get(ref)
            if not record:
                problems.append(f"{ref}: unresolvable")
                continue
            party = str(record.get("party"))
            by_party.setdefault(party, []).append(ref)
            if record.get("consent_hash") != self._consent_hash(record):
                problems.append(f"{ref}: hash mismatch (forgery or corruption)")
            expiry = record.get("expires_at")
            if expiry and _parse_ts(expiry) and _parse_ts(now) and \
                    _parse_ts(expiry) <= _parse_ts(now):
                problems.append(f"{ref}: expired")
            if record.get("revoked"):
                problems.append(f"{ref}: revoked")
            if record.get("purpose") != request.get("purpose"):
                problems.append(f"{ref}: purpose mismatch "
                                f"({record.get('purpose')!r} != "
                                f"{request.get('purpose')!r})")
        # Every party needs at least one valid consent (§3.1).
        for party in request.get("parties") or []:
            identity = str(party.get("identity"))
            valid_refs = [r for r in by_party.get(identity, [])
                          if not any(r in p for p in problems)]
            if not valid_refs:
                problems.append(f"party {identity}: no valid consent")
        return (len(problems) == 0, problems)

    def _cross_owner_leakage(
        self,
        request: Dict[str, Any],
        consent_registry: Dict[str, Any],
        now: str,
    ) -> Optional[str]:
        """§4.5: scope exposing owner A's context with only owner B's consent."""
        scope_by_owner: Dict[str, set] = {}
        for entry in request.get("scope") or []:
            scope_by_owner.setdefault(str(entry.get("owner_scope")),
                                      set()).update(
                entry.get("content_classes") or [])
        owner_of = {str(p.get("identity")): str(p.get("owner_scope"))
                    for p in request.get("parties") or []}
        consenting_by_owner: Dict[str, bool] = {}
        for ref in request.get("consentRefs") or []:
            record = (consent_registry or {}).get(ref) or {}
            party = str(record.get("party"))
            owner = owner_of.get(party)
            good = (record.get("consent_hash") == self._consent_hash(record)
                    and not record.get("revoked"))
            expiry = record.get("expires_at")
            if expiry and _parse_ts(expiry) and _parse_ts(now) and \
                    _parse_ts(expiry) <= _parse_ts(now):
                good = False
            if owner and good:
                consenting_by_owner[owner] = True
        for owner, classes in scope_by_owner.items():
            if classes and not consenting_by_owner.get(owner, False):
                return (f"owner_scope '{owner}' exposes classes "
                        f"{sorted(classes)} with no valid consent from that "
                        f"owner")
        # Consent is not transferable upward (§2.1): PUBLIC for another mind's
        # scope is leakage, not authorization.
        ladder = request.get("consentLadder") or LADDER_SHARED
        if ladder == LADDER_PUBLIC:
            owners = {str(p.get("owner_scope")) for p in
                      request.get("parties") or []}
            if len(owners) > 1:
                return ("PUBLIC ladder over multiple owner_scopes: the "
                        "director cannot consent on behalf of another mind")
        return None

    @staticmethod
    def _door_rule(request: Dict[str, Any]) -> Tuple[bool, str]:
        """§5.4: a new interface must improve without a competing source of truth."""
        proposal = request.get("door_proposal") or {}
        missing = [f for f in ("improves", "for_whom", "state_kept",
                               "governance")
                   if not proposal.get(f)]
        if missing:
            return False, f"door proposal names none of {missing}"
        for item in proposal.get("state_kept") or []:
            lowered = str(item).lower()
            if any(marker in lowered for marker in
                   ("memory", "database", "law", "authority", "substrate")):
                return False, (f"interface keeps competing state '{item}' — "
                               f"second database/shadow memory/separate "
                               f"authority (§4.7)")
        if not proposal.get("improves"):
            return False, "no named improvement"
        return True, "door satisfies §5.4"

    @staticmethod
    def _governance_export(request: Dict[str, Any]) -> Optional[str]:
        """§4.8: LAW state, gate config, constitutional deliberation stay home."""
        for entry in request.get("scope") or []:
            for cls in entry.get("content_classes") or []:
                lowered = str(cls).lower()
                if any(marker in lowered for marker in
                       ("law_state", "gate_config", "constitution",
                        "deliberation", "governance_internals")):
                    return f"scope names governance-internal class '{cls}'"
        return None
    # ------------------------------------------------------------------
    # Lifecycle: propose → validate → activate (§8)
    # ------------------------------------------------------------------
    def _record_transition(self, record: Dict[str, Any], before: str,
                           after: str, reason: str,
                           execution_id: str) -> Dict[str, Any]:
        frame = {"before": before, "after": after, "reason": reason,
                 "execution_id": execution_id, "at": _now_iso()}
        record.setdefault("transitions", []).append(frame)
        return frame

    def _emit_receipt(self, kind: str, payload: Dict[str, Any],
                      execution_id: str) -> Dict[str, Any]:
        receipt = {
            "node_id": NODE_ID,
            "node_version": NODE_VERSION,
            "receipt_kind": kind,          # establish|share|suspend|revoke|
                                          # supersede|reject|edge|space|drift|
                                          # interface|handshake|lease
            "execution_id": execution_id,
            "issued_at": _now_iso(),
            "payload": _deepcopy_json(payload),
        }
        receipt["receipt_hash"] = _sha256(
            {k: v for k, v in receipt.items() if k != "receipt_hash"})
        self.ledger.append(receipt)
        self.last_receipt = receipt
        return _deepcopy_json(receipt)

    def _idempotent(self, execution_id: str, action: str,
                    work) -> Dict[str, Any]:
        """§3.4: replaying a mutation with the same execution_id is safe."""
        if execution_id in self.mutations:
            original = self.mutations[execution_id]
            return _deepcopy_json({
                "replayed": True, "execution_id": execution_id,
                "action": action, "receipt": original.get("receipt"),
            })
        result = work()
        self.mutations[execution_id] = {
            "action": action,
            "receipt": _deepcopy_json(result.get("receipt")),
            "at": _now_iso(),
        }
        result = _deepcopy_json(result)
        result["replayed"] = False
        return result

    def propose(self, request: Dict[str, Any],
                context: Optional[Dict[str, Any]] = None,
                execution_id: Optional[str] = None) -> Dict[str, Any]:
        """Run the admission gate and record the connection proposal.

        On PASS: VALIDATED → ACTIVE for synchronous kinds (GRAPH_EDGE,
        INTERFACE_OPEN), CONSENT_PENDING for async kinds (MIND_LINK,
        SPACE_JOIN) until the handshake completes. On NEED_EVIDENCE the
        proposal is held inert (§8.3: never half-trust). On FAIL: REJECTED
        with refusal reasons — rejection receipts are first-class lineage
        (§13).
        """
        context = context or {}
        execution_id = execution_id or \
            f"prop-{_sha256(request.get('id') or '')[:12]}"

        def work():
            state = {
                "connection_request": request,
                "consent_registry": context.get("consent_registry") or {},
                "identity_bindings": context.get("identity_bindings") or {},
                "evidence_registry": context.get("evidence_registry") or {},
                "boundary_policy": context.get("boundary_policy") or {},
                "now": context.get("now") or _now_iso(),
            }
            result = self.gate(state)
            connection_id = str(request.get("id") or "unknown")
            if result.verdict == GateVerdict.FAIL:
                record = {
                    "connection_id": connection_id,
                    "state": C_REJECTED,
                    "request": _deepcopy_json(request),
                    "transitions": [],
                    "handshake": None,
                }
                self._record_transition(
                    record, C_PROPOSED, C_REJECTED,
                    "; ".join(result.reasons), execution_id)
                self.connections[connection_id] = record
                receipt = self._emit_receipt("reject", {
                    "connection_id": connection_id, "state": C_REJECTED,
                    "request": _deepcopy_json(request),
                    "refusal_reasons": result.reasons,
                    "prohibited": any(
                        any(code in reason for code in PROHIBITED_CODES)
                        for reason in result.reasons),
                    "transitions": record["transitions"],
                }, execution_id)
                return {"verdict": "REJECTED", "receipt": receipt,
                        "reasons": result.reasons}
            if result.verdict == GateVerdict.NEED_EVIDENCE:
                record = {
                    "connection_id": connection_id,
                    "state": C_CONSENT_PENDING,
                    "request": _deepcopy_json(request),
                    "transitions": [],
                    "handshake": {"steps": [], "complete": False,
                                  "window_expires": (
                                      _parse_ts(state["now"]) +
                                      timedelta(hours=24)).isoformat()
                                  if _parse_ts(state["now"]) else None},
                    "revoked_at": None,
                    "shared_manifest": [],
                    "calculus": self._calculus_posture(request),
                }
                self._record_transition(
                    record, C_PROPOSED, C_CONSENT_PENDING,
                    "; ".join(result.reasons), execution_id)
                self.connections[connection_id] = record
                receipt = self._emit_receipt("handshake", {
                    "connection_id": connection_id,
                    "state": C_CONSENT_PENDING,
                    "reasons": result.reasons,
                    "transitions": record["transitions"],
                }, execution_id)
                return {"verdict": "CONSENT_PENDING", "receipt": receipt,
                        "reasons": result.reasons}
            # PASS — synchronous kinds activate; async kinds need a handshake.
            kind = request.get("kind")
            if kind in (KIND_MIND_LINK, KIND_SPACE_JOIN):
                return self._start_handshake(connection_id, request,
                                             execution_id, result.reasons)
            return self._activate(connection_id, request, execution_id,
                                  result.reasons)

        return self._idempotent(execution_id, "propose", work)

    def _activate(self, connection_id: str, request: Dict[str, Any],
                  execution_id: str,
                  admit_reasons: List[str]) -> Dict[str, Any]:
        record = {
            "connection_id": connection_id,
            "state": C_VALIDATED,
            "request": _deepcopy_json(request),
            "transitions": [],
            "handshake": None,
            "revoked_at": None,
            "shared_manifest": [],
            "calculus": self._calculus_posture(request),
        }
        self._record_transition(record, C_PROPOSED, C_VALIDATED,
                                "admission gate passed", execution_id)
        self._record_transition(record, C_VALIDATED, C_ACTIVE,
                                "lease issued: "
                                f"{request.get('expiresAt') or 'no-expiry'}",
                                execution_id)
        record["state"] = C_ACTIVE
        self.connections[connection_id] = record
        # §10: validated connections become V2 edges (consent_ref required).
        edge = self._edge_for(request)
        receipt = self._emit_receipt("establish", {
            "connection_id": connection_id,
            "kind": request.get("kind"),
            "parties": _deepcopy_json(request.get("parties")),
            "consent_refs": list(request.get("consentRefs") or []),
            "purpose": request.get("purpose"),
            "scope": _deepcopy_json(request.get("scope")),
            "consent_ladder": request.get("consentLadder") or LADDER_SHARED,
            "boundary_policy": _deepcopy_json(
                request.get("boundaryPolicy")),
            "evidence_refs": list(request.get("evidenceRefs") or []),
            "lease_expiry": request.get("expiresAt"),
            "reversibility": request.get("reversibility"),
            "calculus": record["calculus"],
            "authority_basis": {
                "kind": "consent",
                "consent_refs": list(request.get("consentRefs") or []),
            },
            "edge": edge,
            "transitions": record["transitions"],
        }, execution_id)
        self.edge_ledger[connection_id] = edge
        return {"verdict": "ACTIVE", "receipt": receipt,
                "reasons": admit_reasons}

    def _start_handshake(self, connection_id: str, request: Dict[str, Any],
                         execution_id: str,
                         admit_reasons: List[str]) -> Dict[str, Any]:
        """§5.3 — the async handshake. No half-open trust (§8.3)."""
        record = {
            "connection_id": connection_id,
            "state": C_CONSENT_PENDING,
            "request": _deepcopy_json(request),
            "transitions": [],
            "handshake": {"steps": [], "complete": False,
                          "window_expires": (
                              datetime.now(timezone.utc) +
                              timedelta(hours=24)).isoformat()},
            "revoked_at": None,
            "shared_manifest": [],
            "calculus": self._calculus_posture(request),
        }
        self._record_transition(
            record, C_PROPOSED, C_CONSENT_PENDING,
            "async handshake opened (§5.3)", execution_id)
        self.connections[connection_id] = record
        receipt = self._emit_receipt("handshake", {
            "connection_id": connection_id, "state": C_CONSENT_PENDING,
            "steps_required": ["mutual_auth", "policy_exchange",
                               "consent_exchange", "capability_advertisement",
                               "lease_issuance"],
            "transitions": record["transitions"],
        }, execution_id)
        return {"verdict": "CONSENT_PENDING", "receipt": receipt,
                "reasons": admit_reasons + [
                    "CONNECT HANDSHAKE: complete §5.3 steps via "
                    "handshake_step(), then handshake_complete()"]}

    # ------------------------------------------------------------------
    # Handshake (§5.3), policy intersection, lease issuance
    # ------------------------------------------------------------------
    def handshake_step(self, connection_id: str, step: str,
                       payload: Dict[str, Any],
                       execution_id: str) -> Dict[str, Any]:
        """Record one §5.3 handshake step. Advertisement is never permission."""
        record = self.connections.get(connection_id)
        if record is None:
            raise KeyError(f"unknown connection {connection_id}")
        if record["state"] != C_CONSENT_PENDING:
            raise ValueError(
                f"handshake_step only in {C_CONSENT_PENDING}, "
                f"connection is {record['state']}")
        if step not in ("mutual_auth", "policy_exchange", "consent_exchange",
                        "capability_advertisement", "lease_issuance"):
            raise ValueError(f"unknown handshake step {step}")
        if step == "mutual_auth" and not payload.get("both_authenticated"):
            raise ValueError("mutual_auth requires both_authenticated=true")
        if step == "capability_advertisement":
            # §5.3 step 4: advertisement creates NO permission to have it done.
            payload = {**payload, "grants_nothing": True}

        def work():
            handshake = record["handshake"]
            handshake["steps"].append(
                {"step": step, "payload": _deepcopy_json(payload),
                 "at": _now_iso()})
            if step == "policy_exchange":
                # The connection runs under the STRICTER of the two policies:
                # intersection of permissions, union of forbiddens (§5.3).
                ours = _deepcopy_json(
                    record["request"].get("boundaryPolicy") or {})
                theirs = payload.get("policy") or {}
                record["intersected_policy"] = {
                    "version": f"{ours.get('version')}+{theirs.get('version')}",
                    "strictness": max(int(ours.get("strictness", 0)),
                                     int(theirs.get("strictness", 0))),
                    "forbidden_classes": sorted(set(
                        ours.get("forbidden_classes") or []) | set(
                        theirs.get("forbidden_classes") or [])),
                }
            receipt = self._emit_receipt("handshake", {
                "connection_id": connection_id, "step": step,
                "steps_done": [s["step"] for s in handshake["steps"]],
            }, execution_id)
            return {"verdict": record["state"], "receipt": receipt}

        return self._idempotent(execution_id, f"handshake:{step}", work)

    def handshake_complete(self, connection_id: str,
                           execution_id: str) -> Dict[str, Any]:
        """Close the handshake: all five §5.3 steps, else REJECTED."""
        record = self.connections.get(connection_id)
        if record is None:
            raise KeyError(f"unknown connection {connection_id}")
        if record["state"] != C_CONSENT_PENDING:
            raise ValueError(
                f"handshake_complete only in {C_CONSENT_PENDING}")
        required = {"mutual_auth", "policy_exchange", "consent_exchange",
                    "capability_advertisement", "lease_issuance"}
        done = {s["step"] for s in record["handshake"]["steps"]}
        if required - done:
            raise ValueError(f"handshake incomplete, missing "
                             f"{sorted(required - done)}")
        record["handshake"]["complete"] = True
        self._record_transition(
            record, C_CONSENT_PENDING, C_VALIDATED,
            "all §5.3 steps recorded", execution_id)
        self._record_transition(record, C_VALIDATED, C_ACTIVE,
                                "lease issued at handshake", execution_id)
        record["state"] = C_ACTIVE
        request = record["request"]
        edge = self._edge_for(request)
        receipt = self._emit_receipt("establish", {
            "connection_id": connection_id, "kind": request.get("kind"),
            "parties": _deepcopy_json(request.get("parties")),
            "consent_refs": list(request.get("consentRefs") or []),
            "purpose": request.get("purpose"),
            "scope": _deepcopy_json(request.get("scope")),
            "consent_ladder": request.get("consentLadder") or LADDER_SHARED,
            "boundary_policy": record.get("intersected_policy") or
            _deepcopy_json(request.get("boundaryPolicy")),
            "evidence_refs": list(request.get("evidenceRefs") or []),
            "lease_expiry": request.get("expiresAt"),
            "reversibility": request.get("reversibility"),
            "calculus": record["calculus"],
            "authority_basis": {"kind": "consent",
                                "consent_refs":
                                list(request.get("consentRefs") or [])},
            "edge": edge,
            "transitions": record["transitions"],
        }, execution_id)
        self.edge_ledger[connection_id] = edge
        return {"verdict": "ACTIVE", "receipt": receipt}

    def close_stale_handshakes(self, now: Optional[str] = None,
                               execution_id: Optional[str] = None
                               ) -> List[Dict[str, Any]]:
        """§8.3/§11: handshakes past their window fail closed to REJECTED."""
        now = now or _now_iso()
        execution_id = execution_id or f"close-{_sha256(now)[:12]}"
        closed = []
        for connection_id, record in self.connections.items():
            if record["state"] != C_CONSENT_PENDING:
                continue
            expires = (record.get("handshake") or {}).get("window_expires")
            if expires and _parse_ts(expires) and _parse_ts(now) and \
                    _parse_ts(expires) <= _parse_ts(now):
                self._record_transition(
                    record, C_CONSENT_PENDING, C_REJECTED,
                    "handshake window elapsed: fail closed, never half-trust",
                    execution_id)
                record["state"] = C_REJECTED
                closed.append(self._emit_receipt("reject", {
                    "connection_id": connection_id, "state": C_REJECTED,
                    "refusal_reasons": ["half-open handshake timed out "
                                        "(§8.3)"],
                    "transitions": record["transitions"],
                }, execution_id))
        return closed

    # ------------------------------------------------------------------
    # Transitions (§8.1): every move recorded, illegal moves fail closed
    # ------------------------------------------------------------------
    def apply_transition(self, connection_id: str, to_state: str,
                         reason: str, execution_id: str,
                         evidence_refs: Optional[List[str]] = None
                         ) -> Dict[str, Any]:
        record = self.connections.get(connection_id)
        if record is None:
            raise KeyError(f"unknown connection {connection_id}")
        from_state = record["state"]
        if to_state not in LEGAL_TRANSITIONS.get(from_state, frozenset()):
            raise ValueError(
                f"illegal transition {from_state} -> {to_state}: fail closed")

        def work():
            self._record_transition(record, from_state, to_state, reason,
                                    execution_id)
            record["state"] = to_state
            receipt = self._emit_receipt("transition", {
                "connection_id": connection_id,
                "transition": {"from": from_state, "to": to_state,
                               "reason": reason,
                               "evidence_refs": evidence_refs or []},
                "transitions": record["transitions"],
            }, execution_id)
            return {"verdict": to_state, "receipt": receipt}

        return self._idempotent(execution_id, f"transition:{to_state}", work)

    def suspend(self, connection_id: str, reason: str,
                execution_id: str) -> Dict[str, Any]:
        """Suspend on drift/scope request — fail-closed, not fail-polite (§4.6)."""
        return self.apply_transition(connection_id, C_SUSPENDED, reason,
                                     execution_id)

    def revoke(self, connection_id: str, reason: str, execution_id: str,
               now: Optional[str] = None) -> Dict[str, Any]:
        """§8.2: REVOKED stops future crossing immediately."""
        now = now or _now_iso()
        record = self.connections.get(connection_id)
        if record is None:
            raise KeyError(f"unknown connection {connection_id}")
        from_state = record["state"]
        if C_REVOKED not in LEGAL_TRANSITIONS.get(from_state, frozenset()):
            raise ValueError(f"illegal transition {from_state} -> "
                             f"{C_REVOKED}: fail closed")

        def work():
            self._record_transition(record, from_state, C_REVOKED, reason,
                                    execution_id)
            record["state"] = C_REVOKED
            record["revoked_at"] = now
            # §8.2: derived edges and shared manifests are marked STALE —
            # lineage is evidence, so nothing is deleted.
            edge = self.edge_ledger.get(connection_id)
            if edge is not None:
                edge["epistemic_state"] = "STALE"
                edge["status"] = "REVOKED"
            receipt = self._emit_receipt("revoke", {
                "connection_id": connection_id,
                "revoked_at": now,
                "reason": reason,
                # The revoking party's VERIFY audits what crossed (§8.2).
                "manifest_for_verify": _deepcopy_json(
                    record.get("shared_manifest") or []),
                "transitions": record["transitions"],
            }, execution_id)
            return {"verdict": C_REVOKED, "receipt": receipt}

        return self._idempotent(execution_id, "revoke", work)
    def supersede(self, connection_id: str, successor_id: str,
                  execution_id: str) -> Dict[str, Any]:
        """Supersession keeps the lineage frame: the old connection points
        at its successor; nothing is silently replaced (§8.1)."""
        if successor_id not in self.connections:
            raise KeyError(f"unknown successor connection {successor_id}")
        result = self.apply_transition(
            connection_id, C_SUPERSEDED,
            f"superseded by {successor_id} (lineage retained)", execution_id)
        record = self.connections[connection_id]
        record["superseded_by"] = successor_id
        result["superseded_by"] = successor_id
        return result

    def invalidate(self, connection_id: str, reason: str,
                   execution_id: str) -> Dict[str, Any]:
        """§4.1/§11: evidence shows the counterpart illegitimate → INVALID."""
        record = self.connections.get(connection_id)
        if record is None:
            raise KeyError(f"unknown connection {connection_id}")
        from_state = record["state"]
        if C_INVALID not in LEGAL_TRANSITIONS.get(from_state, frozenset()):
            raise ValueError(f"illegal transition {from_state} -> "
                             f"{C_INVALID}: fail closed")

        def work():
            self._record_transition(record, from_state, C_INVALID, reason,
                                    execution_id)
            record["state"] = C_INVALID
            # Poisoned edge: INVALIDATED + an INVALIDATES edge (§11).
            edge = self.edge_ledger.get(connection_id)
            if edge is not None:
                edge["epistemic_state"] = "INVALIDATED"
                edge["status"] = "INVALID"
            receipt = self._emit_receipt("invalidate", {
                "connection_id": connection_id, "reason": reason,
                "invalidates_edge": edge is not None,
                "transitions": record["transitions"],
            }, execution_id)
            return {"verdict": C_INVALID, "receipt": receipt}

        return self._idempotent(execution_id, "invalidate", work)

    # ------------------------------------------------------------------
    # Sharing: scope checked at EVERY crossing (§3.2)
    # ------------------------------------------------------------------
    def share(self, connection_id: str, crossing: Dict[str, Any],
              execution_id: str,
              consent_registry: Optional[Dict[str, Any]] = None,
              boundary_policy: Optional[Dict[str, Any]] = None,
              now: Optional[str] = None) -> Dict[str, Any]:
        """Share distilled context across an ACTIVE connection (§2.2).

        `crossing` = {content_class, content_hash, purpose, owner_scope,
        from_party, to_party, at}. Checks, in order: connection ACTIVE,
        lease live, scope allow-list (§3.2), purpose binding (§3.3),
        owner consent still valid (§3.1), policy floor (§2.3(6)),
        revocation race (§11). Violations fail closed and are receipted.
        """
        now = now or _now_iso()

        def work():
            record = self.connections.get(connection_id)
            if record is None:
                raise KeyError(f"unknown connection {connection_id}")
            request = record["request"]
            at = crossing.get("at") or now
            if record["state"] != C_ACTIVE:
                return self._share_refusal(
                    connection_id, f"connection is {record['state']}, "
                    f"not ACTIVE", crossing, execution_id)
            # Lease: expired leases refuse automatically (§8.1 diagram).
            expiry = request.get("expiresAt")
            if expiry and _parse_ts(expiry) and _parse_ts(now) and \
                    _parse_ts(expiry) <= _parse_ts(now):
                self._record_transition(
                    record, C_ACTIVE, C_REVOKED,
                    f"lease expired at {expiry}", execution_id)
                record["state"] = C_REVOKED
                record["revoked_at"] = expiry
                return self._share_refusal(
                    connection_id, "lease expired → REVOKED", crossing,
                    execution_id)
            # Revocation race (§11): crossings after the revocation
            # timestamp are violations, receipted and reported.
            if record.get("revoked_at") and _parse_ts(at) and \
                    _parse_ts(record["revoked_at"]) and \
                    _parse_ts(at) > _parse_ts(record["revoked_at"]):
                return self._share_violation(
                    connection_id, "E_REVOCATION_RACE",
                    f"crossing at {at} after revocation at "
                    f"{record['revoked_at']}", crossing, execution_id)
            # Scope: closed-world allow-list, checked at every crossing.
            allowed = self._scope_allows(request, crossing)
            if not allowed:
                return self._share_refusal(
                    connection_id,
                    f"{E_SCOPE_CREEP}: class "
                    f"{crossing.get('content_class')} not in scope allow-list",
                    crossing, execution_id)
            # Purpose binding: use beyond the stated purpose (§3.3).
            if crossing.get("purpose") != request.get("purpose"):
                return self._purpose_drift(connection_id, crossing,
                                           execution_id)
            # Owner consent still valid at crossing time.
            ok_consent, consent_gap = self._consents_valid(
                request, consent_registry or {}, now)
            if not ok_consent:
                return self._share_violation(
                    connection_id, E_CONSENT_MISSING,
                    "; ".join(consent_gap), crossing, execution_id)
            # Policy floor on the crossing class (§2.3(6)).
            forbidden = set(
                (boundary_policy or {}).get("forbidden_classes") or []) | \
                set((request.get("boundaryPolicy") or {})
                    .get("forbidden_classes") or [])
            if str(crossing.get("content_class")).upper() in \
                    {str(f).upper() for f in forbidden}:
                return self._share_violation(
                    connection_id, E_PROHIBITED_CROSSING,
                    f"class {crossing.get('content_class')} forbidden by "
                    f"policy", crossing, execution_id)
            # Crossing authorized: record the manifest entry (hashes, never
            # raw content) and emit the share receipt.
            manifest_entry = {
                "connection_id": connection_id,
                "content_class": crossing.get("content_class"),
                "content_hash": crossing.get("content_hash"),
                "from_party": crossing.get("from_party"),
                "to_party": crossing.get("to_party"),
                "owner_scope": crossing.get("owner_scope"),
                "purpose": crossing.get("purpose"),
                "at": at,
            }
            record["shared_manifest"].append(manifest_entry)
            receipt = self._emit_receipt("share", {
                "connection_id": connection_id,
                "crossing": _deepcopy_json(crossing),
                "manifest_entry": manifest_entry,
            }, execution_id)
            return {"verdict": "SHARED", "receipt": receipt}

        return self._idempotent(execution_id, "share", work)

    def _scope_allows(self, request: Dict[str, Any],
                      crossing: Dict[str, Any]) -> bool:
        """Closed-world scope check (§3.2): anything not named does not cross."""
        cls = crossing.get("content_class")
        owner = crossing.get("owner_scope")
        for entry in request.get("scope") or []:
            if str(entry.get("owner_scope")) == str(owner) and \
                    cls in (entry.get("content_classes") or []):
                return True
        return False

    def _share_refusal(self, connection_id: str, detail: str,
                       crossing: Dict[str, Any],
                       execution_id: str) -> Dict[str, Any]:
        receipt = self._emit_receipt("share_refused", {
            "connection_id": connection_id, "detail": detail,
            "crossing": _deepcopy_json(crossing),
        }, execution_id)
        return {"verdict": "REFUSED", "receipt": receipt, "detail": detail}

    def _share_violation(self, connection_id: str, code: str, detail: str,
                         crossing: Dict[str, Any],
                         execution_id: str) -> Dict[str, Any]:
        """Cross-owner leakage attempts are critical findings (§11)."""
        record = self.connections[connection_id]
        receipt = self._emit_receipt("violation", {
            "connection_id": connection_id, "code": code, "detail": detail,
            "crossing": _deepcopy_json(crossing),
            "severity": "CRITICAL" if code == E_CROSS_OWNER_LEAKAGE
            else "HIGH",
            "notify": "affected owner's VERIFY + connection ledger",
        }, execution_id)
        return {"verdict": "VIOLATION", "receipt": receipt,
                "code": code, "detail": detail}

    def _purpose_drift(self, connection_id: str, crossing: Dict[str, Any],
                       execution_id: str) -> Dict[str, Any]:
        """§3.3/§4.6: drift suspends first; the crossing is refused."""
        record = self.connections[connection_id]
        from_state = record["state"]
        self._record_transition(
            record, from_state, C_SUSPENDED,
            f"{E_PURPOSE_DRIFT}: shared purpose "
            f"{crossing.get('purpose')!r} != connection purpose "
            f"{record['request'].get('purpose')!r} — fail-closed, pending "
            f"review", execution_id)
        record["state"] = C_SUSPENDED
        receipt = self._emit_receipt("drift", {
            "connection_id": connection_id, "code": E_PURPOSE_DRIFT,
            "expected_purpose": record["request"].get("purpose"),
            "observed_purpose": crossing.get("purpose"),
            "crossing": _deepcopy_json(crossing),
            "transitions": record["transitions"],
            "review": "SUSPENDED pending review; confirmed drift → REVOKED",
        }, execution_id)
        return {"verdict": "SUSPENDED", "receipt": receipt,
                "code": E_PURPOSE_DRIFT}

    def confirm_drift(self, connection_id: str, execution_id: str
                      ) -> Dict[str, Any]:
        """Confirmed purpose drift → REVOKED (§4.6)."""
        return self.revoke(connection_id,
                           "purpose drift confirmed on review", execution_id)

    def clear_review(self, connection_id: str, execution_id: str,
                     reviewer: str) -> Dict[str, Any]:
        """SUSPENDED → ACTIVE after human review clears the finding."""
        return self.apply_transition(
            connection_id, C_ACTIVE,
            f"review cleared by {reviewer}; scope unchanged "
            f"(never silently widened, §3.2)", execution_id)

    def narrow_scope(self, connection_id: str,
                     new_scope: List[Dict[str, Any]],
                     execution_id: str) -> Dict[str, Any]:
        """A connection's scope may narrow; it may never silently widen (§3.2)."""
        record = self.connections.get(connection_id)
        if record is None:
            raise KeyError(f"unknown connection {connection_id}")
        old = {(str(e.get("owner_scope")), c)
               for e in record["request"].get("scope") or []
               for c in (e.get("content_classes") or [])}
        new = {(str(e.get("owner_scope")), c)
               for e in new_scope
               for c in (e.get("content_classes") or [])}
        widened = new - old
        if widened:
            raise ValueError(
                f"scope widening refused (§3.2): {sorted(widened)}; a new "
                f"consent-gated proposal is required")
        record["request"]["scope"] = _deepcopy_json(new_scope)
        receipt = self._emit_receipt("transition", {
            "connection_id": connection_id,
            "transition": {"from": "SCOPE", "to": "SCOPE",
                           "reason": "scope narrowed (widening refused)",
                           "narrowed_from": sorted(old), "narrowed_to":
                           sorted(new)},
        }, execution_id)
        return {"verdict": "SCOPE_NARROWED", "receipt": receipt}
    # ------------------------------------------------------------------
    # Retrieval: the V2 selector view (§10, §7 battery item)
    # ------------------------------------------------------------------
    def retrieve(self, connection_id: str) -> Optional[Dict[str, Any]]:
        """What the V2 selector may serve.

        REVOKED/SUSPENDED/INVALID connections are INVISIBLE to retrieval
        (fail-closed to the selector) while remaining visible as lineage —
        the connection ledger keeps every receipt.
        """
        record = self.connections.get(connection_id)
        if record is None:
            return None
        if record["state"] not in (C_ACTIVE, C_VALIDATED):
            return None
        edge = _deepcopy_json(self.edge_ledger.get(connection_id) or {})
        return {
            "connection_id": connection_id,
            "state": record["state"],
            "kind": record["request"].get("kind"),
            "purpose": record["request"].get("purpose"),
            "scope": _deepcopy_json(record["request"].get("scope")),
            "edge": edge,
        }

    def lineage(self, connection_id: str) -> Optional[Dict[str, Any]]:
        """Everything, including terminal states — lineage is evidence."""
        record = self.connections.get(connection_id)
        if record is None:
            return None
        return {
            "connection_id": connection_id,
            "state": record["state"],
            "transitions": _deepcopy_json(record.get("transitions") or []),
            "shared_manifest": _deepcopy_json(
                record.get("shared_manifest") or []),
            "superseded_by": record.get("superseded_by"),
            "revoked_at": record.get("revoked_at"),
        }

    # ------------------------------------------------------------------
    # §10 — the connection → V2 edge binding
    # ------------------------------------------------------------------
    def _edge_for(self, request: Dict[str, Any]) -> Dict[str, Any]:
        kind = request.get("kind")
        relationship_type = {
            KIND_MIND_LINK: EDGE_CONNECTED_TO,
            KIND_SPACE_JOIN: EDGE_MEMBER_OF,
            KIND_GRAPH_EDGE: EDGE_SUPPORTS,
            KIND_INTERFACE_OPEN: EDGE_CONNECTED_TO,
        }.get(kind, EDGE_CONNECTED_TO)
        parties = request.get("parties") or []
        scopes = [str(p.get("owner_scope")) for p in parties]
        return {
            "relationship_id": request.get("id"),
            "source_id": str(parties[0].get("identity")) if parties else None,
            "target_id": str(parties[1].get("identity"))
            if len(parties) > 1 else None,
            "relationship_type": relationship_type,
            # Cross-owner edges carry BOTH parties' scopes (§10).
            "owner_scope": "+".join(sorted(set(scopes))) or None,
            "epistemic_state": "CONNECTED",
            "status": "ACTIVE",
            "provenance": {"node": NODE_ID, "kind": "connection_receipt"},
            "evidence_refs": list(request.get("evidenceRefs") or []),
            "valid_from": _now_iso(),
            "valid_until": request.get("expiresAt"),
            # Consent-gated retrieval: the selector MUST have consent_refs.
            "consent_ref": list(request.get("consentRefs") or []),
            "applicability": {
                "purpose": request.get("purpose"),
                "scope": _deepcopy_json(request.get("scope")),
            },
            "reason_codes": ["CONNECT_VALIDATED"] +
            ([kind] if kind in (KIND_MIND_LINK, KIND_SPACE_JOIN) else []),
        }

    # ------------------------------------------------------------------
    # Internal surface: synchronous graph operations (§8.3)
    # ------------------------------------------------------------------
    def validate_edge(self, request: Dict[str, Any],
                      context: Optional[Dict[str, Any]] = None,
                      execution_id: Optional[str] = None) -> Dict[str, Any]:
        """GRAPH_EDGE validation: evidence for the relationship plus consent.

        §4.1: a relationship justified by proximity or semantic similarity
        alone is refused — the mechanical form of 'relationship semantics
        require evidence'.
        """
        if request.get("kind") != KIND_GRAPH_EDGE:
            raise ValueError("validate_edge only serves GRAPH_EDGE requests")
        return self.propose(request, context, execution_id)

    def resolve_relationship(self, source_id: str, target_id: str,
                             ) -> Optional[Dict[str, Any]]:
        """What relationship (if any) CONNECT holds between two blocks."""
        for connection_id, record in self.connections.items():
            parties = record["request"].get("parties") or []
            identities = {str(p.get("identity")) for p in parties}
            if {source_id, target_id} <= identities and \
                    record["state"] == C_ACTIVE:
                return self.retrieve(connection_id)
        return None

    def traverse(self, start_identity: str, max_hops: int = 3,
                 purpose: Optional[str] = None) -> List[Dict[str, Any]]:
        """Bounded, deterministic traversal over ACTIVE connections only."""
        adjacency: Dict[str, List[str]] = {}
        for record in self.connections.values():
            if record["state"] != C_ACTIVE:
                continue
            if purpose is not None and \
                    record["request"].get("purpose") != purpose:
                continue
            parties = record["request"].get("parties") or []
            identities = [str(p.get("identity")) for p in parties]
            for identity in identities:
                for other in identities:
                    if other != identity:
                        adjacency.setdefault(identity, []).append(other)
        seen = {start_identity}
        frontier = [start_identity]
        hops: List[Dict[str, Any]] = []
        for _ in range(max(0, max_hops)):
            nxt: List[str] = []
            for node in sorted(frontier):
                for neighbor in sorted(adjacency.get(node, [])):
                    if neighbor not in seen:
                        seen.add(neighbor)
                        nxt.append(neighbor)
                        hops.append({"from": node, "to": neighbor})
            if not nxt:
                break
            frontier = nxt
        return hops

    def rank_relevance(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Deterministic recorded ranking over ACTIVE edges (§8.3).

        Scoring inputs are explicit (purpose match, scope overlap, consent
        ladder rank, recency); the ranking function is recorded on the
        receipt-equivalent so a cold successor can re-derive it.
        """
        purpose = query.get("purpose")
        scope_classes = set(query.get("content_classes") or [])
        scored: List[Dict[str, Any]] = []
        for connection_id, record in self.connections.items():
            if record["state"] != C_ACTIVE:
                continue
            request = record["request"]
            purpose_match = 1.0 if request.get("purpose") == purpose else 0.0
            edge_classes = {c for e in request.get("scope") or []
                            for c in (e.get("content_classes") or [])}
            scope_overlap = len(scope_classes & edge_classes)
            ladder_rank = LADDER_RANK.get(
                request.get("consentLadder") or LADDER_SHARED, 0)
            score = purpose_match * 4 + scope_overlap * 2 + ladder_rank
            scored.append({"connection_id": connection_id, "score": score,
                           "factors": {"purpose_match": purpose_match,
                                       "scope_overlap": scope_overlap,
                                       "ladder_rank": ladder_rank}})
        scored.sort(key=lambda r: (-r["score"], r["connection_id"]))
        return scored

    def assess_applicability(self, connection_id: str,
                             use: Dict[str, Any]) -> Dict[str, Any]:
        """Are the applicability conditions satisfied for this use?"""
        record = self.connections.get(connection_id)
        if record is None:
            return {"applicable": False, "reason": "unknown connection"}
        if record["state"] != C_ACTIVE:
            return {"applicable": False,
                    "reason": f"connection is {record['state']}"}
        request = record["request"]
        if use.get("purpose") != request.get("purpose"):
            return {"applicable": False,
                    "reason": f"purpose binding: {use.get('purpose')!r} != "
                    f"{request.get('purpose')!r}"}
        if not self._scope_allows(
                request, {"content_class": use.get("content_class"),
                          "owner_scope": use.get("owner_scope")}):
            return {"applicable": False, "reason": "scope allow-list"}
        return {"applicable": True, "reason": "purpose + scope satisfied"}

    def explain_connection(self, connection_id: str) -> Dict[str, Any]:
        """The five cold-successor questions for one connection (§13)."""
        record = self.connections.get(connection_id)
        if record is None:
            raise KeyError(f"unknown connection {connection_id}")
        request = record["request"]
        return {
            "connection_id": connection_id,
            "state": record["state"],
            "who": [{"identity": p.get("identity"),
                     "owner_scope": p.get("owner_scope"),
                     "role": p.get("role")}
                    for p in request.get("parties") or []],
            "under_what_consent": list(request.get("consentRefs") or []),
            "what_crossed": _deepcopy_json(
                record.get("shared_manifest") or []),
            "boundary_policy": _deepcopy_json(
                request.get("boundaryPolicy")),
            "transitions": _deepcopy_json(record.get("transitions") or []),
        }

    def applicable_context(self, connection_id: str,
                           query_scope: Dict[str, Any]) -> Dict[str, Any]:
        """What context ACT may see through this connection — measured, not
        asserted (spec §14 battery item 11: connection changes the context
        ACT can see)."""
        record = self.connections.get(connection_id)
        if record is None or record["state"] != C_ACTIVE:
            return {"connection_id": connection_id, "visible": [],
                    "reason": f"connection is "
                    f"{record['state'] if record else 'unknown'}"}
        request = record["request"]
        visible = [
            {"content_class": cls, "owner_scope": entry.get("owner_scope"),
             "purpose": request.get("purpose")}
            for entry in request.get("scope") or []
            for cls in (entry.get("content_classes") or [])
            if query_scope.get("content_class") in (None, cls)
        ]
        return {"connection_id": connection_id, "visible": visible,
                "reason": "scope allow-list within purpose binding"}
    # ------------------------------------------------------------------
    # Connection spaces (§6): bounded multi-party contexts, chartered
    # ------------------------------------------------------------------
    def create_space(self, space: Dict[str, Any],
                     execution_id: str) -> Dict[str, Any]:
        """A space is a projection over the canonical substrate — no parallel
        stores, identity, or governance of its own (§6)."""
        missing = [f for f in ("id", "charter") if not space.get(f)]
        if missing:
            raise ValueError(f"space missing {missing}")
        charter = space.get("charter") or {}
        for field in ("purpose", "membership_rules", "retention_policy"):
            if not charter.get(field):
                raise ValueError(
                    f"charter must state {field} at creation (§6)")

        def work():
            space_id = str(space["id"])
            if space_id in self.spaces:
                raise ValueError(f"space {space_id} already exists")
            record = {
                "space_id": space_id,
                "charter": _deepcopy_json(charter),
                "charter_version": 1,
                "members": [],           # [{identity, owner_scope, consent_ref}]
                "boundary_policy": _deepcopy_json(
                    space.get("boundaryPolicy") or {}),
                "shared_ledger": [],     # hashes + receipts, never content
                "created_at": _now_iso(),
                "state": SPACE_ACTIVE,
                "history": [],
            }
            record["history"].append({"event": "created",
                                      "at": record["created_at"],
                                      "execution_id": execution_id})
            self.spaces[space_id] = record
            receipt = self._emit_receipt("space", {
                "space_id": space_id, "event": "created",
                "charter": _deepcopy_json(charter),
            }, execution_id)
            return {"verdict": SPACE_ACTIVE, "receipt": receipt}

        return self._idempotent(execution_id, "create_space", work)

    def join_space(self, space_id: str, member: Dict[str, Any],
                   execution_id: str,
                   member_consents: Optional[Dict[str, List[str]]] = None,
                   ) -> Dict[str, Any]:
        """Entry requires the entrant's consent to the charter AND existing
        members' consent per the charter's admission rule (§6.1)."""
        space = self.spaces.get(space_id)
        if space is None:
            raise KeyError(f"unknown space {space_id}")
        if space["state"] != SPACE_ACTIVE:
            raise ValueError(f"space {space_id} is {space['state']}")
        if not member.get("consent_ref"):
            raise ValueError(
                f"member {member.get('identity')}: no consent_ref to the "
                f"charter — entry is consent-gated (§6.1)")
        admission = (space["charter"].get("membership_rules") or {}).get(
            "admission", "charter-consent")
        if admission == "unanimous" and space["members"]:
            approvers = set(member_consents or {}).get(space_id, [])
            member_ids = {m["identity"] for m in space["members"]}
            if not member_ids <= set(approvers):
                raise ValueError(
                    "admission=unanimous: every existing member must consent")

        def work():
            entry = {"identity": member.get("identity"),
                     "owner_scope": member.get("owner_scope"),
                     "consent_ref": member.get("consent_ref"),
                     "joined_at": _now_iso(),
                     "charter_version": space["charter_version"]}
            space["members"].append(entry)
            space["history"].append({"event": "joined",
                                     "identity": entry["identity"],
                                     "at": entry["joined_at"],
                                     "execution_id": execution_id})
            receipt = self._emit_receipt("space", {
                "space_id": space_id, "event": "joined", "member": entry,
            }, execution_id)
            return {"verdict": "JOINED", "receipt": receipt}

        return self._idempotent(execution_id, f"join_space:{space_id}", work)

    def exit_space(self, space_id: str, identity: str,
                   execution_id: str) -> Dict[str, Any]:
        """Exit is unilateral and immediate for future sharing (§6.1)."""
        space = self.spaces.get(space_id)
        if space is None:
            raise KeyError(f"unknown space {space_id}")

        def work():
            before = len(space["members"])
            space["members"] = [m for m in space["members"]
                                if m["identity"] != identity]
            if len(space["members"]) == before:
                raise ValueError(f"{identity} is not a member of {space_id}")
            retention = (space["charter"].get("retention_policy") or {})
            space["history"].append({
                "event": "exited", "identity": identity, "at": _now_iso(),
                "retention_applied": retention.get(
                    "after_exit", "no retention beyond participation"),
                "execution_id": execution_id})
            receipt = self._emit_receipt("space", {
                "space_id": space_id, "event": "exited",
                "identity": identity,
                "retention_applied": retention.get(
                    "after_exit", "no retention beyond participation"),
            }, execution_id)
            return {"verdict": "EXITED", "receipt": receipt}

        return self._idempotent(execution_id, f"exit_space:{space_id}", work)

    def change_charter(self, space_id: str, new_charter: Dict[str, Any],
                       member_consents: List[str],
                       execution_id: str) -> Dict[str, Any]:
        """Charter changes (purpose, retention, admission) require re-consent
        from ALL members. A space cannot silently re-purpose itself (§6.1)."""
        space = self.spaces.get(space_id)
        if space is None:
            raise KeyError(f"unknown space {space_id}")

        def work():
            member_ids = [m["identity"] for m in space["members"]]
            if set(member_consents) != set(member_ids) or \
                    len(member_consents) != len(member_ids):
                raise ValueError(
                    "charter change requires re-consent from every member; "
                    f"have {sorted(member_consents)}, need "
                    f"{sorted(member_ids)}")
            space["charter"] = _deepcopy_json(new_charter)
            space["charter_version"] += 1
            space["history"].append({
                "event": "charter_changed",
                "charter_version": space["charter_version"],
                "reconsents": sorted(member_consents), "at": _now_iso(),
                "execution_id": execution_id})
            receipt = self._emit_receipt("space", {
                "space_id": space_id, "event": "charter_changed",
                "charter_version": space["charter_version"],
                "reconsents": sorted(member_consents),
            }, execution_id)
            return {"verdict": "CHARTER_CHANGED", "receipt": receipt}

        return self._idempotent(execution_id,
                               f"change_charter:{space_id}", work)

    def dissolve_space(self, space_id: str, execution_id: str) -> Dict[str,
                                                                       Any]:
        """DISSOLVED: no new crossing; the shared ledger remains as lineage."""
        space = self.spaces.get(space_id)
        if space is None:
            raise KeyError(f"unknown space {space_id}")

        def work():
            space["state"] = SPACE_DISSOLVED
            space["history"].append({"event": "dissolved", "at": _now_iso(),
                                     "execution_id": execution_id})
            receipt = self._emit_receipt("space", {
                "space_id": space_id, "event": "dissolved",
                "ledger_retained_as_lineage":
                len(space["shared_ledger"]),
            }, execution_id)
            return {"verdict": SPACE_DISSOLVED, "receipt": receipt}

        return self._idempotent(execution_id,
                               f"dissolve_space:{space_id}", work)

    # ------------------------------------------------------------------
    # Doors: new interfaces (§5.4). Every interface is a projection and
    # transport surface — no interface becomes an independent brain (§5.2).
    # ------------------------------------------------------------------
    def open_interface(self, request: Dict[str, Any],
                       context: Optional[Dict[str, Any]] = None,
                       execution_id: Optional[str] = None) -> Dict[str, Any]:
        """INTERFACE_OPEN runs the full refusal ladder (§4.7/§5.4 included)."""
        if request.get("kind") != KIND_INTERFACE_OPEN:
            raise ValueError("open_interface only serves INTERFACE_OPEN")
        result = self.propose(request, context, execution_id)
        if result["verdict"] == "ACTIVE":
            interface_id = str(request.get("id"))
            self.interfaces[interface_id] = {
                "interface_id": interface_id,
                "door_proposal": _deepcopy_json(
                    request.get("door_proposal") or {}),
                "opened_at": _now_iso(),
                "state": "OPEN",
            }
        return result

    def audit_interface(self, interface_id: str) -> Dict[str, Any]:
        """§5.2/§11: an interface accumulating competing state gets
        disconnected, not promoted."""
        record = self.interfaces.get(interface_id)
        if record is None:
            raise KeyError(f"unknown interface {interface_id}")
        proposal = record.get("door_proposal") or {}
        kept = proposal.get("state_kept") or []
        competing = [s for s in kept if any(
            marker in str(s).lower()
            for marker in ("memory", "database", "law", "authority",
                           "substrate"))]
        if competing:
            record["state"] = "DISCONNECTED"
            receipt = self._emit_receipt("interface", {
                "interface_id": interface_id, "event": "disconnected",
                "competing_state": competing,
                "brief": "door-rule violation: interface keeps independent "
                         "state (§5.2); Director notified",
            }, f"audit-{interface_id}")
            return {"verdict": "DISCONNECTED", "receipt": receipt}
        return {"verdict": "OPEN", "note": "interface remains stateless "
                                           "by rule"}

    # ------------------------------------------------------------------
    # §9 — calculus gate posture (aspirational; the math is CANDIDATE)
    # ------------------------------------------------------------------
    def _calculus_posture(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Records the §9.2 posture without letting a score authorize.

        Hard refusals (§4.2/§4.4/§2.3) are PROHIBITED regardless of any
        score. Cross-owner connections additionally require ADMISSIBLE ∧
        Q ≥ 9.0 ∧ V_safe > 0 ∧ reversibility ≥ 7 — computed here so the
        posture is inspectable, but marked aspirational until the calculus
        is ratified.
        """
        owners = {str(p.get("owner_scope")) for p in
                  request.get("parties") or []}
        cross_owner = len(owners) > 1
        ladder = request.get("consentLadder") or LADDER_SHARED
        reversibility = float(request.get("reversibility") or 0)
        evidence_count = len(request.get("evidenceRefs") or [])
        # Proxy quality inputs (explicit, bounded; not a substitute for Q).
        evidence_sufficiency = min(10.0, evidence_count * 2.0)
        q_proxy = round((evidence_sufficiency + reversibility) / 2, 2)
        v_safe_proxy = round(
            (1.0 if ladder in (LADDER_PRIVATE, LADDER_SHARED) else 0.5)
            - (0.5 if cross_owner else 0.0), 2)
        admissible = q_proxy >= 9.0 and v_safe_proxy > 0 and \
            reversibility >= 7 if cross_owner else True
        return {
            "calculusVersion": "v2.1-CANDIDATE",
            "configHash": "calculus-not-ratified",
            "aspirational": True,
            "note": CALCULUS_CANDIDATE_NOTE,
            "cross_owner": cross_owner,
            "q_proxy": q_proxy,
            "v_safe_proxy": v_safe_proxy,
            "gate": "ADMISSIBLE" if admissible else "NEEDS_EVIDENCE",
        }

    # ------------------------------------------------------------------
    # Receipts: recompute + cold reconstruction (§7, §13)
    # ------------------------------------------------------------------
    @staticmethod
    def _verify_receipt_hash(receipt: Dict[str, Any]) -> bool:
        claimed = (receipt or {}).get("receipt_hash")
        if not claimed:
            return False
        content = {k: v for k, v in receipt.items()
                   if k != "receipt_hash"}
        return _sha256(content) == claimed

    def recompute(self, receipt: Dict[str, Any]) -> str:
        """Re-derive a receipt's hash AND re-evaluate its gate outcome.

        Returns MATCH only when both the hash verifies and the stored inputs
        re-evaluate to the recorded verdict. MISMATCH suspends the
        connection (§14 battery item 6: provenance loss is detected).
        """
        if not self._verify_receipt_hash(receipt):
            return "MISMATCH"
        payload = receipt.get("payload") or {}
        kind = receipt.get("receipt_kind")
        if kind in ("reject", "establish"):
            connection_id = payload.get("connection_id")
            record = self.connections.get(connection_id)
            expected = {"reject": "REJECTED",
                        "establish": "ACTIVE"}.get(kind)
            if record is None:
                # Cold path: hash verified but no live record — the receipt
                # itself carries everything needed for cold_reconstruct.
                return "MATCH"
            actual = record.get("state")
            if kind == "establish":
                return "MATCH" if actual == expected else "MISMATCH"
            return "MATCH" if actual == expected else "MISMATCH"
        return "MATCH"

    def cold_reconstruct(self, receipts: List[Dict[str, Any]]
                         ) -> Dict[str, Any]:
        """§13 — the five cold-successor questions, from receipts alone.

        A genuinely cold agent given the receipt set must reconstruct: (1)
        who is connected to whom and in what state; (2) under what consent
        each connection operates; (3) what crossed each boundary; (4) the
        boundary policy at any point; (5) what was refused and why.
        """
        connections: Dict[str, Dict[str, Any]] = {}
        consent_state: Dict[str, Dict[str, Any]] = {}
        crossed: List[Dict[str, Any]] = []
        policy_history: List[Dict[str, Any]] = []
        refusals: List[Dict[str, Any]] = []
        spaces: Dict[str, Dict[str, Any]] = {}
        for receipt in receipts:
            if not self._verify_receipt_hash(receipt):
                continue  # forged/corrupt receipts are not lineage
            payload = receipt.get("payload") or {}
            kind = receipt.get("receipt_kind")
            if kind == "establish":
                connection_id = payload.get("connection_id")
                connections[connection_id] = {
                    "state": payload.get("transitions", [{}])[-1].get(
                        "after", "ACTIVE"),
                    "parties": payload.get("parties"),
                    "consent_refs": payload.get("consent_refs"),
                    "purpose": payload.get("purpose"),
                    "scope": payload.get("scope"),
                    "boundary_policy": payload.get("boundary_policy"),
                    "lease_expiry": payload.get("lease_expiry"),
                }
                policy = payload.get("boundary_policy") or {}
                if policy.get("version"):
                    policy_history.append({
                        "at": receipt.get("issued_at"),
                        "version": policy.get("version"),
                        "forbidden_classes": policy.get("forbidden_classes"),
                        "strictness": policy.get("strictness"),
                    })
            elif kind == "share":
                crossed.append(payload.get("manifest_entry") or {})
            elif kind in ("reject", "violation"):
                refusals.append({
                    "connection_id": payload.get("connection_id"),
                    "kind": kind,
                    "reasons": payload.get("refusal_reasons") or
                    [payload.get("code")],
                })
            elif kind == "revoke":
                connection_id = payload.get("connection_id")
                if connection_id in connections:
                    connections[connection_id]["state"] = "REVOKED"
            elif kind == "transition":
                transition = payload.get("transition") or {}
                connection_id = payload.get("connection_id")
                if connection_id in connections and transition.get("to"):
                    connections[connection_id]["state"] = transition["to"]
            elif kind == "space":
                space_id = payload.get("space_id")
                spaces[space_id] = {
                    "event": payload.get("event"),
                    "charter": payload.get("charter"),
                }
        return {
            "connections": connections,
            "consent_state": consent_state,
            "what_crossed": crossed,
            "policy_history": sorted(
                policy_history, key=lambda p: (p.get("at") or "")),
            "refusals": refusals,
            "spaces": spaces,
            "hash_verified_receipts": len([r for r in receipts
                                          if self._verify_receipt_hash(r)]),
            "forged_receipts_skipped": len(receipts) - len(
                [r for r in receipts if self._verify_receipt_hash(r)]),
        }
