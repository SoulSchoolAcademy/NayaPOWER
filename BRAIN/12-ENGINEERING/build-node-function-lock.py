#!/usr/bin/env python3
"""Derive and enforce the canonical per-Node function lock.

The nine Node CONTRACTS are genuinely specific: each declares its own outputs,
prohibitions and failure states, and each embeds a TYPED decision vocabulary in
prose (VERIFY: SUCCESS/FAILURE/INCONCLUSIVE/NOT_PROVEN; LEARN:
CANDIDATE/VERIFIED/REJECTED/CONTRADICTED; PROVE: CLAIMED/SUPPORTED/VERIFIED...).

That typing is real but not machine-readable. The machine-readable OBJECTS, by
contrast, are one template across all nine Nodes, so a runtime consuming them
would give every Node identical behaviour.

This script DERIVES the lock from the contracts themselves - nothing is invented -
then verifies the result is genuinely per-Node and fail-closed.

    python BRAIN/12-ENGINEERING/build-node-function-lock.py --write
    python BRAIN/12-ENGINEERING/build-node-function-lock.py --check

Read-only unless --write. Exits 1 if any Node is indistinguishable, unlocks, or
lacks a typed decision vocabulary.
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NODES = ('SELF', 'LAW', 'ACT', 'KNOW', 'PROVE', 'CONNECT', 'VERIFY', 'LEARN', 'EVOLVE')
CONTRACT_T = 'BRAIN/03-KERNEL/NODES/{n}/0001-CONTRACT.md'
LOCK_REL = 'BRAIN/03-KERNEL/NODE-FUNCTION-LOCK-V1.json'

# A typed decision vocabulary: 2+ ALL-CAPS tokens inside one output line.
TYPED_VOCAB = re.compile(r'\(([^()]*[A-Z][A-Z_]+[^()]*)\)')


def section(text: str, title: str) -> list[str]:
    m = re.search(rf'^##\s*{re.escape(title)}\s*$(.*?)(?=^##\s|\Z)', text, re.M | re.S)
    if not m:
        return []
    return [l.strip().lstrip('-*').strip() for l in m.group(1).splitlines()
            if l.strip().startswith(('-', '*')) and l.strip() not in ('-', '*')]


def failure_states(text: str) -> list[dict]:
    m = re.search(r'^##\s*Failure States\s*$(.*)$', text, re.M | re.S)
    if not m:
        return []
    out = []
    for line in m.group(1).splitlines():
        if not line.strip().startswith('|') or '---' in line:
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) >= 2 and cells[0].lower() != 'failure':
            out.append({'condition': cells[0], 'behavior': cells[1]})
    return out


def derive(node: str) -> dict:
    text = (ROOT / CONTRACT_T.format(n=node)).read_text(encoding='utf-8', errors='replace')
    outputs = section(text, 'Outputs')
    vocab: dict[str, list[str]] = {}
    leading = []
    for line in outputs:
        lead = re.match(r'^([A-Z][A-Z_]{2,})\s*(?:\u2014|\u2013|-|\u2015|:)\s+\S', line)
        if lead:
            leading.append(lead.group(1))
    if len(leading) >= 2:
        # Form B: one typed decision value per output line (LAW's AUTHORIZED/DENIED/...).
        vocab['decision'] = sorted(set(leading))
    for line in outputs:
        # Form A: a parenthesised vocabulary, e.g. "Truth state (CLAIMED, SUPPORTED, VERIFIED)".
        m = TYPED_VOCAB.search(line)
        tokens = []
        if m:
            tokens = [t.strip() for t in re.split(r'[,/]| and ', m.group(1)) if t.strip()]
        else:
            pass
        tokens = [t for t in tokens if re.fullmatch(r'[A-Z][A-Z_]{1,}', t)]
        if len(tokens) >= 2:
            label = re.sub(r'\s*[\(\u2014-].*$', '', line).strip() or 'decision'
            key = re.sub(r'[^a-z0-9]+', '_', label.lower()).strip('_') or 'decision'
            vocab[key] = sorted(set(tokens))
    return {
        'node': node,
        'stable_id': f'NAYA-KERNEL-{node}',
        'contract': CONTRACT_T.format(n=node),
        'purpose': (re.search(r'^##\s*Purpose\s*$(.*?)(?=^##\s|\Z)', text, re.M | re.S)
                    .group(1).strip().splitlines()[0] if re.search(r'^##\s*Purpose', text, re.M) else ''),
        'inputs': section(text, 'Inputs'),
        'outputs': outputs,
        'typed_decision_vocabulary': vocab,
        'must_rules': section(text, 'MUST Rules'),
        'must_not_rules': section(text, 'MUST NOT Rules'),
        'acceptance_criteria': section(text, 'Acceptance Criteria'),
        'failure_states': failure_states(text),
    }


def fail(msg: str) -> int:
    print('FAIL:', msg, file=sys.stderr)
    return 1


def verify(lock: dict) -> int:
    entries = lock.get('nodes', [])
    problems = []
    by_id = {e['node']: e for e in entries}
    for n in NODES:
        if n not in by_id:
            problems.append(f'{n}: absent from the lock')
    # Every node must be individually distinguishable.
    for field in ('purpose', 'outputs', 'must_not_rules', 'failure_states'):
        buckets: dict[str, list[str]] = {}
        for n in NODES:
            e = by_id.get(n)
            if e:
                buckets.setdefault(json.dumps(e.get(field), sort_keys=True), []).append(n)
        for shared in buckets.values():
            if len(shared) > 1:
                problems.append(f'{field} is identical across {shared} - Nodes are not distinct')
    # Every node must expose at least one machine-typed decision vocabulary.
    for n in NODES:
        e = by_id.get(n)
        if e and not e.get('typed_decision_vocabulary'):
            problems.append(f'{n}: no machine-typed decision vocabulary extracted from its contract')
    for n in NODES:
        e = by_id.get(n)
        if e:
            for f in ('inputs', 'outputs', 'must_rules', 'must_not_rules',
                      'acceptance_criteria', 'failure_states'):
                if not e.get(f):
                    problems.append(f'{n}: {f} is empty')
    return problems


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--check', action='store_true')
    a = ap.parse_args()

    entries = [derive(n) for n in NODES]
    lock = {
        'schema': 'naya.node.function.lock/v1',
        'title': 'NayaPOWER Nine Master Node Function Lock V1',
        'purpose': 'Authoritative per-Node function specification, DERIVED from each Node contract. '
                   'This is what machine law enforces; the contracts remain the human source. '
                   'Where the machine-readable Node objects disagree with this lock, this lock wins.',
        'derivation': 'Generated by BRAIN/12-ENGINEERING/build-node-function-lock.py directly from '
                      'BRAIN/03-KERNEL/NODES/*/0001-CONTRACT.md. No content is invented.',
        'distinctness_law': 'Two Nodes may never share a purpose, an output set, a prohibition set '
                            'or a failure-state set. A Node that cannot be distinguished from another '
                            'is not a Node; it is a label.',
        'typed_vocabulary_law': 'Every Node must expose at least one machine-typed decision vocabulary '
                                'extracted from its own contract, so a runtime can check results instead '
                                'of parsing prose.',
        'status_of_this_lock': 'CANONICAL_FUNCTION_SPECIFICATION. Behavioural proof is separate and is '
                               'currently NOT_PROVEN for all nine Nodes.',
        'nodes': entries,
    }

    if a.write:
        out = ROOT / LOCK_REL
        out.write_text(json.dumps(lock, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
        print(f'wrote {LOCK_REL} ({out.stat().st_size} bytes)')

    if a.check or not a.write:
        if (ROOT / LOCK_REL).is_file():
            on_disk = json.loads((ROOT / LOCK_REL).read_text(encoding='utf-8'))
            if on_disk != lock:
                return fail('the lock on disk differs from what the contracts derive; regenerate with --write')
            print('lock on disk matches the contracts exactly')
        else:
            print('lock not yet written; derived from contracts in memory')

    print()
    print(f'{"NODE":<9}{"IN":<4}{"OUT":<5}{"MUST":<6}{"MUSTNOT":<9}{"ACCEPT":<8}{"FAILS":<7}{"TYPED VOCABULARIES"}')
    print('-' * 96)
    for e in entries:
        v = e['typed_decision_vocabulary']
        summary = '; '.join(f"{k}={len(x)}" for k, x in v.items()) or 'NONE'
        print(f'{e["node"]:<9}{len(e["inputs"]):<4}{len(e["outputs"]):<5}{len(e["must_rules"]):<6}'
              f'{len(e["must_not_rules"]):<9}{len(e["acceptance_criteria"]):<8}'
              f'{len(e["failure_states"]):<7}{summary}')

    problems = verify(lock)
    print()
    if problems:
        for p in problems:
            print('  - ' + p, file=sys.stderr)
        return fail(f'{len(problems)} node-function lock finding(s)')
    print('PASS: all nine Nodes are distinct, contract-derived and machine-typed')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
