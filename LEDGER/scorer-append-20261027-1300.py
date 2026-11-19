import json

base = '/home/hatch/workspace/goals/bring-naya-to-life/hidden_files'
path = f'{base}/twelve-lane-scores.jsonl'

rows = [
    {
        'tick': 't0412',
        'agent': 'Team Naya Scorer',
        'lane': 3,
        'task': 'Stage-0 [REPLAY] slice 1 - 3 high-stakes decisions replayed against the 15 principles',
        'score': 8.5,
        'note': "Verified by this scorer from live bytes: hidden_files/lane-3/t0412/replay-report.md present (11764 bytes, D1/D2/D3 each with quoted pins, counter-principle run, delta); cited receipts t972-lane3, t1442-lane8, t942-lane5 all present on disk; strict-bar proof script and the 20261012T070849Z decision json present. No branch/SHA applies - read-only authority, so no PHANTOM. Score 8.5 - REWORK band. Why not 9.5: (1) D1 replays the lane's own seat work - self-replay bias disclosed but not cured; (2) all three deltas returned SAME, so the method is shown to run, not shown to bite - no observed flipped verdict; (3) lane-feed sign-in skipped (disclosed, read-only authority cited over template boilerplate). Gap follow-up NOT filed: 8.5 is below the 9.0-9.4 gap-recycling band.",
    },
    {
        'tick': 't0525',
        'agent': 'Team Naya Scorer',
        'lane': 9,
        'task': 'FP-003 feedback - receipt-evidence verdict + registry-allocator existence check on disk',
        'score': 9.0,
        'note': "Verified by this scorer from live bytes: feedback-feed.md carries the Lane 9 t0525 FP-003 entry (line 437 at read time; receipt's line-300 pin predates later file growth); bin/stage_smart_note.py claim check present at lines ~60-91, scanning the branch tree and exiting 2 with 'First claim stands' on collision - the detect-and-refuse allocator verdict independently confirmed; smart-notes-counter.md present. Score 9.0 - GOOD, ONE MORE PASS. Why not 9.5: (1) receipt-gate binaries not re-run on disk this tick - the verdict leans on the journal's t0492 rules, as the receipt itself admits; (2) the collision guard's refusal arm is still untested - no post-guard exit-2 collision event on disk; (3) the Lane 10 FP-002/FP-003 misfile is flagged, not resolved (dispatcher-owned). Gap follow-up NOT filed: GAP-RECYCLE THROTTLED - rotation queued=31 >= 30, zero follow-ups this tick.",
    },
]

existing = set()
with open(path) as f:
    for line in f:
        line = line.strip()
        if line:
            try:
                r = json.loads(line)
                if r.get('agent') == 'Team Naya Scorer':
                    existing.add((r.get('tick'), r.get('lane')))
            except Exception:
                pass

added = 0
with open(path, 'a') as f:
    for row in rows:
        if (row['tick'], row['lane']) in existing:
            print('skip already scored', row['tick'], row['lane'])
            continue
        f.write(json.dumps(row) + '\n')
        added += 1
print('added', added)
