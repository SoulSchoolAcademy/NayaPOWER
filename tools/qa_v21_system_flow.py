#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from urllib.request import Request, urlopen
import re

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / '20260817 912am RESULTS PAGE CODE'
REPORT = ROOT / 'V21-SYSTEM-FLOW-QA.md'
ASSESSMENT_URL = 'https://raw.githubusercontent.com/SoulSchoolAcademy/maxess/main/CURRENT%20WORKING%20FILE'
RESULTS_HOST = 'https://results.nayanet.xyz/'

fail: list[str] = []
warn: list[str] = []


def fetch(url: str) -> str:
    req = Request(url, headers={'User-Agent': 'MAXESS-V21-QA/1.0'})
    with urlopen(req, timeout=20) as r:
        return r.read().decode('utf-8', errors='replace')


def main() -> int:
    result_text = RESULTS.read_text(encoding='utf-8') if RESULTS.exists() else ''
    if not result_text:
        fail.append('Results working source missing or empty')

    try:
        assessment_text = fetch(ASSESSMENT_URL)
    except Exception as exc:
        assessment_text = ''
        warn.append(f'Assessment source could not be fetched: {exc}')

    # Results contract.
    canonical = re.search(
        r'<script id="maxess-results-v21-canonical-js">(.*?)</script>',
        result_text,
        re.S,
    )
    js = canonical.group(1) if canonical else ''
    if not canonical:
        fail.append('Canonical V21 Results JS not found')
    for token, label in [
        ('window.MAXESS_RESULT', 'Results source of truth'),
        ('data-results-state','ready', 'Results ready state'),
    ]:
        pass
    checks = [
        ('window.MAXESS_RESULT', 'Results source of truth'),
        ("data-results-state','ready'", 'Results ready state'),
        ('list.slice(0,5)', 'five-dimension runtime constraint'),
        ("data-results-state','awaiting'", 'safe missing-result state'),
        ("data-results-data-source','window.MAXESS_RESULT'", 'Result Contract provenance marker'),
    ]
    for token, label in checks:
        if token not in js:
            fail.append(f'Missing Results contract behavior: {label}')

    # Assessment → Results boundary.
    if assessment_text:
        if RESULTS_HOST not in assessment_text and 'results.nayanet.xyz' not in assessment_text:
            warn.append('Assessment source does not visibly contain the Results destination URL')

        # Heuristics for a 15-question assessment. Prefer explicit question arrays/counts;
        # otherwise report uncertainty instead of inventing a failure.
        explicit_counts = []
        for pat in [
            r'(?:questionCount|totalQuestions|QUESTIONS_COUNT)\s*[:=]\s*15',
            r'\b15\s+questions\b',
            r'\bquestions\s*[:=]\s*\[',
        ]:
            if re.search(pat, assessment_text, re.I):
                explicit_counts.append(pat)
        if not explicit_counts:
            warn.append('Assessment source does not expose an explicit machine-readable 15-question marker; browser-level question-count verification remains required')

        # Look for result handoff mechanisms.
        handoff_tokens = [
            'localStorage',
            'sessionStorage',
            'URLSearchParams',
            'MAXESS_RESULT',
            'results.nayanet.xyz',
        ]
        found_handoff = [t for t in handoff_tokens if t in assessment_text]
        if not found_handoff:
            fail.append('No recognizable Assessment → Results handoff mechanism found in the assessment source')
        else:
            if 'MAXESS_RESULT' not in assessment_text:
                warn.append('Assessment source does not itself set MAXESS_RESULT; verify the Result Contract is serialized/transferred before Results loads')

    # End-state promises.
    required_sections = [
        'NAYA · YOUR AI GUIDE', 'YOUR RESULT', 'YOUR FIVE DIMENSIONS',
        'YOUR PERSONALIZED REPORT', 'YOUR PATTERN', 'YOUR STRENGTH',
        'YOUR LEVER', 'YOUR NEXT MOVE', '18 NAYA MASTERS', 'PLAYGROUND',
        'YOUR AI MASTERY JOURNEY'
    ]
    for token in required_sections:
        if token not in result_text:
            fail.append(f'Missing Results section: {token}')

    report = [
        '# MAXESS V21 — SYSTEM FLOW QA',
        '',
        f'- Assessment source fetched: `{"YES" if assessment_text else "NO"}`',
        f'- Results source lines: `{len(result_text.splitlines())}`',
        f'- Failures: `{len(fail)}`',
        f'- Warnings: `{len(warn)}`',
        '', '## Failures'
    ]
    report += [f'- {x}' for x in fail] if fail else ['- NONE']
    report += ['', '## Warnings']
    report += [f'- {x}' for x in warn] if warn else ['- NONE']
    report += ['', '## Gate', 'PASS' if not fail else 'FAIL', '']
    REPORT.write_text('\n'.join(report), encoding='utf-8')

    for x in fail:
        print('FAIL:', x)
    for x in warn:
        print('WARN:', x)
    print(f'ASSESSMENT SOURCE FETCH: {"PASS" if assessment_text else "WARN"}')
    print(f'RESULTS SOURCE LINES: {len(result_text.splitlines())}')
    print(f'FAILURES: {len(fail)}')
    print(f'WARNINGS: {len(warn)}')
    print('V21 SYSTEM FLOW QA PASS' if not fail else 'V21 SYSTEM FLOW QA FAIL')
    return 0 if not fail else 5


if __name__ == '__main__':
    raise SystemExit(main())
