#!/usr/bin/env python3
"""Measure Collective Intelligence Chain readiness against the real repository.

The chain is the acceptance test for NayaPOWER:
    LESSON -> INTELLIGENT BLOCK -> VALIDATE -> CONNECT/RECONCILE -> INTEGRATE
    -> CHECKPOINT -> COLD RETRIEVE -> APPLICABILITY -> ACT -> VERIFY -> IMPROVE

This gate MEASURES that chain. It does not simulate it, and it cannot satisfy a link
by existing. It reads the readiness contract, inspects the repository, and reports
exactly one of:

    SATISFIED         inspected evidence for this link is present
    NOT_SATISFIED      the link is checkable now and the evidence is absent
    BLOCKED_NO_RUNTIME the link requires a live runtime that is not on this branch
    UNKNOWN            the gate cannot determine it

Anti-false-positive law: missing evidence is UNKNOWN, never PASS. A locally minted
Intelligent Block id can never satisfy L01, because identity may only be allocated
by the canonical receiver.

Read-only. Exits 1 when any link is not SATISFIED. Mutates nothing.
"""
from __future__ import annotations
import json
import re
import subprocess
import sys
from pathlib import Path

# This gate is a measurement instrument for the whole collective, including Nayas
# running on Windows. A cp1252 console (the Windows default) makes printing the
# report raise UnicodeEncodeError, so the instrument reports NOTHING where it is
# needed most. Force UTF-8 with replacement so the verdict always reaches the operator.
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, 'reconfigure'):
        try:
            _stream.reconfigure(encoding='utf-8', errors='replace')
        except (ValueError, OSError):
            pass

ROOT = Path(__file__).resolve().parents[2]
CONTRACT_REL = 'BRAIN/12-ENGINEERING/COLLECTIVE-INTELLIGENCE-CHAIN-READINESS-V1.json'
MACHINE_CONTRACT_REL = 'BRAIN/00-SPEC/BRAIN-MACHINE-CONTRACT-V1.schema.json'
GRAPH_SEED_REL = 'BRAIN/04-INTELLIGENCE/GRAPH/0001-KERNEL-GRAPH-SEED-V1.json'
RECEIVER_REL = 'supabase/functions/v7-smart-note-canonical/index.ts'
RECEIVER_TABLE = 'v7_smart_note_transactions'

SATISFIED, NOT_SATISFIED, BLOCKED, UNKNOWN = 'SATISFIED', 'NOT_SATISFIED', 'BLOCKED_NO_RUNTIME', 'UNKNOWN'


def tracked(rel: str) -> bool:
    return subprocess.run(['git', 'cat-file', '-e', f'HEAD:{rel}'], cwd=ROOT,
                          capture_output=True).returncode == 0


def fail(msg: str) -> int:
    print('FAIL:', msg, file=sys.stderr)
    return 1


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT
    contract_file = root / CONTRACT_REL
    if not contract_file.is_file():
        return fail(f'chain readiness contract is absent: {CONTRACT_REL}')
    contract = json.loads(contract_file.read_text(encoding='utf-8'))
    links = contract.get('links', [])

    # Runtime preconditions, measured once.
    receiver_present = (root / RECEIVER_REL).is_file()
    migrations = list((root / 'supabase/migrations').glob('*.sql')) if (root / 'supabase/migrations').is_dir() else []
    ts_files = list((root / 'supabase/functions').rglob('*.ts')) if (root / 'supabase/functions').is_dir() else []
    runtime_present = receiver_present and bool(migrations) and bool(ts_files)

    results = []
    for link in links:
        lid, name = link.get('id'), link.get('name')
        if link.get('runtime_required') and not runtime_present:
            results.append((lid, name, BLOCKED,
                            'no live runtime on this branch: no canonical receiver, no migrations, no edge functions'))
            continue
        # Checkable now, without a runtime.
        if lid == 'L01':
            results.append((lid, name, NOT_SATISFIED,
                            'no receiver-issued Intelligent Block identity exists on this branch'))
        elif lid == 'L02':
            ok = (root / MACHINE_CONTRACT_REL).is_file()
            results.append((lid, name, SATISFIED if ok else NOT_SATISFIED,
                            'canonical machine contract present' if ok else 'canonical machine contract absent'))
        elif lid == 'L03':
            seed = root / GRAPH_SEED_REL
            if not seed.is_file():
                results.append((lid, name, NOT_SATISFIED, 'graph seed absent'))
            else:
                doc = json.loads(seed.read_text(encoding='utf-8'))
                edges = doc.get('edges', [])
                typed = [e for e in edges if e.get('type') and e.get('provenance')]
                results.append((lid, name, SATISFIED if typed else NOT_SATISFIED,
                                f'{len(typed)}/{len(edges)} graph relationships carry a canonical type and provenance'))
        elif lid == 'L04':
            seed = root / GRAPH_SEED_REL
            doc = json.loads(seed.read_text(encoding='utf-8')) if seed.is_file() else {'edges': []}
            conflicts = [e for e in doc.get('edges', []) if e.get('type') == 'CONTRADICTS']
            unadjudicated = [e for e in conflicts if e.get('status') == 'CONFLICTED']
            results.append((lid, name, SATISFIED if conflicts and not unadjudicated else
                            (NOT_SATISFIED if conflicts else UNKNOWN),
                            f'{len(conflicts)} declared contradictions, {len(unadjudicated)} unadjudicated; '
                            'no contradiction is evidence of a reconciled system'))
        else:
            results.append((lid, name, UNKNOWN,
                            'evidence for this link is runtime-produced and cannot be inspected on this branch'))

    print('COLLECTIVE INTELLIGENCE CHAIN ΓÇö MEASURED READINESS')
    print(f'  runtime on branch : receiver={receiver_present} migrations={len(migrations)} edge_functions={len(ts_files)}')
    print(f'  chain verdict     : {sum(1 for r in results if r[2] == SATISFIED)}/{len(results)} links SATISFIED')
    print()
    width = max(len(r[0]) for r in results)
    for lid, name, status, why in results:
        print(f'  {lid:<{width}}  {status:<19} {name}')
        print(f'  {"":<{width}}  {"":<19} {why}')
    print()

    unmet = [r for r in results if r[2] != SATISFIED]
    if unmet:
        print(f'  {len(unmet)} of {len(results)} links are not satisfied.', file=sys.stderr)
        if not runtime_present:
            print('  ROOT CAUSE: there is no runtime on this branch. The chain cannot be executed, '
                  'only declared. It is NOT simulated here.', file=sys.stderr)
        return fail(f'collective intelligence chain is {len(unmet)}/{len(results)} links from ready')
    print('PASS: every chain link is satisfied by inspected evidence')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
