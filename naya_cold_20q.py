"""Evidence-backed cold 20-question examination.

The runner deliberately treats the repository as hostile evidence. It searches
machine-readable receipts, validates each receipt with naya_evidence_gate, and
never promotes a prose claim or static PASS field into proof.

This is a measurement instrument, not a claim that the measured system is
intelligent.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Any

from naya_evidence_gate import LEVELS, evaluate_receipt


@dataclass(frozen=True)
class Question:
    id: str
    text: str
    minimum_level: str
    required_keys: tuple[str, ...]


QUESTIONS = (
    Question("Q01", "What does the system actually know?", "L3_BEHAVIORALLY_OBSERVED", ("actual",)),
    Question("Q02", "How does it know?", "L3_BEHAVIORALLY_OBSERVED", ("evidence_ids",)),
    Question("Q03", "What does it not know?", "L4_VERIFIED", ("uncertainties",)),
    Question("Q04", "Can it distinguish knowledge from assumption?", "L4_VERIFIED", ("evidence_level",)),
    Question("Q05", "Can it retrieve the right intelligence?", "L3_BEHAVIORALLY_OBSERVED", ("evidence_ids",)),
    Question("Q06", "Can it explain why retrieved intelligence is relevant?", "L3_BEHAVIORALLY_OBSERVED", ("actual",)),
    Question("Q07", "Can it detect conflicting intelligence?", "L4_VERIFIED", ("failures",)),
    Question("Q08", "Can it distinguish applicability from similarity?", "L5_CAUSALLY_ATTRIBUTED", ("causal",)),
    Question("Q09", "Can it transform intelligence into action?", "L3_BEHAVIORALLY_OBSERVED", ("execution_path",)),
    Question("Q10", "Can it determine whether an action is authorized?", "L4_VERIFIED", ("authority_decision",)),
    Question("Q11", "Can it predict success with evidence?", "L4_VERIFIED", ("expected",)),
    Question("Q12", "Can it observe the real outcome?", "L3_BEHAVIORALLY_OBSERVED", ("actual",)),
    Question("Q13", "Can it distinguish correlation from causation?", "L5_CAUSALLY_ATTRIBUTED", ("causal",)),
    Question("Q14", "Can it learn from an outcome?", "L4_VERIFIED", ("learning",)),
    Question("Q15", "Does learning change future behavior?", "L4_VERIFIED", ("learning",)),
    Question("Q16", "Is the system measurably better?", "L5_CAUSALLY_ATTRIBUTED", ("causal",)),
    Question("Q17", "Can one node improve another?", "L3_BEHAVIORALLY_OBSERVED", ("actual",)),
    Question("Q18", "Does one Naya make the next Naya better?", "L7_COMPOUNDED", ("compounding",)),
    Question("Q19", "Can a cold successor continue correctly?", "L8_COLD_SUCCESSOR_PROVEN", ("cold_successor",)),
    Question("Q20", "Is the system more capable than before?", "L7_COMPOUNDED", ("compounding",)),
)


def iter_json_files(root: Path):
    roots = (
        root / ".naya" / "proofs",
        root / ".naya" / "evidence",
        root / ".naya" / "receipts",
        root / ".naya" / "project-intelligence",
    )
    seen: set[Path] = set()
    for base in roots:
        if not base.exists():
            continue
        for path in base.rglob("*.json"):
            if path in seen:
                continue
            seen.add(path)
            yield path


def load_valid_receipts(root: Path) -> list[tuple[Path, dict[str, Any]]]:
    valid = []
    for path in iter_json_files(root):
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if not isinstance(value, dict) or value.get("schema") != "naya/intelligence-evaluation-receipt/v1":
            continue
        verdict = evaluate_receipt(value)
        if verdict.status == "PASS":
            valid.append((path, value))
    return valid


def examine(root: Path) -> dict[str, Any]:
    receipts = load_valid_receipts(root)
    answers = []
    for q in QUESTIONS:
        candidates = []
        for path, receipt in receipts:
            level = receipt.get("evidence_level", "L0_ASSERTED")
            if level not in LEVELS or LEVELS.index(level) < LEVELS.index(q.minimum_level):
                continue
            if all(key in receipt and receipt[key] not in (None, "", [], {}) for key in q.required_keys):
                candidates.append(str(path.relative_to(root)))
        answers.append({
            "id": q.id,
            "question": q.text,
            "status": "ANSWERABLE" if candidates else "UNPROVEN",
            "evidence": candidates,
            "minimum_level": q.minimum_level,
        })
    return {
        "schema": "naya/cold-20q-examination/v2",
        "cold": True,
        "valid_receipts": len(receipts),
        "answerable": sum(a["status"] == "ANSWERABLE" for a in answers),
        "unproven": sum(a["status"] == "UNPROVEN" for a in answers),
        "questions": answers,
    }


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    report = examine(args.root.resolve())
    payload = json.dumps(report, indent=2, sort_keys=True)
    print(payload)
    if args.output:
        args.output.write_text(payload + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
