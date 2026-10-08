PREREGISTRATION-DESIGN

1. Hypothesis

Agents instructed to retrieve relevant Smart Notes from the corpus at decision time BEFORE answering project-specific questions will achieve a higher subject-level pass rate than agents given no retrieval instruction and no knowledge of the corpus. The behavioral effect isolated is the marginal gain from retrieval-before-answering, not from task familiarity or general reasoning. Null hypothesis: pass proportions are equal across arms.

2. Arm definitions

The exact brief text each arm receives (no additions, no omissions):

CONTROL BRIEF (final, rewritten from draft):
"You are answering project-specific questions. Answer each question thoroughly and precisely. If you do not know the answer, say so rather than guessing."

(The draft control brief was rejected: it named the corpus path and told subjects to "consult them as needed," which both implies the lesson's prescription and triggers availability contamination. The final control brief contains no mention of any corpus, path, or retrieval.)

TREATMENT BRIEF:
"You are answering project-specific questions. BEFORE answering any question, retrieve relevant Smart Notes from the corpus at /corpus/notes/ and read them. Use the retrieved notes to answer each question thoroughly and precisely. If the notes do not contain an answer, say so rather than guessing."

3. Task/questions

The corpus at /corpus/notes/ contains 12 Smart Notes. Three target facts are each stated verbatim in exactly one note: SN-EXPORT-03, SN-DEPLOY-07, SN-ROLLBACK-02. Facts are project-specific and not derivable from general reasoning.

Each subject answers the same three questions, in fixed order:

Q1. "What is the maximum number of records allowed in a single nightly export batch?" Expected: "500" (source: SN-EXPORT-03).
Q2. "Which team must approve a deployment before it goes live?" Expected: "Release Engineering" (source: SN-DEPLOY-07).
Q3. "Within how many minutes of a failed deployment must a rollback begin?" Expected: "30" or "30 minutes" (source: SN-ROLLBACK-02).

Scoring: each question scored 0/1 by two independent scorers blinded to arm, using the rubric above (case-insensitive; Q3 accepts "30" or "30 minutes"; no partial credit). Disagreements are adjudicated by a third blinded scorer before unblinding. Primary outcome per subject: PASS if score >= 2 of 3, else FAIL.

4. Statistics

Primary analysis: Fisher's exact test, two-sided, on the 2x2 table (arm: treatment/control x outcome: pass/fail). Alpha = 0.05. Sample size: n = 12 subjects per arm (24 total), randomized by a pre-generated list. Tier-S bar: Fisher's exact two-sided p < 0.05 AND Cohen's h >= 1.4 computed on the observed pass proportions (h = 2*arcsin(sqrt(p_treatment)) - 2*arcsin(sqrt(p_control))). Intent-to-treat is the primary population; a per-protocol population (treatment subjects meeting the retrieval-compliance criterion) is reported secondarily.

5. Validity gates

G1. Derivability ceiling (pre-launch pilot). Six lesson-free pilot subjects receive the final control brief with no corpus access. Threshold: pilot pass rate must be 0/6. If >= 1 pilot subject passes, the trial is INVALID: questions are answerable without retrieval; redesign the questions and re-pilot.

G2. Leaky control briefing. Automated grep of the final control brief for {"retriev", "corpus", "smart note", "smartnote", "/corpus", "notes/"}. Threshold: 0 hits. Any hit: INVALID briefing; rewrite and re-audit before launch.

G3. Availability contamination. The control brief must not contain the corpus path or any path-like token pointing to the notes. Threshold: 0 occurrences. Any occurrence: INVALID; remove and re-audit.

G4. Doctrine redundancy. Search standing doctrine for the lesson's prescription (a "retrieve"-family term in the same sentence as "before answering"). Threshold: 0 matches. Any match: INVALID; the lesson is already learned and the trial must not run.

G5. Treatment compliance. A treatment subject is compliant if the log shows at least one corpus read before the timestamp of their first answer. Threshold: >= 10 of 12 (80%) compliant. If compliance is 50-79%, the Tier-S claim is withheld and only per-protocol results are reported. If compliance < 50%, the trial is INVALID as a test of the lesson.

G6. Scorer reliability. Cohen's kappa between the two blinded scorers on question-level scores must be >= 0.80. If below, the third scorer adjudicates all disagreements before unblinding; if kappa remains < 0.80 after adjudication, the scoring is INVALID and results are not reported.

G7. No ceiling in the main run. If the control pass proportion is >= the treatment pass proportion, the trial is INVALID (the effect was not isolated); report as failed isolation, not as a null result.

6. Pre-launch audit checklist

All checks are completed and recorded before any subject is spawned:

1. Corpus check: confirm SN-EXPORT-03, SN-DEPLOY-07, and SN-ROLLBACK-02 exist at /corpus/notes/, each contains its target fact verbatim, and no other note contains a conflicting value. Record file hashes.
2. Control brief audit: run the G2/G3 greps on the exact final control brief text; record 0 hits and confirm no path string is present.
3. Treatment brief audit: confirm it contains an explicit before-answering retrieval instruction and the exact path "/corpus/notes/".
4. Pilot: run 6 lesson-free pilot subjects under the control brief with no corpus access; record 0/6 passes (G1).
5. Doctrine search: run the G4 search over standing doctrine; record 0 matches.
6. Rubric verification: a second checker independently confirms each expected answer matches the cited note verbatim.
7. Randomization and blinding: pre-generate the 12/12 assignment list; document that scorers receive only anonymized subject IDs with no arm labels.
8. Logging check: confirm retrieval tool calls and answer timestamps are captured per subject so the G5 compliance metric is computable.
