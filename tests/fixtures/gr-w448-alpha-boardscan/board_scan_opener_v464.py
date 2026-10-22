#!/usr/bin/env python3
"""Board scan opener (LEARN standing instrument, shipped w408 by Naya Alpha).

Classifies a board comment as agentish (skip in the human-voice hunt) vs
needs-body-voice-review. Header set is seeded from ALL active teams so the
w405 hole (a [Team Verity]-only set flagging every other seat's posts as
human voice) cannot recur. Enforcement: run self-test on a fresh span;
first-pass false-positive count >10% FAILS the run before any API spend.

KNOWN LIMIT (w437, Naya Alpha): a substantive post whose first line carries no
seeded header (e.g. '# MAIN SEAT — L269 adjudication', comment 6245955948)
escapes the header set. Misses fail SAFE to needs-body-voice-review — the
classifier never auto-marks a substantive body as agentish on my judgment
alone. Voice authorship is a human-seat call (BODY-VOICE DISCRIMINATOR, LAW
w232). Regression: board_scan_fixtures/regression-span-w437.json (3
review-miss bodies; 2/3 gate-clean, the MAIN-SEAT class documented fail-safe).

Usage:
  python3 board_scan_opener.py --self-test <comments.json>
  python3 board_scan_opener.py --classify <comments.json>
"""
import json, re, sys, argparse, os

# VENDOR-NOTE (Naya Alpha, w471): vendored from hidden_files/board_scan_opener.py
# (w408 instrument). Byte-identical EXCEPT this line: the header set resolves
# relative to THIS file so the fixture dir is self-contained — a cold seat runs
# the runner from a bare checkout with zero machine-local paths.
_HERE = os.path.dirname(os.path.abspath(__file__))
SET = json.load(open(os.path.join(_HERE, 'agent-header-set-v1.json')))

def _norm_first_line(body):
    first = (body or '').strip().split('\n')[0]
    first = re.sub(r'^[\s#*>_\-]+', '', first)          # strip md decorations
    first = re.sub(r'^[^\w\[]+', '', first)             # strip emoji/punct prefix
    return first

def agentish(body):
    b = body or ''
    first = _norm_first_line(b)
    for p in SET['header_prefixes']:
        if first.startswith(p):
            return True
    head = '\n'.join(b.split('\n')[:10])
    if all(m in head for m in SET['schema_markers']):
        return True
    if all(m in b for m in SET['whodidto_markers']):
        return True
    if 'Naya ' in b[:200] and re.search(r'sign[- ]?(in|out)', b[:200], re.I):
        return True
    return False

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--self-test', metavar='comments.json')
    ap.add_argument('--classify', metavar='comments.json')
    a = ap.parse_args()
    if a.self_test:
        cs = json.load(open(a.self_test))
        misses = [(c['id'], _norm_first_line(c.get('body'))) for c in cs if not agentish(c.get('body'))]
        n = len(cs)
        print(f'n={n} false_positives={len(misses)}')
        for mid, fl in misses:
            print(f'  MISS {mid}: {fl[:70]}')
        gate = len(misses) / max(n, 1)
        print('GATE:', 'FAIL (>10%)' if gate > 0.10 else 'PASS (<=10%)')
        sys.exit(2 if gate > 0.10 else 0)
    if a.classify:
        cs = json.load(open(a.classify))
        for c in cs:
            print(c['id'], 'AGENT' if agentish(c.get('body')) else 'REVIEW')

if __name__ == '__main__':
    main()
