"""NAYA-KERNEL-VERIFY — CANDIDATE implementation (NOT RATIFIED — NOT MERGED).

Implements the VERIFY node contract from VERIFY-NODE-SPEC-CANDIDATE.md (the
reconciled candidate: other Naya seat's "NODE 7: VERIFY — Ultimate Master
Specification V1 — Lock Candidate" + Naya 4 draft) against the NodeBase
interface. Candidate code on a feature branch: it proves the spec is
implementable; it grants nothing, merges nothing, deploys nothing.

Contractual responsibility (spec §0): VERIFY is the organism's immune system —
the independent seat that re-derives, attacks, and closes. It takes claimed
results, subjects them to independent reproduction by a different seat,
classifies every failure before any code changes, runs adversarial controls
designed to make false claims fail, and emits the verified receipts that
LEARN may consume.

Master law: EXECUTION != OUTCOME; Attempted != Executed != Successful;
Observed != Verified; SelfReport != IndependentVerification;
TestsPassed != ProductionProven. Success criteria must be predeclared
before the result is known — no goalpost-moving (spec §0).

The four axes (§1) are normative and bound to receipt fields; they are never
collapsed:
  A — outcome_status        SUCCESS / FAILURE / INCONCLUSIVE / NOT_PROVEN / PARTIAL
  B — acceptance_decision   ACCEPTED / REJECTED / PENDING / PENDING_HUMAN
  C — causal_status         NOT_CLAIMED / CLAIMED / CAUSAL_SUPPORTED /
                            CAUSAL_CONTRADICTED / CAUSAL_INCONCLUSIVE / UNVERIFIED
  D — verification_state    UNVERIFIED / IN_VERIFICATION / PASS_PENDING_WINDOW /
                            VERIFIED_PASS / FAIL / ESCALATE / REOPENED / CANNOT_VERIFY

VERIFY never grants, infers, or modifies authority — ever. VERIFY has no
delete operation, on any stream, ever (spec §3, N4 §5.2).

Gate input contract (`state` dict keys for the NodeBase `gate()`; all reads
are explicit):
  receipt_id           str   a VerifiedReceipt id to report on
  request              VERIFICATION_REQUEST dict (see contract below) to pre-check
  downgrade_instruction dict e.g. {"type": "convert_fail_to_pass",
                                  "target_receipt": "vr-...", "source": "director"}
  now                  ISO-8601 timestamp override (tests / determinism)

The imperative API below (submit / reproduce / run_tier1 / classify_failure /
close / reopen / ...) is what the kernel pipeline drives; `gate()` is the
NodeBase conformance surface over it.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from naya_kernel.node_base import (GateResult, GateVerdict, ManifestEntry,
                                  NodeBase, CALCULUS_V21_VERSION,
                                  CALCULUS_V21_SPEC_HASH)

NODE_ID = "NAYA-KERNEL-VERIFY"
NODE_VERSION = "0.1.0-candidate"
PIPELINE_POSITION = 7

# ---------------------------------------------------------------------------
# Spec constants (§1 — the four axes; never collapsed)
# ---------------------------------------------------------------------------

# Axis A — Outcome. FAILURE != NOT_PROVEN != INCONCLUSIVE (spec §1, PDF §11).
OUTCOME_STATUSES = ("SUCCESS", "FAILURE", "INCONCLUSIVE", "NOT_PROVEN", "PARTIAL")

# Axis B — Acceptance. A factually verified outcome can still be REJECTED
# (spec §1, PDF §39); ESCALATE/PENDING_HUMAN covers Shawn-reserved judgment
# (brand, mission, final release, ratification) (spec §1, PDF §61).
ACCEPTANCE_DECISIONS = ("ACCEPTED", "REJECTED", "PENDING", "PENDING_HUMAN")

# Axis C — Causality (spec §1, PDF §20-§31).
CAUSAL_STATUSES = (
    "NOT_CLAIMED",
    "CLAIMED",
    "CAUSAL_SUPPORTED",
    "CAUSAL_CONTRADICTED",
    "CAUSAL_INCONCLUSIVE",
    "UNVERIFIED",
)

# Axis D — Verification maturity. Terminal per receipt: VERIFIED_PASS, FAIL,
# CANNOT_VERIFY. Re-examination is a NEW receipt (spec §3).
VERIFICATION_STATES = (
    "UNVERIFIED",
    "IN_VERIFICATION",
    "PASS_PENDING_WINDOW",
    "VERIFIED_PASS",
    "FAIL",
    "ESCALATE",
    "REOPENED",
    "CANNOT_VERIFY",
)
TERMINAL_STATES = ("VERIFIED_PASS", "FAIL", "CANNOT_VERIFY")

# §3 — the receipt state machine. Every transition records before/after,
# reason, execution ID, evidence refs, verifier seat identity, timestamp.
TRANSITIONS = {
    "intake_accepted": ("UNVERIFIED", "IN_VERIFICATION"),
    "verification_pass": ("IN_VERIFICATION", "VERIFIED_PASS"),
    "window_hold": ("IN_VERIFICATION", "PASS_PENDING_WINDOW"),
    "window_closed_clean": ("PASS_PENDING_WINDOW", "VERIFIED_PASS"),
    "window_reopened": ("PASS_PENDING_WINDOW", "REOPENED"),
    "postpass_reopened": ("VERIFIED_PASS", "REOPENED"),
    "reexamination_started": ("REOPENED", "IN_VERIFICATION"),
    "verification_fail": ("IN_VERIFICATION", "FAIL"),
    "cannot_verify": ("IN_VERIFICATION", "CANNOT_VERIFY"),
    "escalated": ("IN_VERIFICATION", "ESCALATE"),
    "escalate_returned": ("ESCALATE", "IN_VERIFICATION"),
}

# §2 / N4 §4.2 — failure taxonomy. Every falsified claim is classified into
# exactly one of these BEFORE any code change; misclassification is itself a
# defect; classification receipts are superseded with lineage, never edited.
FAILURE_CLASSES = (
    "TRANSIENT_INFRA",
    "EVIDENCE_GAP",
    "CALIBRATION_ERROR",
    "LOGIC_DEFECT",
    "AUTHORITY_VIOLATION",
    "PROVENANCE_FAILURE",
    "ADVERSARIAL_COMPROMISE",
    "UNKNOWN",
)

# §2 — independent reproduction modes. Reproducer seat != deciding seat
# (different instance identity, no shared unlogged context, own
# authenticated issuedBy). Same code may reread with a fresh identity, but
# the receipt must state exactly which independence dimensions were achieved.
REPRODUCTION_MODES = ("RECOMPUTE", "REPLICATE", "ADVERSARIAL", "AUDIT_SAMPLE")
INDEPENDENCE_DIMS = (
    "different_seat_identity",
    "no_shared_unlogged_context",
    "own_authenticated_issued_by",
)

# §2 — observation windows. Candidate caveat: window lengths follow the
# CANDIDATE calculus schedule (24h/7d/30d/90d) — director-set until V2.1 is
# ratified; all V2.1 state references in this spec are aspirational.
WINDOW_SCHEDULE_SECONDS = {
    "24h": 24 * 3600,
    "7d": 7 * 24 * 3600,
    "30d": 30 * 24 * 3600,
    "90d": 90 * 24 * 3600,
}

# §4 — refusal conditions. Downgrade pressure wins over everything: any
# instruction, from any seat INCLUDING the Director, to convert FAIL->PASS,
# skip classification, or suppress an adversarial finding is refused and
# receipted with the pressure recorded as evidence, citing the Judgment Rule
# (Prime Directive, ratified 2026-09-30).
REFUSAL_CODES = (
    "R_EVIDENCE_INACCESSIBLE",     # evidence refs unretrievable
    "R_INDEPENDENCE_VIOLATION",    # self-verification presented as verification
    "R_BATTERY_TRUNCATION",        # battery truncated to meet a deadline
    "R_WINDOW_SKIPPING",           # observation window skipped
    "R_REPAIR_BY_VERIFIER",        # verifier asked/attempted repair
    "R_DOWNGRADE_PRESSURE",        # FAIL->PASS / skip classification / suppress
    "R_CROSS_OWNER_LEAKAGE",       # §8: cross-owner evidence without consent
)

# Downgrade instruction types that trigger R_DOWNGRADE_PRESSURE. The source
# field may be "director" — the refusal applies anyway (spec §4, N4 §7.4).
DOWNGRADE_TYPES = (
    "convert_fail_to_pass",
    "skip_classification",
    "suppress_adversarial_finding",
)

# §6 — inter-node baton contracts VERIFY accepts. VERIFY rereads raw
# observations; it never blindly accepts summaries.
BATON_KINDS = ("action_baton", "claim_baton", "context_baton")
BATON_REQUIRED_FIELDS = {
    "action_baton": ("action_contract", "law_receipt", "execution_receipt",
                     "raw_observations", "expected_outcome"),
    "claim_baton": ("claim", "epistemic_state", "evidence", "provenance",
                    "scope", "limitations", "gaps"),
    "context_baton": ("task_context", "selected_intelligence",
                      "relationship_paths", "applicability", "conflicts",
                      "supersession"),
}

# §5 — Causal Verification Object slots (PDF §20). The CVO is the
# evidence-bearing bridge; CVO != Authority (PDF §21).
CVO_SLOTS = (
    "known",
    "relevant",
    "authorized",
    "done",
    "observed",
    "evidenced",
    "checked",
    "changed",
    "reusable",
)

# §8 — intelligence classes. Class is preserved through verification and into
# derived verification evidence. CORE is never auto-assigned by VERIFY.
INTELLIGENCE_CLASSES = ("CORE", "REUSABLE", "CONTEXT", "REFERENCE", "EPHEMERAL")

# Battery identity (candidate; director-reviewable).
BATTERY_ID = "verify-adversarial-battery"
BATTERY_VERSION = "0.1.0-candidate"

NO_AUTHORITY_GRANT = "no_authority_granted_by_verify"

# ---------------------------------------------------------------------------
# Canonical hashing / determinism helpers
# ---------------------------------------------------------------------------


def _canonical(obj: Any) -> str:
    """Deterministic canonical serialization for hashing."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str)


def _hash(obj: Any) -> str:
    return hashlib.sha256(_canonical(obj).encode("utf-8")).hexdigest()


def _now_iso(now: Optional[str]) -> str:
    if now:
        return now
    return datetime.now(timezone.utc).isoformat()


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
# VERIFICATION_REQUEST contract (spec §0 / §2 / §4)
#
#   verify_key            str    idempotency key; VerifyKey-bound determinism
#   kind                  one of BATON_KINDS
#   subject               baton dict (BATON_REQUIRED_FIELDS[kind])
#   expected_outcome      dict   predeclared success criteria (no goalpost-moving)
#   acceptance_criteria   [{"id": str, "critical": bool, "met": bool, ...}]
#                              critical criteria can never be averaged away
#   evidence_refs         [{"address": str, "class": str|None,
#                           "retrievable": bool, "owner": str|None,
#                           "consent_ref": str|None}]
#   reproducer_seat       {"identity": str, ...}  must differ from deciding seat
#   deciding_seat         {"identity": str, ...}
#   delayed_harm_horizon  "24h"|"7d"|"30d"|"90d"|None  → window hold if set
#   predicted_delta_v     float|None  §7 (aspirational until V2.1 ratified)
#   causal_claim          dict|None   §5 CVO inputs when causality is claimed
# ---------------------------------------------------------------------------


class VerifyNode(NodeBase):
    """NAYA-KERNEL-VERIFY. See module docstring for the contractual role."""

    # -- NodeBase interface ------------------------------------------------

    def manifest_entry(self) -> ManifestEntry:
        """Return this node's manifest entry (candidate spec, §9 acceptance battery)."""
        return ManifestEntry(
            node_id=NODE_ID,
            version=NODE_VERSION,
            responsibilities=[
                "independently reproduce claimed results (RECOMPUTE/REPLICATE/"
                "ADVERSARIAL/AUDIT_SAMPLE) with a different seat (§2)",
                "classify every failure before any code change, using the "
                "8-class taxonomy (§2, N4 §4.2)",
                "run the adversarial battery (tier-1 sync / tier-2 async), "
                "recording every result including failed attacks (§2)",
                "close the four axes (outcome/acceptance/causality/maturity) "
                "without collapsing them (§1)",
                "hold observation windows mechanically via promotionEligible "
                "(§2, candidate 24h/7d/30d/90d schedule)",
                "refuse downgrade pressure — from any seat including the "
                "Director — and receipt the pressure as evidence (§4, N4 §7.4)",
                "emit VerifiedReceipts that LEARN may consume, with MAY-USE / "
                "MUST-NOT-GENERALIZE lists (§6)",
            ],
        )

    def gate(self, state: Dict[str, Any]) -> GateResult:
        """Evaluate VERIFY's gate on `state` (§1 axes, §4 refusals first).

        - downgrade_instruction present → FAIL (refusal receipted).
        - receipt_id present → PASS/FAIL/NEED_EVIDENCE from axis D, with the
          four axes reported in reasons.
        - request present → refusal precheck (§4); PASS is never pre-declared
          for a live claim: at most NEED_EVIDENCE.
        - else → NEED_EVIDENCE (nothing presented).
        """
        state = state or {}
        instruction = state.get("downgrade_instruction")
        if instruction:
            refusal = self.downgrade_pressure(instruction)
            if refusal.get("refused"):
                rid = refusal["refusal"]["id"]
                return GateResult(
                    GateVerdict.FAIL,
                    [f"VERIFY gate FAIL: downgrade pressure refused ({refusal['code']}); "
                     f"refusal receipt {rid} cites the Judgment Rule"],
                )
            # Not a downgrade type after all — continue to receipt/request.
        receipt_id = state.get("receipt_id")
        if receipt_id:
            receipt = self._receipts.get(receipt_id)
            if receipt is None:
                return GateResult(
                    GateVerdict.NEED_EVIDENCE,
                    [f"VERIFY gate: receipt '{receipt_id}' unknown"],
                )
            axes = (
                f"A={receipt['outcome_status']} B={receipt['acceptance_decision']} "
                f"C={receipt['causal_status']} D={receipt['verification_state']}"
            )
            vstate = receipt["verification_state"]
            if vstate == "VERIFIED_PASS":
                return GateResult(
                    GateVerdict.PASS,
                    [f"VERIFY PASS: receipt {receipt_id} closed ({axes}); "
                     "independent reproduction recorded"],
                )
            if vstate in ("FAIL", "CANNOT_VERIFY"):
                return GateResult(
                    GateVerdict.FAIL,
                    [f"VERIFY gate FAIL: receipt {receipt_id} closed ({axes})"],
                )
            return GateResult(
                GateVerdict.NEED_EVIDENCE,
                [f"VERIFY gate: receipt {receipt_id} not closed ({axes})"],
            )
        request = state.get("request")
        if request:
            refusal = self._refusal_precheck(request)
            if refusal:
                return GateResult(
                    GateVerdict.FAIL,
                    [f"VERIFY gate FAIL: request refused ({refusal['code']})"],
                )
            return GateResult(
                GateVerdict.NEED_EVIDENCE,
                ["VERIFY gate: verification accepted into IN_VERIFICATION; "
                 "PASS requires completed reproduction + closed axes"],
            )
        return GateResult(
            GateVerdict.NEED_EVIDENCE,
            ["VERIFY gate: no claim or receipt presented"],
        )

    def persisted_transitions(self) -> List[str]:
        """List the receipt transitions this node persists (candidate spec, §9 acceptance battery)."""
        return list(TRANSITIONS.keys()) + [
            "lineage_correction",      # corrections create a NEW receipt (V1 persists)
            "battery_broken_reopen",   # negative control passing → REOPEN all PASS
            "classification_superseded",  # classification receipts superseded, never edited
        ]

    def evidence_hooks(self) -> List[str]:
        """List the evidence hooks this node exposes (candidate spec, §9 acceptance battery)."""
        return [
            "verification_requests",   # intake registry (verify_key → receipt)
            "verified_receipts",       # hash-bound receipts with the four axes (§1)
            "reproduction_records",    # independence dims + mode per reproduction (§2)
            "adversarial_results",     # tier-1/tier-2 incl. failed attacks (§2)
            "failure_classifications", # taxonomy records, superseded-with-lineage (§2)
            "window_records",          # observation-window holds and closures (§2)
            "refusal_receipts",        # §4 refusals incl. downgrade pressure
            "cvo_objects",             # §5 Causal Verification Objects
            "learn_batons",            # §6 VERIFY→LEARN MAY-USE/MUST-NOT lists
            "propagation_records",     # §6 failure-propagation routing
            "transition_log",          # §3 state-machine transitions
        ]

    def authority_checks(self) -> List[str]:
        """Declare this node's authority checks; declares, never grants (candidate spec, §9 acceptance battery)."""
        # VERIFY performs these validations and grants nothing. The first entry
        # is the negation convention tests assert.
        return [
            NO_AUTHORITY_GRANT,
            "verification request bound to authenticated deciding seat",
            "reproducer seat identity distinct from deciding seat",
            "no parallel authority created by verification receipts",
            "downgrade instructions refused even from director seat",
            "cross-owner evidence requires applicable consent ref",
        ]

    def cold_reconstruct(self, receipts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Rebuild VERIFY's durable state from receipts alone (cold start).

        Replays receipts in issued_at order, re-running `recompute()` on every
        sealed receipt. A receipt that does not recompute to MATCH is not
        trusted: the successor lists it for REOPEN instead (§3; recomputation
        law — mismatch → VERIFICATION_MISMATCH, never trust the earlier
        receipt).
        """
        ordered = sorted(receipts or [], key=lambda r: r.get("issued_at", ""))
        state: Dict[str, Any] = {
            "receipts": {},
            "verify_keys": {},
            "determinism": {"checked": 0, "matched": 0, "mismatched": []},
            "reopened_on_mismatch": [],
        }
        for receipt in ordered:
            rid = receipt.get("id")
            key = receipt.get("verify_key")
            if rid:
                state["receipts"][rid] = {
                    "verification_state": receipt.get("verification_state"),
                    "axes": (
                        receipt.get("outcome_status"),
                        receipt.get("acceptance_decision"),
                        receipt.get("causal_status"),
                        receipt.get("verification_state"),
                    ),
                }
            if key and rid:
                state["verify_keys"][key] = rid
            if receipt.get("sealed"):
                state["determinism"]["checked"] += 1
                if self._recompute_from_receipt(receipt) == "MATCH":
                    state["determinism"]["matched"] += 1
                else:
                    state["determinism"]["mismatched"].append(rid)
                    state["reopened_on_mismatch"].append(rid)
        return state

    # -- internal registry -------------------------------------------------

    def __init__(self) -> None:
        self._receipts: Dict[str, Dict[str, Any]] = {}
        self._verify_keys: Dict[str, str] = {}
        self._refusals: Dict[str, Dict[str, Any]] = {}
        self._transitions: List[Dict[str, Any]] = []
        self._battery_broken: set = set()
        self._seq = 0

    # -- intake (§2, §4) ---------------------------------------------------

    def submit(self, request: Dict[str, Any], now: Optional[str] = None) -> Dict[str, Any]:
        """Accept a verification request into IN_VERIFICATION (§2 protocol).

        Idempotent on verify_key (replay preserves the original evidence/time
        boundary — §2). Runs the §4 refusal precheck first: evidence
        inaccessibility, independence violation, cross-owner leakage without
        consent, battery truncation, window skipping, and downgrade pressure
        are refused (hash-bound refusal receipts), never silently passed.
        """
        request = dict(request or {})
        now_iso = _now_iso(now)
        verify_key = request.get("verify_key")
        if not verify_key:
            return self._refuse(
                "R_EVIDENCE_INACCESSIBLE",
                "verification request has no verify_key; VerifyKey-bound "
                "determinism requires one (§2)",
                request, now_iso,
            )
        if verify_key in self._verify_keys:
            # Replay: the original receipt stands; the original evidence/time
            # boundary is preserved (spec §2 idempotency/replay).
            rid = self._verify_keys[verify_key]
            receipt = self._receipts[rid]
            self._record_transition(
                rid, "REPLAY", receipt["verification_state"],
                receipt["verification_state"],
                "duplicate submit on verify_key; original receipt stands",
                now_iso, request.get("deciding_seat", {}).get("identity", "?"),
            )
            return {"receipt_id": rid, "replay": True, "receipt": receipt}
        refusal = self._refusal_precheck(request)
        if refusal:
            return refusal
        receipt = self._new_receipt(request, now_iso)
        self._transition(
            receipt, "UNVERIFIED", "IN_VERIFICATION", "intake_accepted",
            "claim accepted with evidence refs; expected outcome predeclared",
            now_iso,
        )
        self._receipts[receipt["id"]] = receipt
        self._verify_keys[verify_key] = receipt["id"]
        return {"receipt_id": receipt["id"], "replay": False, "receipt": receipt}

    def _refusal_precheck(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """§4 refusal conditions, checked before any verification work."""
        now_iso = _now_iso(request.get("now"))
        refs = request.get("evidence_refs") or []
        if not refs:
            return self._refuse(
                "R_EVIDENCE_INACCESSIBLE",
                "no evidence refs presented; Observed != Verified (§4)",
                request, now_iso,
            )
        for ref in refs:
            if not ref.get("retrievable", False):
                return self._refuse(
                    "R_EVIDENCE_INACCESSIBLE",
                    f"evidence ref '{ref.get('address', '?')}' not retrievable "
                    "(§4: evidence inaccessibility)",
                    request, now_iso,
                )
        reproducer = (request.get("reproducer_seat") or {}).get("identity")
        deciding = (request.get("deciding_seat") or {}).get("identity")
        if reproducer and deciding and reproducer == deciding:
            # Self-verification presented as verification = provenance failure.
            return self._refuse(
                "R_INDEPENDENCE_VIOLATION",
                "reproducer seat == deciding seat; SelfReport != "
                "IndependentVerification (§4, §2)",
                request, now_iso,
            )
        for ref in refs:
            owner = ref.get("owner")
            requesting_owner = request.get("requesting_owner")
            if (owner and requesting_owner and owner != requesting_owner
                    and not ref.get("consent_ref")):
                # §8: VERIFY never reconstructs a causal claim by exposing one
                # owner's private source to another without applicable consent.
                return self._refuse(
                    "R_CROSS_OWNER_LEAKAGE",
                    f"evidence ref '{ref.get('address', '?')}' owned by "
                    f"'{owner}' lacks consent_ref for '{requesting_owner}' (§8)",
                    request, now_iso,
                )
        if request.get("truncate_battery"):
            return self._refuse(
                "R_BATTERY_TRUNCATION",
                "refuse rather than truncate the battery — a rushed PASS is a "
                "falsified PASS (§4, N4 §7.3)",
                request, now_iso,
            )
        if request.get("skip_window"):
            return self._refuse(
                "R_WINDOW_SKIPPING",
                "observation window may not be skipped; "
                "promotionEligible() blocks promotion mechanically (§4, N4 §7.6)",
                request, now_iso,
            )
        downgrade = request.get("downgrade_instruction")
        if downgrade:
            return self.downgrade_pressure(downgrade, request=request)
        return None

    def _refuse(self, code: str, reason: str, request: Dict[str, Any],
                now_iso: str) -> Dict[str, Any]:
        """Emit a hash-bound refusal receipt (§4). Refusals are receipts too:
        they name the pressure/condition, the evidence, and the law cited."""
        self._seq += 1
        body = {
            "id": f"vref-{_hash([code, reason, self._seq])[:16]}",
            "node_id": NODE_ID,
            "kind": "refusal",
            "code": code,
            "reason": reason,
            "law_cited": (
                "Judgment Rule (Prime Directive, ratified 2026-09-30)"
                if code == "R_DOWNGRADE_PRESSURE" else
                "VERIFY-NODE-SPEC-CANDIDATE.md §4"
            ),
            "verify_key": (request or {}).get("verify_key"),
            "issued_at": now_iso,
            "sealed": True,
            "refused": True,
        }
        body["receipt_hash"] = _hash(body)
        self._refusals[body["id"]] = body
        return {"refused": True, "code": code, "reason": reason,
                "refusal": body}

    # -- downgrade pressure (§4, N4 §7.4) -----------------------------------

    def downgrade_pressure(self, instruction: Dict[str, Any],
                           request: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Refuse any instruction to convert FAIL→PASS, skip classification,
        or suppress an adversarial finding — from ANY seat, including the
        Director — and receipt the pressure as evidence.

        "I was told to" never justifies a false verification (Judgment Rule).
        

        Spec §7.4 — downgrade pressure refused from ANY seat, Director included (Judgment Rule)."""
        instruction = dict(instruction or {})
        now_iso = _now_iso(instruction.get("now"))
        itype = instruction.get("type")
        source = instruction.get("source", "unknown")
        if itype not in DOWNGRADE_TYPES:
            # Not a downgrade instruction at all; nothing to refuse.
            return {"refused": False, "type": itype,
                    "note": "not a downgrade instruction type"}
        reason = (
            f"downgrade pressure refused: '{itype}' from '{source}' — "
            "any instruction, from any seat including the Director, to convert "
            "FAIL→PASS, skip classification, or suppress an adversarial finding "
            "is refused. \"I was told to\" never justifies a false verification."
        )
        return self._refuse("R_DOWNGRADE_PRESSURE", reason,
                            {"verify_key": instruction.get("verify_key"),
                             "instruction": instruction}, now_iso)

    # -- independent reproduction (§2) ---------------------------------------

    def record_reproduction(self, receipt_id: str, mode: str,
                            reproducer_seat: Dict[str, Any],
                            achieved_dims: List[str],
                            result: str,
                            detail: Optional[Dict[str, Any]] = None,
                            now: Optional[str] = None) -> Dict[str, Any]:
        """Record one independent reproduction attempt (§2).

        mode ∈ REPRODUCTION_MODES; achieved_dims names exactly which
        independence dimensions were achieved (fresh-identity same-code runs
        must state this explicitly). result ∈ {"MATCH","MISMATCH","INCONCLUSIVE"}.
        """
        receipt = self._require_live(receipt_id)
        now_iso = _now_iso(now)
        if mode not in REPRODUCTION_MODES:
            raise ValueError(f"unknown reproduction mode '{mode}'")
        deciding = receipt.get("deciding_seat_identity")
        reproducer_id = (reproducer_seat or {}).get("identity")
        if reproducer_id and deciding and reproducer_id == deciding:
            raise ValueError(
                "R_INDEPENDENCE_VIOLATION: reproducer seat == deciding seat")
        if not achieved_dims:
            raise ValueError(
                "independence dimensions must be named explicitly (§2)")
        for dim in achieved_dims:
            if dim not in INDEPENDENCE_DIMS:
                raise ValueError(f"unknown independence dimension '{dim}'")
        if result not in ("MATCH", "MISMATCH", "INCONCLUSIVE"):
            raise ValueError(f"unknown reproduction result '{result}'")
        record = {
            "mode": mode,
            "reproducer_seat": reproducer_id,
            "achieved_dims": list(achieved_dims),
            "result": result,
            "detail": detail or {},
            "recorded_at": now_iso,
        }
        receipt.setdefault("reproductions", []).append(record)
        self._record_transition(
            receipt_id, "REPRODUCE", receipt["verification_state"],
            receipt["verification_state"],
            f"{mode} {result} by '{reproducer_id}' (dims: "
            f"{','.join(achieved_dims)})",
            now_iso, reproducer_id or "?",
        )
        return record

    # -- adversarial battery (§2) --------------------------------------------

    def run_tier1(self, receipt_id: str, battery: Dict[str, Any],
                  now: Optional[str] = None) -> Dict[str, Any]:
        """Tier-1 (synchronous) adversarial battery (§2, PDF §68 subset).

        battery keys:
          recompute_match   bool — RECOMPUTE with same facts+configHash → MATCH
          evidence_ref_integrity bool — every evidence ref hashes to its claim
          gate_conformance  bool — gate re-derivation matches the deciding seat
          negation_probes   [{"probe": str, "passed": bool, "expected": "fail",
                              "note": str}]
          A PASS recorded WITHOUT a negation probe is malformed.
        Every adversarial result is recorded, including failed attacks (§2).
        """
        receipt = self._require_live(receipt_id)
        now_iso = _now_iso(now)
        battery = dict(battery or {})
        probes = battery.get("negation_probes") or []
        verdicts: List[Dict[str, Any]] = []
        for key in ("recompute_match", "evidence_ref_integrity", "gate_conformance"):
            verdicts.append({
                "probe": key, "passed": bool(battery.get(key, False)),
                "expected": "pass",
            })
        if not probes:
            verdicts.append({
                "probe": "negation_probe_presence",
                "passed": False,
                "expected": "pass",
                "note": "MALFORMED: a PASS recorded without a negation probe "
                        "is malformed (§2, PDF §68)",
            })
        for probe in probes:
            verdicts.append({
                "probe": probe.get("probe"),
                "passed": bool(probe.get("passed")),
                "expected": probe.get("expected", "fail"),
                "note": probe.get("note", ""),
            })
        clean = all(v["passed"] == (v["expected"] == "pass") for v in verdicts)
        record = {
            "tier": 1,
            "battery_id": BATTERY_ID,
            "battery_version": BATTERY_VERSION,
            "verdicts": verdicts,
            "clean": clean,
            "recorded_at": now_iso,
        }
        receipt.setdefault("adversarial", {}).setdefault("tier1", []).append(record)
        self._record_transition(
            receipt_id, "TIER1", receipt["verification_state"],
            receipt["verification_state"],
            f"tier-1 battery {'clean' if clean else 'NOT CLEAN'} "
            f"({len(verdicts)} probes)",
            now_iso, receipt.get("deciding_seat_identity", "?"),
        )
        return record

    def run_tier2(self, receipt_id: str, battery: Dict[str, Any],
                  now: Optional[str] = None) -> Dict[str, Any]:
        """Tier-2 (async) adversarial battery (§2, PDF §68 + N4 §4.3).

        negative_controls must FAIL (they are attacks designed to fail); a
        negative control that unexpectedly PASSES declares the battery broken:
        the battery id is marked broken and EVERY VERIFIED_PASS receipt under
        it is REOPENED (new receipts; originals persist) — spec §9 battery
        items 10–11.
        """
        receipt = self._require_live(receipt_id)
        now_iso = _now_iso(now)
        battery = dict(battery or {})
        results: List[Dict[str, Any]] = []
        broken = False
        for control in battery.get("negative_controls") or []:
            passed = bool(control.get("passed"))
            results.append({
                "control": control.get("control"),
                "passed": passed,
                "expected": "fail",
                "note": control.get("note", ""),
            })
            if passed:
                broken = True
        for probe in battery.get("gaming_probes") or []:
            results.append({
                "probe": probe.get("probe"),
                "passed": bool(probe.get("passed")),
                "expected": probe.get("expected", "fail"),
                "note": probe.get("note", ""),
            })
        record = {
            "tier": 2,
            "battery_id": BATTERY_ID,
            "battery_version": BATTERY_VERSION,
            "results": results,
            "battery_broken": broken,
            "recorded_at": now_iso,
        }
        receipt.setdefault("adversarial", {}).setdefault("tier2", []).append(record)
        if broken:
            self._declare_battery_broken(receipt_id, now_iso)
        self._record_transition(
            receipt_id, "TIER2", receipt["verification_state"],
            receipt["verification_state"],
            f"tier-2 battery {'BROKEN' if broken else 'held'} "
            f"({len(results)} controls/probes)",
            now_iso, receipt.get("deciding_seat_identity", "?"),
        )
        return record

    def _declare_battery_broken(self, triggering_receipt_id: str, now_iso: str) -> None:
        """§9 acceptance battery item 10: a negative control that unexpectedly
        passes declares the battery broken — everything under it is REOPENED."""
        self._battery_broken.add(BATTERY_ID)
        for rid, receipt in list(self._receipts.items()):
            adv = receipt.get("adversarial", {})
            under_this_battery = any(
                r.get("battery_id") == BATTERY_ID
                for tier in ("tier1", "tier2") for r in adv.get(tier, [])
            )
            if under_this_battery and receipt["verification_state"] == "VERIFIED_PASS":
                self.reopen(
                    rid,
                    reason=("battery declared broken: a negative control "
                            "unexpectedly passed (spec §9 item 10)"),
                    contradictory_evidence={"battery_id": BATTERY_ID,
                                            "trigger": triggering_receipt_id},
                    now=now_iso,
                )

    # -- failure classification (§2, N4 §4.2) --------------------------------

    def classify_failure(self, receipt_id: str, failure_class: str,
                         evidence: Optional[Dict[str, Any]] = None,
                         now: Optional[str] = None) -> Dict[str, Any]:
        """Classify a falsified claim into the 8-class taxonomy (§2).

        Classification is the OUTPUT of verification — it happens before any
        code change, and VERIFY never repairs (repair-by-verifier is refused).
        Classification receipts are superseded with lineage, never edited.
        """
        receipt = self._require_live(receipt_id)
        now_iso = _now_iso(now)
        if failure_class not in FAILURE_CLASSES:
            raise ValueError(
                f"failure class '{failure_class}' not in the taxonomy; "
                "misclassification is itself a defect (§2)")
        prior = receipt.get("failure_classification")
        classification = {
            "class": failure_class,
            "evidence": evidence or {},
            "classified_at": now_iso,
            "classified_by": receipt.get("deciding_seat_identity", "?"),
            "supersedes": prior.get("id") if prior else None,
        }
        classification["id"] = f"fc-{_hash([receipt_id, failure_class, now_iso, prior])[:16]}"
        receipt["failure_classification"] = classification
        self._record_transition(
            receipt_id, "CLASSIFY", receipt["verification_state"],
            receipt["verification_state"],
            f"failure classified as {failure_class}"
            + (f" (supersedes {prior['id']})" if prior else ""),
            now_iso, classification["classified_by"],
        )
        return classification

    def attempt_repair(self, receipt_id: str) -> Dict[str, Any]:
        """Repair-by-verifier is refused (§4, N4 §7.5).

        Classification is the output; repair re-enters at ACT/PROVE.
        """
        return self._refuse(
            "R_REPAIR_BY_VERIFIER",
            f"repair refused for receipt {receipt_id}: VERIFY classifies; "
            "repair re-enters at ACT/PROVE (§4, N4 §7.5)",
            {"verify_key": receipt_id}, _now_iso(None),
        )

    # -- closing the four axes (§1, §3) --------------------------------------

    def close(self, receipt_id: str, outcome_status: str,
              acceptance_decision: str, causal_status: str,
              target_state: str,
              now: Optional[str] = None) -> Dict[str, Any]:
        """Close verification on a receipt (§1 axes, §3 state machine).

        - Critical acceptance criteria can never be averaged away: if any
          critical criterion is unmet, ACCEPTED is refused mechanically.
        - VERIFIED_PASS requires: sync reproduction (recompute MATCH recorded),
          tier-1 clean (incl. a recorded negation probe), independence named,
          no open delayed-harm window (else PASS_PENDING_WINDOW), and for
          FAIL a classified failure first.
        - acceptance != verification: a verified outcome may be REJECTED (§1).
        """
        receipt = self._require_live(receipt_id)
        now_iso = _now_iso(now)
        for axis, value, allowed in (
            ("outcome_status", outcome_status, OUTCOME_STATUSES),
            ("acceptance_decision", acceptance_decision, ACCEPTANCE_DECISIONS),
            ("causal_status", causal_status, CAUSAL_STATUSES),
        ):
            if value not in allowed:
                raise ValueError(f"{axis} '{value}' not in the axis enum")
        # Critical criteria are never averaged away (spec §1, PDF §16).
        critical_unmet = [
            c["id"] for c in receipt.get("acceptance_criteria", [])
            if c.get("critical") and not c.get("met")
        ]
        if critical_unmet and acceptance_decision == "ACCEPTED":
            raise ValueError(
                f"critical acceptance criteria unmet {critical_unmet}: "
                "critical criteria can never be averaged away (§1, PDF §16)")
        if target_state == "VERIFIED_PASS":
            self._assert_pass_readiness(receipt)
        if target_state == "FAIL" and not receipt.get("failure_classification"):
            raise ValueError(
                "FAIL requires a classified failure first — classification "
                "before verdict (§2, N4 §4.2)")
        receipt["outcome_status"] = outcome_status
        receipt["acceptance_decision"] = acceptance_decision
        receipt["causal_status"] = causal_status
        if target_state == "VERIFIED_PASS" and receipt.get("delayed_harm_horizon"):
            # Material delayed harm possible → window hold; promotionEligible()
            # blocks promotion mechanically until the window closes (§2).
            self._transition(receipt, receipt["verification_state"],
                             "PASS_PENDING_WINDOW", "window_hold",
                             f"delayed-harm window {receipt['delayed_harm_horizon']} "
                             "opened; promotion blocked until closure", now_iso)
            receipt.setdefault("windows", {})["opened_at"] = now_iso
        else:
            self._transition(receipt, receipt["verification_state"],
                             target_state, "close",
                             f"axes closed A={outcome_status} B={acceptance_decision} "
                             f"C={causal_status} D={target_state}", now_iso)
        receipt["learn_baton"] = self._learn_baton_fields(receipt)
        receipt["propagation"] = self._failure_propagation_fields(receipt)
        self._seal(receipt)
        return receipt

    def _assert_pass_readiness(self, receipt: Dict[str, Any]) -> None:
        """Gate every sync-verification PASS on the non-negotiables (§2)."""
        repros = receipt.get("reproductions", [])
        if not any(r.get("mode") == "RECOMPUTE" and r.get("result") == "MATCH"
                   for r in repros):
            raise ValueError(
                "VERIFIED_PASS requires a recorded RECOMPUTE MATCH "
                "(recomputation law, §2)")
        tier1 = (receipt.get("adversarial", {}).get("tier1") or [])
        if not any(r.get("clean") for r in tier1):
            raise ValueError(
                "VERIFIED_PASS requires a clean tier-1 battery incl. a "
                "recorded negation probe (§2, PDF §68)")
        if not any(r.get("achieved_dims") for r in repros):
            raise ValueError(
                "VERIFIED_PASS requires named independence dimensions (§2)")

    def close_window(self, receipt_id: str, outcome: str,
                     evidence: Optional[Dict[str, Any]] = None,
                     now: Optional[str] = None) -> Dict[str, Any]:
        """Close an observation window (§2, §3).

        outcome="clean" → VERIFIED_PASS; "contradictory" → REOPENED (a new
        receipt; the window-held receipt persists with its lineage).
        """
        receipt = self._receipts.get(receipt_id)
        if receipt is None:
            raise KeyError(f"unknown receipt '{receipt_id}'")
        now_iso = _now_iso(now)
        if receipt["verification_state"] != "PASS_PENDING_WINDOW":
            raise ValueError("close_window applies only to PASS_PENDING_WINDOW")
        if outcome == "clean":
            self._transition(receipt, "PASS_PENDING_WINDOW", "VERIFIED_PASS",
                             "window_closed_clean",
                             "observation window closed with no contradictory "
                             "evidence or harm", now_iso)
            receipt.setdefault("windows", {})["closed_clean"] = True
            self._seal(receipt)
            return receipt
        if outcome == "contradictory":
            return self.reopen(
                receipt_id,
                reason="contradictory evidence or harm observed inside the "
                       "observation window (§3)",
                contradictory_evidence=evidence or {},
                now=now_iso,
            )
        raise ValueError("window outcome must be 'clean' or 'contradictory'")

    def reopen(self, receipt_id: str, reason: str,
               contradictory_evidence: Optional[Dict[str, Any]] = None,
               now: Optional[str] = None) -> Dict[str, Any]:
        """REOPEN a receipt (§3): the original persists; a NEW receipt carries
        the re-examination with a REOPENED_BY link. Re-examination is never an
        edit of the original."""
        receipt = self._receipts.get(receipt_id)
        if receipt is None:
            raise KeyError(f"unknown receipt '{receipt_id}'")
        now_iso = _now_iso(now)
        current = receipt["verification_state"]
        transition_name = (
            "window_reopened" if current == "PASS_PENDING_WINDOW"
            else "postpass_reopened" if current == "VERIFIED_PASS"
            else None
        )
        if transition_name is None:
            raise ValueError(
                f"REOPEN applies to PASS_PENDING_WINDOW/VERIFIED_PASS, not {current}")
        self._transition(receipt, current, "REOPENED", transition_name,
                         reason, now_iso)
        self._seal(receipt)
        new_key = f"{receipt['verify_key']}:reopen:{_hash([receipt_id, now_iso])[:8]}"
        new_request = dict(receipt.get("request_snapshot", {}))
        new_request["verify_key"] = new_key
        new_receipt = self._new_receipt(new_request, now_iso)
        new_receipt["reopened_by"] = receipt_id
        new_receipt["reopen_reason"] = reason
        new_receipt["contradictory_evidence"] = contradictory_evidence or {}
        new_receipt["verify_version"] = receipt.get("verify_version", 1) + 1
        self._transition(new_receipt, "UNVERIFIED", "IN_VERIFICATION",
                         "intake_accepted",
                         f"re-examination of {receipt_id}: {reason}", now_iso)
        self._receipts[new_receipt["id"]] = new_receipt
        self._verify_keys[new_key] = new_receipt["id"]
        return new_receipt

    def correct(self, receipt_id: str, correction: Dict[str, Any],
                now: Optional[str] = None) -> Dict[str, Any]:
        """§2 idempotency/versioning: corrections create a NEW lineage receipt
        (V1 PASS at t0, V2 FAIL at t1 — both persist)."""
        receipt = self._receipts.get(receipt_id)
        if receipt is None:
            raise KeyError(f"unknown receipt '{receipt_id}'")
        now_iso = _now_iso(now)
        new_key = f"{receipt['verify_key']}:v{receipt.get('verify_version', 1) + 1}"
        new_request = dict(receipt.get("request_snapshot", {}))
        new_request["verify_key"] = new_key
        new_request["correction_of"] = receipt_id
        new_request["correction"] = correction
        new_receipt = self._new_receipt(new_request, now_iso)
        new_receipt["supersedes"] = receipt_id
        new_receipt["verify_version"] = receipt.get("verify_version", 1) + 1
        self._receipts[new_receipt["id"]] = new_receipt
        self._verify_keys[new_key] = new_receipt["id"]
        self._record_transition(
            new_receipt["id"], "LINEAGE_CORRECTION",
            "UNVERIFIED", "UNVERIFIED",
            f"correction lineage of {receipt_id}: {correction.get('note', '')}",
            now_iso, receipt.get("deciding_seat_identity", "?"),
        )
        return new_receipt

    def promotion_eligible(self, receipt_id: str) -> bool:
        """§2: while material delayed harm is possible (PASS_PENDING_WINDOW
        with an open window), promotion is blocked MECHANICALLY."""
        receipt = self._receipts.get(receipt_id)
        if receipt is None:
            return False
        if receipt["verification_state"] == "PASS_PENDING_WINDOW":
            return False
        return receipt["verification_state"] == "VERIFIED_PASS"

    # -- recomputation law (§2, PDF §50) --------------------------------------

    def recompute(self, receipt_id: str) -> str:
        """Re-derive the verdict from (CanonicalEvidence, ExpectedOutcome,
        AcceptanceCriteria). Mismatch → VERIFICATION_MISMATCH: never trust the
        earlier receipt.

        Spec §2 — recomputation law (Verdict' = f(canonical evidence, expected outcome, acceptance criteria))."""
        receipt = self._receipts.get(receipt_id)
        if receipt is None:
            return "UNKNOWN_RECEIPT"
        if not receipt.get("sealed"):
            return "MISMATCH"
        verdict = self._recompute_from_receipt(receipt)
        if verdict == "MISMATCH":
            self._record_transition(
                receipt_id, "VERIFICATION_MISMATCH",
                receipt["verification_state"], receipt["verification_state"],
                "recomputation law: re-derived verdict differs from the "
                "stored verdict — the earlier receipt is not trusted (§2, PDF §50)",
                _now_iso(None), receipt.get("deciding_seat_identity", "?"),
            )
        return verdict

    def _recompute_from_receipt(self, receipt: Dict[str, Any]) -> str:
        """Re-derive the four axes from the sealed evidence and compare.

        Verdict' = f(CanonicalEvidence, ExpectedOutcome, AcceptanceCriteria):
        the stored axes must be the mechanical consequence of the stored
        evidence, the predeclared expected outcome, and the acceptance
        criteria — otherwise MISMATCH.
        """
        stored_hash = receipt.get("receipt_hash")
        body = {k: v for k, v in receipt.items() if k != "receipt_hash"}
        if _hash(body) != stored_hash:
            return "MISMATCH"
        # Axis D must be entailed by the recorded work: a VERIFIED_PASS with
        # no clean tier-1, no recompute MATCH, or no named independence is a
        # recomputation mismatch by construction.
        vstate = receipt.get("verification_state")
        if vstate == "VERIFIED_PASS":
            repros = receipt.get("reproductions", [])
            tier1 = (receipt.get("adversarial", {}).get("tier1") or [])
            ok = (
                any(r.get("mode") == "RECOMPUTE" and r.get("result") == "MATCH"
                    for r in repros)
                and any(r.get("clean") for r in tier1)
                and any(r.get("achieved_dims") for r in repros)
            )
            if not ok:
                return "MISMATCH"
        if vstate == "FAIL" and not receipt.get("failure_classification"):
            return "MISMATCH"
        return "MATCH"

    # -- §6 batons (VERIFY→LEARN, failure propagation) ------------------------

    def _learn_baton_fields(self, receipt: Dict[str, Any]) -> Dict[str, Any]:
        """VERIFY→LEARN: expected vs actual, evidence, acceptance, causal
        status, surviving alternatives, window state, recomputation status,
        and the explicit MAY-USE / MUST-NOT-GENERALIZE lists (§6, PDF §66).

        Aliveness gate (PDF §82): VERIFY must change LEARN eligibility, or it
        is decorative — a FAIL/REOPENED receipt always lands on the
        MUST-NOT-GENERALIZE list.
        """
        vstate = receipt["verification_state"]
        may_use: List[str] = []
        must_not: List[str] = []
        if vstate == "VERIFIED_PASS":
            may_use.append(receipt["verify_key"])
        else:
            must_not.append(receipt["verify_key"])
        return {
            "may_use": may_use,
            "must_not_generalize": must_not,
            "surviving_alternatives": receipt.get("surviving_alternatives", []),
            "window_state": receipt.get("windows", {}),
            "causal_status": receipt["causal_status"],
            "value": receipt.get("value", {}),
        }

    def learn_baton(self, receipt_id: str) -> Dict[str, Any]:
        """Return the VERIFY→LEARN baton for a sealed receipt (§6)."""
        receipt = self._receipts.get(receipt_id)
        if receipt is None:
            raise KeyError(f"unknown receipt '{receipt_id}'")
        if not receipt.get("sealed"):
            raise ValueError("learn_baton requires a sealed (closed) receipt")
        return receipt.get("learn_baton", {})

    def _failure_propagation_fields(self, receipt: Dict[str, Any]) -> Dict[str, Any]:
        """§6 / N4 §8 failure propagation: FAIL → LEARN (pattern only, not
        learning input), EVOLVE (failed_verifications[]), SELF (known
        failures), LAW (AUTHORITY_VIOLATION/PROVENANCE_FAILURE as integrity
        events), deciding seat (feedback). Nothing deleted; claim → attack →
        classification → consequence all persist, linked."""
        classification = receipt.get("failure_classification") or {}
        fclass = classification.get("class")
        routes: Dict[str, Any] = {
            "learn": {"pattern_only": True, "learning_input": False,
                      "verify_key": receipt["verify_key"]},
            "evolve": {"failed_verifications": [receipt["id"]] if fclass else []},
            "self": {"known_failures": [receipt["verify_key"]] if fclass else []},
            "deciding_seat": {"feedback": classification.get("evidence", {})},
            "law": {"integrity_events": []},
        }
        if fclass in ("AUTHORITY_VIOLATION", "PROVENANCE_FAILURE"):
            routes["law"]["integrity_events"].append({
                "class": fclass, "receipt_id": receipt["id"],
            })
        return routes

    def failure_propagation(self, receipt_id: str) -> Dict[str, Any]:
        """Return the persisted failure-propagation routing for a receipt (§6)."""
        receipt = self._receipts.get(receipt_id)
        if receipt is None:
            raise KeyError(f"unknown receipt '{receipt_id}'")
        return receipt.get("propagation", {})

    # -- §5 CVO, §7 value, §8 class preservation --------------------------------

    def build_cvo(self, receipt_id: str, slots: Dict[str, Any],
                  now: Optional[str] = None) -> Dict[str, Any]:
        """Attach a Causal Verification Object (§5, PDF §20): what was known /
        relevant / authorized / done / observed / evidenced / independently
        checked / changed / reusable by a successor. CVO != Authority (§5)."""
        receipt = self._require_live(receipt_id)
        missing = [s for s in CVO_SLOTS if s not in (slots or {})]
        if missing:
            raise ValueError(f"CVO missing slots {missing} (§5, PDF §20)")
        receipt["cvo"] = {s: slots[s] for s in CVO_SLOTS}
        receipt["cvo"]["recorded_at"] = _now_iso(now)
        return receipt["cvo"]

    def record_value(self, receipt_id: str, predicted_delta_v: Optional[float],
                     actual_delta_v: Optional[float],
                     now: Optional[str] = None) -> Dict[str, Any]:
        """§7: VERIFY owns the reality side — predicted vs actual value.
        CalibrationError = |ΔV_predicted − ΔV_actual|. Outcome verification
        and value verification remain distinct dimensions (PDF §60).

        The Decision Value Calculus V2.1 is RATIFIED law (bound into main via
        #1186/#1190/#1192, FLAG-001 step 4); V2.1-derived value states are
        no longer aspirational. The receipt binds the ratified config hash.
        """
        receipt = self._require_live(receipt_id)
        calibration = None
        if predicted_delta_v is not None and actual_delta_v is not None:
            calibration = abs(predicted_delta_v - actual_delta_v)
        receipt["value"] = {
            "predicted_delta_v": predicted_delta_v,
            "actual_delta_v": actual_delta_v,
            "calibration_error": calibration,
            "aspirational": False,
            "calculusVersion": CALCULUS_V21_VERSION,
            "configHash": CALCULUS_V21_SPEC_HASH,
            "recorded_at": _now_iso(now),
        }
        return receipt["value"]

    # -- deletion is not a thing (§3, N4 §5.2) ---------------------------------

    def delete_receipt(self, receipt_id: str) -> None:
        """VERIFY has no delete operation, on any stream, ever (§3)."""
        raise RuntimeError(
            "VERIFY has no delete operation — append-only ledger (§3, N4 §5.2)")

    # -- internals --------------------------------------------------------------

    def _require_live(self, receipt_id: str) -> Dict[str, Any]:
        receipt = self._receipts.get(receipt_id)
        if receipt is None:
            raise KeyError(f"unknown receipt '{receipt_id}'")
        if receipt.get("sealed") and receipt["verification_state"] in TERMINAL_STATES:
            raise ValueError(
                f"receipt {receipt_id} is terminal ({receipt['verification_state']}); "
                "re-examination is a new receipt (§3)")
        return receipt

    def _new_receipt(self, request: Dict[str, Any], now_iso: str) -> Dict[str, Any]:
        kind = request.get("kind")
        if kind not in BATON_KINDS:
            raise ValueError(f"baton kind '{kind}' not in {BATON_KINDS}")
        subject = request.get("subject") or {}
        missing = [f for f in BATON_REQUIRED_FIELDS[kind] if f not in subject]
        if missing:
            raise ValueError(
                f"{kind} missing baton fields {missing} — VERIFY rereads raw "
                "observations, never blind summaries (§6)")
        request = dict(request)
        self._seq += 1
        evidence_refs = request.get("evidence_refs") or []
        receipt = {
            "id": f"vr-{_hash([request.get('verify_key'), self._seq])[:16]}",
            "node_id": NODE_ID,
            "node_version": NODE_VERSION,
            "verify_key": request.get("verify_key"),
            "verify_version": 1,
            "supersedes": None,
            "reopened_by": None,
            "kind": kind,
            "subject_ref": {k: subject.get(k) for k in BATON_REQUIRED_FIELDS[kind]},
            "expected_outcome": request.get("expected_outcome") or {},
            "acceptance_criteria": list(request.get("acceptance_criteria") or []),
            "outcome_status": "NOT_PROVEN",
            "acceptance_decision": "PENDING",
            "causal_status": "NOT_CLAIMED" if not request.get("causal_claim") else "CLAIMED",
            "verification_state": "UNVERIFIED",
            "failure_classification": None,
            "reproductions": [],
            "adversarial": {"tier1": [], "tier2": []},
            "delayed_harm_horizon": request.get("delayed_harm_horizon"),
            "windows": {},
            "evidence_refs": evidence_refs,
            "evidence_classes": [  # §8: class preserved through verification
                ref.get("class") for ref in evidence_refs
            ],
            "cvo": {},
            "value": {},
            "learn_baton": {"may_use": [], "must_not_generalize": []},
            "propagation": {},
            "deciding_seat_identity": (request.get("deciding_seat") or {}).get("identity"),
            "request_snapshot": {k: v for k, v in request.items()
                                 if k != "downgrade_instruction"},
            "config_hash": request.get("config_hash"),
            "issued_at": now_iso,
            "issued_by": (request.get("deciding_seat") or {}).get("identity"),
            "sealed": False,
        }
        return receipt

    def _transition(self, receipt: Dict[str, Any], before: str, after: str,
                    name: str, reason: str, now_iso: str) -> None:
        expected = TRANSITIONS.get(name)
        if expected is not None and (before, after) != expected:
            raise ValueError(
                f"illegal transition '{name}': {before}→{after}; "
                f"spec §3 allows {expected[0]}→{expected[1]}")
        self._record_transition(receipt["id"], name, before, after, reason,
                                now_iso, receipt.get("deciding_seat_identity", "?"))
        receipt["verification_state"] = after

    def _record_transition(self, receipt_id: str, name: str, before: str,
                           after: str, reason: str, now_iso: str,
                           verifier_seat: str) -> None:
        self._transitions.append({
            "receipt_id": receipt_id,
            "transition": name,
            "before": before,
            "after": after,
            "reason": reason,
            "execution_id": f"vx-{_hash([receipt_id, name, now_iso, len(self._transitions)])[:12]}",
            "evidence_refs": [],
            "verifier_seat": verifier_seat,
            "recorded_at": now_iso,
        })

    def _seal(self, receipt: Dict[str, Any]) -> None:
        """Seal the receipt: extra fields are sealed UNDER the receipt_hash."""
        receipt["sealed"] = True
        body = {k: v for k, v in receipt.items() if k != "receipt_hash"}
        receipt["receipt_hash"] = _hash(body)
