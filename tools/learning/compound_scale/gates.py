"""The six compounding gates. Each returns (score 0-9, detail).

Verdict = minimum gate. Lesson PROVEN iff verdict >= 7.0.
Adversarial lessons pass iff the Truth gate correctly REJECTS them
(they are never injected).

Honesty note (D32): the Truth gate verifies CITATION INTEGRITY — the
cited evidence exists verbatim in the cited source, and for adversarial
lessons the pre-registered contradiction evidence exists too. It does not
do semantic entailment; the claim<->evidence binding is pre-registered and
auditable by an independent seat.
"""
from __future__ import annotations

import json
import re
from pathlib import Path


def _read_receipt(path_str: str) -> str | None:
    p = Path(path_str).expanduser()
    if not p.is_file():
        return None
    try:
        return p.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


# ------------------------------------------------------------------ 1. Truth
def gate_truth(lesson: dict) -> tuple[int, str]:
    truth = lesson["truth"]
    mode = truth["mode"]
    content = _read_receipt(truth["receipt_file"])
    if content is None:
        return 0, f"receipt file missing: {truth['receipt_file']}"
    quote = truth["receipt_quote"]
    if quote not in content:
        return 4, "receipt file exists but the cited quote is not in it"
    if mode == "must_hold":
        return 9, "cited evidence present verbatim in cited source"
    # must_contradict: the pre-registered contradiction must ALSO be present.
    contra = truth.get("contradicting_quote", "")
    if contra and contra not in content:
        return 2, ("adversarial probe failed: the pre-registered contradiction "
                   "evidence is not in the cited source — rejection unearned")
    return 9, ("REJECTED: cited source contradicts the claim "
               f"({contra[:60]!r}...) — lesson refused before inject")


# ---------------------------------------------------------- 2. Understanding
_STOP = set("the a an to of in on for with is are be by as at or and not no "
            "it its this that you your we our they their from into over under "
            "never always when what how do does did will would should must can "
            "if then than so such only just".split())


def _tokens(s: str) -> set[str]:
    return {t for t in re.findall(r"[a-z0-9`]+", s.lower()) if t not in _STOP}


def comprehension_probe(distilled: str, lesson: dict) -> tuple[bool, str]:
    """The subject gets ONLY the distilled one-liner and must pick the
    right action from 3 options. Scored by informative word overlap: the
    probe passes iff the correct option outscores both others. A vague
    distilled sentence fails this honestly."""
    comp = lesson["comprehension"]
    operative = _tokens(lesson["distill"]["operative_action"])
    d = _tokens(distilled)
    scores = []
    for opt in comp["options"]:
        o = _tokens(opt)
        shared = o & d
        # Only words present in the DISTILLED text count; operative terms
        # (the action the lesson teaches) weigh double. A vague distilled
        # sentence shares nothing -> all zeros -> probe fails honestly.
        scores.append(len(shared) + 2 * len(shared & operative))
    best = max(range(len(scores)), key=lambda i: scores[i])
    if best == comp["answer"] and scores[best] > max(
            [s for i, s in enumerate(scores) if i != best] + [0]):
        return True, f"correct option wins on distilled text ({scores})"
    return False, f"distilled text does not discriminate options ({scores})"


def gate_understanding(lesson: dict, distilled: str) -> tuple[int, str]:
    operative = lesson["distill"]["operative_action"]
    if operative not in distilled:
        return 2, "distilled sentence lost the operative action"
    ok, why = comprehension_probe(distilled, lesson)
    if ok:
        return 9, f"operative preserved + {why}"
    return 5, f"operative preserved but {why}"


# ---------------------------------------------------------------- 3. Effect
def gate_effect(arms: dict) -> tuple[int, str]:
    t = arms["treatment"]["passed"]
    c = arms["control"]["passed"]
    if t and not c:
        return 9, "treatment passes, control fails: behavior changed"
    if t and c:
        return 5, "both pass: no behavioral contrast (lesson unneeded here)"
    if not t:
        return 1, f"treatment failed: {arms['treatment']['reason'][:100]}"
    return 3, "control passed but treatment failed: inverted"


# -------------------------------------------------------------- 4. Causality
def gate_causality(arms: dict) -> tuple[int, str]:
    cc, tc = arms["control"]["context_canonical"], arms["treatment"]["context_canonical"]
    cj, tj = json.loads(cc), json.loads(tc)
    # isolation: contexts must differ ONLY by the injected rule
    control_minus = [r for r in cj]
    treatment_minus = [{k: v for k, v in r.items()} for r in tj]
    isolated = (len(tj) == len(cj) + 1 and cj == tj[:len(cj)] or
                (not cj and len(tj) == 1))
    contrast = arms["treatment"]["passed"] and not arms["control"]["passed"]
    applied = arms["treatment"].get("applied_rule")
    if isolated and contrast and applied:
        return 9, "arm isolation holds; only difference is the injected rule"
    if not isolated:
        return 2, "contexts differ by more than the injection"
    if not contrast:
        return 4, "isolated but no behavioral contrast"
    return 6, "isolated with contrast but rule application unrecorded"


# ------------------------------------------------------------- 5. Durability
def gate_durability(durable_passed: bool, detail: str) -> tuple[int, str]:
    if durable_passed:
        return 9, f"fresh-process reload re-verified: {detail[:100]}"
    return 1, f"did not survive the process boundary: {detail[:100]}"


# --------------------------------------------------------------- 6. Transfer
def gate_transfer(mech_passed: bool, real_passed: bool | None) -> tuple[int, str]:
    # 9 = cold real agent reproduces blind; 8 = mechanical stateless successor
    # via the persisted-store inject path reproduces.
    if real_passed:
        return 9, "cold real successor reproduced the behavior blind"
    if mech_passed:
        return 8, "stateless mechanical successor reproduced via stored lesson"
    return 1, "successor did not reproduce"


def verdict(scores: dict[str, int]) -> tuple[float, str]:
    v = min(scores.values())
    return float(v), f"verdict = min gate = {v}"
