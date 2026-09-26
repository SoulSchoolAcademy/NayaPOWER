"""Mutation harness: prove the constitutional claim audit test suite has teeth.

Deliberately breaks the module in specific ways and asserts the test suite
notices. A green suite that cannot detect a broken detector is worthless.
"""
import pathlib
import shutil
import subprocess
import sys

TARGET = pathlib.Path(".naya/runtime/constitutional_claim_audit.py")
TESTS = ".naya/tests/test_constitutional_claim_audit.py"

MUTATIONS = {
    "M1 drop governance-surface filter": (
        "        if not is_governance_surface(path, rel):\n            continue\n",
        "",
    ),
    "M2 fingerprint ignores locations": (
        '(kind + "|" + "|".join(locs))',
        "(kind)",
    ),
    "M3 render never fails closed": (
        'return (1 if new_drift else 0), "\\n".join(lines)',
        'return 0, "\\n".join(lines)',
    ),
    "M4 supersession word always resolves": (
        "    if not SUPERSESSION_RE.search(head):\n        return []",
        "    if not SUPERSESSION_RE.search(head):\n        return []\n    return []",
    ),
    "M5 missing registry treated as present": (
        "    if not registry.is_file():\n        return None",
        "    if not registry.is_file():\n        return set()",
    ),
    "M6 registry mapping check inverted": (
        '            if not any(claim["path"].endswith(ref) for ref in referenced):',
        '            if any(claim["path"].endswith(ref) for ref in referenced):',
    ),
    "M7 concurrent claim needs only one survivor": (
        "    if len(survivors) > 1:",
        "    if len(survivors) > 0:",
    ),
}


def run(label: str) -> bool:
    proc = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", TESTS, "-q"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    summary = next(
        (line for line in reversed(proc.stdout.splitlines()) if "passed" in line or "failed" in line),
        "NO SUMMARY",
    )
    caught = proc.returncode != 0
    print(f"  [{'CAUGHT' if caught else 'MISSED'}] {label}: {summary.strip()}")
    return caught


def main() -> int:
    original = TARGET.read_text(encoding="utf-8")
    backup = TARGET.with_suffix(".py.mutationbak")
    shutil.copy(TARGET, backup)
    missed = []
    try:
        print("baseline (must pass):")
        if run("clean"):
            print("  UNEXPECTED: clean suite failed")
            return 1
        for name, (needle, replacement) in MUTATIONS.items():
            if needle not in original:
                print(f"  [ERROR] {name}: pattern not found, mutation not applied")
                missed.append(name)
                continue
            TARGET.write_text(original.replace(needle, replacement, 1), encoding="utf-8")
            if not run(name):
                missed.append(name)
    finally:
        TARGET.write_text(original, encoding="utf-8")
        backup.unlink(missing_ok=True)
    print()
    if missed:
        print(f"RESULT: {len(missed)} mutation(s) survived: {missed}")
        return 1
    print(f"RESULT: all {len(MUTATIONS)} mutations caught; module restored")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
