#!/usr/bin/env python3
"""Hub feeds emitter — tick t0479 (Lane 4, Mason/ACT build item #4).

Reads the live Supabase tables through the sb-api Management path (read-only SQL)
and writes room-feed/v1 JSON envelopes for the first three hub rooms:
today, lists, spaces.

Source tables (row counts re-derived at emission time):
  nayanet_intelligence_index, smart_note_artifacts, nayanet_intelligent_blocks

Privacy: this job emits METADATA-LEVEL items only (ids, titles, topics,
short summaries). Full block content bodies are NOT emitted; all
nayanet_intelligent_blocks rows are owner_scope=PRIVATE, and full public
publication of PRIVATE-scope content awaits Shawn's word.

Usage:
  python3 emit_hub_feeds.py            # writes today.json lists.json spaces.json
Output dir: the directory containing this script (HUB/FEEDS/).
"""
import json
import os
import subprocess
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

SB_API = os.path.expanduser("~/workspace/custom-connectors/custom.legacy-supabase/bin/sb-api")
PROJECT = "dahisasgpfvziswqvmvm"
SOURCE_REF = "engine-job:hub-feeds-emitter-t0479"
CONTRACT = "room-feed/v1"
TZ = ZoneInfo("America/Los_Angeles")


def q(sql):
    env = dict(os.environ)
    env["PYTHONPATH"] = "/opt/muse/skills/custom-connector-setup/bin"
    env["no_proxy"] = "localhost,127.0.0.1,::1"
    env["NO_PROXY"] = "localhost,127.0.0.1,::1"
    body = json.dumps({"query": sql, "read_only": True})
    p = subprocess.run(
        [SB_API, "POST", f"/v1/projects/{PROJECT}/database/query", body],
        capture_output=True, text=True, env=env, timeout=120,
    )
    if p.returncode != 0:
        raise RuntimeError(f"sb-api failed: {p.stderr[:500]}")
    return json.loads(p.stdout)


def slug(s):
    return "".join(c.lower() if c.isalnum() else "-" for c in (s or "untitled"))[:48].strip("-") or "untitled"


def emit_today():
    rows = q(
        "SELECT id, title, object_type, status, event_time "
        "FROM nayanet_intelligence_index "
        "WHERE status IN ('VERIFIED','DURABLE','BLOCKED','FAILED') "
        "ORDER BY event_time DESC NULLS LAST LIMIT 14"
    )
    arts = q(
        "SELECT id, artifact_type, left(content, 280) AS summary, created_at "
        "FROM smart_note_artifacts WHERE artifact_type = 'INTELLIGENCE_FEED_NOTE' "
        "ORDER BY created_at DESC LIMIT 6"
    )
    items = []
    for r in rows:
        st = (r["status"] or "").upper()
        blocker = st in ("BLOCKED", "FAILED")
        priority = 5 if st in ("BLOCKED", "FAILED") else (3 if st in ("VERIFIED", "DURABLE") else 2)
        items.append({
            "id": f"idx-{r['id']}",
            "title": r["title"] or "(untitled index row)",
            "topics": [r["object_type"] or "GENERAL"],
            "kind": "task" if blocker else "note",
            "priority": priority,
            "blocker": blocker,
            "next_action": ("resolve-blocker" if st == "BLOCKED"
                            else "triage-failure" if st == "FAILED"
                            else "carry-forward"),
            "layers": [{
                "name": "IN A NUTSHELL", "key": "nutshell", "color": "#FFFFFF",
                "tier": "primary",
                "body": f"{r['object_type'] or 'row'} · status {r['status'] or 'unknown'} · "
                        f"event {r['event_time'] or 'n/a'}",
            }],
        })
    for a in arts:
        items.append({
            "id": f"art-{a['id']}",
            "title": (a["summary"] or "")[:120] or "(untitled feed note)",
            "topics": ["SMART_NOTE"],
            "kind": "note",
            "priority": 3,
            "blocker": False,
            "next_action": "carry-forward",
            "layers": [{
                "name": "IN A NUTSHELL", "key": "nutshell", "color": "#FFFFFF",
                "tier": "primary", "body": a["summary"] or "",
            }],
        })
    items.sort(key=lambda i: -i["priority"])
    return items[:20], len(rows) + len(arts)


def emit_lists():
    # Top-20 blocks by recency -> one list per content topic.
    blocks = q(
        "SELECT intelligent_block_id, title, content->>'topic' AS topic, updated_at "
        "FROM nayanet_intelligent_blocks ORDER BY updated_at DESC NULLS LAST LIMIT 20"
    )
    by_topic = {}
    for b in blocks:
        by_topic.setdefault(b["topic"] or "UNTITLED", []).append(b)
    items = []
    for topic, members in sorted(by_topic.items(), key=lambda kv: -len(kv[1])):
        rule = (f"all nayanet_intelligent_blocks with content->>'topic' = '{topic}', "
                "ordered by updated_at desc")
        items.append({
            "id": f"list-{slug(topic)}",
            "title": f"Intelligent Blocks — {topic}",
            "topics": [topic],
            "kind": "list",
            "list_id": f"list-{slug(topic)}",
            "members": [m["intelligent_block_id"] for m in members][:20],
            "membership_rule": rule,
        })
    return items, len(blocks)


def emit_spaces():
    # Artifacts carry no topic column; partition by artifact_type (stated honestly).
    rows = q(
        "SELECT artifact_type, array_agg(id::text ORDER BY created_at DESC) AS ids, "
        "count(*) AS n FROM smart_note_artifacts GROUP BY artifact_type ORDER BY n DESC"
    )
    items = []
    for r in rows:
        sid = f"space-{slug(r['artifact_type'])}"
        items.append({
            "id": sid,
            "title": f"Space — {r['artifact_type']}",
            "topics": ["SMART_NOTE_ARTIFACT"],
            "kind": "snapshot",
            "space_id": sid,
            "pins": (r["ids"] or [])[:20],
            "posts": [],
        })
    total = sum(r["n"] for r in rows)
    return items, total


def envelope(room, items):
    return {
        "contract": CONTRACT,
        "room": room,
        "emitted_at": datetime.now(TZ).isoformat(),
        "source_ref": SOURCE_REF,
        "items": items,
    }


def validate(room, data):
    assert data["contract"] == CONTRACT, "contract field"
    assert data["room"] == room, "room match"
    assert isinstance(data["items"], list) and data["items"], "non-empty items"
    for it in data["items"]:
        for f in ("id", "title", "topics", "kind"):
            assert f in it and it[f], f"item missing {f}: {it.get('id')}"
        assert isinstance(it["topics"], list) and len(it["topics"]) >= 1, "topics >= 1"
        assert isinstance(it["id"], str) and isinstance(it["title"], str), "id/title strings"
    raw = json.dumps(data, ensure_ascii=False).encode("utf-8")
    assert len(raw) <= 256 * 1024, f"size {len(raw)} > 256KB"
    return len(raw)


def main():
    outdir = os.path.dirname(os.path.abspath(__file__))
    counts = {}
    today, counts["today_rows"] = emit_today()
    lists, counts["lists_rows"] = emit_lists()
    spaces, counts["spaces_rows"] = emit_spaces()
    for room, items in (("today", today), ("lists", lists), ("spaces", spaces)):
        data = envelope(room, items)
        size = validate(room, data)
        path = os.path.join(outdir, f"{room}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"{room}.json: {len(items)} items, {size} bytes, {path}")
    print("row counts read:", counts)


if __name__ == "__main__":
    main()
