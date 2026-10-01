"""NAYA-KERNEL-ACT — CANDIDATE implementation (NOT RATIFIED — NOT MERGED).

Implements the ACT node contract from ACT-NODE-SPEC-CANDIDATE.md (draft)
against the NodeBase interface. Candidate code on a feature branch: it proves
the spec is implementable; it grants nothing, merges nothing, deploys nothing.

Contractual responsibility (spec §0): ACT is the only node that produces
effects in the world. LAW decides; ACT does. Every authorized decision
becomes real through exactly one disciplined path: claim the execution under
an idempotency key, invoke only registered tools within the granted authority
envelope, observe the effects, and emit a receipt that a cold successor can
trust.

Gate input contract (`state` dict keys; all reads explicit, nothing inferred):
  decision_receipt {
    receipt_id: str, decision: "ACT" | "READ_MORE" | "ASK" | "REFUSE",
    winner: {tool_id: str, version: str|None, params: {...}, bounds: {...}},
    authority_basis: {kind: str, ref: str, revoked: bool},
    calculusVersion: str, configHash: str, configHashCurrent: str,
    reversibility: float, stakes: str,
    issued_at: str, valid_until: str, issued_by: str,
    execution_budget: {timeout_ms: int, max_retries: int, read_more_loop: int},
    flags: {harm_flag: bool, harm_facts: [...],
            known_wrong_flag: bool, known_wrong_facts: [...]},
    read_more_directive: {...} | None,
    decision_brief: {...} | None,
    receipt_hash: str | None           # hash-bound receipt for §4.1 recompute
  }
  tool_registry: {tool_id: {version, authority_class, idempotent,
                            max_timeout_ms, retry_policy,
                            required_authority: str, compensating_tool: str|None,
                            evidence_capture: str}}
  execution_ledger: {idempotency_key: ExecutionRecord}   # persisted ledger
  now: str | None                          # injection point; default UTC now

Gate outcomes (spec §4, intake) map onto NodeBase.GateVerdict as:
  ADMITTED (the decision verb's path will be served)   -> PASS
     (ACT, READ_MORE within bound, and ASK are admitted; the READ_MORE/
     ASK paths emit their own receipts through execute() — a loop or
     suspension is not a failure, just not an execution)
  READ_MORE bound breached (forced ASK, §2.2)          -> NEED_EVIDENCE
  REFUSED (§4.1–4.8)                                   -> FAIL (terminal for this receipt)

The four execution paths (§2) run through `execute()`. The full typed
ExecutionReceipt (§6) is kept on the instance as `last_receipt`; GateResult
reasons carry the path name and receipt id. ACT never re-scores, never
overrides the verb, never grants authority: authority_checks() declares
validations only.
"""

from __future__ import annotations

import fnmatch
import hashlib
import json
from datetime import datetime, timedelta, timezone
from typing import Any, Callable, Dict, List, Optional, Tuple

from naya_kernel.node_base import GateResult, GateVerdict, ManifestEntry, NodeBase

NODE_ID = "NAYA-KERNEL-ACT"
NODE_VERSION = "0.1.0-candidate"
PIPELINE_POSITION = 3

# §2 — the four execution paths; there is no fifth path.
PATH_EXECUTED = "EXECUTED"
PATH_READ_MORE_LOOP = "READ_MORE_LOOP"
PATH_ASK_SUSPENDED = "ASK_SUSPENDED"
PATH_REFUSED = "REFUSED"
PATH_FAILED = "FAILED"
PATH_CANCELLED = "CANCELLED"
PATH_TIMED_OUT = "TIMED_OUT"

# §6 receipt outcomes / error classes.
OUTCOME_SUCCESS = "SUCCESS"
OUTCOME_FAILURE = "FAILURE"
OUTCOME_TIMEOUT = "TIMEOUT"
OUTCOME_REFUSED = "REFUSED"
OUTCOME_CONFLICT = "CONFLICT"

ERROR_TRANSIENT = "TRANSIENT"
ERROR_PERMANENT = "PERMANENT"
ERROR_AUTHORITY = "AUTHORITY"
ERROR_HARM_SIGNAL = "HARM_SIGNAL"

# §7.2 lifecycle states.
S_AUTHORIZED = "AUTHORIZED"
S_CLAIMED = "CLAIMED"
S_EXECUTING = "EXECUTING"
S_RECOVERABLE = "RECOVERABLE"
S_EFFECTS_OBSERVED = "EFFECTS_OBSERVED"
S_RECEIPTED = "RECEIPTED"
S_REFUSED = "REFUSED"
S_FAILED = "FAILED"
S_TIMED_OUT = "TIMED_OUT"
S_CANCELLED = "CANCELLED"
S_COMPENSATED = "COMPENSATED"
S_ASK_SUSPENDED = "ASK_SUSPENDED"

TERMINAL_STATES = frozenset({
    S_RECEIPTED, S_REFUSED, S_FAILED, S_TIMED_OUT,
    S_CANCELLED, S_COMPENSATED, S_ASK_SUSPENDED,
})

# Legal transitions (from -> set(to)). Everything else fails closed (§7.2).
LEGAL_TRANSITIONS: Dict[str, frozenset] = {
    S_AUTHORIZED: frozenset({S_CLAIMED, S_REFUSED}),
    S_CLAIMED: frozenset({S_EXECUTING, S_RECOVERABLE, S_REFUSED}),
    S_EXECUTING: frozenset({S_EFFECTS_OBSERVED, S_FAILED, S_TIMED_OUT,
                            S_CANCELLED, S_RECOVERABLE}),
    S_EFFECTS_OBSERVED: frozenset({S_RECEIPTED}),
    S_RECOVERABLE: frozenset({S_EXECUTING, S_REFUSED}),
    S_RECEIPTED: frozenset({S_COMPENSATED}),
    S_FAILED: frozenset({S_COMPENSATED}),
    S_REFUSED: frozenset(),
    S_TIMED_OUT: frozenset(),
    S_CANCELLED: frozenset(),
    S_COMPENSATED: frozenset(),
    S_ASK_SUSPENDED: frozenset({S_CANCELLED}),
}

# §3 authority classes. IRREVERSIBLE and EXTERNAL_EFFECT require the receipt
# to name the irreversibility explicitly (AskHuman Consequential
# Irreversibility law); enforced via `reversibility` / explicit flags on the
# decision receipt.
TOOL_CLASS_READ = "READ"
TOOL_CLASS_WRITE_SCOPED = "WRITE_SCOPED"
TOOL_CLASS_WRITE_BROAD = "WRITE_BROAD"
TOOL_CLASS_IRREVERSIBLE = "IRREVERSIBLE"
TOOL_CLASS_EXTERNAL_EFFECT = "EXTERNAL_EFFECT"

# §7.3 — circuit breaker. Candidate default: 5 consecutive failures trip OPEN.
CIRCUIT_TRIP_THRESHOLD = 5
CIRCUIT_COOLDOWN_MS = 60_000

# §2.2 — READ_MORE loop bound. Candidate default: 3 round-trips, then forced
# ASK. The loop count arrives on the decision receipt (`execution_budget`
# may override); the default is declared in every receipt.
DEFAULT_READ_MORE_LOOP_BOUND = 3

# §5.4 — lease default when the caller does not name one.
DEFAULT_LEASE_MS = 30_000


def _canonical(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str)


def _sha256(obj: Any) -> str:
    return hashlib.sha256(_canonical(obj).encode("utf-8")).hexdigest()


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _deepcopy_json(obj: Any) -> Any:
    return json.loads(_canonical(obj))


def _params_hash(params: Any) -> str:
    return _sha256(params)


class ActNode(NodeBase):
    """NAYA-KERNEL-ACT. The only node that produces effects in the world."""

    def __init__(
        self,
        executor: Optional[Callable[[str, Dict[str, Any]], Dict[str, Any]]] = None,
    ) -> None:
        """`executor(tool_id, params)` invokes the tool and returns a dict:
        {status: "ok"|"error"|"timeout"|"harm_signal"|"refused",
         effects: str (observed effects), error_class: one of the ERROR_*
         constants, error_detail: str}. In production this is the bounded
        tool-call seam; in tests it is a stub. ACT never invents effects:
        with no executor the ACT path refuses under §4.7 (evidence capture
        impossible — ACT cannot observe what it cannot invoke observably).
        """
        self._executor = executor
        self.last_receipt: Optional[Dict[str, Any]] = None
        # Persisted execution ledger mirror: key -> execution record.
        # In production this is the SmartLedger `execution` stream (§10.6);
        # here it is the node's durable state for tests and cold-start demos.
        self.ledger: Dict[str, Dict[str, Any]] = {}
        # Circuit breaker state: tool_id -> {consecutive_failures, state, opened_at}
        self._breakers: Dict[str, Dict[str, Any]] = {}

    # ------------------------------------------------------------------
    # NodeBase interface
    # ------------------------------------------------------------------
    def manifest_entry(self) -> ManifestEntry:
        """Node identity + responsibilities (spec §8.1)."""
        return ManifestEntry(
            node_id=NODE_ID,
            version=NODE_VERSION,
            responsibilities=[
                "claim authorized executions under an idempotency key",
                "invoke only registered tools within the granted authority envelope",
                "serve the four execution paths (ACT/READ_MORE/ASK/REFUSE)",
                "observe effects and emit hash-bound ExecutionReceipts",
                "enforce claim races, leases, and fail-closed fingerprint conflicts",
                "reconstruct in-flight state for cold successors from receipts",
            ],
        )

    def gate(self, state: Dict[str, Any]) -> GateResult:
        """Admission intake for a decision receipt (spec §4).

        Verifies the receipt is present, recomputable, fresh, authority-valid,
        and flag-clean, then admits the decision verb's path. The invocation
        rule (§3) is evaluated at admission for the ACT verb so an
        unregistered or out-of-envelope tool refuses before any claim.
        """
        receipt = state.get("decision_receipt") or {}
        registry = state.get("tool_registry") or {}
        now = state.get("now") or _now_iso()

        verdict, reasons = self._admit(receipt, registry, now)
        return GateResult(verdict=verdict, reasons=reasons)

    def persisted_transitions(self) -> List[str]:
        """Legal §7.2 state-machine edges in 'FROM -> TO' form (spec §8.1)."""
        return [f"{frm} -> {to}" for frm, tos in LEGAL_TRANSITIONS.items()
                for to in sorted(tos)]

    def evidence_hooks(self) -> List[str]:
        """SmartLedger evidence streams this node writes (spec §8.1)."""
        return [
            "smartledger.execution (ExecutionReceipt stream, proposed)",
            "tool.effects_observed (per-tool evidence_capture declaration)",
            "conflict receipts (fail-closed fingerprint conflicts)",
            "lease heartbeats (claim liveness evidence)",
            "circuit breaker state (per-tool failure counters)",
        ]

    def authority_checks(self) -> List[str]:
        """Authority declarations — declared only, never granted (spec §8.1)."""
        return [
            "decision receipt recompute under bound configHash (§4.1)",
            "receipt freshness: valid_until, config hash, authority revocation (§4.2)",
            "tool registration at pinned version (§4.3)",
            "required_authority predicate satisfied by authority_basis (§3)",
            "irreversibility naming for IRREVERSIBLE/EXTERNAL_EFFECT tools (§3)",
            "no authority grant/inference/expansion/persistence — declared only",
        ]

    def cold_reconstruct(self, receipts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Deterministic §8 reconstruction from the ledger alone.

        Returns a recovery plan: for each in-flight execution, one of
        "leave_alone", "done", "re_executable", "recovery_eligible",
        "unknown_effects_brief_human", "ask_suspended_survives". Two cold
        successors given the same receipts reach the same plan.
        """
        now = _now_iso()
        in_flight = ["CLAIMED", "EXECUTING", "ASK_SUSPENDED"]
        records = [r for r in receipts
                   if r.get("stream") == "execution" or "path" in r]

        # Index receipts by key: keep the latest final receipt per key.
        final_by_key: Dict[str, Dict[str, Any]] = {}
        claims: Dict[str, Dict[str, Any]] = {}
        for r in records:
            key = r.get("idempotency_key") or r.get("key")
            if not key:
                continue
            path = r.get("path")
            if path in (PATH_EXECUTED, PATH_REFUSED, PATH_FAILED,
                        PATH_TIMED_OUT, PATH_CANCELLED):
                final_by_key[key] = r
            elif path in ("CLAIMED", "EXECUTING") or r.get("state") in in_flight:
                claims[key] = r
            elif r.get("path") == PATH_ASK_SUSPENDED or r.get("state") == "ASK_SUSPENDED":
                claims[key] = r

        plan: List[Dict[str, Any]] = []
        for key in sorted(set(list(final_by_key.keys()) + list(claims.keys()))):
            claim = claims.get(key)
            final = final_by_key.get(key)
            if final is not None:
                plan.append({"key": key, "action": "done",
                             "reason": f"final receipt {final.get('receipt_id', final.get('path'))} exists; touch nothing"})
                continue
            if claim is None:
                continue
            state = claim.get("state") or claim.get("path")
            if state in ("ASK_SUSPENDED", PATH_ASK_SUSPENDED):
                plan.append({"key": key, "action": "ask_suspended_survives",
                             "reason": "brief persisted; human answer resumes via fresh LAW decision"})
                continue
            lease_deadline = claim.get("lease_deadline")
            live = lease_deadline is not None and lease_deadline > now
            heartbeat = claim.get("heartbeat_at")
            heartbeat_fresh = heartbeat is not None and heartbeat > now
            if live and (heartbeat_fresh or heartbeat is None):
                plan.append({"key": key, "action": "leave_alone",
                             "reason": "live lease; another instance owns it"})
                continue
            # Lease expired: recovery-eligible (§8 step 2).
            tool_info = claim.get("tool") or {}
            idempotent = bool(tool_info.get("idempotent", False))
            effects_known = claim.get("effects_observed") not in (None, "")
            if idempotent:
                plan.append({"key": key, "action": "re_executable",
                             "reason": "idempotent tool, no receipt; re-execute under same key with new execution_id"})
            elif effects_known:
                plan.append({"key": key, "action": "recovery_eligible",
                             "reason": "effects known, non-idempotent; proceed per stored evidence"})
            else:
                plan.append({"key": key, "action": "unknown_effects_brief_human",
                             "reason": "non-idempotent, no receipt, effects unknown; do NOT blindly re-execute"})

        return {
            "node_id": NODE_ID,
            "reconstructed_at": now,
            "keys_examined": len(plan),
            "plan": plan,
            "deterministic": True,
        }

    # ------------------------------------------------------------------
    # Execution — the four paths (§2)
    # ------------------------------------------------------------------
    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Serve one decision receipt through its verb's path (§2).

        Admission (§4) runs first; on admission the verb selects the path.
        Returns the handoff (§1.2): {execution_id, decision_ref, path,
        receipt, ticket}.
        """
        receipt_in = state.get("decision_receipt") or {}
        registry = state.get("tool_registry") or {}
        ledger = state.get("execution_ledger")
        if ledger is None:
            ledger = self.ledger
        now = state.get("now") or _now_iso()

        gate_verdict, gate_reasons = self._admit(
            receipt_in, registry, now, grants=state.get("grants"))
        decision = receipt_in.get("decision")
        decision_ref = receipt_in.get("receipt_id") or "unknown"

        if gate_verdict == GateVerdict.FAIL:
            return self._handoff_refused(
                decision_ref, ledger, now, gate_reasons, refusal_gate="admission")
        if gate_verdict == GateVerdict.NEED_EVIDENCE:
            return self._handoff_awaiting(decision_ref, ledger, now,
                                          gate_reasons, decision)

        if decision == "ACT":
            return self._path_act(receipt_in, registry, ledger, now)
        if decision == "READ_MORE":
            return self._path_read_more(receipt_in, ledger, now)
        if decision == "ASK":
            return self._path_ask(receipt_in, ledger, now)
        # Decision REFUSE was already failed by admission with the LAW reasons
        # carried on the refusal receipt (§2.4); nothing more to route.
        # Unreachable: _admit fails unknown verbs before routing (§2).
        return self._handoff_refused(
            decision_ref, ledger, now,
            ["unreachable: admission failed this verb; see admission reasons"],
            refusal_gate="unknown_verb")

    # ------------------------------------------------------------------
    # Admission (§4) — refuses before anything can happen
    # ------------------------------------------------------------------
    def _admit(self, receipt: Dict[str, Any], registry: Dict[str, Any],
               now: str, grants: Optional[List[Dict[str, Any]]] = None
               ) -> Tuple[GateVerdict, List[str]]:
        reasons: List[str] = []

        # §4.6 hard stops run before everything else: no scoring, no appeal.
        flags = receipt.get("flags") or {}
        if flags.get("harm_flag"):
            reasons.append("REFUSE §4.6: harmFlag (LAW_OF_ONE) — no scoring, no appeal")
            return GateVerdict.FAIL, reasons
        if flags.get("known_wrong_flag"):
            reasons.append("REFUSE §4.6: knownWrongFlag (Judgment Rule) — no scoring, no appeal")
            return GateVerdict.FAIL, reasons
        if flags.get("tau_zero_class"):
            reasons.append(f"REFUSE §4.6: τ=0 class {flags.get('tau_zero_class')} — zero tolerance")
            return GateVerdict.FAIL, reasons

        # §4.1 no LAW receipt / fails recompute.
        if not receipt.get("receipt_id"):
            reasons.append("REFUSE §4.1: no decision receipt — ACT acts on authorization, not intention")
            return GateVerdict.FAIL, reasons
        if not self._recompute_ok(receipt):
            reasons.append("REFUSE §4.1: receipt fails recompute() under bound configHash")
            return GateVerdict.FAIL, reasons

        # §4.2 stale or superseded receipt.
        valid_until = receipt.get("valid_until")
        if valid_until and now > valid_until:
            reasons.append(f"REFUSE §4.2: stale receipt (now {now} > valid_until {valid_until})")
            return GateVerdict.FAIL, reasons
        if (receipt.get("configHash") and receipt.get("configHashCurrent")
                and receipt["configHash"] != receipt["configHashCurrent"]):
            reasons.append("REFUSE §4.2: config hash moved since issuance — superseded receipt")
            return GateVerdict.FAIL, reasons
        basis = receipt.get("authority_basis") or {}
        if basis.get("revoked"):
            reasons.append(f"REFUSE §4.2: authority basis {basis.get('ref')} revoked")
            return GateVerdict.FAIL, reasons

        decision = receipt.get("decision")
        if decision == "READ_MORE":
            bound = (receipt.get("execution_budget") or {}).get("read_more_bound",
                                                                 DEFAULT_READ_MORE_LOOP_BOUND)
            loop = (receipt.get("execution_budget") or {}).get("read_more_loop", 0)
            if loop >= bound:
                reasons.append(
                    f"READ_MORE loop bound reached ({loop} >= {bound}) — forcing ASK (§2.2)")
                return GateVerdict.NEED_EVIDENCE, reasons
            reasons.append(f"ADMITTED READ_MORE: returning to KNOW (loop {loop}/{bound})")
            return GateVerdict.PASS, reasons
        if decision == "ASK":
            reasons.append("ADMITTED ASK: suspending for the human — silence never equals consent")
            return GateVerdict.PASS, reasons
        if decision == "REFUSE":
            law_reasons = flags.get("refusal_reasons") or "law reasons carried on the receipt"
            reasons.append(f"REFUSE verdict from LAW — terminating with reasons (§2.4): {law_reasons}")
            return GateVerdict.FAIL, reasons
        if decision != "ACT":
            reasons.append(
                f"REFUSE: unknown decision verb {decision!r} — there is no fifth path (§2)")
            return GateVerdict.FAIL, reasons

        # §4.3 + §3 invocation rule, evaluated at admission so refusal lands
        # before any claim or lease.
        winner = receipt.get("winner") or {}
        tool_id = winner.get("tool_id")
        reg = (registry or {}).get(tool_id) if tool_id else None
        if tool_id is None or reg is None:
            reasons.append(f"REFUSE §4.3: tool {tool_id!r} not registered — ACT never self-registers")
            return GateVerdict.FAIL, reasons
        required = reg.get("required_authority")
        basis_kind = (receipt.get("authority_basis") or {}).get("kind")
        if required and basis_kind != required:
            reasons.append(
                f"REFUSE §4.3: authority basis {basis_kind!r} does not satisfy "
                f"tool's required_authority {required!r} — no self-escalation")
            return GateVerdict.FAIL, reasons
        if reg.get("authority_class") in (TOOL_CLASS_IRREVERSIBLE, TOOL_CLASS_EXTERNAL_EFFECT):
            if not receipt.get("names_irreversibility"):
                reasons.append(
                    f"REFUSE §3: tool {tool_id} is {reg.get('authority_class')} but the "
                    "receipt does not name the irreversibility explicitly "
                    "(AskHuman Consequential Irreversibility law)")
                return GateVerdict.FAIL, reasons

        # Circuit breaker: an OPEN tool fails fast with a receipt (§7.3).
        if self._breaker_open(tool_id, now):
            reasons.append(f"REFUSE §7.3: circuit breaker OPEN for tool {tool_id} — fail fast with receipt")
            return GateVerdict.FAIL, reasons

        # LAW-envelope path (additive): when the decision receipt carries a
        # LAW-issued envelope, ACT re-validates the grant and the envelope
        # coverage at invocation time — the real clock gates the executor,
        # and a receipt tampered after LAW's verdict cannot broaden it.
        # Receipts without an envelope keep the checks above (fixture/test
        # path, explicitly labelled where used).
        envelope = receipt.get("law_envelope")
        if envelope is not None:
            grant_ref = (receipt.get("authority_basis") or {}).get("ref")
            grant = {g.get("grant_ref"): g for g in (grants or [])}.get(grant_ref)
            if grant is None:
                reasons.append(
                    f"REFUSE §8: authority basis ref {grant_ref!r} resolves "
                    "to no grant — absent grant; LAW never issued this")
                return GateVerdict.FAIL, reasons
            if grant.get("revoked"):
                reasons.append(
                    f"REFUSE §8: grant {grant_ref!r} is revoked — "
                    "revocation binds at invocation time")
                return GateVerdict.FAIL, reasons
            expiry = grant.get("expiry")
            if expiry and now > expiry:
                reasons.append(
                    f"REFUSE §8: grant {grant_ref!r} expired at {expiry} "
                    f"(now {now}) — the real clock gates the executor")
                return GateVerdict.FAIL, reasons
            if envelope.get("scope_tag") not in (grant.get("scope") or []):
                reasons.append(
                    f"REFUSE §8: envelope scope_tag "
                    f"{envelope.get('scope_tag')!r} not in grant scope "
                    f"{grant.get('scope')} — grant does not cover this envelope")
                return GateVerdict.FAIL, reasons
            if tool_id != envelope.get("action"):
                reasons.append(
                    f"REFUSE §7: winner tool {tool_id!r} != envelope action "
                    f"{envelope.get('action')!r} — wrong action")
                return GateVerdict.FAIL, reasons
            if reg.get("target") not in (envelope.get("targets") or []):
                reasons.append(
                    f"REFUSE §7: registry target {reg.get('target')!r} not in "
                    f"envelope targets {envelope.get('targets')} — wrong target")
                return GateVerdict.FAIL, reasons
            bounds = envelope.get("bounds") or {}
            params = winner.get("params") or {}
            pattern = bounds.get("filename")
            filename = params.get("filename", "")
            if pattern and not fnmatch.fnmatch(filename, pattern):
                reasons.append(
                    f"REFUSE §7: filename {filename!r} outside envelope "
                    f"pattern {pattern!r} — broader scope")
                return GateVerdict.FAIL, reasons
            max_bytes = bounds.get("max_bytes")
            content = params.get("content", "")
            size = len(content.encode("utf-8") if isinstance(content, str)
                        else bytes(content))
            if max_bytes is not None and size > max_bytes:
                reasons.append(
                    f"REFUSE §7: content {size} bytes exceeds envelope "
                    f"max_bytes {max_bytes} — broader scope")
                return GateVerdict.FAIL, reasons
            reasons.append(
                f"ENVELOPE-BOUND: grant {grant_ref!r} valid, envelope covers "
                f"{tool_id} within declared bounds")

        reasons.append(f"ADMITTED: ACT path, tool {tool_id}@{reg.get('version')}")
        return GateVerdict.PASS, reasons

    # ------------------------------------------------------------------
    # Path ACT — claim, invoke, observe, receipt (§5, §7)
    # ------------------------------------------------------------------
    def _path_act(self, receipt_in: Dict[str, Any], registry: Dict[str, Any],
                  ledger: Dict[str, Dict[str, Any]], now: str) -> Dict[str, Any]:
        decision_ref = receipt_in.get("receipt_id")
        winner = receipt_in.get("winner") or {}
        tool_id = winner.get("tool_id")
        params = winner.get("params") or {}
        reg = registry[tool_id]

        fingerprint = self._fingerprint(receipt_in, winner)
        key = "act:" + fingerprint

        # §5.2 step 1 — pre-check: a receipt or live claim for this key
        # returns the existing outcome. No re-execution, ever.
        existing = ledger.get(key) or self.ledger.get(key)
        if existing is not None and existing.get("receipt"):
            rec = existing["receipt"]
            self.last_receipt = _deepcopy_json(rec)
            return self._handoff(existing["execution_id"], decision_ref,
                                 rec["path"], rec, None)

        # §5.3 fail-closed on conflicting reuse: same key, different
        # fingerprint = replay/forgery. Refuse, conflict receipt, alert.
        if existing is not None and existing.get("fingerprint") != fingerprint:
            return self._handoff_conflict(decision_ref, ledger, now, key,
                                          existing["fingerprint"], fingerprint)

        # §4.5 conflicting execution in flight: coalesce to the winner's ticket.
        # The loser does not execute — it gets the in-flight ticket view.
        if existing is not None and existing.get("state") in (S_CLAIMED, S_EXECUTING):
            ticket = existing.get("ticket") or {
                "execution_id": existing["execution_id"],
                "key": key,
                "status": existing.get("state"),
                "cancel_handle": f"cancel:{existing['execution_id']}",
            }
            return self._handoff(existing["execution_id"], decision_ref,
                                 existing.get("state"), None, ticket, coalesced=True)

        # §5.2 step 2 — claim (compare-and-set on the key; the claim is the
        # linearization point). A single-process stand-in for atomic CAS:
        # the ledger dict write is the unique-constraint analogue.
        execution_id = f"exec-{fingerprint[:16]}"
        lease_deadline = _add_ms(now, DEFAULT_LEASE_MS)
        claim = {
            "execution_id": execution_id,
            "decision_ref": decision_ref,
            "idempotency_key": key,
            "fingerprint": fingerprint,
            "state": S_CLAIMED,
            "tool": {"tool_id": tool_id, "version": reg.get("version"),
                     "idempotent": bool(reg.get("idempotent"))},
            "params_hash": _params_hash(params),
            "lease_deadline": lease_deadline,
            "heartbeat_at": None,
            "transitions": [{"from": S_AUTHORIZED, "to": S_CLAIMED,
                             "at": now, "reason": "claim won (§5.2)"}],
            "ticket": None,
            "receipt": None,
            "claimed_at": now,
        }
        ledger[key] = claim
        self.ledger[key] = claim

        # §4.7 evidence capture impossible: ACT cannot observe what it cannot
        # invoke observably — no executor, no invocation, no unreceipted act.
        if self._executor is None or not reg.get("evidence_capture"):
            return self._terminate(claim, ledger, now, S_REFUSED,
                                   OUTCOME_REFUSED, None,
                                   "REFUSE §4.7: evidence capture impossible — no executor or "
                                   "no evidence_capture declaration; no receiptable act performed unreceipted")

        self._transition(claim, S_CLAIMED, S_EXECUTING, now, "tool invoked")
        budget = receipt_in.get("execution_budget") or {}
        max_retries = budget.get("max_retries",
                                 (reg.get("retry_policy") or {}).get("attempts", 0))
        attempts = 0
        started = _now_iso()

        while True:
            attempts += 1
            result = self._executor(tool_id, params)
            status = result.get("status")
            error_class = result.get("error_class")
            self.heartbeat(key, ledger, now=_now_iso())

            if status == "ok":
                return self._terminate(claim, ledger, _now_iso(), S_EFFECTS_OBSERVED,
                                       OUTCOME_SUCCESS, None,
                                       effects=str(result.get("effects", "")),
                                       attempts=attempts, started_at=started,
                                       receipt_in=receipt_in, reg=reg,
                                       params_hash=_params_hash(params))

            if status == "harm_signal":
                return self._harm_abort(claim, ledger, receipt_in, reg, params,
                                        attempts, started, result)

            if status in ("error", "timeout"):
                retryable = (error_class == ERROR_TRANSIENT
                             and bool(reg.get("idempotent"))
                             and attempts <= max_retries)
                if retryable:
                    continue  # backoff per registry (simulated by stub executor)
                return self._terminate(claim, ledger, _now_iso(), S_FAILED,
                                       OUTCOME_FAILURE, error_class,
                                       str(result.get("error_detail", "unknown")),
                                       attempts=attempts, started_at=started,
                                       receipt_in=receipt_in, reg=reg,
                                       params_hash=_params_hash(params))

            # Executor misbehaved (unknown status): fail closed, never invent.
            return self._terminate(claim, ledger, _now_iso(), S_FAILED,
                                   OUTCOME_FAILURE, ERROR_PERMANENT,
                                   f"executor returned unknown status {status!r} — fail closed",
                                   attempts=attempts, started_at=started,
                                   receipt_in=receipt_in, reg=reg,
                                   params_hash=_params_hash(params))

    # ------------------------------------------------------------------
    # Paths READ_MORE / ASK (§2.2–2.3)
    # ------------------------------------------------------------------
    def _path_read_more(self, receipt_in: Dict[str, Any],
                        ledger: Dict[str, Dict[str, Any]],
                        now: str) -> Dict[str, Any]:
        decision_ref = receipt_in.get("receipt_id")
        directive = receipt_in.get("read_more_directive") or {}
        receipt = self._execution_receipt(
            execution_id=f"readmore-{_sha256(receipt_in.get('receipt_id') or 'x')[:16]}",
            decision_ref=decision_ref, path=PATH_READ_MORE_LOOP,
            idempotency_key="", fingerprint="", tool=None, params_hash="",
            authority_basis=receipt_in.get("authority_basis"),
            calculus_version=receipt_in.get("calculusVersion"),
            config_hash=receipt_in.get("configHash"),
            outcome=OUTCOME_SUCCESS, error_class=None, attempts=0,
            duration_ms=0, effects_observed="returned to KNOW: " + _canonical(directive),
            issued_by=receipt_in.get("issued_by"),
            transitions=[{"from": S_AUTHORIZED, "to": S_AUTHORIZED,
                           "at": now, "reason": "READ_MORE loop to KNOW (§2.2)"}],
            now=now,
        )
        self.last_receipt = receipt
        return {"execution_id": receipt["execution_id"], "decision_ref": decision_ref,
                "path": PATH_READ_MORE_LOOP, "receipt": receipt, "ticket": None}

    def _path_ask(self, receipt_in: Dict[str, Any],
                  ledger: Dict[str, Dict[str, Any]],
                  now: str) -> Dict[str, Any]:
        decision_ref = receipt_in.get("receipt_id")
        brief = receipt_in.get("decision_brief") or {}
        fingerprint = self._fingerprint(receipt_in, receipt_in.get("winner") or {})
        key = "act:" + fingerprint
        execution_id = f"ask-{fingerprint[:16]}"
        # ASK_SUSPENDED persists the question/options/brief intact (§8.6).
        record = {
            "execution_id": execution_id,
            "decision_ref": decision_ref,
            "idempotency_key": key,
            "fingerprint": fingerprint,
            "state": S_ASK_SUSPENDED,
            "brief": _deepcopy_json(brief),
            "transitions": [{"from": S_AUTHORIZED, "to": S_ASK_SUSPENDED,
                             "at": now, "reason": "ASK suspended for the human (§2.3)"}],
            "receipt": None,
            "suspended_at": now,
        }
        ledger[key] = record
        self.ledger[key] = record
        receipt = self._execution_receipt(
            execution_id=execution_id, decision_ref=decision_ref,
            path=PATH_ASK_SUSPENDED, idempotency_key=key,
            fingerprint=fingerprint, tool=None, params_hash="",
            authority_basis=receipt_in.get("authority_basis"),
            calculus_version=receipt_in.get("calculusVersion"),
            config_hash=receipt_in.get("configHash"),
            outcome=OUTCOME_SUCCESS, error_class=None, attempts=0,
            duration_ms=0, effects_observed="suspended; brief persisted",
            issued_by=receipt_in.get("issued_by"),
            transitions=record["transitions"], now=now,
        )
        self.last_receipt = receipt
        ticket = {"execution_id": execution_id, "key": key,
                  "status": "ASK_SUSPENDED", "cancel_handle": f"cancel:{execution_id}",
                  "deadline": receipt_in.get("valid_until")}
        return {"execution_id": execution_id, "decision_ref": decision_ref,
                "path": PATH_ASK_SUSPENDED, "receipt": receipt, "ticket": ticket}

    # ------------------------------------------------------------------
    # Terminal paths: REFUSE / CONFLICT (§4, §5.3, §2.4)
    # ------------------------------------------------------------------
    def _handoff_refused(self, decision_ref: str,
                         ledger: Dict[str, Dict[str, Any]], now: str,
                         reasons: List[str], refusal_gate: str) -> Dict[str, Any]:
        execution_id = f"refuse-{_sha256(decision_ref + _canonical(reasons))[:16]}"
        receipt = self._execution_receipt(
            execution_id=execution_id, decision_ref=decision_ref,
            path=PATH_REFUSED, idempotency_key="", fingerprint="",
            tool=None, params_hash="", authority_basis=None,
            calculus_version=None, config_hash=None,
            outcome=OUTCOME_REFUSED, error_class=None, attempts=0,
            duration_ms=0, effects_observed="no effects — refused",
            issued_by="NAYA-KERNEL-ACT",
            transitions=[{"from": S_AUTHORIZED, "to": S_REFUSED, "at": now,
                           "reason": f"{refusal_gate}: {'; '.join(reasons)}"}],
            now=now,
            extra={"refusal_reasons": list(reasons)},
        )
        self.last_receipt = receipt
        return {"execution_id": execution_id, "decision_ref": decision_ref,
                "path": PATH_REFUSED, "receipt": receipt, "ticket": None,
                "refusal_gate": refusal_gate}

    def _handoff_awaiting(self, decision_ref: str,
                          ledger: Dict[str, Dict[str, Any]], now: str,
                          reasons: List[str], decision: Optional[str]) -> Dict[str, Any]:
        if decision == "READ_MORE":
            # Loop-bound case surfaces via admission; the plain loop is
            # handled by _path_read_more. Here: forced ASK on bound breach.
            loop = [r for r in reasons if "forcing ASK" in r]
            if loop:
                return self._handoff_forced_ask(decision_ref, ledger, now, reasons)
            return {"execution_id": f"readmore-{_sha256(decision_ref)[:16]}",
                    "decision_ref": decision_ref, "path": PATH_READ_MORE_LOOP,
                    "receipt": None, "ticket": None,
                    "reasons": reasons}
        return {"execution_id": f"ask-{_sha256(decision_ref)[:16]}",
                "decision_ref": decision_ref, "path": PATH_ASK_SUSPENDED,
                "receipt": None, "ticket": None, "reasons": reasons}

    def _handoff_forced_ask(self, decision_ref: str,
                            ledger: Dict[str, Dict[str, Any]], now: str,
                            reasons: List[str]) -> Dict[str, Any]:
        receipt = self._execution_receipt(
            execution_id=f"forced-ask-{_sha256(decision_ref)[:16]}",
            decision_ref=decision_ref, path=PATH_ASK_SUSPENDED,
            idempotency_key="", fingerprint="", tool=None, params_hash="",
            authority_basis=None, calculus_version=None, config_hash=None,
            outcome=OUTCOME_SUCCESS, error_class=None, attempts=0,
            duration_ms=0, effects_observed="READ_MORE bound exceeded — forced ASK",
            issued_by="NAYA-KERNEL-ACT",
            transitions=[{"from": S_AUTHORIZED, "to": S_ASK_SUSPENDED, "at": now,
                           "reason": "; ".join(reasons)}], now=now)
        self.last_receipt = receipt
        return {"execution_id": receipt["execution_id"], "decision_ref": decision_ref,
                "path": PATH_ASK_SUSPENDED, "receipt": receipt,
                "ticket": {"status": "ASK_SUSPENDED_FORCED",
                           "cancel_handle": f"cancel:{receipt['execution_id']}"}}

    def _handoff_conflict(self, decision_ref: str,
                          ledger: Dict[str, Dict[str, Any]], now: str,
                          key: str, stored_fp: str, incoming_fp: str) -> Dict[str, Any]:
        execution_id = f"conflict-{_sha256(key + incoming_fp)[:16]}"
        receipt = self._execution_receipt(
            execution_id=execution_id, decision_ref=decision_ref,
            path=PATH_REFUSED, idempotency_key=key,
            fingerprint=incoming_fp, tool=None, params_hash="",
            authority_basis=None, calculus_version=None, config_hash=None,
            outcome=OUTCOME_CONFLICT, error_class=None, attempts=0,
            duration_ms=0, effects_observed="conflicting reuse — fail closed",
            issued_by="NAYA-KERNEL-ACT",
            transitions=[{"from": S_AUTHORIZED, "to": S_REFUSED, "at": now,
                           "reason": f"§5.3 fingerprint conflict on key {key}"}],
            now=now,
            extra={"conflict": {"key": key, "stored_fingerprint": stored_fp,
                                "incoming_fingerprint": incoming_fp,
                                "alert": "RAISED — ambiguity about what was authorized is itself a refusal reason"}},
        )
        self.last_receipt = receipt
        return {"execution_id": execution_id, "decision_ref": decision_ref,
                "path": PATH_REFUSED, "receipt": receipt, "ticket": None,
                "refusal_gate": "fingerprint_conflict"}

    def _handoff(self, execution_id: str, decision_ref: str, path: str,
                 receipt: Optional[Dict[str, Any]],
                 ticket: Optional[Dict[str, Any]],
                 coalesced: bool = False) -> Dict[str, Any]:
        return {"execution_id": execution_id, "decision_ref": decision_ref,
                "path": path, "receipt": receipt, "ticket": ticket,
                "coalesced": coalesced}

    # ------------------------------------------------------------------
    # Execution internals
    # ------------------------------------------------------------------
    def _terminate(self, claim: Dict[str, Any], ledger: Dict[str, Dict[str, Any]],
                   now: str, final_state: str, outcome: str,
                   error_class: Optional[str], detail: str = "",
                   attempts: int = 1, started_at: Optional[str] = None,
                   effects: str = "",
                   receipt_in: Optional[Dict[str, Any]] = None,
                   reg: Optional[Dict[str, Any]] = None,
                   params_hash: str = "") -> Dict[str, Any]:
        if final_state == S_EFFECTS_OBSERVED:
            self._transition(claim, S_EXECUTING, S_EFFECTS_OBSERVED, now,
                             "effects observed")
            self._transition(claim, S_EFFECTS_OBSERVED, S_RECEIPTED, now,
                             "receipt emitted")
            terminal_path = PATH_EXECUTED
        else:
            # From-state is whatever the claim holds: EXECUTING for
            # mid-execution failures, CLAIMED for refuse-before-invocation
            # (§4.7 — the CLAIMED -> REFUSED edge is legal per §7.2).
            frm = claim.get("state") or S_AUTHORIZED
            self._transition(claim, frm, final_state, now, detail[:200])
            terminal_path = {
                S_FAILED: PATH_FAILED, S_TIMED_OUT: PATH_TIMED_OUT,
                S_CANCELLED: PATH_CANCELLED, S_REFUSED: PATH_REFUSED,
            }[final_state]
        duration_ms = _duration_ms(started_at or claim.get("claimed_at") or now, now)
        extra: Optional[Dict[str, Any]] = None
        if final_state == S_REFUSED:
            extra = {"refusal_reasons": [detail]}
        receipt = self._execution_receipt(
            execution_id=claim["execution_id"], decision_ref=claim["decision_ref"],
            path=terminal_path, idempotency_key=claim["idempotency_key"],
            fingerprint=claim["fingerprint"],
            tool=claim.get("tool"), params_hash=params_hash,
            authority_basis=(receipt_in or {}).get("authority_basis"),
            calculus_version=(receipt_in or {}).get("calculusVersion"),
            config_hash=(receipt_in or {}).get("configHash"),
            outcome=outcome, error_class=error_class, attempts=attempts,
            duration_ms=duration_ms,
            effects_observed=(effects if effects
                              else ("no effects — refused" if final_state == S_REFUSED
                                    else detail)),
            issued_by=(receipt_in or {}).get("issued_by", "NAYA-KERNEL-ACT"),
            transitions=claim["transitions"], now=now, extra=extra)
        claim["receipt"] = receipt
        claim["state"] = S_RECEIPTED if final_state == S_EFFECTS_OBSERVED else final_state
        ledger[claim["idempotency_key"]] = claim
        self.ledger[claim["idempotency_key"]] = claim
        self.last_receipt = receipt
        self._record_breaker(claim["tool"]["tool_id"], outcome, now)
        return {"execution_id": claim["execution_id"],
                "decision_ref": claim["decision_ref"], "path": terminal_path,
                "receipt": receipt, "ticket": None}

    def _harm_abort(self, claim: Dict[str, Any], ledger: Dict[str, Dict[str, Any]],
                    receipt_in: Dict[str, Any], reg: Dict[str, Any],
                    params: Dict[str, Any], attempts: int, started: str,
                    result: Dict[str, Any]) -> Dict[str, Any]:
        now = _now_iso()
        compensation = None
        compensating_tool = reg.get("compensating_tool")
        if compensating_tool and self._executor is not None:
            try:
                comp = self._executor(compensating_tool, params)
                compensation = {"tool": compensating_tool,
                                "effects": str(comp.get("effects", "")),
                                "status": comp.get("status")}
            except Exception as exc:  # never let compensation crash the abort
                compensation = {"tool": compensating_tool, "status": "error",
                                "error_detail": str(exc)}
        out = self._terminate(claim, ledger, now, S_FAILED, OUTCOME_FAILURE,
                              ERROR_HARM_SIGNAL,
                              "HARM_SIGNAL §7.3: the world says stop — abort immediately",
                              attempts=attempts, started_at=started,
                              effects=str(result.get("effects", "")),
                              receipt_in=receipt_in, reg=reg,
                              params_hash=_params_hash(params))
        out["receipt"]["compensation"] = compensation
        out["receipt"]["alert"] = "RAISED — harm signal during execution"
        # Re-seal: the post-hoc fields must be covered by the receipt hash.
        out["receipt"]["receipt_hash"] = _sha256(
            {k: v for k, v in out["receipt"].items() if k != "receipt_hash"})
        self.last_receipt = out["receipt"]
        return out

    def _transition(self, claim: Dict[str, Any], frm: str, to: str,
                    now: str, reason: str) -> None:
        current = claim.get("state")
        if current != frm:
            raise RuntimeError(
                f"ACT illegal transition: claim is {current!r}, expected {frm!r}")
        if to not in LEGAL_TRANSITIONS.get(frm, frozenset()):
            raise RuntimeError(
                f"ACT illegal transition: {frm} -> {to} (fail closed)")
        claim["state"] = to
        claim.setdefault("transitions", []).append(
            {"from": frm, "to": to, "at": now, "reason": reason})

    def heartbeat(self, key: str, ledger: Dict[str, Dict[str, Any]],
                  now: Optional[str] = None) -> bool:
        """Renew the claim lease (§5.4). Returns False if no live claim."""
        rec = ledger.get(key) or self.ledger.get(key)
        if rec is None or rec.get("state") not in (S_CLAIMED, S_EXECUTING):
            return False
        ts = now or _now_iso()
        rec["heartbeat_at"] = ts
        rec["lease_deadline"] = _add_ms(ts, DEFAULT_LEASE_MS)
        return True

    # ------------------------------------------------------------------
    # Circuit breaker (§7.3)
    # ------------------------------------------------------------------
    def _breaker_open(self, tool_id: str, now: str) -> bool:
        b = self._breakers.get(tool_id)
        if b is None:
            return False
        if b.get("state") == "OPEN":
            if _add_ms(b["opened_at"], CIRCUIT_COOLDOWN_MS) > now:
                return True
            b["state"] = "HALF_OPEN"  # cooldown elapsed: probe once
            return False
        return False

    def _record_breaker(self, tool_id: str, outcome: str, now: str) -> None:
        b = self._breakers.setdefault(
            tool_id, {"consecutive_failures": 0, "state": "CLOSED",
                      "opened_at": None})
        if outcome == OUTCOME_SUCCESS:
            b["consecutive_failures"] = 0
            if b.get("state") == "HALF_OPEN":
                b["state"] = "CLOSED"  # probe succeeded — re-close
            return
        if outcome in (OUTCOME_FAILURE, OUTCOME_TIMEOUT):
            b["consecutive_failures"] += 1
            if (b["consecutive_failures"] >= CIRCUIT_TRIP_THRESHOLD
                    and b.get("state") != "OPEN"):
                b["state"] = "OPEN"
                b["opened_at"] = now

    # ------------------------------------------------------------------
    # Idempotency key / fingerprint (§5.1)
    # ------------------------------------------------------------------
    def _fingerprint(self, receipt_in: Dict[str, Any],
                     winner: Dict[str, Any]) -> str:
        material = {
            "decision_receipt_id": receipt_in.get("receipt_id"),
            "action_spec": winner.get("tool_id"),
            "params_hash": _params_hash(winner.get("params") or {}),
            "authority_basis": _canonical(receipt_in.get("authority_basis") or {}),
            "configHash": receipt_in.get("configHash"),
            "issuedBy": receipt_in.get("issued_by"),
        }
        return _sha256(material)

    # ------------------------------------------------------------------
    # Receipt (§6) + recompute (§4.1 cold check)
    # ------------------------------------------------------------------
    def _execution_receipt(self, execution_id: str, decision_ref: str,
                           path: str, idempotency_key: str, fingerprint: str,
                           tool: Optional[Dict[str, Any]], params_hash: str,
                           authority_basis: Optional[Dict[str, Any]],
                           calculus_version: Optional[str],
                           config_hash: Optional[str], outcome: str,
                           error_class: Optional[str], attempts: int,
                           duration_ms: int, effects_observed: str,
                           issued_by: Optional[str],
                           transitions: List[Dict[str, Any]],
                           now: str,
                           extra: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        receipt = {
            "node_id": NODE_ID,
            "node_version": NODE_VERSION,
            "status": "CANDIDATE — NOT RATIFIED — NOT MERGED",
            "ledger": "smartledger",
            "stream": "execution",
            "execution_id": execution_id,
            "decision_ref": decision_ref,
            "path": path,
            "idempotency_key": idempotency_key,
            "fingerprint": fingerprint,
            "tool": _deepcopy_json(tool) if tool else None,
            "params_hash": params_hash,
            "authority_basis": _deepcopy_json(authority_basis)
            if authority_basis else None,
            "calculusVersion": calculus_version,
            "configHash": config_hash,
            "state_transitions": _deepcopy_json(transitions),
            "effects_observed": effects_observed,
            "outcome": outcome,
            "error_class": error_class,
            "attempts": attempts,
            "duration_ms": duration_ms,
            "compensation": None,
            "issued_at": now,
            "issued_by": issued_by or "NAYA-KERNEL-ACT",
        }
        if extra:
            receipt.update(_deepcopy_json(extra))
        receipt["receipt_hash"] = _sha256(
            {k: v for k, v in receipt.items() if k != "receipt_hash"})
        return receipt

    def _recompute_ok(self, receipt: Dict[str, Any]) -> bool:
        """§4.1: the receipt must recompute under the bound configHash.

        For ACT-generated ExecutionReceipts the receipt_hash is recomputed
        over the canonical body. For LAW DecisionReceipts arriving from the
        pipeline, ACT checks the receipt_hash if present; if the receipt
        carries no hash it is unverifiable and refused (fail closed).
        """
        claimed = receipt.get("receipt_hash")
        if not claimed:
            return False
        body = {k: v for k, v in receipt.items() if k != "receipt_hash"}
        return _sha256(body) == claimed

    def recompute(self, receipt: Dict[str, Any]) -> str:
        """Cold check: MATCH when the receipt recomputes, else MISMATCH.

        Spec §8 — deterministic cold-reconstruction plan."""
        return "MATCH" if self._recompute_ok(receipt) else "MISMATCH"


def _add_ms(iso: str, ms: int) -> str:
    dt = datetime.fromisoformat(iso)
    return (dt + timedelta(milliseconds=ms)).isoformat()


def _duration_ms(start_iso: str, end_iso: str) -> int:
    try:
        return int((datetime.fromisoformat(end_iso)
                    - datetime.fromisoformat(start_iso)).total_seconds() * 1000)
    except Exception:
        return 0


def make_decision_receipt(**overrides: Any) -> Dict[str, Any]:
    """Test helper: build a valid, recomputable ACT-verb decision receipt.

    The receipt_hash is computed over the body so it passes _recompute_ok.
    """
    body = {
        "receipt_id": "dec-test-001",
        "decision": "ACT",
        "winner": {"tool_id": "echo_tool", "version": "1.0.0",
                   "params": {"text": "hello"}},
        "authority_basis": {"kind": "director_order", "ref": "order-1",
                            "revoked": False},
        "calculusVersion": "v2.1-candidate",
        "configHash": "cfg-aaa",
        "configHashCurrent": "cfg-aaa",
        "reversibility": 1.0,
        "stakes": "low",
        "issued_at": "2026-09-30T18:00:00+00:00",
        "valid_until": "2026-10-02T00:00:00+00:00",
        "issued_by": "NAYA-KERNEL-LAW",
        "execution_budget": {"timeout_ms": 5000, "max_retries": 2,
                             "read_more_loop": 0},
        "flags": {},
        "names_irreversibility": False,
    }
    body.update(overrides)
    body["receipt_hash"] = _sha256(body)
    return body


def make_tool_registry(**overrides: Any) -> Dict[str, Any]:
    """Test helper: a registry with one READ idempotent tool."""
    reg = {
        "echo_tool": {
            "version": "1.0.0",
            "authority_class": TOOL_CLASS_READ,
            "idempotent": True,
            "max_timeout_ms": 5000,
            "retry_policy": {"attempts": 2, "backoff": "linear"},
            "required_authority": "director_order",
            "compensating_tool": None,
            "evidence_capture": "return_value",
        }
    }
    reg.update(overrides)
    return reg
