PREREGISTRATION-DESIGN

Trial ID: L-RETRIEVE-01. Lesson under test: "Retrieve relevant Smart Notes from the corpus at decision time BEFORE answering project-specific questions." This preregistration is locked before any subject is spawned; any deviation is a protocol violation and must be reported as such.

1. HYPOTHESIS

The behavioral effect being isolated is the act of retrieving relevant Smart Notes from the corpus BEFORE answering — not mere availability of the corpus, not consulting notes after answering, and not general thoroughness.

H-behavioral: Subjects who receive an explicit instruction to retrieve relevant Smart Notes from the corpus before answering will perform a corpus retrieval prior to answering at a higher rate than subjects who receive a neutral brief with no retrieval instruction.

H-primary (outcome): Subjects receiving the retrieval-before-answering directive achieve a higher subject-level success rate on project-specific questions (defined in Section 3) than subjects receiving the neutral brief.

The causal contrast is the brief's retrieval directive alone. Both arms work in identical environments with identical read access to the same corpus; the ONLY difference between arms is the brief text. If the treatment arm succeeds more often, the cause is the retrieve-before-answering instruction changing behavior, not differential access to information.

2. ARM DEFINITIONS

Both briefs are delivered verbatim as the subject's full instruction text. The two briefs differ by exactly one inserted directive (the retrieval instruction plus a citation requirement that doubles as the manipulation check).

CONTROL BRIEF (verbatim):
"You are answering project-specific questions. Read each question and answer it to the best of your ability. Answer every question, even if you are unsure. When you are finished, stop."

TREATMENT BRIEF (verbatim):
"You are answering project-specific questions. BEFORE you answer any question, first retrieve relevant Smart Notes from the corpus at /corpus/notes/. Read the notes that are relevant to the question. Then answer each question, and for each answer state which Smart Note(s) you used. Answer every question, even if you are unsure. When you are finished, stop."

Randomization: 20 subjects, 1:1 to arms (10 treatment, 10 control), via seeded RNG; the seed is recorded in the pre-launch audit log. Subjects are fresh instances with no prior exposure to the corpus content. Corpus access (read-only mount of /corpus/notes/) is identical in both arms.

AUDIT FINDINGS ON THE DRAFT CONTROL BRIEF (why it was rewritten):
(a) The draft told control subjects the notes exist and to "consult them as needed" — it instructed the very retrieval behavior under test in the control arm, collapsing the treatment contrast.
(b) "Answer thoroughly using all available resources" is unmeasurable and invites non-corpus strategies (guessing, general knowledge), muddying attribution.
(c) "as needed" permits consultation AFTER answering, which tests nothing about retrieval BEFORE answering — the timing is the lesson's core.
(d) The path /corpus/notes/ was asserted, never verified; path existence and corpus contents are verified in the pre-launch audit (Section 6), not assumed.

3. TASK / QUESTIONS

Subject procedure: Each subject receives its arm's brief, then answers the same 10 project-specific questions in a fixed order, one response per question, no time limit.

Question-bank specification (locked before launch in a gold-answer ledger): exactly 10 questions. Each question's gold answer is a specific fact documented in the Smart Notes corpus (e.g., an identifier, date, decision, or owner recorded in a project note) and is NOT reliably answerable from general knowledge alone. Each ledger row contains: question text, gold answer, the key facts an acceptable answer must contain, and the source note file plus line range where the answer appears.

Scoring rubric: each question is scored binary — 1 if the response contains all key facts from the ledger row (paraphrase accepted; verbatim match not required), 0 otherwise; blank or "I don't know" = 0. Primary outcome (per subject): SUCCESS if the subject scores ≥7 of 10; otherwise FAILURE. Scoring is performed by two independent scorers blind to arm assignment, using only the ledger. Inter-rater agreement is gated (Section 5); disagreements are adjudicated by a third blind scorer, majority rules.

4. STATISTICS

Primary analysis: Fisher's exact test, two-sided, on the 2x2 table (arm: treatment/control x outcome: success/failure), with alpha = 0.05. Effect size: Cohen's h on the two subject-level success proportions, h = 2*arcsin(sqrt(p_treatment)) - 2*arcsin(sqrt(p_control)).

TIER-S BAR (both required, on the primary outcome): Fisher's exact two-sided p < 0.05 AND Cohen's h >= 1.4.

Sample size: N = 20 (10 per arm), fixed before launch. With 10 per arm the bar bites on both sides: e.g., 9/10 treatment success vs 2/10 control success gives h = 1.57 and p < 0.05 (qualifies); 9/10 vs 3/10 gives h = 1.34 (fails the h bar despite p < 0.05). No interim looks, no optional stopping, no arm reassignment. All responses are scored and reported; secondary analyses (mean per-question accuracy per arm with 95% CIs, per-question item analysis) are descriptive only and labeled exploratory.

5. VALIDITY GATES

Gate 1 — Manipulation check (treatment arm): a treatment subject counts as "retrieved" if tool/file-access logs show at least one read of /corpus/notes/ before the subject's first answer, OR the subject cites at least one Smart Note. Threshold: >=8 of 10 treatment subjects must count as retrieved. FIRES if <8/10: classify as MANIPULATION FAILURE. Consequence: the trial cannot test the lesson; a null result is inadmissible as evidence against L-RETRIEVE. Report as inconclusive, strengthen the brief, re-run.

Gate 2 — Control contamination: a control subject counts as "retrieved" by the same evidence rule. Threshold: <=2 of 10 control subjects may count as retrieved. FIRES if >2/10: classify as CONTAMINATED CONTRAST. Consequence: report intention-to-treat and per-protocol results separately; no Tier-S claim permitted on the primary analysis.

Gate 3 — Floor/ceiling: if control-arm success rate >= 0.8, the questions are too easy (ceiling); if treatment-arm success rate <= 0.2, the questions are unanswerable even with retrieval (floor). FIRES on either. Consequence: the trial is an INVALID TEST of the lesson, not a null result. Redesign the question bank, re-run.

Gate 4 — Data integrity: >10% of question responses missing or unscorable (>20 of 200 responses). FIRES if exceeded. Consequence: no Tier-S claim; diagnose the data loss and re-run.

Gate 5 — Scorer agreement: Cohen's kappa between the two blind scorers < 0.8. FIRES if below. Consequence: scoring is invalid; adjudicate all disagreements with the third scorer and recompute kappa on the final scores before any analysis.

Gate 6 — Randomization integrity: final arm sizes must be exactly 10 and 10; the assignment seed must match the audit log. FIRES on any mismatch or post-hoc reassignment. Consequence: primary analysis is void; report the breach and re-run.

Gate precedence: if multiple gates fire, report all of them; Gate 6 voids everything regardless of other results.

6. PRE-LAUNCH AUDIT CHECKLIST

Every item must PASS before the first subject is spawned. Any FAIL blocks launch until resolved; the checklist outcome is logged with timestamps.

1. Corpus existence: /corpus/notes/ exists, is readable from the subject sandbox, and contains the Smart Notes corpus (spot-check >=5 note files open and are project notes, not empty or placeholder).
2. Corpus snapshot: record a content hash (sha256 over all files) of /corpus/notes/ in the audit log; both arms mount this exact snapshot.
3. Question answerability: for all 10 ledger rows, the gold answer is confirmed present in the cited note file and line range by an auditor independent of the question author.
4. Question difficulty screen: all 10 gold answers contain project-specific identifiers (names, dates, version numbers, IDs) not plausibly present in general pretraining knowledge; any question answerable from general knowledge is replaced.
5. Brief diff: the treatment and control brief texts differ by exactly the retrieval directive (word-level diff recorded); no other wording differences; neither brief mentions any other resource, tool, or strategy.
6. Scoring ledger locked: all 10 rows complete (question, gold answer, key facts, source citation); ledger version hash recorded; scorers receive the ledger but not arm labels.
7. Analysis script verified: the Fisher's-exact (two-sided) + Cohen's-h script runs on synthetic data and reproduces hand-checked values, including the Section 4 critical examples (h = 1.57 for 0.9 vs 0.2; h = 1.34 for 0.9 vs 0.3).
8. Environment parity: both arms' sandboxes are byte-identical except the brief file (same tools, same corpus mount, same question file, no network, no brief leakage across arms); verified by a diff of the two sandbox configurations.
9. Manipulation-check instrumentation: file-access logging for /corpus/notes/ is enabled and tested with a dry-run read; log format confirmed parseable by the retrieval-evidence rule in Section 5.
10. Randomization: seed generated and recorded; assignment list (subject ID -> arm) produced and stored sealed from scorers; arm sizes confirmed 10/10.
11. Evidence store: a durable, versioned evidence directory is designated; raw responses, retrieval logs, ledger, briefs, seed, and audit log will be committed there — no ephemeral-only storage (raw data loss voids the trial per the standing evidence rule).
12. Sign-off: the auditor (a party independent of the trial designer) confirms items 1-11 PASS in writing; the sign-off, with timestamp, is the launch authorization.
