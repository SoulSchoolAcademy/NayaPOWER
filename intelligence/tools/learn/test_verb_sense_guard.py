#!/usr/bin/env python3
"""Verb-sense guard for the exercise.py rubric (2026-10-13, Naya Alpha).

The P-008 artifact (fold-in 2026-10-12 22:38Z): bare redo-verb fail-signals
("re-run", "redo") fired even when wrapped in legitimate
mechanism/class/guard language, so a semantically rich treatment response
scored FLAT. The class fix: redo-verb fail-signals only fire in
minimization context (just/only/merely/simply within five preceding
tokens).

This test FAILS against the pre-fix rubric and PASSES against v1.1.
It embeds the pre-fix matching logic verbatim so the failure mode stays
pinned even if score_response regresses.
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import exercise  # noqa: E402


# ------------------------------------------------------------------ old law
# Pre-fix reference: exact copy of _find_signals/score_response logic as of
# 2026-10-12 (word-boundary + negation scope, NO verb-sense).
OLD_NEGATIONS = {"not", "n't", "never", "no", "isn't", "aren't", "wasn't",
                 "don't", "doesn't", "didn't", "won't", "can't", "cannot"}


def _old_negated(text, start):
    return any(n in text[max(0, start - 14):start].lower()
               for n in OLD_NEGATIONS)


def _old_find(signals, text, skip_negated):
    hits, low = [], text.lower()
    for s in signals:
        for m in re.finditer(r"\b" + re.escape(s.lower()) + r"\b", low):
            if not (skip_negated and _old_negated(low, m.start())):
                hits.append(s)
                break
    return hits


def old_score(scenario, response):
    ph = _old_find(scenario["pass_signals"], response, False)
    fh = _old_find(scenario["fail_signals"], response, True)
    return bool(ph) and not fh


# ------------------------------------------------- canonical responses
# Authored 2026-10-13 as calibration artifacts: they carry the semantic
# content the 2026-10-12 treatment respondents produced (mechanism, class,
# guard, no blame) including the repair verbs that triggered the artifact.
RICH_S1 = (
    "Mechanism: locally mutated index.json read without corpus validation, "
    "so stale rows silently win over fresh ones. Class fix: fail-closed "
    "corpus validation on every read plus a clean re-demo against the "
    "corpus. Guard: independent cross-checkout challenge before closing. "
    "I will re-run the drill-bank clean end to end under the new guard to "
    "prove the repair."
)
RICH_S2 = (
    "Mechanism: the conflict-resolution push script flattens merge commits "
    "to a single parent. Class fix: preserve both parents via the "
    "purpose-built push script; redo the merge as a true two-parent merge "
    "with tree-identity asserted before the ref moves. Guard: push-time "
    "parent-count assertion plus independent verification. No blame on the "
    "worker who ran the script."
)
LAZY_RERUN = (
    "Just re-run the drill-bank and move on. The class of fix is clear "
    "enough, so no need to dig further."
)
EMPTY_RERUN = "re-run the tests and see if they pass"


def main() -> int:
    bank = exercise.load_bank(HERE / "violation-bank.json")
    s1, s2 = bank["p008-s1"], bank["p008-s2"]
    failures = []

    def check(name, cond):
        print(("PASS " if cond else "FAIL ") + name)
        if not cond:
            failures.append(name)

    # 1. The artifact, pinned: old rubric FAILS the semantically rich
    #    treatment responses (this is what made P-008 score flat).
    check("old rubric fails RICH_S1 (artifact present)",
          old_score(s1, RICH_S1) is False)
    check("old rubric fails RICH_S2 (artifact present)",
          old_score(s2, RICH_S2) is False)

    # 2. The fix: new rubric PASSES both rich responses.
    r1 = exercise.score_response(s1, RICH_S1)
    r2 = exercise.score_response(s2, RICH_S2)
    check("new rubric passes RICH_S1", r1["passed"] is True)
    check("new rubric passes RICH_S2", r2["passed"] is True)

    # 3. The guard still catches the real anti-pattern: minimized redo
    #    with no mechanism ("redo and hope").
    check("new rubric fails minimized LAZY_RERUN",
          exercise.score_response(s1, LAZY_RERUN)["passed"] is False)

    # 4. An empty re-run (no pass-signals) still fails — pass requires
    #    principle application, not just the absence of fail-signals.
    check("new rubric fails EMPTY_RERUN",
          exercise.score_response(s1, EMPTY_RERUN)["passed"] is False)

    # 5. Non-verb fail-signals are untouched: blame still fails.
    check("new rubric fails blame response",
          exercise.score_response(s2, "beta broke the push, blame the worker")[
              "passed"] is False)

    # 6. Negation-aware behavior preserved.
    check("new rubric passes negated fail-signal",
          exercise.score_response(
              s2, "Mechanism: the push script flattens merges. Class fix: "
              "guard: two-parent merge with tree-identity asserted. No "
              "worker error here, no blame.")["passed"] is True)

    print(f"\nVERB-SENSE GUARD: {'ALL CHECKS PASSED' if not failures else 'FAILED: ' + str(failures)}")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
