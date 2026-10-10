#!/usr/bin/env python3
"""
POISON-1..5 — run the full adversarial battery in one command.

Usage: python3 run_all.py
Exit code: 0 if all PASS, 1 otherwise.
Each test snapshots + restores the substrate, so the learn/ directory
and ~/AGENTS.md are left exactly as found.
"""

import os
import subprocess
import sys

POISON_DIR = os.path.dirname(os.path.abspath(__file__))
TESTS = [f"test_poison_{i}.py" for i in range(1, 6)]


def main():
    results = {}
    print("=" * 60)
    print("POISON BATTERY — Immune System adversarial tests")
    print("=" * 60)
    for t in TESTS:
        path = os.path.join(POISON_DIR, t)
        r = subprocess.run([sys.executable, path],
                           capture_output=True, text=True, timeout=300)
        print(r.stdout)
        if r.stderr:
            print(f"--- stderr ({t}) ---")
            print(r.stderr[-2000:])
        test_id = t.replace("test_", "").replace(".py", "").upper().replace(
            "_", "-")
        results[test_id] = (r.returncode == 0)

    print("\n" + "=" * 60)
    print("BATTERY SUMMARY")
    print("=" * 60)
    passed = sum(1 for v in results.values() if v)
    for tid, ok in results.items():
        print(f"  {tid}: {'PASS' if ok else 'FAIL'}")
    print(f"\n{passed}/5 PASS")
    if passed == 5:
        print("Immune System adversarial battery: GREEN.")
    else:
        print("Immune System remains UNKNOWN — see gaps above.")
    return 0 if passed == 5 else 1


if __name__ == "__main__":
    sys.exit(main())
