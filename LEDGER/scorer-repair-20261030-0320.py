import json
p = "/home/hatch/workspace/goals/bring-naya-to-life/hidden_files/twelve-lane-scores.jsonl"
lines = open(p).read().splitlines()
bad_idx = None
for i, line in enumerate(lines):
    try:
        json.loads(line)
    except Exception:
        bad_idx = i
        break
assert bad_idx is not None, "no bad line"
line = lines[bad_idx]
marker = '{"tick": "t0700", "agent": "Team Naya Scorer", "lane": 5'
pos = line.index(marker)
first, second = line[:pos], line[pos:]
a = json.loads(first)
b = json.loads(second)
print("split ok:", a.get("receipt"), "|", b.get("receipt"), b.get("score"))
lines[bad_idx:bad_idx + 1] = [first, second]
with open(p, "w") as f:
    for ln in lines:
        f.write(ln + "\n")
# re-validate whole file
bad = 0
for ln in open(p):
    try:
        json.loads(ln)
    except Exception:
        bad += 1
print("total lines:", len(lines), "bad after repair:", bad)
