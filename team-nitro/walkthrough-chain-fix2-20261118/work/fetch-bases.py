#!/usr/bin/env python3
"""Fetch base blobs for fix2 via gh-direct blob API, write + verify locally."""
import base64, hashlib, json, os, subprocess, sys

HOME = os.path.expanduser("~")
GH = os.path.join(HOME, "workspace/team-nitro/gh-direct.py")
OUT = os.path.join(HOME, "workspace/team-nitro/walkthrough-chain-fix2-20261118/work")
BLOBS = {
    "welcome-base.html": "5ac2054de7477c97af50125660832ac08f80fe85",
    "identity-base.html": "98b0efc0ca79bd91d5c31203eb1b264aa298985d",
    "worker-base.js": "b3001cfe6099882e2801e146975bda8ed8ffaec3",
    "builder-base.py": "b5e6ef6a09831362acd6bdfa78b3ff32de3067d3",
}
EXPECTED = {
    "welcome-base.html": ("1854672", "1a48347f9f7907c1404f3086302c6e7554a3e74ea6f898574da2dca90f3936ae"),
    "identity-base.html": ("387458", "d8c0d583e16f70194227b017db42980c2d4507283292475c5a8fde9c0fc46219"),
    "worker-base.js": ("8321721", "9a993d2d70cdf7d565fd30656d121ebb1184850840e8d58c75d2629df7545473"),
    "builder-base.py": ("90333", "1cf5500ce01abf54191109f7146509d4130fac1e1b388709253bd89f742889fe"),
}

def gh(method, path):
    p = subprocess.run([sys.executable, GH, method, path], capture_output=True)
    out = p.stdout.decode("utf-8", "replace")
    lines = out.split("\n", 1)
    status = int(lines[0].split()[1]) if lines and lines[0].startswith("HTTP") else -1
    payload = lines[1] if len(lines) > 1 else ""
    if status >= 400:
        raise RuntimeError("GH %s %s -> %s %s" % (method, path, status, payload[:400]))
    return json.loads(payload)

def write_resilient(path, data):
    for attempt in range(20):
        try:
            tmp = path + ".tmpf2"
            with open(tmp, "wb") as f:
                for i in range(0, len(data), 8192):
                    f.write(data[i:i+8192])
                f.flush(); os.fsync(f.fileno())
            got = open(tmp, "rb").read()
            if len(got) == len(data) and hashlib.sha256(got).hexdigest() == hashlib.sha256(data).hexdigest():
                os.replace(tmp, path)
                got2 = open(path, "rb").read()
                assert len(got2) == len(data) and hashlib.sha256(got2).hexdigest() == hashlib.sha256(data).hexdigest()
                return
        except Exception as e:
            print("write retry %s: %r" % (path, e), flush=True)
        import time; time.sleep(2)
    raise RuntimeError("write failed: " + path)

for name, blob in BLOBS.items():
    d = gh("GET", "/repos/SoulSchoolAcademy/NayaPOWER/git/blobs/" + blob)
    raw = base64.b64decode(d["content"])
    exp_size, exp_sha = EXPECTED[name]
    ok = str(len(raw)) == exp_size and hashlib.sha256(raw).hexdigest() == exp_sha
    print("%s: %d B sha %s expected-size-ok=%s sha-ok=%s" % (name, len(raw), hashlib.sha256(raw).hexdigest()[:12], str(len(raw)) == exp_size, hashlib.sha256(raw).hexdigest() == exp_sha), flush=True)
    assert ok, "base mismatch for " + name
    write_resilient(os.path.join(OUT, name), raw)
    print("wrote " + name, flush=True)
print("ALL BASES VERIFIED", flush=True)
