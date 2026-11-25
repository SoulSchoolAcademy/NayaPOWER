#!/usr/bin/env python3
"""Add MAKER-REPORT.md to branch jewel-icon-set-20261124 (second commit).
Same gh-direct in-memory-token git-data API as file-jewel-to-github.py."""
import base64
import hashlib
import importlib.util
import json
import urllib.request
import urllib.error

BRANCH = "jewel-icon-set-20261124"
REPO = "SoulSchoolAcademy/NayaPOWER"
PATH = "TEAM-NITRO/jewel-icon-set-20261124/MAKER-REPORT.md"
LOCAL = "/home/hatch/workspace/team-nitro/jewel-icon-set-20261124/maker/MAKER-REPORT.md"

spec = importlib.util.spec_from_file_location(
    "ghdirect", "/home/hatch/workspace/team-nitro/gh-direct.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
token = mod.get_token()
HEADERS = {"Accept": "application/vnd.github+json",
           "X-GitHub-Api-Version": "2022-11-28",
           "Authorization": f"Bearer {token}",
           "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
           "Content-Type": "application/json"}


def api(method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(mod.BASE + path, method=method,
                                 headers=HEADERS, data=data)
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")
        print(f"API {method} {path} -> HTTP {e.code}: {detail[:600]}")
        raise


with open(LOCAL, "rb") as f:
    data = f.read()
expected = hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()
blob = api("POST", f"/repos/{REPO}/git/blobs",
           {"content": base64.b64encode(data).decode(), "encoding": "base64"})
print(f"blob: {blob['sha']} (expect {expected}) size: {len(data)}")
assert blob["sha"] == expected, "BLOB MISMATCH"

ref = api("GET", f"/repos/{REPO}/git/ref/heads/{BRANCH}")
parent = ref["object"]["sha"]
commit0 = api("GET", f"/repos/{REPO}/git/commits/{parent}")
tree = api("POST", f"/repos/{REPO}/git/trees",
           {"base_tree": commit0["tree"]["sha"],
            "tree": [{"path": PATH, "mode": "100644", "type": "blob",
                      "sha": blob["sha"]}]})
print(f"tree: {tree['sha']}")
commit = api("POST", f"/repos/{REPO}/git/commits",
             {"message": "Jewel icon set — maker report\n\nMaker report for the 2026-11-24 jewel icon set round: activation,\nharvest table, colour assignment, §11 check, law-check counts,\nverification receipts, and what is still owed. Staged only.",
              "tree": tree["sha"], "parents": [parent]})
print(f"commit: {commit['sha']}")
upd = api("PATCH", f"/repos/{REPO}/git/ref/heads/{BRANCH}",
          {"sha": commit["sha"]})
print(f"ref: {upd['ref']} -> {upd['object']['sha']}")
back = api("GET", f"/repos/{REPO}/git/ref/heads/{BRANCH}")
print(f"verify ref: {back['object']['sha']} (expect {commit['sha']})")
print("VERIFY:", "OK" if back["object"]["sha"] == commit["sha"] else "FAILED")
