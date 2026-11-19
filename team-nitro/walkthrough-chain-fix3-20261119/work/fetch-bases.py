#!/usr/bin/env python3
"""FIX3 fetch bases — walkthrough chain fix round 3.
Fetches the fix2 blobs via the git blob API, verifies sha256+size,
writes them to work/bases/ with resilient chunked writes.
"""
import base64, hashlib, json, os, subprocess, sys, time

HOME = os.path.expanduser("~")
WORK = os.path.join(HOME, "workspace/team-nitro/walkthrough-chain-fix3-20261119/work")
BASES = os.path.join(WORK, "bases")
GH = os.path.join(HOME, "workspace/team-nitro/gh-direct.py")
REPO = "SoulSchoolAcademy/NayaPOWER"
BLOBS = {
    "welcome-staged.html": ("868c746d1219b376419e8d49631dcd920256b45f",
        "c8581fca0a697204a94d64b17b28e5ae67ef70d887fd95dd2cdd5b8ba1815d03", 1857688),
    "identity-fixed.html": ("c0a351221d48948d950dba0146e393709790e435",
        "803e7ea8a7822f8f1e5942913615ca62bfec81e54b28bb4a05924134322bd617", 388608),
    "build-v23-staging-worker.py": ("582b2804a4ef4e6d80bb7b2fa02170d1c5f3a16c",
        "0cd80c8532baf7de159cfdef6ff5108ed57242c0448a02ef58cdee1295ad7003", 90917),
    "walk-beginning-staging-worker.js": ("95191dfde4b9dc92be4007a5e92da3bf235467ae",
        "2a348c2d6354646142202ce3709f28417a8276c847decca70f4dcfdefaf599d0", 8326561),
}

def sha(b):
    return hashlib.sha256(b).hexdigest()

def gh_blob(blob_sha):
    p = subprocess.run([sys.executable, GH, "GET",
        "/repos/%s/git/blobs/%s" % (REPO, blob_sha)],
        capture_output=True)
    out = p.stdout.decode("utf-8", "replace")
    lines = out.split("\n", 1)
    status = int(lines[0].split()[1]) if lines and lines[0].startswith("HTTP") else -1
    if status != 200:
        raise RuntimeError("blob %s HTTP %s: %s" % (blob_sha, status, out[:400]))
    d = json.loads(lines[1])
    if d.get("encoding") != "base64":
        raise RuntimeError("unexpected encoding %r" % d.get("encoding"))
    return base64.b64decode(d["content"])

def write_resilient(path, data, attempts=40):
    tmp = path + ".tmp-fix3"
    last = None
    for n in range(attempts):
        try:
            with open(tmp, "wb") as f:
                for i in range(0, len(data), 8192):
                    f.write(data[i:i + 8192])
                f.flush()
                os.fsync(f.fileno())
            got = open(tmp, "rb").read()
            if len(got) == len(data) and sha(got) == sha(data):
                os.replace(tmp, path)
                got2 = open(path, "rb").read()
                if len(got2) == len(data) and sha(got2) == sha(data):
                    print("wrote %s %d B sha %s" % (path, len(data), sha(data)[:12]), flush=True)
                    return
        except Exception as e:
            last = e
        time.sleep(2)
    raise RuntimeError("write_resilient failed for %s: %r" % (path, last))

os.makedirs(BASES, exist_ok=True)
for name, (blob, expect_sha, expect_size) in BLOBS.items():
    data = gh_blob(blob)
    assert len(data) == expect_size, (name, len(data), expect_size)
    assert sha(data) == expect_sha, (name, sha(data), expect_sha)
    print("OK blob %s %d B sha %s" % (name, len(data), sha(data)[:12]), flush=True)
    write_resilient(os.path.join(BASES, name), data)
print("ALL BASES VERIFIED")
