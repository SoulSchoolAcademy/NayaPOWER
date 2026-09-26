"""Read-only live source adapter for canonical Intelligent Blocks.

Uses the existing authenticated owner session and Supabase REST endpoint.
It is a source adapter only: no mutation, no currentness decisions.
"""
from __future__ import annotations

import json
import os
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

from intelligent_block_source import load_intelligent_blocks

ROOT = Path(__file__).resolve().parents[2]


def _session_token() -> str:
    raw = os.environ.get("NAYANET_OWNER_ACCESS_TOKEN", "").strip()
    if raw:
        return raw
    p = ROOT / ".nayanet-owner-session.json"
    if p.exists():
        session = json.loads(p.read_text(encoding="utf-8"))
        token = str(session.get("access_token") or "").strip()
        if token:
            return token
    raise RuntimeError("LIVE_INTELLIGENT_BLOCK_SOURCE_ACCESS_TOKEN_MISSING")


def load_live_intelligent_blocks(*, owner_id: str) -> list[dict[str, Any]]:
    base = os.environ.get("SUPABASE_URL", "https://dahisasgpfvziswqvmvm.supabase.co").rstrip("/")
    key = os.environ.get("SUPABASE_PUBLISHABLE_KEY", "").strip()
    if not key:
        raise RuntimeError("LIVE_INTELLIGENT_BLOCK_SOURCE_PUBLISHABLE_KEY_MISSING")
    if not owner_id:
        raise RuntimeError("LIVE_INTELLIGENT_BLOCK_SOURCE_OWNER_ID_MISSING")

    query = urllib.parse.urlencode(
        {
            "select": "*",
            "owner_id": "eq." + owner_id,
            "order": "updated_at.desc",
        }
    )
    req = urllib.request.Request(
        f"{base}/rest/v1/nayanet_intelligent_blocks?{query}",
        method="GET",
        headers={
            "apikey": key,
            "Authorization": "Bearer " + _session_token(),
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            rows = json.loads(response.read().decode("utf-8"))
    except Exception as exc:
        raise RuntimeError("LIVE_INTELLIGENT_BLOCK_SOURCE_QUERY_FAILED") from exc

    if not isinstance(rows, list):
        raise RuntimeError("LIVE_INTELLIGENT_BLOCK_SOURCE_INVALID_RESPONSE")
    if not rows:
        raise RuntimeError("CANONICAL_SOURCE_EMPTY")
    return load_intelligent_blocks(rows)
