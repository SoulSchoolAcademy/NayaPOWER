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

ADAPTER_VERSION = "persistence-seam-v1"
CONTRACT_REF = "NAYANODE/0101-PERSISTENCE-CONTRACT-V1.md"
SCHEMA_VERSION = "1.0.0"  # matches the ledger function's hardcoded schema_version

SOURCE_TABLE = "naya_kernel_decision"
EVENT_TYPE = "DECISION"

_OWNER_SCOPES = ("PRIVATE", "SHARED", "COLLECTIVE", "PUBLIC")
_UUID_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.I
)


# ---------------------------------------------------------------------------
# Kernel receipt verification (canonicalization mirrors naya_kernel/kernel.py)
# ---------------------------------------------------------------------------

def _canon(obj: Any) -> str:
    """Canonical JSON: sort_keys, compact separators, ensure_ascii, default=str."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, default=str)


def _sha256(obj: Any) -> str:
    return hashlib.sha256(_canon(obj).encode("utf-8")).hexdigest()


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
    """
    violations = _validate_inputs(receipt, owner_id, kernel_sha, owner_scope,
                                  parent_ledger_event_id, inputs_state, verify)
    if violations:
        raise ValueError("seam boundary violations: " + "; ".join(violations))

    decision_id = receipt["decision_id"]
    provenance = {
        "node_id": receipt.get("node_id"),
        "kernel_version": receipt.get("kernel_version"),
        "kernel_sha": kernel_sha,
        "config_hash": config_hash,
        "received_at": datetime.now(timezone.utc).isoformat(),
        "adapter_version": ADAPTER_VERSION,
        "contract_ref": CONTRACT_REF,
    }
    # Strip None provenance entries the kernel did not supply; keep the seam's.
    provenance = {k: v for k, v in provenance.items()
                  if v is not None or k in ("received_at", "adapter_version", "contract_ref")}

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
        # Execution evidence: the kernel receipt, verbatim.
        "p_value": dict(receipt),
        # No observed outcome at insert time. Ever.
        "p_outcome": {},
        "p_learning_refs": [],
        "p_metadata": provenance,
        "p_parent_ledger_event_id": parent_ledger_event_id,
    }


def idempotency_key(owner_id: str, source_id: str) -> str:
    """The identity the database uses for duplicate-write idempotency."""
    return f"{owner_id}|{SOURCE_TABLE}|{source_id}"


def _validate_inputs(receipt, owner_id, kernel_sha, owner_scope,
                     parent_ledger_event_id, inputs_state, verify) -> List[str]:
    v: List[str] = []
    if not isinstance(receipt, dict):
        return ["receipt must be a JSON object"]
    # 2. missing required metadata
    for f in ("receipt_hash", "receipt_id", "decision_id", "issued_at",
              "kernel_version", "verdict"):
        if receipt.get(f) in (None, ""):
            v.append(f"receipt missing required field: {f}")
    # 4. hash mismatch (tamper / non-kernel canonicalization)
    if isinstance(receipt.get("receipt_hash"), str):
        r = verify(receipt)
        if r.get("result") != "MATCH":
            v.append("receipt_hash MISMATCH — receipt failed independent recomputation")
    # 4b. inputs_hash: the kernel produces it; the adapter recomputes it over
    # the submitted state and rejects mismatch. Neither side invents it.
    claimed_inputs_hash = receipt.get("inputs_hash")
    if claimed_inputs_hash is not None:
        if not isinstance(claimed_inputs_hash, str) or \
                not re.fullmatch(r"[0-9a-f]{64}", claimed_inputs_hash):
            v.append("inputs_hash must be 64-char lowercase hex when present")
        elif inputs_state is None:
            v.append("inputs_hash present but no inputs_state submitted for recomputation")
        elif _sha256(inputs_state) != claimed_inputs_hash:
            v.append("inputs_hash MISMATCH — submitted state does not reproduce the kernel's hash")
    # 5. source/configuration mismatch
    if not isinstance(kernel_sha, str) or len(kernel_sha) != 40 or \
            not re.fullmatch(r"[0-9a-f]{40}", kernel_sha):
        v.append("kernel_sha must be a 40-char lowercase hex SHA")
    # 6. wrong ownership / scope
    if not isinstance(owner_id, str) or not _UUID_RE.match(owner_id):
        v.append("owner_id must be a uuid (auth identity)")
    if owner_scope not in _OWNER_SCOPES:
        v.append(f"owner_scope must be one of {_OWNER_SCOPES}")
    # 8. successor authority shape
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


def validate_contract_record(record: Dict[str, Any]) -> List[str]:
    """Validate a 12-field contract record. Returns violations (empty = valid).

    Known accepted gaps (documented, not hidden): ``updated_at`` may live in
    provenance/metadata; ``truth_state`` is carried by status+verification;
    ``superseded_by`` is reverse-derivable and may be null.
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
    if not isinstance(record.get("provenance"), dict):
        v.append("provenance must be an object")
    if not isinstance(record.get("lineage"), dict):
        v.append("lineage must be an object")
    ch = record.get("content_hash")
    if not isinstance(ch, str) or not re.fullmatch(r"[0-9a-f]{64}", ch):
        v.append("content_hash must be 64-char lowercase hex")
    return v
