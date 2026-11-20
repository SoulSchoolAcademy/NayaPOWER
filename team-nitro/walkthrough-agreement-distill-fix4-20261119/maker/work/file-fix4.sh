#!/usr/bin/env bash
# Agreement distill fix-4 — filing to branch walkthrough/agreement-distill-fix4-20261119
# via the git-data API (gh-direct.py). Blob API throughout (contents API
# returns EMPTY for files over 1 MB). Base64 is piped via process
# substitution — never staged to disk. Every blob sha is checked against
# local `git hash-object` before the tree is built.
set -euo pipefail
GH=~/workspace/team-nitro/gh-direct.py
REPO=SoulSchoolAcademy/NayaPOWER
BASE_TIP=dc262be69cb2c4e0eec6ec923a85f7eae5fafacb
BASE_TREE=a5de33d536f236f9b38ef197550a115e65ba7f06
BRANCH=walkthrough/agreement-distill-fix4-20261119
WORK=~/workspace/team-nitro/walkthrough-agreement-distill-fix4-20261119/maker/work
MAKER=~/workspace/team-nitro/walkthrough-agreement-distill-fix4-20261119/maker
ROUND=~/workspace/team-nitro/walk-v23-assembly-20261114

# local-file : repo-path  (order matters only for the log)
FILES=(
  "$WORK/fix4b-agreement-unfold-fixed.html:team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html"
  "$WORK/fix4b-welcome-staged.html:team-nitro/walk-v23-assembly-20261114/welcome-staged.html"
  "$WORK/fix4b-walk-beginning-fixed.html:team-nitro/walk-v23-assembly-20261114/walk-beginning-fixed.html"
  "$WORK/fix4b-identity-fixed.html:team-nitro/walk-v23-assembly-20261114/identity-fixed.html"
  "$WORK/fix4b-walk-beginning-staging-worker.js:team-nitro/walk-v23-assembly-20261114/walk-beginning-staging-worker.js"
  "$ROUND/build-v23-staging-worker.py:team-nitro/walk-v23-assembly-20261114/build-v23-staging-worker.py"
  "$MAKER/MAKER-REPORT.md:team-nitro/walkthrough-agreement-distill-fix4-20261119/maker/MAKER-REPORT.md"
)
for s in fetch-base.py fix4.js fix4b.js update-build-script.js update-build-script-b.js staging-meta.json probe-fix4-base.py probe-fix4-detail.py probe-fix4-verify.py probe-fix4-facts.py probe-fix4-linefix.py probe-fix4-verify2.py probe-fix4-1920.py probe-fix4-caption.py probe-fix4-img.py; do
  FILES+=("$WORK/$s:team-nitro/walkthrough-agreement-distill-fix4-20261119/maker/work/$s")
done

declare -a ENTRIES=()
for pair in "${FILES[@]}"; do
  local="${pair%%:*}"; repo="${pair##*:}"
  want="$(git hash-object "$local")"
  got="$(python3 "$GH" POST "/repos/$REPO/git/blobs" @<(base64 -w0 "$local" | jq -Rs '{content:.,encoding:"base64"}') | python3 -c "import json,sys; d=sys.stdin.read(); j=json.loads(d.split('\n',1)[1]); print(j['sha'])")"
  if [ "$got" != "$want" ]; then echo "BLOB MISMATCH $repo local=$want remote=$got"; exit 1; fi
  echo "blob OK $repo $got ($(wc -c < "$local") B)"
  ENTRIES+=("$(jq -n --arg p "$repo" --arg s "$got" '{path:$p, mode:"100644", type:"blob", sha:$s}')")
done

TREE_BODY="$(jq -n --arg bt "$BASE_TREE" --argjson t "[$(IFS=,; echo "${ENTRIES[*]}")]" '{base_tree:$bt, tree:$t}')"
TREE_SHA="$(python3 "$GH" POST "/repos/$REPO/git/trees" @<(printf '%s' "$TREE_BODY") | python3 -c "import json,sys; d=sys.stdin.read(); j=json.loads(d.split('\n',1)[1]); print(j['sha'])")"
echo "tree $TREE_SHA"

COMMIT_MSG="Agreement distill fix-4: phone-width A-F fixes (fix-4b)

Six 390px presentation defects from the fix-3 captain's eye, CSS/layout-only at <=480px: A hero name clears the certificate title (28px + zone margin; certifies line hides while the hero shows); B door heading clears the corner jewels (80px side padding); C taken-note banner clears the jewels (76px padding; bottom frame stone hidden while the note shows); D board-37 title 22px on unfold (.frame-title), deck and letter (beats the af-deck !important rule); E deck/letter sign photo below the text box (64px frame margin); F footer links strip confirmed scrollable (no change). Worker rebuilt from the fixed inputs (byte-identical second rebuild). F9 regression passes at 390 and 1920; laws delta 0. Maker report: team-nitro/walkthrough-agreement-distill-fix4-20261119/maker/MAKER-REPORT.md"
COMMIT_SHA="$(python3 "$GH" POST "/repos/$REPO/git/commits" @<(jq -n --arg m "$COMMIT_MSG" --arg t "$TREE_SHA" --arg p "$BASE_TIP" '{message:$m, tree:$t, parents:[$p]}') | python3 -c "import json,sys; d=sys.stdin.read(); j=json.loads(d.split('\n',1)[1]); print(j['sha'])")"
echo "commit $COMMIT_SHA"

python3 "$GH" POST "/repos/$REPO/git/refs" @<(jq -n --arg r "refs/heads/$BRANCH" --arg s "$COMMIT_SHA" '{ref:$r, sha:$s}')
echo "branch $BRANCH tip $COMMIT_SHA"
