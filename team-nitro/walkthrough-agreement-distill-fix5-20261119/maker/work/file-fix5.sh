#!/usr/bin/env bash
# Agreement distill fix-5 — file the fixed files + maker report + work
# scripts to branch walkthrough/agreement-distill-fix5-20261119, from
# fix-4 tip d5003b2fd5c59e352b84169294b2773263876e01.
# Blobs via the git-data API (gh-direct.py); the contents API returns EMPTY
# for files over 1 MB, so the blob API is used for everything. Multi-MB
# base64 payloads are piped (base64 -> jq via process substitution), never
# staged to disk. Every filed blob sha is verified against local
# `git hash-object` before the tree is built.
set -euo pipefail
GH=~/workspace/team-nitro/gh-direct.py
REPO=SoulSchoolAcademy/NayaPOWER
PARENT=d5003b2fd5c59e352b84169294b2773263876e01
BASE_TREE=41ab80421cae5e9ee896e7105fe93c407f103556
BRANCH=walkthrough/agreement-distill-fix5-20261119
W=~/workspace/team-nitro/walkthrough-agreement-distill-fix5-20261119/maker/work
M=~/workspace/team-nitro/walkthrough-agreement-distill-fix5-20261119/maker
cd "$W"

# local file -> repo path (one per line, | separated)
FILES="
fix5-agreement-unfold-fixed.html|team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html
fix5-welcome-staged.html|team-nitro/walk-v23-assembly-20261114/welcome-staged.html
fix5-walk-beginning-fixed.html|team-nitro/walk-v23-assembly-20261114/walk-beginning-fixed.html
fix5-identity-fixed.html|team-nitro/walk-v23-assembly-20261114/identity-fixed.html
fix5-walk-beginning-staging-worker.js|team-nitro/walk-v23-assembly-20261114/walk-beginning-staging-worker.js
fix5-build-v23-staging-worker.py|team-nitro/walk-v23-assembly-20261114/build-v23-staging-worker.py
$M/MAKER-REPORT.md|team-nitro/walkthrough-agreement-distill-fix5-20261119/maker/MAKER-REPORT.md
verify-base.cjs|team-nitro/walkthrough-agreement-distill-fix5-20261119/maker/work/verify-base.cjs
base-verify.json|team-nitro/walkthrough-agreement-distill-fix5-20261119/maker/work/base-verify.json
fix5.js|team-nitro/walkthrough-agreement-distill-fix5-20261119/maker/work/fix5.js
update-build-script-fix5.js|team-nitro/walkthrough-agreement-distill-fix5-20261119/maker/work/update-build-script-fix5.js
serve.cjs|team-nitro/walkthrough-agreement-distill-fix5-20261119/maker/work/serve.cjs
staging-meta.json|team-nitro/walkthrough-agreement-distill-fix5-20261119/maker/work/staging-meta.json
browsertest.py|team-nitro/walkthrough-agreement-distill-fix5-20261119/maker/work/browsertest.py
intro-diag.py|team-nitro/walkthrough-agreement-distill-fix5-20261119/maker/work/intro-diag.py
intro-diag2.py|team-nitro/walkthrough-agreement-distill-fix5-20261119/maker/work/intro-diag2.py
probe-fix5-base.py|team-nitro/walkthrough-agreement-distill-fix5-20261119/maker/work/probe-fix5-base.py
probe-fix5-verify.py|team-nitro/walkthrough-agreement-distill-fix5-20261119/maker/work/probe-fix5-verify.py
probe-fix5-f9.py|team-nitro/walkthrough-agreement-distill-fix5-20261119/maker/work/probe-fix5-f9.py
probe-fix5-f9b.py|team-nitro/walkthrough-agreement-distill-fix5-20261119/maker/work/probe-fix5-f9b.py
probe-fix5-f9c.py|team-nitro/walkthrough-agreement-distill-fix5-20261119/maker/work/probe-fix5-f9c.py
probe-fix5-staged.py|team-nitro/walkthrough-agreement-distill-fix5-20261119/maker/work/probe-fix5-staged.py
laws-base.txt|team-nitro/walkthrough-agreement-distill-fix5-20261119/maker/work/laws-base.txt
laws-fix5.txt|team-nitro/walkthrough-agreement-distill-fix5-20261119/maker/work/laws-fix5.txt
file-fix5.sh|team-nitro/walkthrough-agreement-distill-fix5-20261119/maker/work/file-fix5.sh
proof-base/fix5-base.json|team-nitro/walkthrough-agreement-distill-fix5-20261119/maker/work/proof-base/fix5-base.json
proof-base/fix5-base-bridge-s0.png|team-nitro/walkthrough-agreement-distill-fix5-20261119/maker/work/proof-base/fix5-base-bridge-s0.png
proof-base/fix5-base-bridge-smax.png|team-nitro/walkthrough-agreement-distill-fix5-20261119/maker/work/proof-base/fix5-base-bridge-smax.png
proof-base/fix5-base-bridge-full.png|team-nitro/walkthrough-agreement-distill-fix5-20261119/maker/work/proof-base/fix5-base-bridge-full.png
proof-base/fix5-base-intro-s0.png|team-nitro/walkthrough-agreement-distill-fix5-20261119/maker/work/proof-base/fix5-base-intro-s0.png
proof-fix5/fix5-verify.json|team-nitro/walkthrough-agreement-distill-fix5-20261119/maker/work/proof-fix5/fix5-verify.json
proof-fix5/fix5-f9-deck-letter.json|team-nitro/walkthrough-agreement-distill-fix5-20261119/maker/work/proof-fix5/fix5-f9-deck-letter.json
proof-fix5/fix5-f9-deck-letter2.json|team-nitro/walkthrough-agreement-distill-fix5-20261119/maker/work/proof-fix5/fix5-f9-deck-letter2.json
proof-fix5/fix5-f9-deck-letter3.json|team-nitro/walkthrough-agreement-distill-fix5-20261119/maker/work/proof-fix5/fix5-f9-deck-letter3.json
proof-fix5/fix5-bridge-s0.png|team-nitro/walkthrough-agreement-distill-fix5-20261119/maker/work/proof-fix5/fix5-bridge-s0.png
proof-fix5/fix5-bridge-smax.png|team-nitro/walkthrough-agreement-distill-fix5-20261119/maker/work/proof-fix5/fix5-bridge-smax.png
proof-fix5/fix5-bridge-full.png|team-nitro/walkthrough-agreement-distill-fix5-20261119/maker/work/proof-fix5/fix5-bridge-full.png
proof-fix5/fix5-1920-bridge.png|team-nitro/walkthrough-agreement-distill-fix5-20261119/maker/work/proof-fix5/fix5-1920-bridge.png
proof-fix5/fix5-1920-unfold37.png|team-nitro/walkthrough-agreement-distill-fix5-20261119/maker/work/proof-fix5/fix5-1920-unfold37.png
proof-fix5/fix5-staged-bridge-s0.png|team-nitro/walkthrough-agreement-distill-fix5-20261119/maker/work/proof-fix5/fix5-staged-bridge-s0.png
stage5_.bin|team-nitro/walkthrough-agreement-distill-fix5-20261119/maker/work/stage5_.bin
stage5_identity.html.bin|team-nitro/walkthrough-agreement-distill-fix5-20261119/maker/work/stage5_identity.html.bin
stage5_welcome.bin|team-nitro/walkthrough-agreement-distill-fix5-20261119/maker/work/stage5_welcome.bin
stage5_agreement.bin|team-nitro/walkthrough-agreement-distill-fix5-20261119/maker/work/stage5_agreement.bin
"

: > /tmp/fix5-tree-entries.jsonl
echo "$FILES" | grep -v '^$' | while IFS='|' read -r local repo; do
  [ -f "$local" ] || { echo "MISSING LOCAL FILE: $local"; exit 1; }
  want="$(git hash-object "$local")"
  got="$(python3 "$GH" POST "/repos/$REPO/git/blobs" @<(base64 -w0 "$local" | jq -Rs '{content:.,encoding:"base64"}') | python3 -c "import json,sys; d=sys.stdin.read(); j=json.loads(d.split('\n',1)[1]); print(j['sha'])")"
  [ "$got" = "$want" ] || { echo "BLOB MISMATCH $local local=$want remote=$got"; exit 1; }
  echo "blob OK $repo $got ($(stat -c %s "$local") B)"
  jq -n --arg p "$repo" --arg s "$got" '{path:$p, mode:"100644", type:"blob", sha:$s}' >> /tmp/fix5-tree-entries.jsonl
done
echo "ALL BLOBS OK: $(wc -l < /tmp/fix5-tree-entries.jsonl) files"

TREE_PAYLOAD=/tmp/fix5-tree-payload.json
jq -n --arg bt "$BASE_TREE" --slurpfile entries /tmp/fix5-tree-entries.jsonl '{base_tree:$bt, tree:$entries}' > "$TREE_PAYLOAD"
TREE="$(python3 "$GH" POST "/repos/$REPO/git/trees" @"$TREE_PAYLOAD" | python3 -c "import json,sys; d=sys.stdin.read(); j=json.loads(d.split('\n',1)[1]); print(j['sha'])")"
echo "tree $TREE"
COMMIT_PAYLOAD=/tmp/fix5-commit-payload.json
jq -n --arg t "$TREE" --arg p "$PARENT" '{message:"Agreement distill fix-5: footer links reachable at 390 (F)", tree:$t, parents:[$p]}' > "$COMMIT_PAYLOAD"
COMMIT="$(python3 "$GH" POST "/repos/$REPO/git/commits" @"$COMMIT_PAYLOAD" | python3 -c "import json,sys; d=sys.stdin.read(); j=json.loads(d.split('\n',1)[1]); print(j['sha'])")"
echo "commit $COMMIT"
python3 "$GH" POST "/repos/$REPO/git/refs" @<(jq -n --arg b "refs/heads/$BRANCH" --arg s "$COMMIT" '{ref:$b, sha:$s}') | head -3
echo "branch $BRANCH tip $COMMIT"
