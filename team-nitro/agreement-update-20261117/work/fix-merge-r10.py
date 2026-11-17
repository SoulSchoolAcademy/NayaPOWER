#!/usr/bin/env python3
"""R10 — pre-existing syntax fix (found by verification, NOT by the brief).
Base root block 1 (returning-citizen script) does not parse: the try at
line 220 is closed by a stray lone '}' at line 237 with no catch, leaving
the catch at line 266 orphaned. node --check + new Function both fail on
the BASE bytes (sha 9eea1703); blocks 0/2 and both /agreement blocks parse.
The stray brace kills the whole returning-citizen block in the browser
(the jump-back-in view + new-account line never wire up). The fix deletes
exactly that one brace, restoring the plainly intended structure
(try 220 -> catch 266). No other byte moves. Proved by node --check
before/after in the run log.
"""
import hashlib
import re
import subprocess
import sys

WORK = "/home/hatch/workspace/team-nitro/agreement-update-20261117/work/"
ROOT = WORK + "welcome-merged.html"

h = open(ROOT, encoding="utf-8").read()
old = "}catch(e){} }\n    }\n    var others=idList.filter"
assert h.count(old) == 1, "R10 anchor count %d != 1" % h.count(old)
h = h.replace(old, "}catch(e){} }\n    var others=idList.filter")
open(ROOT, "w", encoding="utf-8").write(h)
print("root after R10: %d B sha %s" % (len(h.encode()), hashlib.sha256(h.encode()).hexdigest()[:12]))

scripts = re.findall(r'<script>(.*?)</script>', h, re.S)
print("script blocks:", len(scripts))
for k, s in enumerate(scripts):
    p = "/tmp/merged-r10-%d.js" % k
    open(p, "w", encoding="utf-8").write(s)
    r = subprocess.run(["node", "--check", p], capture_output=True, text=True)
    print("block %d: %s" % (k, "PARSES OK" if r.returncode == 0 else "FAIL: " + r.stderr.strip().split("\n")[0]))
    assert r.returncode == 0, "block %d still fails" % k
print("R10 APPLIED AND PROVED")
