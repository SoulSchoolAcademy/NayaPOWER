#!/usr/bin/env python3
"""FIX7 report commit (2026-11-19): file the updated MAKER-REPORT.md
(landing section) + the fixed law-fix7.py (reads the filed unfold blob,
not the pipeline — the local worker now holds fix-7 bytes) as commit 2
on walkthrough/chain-fix7-20261119. Follows the fix-6 file-report
pattern (inline gh() calls)."""
import base64, importlib.util, json, subprocess, sys, time

SPEC3 = importlib.util.spec_from_file_location(
    "stage_fix3", "/home/hatch/workspace/team-nitro/walkthrough-chain-fix3-20261119/work/stage-fix3.py")
st = importlib.util.module_from_spec(SPEC3)
SPEC3.loader.exec_module(st)

BRANCH = "walkthrough/chain-fix7-20261119"
REC = "/home/hatch/workspace/team-nitro/walkthrough-chain-fix7-20261119"
WORK = REC + "/work"


def main():
    _, ref = st.gh("GET", "/repos/%s/git/refs/heads/%s" % (st.REPO, BRANCH))
    parent = ref["object"]["sha"]
    print("parent:", parent, flush=True)
    _, commit = st.gh("GET", "/repos/%s/git/commits/%s" % (st.REPO, parent))
    base_tree = commit["tree"]["sha"]
    files = [
        ("team-nitro/walkthrough-chain-fix7-20261119/MAKER-REPORT.md", st.read_bytes(REC + "/MAKER-REPORT.md")),
        ("team-nitro/walkthrough-chain-fix7-20261119/work/law-fix7.py", st.read_bytes(WORK + "/law-fix7.py")),
        ("team-nitro/walkthrough-chain-fix7-20261119/work/file-report-fix7.py", st.read_bytes(WORK + "/file-report-fix7.py")),
    ]
    blobs = {}
    for path, data in files:
        _, blob = st.gh("POST", "/repos/%s/git/blobs" % st.REPO,
                        {"content": base64.b64encode(data).decode("ascii"), "encoding": "base64"})
        blobs[path] = blob["sha"]
        print("blob %s: %s (%d B)" % (path.split("/")[-1], blob["sha"][:12], len(data)), flush=True)
    _, tree = st.gh("POST", "/repos/%s/git/trees" % st.REPO,
                    {"base_tree": base_tree,
                     "tree": [{"path": p, "mode": "100644", "type": "blob", "sha": s} for p, s in blobs.items()]})
    print("new tree:", tree["sha"], flush=True)
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    _, cm = st.gh("POST", "/repos/%s/git/commits" % st.REPO,
                  {"message": "Walkthrough CHAIN FIX7 — commit 2: landing report + fixed law check\n\n"
                              "MAKER-REPORT.md gains the LANDING section (branch, commit, worker\n"
                              "sha, route verification, laws delta, the face-images gap). law-fix7.py\n"
                              "reads the filed unfold blob instead of the pipeline: the stage run's\n"
                              "write_resilient landed the fix-7 worker locally, so the transform's\n"
                              "base extraction (local worker, expecting fix-3 bytes) no longer\n"
                              "applies. Laws: zero new violations (welcome 83/4, identity 11/2,\n"
                              "walk 128/8, unfold 1/2 — all identical to fix-6).",
                   "tree": tree["sha"], "parents": [parent],
                   "author": {"name": "nayapower-lane-agent[bot]",
                              "email": "338161897+nayapower-lane-agent[bot]@users.noreply.github.com",
                              "date": now},
                   "committer": {"name": "GitHub", "email": "noreply@github.com", "date": now}})
    commit_sha = cm["sha"]
    print("commit sha:", commit_sha, flush=True)
    _, ref3 = st.gh("PATCH", "/repos/%s/git/refs/heads/%s" % (st.REPO, BRANCH),
                    {"sha": commit_sha, "force": False})
    print("branch now:", ref3["object"]["sha"], flush=True)
    assert ref3["object"]["sha"] == commit_sha
    for path, data in files:
        _, rb = st.gh("GET", "/repos/%s/git/blobs/%s" % (st.REPO, blobs[path]))
        raw = base64.b64decode("".join(rb["content"].split()))
        assert len(raw) == len(data) and st.sha(raw) == st.sha(data), "blob read-back mismatch for %s" % path
        print("blob read-back OK:", path.split("/")[-1], flush=True)
    print("REPORT-RESULT branch=%s commit=%s" % (BRANCH, commit_sha), flush=True)


if __name__ == "__main__":
    main()
