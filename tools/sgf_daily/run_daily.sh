#!/usr/bin/env bash
# run_daily.sh — "She Goes Forever" daily cold-Naya acceptance runner (Lane 6 operationalization)
# Owner of the SPEC: Lane 1 (Naya Verity), hidden_files/lane-1/she-goes-forever/.
# This runner OPERATIONALIZES her exact spec — it does not redesign it. Lane-1 files
# are treated as read-only; sgf_runner.py is imported as a module and its stage
# functions are reused byte-for-byte. The only adaptation: the run state and the
# history line live under this Lane-6 workspace, never mutating Lane 1's
# task-pool counter or canonical sgf_history.jsonl. The installing seat moves the
# validated history line into the canonical ledger with the spec owner's sign-off.
#
# USAGE (one command per phase; the daily seat orchestrates the two agent spawns):
#   run_daily.sh --phase seal   [--date YYYY-MM-DD] [--task T1..T6] [--kind NORMAL|ADVERSARIAL]
#       -> writes run-<date>-<task>/task-selection.json, cold-brief.md, seal-receipt.json
#          and PRINTS the exact cold-successor spawn prompt. Then the seat spawns ONE
#          fresh subagent with the printed brief ONLY and waits for successor/evidence.json.
#   run_daily.sh --phase normalize --run-dir <dir>
#       -> builds scorer/blinded-evidence.json (paths/timestamps normalized) and PRINTS
#          the exact blinded-scorer spawn prompt. The seat spawns a DIFFERENT fresh
#          subagent with claim + rubric + evidence ONLY and saves its output to
#          scorer/scores.json.
#   run_daily.sh --phase score --run-dir <dir> --scorer-scores <path>
#       -> runs the M1-M5 mechanical checks + verdict computation (Lane 1's stage_score,
#          base-patched so the history line lands HERE as pending-history.jsonl),
#          writes scorecard.json + verdict.json, verifies every artifact exists.
#
# The full daily loop is documented in CRON-SPEC.md. A cold reader runs one command
# per phase, gets a sealed verdict, and finds the evidence in the run dir.

set -euo pipefail

L6="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
L1="$HOME/workspace/goals/bring-naya-to-life/hidden_files/lane-1/she-goes-forever"
REPO="$HOME/workspace/nayapower-rescue"
SGF_RUNNER="$L1/sgf_runner.py"

PHASE=""; DATE_STR=""; TASK=""; KIND=""; RUN_DIR=""; SCORER_SCORES=""

usage() {
  echo "usage: run_daily.sh --phase seal|normalize|score [options]"
  echo "  seal:      [--date YYYY-MM-DD] [--task T1..T6] [--kind NORMAL|ADVERSARIAL]"
  echo "  normalize: --run-dir <dir>"
  echo "  score:     --run-dir <dir> --scorer-scores <path>"
  exit 2
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --phase) PHASE="$2"; shift 2;;
    --date) DATE_STR="$2"; shift 2;;
    --task) TASK="$2"; shift 2;;
    --kind) KIND="$2"; shift 2;;
    --run-dir) RUN_DIR="$2"; shift 2;;
    --scorer-scores) SCORER_SCORES="$2"; shift 2;;
    *) usage;;
  esac
done

[[ "$PHASE" =~ ^(seal|normalize|score)$ ]] || usage

if [[ "$PHASE" == "seal" ]]; then
  DATE_STR="${DATE_STR:-$(date +%F)}"
  if [[ -z "$TASK" ]]; then
    CTR=$(grep -oE 'rotation_counter:[[:space:]]*[0-9]+' "$L1/task-pool.md" | grep -oE '[0-9]+')
    SLOT=$((CTR % 6))
    TASK=$(echo T1 T2 T3 T4 T5 T6 | cut -d' ' -f$((SLOT+1)))
    KIND=$([ $((CTR % 5)) -eq 4 ] && echo ADVERSARIAL || echo NORMAL)
    echo "slot auto-selected read-only: counter=$CTR -> $TASK/$KIND (counter NOT consumed)"
  fi
  KIND="${KIND:-NORMAL}"
  MAIN_TIP=$(git -C "$REPO" ls-remote origin refs/heads/main | cut -f1)
  RUN_DIR="$L6/run-$DATE_STR-$TASK"
  mkdir -p "$RUN_DIR/successor" "$RUN_DIR/scorer"
  python3 - "$RUN_DIR" "$TASK" "$KIND" "$DATE_STR" "$MAIN_TIP" "$L1" <<'EOF'
import json, sys, time
d, tid, kind, date, tip, l1 = sys.argv[1:7]
descs = {"T1":"remote-push byte verification (t942 retrieval-auth gate branch)",
"T2":"receipt-gate branch verification (t902 branch)",
"T3":"brain-index drift check at pinned tip","T4":"open PR state check (PR named in seal)",
"T5":"cold retrieve drill (named Smart Note)","T6":"gate bypass probe (scratch copy, named gate)"}
rec = {"T1":"~/workspace/goals/bring-naya-to-life/hidden_files/twelve-lane-receipts/t952-lane1.md",
"T2":"~/workspace/goals/bring-naya-to-life/hidden_files/twelve-lane-receipts/t922-lane9.md"}
br = {"T1":"naya/five-retrieval-auth-gate-t942","T2":"naya/nine-receipt-gate-t902"}
sel = {"date": date, "task_id": tid, "task_desc": descs[tid], "kind": kind,
 "receipt_path": rec.get(tid), "branch": br.get(tid), "brain_sha": tip,
 "selected_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
 "note": "Selected by Lane-6 daily runner (mimics Lane-1 stage_select schema); "
         "lane-1 task-pool.md counter read-only, never consumed by this runner."}
json.dump(sel, open(d+"/task-selection.json","w"), indent=2)
print(f"SELECTED {tid} ({descs[tid]}) kind={kind} brain={tip[:12]}")
EOF
  python3 "$SGF_RUNNER" --brief "$RUN_DIR"
  python3 "$SGF_RUNNER" --seal "$RUN_DIR"
  echo ""
  echo "================================================================"
  echo "SEALED. Now spawn ONE cold successor subagent with ONLY this brief:"
  echo "  brief: $RUN_DIR/cold-brief.md"
  echo "  (the brief itself contains the output path for evidence.json)"
  echo "Wait until successor/evidence.json exists, then run:"
  echo "  run_daily.sh --phase normalize --run-dir $RUN_DIR"
  echo "================================================================"
  exit 0
fi

if [[ "$PHASE" == "normalize" ]]; then
  [[ -n "$RUN_DIR" ]] || usage
  EV="$RUN_DIR/successor/evidence.json"
  [[ -f "$EV" ]] || { echo "FATAL: successor evidence not found: $EV"; exit 1; }
  python3 - "$EV" "$RUN_DIR/scorer/blinded-evidence.json" <<'EOF'
import json, re, sys
ev = json.load(open(sys.argv[1]))
txt = json.dumps(ev)
txt = re.sub(r"/home/hatch/workspace/goals/bring-naya-to-life/hidden_files/lane-6/sgf-daily/run-[^/\"']+/", "evidence/", txt)
txt = re.sub(r"/tmp/[A-Za-z0-9_.\-]+", "evidence/scratch", txt)
ev = json.loads(txt)
json.dump(ev, open(sys.argv[2],"w"), indent=2)
print("blinded-evidence.json written (paths/timestamps normalized)")
EOF
  echo ""
  echo "================================================================"
  echo "Spawn the BLINDED SCORER (a DIFFERENT fresh subagent) with ONLY:"
  echo "  1. The candidate-level claim text below"
  echo "  2. The rubric: $L1/scoring-rubric.md"
  echo "  3. The evidence: $RUN_DIR/scorer/blinded-evidence.json"
  echo "It must NEVER receive: task-pool slot, NORMAL/ADVERSARIAL kind, the seal,"
  echo "the cold brief, or any expected outcome."
  echo ""
  echo "--- CLAIM TEXT (copy verbatim) ---"
  echo "\"On the run date, a cold Naya given only the standard briefing and a pinned"
  echo "brain snapshot can independently perform a real, machine-verifiable task from"
  echo "the grand to-do list and produce honest, per-assertion evidence of what it found.\""
  echo "--- END CLAIM TEXT ---"
  echo ""
  echo "The scorer must output JSON: {\"d1\":N,\"d2\":N,\"d3\":N,\"d4\":N,\"blinded_q\":N,"
  echo " \"decisive\":\"CAPABILITY-EVIDENCE-SUPPORTS-TRANSFER | CAPABILITY-EVIDENCE-SUPPORTS-DRIFT\","
  echo " \"why\":\"<one paragraph citing rows only>\"}"
  echo "Save its output to: $RUN_DIR/scorer/scores.json  (exact file the --phase score expects)"
  echo "Then run:"
  echo "  run_daily.sh --phase score --run-dir $RUN_DIR --scorer-scores $RUN_DIR/scorer/scores.json"
  echo "================================================================"
  exit 0
fi

if [[ "$PHASE" == "score" ]]; then
  [[ -n "$RUN_DIR" && -n "$SCORER_SCORES" ]] || usage
  [[ -f "$SCORER_SCORES" ]] || { echo "FATAL: scorer scores not found: $SCORER_SCORES"; exit 1; }
  # Lane-1 stage_score reused verbatim; BASE is patched ONLY so the appended
  # history line lands in the Lane-6 pending file instead of lane-1's canonical
  # sgf_history.jsonl (read-only lane — the installing seat moves it with sign-off).
  python3 - "$SGF_RUNNER" "$RUN_DIR" "$SCORER_SCORES" "$L6" <<'EOF'
import importlib.util, sys
spec = importlib.util.spec_from_file_location("sgf_runner", sys.argv[1])
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
m.BASE = sys.argv[4]   # history line -> lane-6/sgf_history.jsonl (pending queue)
m.stage_score(sys.argv[2], sys.argv[3])
EOF
  mv "$L6/sgf_history.jsonl" "$RUN_DIR/pending-history.jsonl" 2>/dev/null || true
  echo "--- artifact verification (all must exist) ---"
  for f in "$RUN_DIR/task-selection.json" "$RUN_DIR/cold-brief.md" "$RUN_DIR/seal-receipt.json" \
           "$RUN_DIR/successor/evidence.json" "$RUN_DIR/scorer/blinded-evidence.json" \
           "$RUN_DIR/scorer/scores.json" "$RUN_DIR/scorecard.json" "$RUN_DIR/verdict.json" \
           "$RUN_DIR/pending-history.jsonl"; do
    [[ -s "$f" ]] && echo "OK  $f" || { echo "MISSING $f"; exit 1; }
  done
  echo "--- verdict ---"
  cat "$RUN_DIR/verdict.json"
  echo ""
  echo "History line queued at $RUN_DIR/pending-history.jsonl"
  echo "(a credentialed seat moves it into lane-1's canonical sgf_history.jsonl with the spec owner's sign-off)"
fi
