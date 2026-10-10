#!/usr/bin/env python3
"""
performance_ledger.py — The digital codex. Every shift scored, every lane measured.

Records per-shift performance: actions spent, verdict, outcome, mistakes, value.
Generates the daily scorecard Shawn reads.

Usage:
    python3 tools/performance_ledger.py log --lane <lane> --verdict <verdict> \
        --actions <n> --outcome <text> [--mistakes <n>] [--value <1-10>]
    python3 tools/performance_ledger.py report [--date YYYY-MM-DD]
    python3 tools/performance_ledger.py score --lane <lane> [--days N]

The ledger lives at: BRAIN/05-MEMORY/PERFORMANCE-LEDGER.jsonl (append-only)
One JSON object per shift. Immutable. Accountable.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from collections import defaultdict

HOME = os.path.expanduser("~")
LEDGER_PATH = os.path.join(HOME, "workspace/goals/nayapower-10-10-completion-drive/hidden_files/performance-ledger.jsonl")


def log_shift(lane, verdict, actions, outcome, mistakes=0, value=5):
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "lane": lane,
        "verdict": verdict,  # NO_WORK | WORK_AVAILABLE-done | WORK_AVAILABLE-blocked | STAND_DOWN
        "actions_spent": actions,
        "outcome": outcome[:200],
        "mistakes": mistakes,
        "value_score": value,  # 1-10: did this shift produce real value?
    }
    os.makedirs(os.path.dirname(LEDGER_PATH), exist_ok=True)
    with open(LEDGER_PATH, "a") as f:
        f.write(json.dumps(entry) + "\n")
    print(f"Logged: {lane} | {verdict} | {actions} actions | value {value}/10")
    return entry


def load_entries(date=None, lane=None, days=None):
    entries = []
    if not os.path.exists(LEDGER_PATH):
        return entries
    with open(LEDGER_PATH) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                e = json.loads(line)
                if date and e.get("date") != date:
                    continue
                if lane and e.get("lane") != lane:
                    continue
                entries.append(e)
            except json.JSONDecodeError:
                continue
    return entries


def daily_report(date=None):
    if not date:
        date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    entries = load_entries(date=date)
    if not entries:
        print(f"No shifts logged for {date}.")
        return

    by_lane = defaultdict(list)
    for e in entries:
        by_lane[e["lane"]].append(e)

    total_actions = sum(e["actions_spent"] for e in entries)
    total_mistakes = sum(e["mistakes"] for e in entries)
    productive = [e for e in entries if e["verdict"] not in ("NO_WORK", "STAND_DOWN")]
    clean_exits = [e for e in entries if e["verdict"] in ("NO_WORK", "STAND_DOWN")]

    print(f"\n{'='*60}")
    print(f"PERFORMANCE REPORT — {date}")
    print(f"{'='*60}")
    print(f"Total shifts: {len(entries)} | Total actions: {total_actions} | Mistakes: {total_mistakes}")
    print(f"Productive shifts: {len(productive)} | Clean exits: {len(clean_exits)}")

    if entries:
        avg_value = sum(e["value_score"] for e in entries) / len(entries)
        print(f"Average value score: {avg_value:.1f}/10")

    print(f"\n{'-'*60}")
    print(f"{'LANE':<25} {'SHIFTS':<8} {'ACTIONS':<8} {'MISTAKES':<9} {'AVG VALUE'}")
    print(f"{'-'*60}")
    for lane, shifts in sorted(by_lane.items()):
        actions = sum(s["actions_spent"] for s in shifts)
        mistakes = sum(s["mistakes"] for s in shifts)
        avg_v = sum(s["value_score"] for s in shifts) / len(shifts)
        print(f"{lane:<25} {len(shifts):<8} {actions:<8} {mistakes:<9} {avg_v:.1f}/10")

    # Waste detection
    print(f"\n{'-'*60}\nWASTE SIGNALS:")
    waste = [e for e in entries if e["actions_spent"] > 30 and e["value_score"] < 4]
    if waste:
        for w in waste:
            print(f"  ⚠ {w['lane']} spent {w['actions_spent']} actions for value {w['value_score']}/10: {w['outcome'][:60]}")
    else:
        print("  None detected. Clean day.")

    repeat_mistakes = [e for e in entries if e["mistakes"] > 1]
    if repeat_mistakes:
        print(f"\n  ⚠ Repeat mistakes:")
        for r in repeat_mistakes:
            print(f"    {r['lane']}: {r['mistakes']} mistakes — {r['outcome'][:60]}")


def lane_score(lane, days=7):
    entries = load_entries(lane=lane)
    if not entries:
        print(f"No data for lane {lane}.")
        return
    # Last N days
    entries = entries[-50:]  # rough window
    total_actions = sum(e["actions_spent"] for e in entries)
    total_mistakes = sum(e["mistakes"] for e in entries)
    avg_value = sum(e["value_score"] for e in entries) / len(entries)
    productive = len([e for e in entries if e["value_score"] >= 7])

    # Score: value per action, penalized by mistakes
    if total_actions == 0:
        score = 0
    else:
        raw = (sum(e["value_score"] for e in entries) / total_actions) * 10
        mistake_penalty = total_mistakes * 0.5
        score = max(0, min(10, raw - mistake_penalty))

    print(f"\nLane: {lane}")
    print(f"  Shifts: {len(entries)} | Actions: {total_actions} | Mistakes: {total_mistakes}")
    print(f"  Avg value: {avg_value:.1f}/10 | High-value shifts: {productive}/{len(entries)}")
    print(f"  EFFICIENCY SCORE: {score:.1f}/10")


def main():
    parser = argparse.ArgumentParser(description="Performance ledger — the digital codex")
    sub = parser.add_subparsers(dest="cmd", required=True)

    log_p = sub.add_parser("log", help="Log a shift")
    log_p.add_argument("--lane", required=True)
    log_p.add_argument("--verdict", required=True)
    log_p.add_argument("--actions", type=int, required=True)
    log_p.add_argument("--outcome", required=True)
    log_p.add_argument("--mistakes", type=int, default=0)
    log_p.add_argument("--value", type=int, default=5)

    rep_p = sub.add_parser("report", help="Daily report")
    rep_p.add_argument("--date", default=None)

    score_p = sub.add_parser("score", help="Lane efficiency score")
    score_p.add_argument("--lane", required=True)
    score_p.add_argument("--days", type=int, default=7)

    args = parser.parse_args()

    if args.cmd == "log":
        log_shift(args.lane, args.verdict, args.actions, args.outcome, args.mistakes, args.value)
    elif args.cmd == "report":
        daily_report(args.date)
    elif args.cmd == "score":
        lane_score(args.lane, args.days)


if __name__ == "__main__":
    main()
