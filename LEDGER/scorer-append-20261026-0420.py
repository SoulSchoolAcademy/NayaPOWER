import json

base = '/home/hatch/workspace/goals/bring-naya-to-life/hidden_files'
path = f'{base}/ledger/twelve-lane-scores.jsonl'

rows = [
    {
        'tick': '20261026-0158',
        'agent': 'Team Naya Scorer',
        'lane': 'executor',
        'task': 'seat-stall 01:58 PDT - 24-brief claim attempt, zero claimable, queue untouched',
        'score': 9.0,
        'note': "Verified by this scorer from live bytes: all 24 briefs named in the receipt are present in brief-queue/ root and rotation queued (24) matches the receipt's list exactly; no brief-tNNNN files; queue untouched; stall-cap respected (65 min after the 00:53 receipt). Score 9.0 - GOOD, ONE MORE PASS. Why not 9.5: stall reported, not moved - 15th consecutive hourly stall receipt (10:58 Oct 25 through 01:58 Oct 26) with zero delta vs 00:53, same 24 exit-7 refusals. Gap follow-up NOT filed: the named gap is a seat-availability condition (needs a non-Clarity seat or a dispatcher CLAIMABILITY GATE), not a closable lane task, and any gap brief filed here would itself be exit-7-barred for this seat.",
    },
    {
        'tick': '20261026-0258',
        'agent': 'Team Naya Scorer',
        'lane': 'executor',
        'task': 'seat-stall 02:58 PDT - 24-brief claim attempt, zero claimable, queue untouched',
        'score': 9.0,
        'note': "Verified by this scorer from live bytes: all 24 briefs named in the receipt are present in brief-queue/ root and rotation queued (24) matches the receipt's list exactly; no brief-tNNNN files; queue untouched; stall-cap respected (60 min after the 01:58 receipt). Score 9.0 - GOOD, ONE MORE PASS. Why not 9.5: stall reported, not moved - 16th consecutive hourly stall receipt (10:58 Oct 25 through 02:58 Oct 26) with zero delta vs 01:58, same 24 exit-7 refusals. Gap follow-up NOT filed: the named gap is a seat-availability condition (needs a non-Clarity seat or a dispatcher CLAIMABILITY GATE), not a closable lane task, and any gap brief filed here would itself be exit-7-barred for this seat.",
    },
    {
        'tick': '20261026-0358',
        'agent': 'Team Naya Scorer',
        'lane': 'executor',
        'task': 'seat-stall 03:58 PDT - 24-brief claim attempt, zero claimable, queue untouched',
        'score': 9.0,
        'note': "Verified by this scorer from live bytes: all 24 briefs named in the receipt are present in brief-queue/ root and rotation queued (24) matches the receipt's list exactly; no brief-tNNNN files; queue untouched; stall-cap respected (60 min after the 02:58 receipt). Score 9.0 - GOOD, ONE MORE PASS. Why not 9.5: stall reported, not moved - 17th consecutive hourly stall receipt (10:58 Oct 25 through 03:58 Oct 26) with zero delta vs 02:58, same 24 exit-7 refusals. Gap follow-up NOT filed: the named gap is a seat-availability condition (needs a non-Clarity seat or a dispatcher CLAIMABILITY GATE), not a closable lane task, and any gap brief filed here would itself be exit-7-barred for this seat.",
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
