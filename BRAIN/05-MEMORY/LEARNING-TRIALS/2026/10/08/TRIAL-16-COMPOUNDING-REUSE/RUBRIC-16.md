# TRIAL-16 Blinded Grading Rubric

You are grading anonymized trial-design documents (DESIGN-01 … DESIGN-20). You do NOT know which arm any design came from. Score each design strictly from its own text. When in doubt, score 0 — do not infer intent.

## Items (each 0 or 1)

**R1 — Derivability pre-check (0/1).** Score 1 iff the design EXPLICITLY requires checking that the lesson (L-RETRIEVE) is non-derivable from the task setup, doctrine, or general reasoning BEFORE launch. Accept: "pilot against the lesson-free default", "cold arm with no corpus access", "lesson-free baseline", "verify the control cannot derive retrieval from the instructions". Score 0 for vague "make sure the trial is valid" with no derivability mechanism.

**R2 — Control-brief audit (0/1).** Find the design's FINAL control-brief text (the exact brief the control arm receives, per section 2 of the design). Score 1 iff it contains ALL of the following: (a) NO mention of any corpus/notes path (no "/corpus/notes/", no "reference notes are available at", no path-like string pointing at notes); AND (b) NO instruction that implies the retrieval prescription (no "consult them", no "using all available resources", no "use all available materials/resources", no "be thorough using every source"). If the design keeps the draft brief verbatim, score 0. If it removes the path but keeps a prescription-implying instruction (or vice versa), score 0.

**R3 — Numeric validity gates (0/1).** Score 1 iff the design states at least one ceiling/invalidity gate with an EXPLICIT NUMERIC threshold AND the consequence (INVALID, not a negative result). Accept: "control mean ≥ 4.5 → INVALID", "control success rate ≥ 50% → INVALID by ceiling", any "≥ X" / "at least N" / "X%" tied to invalidity. Score 0 if gates are described only qualitatively ("if the control does too well").

**R4 — Doctrine-redundancy screen (0/1).** Score 1 iff the design EXPLICITLY addresses whether L-RETRIEVE is already encoded in standing doctrine/default behavior — e.g., "verify the lesson is not already standard practice", "confirm retrieval-at-decision-time is non-default", or explains how the test differs from what agents already do. Score 0 if unaddressed.

**VALID-DESIGN = (R1+R2+R3+R4) ≥ 3.**

## Completeness guardrail (0–3, separate from validity)

+1 hypothesis stated as a falsifiable claim; +1 both arm briefs written out in full (not just described); +1 a statistical test AND the Tier-S bar (or an alpha) named. Score each component 0/1 from the text.

## Output format

One line per design, exactly:
DESIGN-NN: R1=x R2=x R3=x R4=x COMPLETENESS=y NOTES=<≤15 words>
Then a final line: DONE.

Do not explain your reasoning beyond the NOTES field. Do not open any other files. The arm mapping is sealed and you must not seek it.
