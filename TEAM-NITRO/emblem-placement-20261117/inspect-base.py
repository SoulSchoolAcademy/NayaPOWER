#!/usr/bin/env python3
"""Verify emblem round base: branch pricing/certificate-fix-20261117 tip,
fetch fixed-entry.html blob via the BLOB API (never contents API for >1MB),
sha256-check it, and dump the certificate structure for the survey."""
import base64, hashlib, importlib.util, json, sys
spec = importlib.util.spec_from_file_location("gh_direct", "/home/hatch/workspace/team-nitro/gh-direct.py")
gh = importlib.util.module_from_spec(spec); spec.loader.exec_module(gh)
REPO = "SoulSchoolAcademy/NayaPOWER"
BASE_BRANCH = "pricing/certificate-fix-20261117"
def call(method, path, body=None):
    import urllib.request, urllib.error
    req = urllib.request.Request("https://api.github.com"+path,
        data=json.dumps(body).encode() if body is not None else None, method=method,
        headers={"Accept":"application/vnd.github+json","X-GitHub-Api-Version":"2022-11-28",
                 "Authorization":f"Bearer {gh.get_token()}","Content-Type":"application/json",
                 "User-Agent":"muse-github-skill/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r: return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8","replace")
        try: return e.code, json.loads(raw)
        except json.JSONDecodeError: return e.code, {"raw": raw[:300]}
st, ref = call("GET", f"/repos/{REPO}/git/ref/heads/{BASE_BRANCH}")
print("ref:", st, ref.get("object",{}).get("sha") if st==200 else ref)
tip = ref["object"]["sha"]
st, c = call("GET", f"/repos/{REPO}/git/commits/{tip}")
print("tip commit:", st, c.get("message","")[:160] if st==200 else c, "| tree:", c.get("tree",{}).get("sha") if st==200 else "")
st, blob = call("GET", "/repos/{}/git/blobs/67334408be3ae947ade81c11372dc173e6d47358".format(REPO))
print("blob:", st, "size:", blob.get("size") if st==200 else blob)
raw = base64.b64decode(blob["content"])
print("decoded:", len(raw), "B sha256:", hashlib.sha256(raw).hexdigest())
open("/home/hatch/workspace/team-nitro/emblem-placement-20261117/base-entry.html","wb").write(raw)
