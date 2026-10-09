"""Deterministic verifiers for the OBSERVE / INDEPENDENTLY VERIFY stages.

A verifier is a pure function: source text in, PASS/FAIL out, with the
machine-counted evidence attached. The verifier is always a different
mechanism from the applier (an AST walk, not an agent judgment) — that
separation is what makes the verification independent.

Task families register their verifier in VERIFIERS. A family with no
registered verifier cannot complete the chain: the stage reports
UNINSTRUMENTED rather than passing on vibes.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass


@dataclass(frozen=True)
class VerifyResult:
    verdict: str  # PASS | FAIL
    evidence: str
    detail: str = ""


def count_ifexp(py_source: str) -> int:
    """Count inline conditional expressions (X if C else Y) in source."""
    tree = ast.parse(py_source)
    return sum(isinstance(n, ast.IfExp) for n in ast.walk(tree))


def verify_state_file_task(py_source: str) -> VerifyResult:
    """T14 family: state files must not use inline conditional expressions.

    The T14 verified law: 'Never write state files through inline
    conditional expressions.' The check is syntactic and total: it counts
    IfExp nodes, so there is no judgment call to dispute.
    """
    try:
        n = count_ifexp(py_source)
    except SyntaxError as exc:
        return VerifyResult("FAIL", "syntax_error", f"source does not parse: {exc}")
    if n == 0:
        return VerifyResult("PASS", "ifexp_count=0",
                            "no inline conditional expressions found")
    return VerifyResult("FAIL", f"ifexp_count={n}",
                        f"found {n} inline conditional expression(s)")


VERIFIERS = {
    "state_file": verify_state_file_task,
}


def verify(task_family: str, artifact: str) -> VerifyResult:
    fn = VERIFIERS.get(task_family)
    if fn is None:
        return VerifyResult("FAIL", "no_verifier",
                            f"no deterministic verifier registered for '{task_family}'")
    return fn(artifact)
