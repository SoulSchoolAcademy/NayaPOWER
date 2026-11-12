#!/usr/bin/env python3
"""Fail if a competing decision/scoring engine is defined in kernel/.

Prime 2: THE LAW IS THE CODE. The Decision Value Calculus
(kernel/value_calculus.py) is the one decision engine. The activation chain
is the one boot path.

This check uses the AST, so it sees only actual definitions — imports,
comments, docstrings, and string mentions can never trip it. (The previous
grep-based version false-positived on `from kernel.value_calculus import ...`
and on comments, red-lining every PR.)

A file fails the check when, outside the canonical locations, it DEFINES
(module level or nested) a function or class whose name is:
  - the engine's own name (value_calculus, decision_value_calculus, ...), or
  - one of the canonical engine's public scoring/decision functions
    (evaluate_candidates, score_quality, gate_candidate, ...), or
  - a new decision/scoring engine name
    (decision_engine, scoring_engine, score_action, evaluate_decision, ...).

Canonical locations (never flagged):
  - kernel/value_calculus.py        — the one decision engine
  - kernel/protocol/                — machine-law protocol code (domain
                                      evaluators like evaluate_takeover,
                                      which are protocol gates, not a
                                      second decision engine)

Usage: python3 tools/check_no_competing_engine.py [--root PATH]
Exit 0: no competing engine. Exit 1: competing engine defined (lists it).
"""

import ast
import re
import sys
from pathlib import Path

# The canonical engine's public scoring/decision API. A second definition
# of any of these outside the canonical locations is a competing engine.
CANONICAL_ENGINE_NAMES = frozenset({
    "evaluate_candidates",
    "score_quality",
    "delta_value",
    "conservative_value",
    "value_interval",
    "gate_candidate",
    "pareto_frontier",
    "relative_margin",
    "verification_state",
    "interval_gap",
})

# Name patterns for a NEW decision/scoring engine. Matched against the
# normalized (lowercased, underscores removed) definition name.
ENGINE_NAME_RES = [
    re.compile(r"^(the)?decisionvaluecalculus$"),
    re.compile(r"^valuecalculus$"),
    re.compile(r"^(decision|scoring|value|choice|action)engine$"),
    re.compile(r"^score(action|decision|candidate|option|choice)$"),
    re.compile(r"^evaluate(decision|action|choice|candidate)$"),
    re.compile(r"^rank(candidates|actions|options|choices)$"),
    re.compile(r"^choose(action|candidate|option|choice)$"),
    re.compile(r"^decide(action|candidate|option)$"),
    re.compile(r"^(calculate|compute)decisionvalue$"),
    re.compile(r"^decisionvalue$"),
]

ALLOWLIST_FILES = {"kernel/value_calculus.py"}
ALLOWLIST_PREFIXES = ("kernel/protocol/",)


def is_allowlisted(rel: str) -> bool:
    return rel in ALLOWLIST_FILES or rel.startswith(ALLOWLIST_PREFIXES)


def normalized(name: str) -> str:
    return name.lower().replace("_", "")


def is_competing(name: str) -> str | None:
    """Return the reason the name is a competing engine, or None."""
    if name in CANONICAL_ENGINE_NAMES:
        return f"redefines canonical engine function '{name}'"
    norm = normalized(name)
    for rx in ENGINE_NAME_RES:
        if rx.match(norm):
            return f"defines competing engine '{name}'"
    return None


def check_file(path: Path, rel: str) -> list[str]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except (SyntaxError, UnicodeDecodeError) as e:
        return [f"{rel}: unparseable ({e})"]
    hits = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            reason = is_competing(node.name)
            if reason:
                kind = "class" if isinstance(node, ast.ClassDef) else "def"
                hits.append(f"{rel}:{node.lineno}: {kind} {node.name} — {reason}")
    return hits


def main() -> int:
    root = Path(sys.argv[sys.argv.index("--root") + 1]) if "--root" in sys.argv else Path(".")
    kernel = root / "kernel"
    if not kernel.is_dir():
        print(f"error: no kernel/ directory under {root}", file=sys.stderr)
        return 2
    hits: list[str] = []
    for path in sorted(kernel.rglob("*.py")):
        rel = path.relative_to(root).as_posix()
        if is_allowlisted(rel):
            continue
        hits.extend(check_file(path, rel))
    if hits:
        print("FAIL: competing decision/scoring engine detected in kernel/:")
        for h in hits:
            print(f"  {h}")
        print("The Decision Value Calculus (kernel/value_calculus.py) is the one decision engine.")
        return 1
    print("OK: one decision engine (kernel/value_calculus.py), one boot path")
    return 0


if __name__ == "__main__":
    sys.exit(main())
