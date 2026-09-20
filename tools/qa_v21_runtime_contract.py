#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "20260817 912am RESULTS PAGE CODE"
REPORT = ROOT / "V21-RUNTIME-CONTRACT-QA.md"


def canonical_sections(js: str) -> list[str]:
    """Inspect the actual V21 renderer construction and its deterministic order."""
    start = js.find("var experience=document.createElement('main')")
    if start < 0:
        start = js.find("var experience = document.createElement('main')")
    if start < 0:
        return []

    tail = js[start:]
    end = tail.find("root.appendChild(experience)")
    if end < 0:
        return []
    payload = tail[:end]

    sections: list[str] = []
    for label, token in [
        ("NAYA · YOUR AI GUIDE", "experience.appendChild(naya)"),
        ("YOUR MAXESS SCORE", "experience.appendChild(scoreSec)"),
        ("YOUR FIVE DIMENSIONS", "experience.appendChild(dimSec)"),
        ("YOUR PERSONALIZED REPORT", "experience.appendChild(report)"),
    ]:
        if token in payload:
            sections.append(label)

    m = re.search(r"var orderIds=\[(.*?)\];", payload, re.S)
    if m:
        for a, b in re.findall(r"'([^']+)'|\"([^\"]+)\"", m.group(1)):
            ident = a or b
            if ident in {"v21-dimensions", "v21-report"}:
                continue
            if ident in {"v21-pattern", "v11-pattern", "v13-pattern", "v15-pattern", "v12-pattern"}:
                sections.append("YOUR PATTERN")
            elif ident in {"v11-strengths", "v13-strengths", "v12-strengths", "v18-strength-section"}:
                sections.append("YOUR STRENGTH")
            elif ident in {"v11-masters", "v13-masters", "v12-masters"}:
                sections.append("18 NAYA MASTERS")

    return sections


def main() -> int:
    text = SOURCE.read_text(encoding="utf-8") if SOURCE.exists() else ""
    failures: list[str] = []
    warnings: list[str] = []

    m = re.search(r'<script id="maxess-results-v21-canonical-js">(.*?)</script>', text, re.I | re.S)
    js = m.group(1) if m else ""
    if not js:
        failures.append("canonical V21 runtime JS block missing")

    required_js = {
        "source-of-truth": "window.MAXESS_RESULT",
        "dynamic overall score": "function score(r)",
        "five dimensions": "slice(0,5)",
        "five-stage model": "Supporting",
        "safe fallback": "Your result is not loaded yet.",
        "single Listen control": 'class=\"v21-listen\"',
        "dimension interaction": ".addEventListener('click'",
        "ready state": "data-results-state','ready",
    }
    for label, token in required_js.items():
        if token not in js:
            failures.append(f"runtime requirement missing: {label}")

    for stage in ("Supporting", "Foundation", "Developing", "Advancing", "Mastering"):
        if stage not in js:
            failures.append(f"runtime mastery stage missing: {stage}")

    if re.search(r"v21-score-number[^\n]*>\s*(82|91|79|74|68)\s*<", js):
        failures.append("canonical runtime contains hard-coded demo score")

    if "root.querySelectorAll('.v21-dim').forEach" not in js:
        failures.append("dimension controls do not have a per-dimension interaction loop")

    if "@media print" not in text:
        failures.append("print CSS missing")
    if "prefers-reduced-motion:reduce" not in text:
        failures.append("reduced-motion CSS missing")
    if 'aria-label=\"Listen to Naya interpret your MAXESS results\"' not in js:
        failures.append("Listen accessibility label missing")

    sections = canonical_sections(js)
    if not sections:
        failures.append("canonical renderer sections could not be parsed from the actual V21 renderer")
    else:
        required_core = [
            "NAYA · YOUR AI GUIDE",
            "YOUR MAXESS SCORE",
            "YOUR FIVE DIMENSIONS",
            "YOUR PERSONALIZED REPORT",
        ]
        positions = []
        for marker in required_core:
            try:
                positions.append(sections.index(marker))
            except ValueError:
                failures.append(f"canonical renderer section marker missing: {marker}")
        if len(positions) == len(required_core) and positions != sorted(positions):
            failures.append("canonical runtime section order is incorrect")

    report = [
        "# MAXESS V21 — RUNTIME CONTRACT QA", "",
        f"- Runtime JS lines: `{len(js.splitlines()) if js else 0}`",
        f"- Failures: `{len(failures)}`",
        f"- Warnings: `{len(warnings)}`", "", "## Failures",
    ]
    report.extend(f"- {x}" for x in failures) if failures else report.append("- NONE")
    report += ["", "## Warnings"]
    report.extend(f"- {x}" for x in warnings) if warnings else report.append("- NONE")
    report += ["", "## Gate", "PASS" if not failures else "FAIL", ""]
    REPORT.write_text("\n".join(report), encoding="utf-8")

    for x in failures:
        print("FAIL:", x)
    for x in warnings:
        print("WARN:", x)
    print(f"RUNTIME JS LINES: {len(js.splitlines()) if js else 0}")
    print(f"FAILURES: {len(failures)}")
    print(f"WARNINGS: {len(warnings)}")
    print("V21 RUNTIME CONTRACT QA PASS" if not failures else "V21 RUNTIME CONTRACT QA FAIL")
    return 0 if not failures else 5


if __name__ == '__main__':
    raise SystemExit(main())
