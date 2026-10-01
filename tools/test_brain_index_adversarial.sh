#!/usr/bin/env bash
# Adversarial self-test for tools/regenerate_brain_index.py.
#
# Proves the generator FAILS LOUDLY (exit 2) on the two defect classes it
# guards, instead of faithfully regenerating around the lie:
#   (a) a dangling path pointer in the index layer
#   (b) a skewed per-domain file count
# plus a positive control proving the clean tree passes.
#
# Each case runs in a scratch clone under a temp dir; nothing here touches
# the real working tree. The script prints the generator's captured output
# for each case as evidence and exits nonzero if any expectation is unmet.
#
# Usage: bash tools/test_brain_index_adversarial.sh

set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GEN="$SCRIPT_DIR/regenerate_brain_index.py"
REPO="$SCRIPT_DIR/.."   # the repo this script lives in

T="$(mktemp -d /tmp/brain-index-adversarial-XXXXXX)"
trap 'rm -rf "$T"' EXIT

PASS=0
FAIL=0

report() { # $1=name $2=ok(1/0) $3=detail
  if [ "$2" = 1 ]; then PASS=$((PASS+1)); echo "PASS: $1"; else FAIL=$((FAIL+1)); echo "FAIL: $1"; fi
  [ -n "${3:-}" ] && echo "$3"
  echo "---"
}

# ---------------------------------------------------------------- positive control
echo "### CASE 0: positive control — clean tree must pass"
git clone -q "$REPO" "$T/clean" 2>/dev/null
out="$(python3 "$GEN" --root "$T/clean" --check 2>&1)"; code=$?
if [ $code -eq 0 ]; then report "clean tree --check exits 0" 1 "$out"; else report "clean tree --check exits 0" 0 "exit=$code :: $out"; fi

# ------------------------------------------------- case A: dangling pointer
echo "### CASE A: dangling pointer in MASTER-INDEX.json must fail exit 2"
git clone -q "$REPO" "$T/a" 2>/dev/null
python3 - "$T/a" <<'EOF'
import json, sys
p = sys.argv[1] + "/BRAIN/04-INTELLIGENCE/MASTER-INDEX.json"
d = json.loads(open(p).read())
d["object_contract"] = "BRAIN/04-INTELLIGENCE/0001-DOES-NOT-EXIST-V1.md"
open(p, "w").write(json.dumps(d))
EOF
git -C "$T/a" -c user.name=adv -c user.email=adv@local add -A
git -C "$T/a" -c user.name=adv -c user.email=adv@local commit -qm "sabotage: dangling object_contract pointer"
out="$(python3 "$GEN" --root "$T/a" 2>&1)"; code=$?
echo "$out"
if [ $code -eq 2 ] \
   && echo "$out" | grep -q "MASTER-INDEX.json" \
   && echo "$out" | grep -q "object_contract" \
   && echo "$out" | grep -q "0001-DOES-NOT-EXIST-V1.md"; then
  report "dangling pointer fails exit 2 naming file+field+target" 1 ""
else
  report "dangling pointer fails exit 2 naming file+field+target" 0 "exit=$code (expected 2)"
fi

# --check mode must also catch it
out="$(python3 "$GEN" --root "$T/a" --check 2>&1)"; code=$?
if [ $code -eq 2 ] && echo "$out" | grep -q "dangling pointer"; then
  report "dangling pointer fails --check with exit 2" 1 ""
else
  report "dangling pointer fails --check with exit 2" 0 "exit=$code (expected 2)"
fi

# ------------------------------------------------- case B: count skew
echo "### CASE B: skewed domain count must fail exit 2"
git clone -q "$REPO" "$T/b" 2>/dev/null
git -C "$T/b" -c user.name=adv -c user.email=adv@local rm -q "BRAIN/99-ARCHIVE/README.md"
git -C "$T/b" -c user.name=adv -c user.email=adv@local commit -qm "sabotage: delete 99-ARCHIVE README (count skew)"
out="$(python3 "$GEN" --root "$T/b" 2>&1)"; code=$?
echo "$out"
if [ $code -eq 2 ] && echo "$out" | grep -q "domain counts do not match"; then
  report "count skew fails exit 2 with count message" 1 ""
else
  report "count skew fails exit 2 with count message" 0 "exit=$code (expected 2)"
fi

# --------------------------------- case C: undeclared pointer (backstop)
echo "### CASE C: undeclared new pointer field must fail via backstop scan"
git clone -q "$REPO" "$T/c" 2>/dev/null
python3 - "$T/c" <<'EOF'
import json, sys
p = sys.argv[1] + "/BRAIN/NAYAPOWER-BRAIN-INDEX.json"
d = json.loads(open(p).read())
d["some_future_pointer"] = "BRAIN/12-ENGINEERING/9999-NOT-HERE-V1.md"
open(p, "w").write(json.dumps(d, indent=2))
EOF
git -C "$T/c" -c user.name=adv -c user.email=adv@local add -A
git -C "$T/c" -c user.name=adv -c user.email=adv@local commit -qm "sabotage: undeclared dangling pointer"
out="$(python3 "$GEN" --root "$T/c" 2>&1)"; code=$?
echo "$out"
if [ $code -eq 2 ] \
   && echo "$out" | grep -q "backstop scan" \
   && echo "$out" | grep -q "some_future_pointer" \
   && echo "$out" | grep -q "9999-NOT-HERE-V1.md"; then
  report "undeclared pointer fails exit 2 via backstop scan" 1 ""
else
  report "undeclared pointer fails exit 2 via backstop scan" 0 "exit=$code (expected 2)"
fi

# -------------------------------- case D: governed report append is allowed
echo "### CASE D: append-only intelligence-report growth must remain valid"
git clone -q "$REPO" "$T/d" 2>/dev/null
mkdir -p "$T/d/BRAIN/05-MEMORY/INTELLIGENCE-REPORTS/DAILY/2099/01/01"
cat > "$T/d/BRAIN/05-MEMORY/INTELLIGENCE-REPORTS/DAILY/2099/01/01/IB-DIR-TEST-20990101-001.md" <<'EOF'
# Test Daily Intelligence Report
Object: governed append-only report fixture.
EOF
git -C "$T/d" -c user.name=adv -c user.email=adv@local add -A
git -C "$T/d" -c user.name=adv -c user.email=adv@local commit -qm "test: append governed daily intelligence report"
out="$(python3 "$GEN" --root "$T/d" 2>&1)"; code=$?
echo "$out"
if [ $code -eq 0 ]; then
  git -C "$T/d" -c user.name=adv -c user.email=adv@local add BRAIN/REAL-TREE.json BRAIN/REAL-TREE.md BRAIN/NAYAPOWER-BRAIN-INDEX.json
  git -C "$T/d" -c user.name=adv -c user.email=adv@local commit -qm "test: regenerate report-aware indexes"
  out2="$(python3 "$GEN" --root "$T/d" --check 2>&1)"; code2=$?
  if [ $code2 -eq 0 ]; then
    report "governed report append regenerates and --check passes" 1 "$out2"
  else
    report "governed report append regenerates and --check passes" 0 "check exit=$code2 :: $out2"
  fi
else
  report "governed report append regenerates and --check passes" 0 "regen exit=$code :: $out"
fi

echo "=== RESULT: $PASS passed, $FAIL failed ==="
[ $FAIL -eq 0 ]
