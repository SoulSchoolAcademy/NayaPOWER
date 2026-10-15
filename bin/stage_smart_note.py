#!/usr/bin/env python3
"""Stage one Smart Note onto the naya4/smart-notes-2026-09-30 branch via Git Data API.
Usage: stage_smart_note.py <local_md_file> <repo_path> [sn_number]
If sn_number omitted, reads/increments hidden_files/smart-notes-counter.md.
Prints the new commit sha. Idempotent per unique repo_path (skips if path+content already staged).
"""
import json, subprocess, sys, os, hashlib, urllib.parse

# t0796 (lane 1, Verity) identity repair: seat-parameterized authorship,
# fail-closed when NAYA_SEAT_NAME/NAYA_SEAT_EMAIL are unset.
sys.path.insert(0, "/home/hatch/workspace/goals/bring-naya-to-life/hidden_files/bin")
from seat_identity import seat_identity

GH = "/home/hatch/workspace/skills/github/bin/gh-api"
REPO = "SoulSchoolAcademy/NayaPOWER"
BRANCH = "naya4/smart-notes-2026-09-30"
HIDDEN = "/home/hatch/workspace/goals/bring-naya-to-life/hidden_files"
COUNTER = os.path.join(HIDDEN, "smart-notes-counter.md")

def api(method, path, body=None):
    cmd = [GH, method, f"/repos/{REPO}{path}"]
    if body is not None:
        cmd.append(json.dumps(body))
    r = subprocess.run(cmd, capture_output=True, text=True, cwd="/home/hatch/workspace")
    if r.returncode != 0:
        print(f"API FAIL {method} {path}: {r.stdout[:400]}", file=sys.stderr)
        sys.exit(1)
    return json.loads(r.stdout)

def main():
    local, repo_path = sys.argv[1], sys.argv[2]
    with open(local, encoding="utf-8") as fh:
        content = fh.read()
    digest = hashlib.sha256(content.encode()).hexdigest()[:12]

    # branch tip
    ref = api("GET", f"/git/refs/heads/{BRANCH}")
    tip = ref["object"]["sha"]
    commit = api("GET", f"/git/commits/{tip}")
    base_tree = commit["tree"]["sha"]

    # skip if identical content already at path
    try:
        tree = api("GET", f"/git/trees/{base_tree}?recursive=1")
        import base64
        for e in tree.get("tree", []):
            if e["path"] == repo_path:
                blob = api("GET", f"/git/blobs/{e['sha']}")
                existing = base64.b64decode(blob["content"]).decode("utf-8", "replace")
                if hashlib.sha256(existing.encode()).hexdigest()[:12] == digest:
                    print(f"SKIP identical already staged: {repo_path}")
                    return
    except SystemExit:
        raise
    except Exception as ex:
        print(f"warn: tree check failed ({ex}), continuing")

    blob = api("POST", "/git/blobs", {"content": content, "encoding": "utf-8"})
    new_tree = api("POST", "/git/trees", {
        "base_tree": base_tree,
        "tree": [{"path": repo_path, "mode": "100644", "type": "blob", "sha": blob["sha"]}],
    })
    sn = sys.argv[3] if len(sys.argv) > 3 else "SN-?"

    # CLAIM CHECK (mechanical collision guard): refuse to stage under an SN number
    # already claimed anywhere on the branch tree. First claim stands; the caller
    # must take the next free number. Prevents the SN-0449 / SN-0455 / SN-0457
    # class of collisions (2026-10-06).
    import re
    m = re.fullmatch(r"SN-(\d+)", sn)
    if m:
        claimed_seg = f"/SN-{m.group(1)}/"
        try:
            full_tree = api("GET", f"/git/trees/{base_tree}?recursive=1")
            taken = set()
            collision_paths = []
            for e in full_tree.get("tree", []):
                p = e.get("path", "")
                mm = re.search(r"/SN-(\d+)/", p)
                if mm:
                    taken.add(int(mm.group(1)))
                if claimed_seg in p and p != repo_path:
                    collision_paths.append(p)
            if collision_paths:
                nxt = (max(taken) + 1) if taken else int(m.group(1)) + 1
                print(
                    f"COLLISION REFUSED: {sn} already claimed on branch "
                    f"(e.g. {collision_paths[0]}). First claim stands — "
                    f"re-stage with the next free number (SN-{nxt:04d}).",
                    file=sys.stderr,
                )
                sys.exit(2)
        except SystemExit:
            raise
        except Exception as ex:
            print(f"warn: claim check failed ({ex}), continuing")
    ident = seat_identity()  # t0796: parameterized by executing seat
    new_commit = api("POST", "/git/commits", {
        "message": f"docs(smart-notes): add {sn} (CANDIDATE) — proactive capture",
        "tree": new_tree["sha"],
        "parents": [tip],
        "author": ident,
        "committer": ident,
    })
    api("PATCH", f"/git/refs/heads/{urllib.parse.quote(BRANCH, safe='')}", {"sha": new_commit["sha"]})
    print(f"STAGED {repo_path} -> {new_commit['sha'][:8]}")

if __name__ == "__main__":
    main()
