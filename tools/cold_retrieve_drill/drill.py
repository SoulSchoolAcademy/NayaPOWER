#!/usr/bin/env python3
"""Weekly cold-retrieve drill — prototype.

Usage:
  drill.py --bank drill_bank.json --repo /tmp/drill-worktree --week 41 --show
      Print this week's drill item (query + application question). The cold
      worker then runs the KNOW retrieval itself and answers.
  drill.py --bank drill_bank.json --grade --answer-file /tmp/answer.txt --week 41
      Grade a submitted answer against the week's expected phrases.

The drill is PASS only if the worker (a) retrieved the expected note
(verified separately from the worker's report) and (b) the answer contains
all expected phrases (case-insensitive substring match).

Append-only log: drill.py --log --record '{"week":41,...}' >> drill_log.jsonl
"""
import argparse, json, sys, datetime

def load_bank(path):
    b = json.load(open(path))
    items = [i for i in b["items"] if not i.get("retired")]
    return b, items

def pick(items, week):
    act = [i for i in items]
    if not act:
        # All bank items retired (or bank empty): fail LOUD, never silently
        # pick index 0 of nothing (was: cryptic ZeroDivisionError) and never
        # let a weekly cron report a pass it never earned.
        raise SystemExit("BANK_EMPTY")
    return act[week % len(act)]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bank", required=True)
    ap.add_argument("--week", type=int)
    ap.add_argument("--show", action="store_true")
    ap.add_argument("--grade", action="store_true")
    ap.add_argument("--answer-file")
    ap.add_argument("--log", action="store_true")
    ap.add_argument("--record")
    a = ap.parse_args()
    b, items = load_bank(a.bank)
    week = a.week if a.week is not None else datetime.date.today().isocalendar()[1]
    item = pick(items, week)
    if a.show:
        print(json.dumps({
            "week": week,
            "drill_id": item["id"],
            "expected_note_id": item["note_id"],
            "know_query": item["query"],
            "application_question": item["application_question"],
            "instructions": (
                "You are a cold session with zero context. (1) Run: "
                "python3 tools/smart_note_v2.py retrieve --query '<know_query>' "
                "from the repo root. Record the returned smart_note_id. "
                "(2) Read the retrieved note. (3) Answer the application "
                "question using ONLY the retrieved note. Write your answer to "
                "the answer file. Do not consult anything else."
            ),
        }, indent=2))
    elif a.grade:
        if not a.answer_file:
            sys.exit("GRADE_NEEDS_ANSWER_FILE")
        ans = open(a.answer_file).read().lower()
        missing = [p for p in item["expected_phrases"] if p.lower() not in ans]
        verdict = "PASS" if not missing else "FAIL"
        print(json.dumps({
            "week": week, "drill_id": item["id"],
            "expected_note_id": item["note_id"],
            "verdict": verdict,
            "missing_phrases": missing,
            "graded_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        }, indent=2))
        sys.exit(0 if verdict == "PASS" else 1)
    elif a.log:
        if not a.record:
            sys.exit("LOG_NEEDS_RECORD")
        rec = json.loads(a.record)
        rec.setdefault("logged_at", datetime.datetime.now(datetime.timezone.utc).isoformat())
        print(json.dumps(rec))
    else:
        ap.print_help()

if __name__ == "__main__":
    main()
