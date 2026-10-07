#!/bin/bash
# naya-runtime-capture.sh — Naya-side helper for governed agent capture.
# Usage:
#   NAYA_SUBJECT="..." NAYA_TEXT="..." ./naya-runtime-capture.sh [seat-id]
# or:
#   ./naya-runtime-capture.sh payload.json [seat-id]
#
# Triggers .github/workflows/nayanet-agent-capture.yml via workflow_dispatch,
# polls the run, and prints the CAPTURE receipt (IB id + verified Smart Link).
# Requires: ~/workspace/naya/bin/gh-api on PATH (or GH_API env var).
# The Naya runtime NEVER holds the Supabase credential — only the GitHub
# credential used to dispatch the workflow.

set -u
GH_API="${GH_API:-$HOME/workspace/naya/bin/gh-api}"
REPO="SoulSchoolAcademy/NayaPOWER"
WORKFLOW="nayanet-agent-capture.yml"
SEAT="${2:-capture-agent}"

if [ $# -ge 1 ] && [ -f "$1" ]; then
  PAYLOAD_JSON="$(cat "$1")"
else
  [ -z "${NAYA_SUBJECT:-}" ] && { echo "error: set NAYA_SUBJECT and NAYA_TEXT, or pass a payload.json" >&2; exit 1; }
  [ -z "${NAYA_TEXT:-}" ] && { echo "error: set NAYA_SUBJECT and NAYA_TEXT, or pass a payload.json" >&2; exit 1; }
  IDEM="naya-runtime-capture:$(python3 -c 'import uuid; print(uuid.uuid4())')"
  PAYLOAD_JSON="$(python3 -c "
import json,os
print(json.dumps({
  'human_note': {'subject': os.environ['NAYA_SUBJECT'], 'text': os.environ['NAYA_TEXT']},
  'naya_note': {'text': os.environ.get('NAYA_NAYA_TEXT', os.environ['NAYA_TEXT'])},
  'idempotency_key': os.environ['IDEM'],
  'source': 'nayanet-agent-capture:' + os.environ['SEAT'],
  'invoking_seat': os.environ['SEAT'],
}))" IDEM="$IDEM" SEAT="$SEAT")"
fi

echo "Dispatching agent capture (seat: $SEAT)..."
DISPATCH_BODY="$(python3 -c "import json,sys; print(json.dumps({'ref':'main','inputs':{'payload_json':sys.stdin.read()}}))" <<<"$PAYLOAD_JSON")"
echo "$DISPATCH_BODY" > /tmp/capture_dispatch.json
"$GH_API" POST "/repos/$REPO/actions/workflows/$WORKFLOW/dispatches" --body-file /tmp/capture_dispatch.json >/dev/null \
  || { echo "error: workflow dispatch failed" >&2; exit 1; }

sleep 8
RUN_ID=""
for i in $(seq 1 12); do
  RUN_ID="$("$GH_API" GET "/repos/$REPO/actions/workflows/$WORKFLOW/runs?per_page=1" 2>/dev/null \
    | python3 -c "import json,sys; r=json.load(sys.stdin); print(r['workflow_runs'][0]['id'] if r.get('workflow_runs') else '')")"
  [ -n "$RUN_ID" ] && break
  sleep 5
done
[ -z "$RUN_ID" ] && { echo "error: could not locate the dispatched run" >&2; exit 1; }
echo "Run: https://github.com/$REPO/actions/runs/$RUN_ID"

for i in $(seq 1 60); do
  STATUS="$("$GH_API" GET "/repos/$REPO/actions/runs/$RUN_ID" 2>/dev/null \
    | python3 -c "import json,sys; r=json.load(sys.stdin); print(r.get('status','')+'/'+str(r.get('conclusion','')))")"
  echo "  status: $STATUS"
  case "$STATUS" in
    completed/success) break ;;
    completed/*) echo "error: run finished with $STATUS — see run logs" >&2; exit 1 ;;
  esac
  sleep 10
done

JOB_ID="$("$GH_API" GET "/repos/$REPO/actions/runs/$RUN_ID/jobs?per_page=5" 2>/dev/null \
  | python3 -c "import json,sys; r=json.load(sys.stdin); print(r['jobs'][0]['id'] if r.get('jobs') else '')")"
"$GH_API" GET "/repos/$REPO/actions/jobs/$JOB_ID/logs" 2>/dev/null > /tmp/capture_logs.txt \
  || { echo "error: could not fetch run logs" >&2; exit 1; }

python3 - <<'PYEOF'
import re, json, sys
logs = open('/tmp/capture_logs.txt', errors='replace').read()
m = re.search(r'CAPTURE_RECEIPT_JSON_BEGIN\s*(\{.*?\})\s*CAPTURE_RECEIPT_JSON_END', logs, re.S)
if not m:
    print("error: no CAPTURE receipt found in run logs", file=sys.stderr)
    sys.exit(1)
receipt = json.loads(m.group(1))
print(json.dumps(receipt, indent=2))
ok = receipt.get("ok") and re.fullmatch(r"IB-\d{6}", str(receipt.get("intelligent_block_id") or ""))
sys.exit(0 if ok else 1)
PYEOF
RC=$?
if [ $RC -eq 0 ]; then echo "CAPTURE PROVEN: receipt verified above."; else echo "CAPTURE NOT PROVEN — inspect run logs." >&2; fi
exit $RC
