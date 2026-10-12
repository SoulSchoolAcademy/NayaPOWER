"""The CI gate must be capable of failing.

An enforcement step that ends with an unconditional `exit 0` cannot turn a build red,
no matter what it prints. That is not hypothetical: the migration-coherence step in
`.github/workflows/collective-chain-readiness-gate.yml` did exactly this, and run
36501228953 shows the real consequence --

    migration defect floor=11   measured=14

printed on a step whose job concluded `success`. Three new uncreated tables reached main
because the gate reported the regression and then ignored it.

A gate that cannot fail is worse than no gate, because it converts an honest red into a
confident green. These tests assert the capability, so the class of defect cannot return
in any workflow in this repository.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
WORKFLOWS = REPO / '.github/workflows'
GATE = WORKFLOWS / 'collective-chain-readiness-gate.yml'

# Any enforcement step must let its last real command decide the outcome.
# `exit 0` and `|| true` are the two ways a step silently swallows its own failure.
MASKING = re.compile(r'^\s*(exit\s+0\b|\|\|\s*true\b)', re.M)

# A deliberate out-of-scope PASS is NOT masking, but only when the step says so
# in plain words: a scope gate that documents its decision (e.g. receipt-gate's
# "Scope gate ... PASS by decision") is auditable, which is the opposite of the
# silent-masking failure mode this guard exists to catch. The carve-out is
# per-step and requires BOTH markers — an unmarked `exit 0` still fails the guard.
STEP_BOUNDARY = re.compile(r'(?m)^\s*-\s+(?:name|uses):')
SCOPE_DECISION_MARKERS = ('Scope gate', 'PASS by decision')


def test_migration_coherence_gate_workflow_exists():
    assert GATE.is_file(), f'{GATE.name} is missing, so chain and migration readiness are unmeasured in CI.'


def _step_spans(text):
    """(start, end) spans of each top-level step in a workflow file.

    A step runs from its `- name:`/`- uses:` line to the next step's line.
    Text before the first step (triggers, env) is span 0 — it gets no carve-out.
    """
    bounds = [m.start() for m in STEP_BOUNDARY.finditer(text)]
    spans = []
    if bounds and bounds[0] > 0:
        spans.append((0, bounds[0]))
    for i, start in enumerate(bounds):
        end = bounds[i + 1] if i + 1 < len(bounds) else len(text)
        spans.append((start, end))
    return spans


def test_no_workflow_step_swallows_its_own_failure():
    offenders = []
    for wf in sorted(WORKFLOWS.glob('*.y*ml')):
        text = wf.read_text(encoding='utf-8', errors='replace')
        for start, end in _step_spans(text):
            chunk = text[start:end]
            # Explicit scope decisions are documented, not silent — see the note
            # above. Only the `exit 0` form can be a scope decision; `|| true`
            # never is, so it is never exempted.
            scope_decision = all(marker in chunk for marker in SCOPE_DECISION_MARKERS)
            for m in MASKING.finditer(chunk):
                kind = m.group(1).strip()
                if scope_decision and kind.startswith('exit 0'):
                    continue
                line = text[:start + m.start()].count('\n') + 1
                offenders.append(f'{wf.name}:{line}: {kind}')
    assert not offenders, (
        'These workflow lines discard the exit status of the step containing them, so the '
        'step cannot fail. A regression check that cannot fail is not a check. '
        '(An `exit 0` is only allowed inside a step that documents it as a scope '
        'decision with both Scope gate + PASS by decision markers):\n  '
        + '\n  '.join(offenders)
    )


def test_migration_enforcement_compares_finding_identity_not_just_a_count():
    """A bare count says nothing about WHICH table regressed, so new debt can hide
    inside an unchanged total. The enforcement must load the named ledger."""
    text = GATE.read_text(encoding='utf-8')
    assert 'verify-migration-coherence-baseline.py' in text, (
        'The workflow must enforce the named debt ledger via '
        'verify-migration-coherence-baseline.py, not compare a bare defect count.'
    )
    ledger = REPO / 'BRAIN/12-ENGINEERING/MIGRATION-COHERENCE-BASELINE.json'
    assert ledger.is_file(), 'The recorded debt ledger is missing, so there is nothing to regress against.'
    assert '--json' in text, (
        'The gate must emit machine-readable findings so the ledger check compares '
        'identities rather than magnitudes.'
    )


def test_baseline_enforcement_controls_pass():
    """The controls prove the enforcement discriminates. Run them, do not assume them."""
    script = REPO / 'BRAIN/12-ENGINEERING/verify-migration-coherence-baseline-controls.py'
    assert script.is_file(), 'Baseline enforcement controls are missing.'
    r = subprocess.run([sys.executable, str(script)], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    assert 'CONTROLS: 7/7' in r.stdout, r.stdout
    assert 'UNSOUND' not in r.stdout, r.stdout


def test_baseline_enforcement_rejects_an_unrecorded_table():
    """Drive the shipped enforcement with an unrecorded finding. It must exit non-zero.

    This is the regression that reached main, asserted directly.
    """
    import importlib.util
    import json
    import tempfile

    target = REPO / 'BRAIN/12-ENGINEERING/verify-migration-coherence-baseline.py'
    spec = importlib.util.spec_from_file_location('migbase_probe', target)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    ledger = {
        'known_defects': {'UNCREATED_DEPENDENCY': ['public.alpha']},
    }
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        (base / 'BRAIN/12-ENGINEERING').mkdir(parents=True)
        src = REPO / 'BRAIN/12-ENGINEERING/MIGRATION-COHERENCE-BASELINE.json'
        (base / 'BRAIN/12-ENGINEERING/MIGRATION-COHERENCE-BASELINE.json').write_text(
            json.dumps(ledger), encoding='utf-8')
        report = base / 'report.json'
        report.write_text(json.dumps({'findings': [
            {'class': 'UNCREATED_DEPENDENCY', 'object': 'public.alpha'},
            {'class': 'UNCREATED_DEPENDENCY', 'object': 'public.unrecorded'},
        ]}), encoding='utf-8')
        r = subprocess.run(
            [sys.executable, str(target), str(base), str(report)],
            capture_output=True, text=True)
    assert r.returncode != 0, (
        'The enforcement passed an unrecorded finding. It would let new migration debt '
        'through silently, which is precisely the defect that reached main.'
    )
    assert 'public.unrecorded' in (r.stdout + r.stderr), (
        'The enforcement failed without naming the offending table, so the failure is '
        'not actionable.'
    )
