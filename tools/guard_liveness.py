#!/usr/bin/env python3
"""Guard liveness: a refusal that cannot be observed to fire is not a guard.

Enforces SN-0468 (fail closed, always) in a measurable form: "closed" must mean a test
can watch the guard reject something. Also the machine-checkable half of SN-0461
(source-text assertions are green by construction) -- a grep reference to a refusal
literal is explicitly NOT firing evidence, because that is the exact shape that let a
real defect ship while CI stayed green.

Why this exists
---------------
The most expensive defect class in this repo is the silent one:

  - ``nayanet-verified-ai-action`` called ``insertIdempotentActionReceipt`` with two
    arguments against a three-parameter declaration. ``idempotency_key`` was therefore
    ``undefined`` on every governed action receipt, and because the enforcing unique
    index is partial (``where idempotency_key is not null``) replays never collided.
    The replay guard, the ``IDEMPOTENCY_KEY_REUSE_CONFLICT`` check, and the
    fingerprint comparison were all unreachable. It failed OPEN and said nothing.
  - ``nayanet-know-runtime/know.ts`` guarded authority expiry with
    ``if (x === NaN || Number.isNaN(x))`` where ``parsedTime`` returns
    ``number | null``. The ``=== NaN`` half can never be true, so half of two
    authority-expiry guards was dead code.

Both look identical from outside: a guard-shaped branch that never fires. Neither is
findable by reading, by grepping, or by a type checker. Both are findable by asking one
question -- **can I watch this thing reject something?**

Method
------
For each refusal literal emitted by a runtime surface, require evidence that a test
*executes* the code and observes the refusal. Output is JSON so CI can diff it.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RUNTIME_DIRS = ["supabase/functions", "kernel", "BRAIN/12-ENGINEERING"]

# Refusal literals: reason strings a handler returns when it DENIES or BLOCKS.
#
# The refusal-context requirement is load-bearing. `reason:` alone matches success
# reasons too (`LAW_AND_LIVE_AUTHORITY_MATCH`, `ACTIVE_IN_SCOPE_GRANT`), and counting
# those would inflate the denominator -- a scanner that flatters its own numbers is
# exactly the theater this gate exists to detect. So a `reason:` literal only counts
# when it appears in a return that also declares failure.
REFUSAL_PATTERNS = [
    # json({ok:false, error:"LITERAL", ...}) and multi-line variants
    re.compile(r'ok\s*:\s*false[^{}]{0,200}?error\s*:\s*"([A-Z][A-Z0-9_]{6,})"', re.S),
    re.compile(r'error\s*:\s*"([A-Z][A-Z0-9_]{6,})"[^{}]{0,200}?ok\s*:\s*false', re.S),
    # {ok:false, reason:"LITERAL"}
    re.compile(r'ok\s*:\s*false[^{}]{0,200}?reason\s*:\s*"([A-Z][A-Z0-9_]{6,})"', re.S),
    re.compile(r'reason\s*:\s*"([A-Z][A-Z0-9_]{6,})"[^{}]{0,200}?ok\s*:\s*false', re.S),
    # blocking attribution
    re.compile(r'\bblocked_by\s*=\s*"([A-Z][A-Z0-9_]{6,})"'),
    re.compile(r'throw new Error\(\s*"([A-Z][A-Z0-9_]{6,})"'),
    re.compile(r'\braise\s+Exception\(\s*\'([A-Z][A-Z0-9_]{6,})'),
]

# Literals that name a SUCCESS. Excluded explicitly and reported, because a reviewer
# seeing them in the "unproven guards" list would rightly ask why a pass is listed.
SUCCESS_LITERALS = {
    "LAW_AND_LIVE_AUTHORITY_MATCH",
    "ACTIVE_IN_SCOPE_GRANT",
    "OWNER_SCOPED_CURRENT_BLOCK_MATCHES_REQUIRED_CAPABILITY",
}

# A firing proof must EXECUTE code and assert the literal as an observed outcome.
# These are the shapes that count.
EXECUTED_PROOF_PATTERNS = [
    re.compile(r'\.runInNewContext\(|vm\.'),          # node VM sandbox execution
    re.compile(r'^\s*from\s+kernel\.', re.M),          # python kernel import
    re.compile(r'\bexecute_cycle\(|\.decide\('),       # direct kernel invocation
    re.compile(r'\.invoke\(|\bhandleCycle\(|\breceipt\['),  # handler driven end to end
    # Direct named import from a runtime module. You cannot execute a module's own
    # function without importing it, so this is itself evidence of execution.
    #
    # This signal was MISSING in the first version, which only recognised VM-sandbox
    # execution. A full suite of direct-call firing proofs therefore scored 0 and the
    # coverage number did not move -- the detector could not see real proof work. A
    # detector blind to genuine evidence is worse than no detector, because it reports a
    # confident number that is wrong.
    re.compile(r'import\s*\{[^}]*\}\s*from\s*["\'][^"\']*(?:\.\./)?(?:supabase/functions|kernel)/', re.S),
]


def collect_refusals() -> list[dict]:
    found: dict[str, dict] = {}
    for rel_dir in RUNTIME_DIRS:
        base = ROOT / rel_dir
        if not base.exists():
            continue
        for path in sorted(base.rglob("*")):
            if path.suffix not in {".ts", ".py"} or not path.is_file():
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            for pattern in REFUSAL_PATTERNS:
                for match in pattern.finditer(text):
                    literal = match.group(1)
                    if literal in SUCCESS_LITERALS:
                        continue
                    line = text[: match.start()].count("\n") + 1
                    entry = found.setdefault(
                        literal,
                        {"literal": literal, "sites": []},
                    )
                    entry["sites"].append(
                        {"file": str(path.relative_to(ROOT)).replace("\\", "/"), "line": line}
                    )
    return [found[k] for k in sorted(found)]


def load_tests() -> list[dict]:
    tests_dir = ROOT / "tests"
    out = []
    for path in sorted(tests_dir.iterdir()):
        if path.suffix in {".py", ".mjs"} and path.is_file():
            out.append(
                {
                    "file": path.name,
                    "text": path.read_text(encoding="utf-8", errors="replace"),
                }
            )
    return out


def is_executed_test(text: str) -> bool:
    return any(p.search(text) for p in EXECUTED_PROOF_PATTERNS)


def firing_evidence(literal: str, tests: list[dict]) -> dict:
    """Find a test that executes runtime code AND asserts this literal as an outcome.

    Importing a runtime module is necessary but not sufficient: a test can import one
    module and then grep a *different* handler for a literal. So the literal must appear
    on a line that is not a source-read assertion. A line mentioning `source` (the
    conventional name for a readFileSync result) is treated as grep-only, which keeps
    SN-0461 out of the proven column even when the file also imports runtime code.
    """
    referencing = [t for t in tests if literal in t["text"]]
    executed: list[str] = []
    grep_only: list[str] = []

    for t in referencing:
        if not is_executed_test(t["text"]):
            grep_only.append(t["file"])
            continue
        outcome_lines = [
            line for line in t["text"].splitlines()
            if literal in line and not re.search(r'\b(source|src|code)\b', line)
        ]
        if outcome_lines:
            executed.append(t["file"])
        else:
            grep_only.append(t["file"])

    return {
        "executed_proofs": sorted(set(executed)),
        "grep_only": sorted(set(grep_only)),
        "firing_observed": bool(executed),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    parser.add_argument(
        "--fail-under",
        type=float,
        default=None,
        help="exit nonzero if coverage is below this percentage. Default: report only. "
        "The pass/fail decision belongs to the committed ratchet floor "
        "(tools/guard-liveness-floor.json), not to this script -- a tool that fails at "
        "the honest starting number blocks every merge and trains people to bypass it.",
    )
    args = parser.parse_args()

    refusals = collect_refusals()
    tests = load_tests()

    rows = []
    for refusal in refusals:
        ev = firing_evidence(refusal["literal"], tests)
        rows.append({**refusal, **ev, "sites_count": len(refusal["sites"])})

    proven = [r for r in rows if r["firing_observed"]]
    unproven = [r for r in rows if not r["firing_observed"]]
    pct = (len(proven) / len(rows) * 100.0) if rows else 100.0

    if args.json:
        print(
            json.dumps(
                {
                    "total_guards": len(rows),
                    "with_firing_proof": len(proven),
                    "without_firing_proof": len(unproven),
                    "pct_with_firing_proof": round(pct, 1),
                    "unproven": unproven,
                },
                indent=2,
            )
        )
        return 0 if args.fail_under is None or pct >= args.fail_under else 1

    print("GUARD LIVENESS")
    print("=" * 78)
    print("A refusal literal with no executed test that observes it is a guard")
    print("that cannot fire. Source-grep references do not count -- that is the very")
    print("defect class this gate detects.")
    print("-" * 78)
    print(f"refusal literals found        : {len(rows)}")
    print(f"with executed firing proof    : {len(proven)}")
    print(f"without firing proof          : {len(unproven)}")
    print(f"coverage                      : {pct:.1f}%")
    if unproven:
        print("\nGUARDS THAT CANNOT BE OBSERVED TO FIRE:")
        for r in sorted(unproven, key=lambda x: -x["sites_count"]):
            sites = ", ".join(f"{s['file']}:{s['line']}" for s in r["sites"][:3])
            more = f" (+{r['sites_count'] - 3} more)" if r["sites_count"] > 3 else ""
            grep = f"   [grep-only refs: {', '.join(r['grep_only'][:2])}]" if r["grep_only"] else ""
            print(f"  {r['literal']:<44} {sites}{more}{grep}")
    print("=" * 78)
    print("Reading: a guard listed here may be perfectly correct code. What is NOT")
    print("proven is that it has ever rejected anything. That is the gap to close.")
    return 0 if args.fail_under is None or pct >= args.fail_under else 1


if __name__ == "__main__":
    raise SystemExit(main())
