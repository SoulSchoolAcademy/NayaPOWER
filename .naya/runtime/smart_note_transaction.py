#!/usr/bin/env python3
"""Canonical Smart Note -> governed learning -> PIS -> Hub transaction.

The Smart Note is the authoritative durable human-readable intelligence record.
This module is the single transaction boundary that turns one canonical Smart
Note into:
1) a retained CIS learning record,
2) a projected PIS event for the Intelligent Hub, and
3) a durable transaction receipt.

No caller may claim completion without all three boundaries succeeding.
"""
from __future__ import annotations

import hashlib
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
SMART_NOTES_ROOT = ROOT / "SUPERBRAIN" / "SMART-NOTES"
CIS_ROOT = ROOT / ".naya" / "memory" / "intelligence"
CIS_PATH = CIS_ROOT / "CIS.json"
RECEIPTS_ROOT = CIS_ROOT / "transactions"
PIS_PATH = ROOT / "NAYANET" / "HUB" / "public" / "intelligence" / "pis-feed.json"

REQUIRED = (
    "in_a_nutshell", "child", "grammar", "human", "naya", "machine",
    "learning", "why_it_matters", "how_to_use", "value", "evidence",
    "current_state", "next_action",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def slug(value: str) -> str:
    token = re.sub(r"[^A-Za-z0-9]+", "-", value.strip()).strip("-").upper()
    return token[:100] or "SMART-NOTE"


def note_id(timestamp: str, topic: str) -> str:
    stamp = timestamp.replace(":", "").replace("+00:00", "Z").replace("-", "")
    return f"SN-{stamp}-{slug(topic)}"


def validate_note(note: dict[str, Any]) -> None:
    missing = [k for k in REQUIRED if not str(note.get(k, "")).strip()]
    if missing:
        raise ValueError("Smart Note missing required perspectives: " + ", ".join(missing))
    if not isinstance(note["evidence"], list) or not note["evidence"]:
        raise ValueError("Smart Note requires at least one evidence item")
    if isinstance(note["next_action"], list):
        raise ValueError("Smart Note Next Action must be one executable action, not a list")


def render_note(note: dict[str, Any]) -> str:
    evidence = "\n".join(f"- {item}" for item in note["evidence"])
    return f"""# SMART NOTE — {note["topic"]}

**Timestamp:** {note["timestamp"]}
**Smart Note ID:** `{note["id"]}`
**Status:** CANONICAL / TRANSACTIONALLY PROJECTED
**Type:** Durable intelligence
**Parent:** NayaPOWER Superbrain

## In a Nutshell

{note["in_a_nutshell"]}

## Child / Derived Note

{note["child"]}

## Grammar Note

{note["grammar"]}

## Human Note

{note["human"]}

## Naya Note

{note["naya"]}

## Machine Note

{note["machine"]}

## Learning Lesson / Adaptive Learning

{note["learning"]}

## Why It Matters

{note["why_it_matters"]}

## How to Use It

{note["how_to_use"]}

## What's In It For Me / You / Us

{note["value"]}

## Evidence / Smart Links

{evidence}

## Current State

{note["current_state"]}

## ONE Next Action

**{note["next_action"]}**

## Transaction State

- Smart Note: **PERSISTED**
- CIS learning: **{note["cis_status"]}**
- PIS projection: **{note["pis_status"]}**
- Hub projection: **{note["hub_status"]}**
- Receipt: `{note["receipt_id"]}`
"""


def _load_cis() -> dict[str, Any]:
    if not CIS_PATH.exists():
        return {"schema_version": "CIS-1.0", "updated_at": utc_now(), "learning": []}
    return json.loads(CIS_PATH.read_text(encoding="utf-8"))


def _write_json(path: Path, body: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(body, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def apply_cis_learning(note: dict[str, Any]) -> dict[str, Any]:
    cis = _load_cis()
    rows = cis.setdefault("learning", [])
    fingerprint = hashlib.sha256(
        f'{note["topic"]}|{note["learning"]}|{"|".join(note["evidence"])}'.encode("utf-8")
    ).hexdigest()
    existing = next((row for row in rows if row.get("fingerprint") == fingerprint), None)
    if existing:
        return {"status": "REPLAY", "fingerprint": fingerprint, "learning": existing}

    row = {
        "learning_id": f"CL-{fingerprint[:16]}",
        "smart_note_id": note["id"],
        "topic": note["topic"],
        "lesson": note["learning"],
        "machine_consequence": note["machine"],
        "current_state": note["current_state"],
        "next_action": note["next_action"],
        "evidence": note["evidence"],
        "status": "RETAINED_GOVERNED_CANDIDATE",
        "fingerprint": fingerprint,
        "created_at": utc_now(),
    }
    rows.append(row)
    cis["updated_at"] = utc_now()
    _write_json(CIS_PATH, cis)
    return {"status": "CREATED", "fingerprint": fingerprint, "learning": row}


def build_pis_projection(note: dict[str, Any]) -> dict[str, Any]:
    import importlib.util

    script = ROOT / "scripts" / "build-smart-feed-projection.py"
    spec = importlib.util.spec_from_file_location("naya_pis_projection", script)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load canonical PIS projection builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not hasattr(module, "build_projection"):
        raise RuntimeError("canonical PIS projection builder lacks build_projection()")
    return module.build_projection()


def build_personal_feed_block(event: dict[str, Any], *, consumer: str = "nayanet-hub.personal-feed") -> dict[str, Any]:
    """Create the human-facing block from one authoritative PIS event."""
    if event.get("privacy") != {"visibility": "private", "consent_state": "not_granted"}:
        raise RuntimeError(f"Personal Feed boundary requires private-by-default event: {event.get('event_id')}")
    import importlib.util
    import sys
    cct_path = Path(__file__).with_name("cct_intelligent_block.py")
    spec = importlib.util.spec_from_file_location("naya_cct_intelligent_block", cct_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load canonical Intelligent Block verifier")
    cct = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = cct
    spec.loader.exec_module(cct)
    make_block = cct.make_block
    verify_block = cct.verify_block

    block = make_block(
        block_id=f"IB-{event['event_id']}",
        producer="naya.superbrain.pis",
        content={
            "event_id": event["event_id"],
            "title": event["source"]["label"],
            "summary": event.get("weaver_synthesis", {}).get("summary"),
            "lesson": event.get("lesson", {}).get("text"),
            "meaning": event.get("meaning", {}).get("text"),
            "action": event.get("action", {}).get("text"),
        },
        evidence=[
            {"kind": "source_event", "event_id": event["event_id"]},
            *[{"kind": "event_evidence", "value": item} for item in event.get("machine_evidence", {}).get("items", [])],
        ],
        permissions={"consumers": [consumer], "purposes": ["consume"]},
        verification="SUPPORTED",
        parent=event["event_id"],
        derivation="pis-to-personal-feed",
    )
    decision = verify_block(block, consumer=consumer, purpose="consume")
    if not decision.allowed:
        raise RuntimeError(f"Personal Feed Intelligent Block rejected: {decision.reason}")
    return block


def _persist_and_verify(path: Path, rendered: str, note_id_value: str) -> dict[str, str]:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(rendered, encoding="utf-8")
    if not path.exists():
        raise RuntimeError(f"authoritative Smart Note persistence failed: {path}")
    persisted = path.read_text(encoding="utf-8")
    if persisted != rendered or note_id_value not in persisted:
        raise RuntimeError(f"authoritative Smart Note persistence verification failed: {path}")
    return {
        "path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "sha256": hashlib.sha256(persisted.encode("utf-8")).hexdigest(),
        "verified_at": utc_now(),
    }


class _TransactionLock:
    """Cross-process atomic lock for the shared CIS/PIS transaction boundary."""
    def __init__(self, root: Path, timeout: float = 30.0, stale_after: float = 300.0):
        self.path = root / ".naya" / "locks" / "smart-note-transaction.lock"
        self.timeout = timeout
        self.stale_after = stale_after

    def __enter__(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        deadline = time.monotonic() + self.timeout
        while True:
            try:
                self.path.mkdir()
                (self.path / "owner").write_text(f"{time.time()}\n", encoding="utf-8")
                return self
            except FileExistsError:
                try:
                    age = time.time() - self.path.stat().st_mtime
                    if age > self.stale_after:
                        import shutil
                        shutil.rmtree(self.path, ignore_errors=True)
                        continue
                except FileNotFoundError:
                    continue
                if time.monotonic() >= deadline:
                    raise RuntimeError("Smart Note transaction lock contention: another transaction is active")
                time.sleep(0.05)

    def __exit__(self, exc_type, exc, tb):
        import shutil
        shutil.rmtree(self.path, ignore_errors=True)


def execute(note: dict[str, Any]) -> dict[str, Any]:
    validate_note(note)
    with _TransactionLock(ROOT):
        stamp = str(note.get("timestamp") or utc_now())
        note = dict(note)
        note["timestamp"] = stamp
        note["id"] = str(note.get("id") or note_id(stamp, note["topic"]))

        dt = datetime.fromisoformat(stamp.replace("Z", "+00:00")).astimezone(timezone.utc)
        path = SMART_NOTES_ROOT / f"{dt:%Y}" / f"{dt:%m}" / f"{dt:%d}" / (
            f"{dt:%Y-%m-%dT%H-%M-%SZ}__{slug(note['topic'])}.md"
        )
        if path.exists():
            existing = path.read_text(encoding="utf-8")
            if note["id"] not in existing:
                raise RuntimeError(f"Smart Note path conflict: {path}")

        note["cis_status"] = "PENDING"
        note["pis_status"] = "PENDING"
        note["hub_status"] = "PENDING"
        note["receipt_id"] = f"SN-RCP-{note['id']}"
        rendered = render_note(note)
        persistence = _persist_and_verify(path, rendered, note["id"])

        cis = apply_cis_learning(note)
        note["cis_status"] = cis["status"]
        pis = build_pis_projection(note)
        note["pis_status"] = pis["status"]
        note["hub_status"] = "PROJECTED"
        _persist_and_verify(path, render_note(note), note["id"])

        projected_event = next((e for e in pis.get("events", []) if e.get("event_id") == note["id"]), None)
        if projected_event is None:
            raise RuntimeError(f"PIS projection missing authoritative Smart Note event: {note['id']}")
        if projected_event.get("created_at") != stamp or projected_event.get("updated_at") != stamp:
            raise RuntimeError(f"Smart Note timestamp provenance mismatch: {note['id']}")
        if projected_event.get("source", {}).get("id") != note["id"]:
            raise RuntimeError(f"Smart Note source provenance mismatch: {note['id']}")
        if projected_event.get("context", {}).get("canonical_path") != persistence["path"]:
            raise RuntimeError(f"Smart Note canonical-path provenance mismatch: {note['id']}")
        if projected_event.get("privacy") != {"visibility": "private", "consent_state": "not_granted"}:
            raise RuntimeError(f"Smart Note privacy boundary mismatch: {note['id']}")

        personal_feed_block = build_personal_feed_block(projected_event)
        projected_event["intelligent_block"] = personal_feed_block
        for index, event in enumerate(pis.get("events", [])):
            if event.get("event_id") == note["id"]:
                pis["events"][index] = projected_event
                break
        _write_json(PIS_PATH, pis)

        receipt = {
            "schema_version": "SMART-NOTE-TRANSACTION-1.1",
            "receipt_id": note["receipt_id"],
            "status": "VERIFIED_TRANSACTION" if pis.get("status") in {"CREATED", "REBUILT"} else "REPLAY_TRANSACTION",
            "smart_note_id": note["id"],
            "smart_note_path": persistence["path"],
            "authoritative_persistence": persistence,
            "cis": cis,
            "pis": {"status": pis.get("status"), "path": str(PIS_PATH.relative_to(ROOT)).replace("\\", "/"), "event_id": note["id"], "created_at": projected_event["created_at"], "updated_at": projected_event["updated_at"]},
            "hub": {"status": "PROJECTED", "path": str(PIS_PATH.relative_to(ROOT)).replace("\\", "/"), "intelligent_block_id": personal_feed_block["block_id"], "personal_feed": "PRIVATE"},
            "privacy": projected_event["privacy"],
            "intelligent_block": {"status": "VERIFIED", "block_id": personal_feed_block["block_id"], "consumer": "nayanet-hub.personal-feed", "parent_event_id": note["id"]},
            "provenance": {"source_id": projected_event["source"]["id"], "canonical_path": projected_event["context"]["canonical_path"]},
            "evidence": note["evidence"],
            "current_state": note["current_state"],
            "next_action": note["next_action"],
            "completed_at": utc_now(),
        }
        receipt_path = RECEIPTS_ROOT / f"{note['id']}.json"
        _write_json(receipt_path, receipt)
        return {"status": receipt["status"], "smart_note": path, "cis": cis, "pis": pis, "receipt": receipt_path}


    __all__ = ["execute", "validate_note", "REQUIRED"]
