#!/usr/bin/env python3
"""Diff the repair build against the third-surface tip (in memory):
fetch tip blob from GitHub, run build-repair.py, difflib n=0, count hunks
and list each hunk's first changed line + which F-site it touches."""
import base64, difflib, hashlib, json, subprocess, sys

GH = "/home/hatch/workspace/team-nitro/gh-direct.py"
REPO = "SoulSchoolAcademy/NayaPOWER"
BLOB = "ce42cec8d4c18f6b89eccab8ff20d7b9a6221ee2"
out = subprocess.run(["python3", GH, "GET", f"/repos/{REPO}/git/blobs/{BLOB}"],
                     capture_output=True, text=True, timeout=120)
lines = out.stdout.splitlines()
body = "\n".join(lines[1:]) if lines and lines[0].startswith("HTTP ") else out.stdout
tip = base64.b64decode(json.loads(body)["content"]).decode("utf-8")
print("tip sha:", hashlib.sha256(tip.encode()).hexdigest(), "lines:", tip.count("\n") + 1, file=sys.stderr)

b = subprocess.run(["python3", "/home/hatch/workspace/team-nitro/auto-translate-20261113/build-repair.py", "TIP"],
                   capture_output=True, timeout=180)
assert b.returncode == 0, b.stderr.decode()[:500]
built = b.stdout.decode("utf-8")
print("built sha:", hashlib.sha256(b.stdout).hexdigest(), "lines:", built.count("\n") + 1, file=sys.stderr)

a = tip.splitlines()
c = built.splitlines()
hunks = list(difflib.unified_diff(a, c, n=0, lineterm=""))
print("diff lines:", len(hunks))
nh = 0
for ln in hunks:
    if ln.startswith("@@"):
        nh += 1
        print("HUNK", ln.strip())
print("total hunks:", nh)
# changed-line counts
plus = sum(1 for ln in hunks if ln.startswith("+") and not ln.startswith("+++"))
minus = sum(1 for ln in hunks if ln.startswith("-") and not ln.startswith("---"))
print(f"changed lines: +{plus}/-{minus}")
# dict key counts in built
import re as _re
m = _re.search(r"var MW_I18N\s*=\s*(\{.*?\});", built, _re.S)
d = json.loads(m.group(1))
print("built dict keys:", {k: len(v) for k, v in d.items()},
      "empty values:", sum(1 for lang in d for v in d[lang].values() if not v),
      "key sets identical:", len(set(map(lambda l: frozenset(d[l]), d))) == 1)
newkeys = ["Posts, messages and invites together.",
           "A quiet stretch — the next post, message or invite lights the first bar.",
           "A quiet stretch — the next post, message or invite lights the first circle.",
           "A quiet stretch so far — the chart is waiting.",
           "The next post, note, message or invite lights the first circle.",
           "The circles show the story week by week; the totals cover the whole story.",
           "The circles show the last 7 days; the totals cover the full period.",
           "No invites yet — record the first one above.",
           " walked the whole invite journey.",
           "Send a message", "Add a Smart Link", "Add to a list", "Add something",
           "Change picture", "Edit photo", "Hide breakdown"]
for k in newkeys:
    print(("KEY-OK  " if k in d["es"] else "KEY-MISSING  ") + repr(k),
          f"es={d['es'].get(k)!r} fr={d['fr'].get(k)!r} de={d['de'].get(k)!r}" if k in d["es"] else "")
