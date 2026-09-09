#!/usr/bin/env python3
"""Static 10/10 release gate for the NayaNET Intelligent Hub.

This verifier proves source-level invariants only. It deliberately refuses to
claim authenticated persistence or live-runtime parity; those require runtime
receipts and independent observation.
"""
from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = {
    "canonical_hub": ROOT / "2026 09 09 1213 NAYANET HUB.html",
    "cognitive_engine": ROOT / "scripts/nayanet-cognitive-engine.js",
    "hub_layer": ROOT / "scripts/nayanet-hub-intelligence-layer.js",
    "smart_note_constitution": ROOT / "SMART_NOTE_CONSTITUTION.md",
    "constitutional_mandates": ROOT / "00-NAYA-POWER-CONSTITUTIONAL-MANDATES.md",
    "lifecycle_harness": ROOT / "tests/nayanet-authenticated-lifecycle.html",
    "smart_note_tests": ROOT / "tests/test_smart_note_enforcement.py",
    "hub_contract": ROOT / "SUPERBRAIN/INTELLIGENT-HUB-MASTER-PLAN.md",
}

REQUIRED_TEXT = {
    "canonical_hub": [
        "NAYANET-COGNITIVE-ENGINE-V1:START",
        "NAYANET-HUB-INTELLIGENCE-V2:START",
        "NayaNetCognition",
    ],
    "cognitive_engine": [
        "recordPersistent",
        "searchRemote",
        "handoff",
        "nayanet:cognition-ready",
        "supabase",
    ],
    "hub_layer": [
        "capture",
        "searchRemote",
        "verify",
        "handoff",
        "persistence",
    ],
    "smart_note_constitution": [
        "NO RECEIPT = NOT COMPLETE",
        "One Canonical Event",
        "four logical/persistence artifacts",
        "six required semantic perspectives",
        "Idempotency",
    ],
    "constitutional_mandates": [
        "SMART NOTE + RECEIPT LAW",
        "CONTINUOUS ACTION + NO DEAD END LAW",
        "NO FABRICATION",
        "VERIFY",
        "HANDOFF",
    ],
    "lifecycle_harness": [
        "BIRTH",
        "WRITE",
        "RECEIPT",
        "DEATH",
        "RESURRECTION",
        "SUCCESSOR",
        "api.clear()",
        "searchRemote",
    ],
    "hub_contract": [
        "Connect the Superbrain. Preserve sovereignty. Contribute wisdom. Compound intelligence.",
        "least-privilege",
        "human approval",
        "No competing personal-memory store",
    ],
}

FORBIDDEN_SECRET_PATTERNS = [
    re.compile(r"-----BEGIN (?:RSA|EC|OPENSSH|PRIVATE) KEY-----"),
    re.compile(r"ghp_[A-Za-z0-9]{30,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{30,}"),
    re.compile(r"sk-[A-Za-z0-9]{30,}"),
]

errors: list[str] = []
checks = 0

def check(label: str, ok: bool, detail: str = "") -> None:
    global checks
    checks += 1
    if ok:
        print(f"PASS  {label}")
    else:
        print(f"FAIL  {label}{(': ' + detail) if detail else ''}")
        errors.append(label)

for label, path in REQUIRED.items():
    check(f"required:{label}", path.is_file(), str(path))

for label, needles in REQUIRED_TEXT.items():
    path = REQUIRED[label]
    if not path.is_file():
        continue
    text = path.read_text(encoding="utf-8", errors="replace")
    for needle in needles:
        check(f"contract:{label}:{needle}", needle in text)

# The browser harness must not contain a credential-entry flow.
harness = REQUIRED["lifecycle_harness"].read_text(encoding="utf-8", errors="replace")
check("harness:no-password-input", "type=\"password\"" not in harness.lower())
check("harness:no-credential-request", "enter your password" not in harness.lower())

# Scan source/config text for obvious private-key or token leakage.
scan_roots = [ROOT / "scripts", ROOT / "tests", ROOT / ".github", ROOT / "SUPERBRAIN"]
scanned = 0
for base in scan_roots:
    if not base.exists():
        continue
    for path in base.rglob("*"):
        if not path.is_file() or path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".zip"}:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        scanned += 1
        for pattern in FORBIDDEN_SECRET_PATTERNS:
            check(f"secret-scan:{path.relative_to(ROOT)}:{pattern.pattern}", pattern.search(text) is None)

check("secret-scan:executed", scanned > 0)

# The final two gates are intentionally NOT converted into false passes here.
print("INFO  gate-19-runtime-parity: EXTERNAL — requires exact public runtime observation")
print("INFO  gate-20-final-10-proof: EXTERNAL — requires authenticated lifecycle receipts + runtime proof")

if errors:
    print(f"\n10/10 STATIC GATE: FAIL ({len(errors)} failed checks / {checks} checks)")
    sys.exit(1)

print(f"\n10/10 STATIC GATE: PASS ({checks} source-level checks)")
print("RELEASE STATUS: NOT YET 10/10 — runtime gates remain explicitly external")
