#!/usr/bin/env python3
"""Self-healing revert for FULL-AUTO-MERGE-V1 hardening clause H3.

Rule: if an auto-merge turns the verification battery red, the merge is
automatically reverted and the evidence is posted to #1354. The loop heals
itself; no human needed.

This helper performs the revert half. The battery watch (which already
observes every main move) decides WHEN to call it; this script decides
whether a revert is SAFE and executes it.

Safety rule: revert is only automatic when the offending merge commit is
still the main tip. Otherwise later work sits on top and an automatic
revert could destroy it -> refuse and escalate to the human director.

Usage:
    python3 tools/auto_merge_self_heal.py <merge_sha> <evidence_json_path>

evidence_json_path: JSON with {"battery": "...", "failing_checks": [...],
"detected_at": "...", "reported_by": "..."} — posted to #1354 with the revert.

Stdlib only. Uses ~/workspace/naya/bin/gh-api for GitHub API calls.
"""

import json
import os
import subprocess
import sys

REPO = "SoulSchoolAcademy/NayaPOWER"
GH_API = os.path.expanduser("~/workspace/naya/bin/gh-api")
BOARD_ISSUE = 1354


def api(method, path, body=None):
    cmd = [GH_API, method, path]
    if body is not None:
        cmd.append(json.dumps(body))
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if proc.returncode != 0:
        raise RuntimeError(f"gh-api {method} {path} failed: {proc.stderr[:500]}")
    return json.loads(proc.stdout or "{}")


def main(argv):
    if len(argv) != 3:
        print("usage: python3 tools/auto_merge_self_heal.py <merge_sha> <evidence_json>",
              file=sys.stderr)
        return 2
    merge_sha, evidence_path = argv[1], argv[2]
    try:
        with open(evidence_path, "r", encoding="utf-8") as fh:
            evidence = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"reverted": False, "error": f"bad evidence file: {exc}"}))
        return 2

    # 1. Is the offending merge still the tip? If not, refuse — escalate.
    main_ref = api("GET", f"/repos/{REPO}/git/refs/heads/main")
    tip_sha = main_ref["object"]["sha"]
    if tip_sha != merge_sha:
        msg = (f"H3 self-heal REFUSED: merge {merge_sha} is not the main tip "
               f"(tip is {tip_sha}). Later work sits on top; automatic revert "
               "could destroy it. Escalating to the human director.")
        print(json.dumps({"reverted": False, "escalated": True, "reason": msg}))
        return 1

    # 2. Build the revert commit: tree = first parent's tree (pre-merge state).
    merge_commit = api("GET", f"/repos/{REPO}/git/commits/{merge_sha}")
    parents = merge_commit.get("parents", [])
    if len(parents) < 2:
        print(json.dumps({"reverted": False, "escalated": True,
                          "reason": f"{merge_sha} is not a merge commit; refusing"}))
        return 1
    pre_merge_tree = parents[0]["sha"]
    parent_tree = api("GET", f"/repos/{REPO}/git/commits/{pre_merge_tree}")["tree"]["sha"]

    revert_body = {
        "message": (
            f"Revert auto-merge {merge_sha}\n\n"
            "H3 self-heal (FULL-AUTO-MERGE-V1): the merge turned the "
            "verification battery red. Reverting to pre-merge tree.\n"
            f"Evidence: {json.dumps(evidence)}"
        ),
        "tree": parent_tree,
        "parents": [tip_sha],
    }
    revert_commit = api("POST", f"/repos/{REPO}/git/commits", revert_body)
    revert_sha = revert_commit["sha"]

    # 3. Move main to the revert commit (fast-forward: tip is still merge_sha).
    api("PATCH", f"/repos/{REPO}/git/refs/heads/main",
        {"sha": revert_sha, "force": False})

    # 4. Post the evidence + revert receipt to the board.
    board_body = (
        "## [H3 SELF-HEAL] auto-merge reverted\n\n"
        f"Merge `{merge_sha}` turned the verification battery red and has been "
        f"automatically reverted (`{revert_sha}`). The loop healed itself.\n\n"
        f"**Evidence:**\n```json\n{json.dumps(evidence, indent=2)}\n```\n\n"
        "Owning seat: re-score the decision and re-propose repaired, or escalate."
    )
    with open("/tmp/h3_self_heal_board.md", "w", encoding="utf-8") as fh:
        fh.write(board_body)
    api("POST", f"/repos/{REPO}/issues/{BOARD_ISSUE}/comments",
        {"body": board_body})

    print(json.dumps({"reverted": True, "revert_sha": revert_sha,
                      "reverted_merge": merge_sha}))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
