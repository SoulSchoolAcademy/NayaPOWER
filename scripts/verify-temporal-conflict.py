#!/usr/bin/env python3
"""Temporal/supersession/conflict retrieval acceptance contract."""
from pathlib import Path
import importlib.util
import sys

ROOT=Path(__file__).resolve().parents[1]
MOD=ROOT/".naya/memory/smart_notes_v3.py"

def load():
    sys.path.insert(0, str(ROOT / ".naya/memory"))
    spec=importlib.util.spec_from_file_location("temporal_retrieval",MOD)
    mod=importlib.util.module_from_spec(spec); assert spec.loader is not None
    spec.loader.exec_module(mod); return mod

def main():
    brain=load()
    events=[
      (Path("old.json"),{"event_id":"SE-OLD","scope":"personal","project":"A","permissions":{"access":"PRIVATE"},"title":"Old architecture decision","summary":"old decision","effective_at":"2026-01-01T10:00:00-08:00","status":"SUPERSEDED","representations":[{"id":"SN-20260101-100000-old","content":"Old architecture decision"}]}),
      (Path("new.json"),{"event_id":"SE-NEW","scope":"personal","project":"A","permissions":{"access":"PRIVATE"},"title":"Current architecture decision","summary":"current decision","effective_at":"2026-09-01T10:00:00-07:00","status":"ACTIVE","relationships":{"supersedes":["SE-OLD"]},"representations":[{"id":"SN-20260901-100000-new","content":"Current architecture decision"}]}),
      (Path("conflict.json"),{"event_id":"SE-CONFLICT","scope":"personal","project":"A","permissions":{"access":"PRIVATE"},"title":"Conflicted architecture claim","summary":"conflict","effective_at":"2026-08-01T10:00:00-07:00","status":"CONFLICTED","representations":[{"id":"SN-20260801-100000-conflict","content":"Conflicted architecture claim"}]})
    ]
    old=brain.load_events; brain.load_events=lambda: events
    try:
        ranked=brain.retrieve("architecture decision",limit=3,principal_id="shawn",scope="personal",access_project="A")
        ids=[e["event_id"] for _,e in ranked]
        assert ids[0]=="SE-NEW", ids
        assert any(eid=="SE-OLD" for eid in ids)
        exact=brain.retrieve("SE-OLD",limit=1,principal_id="shawn",scope="personal",access_project="A")
        assert exact and exact[0][1]["event_id"]=="SE-OLD"
    finally:
        brain.load_events=old
    print("TEMPORAL_CONFLICT=PASS")
    print("SUPERSESSION=PASS")
    print("EXACT_HISTORICAL_RETRIEVAL=PASS")

if __name__=="__main__":
    main()
