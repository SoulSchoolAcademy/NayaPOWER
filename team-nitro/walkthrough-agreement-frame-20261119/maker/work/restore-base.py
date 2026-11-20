#!/usr/bin/env python3
"""Restore the fix-9 base files (unfold + welcome) from their filed
blobs, so the AF transform can re-run from its guarded base. Blobs are
taken from the fix-9 commit's own tree (never from memory)."""
import base64, importlib.util, sys

SPEC3 = importlib.util.spec_from_file_location(
    "stage_fix3", "/home/hatch/workspace/team-nitro/walkthrough-chain-fix3-20261119/work/stage-fix3.py")
st = importlib.util.module_from_spec(SPEC3)
SPEC3.loader.exec_module(st)
SPECAF = importlib.util.spec_from_file_location(
    "build_af", "/home/hatch/workspace/team-nitro/walkthrough-agreement-frame-20261119/maker/work/build-af.py")
bf = importlib.util.module_from_spec(SPECAF)
SPECAF.loader.exec_module(bf)

PARENT = "cdc94c72bdcae03c5c815f59b67513a6077dc762"
_, commit = st.gh("GET", "/repos/%s/git/commits/%s" % (st.REPO, PARENT))
_, tree = st.gh("GET", "/repos/%s/git/trees/%s?recursive=1" % (st.REPO, commit["tree"]["sha"]))
print("tree entries: %d truncated=%s" % (len(tree.get("tree", [])), tree.get("truncated")), flush=True)
want = {
    "team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html":
        "/home/hatch/workspace/team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html",
    "team-nitro/walk-v23-assembly-20261114/welcome-staged.html":
        "/home/hatch/workspace/team-nitro/walk-v23-assembly-20261114/welcome-staged.html",
}
for entry in tree["tree"]:
    if entry["path"] in want:
        _, d = st.gh("GET", "/repos/%s/git/blobs/%s" % (st.REPO, entry["sha"]))
        raw = base64.b64decode("".join(d["content"].split()))
        print("fetched %s: blob %s %d B sha %s" % (entry["path"], entry["sha"][:12], len(raw), st.sha(raw)[:12]), flush=True)
        bf.land_via_writer9(raw, want[entry["path"]], tries=12)
        back = st.read_bytes(want[entry["path"]])
        assert st.sha(back) == st.sha(raw), "restore mismatch for %s" % entry["path"]
        print("restored %s OK" % want[entry["path"]], flush=True)
print("RESTORE DONE")
