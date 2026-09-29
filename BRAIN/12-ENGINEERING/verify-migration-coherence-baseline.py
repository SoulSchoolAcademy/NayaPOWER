"""Compare measured migration-coherence findings against the recorded debt ledger.

A defect *count* is not a safe regression floor. It says nothing about WHICH table
regressed, so new debt can hide inside an unchanged total, and lowering the count to
make a build green destroys the evidence the gate exists to preserve.

This script therefore compares identities: every finding is keyed by (class, object)
and checked against the ledger in MIGRATION-COHERENCE-BASELINE.json.

Verdicts
--------
PASS  no finding outside the ledger (known debt only, or an improvement)
FAIL  at least one finding the ledger does not record -- genuine new debt

An improvement (a ledger entry no longer defective) PASSES but is reported loudly,
because the ledger must then be updated deliberately rather than left stale.

Accepts an explicit tree and an explicit report path so it can be pointed at a
fixture. An instrument that cannot be pointed at a fixture cannot be proven to
discriminate, which is exactly how two vacuous controls were shipped earlier.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASELINE_REL = 'BRAIN/12-ENGINEERING/MIGRATION-COHERENCE-BASELINE.json'


def load_ledger(baseline: dict) -> set[tuple[str, str]]:
    ledger: set[tuple[str, str]] = set()
    for cls, objects in (baseline.get('known_defects') or {}).items():
        for obj in objects:
            ledger.add((cls, obj))
    return ledger


def check(findings: list[dict], baseline: dict) -> tuple[int, list[str]]:
    """Return (exit_code, human lines)."""
    measured = {(f['class'], f['object']) for f in findings}
    ledger = load_ledger(baseline)

    new = sorted(measured - ledger)
    resolved = sorted(ledger - measured)
    lines: list[str] = []

    lines.append('MIGRATION COHERENCE BASELINE ENFORCEMENT')
    lines.append(f'  measured findings : {len(measured)}')
    lines.append(f'  recorded in ledger: {len(ledger)}')
    lines.append('')

    if new:
        lines.append(f'  REGRESSION: {len(new)} finding(s) NOT recorded in the ledger:')
        for cls, obj in new:
            lines.append(f'    + {cls} {obj}')
        lines.append('')
        lines.append('  This is new debt. Either fix it, or -- if the finding is real and')
        lines.append('  accepted -- record it in the ledger with a reason. Do not widen the')
        lines.append('  ledger silently: a ledger that absorbs every change stops being a')
        lines.append('  regression floor and becomes a rubber stamp.')
        lines.append('')

    if resolved:
        lines.append(f'  IMPROVEMENT: {len(resolved)} recorded finding(s) are no longer present:')
        for cls, obj in resolved:
            lines.append(f'    - {cls} {obj}')
        lines.append('')
        lines.append('  Remove these from the ledger deliberately so the recorded debt stays')
        lines.append('  true. This does not fail the build.')
        lines.append('')

    if new:
        return 1, lines

    lines.append('  No finding outside the recorded ledger. Known debt unchanged' if not resolved
                 else '  No finding outside the recorded ledger; recorded debt is stale and needs updating.')
    lines.append('')
    lines.append('  This is NOT proof that a rebuild works. It means the migrations have not')
    lines.append('  regressed against a recorded, named debt ledger. UNKNOWN is not PASS.')
    return 0, lines


def main() -> int:
    args = sys.argv[1:]
    root = Path(args[0]).resolve() if args else ROOT
    report = Path(args[1]) if len(args) > 1 else None

    base_file = root / BASELINE_REL
    if not base_file.is_file():
        print(f'FAIL: {BASELINE_REL} is absent; there is no recorded debt to regress against.',
              file=sys.stderr)
        return 1
    baseline = json.loads(base_file.read_text(encoding='utf-8'))

    if report is None:
        print('FAIL: no measurement report supplied.', file=sys.stderr)
        return 1
    payload = json.loads(report.read_text(encoding='utf-8'))
    findings = payload.get('findings') or []

    code, lines = check(findings, baseline)
    print('\n'.join(lines))
    if code:
        print(f'FAIL: {len(findings)} measured finding(s) include unrecorded debt.', file=sys.stderr)
    return code


if __name__ == '__main__':
    raise SystemExit(main())
