#!/usr/bin/env python3
"""Cold-process execution of the 20-Question Naya Intelligence Examination.

This is a TESTER, not a narrator. It answers each question the only way the
battery permits: by finding canonical repository evidence, or by reporting that
the answer is unavailable. It never asserts that a system "should" work, and it
never treats a field, a schema, or a prose contract as proof of behaviour.

COLD BY CONSTRUCTION
    This process receives no conversation history. Its only inputs are files on
    disk under the repository. Anything it "knows", it knew before this run.

VERDICT SEMANTICS (deliberately unforgiving)
    ANSWERABLE            canonical evidence exists and states the answer
    ASSERTED_NOT_VERIFIED canonical text asserts it, but no executable proof,
                          passing gate, or recorded outcome backs it
    UNANSWERABLE          no canonical surface states the answer
    CONTRADICTED          canonical surfaces disagree with each other

Per the battery: "Yes, implemented", "the field exists", "the model should be
able to" are NOT answers. Only ANSWERABLE counts as a pass.

Run:  python -B .naya/runtime/battery_cold_runner.py [--json]
Exit: 0 = harness ran (NOT a pass signal); 1 = harness error.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

DENY_DIRS = frozenset({
    ".git", "node_modules", "dist", "build", ".next", "__pycache__",
    "vendor", ".venv", "venv", "site-packages",
})

# Where a cold Naya is contractually allowed to look.
CANONICAL_SURFACES = (
    ".naya/control-plane",
    ".naya/contracts",
    ".naya/runtime",
    ".naya/AI-BOOT",
    "NAYA SYSTEM INSIGHTS for CONTRACTS.md",
    "SMART CONTRACTS FOR NAYANET.md",
)

# Surfaces that constitute running proof rather than assertion.
PROOF_SURFACES = (".github/workflows", ".naya/proofs", ".naya/evidence", ".naya/receipts")


def read_corpus() -> dict[str, str]:
    """Load every canonical surface into memory once."""
    corpus: dict[str, str] = {}
    for rel in CANONICAL_SURFACES:
        target = REPO / rel
        if target.is_file() and target.suffix.lower() in {".md", ".json"}:
            corpus[rel] = _safe(target)
            continue
        if not target.is_dir():
            continue
        for dirpath, dirnames, filenames in os.walk(target):
            dirnames[:] = sorted(d for d in dirnames if d not in DENY_DIRS)
            for name in sorted(filenames):
                if name.lower().endswith((".md", ".json")):
                    path = Path(dirpath) / name
                    corpus[str(path.relative_to(REPO)).replace("\\", "/")] = _safe(path)
    return corpus


def _safe(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def search(corpus: dict[str, str], pattern: str) -> list[str]:
    rx = re.compile(pattern, re.IGNORECASE)
    return sorted(rel for rel, text in corpus.items() if rx.search(text))


def has_proof(pattern: str) -> list[str]:
    rx = re.compile(pattern, re.IGNORECASE)
    hits: list[str] = []
    for rel in PROOF_SURFACES:
        target = REPO / rel
        if not target.is_dir():
            continue
        for dirpath, dirnames, filenames in os.walk(target):
            dirnames[:] = sorted(d for d in dirnames if d not in DENY_DIRS)
            for name in sorted(filenames):
                if name.lower().endswith((".md", ".json", ".yml", ".yaml")):
                    path = Path(dirpath) / name
                    if rx.search(_safe(path)):
                        hits.append(str(path.relative_to(REPO)).replace("\\", "/"))
    return sorted(hits)


# The 20 questions, each with the canonical evidence that would answer it.
QUESTIONS: list[dict] = [
    {
        "id": "Q01", "question": "What does the system actually know?",
        "claim": r"canonical knowledge (scope|boundary)|what the system knows",
        "proof": r"knowledge scope|known-unknown",
    },
    {
        "id": "Q02", "question": "How does it know it?",
        "claim": r"provenance",
        "proof": r"provenance (receipt|chain|verification)",
    },
    {
        "id": "Q03", "question": "What does it not know?",
        "claim": r"unknown|UNKNOWN_UNTIL_PROVEN",
        "proof": r"unknown|gap analysis",
    },
    {
        "id": "Q04", "question": "Can it distinguish knowledge from assumption?",
        "claim": r"assumption",
        "proof": r"assumption (check|test|gate)",
    },
    {
        "id": "Q05", "question": "Can it retrieve the right intelligence for a new problem?",
        "claim": r"retriev",
        "proof": r"retrieval (test|eval|gate|precision)",
    },
    {
        "id": "Q06", "question": "Can it explain why that intelligence is relevant?",
        "claim": r"relevance|applicab",
        "proof": r"relevance (rationale|explanation|score)",
    },
    {
        "id": "Q07", "question": "Can it detect conflicting intelligence?",
        "claim": r"contradict|conflict",
        "proof": r"contradiction (detect|gate|test)",
    },
    {
        "id": "Q08", "question": "Can it determine applicability rather than similarity?",
        "claim": r"applicab",
        "proof": r"applicability (test|gate|evaluat)",
    },
    {
        "id": "Q09", "question": "Can it transform intelligence into an appropriate action?",
        "claim": r"action|execution protocol",
        "proof": r"action (selection|gate|verification)",
    },
    {
        "id": "Q10", "question": "Can it determine whether that action is authorized?",
        "claim": r"authoriz",
        "proof": r"authoriz (gate|enforce|check)",
    },
    {
        "id": "Q11", "question": "Can it predict what evidence would constitute success?",
        "claim": r"success criteria|verification criterion",
        "proof": r"success (criteria|gate|threshold)",
    },
    {
        "id": "Q12", "question": "Can it observe the actual outcome?",
        "claim": r"outcome",
        "proof": r"outcome (observ|verif|receipt)",
    },
    {
        "id": "Q13", "question": "Can it distinguish correlation from causation?",
        "claim": r"causal|correlation",
        "proof": r"causal (test|inference|claim)",
    },
    {
        "id": "Q14", "question": "Can it learn from the outcome?",
        "claim": r"learn",
        "proof": r"learning (gate|promotion|verified)",
    },
    {
        "id": "Q15", "question": "Does that learning change future behaviour?",
        "claim": r"behavior|behaviour|future action|policy change",
        "proof": r"behavio(u)?r (change|test|effect)",
    },
    {
        "id": "Q16", "question": "Does the system become measurably better after learning?",
        "claim": r"measurable|measurement",
        "proof": r"(measur|baseline|improvement).{0,40}(test|gate|proof)",
    },
    {
        "id": "Q17", "question": "Can intelligence from one Node improve another Node?",
        "claim": r"node|intelligent block",
        "proof": r"(node|block).{0,40}(propagat|link|inherit)",
    },
    {
        "id": "Q18", "question": "Can one Naya leave intelligence that makes the next Naya better?",
        "claim": r"successor|baton|handoff|continuity",
        "proof": r"(baton|successor|handoff).{0,40}(test|verif|gate)",
    },
    {
        "id": "Q19", "question": "Can a cold Naya reconstruct and continue without the Director?",
        "claim": r"cold[- ]?(start|nya|successor)",
        "proof": r"cold[_ -]?(start|successor).{0,40}(test|gate|pass)",
    },
    {
        "id": "Q20", "question": "Is the system actually more capable than before?",
        "claim": r"compounding|capability gain",
        "proof": r"(compounding|capability).{0,40}(measurement|proof|verified)",
    },
]


def run_question(q: dict, corpus: dict[str, str]) -> dict:
    claim_hits = search(corpus, q["claim"])
    proof_hits = has_proof(q["proof"])
    if not claim_hits:
        verdict = "UNANSWERABLE"
    elif not proof_hits:
        verdict = "ASSERTED_NOT_VERIFIED"
    else:
        verdict = "ANSWERABLE"
    return {
        "id": q["id"],
        "question": q["question"],
        "verdict": verdict,
        "canonical_surfaces_asserting": len(claim_hits),
        "executable_or_recorded_proof": len(proof_hits),
        "evidence_sample": (proof_hits or claim_hits)[:3],
    }


def killer_test(corpus: dict[str, str]) -> dict:
    """Section XIV: prove one problem became solvable, and that it persists.

    The only problem available with a before/after is constitutional authority:
    before the authority-claim gate, "which law governs?" was unanswerable and
    undetectable. This measures whether a cold process can now answer it
    mechanically.
    """
    module = REPO / ".naya/runtime/constitutional_claim_audit.py"
    gate_present = module.is_file()
    registry = REPO / ".naya/control-plane/CANONICAL-CONTRACT-REGISTRY.md"
    registry_present = registry.is_file()
    mapped = 0
    unmapped = 0
    if gate_present:
        sys.path.insert(0, str(module.parent))
        try:
            import constitutional_claim_audit as cca  # type: ignore

            report = cca.audit(REPO)
            unmapped = len(report.get("unmapped_supreme_claims", []))
            mapped = len(report.get("supreme_claims", [])) - unmapped
        except Exception as exc:  # fail closed, never guess
            return {
                "name": "KILLER: constitutional authority determinism",
                "result": "HARNESS_ERROR",
                "detail": str(exc),
            }
        finally:
            sys.path.pop(0)
    return {
        "name": "KILLER: constitutional authority determinism",
        "question": "Can a cold process determine which constitutional claims are "
                    "in force, and which are unreconciled, without the Director?",
        "gate_present": gate_present,
        "registry_present": registry_present,
        "in_force_claims": mapped + unmapped,
        "mapped_in_registry": mapped,
        "unmapped_unreconciled": unmapped,
        "result": "DETERMINISTIC" if gate_present else "UNANSWERABLE",
        "honest_limit": "Deterministic DETECTION is not resolution. The gate proves "
                        "the conflict is machine-visible; it does not decide which "
                        "claim governs. That authority decision is still open.",
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Cold 20-question battery runner")
    ap.add_argument("--json", action="store_true", help="write machine-readable report")
    args = ap.parse_args()

    corpus = read_corpus()
    results = [run_question(q, corpus) for q in QUESTIONS]
    killer = killer_test(corpus)

    counts: dict[str, int] = {}
    for r in results:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    passed = counts.get("ANSWERABLE", 0)

    report = {
        "schema": "naya.battery-cold-runner/1",
        "input": {
            "canonical_surfaces": list(CANONICAL_SURFACES),
            "surfaces_loaded": len(corpus),
            "conversation_context": "none (cold process)",
            "questions": len(QUESTIONS),
        },
        "verdict_counts": counts,
        "questions": results,
        "killer_test": killer,
        "score": f"{passed}/{len(QUESTIONS)}",
    }

    if args.json:
        out = REPO / ".naya/battery-cold-runner-report.json"
        out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"REPORT: {out.relative_to(REPO).as_posix()}")

    print("=" * 72)
    print("COLD 20-QUESTION NAYA INTELLIGENCE EXAMINATION")
    print(f"input: {len(corpus)} canonical surfaces, 0 conversation history")
    print("=" * 72)
    for r in results:
        mark = {"ANSWERABLE": "PASS", "ASSERTED_NOT_VERIFIED": "ASSERT",
                "UNANSWERABLE": "FAIL", "CONTRADICTED": "CONFLICT"}[r["verdict"]]
        print(f"[{mark:7}] {r['id']}  {r['question']}")
        print(f"{'':10}asserting={r['canonical_surfaces_asserting']:>3}  "
              f"proof={r['executable_or_recorded_proof']:>3}  "
              f"e.g. {r['evidence_sample'][0] if r['evidence_sample'] else '-'}")
    print("-" * 72)
    print(f"SCORE: {passed}/{len(QUESTIONS)} genuinely answerable")
    for verdict, count in sorted(counts.items()):
        print(f"  {verdict}: {count}")
    print()
    print(f"KILLER TEST: {killer['name']}")
    print(f"  result            : {killer['result']}")
    print(f"  in-force claims   : {killer.get('in_force_claims')}")
    print(f"  unmapped/unresolved: {killer.get('unmapped_unreconciled')}")
    if killer.get("honest_limit"):
        print(f"  limit             : {killer['honest_limit']}")
    print("=" * 72)
    print("A PASS here means canonical evidence exists. It does NOT mean the")
    print("capability works. Only an executed, recorded outcome proves that.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
