PREREGISTRATION-DESIGN
Trial ID: T-RETRIEVE-01
Lesson under test: L-RETRIEVE — "Retrieve relevant Smart Notes from the corpus at decision time BEFORE answering project-specific questions."

1. HYPOTHESIS
Subjects who are instructed to retrieve relevant Smart Notes from the corpus at decision time BEFORE answering project-specific questions will achieve a higher rate of task success than subjects given the same resources and the same awareness of the corpus but no retrieve-before-answering instruction.
Operationalized: P(subject success | treatment) > P(subject success | control), where subject success = scoring >= 7 correct out of 10 project-specific questions. The isolated behavioral effect is the retrieve-before-answering step itself, not mere knowledge that a corpus exists.

2. ARM DEFINITIONS
Both arms receive their brief text verbatim. The briefs are identical except for the retrieval instruction, so the only contrast between arms is the L-RETRIEVE behavior.

Audit of the draft control brief: the supplied draft ("...consult them as needed before answering. Answer thoroughly using all available resources.") was REJECTED. It instructs the control arm to perform the very retrieval behavior under test ("consult them ... before answering") and further pushes retrieval ("using all available resources"). A control arm told to consult the notes before answering is not a control — it collapses the arm contrast and guarantees a null or attenuated result. The control brief below was rewritten to hold corpus awareness constant while removing every retrieval directive.

CONTROL BRIEF (verbatim, in full):
"You are answering project-specific questions about the project.
Project reference notes exist at: /corpus/notes/.
Answer each of the 10 questions below. Give your best answer to every question."

TREATMENT BRIEF (verbatim, in full):
"You are answering project-specific questions about the project.
Project reference notes exist at: /corpus/notes/.
BEFORE answering any question, FIRST retrieve the relevant Smart Notes from /corpus/notes/ that pertain to that question.
Only after retrieving the relevant notes, answer each question using what you retrieved.
Give your best answer to every question."

3. TASK / QUESTIONS
Each subject answers the same 10 project-specific multiple-choice questions (4 options each, one correct). Each question's correct answer is documented in exactly one designated target Smart Note in /corpus/notes/ (10 target notes total, one per question); the corpus also contains distractor notes. Questions are written so the answer is not inferable without the target note (verified by Gate V2).
Scoring: each question scored 1 (correct) or 0 (incorrect) against a locked answer key; no partial credit. Two independent raters score all answers; discrepancies adjudicated by a third rater.
Primary outcome per subject (binary): SUCCESS = >= 7/10 correct; FAILURE = <= 6/10 correct.
Secondary outcome: mean number correct per arm (descriptive only; no Tier-S claim attached).
Retrieval behavior is measured from access logs of /corpus/notes/ (subject ID, timestamp, file) — specifically whether any corpus file was accessed before the subject's first answer submission — never from self-report.

4. STATISTICS
Primary test: Fisher's exact test, two-sided, on the 2x2 table (arm: control/treatment x outcome: success/failure).
Alpha: 0.05, fixed in advance.
Tier-S bar (both conditions must hold on the primary outcome):
  (a) Fisher's exact two-sided p < 0.05, AND
  (b) Cohen's h >= 1.4 computed on the two success proportions (treatment vs control).
Sample size: N = 30 total, 15 per arm, fixed before launch; no interim looks, no optional stopping. Report: success proportion per arm, difference, Cohen's h, and the exact two-sided p-value.

5. VALIDITY GATES (numeric thresholds + consequence when each fires)
V1 — Corpus integrity: all 10 target notes present at /corpus/notes/ and each verified by the auditor to contain its question's answer. If any target note is missing or lacks the answer -> HALT; fix the corpus and re-audit before any subject is spawned.
V2 — Question validity: 3 pilot subjects with no corpus access and the control brief score mean <= 3/10. If pilot mean > 3/10 -> questions are answerable without retrieval; REWRITE the failing questions and re-pilot before launch.
V3 — Treatment compliance: >= 80% of treatment subjects (>= 12/15) access at least one corpus file before submitting their first answer (per access logs). If below -> trial INVALID; do not interpret the result; diagnose brief adherence and re-run.
V4 — Control contamination: <= 20% of control subjects (<= 3/15) access any /corpus/notes/ file before finishing. If above -> trial INVALID (arm contrast collapsed); re-run with a control brief that withholds corpus location.
V5 — No peeking: zero interim analyses before all 30 subjects complete. If any interim look occurs -> result downgraded to exploratory; Tier-S may not be claimed.
V6 — Scoring reliability: inter-rater agreement >= 95% across all 300 item-scores before adjudication. If < 95% -> re-calibrate raters and re-score all answers.

6. PRE-LAUNCH AUDIT CHECKLIST (all completed before any subject is spawned)
1. Corpus audit: list /corpus/notes/; confirm the 10 target notes exist with exact filenames; record sha256 of each target note.
2. Answer-key lock: commit the answer key and question set; record the commit hash; freeze both.
3. Brief verbatim check: paste both arm briefs into the run configuration and diff character-for-character against Section 2 above; exact match required.
4. Randomization: generate the 15/15 assignment sequence with a seeded RNG; record the seed; keep assignments concealed until spawn.
5. Logging verification: confirm /corpus/notes/ access logging captures subject ID, timestamp, and filename; test with one dummy subject and inspect the log.
6. Pilot run: run 3 no-corpus pilot subjects on the control brief; confirm mean <= 3/10 (Gate V2).
7. Rater calibration: both raters independently score 10 pilot answers; require 100% agreement before launch.
8. Sample-size lock: record N = 30 (15/arm) in the run config; confirm no optional-stopping rule is present.
9. Analysis script: pre-write the Fisher's exact (two-sided) + Cohen's h script; test it on synthetic data and confirm it outputs p and h.
10. Sign-off: auditor initials and timestamp on this checklist; any deviation from it logged as a protocol deviation before launch.
