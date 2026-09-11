#!/usr/bin/env python3
"""Run the NayaPOWER Superbrain acceptance/regression suite locally.

The runner executes canonical Superbrain checks plus relevant regression
families. Legacy product-specific renderer contracts are excluded unless
explicitly promoted into the Superbrain acceptance boundary.
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECEIPT_DIR = ROOT / ".naya" / "receipts" / "local-superbrain"
CORE = [
    ROOT / "tools/qa_naya_context_boot.py",
    ROOT / "tools/qa_superbrain_continuity.py",
    ROOT / ".naya/runtime/restore_context.py",
    ROOT / "SUPERBRAIN/test_naya_power_excellence.py",
    ROOT / "SUPERBRAIN/test_naya_power_decision_calculus.py",
    ROOT / "tools/test_superbrain_a_b_c_compounding.py",
    ROOT / "tools/test_superbrain_adversarial.py",
]
REGRESSION_KEYWORDS = (
    "smart_note", "smart_notes", "canonical_event", "event_store", "promot", "cct",
    "continuity", "retrieval", "governance", "reality", "torch", "runtime",
)
EXCLUDED_LEGACY_CONTRACTS = {
    "qa_v21_runtime_contract.py": "legacy V21 renderer/product contract; not a canonical Superbrain acceptance criterion",
}


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def selected_commands() -> list[list[str]]:
    commands: list[list[str]] = []
    for path in CORE:
        if not path.is_file():
            raise FileNotFoundError(path)
        if path.name == "restore_context.py":
            commands.append([sys.executable, str(path.relative_to(ROOT)), "restore", "--pretty"])
        else:
            commands.append([sys.executable, str(path.relative_to(ROOT))])
    seen = {tuple(command[1:]) for command in commands}
    candidates = sorted(ROOT.glob("tools/test_*.py")) + sorted(ROOT.glob("tools/qa_*.py"))
    for path in candidates:
        if path.name in EXCLUDED_LEGACY_CONTRACTS:
            continue
        lowered = path.name.lower()
        if not any(keyword in lowered for keyword in REGRESSION_KEYWORDS):
            continue
        command = [sys.executable, str(path.relative_to(ROOT))]
        if tuple(command[1:]) not in seen and path not in CORE:
            commands.append(command)
            seen.add(tuple(command[1:]))
    return commands


def main() -> int:
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    started = datetime.now(timezone.utc)
    head = git("rev-parse", "HEAD")
    clean_before = git("status", "--porcelain") == ""
    commands = selected_commands()
    results = []
    overall = 0

    print(f"LOCAL SUPERBRAIN SUITE — observed HEAD: {head}")
    print(f"Selected checks: {len(commands)}")
    for name, reason in EXCLUDED_LEGACY_CONTRACTS.items():
        print(f"EXCLUDED: {name} — {reason}")

    for command in commands:
        t0 = time.monotonic()
        proc = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
        elapsed_ms = round((time.monotonic() - t0) * 1000, 2)
        result = {"command": command, "exit_code": proc.returncode, "elapsed_ms": elapsed_ms, "stdout": proc.stdout, "stderr": proc.stderr}
        results.append(result)
        print(f"[{proc.returncode}] {' '.join(command)} ({elapsed_ms} ms)")
        if proc.stdout:
            print(proc.stdout.rstrip())
        if proc.stderr:
            print(proc.stderr.rstrip(), file=sys.stderr)
        if proc.returncode != 0:
            overall = 1
            print("CONTINUING — failure recorded; remaining checks will still execute.")

    receipt = {
        "schema": "naya-power-local-superbrain-suite/v4",
        "started_at": started.isoformat(),
        "finished_at": datetime.now(timezone.utc).isoformat(),
        "observed_head": head,
        "clean_worktree_before": clean_before,
        "github_actions_used": False,
        "selected_check_count": len(commands),
        "excluded_checks": EXCLUDED_LEGACY_CONTRACTS,
        "mandatory_layers": ["EXCELLENCE_BY_DEFAULT", "DECISION_CALCULUS", "VERIFICATION", "SMART_NOTE_PROMOTION", "A_TO_B_TO_C_COMPOUNDING"],
        "commands": results,
        "overall": "PASS" if overall == 0 else "FAIL",
    }
    stamp = started.strftime("%Y%m%dT%H%M%SZ")
    path = RECEIPT_DIR / f"suite-{stamp}.json"
    path.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"RECEIPT: {path.relative_to(ROOT)}")
    print(f"SUPERBRAIN LOCAL SUITE: {receipt['overall']}")
    return overall


if __name__ == "__main__":
    raise SystemExit(main())
