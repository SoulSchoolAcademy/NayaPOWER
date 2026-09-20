#!/usr/bin/env python3
"""Regression checks for universal execution continuity and optimization governance."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NAYA = ROOT / '.naya'

LAW = NAYA / 'NAYA-EXECUTION-CONTINUITY-AND-LEARNING-LAW.md'
OPT = NAYA / 'codex' / 'NAYA-OPTIMIZATION-AND-EXCELLENCE-LAW.md'
MANIFEST = NAYA / 'naya-context-manifest.json'
SCHEMA = NAYA / 'memory' / 'note.schema.json'
ACTION = NAYA / 'NAYA-ACTION-DELIVERY-LAW.md'
BOOT = NAYA / 'NAYA-CONTEXT-BOOT-PROTOCOL.md'
RESTORE = NAYA / 'runtime' / 'RESTORE-CONTEXT-RUNTIME.md'

for path in (LAW, OPT, MANIFEST, SCHEMA, ACTION, BOOT, RESTORE):
    assert path.exists(), f'missing governance artifact: {path.relative_to(ROOT)}'

law = LAW.read_text(encoding='utf-8')
opt = OPT.read_text(encoding='utf-8')
manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
schema = json.loads(SCHEMA.read_text(encoding='utf-8'))

def contains(text: str, phrase: str, label: str) -> None:
    assert phrase in text, f'{label}: missing required phrase: {phrase}'

contains(law, 'AN AI DOES NOT LEAVE SILENTLY', 'continuity law')
contains(law, 'AI-TO-AI MESSAGE', 'continuity law')
contains(law, 'LEARNING / WISDOM', 'continuity law')
contains(law, 'THE NEXT AI RESTORES FROM THE REPOSITORY', 'continuity law')
contains(opt, 'DO AS MUCH VERIFIED, SAFE, REVERSIBLE, HIGH-VALUE WORK', 'optimization law')
contains(opt, 'MAXIMIZE WITHIN BOUNDS', 'optimization law')
contains(opt, 'OSCAR CHALLENGE', 'optimization law')
contains(opt, 'NO FALSE 10/10', 'optimization law')
contains(ACTION.read_text(encoding='utf-8'), 'NO “NOW WHAT?”', 'action delivery law')
contains(RESTORE.read_text(encoding='utf-8'), 'next best action', 'restore runtime')

assert manifest['subjects']['execution_continuity']['canonical'] == '.naya/NAYA-EXECUTION-CONTINUITY-AND-LEARNING-LAW.md'
assert manifest['subjects']['execution_continuity']['purpose']
assert manifest['subjects']['optimization_excellence']['canonical'] == '.naya/codex/NAYA-OPTIMIZATION-AND-EXCELLENCE-LAW.md'
route_text = json.dumps(manifest['task_routes']['restore'])
assert 'execution_continuity' in route_text, 'restore route does not load execution continuity law'
assert 'optimization_excellence' in route_text, 'restore route does not load optimization law'

rules = manifest['continuity_rules']
assert rules['meaningful_execution_requires_durable_exit_report'] is True
assert rules['exit_report_requires_ai_to_ai_handoff'] is True
assert rules['exit_report_requires_learning_when_material_learning_exists'] is True
assert rules['next_ai_restores_from_repository_not_session_memory'] is True
assert rules['maximum_useful_progress_per_execution'] is True
assert rules['preserve_working_architecture_before_polish'] is True
assert rules['honest_10_10_requires_evidence'] is True

props = schema['properties']
assert 'what_we_learned' in props
assert 'next_best_action' in props
assert 'verification' in props
assert props['type']['enum'] and 'handoff' in props['type']['enum']

print('PASS — continuity + optimization governance is wired and regression-protected')
print('optimization_law=present')
print('execution_continuity_law=present')
print('manifest_boot_and_restore_routes=present')
print('schema_learning_handoff_verification=present')
