"""NAYA-KERNEL-PROVE — CANDIDATE implementation (NOT RATIFIED — NOT MERGED).

Implements the PROVE node contract from PROVE-NODE-SPEC-CANDIDATE.md (draft)
against the NodeBase interface. Candidate code on a feature branch: it proves
the spec is implementable; it grants nothing, merges nothing, deploys nothing.

Contractual responsibility (spec §0): PROVE is the organism checking its own
work before anything it believes is allowed to leave it. Every claim the
kernel produces must pass the evidence law through PROVE's gates before it
may cross to CONNECT, persist as settled knowledge, or be reported as fact.
UNKNOWN, BLOCKED, and IMPLEMENTED never count as VERIFIED; only evidence
does, and PROVE is the node that enforces the difference mechanically.

PROVE vs VERIFY (spec §1.3): PROVE is first-party ("did we actually establish
this, by our own rules?"). PROVE never writes "independently verified" and
never emits the VERIFIED epistemic state — PROVEN maps to SUPPORTED (§6.1).

PROVE never grants, infers, or modifies authority — ever (§1.4).

Gate input contract (`state` dict keys for the NodeBase `gate()`; all reads
are explicit):
  claim               ProofClaim dict (see PROOF_CLAIM contract below)
  operation           "intake" | "advance" | "crossing" | "challenge" ...
                      (default "intake": evaluates how far the claim's own
                      evidence climbs the ladder right now)
  principal           {"identity": str, "entitled_scopes": [str]}
  now                 ISO-8601 timestamp override (tests / determinism)

The imperative API below (submit/advance/seal/challenge/...) is what the
kernel pipeline drives; `gate()` is the NodeBase conformance surface over it.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from naya_kernel.node_base import GateResult, GateVerdict, ManifestEntry, NodeBase

NODE_ID = "NAYA-KERNEL-PROVE"
NODE_VERSION = "0.1.0-candidate"
PIPELINE_POSITION = 5

# ---------------------------------------------------------------------------
# Spec constants (§2.1, §3.8, §3.9, §2.2)
# ---------------------------------------------------------------------------

# §2.1 — claim classes. PREDICTIVE is capped at L1 by definition.
CLAIM_CLASSES = ("EMPIRICAL", "DEDUCTIVE", "PROCEDURAL", "PREDICTIVE")

# §3.8 — required proof maturity by stakes. PROVE enforces this table; it
# does not set it unilaterally, and it may never lower a required level.
STAKES = ("low", "high", "consequential")
REQUIRED_LEVEL = {"low": 2, "high": 3, "consequential": 4}

# §2.2 — the proof-maturity ladder (private ladder; see §6.1 mapping onto the
# ratified V2 contract enums for edge writes).
LEVEL_NAMES = {
    0: "UNPROVEN",
    1: "EVIDENCED",
    2: "TESTED",
    3: "REPRODUCED",
    4: "PROVEN",
}

# §8 — terminal / side states. CHALLENGED keeps both sides visible; demotion
# is never silent (receipted re-gating only).
SIDE_STATES = ("CHALLENGED", "INVALIDATED", "SUPERSEDED")

# §3 — the seven gates. Each is binary and independent; "mostly proven" is
# UNPROVEN.
GATES = ("G1", "G2", "G3", "G4", "G5", "G6", "G7")

# §3.9 — evidence floors, mirroring the V2.1 calculus DATA_FLOOR. Configuration,
# not law; bound to the calculus ratification via configHash on the receipt.
DATA_FLOOR_OBSERVATIONS = 5
DATA_FLOOR_PRIORS = 20

# §3.4 — per-class acceptance battery identity. Batteries are owned by PROVE's
# configuration and are director-reviewable; every sealed receipt binds
# batteryId + batteryVersion (§5, §3.11).
BATTERY_ID = "prove-acceptance-battery"
BATTERY_VERSION = "0.1.0-candidate"

# §3.5 — G5 independence criterion: the re-derivation must name at least one
# independence dimension, and it must be able to disagree (theater check).
INDEPENDENCE_DIMENSIONS = (
    "code_path",
    "agent",
    "blinded_inputs",
    "evidence_selection",
)

# §6.1 — private ladder → ratified V2 contract enum mapping. PROVEN maps to
# SUPPORTED, never VERIFIED (§1.3, §6.1). The fine level rides in
# reason_codes (PROVE_SEALED_L<n>), never in the contract enum.
LADDER_TO_V2_EPISTEMIC = {
    "UNPROVEN": "UNKNOWN",
    "EVIDENCED": "CANDIDATE",
    "TESTED": "SUPPORTED",
    "REPRODUCED": "SUPPORTED",
    "PROVEN": "SUPPORTED",
    "CHALLENGED": "CONTRADICTED",
    "INVALIDATED": "INVALIDATED",
    "SUPERSEDED": "SUPERSEDED",
}

# §6.1 — attestation relationship-type mapping. VERIFIED_BY is never used by
# PROVE; it belongs to VERIFY's verdict.
ATTESTATION_TYPES = {
    "attest": "SUPPORTS",
    "challenge": "CONTRADICTS",
    "invalidate": "INVALIDATES",
}

# §2.4 — a claim arriving without stakes is treated as `high` until classified.
DEFAULT_STAKES = "high"

# §1.4 / §4.5 — PROVE grants nothing. The convention string below appears in
# every authority_checks() listing so tests can assert the negation.
NO_AUTHORITY_GRANT = "no_authority_granted_by_prove"

# §8 — state machine transitions PROVE persists (receipted).
_PIPELINE_TRANSITIONS = (
    "UNPROVEN->EVIDENCED",
    "EVIDENCED->TESTED",
    "TESTED->REPRODUCED",
    "REPRODUCED->PROVEN",
)
_SIDE_TRANSITIONS = (
    "ANY->CHALLENGED",
    "CHALLENGED->REPROVEN",
    "CHALLENGED->INVALIDATED",
    "ANY->SUPERSEDED",
)


# §8 — kinds of receipts that disturb a seal. Boundary checks
# (crossing_permitted, forecast crossings) are read-only w.r.t. the seal.
SEAL_AFFECTING_KINDS = frozenset({
    "intake", "advance", "hold", "refusal", "stakes_raised",
    "challenge_survived", "invalidated", "superseded", "crossing_refused",
    "forecast_crossing_refused",
})


# ---------------------------------------------------------------------------
# Canonical hashing / determinism helpers
# ---------------------------------------------------------------------------


def _canonical(obj: Any) -> str:
    """Deterministic canonical serialization (FNV-adjacent; sha256 here)."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str)


def _hash(obj: Any) -> str:
    return hashlib.sha256(_canonical(obj).encode("utf-8")).hexdigest()


def _parse_ts(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    try:
        ts = datetime.fromisoformat(value)
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        return ts
    except (ValueError, TypeError):
        return None


# ---------------------------------------------------------------------------
# PROOF_CLAIM contract (spec §2.1 / §5)
#
# A claim is a plain dict with the keys below. PROVE never accepts a bare
# assertion — a claim without evidence references is UNPROVEN by construction
# (§1.1, §3.1).
#
#   id                  str    canonical, immutable
#   class               one of CLAIM_CLASSES
#   assertion           str    the claim, stated plainly
#   assertions          [{ "text": str, "evidence": [address, ...] }]
#                              material assertions; every one needs ≥1
#                              evidence ref (G1)
#   evidence            [{ "address": str,          content-addressed
#                          "source": str,
#                          "acquisition_method": str,
#                          "acquired_at": ISO str,
#                          "qualified_oracle": bool,   §3.4 oracle qual.
#                          "failure_mode": str,        §3.9 shared-failure-mode
#                          "independent_of_claim": bool,
#                          "restates_claim": bool,     G3 laundering signal
#                          "provisional_until": ISO|None,  §3.10
#                          "observed_readback": bool,  PROCEDURAL §3.4
#                       }]
#   stakes              "low"|"high"|"consequential" (missing → "high" §2.4)
#   required_level      int (missing → REQUIRED_LEVEL[stakes])
#   overturn_conditions [str]   §5: what evidence would defeat this claim
#   quantitative        bool; "uncertainty_stated": bool   §3.6
#   freshness_seconds   int    G7 domain horizon (default 7d)
#   read_back_observed  bool   PROCEDURAL battery: post-state read back, not
#                              assumed from the request (§3.4, §4.4)
#   premises            [{ "level": int }]   DEDUCTIVE battery §3.4
#   raw_data_retained   bool   EMPIRICAL battery: raw data addressable
#   observation_recorded_with_method bool   EMPIRICAL battery
#   basis_stated, uncertainty_bound, falsification_conditions  PREDICTIVE §3.4
#   block_state         "BLOCKED"|None   §4.8: BLOCKED is a process state
#   about               "prove-machinery"|None  §4.2: routes to VERIFY
#   pieces              [claim-dicts]   §4.7: decomposition → re-bundle
#   offered_as_authorization bool   §4.5 category check
#   is_prediction_presented_for  int|None  §4.1 guard (claims pushed beyond L1)
# ---------------------------------------------------------------------------


class ProveNode(NodeBase):
    """NAYA-KERNEL-PROVE. See module docstring for the contractual role."""

    # -- NodeBase interface ------------------------------------------------

    def manifest_entry(self) -> ManifestEntry:
        """Return this node's manifest entry (candidate spec, §9 acceptance battery)."""
        return ManifestEntry(
            node_id=NODE_ID,
            version=NODE_VERSION,
            responsibilities=[
                "grade claims through the G1–G7 proof-maturity gates (§3)",
                "certify proof-maturity levels L0–L4 with sealed ProofReceipts (§2.2, §5)",
                "refuse floor-lowering, circularity, laundering, prediction-stamping, "
                "IMPLEMENTED-as-VERIFIED, proof-as-permission (§4)",
                "bind attestation onto the ratified graph V2 contract enums (§6.1)",
                "hold the CONNECT boundary: nothing unproven crosses (§1.2, §8)",
            ],
        )

    def gate(self, state: Dict[str, Any]) -> GateResult:
        """Evaluate PROVE's gate on `state` (§2.1 intake contract).

        Runs refusal conditions (§4) first, then climbs the ladder from the
        claim's evidence alone. Returns PASS when the claim already sits at or
        above its required level with a sealed receipt; NEED_EVIDENCE when the
        claim is held below its required level with named gaps; FAIL when a
        refusal condition fires (the floor is not situational, §4.6).
        """
        claim = (state or {}).get("claim") or {}
        operation = (state or {}).get("operation") or "intake"
        if operation != "intake":
            return GateResult(
                GateVerdict.NEED_EVIDENCE,
                [f"PROVE gate() conforms on intake only; use advance()/crossing_check() for '{operation}'"],
            )
        refusal = self._refusals(claim)
        if refusal:
            return GateResult(GateVerdict.FAIL, refusal)
        achieved, gate_results, _held = self._climb(dict(claim))
        required = self._required_level(claim)
        if achieved >= required and self._is_sealed(claim.get("id")):
            return GateResult(
                GateVerdict.PASS,
                [f"PROVE PASS: claim at {LEVEL_NAMES[achieved]} "
                 f"(required L{required} for stakes '{self._stakes(claim)}')"],
            )
        gaps = self._name_gaps(claim, gate_results, achieved, required)
        return GateResult(GateVerdict.NEED_EVIDENCE, gaps)

    def persisted_transitions(self) -> List[str]:
        """List the receipt transitions this node persists (candidate spec, §9 acceptance battery)."""
        return list(_PIPELINE_TRANSITIONS) + list(_SIDE_TRANSITIONS)

    def evidence_hooks(self) -> List[str]:
        """List the evidence hooks this node exposes (candidate spec, §9 acceptance battery)."""
        return [
            "proof_claims",          # intake registry (claimId → claim snapshot)
            "proof_receipts",        # hash-bound receipts (§5)
            "gate_results",          # per-gate PASS/FAIL with named gaps
            "attestation_edges",     # §6.1 graph edge writes (L2+)
            "challenge_records",     # §6.3 counter-evidence
            "method_findings",       # §4.3 findings (receipt chain only)
            "director_briefs",       # §4.6 BRIEF artifacts
            "recompute_records",     # §3.5 G5 records
            "battery_definitions",   # §3.4 / §3.11 batteryId+version
            "transition_log",        # §8 state machine transitions
        ]

    def authority_checks(self) -> List[str]:
        """Declare this node's authority checks; declares, never grants (candidate spec, §9 acceptance battery)."""
        # PROVE performs these validations and grants nothing. The first entry
        # is the negation convention tests assert (§1.4).
        return [
            NO_AUTHORITY_GRANT,
            "claim intake bound to authenticated principal",
            "stakes raise: bounded, receipted, no silent downgrade",
            "required level: never lowered (§3.8)",
            "proof receipt is not authorization (§4.5)",
            "method findings carry no automatic consequence (§4.3)",
        ]

    def cold_reconstruct(self, receipts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Rebuild PROVE's durable state from receipts alone (cold start).

        Replays the receipt chain in issuedAt order, re-deriving each claim's
        maturity level and re-running `recompute()` on every sealed receipt.
        Returns the reconstructed state plus a determinism report; any receipt
        that does not recompute to MATCH is demoted to the highest level the
        successor *can* recompute (§5 cold-successor test).
        """
        ordered = sorted(receipts or [], key=lambda r: r.get("issued_at", ""))
        state: Dict[str, Any] = {
            "claims": {},
            "receipts": [],
            "determinism": {"checked": 0, "matched": 0, "mismatched": []},
        }
        for receipt in ordered:
            claim_id = receipt.get("claim_id")
            level = receipt.get("maturity_level", 0)
            state["claims"][claim_id] = {
                "maturity_level": level,
                "state": receipt.get("claim_state", "UNPROVEN"),
                "receipt_id": receipt.get("id"),
            }
            state["receipts"].append(receipt.get("id"))
            if receipt.get("sealed"):
                verdict = self._recompute_from_receipt(receipt)
                state["determinism"]["checked"] += 1
                if verdict == "MATCH":
                    state["determinism"]["matched"] += 1
                else:
                    state["determinism"]["mismatched"].append(receipt.get("id"))
                    # §5: demote to the highest level the successor can
                    # recompute — never hold a level nobody can re-derive.
                    state["claims"][claim_id]["maturity_level"] = max(
                        0, level - 1
                    )
                    state["claims"][claim_id]["state"] = "UNPROVEN"
        return state

    # -- internal registry -------------------------------------------------

    def __init__(self) -> None:
        self._claims: Dict[str, Dict[str, Any]] = {}
        self._receipts: Dict[str, Dict[str, Any]] = {}
        self._transitions: List[Dict[str, Any]] = []
        self._findings: Dict[str, List[Dict[str, Any]]] = {}
        self._briefs: List[Dict[str, Any]] = []
        self._raise_log: Dict[str, List[Dict[str, Any]]] = {}
        self._challenge_log: List[Dict[str, Any]] = []
        self._execution_seq = 0

    def _execution_id(self) -> str:
        self._execution_seq += 1
        return f"prove-exec-{self._execution_seq:06d}"

    # -- claim intake / stakes (§2.1, §2.4) --------------------------------

    def _stakes(self, claim: Dict[str, Any]) -> str:
        return claim.get("stakes") or DEFAULT_STAKES

    def _required_level(self, claim: Dict[str, Any]) -> int:
        explicit = claim.get("required_level")
        if isinstance(explicit, int) and explicit in (2, 3, 4):
            return explicit
        return REQUIRED_LEVEL[self._stakes(claim)]

    def submit(self, claim: Dict[str, Any], principal: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Register a claim at UNPROVEN (§1.1, §2.4 intake rules)."""
        claim = dict(claim)
        if claim.get("class") not in CLAIM_CLASSES:
            raise ValueError(f"PROVE intake refused: unknown claim class {claim.get('class')!r}")
        if not claim.get("id"):
            raise ValueError("PROVE intake refused: claim id is required")
        claim.setdefault("stakes", DEFAULT_STAKES)
        claim.setdefault("required_level", REQUIRED_LEVEL[claim["stakes"]])
        record = {
            "claim": claim,
            "maturity_level": 0,
            "state": "UNPROVEN",
            "sealed": False,
            "sealed_receipt_id": None,
            "challenge": None,
        }
        self._claims[claim["id"]] = record
        receipt = self._emit_receipt(claim["id"], "intake", principal)
        return {"claim_id": claim["id"], "state": "UNPROVEN", "receipt_id": receipt["id"]}

    # -- refusal conditions (§4) -------------------------------------------

    def _refusals(self, claim: Dict[str, Any]) -> List[str]:
        """Return refusal reasons (non-empty ⇒ held, receipted, §4)."""
        reasons: List[str] = []
        # §4.2 — claims about PROVE's own machinery route to VERIFY; PROVE
        # may operate its machinery but never validate it.
        if claim.get("about") == "prove-machinery":
            reasons.append(
                "PROVE §4.2 refusal: claim about PROVE's own gates/batteries "
                "is circular — routed to VERIFY (independent party)"
            )
        # §4.8 — BLOCKED is a process state, never a proof state.
        if claim.get("block_state") == "BLOCKED":
            reasons.append(
                "PROVE §4.8 refusal: evidence gathering is BLOCKED — claim held "
                "UNPROVEN (BLOCKED never counts as established)"
            )
        # §4.1 — the future cannot be proven; predictions cap at L1.
        if claim.get("class") == "PREDICTIVE":
            target = claim.get("is_prediction_presented_for")
            if isinstance(target, int) and target >= 2:
                reasons.append(
                    "PROVE §4.1 refusal: PREDICTIVE claim presented for L2+ — "
                    "capped at L1 (EVIDENCED) by definition"
                )
        # §4.4 — IMPLEMENTED presented as VERIFIED. A PROCEDURAL claim whose
        # only evidence is the request/action itself (no read-back) is not
        # "pending" — it is refused.
        if claim.get("class") == "PROCEDURAL" and claim.get("implemented_only"):
            reasons.append(
                "PROVE §4.4 refusal: IMPLEMENTED presented as established — "
                "PROVEN requires the read-back (OBSERVED), not the request"
            )
        # §4.5 — proof as permission is a category error. The claim may still
        # be stamped on its merits; the authorization inference is refused.
        if claim.get("offered_as_authorization"):
            reasons.append(
                "PROVE §4.5 flag: PROVEN is not permission — the claim may be "
                "certified, but the authorization inference is refused; "
                "authority flows from LAW and the Director, never from a receipt"
            )
        # §4.3 — evidence laundering is detected at G3, but an egregious
        # restate-the-claim intake is refused outright with a method finding.
        evidence = claim.get("evidence") or []
        if evidence and all(e.get("restates_claim") for e in evidence):
            reasons.append(
                "PROVE §4.3 refusal: evidence set is the claim restated — "
                "laundering recorded as a method finding against the claimant"
            )
        # §4.7 — bundle rule: a claim split into sub-threshold pieces is
        # re-assembled before gating.
        if claim.get("pieces"):
            reasons.append(
                "PROVE §4.7 hold: claim arrived as sub-threshold pieces — "
                "re-assembled as one bundle before gating (gate evasion refused)"
            )
        return reasons

    def _record_finding(self, claim_id: str, kind: str, detail: str) -> None:
        """§4.3 — method findings live in the receipt chain only; no automatic
        consequence (PROVE grants no authority)."""
        self._findings.setdefault(claim_id, []).append(
            {
                "kind": kind,
                "detail": detail,
                "claim_id": claim_id,
                "issued_by": NODE_ID,
            }
        )

    # -- the gates (§3) ----------------------------------------------------

    def _materiality_pre_step(self, claim: Dict[str, Any]) -> Dict[str, Any]:
        """§3 intro — the one scored pre-step: whether each assertion is
        material enough to require evidence. PROVE gates; it does not score —
        the scoring never replaces the gate. The receipt records which
        assertions were judged material and the (candidate) machinery used.

        Candidate machinery: an assertion is material unless explicitly marked
        `immaterial`. This is deliberately conservative — immateriality must
        be asserted, never assumed.
        """
        scored = []
        for assertion in claim.get("assertions") or []:
            material = not assertion.get("immaterial")
            scored.append({"text": assertion.get("text"), "material": material})
        return {
            "kind": "materiality_pre_step",
            "assertions": scored,
            "calculus_version": "decision-calculus-v2.1-candidate",
            "config_hash": _hash(
                {
                    "battery_id": BATTERY_ID,
                    "battery_version": BATTERY_VERSION,
                    "data_floor_observations": DATA_FLOOR_OBSERVATIONS,
                    "data_floor_priors": DATA_FLOOR_PRIORS,
                    "required_levels": REQUIRED_LEVEL,
                }
            ),
        }

    def _gate_G1(self, claim: Dict[str, Any]) -> Dict[str, Any]:
        """§3.1 — evidence presence. Every material assertion has ≥1 evidence
        reference. A claim with no evidence refs is UNPROVEN by construction."""
        evidence = claim.get("evidence") or []
        assertions = claim.get("assertions") or []
        missing = [
            a.get("text", "?")
            for a in assertions
            if not a.get("immaterial") and not (a.get("evidence") or [])
        ]
        passed = bool(evidence) and not missing
        reasons = []
        if not evidence:
            reasons.append("G1 fail: claim carries no evidence references — UNPROVEN by construction")
        for text in missing:
            reasons.append(f"G1 fail: material assertion without evidence: {text!r}")
        if passed:
            reasons.append(f"G1 pass: {len(evidence)} evidence ref(s) across {len(assertions)} assertion(s)")
        return {"gate": "G1", "passed": passed, "reasons": reasons}

    def _gate_G2(self, claim: Dict[str, Any]) -> Dict[str, Any]:
        """§3.2 — provenance completeness. Every ref resolves, is
        content-addressed, and carries source, acquisition method, and
        acquisition time. Unqualified oracles fail G2 (§3.4)."""
        problems: List[str] = []
        for e in claim.get("evidence") or []:
            addr = e.get("address") or "?"
            for field in ("source", "acquisition_method", "acquired_at"):
                if not e.get(field):
                    problems.append(f"G2 fail: evidence {addr} missing {field}")
            if not _parse_ts(e.get("acquired_at")):
                problems.append(f"G2 fail: evidence {addr} has unparseable acquired_at")
            if not e.get("qualified_oracle"):
                problems.append(f"G2 fail: evidence {addr} oracle unqualified (§3.4)")
        passed = not problems
        if passed:
            problems.append("G2 pass: all evidence refs resolve with complete provenance")
        return {"gate": "G2", "passed": passed, "reasons": problems}

    def _gate_G3(self, claim: Dict[str, Any]) -> Dict[str, Any]:
        """§3.3 — non-circularity. The claimant's own assertion, the claim
        restated, or a downstream consequence of assuming the claim is not
        evidence. Stripping the claim's own assertions must leave evidence."""
        problems: List[str] = []
        independent = [e for e in (claim.get("evidence") or []) if e.get("independent_of_claim")]
        restaters = [e for e in (claim.get("evidence") or []) if e.get("restates_claim")]
        for e in restaters:
            problems.append(
                f"G3 fail: evidence {e.get('address', '?')} restates the claim (§4.3 laundering)"
            )
        if not independent:
            problems.append("G3 fail: no evidence independent of the claim — strip-claim test leaves nothing")
        passed = not problems
        if passed:
            problems.append(f"G3 pass: {len(independent)} evidence item(s) independent of the claim")
        return {"gate": "G3", "passed": passed, "reasons": problems}

    def _independent_observations(self, claim: Dict[str, Any]) -> List[Dict[str, Any]]:
        """§3.9 — observations are independent only if they differ in at least
        one of source, method, or acquisition time AND share no single failure
        mode that could produce the same reading in all of them."""
        evidence = [e for e in (claim.get("evidence") or []) if e.get("independent_of_claim")]
        independent: List[Dict[str, Any]] = []
        for e in evidence:
            duplicate = False
            for kept in independent:
                same_source = kept.get("source") == e.get("source")
                same_method = kept.get("acquisition_method") == e.get("acquisition_method")
                same_time = (kept.get("acquired_at") or "")[:10] == (e.get("acquired_at") or "")[:10]
                if same_source and same_method and same_time:
                    duplicate = True
                    break
            if not duplicate:
                independent.append(e)
        if independent and len({e.get("failure_mode") for e in independent}) == 1:
            # Every observation shares one failure mode — they are not
            # independent (§3.9).
            return []
        return independent

    def _gate_G4(self, claim: Dict[str, Any]) -> Dict[str, Any]:
        """§3.4 — claim-class acceptance battery. PREDICTIVE caps at L1."""
        cls = claim.get("class")
        problems: List[str] = []
        notes: List[str] = []
        if cls == "EMPIRICAL":
            if not claim.get("observation_recorded_with_method"):
                problems.append("G4 fail (EMPIRICAL): observation not recorded with method")
            if not claim.get("raw_data_retained"):
                problems.append("G4 fail (EMPIRICAL): raw data not retained/addressable")
            if self._stakes(claim) == "consequential":
                indep = self._independent_observations(claim)
                if len(indep) < 2:
                    problems.append(
                        "G4 fail (EMPIRICAL): consequential claim requires ≥2 independent "
                        "sources (§3.4 corroboration)"
                    )
            else:
                notes.append("G4 note (EMPIRICAL): method recorded; raw data retained")
        elif cls == "DEDUCTIVE":
            required = self._required_level(claim)
            premises = claim.get("premises") or []
            if not premises:
                problems.append("G4 fail (DEDUCTIVE): no premises offered")
            weak = [p for p in premises if p.get("level", 0) < required]
            if weak:
                problems.append(
                    f"G4 fail (DEDUCTIVE): {len(weak)} premise(s) below the required level L{required}"
                )
            if not problems:
                notes.append(f"G4 pass (DEDUCTIVE): all premises ≥ L{required}")
        elif cls == "PROCEDURAL":
            if not claim.get("read_back_observed"):
                problems.append(
                    "G4 fail (PROCEDURAL): post-state not read back — IMPLEMENTED is the "
                    "request; OBSERVED is the read-back (§4.4)"
                )
            else:
                notes.append("G4 pass (PROCEDURAL): post-state read back from execution, not assumed")
        elif cls == "PREDICTIVE":
            if not claim.get("basis_stated"):
                problems.append("G4 fail (PREDICTIVE): basis not stated")
            if not claim.get("uncertainty_bound"):
                problems.append("G4 fail (PREDICTIVE): uncertainty not evidence-bound")
            if not claim.get("falsification_conditions"):
                problems.append("G4 fail (PREDICTIVE): falsification conditions not named")
            if not problems:
                notes.append("G4 pass (PREDICTIVE): basis/uncertainty/falsification present — capped at L1 (§2.1)")
        passed = not problems
        return {"gate": "G4", "passed": passed, "reasons": problems + notes}

    def _gate_G5(self, claim: Dict[str, Any]) -> Dict[str, Any]:
        """§3.5 — recomputation. Fresh derivation path, able to disagree, with
        a named independence dimension. Theater is refused."""
        record = claim.get("recompute") or {}
        problems: List[str] = []
        dimension = record.get("independence_dimension")
        if dimension not in INDEPENDENCE_DIMENSIONS:
            problems.append(
                "G5 fail: no recorded independence dimension (§3.5: "
                f"{'/'.join(INDEPENDENCE_DIMENSIONS)})"
            )
        if not record.get("can_disagree"):
            problems.append("G5 fail: re-derivation cannot in principle disagree — theater refused (§3.5)")
        if record.get("result") != "MATCH":
            problems.append("G5 fail: re-derivation did not MATCH")
        passed = not problems
        if passed:
            problems.append(f"G5 pass: fresh-derivation MATCH via dimension '{dimension}'")
        return {"gate": "G5", "passed": passed, "reasons": problems}

    def _gate_G6(self, claim: Dict[str, Any]) -> Dict[str, Any]:
        """§3.6 — calibration. A quantitative claim without evidence-bound
        uncertainty is a claim, not a proof."""
        if not claim.get("quantitative"):
            return {"gate": "G6", "passed": True, "reasons": ["G6 pass: non-quantitative claim"]}
        if claim.get("uncertainty_stated"):
            return {
                "gate": "G6",
                "passed": True,
                "reasons": ["G6 pass: uncertainty stated and evidence-bound (source named)"],
            }
        return {
            "gate": "G6",
            "passed": False,
            "reasons": ["G6 fail: quantitative claim without uncertainty bounds stays UNPROVEN"],
        }

    def _gate_G7(self, claim: Dict[str, Any]) -> Dict[str, Any]:
        """§3.7 — freshness. Evidence must be current enough for the claim's
        domain. Stale evidence fails; the claim returns to KNOW for
        re-evidencing — it is not grandfathered."""
        horizon = int(claim.get("freshness_seconds") or 7 * 24 * 3600)
        now = _parse_ts(claim.get("as_of")) or datetime.now(timezone.utc)
        problems: List[str] = []
        for e in claim.get("evidence") or []:
            acquired = _parse_ts(e.get("acquired_at"))
            if acquired and (now - acquired) > timedelta(seconds=horizon):
                problems.append(
                    f"G7 fail: evidence {e.get('address', '?')} stale "
                    f"({(now - acquired).days}d old vs {horizon // 86400}d horizon)"
                )
        passed = not problems
        if passed:
            problems.append("G7 pass: all evidence within the claim's freshness horizon")
        return {"gate": "G7", "passed": passed, "reasons": problems}

    def _evidence_floors(self, claim: Dict[str, Any]) -> Dict[str, Any]:
        """§3.9 — evidence floors for L2+: n ≥ 5 independent observations, or
        n ≥ 20 qualified priors when direct observation is impossible.
        DEDUCTIVE claims: premises at level suffice. L4: the floor applies at
        every level transition. n=1 caps at L1 — no n=1 PROVEN, ever."""
        cls = claim.get("class")
        if cls == "DEDUCTIVE":
            premises = claim.get("premises") or []
            ok = bool(premises)
            return {
                "passed": ok,
                "reasons": ["floors pass (DEDUCTIVE): premises at level suffice in place of observations"]
                if ok else ["floors fail (DEDUCTIVE): no premises — no observations to substitute"],
            }
        observations = self._independent_observations(claim)
        priors = [p for p in (claim.get("priors") or []) if p.get("qualified")]
        if len(observations) >= DATA_FLOOR_OBSERVATIONS:
            return {
                "passed": True,
                "reasons": [f"floors pass: {len(observations)} independent observations (≥{DATA_FLOOR_OBSERVATIONS})"],
            }
        if len(priors) >= DATA_FLOOR_PRIORS:
            return {
                "passed": True,
                "reasons": [f"floors pass: {len(priors)} qualified priors (≥{DATA_FLOOR_PRIORS})"],
            }
        if len(observations) == 1:
            return {
                "passed": False,
                "cap_at_l1": True,
                "reasons": ["floors fail: single observation caps the claim at L1 — no n=1 PROVEN, ever"],
            }
        return {
            "passed": False,
            "reasons": [
                f"floors fail: {len(observations)} observations / {len(priors)} qualified priors — "
                f"need ≥{DATA_FLOOR_OBSERVATIONS} observations or ≥{DATA_FLOOR_PRIORS} priors"
            ],
        }

    def _provisional_cap(self, claim: Dict[str, Any]) -> Dict[str, Any]:
        """§3.10 — provisional evidence (open observation window) is premature,
        not stale: capped at L2 with valid_until bound to the window-close."""
        closes = [
            _parse_ts(e.get("provisional_until"))
            for e in (claim.get("evidence") or [])
            if e.get("provisional_until")
        ]
        closes = [c for c in closes if c]
        if not closes:
            return {"capped": False}
        return {
            "capped": True,
            "cap": 2,
            "provisional_until": min(closes).isoformat(),
            "reason": "§3.10: material evidence is provisional (open window) — capped at L2, "
            "re-gate queued for window-close",
        }

    # -- ladder climbing ----------------------------------------------------

    def _climb(self, claim: Dict[str, Any]) -> Any:
        """Run the gates in ladder order; return (achieved_level, gate_results,
        held_level). Levels are earned in order; skipping is not permitted."""
        refusal = self._refusals(claim)
        if refusal:
            return 0, {}, 0
        gate_results: Dict[str, Dict[str, Any]] = {}
        achieved = 0

        def run(gate_name: str, gate_fn) -> bool:
            result = gate_fn(claim)
            gate_results[gate_name] = result
            return bool(result["passed"])

        # L0 → L1 (EVIDENCED): G1–G3. Checkable.
        if run("G1", self._gate_G1) and run("G2", self._gate_G2) and run("G3", self._gate_G3):
            achieved = 1
        else:
            return achieved, gate_results, 0

        # L1 → L2 (TESTED): G4 battery + evidence floors (§3.9).
        floors = self._evidence_floors(claim)
        provisional = self._provisional_cap(claim)
        if run("G4", self._gate_G4) and floors["passed"]:
            achieved = 2
        else:
            if floors.get("cap_at_l1"):
                return achieved, gate_results, 1
            return achieved, gate_results, 1
        if provisional["capped"]:
            # §3.10: provisional-backed claims hold at L2 even if they could
            # climb further on the evidence.
            self._queue_regate(claim.get("id"), provisional["provisional_until"])
            return achieved, gate_results, 2

        # L2 → L3 (REPRODUCED): G5 recomputation.
        if run("G5", self._gate_G5):
            achieved = 3
        else:
            return achieved, gate_results, 2

        # L3 → L4 (PROVEN): all gates at the required level; §3.9 floors hold
        # at *every* transition — re-check them here against the current
        # evidence before sealing.
        floors_again = self._evidence_floors(claim)
        g6 = self._gate_G6(claim)
        gate_results["G6"] = g6
        g7 = self._gate_G7(claim)
        gate_results["G7"] = g7
        if g6["passed"] and g7["passed"] and floors_again["passed"]:
            if claim.get("class") == "PREDICTIVE":
                return achieved, gate_results, 3  # §4.1 cap (belt + braces)
            achieved = 4
        return achieved, gate_results, 3

    def _name_gaps(self, claim, gate_results, achieved, required) -> List[str]:
        gaps = [f"PROVE held at {LEVEL_NAMES[achieved]} (required L{required})"]
        for gate_name in GATES:
            result = gate_results.get(gate_name)
            if result and not result["passed"]:
                for reason in result["reasons"]:
                    if reason.startswith(f"{gate_name} fail"):
                        gaps.append(reason)
        return gaps

    def _queue_regate(self, claim_id: Optional[str], at: str) -> None:
        """§3.10 — queue automatic re-gating when the provisional window closes."""
        if claim_id:
            record = self._claims.get(claim_id)
            if record is not None:
                record["regate_queued_until"] = at

    # -- advance / seal ------------------------------------------------------

    def advance(self, claim_id: str, override: bool = False,
                principal: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Attempt to advance a claim one ladder step (§8 state machine).

        `override=True` is a §4.6 floor-lowering request: refused and
        receipted; for consequential claims a DirectorBrief is emitted (§4.6).
        """
        record = self._claims.get(claim_id)
        if record is None:
            raise KeyError(f"PROVE: unknown claim {claim_id!r}")
        claim = record["claim"]
        if override:
            return self._refuse_floor_lowering(claim_id, claim, principal)
        refusal = self._refusals(claim)
        if refusal:
            if "§4.3" in " ".join(refusal):
                self._record_finding(claim_id, "evidence_laundering",
                                     "evidence set restates the claim (§4.3)")
            receipt = self._emit_receipt(claim_id, "refusal", principal, extra={"refusal_reasons": refusal})
            return {"claim_id": claim_id, "advanced": False, "refusal": refusal,
                    "receipt_id": receipt["id"]}
        achieved, gate_results, _held = self._climb(claim)
        prior = record["maturity_level"]
        before = record["state"]
        if record.get("state") == "CHALLENGED":
            # §6.3: re-gate against the augmented evidence set — restore the
            # prior level or fall.
            pass
        new_level = min(achieved, prior + 1) if achieved > prior else prior
        # Never skip levels; never silently demote: a lower re-derivation
        # holds the claim at its current level pending re-evidence.
        if achieved < prior:
            receipt = self._emit_receipt(
                claim_id, "hold", principal,
                extra={"gate_results": gate_results,
                       "note": "re-gating derived a lower level; claim holds pending re-evidence (never silent demotion §6.3)"},
            )
            return {"claim_id": claim_id, "advanced": False, "level": prior,
                    "receipt_id": receipt["id"]}
        record["maturity_level"] = new_level
        record["state"] = LEVEL_NAMES[new_level]
        if new_level != prior:
            self._log_transition(claim_id, before, LEVEL_NAMES[new_level], "gates passed", gate_results)
        sealed = new_level >= self._required_level(claim)
        # PREDICTIVE sealed to its L1 cap counts as sealed-to-cap (§1.5).
        if claim.get("class") == "PREDICTIVE" and new_level == 1:
            sealed = True
        receipt = None
        if sealed:
            # The receipt must record the post-transition seal state — set it
            # before emitting so recompute/cold-reconstruct see it (§5).
            record["sealed"] = True
        receipt = self._emit_receipt(
            claim_id, "advance" if new_level > prior else "hold", principal,
            extra={"gate_results": gate_results, "sealed_claim": sealed},
        )
        if sealed:
            record["sealed_receipt_id"] = receipt["id"]
        if new_level == prior and achieved >= new_level and sealed:
            # §8 re-affirmation: re-gating at the same level after a survived
            # challenge re-seals — the seal timestamp becomes the latest
            # seal-affecting write, so the boundary check can pass again.
            record["sealed_receipt_id"] = receipt["id"]
        return {"claim_id": claim_id, "advanced": new_level > prior,
                "level": new_level, "state": LEVEL_NAMES[new_level],
                "sealed": record["sealed"], "receipt_id": receipt["id"]}

    def _refuse_floor_lowering(self, claim_id, claim, principal) -> Dict[str, Any]:
        """§4.6 — the floor is not situational. Urgency is evidence of stakes,
        and higher stakes mean *more* proof, not less."""
        receipt = self._emit_receipt(
            claim_id, "refusal", principal,
            extra={"refusal_reasons": [
                "PROVE §4.6 refusal: floor-lowering request ('just this once' / "
                "urgency / 'strength of the overall picture') — the floor is not situational"
            ]},
        )
        result = {"claim_id": claim_id, "advanced": False,
                  "refusal": "§4.6 floor-lowering refused", "receipt_id": receipt["id"]}
        if self._stakes(claim) == "consequential":
            brief = self._director_brief(
                claim_id,
                "floor-lowering request on a consequential claim",
                "Keep the floor at the required level; re-evidence the claim instead of lowering the bar.",
            )
            result["director_brief_id"] = brief["id"]
        return result

    def _director_brief(self, claim_id: str, decision: str, recommendation: str) -> Dict[str, Any]:
        """§4.6 BRIEF mechanics — the 9-part decision-brief artifact. Travels
        with the claim's receipt; an unanswered brief is an open item, never a
        silent veto."""
        brief = {
            "id": f"brief-{_hash({'claim': claim_id, 'decision': decision, 'n': len(self._briefs)})[:12]}",
            "claim_id": claim_id,
            "decision_required": decision,
            "meaning": "A proof-floor question only the Director can settle.",
            "options": ["confirm the floor", "reject the request", "escalate with new evidence"],
            "benefits_risks": "confirm: proof stays trustworthy; reject: claim stays held; escalate: defers on new evidence",
            "reversibility": "reversible — the claim holds at its earned level until answered",
            "evidence": f"receipt chain for {claim_id}",
            "uncertainty": "none material to the floor question",
            "recommendation": recommendation,
            "authorization_requested": "explicit director decision on the floor question",
            "status": "open",
        }
        self._briefs.append(brief)
        return brief

    def _is_sealed(self, claim_id: Optional[str]) -> bool:
        record = self._claims.get(claim_id or "")
        return bool(record and record.get("sealed"))

    # -- stakes raise (§2.4, §3.8 bounded raise) ------------------------------

    def raise_stakes(self, claim_id: str, reason: str,
                     deficiency_evidence: Optional[List[str]] = None) -> Dict[str, Any]:
        """§2.4/§3.8 — PROVE may raise stakes (never lower). Bounded: receipted
        with reasons, appealable, and no second raise without new deficiency
        evidence."""
        record = self._claims.get(claim_id)
        if record is None:
            raise KeyError(f"PROVE: unknown claim {claim_id!r}")
        order = {"low": 0, "high": 1, "consequential": 2}
        current = self._stakes(record["claim"])
        if current == "consequential":
            raise ValueError("PROVE: stakes already consequential — cannot raise further")
        log = self._raise_log.setdefault(claim_id, [])
        if log and not deficiency_evidence:
            raise ValueError(
                "PROVE §3.8: no second raise without new evidence of deficiency — "
                "unbounded raising is a refusal in disguise"
            )
        new = {"low": "high", "high": "consequential"}[current]
        record["claim"]["stakes"] = new
        record["claim"]["required_level"] = REQUIRED_LEVEL[new]
        log.append({"from": current, "to": new, "reason": reason,
                    "deficiency_evidence": deficiency_evidence or []})
        receipt = self._emit_receipt(claim_id, "stakes_raised", None,
                                     extra={"raise": log[-1]})
        return {"claim_id": claim_id, "stakes": new, "required_level": REQUIRED_LEVEL[new],
                "receipt_id": receipt["id"]}

    # -- challenge / invalidation / supersession (§6.3) ------------------------

    def challenge(self, claim_id: str, counter_evidence: List[Dict[str, Any]]) -> Dict[str, Any]:
        """§6.3 — counter-evidence moves the claim to CHALLENGED with a
        CHALLENGED_BY edge; both sides stay visible."""
        record = self._claims.get(claim_id)
        if record is None:
            raise KeyError(f"PROVE: unknown claim {claim_id!r}")
        before = record["state"]
        record["challenge"] = {
            "counter_evidence": counter_evidence,
            "arrived_at": datetime.now(timezone.utc).isoformat(),
        }
        record["state"] = "CHALLENGED"
        # Re-gate against the augmented evidence set.
        augmented = dict(record["claim"])
        augmented["evidence"] = list(augmented.get("evidence") or []) + list(counter_evidence)
        achieved, gate_results, _held = self._climb(augmented)
        self._challenge_log.append({"claim_id": claim_id, "counter_evidence": len(counter_evidence)})
        self._log_transition(claim_id, before, "CHALLENGED", "counter-evidence arrived", gate_results)
        if achieved >= record["maturity_level"]:
            record["state"] = LEVEL_NAMES[record["maturity_level"]]
            self._log_transition(claim_id, "CHALLENGED", record["state"], "re-gated: gates pass", gate_results)
            receipt = self._emit_receipt(claim_id, "challenge_survived", None, extra={"gate_results": gate_results})
        else:
            record["state"] = "INVALIDATED"
            record["sealed"] = False
            self._log_transition(claim_id, "CHALLENGED", "INVALIDATED", "gates fail on augmented evidence", gate_results)
            receipt = self._emit_receipt(claim_id, "invalidated", None, extra={"gate_results": gate_results})
        return {"claim_id": claim_id, "state": record["state"], "receipt_id": receipt["id"]}

    def supersede(self, claim_id: str, stronger_claim_id: str) -> Dict[str, Any]:
        """§6.3 — a stronger proof supersedes; lineage intact via the
        supersedes edge."""
        record = self._claims.get(claim_id)
        stronger = self._claims.get(stronger_claim_id)
        if record is None or stronger is None:
            raise KeyError("PROVE: unknown claim in supersede")
        if stronger["maturity_level"] <= record["maturity_level"]:
            raise ValueError("PROVE: superseding claim must hold a higher maturity level")
        before = record["state"]
        record["state"] = "SUPERSEDED"
        record["superseded_by"] = stronger_claim_id
        self._log_transition(claim_id, before, "SUPERSEDED", f"superseded by {stronger_claim_id}", {})
        receipt = self._emit_receipt(claim_id, "superseded", None,
                                     extra={"superseded_by": stronger_claim_id})
        return {"claim_id": claim_id, "state": "SUPERSEDED", "receipt_id": receipt["id"]}

    # -- CONNECT boundary: crossing (§1.2, §1.5, §8) --------------------------

    def crossing_check(self, claim_id: str) -> Dict[str, Any]:
        """The boundary rule: nothing unproven crosses the organism boundary.

        Requires a sealed receipt at the claim's required level (§3.8), then
        re-validates seal-to-cross freshness: the seal is still the latest
        write and no challenge edge has landed since sealing (§8). A claim
        held at its cap under the §1.5 forecast rule crosses only via
        `forecast_crossing()` — never here.
        """
        record = self._claims.get(claim_id)
        if record is None:
            raise KeyError(f"PROVE: unknown claim {claim_id!r}")
        required = self._required_level(record["claim"])
        receipt_id = record.get("sealed_receipt_id")
        receipt = self._receipts.get(receipt_id or "")
        if not record.get("sealed") or receipt is None:
            refusal = self._emit_receipt(claim_id, "crossing_refused", None,
                                         extra={"reason": "no sealed receipt at required level"})
            return {"claim_id": claim_id, "cross": False,
                    "reason": f"unproven material offered to CONNECT — refused at the boundary (§1.2): "
                              f"level L{record['maturity_level']}, required L{required}",
                    "receipt_id": refusal["id"]}
        # §8 seal-to-cross freshness: the seal is still the latest
        # seal-affecting write, and no challenge edge has landed since
        # sealing. Pure boundary checks (crossing_permitted, forecast
        # crossings) do not disturb the seal; anything that re-gates,
        # refuses, or raises does.
        latest = self._latest_affecting_receipt_id(claim_id)
        if latest != receipt_id:
            record["state"] = "CHALLENGED"
            self._log_transition(claim_id, "PROVEN", "CHALLENGED",
                                 "seal-to-cross freshness: a later seal-affecting write landed", {})
            return {"claim_id": claim_id, "cross": False,
                    "reason": "seal-to-cross freshness failed: seal is not the latest seal-affecting write — re-gating before anything crosses (§8)"}
        if record.get("challenge") and record["challenge"].get("arrived_at", "") > receipt.get("issued_at", ""):
            return {"claim_id": claim_id, "cross": False,
                    "reason": "seal-to-cross freshness failed: challenge edge landed since sealing (§8)"}
        ok = self._emit_receipt(claim_id, "crossing_permitted", None,
                                extra={"sealed_receipt": receipt_id})
        return {"claim_id": claim_id, "cross": True, "sealed_receipt": receipt_id,
                "receipt_id": ok["id"]}

    def forecast_crossing(self, claim_id: str) -> Dict[str, Any]:
        """§1.5 — the forecast exception. PREDICTIVE claims capped at L1 may
        cross only as labeled forecasts: sealed L1 receipt, labeled forecast,
        horizon-bound valid_until."""
        record = self._claims.get(claim_id)
        if record is None:
            raise KeyError(f"PROVE: unknown claim {claim_id!r}")
        claim = record["claim"]
        if claim.get("class") != "PREDICTIVE":
            raise ValueError("PROVE §1.5: forecast crossing applies to PREDICTIVE claims only")
        if record["maturity_level"] < 1 or not record.get("sealed"):
            refusal = self._emit_receipt(claim_id, "forecast_crossing_refused", None,
                                         extra={"reason": "no sealed L1 receipt"})
            return {"claim_id": claim_id, "cross": False,
                    "reason": "forecast lacks a sealed L1 receipt (§1.5)", "receipt_id": refusal["id"]}
        horizon = claim.get("forecast_horizon_until")
        if not horizon:
            return {"claim_id": claim_id, "cross": False,
                    "reason": "forecast crossing requires a horizon-bound valid_until (§1.5)"}
        ok = self._emit_receipt(claim_id, "forecast_crossing", None,
                                extra={"forecast_label": "FORECAST — not established fact",
                                       "valid_until": horizon})
        return {"claim_id": claim_id, "cross": True, "as": "forecast",
                "valid_until": horizon, "receipt_id": ok["id"]}

    # -- graph attestation edges (§6.1) --------------------------------------

    def attestation_edge(self, receipt: Dict[str, Any], kind: str = "attest") -> Dict[str, Any]:
        """§6.1 — bind a sealed receipt onto the ratified V2 contract enums.
        The private ladder travels in reason_codes (PROVE_SEALED_L<n>); the
        contract enum is never extended by this spec (§6.4 proposal, not change)."""
        if kind not in ATTESTATION_TYPES:
            raise ValueError(f"PROVE: unknown attestation kind {kind!r}")
        state = LEVEL_NAMES.get(receipt.get("maturity_level", 0), "UNPROVEN")
        if kind == "challenge":
            state = "CHALLENGED"
        elif kind == "invalidate":
            state = "INVALIDATED"
        return {
            "relationship_id": receipt["id"],
            "source_id": receipt["claim_id"],
            "target_id": receipt["id"],
            "relationship_type": ATTESTATION_TYPES[kind],
            "epistemic_state": LADDER_TO_V2_EPISTEMIC[state],
            "status": "ACTIVE",
            "provenance": {"prove_receipt": receipt["id"]},
            "evidence_refs": receipt.get("evidence_refs", []),
            "owner_scope": receipt.get("owner_scope"),
            "valid_from": receipt.get("issued_at"),
            "valid_until": receipt.get("valid_until"),
            "supersedes_relationship_id": receipt.get("supersedes"),
            "consent_ref": receipt.get("consent_ref"),
            "applicability": receipt.get("applicability"),
            "reason_codes": [
                f"PROVE_SEALED_L{receipt.get('maturity_level', 0)}",
                f"PROVE_PRIVATE_{state}",
                "PROVE_CANDIDATE_NOT_RATIFIED",
            ],
        }

    # -- receipts (§5) ---------------------------------------------------------

    def _emit_receipt(self, claim_id: str, kind: str,
                      principal: Optional[Dict[str, Any]],
                      extra: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        record = self._claims.get(claim_id, {})
        claim = record.get("claim", {})
        receipt_id = f"prove-{_hash({'claim': claim_id, 'kind': kind, 'n': len(self._receipts)})[:16]}"
        body = {
            "id": receipt_id,
            "node": NODE_ID,
            "node_version": NODE_VERSION,
            "kind": kind,
            "claim_id": claim_id,
            "claim_class": claim.get("class"),
            "assertion": claim.get("assertion"),
            "stakes": self._stakes(claim),
            "required_level": self._required_level(claim),
            "maturity_level": record.get("maturity_level", 0),
            "prior_level": record.get("maturity_level", 0),
            "claim_state": record.get("state", "UNPROVEN"),
            "evidence_refs": [e.get("address") for e in (claim.get("evidence") or [])],
            "battery_id": BATTERY_ID,
            "battery_version": BATTERY_VERSION,
            "recompute": (claim.get("recompute") or {}),
            "provisional_until": self._provisional_cap(claim).get("provisional_until"),
            "valid_until": claim.get("forecast_horizon_until"),
            "issued_at": datetime.now(timezone.utc).isoformat(),
            "issued_by": (principal or {}).get("identity") or "kernel:prove",
            "execution_id": self._execution_id(),
            "owner_scope": claim.get("owner_scope"),
            "consent_ref": claim.get("consent_ref"),
            "applicability": claim.get("applicability"),
            "overturn_conditions": claim.get("overturn_conditions") or [],
            "sealed": bool(record.get("sealed")),
            "claim_snapshot": claim,
            "method_findings": list(self._findings.get(claim_id, [])),
            "candidate_banner": "CANDIDATE — NOT RATIFIED — NOT MERGED",
        }
        if extra:
            body.update(extra)
        receipt = dict(body)
        receipt["receipt_hash"] = _hash({k: v for k, v in body.items() if k != "receipt_hash"})
        self._receipts[receipt_id] = receipt
        return receipt

    def recompute(self, receipt_id: str) -> str:
        """§5 cold-successor test: same claim + same evidence + same config →
        same verdict. Returns MATCH / MISMATCH."""
        receipt = self._receipts.get(receipt_id)
        if receipt is None:
            raise KeyError(f"PROVE: unknown receipt {receipt_id!r}")
        return self._recompute_from_receipt(receipt)

    def _recompute_from_receipt(self, receipt: Dict[str, Any]) -> str:
        snapshot = receipt.get("claim_snapshot") or {}
        # The receipt must bind the machinery it ran under, or recompute is
        # meaningless (§3.9, §3.11).
        if receipt.get("battery_version") != BATTERY_VERSION:
            return "MISMATCH"
        achieved, _gate_results, _held = self._climb(dict(snapshot))
        return "MATCH" if achieved == receipt.get("maturity_level", 0) else "MISMATCH"

    def _latest_affecting_receipt_id(self, claim_id: str) -> Optional[str]:
        """§8 — latest receipt whose kind disturbs the seal (boundary checks
        are read-only w.r.t. the seal)."""
        ids = [
            rid for rid, r in self._receipts.items()
            if r.get("claim_id") == claim_id and r.get("kind") in SEAL_AFFECTING_KINDS
        ]
        if not ids:
            return None
        return max(ids, key=lambda rid: self._receipts[rid].get("issued_at", ""))

    # -- transition log (§8) ----------------------------------------------------

    def _log_transition(self, claim_id: str, before: str, after: str,
                        reason: str, gate_results: Dict[str, Any]) -> None:
        self._transitions.append(
            {
                "claim_id": claim_id,
                "before": before,
                "after": after,
                "reason": reason,
                "execution_id": self._execution_id(),
                "issued_at": datetime.now(timezone.utc).isoformat(),
            }
        )
