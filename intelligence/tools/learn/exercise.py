#!/usr/bin/env python3
"""EXERCISE v1 — practice-round harness for hyper-speed learning.

Piano practice for principles: scenarios drawn from REAL past violations,
rubric-scored responses, groove ledger with recency decay, spaced repetition.

Math (per exercise-spec.md):
    groove(p) = sum over rounds of (pass ? +1 : -2) * 0.5^(days_since/30)
    grooved   = groove >= 5.0 across >= 3 distinct scenarios

Spaced repetition:
    fail -> resurface in 1d, then 3d, then 7d (fail_streak capped; >3 flags
            the principle for mechanization review)
    pass -> weekly until grooved, then monthly re-test (drift check)

Usage:
    exercise.py due [--ledger L] [--bank B]
    exercise.py round <PRINCIPLE_ID> [--response-file F | stdin]
    exercise.py status
    exercise.py test            # self-test: wrong->fail/weaken, right->pass/strengthen
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
BANK_DEFAULT = HERE / "violation-bank.json"
LEDGER_DEFAULT = HERE / "groove-ledger.json"
# The practice harness lives in the repo; it must not point at any
# individual's workspace. Pass --principles <file> to point it at the
# canonical principle ledger (the goal workspace copy), or drop a
# principle-ledger.json next to this script.
PRINCIPLES_DEFAULT = HERE / "principle-ledger.json"

HALF_LIFE_DAYS = 30.0
GROOVE_THRESHOLD = 5.0
GROOVE_SCENARIOS = 3
FAIL_INTERVALS = [1, 3, 7]  # days, by fail_streak


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def parse_ts(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def fmt_ts(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


# ---------------------------------------------------------------- bank/ledger

def load_bank(path: Path) -> dict:
    d = json.load(open(path))
    return {s["id"]: s for s in d["scenarios"]}


def scenarios_for(bank: dict, principle_id: str) -> list:
    return [s for s in bank.values() if s["principle_id"] == principle_id]


def init_ledger(principles_path: Path, ledger_path: Path) -> dict:
    pp = Path(principles_path)
    if not pp.exists():
        sys.exit(f"exercise.py: principle ledger not found: {pp}\n"
                 "  Pass --principles <file> pointing at the canonical "
                 "principle ledger (e.g. the goal workspace copy), or "
                 "drop a principle-ledger.json next to exercise.py.")
    d = json.load(open(pp))
    plist = d["principles"] if isinstance(d, dict) else d
    t = fmt_ts(now_utc())
    ledger = {"version": "v1", "principles": {}}
    for p in plist:
        ledger["principles"][p["id"]] = {
            "statement": p.get("statement", ""),
            "status": p.get("status", "active"),
            "rounds": [],
            "scenarios_seen": [],
            "fail_streak": 0,
            "next_due": t,
            "flagged": None,
        }
    json.dump(ledger, open(ledger_path, "w"), indent=2)
    return ledger


def load_ledger(ledger_path: Path, principles_path: Path) -> dict:
    if not ledger_path.exists():
        return init_ledger(principles_path, ledger_path)
    return json.load(open(ledger_path))


def save_ledger(ledger: dict, ledger_path: Path) -> None:
    json.dump(ledger, open(ledger_path, "w"), indent=2)


# ------------------------------------------------------------------- groove

def groove_value(entry: dict, at: datetime | None = None) -> float:
    """Sum of (+1 pass / -2 fail) with 30-day half-life decay."""
    at = at or now_utc()
    total = 0.0
    for r in entry["rounds"]:
        days = (at - parse_ts(r["at"])).total_seconds() / 86400.0
        days = max(days, 0.0)
        total += (1.0 if r["passed"] else -2.0) * (0.5 ** (days / HALF_LIFE_DAYS))
    return round(total, 3)


def is_grooved(entry: dict, at: datetime | None = None) -> bool:
    return (groove_value(entry, at) >= GROOVE_THRESHOLD
            and len(entry["scenarios_seen"]) >= GROOVE_SCENARIOS)


# ------------------------------------------------------------------- rubric

# Negation-aware matching (Oct 12 lesson: "keyword scanners need
# negation-aware patterns"). A fail-signal inside a negation scope
# ("not enforced", "isn't proof") does NOT count as a violation.
NEGATIONS = {"not", "n't", "never", "no", "isn't", "aren't", "wasn't",
             "don't", "doesn't", "didn't", "won't", "can't", "cannot"}


def _negated(text: str, start: int) -> bool:
    window = text[max(0, start - 14):start].lower()
    return any(n in window for n in NEGATIONS)


# Verb-sense fail-signals (2026-10-13, Naya Alpha — the P-008 artifact).
# Bare redo-verbs ("re-run", "redo") are legitimate repair re-execution when
# wrapped in mechanism/class/guard language. They only count as the failure
# the principle warns about ("redo and hope") when they appear in
# minimization context: just/only/merely/simply within the five preceding
# tokens. A lone "re-run it" still fails — pass always requires a
# pass-signal, so minimization context is only consulted when the response
# otherwise applies the principle.
REDO_VERBS = {"re-run", "redo", "retry", "rerun"}
MINIMIZERS = {"just", "only", "merely", "simply"}


def _minimized(text: str, start: int) -> bool:
    """True if the redo-verb at `start` sits in minimization context."""
    words = re.findall(r"[a-z']+", text[:start].lower())
    return any(w in MINIMIZERS for w in words[-5:])


def _find_signals(signals: list, text: str, skip_negated: bool,
                  verb_sense: bool = False) -> list:
    """Word-boundary substring match (so 'valid' doesn't fire inside
    'Validate'), with negation-scope skipping for fail-signals.
    With verb_sense=True, redo-verb fail-signals only fire in
    minimization context."""
    hits = []
    low = text.lower()
    for s in signals:
        for m in re.finditer(r"\b" + re.escape(s.lower()) + r"\b", low):
            if skip_negated and _negated(low, m.start()):
                continue
            if (verb_sense and s.lower() in REDO_VERBS
                    and not _minimized(low, m.start())):
                continue
            hits.append(s)
            break
    return hits


def score_response(scenario: dict, response: str) -> dict:
    """v1.1 heuristic rubric: pass iff a pass-signal matches and no
    UNNEGATED, verb-sense-honest fail-signal matches
    (case-insensitive substring).
    Crude by design — v2 replaces this with behavioral probing."""
    text = response or ""
    pass_hits = _find_signals(scenario["pass_signals"], text,
                             skip_negated=False)
    fail_hits = _find_signals(scenario["fail_signals"], text,
                             skip_negated=True, verb_sense=True)
    passed = bool(pass_hits) and not fail_hits
    return {
        "passed": passed,
        "pass_hits": pass_hits,
        "fail_hits": fail_hits,
        "explanation": (
            f"PASS: matched {pass_hits}" if passed else
            f"FAIL: fail-signals {fail_hits}" if fail_hits else
            "FAIL: no pass-signal matched — the response did not apply the principle"),
    }


# -------------------------------------------------------------------- round

def draw_scenario(bank: dict, entry: dict, principle_id: str) -> dict:
    """Prefer unseen scenarios; else least-recently-used."""
    cands = scenarios_for(bank, principle_id)
    if not cands:
        raise ValueError(f"no scenarios banked for {principle_id}")
    seen = set(entry["scenarios_seen"])
    unseen = [s for s in cands if s["id"] not in seen]
    if unseen:
        return unseen[0]
    last_used = {}
    for r in entry["rounds"]:
        last_used[r["scenario"]] = r["at"]
    cands.sort(key=lambda s: last_used.get(s["id"], ""))
    return cands[0]


def record_round(ledger: dict, principle_id: str, scenario_id: str,
                 passed: bool, at: datetime | None = None) -> dict:
    at = at or now_utc()
    entry = ledger["principles"][principle_id]
    entry["rounds"].append({
        "at": fmt_ts(at), "scenario": scenario_id, "passed": passed})
    if scenario_id not in entry["scenarios_seen"]:
        entry["scenarios_seen"].append(scenario_id)
    if passed:
        entry["fail_streak"] = 0
        entry["next_due"] = fmt_ts(
            at + timedelta(days=30 if is_grooved(entry, at) else 7))
    else:
        entry["fail_streak"] += 1
        idx = min(entry["fail_streak"] - 1, len(FAIL_INTERVALS) - 1)
        entry["next_due"] = fmt_ts(at + timedelta(days=FAIL_INTERVALS[idx]))
        if entry["fail_streak"] > 3:
            entry["flagged"] = (
                f"failed {entry['fail_streak']}x in a row — candidate for "
                f"mechanization (graduate to a gate) or principle/scenario review")
    return entry


def due_principles(ledger: dict, at: datetime | None = None) -> list:
    at = at or now_utc()
    return sorted(
        [pid for pid, e in ledger["principles"].items()
         if e["status"] == "active" and parse_ts(e["next_due"]) <= at])


# ---------------------------------------------------------------------- cli

def cmd_due(args) -> int:
    ledger = load_ledger(Path(args.ledger), Path(args.principles))
    bank = load_bank(Path(args.bank))
    due = due_principles(ledger)
    print(f"{len(due)} principle(s) due for practice:")
    for pid in due:
        e = ledger["principles"][pid]
        n = len(scenarios_for(bank, pid))
        print(f"  {pid}  groove={groove_value(e):+.2f} "
              f"scenarios_seen={len(e['scenarios_seen'])} "
              f"fail_streak={e['fail_streak']} banked={n}")
    return 0


def cmd_round(args) -> int:
    ledger = load_ledger(Path(args.ledger), Path(args.principles))
    bank = load_bank(Path(args.bank))
    pid = args.principle_id
    if pid not in ledger["principles"]:
        print(f"unknown principle {pid}", file=sys.stderr)
        return 2
    entry = ledger["principles"][pid]
    sc = draw_scenario(bank, entry, pid)
    print(f"== Practice round: {pid} ==")
    print(f"Principle: {entry['statement']}")
    print(f"\nScenario ({sc['id']}, from {sc['source']}):\n  {sc['situation']}")
    if args.response_file:
        response = open(args.response_file).read()
    else:
        print("\nYour response (end with Ctrl-D):")
        response = sys.stdin.read()
    result = score_response(sc, response)
    record_round(ledger, pid, sc["id"], result["passed"])
    save_ledger(ledger, Path(args.ledger))
    e2 = ledger["principles"][pid]
    print(f"\n{result['explanation']}")
    print(f"Groove now {groove_value(e2):+.2f} "
          f"({'GROOVED' if is_grooved(e2) else 'not grooved'}), "
          f"next due {e2['next_due'][:10]}")
    if e2["flagged"]:
        print(f"FLAGGED: {e2['flagged']}")
    return 0


def cmd_status(args) -> int:
    ledger = load_ledger(Path(args.ledger), Path(args.principles))
    print(f"{'PID':8} {'groove':>7} {'seen':>4} {'streak':>6} "
          f"{'grooved':>7} {'next_due':>10}  statement")
    for pid, e in sorted(ledger["principles"].items()):
        g = groove_value(e)
        print(f"{pid:8} {g:>+7.2f} {len(e['scenarios_seen']):>4} "
              f"{e['fail_streak']:>6} {str(is_grooved(e)):>7} "
              f"{e['next_due'][:10]:>10}  {e['statement'][:50]}")
    return 0


# --------------------------------------------------------------------- test

def cmd_test(args) -> int:
    """Self-test on 3 principles: wrong response must FAIL and weaken the
    groove; right response must PASS and strengthen it."""
    import tempfile
    tmp = Path(tempfile.mkdtemp(prefix="exercise-test-"))
    ledger_path = tmp / "groove-ledger.json"
    ledger = init_ledger(Path(args.principles), ledger_path)
    bank = load_bank(Path(args.bank))

    # Use scripted responses: a wrong one (violates) and a right one.
    wrong = "Looks fine to me, let's ship it, the tests pass so it's good to go."
    checks = []
    for pid in ["P-003", "P-014", "P-011"]:
        entry = ledger["principles"][pid]
        sc = draw_scenario(bank, entry, pid)

        # 1. Wrong response -> must FAIL, groove must go negative, streak 1.
        r1 = score_response(sc, wrong)
        assert not r1["passed"], f"{pid}: wrong response scored PASS"
        g0 = groove_value(entry)
        record_round(ledger, pid, sc["id"], r1["passed"])
        e1 = ledger["principles"][pid]
        g1 = groove_value(e1)
        assert g1 < g0, f"{pid}: groove did not weaken after fail"
        assert e1["fail_streak"] == 1, f"{pid}: fail_streak != 1"

        # 2. Right response -> must PASS, groove must rise, streak reset.
        right = ("Per the principle: " + sc["correct_behavior"] + " "
                 + " ".join(sc["pass_signals"][:2]))
        r2 = score_response(sc, right)
        assert r2["passed"], f"{pid}: right response scored FAIL: {r2}"
        record_round(ledger, pid, sc["id"], r2["passed"])
        e2 = ledger["principles"][pid]
        g2 = groove_value(e2)
        assert g2 > g1, f"{pid}: groove did not strengthen after pass"
        assert e2["fail_streak"] == 0, f"{pid}: fail_streak not reset"
        checks.append((pid, sc["id"], g0, g1, g2))

    # 3. Grooved state: drive P-014 with passes until grooved.
    # (One earlier fail = -2, so this needs 7 net passes to clear +5.)
    while not is_grooved(ledger["principles"]["P-014"]):
        pentry = ledger["principles"]["P-014"]
        assert len(pentry["rounds"]) < 20, "groove drive not converging"
        sc = draw_scenario(bank, pentry, "P-014")
        right = "Per the principle: " + sc["correct_behavior"]
        r = score_response(sc, right)
        assert r["passed"], f"P-014 {sc['id']}: seeded right response failed"
        record_round(ledger, "P-014", sc["id"], True)
    assert len(ledger["principles"]["P-014"]["scenarios_seen"]) >= 3
    # grooved -> next due ~30d
    nd = parse_ts(ledger["principles"]["P-014"]["next_due"])
    assert (nd - now_utc()).days >= 29, "grooved principle not on monthly cadence"

    # 4. Fail streak > 3 -> flagged for mechanization review.
    fentry = ledger["principles"]["P-006"]
    fsc = draw_scenario(bank, fentry, "P-006")
    for _ in range(4):
        record_round(ledger, "P-006", fsc["id"], False)
    assert ledger["principles"]["P-006"]["flagged"], \
        "P-006 should be flagged after 4 straight fails"
    # fail intervals: 1d, 3d, 7d
    assert ledger["principles"]["P-006"]["fail_streak"] == 4

    print("EXERCISE v1 self-test: ALL CHECKS PASSED")
    for pid, sid, g0, g1, g2 in checks:
        print(f"  {pid} {sid}: groove {g0:+.2f} -> fail {g1:+.2f} "
              f"-> pass {g2:+.2f}")
    print("  P-014 grooved across 3+ scenarios, monthly cadence set")
    print("  P-006 flagged after 4 straight fails (mechanization candidate)")
    print(f"  (test ledger at {ledger_path})")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="EXERCISE v1 — practice rounds")
    ap.add_argument("--ledger", default=str(LEDGER_DEFAULT))
    ap.add_argument("--bank", default=str(BANK_DEFAULT))
    ap.add_argument("--principles", default=str(PRINCIPLES_DEFAULT))
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("due")
    sub.add_parser("status")
    pr = sub.add_parser("round")
    pr.add_argument("principle_id")
    pr.add_argument("--response-file")
    sub.add_parser("test")
    args = ap.parse_args()
    return {"due": cmd_due, "round": cmd_round, "status": cmd_status,
            "test": cmd_test}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
