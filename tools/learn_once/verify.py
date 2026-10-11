"""Verification harness — VERIFY stage + the machine gate.

Behavioral proof that a lesson is active. A lesson is LEARNED only when:
  * its stage is VERIFIED or ACTIVE,
  * its behavioral check passes right now,
  * its re-tell count is zero.

This file is also the protocol manifest's machine check
(kernel/protocol/protocol_manifest.json -> SN-LEARN-ONCE -> check):

    python3 tools/learn_once/verify.py --registry tools/learn_once/data/lessons.jsonl

Exit 0: every encoded-or-beyond lesson passes and no outstanding failures.
Exit 1: any FAILED / REGRESSED lesson, failing check, or re-tell on an
        encoded lesson. The output names exactly what failed.

Checks are named callables returning (passed: bool, detail: str), or shell
commands. Register new ones with register_check(); the registry stores the
check spec on each lesson.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.learn_once.models import LEARNED_STAGES, Stage  # noqa: E402
from tools.learn_once.registry import load, upsert  # noqa: E402

CheckResult = tuple  # (passed: bool, detail: str)

CHECKS: dict = {}


def register_check(name: str):
    def deco(fn):
        CHECKS[name] = fn
        return fn

    return deco


@register_check("loop_selftest")
def _loop_selftest():
    """The Learn-Once Loop proves itself: its own falsifier suite passes."""
    root = Path(__file__).resolve().parents[2]
    r = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/test_learn_once.py", "-q"],
        capture_output=True,
        text=True,
        timeout=300,
        cwd=root,
    )
    passed = r.returncode == 0
    tail = (r.stdout + r.stderr).strip().splitlines()[-1] if (r.stdout + r.stderr).strip() else "no output"
    return passed, f"pytest tests/test_learn_once.py -> {tail}"


def run_check(spec: dict | None) -> CheckResult:
    """Run a lesson's behavioral check. No spec = not verifiable (fail)."""
    if not spec:
        return False, "no behavioral check recorded — lesson cannot be proven active"
    kind = spec.get("kind")
    if kind == "python":
        name = spec.get("name")
        fn = CHECKS.get(name)
        if fn is None:
            return False, f"unknown check {name!r} — not registered"
        try:
            return fn()
        except Exception as e:  # a crashing check is a failing check
            return False, f"check {name!r} raised: {e}"
    if kind == "shell":
        cmd = spec.get("cmd", "")
        try:
            r = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, timeout=120
            )
            out = (r.stdout + r.stderr).strip().splitlines()
            detail = out[-1] if out else "(no output)"
            return r.returncode == 0, f"shell exited {r.returncode}: {detail}"
        except Exception as e:
            return False, f"shell check raised: {e}"
    return False, f"unknown check kind {kind!r}"


def audit_lesson(lesson) -> dict:
    """Learned/unlearned verdict for one lesson. Read-only."""
    problems: list[str] = []
    if lesson.stage == Stage.FAILED.value:
        problems.append(
            f"re-tell recorded x{lesson.re_tells} — loop failure, bug refs: {lesson.bug_refs or 'NONE FILED'}"
        )
    if lesson.stage == Stage.REGRESSED.value:
        problems.append("behavioral check previously passed, now failing")
    if lesson.stage in (
        Stage.ENCODED.value,
        Stage.VERIFIED.value,
        Stage.ACTIVE.value,
        Stage.REGRESSED.value,
    ):
        if lesson.re_tells > 0 and lesson.stage != Stage.FAILED.value:
            problems.append(
                f"re_tells={lesson.re_tells} on an encoded lesson without FAILED status — registry inconsistent"
            )
        passed, detail = run_check(lesson.check)
        if not passed:
            problems.append(f"behavioral check failing: {detail}")
    learned = not problems and lesson.stage in (
        Stage.VERIFIED.value,
        Stage.ACTIVE.value,
    )
    return {
        "lesson_id": lesson.lesson_id,
        "title": lesson.title,
        "stage": lesson.stage,
        "re_tells": lesson.re_tells,
        "learned": learned,
        "problems": problems,
    }


def audit(registry_path: str | Path) -> dict:
    """Audit the registry. Two separate verdicts:

    * learned: the positive state (VERIFIED/ACTIVE + check passing + zero re-tells)
    * failures: things that are actually wrong (FAILED, REGRESSED, failing
      check, re-tell inconsistency). A lesson merely awaiting its first
      verification (ENCODED) is not a failure — it is mid-flight.

    The gate (ok) fails only on failures, never on incompleteness.
    """
    lessons = load(registry_path)
    results = [audit_lesson(l) for l in lessons]
    failures = [r for r in results if r["problems"]]
    return {
        "registry": str(registry_path),
        "lessons": len(results),
        "learned": sum(1 for r in results if r["learned"]),
        "failures": failures,
        "ok": not failures,
        "results": results,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="Learn-Once Loop verification gate")
    ap.add_argument("--registry", required=True, help="path to lessons.jsonl")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument(
        "--apply",
        action="store_true",
        help="persist status transitions (e.g. mark REGRESSED)",
    )
    args = ap.parse_args()

    lessons = load(args.registry)
    by_id = {l.lesson_id: l for l in lessons}
    report = audit(args.registry)

    if args.apply:
        for r in report["results"]:
            lesson = by_id[r["lesson_id"]]
            if (
                lesson.stage in (Stage.VERIFIED.value, Stage.ACTIVE.value)
                and any("behavioral check failing" in p for p in r["problems"])
                and lesson.stage != Stage.REGRESSED.value
            ):
                lesson.stage = Stage.REGRESSED.value
                lesson.log("REGRESSED: behavioral check failing on audit")
                upsert(args.registry, lesson)

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"Learn-Once audit: {report['registry']}")
        print(f"  lessons: {report['lessons']}, learned: {report['learned']}")
        if report["ok"]:
            print("  OK — no loop failures; every encoded lesson behaviorally active")
        else:
            print("  FAILURES:")
            for r in report["failures"]:
                print(f"    [{r['lesson_id']}] {r['title']} ({r['stage']})")
                for p in r["problems"]:
                    print(f"      - {p}")
    sys.exit(0 if report["ok"] else 1)


if __name__ == "__main__":
    main()
