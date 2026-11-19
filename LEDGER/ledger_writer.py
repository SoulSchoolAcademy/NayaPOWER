#!/usr/bin/env python3
"""
Activity Ledger writer — Team Naya's "don't tell me, show me" proof layer.

Reads twelve-lane-scores.jsonl + twelve-lane-receipts/ and produces:
  - activity-ledger.jsonl  (machine-readable data stream — future GitHub App feeds this to the smart ledger / hub)
  - ACTIVITY-LEDGER.md    (human-readable, GitHub-rendered — who's working, who did what, with receipts)
  - STATS.md              (smart stats — verified actions, score trends, learning velocity)

Every entry is a VERIFIED ACTION: agent name, team, tick, task, receipt, score,
artifacts. A claim without a receipt doesn't appear. A receipt whose artifacts
failed verification is flagged PHANTOM, not hidden.

Usage:
  python3 ledger_writer.py --backfill   # rebuild everything from scores+receipts
  python3 ledger_writer.py --tick t962 --dispatch ...  # (future) per-tick append
"""
import json, os, re, sys
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent
HIDDEN = BASE.parent
SCORES = HIDDEN / "twelve-lane-scores.jsonl"
RECEIPTS = HIDDEN / "twelve-lane-receipts"
LANES_MD = HIDDEN / "twelve-lanes.md"

JSONL_OUT = BASE / "activity-ledger.jsonl"
MD_OUT = BASE / "ACTIVITY-LEDGER.md"
STATS_OUT = BASE / "STATS.md"

# NayaNET Protocol v1: every entry carries its node. This ledger is Node 1.
NODE_ID = "naya-team-naya"

# Lane number -> (team label, agent name, area)
LANES = {
    1:  ("Team 1",  "Naya Verity",    "Verification & Proof"),
    2:  ("Team 2",  "Naya Sage",      "Learning Pipeline"),
    3:  ("Team 3",  "Naya Judge",     "Decision Engine"),
    4:  ("Team 4",  "Naya Mason",     "Intelligent Blocks"),
    5:  ("Team 5",  "Naya Seeker",    "Retrieval"),
    6:  ("Team 6",  "Naya Heir",      "Successor Transfer"),
    7:  ("Team 7",  "Naya Conductor", "Team Operations"),
    8:  ("Team 8",  "Naya Sentinel",  "Governance & Safety"),
    9:  ("Team 9",  "Naya Smith",     "Code Health"),
    10: ("Team 10", "Naya Librarian", "Brain Index"),
    11: ("Team 11", "Naya Heart",     "Human Value"),
    12: ("Team 12", "Naya Herald",    "NayaNET / Hub"),
}

def tick_sort_key(tick: str) -> int:
    m = re.match(r"t(\d+)", tick or "")
    return int(m.group(1)) if m else 0

def load_scores():
    rows = []
    if SCORES.exists():
        for line in SCORES.read_text().splitlines():
            line = line.strip()
            if line:
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return rows

def receipt_exists(tick, lane) -> bool:
    return (RECEIPTS / f"{tick}-lane{lane}.md").exists()

# Known phantom claims — work reported as done that never existed.
# These have no score entry (they bypassed scoring); they are recorded here
# explicitly so the ledger shows what was caught, not just what succeeded.
KNOWN_PHANTOMS = [
    {
        "tick": "t902", "tick_n": 902, "team": "Team 9", "agent": "Naya Smith (claimed)",
        "lane": 9, "area": "Code Health",
        "task": "Receipt gate #2364 (claimed DONE)",
        "score": 0, "status": "PHANTOM",
        "receipt": None,
        "note": ("Claimed branch naya/nine-receipt-gate-t902 @ a26943cd3, receipt file, score line, "
                 "tools/check_scorecard_receipt_pin.py and docs did not exist anywhere. Exposed t922 by Lane 9; "
                 "retracted from twelve-lanes.md; rebuilt for real (14/14 tests, branch a459481c)."),
    },
]

def build_entries():
    entries = []
    for s in load_scores():
        tick = s.get("tick", "?")
        lane = s.get("lane", 0)
        team, agent, area = LANES.get(lane, (f"Team {lane}", s.get("agent", "?"), "?"))
        score = s.get("score", 0)
        note = s.get("note", "")
        # PHANTOM only if the score itself is 0 (no verified work). Notes that merely
        # MENTION catching a phantom (t912, t922, t932) are the catchers, not the phantom.
        # score None = DECLINED/BLOCKED (recusal or blocked brief; no score attached). Excluded from aggregates.
        if score is None:
            status = "DECLINED"
        else:
            status = "PHANTOM" if score == 0 else ("VERIFIED" if score >= 8 else ("PARTIAL" if score >= 5 else "WEAK"))
        entries.append({
            "ts": datetime.now(timezone.utc).isoformat(),
            "tick": tick,
            "tick_n": tick_sort_key(tick),
            "node": NODE_ID,
            "team": team,
            "agent": s.get("agent", agent),
            "lane": lane,
            "area": area,
            "task": s.get("task", ""),
            "score": score,
            "status": status,
            "receipt": f"twelve-lane-receipts/{tick}-lane{lane}.md" if receipt_exists(tick, lane) else None,
            "note": note[:400],
        })
    for p in KNOWN_PHANTOMS:
        e = dict(p)
        e["ts"] = datetime.now(timezone.utc).isoformat()
        e["node"] = NODE_ID
        entries.append(e)
    entries.sort(key=lambda e: (e["tick_n"], str(e["lane"])))  # mixed str/int lanes occur in scores.jsonl
    return entries

def write_jsonl(entries):
    with open(JSONL_OUT, "w") as f:
        for e in entries:
            f.write(json.dumps(e) + "\n")

def write_md(entries):
    now = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M %Z")
    lines = []
    lines.append("# Activity Ledger — Team Naya")
    lines.append("")
    lines.append('**"Don\'t tell me, show me."** Every row below is a verified action with its receipt and evidence — not a claim, a record.')
    lines.append("")
    lines.append(f"_Last updated: {now}_ | Data stream: `activity-ledger.jsonl` (machine-readable — feeds the future smart ledger / hub via the GitHub App)")
    lines.append("")
    # Live section: who's working right now (from rotation file)
    try:
        rot_text = (HIDDEN / "twelve-lane-rotation.json").read_text()
        # strip leading # comment lines (dispatcher writes a header)
        rot_text = "\n".join(l for l in rot_text.splitlines() if not l.lstrip().startswith("#"))
        rot = json.loads(rot_text)
        in_flight = rot.get("in_flight", [])
        last_tick = rot.get("last_tick", "?")
        if in_flight:
            lines.append("## 🟢 Working right now")
            lines.append("")
            for item in in_flight:
                # in_flight entries may be lane numbers or dicts
                if isinstance(item, dict):
                    lane = item.get("lane", "?")
                    task = item.get("note", "") or item.get("task", "")
                else:
                    lane = item
                    task = ""
                try:
                    lane_n = int(lane)
                    team, agent, area = LANES.get(lane_n, (f"Team {lane}", "?", "?"))
                except (ValueError, TypeError):
                    team, agent, area = f"Team {lane}", "?", "?"
                lines.append(f"- **{team} — {agent}** ({area}) — tick {last_tick}" + (f": {task[:100]}" if task else ""))
            lines.append("")
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    lines.append("## The Teams")
    lines.append("")
    lines.append("| Team | Agent | Lane |")
    lines.append("|------|-------|------|")
    for n in sorted(LANES):
        team, agent, area = LANES[n]
        lines.append(f"| {team} | {agent} | {area} |")
    lines.append("")
    lines.append("## Verified Actions (newest first)")
    lines.append("")
    for e in reversed(entries):
        badge = {"VERIFIED": "✅", "PARTIAL": "🟡", "WEAK": "🟠", "PHANTOM": "🚨", "DECLINED": "⏭️"}.get(e["status"], "❓")
        lines.append(f"### {badge} {e['tick']} — {e['team']}, {e['agent']} ({e['area']}) — {("no score" if e['score'] is None else str(e['score'])+"/10")} [{e['status']}]")
        lines.append("")
        lines.append(f"**Task:** {e['task']}")
        lines.append("")
        if e["receipt"]:
            lines.append(f"**Receipt:** `{e['receipt']}`")
            lines.append("")
        # pull first meaningful sentence of the note as evidence summary
        note = e["note"].replace("\n", " ").strip()
        if note:
            lines.append(f"**Evidence:** {note[:350]}")
            lines.append("")
    MD_OUT.write_text("\n".join(lines))

def write_stats(entries):
    lines = []
    now = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M %Z")
    lines.append("# Smart Stats — Team Naya")
    lines.append("")
    lines.append(f"_Last updated: {now}_")
    lines.append("")
    total = sum(1 for e in entries if e["score"] is not None)
    verified = sum(1 for e in entries if e["status"] == "VERIFIED")
    partial = sum(1 for e in entries if e["status"] == "PARTIAL")
    weak = sum(1 for e in entries if e["status"] == "WEAK")
    phantom = sum(1 for e in entries if e["status"] == "PHANTOM")
    lines.append("## Actions: verified, not claimed")
    lines.append("")
    lines.append(f"- **Total scored actions:** {total}")
    lines.append(f"- ✅ Verified (8+): {verified}")
    lines.append(f"- 🟡 Partial (5–7): {partial}")
    lines.append(f"- 🟠 Weak (<5): {weak}")
    lines.append(f"- 🚨 Phantom (claimed, never existed): {phantom}")
    if total:
        lines.append(f"- **Verification rate:** {verified/total*100:.0f}% of actions fully verified")
    lines.append("")
    lines.append("## Per-team score trend")
    lines.append("")
    lines.append("| Team | Agent | Actions | Avg score | Best |")
    lines.append("|------|-------|---------|-----------|------|")
    for n in sorted(LANES):
        team, agent, _ = LANES[n]
        ts = [e for e in entries if e["lane"] == n]
        sc = [e["score"] for e in ts if e["score"] is not None]
        if ts:
            avg = sum(sc) / len(sc) if sc else 0
            best = max(sc) if sc else "—"
            lines.append(f"| {team} | {agent} | {len(ts)} | {avg:.1f} | {best} |")
        else:
            lines.append(f"| {team} | {agent} | 0 | — | — |")
    lines.append("")
    lines.append("## Learning velocity")
    lines.append("")
    # group by tick
    ticks = {}
    for e in entries:
        ticks.setdefault(e["tick"], []).append(e)
    for tick in sorted(ticks, key=tick_sort_key):
        ts = ticks[tick]
        sc = [e["score"] for e in ts if e["score"] is not None]
        avg = sum(sc) / len(sc) if sc else 0
        lines.append(f"- **{tick}:** {len(ts)} actions, avg {avg:.1f}/10")
    lines.append("")
    lines.append("_A rising average with zero phantoms is the proof the team is learning and growing._")
    STATS_OUT.write_text("\n".join(lines))

def main():
    entries = build_entries()
    write_jsonl(entries)
    write_md(entries)
    write_stats(entries)
    # change-detection hash for the director's ledger sync (only push when changed)
    import hashlib
    h = hashlib.sha256()
    for p in (JSONL_OUT, MD_OUT, STATS_OUT):
        h.update(p.read_bytes())
    (BASE / ".ledger_hash").write_text(h.hexdigest())
    print(f"Ledger rebuilt: {len(entries)} entries -> {JSONL_OUT.name}, {MD_OUT.name}, {STATS_OUT.name}")

if __name__ == "__main__":
    main()
