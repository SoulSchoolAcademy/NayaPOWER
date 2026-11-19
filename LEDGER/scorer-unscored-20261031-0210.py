import json, os, re
base = "/home/hatch/workspace/goals/bring-naya-to-life/hidden_files"
rdir = os.path.join(base, "twelve-lane-receipts")
scored_receipts = set()
scored_tick_lane = set()
n = 0
for line in open(os.path.join(base, "twelve-lane-scores.jsonl")):
    try:
        j = json.loads(line)
    except Exception:
        continue
    n += 1
    if j.get("agent") == "Team Naya Scorer":
        if j.get("receipt"):
            scored_receipts.add(j["receipt"])
        try:
            scored_tick_lane.add((str(j.get("tick")), int(j.get("lane"))))
        except Exception:
            pass
print("score rows", n, "scorer receipts", len(scored_receipts))
rows = []
for fn in sorted(os.listdir(rdir)):
    p = os.path.join(rdir, fn)
    mt = os.path.getmtime(p)
    m = re.match(r"t(\d+)-lane(\d+)\.md$", fn)
    key_hit = False
    if m:
        t, l = int(m.group(1)), int(m.group(2))
        for cand in (("t%04d" % t), ("t%d" % t), str(t)):
            if (cand, l) in scored_tick_lane:
                key_hit = True
    unscored = (fn not in scored_receipts) and not key_hit
    rows.append((mt, fn, unscored))
unsc = [r for r in rows if r[2]]
print("total receipts", len(rows), "unscored by receipt-or-ticklane", len(unsc))
print("--- newest 25 unscored by mtime ---")
for mt, fn, _ in sorted(unsc, reverse=True)[:25]:
    print(fn)
print("--- newest 10 scored ---")
sc = [r for r in rows if not r[2]]
for mt, fn, _ in sorted(sc, reverse=True)[:10]:
    print(fn)
print("--- oldest unscored lane t-pattern ---")
lane_unsc = [fn for _, fn, u in rows if u and re.match(r"t\d+-lane\d+\.md$", fn)]
print(len(lane_unsc), lane_unsc[:20])
