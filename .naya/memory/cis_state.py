#!/usr/bin/env python3
"""Deterministic next-day Intelligence State synthesis from verified events."""
from __future__ import annotations
import json
from datetime import datetime, timedelta
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/".naya"/"memory"))
import smart_notes_v3 as brain


def build(day: str, timezone_name: str="America/Vancouver") -> dict:
    report=brain.daily_report(day, timezone_name)
    next_day=(datetime.fromisoformat(day).date()+timedelta(days=1)).isoformat()
    return {"schema":"naya-power-intelligence-state/v1","status":"DERIVED_PENDING_VERIFICATION","source_period":day,"next_day":next_day,"source_event_ids":report["source_event_ids"],"wins":report["wins"],"lessons":report["what_we_learned"],"changes":report["what_changed"],"open_loops":report["open_loops"],"next_best_actions":report["next_best_actions"],"source_event_count":report["event_count"],"verification_required":True,"preservation_rule":"This is synthesis; canonical events remain authoritative and are never deleted or replaced by the synthesis."}

if __name__=="__main__":
    import argparse
    ap=argparse.ArgumentParser(); ap.add_argument("--day",required=True); ap.add_argument("--timezone",default="America/Vancouver"); args=ap.parse_args(); print(json.dumps(build(args.day,args.timezone),indent=2,ensure_ascii=False))
