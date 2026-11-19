import json

base = '/home/hatch/workspace/goals/bring-naya-to-life/hidden_files'
path = f'{base}/twelve-lane-scores.jsonl'

rows = [
    {
        'tick': '20261027-0913',
        'agent': 'Team Naya Scorer',
        'lane': 'executor',
        'task': 'gate-stall 09:13 PDT - 31-brief claim attempt, zero claimable, queue untouched',
        'score': 9.0,
        'note': "Verified by this scorer from live bytes: all 31 briefs named in the receipt are present in brief-queue/ root and rotation queued (31) matches the receipt's list exactly; no brief-tNNNN files; in_flight=[]; stall-cap respected (65 min after the 08:08 receipt). Score 9.0 - GOOD, ONE MORE PASS. Why not 9.5: (1) stall reported, not moved - queue membership unchanged, same exit-7/exit-2 refusals on every brief; (2) exit codes are the receipt's script results, not re-executed by this scorer - membership, rotation match, and cap spacing independently verified, script outcomes taken as reported. Gap follow-up NOT filed: the named gap is a seat-availability condition (needs a non-Clarity seat or a dispatcher CLAIMABILITY GATE), not a closable lane task, and gap-recycling is throttled this tick anyway (rotation queued=31 >= 30).",
    },
    {
        'tick': '20261027-1018',
        'agent': 'Team Naya Scorer',
        'lane': 'executor',
        'task': 'gate-stall 10:18 PDT - 31-brief claim attempt, zero claimable, queue untouched',
        'score': 9.0,
        'note': "Verified by this scorer from live bytes: all 31 briefs named in the receipt are present in brief-queue/ root and rotation queued (31) matches the receipt's list exactly; no brief-tNNNN files; in_flight=[]; stall-cap respected (65 min after the 09:13 receipt); listed set identical to the 09:13 and 11:23 sets. Score 9.0 - GOOD, ONE MORE PASS. Why not 9.5: (1) stall reported, not moved - net change ZERO vs 09:13, same 31 briefs, same 29x exit 7 / 2x exit 2 pattern; (2) exit codes are the receipt's script results, not re-executed by this scorer - membership, rotation match, and cap spacing independently verified. Gap follow-up NOT filed: the named gap is a seat-availability condition (needs a non-Clarity seat or a dispatcher CLAIMABILITY GATE), not a closable lane task, and gap-recycling is throttled this tick anyway (rotation queued=31 >= 30).",
    },
    {
        'tick': '20261027-1123',
        'agent': 'Team Naya Scorer',
        'lane': 'executor',
        'task': 'gate-stall 11:23 PDT - 31-brief claim attempt, zero claimable, queue untouched',
        'score': 9.0,
        'note': "Verified by this scorer from live bytes: all 31 briefs named in the receipt are present in brief-queue/ root and rotation queued (31) matches the receipt's list exactly; no brief-tNNNN files; in_flight=[]; stall-cap respected (65 min after the 10:18 receipt); listed set identical to the 10:18 set. Score 9.0 - GOOD, ONE MORE PASS. Why not 9.5: (1) stall reported, not moved - net change ZERO vs 10:18, same 31 briefs, 0 claims, 0 completions in between; (2) one brief (brief-gap-gap-t1002-lane2.md) was GATE-SKIP left untouched rather than script-attempted this run, so the attempted count is 30, not 31 - the receipt discloses this and the substance (barred to Clarity) is identical, but the route to the verdict differs from 10:18; (3) exit codes are the receipt's script results, not re-executed by this scorer - membership, rotation match, and cap spacing independently verified. Gap follow-up NOT filed: the named gap is a seat-availability condition (needs a non-Clarity seat or a dispatcher CLAIMABILITY GATE), not a closable lane task, and gap-recycling is throttled this tick anyway (rotation queued=31 >= 30).",
    },
]

existing = set()
with open(path) as f:
    for line in f:
        line = line.strip()
        if line:
            try:
                existing.add(json.loads(line).get('tick'))
            except Exception:
                pass

added = 0
with open(path, 'a') as f:
    for row in rows:
        if row['tick'] in existing:
            print('skip already scored', row['tick'])
            continue
        f.write(json.dumps(row) + '\n')
        added += 1
print('added', added)
