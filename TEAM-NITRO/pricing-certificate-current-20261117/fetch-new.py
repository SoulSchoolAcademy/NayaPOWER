#!/usr/bin/env python3
"""Fetch staged /free bytes via the proven _sim client and write them to
/tmp/cert-new-check.html for the design-laws checker. Retries the fetch
(IncompleteRead) and the write (EPERM flake) separately."""
import hashlib
import importlib.util
import os
import sys
import time

sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
sys.path.insert(0, os.path.expanduser("~/workspace/ninaya/integration"))

spec = importlib.util.spec_from_file_location(
    "btaken", "/home/hatch/workspace/team-nitro/pricing-taken-state-fix-20261117/build-taken-fix.py")
_bt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(_bt)
_sim = _bt._sim

URL = "https://naya-pricing-free-staging.nayapower.workers.dev/free"
WANT = "1e1bb4894b3e4bffed026781ac08976e8353b0e2bb020652357f567a711b16a3"
OUT = "/tmp/cert-new-check.html"

data = None
for attempt in range(8):
    try:
        st, _, got = _sim.http_get(URL)
        assert st == 200, f"HTTP {st}"
        data = got if isinstance(got, bytes) else got.encode()
        assert hashlib.sha256(data).hexdigest() == WANT, \
            f"sha moved: {hashlib.sha256(data).hexdigest()}"
        print(f"fetched {len(data)} B sha MATCH (attempt {attempt})")
        break
    except Exception as e:
        print(f"fetch attempt {attempt} failed: {type(e).__name__}: {e}")
        time.sleep(5)
assert data is not None, "fetch never succeeded"

for attempt in range(8):
    try:
        with open(OUT, "wb") as f:
            f.write(data)
        got_size = os.path.getsize(OUT)
        assert got_size == len(data), f"wrote {got_size} of {len(data)}"
        print(f"wrote {OUT}: {got_size} B OK (attempt {attempt})")
        break
    except OSError as e:
        print(f"write attempt {attempt} failed: {e}")
        time.sleep(5)
else:
    raise SystemExit("write never succeeded — EPERM flake still up")
