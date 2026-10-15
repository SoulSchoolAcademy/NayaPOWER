# 31 — DECISION: the calculators, how to use them
*Author: Naya Verity Scale · Shawn's order, 2026-10-15.*

## THE LAW
The math advises; the protocol authorizes. A score is a decision aid, never an authority loophole.

## HOW A NAYA BEHAVES HERE
- **Do** run hard gates first: an action that violates a non-negotiable protection is DISQUALIFIED, not scored low — disqualification is exclusion, not zero points (`kernel/decision_principle.py`).
- **Do** show the full decision packet: problem, options, consequences, scores, evidence, unknowns, recommendation, and the exact human decision required — never "what do you want to do?"
- **Do** use the existing seams: `NAYANODE/0025-VALUE-CALCULUS-SPECIFICATION-V1.md`, `kernel/value_calculus.py`, the V2.1 schemas. Never invent another scorecard or decision engine.
- **Do** treat "I don't know yet" as a complete, honorable answer — never manufacture confidence.
- **Don't** let any number override a hard safety, privacy, constitutional, or authority boundary.
- **Don't** tune weights to produce the answer you want — that's laundering, not calibration.

## WHAT LIVES HERE (real paths on main)
- **`kernel/value_calculus.py`** — the Decision Value Calculus V2.1, as code. Deterministic, dependency-free. Seven quality dimensions with default weights: objective_fit 0.20, evidence_sufficiency 0.20, applicability 0.15, robustness 0.15, reversibility 0.10, blast_containment 0.10, simplicity 0.10. Admissibility states: PROHIBITED / NEEDS_AUTHORITY / NEEDS_EVIDENCE / ADMISSIBLE. Outcomes: ACT / READ_MORE / ASK / REFUSE. Library module (import it; no CLI). Engine version: `DECISION-VALUE-CALCULUS-V2.1`.
- **`kernel/decision_principle.py`** — the two-phase architecture: hard gates first, then `argmax` over admissible options of verified value.
- **`NAYANODE/0025-VALUE-CALCULUS-SPECIFICATION-V1.md`** — the canonical spec the code implements.
- **`.naya/specifications/NAYA-DECISION-VALUE-CALCULUS-V2.1.schema.json`** and **`NAYA-VALUE-RECALIBRATION-V2.1.schema.json`** — the machine schemas.
- **`tools/decision_output.py`** — Layer 5 of the Ultimate Decision Machine: MATH → PLAIN WORDS. Takes Layer 4's `score_options()` result and renders it. Three modes: `human` (default, plain words, recommendation first), `worker` (full structured JSON), `questions` (clarifying questions, never a guess dressed as an answer). Zero network calls. Confidence always shown, whole percent.
- **`tools/protocol/checks/scorecard.py`** — the scorecard arithmetic check: validates a 7-dimension scorecard (objective_alignment, evidence_strength, effect_size, risk-as-safety, reversibility, cost_of_inaction, authority_clearance), weights sum to 1.0, recomputed totals match claimed totals within 1e-6, claimed winner == argmax. Arithmetic fraud fails.
- **Branch `naya5/auto-decision-calculator`** (51e99c0d, unmerged) — the auto-decision-calculator implementation; merge-intent clarification owed. Not on main: treat as candidate, not machinery.

## WHERE INPUTS GO
- A decision to score → build the scorecard record (dimensions, weights, options, claimed totals, scorer) and run it through `tools/protocol/checks/scorecard.py` to prove the arithmetic before anyone trusts the verdict.
- A scored decision to communicate → `tools/decision_output.py decide --scored '<json>' --mode human|worker|questions`.
- Calculator changes → the branch + PR path, never direct to main; needs independent validation like any build.

## HOW TO USE THEM (the procedure, from the repo's own law)
1. **Hard gates first.** Safety, constitutional/governance, privacy, authority, destructive/irreversible risk, credentials/money, production boundaries — not tradeable points. Violations disqualify; they don't score.
2. **Score only admissible options**, in this order: OBJECTIVE → EVIDENCE → EFFECT → RISK → BLAST RADIUS → REVERSIBILITY → COST OF INACTION → NET VALUE → AUTHORITY.
3. **Check the arithmetic**: `python3 tools/protocol/checks/scorecard.py --record '{...}'` — claimed totals must match recomputation; claimed winner must be the argmax. Worked example (run at main by this manual's author): the #2455 revert-vs-remediate scorecard first FAILED the check — my own claimed total for remediate (4.05) didn't match recomputation (4.2). The tool caught my arithmetic before any human had to. Corrected and re-run: `"pass": true` — *"winner 'revert' (9.75) is the math's winner."* That's the tool doing its job.
4. **Render for the reader**: `python3 tools/decision_output.py decide --scored '<scored-json>' --mode human` — recommendation first, why in one or two sentences citing real evidence, honest caveat with confidence. Exit 0 = verdict rendered; 2 = questions / "I don't know yet"; 3 = REQUIRES_SHAWN (a hard gate is present — the gate is the message, stated first). Note: the input must be Layer 4's `score_options()` result — a hand-shaped dict correctly degrades to honest UNKNOWN rather than hallucinating (verified at main; the fail-safe works).
5. **Record the packet**: problem, options, consequences, scorecard, evidence, unknowns, recommendation, exact authorization requested — on the venue, with the raw output linked.

## THE RIGHT WAY
Show every option, its score, and why the winner won — with the math checkable by a stranger. The #2455 revert decision: scored options (revert 9.75 / remediate 4 / escalate 5), tree-equality proof, and the deciding line — *"Fixing a review-bypass with a review-bypass would be the same disease."* Options, scores, evidence, principle — in that order: https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2175#issuecomment-6119779429

## THE WRONG WAY
Scoring with the wrong rubric and calling the number a verdict. A manual was scored 3.0 HOLD by the generic work rubric for "blocking = tests/proof" — but a manual is an instruction set *to achieve* success; it cannot carry proof before it is followed. Re-scored on the document rubric: 7.0. Wrong rubric in, wrong verdict out — the calculator never knew: https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537#issuecomment-6171210114

## WHEN XYZ
- **The calculator says SHIP but the gates are red →** the gates win. The calculator advises; the gates decide. Exit code 3 exists for exactly this: REQUIRES_SHAWN, stated first, never buried.
- **Two options score within noise →** say "too close to call" (exit 2 territory) and let the tie-breakers decide: dependencies first, then learning. False precision is a lie.
- **Someone treats the score as the decision →** correct them on the spot: the scorecard is evidence, the protocol is the authorization. Scores never create authority.

## THE TEST
1. Did hard gates run before scoring — is anything disqualified, not just low-scored?
2. Could a stranger re-derive my winner from my scorecard record alone (dimensions, weights, evidence)?
3. If the score and a hard boundary disagree, which did I follow? (The boundary. Every time.)

## WHERE IT'S ENFORCED
The repo's own law: `kernel/value_calculus.py` ("Value ranks only actions that governance already permits. Scores never create authority."), the Prime Judgment Rule (no score overrides a hard boundary), the five-gate merge dock (a calculator's 9.5 means ready for independent check, never ready to merge). `tools/protocol/checks/scorecard.py` enforces arithmetic honesty mechanically.

---
*Honesty note: exact CLI for `kernel/value_calculus.py` — it is a library module with no CLI; use it by import, or through `tools/decision_output.py`. The `naya5/auto-decision-calculator` branch is unmerged; anything on it is candidate, not machinery. The draft's "scorecard calculator outputs 10.0 SHIP on unverified text" falsifier claim is UNVERIFIED by this author — the verifiable version stands in its place: `scorecard.py` checks arithmetic only; it cannot judge evidence truth, which is exactly why calculator output stays advisory. Eta owns this area's technical completion.*

## SELF-SCORE — 9.5/10
Why not 10: two gaps, both named and both owed to Eta, not closable without inventing — (1) no full worked `decision_output.py` run, because the Layer 4 `score_options()` input schema wasn't verified in this pass (the fail-safe degradation WAS verified); (2) Eta's value-spectrum / three-tongue specifics not yet pinned to repo paths. Everything else on the page was run or read at main by this author: both tools executed, both example links live, every path verified on disk.
