PREREGISTRATION-DESIGN

Title: Behavioral Trial for Lesson L-RETRIEVE — Mandated Pre-Answer Retrieval vs. Optional Consultation

1. Hypothesis

Subjects who are instructed to FIRST retrieve relevant Smart Notes from the project corpus at decision time, and to base their answers on what they retrieve, will score a higher proportion of correct answers on project-specific questions (whose answers are present only in the corpus) than subjects given an optional-consultation brief. The behavioral effect being isolated is the retrieval-first procedure itself: identical corpus, identical questions, identical scoring — the only difference between arms is whether retrieval precedes answering (mandated, sequenced) or is left to the subject's discretion (optional, "as needed").

2. Arm Definitions

Both arms receive their brief verbatim as the sole instruction block at the start of the session. Nothing else differs between arms.

2a. Control arm brief (audited and rewritten; see Section 6 for the traps in the draft it replaces):

"You are answering project-specific questions. The authoritative answers to these questions live in the project reference notes stored in the corpus at: /corpus/notes/. You may consult the notes if you wish, but you are not required to — answer in whatever way you prefer, including from your own knowledge. Provide your best answer to each question."

2b. Treatment arm brief:

"Before you answer any project-specific question, you MUST first retrieve the relevant Smart Notes from the project corpus. Follow this procedure for EVERY question, in this exact order: (1) Search the corpus at /corpus/notes/ for notes relevant to the question. (2) Open and read the most relevant notes. (3) Only AFTER completing steps 1 and 2, write your answer, grounding it in what the notes say. Do not answer from your own knowledge before you have retrieved and read the notes. If no relevant note exists for a question, say so explicitly and then give your best answer."

3. Task / Questions

Each subject answers 10 project-specific questions. Each question is constructed so that its correct answer appears verbatim or near-verbatim in one or more designated Smart Notes in the corpus, and does NOT reliably appear in the subject's unaided general knowledge (each question is pre-screened: it must contain at least one project-specific fact — a name, date, value, or decision — that is unique to the corpus).

Scoring: Each answer is scored independently by a blinded rater against a written answer key (1 point per question, integer scoring, no partial credit). The rater is blind to arm assignment. The primary outcome for each subject is the proportion correct: (questions correct) / 10.

Secondary observation (not a primary outcome): for the treatment arm, whether the subject's session log shows a corpus search/read before each answer (compliance check).

4. Statistics

- Primary outcome: per-subject proportion correct on the 10 questions.
- Primary comparison: control-arm subjects vs. treatment-arm subjects on proportion correct, tested as a two-sample comparison of proportions (each question response treated as a binary correct/incorrect outcome; pooled across subjects within each arm).
- Test: Fisher's exact test, two-sided.
- Alpha: 0.05.
- Tier-S bar (pre-registered): the trial PASSES if and only if BOTH conditions hold: (a) Fisher's exact two-sided p < 0.05, AND (b) Cohen's h >= 1.4 on the primary outcome proportions (treatment proportion correct vs. control proportion correct, treatment expected higher).

5. Validity Gates

Each gate has a numeric threshold and a fired action. Any fired gate that invalidates the primary outcome marks the trial INCONCLUSIVE rather than PASS or FAIL.

- Gate V1 — Sample size: fewer than 10 subjects completing all 10 questions in EITHER arm. Threshold: n < 10/arm. Fires: trial is underpowered; result reported as INCONCLUSIVE, no Tier-S claim.
- Gate V2 — Ceiling effect: control-arm mean proportion correct >= 0.85. Threshold: >= 0.85. Fires: questions are answerable without retrieval; trial INCONCLUSIVE; questions must be re-screened before any rerun.
- Gate V3 — Floor effect: treatment-arm mean proportion correct <= 0.15. Threshold: <= 0.15. Fires: treatment cannot demonstrate retrieval benefit (notes unusable or procedure broken); trial INCONCLUSIVE.
- Gate V4 — Treatment non-compliance: fewer than 80% of treatment-arm answers preceded by a logged corpus search/read. Threshold: < 80%. Fires: the treatment was not actually delivered; trial INCONCLUSIVE (per-protocol re-analysis permitted as a secondary, non-preregistered readout only).
- Gate V5 — Control contamination: any control-arm subject whose log shows corpus retrieval before answering on 3 or more questions is excluded; if exclusions reduce either arm below 10 subjects, V1 fires. Threshold: >= 3 questions with pre-answer retrieval. Fires: exclude subject, re-check V1.
- Gate V6 — Answer-key coverage: any question on which zero treatment-compliant subjects answered correctly (0/10 or worse) is flagged; if 3 or more of the 10 questions flag, the corpus lacks the needed notes. Threshold: >= 3 flagged questions. Fires: trial INCONCLUSIVE; corpus must be repaired before rerun.
- Gate V7 — Attrition imbalance: completion rate differs between arms by more than 20 percentage points. Threshold: |rate_treatment − rate_control| > 0.20. Fires: investigate differential attrition; if no innocent cause documented, trial INCONCLUSIVE.

6. Pre-Launch Audit Checklist

All checks must be performed and recorded before any subject is spawned. The trial does not launch until every check passes.

1. Corpus path verification: confirm the corpus directory exists at the exact path named in both briefs (/corpus/notes/), is readable by subjects, and contains the designated Smart Notes. Record the absolute path and a file listing with checksums.
2. Answer-key coverage check: for each of the 10 questions, name the specific note file(s) and line span containing the correct answer; two independent reviewers confirm the answer is derivable from those notes alone. Any question failing this is replaced.
3. Unaided-answerability screen: run each question past a held-out screener with NO corpus access; any question the screener answers correctly is replaced (prevents V2 ceiling failures).
4. Draft-brief trap audit (control brief): the starter draft contained three traps, all repaired in the Section 2a brief — (i) it said "Project reference notes are available at" without stating the notes are the AUTHORITATIVE answers, implying optional background material; (ii) "consult them as needed" frames consultation as discretionary, leaking treatment behavior into control is unmeasured; (iii) "Answer thoroughly using all available resources" actively instructs using outside resources/general knowledge, which inflates the control arm and compresses the measurable effect. The rewritten brief removes the resource-solicitation sentence, states the notes hold the authoritative answers, and leaves consultation explicitly voluntary.
5. Arm-parity check: both briefs name the same corpus path, the same question set, the same scoring rule; the ONLY deliberate difference is the mandated retrieve-first procedure in the treatment brief. A reviewer blind to the hypothesis confirms the control brief contains no hidden retrieval mandate and the treatment brief contains an explicit sequencing mandate.
6. Scorer blinding: the scoring rater receives answers labeled by random ID only, with arm assignment withheld; the answer key is frozen (hash recorded) before scoring begins.
7. Randomization: subject-to-arm assignment uses a recorded random seed; assignment log preserved.
8. Dry-run pilot: one pilot subject per arm (data excluded from analysis) completes the full flow; logs confirm treatment-arm retrieval events are captured and control-arm logs are captured.
9. Raw-data storage: designate the persistent storage location (not ephemeral tmpfs) for session logs, answers, and scoring records; verify writability before launch.
10. Gate-threshold freeze: record all Section 5 thresholds and the Section 4 Tier-S bar in the launch log; any post-launch change to a threshold or the bar invalidates the preregistration.
