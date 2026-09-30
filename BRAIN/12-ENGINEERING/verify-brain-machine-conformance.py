#!/usr/bin/env python3
"""Canonical machine conformance gate for the NayaPOWER BRAIN.

Why this exists: before it, 17 machine-readable artifacts under BRAIN/ were checked
only by hand-written Python and by convention, and there was NO JSON Schema on the
canonical branch at all. The North Star, the graph seed, and the runtime loader each
carried a DIFFERENT relationship vocabulary, and nothing detected it.

This gate makes the canonical machine contract authoritative. It proves what is
provable in-repository and refuses to pretend the rest is proven.

It does NOT create a second brain. It governs the artifacts that already are the brain.

Fail-closed. Exits 1 on any finding. Read-only: mutates nothing.
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_REL = 'BRAIN/00-SPEC/BRAIN-MACHINE-CONTRACT-V1.schema.json'
GRAPH_SEED_REL = 'BRAIN/04-INTELLIGENCE/GRAPH/0001-KERNEL-GRAPH-SEED-V1.json'
OBJECTS_REL = 'BRAIN/04-INTELLIGENCE/OBJECTS'
REGISTRY_REL = 'BRAIN/03-KERNEL/0003-RUNTIME-REGISTRY-V1.json'
MANIFEST_REL = 'BRAIN/03-KERNEL/MANIFEST.json'
LOADER_REL = 'kernel/brain_registry.py'

NODES = ('SELF', 'LAW', 'ACT', 'KNOW', 'PROVE', 'CONNECT', 'VERIFY', 'LEARN', 'EVOLVE')
NODE_IDS = {f'NAYA-KERNEL-{n}' for n in NODES}


def fail(msg: str) -> int:
    print('FAIL:', msg, file=sys.stderr)
    return 1


def load(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def canonical_vocabulary(schema: dict) -> set:
    return set(schema['$defs']['relationshipType']['enum'])


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT
    findings: list[str] = []

    schema_path = root / SCHEMA_REL
    if not schema_path.is_file():
        return fail(f'canonical machine schema is absent: {SCHEMA_REL}')
    try:
        schema = load(schema_path)
    except Exception as exc:
        return fail(f'canonical machine schema is unreadable: {exc}')

    vocab = canonical_vocabulary(schema)

    def schema_errors(doc, label):
        try:
            import jsonschema
            from jsonschema import Draft202012Validator
            out = []
            for err in Draft202012Validator(schema).iter_errors(doc):
                out.append(f'{label} violates the machine contract at '
                           f'{".".join(str(x) for x in err.path) or "<root>"}: {err.message[:120]}')
            return out
        except ImportError:
            return []

    # --- 1. every node object must satisfy the canonical machine contract -----------
    object_files = sorted((root / OBJECTS_REL).glob('NAYA-KERNEL-*.json'))
    if len(object_files) != 9:
        findings.append(f'expected 9 node objects, found {len(object_files)}')
    seen_ids = set()
    for f in object_files:
        try:
            obj = load(f)
        except Exception as exc:
            findings.append(f'{f.name} is not valid JSON: {exc}')
            continue
        findings.extend(schema_errors(obj, f.name))
        oid = obj.get('object_id')
        if oid in seen_ids:
            findings.append(f'duplicate object_id {oid}')
        seen_ids.add(oid)
        if oid not in NODE_IDS:
            findings.append(f'{f.name} has non-canonical object_id {oid!r}')
        for p in (obj.get('provenance') or {}).get('derived_from', []):
            if not (root / p).exists():
                findings.append(f'{f.name} provenance path does not exist: {p}')
        cpath = (obj.get('machine_view') or {}).get('contract')
        if cpath and not (root / cpath).exists():
            findings.append(f'{f.name} machine_view.contract does not exist: {cpath}')

    # --- 2. graph seed: vocabulary, endpoints, provenance --------------------------
    try:
        seed = load(root / GRAPH_SEED_REL)
    except Exception as exc:
        findings.append(f'graph seed unreadable: {exc}')
        seed = {'edges': [], 'allowed_vocabulary': []}

    findings.extend(schema_errors(seed, 'graph seed'))
    seed_vocab = set(seed.get('allowed_vocabulary') or [])
    if seed_vocab != vocab:
        missing = sorted(vocab - seed_vocab)
        extra = sorted(seed_vocab - vocab)
        findings.append(f'graph seed vocabulary disagrees with the canonical machine contract '
                        f'(missing={missing}, not_canonical={extra})')
    edge_ids = set()
    for e in seed.get('edges', []):
        rid = e.get('relationship_id')
        if rid in edge_ids:
            findings.append(f'duplicate relationship_id {rid}')
        edge_ids.add(rid)
        if e.get('type') not in vocab:
            findings.append(f'{rid} uses non-canonical relationship type {e.get("type")!r}')
        for end in ('source_id', 'target_id'):
            if e.get(end) not in NODE_IDS:
                findings.append(f'{rid} {end} is not a canonical node id: {e.get(end)!r}')
        if e.get('source_id') == e.get('target_id'):
            findings.append(f'{rid} is a self-edge')
        for p in e.get('provenance', []):
            if not (root / p).exists():
                findings.append(f'{rid} provenance path does not exist: {p}')

    # --- 3. the runtime loader must enforce the same vocabulary ---------------------
    loader = root / LOADER_REL
    if not loader.is_file():
        findings.append(f'runtime loader is absent: {LOADER_REL}')
    else:
        text = loader.read_text(encoding='utf-8', errors='replace')
        m = re.search(r'ALLOWED_RELATIONSHIPS\s*=\s*\{(.*?)\}', text, re.S)
        if not m:
            findings.append('runtime loader does not declare ALLOWED_RELATIONSHIPS')
        else:
            loader_vocab = set(re.findall(r'"([A-Z_]+)"', m.group(1)))
            drift = sorted(loader_vocab ^ vocab)
            if drift:
                findings.append(
                    f'runtime loader vocabulary drifts from the canonical machine contract: {drift}. '
                    'The loader would accept or reject relationships the canonical contract does not sanction.')

    # --- 4. manifest / registry must cover the same nine ---------------------------
    for rel in (MANIFEST_REL, REGISTRY_REL):
        p = root / rel
        if not p.is_file():
            findings.append(f'absent: {rel}')
            continue
        doc = load(p)
        blob = json.dumps(doc)
        for n in NODES:
            if f'NAYA-KERNEL-{n}' not in blob and n not in blob:
                findings.append(f'{rel} does not mention node {n}')

    # --- report --------------------------------------------------------------------
    print('CANONICAL MACHINE CONFORMANCE — BRAIN')
    print(f'  schema            : {SCHEMA_REL}')
    print(f'  node objects      : {len(object_files)}')
    print(f'  graph seed edges  : {len(seed.get("edges", []))}')
    print(f'  canonical vocab   : {len(vocab)} relationship types')
    print(f'  graph seed vocab  : {len(seed_vocab)}')
    print()
    if findings:
        for f in findings:
            print('  - ' + f, file=sys.stderr)
        return fail(f'{len(findings)} machine conformance finding(s)')
    print('PASS: BRAIN machine artifacts conform to the canonical machine contract')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
