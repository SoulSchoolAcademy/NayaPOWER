#!/usr/bin/env python3
"""Fetch fix-3 base files via the git blob API, write to disk, verify size+sha256.
Usage: python3 fetch-base.py   (run from maker/work/)
Uses gh-direct.py's in-memory token minting (never touches the token cache).
The script itself writes the files (never `python3 ... > file`).
"""
import base64, hashlib, importlib.util, json, os, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location(
    "ghdirect", os.path.expanduser("~/workspace/team-nitro/gh-direct.py"))
ghd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ghd)

FILES = [
    ("agreement-unfold-fixed.html", "f7f919db59dbaafbfc76b0bdfaebc20b85651e8a", 142120,
     "50876fff8caa79eeb3d6d75b4d2099db39ade2688edf6762e58ac9083eb0d26b"),
    ("welcome-staged.html", "4830958834321eea8d647b82daea47b6968f998c", 1929575,
     "3874b7ebcc6b95e2a7ef2d320ed95e13253083a954fe6c0efc36afe6d58fa747"),
    ("walk-beginning-fixed.html", "5f914291abb84d6e61e27b98f9b376a4386d9900", 4363264,
     "ef98226767ddbb507b7e8282a64c72e4c741b3bf0b38413985484798dbc7464f"),
    ("identity-fixed.html", "2d1266553ecde92ad0f4febfdf154ca4a445cc27", 402647,
     "51776174b59cee4a39f7a00eb7f7b874fc33103a0235308a876d4a94179307f5"),
    ("walk-beginning-staging-worker.js", "da8f3cc8fe4784e86b5195e62b183bffb7297a21", 8459261,
     "cc46798578df4c9b587a2044c5091b600d03bcd0df65a1343776fe10413d11ed"),
    ("build-v23-staging-worker.py", "91ebfe7f4d46aac635c9fa364e04d4ddf5ec5214", 93731,
     "f6107678a0e9eef687637f66bbd1f702744c7d0d1dd3a261734691169fdc9978"),
]

def fetch_blob(sha):
    token = ghd.get_token()
    req = urllib.request.Request(
        f"https://api.github.com/repos/SoulSchoolAcademy/NayaPOWER/git/blobs/{sha}",
        headers={"Accept": "application/vnd.github+json",
                 "X-GitHub-Api-Version": "2022-11-28",
                 "Authorization": f"Bearer {token}",
                 "User-Agent": "muse-github-skill/1.0"})
    with urllib.request.urlopen(req) as resp:
        data = json.load(resp)
    raw = base64.b64decode("".join(data["content"].split()))
    return raw

ok = True
for name, blob, exp_size, exp_sha in FILES:
    path = os.path.join(HERE, name)
    raw = fetch_blob(blob)
    with open(path, "wb") as f:
        f.write(raw)
    size = len(raw)
    sha = hashlib.sha256(raw).hexdigest()
    status = "OK " if (size == exp_size and sha == exp_sha) else "MISMATCH"
    if status != "OK ":
        ok = False
    print(f"{status} {name}: {size} B sha256 {sha} (expected {exp_size} B {exp_sha[:16]}...)")
print("ALL OK" if ok else "FAILURES PRESENT")
sys.exit(0 if ok else 1)
