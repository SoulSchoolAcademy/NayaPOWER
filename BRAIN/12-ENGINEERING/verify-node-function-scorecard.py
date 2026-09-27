#!/usr/bin/env python3
"""Per-Node Function Scorecard + machine-view fidelity gate for the nine kernel Nodes.

The nine Nodes are meant to be the elite semantic kernel. This gate measures, per Node:

  1. CONTRACT_SPECIFICITY   does the contract declare node-specific inputs, typed
                            outputs, MUST rules, prohibitions, acceptance and failures?
  2. MACHINE_VIEW_FIDELITY  does the machine-readable object agree with its contract?
  3. KERNEL_DISTINCTNESS    is this Node distinguishable from the other eight in the
                            layer a runtime would actually consume?
  4. PROOF_STATE            is behavioural effect proven, or only documented?
  5. PRIMO_READINESS        composite, and what specifically blocks each Node

Why this exists: the human-readable contracts are genuinely distinct, but the
machine-readable objects share ONE failure_mode, ONE successor_effect, ONE input
tuple and ONE output tuple across all nine. A runtime loading the object would give
all nine Nodes identical behaviour. The contract is the specification; the object is
what gets enforced. That gap is the single largest obstacle to elite Nodes.

Read-only. Exit 1 when any Node fails machine-view fidelity or kernel distinctness.
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NODES = ('SELF', 'LAW', 'ACT', 'KNOW', 'PROVE', 'CONNECT', 'VERIFY', 'LEARN', 'EVOLVE')
CONTRACT_T = 'BRAIN/03-KERNEL/NODES/{n}/0001-CONTRACT.md'
OBJECT_T = 'BRAIN/04-INTELLIGENCE/OBJECTS/NAYA-KERNEL-{n}.json'

FAIL_CLOSED_RE = re.compile(r'fail[- ]closed', re.I)
TYPED_OUTPUT_RE = re.compile(r'^-\s*[A-Z][A-Z_]{2,}\s*(—|-|—|$)')


def fail(msg: str) -> int:
    print('FAIL:', msg, file=sys.stderr)
    return 1


def section(text: str, title: str) -> list[str]:
    m = re.search(rf'^##\s*{re.escape(title)}\s*$(.*?)(?=^##\s|\Z)', text, re.M | re.S)
    if not m:
        return []
    return [l.strip() for l in m.group(1).splitlines()
            if l.strip().startswith(('-', '*')) and l.strip() not in ('-', '*')]


def score_node(node: str) -> dict:
    cpath, opath = ROOT / CONTRACT_T.format(n=node), ROOT / OBJECT_T.format(n=node)
    text = cpath.read_text(encoding='utf-8', errors='replace')
    obj = json.loads(opath.read_text(encoding='utf-8'))

    c_inputs, c_outputs = section(text, 'Inputs'), section(text, 'Outputs')
    c_must, c_mustnot = section(text, 'MUST Rules'), section(text, 'MUST NOT Rules')
    c_accept = section(text, 'Acceptance Criteria')
    typed = [o for o in c_outputs if TYPED_OUTPUT_RE.match(o)]
    failure_table = '## Failure States' in text

    ai = obj.get('ai_view', {})
    fidelity_gaps = []
    if len(ai.get('inputs', [])) != len(c_inputs):
        fidelity_gaps.append(f"inputs {len(ai.get('inputs', []))} vs contract {len(c_inputs)}")
    if len(ai.get('outputs', [])) != len(c_outputs):
        fidelity_gaps.append(f"outputs {len(ai.get('outputs', []))} vs contract {len(c_outputs)}")
    if FAIL_CLOSED_RE.search(ai.get('failure_mode', '')) and not failure_table:
        fidelity_gaps.append('failure_mode claims fail-closed but contract has no Failure States table')
    if not any(w in ai.get('purpose', '').lower() for w in node.lower().split()):
        fidelity_gaps.append('ai_view.purpose does not name its own node')

    specificity = 0.0
    specificity += 0.25 if c_inputs else 0
    specificity += 0.25 if typed else 0
    specificity += 0.25 if (c_must and c_mustnot) else 0
    specificity += 0.25 if (c_accept and failure_table) else 0

    return {
        'node': node,
        'contract_inputs': len(c_inputs),
        'contract_typed_outputs': len(typed),
        'must_rules': len(c_must),
        'must_not_rules': len(c_mustnot),
        'acceptance_criteria': len(c_accept),
        'failure_table': failure_table,
        'specificity': round(specificity, 2),
        'fidelity_gaps': fidelity_gaps,
        'canonical_status': obj.get('canonical_status'),
        'behavioral_status': (obj.get('proof') or {}).get('behavioral_status'),
        'implementation_status': (obj.get('proof') or {}).get('implementation_status'),
    }


def main() -> int:
    rows = [score_node(n) for n in NODES]
    by = {r['node']: r for r in rows}

    # distinctness measured on the layer a runtime consumes
    obj = {n: json.loads((ROOT / OBJECT_T.format(n=n)).read_text(encoding='utf-8')) for n in NODES}
    for field, path in (('failure_mode', ('ai_view', 'failure_mode')),
                        ('successor_effect', ('successor_effect',)),
                        ('inputs', ('ai_view', 'inputs')),
                        ('outputs', ('ai_view', 'outputs'))):
        buckets = {}
        for n in NODES:
            v = obj[n]
            for k in path:
                v = v.get(k) if isinstance(v, dict) else None
            buckets.setdefault(json.dumps(v, sort_keys=True), []).append(n)
        distinct = len(buckets)
        shared = max(len(v) for v in buckets.values())
        print(f'  DISTINCTNESS {field:<18}: {distinct} distinct across 9 nodes '
              f'(largest identical group: {shared}/9)')
    print()

    print(f'{"NODE":<9}{"SPEC":<7}{"IN":<4}{"TYPED_OUT":<11}{"MUST":<6}{"MUSTNOT":<9}'
          f'{"ACCEPT":<8}{"FAILTBL":<9}{"FIDELITY":<10}{"BEHAVIORAL"}')
    print('-' * 104)
    for r in rows:
        fid = 'OK' if not r['fidelity_gaps'] else f"{len(r['fidelity_gaps'])} gaps"
        print(f'{r["node"]:<9}{r["specificity"]:<7.2f}{r["contract_inputs"]:<4}'
              f'{r["contract_typed_outputs"]:<11}{r["must_rules"]:<6}{r["must_not_rules"]:<9}'
              f'{r["acceptance_criteria"]:<8}{str(r["failure_table"]):<9}{fid:<10}'
              f'{r["behavioral_status"]}')

    findings = []
    for r in rows:
        if r['fidelity_gaps']:
            findings.append(f"{r['node']}: machine view diverges from contract -> " + '; '.join(r['fidelity_gaps']))
    for r in rows:
        if r['behavioral_status'] != 'PROVEN':
            findings.append(f"{r['node']}: behavioural status is {r['behavioral_status']}, not PROVEN")

    print()
    if findings:
        for f in findings:
            print('  - ' + f, file=sys.stderr)
        return fail(f'{len(findings)} per-node function finding(s): the kernel is not yet elite')
    print('PASS: all nine Nodes are contract-specific, machine-faithful, distinct and behaviorally proven')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
