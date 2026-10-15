#!/usr/bin/env python3
"""Push the demote candidate branch via the git-data API (no push creds here).

Mirrors the local plumbing exactly: blob -> tree (base=live main tip tree)
-> verify tree == locally computed tree -> commit (parent=live tip) ->
create ref -> verify. Refuses on any mismatch or tip move.
"""
import json, subprocess, sys

# t0796 (lane 1, Verity) identity repair: the author/committer identity is
# parameterized by the executing seat via NAYA_SEAT_NAME/NAYA_SEAT_EMAIL
# (fail-closed, exit 2 when unset). The old hardcode ("Naya Clarity
# Narzan"/naya4@nayapower.local) made the bytes lie about who built them.
sys.path.insert(0, "/home/hatch/workspace/goals/bring-naya-to-life/hidden_files/bin")
from seat_identity import seat_identity

GH = "/home/hatch/workspace/skills/github/bin/gh-api"
REPO = "/repos/SoulSchoolAcademy/NayaPOWER"
BASE_TIP = "0cc7c9f214ea9ef0503263e583e16b91801e2096"
BRANCH = "naya/demote-falsified-t0762"
FILE = "tools/smart_note_v2.py"
SRC = "/tmp/demote-live/tools/smart_note_v2.py"
EXPECT_BLOB = "61c82bacb0e39f247037ed008688a61050694b12"
EXPECT_TREE = "2c225f9a9876e70af4eb1368c9736b8a9dc4bba0"

MSG = """CANDIDATE: veracity demote for FALSIFIED lessons at retrieve (t0762 lane 5)

Base: live main tip 0cc7c9f2. Wires governance verdict t0758 lane 8
(verdict sha16 48f873518109fc1f): DEMOTE FALSIFIED at retrieve
(bucket sort + visibility marker, FALSIFIED-only scope).

retrieve() now demotes the pure-relevance ranking from
_ranked_candidates(): FALSIFIED candidates sink into a lower veracity
bucket and sort below non-FALSIFIED candidates regardless of relevance
score; within a bucket the ordering is byte-identical to the pure order.
The 40.0 relevance floor still gates the pure-relevance best (a
FALSIFIED note below the floor is still refused, exactly as before).
FALSIFIED entries are never dropped (demote, never refuse). Payload
gains veracity_demotion_applied: true whenever demotion reordered
anything, explicit false otherwise — the demotion is visible, never
silent.

Acceptance: the t1282 adversarial arm (SN-D4 FALSIFIED vs SN-D5
VERIFIED) re-derived on live bytes — pre-change SN-D4 wins 81.89 vs
70.98 unflagged; post-change SN-D5 wins with the marker set, SN-D4
still a live candidate. 20/20 acceptance checks green
(hidden_files/lane-5/test_demote_acceptance_live_t0762.py).

CANDIDATE ONLY: branch-only wiring per the brief. Refuse stays Shawn's
spec-0007 word; the flip-on decision belongs to governance +
second-seat review. Never merge."""

def api(method, path, payload=None):
    cmd = [GH, method, REPO + path]
    if payload is not None:
        body = json.dumps(payload)
        assert len(body) < 100_000, f"payload too large: {len(body)}"
        cmd.append(body)
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"API {method} {path} FAILED: {r.stderr[:500]}")
    return json.loads(r.stdout)

def live_tip():
    ref = api("GET", "/git/refs/heads/main")
    return ref["object"]["sha"]

tip = live_tip()
print("live main tip:", tip)
if tip != BASE_TIP:
    sys.exit(f"TIP MOVED ({BASE_TIP} -> {tip}); decision expired, re-anchor first")

base_tree = api("GET", f"/git/commits/{BASE_TIP}")["tree"]["sha"]
print("base tree:", base_tree)

content = open(SRC, encoding="utf-8").read()
blob = api("POST", "/git/blobs", {"content": content, "encoding": "utf-8"})["sha"]
print("blob:", blob)
if blob != EXPECT_BLOB:
    sys.exit(f"BLOB MISMATCH: api {blob} != local {EXPECT_BLOB}; refusing")

tree = api("POST", "/git/trees",
           {"base_tree": base_tree,
            "tree": [{"path": FILE, "mode": "100644", "type": "blob", "sha": blob}]})["sha"]
print("new tree:", tree)
if tree != EXPECT_TREE:
    sys.exit(f"TREE MISMATCH: api {tree} != local {EXPECT_TREE}; refusing")

ident = seat_identity()  # t0796: parameterized by executing seat, not a hardcode
commit = api("POST", "/git/commits",
             {"message": MSG, "tree": tree, "parents": [BASE_TIP],
              "author": ident, "committer": ident})["sha"]
print("new commit:", commit)
print("commit identity:", ident["name"], "<" + ident["email"] + ">")

tip2 = live_tip()
if tip2 != BASE_TIP:
    sys.exit(f"TIP MOVED mid-push ({BASE_TIP} -> {tip2}); ref NOT created")

r = subprocess.run([GH, "GET", REPO + "/git/refs/heads/naya%2Fdemote-falsified-t0762"],
                     capture_output=True, text=True)
ref_exists = not (r.returncode != 0 or '"http_status": 404' in r.stdout)
if ref_exists:
    sys.exit(f"ref already exists: {r.stdout[:200]}; refusing to overwrite")
print("ref absent: proceeding")

ref = api("POST", "/git/refs",
          {"ref": f"refs/heads/{BRANCH}", "sha": commit})["object"]["sha"]
print("ref created:", ref)
assert ref == commit, "ref target != commit"

verify = api("GET", "/git/refs/heads/naya%2Fdemote-falsified-t0762")
ok = verify["object"]["sha"] == commit
print("ref verifies:", ok)
assert ok
print("PUSH OK:", BRANCH, "@", commit[:12])
