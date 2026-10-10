PREREGISTRATION-DESIGN

PREREGISTRATION FOR BEHAVIORAL TRIAL: L-RETRIEVE
Lesson under test: L-RETRIEVE — "Retrieve relevant Smart Notes from the corpus at decision time BEFORE answering project-specific questions."

---

1. HYPOTHESIS

The isolated behavioral effect is: retrieval-before-answering. Subjects instructed to retrieve relevant Smart Notes from the corpus at decision time, before answering project-specific questions, will produce correct answers on questions whose correct answers are contained only in the corpus notes at a significantly higher rate than control subjects who receive no retrieval instruction and no indication the corpus exists.

The precise claim: the instruction to retrieve (not the existence of knowledge alone) causally increases answer correctness on corpus-gated questions. The control condition is the lesson-free default agent behavior: answering from general reasoning and standing knowledge without any prompt toward a corpus.

2. ARM DEFINITIONS

Each arm below is the EXACT brief text the subject agent receives, verbatim. Nothing is added.

CONTROL ARM BRIEF (exact text):
"You are answering project-specific questions. Answer each question thoroughly. If you are unsure of an answer, say so honestly rather than guessing."

TREATMENT ARM BRIEF (exact text):
"You are answering project-specific questions. Before answering each question, you must retrieve relevant Smart Notes from the learning corpus. The corpus of Smart Notes is available at: /corpus/notes/ — search it and read the notes relevant to the question at decision time, BEFORE you answer. Use what you retrieve to inform your answer. Answer each question thoroughly, using the retrieved notes."

Notes on the briefs:
- The control brief contains NO mention of a corpus, a notes path, notes, retrieval, searching, or consulting resources of any kind. (The draft control brief was rejected in audit: mentioning "/corpus/notes/ ... consult them as needed" is availability contamination per L16 mode 3 — observed to drive control retrieval to 9.0/9 versus 0.0/9 for a true cold control.)
- Both briefs are otherwise identical in length, tone, and answer-expectation wording so that only the retrieval instruction differs.

3. TASK / QUESTIONS

Subjects receive 8 project-specific questions. Each question is designed so that:
- The correct answer is stated explicitly in exactly one Smart Note in /corpus/notes/ (answer key tied to note ID).
- The correct answer is NOT derivable from general reasoning, standing doctrine, or common-sense alone (verified in the pre-launch pilot, see section 6).
- Questions cover different notes across the corpus so retrieval effort is per-question, not once-and-done.

Procedure per subject:
1. Subject receives its arm's brief.
2. Subject receives the 8 questions one at a time.
3. For each question, the subject's answer is recorded. For treatment subjects, the subject must report which note ID(s) it retrieved before answering (enables the retrieval-verification gate in section 5).
4. Subjects have no other tools or context besides the brief, the questions, and (treatment arm only) read access to /corpus/notes/.

Scoring:
- Each question is scored binary: 1 if the answer matches the answer key extracted verbatim (or in substance, judged against a written rubric per question) from the target note; 0 otherwise.
- A subject's score is the count of correct answers out of 8.
- PRIMARY OUTCOME: a binary subject-level outcome — "PASS" if the subject scores >= 6/8, "FAIL" otherwise. Trial analysis is on the proportion of PASS subjects per arm.

Answer keys and per-question scoring rubrics are frozen before launch and attached to this preregistration.

4. STATISTICS

- Primary test: Fisher's exact test (two-sided) on the 2x2 table of PASS/FAIL proportions across the two arms.
- Alpha: 0.05.
- Sample size: 20 subjects per arm (40 total), assigned by random shuffle.
- Tier-S bar: Fisher's exact two-sided p < 0.05 AND Cohen's h >= 1.4 on the primary outcome proportions (PASS rates). Both conditions must hold for a Tier-S pass. Cohen's h is computed on the two arms' PASS proportions.
- Secondary (descriptive only, not gating): mean score out of 8 per arm; retrieval-attempt rate in treatment (share of questions with a reported note ID).

5. VALIDITY GATES

Each gate below has a numeric threshold and a specified consequence. Gates are evaluated in order; a fired gate invalidates the affected inference, as stated.

- GATE 1 — Derivability ceiling (pilot). BEFORE launch, 6 pilot subjects run the task under the exact control brief with no corpus access. Threshold: if >= 2 of 6 pilot subjects score >= 6/8, the task set is rejected as derivable and the trial does not launch. If exactly 1 of 6 reaches >= 6/8, that question is replaced and re-piloted. Consequence: failure = redesign questions, never relaunch the same set.

- GATE 2 — Brief leakage (control audit). Before launch, the control brief text is grepped against the lesson's key content terms: {"retrieve", "retrieval", "corpus", "Smart Note", "notes", "/corpus", "search", "consult", "before answering"}. Threshold: 0 matches allowed. Consequence: any match = rewrite and re-audit; trial does not launch until the grep is clean. (This gate already fired once: the draft control brief mentioning "/corpus/notes/" was rejected and rewritten to the cold version in section 2.)

- GATE 3 — Treatment non-retrieval. Threshold: if fewer than 14 of 20 treatment subjects report retrieving at least one note on at least 6 of 8 questions, the manipulation failed — the result is INCONCLUSIVE, not a null effect. Consequence: report as failed manipulation; do not interpret the arm comparison.

- GATE 4 — Control contamination. Threshold: if >= 2 of 20 control subjects spontaneously reference a corpus, notes, or any path resembling /corpus/notes/ in their answers, the control arm is contaminated. Consequence: trial INVALID — the effect is unmeasurable with this setup; do not report an arm comparison.

- GATE 5 — Doctrine redundancy ceiling. Threshold: if both arms' PASS proportions are >= 0.90 (i.e., >= 18/20 each), the trial is INVALID per doctrine redundancy — the questions do not discriminate a lesson's marginal effect. Consequence: do not claim a pass; redesign with harder, genuinely corpus-gated questions.

- GATE 6 — Evidence preservation. Threshold: 100% of subjects must have their full transcripts (brief, questions, reported note IDs, answers) written to durable storage (a committed branch), not /tmp. Consequence: any missing or tmpfs-only transcript = the corresponding subject is excluded, and if exclusions drop an arm below 15 subjects the trial is INCONCLUSIVE.

6. PRE-LAUNCH AUDIT CHECKLIST

All checks below are performed and signed off before any subject is spawned:

1. [ ] Question pilot complete: 6 lesson-free pilot subjects ran the exact control brief with no corpus access; 0 or 1 of 6 scored >= 6/8 (GATE 1 satisfied); any replaced question re-piloted.
2. [ ] Answer keys and per-question scoring rubrics frozen and attached; each key cites the exact note ID and quote it is drawn from.
3. [ ] Control brief grepped against the leakage term list — 0 matches (GATE 2 clean); the draft mentioning /corpus/notes/ is confirmed removed.
4. [ ] Treatment brief verified to contain the retrieval instruction and the corpus path; control brief verified to contain no corpus mention, no path, no resource language.
5. [ ] Corpus verified: all 8 target notes exist at /corpus/notes/ with the answer-bearing content; no note contains the answer to another question (no cross-contamination of keys).
6. [ ] Randomization script produces a shuffled 20/20 arm assignment; assignment is blind to scoring (scorer sees subject IDs only, not arm).
7. [ ] Durable evidence store ready: target branch and commit path confirmed writable from the runner; /tmp explicitly excluded from the evidence path.
8. [ ] Pre-registered analysis code (Fisher's exact two-sided + Cohen's h on PASS proportions, Tier-S bar as stated) written and run against synthetic data to confirm it executes; no changes to the analysis after launch.
9. [ ] Sign-off: designer's name, date, and this document's hash recorded; any deviation after sign-off is logged as a protocol violation in the final report.
