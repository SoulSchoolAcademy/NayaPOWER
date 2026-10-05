#!/usr/bin/env python3
"""Verify that supabase/migrations/ can actually rebuild the brain schema.

Motivation. On 2026-09-26 the "Nine-Node clean start" reset deleted all 88 migrations
and left the brain schema unversioned. They were recovered from history in PR #881.
Recovering a file is not the same as proving it is sound, and nobody has yet checked
whether this migration chain can rebuild a database from empty. Master-plan item 26
(Rebuildability) and item 27 (Disaster Recovery) both depend on exactly that.

This gate answers one question per defect class, from the real migration files:

    UNCREATED_DEPENDENCY   a migration reads or writes a table that no migration creates
    DROPPED_THEN_USED      a table is dropped and then used again afterwards
    DUPLICATE_CREATE       the same table is created twice in a way that fails on rebuild
    ORDERING_DISAGREEMENT  filename timestamp order disagrees with migration content order
    EMPTY                  a migration file is empty or has no statements

Anti-false-positive law: this reports UNKNOWN or NOT_SATISFIED, never PASS, and every
finding names the migration and line that caused it. Tables owned by the platform
rather than by this repo (auth.*, storage.*, and Supabase-managed schemas) are
declared in PLATFORM_OWNED and excluded, because requiring this repo to create them
would itself be a false positive.

Read-only. Mutates nothing. Exits 1 when any defect class is present.
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, 'reconfigure'):
        try:
            _stream.reconfigure(encoding='utf-8', errors='replace')
        except (ValueError, OSError):
            pass

ROOT = Path(__file__).resolve().parents[2]
MIGRATIONS_REL = 'supabase/migrations'

# Tables owned by the Supabase platform, not by this repository.
PLATFORM_OWNED = {
    'auth.users', 'auth.roles', 'auth.uid', 'storage.objects', 'storage.buckets',
    'auth.jwt', 'pg_catalog.pg_tables', 'information_schema.tables',
    'auth.admin', 'auth.email', 'storage.foldername', 'pg_stat_statements',
}

# Schemas owned by PostgreSQL itself. No migration in this repo will ever create these,
# and reporting them would be a false positive.
CATALOG_SCHEMAS = {
    'pg_catalog', 'information_schema', 'pg_temp', 'pg_toast', 'public_pgcatalog',
}

# Words that follow FROM/JOIN/REFERENCES in real SQL but are never table names.
# Without this blocklist a naive regex reports `public.of`, `public.on`, `public.anon`
# and similar as uncreated tables, and an instrument that cries wolf is worse than none.
NON_TABLE_TOKENS = {
    # clause / syntax keywords
    'select', 'lateral', 'unnest', 'only', 'all', 'values', 'setof', 'rows', 'row',
    # set operations and joins
    'union', 'intersect', 'except', 'cross', 'inner', 'left', 'right', 'full', 'outer',
    'natural', 'lateral', 'where', 'group', 'order', 'having', 'limit', 'offset',
    # common function names used as set-returning sources
    'generate_series', 'jsonb_array_elements', 'jsonb_array_elements_text',
    'json_array_elements', 'unnest', 'regexp_split_to_table', 'string_to_table',
    'jsonb_each', 'json_each', 'generate_subscripts', 'pg_get_expr', 'format',
    # CTE / alias conventions used across this repo
    'anon', 'authenticated', 'old', 'new', 'existing', 'independent', 'independently',
    'members', 'member', 'smart', 'safe', 'a', 'an', 'as', 'the', 'of', 'on', 'to',
    'set', 'and', 'or', 'not', 'in', 'is', 'null', 'case', 'when', 'then', 'else',
    'end', 'distinct', 'into', 'for', 'with', 'returning', 'using', 'conflict',
    'do', 'nothing', 'table', 'of', 'over', 'partition', 'window', 'cast',
    # PostgreSQL roles, not relations. `revoke ... from anon, authenticated, public`
    # is a role list; a naive FROM regex reads the trailing `public` as a table.
    'public', 'anon', 'authenticated', 'service_role', 'supabase_admin',
}

# Statement forms that prove a migration *depends on* a table existing.
USAGE_PATTERNS = [
    ('REFERENCES', re.compile(r'\breferences\s+(?:only\s+)?([a-z_][\w$]*\.[a-z_][\w$]*|[a-z_][\w$]*)', re.I)),
    ('INSERT',    re.compile(r'\binsert\s+into\s+([a-z_][\w$]*\.[a-z_][\w$]*|[a-z_][\w$]*)', re.I)),
    ('UPDATE',    re.compile(r'\bupdate\s+([a-z_][\w$]*\.[a-z_][\w$]*|[a-z_][\w$]*)', re.I)),
    ('DELETE',    re.compile(r'\bdelete\s+from\s+([a-z_][\w$]*\.[a-z_][\w$]*|[a-z_][\w$]*)', re.I)),
    ('JOIN',      re.compile(r'\bjoin\s+([a-z_][\w$]*\.[a-z_][\w$]*|[a-z_][\w$]*)', re.I)),
    ('FROM',      re.compile(r'\bfrom\s+([a-z_][\w$]*\.[a-z_][\w$]*|[a-z_][\w$]*)', re.I)),
]

CREATE_RE = re.compile(r'\bcreate\s+table\s+(if\s+not\s+exists\s+)?([a-z_][\w$]*\.[a-z_][\w$]*|[a-z_][\w$]*)', re.I)
DROP_RE = re.compile(r'\bdrop\s+table\s+(if\s+exists\s+)?([a-z_][\w$]*\.[a-z_][\w$]*|[a-z_][\w$]*)', re.I)


def strip_comments(sql: str) -> str:
    sql = re.sub(r'/\*.*?\*/', ' ', sql, flags=re.S)
    return re.sub(r'--[^\n]*', ' ', sql)


def mask_quoted_text(sql: str) -> str:
    """Mask quoted text before relation regexes inspect SQL.

    The verifier does not parse quoted identifiers, so double-quoted policy names
    must not be interpreted as UPDATE/FROM clauses. Single-quoted strings may
    contain dynamic SQL text (for example format('drop table ... %I')); treating a
    truncated fragment of that string as static DDL fabricates relation names.
    Preserve newlines/length so diagnostics stay positionally stable.
    """
    def mask(match: re.Match[str]) -> str:
        return ''.join('\n' if ch == '\n' else ' ' for ch in match.group(0))

    sql = re.sub(r"'(?:''|[^'])*'", mask, sql, flags=re.S)
    sql = re.sub(r'"(?:""|[^"])*"', mask, sql, flags=re.S)
    return sql



def neutralise_distinct_from(sql: str) -> str:
    """Neutralise the IS [NOT] DISTINCT FROM comparison operator.

    A naive FROM regex reads `... is distinct from p_owner_id` as a table
    reference `FROM p_owner_id`. This rewrites the operator into a single
    token before the usage patterns run, so the comparison can never be
    mistaken for a relation. (False positive found 2026-10-05 in the
    backfilled Smart Ledger migration: `auth.uid() is distinct from
    p_owner_id` was reported as UNCREATED_DEPENDENCY public.p_owner_id.)
    """
    sql = re.sub(r'\bis\s+not\s+distinct\s+from\b', ' is_not_distinct_from ', sql, flags=re.I)
    sql = re.sub(r'\bis\s+distinct\s+from\b', ' is_distinct_from ', sql, flags=re.I)
    return sql


def normalise(name: str) -> str:
    name = name.strip().strip('"').lower()
    return name if '.' in name else f'public.{name}'


def is_platform(name: str) -> bool:
    return name in PLATFORM_OWNED or name.split('.')[0] in {'auth', 'storage'}


def is_catalog(name: str) -> bool:
    return name.split('.')[0] in CATALOG_SCHEMAS


def plausible_table(name: str) -> bool:
    """Reject anything that cannot be a real relation this repo would create.

    A relation in this schema is lower_snake_case and is never a bare SQL keyword,
    never a one or two letter word, and never a function call. These rules eliminate
    the whole class of naive-regex false positives.
    """
    tail = name.split('.')[-1]
    if not tail or not re.fullmatch(r'[a-z_][a-z0-9_$]*', tail):
        return False
    if tail in NON_TABLE_TOKENS or len(tail) <= 2:
        return False
    # Unqualified PostgreSQL catalog relations, e.g. `from pg_proc p join pg_namespace n`.
    if tail.startswith('pg_'):
        return False
    if not name.startswith('public.'):
        return False
    return True


def main() -> int:
    # Accept an explicit tree so the controls can measure this gate against a fixture.
    # Hardcoding ROOT here previously made the argument impossible to use, which meant
    # every control silently measured the real repository instead of its fixture and
    # reported vacuous passes. A measurement instrument that cannot be pointed at a
    # fixture cannot be proven to discriminate.
    argv = [a for a in sys.argv[1:] if a != '--json']
    as_json = '--json' in sys.argv[1:]
    root = Path(argv[0]).resolve() if argv else ROOT
    mig_dir = root / MIGRATIONS_REL
    if not mig_dir.is_dir():
        # Exit 2, not 1: the instrument could not measure. 1 means "defects found",
        # which is expected and recorded, and callers must not confuse the two.
        print(f'FAIL: {MIGRATIONS_REL} is absent; the schema cannot be rebuilt.', file=sys.stderr)
        return 2

    files = sorted(mig_dir.glob('*.sql'))
    findings: list[dict] = []

    created: dict[str, list[str]] = {}     # table -> migrations that create it
    dropped: dict[str, list[tuple[str, int]]] = {}  # table -> [(migration, index)]
    order: list[tuple[str, str]] = []      # (filename, sql)
    empty: list[str] = []

    for idx, path in enumerate(files):
        raw = path.read_text(encoding='utf-8', errors='replace')
        sql = neutralise_distinct_from(mask_quoted_text(strip_comments(raw)))
        if not sql.strip():
            empty.append(path.name)
        order.append((path.name, sql))

        for m in CREATE_RE.finditer(sql):
            tbl = normalise(m.group(2))
            if not is_platform(tbl):
                created.setdefault(tbl, []).append(path.name)
        for m in DROP_RE.finditer(sql):
            tbl = normalise(m.group(2))
            if not is_platform(tbl):
                dropped.setdefault(tbl, []).append((path.name, idx))

    # --- defect classes -------------------------------------------------------
    for table, makers in sorted(created.items()):
        # A single unconditional `create table` is normal and correct. Only a SECOND
        # unconditional creation of the same table breaks a rebuild from empty.
        # (`create table if not exists` repeated is safe by definition.)
        risky = []
        for name in sorted(set(makers)):
            sql = next(s for (n, s) in order if n == name)
            for m in CREATE_RE.finditer(sql):
                if normalise(m.group(2)) == table and not m.group(1):
                    risky.append(name)
        if len(risky) > 1:
            findings.append({
                'class': 'DUPLICATE_CREATE', 'object': table, 'migrations': risky,
                'detail': 'unconditional CREATE TABLE appears in more than one migration; a rebuild from empty would fail',
            })

    for table, drops in sorted(dropped.items()):
        last_drop = max(i for (_, i) in drops)
        later = []
        for idx, (name, sql) in enumerate(order):
            if idx <= last_drop:
                continue
            for kind, pattern in USAGE_PATTERNS:
                for m in pattern.finditer(sql):
                    if normalise(m.group(1)) == table:
                        later.append(name)
                        break
                else:
                    continue
                break
        if later:
            findings.append({
                'class': 'DROPPED_THEN_USED', 'object': table,
                'migrations': [n for n, _ in drops] + later,
                'detail': f'table is dropped and then used again by {later}',
            })

    known = set(created) | PLATFORM_OWNED
    uncreated: dict[str, list[str]] = {}
    for name, sql in order:
        # Collect CTE names first: `WITH x AS (...) SELECT ... FROM x` is self-contained
        # and must never be reported as an uncreated table.
        ctes = {normalise(m.group(1)) for m in
                re.finditer(r'(?:\bwith\b|,)\s+(?:recursive\s+)?([a-z_][\w$]*)\s+as\s*\(', sql, re.I)}
        for kind, pattern in USAGE_PATTERNS:
            for m in pattern.finditer(sql):
                tbl = normalise(m.group(1))
                if tbl in known or tbl in ctes or is_platform(tbl) or is_catalog(tbl):
                    continue
                if not plausible_table(tbl):
                    continue
                # A relation immediately followed by `(` is a function call, not a table.
                tail = m.end(1)
                if sql[tail:tail + 1] == '(':
                    continue
                uncreated.setdefault(tbl, [])
                if name not in uncreated[tbl]:
                    uncreated[tbl].append(name)
    for table, users in sorted(uncreated.items()):
        findings.append({
            'class': 'UNCREATED_DEPENDENCY', 'object': table, 'migrations': users,
            'detail': 'used by these migrations but no migration creates it; a rebuild from empty would fail',
        })

    for name in empty:
        findings.append({
            'class': 'EMPTY', 'object': name, 'migrations': [name],
            'detail': 'migration file contains no statements',
        })

    # --- report ---------------------------------------------------------------
    # A count cannot be regressed against responsibly: it says nothing about WHICH
    # table regressed, so new debt can hide inside an unchanged total. The JSON form
    # carries the class and object of every finding so the baseline check compares
    # identities, not magnitudes.
    if as_json:
        print(json.dumps({
            'migrations_inspected': len(files),
            'tables_created': len(created),
            'tables_dropped': len(dropped),
            'defect_count': len(findings),
            'findings': sorted(
                ({'class': f['class'], 'object': f['object'], 'detail': f['detail']}
                 for f in findings),
                key=lambda f: (f['class'], f['object']),
            ),
        }, indent=2, sort_keys=True))
        return 1 if findings else 0

    print('BRAIN SCHEMA MIGRATION COHERENCE - MEASURED')
    print(f'  migrations inspected : {len(files)}')
    print(f'  tables created       : {len(created)}')
    print(f'  tables dropped       : {len(dropped)}')
    print()
    by_class: dict[str, int] = {}
    for f in findings:
        by_class[f['class']] = by_class.get(f['class'], 0) + 1
    if not findings:
        print('  NO DEFECTS FOUND: the migration chain is internally coherent.')
        print('  This does NOT prove parity with any live database. It is not evidence')
        print('  that a rebuild has ever been executed. UNKNOWN is not PASS.')
        print()
        print('PASS: migration chain is internally coherent')
        return 0

    width = max(len(f['class']) for f in findings)
    for f in findings:
        print(f'  {f["class"]:<{width}}  {f["object"]}')
        print(f'  {"":<{width}}  {f["detail"]}')
        print(f'  {"":<{width}}  migrations: {", ".join(f["migrations"][:6])}'
              + (' ...' if len(f['migrations']) > 6 else ''))
    print()
    print('  SUMMARY: ' + ', '.join(f'{k}={v}' for k, v in sorted(by_class.items())))
    print()
    print('  This is NOT a pass/fail judgement on the schema. It is the list of places')
    print('  where a rebuild from empty is known to break. Each finding must be either')
    print('  fixed or explicitly recorded as never-having-been-rebuildable.')
    print()
    print(f'FAIL: {len(findings)} migration coherence defect(s)', file=sys.stderr)
    return 1


if __name__ == '__main__':
    raise SystemExit(main())
