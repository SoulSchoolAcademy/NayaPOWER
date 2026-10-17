PREREGISTRATION-DESIGN

1. Hypothesis

L-RETRIEVE: "Retrieve relevant Smart Notes from the corpus at decision time BEFORE answering project-specific questions."

Precise behavioral effect under isolation: Subjects who receive an explicit retrieval-before-answering instruction will produce a higher proportion of answers that demonstrably incorporate relevant Smart Notes from the corpus (/corpus/notes/) than subjects who receive no such instruction. The isolated effect is the instruction to RETRIEVE FIRST — not access to the corpus (both arms have identical access), not the quality of the corpus, and not answering skill. The primary outcome is binary per question: the answer either demonstrably uses at least one relevant Smart Note from the corpus, or it does not.

2. Arm definitions

CONTROL ARM brief (audited and rewritten — the starter draft contained a retrieval instruction embedded in "consult them as needed before answering", which would have taught the control the very behavior under test; it also referenced /corpus/notes/ explicitly, priming retrieval):

"You are answering project-specific questions. Use your best judgment and answer each question as completely and accurately as you can. There is no time limit."

TREATMENT ARM brief:

"You are answering project-specific questions. Project reference notes (Smart Notes) are available at: /corpus/notes/. Before answering each question, first search /corpus/notes/ for notes relevant to that question, read the relevant ones, and then answer using the retrieved notes together with your best judgment."

Both briefs are frozen for the trial; no other corpus or retrieval instructions may be added by the experimenter.

3. Task/questions

- Subjects: fresh agents (no prior exposure to this trial or the corpus notes), randomized 1:1 to control or treatment.
- Task: each subject answers the same fixed set of 10 project-specific questions. Each question is designed so that at least one Smart Note in /corpus/notes/ is directly relevant (contains information materially improving the answer), while at least one other note is superficially related but irrelevant (decoy), to test whether retrieval is relevant rather than decorative.
- The question set is frozen before launch and identical for both arms; subjects may not consult each other.
- Scoring (binary per question, scored by a blind rater who does not know arm assignment):
  - PASS: the answer demonstrably incorporates the relevant Smart Note — i.e., it states or applies at least one fact or conclusion that is present in the relevant note and not in the question prompt itself.
  - FAIL: otherwise (no corpus content used, or only decoy/generic content).
- Primary outcome: per-question PASS/FAIL proportions, pooled across the 10 questions within each arm (n = 10 questions x number of subjects per arm).

4. Statistics

- Test: Fisher's exact test, two-sided, on the 2x2 contingency table (PASS vs FAIL x treatment vs control), alpha = 0.05.
- Effect size: Cohen's h on the two PASS proportions (treatment minus control), directional expectation treatment > control.
- Tier-S bar: Fisher's exact two-sided p < 0.05 AND Cohen's h >= 1.4 on the primary outcome proportions.
- Sample size: minimum 10 questions x 5 subjects per arm (n = 50 observations per arm) before the bar may be assessed; the trial is not evaluated early. All randomized subjects who begin the task are included in the analysis; subjects who fail to complete all 10 questions are counted as FAIL on unanswered questions (intention-to-treat).

5. Validity gates — numeric thresholds and actions

- Gate 1 — Control contamination: if more than 10% of control answers score PASS via explicit corpus citation (indicating the control arm retrieved anyway, collapsing the isolation), the trial is declared INVALID; no Tier-S claim is made, and the control brief must be redesigned.
- Gate 2 — Question solvability: if the pooled PASS rate in the treatment arm is below 50%, the questions or corpus are too hard / the notes are not findable — the trial is declared INCONCLUSIVE, not a failure of the hypothesis; questions and corpus linkage must be repaired and the trial re-run.
- Gate 3 — Rater reliability: a second blind rater independently scores a random 20% sample of all answers; if inter-rater agreement on PASS/FAIL is below 85% (Cohen's kappa-equivalent check), scoring rules are tightened and the full set is re-scored; results computed before this gate passes are provisional only.
- Gate 4 — Sample integrity: if fewer than 5 subjects per arm complete the task, the trial is UNDERPOWERED and the Tier-S bar may not be assessed; recruit more subjects before any inference.

6. Pre-launch audit checklist

1. Brief isolation check: verify neither brief contains the words "retrieve", "search", "consult", "reference", "notes", or any path/URL, except the treatment brief's single authorized retrieval instruction. Confirm the control brief contains no corpus pointer.
2. Corpus freeze: record the SHA-256 hash of every file under /corpus/notes/ and lock the directory read-only for the trial duration; any corpus change invalidates the run.
3. Question-notes mapping: for each of the 10 questions, an independent reviewer (not the trial designer) confirms in writing that at least one note is directly relevant and at least one decoy note exists.
4. Scoring rubric lock: the PASS/FAIL definitions and the blind-rater protocol are written down, dated, and frozen; raters are blinded to arm assignment before scoring begins.
5. Randomization: subjects are assigned by a fixed pre-generated randomization list (seed recorded) 1:1 to arms; assignment is concealed from raters.
6. Subject freshness: confirm each subject has no prior exposure to this trial, its questions, or /corpus/notes/ contents; subjects may not share information with each other.
7. Results storage: raw answers, rater scores, and the randomization list are committed to the evidence branch before any statistics are computed; results are never kept in /tmp or other ephemeral storage.
