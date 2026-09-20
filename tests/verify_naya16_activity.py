#!/usr/bin/env python3
"""Machine gate for Naya 16 activity-record compliance."""
from __future__ import annotations
import argparse, pathlib, subprocess
ROOT=pathlib.Path(__file__).resolve().parents[1]
FEED=ROOT/"SUPERBRAIN"/"NAYA-ACTIVITY-FEED.md"
ACTIVITY_DIR="SUPERBRAIN/NAYA-ACTIVITY/"
REQUIRED=["### 01 — WHAT IS HAPPENING NOW?","### 02 — WHAT ARE WE ACTUALLY TRYING TO ACHIEVE?","### 03 — WHAT DOES THE EXISTING SYSTEM ACTUALLY DO?","### 04 — WHAT COULD I BE MISUNDERSTANDING?","### 05 — WHAT ARE THE CONSEQUENCES OF EACH OPTION?","### 06 — WHAT MATTERS MOST?","### 07 — WHAT SHOULD I DO?","### 08 — WHAT SHOULD I NOT DO?","### 09 — EXECUTE SURGICALLY","### 10 — VERIFY THE CHANGE","### 11 — TRACE REALITY END-TO-END","### 12 — PRODUCE RECEIPTS","### 13 — CHALLENGE MY OWN CONCLUSION","### 14 — REPORT CONFIDENCE","### 15 — DETERMINE WHAT MATTERS NEXT","### 16 — LEARN AND CHANGE THE SYSTEM","### PRESERVED","### RECEIPTS","### NEXT ACTION","### SUCCESSOR HANDOFF","**16-PROTOCOL CHECK:**"]
GOVERNED_PREFIXES=("NAYANET/","SUPERBRAIN/",".naya/","scripts/","supabase/","tests/",".github/workflows/")
def changed_files(before,after):
    cmd=["git","diff-tree","--no-commit-id","--name-only","-r",after] if not before or before=="0"*40 else ["git","diff","--name-only",before,after]
    return [x.strip() for x in subprocess.check_output(cmd,cwd=ROOT,text=True).splitlines() if x.strip()]
def has_complete_report(text): return all(item in text for item in REQUIRED)
def has_activity_record(files): return any(p=="SUPERBRAIN/NAYA-ACTIVITY-FEED.md" or p.startswith(ACTIVITY_DIR) for p in files)
def has_prior_activity_record(governed_files):
    if not governed_files:return False
    candidates=[]
    if FEED.exists():candidates.append(FEED)
    activity_root=ROOT/ACTIVITY_DIR
    if activity_root.exists():candidates.extend(sorted(activity_root.glob("*.md")))
    needles=set(governed_files)
    for path in governed_files:
        p=pathlib.PurePosixPath(path); needles.add(p.name); needles.add(p.stem)
    for candidate in candidates:
        try:text=candidate.read_text(encoding="utf-8")
        except OSError:continue
        if any(needle and needle in text for needle in needles):return True
    return False
def main():
    parser=argparse.ArgumentParser();parser.add_argument("--before",default="");parser.add_argument("--after",default="HEAD");parser.add_argument("--negative-test",action="store_true");args=parser.parse_args()
    if not FEED.exists() or not has_complete_report(FEED.read_text(encoding="utf-8")):
        print("NAYA16 FAIL: canonical activity feed is missing required report fields");return 1
    if args.negative_test:
        synthetic=["NAYANET/HUB/src/App.tsx"]
        if has_activity_record(synthetic) or has_prior_activity_record(synthetic):
            print("NAYA16 NEGATIVE TEST FAIL: synthetic governed change incorrectly accepted");return 1
        print("NAYA16 NEGATIVE TEST PASS: governed change without activity record is rejected");return 0
    files=changed_files(args.before,args.after); governed=[p for p in files if p.startswith(GOVERNED_PREFIXES)]; recorded=has_activity_record(files) or has_prior_activity_record(governed)
    if governed and not recorded:
        print("NAYA16 FAIL: governed execution changed files without an activity record")
        for p in governed:print(f" - {p}")
        return 1
    print("NAYA16 PASS");print(f"changed_files={len(files)}");print(f"governed_files={len(governed)}");print(f"activity_record_present={recorded}");return 0
if __name__=="__main__":raise SystemExit(main())