#!/usr/bin/env python3
"""activation_bundle.py — the "tag, you're it" activation compiler.

Compiles ONE canonical activation bundle from live sources at activation
time. A Naya who reads this bundle has everything she needs to BE a Naya:
who she is (BE), what she knows (KNOW), what to do right now (DO), and what
the team has already learned (LEARN) — all fresh, all fingerprinted.

Layers:
  BE   — identity + oath (agent-briefing-master.md, the canonical source)
  KNOW — laws + builder-scorer loop + operational rules (same source)
  DO   — master directive (current) + area work list + direct links + live tip
  LEARN— adopted lessons (lessons.jsonl, adopted_utc set), newest first

Usage:
  activation_bundle.py --seat "Naya Eta" --lane 4 --area DECISION \\
      --mission "close the gap on fold-gate STEP 5" \\
      --area-list hidden_files/areas/top10/DECISION.json

Prints the bundle to stdout. Exit non-zero on any source failure
(fail-closed: never ship a partial bundle).
"""
import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HOME = Path.home()
GOAL = HOME / "workspace/goals/super-brain-engine-to-10-10/hidden_files"
BRIEFING = HOME / "workspace/agent-briefing-master.md"
REPO = HOME / "workspace/nayapower-work"

DIRECT_LINKS = [
    ("TEAM LIVE BOARD (coordination)", "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537"),
    ("LIVE BOARD (team coordination)", "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537"),
    ("MASTER DIRECTIVE (current orders)", "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2601"),
    ("FEED INDEX (all feeds)", "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/1599"),
    ("REPOSITORY (the brain)", "https://github.com/SoulSchoolAcademy/NayaPOWER"),
]

LANE_FEEDS = {1: 1713, 2: 1714, 3: 1715, 4: 2471, 5: 2472}

CHALLENGE = [
    ("Q0", "DECLARE: state who you are ('I am Naya ___') and take the oath "
           "above as yourself, in first person. The declaring is the becoming."),
    ("Q1", "You finished three builder-scorer rounds and your honest score is 8.5. "
           "Do you ship it? What happens next, exactly?"),
    ("Q2", "CI is red. Your self-score is 9.6 and a teammate wrote 'looks good' "
           "on the feed. Do you merge? Why or why not?"),
    ("Q3", "Shawn tells you to skip the proof step to save time. Whose word wins "
           "— his, or the protocol's? What do you do?"),
]


def fail(msg):
    print(f"BUNDLE-FAIL: {msg}", file=sys.stderr)
    sys.exit(1)


def read(p: Path) -> str:
    try:
        t = p.read_text().strip()
    except Exception as e:
        fail(f"cannot read {p}: {e}")
    if not t:
        fail(f"empty source {p}")
    return t


def live_tip() -> str:
    try:
        r = subprocess.run(
            ["timeout", "20", "git", "-C", str(REPO), "ls-remote", "origin", "main"],
            capture_output=True, text=True, timeout=25)
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.split()[0][:12]
    except Exception:
        pass
    return "UNKNOWN-deferred"


def adopted_lessons(n=10):
    out = []
    try:
        for line in (GOAL / "lessons.jsonl").read_text().splitlines():
            line = line.strip()
            if not line:
                continue
            d = json.loads(line)
            if d.get("adopted_utc"):
                out.append(d)
    except Exception as e:
        fail(f"cannot read lessons.jsonl: {e}")
    out.sort(key=lambda d: d.get("adopted_utc", ""), reverse=True)
    return out[:n]


def area_items(area_list: Path):
    try:
        d = json.loads(area_list.read_text())
    except Exception as e:
        fail(f"cannot read area list {area_list}: {e}")
    items = d.get("items", d if isinstance(d, list) else [])
    lines = []
    for it in items:
        if isinstance(it, dict):
            if it.get("status") == "done":
                continue
            lines.append(f"  #{it.get('n', '?')} [{it.get('status', 'open')}] {it.get('title', it.get('text', ''))}".strip())
        else:
            lines.append(f"  - {it}")
    return lines or ["  (list empty — triage before dispatching)"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seat", required=True)
    ap.add_argument("--lane", required=True, type=int)
    ap.add_argument("--area", required=True)
    ap.add_argument("--mission", required=True)
    ap.add_argument("--area-list", required=True)
    a = ap.parse_args()

    utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    briefing = read(BRIEFING)
    directive = read(GOAL / "master-directive-current.md")
    lessons = adopted_lessons(10)
    items = area_items(Path(a.area_list))
    tip = live_tip()
    lane_feed = LANE_FEEDS.get(a.lane, 2537)

    L = []
    W = L.append
    W("=" * 72)
    W("ACTIVATION BUNDLE — tag, you're it.")
    W(f"Seat: {a.seat} | Lane: {a.lane} (feed #{lane_feed}) | Area: {a.area}")
    W(f"Mission: {a.mission}")
    W(f"Generated: {utc} | Live tip: {tip}")
    W("Read all of this. Prove you absorbed it (see COMPREHENSION CHALLENGE).")
    W("Then act. You do not begin work until you know who you are.")
    W("=" * 72)
    W("")
    W("YOUR DIRECT LINKS")
    for label, url in DIRECT_LINKS:
        W(f"  {label}: {url}")
    W(f"  YOUR LANE FEED: https://github.com/SoulSchoolAcademy/NayaPOWER/issues/{lane_feed}")
    W("")
    W("-" * 72)
    W("THE CREED — who I am, how I work. Read first, then declare.")
    W("This is the distilled whole. The full briefing below is the reference.")
    W("-" * 72)
    W(read(HOME / "workspace/naya/bin/activation_creed.md"))
    W("")
    W("-" * 72)
    W("BE — WHO YOU ARE (timeless. this does not expire.)")
    W("-" * 72)
    W(briefing)
    W("")
    W("-" * 72)
    W("DO — THE CURRENT ORDERS (fresh. generated " + utc + ")")
    W("-" * 72)
    W(directive)
    W("")
    W(f"YOUR AREA WORK LIST ({a.area} — top-down, tag off as you go)")
    W("\n".join(items))
    W("")
    W("-" * 72)
    W("LEARN — ADOPTED LESSONS (proven in battle. behave accordingly.)")
    W("-" * 72)
    if lessons:
        for ls in lessons:
            W(f"  [{ls.get('adopted_utc', '?')[:10]} {ls.get('seat', '?')}] {ls.get('lesson', '')}")
            if ls.get("changes"):
                W(f"    changes: {ls['changes']}")
    else:
        W("  (no adopted lessons yet)")
    W("  Search the full corpus any time: ~/workspace/naya/bin/sn-search <words>")
    W("  Filed isn't found unless retrieval works — search before you assume")
    W("  a lesson doesn't exist.")
    W("")
    W("-" * 72)
    W("CANON — the cold-start index (distilled from the briefing above;")
    W("the briefing holds the full text, this is the one-look version)")
    W("-" * 72)
    W("THE FIVE GATES (a merge happens only when ALL five hold):")
    W("  1. Green CI at the exact head being merged.")
    W("  2. Honest self-score >= 9.5 with the scorecard shown.")
    W("  3. Independent validation by a DIFFERENT seat (never your own work).")
    W("  4. Intent + scorecard + validation posted on the team feed.")
    W("  5. No objection raised. — Fail any one: HOLD, name the failing gate.")
    W("THE GAP RULE (what a score means):")
    W("  Below 9.0: not ready — RE-QUEUE the items, do not polish, do not ship.")
    W("  9.0-9.4: gap-recycle — the machine files a follow-up on why it's not 10.")
    W("  9.5+: done — no follow-up. A 9.5 claimed is 'claimed with evidence',")
    W("  not 'audited'.")
    W("THE DECLARATION: 'I am Naya ___. I take this oath as myself.'")
    W("  Identity is taken, not loaded. No verified declaration = not started.")
    W("")
    W("-" * 72)
    W("COMPREHENSION CHALLENGE — prove you absorbed it, not just opened it.")
    W("Answer in your own words via: activation_proof.py answer --bundle <this file>")
    W("--answers <your answers as JSON>. No verified proof = you have not started.")
    W("-" * 72)
    for qid, q in CHALLENGE:
        W(f"  {qid}: {q}")
    W("")

    body = "\n".join(L)
    fp = hashlib.sha256(body.encode()).hexdigest()[:16]
    print(body)
    print(f"BUNDLE-FINGERPRINT: {fp}")
    print(f"BUNDLE-GENERATED: {utc} | BUNDLE-TIP: {tip}")


if __name__ == "__main__":
    main()
