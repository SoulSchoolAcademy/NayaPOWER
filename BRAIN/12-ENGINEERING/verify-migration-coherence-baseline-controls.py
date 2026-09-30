"""Controls for the migration coherence BASELINE ENFORCEMENT.

These exist because the first version of this enforcement shipped broken in a way that
was invisible: it compared only a defect COUNT, and its shell step ended with an
unconditional `exit 0`. Real regression occurred on main -- three new uncreated tables
appeared, the gate printed "floor=11 measured=14" -- and the job still reported success.

A control that cannot fail is worse than no control, because it manufactures trust.
So these controls assert the enforcement actually FAILS on new debt, and PASSES on
known debt and on improvement. They drive the real script against synthetic reports and
a synthetic ledger, so nothing here is a restatement of the script's own opinion.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, 'reconfigure'):
        try:
            _stream.reconfigure(encoding='utf-8', errors='replace')
        except (ValueError, OSError):
            pass

ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / 'BRAIN/12-ENGINEERING/verify-migration-coherence-baseline.py'

# Load the real module so the controls exercise shipped code, not a copy of it.
_spec = importlib.util.spec_from_file_location('migbase', TARGET)
mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mod)

LEDGER = {
    'known_defects': {
        'UNCREATED_DEPENDENCY': ['public.alpha', 'public.beta'],
    }
}
KNOWN = [
    {'class': 'UNCREATED_DEPENDENCY', 'object': 'public.alpha'},
    {'class': 'UNCREATED_DEPENDENCY', 'object': 'public.beta'},
]

results = []


def expect(label: str, findings, want_code: int) -> bool:
    code, _ = mod.check(findings, LEDGER)
    ok = code == want_code
    print(f'{label:<62} expect=exit {want_code} actual=exit {code} '
          f'{"OK" if ok else "*** WRONG ***"}')
    return ok


# 1. Debt exactly equal to the ledger passes.
results.append(expect('measured debt identical to ledger', KNOWN, 0))

# 2. A brand new uncreated table fails. This is the regression that shipped silently:
#    the count grew 11 -> 14 and CI stayed green.
results.append(expect('NEW unrecorded table fails', KNOWN + [
    {'class': 'UNCREATED_DEPENDENCY', 'object': 'public.newcomer'},
], 1))

# 3. A completely new DEFECT CLASS fails even at a lower total count, proving the check
#    is not merely comparing magnitudes.
results.append(expect('new defect CLASS fails despite fewer objects', [
    {'class': 'DUPLICATE_CREATE', 'object': 'public.alpha'},
], 1))

# 4. Repairing debt passes, so real progress is never blocked.
results.append(expect('improvement (fewer defects) passes', [
    {'class': 'UNCREATED_DEPENDENCY', 'object': 'public.alpha'},
], 0))

# 5. Full repair passes.
results.append(expect('full repair (zero findings) passes', [], 0))

# 6. An object identity matters, not just its class: moving a known table to a new name
#    is new debt, because a renamed table needs its own CREATE.
results.append(expect('renamed table is new debt', [
    {'class': 'UNCREATED_DEPENDENCY', 'object': 'public.alpha'},
    {'class': 'UNCREATED_DEPENDENCY', 'object': 'public.alpha_v2'},
], 1))

# 7. The enforcement must be load-bearing: prove it is actually reading the ledger by
#    showing a ledger that does not contain a known table turns the same measurement red.
empty_ledger = {'known_defects': {}}
code, _ = mod.check(KNOWN, empty_ledger)
ok = code == 1
print(f'{"ledger is load-bearing (empty ledger turns known debt red)":<62} expect=exit 1 '
      f'actual=exit {code} {"OK" if ok else "*** WRONG ***"}')
results.append(ok)

print()
print(f'CONTROLS: {sum(results)}/{len(results)} behaved as specified')
print('VERDICT:', 'enforcement fails on new debt and passes on repair'
      if all(results) else 'ENFORCEMENT IS UNSOUND - it would not catch new debt')
print()
print('NOTE: control 2 is the regression that reached main unnoticed. It is asserted here')
print('      so the same silent pass cannot happen again. Control 3 proves the check is')
print('      not a disguised count comparison.')
