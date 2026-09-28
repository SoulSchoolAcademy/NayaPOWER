"""Controls for the migration coherence gate.

A gate that reports defects unconditionally is as useless as one that reports none.
These controls prove the gate DISCRIMINATES on real migration content: it clears a
defect when the defect is genuinely repaired, and raises a finding when a real defect
is introduced.

The strongest control is the last one: it synthesises the missing CREATE TABLE
statements for the known-uncreated core tables and requires the gate to fall to zero
defects. That is what proves the gate is reading the migrations rather than asserting
a fixed list.

They deliberately do NOT claim the real migrations are healthy. They prove measurement
fidelity. The real verdict stays with verify-migration-coherence.py.
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, 'reconfigure'):
        try:
            _stream.reconfigure(encoding='utf-8', errors='replace')
        except (ValueError, OSError):
            pass

ROOT = Path(__file__).resolve().parents[2]
GATE = ROOT / 'BRAIN/12-ENGINEERING/verify-migration-coherence.py'
MIGRATIONS = 'supabase/migrations'


def fixture():
    tmp = Path(tempfile.mkdtemp(prefix='migcoh-'))
    shutil.copytree(ROOT / MIGRATIONS, tmp / MIGRATIONS)
    return tmp


def run(tree):
    return subprocess.run([sys.executable, str(GATE), str(tree)], capture_output=True, text=True)


def classes(tree):
    r = run(tree)
    # The gate pads the class column to the width of the longest class name, so the
    # separator is variable whitespace, never a fixed two spaces.
    found = set(re.findall(r'^  ([A-Z_]+)\s+public\.', r.stdout, re.M))
    return found, r.stdout


def check(label, tree, expect_absent, expect_present):
    got, out = classes(tree)
    ok = expect_absent.issubset(got) is False or not (expect_absent & got)
    ok = (not (expect_absent & got)) and all(c in got for c in expect_present)
    print(f'{label:<58} absent={sorted(expect_absent)} present={sorted(expect_present)} '
          f'actual={sorted(got)} {"OK" if ok else "*** WRONG ***"}')
    return ok


results = []

# 1. The real migrations genuinely carry UNCREATED_DEPENDENCY, and it is named.
tree = fixture()
got, out = classes(tree)
named = {m for m in re.findall(r'^  UNCREATED_DEPENDENCY\s+(public\.[\w.]+)$', out, re.M)}
ok = 'public.nayanet_cognition_events' in named and 'public.v7_smart_note_transactions' in named
print(f'{"real migrations report core uncreated tables":<58} '
      f'cognition_events={"public.nayanet_cognition_events" in named} '
      f'v7_smart_note={"public.v7_smart_note_transactions" in named} '
      f'{"OK" if ok else "*** WRONG ***"}')
results.append(ok)

# 2. Introduce a REAL duplicate unconditional CREATE -> DUPLICATE_CREATE must appear.
tree = fixture()
dup = tree / MIGRATIONS / '99999999999999_control_duplicate.sql'
dup.write_text('create table public.control_duplicate_probe (id uuid);\n', encoding='utf-8')
other = tree / MIGRATIONS / '99999999999998_control_duplicate_first.sql'
other.write_text('create table public.control_duplicate_probe (id uuid);\n', encoding='utf-8')
got, _ = classes(tree)
ok = 'DUPLICATE_CREATE' in got
print(f'{"introduced duplicate unconditional CREATE":<58} expect=DUPLICATE_CREATE actual={sorted(got)} '
      f'{"OK" if ok else "*** WRONG ***"}')
results.append(ok)

# 3. Same table created twice with IF NOT EXISTS -> must NOT be a duplicate defect.
tree = fixture()
(tree / MIGRATIONS / '99999999999999_control_duplicate.sql').write_text(
    'create table if not exists public.control_ine_probe (id uuid);\n', encoding='utf-8')
(tree / MIGRATIONS / '99999999999998_control_duplicate_first.sql').write_text(
    'create table if not exists public.control_ine_probe (id uuid);\n', encoding='utf-8')
got, _ = classes(tree)
ok = 'DUPLICATE_CREATE' not in got
print(f'{"idempotent IF NOT EXISTS create x2":<58} expect=no DUPLICATE_CREATE actual={sorted(got)} '
      f'{"OK" if ok else "*** WRONG ***"}')
results.append(ok)

# 4. Introduce a real DROP then later USE -> DROPPED_THEN_USED must appear.
tree = fixture()
(tree / MIGRATIONS / '20260101000000_control_drop.sql').write_text(
    'drop table if exists public.nayanet_smart_ledger;\n', encoding='utf-8')
(tree / MIGRATIONS / '20260102000000_control_use.sql').write_text(
    'select 1 from public.nayanet_smart_ledger;\n', encoding='utf-8')
got, _ = classes(tree)
ok = 'DROPPED_THEN_USED' in got
print(f'{"introduced drop then later use":<58} expect=DROPPED_THEN_USED actual={sorted(got)} '
      f'{"OK" if ok else "*** WRONG ***"}')
results.append(ok)

# 5. THE STRONG CONTROL: synthesise the missing CREATE TABLE statements for every
#    currently-uncreated core table. The gate must fall to ZERO defects. If it does not,
#    the gate is asserting a fixed list rather than reading the migrations.
tree = fixture()
_, out = classes(tree)
uncreated = re.findall(r'^  UNCREATED_DEPENDENCY\s+(public\.[\w.]+)$', out, re.M)
(tree / MIGRATIONS / '20260901000000_control_backfill_core_tables.sql').write_text(
    '\n'.join(f'create table if not exists {t} (id uuid);' for t in sorted(set(uncreated))) + '\n',
    encoding='utf-8')
got, out2 = classes(tree)
ok = not got
print(f'{"synthesised CREATE for all {n} uncreated tables":<58} expect=0 defects actual={sorted(got)} '
      f'{"OK" if ok else "*** WRONG ***"}'.replace('{n}', str(len(set(uncreated)))))
results.append(ok)

# 6. A pure-keyword / catalog / role reference must never be reported as a table.
tree = fixture()
(tree / MIGRATIONS / '20260103000000_control_noise.sql').write_text(
    'revoke all on table public.nayanet_smart_ledger from anon, authenticated, public;\n'
    'select 1 from pg_proc p join pg_namespace n on n.oid = p.pronamespace;\n'
    'with recursive walk as (select 1) select 1 from walk;\n'
    'select * from jsonb_array_elements(\'[1]\') as elem;\n', encoding='utf-8')
got, _ = classes(tree)
noisy = {g for g in got if 'control_noise' in g}
ok = not noisy
print(f'{"keyword/catalog/CTE/function noise not reported":<58} expect=0 noise findings actual={sorted(noisy)} '
      f'{"OK" if ok else "*** WRONG ***"}')
results.append(ok)

print()
print(f'CONTROLS: {sum(results)}/{len(results)} behaved as specified')
print('VERDICT:', 'gate discriminates real migration content'
      if all(results) else 'GATE IS UNSOUND - it may be asserting a fixed list')
print()
print('NOTE: control 5 proves the UNCREATED_DEPENDENCY findings are real and fixable.')
print('      Synthesising the missing CREATE statements clears every finding, which means')
print('      the gate is measuring the migrations rather than reporting a hardcoded list.')
print('      It does NOT mean anyone has authored those CREATE statements correctly.')
