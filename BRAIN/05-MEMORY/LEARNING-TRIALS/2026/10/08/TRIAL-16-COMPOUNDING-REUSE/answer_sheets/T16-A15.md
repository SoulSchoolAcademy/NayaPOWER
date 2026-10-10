PREREGISTRATION-DESIGN

1. Hypothesis

Treatment-arm subjects who are explicitly instructed to retrieve relevant Smart Notes from the corpus at decision time BEFORE answering will achieve a higher subject-level success rate than control-arm subjects who receive no retrieval instruction, where "success" is defined as answering at least 9 of 12 project-specific questions correctly per the scoring rubric. The behavioral effect being isolated is the marginal effect of the retrieval lesson (L-RETRIEVE): deliberately consulting the Smart Note corpus before answering, over and above whatever a subject can produce from reasoning alone with no corpus access and no retrieval instruction.

2. Arm definitions

The exact brief text each arm receives is written out in full below. Neither brief may be edited after the pre-launch audit without a new audit.

CONTROL BRIEF (final, rewritten — the draft control brief in starter material (a) was REJECTED in audit: it names the corpus path and explicitly instructs consultation of notes, which is both a leaky control briefing (L16 mode 2) and availability contamination (L16 mode 3). It has been replaced):

"You are answering project-specific questions. Read each question carefully and answer to the best of your ability using your own reasoning and knowledge. Give the most accurate answer you can for each question."

TREATMENT BRIEF (final):

"You are answering project-specific questions. Before answering any question, retrieve the relevant Smart Notes from the corpus at /corpus/notes/ and read them. Consult the retrieved notes at decision time, then answer each question using what you found. If a note appears relevant, read it fully before answering."

3. Task/questions

Each subject receives the same 12 project-specific questions. Each question was selected because its correct answer depends on a fact stated only in one specific Smart Note in the corpus (i.e., the fact is not derivable from general knowledge, standing doctrine, or the question wording alone). Subjects answer in writing. Answers are scored against a fixed rubric: 1 point for a fully correct answer (must contain the rubric's required fact elements), 0 otherwise; no partial credit. Scoring is performed blind to arm assignment.

Example question shape (all 12 follow this form): "According to the captured guidance on [project topic], what is the required [procedure/threshold/sequence]? State the exact value or steps." The rubric lists the required fact elements verbatim from the source note.

Subject-level primary outcome: SUCCESS if total score >= 9/12, otherwise FAILURE. The primary outcome is this binary subject-level classification.

4. Statistics

- Test: Fisher's exact test, two-sided, on the 2x2 contingency table of arm (control/treatment) x primary outcome (success/failure).
- Alpha: 0.05.
- Tier-S bar: Fisher's exact two-sided p < 0.05 AND Cohen's h >= 1.4 computed on the primary outcome proportions (treatment success rate vs control success rate).
- Sample size: n = 20 per arm (40 subjects total), fixed in advance; no interim analysis, no optional stopping.

5. Validity gates

Each gate below is checked as stated; if a gate fires, the trial is declared INVALID and no Tier-S claim may be made from it.

- GATE 1 (derivability ceiling / L16 mode 1): pre-launch pilot of n = 5 lesson-free subjects (control brief, no corpus access). If pilot success rate >= 0.40 (i.e., >= 2 of 5 succeed), the task setup is too easy or the prescription is derivable without retrieval — trial INVALID; questions must be redesigned and re-piloted. Pass requires <= 1/5 successes.
- GATE 2 (leaky control briefing / L16 mode 2): grep the finalized control brief for the banned terms: "corpus", "notes" (any casing/plural), "retrie", "consult", "library", "archive", "look up", "search", "/corpus". Required: 0 matches. Any match fires the gate — trial INVALID until the brief is rewritten and re-audited.
- GATE 3 (availability contamination / L16 mode 3): in the control arm, count subjects with any observed corpus access (any file read under /corpus/ or mention of corpus contents in answers). Required: 0 of 20. If >= 1 control subject accesses the corpus, the arm is contaminated — trial INVALID.
- GATE 4 (doctrine redundancy / L16 mode 4): if both arms achieve success rates >= 0.85 (>= 17/20 each), the lesson is redundant with already-learned principles — trial INVALID (ceiling effect).
- GATE 5 (answerability): treatment-arm pilot of n = 5 subjects must reach >= 3/5 successes. If fewer, the questions are not retrieval-dependent or the notes are insufficient — trial INVALID; do not launch the full n = 40.
- GATE 6 (independence): all 40 subjects run in isolated sessions with no cross-talk, no shared context, no visible prior subjects' answers. If any session shares context with another, that subject is excluded and, if exclusions exceed 2 per arm, the trial is INVALID.

6. Pre-launch audit checklist

All checks must be performed and documented before the first subject is spawned:

1. Pilot the full 12-question task with n = 5 lesson-free subjects (control brief, no corpus access); record each score; confirm <= 1/5 succeed (Gate 1).
2. Pilot the full task with n = 5 treatment-brief subjects (with corpus access); confirm >= 3/5 succeed (Gate 5).
3. Grep the finalized control brief for all Gate 2 banned terms; record 0 matches; store the grep output.
4. Confirm the control brief contains no mention of any corpus path, note store, or retrieval instruction (manual read-through by the auditor).
5. Confirm every one of the 12 questions maps to a specific corpus note: for each question, record the note file path and the rubric fact elements; verify each note exists at /corpus/notes/ and contains the required facts verbatim.
6. Confirm the scoring rubric is frozen, written, and stored under version control; scorer blind to arm assignment.
7. Freeze both brief texts exactly as written in Section 2; any subsequent edit triggers a full re-audit.
8. Verify subject-isolation procedure: 40 independent sessions, no shared context, no prompt history visible between subjects; verify the harness cannot leak treatment instructions into control sessions.
9. Confirm n = 20 per arm, alpha = 0.05, Tier-S bar (p < 0.05 AND Cohen's h >= 1.4), no interim looks, fixed at preregistration.
10. Log the audit: auditor name/role, date, SHA or identifier of frozen materials, pilot results table, grep output, and gate verdicts (PASS/FAIL) — all attached to the preregistration record before launch.
