#!/usr/bin/env python3
"""Fail-closed guard for NayaPOWER protected state and verified checkpoints."""
from __future__ import annotations
import json, os, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / '.naya/governance/PROTECTED-STATE.json'

def git(*args: str) -> str:
    p = subprocess.run(['git', *args], cwd=ROOT, text=True, capture_output=True)
    if p.returncode:
        raise RuntimeError(p.stderr.strip() or 'git command failed')
    return p.stdout.strip()

def fail(msg: str) -> None:
    print(f'::error::MONOTONIC PROGRESS GUARD: {msg}')
    raise SystemExit(1)

def main() -> None:
    if not MANIFEST.is_file(): fail('protected-state manifest is missing')
    try:
        m = json.loads(MANIFEST.read_text(encoding='utf-8'))
    except Exception as e:
        fail(f'protected-state manifest is invalid JSON: {e}')
    if m.get('status') != 'CANONICAL': fail('protected-state manifest is not CANONICAL')
    protected = tuple(m.get('protected_paths', []))
    if not protected: fail('protected_paths is empty')
    for marker in ('NAYA-AUTHORIZED-CHANGE:', 'NAYA-BASELINE-IMPACT:'):
        if marker not in m.get('required_declaration_markers', []):
            fail(f'missing required declaration marker: {marker}')

    checkpoint = m.get('baseline', {}).get('commit')
    if not checkpoint: fail('baseline commit is missing')
    try:
        git('merge-base', '--is-ancestor', checkpoint, 'HEAD')
    except RuntimeError:
        fail(f'current HEAD is not descended from protected checkpoint {checkpoint}; recovery/reconciliation is required')

    event_path = os.environ.get('GITHUB_EVENT_PATH')
    event = {}
    if event_path and Path(event_path).is_file():
        try: event = json.loads(Path(event_path).read_text(encoding='utf-8'))
        except Exception: fail('GITHUB_EVENT_PATH is not valid JSON')
    event_name = os.environ.get('GITHUB_EVENT_NAME', '')

    base = None
    head = 'HEAD'
    body = ''
    if event_name == 'pull_request':
        pr = event.get('pull_request', {})
        base = pr.get('base', {}).get('sha')
        head = pr.get('head', {}).get('sha') or 'HEAD'
        body = pr.get('body') or ''
    elif event_name == 'push':
        before = event.get('before')
        if before and set(before) != {'0'}: base = before
        body = event.get('head_commit', {}).get('message', '') or ''
    else:
        base = os.environ.get('NAYA_GUARD_BASE_SHA') or None
        body = os.environ.get('NAYA_GUARD_DECLARATION', '')

    if not base:
        print('No comparison base supplied; checkpoint ancestry validation passed. Protected-change scope will be enforced on PR/push events.')
        return

    try:
        names = git('diff', '--name-only', f'{base}...{head}').splitlines()
    except RuntimeError as e:
        fail(f'could not compute change set: {e}')

    protected_changes = [p for p in names if any(p == prefix.rstrip('/') or p.startswith(prefix) for prefix in protected)]
    if protected_changes:
        authorized = 'NAYA-AUTHORIZED-CHANGE:' in body and 'NAYA-BASELINE-IMPACT:' in body
        if not authorized:
            fail('protected state changed without both NAYA-AUTHORIZED-CHANGE: and NAYA-BASELINE-IMPACT: declarations. Changed: ' + ', '.join(protected_changes))
        print('Protected-state change is explicitly declared; human review/merge protection remains required.')
        print('\n'.join(f'  governed: {p}' for p in protected_changes))
    else:
        print('Protected-state preservation: PASS — no protected paths changed.')

    # Detect deleted protected files/directories separately for an unmistakable signal.
    try:
        status = git('diff', '--name-status', f'{base}...{head}').splitlines()
    except RuntimeError as e:
        fail(f'could not compute status: {e}')
    deletions = []
    for row in status:
        parts = row.split('\t')
        if parts and parts[0].startswith('D') and len(parts) >= 2:
            path = parts[-1]
            if any(path == prefix.rstrip('/') or path.startswith(prefix) for prefix in protected):
                deletions.append(path)
    if deletions and not ('NAYA-AUTHORIZED-CHANGE:' in body and 'NAYA-BASELINE-IMPACT:' in body):
        fail('protected deletion detected without governed authorization: ' + ', '.join(deletions))

    print(f'CHECKPOINT: {checkpoint}')
    print(f'HEAD: {git("rev-parse", "HEAD")}')
    print('MONOTONIC PROGRESS GUARD: PASS')

if __name__ == '__main__': main()
