#!/usr/bin/env python3
"""Semantic conformance across the three ratified sources of the nine-node kernel.

Three artifacts define or enforce "what the nine Nodes are":

  1. .naya/NAYAPOWER-SYSTEM-NORTH-STAR-WHITE-PAPER-AND-ENGINEERING-BLUEPRINT-V1.md  (strategic model, section 8)
  2. .naya/specifications/NAYA-MASTER-NODE-KERNEL-V1.json                            (RATIFIED_BASELINE kernel)
  3. supabase/functions/nayanet-compound-intelligence/index.ts                        (runtime boot gate, hardcoded keys)

The runtime enforces kernel semantics positionally and REJECTS any node whose key
differs. If the strategic model assigns different meaning to the same ordinal, a
Naya following the strategic model is rejected by the live kernel boot gate.

This gate does not guess whether two descriptions are semantically equivalent.
A gate that guesses becomes a gate that lies. It requires an explicit, declared,
machine-readable reconciliation, and fails closed when none exists.

Read-only. Exits 1 on any conformance failure. Mutates nothing.
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

WHITE_PAPER = '.naya/NAYAPOWER-SYSTEM-NORTH-STAR-WHITE-PAPER-AND-ENGINEERING-BLUEPRINT-V1.md'
KERNEL = '.naya/specifications/NAYA-MASTER-NODE-KERNEL-V1.json'
RUNTIME = 'supabase/functions/nayanet-compound-intelligence/index.ts'
MAPPING = '.naya/specifications/NAYA-MASTER-NODE-SEMANTIC-MAPPING.json'
EXPECTED_KEYS = ['SELF', 'LAW', 'ACT', 'KNOW', 'PROVE', 'CONNECT', 'VERIFY', 'LEARN', 'EVOLVE']
WHITE_PAPER_SECTION = 'MASTER NODES: THE SYSTEM'
NODE_HEADING = re.compile(r'^##\s*(\d{2})\s*[—–-]\s*(.+?)\s*$')


def fail(msg: str) -> int:
    print('FAIL:', msg, file=sys.stderr)
    return 1


def parse_white_paper_nodes(repo: Path) -> list[tuple[str, str]]:
    lines = (repo / WHITE_PAPER).read_text(encoding='utf-8').splitlines()
    start = next((i for i, l in enumerate(lines) if WHITE_PAPER_SECTION in l), None)
    if start is None:
        raise ValueError('white paper section 8 heading not found')
    end = next((i for i, l in enumerate(lines[start + 1:], start + 1) if l.startswith('# 9.')), len(lines))
    out = []
    for line in lines[start:end]:
        m = NODE_HEADING.match(line)
        if m:
            out.append((m.group(1), m.group(2).strip()))
    return out


def parse_runtime_keys(repo: Path) -> list[str]:
    src = (repo / RUNTIME).read_text(encoding='utf-8')
    m = re.search(r'MASTER_NODE_KEYS\s*=\s*\[(.*?)\]\s*as const', src, re.S)
    if not m:
        raise ValueError('MASTER_NODE_KEYS not found in runtime')
    return re.findall(r'"([A-Z]+)"', m.group(1))


def main() -> int:
    repo = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]

    try:
        paper = parse_white_paper_nodes(repo)
        kernel = json.loads((repo / KERNEL).read_text(encoding='utf-8'))
        runtime_keys = parse_runtime_keys(repo)
    except Exception as exc:
        return fail(f'cannot read a ratified source: {exc}')

    errors = []

    # Gate 1 - the runtime must still agree with the kernel it enforces.
    kernel_keys = [n.get('key') for n in kernel.get('nodes', [])]
    if kernel_keys != EXPECTED_KEYS:
        errors.append(f'kernel keys are not the canonical nine: {kernel_keys}')
    if runtime_keys != kernel_keys:
        errors.append(f'runtime MASTER_NODE_KEYS {runtime_keys} != kernel keys {kernel_keys} '
                      '(the boot gate would reject live Nodes)')

    # Gate 2 - the strategic model must define exactly nine ordinals.
    if len(paper) != 9:
        errors.append(f'white paper section 8 defines {len(paper)} nodes, expected 9')

    # Gate 3 - a declared reconciliation must exist and be complete.
    mapping_path = repo / MAPPING
    if not mapping_path.is_file():
        errors.append(
            f'NO DECLARED RECONCILIATION: {MAPPING} is absent. The ratified strategic model and '
            'the ratified kernel are both authoritative for the same nine ordinals, and nothing '
            'machine-readable reconciles them. A Naya following the strategic model is rejected '
            'by the runtime boot gate, which enforces kernel semantics positionally.'
        )
    else:
        try:
            mapping = json.loads(mapping_path.read_text(encoding='utf-8'))
        except Exception as exc:
            mapping = {}
            errors.append(f'semantic mapping is unreadable: {exc}')
        entries = mapping.get('entries', []) if isinstance(mapping, dict) else []
        by_ordinal = {e.get('ordinal'): e for e in entries if isinstance(e, dict)}
        for ordinal, _ in paper:
            if ordinal not in by_ordinal:
                errors.append(f'semantic mapping has no entry for white paper node {ordinal}')
        for ordinal, entry in by_ordinal.items():
            for field in ('master_node_id', 'semantic_domain', 'ratified_by'):
                if not entry.get(field):
                    errors.append(f'semantic mapping entry {ordinal} missing {field}')
        if mapping.get('status') == 'RATIFIED' and mapping.get('ratified_by') in (None, '', 'MACHINE'):
            errors.append('semantic mapping claims RATIFIED without a human ratifier')

    # Report - always show the two definitions side by side, conflict or not.
    print('ordinal | strategic model (white paper section 8)            | kernel / deployed (MN)')
    print('-' * 100)
    for idx, (ordinal, name) in enumerate(paper):
        k = kernel.get('nodes', [])
        kname = f"{k[idx]['id']} {k[idx]['key']} - {k[idx]['name']}" if idx < len(k) else '(none)'
        print(f'  {ordinal}    | {name[:44]:<44} | {kname[:44]}')
    print()
    print(f'strategic model nodes : {len(paper)}')
    print(f'kernel nodes          : {len(kernel.get("nodes", []))}')
    print(f'runtime enforced keys : {runtime_keys}')
    print(f'declared mapping      : {"present" if mapping_path.is_file() else "ABSENT"}')
    print()

    if errors:
        for e in errors:
            print('  - ' + e, file=sys.stderr)
        return fail(f'{len(errors)} semantic conformance failure(s): the nine-node kernel has no '
                    'single machine-readable source of truth across the strategic model, the '
                    'ratified kernel, and the runtime boot gate')
    print('PASS: strategic model, ratified kernel, runtime boot gate, and declared semantic '
          'mapping agree on what the nine Nodes are')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
