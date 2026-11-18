#!/usr/bin/env python3
"""Fetch the live staged /free and sha-verify it against the filed fix
bytes (entry 335,915 B, sha fbd6477f...). Mirrors fetch-new.py.
Run any time: a mismatch means staging moved and the round stops.
"""
import hashlib
import importlib.util
import os
import sys

sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
sys.path.insert(0, os.path.expanduser("~/workspace/ninaya/integration"))

FIXDIR = os.path.expanduser("~/workspace/team-nitro/pricing-certificate-fix-20261117")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_bt = load("bt", os.path.expanduser(
    "~/workspace/team-nitro/pricing-certificate-current-20261117/build-certificate.py"))._bt
_sim = _bt._sim

WANT = "fbd6477f348ab50b8b0eb278fb36e475c25eb55ae27a4d79ca416942161f16fd"
URL = "https://naya-pricing-free-staging.nayapower.workers.dev/free"

st, _, got = _sim.http_get(URL)
assert st == 200, f"GET {URL}: {st}"
got_sha = hashlib.sha256(got).hexdigest()
print(f"live staged /free: {len(got)} B sha256={got_sha}")
assert got_sha == WANT, f"MISMATCH — want {WANT}"
print("MATCH — staged /free == filed fix bytes")
