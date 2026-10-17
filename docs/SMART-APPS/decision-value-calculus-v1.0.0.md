# Decision Value Calculus — Smart App v1.0.0 (Frozen)

**Smart App ID:** `nayapower.decision-value-calculus`
**Frozen version:** 1.0.0
**Engine version:** DECISION-VALUE-CALCULUS-V2.1
**Module:** `kernel/value_calculus.py`
**Frozen on:** 2026-10-10 (Workstream 9 — First True Smart App, #1354)
**Status:** FROZEN. Use it; do not rebuild it.

---

## In plain words

This is the math every Naya uses to make a decision. You give it your options,
it tells you which one wins and why — or it tells you to stop.

It answers four questions, in order:

1. **Is this even allowed?** — hard gates first. Forbidden things stay forbidden,
   no matter how good they score. Things that need Shawn's word get flagged as
   needing Shawn's word. Things missing evidence get flagged as missing evidence.
2. **How good is each option?** — seven kinds of goodness: does it fit the goal,
   is there enough evidence, does it apply to this situation, how solid is it,
   can it be undone, how contained is the blast if it goes wrong, how simple is it.
3. **Which one wins?** — it compares every option against the do-nothing
   baseline and picks the clear winner. If it's a near-tie, it says "go read
   more" instead of guessing.
4. **What happened?** — it writes a receipt you (or any other Naya) can
   re-check later, independently, from the same inputs.

The golden rule is in the code's own words: **scores never create authority.**
A high score on a forbidden action does not permit it. The math advises;
governance decides.

---

## How to call it

```python
from kernel import value_calculus as vc

# 1. Describe what "good" means for THIS decision
profile = vc.QualityProfile(
    profile_id="MY-LANE-DECISION",
    version="1.0",
    objective="pick the repair that heals the most with the least risk",
    min_evidence_count=2,
    relative_margin=0.10,   # winner must beat runner-up by 10%+ or it's READ_MORE
)

# 2. Describe each option
def opt(cid, quality_score, benefit):
    q = {d: quality_score for d in vc.QUALITY_DIMENSIONS}
    c = {k: 0.95 for k in ("B", "H", "C", "R")}
    return vc.Candidate(
        cid, q, c, vc.PVEstimate(benefit, 0, 1, 0.2, c, 3),
        authorized=True, reversible=True, is_baseline=(cid == "do-nothing"),
        lawful=True, rights_safe=True, privacy_safe=True, safety_safe=True,
    )

# 3. Run the math
result = vc.evaluate_candidates(
    [opt("do-nothing", 9.0, 0), opt("repair-a", 9.0, 40), opt("repair-b", 6.0, 25)],
    "do-nothing", profile,
)
print(result["decision"])   # ACT | READ_MORE | ASK | REFUSE
print(result["selected"])    # "repair-a"
```

Other entry points for common jobs:

| Job | Call |
|---|---|
| Gate one option through hard gates | `vc.gate_candidate(candidate, profile, vc.RiskPolicy())` → `(verdict, reasons, detail)` |
| Score one option's quality (0–10) | `vc.score_quality(candidate, profile)["Q"]` |
| Rank next-best actions (the NBA overlay) | `vc.rank_next_best_actions([vc.NextBestActionCandidate(...)])` |
| Write a decision receipt | `vc.build_decision_receipt(decision_id=..., objective=..., ...)` |
| Re-check someone else's receipt independently | `vc.independent_recompute(receipt, candidates, profile)` |
| Score a contribution (compounding points) | `vc.contribution_value_score(quality=..., relevance=..., ...)` |

Verdicts you will see: `PROHIBITED`, `NEEDS_AUTHORITY`, `NEEDS_EVIDENCE`,
`ADMISSIBLE` (the gate), and `ACT`, `READ_MORE`, `ASK`, `REFUSE` (the decision).

---

## What it guarantees

- **Deterministic.** Same inputs → same outputs, every time. The freeze test
  proves it on every CI run.
- **No dependencies.** Python standard library only. Nothing to install.
- **Frozen interface.** The public functions, classes, and constants listed in
  `tests/test_value_calculus_smart_app_freeze_v1.py` cannot change without a
  new major version. CI fails the build if they do.
- **Gates before scores.** Hard gates (prohibited / needs-authority /
  needs-evidence) are evaluated first; no score can override them.
- **Independent re-checking.** Any receipt can be recomputed by a different
  seat from the same inputs via `independent_recompute`.
- **52+ existing tests** on the engine (`tests/test_value_calculus.py`) plus
  the freeze lock (`tests/test_value_calculus_smart_app_freeze_v1.py`).

## What it will never do

- Never grant authority. `ADMISSIBLE` means "governance permits this", not
  "you may do it".
- Never change its interface silently. Breaking change = new major version
  (2.0.0), with a migration note. Additive change (new optional parameter,
  new function) = new minor version, announced.
- Never get rebuilt. If the math needs to change, it changes HERE, versioned,
  with the full test battery — not in a copy.

## How to propose a change

1. Open an issue describing the hole (the engine at 10 has no holes; prove
   the hole exists with a failing case).
2. PR against `kernel/value_calculus.py` + update the frozen baseline in the
   freeze test + bump `SMART_APP_VERSION`.
3. Green CI at exact tip, builder + independent scores on the receipt.
4. Breaking changes need the same authority as a constitutional change:
   they alter every consumer.

## For cold successors

If you just activated and need decision math: this is it. Import it. Do not
write your own scorecard, your own gate, or your own weighted comparison —
the repo's standing law (AGENTS.md, "One decision engine") says so, and this
frozen module is why the law is enforceable.
