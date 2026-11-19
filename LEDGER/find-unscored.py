import json, os, re
base = "/home/hatch/workspace/goals/bring-naya-to-life/hidden_files"
receipts_dir = os.path.join(base, "twelve-lane-receipts")
scored = set()
allrows = 0
for line in open(os.path.join(base, "twelve-lane-scores.jsonl")):
    try:
        j = json.loads(line)
    except Exception:
        continue
    allrows += 1
    if j.get("agent") == "Team Naya Scorer":
        try:
            scored.add((str(j.get("tick")), int(j.get("lane"))))
        except Exception:
            pass
print("total score rows:", allrows)
print("independent scorer rows:", len(scored))
receipts = []
for fn in sorted(os.listdir(receipts_dir)):
    m = re.match(r"t(\d+)-lane(\d+)\.md$", fn)
    if m:
        receipts.append((int(m.group(1)), int(m.group(2)), fn))
receipts.sort()
print("lane receipts:", len(receipts))
unscored = [(t, l, fn) for (t, l, fn) in receipts if (("t%04d" % t), l) not in scored and (("t%d" % t), l) not in scored and (str(t), l) not in scored]
print("unscored:", len(unscored))
# also check raw tick string variants present in scored
for t, l, fn in unscored:
    print(t, l, fn)
print("--- latest scored ticks ---")
# max tick among scored
nums = []
for tick, lane in scored:
    mm = re.match(r"t(\d+)", tick)
    if mm:
        nums.append(int(mm.group(1)))
print("max scored tick num:", max(nums) if nums else None)
print("--- unscored sorted by tick desc (fresh) ---")
for t, l, fn in sorted(unscored, reverse=True)[:40]:
    print(t, l, fn)
