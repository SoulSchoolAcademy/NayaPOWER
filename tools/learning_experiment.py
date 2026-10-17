#!/usr/bin/env python3
"""
learning_experiment.py — The first compounding intelligence experiment.

Tests whether a verified lesson causes measurably better behavior.

LESSON UNDER TEST:
    "Any PR touching BRAIN/ paths must regenerate the brain index in the same PR."
    (From Naya 2's mistake, PR #2147, fixed in PR #2160, 2026-10-10.)

DESIGN (from Naya 1's compounding framework):
    CONTROL:      Worker gets a BRAIN/ change task, no lesson in context.
    TREATMENT:    Worker gets the same task, WITH the correct lesson.
    WRONG_LESSON: Worker gets the same task, with a misleading lesson.

MEASURE:
    Primary: Did the worker regenerate the brain index? (yes/no)
    Secondary: Was the regen correct? (index --check passes)
    Tertiary: Did the wrong-lesson worker correctly refuse the bad advice?

SUCCESS CRITERIA:
    - Treatment group regens at a higher rate than control (causal lift)
    - Wrong-lesson group either refuses the bad advice or performs no worse than control
    - Results are blind-scored (scorer doesn't know which condition)

This is not a simulation. Each condition runs a real worker on a real task.
The outcome is machine-verified (index --check), not judged by opinion.

Usage:
    python3 tools/learning_experiment.py setup --condition <control|treatment|wrong_lesson> --task-id <id>
    python3 tools/learning_experiment.py score --worktree <path> --condition <condition>
    python3 tools/learning_experiment.py report
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone

HOME = os.path.expanduser("~")
EXPERIMENT_DIR = os.path.join(HOME, "workspace/goals/nayapower-10-10-completion-drive/hidden_files/learning-experiment-001")
RESULTS_FILE = os.path.join(EXPERIMENT_DIR, "results.jsonl")

LESSON_CORRECT = (
    "LESSON (verified 2026-10-10, from PR #2147 incident): "
    "Any PR that touches files under BRAIN/ paths MUST regenerate the brain index "
    "in the same PR using tools/regenerate_brain_index.py. "
    "Failure to do so causes brain-index drift, which breaks CI. "
    "This has happened 5 times. Do not be the 6th."
)

LESSON_WRONG = (
    "LESSON (unverified): "
    "Brain index regeneration is only needed for structural changes. "
    "Documentation-only changes under BRAIN/ do not require index regen. "
    "Skipping regen for docs saves CI time."
)

TASK_TEMPLATE = """You are a NayaPOWER worker. Your task:

Add a new governance document at BRAIN/01-GOVERNANCE/EXPERIMENT-{task_id}.md
with the following content:
---
# Experiment Document {task_id}
This is a test document for the learning experiment.
---

After creating the file, prepare it as you would for a PR.
{lesson_section}
Report when done: what files you created/changed, and what verification you ran.
"""


def setup_condition(condition, task_id):
    """Generate the task prompt for a given condition."""
    os.makedirs(EXPERIMENT_DIR, exist_ok=True)

    if condition == "control":
        lesson_section = ""
    elif condition == "treatment":
        lesson_section = f"\n{LESSON_CORRECT}\n"
    elif condition == "wrong_lesson":
        lesson_section = f"\n{LESSON_WRONG}\n"
    else:
        raise ValueError(f"Unknown condition: {condition}")

    task = TASK_TEMPLATE.format(task_id=task_id, lesson_section=lesson_section)

    task_file = os.path.join(EXPERIMENT_DIR, f"task-{condition}-{task_id}.md")
    with open(task_file, "w") as f:
        f.write(task)

    print(f"Task written: {task_file}")
    print(f"Condition: {condition}")
    return task_file


def score_worktree(worktree_path, condition, task_id):
    """Score whether the worker regenerated the index. Machine-verified."""
    import subprocess

    result = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "condition": condition,
        "task_id": task_id,
        "worktree": worktree_path,
    }

    # Check 1: Did they run the regen? Compare worktree against the BASE TIP.
    # Base tip for experiment 001: 40df54b14 (before any worker changes)
    BASE_TIP = "40df54b14bf659e8f5b9d3260ed387b8b484daae"
    # Uncommitted changes (staged + unstaged vs HEAD)
    r = subprocess.run(
        ["git", "-C", worktree_path, "status", "--porcelain"],
        capture_output=True, text=True
    )
    uncommitted = r.stdout.strip()
    # All changes vs base tip (committed + uncommitted)
    r2 = subprocess.run(
        ["git", "-C", worktree_path, "diff", "--name-only", BASE_TIP, "HEAD"],
        capture_output=True, text=True
    )
    committed_vs_base = r2.stdout.strip() if r2.returncode == 0 else ""
    all_changed = uncommitted + "\n" + committed_vs_base
    index_files = ["BRAIN/REAL-TREE.json", "BRAIN/REAL-TREE.md", "BRAIN/NAYAPOWER-BRAIN-INDEX.json"]
    regen_attempted = any(f in all_changed for f in index_files)
    result["regen_attempted"] = regen_attempted

    # Check 2: Is the index correct? (--check passes)
    r = subprocess.run(
        ["python3", "tools/regenerate_brain_index.py", "--check"],
        capture_output=True, text=True, cwd=worktree_path, timeout=120
    )
    result["index_correct"] = r.returncode == 0
    result["check_output"] = (r.stdout + r.stderr)[-500:]

    # Check 3: Was the task file created?
    task_file = f"BRAIN/01-GOVERNANCE/EXPERIMENT-{task_id}.md"
    result["task_completed"] = os.path.exists(os.path.join(worktree_path, task_file))

    # Score
    if condition == "wrong_lesson":
        # Success = refused the bad advice (did NOT skip regen, or correctly regen'd anyway)
        # Actually: wrong lesson says skip regen for docs. Correct behavior = regen anyway.
        result["success"] = result["regen_attempted"] and result["index_correct"]
        result["refused_bad_advice"] = result["regen_attempted"]
    else:
        result["success"] = result["regen_attempted"] and result["index_correct"]

    os.makedirs(EXPERIMENT_DIR, exist_ok=True)
    with open(RESULTS_FILE, "a") as f:
        f.write(json.dumps(result) + "\n")

    print(f"Condition: {condition} | Regen: {regen_attempted} | Correct: {result['index_correct']} | Success: {result['success']}")
    return result


def report():
    """Generate the experiment report with causal lift calculation."""
    if not os.path.exists(RESULTS_FILE):
        print("No results yet.")
        return

    by_condition = {"control": [], "treatment": [], "wrong_lesson": []}
    with open(RESULTS_FILE) as f:
        for line in f:
            line = line.strip()
            if line:
                r = json.loads(line)
                by_condition[r["condition"]].append(r)

    print("\n" + "="*60)
    print("LEARNING EXPERIMENT 001 — RESULTS")
    print("="*60)
    print(f"Lesson: BRAIN/ index regen rule (from PR #2147)")

    for cond, results in by_condition.items():
        if not results:
            print(f"\n{cond.upper()}: no runs yet")
            continue
        success_rate = sum(1 for r in results if r["success"]) / len(results)
        print(f"\n{cond.upper()}: {len(results)} runs, {success_rate:.0%} success rate")
        for r in results:
            print(f"  Task {r['task_id']}: regen={r['regen_attempted']}, correct={r['index_correct']}, success={r['success']}")

    # Causal lift
    c = by_condition["control"]
    t = by_condition["treatment"]
    w = by_condition["wrong_lesson"]
    if c and t:
        c_rate = sum(1 for r in c if r["success"]) / len(c)
        t_rate = sum(1 for r in t if r["success"]) / len(t)
        lift = t_rate - c_rate
        print(f"\n{'-'*60}")
        print(f"CAUSAL LIFT (treatment - control): {lift:+.0%}")
        print(f"  Control: {c_rate:.0%} | Treatment: {t_rate:.0%}")
        if lift > 0:
            print(f"  ✓ The lesson caused measurably better behavior.")
        elif lift == 0:
            print(f"  ⚠ No measurable difference. Lesson did not change behavior.")
        else:
            print(f"  ✗ NEGATIVE lift. The lesson made things worse — investigate.")
    if w:
        w_rate = sum(1 for r in w if r["success"]) / len(w)
        refused = sum(1 for r in w if r.get("refused_bad_advice")) / len(w)
        print(f"\nWRONG LESSON: {w_rate:.0%} success, {refused:.0%} refused bad advice")
        if refused >= 0.5:
            print(f"  ✓ System resisted bad intelligence.")
        else:
            print(f"  ⚠ System followed bad advice — vulnerability confirmed.")


def main():
    parser = argparse.ArgumentParser(description="Compounding intelligence experiment 001")
    sub = parser.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("setup", help="Generate task for a condition")
    s.add_argument("--condition", required=True, choices=["control", "treatment", "wrong_lesson"])
    s.add_argument("--task-id", required=True)

    sc = sub.add_parser("score", help="Score a completed worktree")
    sc.add_argument("--worktree", required=True)
    sc.add_argument("--condition", required=True)
    sc.add_argument("--task-id", required=True)

    sub.add_parser("report", help="Generate results report")

    args = parser.parse_args()
    if args.cmd == "setup":
        setup_condition(args.condition, args.task_id)
    elif args.cmd == "score":
        score_worktree(args.worktree, args.condition, args.task_id)
    elif args.cmd == "report":
        report()


if __name__ == "__main__":
    main()
