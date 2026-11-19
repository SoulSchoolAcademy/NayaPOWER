import json

base = '/home/hatch/workspace/goals/bring-naya-to-life/hidden_files'
path = f'{base}/twelve-lane-scores.jsonl'

rows = [
    {
        'tick': 't0462',
        'agent': 'Team Naya Scorer',
        'lane': 4,
        'task': 'Retrieval-auth gate migration spec prep (t942 gate) - prep only, no wiring',
        'score': 9.0,
        'note': "Verified by this scorer from live bytes: hidden_files/retrieval-auth-gate-migration-spec.md present (5193 bytes) with sha16 75e3037c435c4c35 matching the receipt exactly; spec header confirms CANDIDATE on main tip via PR #2403, NOT WIRED, NOT RATIFIED, prep-only. Score 9.0 - GOOD, ONE MORE PASS. Why not 9.5: (1) the corpus counts (0/632 retrieval_authorized) and gate/seam SHAs were taken from the receipt, not re-derived by this scorer - old-tip bytes were not re-checked this tick; (2) the receipt's own open holes stand: deployment corpus unmeasured (H1) and scope-vs-publication_scope mapping unresolved (H2); (3) the board-post routing conflict (#2537 vs #2641) remains a dispatcher ruling, not closed work. Gap follow-up NOT newly filed: gap-followup-seen.json already holds t0462-lane4, and rotation queued=31 >= 30 throttles gap-recycling to zero this tick.",
    },
    {
        'tick': 't0465',
        'agent': 'Team Naya Scorer',
        'lane': 4,
        'task': 'Retrieval-auth stamp migration prep + scratch dry-run on real tip modules',
        'score': 9.0,
        'note': "Verified by this scorer from live bytes: hidden_files/retrieval-auth-stamp-migration-prep-t0465.md sha256 prefix 84fb6f18bbd84fe5 matches the receipt exactly; stamp-scratch-t0465.py sha256 prefix 57bb052e46c8dc14 matches exactly; dry-run-log-retrieval-auth-stamp-t0465.md contents match exactly (scratch before ac05d8fa, after 0d11d99a, 632 entries, stamped 26 True / 606 False, VERIFY-1 checks 1-7 PASS, registry_index keyed 56/632). Score 9.0 - GOOD, ONE MORE PASS. Why not 9.5: (1) the G1 registry_index keying finding is load-bearing for the wiring seat and still single-seat - the receipt's own queued second-seat verification has not landed; (2) the stamp policy is a demonstration, not Shawn's Wave-0 ruling, so the mechanics proof is policy-conditional; (3) prep value only - live corpus untouched by design, nothing wired or shipped. Gap follow-up NOT newly filed: gap-followup-seen.json already holds t0465-lane4, and rotation queued=31 >= 30 throttles gap-recycling to zero this tick.",
    },
    {
        'tick': 't0466',
        'agent': 'Team Naya Scorer',
        'lane': 4,
        'task': 'Ledger board-pointer repair - heartbeat phantom file, verified absence report',
        'score': 9.0,
        'note': "Verified by this scorer from live bytes (scoped re-check): timeout-30 find over the goal workspace returns 0 hits for append_ledger.py, supporting the receipt's absence claim in the workspace where the ledger tooling lives; the receipt's 7-surface absence evidence (goal workspace, whole VM, live main tree, contents API, code search, local clones, PR #2398) is taken as reported, not re-run in full this tick. Score 9.0 - GOOD, ONE MORE PASS. Why not 9.5: (1) this tick's re-verification is scoped, not the full 7-surface sweep - branch-wide grep and the #2398 comment thread remain the receipt's own open gaps; (2) absence is not a repair - the team-ledger append mechanism's actual home is still UNKNOWN, routed to keeper/ledger lane but not closed; (3) no second seat has independently re-run the absence search. Gap follow-up NOT newly filed: gap-followup-seen.json already holds t0466-lane4, and rotation queued=31 >= 30 throttles gap-recycling to zero this tick.",
    },
]

existing = set()
with open(path) as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
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
