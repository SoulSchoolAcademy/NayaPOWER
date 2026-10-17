#!/usr/bin/env python3
"""health.py — the Builder Health Report.

Answers one question from canonical sources only:
  "Can the Builder actually build what it promises today?"
Computed from the registry + the builder index + build receipts.
Nothing here is hand-typed; re-run it any time.
"""
import json, os, glob

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.normpath(os.path.join(HERE, '..', '..', 'library'))

def main():
    reg = json.load(open(os.path.join(HERE, 'functions', 'registry.json')))
    idx = json.load(open(os.path.join(LIB, 'catalog', 'builder-index-v1.json')))

    funcs = [f for g in reg['groups'].values() for f in g['functions']]
    built = [f for f in funcs if f['status'] == 'built']
    specified = [f for f in funcs if f['status'] == 'specified']
    feats = reg['groups']['feature']['functions']
    feats_built = [f for f in feats if f['status'] == 'built']

    manifests = sorted(glob.glob(os.path.expanduser('~/workspace/your_files/*.manifest.json')))
    trial = [m for m in manifests if 'trial' in os.path.basename(m).lower()]

    rows = [
        ('Indexed parts', str(idx['meta']['entries']),
         'recorded inventory; regenerate tools/build-index.py to qualify'),
        ('Function contracts', str(len(funcs)), 'registry-defined, v1'),
        ('Built functions', str(len(built)), 'independently test each'),
        ('Specified functions', str(len(specified)), 'not operational until proven'),
        ('Feature breakers built', '%d / %d' % (len(feats_built), len(feats)),
         'contract flips breakers; specified breakers refuse cleanly'),
        ('Full customer-page acceptance',
         'DEMONSTRATED' if trial else 'NOT YET DEMONSTRATED',
         'Trial 1: second contract, real capability, independent verifier'),
    ]
    w = max(len(r[0]) for r in rows)
    print('BUILDER HEALTH — computed %s' % reg.get('locked', ''))
    print('-' * 72)
    for name, val, note in rows:
        print('%-*s  %-22s  %s' % (w, name, val, note))

if __name__ == '__main__':
    main()
