PREREGISTRATION-DESIGN

Trial: L-RETRIEVE Trial 1 (T1)
Lesson under test: L-RETRIEVE — "Retrieve relevant Smart Notes from the corpus at decision time BEFORE answering project-specific questions."

1. HYPOTHESIS

Precise claim: Subjects instructed to retrieve relevant Smart Notes from the corpus BEFORE answering (retrieve-first instruction) will achieve a higher mastery rate on corpus-dependent project questions than subjects given the same questions and the same corpus access without a retrieve-first instruction.

- Isolated behavioral effect: the decision-time instruction to retrieve relevant notes BEFORE answering, holding constant corpus access, the question set, answer format, model, and decoding parameters.
- Null hypothesis (H0): the proportion of subjects reaching mastery is equal in both arms.
- Alternative (H1): the treated arm's mastery proportion exceeds the control arm's.
- Mechanism: retrieve-first grounds answers in project-specific recorded facts; without it, subjects default to parametric/general knowledge and guess on corpus-specific facts.
- Primary outcome (binary per subject): MASTERY = at least 8 of 10 questions answered correctly (per the locked answer key).

2. ARM DEFINITIONS

Both arms receive the identical 10 questions, the identical corpus path, identical answer-format instructions, and run on the identical pinned model with identical decoding settings. The briefs differ ONLY in the retrieval instruction. Each subject sees exactly one brief, once. The draft control brief supplied in the brief materials was audited and REJECTED for two traps: (a) "consult them as needed" makes retrieval optional in both arms, erasing the manipulation; (b) "Answer thoroughly using all available resources" actively pushes the control arm toward retrieval, destroying arm separation. Both phrases are banned from both briefs (see checklist item 5).

TREATED ARM — brief text in full:
---
You are answering 10 project-specific questions. The project reference notes (Smart Notes) are available at: /corpus/notes/

Work in exactly this order:
1. FIRST, before writing any answer, retrieve the Smart Notes from /corpus/notes/ that are relevant to the questions. Read them.
2. THEN answer each question, basing your answers on the notes you retrieved.

Answer each question with a short, direct factual answer (a name, a date, a number, or one sentence). If you cannot determine the answer, write "unknown".
---

CONTROL ARM — brief text in full:
---
You are answering 10 project-specific questions. The project reference notes are available at: /corpus/notes/

Answer each question directly, using your own judgment.

Answer each question with a short, direct factual answer (a name, a date, a number, or one sentence). If you cannot determine the answer, write "unknown".
---

Manipulation check (identical rule both arms): a subject counts as "retrieved before answering" if and only if the session log shows at least one read of a file under /corpus/notes/ timestamped strictly before the subject's first answer token.

3. TASK / QUESTIONS

- Each subject answers 10 project-specific factual questions (Q1–Q10). Every question's correct answer is a fact recorded in the Smart Notes corpus and NOT reliably answerable from general knowledge (verified by the no-notes pilot, Gate G2).
- Questions are short-answer: the subject produces one name, date, number, or sentence per question, or the abstention token "unknown".
- Traceability: a locked matrix maps each question to the specific corpus file(s) and section containing its key fact (10/10 coverage required, Gate G1).
- Scoring: binary per question (1 = correct, 0 = incorrect/abstain/wrong). Correct = exact match to the answer key OR a pre-listed semantic equivalent from the locked equivalence list. No partial credit. Two independent scorers, blinded to arm (answer sheets carry subject ID only), score all 240 answers; disagreements resolved per Gate G6.
- Subject-level primary score: number correct out of 10. Mastery = >= 8/10.

4. STATISTICS

- Test: Fisher's exact test, two-sided, on the 2x2 table (arm: treated vs control) x (outcome: mastery vs non-mastery).
- Alpha: 0.05.
- Effect size: Cohen's h = 2*arcsin(sqrt(p_treated)) - 2*arcsin(sqrt(p_control)), computed on the observed mastery proportions.
- Tier-S bar (BOTH must hold): Fisher's exact two-sided p < 0.05 AND Cohen's h >= 1.4 on the primary outcome proportions.
- Planned sample size: n = 12 subjects per arm (24 total), fixed before launch. Rationale: anticipated mastery rates of 0.85 (treated) vs 0.20 (control) yield h = 2*arcsin(sqrt(0.85)) - 2*arcsin(sqrt(0.20)) = 2(1.1731) - 2(0.4636) = 1.42, clearing the Tier-S bar with margin if the effect is real.
- Analysis population: intention-to-treat — all randomized subjects completing all 10 questions. Subjects completing fewer than 10 questions are excluded from the primary analysis per Gate G7 (exclusions reported; sensitivity analysis counts them as non-mastery).
- Exactly one primary outcome. Secondary outcomes (mean per-question accuracy, perfect-10/10 rate, retrieval counts/latency) are descriptive only and cannot support a Tier-S claim. No interim analyses, no optional stopping, no peeking; the analysis code is written and tested on synthetic data before launch.

5. VALIDITY GATES (numeric threshold + action on fire)

- G1 Corpus coverage (pre-launch): all 10 key facts locatable in /corpus/notes/ by an independent reader using the traceability matrix. Fires if < 10/10. Action: HALT — do not launch; fix corpus or questions.
- G2 No-notes pilot (pre-launch): 5 pilot subjects with no corpus access and no notes knowledge answer the 10 questions; mean accuracy must be <= 30%. Fires if > 30%. Action: HALT — questions leak general knowledge; redesign questions, do not launch.
- G3 Oracle run (pre-launch): a reference run with full corpus access and the treated brief must score >= 9/10. Fires if < 9/10. Action: HALT — questions are unanswerable even with notes; redesign, do not launch.
- G4 Treatment compliance (post-run): >= 80% of treated subjects must meet the "retrieved before answering" manipulation check. Fires if < 80%. Action: COMPLIANCE FAILURE — primary numbers are still reported, but a Tier-S claim is FORBIDDEN; result is exploratory only.
- G5 Control contamination (post-run): < 25% of control subjects may meet the "retrieved before answering" check. Fires if >= 25%. Action: trial INVALID — no efficacy claim of any kind; redesign for stronger arm separation.
- G6 Scorer reliability (post-run): Cohen's kappa between the two blinded scorers must be >= 0.80 across all 240 answers. Fires if < 0.80. Action: full third-scorer adjudication of disagreements; if kappa remains < 0.80, HALT analysis — scoring invalid.
- G7 Completion (post-run): subjects answering < 10/10 questions are excluded; if > 15% of randomized subjects are excluded, the trial is NON-INTERPRETABLE. Action: no claim; report exclusions and stop.
- G8 Answer-key integrity: SHA-256 of the locked answer key + equivalence list is recorded before randomization. Fires on any post-launch mismatch. Action: trial INVALID.

If any gate fires INVALID / HALT / NON-INTERPRETABLE, no Tier-S claim may be made regardless of the p-value and h observed.

6. PRE-LAUNCH AUDIT CHECKLIST

All items must be checked and signed off with timestamps before the first subject is randomized:

1. Corpus reachable: /corpus/notes/ is mounted and readable from the subject runtime; file count matches the manifest; manifest hash recorded. (The draft brief's path is verified, not assumed.)
2. Traceability matrix locked: Q1–Q10 each mapped to corpus file(s) + section containing the key fact; 10/10 coverage confirmed by a second reader (Gate G1 evidence).
3. No-notes pilot completed (n=5): mean accuracy <= 30%, raw scores logged (Gate G2 evidence).
4. Oracle run completed: score >= 9/10 with treated brief + full corpus, transcript logged (Gate G3 evidence).
5. Brief text audit: automated string check plus human read confirms NEITHER brief contains any of the banned phrases: "consult", "as needed", "all available resources", "thoroughly", "look up". The treated brief contains the mandated sequence ("FIRST ... retrieve ... THEN answer"); the control brief contains no retrieval instruction. Both briefs disclose the identical corpus path string.
6. Brief parity confirmed: question list, answer-format instruction, abstention token ("unknown"), corpus path disclosure, model version, temperature, and max tokens are byte-identical across arms except the retrieval instruction.
7. Answer key + equivalence list written, SHA-256 recorded, stored outside subject reach (Gate G8 baseline).
8. Randomization ready: seeded PRNG (seed recorded), 1:1 allocation, block size 4; full allocation list generated before first subject; allocation concealed from scorers.
9. Retrieval logging verified: a dry-run subject's corpus read produces a timestamped log entry before any answer token (manipulation-check instrumentation proven).
10. Scorers briefed and blinded: answer sheets labeled by subject ID only, no arm labels; scoring rubric and equivalence list distributed; dual-scoring workflow tested.
11. Sample size fixed: 12 per arm; no interim look scheduled; analysis code (Fisher's exact two-sided, Cohen's h) written and passing on synthetic data.
12. Fresh-subject rule: 24 unique subject IDs issued, none reused across arms or pilots; model version pinned and identical for all subjects.
13. Decision log: each checklist item signed off with name/handle and timestamp; any deviation from this preregistration is logged before launch or the launch is void.
