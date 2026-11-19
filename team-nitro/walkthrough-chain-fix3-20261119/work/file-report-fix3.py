#!/usr/bin/env python3
"""File the fix3 maker report + remaining work records as commit 4 on
walkthrough/chain-fix3-20261119 (parent: commit 3, 34a73382). No code
changes — the staged version is fix3c, already filed in commit 3 and
already PUT. Read-back verifies every blob by full sha. No PR, no merge,
no live deploy, no message to Shawn.
"""
import base64, importlib.util, json, time

SPEC = importlib.util.spec_from_file_location(
    "stage_fix3", "/home/hatch/workspace/team-nitro/walkthrough-chain-fix3-20261119/work/stage-fix3.py")
st = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(st)

PARENT = "34a733823e24be10b2ae86588cbf4258d103789b"
R = "/home/hatch/workspace/team-nitro/walkthrough-chain-fix3-20261119"
FILES = [
    ("team-nitro/walkthrough-chain-fix3-20261119/MAKER-REPORT.md", st.read_bytes(R + "/MAKER-REPORT.md")),
    ("team-nitro/walkthrough-chain-fix3-20261119/work/resume-fix3.py", st.read_bytes(R + "/work/resume-fix3.py")),
    ("team-nitro/walkthrough-chain-fix3-20261119/work/probe-fix3c-live.py", st.read_bytes(R + "/work/probe-fix3c-live.py")),
    ("team-nitro/walkthrough-chain-fix3-20261119/work/probe-staging-redirect.py", st.read_bytes(R + "/work/probe-staging-redirect.py")),
    ("team-nitro/walkthrough-chain-fix3-20261119/evidence/fix3-live.json", st.read_bytes(R + "/evidence/fix3-live.json")),
    ("team-nitro/walkthrough-chain-fix3-20261119/evidence/fix3b-live.json", st.read_bytes(R + "/evidence/fix3b-live.json")),
    ("team-nitro/walkthrough-chain-fix3-20261119/evidence/fix3c-live.json", st.read_bytes(R + "/evidence/fix3c-live.json")),
    ("team-nitro/walkthrough-chain-fix3-20261119/work/file-report-fix3.py", st.read_bytes(R + "/work/file-report-fix3.py")),
]

def main():
    _, ref = st.gh("GET", "/repos/%s/git/refs/heads/%s" % (st.REPO, st.NEW_BRANCH))
    assert ref["object"]["sha"] == PARENT, ref["object"]["sha"]
    print("branch at commit:", PARENT, flush=True)
    _, commit = st.gh("GET", "/repos/%s/git/commits/%s" % (st.REPO, PARENT))
    base_tree = commit["tree"]["sha"]
    blobs = {}
    for path, data in FILES:
        _, blob = st.gh("POST", "/repos/%s/git/blobs" % st.REPO,
                        {"content": base64.b64encode(data).decode("ascii"), "encoding": "base64"})
        blobs[path] = blob["sha"]
        print("blob %s: %s (%d B)" % (path.split("/")[-1], blob["sha"][:12], len(data)), flush=True)
    _, tree = st.gh("POST", "/repos/%s/git/trees" % st.REPO,
                    {"base_tree": base_tree,
                     "tree": [{"path": p, "mode": "100644", "type": "blob", "sha": s} for p, s in blobs.items()]})
    print("new tree:", tree["sha"], flush=True)
    msg = ("Walkthrough CHAIN FIX3 — maker report + live-probe records, commit 4\n\n"
           "The round's version is fix3c (commit 3): all seven items DONE or "
           "adjudicated not-a-defect, each proven by a live Firefox click-through "
           "against the staged bytes (fix3/fix3b/fix3c live JSON + screenshots in "
           "evidence/). This commit files the maker report and the remaining work "
           "records. No code changes. NO PR, NO MERGE — the checker and the "
           "captain come after this seat. Nothing live.")
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    _, cm = st.gh("POST", "/repos/%s/git/commits" % st.REPO,
                  {"message": msg, "tree": tree["sha"], "parents": [PARENT],
                   "author": {"name": "nayapower-lane-agent[bot]",
                              "email": "338161897+nayapower-lane-agent[bot]@users.noreply.github.com",
                              "date": now},
                   "committer": {"name": "GitHub", "email": "noreply@github.com", "date": now}})
    commit_sha = cm["sha"]
    print("commit sha:", commit_sha, flush=True)
    _, ref3 = st.gh("PATCH", "/repos/%s/git/refs/heads/%s" % (st.REPO, st.NEW_BRANCH),
                    {"sha": commit_sha, "force": False})
    print("branch now:", ref3["object"]["sha"], flush=True)
    assert ref3["object"]["sha"] == commit_sha
    for path, data in FILES:
        _, rb = st.gh("GET", "/repos/%s/git/blobs/%s" % (st.REPO, blobs[path]))
        raw = base64.b64decode("".join(rb["content"].split()))
        assert len(raw) == len(data) and st.sha(raw) == st.sha(data), "blob read-back mismatch for %s" % path
        print("blob read-back OK:", path.split("/")[-1], len(raw), "bytes, sha match", flush=True)
    print("FILE-REPORT-RESULT " + json.dumps({
        "commit": commit_sha, "tree": tree["sha"], "blobs": blobs}, indent=1), flush=True)

if __name__ == "__main__":
    main()
