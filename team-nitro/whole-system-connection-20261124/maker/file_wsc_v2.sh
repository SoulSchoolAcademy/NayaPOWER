#!/bin/bash
# File the whole-system connection round FIX MAKER v2 to GitHub via gh-app-api.
# Parent = branch tip fafd172c (read live and asserted). New commit on top of
# it; the branch ref is MOVED with PATCH (it already exists).
# Blobs are piped via process substitution — no multi-MB base64 staged to disk.
# Every blob sha is checked against local `git hash-object`. Ref PATCH is LAST;
# earlier failure leaves only harmless orphans.
set -euo pipefail
GH="$HOME/workspace/custom-connectors/custom.legacy-github/bin/gh-app-api"
REPO="SoulSchoolAcademy/NayaPOWER"
BRANCH="whole-system-connection-20261124"
EXPECT_TIP="fafd172ce8f40adf6464748d4a60b5bdb6de0e65"
DIR="$HOME/workspace/team-nitro/whole-system-connection-20261124/maker"

JGET() { python3 -c "import sys,json; d=json.load(sys.stdin); print($1)"; }
BLOB() { # $1 = file path; posts the blob, verifies sha vs git hash-object
  local f="$1" exp got
  exp=$(git hash-object "$f")
  got=$($GH POST /repos/$REPO/git/blobs @<(python3 -c 'import base64,json,sys; print(json.dumps({"content": base64.b64encode(open(sys.argv[1],"rb").read()).decode(), "encoding": "base64"}))' "$f") | JGET "d['sha']")
  echo "$f -> $got" >&2
  if [ "$got" != "$exp" ]; then echo "STOP: blob sha mismatch $got != $exp ($f)"; exit 2; fi
  echo "$got"
}

echo "== parent (branch tip, must be $EXPECT_TIP)"
PARENT=$($GH GET /repos/$REPO/git/refs/heads/$BRANCH | JGET "d['object']['sha']")
echo "parent: $PARENT"
if [ "$PARENT" != "$EXPECT_TIP" ]; then echo "STOP: tip moved ($PARENT)"; exit 3; fi
ROOT_TREE=$($GH GET /repos/$REPO/git/commits/$PARENT | JGET "d['tree']['sha']")
echo "root tree: $ROOT_TREE"
TN_SHA=$($GH GET /repos/$REPO/git/trees/$ROOT_TREE | JGET "[e['sha'] for e in d['tree'] if e['path']=='team-nitro'][0]")
ROUND_TREE=$($GH GET /repos/$REPO/git/trees/$TN_SHA | JGET "[e['sha'] for e in d['tree'] if e['path']=='$BRANCH'][0]")
MAKER_TREE=$($GH GET /repos/$REPO/git/trees/$ROUND_TREE | JGET "[e['sha'] for e in d['tree'] if e['path']=='maker'][0]")
echo "team-nitro: $TN_SHA round: $ROUND_TREE maker: $MAKER_TREE"

echo "== post blobs (staged files + report)"
B_PORTAL=$(BLOB "$DIR/welcome-staged.html")
B_AGMT=$(BLOB "$DIR/agreement.html")
B_ID=$(BLOB "$DIR/identity.html")
B_REPORT=$(BLOB "$DIR/MAKER-REPORT.md")

echo "== post blobs (v2 scripts + probes)"
B_EPV2=$(BLOB "$DIR/edit-portal-v2.py")
B_EPV2B=$(BLOB "$DIR/edit-portal-v2b.py")
B_EAGV2=$(BLOB "$DIR/edit-agreement-v2.py")
B_EAGV2B=$(BLOB "$DIR/edit-agreement-v2b.py")
B_EIDV2=$(BLOB "$DIR/edit-identity-v2.py")
B_PPORTAL=$(BLOB "$DIR/probe-v2-portal.py")
B_PAGMT=$(BLOB "$DIR/probe-v2-agreement.py")
B_PID=$(BLOB "$DIR/probe-v2-identity.py")
B_PDISC=$(BLOB "$DIR/probe-v2-disc.py")
B_PNAV=$(BLOB "$DIR/probe-v2-decknav.py")
B_PCOVER=$(BLOB "$DIR/probe-v2-cover.py")
B_PAUDIO=$(BLOB "$DIR/probe-v2-audio.py")
B_PDEBUG=$(BLOB "$DIR/probe-v2-debug.py")
B_PBASE=$(BLOB "$DIR/probe-v2-baseline.py")
B_FILEV2=$(BLOB "$DIR/file_wsc_v2.sh")

echo "== post trees"
NEW_MAKER_TREE=$($GH POST /repos/$REPO/git/trees "{\"base_tree\":\"$MAKER_TREE\",\"tree\":[{\"path\":\"edit-portal-v2.py\",\"mode\":\"100644\",\"type\":\"blob\",\"sha\":\"$B_EPV2\"},{\"path\":\"edit-portal-v2b.py\",\"mode\":\"100644\",\"type\":\"blob\",\"sha\":\"$B_EPV2B\"},{\"path\":\"edit-agreement-v2.py\",\"mode\":\"100644\",\"type\":\"blob\",\"sha\":\"$B_EAGV2\"},{\"path\":\"edit-agreement-v2b.py\",\"mode\":\"100644\",\"type\":\"blob\",\"sha\":\"$B_EAGV2B\"},{\"path\":\"edit-identity-v2.py\",\"mode\":\"100644\",\"type\":\"blob\",\"sha\":\"$B_EIDV2\"},{\"path\":\"probe-v2-portal.py\",\"mode\":\"100644\",\"type\":\"blob\",\"sha\":\"$B_PPORTAL\"},{\"path\":\"probe-v2-agreement.py\",\"mode\":\"100644\",\"type\":\"blob\",\"sha\":\"$B_PAGMT\"},{\"path\":\"probe-v2-identity.py\",\"mode\":\"100644\",\"type\":\"blob\",\"sha\":\"$B_PID\"},{\"path\":\"probe-v2-disc.py\",\"mode\":\"100644\",\"type\":\"blob\",\"sha\":\"$B_PDISC\"},{\"path\":\"probe-v2-decknav.py\",\"mode\":\"100644\",\"type\":\"blob\",\"sha\":\"$B_PNAV\"},{\"path\":\"probe-v2-cover.py\",\"mode\":\"100644\",\"type\":\"blob\",\"sha\":\"$B_PCOVER\"},{\"path\":\"probe-v2-audio.py\",\"mode\":\"100644\",\"type\":\"blob\",\"sha\":\"$B_PAUDIO\"},{\"path\":\"probe-v2-debug.py\",\"mode\":\"100644\",\"type\":\"blob\",\"sha\":\"$B_PDEBUG\"},{\"path\":\"probe-v2-baseline.py\",\"mode\":\"100644\",\"type\":\"blob\",\"sha\":\"$B_PBASE\"},{\"path\":\"file_wsc_v2.sh\",\"mode\":\"100644\",\"type\":\"blob\",\"sha\":\"$B_FILEV2\"}]}" | JGET "d['sha']")
echo "maker tree: $NEW_MAKER_TREE"
NEW_ROUND_TREE=$($GH POST /repos/$REPO/git/trees "{\"base_tree\":\"$ROUND_TREE\",\"tree\":[{\"path\":\"welcome-staged.html\",\"mode\":\"100644\",\"type\":\"blob\",\"sha\":\"$B_PORTAL\"},{\"path\":\"agreement.html\",\"mode\":\"100644\",\"type\":\"blob\",\"sha\":\"$B_AGMT\"},{\"path\":\"identity.html\",\"mode\":\"100644\",\"type\":\"blob\",\"sha\":\"$B_ID\"},{\"path\":\"MAKER-REPORT.md\",\"mode\":\"100644\",\"type\":\"blob\",\"sha\":\"$B_REPORT\"},{\"path\":\"maker\",\"mode\":\"040000\",\"type\":\"tree\",\"sha\":\"$NEW_MAKER_TREE\"}]}" | JGET "d['sha']")
echo "round tree: $NEW_ROUND_TREE"
NTT=$($GH POST /repos/$REPO/git/trees "{\"base_tree\":\"$TN_SHA\",\"tree\":[{\"path\":\"$BRANCH\",\"mode\":\"040000\",\"type\":\"tree\",\"sha\":\"$NEW_ROUND_TREE\"}]}" | JGET "d['sha']")
echo "team-nitro tree: $NTT"
NRT=$($GH POST /repos/$REPO/git/trees "{\"base_tree\":\"$ROOT_TREE\",\"tree\":[{\"path\":\"team-nitro\",\"mode\":\"040000\",\"type\":\"tree\",\"sha\":\"$NTT\"}]}" | JGET "d['sha']")
echo "root tree: $NRT"

echo "== post commit"
MSG=$(cat <<'EOF'
Whole-system connection round (fix maker v2): checker FAIL items fixed by render

Checker FAILED v1 (CHECKER-VERDICT.md): phone front door broken, walk below
the fold, final-reader Close dead on a load-time null, no live "I agree",
visible button still the long label, taken message white/small/below fold.

Portal: at <=480px the deed sentence + reader move out of .content into
.stage below the circle (desktop untouched) — #userName SELF + typable,
deed whole, "NAYA WELCOMES YOU" visible, info button opens the reader at
390x844. .fp-login[hidden]{display:none} + scrollIntoView: the walk comes
into view on load (Q1 in view, end buttons in view, both widths); duplicated
"Welcome home." heading removed. Visible #fpEnterDeal is now "Read the
agreement".

Agreement: final Close wired guarded (wireFinalClose on DOMContentLoaded +
inside openFinal) — zero load errors, Close closes for all 8 final-board
links. New .fp-agree-btn at the deck end AND the letter end: held-press
scale .94 + dim, N hold, then in place to /?from=agreement#userName with
#userName focused. Play disc sinks .94 + dim (idle pulse paused while held).
Choice pills 280x64 both; daybar title whole at 390px. Item 7 flagged: no
real-audio path is demonstrable — the one-play-path rule pauses the audio on
play and the analyser is wired only to it; the synthetic branch stays.
Item 48/50: video-left/audio-right proven on the cover screen by render.
Slide 11 byte-identical (33b0590cfb9f811a); .intel-board count 6.

Identity: "already claimed" is green 19px/800; the green note + "This is me"
scroll into view when they appear (phone + desktop, in viewport).

Item 22 DONE by coordinator restatement (no build). Item 78 HELD pending
parent authorization (artifact untouched). All script blocks pass node
--check. Per-item table for all 78 in MAKER-REPORT.md (v2 section).
Staged only; no merge, no live deploy.
EOF
)
NEW_COMMIT=$($GH POST /repos/$REPO/git/commits @<(MSG="$MSG" python3 -c 'import json,os,sys; print(json.dumps({"message": os.environ["MSG"], "tree": sys.argv[1], "parents": [sys.argv[2]]}))' "$NRT" "$PARENT") | JGET "d['sha']")
echo "new commit: $NEW_COMMIT"

echo "== move ref refs/heads/$BRANCH (PATCH, last)"
$GH PATCH /repos/$REPO/git/refs/heads/$BRANCH "{\"sha\":\"$NEW_COMMIT\"}" | JGET "d['object']['sha']"
echo "== verify ref"
VREF=$($GH GET /repos/$REPO/git/refs/heads/$BRANCH | JGET "d['object']['sha']")
echo "verify ref sha: $VREF MATCH: $([ "$VREF" = "$NEW_COMMIT" ] && echo YES || echo NO)"
echo "== verify blobs (sha + size)"
for b in $B_PORTAL $B_AGMT $B_ID $B_REPORT; do $GH GET /repos/$REPO/git/blobs/$b | JGET "(d['sha'], d['size'])"; done
echo "FILE OK"
echo "branch=$BRANCH commit=$NEW_COMMIT parent=$PARENT"
echo "blobs: portal=$B_PORTAL agreement=$B_AGMT identity=$B_ID report=$B_REPORT"
