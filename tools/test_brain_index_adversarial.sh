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
# Exit codes: 0 = all cases pass; 1 = at least one case failed (the generator
# verdict); 3 = harness/environment failure (no scratch root fits, or a
# scratch clone could not be created) — never a generator verdict. A dead
# clone must fail LOUDLY and abort the run; it must never surface as
# misleading per-case FAILs that blame the generator.
#
# Usage: bash tools/test_brain_index_adversarial.sh
# Env: BRAIN_ADVERSARIAL_TMPDIR names the preferred scratch base. It is used
#   only when it actually fits the 5 clones (see below); otherwise the
#   harness searches for a disk-backed root automatically.

set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GEN="$SCRIPT_DIR/regenerate_brain_index.py"
REPO="$SCRIPT_DIR/.."   # the repo this script lives in

# --- scratch root: it must actually fit the 5 clones ---
# Root-caused 2026-10-05: the 5 scratch clones (~117MB each, growing with the
# repo) exceed a 512MB /tmp tmpfs even when /tmp starts empty, so a plain
# "${BRAIN_ADVERSARIAL_TMPDIR:-/tmp}" default is not safe. Measure the source
# repo and require a scratch root with room for 5 clones plus headroom;
# refuse to run on a too-small filesystem instead of failing mid-run.
# Search order: $BRAIN_ADVERSARIAL_TMPDIR, the repo's parent dir, /var/tmp,
# $HOME. Exit 3 = environment failure (distinct from the generator-defect
# contract), so a red harness can never be misread as a red index.
repo_kb="$(du -sk "$REPO" | cut -f1)"
need_kb=$(( repo_kb * 6 + 102400 ))  # 5 clones + 100MB headroom
REPO_PARENT="$(dirname "$(cd "$REPO" && pwd)")"  # normalized: never inside the checkout
SCRATCH_ROOT=""
for cand in "${BRAIN_ADVERSARIAL_TMPDIR:-}" "$REPO_PARENT" /var/tmp "$HOME"; do
  [ -n "$cand" ] && [ -d "$cand" ] || continue
  avail_kb="$(df -kP "$cand" 2>/dev/null | tail -1 | awk '{print $4}')"
  case "$avail_kb" in ''|*[!0-9]*) continue;; esac
  if [ "$avail_kb" -ge "$need_kb" ]; then SCRATCH_ROOT="$cand"; break; fi
done
if [ -z "$SCRATCH_ROOT" ]; then
  echo "FATAL: no scratch root with >= $(( need_kb / 1024 ))MB free for the 5 adversarial clones (source repo ~$(( repo_kb / 1024 ))MB)." >&2
  echo "Set BRAIN_ADVERSARIAL_TMPDIR to a writable disk directory and re-run." >&2
  exit 3
fi
T="$(mktemp -d "$SCRATCH_ROOT/brain-index-adversarial-XXXXXX")"
trap 'rm -rf "$T"' EXIT
echo "scratch: $T (root $SCRATCH_ROOT, need ~$(( need_kb / 1024 ))MB)" >&2

PASS=0
FAIL=0

report() { # $1=name $2=ok(1/0) $3=detail
  if [ "$2" = 1 ]; then PASS=$((PASS+1)); echo "PASS: $1"; else FAIL=$((FAIL+1)); echo "FAIL: $1"; fi
  [ -n "${3:-}" ] && echo "$3"
  echo "---"
}

# A failed scratch clone is an ENVIRONMENT failure, never a generator
# verdict. Fail LOUDLY (exit 3, named FATAL) and abort the run instead of
# letting later steps run against a missing dir and produce misleading
# case FAILs. (2026-10-01: /tmp exhaustion once made this script report
# 3/5 with case FAILs that blamed the generator for a dead clone.)
need_clone() { # $1=target dir, $2=case name
  local err="$T/clone-$2.err"
  if ! git clone -q "$REPO" "$1" 2>"$err"; then
    echo "FATAL: scratch clone for case '$2' FAILED — the harness cannot test the generator."
    echo "--- git clone stderr ---"
    cat "$err"
    echo "---"
    echo "This is an ENVIRONMENT failure (disk space? permissions? unreadable source?), NOT a generator verdict."
    echo "Fix the environment and rerun."
    exit 3
  fi
  rm -f "$err"
}

# ---------------------------------------------------------------- positive control
echo "### CASE 0: positive control — clean tree must pass"
need_clone "$T/clean" "clean"
out="$(python3 "$GEN" --root "$T/clean" --check 2>&1)"; code=$?
if [ $code -eq 0 ]; then report "clean tree --check exits 0" 1 "$out"; else report "clean tree --check exits 0" 0 "exit=$code :: $out"; fi

# ------------------------------------------------- case A: dangling pointer
echo "### CASE A: dangling pointer in MASTER-INDEX.json must fail exit 2"
need_clone "$T/a" "a"
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
need_clone "$T/b" "b"
git -C "$T/b" -c user.name=adv -c user.email=adv@local rm -q "BRAIN/99-ARCHIVE/README.md"
git -C "$T/b" -c user.name=adv -c user.email=adv@local commit -qm "sabotage: delete 99-ARCHIVE README (count skew)"
out="$(python3 "$GEN" --root "$T/b" 2>&1)"; code=$?
echo "$out"
if [ $code -eq 2 ] && echo "$out" | grep -q "below the baseline floor"; then
  report "count skew fails exit 2 with floor message" 1 ""
else
  report "count skew fails exit 2 with floor message" 0 "exit=$code (expected 2)"
fi

# --------------------------------- case C: undeclared pointer (backstop)
echo "### CASE C: undeclared new pointer field must fail via backstop scan"
need_clone "$T/c" "c"
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
need_clone "$T/d" "d"
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
