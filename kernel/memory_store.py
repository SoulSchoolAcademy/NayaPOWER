"""NayaPOWER memory store: the durable, integrity-governed home for MemoryRecords.

This is the wiring layer between the memory-metabolism machinery
(`kernel/memory_metabolism.py`) and the runtime. The machinery defines *how*
intelligence lives and dies; this store defines *where* it lives and *who*
invokes the lifecycle:

- Append-only JSONL record log: nothing is ever deleted or rewritten. Every
  mutation appends a new full version of the record; on load the latest
  version of each record_id wins. History stays reconstructible.
- Append-only JSONL receipt log: every transition receipt plus every
  corruption/quarantine event, hash-chained (each entry commits to the
  previous). The chain is independently verifiable end-to-end — this is the
  cold-retrievable audit trail of the memory's whole life.
- `load()` reconstructs all records from zero warm state (cold-boot
  reconstruction). Corrupt lines and integrity failures do not poison the
  store: each is individually quarantined with a receipt; QUARANTINED records
  are never served, ever.
- `serve()` routes retrieval through the fail-closed `retrieve()`: ACTIVE
  records with integrity verified *at read*. Retrieval touches
  (last_retrieved_at / retrieval_count) are persisted — the log reflects
  reality.
- `housekeep(now, stale_after_days)` runs the deterministic decay pass.
  Pure function of (records, now, policy): same input, same output, same
  receipts. No clock reads inside.
- CLI (`python -m kernel.memory_store ...`) so any scheduler can invoke the
  periodic wiring without touching runtime code:
      housekeep --store PATH --now ISO --stale-days 90
      serve     --store PATH [--epistemic VERIFIED_FACT]
      verify    --store PATH            # receipt chain + store health

Adapter contract (capture and retrieval lanes integrate here, not inside
this module):
- Capture: build records via `memory_metabolism.create_record()` and call
  `store.save(record)`. Strengthen via the machinery, then `save()` again.
  This module never calls the Receiver; the Receiver is the canonical writer.
- Retrieval: consumers call `store.serve(...)`, never raw record lists.
  Stale intelligence (SUPERSEDED/DECAYED/ARCHIVED) is available for audit
  only through `include_audit_states`, always labeled AUDIT:<STATE>.

Hard laws (inherited from the machinery, enforced here):
- QUARANTINED records are never served under any flag.
- Integrity is verified at load AND at read; any failure fails closed.
- Nothing is deleted: demotion preserves lineage, provenance, history.
- All persisted mutations are receipted; receipts are hash-chained.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from kernel import memory_metabolism as mm


def _utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class MemoryStoreError(ValueError):
    """Raised when the store refuses an operation."""


GENESIS_CHAIN = "MMC-GENESIS"
RECORDS_FILENAME = "records.jsonl"
RECEIPTS_FILENAME = "receipts.jsonl"


# Serialization ----------------------------------------------------------------

_RECORD_FIELDS = tuple(f for f in mm.MemoryRecord.__dataclass_fields__)


def _record_to_dict(record: mm.MemoryRecord) -> dict[str, Any]:
    payload = asdict(record)
    return {k: payload[k] for k in _RECORD_FIELDS}


def _record_from_dict(payload: dict[str, Any]) -> mm.MemoryRecord:
    unknown = set(payload) - set(_RECORD_FIELDS)
    if unknown:
        raise MemoryStoreError(f"record_unknown_fields:{sorted(unknown)}")
    return mm.MemoryRecord(**{k: payload.get(k) for k in _RECORD_FIELDS})


def _canonical(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


# Receipt hash chain ------------------------------------------------------------

def _chain_step(prev_chain: str, receipt: dict[str, Any]) -> str:
    raw = (prev_chain + "\n" + _canonical(receipt)).encode()
    return "MMC-" + hashlib.sha256(raw).hexdigest()[:32]


def verify_receipt_chain(entries: list[dict[str, Any]]) -> list[int]:
    """Return the log_seq values whose chain link does not verify. Empty = clean."""
    broken: list[int] = []
    prev = GENESIS_CHAIN
    for entry in sorted(entries, key=lambda e: e["log_seq"]):
        receipt = {k: v for k, v in entry.items()
                   if k not in ("log_seq", "prev_chain", "chain")}
        if entry.get("prev_chain") != prev:
            broken.append(entry["log_seq"])
            prev = entry.get("chain", prev)
            continue
        if _chain_step(prev, receipt) != entry.get("chain"):
            broken.append(entry["log_seq"])
        prev = entry.get("chain", prev)
    return broken


# Store -------------------------------------------------------------------------

class MemoryStore:
    """Durable, integrity-governed store for memory-metabolism records."""

    def __init__(self, directory: str | Path):
        self.directory = Path(directory)
        self.records_path = self.directory / RECORDS_FILENAME
        self.receipts_path = self.directory / RECEIPTS_FILENAME
        self._records: dict[str, mm.MemoryRecord] = {}
        self._receipts: list[dict[str, Any]] = []
        self._corruption: list[dict[str, Any]] = []

    # -- persistence primitives ------------------------------------------------

    def _append_jsonl(self, path: Path, payload: dict[str, Any]) -> None:
        self.directory.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as fh:
            fh.write(_canonical(payload) + "\n")

    def _read_jsonl(self, path: Path) -> list[tuple[int, str]]:
        if not path.exists():
            return []
        return [(n, line) for n, line in
                enumerate(path.read_text(encoding="utf-8").splitlines(), start=1)
                if line.strip()]

    # -- receipts ----------------------------------------------------------------

    def _log_receipt(self, receipt: dict[str, Any]) -> dict[str, Any]:
        prev = self._receipts[-1]["chain"] if self._receipts else GENESIS_CHAIN
        entry = dict(receipt)
        entry["log_seq"] = len(self._receipts)
        entry["prev_chain"] = prev
        entry["chain"] = _chain_step(prev, receipt)
        self._receipts.append(entry)
        self._append_jsonl(self.receipts_path, entry)
        return entry

    # -- records -----------------------------------------------------------------

    def save(self, record: mm.MemoryRecord) -> str:
        """Append a record version. Integrity must verify; nothing is rewritten."""
        if not mm.integrity_ok(record):
            raise MemoryStoreError("save_refused_integrity_failed")
        self._append_jsonl(self.records_path, _record_to_dict(record))
        self._records[record.record_id] = record
        return record.record_id

    def _quarantine_line(self, lineno: int, raw: str, reason: str,
                        now: str) -> mm.MemoryRecord:
        """Isolate a corrupt log line as a QUARANTINED record. Never served."""
        digest = hashlib.sha256(raw.encode()).hexdigest()[:16]
        placeholder = mm.MemoryRecord(
            record_id=f"CORRUPT-L{lineno}-{digest}",
            content=f"<unparseable log line {lineno}: {reason}>",
            epistemic_state="EXTERNAL_CLAIM",
            provenance={"corrupt_line": lineno, "raw_sha256": digest},
            memory_state=mm.QUARANTINED,
            created_at=now,
            last_verified_at=now,
        )
        # Integrity intentionally left as-is on quarantine: the broken hash
        # (or absence of one) is itself the evidence. Set a marker so the
        # placeholder is a well-formed dataclass instance.
        placeholder.integrity = "QUARANTINED-NO-HASH"
        self._corruption.append({
            "line": lineno, "reason": reason, "raw_sha256": digest,
            "quarantined_as": placeholder.record_id,
        })
        receipt = mm.quarantine(placeholder,
                                f"corrupt_line={lineno} reason={reason}", now=now)
        receipt["raw_sha256"] = digest
        # Idempotent across loads: the corrupt line is permanent evidence in
        # the record log, so re-quarantining it on every load must not mint a
        # new receipt each time. One quarantine receipt per corrupt line.
        already = any(e.get("transition") == "quarantine"
                      and e.get("raw_sha256") == digest
                      for e in self._receipts)
        if not already:
            self._log_receipt(receipt)
        self._records[placeholder.record_id] = placeholder
        return placeholder

    def load(self, *, now: str | None = None) -> dict[str, mm.MemoryRecord]:
        """Cold-boot reconstruction: rebuild all records from zero warm state.

        Latest version of each record_id wins. Lines that fail to parse and
        records that fail integrity are individually quarantined with receipts;
        they never poison the rest of the store. Returns the record map.
        """
        at = now or _utcnow_iso()
        self._records = {}
        self._receipts = [dict(e) for e in self._iter_receipts()]
        self._corruption = []
        for lineno, raw in self._read_jsonl(self.records_path):
            try:
                payload = json.loads(raw)
            except json.JSONDecodeError:
                self._quarantine_line(lineno, raw, "json_decode_failed", at)
                continue
            if not isinstance(payload, dict):
                self._quarantine_line(lineno, raw, "not_an_object", at)
                continue
            try:
                record = _record_from_dict(payload)
            except (MemoryStoreError, TypeError):
                self._quarantine_line(lineno, raw, "schema_mismatch", at)
                continue
            if not mm.integrity_ok(record):
                # Tampered or half-written version: quarantine the *version*,
                # keep the raw line in the log as evidence (nothing deleted).
                self._quarantine_line(lineno, raw, "integrity_failed", at)
                continue
            self._records[record.record_id] = record
        return dict(self._records)

    def _iter_receipts(self) -> Iterable[dict[str, Any]]:
        for _, raw in self._read_jsonl(self.receipts_path):
            try:
                entry = json.loads(raw)
            except json.JSONDecodeError:
                continue
            if isinstance(entry, dict) and "log_seq" in entry:
                yield entry

    # -- runtime wiring ------------------------------------------------------------

    def serve(self, predicate=None, *, include_audit_states: tuple[str, ...] = (),
              now: str | None = None, persist_touch: bool = True
              ) -> mm.RetrievalResult:
        """Serve records under fail-closed discipline; persist retrieval touches."""
        for state in include_audit_states:
            if state == mm.QUARANTINED:
                raise MemoryStoreError("quarantine_never_served")
            if state not in mm.MEMORY_STATES:
                raise MemoryStoreError(f"audit_state_unknown:{state}")
        result = mm.retrieve(
            list(self._records.values()), predicate,
            include_audit_states=include_audit_states, now=now)
        if persist_touch:
            for record, _label in result.items:
                self._append_jsonl(self.records_path, _record_to_dict(record))
        return result

    def housekeep(self, *, now: str, stale_after_days: float = 90.0
                  ) -> list[dict[str, Any]]:
        """Run the deterministic decay pass; persist changes; receipt everything."""
        before = {rid: r.integrity for rid, r in self._records.items()}
        records = list(self._records.values())
        _, receipts = mm.metabolize(records, now=now,
                                    stale_after_days=stale_after_days)
        for record in records:
            if before.get(record.record_id) != record.integrity:
                self._append_jsonl(self.records_path, _record_to_dict(record))
        logged = [self._log_receipt(r) for r in receipts]
        return logged

    # -- health --------------------------------------------------------------------

    def health(self) -> dict[str, Any]:
        """Store health snapshot: counts by state, chain status, corruption."""
        by_state: dict[str, int] = {}
        for record in self._records.values():
            by_state[record.memory_state] = by_state.get(record.memory_state, 0) + 1
        return {
            "records": len(self._records),
            "by_state": by_state,
            "receipts": len(self._receipts),
            "receipt_chain_broken": verify_receipt_chain(self._receipts),
            "corrupt_lines": len(self._corruption),
            "corruption": list(self._corruption),
        }


# CLI ----------------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Memory-metabolism store: durable wiring for the governed "
                    "lifecycle of durable intelligence.")
    parser.add_argument("--store", required=True,
                        help="store directory (records.jsonl + receipts.jsonl)")
    sub = parser.add_subparsers(dest="command", required=True)

    hk = sub.add_parser("housekeep", help="run the deterministic decay pass")
    hk.add_argument("--now", required=True, help="ISO timestamp (explicit; no clock reads)")
    hk.add_argument("--stale-days", type=float, default=90.0)

    sv = sub.add_parser("serve", help="serve ACTIVE records (fail-closed)")
    sv.add_argument("--now", default=None)
    sv.add_argument("--epistemic", default=None,
                    help="filter to one epistemic state")
    sv.add_argument("--include-audit", default="",
                    help="comma-separated audit states to include (labeled)")

    sub.add_parser("verify", help="verify receipt chain + report store health")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    store = MemoryStore(args.store)
    store.load()
    if args.command == "housekeep":
        receipts = store.housekeep(now=args.now, stale_after_days=args.stale_days)
        changed = [r for r in receipts if r.get("to_state") != "ACTIVE"
                   or "not_stale_noop" not in r.get("detail", "")]
        print(json.dumps({"receipts": len(receipts), "state_changes": len(changed),
                          "health": store.health()}, indent=2, sort_keys=True))
    elif args.command == "serve":
        predicate = None
        if args.epistemic:
            predicate = lambda r: r.epistemic_state == args.epistemic  # noqa: E731
        audit = tuple(s for s in args.include_audit.split(",") if s)
        result = store.serve(predicate, include_audit_states=audit, now=args.now)
        print(json.dumps({
            "served": [{"record_id": r.record_id, "label": label,
                        "epistemic_state": r.epistemic_state,
                        "memory_state": r.memory_state}
                       for r, label in result.items],
            "dropped_integrity_failed": result.dropped_integrity_failed,
        }, indent=2, sort_keys=True))
    elif args.command == "verify":
        print(json.dumps(store.health(), indent=2, sort_keys=True))
        if store.health()["receipt_chain_broken"]:
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
