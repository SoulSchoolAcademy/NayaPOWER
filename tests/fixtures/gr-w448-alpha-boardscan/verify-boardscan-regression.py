#!/usr/bin/env python3
"""Regression runner: board_scan_opener against the gr-w448 REVIEW-body fixtures.

Closes the standing open item: 3 REVIEW bodies were captured as regression
fixtures (regression-span-gr-w448.json) but no harness ran them against the
instrument. This runner:
  1. loads the span, verifies each fixture file's body_sha256 (tamper check),
  2. runs board_scan_opener.agentish() on the body,
  3. asserts the outcome matches the span's expected_classification (REVIEW
     = NOT agentish: substantive posts must fail SAFE to needs-body-voice-review,
     never be auto-marked agentish).
Exit 0 = all fixtures hold. Exit 2 = any mismatch (instrument regression).
Naya Alpha, wave 464.
"""
import hashlib, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SPAN = os.path.join(HERE, 'regression-span-gr-w448.json')
# COLD-SEAT RULE (w471): the instrument ships INSIDE the fixture dir
# (board_scan_opener_v464.py + agent-header-set-v1.json vendored) — the runner
# imports from its own directory, never from a machine-local absolute path.
sys.path.insert(0, HERE)
import board_scan_opener_v464 as board_scan_opener

span = json.load(open(SPAN))
expect = span['expected_classification']  # 'REVIEW'
failures = []
for fx in span['fixtures']:
    path = os.path.join(HERE, fx['path'])
    j = json.load(open(path))
    body = j.get('body', '')
    sha = hashlib.sha256(body.encode()).hexdigest()
    if sha != fx['body_sha256']:
        failures.append((fx['id'], 'sha_mismatch', sha[:12]))
        continue
    if sha != j.get('body_sha256'):
        failures.append((fx['id'], 'embedded_sha_mismatch', sha[:12]))
        continue
    is_agentish = board_scan_opener.agentish(body)
    # REVIEW means the body is substantive: it must NOT read as agentish.
    if is_agentish:
        failures.append((fx['id'], 'classified_agentish_expected_REVIEW', fx['fixture_class']))
    else:
        print(f"OK {fx['id']} ({fx['fixture_class']}): holds REVIEW, not agentish")

print(f'n={len(span["fixtures"])} failures={len(failures)}')
if failures:
    for f in failures:
        print('  FAIL', f)
    print('VERDICT: REGRESSION — instrument misclassifies a REVIEW fixture')
    sys.exit(2)
print('VERDICT: PASS — all 3 REVIEW fixtures hold')
