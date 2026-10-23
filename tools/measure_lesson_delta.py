#!/usr/bin/env python3
"""
LI-6 measure_lesson_delta.py — the behavioral-proof instrument (INJECTED -> MEASURED).

Mechanical, evidence-only measurement of the learning funnel:
  FILED -> EVER INJECTED -> JUDGED -> HITS/MISSES -> ADOPTED -> MEASURED (delta)

What MEASURED means here (documented, not assumed):
  A lesson is MEASURED iff the judgment timeline shows a MISS judgment
  followed (in later utc order) by only HIT judgments — i.e. the guarded
  failure stopped recurring after it was recorded. A lesson with hits only
  is HIT-ONLY (compliance, not a proven delta); misses after hits is
  PERSISTENT-MISS (the lesson is not landing).

Caveats (what this does NOT claim):
  - Judgments are worker-reported at fold time (lesson_hits/lesson_misses in
    emit-log.jsonl), not independently re-derived. A reported hit is a claim,
    not a byte-proof.
  - utc ordering of judgments is from fold-line timestamps; 'utc_repaired'
    rows exist in the corpus, so ordering is approximate on those rows.
  - The instrument counts lesson_id STRING equality; id renames/aliases
    (e.g. supersedes chains) are not resolved — a renamed lesson can read
    as INJECTED-NEVER-JUDGED.

Reads only; writes <out.json> + <out.md>. Zero network.
"""
import json, sys, os
from datetime import datetime
from collections import defaultdict

HF = os.path.expanduser("~/workspace/goals/super-brain-engine-to-10-10/hidden_files")

def read_jsonl(path):
    rows = []
    with open(os.path.join(HF, path)) as f:
        for line in f:
            line = line.strip()
            if line:
                try: rows.append(json.loads(line))
                except json.JSONDecodeError: pass
    return rows

def as_id_list(v):
    if v is None: return []
    if isinstance(v, list): return [str(x).strip() for x in v if str(x).strip()]
    s = str(v).strip()
    return [s] if s else []

def ts(s):
    if not s: return None
    try: return datetime.fromisoformat(str(s).replace('Z', '+00:00'))
    except Exception: return None

lessons = read_jsonl("lessons.jsonl")
injections = read_jsonl("lesson-injections.jsonl")
emits = read_jsonl("emit-log.jsonl")

filed = {r['lesson_id']: r for r in lessons
         if r.get('lesson_id') and not r.get('retracted_utc')}
retracted = sum(1 for r in lessons if r.get('retracted_utc'))

inj_by_lesson = defaultdict(list)
for r in injections:
    lid = r.get('lesson_id')
    if lid: inj_by_lesson[lid].append(r)

judgments = []          # (utc, lesson_id, side, seat, receipt_comment)
unparseable_utc = 0
for d in emits:
    u = ts(d.get('utc')); rc = d.get('receipt_comment'); seat = d.get('seat')
    for lid in as_id_list(d.get('lesson_hits')):
        judgments.append((u, lid, 'hit', seat, rc))
    for lid in as_id_list(d.get('lesson_misses')):
        judgments.append((u, lid, 'miss', seat, rc))
    if ('lesson_hits' in d or 'lesson_misses' in d) and u is None:
        unparseable_utc += 1

seen = set(); judged_by_lesson = defaultdict(list)
for u, lid, side, seat, rc in judgments:
    key = (rc, lid, side)
    if key in seen: continue
    seen.add(key)
    judged_by_lesson[lid].append((u, side, seat, rc))

def verdict(lid):
    js = sorted((j for j in judged_by_lesson.get(lid, [])), key=lambda j: (j[0] is None, j[0]))
    sides = [s for _, s, _, _ in js]
    if not sides:
        return ("INJECTED-NEVER-JUDGED" if lid in inj_by_lesson else "NEVER-INJECTED", js)
    if all(s == 'hit' for s in sides): return ('HIT-ONLY', js)
    if all(s == 'miss' for s in sides): return ('MISS-ONLY', js)
    last_miss = max(i for i, s in enumerate(sides) if s == 'miss')
    if all(s == 'hit' for s in sides[last_miss + 1:]): return ('DELTA-HIT', js)
    return ('PERSISTENT-MISS', js)

per_lesson = {}
verdicts = defaultdict(list)
for lid in filed:
    v, js = verdict(lid)
    inj_n = len(inj_by_lesson.get(lid, []))
    per_lesson[lid] = {'verdict': v, 'injections': inj_n,
                       'hits': sum(1 for _, s, _, _ in js if s == 'hit'),
                       'misses': sum(1 for _, s, _, _ in js if s == 'miss')}
    verdicts[v].append(lid)

ever_injected = [l for l in filed if l in inj_by_lesson]
judged = [l for l in filed if verdicts.keys() and l in [x for xs in verdicts.values() for x in xs] and per_lesson[l]['verdict'] not in ('NEVER-INJECTED','INJECTED-NEVER-JUDGED')]
# Orphan-id normalization (LI-6, w555 Naya Alpha): dashes<->spaces are spelling
# aliases of the same lesson id — an injection id that matches a filed id after
# normalization is NOT an orphan (closes 9/19 class-A orphans; 10 class-B stay).
orphan_inj_ids = sorted(lid for lid in set(inj_by_lesson) if lid.replace('-', ' ') not in {k.replace('-', ' ') for k in filed})
rut = max(((len(v), k) for k, v in inj_by_lesson.items()), default=(0, None))
adopted_ev = [l for l, r in filed.items() if r.get('adopted_evidence')]
adopted = [l for l, r in filed.items() if r.get('adopted_utc')]

report = {
  'measured_utc': datetime.now().isoformat() + 'Z',
  'funnel': {
    'FILED': len(filed), 'retracted_excluded': retracted,
    'EVER_INJECTED': len(ever_injected),
    'JUDGED': len(judged),
    'HITS_events': sum(p['hits'] for p in per_lesson.values()),
    'MISSES_events': sum(p['misses'] for p in per_lesson.values()),
    'HIT_ONLY_lessons': len(verdicts['HIT-ONLY']),
    'MISS_ONLY_lessons': len(verdicts['MISS-ONLY']),
    'ADOPTED': len(adopted), 'ADOPTED_EVIDENCED': len(adopted_ev),
    'MEASURED_DELTA_HIT': len(verdicts['DELTA-HIT']),
    'PERSISTENT_MISS': len(verdicts['PERSISTENT-MISS']),
    'INJECTED_NEVER_JUDGED': len(verdicts['INJECTED-NEVER-JUDGED']),
    'NEVER_INJECTED': len(verdicts['NEVER-INJECTED']),
  },
  'data_hygiene': {
    'injection_events': len(injections),
    'unique_injected_ids': len(inj_by_lesson),
    'orphan_injection_ids': len(orphan_inj_ids),
    'orphan_sample': orphan_inj_ids[:8],
    'rut_max_injections_one_lesson': rut[0], 'rut_lesson': rut[1],
    'judgment_events': len(judgments),
    'fold_utc_unparseable_with_judgments': unparseable_utc,
  },
  'measured_lessons': sorted(verdicts['DELTA-HIT']),
  'persistent_miss_lessons': sorted(verdicts['PERSISTENT-MISS']),
  'miss_only_lessons': sorted(verdicts['MISS-ONLY']),
  'caveats': [
    'Judgments are worker-reported at fold time, not independently re-derived.',
    'utc ordering is approximate where utc_repaired rows exist.',
    'lesson_id matching normalizes dashes<->spaces (spelling aliases); other renames unresolved.',
  ],
}

# STRICT MEASURED: same seat, miss judged in fold F1, hit judged in a LATER
# fold F2 (different receipt_comment) with only hits between. This is the
# strongest evidence the lesson changed a behavior it guards.
strict_measured = []
for lid in filed:
    seat_ev = defaultdict(list)
    for u, side, seat, rc in judged_by_lesson.get(lid, []):
        if u is not None:
            seat_ev[seat].append((u, side, rc))
    for seat, ss in seat_ev.items():
        ss.sort(key=lambda e: e[0])
        sides = [s for _, s, _ in ss]
        if 'miss' in sides and 'hit' in sides:
            lm = max(i for i, s in enumerate(sides) if s == 'miss')
            tail = ss[lm + 1:]
            if tail and all(s == 'hit' for s in sides[lm + 1:]) and any(rc != ss[lm][2] for _, _, rc in tail):
                strict_measured.append(lid)
                break
report['funnel']['MEASURED_DELTA_HIT_STRICT'] = len(strict_measured)
report['strict_measured_lessons'] = sorted(strict_measured)

out_base = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HF, 'li6/lesson-delta-report')
with open(out_base + '.json', 'w') as f: json.dump(report, f, indent=1)
lines = ['# Learning-funnel delta report (LI-6 instrument)', '',
 f"measured {report['measured_utc']}", '', '| stage | count |', '|---|---|']
for k, v in report['funnel'].items(): lines.append(f'| {k} | {v} |')
lines += ['', '## Data hygiene', '']
for k, v in report['data_hygiene'].items(): lines.append(f'- {k}: {v}')
lines += ['', '## Caveats', '']
lines += [f'- {c}' for c in report['caveats']]
with open(out_base + '.md', 'w') as f: f.write('\n'.join(lines) + '\n')
print(json.dumps(report['funnel'], indent=1))
