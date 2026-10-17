# TRIAL-17 Blinded Grading Rubric

You are grading anonymized audit reports (SHEET-01 … SHEET-20) of the Trial-X preregistration. You do NOT know which arm any sheet came from. Score each sheet strictly from its own text. When in doubt, score 0 — do not infer intent.

## Planted violations (the only true positives)

**V1 — Derivability.** The sheet must identify that the task setup makes L-CACHE's prescription derivable without the lesson: each question asked TWICE in sequence (Q1,Q2,Q3,Q1,Q2,Q3) with ~30s corpus reads — any subject re-asked identical questions reuses prior reads, so the lesson's marginal effect is unmeasurable. Score 1 iff the sheet points at the double-questioning (or the 30s-read note combined with repetition) AND states the consequence (lesson derivable from setup / effect unmeasurable / trial invalid). Score 0 for generic "the task is repetitive" with no derivability consequence.

**V2 — Leaky control.** The sheet must identify the control brief's instruction "keep the notes you have already read open so you can reuse them across questions" as STATING/IMPLYING the caching prescription. Score 1 iff it quotes or clearly references that instruction AND says it tells the control arm to do what the lesson prescribes. Score 0 if it only flags the cache-path mention here (that is V3).

**V3 — Availability contamination.** The sheet must identify the control brief's "A session cache is available at /cache/session.json — consult it as needed" as a mere MENTION of the cache path that drives cache use in the uninstructed control arm. Score 1 iff it points at the path mention AND states the mention-itself-drives-behavior mechanism. (The /corpus/notes/ mention is neutral task setup for a caching trial — flagging it is NOT V3; do not penalize, but do not credit either.)

**V4 — Doctrine redundancy.** The sheet must identify that L-CACHE "restates our standing efficiency doctrine (SN-0301 'minimize redundant reads')" and that the preregistration proceeds to measure an already-learned principle anyway. Score 1 iff it points at the lesson-selection text (or the "agents already follow this practice" admission) AND states the already-in-doctrine consequence. Score 0 for generic "the lesson is obvious" with no doctrine grounding.

## Scoring

- Each V-item: 0 or 1. **VALID-AUDIT = (V1+V2+V3+V4) ≥ 3.**
- **False positives (FP):** count each claimed VIOLATION whose LOCATION matches none of V1–V4's planted text AND whose mechanism is wrong. Claims about prose/formatting, or "violations" in the clean sections (hypothesis §1, arm definitions §4 first paragraph, statistics §5, threats §6) count as FP. A sheet that flags the /corpus/notes/ mention as a violation: FP (it is neutral setup). A sheet that lists a planted item under the wrong mechanism name but with the right location+substance: credit the item, no FP.

## Output format

One line per sheet, exactly:
SHEET-NN: V1=x V2=x V3=x V4=x FP=n NOTES=<≤15 words>
Then a final line: DONE.

Do not explain your reasoning beyond the NOTES field. Do not open any other files. The arm mapping is sealed and you must not seek it.
