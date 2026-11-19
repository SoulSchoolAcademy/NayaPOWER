#!/usr/bin/env python3
"""FIX6 proof-host verification (2026-11-19): the three changed/unchanged
proof-host pages verified by pipe-to-sha (curl output hashed in memory,
never a file write — EPERM flake live). Run: python3
verify-proof-fix6.py <identity-blob-sha> <walk-blob-sha>
Walk is included this round because the walk changed (fix5 checked only
welcome + identity; welcome is unchanged from fix3 and is not filed in
the fix6 commit — never look it up in this commit's blobs).
"""
import hashlib, subprocess, sys, time

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")
PROOF = "https://naya-proof-host.nayapower.workers.dev"
BRANCH = "walkthrough/chain-fix6-20261119"
IDENT_BLOB = sys.argv[1] if len(sys.argv) > 1 else "PLACEHOLDER"
WALK_BLOB = sys.argv[2] if len(sys.argv) > 2 else "PLACEHOLDER"
CHECKS = (
    ("welcome", "team-nitro/walk-v23-assembly-20261114/welcome-staged.html",
     "d79793c0d9b74121e83c0c65fed095e6d0dd278481b60c7a2b339bbe9231c934",
     "c66e2fa20d2e82a9d10e7eac2d2f11f6a156768f"),
    ("identity", "team-nitro/walk-v23-assembly-20261114/identity-fixed.html",
     "3279dc3572337e5e971369a3742effcaac7f6e5b059192ddaa6e689f0f92886c",
     IDENT_BLOB),
    ("walk", "team-nitro/walk-v23-assembly-20261114/walk-beginning-fixed.html",
     "b6befc332d65dd26d01649edd09810e9f83284a73a10a6af30f6691f5f118773",
     WALK_BLOB),
)

for label, path, want, cb in CHECKS:
    url = "%s/?file=%s&ref=%s&cb=%s&t=%d" % (PROOF, path, BRANCH, cb, int(time.time()))
    r = subprocess.run(["curl", "-s", "-A", UA, url], capture_output=True, timeout=180)
    got = hashlib.sha256(r.stdout).hexdigest()
    print("proof %s: %d B sha=%s (want %s)" % (label, len(r.stdout), got[:12], want[:12]), flush=True)
    assert got == want, "proof-host %s mismatch" % label
print("PROOF-HOST VERIFIED")
