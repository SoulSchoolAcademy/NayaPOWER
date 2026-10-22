"""Mechanical subjects and the four-arm runner.

The subject is deliberately dumb and lesson-agnostic: it never sees lesson
ids, expected outcomes, or the registry. Its fixed decision procedure:

  1. Look for injected rules matching this task's type.
  2. Integrity-check each rule: it must carry a receipt (file + quote) and
     must NOT be marked corrupt. A corrupt or receipt-less rule is REFUSED
     (the subject falls back to the naive default and records the refusal).
  3. Otherwise run the rule's named procedure; with no valid rule, run the
     naive default.

A fresh Subject instance per arm = stateless. The adversarial arm injects a
corrupted rule: the subject must refuse it, so behavior stays naive and the
verifier fails — recorded as a correct rejection, not a pass.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

import fixtures


class Subject:
    """Stateless lesson-follower. One instance per arm."""

    def __init__(self):
        self.refusals: list[dict] = []
        self.applied_rule: dict | None = None

    @staticmethod
    def _integrity_ok(rule: dict) -> tuple[bool, str]:
        if rule.get("corrupt"):
            return False, "rule marked corrupt"
        receipt = rule.get("receipt") or {}
        if not receipt.get("file") or not receipt.get("quote"):
            return False, "rule lacks a verifiable receipt"
        return True, "ok"

    def act(self, task_type: str, context: list[dict], sandbox: Path
            ) -> tuple[Path, dict]:
        """Run the task. Returns (artifact path, ctx the subject acted with)."""
        ctx = self._ctx(task_type, sandbox)
        for rule in context:
            if rule.get("applies_to") != task_type:
                continue
            ok, why = self._integrity_ok(rule)
            if not ok:
                self.refusals.append({"rule": rule.get("name", "?"), "why": why})
                continue
            proc_name = rule.get("procedure")
            proc = fixtures.CORRECT.get(proc_name)
            if proc is None:
                self.refusals.append({"rule": rule.get("name", "?"),
                                      "why": f"unknown procedure {proc_name!r}"})
                continue
            self.applied_rule = {"name": rule.get("name"), "procedure": proc_name}
            return proc(ctx, sandbox), ctx
        return fixtures.NAIVE[task_type](ctx, sandbox), ctx

    @staticmethod
    def _ctx(task_type: str, sandbox: Path) -> dict:
        ctx = fixtures.SETUP[task_type](sandbox)
        post = fixtures.POST_SETUP.get(task_type)
        if post:
            post(ctx)
        return ctx


def canonical_context(context: list[dict]) -> str:
    """Canonical form of a context for the causality isolation check."""
    slim = [{k: r.get(k) for k in ("applies_to", "procedure", "name",
                                  "corrupt")} for r in context]
    return json.dumps(slim, sort_keys=True)


def run_arm(lesson: dict, arm: str, injected_rule: dict | None,
            workdir: Path) -> dict:
    """Run one arm. Returns {arm, artifact, passed, reason, refusals,
    applied_rule, context_canonical}."""
    task_type = lesson["task"]["type"]
    sandbox = fixtures.make_sandbox(f"{lesson['id']}-{arm}")
    subject = Subject()  # fresh = stateless
    context = []
    if arm in ("treatment", "successor") and injected_rule is not None:
        context = [copy.deepcopy(injected_rule)]
    elif arm == "adversarial" and injected_rule is not None:
        bad = copy.deepcopy(injected_rule)
        bad["corrupt"] = True
        bad["name"] = (bad.get("name") or "") + " [TAMPERED]"
        context = [bad]
    artifact, ctx = subject.act(task_type, context, sandbox)
    passed, reason = fixtures.VERIFY[task_type](artifact, ctx)
    return {
        "arm": arm,
        "artifact": str(artifact),
        "sandbox": str(sandbox),
        "passed": passed,
        "reason": reason,
        "refusals": subject.refusals,
        "applied_rule": subject.applied_rule,
        "context_canonical": canonical_context(context),
    }


ARMS = ("control", "treatment", "adversarial", "successor")
