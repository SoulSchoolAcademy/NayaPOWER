#!/usr/bin/env python3
"""Deterministically render the GitHub Smart Note projection from a receiver transaction.

The receiver is the sole IB identity authority. This script never allocates an IB ID.
It accepts the canonical receiver transaction (JSON), derives the canonical path from
receiver-issued identity + projection metadata, and renders the human-readable
Smart Note without re-authoring its intelligence.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

IB_RE = re.compile(r"^IB-\d{6}$")
ROOT = Path(__file__).resolve().parents[1]
SMART_ROOT = ROOT / ".naya" / "memory" / "smart-notes"


def clean(value: Any) -> str:
    return str(value if value is not None else "").strip()


def slug(value: Any, limit: int = 64) -> str:
    text = re.sub(r"[^a-zA-Z0-9]+", "-", clean(value)).strip("-").lower()
    return text[:limit] or "smart-note"


def topic_slug(value: Any) -> str:
    return "-".join(slug(value).split("-")[:3]) or "smart-note"


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def block_hash(block: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_json(block).encode("utf-8")).hexdigest()


def unwrap_transaction(payload: dict[str, Any]) -> dict[str, Any]:
    tx = payload.get("transaction") if isinstance(payload.get("transaction"), dict) else payload
    if not isinstance(tx, dict):
        raise ValueError("receiver transaction object required")
    return tx


def projection_meta(tx: dict[str, Any]) -> tuple[str, str]:
    block = tx.get("intelligent_block") or {}
    meta = block.get("metadata") if isinstance(block.get("metadata"), dict) else {}
    proj = block.get("projections") if isinstance(block.get("projections"), dict) else {}
    machine = proj.get("machine") if isinstance(proj.get("machine"), dict) else {}
    category = clean(meta.get("projection_category") or tx.get("projection_category") or "system")
    topic = clean(meta.get("projection_topic") or tx.get("projection_topic") or block.get("meaning", {}).get("subject") or tx.get("subject") or "smart-note")
    # Receiver-side metadata wins; caller cannot override an authoritative IB identity.
    return slug(category), topic_slug(topic)


def canonical_path(tx: dict[str, Any], root: Path = SMART_ROOT) -> Path:
    block = tx.get("intelligent_block") or {}
    identity = block.get("identity") or {}
    ib = clean(tx.get("intelligent_block_id") or identity.get("intelligent_block_id"))
    if not IB_RE.fullmatch(ib):
        raise ValueError("receiver-issued intelligent_block_id required")
    occurred = clean(
        (block.get("time") or {}).get("occurred_at")
        or tx.get("created_at")
        or tx.get("occurred_at")
    )
    if not occurred:
        raise ValueError("receiver timestamp required")
    dt = datetime.fromisoformat(occurred.replace("Z", "+00:00")).astimezone(timezone.utc)
    category, topic = projection_meta(tx)
    return root / f"{dt:%Y}" / f"{dt:%m}" / f"{dt:%d}" / category / topic / ib / "smart-note.md"


def render(tx: dict[str, Any]) -> str:
    block = tx.get("intelligent_block") or {}
    identity = block.get("identity") or {}
    meaning = block.get("meaning") or {}
    perspectives = block.get("perspectives") or {}
    intent = block.get("intent") or {}
    provenance = block.get("provenance") or {}
    evidence = block.get("evidence") or {}
    truth = block.get("truth") or {}
    authority = block.get("authority") or {}
    learning = block.get("learning") or {}
    action = block.get("action") or {}
    lifecycle = block.get("lifecycle") or {}
    outcome = block.get("outcome") or {}
    context = block.get("context") or {}
    metadata = block.get("metadata") or {}
    ib = clean(tx.get("intelligent_block_id") or identity.get("intelligent_block_id"))
    event = clean(tx.get("event_id") or identity.get("event_id") or evidence.get("event_id"))
    receipt = clean((tx.get("evidence") or {}).get("receipt_id") or evidence.get("receipt_id"))
    transaction_id = clean(tx.get("id") or tx.get("transaction_id"))
    category, topic = projection_meta(tx)
    created = clean((block.get("time") or {}).get("occurred_at") or tx.get("created_at"))
    h = clean((block.get("integrity") or {}).get("content_hash")) or block_hash(block)
    smart_link = f"https://github.com/SoulSchoolAcademy/NayaPOWER/blob/main/.naya/memory/smart-notes/{created[:4]}/{created[5:7]}/{created[8:10]}/{category}/{topic}/{ib}/smart-note.md"

    machine = json.dumps(block, ensure_ascii=False, sort_keys=True, indent=2)
    return f"""# SMART NOTE — {clean(meaning.get("title") or meaning.get("subject") or tx.get("subject") or "Smart Note")} — {created[:10]}

**Smart Note = Intelligent Block**
**Intelligent Block ID:** `{ib}`
**Schema:** `{clean(identity.get("schema_version"))}`
**Category:** {category}
**Topic:** {topic}
**Canonical Source Event:** `{event}`
**Canonical Receiver:** `v7-smart-note-canonical`
**Smart Note Receipt:** `{receipt}`
**Transaction:** `{transaction_id}`
**Intelligent Block Hash:** `{h}`
**Owner Scope:** {clean(context.get("scope") or context.get("visibility"))}
**Truth State:** {clean(truth.get("state"))}
**Learning State:** {clean(learning.get("applicability") or "Candidate — future application and outcome verification required")}

## IN A NUTSHELL

{clean(meaning.get("in_a_nutshell") or meaning.get("summary"))}

## DATE / TIME

{created}

## WHAT

{clean(meaning.get("content") or meaning.get("human"))}

## WHY IT MATTERS

{clean(intent.get("why"))}

## HUMAN

{clean(perspectives.get("human") or meaning.get("human"))}

## CHILD

{clean(perspectives.get("child") or meaning.get("simple"))}

## GRANDMA

{clean(perspectives.get("grandma"))}

## NAYA

{clean(perspectives.get("naya") or meaning.get("naya"))}

## MACHINE

```json
{machine}
```

## WHAT WE LEARNED

{clean(perspectives.get("learning") or learning.get("lesson") or learning.get("what_changed"))}

## CONNECTIONS

{clean(perspectives.get("connections"))}

## HOW TO APPLY

{clean(perspectives.get("application") or action.get("action"))}

## WHAT IT ULTIMATELY MEANS

{clean(perspectives.get("meaning") or intent.get("desired_outcome"))}

## WHAT'S IN IT FOR YOU / US

{clean(perspectives.get("value"))}

## NEXT ACTION

{clean(action.get("action") or "Retrieve and verify when relevant.")

}

## CANONICAL RECEIPT

**Source event:** `{event}`

**Receiver:** `v7-smart-note-canonical`

**Lifecycle:** `{clean(lifecycle.get("stage"))}`

**Outcome:** `{clean(outcome.get("state"))}`

**Provenance source:** `{clean(provenance.get("source"))}`

**Evidence state:** `{clean(evidence.get("evidence_state"))}`

**Authority:** `{clean(authority.get("state"))}`

**Canonical content hash:** `{h}`

**Smart Link:** {smart_link}

**Hub Deep Link:** `/hub?ib={ib}`

> The Smart Link is the direct GitHub `smart-note.md` projection. The Hub URL is a Hub Deep Link and is never substituted for the Smart Link.
"""


def verify_projection(tx: dict[str, Any], existing: str) -> None:
    expected = render(tx)
    if existing != expected:
        raise ValueError("SMART_NOTE_PROJECTION_DRIFT: existing projection differs from deterministic receiver projection")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("transaction_json", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--verify", type=Path)
    args = parser.parse_args()
    payload = json.loads(args.transaction_json.read_text(encoding="utf-8"))
    tx = unwrap_transaction(payload)
    rendered = render(tx)
    if args.verify:
        verify_projection(tx, args.verify.read_text(encoding="utf-8"))
        print("SMART_NOTE_PROJECTION=VERIFIED")
        return 0
    if not args.output:
        raise SystemExit("--output is required unless --verify is used")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(rendered, encoding="utf-8")
    print(json.dumps({"status": "GENERATED", "path": str(args.output), "ib": clean((tx.get("intelligent_block") or {}).get("identity", {}).get("intelligent_block_id") or tx.get("intelligent_block_id"))}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
