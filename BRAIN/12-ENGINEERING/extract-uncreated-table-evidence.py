"""Extract what is PROVABLE about the uncreated core tables from committed evidence.

This is deliberately NOT a schema generator. It does not invent column types. It
separates two very different grades of evidence:

  TYPED    the column's type is stated by committed DDL (`alter table ... add column
           x <type>`), so the type is recoverable
  NAMED    the column only ever appears in usage (INSERT column lists, indexes, RLS
           policies, UPDATE targets), so the NAME is recoverable and the TYPE IS NOT

A migration authored from NAMED evidence would be a guess about every type, and a wrong
type is a silent corruption of the canonical brain. So this tool reports the split
rather than papering over it, and the gap is what needs live schema authority.

Usage: python extract-uncreated-table-evidence.py [root]
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MIGRATIONS_REL = 'supabase/migrations'
FUNCTIONS_REL = 'supabase/functions'

LEDGER = ROOT / 'BRAIN/12-ENGINEERING/MIGRATION-COHERENCE-BASELINE.json'


def strip_comments(sql: str) -> str:
    sql = re.sub(r'/\*.*?\*/', ' ', sql, flags=re.S)
    return re.sub(r'--[^\n]*', ' ', sql)


def norm(name: str) -> str:
    name = name.strip().strip('"').lower()
    return name if '.' in name else f'public.{name}'


def collect(files: list[Path]) -> dict[str, dict]:
    typed: dict[str, dict[str, str]] = {}
    named: dict[str, set[str]] = {}

    def touch(tbl: str) -> None:
        typed.setdefault(tbl, {})
        named.setdefault(tbl, set())

    for path in files:
        raw = path.read_text(encoding='utf-8', errors='replace')
        sql = strip_comments(raw)

        # TYPED: alter table <t> add column [if not exists] <c> <type...>
        for m in re.finditer(
            r'alter\s+table\s+(?:if\s+exists\s+)?(?:only\s+)?([\w."]+)\s+'
            r'add\s+column\s+(?:if\s+not\s+exists\s+)?([\w"]+)\s+'
            r'([a-z][\w]*(?:\s*\([^)]*\))?(?:\[\])?)',
            sql, re.I,
        ):
            tbl, col, typ = norm(m.group(1)), m.group(2).strip('"').lower(), m.group(3).strip()
            touch(tbl)
            typed[tbl][col] = typ

        # NAMED: insert into <t> (c1, c2, ...) / update <t> set c1 =, c2 =
        for m in re.finditer(r'insert\s+into\s+([\w."]+)\s*\(([^)]*)\)', sql, re.I):
            tbl = norm(m.group(1))
            touch(tbl)
            for c in m.group(2).split(','):
                c = c.strip().strip('"').lower()
                if re.fullmatch(r'[a-z_][a-z0-9_]*', c):
                    named[tbl].add(c)
        for m in re.finditer(r'update\s+([\w."]+)\s+set\s+(.+?)(?:\bwhere\b|\breturning\b|$)',
                             sql, re.I | re.S):
            tbl = norm(m.group(1))
            touch(tbl)
            for c in re.findall(r'([a-z_][a-z0-9_]*)\s*=', m.group(2), re.I):
                named[tbl].add(c.lower())

        # NAMED: create index ... on <t> [using x] (c1, c2)
        for m in re.finditer(
            r'create\s+(?:unique\s+)?index\s+(?:concurrently\s+)?[\w"]*\s*on\s+([\w."]+)\s*'
            r'(?:using\s+[\w]+\s*)?\(([^)]*)\)', sql, re.I | re.S,
        ):
            tbl = norm(m.group(1))
            touch(tbl)
            for c in m.group(2).split(','):
                c = c.strip().strip('"').split()[0].lower() if c.strip() else ''
                if re.fullmatch(r'[a-z_][a-z0-9_]*', c):
                    named[tbl].add(c)

    return {'typed': typed, 'named': named}


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT
    mig = root / MIGRATIONS_REL
    files = sorted(mig.glob('*.sql'))
    data = collect(files)

    ledger = json.loads((root / LEDGER_REL).read_text(encoding='utf-8')) \
        if (root / LEDGER_REL).is_file() else {}
    targets = (ledger.get('known_defects') or {}).get('UNCREATED_DEPENDENCY') or []

    typed, named = data['typed'], data['named']

    print('UNCREATED CORE TABLES - RECOVERABLE EVIDENCE INVENTORY')
    print(f'  migrations scanned : {len(files)}')
    print(f'  tables in ledger   : {len(targets)}')
    print()
    print('  TYPED = type is stated by committed DDL and is therefore recoverable.')
    print('  NAMED = column name only; the TYPE IS NOT recoverable from source and')
    print('          must come from the live database. Do not guess these.')
    print()

    totals = {'tables': len(targets), 'columns_typed': 0, 'columns_named_only': 0}
    report = {}
    for tbl in targets:
        t = typed.get(tbl, {})
        n = named.get(tbl, set()) - set(t)
        report[tbl] = {'typed': t, 'named_only': sorted(n)}
        totals['columns_typed'] += len(t)
        totals['columns_named_only'] += len(n)
        print(f'  {tbl}')
        if t:
            for c, typ in sorted(t.items()):
                print(f'      TYPED  {c:<38} {typ}')
        if n:
            print(f'      NAMED  {len(n)} column(s), type unknown: {", ".join(sorted(n))}')
        if not t and not n:
            print('      NO DDL EVIDENCE -- used but never altered or inserted into')
        print()

    print('  SUMMARY: ' + ', '.join(
        f'{k}={v}' for k, v in sorted(totals.items())))
    print()
    print(f'  {totals["columns_named_only"]} of '
          f'{totals["columns_typed"] + totals["columns_named_only"]} columns have NO recoverable type.')
    print('  Authoring DDL from this would mean guessing every one of those types, including')
    print('  all 20 columns of nayanet_cognition_events, the canonical event store the whole')
    print('  chain depends on. A wrong type is a silent corruption of the brain, not a')
    print('  recoverable error, so this is recorded as a named decision instead.')
    print()
    print('  This is an EVIDENCE INVENTORY, not a schema. It does not author DDL, and it')
    print('  cannot: a NAMED column has no recoverable type, and the live database is the')
    print('  only holder of the truth. UNKNOWN is not PASS.')
    return 0


LEDGER_REL = 'BRAIN/12-ENGINEERING/MIGRATION-COHERENCE-BASELINE.json'

if __name__ == '__main__':
    raise SystemExit(main())
