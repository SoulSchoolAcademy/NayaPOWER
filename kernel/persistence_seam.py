"""Persistence seam adapter: kernel decision receipts -> governed ledger.

Maps a ``naya_kernel`` decision receipt onto the parameters of the existing
``public.nayanet_record_ledger_event`` SECURITY DEFINER function, under the
canonical ``NAYANODE/0101-PERSISTENCE-CONTRACT-V1.md`` (12 fields).

Design rules (see docs/PERSISTENCE-SEAM-SPEC-V1.md):
- Pure functions. No I/O, no secrets, stdlib only. The caller performs the
  database call; this module only builds and validates the parameters.
- The kernel's native receipt is never modified. The seam validates the
  kernel's own ``receipt_hash`` (canonicalization reimplemented from
  ``naya_kernel/kernel.py`` at the pinned kernel SHA; injectable for tests).
- The seam assigns ``owner_id`` from the authenticated context. It never
  invents ``executed_at`` / ``observed_at``. Inserts always land as
  ``verification.state = UNVERIFIED``; verification is a later, evidenced
  transition, never a claim at insert time.
"""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional

ADAPTER_VERSION = "persistence-seam-v3"
CONTRACT_REF = "NAYANODE/0101-PERSISTENCE-CONTRACT-V1.md"
SCHEMA_VERSION = "1.0.0"  # matches the ledger function's hardcoded schema_version

SOURCE_TABLE = "naya_kernel_decision"
EVENT_TYPE = "DECISION"

# Canonical verdict vocabulary: naya_kernel/node_base.py::GateVerdict.
# The adapter enforces the producer's own vocabulary; it invents none.
_VERDICTS = ("PASS", "FAIL", "NEED_EVIDENCE")

_OWNER_SCOPES = ("PRIVATE", "SHARED", "COLLECTIVE", "PUBLIC")
_UUID_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.I
)
_HEX64_RE = re.compile(r"^[0-9a-f]{64}$")
_HEX40_RE = re.compile(r"^[0-9a-f]{40}$")


def _parse_timestamp(value: Any) -> bool:
    """True iff value is an ISO-8601 timestamp with a time and a timezone.

    The producer (kernel) emits tz-aware datetimes; the ledger stores
    timestamptz. Date-only values ("2026-10-01") and naive datetimes are
    REJECTED — they do not satisfy the producer's timestamp contract.
    """
    if not isinstance(value, str) or not value.strip():
        return False
    text = value.strip().replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(text)
    except ValueError:
        return False
    if not isinstance(dt, datetime):
        return False
    # fromisoformat("2026-10-01") yields midnight — require an explicit time
    # component in the original text (T or space separator, HH:MM).
    if not re.search(r"[T ]\d{2}:\d{2}", text):
        return False
    return dt.tzinfo is not None


# ---------------------------------------------------------------------------
# Kernel receipt verification (canonicalization mirrors naya_kernel/kernel.py)
# ---------------------------------------------------------------------------

def _canon(obj: Any) -> str:
    """Canonical JSON: sort_keys, compact separators, ensure_ascii, default=str."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, default=str)


def _sha256(obj: Any) -> str:
    return hashlib.sha256(_canon(obj).encode("utf-8")).hexdigest()


def _detached_snapshot(obj: Any, *, what: str) -> Any:
    """Detached JSON-domain snapshot of ``obj``.

    The snapshot is a deep copy through strict canonical JSON: the caller
    can mutate the original afterwards without affecting already-validated
    projected evidence, and mutation of the projection cannot reach back
    into the caller's objects.

    Strictness: ``allow_nan=False`` and no ``default=str`` coercion — values
    that are not JSON-native (sets, bytes, NaN/Infinity, arbitrary objects)
    are REJECTED as boundary violations, not silently stringified. The
    canonical hashing rules (``_canon``/``_sha256``) are unchanged; this only
    governs what may enter the projected snapshot.
    """
    try:
        text = json.dumps(obj, sort_keys=True, separators=(",", ":"),
                          ensure_ascii=True, allow_nan=False)
    except (TypeError, ValueError) as e:
        raise ValueError(f"{what} is not strict JSON-native: {e}")
    return json.loads(text)


def verify_kernel_receipt(receipt: Dict[str, Any]) -> Dict[str, Any]:
    """Re-derive receipt_hash over the canonical body; return MATCH/MISMATCH.

    Mirrors ``naya_kernel.kernel.verify_decision_receipt``. A MISMATCH means
    the receipt was tampered with after issuance or was not produced by the
    kernel's canonicalization — the seam must refuse it.
    """
    if not isinstance(receipt, dict):
        return {"result": "MISMATCH", "receipt_id": None}
    stored = receipt.get("receipt_hash")
    body = {k: v for k, v in receipt.items() if k != "receipt_hash"}
    if not isinstance(stored, str) or _sha256(body) != stored:
        return {"result": "MISMATCH", "receipt_id": receipt.get("receipt_id")}
    return {"result": "MATCH", "receipt_id": receipt.get("receipt_id")}


# ---------------------------------------------------------------------------
# Projection: kernel receipt -> nayanet_record_ledger_event parameters
# ---------------------------------------------------------------------------

def project_kernel_receipt(
    receipt: Dict[str, Any],
    *,
    owner_id: str,
    kernel_sha: str,
    owner_scope: str = "PRIVATE",
    config_hash: Optional[str] = None,
    parent_ledger_event_id: Optional[str] = None,
    inputs_state: Optional[Dict[str, Any]] = None,
    verify: Callable[[Dict[str, Any]], Dict[str, Any]] = verify_kernel_receipt,
) -> Dict[str, Any]:
    """Build the ``nayanet_record_ledger_event`` parameters for a kernel receipt.

    Raises ``ValueError`` on any boundary violation (the caller must not
    swallow these into a silent default). Field responsibilities:
    - kernel: receipt content, ``receipt_hash``, ``issued_at``, ``decision_id``,
      ``node_id``, ``kernel_version``, ``inputs_hash`` (the kernel produces it;
      the adapter recomputes it over ``inputs_state`` and rejects mismatch).
    - seam (this function): ``owner_id`` (from auth context arg), ``owner_scope``,
      provenance envelope, verification ``UNVERIFIED``, idempotency identity.
    - database: ``object_id`` (ledger_event_id), ``created_at``, ``event_hash``,
      ``schema_version='1.0.0'``.

    Snapshot semantics (RED-2): the receipt and ``inputs_state`` are detached
    into JSON-domain snapshots BEFORE validation. Validation and hashing run
    on the snapshots — the exact objects that will be serialized — so caller
    mutation after projection cannot invalidate already-validated evidence.
    """
    # 1. Detach first: validate and hash the snapshots, not the caller's
    #    live objects.
    try:
        receipt = _detached_snapshot(receipt, what="receipt")
    except ValueError as e:
        raise ValueError(f"seam boundary violations: {e}")
    if inputs_state is not None:
        try:
            inputs_state = _detached_snapshot(inputs_state, what="inputs_state")
        except ValueError as e:
            raise ValueError(f"seam boundary violations: {e}")
    # 2. Validate the snapshots (same objects that will be serialized).
    violations = _validate_inputs(receipt, owner_id, kernel_sha, owner_scope,
                                  config_hash, parent_ledger_event_id,
                                  inputs_state, verify)
    if violations:
        raise ValueError("seam boundary violations: " + "; ".join(violations))

    decision_id = receipt["decision_id"]
    # Input-commitment qualification: a receipt WITHOUT inputs_hash is a
    # legacy receipt — it must never carry the recomputation qualification.
    inputs_hash = receipt.get("inputs_hash")
    input_commitment = ("recomputed-match" if isinstance(inputs_hash, str)
                        and _HEX64_RE.match(inputs_hash) else "absent-legacy")
    provenance = {
        "node_id": receipt.get("node_id"),
        "kernel_version": receipt.get("kernel_version"),
        "kernel_sha": kernel_sha,
        "config_hash": config_hash,
        "received_at": datetime.now(timezone.utc).isoformat(),
        "adapter_version": ADAPTER_VERSION,
        "contract_ref": CONTRACT_REF,
        "input_commitment": input_commitment,
    }
    # Strip None provenance entries the kernel did not supply; keep the seam's.
    provenance = {k: v for k, v in provenance.items()
                  if v is not None or k in ("received_at", "adapter_version", "contract_ref")}
    # Cold-recomputation closure: the exact evaluated input state is preserved
    # verbatim (like the receipt) so a fresh consumer retrieving this row can
    # independently recompute inputs_hash. Without it, only the write-time
    # "recomputed-match" commitment would survive — the consumer could not
    # re-verify. States are small decision inputs; privacy posture is unchanged
    # (row is already PRIVATE to the owner, receipt already stored verbatim).
    if inputs_state is not None:
        # Already a detached snapshot (see step 1); the caller's live object
        # cannot alias the projected evidence.
        provenance["inputs_state"] = inputs_state

    return {
        "p_owner_id": owner_id,
        "p_event_type": EVENT_TYPE,
        "p_source_table": SOURCE_TABLE,
        "p_source_id": str(decision_id),
        # event_at is the kernel's own issued_at — received, never invented.
        "p_event_at": receipt["issued_at"],
        "p_actor_id": owner_id,
        "p_privacy_classification": owner_scope,
        "p_status": "RECORDED",
        "p_evidence_refs": [],
        "p_verification": {"state": "UNVERIFIED", "verified_by": None,
                           "verified_at": None},
        # Execution evidence: the kernel receipt, verbatim. Already a detached
        # snapshot (see step 1) — no shallow copy, no aliasing.
        "p_value": receipt,
        # No observed outcome at insert time. Ever.
        "p_outcome": {},
        "p_learning_refs": [],
        "p_metadata": provenance,
        "p_parent_ledger_event_id": parent_ledger_event_id,
    }


def idempotency_key(owner_id: str, source_id: str) -> str:
    """The identity the database uses for duplicate-write idempotency."""
    return f"{owner_id}|{SOURCE_TABLE}|{source_id}"


def _validate_inputs(receipt, owner_id, kernel_sha, owner_scope, config_hash,
                     parent_ledger_event_id, inputs_state, verify) -> List[str]:
    v: List[str] = []
    if not isinstance(receipt, dict):
        return ["receipt must be a JSON object"]
    # 2. required receipt metadata: presence, type, and vocabulary.
    for f in ("receipt_id", "decision_id", "kernel_version"):
        val = receipt.get(f)
        if not isinstance(val, str) or not val.strip():
            v.append(f"receipt field {f} must be a non-empty string")
    verdict = receipt.get("verdict")
    if verdict not in _VERDICTS:
        v.append(f"verdict must be one of {_VERDICTS} (canonical GateVerdict)")
    if not _parse_timestamp(receipt.get("issued_at")):
        v.append("issued_at must be a parseable ISO-8601 timestamp")
    # 3. seal validation: the seal is ALWAYS checked. Missing, null,
    #    non-string, or malformed receipt_hash is rejected — a hash the
    #    verifier never sees is not a verified hash.
    stored = receipt.get("receipt_hash")
    if not isinstance(stored, str):
        v.append("receipt_hash must be a string (missing/null/numeric rejected)")
    elif not _HEX64_RE.match(stored):
        v.append("receipt_hash must be 64-char lowercase hex")
    else:
        r = verify(receipt)
        if r.get("result") != "MATCH":
            v.append("receipt_hash MISMATCH — receipt failed independent recomputation")
    # 4. inputs_hash: the kernel produces it; the adapter recomputes it over
    # the submitted state and rejects mismatch. Neither side invents it.
    claimed_inputs_hash = receipt.get("inputs_hash")
    if claimed_inputs_hash is not None:
        if not isinstance(claimed_inputs_hash, str) or \
                not _HEX64_RE.match(claimed_inputs_hash):
            v.append("inputs_hash must be 64-char lowercase hex when present")
        elif inputs_state is None:
            v.append("inputs_hash present but no inputs_state submitted for recomputation")
        elif _sha256(inputs_state) != claimed_inputs_hash:
            v.append("inputs_hash MISMATCH — submitted state does not reproduce the kernel's hash")
    # 5. source/configuration: shape-checked labels, NOT provenance.
    # A 40-hex kernel_sha proves nothing about which revision produced the
    # receipt; config_hash is a caller-supplied claim. Both are preserved
    # as claims in provenance, never as established facts.
    if not isinstance(kernel_sha, str) or not _HEX40_RE.match(kernel_sha):
        v.append("kernel_sha must be a 40-char lowercase hex SHA")
    if config_hash is not None and \
            (not isinstance(config_hash, str) or not config_hash.strip()):
        v.append("config_hash must be a non-empty string when supplied")
    # 6. ownership / scope: uuid shape only. Shape is not isolation —
    # isolation is enforced by the database (LEDGER_OWNER_MISMATCH, RLS).
    if not isinstance(owner_id, str) or not _UUID_RE.match(owner_id):
        v.append("owner_id must be a uuid (auth identity)")
    if owner_scope not in _OWNER_SCOPES:
        v.append(f"owner_scope must be one of {_OWNER_SCOPES}")
    # 8. successor authority shape (shape only — not lineage authorization).
    if parent_ledger_event_id is not None and \
            not _UUID_RE.match(str(parent_ledger_event_id)):
        v.append("parent_ledger_event_id must be a uuid or null")
    return v


# ---------------------------------------------------------------------------
# Contract-record validation (the 12 fields, for readers/replays)
# ---------------------------------------------------------------------------

CONTRACT_FIELDS = (
    "object_id", "owner_id", "owner_scope", "created_at", "updated_at",
    "schema_version", "provenance", "truth_state", "status",
    "superseded_by", "lineage", "content_hash",
)


# Canonical vocabularies for contract-record validation. These come from the
# migrations, not from the adapter:
# - status: the V1 ledger check constraint
#   (20260919015207_smart_ledger_foundation_v1.sql).
# - truth_state: the V2.1 assessment_state vocabulary
#   (20261001032000_decision_value_smart_ledger_v2_1.sql) — the ledger's
#   native truth/assessment states, which the 12-field reconstruction maps
#   to the contract's truth_state.
_STATUS_VOCAB = ("RECORDED", "VERIFIED", "QUALIFIED", "SUPERSEDED",
                 "BLOCKED", "FAILED")
_TRUTH_VOCAB = ("UNASSESSED", "ASSESSED", "VERIFIED_VALUE", "REJECTED")
_SCHEMA_VERSION_RE = re.compile(r"^\d+\.\d+\.\d+$")


def validate_contract_record(record: Dict[str, Any]) -> List[str]:
    """Validate a 12-field contract record. Returns violations (empty = valid).

    Every field's meaning is checked against the canonical contracts:
    timestamp types and timezone semantics, schema-version shape, the
    status and truth-state vocabularies, supersession identity, lineage
    shape, provenance requirements, and content-hash shape.

    Explicit limitation: a shape-valid ``content_hash`` is NOT evidence the
    content recomputes — recomputation needs the source row and is proven
    by the write→fresh-read path, not by this validator.
    """
    v: List[str] = []
    if not isinstance(record, dict):
        return ["record must be a JSON object"]
    for f in CONTRACT_FIELDS:
        if f not in record:
            v.append(f"missing contract field: {f}")
    if v:
        return v
    for f in ("object_id", "owner_id"):
        if not isinstance(record[f], str) or not _UUID_RE.match(record[f]):
            v.append(f"{f} must be a uuid")
    if record["owner_scope"] not in _OWNER_SCOPES:
        v.append("owner_scope must be PRIVATE/SHARED/COLLECTIVE/PUBLIC")
    for f in ("created_at", "updated_at"):
        if not _parse_timestamp(record.get(f)):
            v.append(f"{f} must be a tz-aware ISO-8601 timestamp with time "
                     f"(date-only and naive values rejected)")
    sv = record.get("schema_version")
    if not isinstance(sv, str) or not _SCHEMA_VERSION_RE.match(sv):
        v.append("schema_version must be a semver string (e.g. '1.0.0')")
    prov = record.get("provenance")
    if not isinstance(prov, dict):
        v.append("provenance must be an object")
    else:
        for pf in ("source_table", "source_id"):
            if not isinstance(prov.get(pf), str) or not prov[pf].strip():
                v.append(f"provenance.{pf} must be a non-empty string")
    if record.get("truth_state") not in _TRUTH_VOCAB:
        v.append(f"truth_state must be one of {list(_TRUTH_VOCAB)} "
                f"(V2.1 assessment vocabulary)")
    if record.get("status") not in _STATUS_VOCAB:
        v.append(f"status must be one of {list(_STATUS_VOCAB)} "
                f"(V1 ledger check constraint)")
    sup = record.get("superseded_by")
    if sup is not None and (not isinstance(sup, str) or not _UUID_RE.match(sup)):
        v.append("superseded_by must be null or a uuid")
    lin = record.get("lineage")
    if not isinstance(lin, dict):
        v.append("lineage must be an object")
    else:
        par = lin.get("parent_ledger_event_id")
        if par is not None and (not isinstance(par, str) or not _UUID_RE.match(par)):
            v.append("lineage.parent_ledger_event_id must be null or a uuid")
        seq = lin.get("chain_seq")
        if seq is not None and not isinstance(seq, int):
            v.append("lineage.chain_seq must be null or an integer")
        pch = lin.get("previous_chain_hash")
        if pch is not None and (not isinstance(pch, str)
                                or not re.fullmatch(r"[0-9a-f]{64}", pch)):
            v.append("lineage.previous_chain_hash must be null or 64-char hex")
    ch = record.get("content_hash")
    if not isinstance(ch, str) or not re.fullmatch(r"[0-9a-f]{64}", ch):
        v.append("content_hash must be 64-char lowercase hex")
    return v
