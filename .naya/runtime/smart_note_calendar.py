#!/usr/bin/env python3
"""Canonical Smart Note / Intelligent Block projection boundary.

The live v7-smart-note-canonical receiver is the sole creation and IB identity
authority. This module only materializes a human-readable projection after a
receiver-issued completion receipt.
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import json
import re
import sys

RUNTIME_ROOT = Path(__file__).resolve().parent
if str(RUNTIME_ROOT) not in sys.path:
    sys.path.insert(0, str(RUNTIME_ROOT))

from calendar_projection import _utc_parts, safe_topic
from smart_note_transaction import canonical_smart_note_path

ROOT = Path(__file__).resolve().parents[2]
SMART_NOTES_ROOT = ROOT / ".naya" / "memory" / "smart-notes"
RECEIVER = "v7-smart-note-canonical"
IB_ID_RE = re.compile(r"^IB-\d{6}$")

REQUIRED_HEADINGS = (
    "IN A NUTSHELL","DATE / TIME","WHAT","WHY IT MATTERS","HUMAN","CHILD",
    "GRANDMA","NAYA","MACHINE","WHAT WE LEARNED","CONNECTIONS","HOW TO APPLY",
    "WHAT IT ULTIMATELY MEANS","WHAT'S IN IT FOR YOU / US","NEXT ACTION",
)

def validate_smart_note(body: str) -> list[str]:
    return [h for h in REQUIRED_HEADINGS if f"## {h}" not in body]

def _receiver_identity(receipt: dict[str, Any]) -> tuple[str, str]:
    if not isinstance(receipt, dict):
        raise ValueError("CANONICAL_RECEIVER_RECEIPT_REQUIRED")
    if str(receipt.get("canonical_receiver","")).strip() != RECEIVER:
        raise ValueError("CANONICAL_RECEIVER_RECEIPT_INVALID")
    status = str(receipt.get("status") or receipt.get("pipeline") or "").strip().lower()
    if status not in {"completed", "replayed"}:
        raise ValueError("CANONICAL_RECEIVER_RECEIPT_NOT_COMPLETED")
    ib_id = str(receipt.get("intelligent_block_id","")).strip()
    event_id = str(receipt.get("event_id") or receipt.get("source_event_id") or "").strip()
    transaction_id = str(receipt.get("transaction_id") or "").strip()
    if not IB_ID_RE.fullmatch(ib_id):
        raise ValueError("CANONICAL_RECEIVER_RECEIPT_MISSING_RECEIVER_ISSUED_IB")
    if not event_id:
        raise ValueError("CANONICAL_RECEIVER_RECEIPT_MISSING_EVENT_ID")
    if not transaction_id:
        raise ValueError("CANONICAL_RECEIVER_RECEIPT_MISSING_TRANSACTION_ID")
    return ib_id, event_id

def _upsert_registry(*, registry_path: Path, ib_id: str, projection_path: Path,
                     timestamp: str, category: str, topic: str, event_id: str) -> None:
    registry = json.loads(registry_path.read_text(encoding="utf-8")) if registry_path.exists() else {
        "$schema":"naya/smart-note-registry/v1","status":"CANONICAL",
        "entries":[]
    }
    if registry.get("status") != "CANONICAL":
        raise ValueError("CANONICAL_SMART_NOTE_REGISTRY_NOT_CANONICAL")
    relative = projection_path.relative_to(registry_path.parents[2]).as_posix()
    entries = registry.setdefault("entries", [])
    matches = [e for e in entries if isinstance(e,dict) and e.get("intelligent_block_id")==ib_id]
    for e in matches:
        if e.get("path") != relative:
            raise ValueError("CANONICAL_IB_ID_ALREADY_BOUND_TO_DIFFERENT_PATH")
    record = {"intelligent_block_id":ib_id,"path":relative,"date":timestamp[:10],
              "category":category,"topic":safe_topic(topic),"status":"CANONICAL",
              "source_event_id":event_id}
    if matches: matches[0].update(record)
    else: entries.append(record)
    entries.sort(key=lambda e:str(e.get("intelligent_block_id","")))
    registry_path.write_text(json.dumps(registry,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")

def persist_smart_note(*, timestamp: str | None, topic: str, body: str,
                       receiver_receipt: dict[str, Any], category: str = "system",
                       root: Path | None = None) -> dict[str, Any]:
    missing = validate_smart_note(body)
    if missing:
        raise ValueError("Smart Note contract missing headings: " + ", ".join(missing))
    ib_id, event_id = _receiver_identity(receiver_receipt)
    stamp = timestamp or datetime.now(timezone.utc).isoformat()
    destination_root = Path(root) if root else SMART_NOTES_ROOT
    path = canonical_smart_note_path(stamp, topic, category=category, ib_id=ib_id, root=destination_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_text(encoding="utf-8") != body:
            raise ValueError(f"Smart Note projection conflict: {path}")
        status = "REPLAY"
    else:
        path.write_text(body.rstrip()+"\n",encoding="utf-8")
        status = "CREATED"
    day_index = path.parent / "INDEX.md"
    link = path.name
    if day_index.exists():
        index = day_index.read_text(encoding="utf-8")
        if link not in index: day_index.write_text(index.rstrip()+f"\n- [{topic}](./{link})\n",encoding="utf-8")
    else:
        dt,_ = _utc_parts(stamp)
        day_index.write_text(f"# Smart Notes — {dt:%Y-%m-%d}\n\n## Records\n\n- [{topic}](./{link})\n",encoding="utf-8")
    _upsert_registry(registry_path=destination_root/"REGISTRY.json",ib_id=ib_id,
                     projection_path=path,timestamp=stamp,category=category,
                     topic=topic,event_id=event_id)
    return {"status":status,"path":str(path),"timestamp":stamp,"topic":safe_topic(topic),
            "intelligent_block_id":ib_id,"source_event_id":event_id,"canonical_receiver":RECEIVER}

__all__=["persist_smart_note","validate_smart_note","SMART_NOTES_ROOT"]
