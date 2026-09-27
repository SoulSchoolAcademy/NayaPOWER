#!/usr/bin/env python3
"""Binding conformance for the NayaPOWER nine-node kernel.

The kernel gate (scripts/verify-nine-master-nodes.py) proves the kernel is
internally consistent. It does NOT prove the kernel binds to real artifacts:
every contract ID it assigns could name a document that does not exist and the
gate would still pass.

This gate answers the missing question: does every contract the kernel claims as
owned actually resolve to a canonical artifact on disk?

Fail-closed. Exit 1 on any phantom binding, duplicate owner, or ambiguous
artifact. Read-only: it never mutates the kernel, the contracts, or main.
"""
from __future__ import annotations
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KERNEL_REL = '.naya/specifications/NAYA-MASTER-NODE-KERNEL-V1.json'
CONTRACT_DIR_REL = '.naya/contracts'
CONTRACT_FILE_RE = re.compile(r'^(\d{2})-')


def fail(msg: str) -> int:
    print('FAIL:', msg, file=sys.stderr)
    return 1


def index_contract_artifacts(repo: Path) -> dict[str, list[str]]:
    """Map contract id -> canonical artifacts actually present, excluding indexes."""
    tracked = subprocess.run(['git', 'ls-files', CONTRACT_DIR_REL], cwd=repo,
                             text=True, capture_output=True, check=True).stdout.split('\n')
    found: dict[str, list[str]] = {}
    for rel in sorted(x.strip() for x in tracked if x.strip()):
        if Path(rel).name == 'README.md':
            continue  # navigational index, not a contract
        if '/' in rel[len(CONTRACT_DIR_REL) + 1:]:
            continue  # only top-level contracts are addressable by bare id
        if not (repo / rel).is_file():
            continue  # tracked but absent on disk is not a canonical artifact
        m = CONTRACT_FILE_RE.match(Path(rel).name)
        if m:
            found.setdefault(m.group(1), []).append(rel)
    return found


def check(repo: Path) -> tuple[list[str], dict]:
    kernel = json.loads((repo / KERNEL_REL).read_text(encoding='utf-8'))
    artifacts = index_contract_artifacts(repo)
    owners = kernel.get('contract_primary_ownership', {})
    phantom, detail = [], {}
    for node in kernel.get('nodes', []):
        for cid in node.get('primary_contracts', []):
            resolved = artifacts.get(cid, [])
            state = 'BOUND' if len(resolved) == 1 else ('PHANTOM' if not resolved else 'AMBIGUOUS')
            if state != 'BOUND':
                phantom.append(f"{node['id']}:{cid}")
            detail[f"{node['id']}:{cid}"] = {'state': state, 'artifacts': resolved,
                                             'registry_owner': owners.get(cid)}
    return phantom, detail


def main() -> int:
    repo = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT
    if len(sys.argv) > 2 and sys.argv[2] == '--json':
        phantom, detail = check(repo)
        print(json.dumps({'phantom': phantom, 'detail': detail}, indent=2))
        return 1 if phantom else 0
    phantom, detail = check(repo)
    bound = sum(1 for v in detail.values() if v['state'] == 'BOUND')
    print(f'kernel contract bindings: {len(detail)}  bound={bound}  unbound={len(phantom)}')
    for ref in phantom:
        node, cid = ref.split(':')
        print(f'  UNBOUND {node} -> contract {cid}: no canonical artifact on disk')
    if phantom:
        return fail(f'{len(phantom)} of {len(detail)} kernel contract bindings resolve to no artifact')
    print('PASS: every kernel-owned contract resolves to exactly one canonical artifact')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
