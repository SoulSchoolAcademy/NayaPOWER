#!/usr/bin/env python3
"""FIX5 proof-host verification (2026-11-19): the proof-host half of the
stage check, run standalone (stage-fix4.py hit a KeyError in its own proof
loop: it looked up blobs['welcome...'] but welcome was not filed in that
commit — it is unchanged from fix3 — and the same holds in fix5). The two
proof-host pages are verified here by pipe-to-sha (curl output hashed in
memory, never a file write — EPERM flake live). Run: python3
verify-proof-fix5.py <identity-blob-sha>
"""
import hashlib, subprocess, sys, time

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")
PROOF = "https://naya-proof-host.nayapower.workers.dev"
BRANCH = "walkthrough/chain-fix5-20261119"
IDENT_BLOB = sys.argv[1] if len(sys.argv) > 1 else "PLACEHOLDER"
CHECKS = (
    ("welcome", "team-nitro/walk-v23-assembly-20261114/welcome-staged.html",
     "d79793c0d9b74121e83c0c65fed095e6d0dd278481b60c7a2b339bbe9231c934",
     "c66e2fa20d2e82a9d10e7eac2d2f11f6a156768f"),
    ("identity", "team-nitro/walk-v23-assembly-20261114/identity-fixed.html",
     "6f805eba00fa7ccbf89103c46878c352e73db5b26792010dc2de535c706418f0",
     IDENT_BLOB),
)

for label, path, want, cb in CHECKS:
    url = "%s/?file=%s&ref=%s&cb=%s&t=%d" % (PROOF, path, BRANCH, cb, int(time.time()))
    r = subprocess.run(["curl", "-s", "-A", UA, url], capture_output=True, timeout=120)
    got = hashlib.sha256(r.stdout).hexdigest()
    print("proof %s: %d B sha=%s (want %s)" % (label, len(r.stdout), got[:12], want[:12]), flush=True)
    assert got == want, "proof-host %s mismatch" % label
print("PROOF-HOST VERIFIED")
