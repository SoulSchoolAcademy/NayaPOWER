PREREGISTRATION-DESIGN

A preregistration for a behavioral trial isolating lesson L-RETRIEVE: "Retrieve relevant Smart Notes from the corpus at decision time BEFORE answering project-specific questions."

1. HYPOTHESIS

H1: Subjects instructed to retrieve relevant Smart Notes from the corpus BEFORE answering project-specific questions will achieve a higher success proportion (success = at least 7 of 10 questions answered correctly) than subjects given the identical task without any retrieval instruction.

H0: There is no difference in success proportions between the two arms.

What is isolated: the behavioral effect of the retrieval procedure itself — mandatory retrieval of relevant notes at decision time, before answering. It is NOT the effect of corpus availability: both arms are told the corpus exists at the same path, and both may in principle open it. The manipulation is the instruction to retrieve first and cite, versus a neutral task brief with no retrieval instruction. The predicted mechanism: subjects who retrieve before answering ground their answers in the notes and therefore answer the corpus-specific facts correctly; subjects without the instruction rely on general knowledge and fail on facts that exist only in the corpus.

2. ARM DEFINITIONS

Both arms receive the same task header: "Answer the 10 project-specific questions about Project Kestrel below. Write one answer per question." Both arms are informed identically that the corpus exists at /corpus/notes/. The ONLY difference is the retrieval procedure.

ARM T (Treatment — L-RETRIEVE). Exact brief text, delivered in full:

"You are answering project-specific questions about Project Kestrel. Project reference notes exist at: /corpus/notes/.

You MUST follow this procedure exactly, in this order:

STEP 1 — RETRIEVE FIRST. Before you read the questions in detail and before you draft any answer, search the corpus at /corpus/notes/ for Smart Notes relevant to Project Kestrel. Open and read each relevant note in full. Do not answer anything until this step is complete.

STEP 2 — RECORD. Write down the IDs or titles of every note you retrieved.

STEP 3 — ANSWER. Only now read the questions and write your answers, grounded in the notes you retrieved. After each answer, cite the note ID that supports it.

Do not skip Step 1. Do not answer from memory or general knowledge when a retrieved note covers the question."

ARM C (Control). Exact brief text, delivered in full:

"You are answering project-specific questions about Project Kestrel. Project reference notes exist at: /corpus/notes/.

Read the questions below and write one answer per question."

Design note (audit of the starter draft): the draft control brief ("consult them as needed before answering… Answer thoroughly using all available resources") was rejected because it contains a retrieval instruction of its own — "consult them as needed" plus "using all available resources" nudges control subjects to retrieve, which would collapse the very contrast the trial isolates. The rewritten control brief above states corpus availability with zero instruction to use it.

3. TASK / QUESTIONS

Subjects answer 10 written questions about the fictional Project Kestrel. All 10 correct answers exist ONLY in planted Smart Notes in the corpus (NOTE-K01 through NOTE-K10) and are not recoverable from general knowledge (verified pre-launch; see Section 6). The 10 questions and the locked answer key:

Q1. What is the internal codename of the harbor sensor grid pilot? → Kestrel
Q2. At which pier is the pilot deployed? → Pier 9, Port Alden
Q3. What is the go-live date? → 2026-11-18
Q4. Which sensor vendor was selected? → Meridian Instruments
Q5. What is the budget cap? → $184,000
Q6. How long is sensor data retained before purge? → 90 days
Q7. Who is the escalation contact? → R. Okafor
Q8. How often are project reviews held, and on which weekday? → every 3 weeks, on Tuesdays
Q9. What is the uptime success threshold? → 94% or higher
Q10. What mitigation was chosen for the gull-interference risk on sensor mounts? → spikes (not nets)

Scoring: each answer is scored 1 (correct) or 0 (incorrect) by a scorer blind to arm assignment, against the locked rubric. The rubric accepts minor spelling/punctuation variants but no semantic substitutes (e.g., "Vantacore" for Q4 = 0; "every two weeks" for Q8 = 0; "nets" for Q10 = 0). Partial credit is not given.

Primary outcome (subject level): SUCCESS = score of 7 or more out of 10; FAIL = 6 or fewer.

Secondary measures (descriptive, non-confirmatory): mean score per arm; proportion of treatment subjects citing at least one valid corpus note ID; proportion of control subjects citing any corpus note ID (contamination check).

4. STATISTICS

Test: Fisher's exact test, two-sided, on the 2×2 table of arm (T vs C) by outcome (SUCCESS vs FAIL).

Alpha: 0.05.

Sample size: fixed at n = 20 subjects, 10 per arm, assigned by a pre-generated balanced randomization list. No interim analyses, no optional stopping, no data-dependent sample-size changes. Analysis is intention-to-treat: every randomized subject is counted in its assigned arm regardless of compliance.

Tier-S bar: the trial counts as support for H1 only if BOTH hold: (a) Fisher's exact two-sided p < 0.05, AND (b) Cohen's h >= 1.4 on the two success proportions, where h = 2·arcsin(√pT) − 2·arcsin(√pC). Meeting only one criterion does not constitute support. If the bar is met, report h and both proportions; if not, H1 is not supported and the result is reported as null.

5. VALIDITY GATES

Each gate has a numeric threshold and a pre-specified consequence. Gates are evaluated before the confirmatory test is interpreted.

Gate 1 — Treatment delivery (manipulation check). Threshold: at least 8 of 10 treatment subjects (≥80%) must cite at least one valid corpus note ID (NOTE-K01…NOTE-K10) in their answers. If it fires (<80%): the retrieval procedure was not delivered; the trial is INVALID for the hypothesis. Do not interpret the Fisher test as evidence about L-RETRIEVE. Redesign the treatment brief for stronger compliance and rerun.

Gate 2 — Control contamination. Threshold: if 3 or more of 10 control subjects (≥30%) cite any corpus note ID in their answers, the gate fires. Consequence: the primary ITT analysis is still computed and reported, but the trial is rated INCONCLUSIVE for the L-RETRIEVE mechanism claim (arms did not stay behaviorally separated). Do not claim the Tier-S bar supports the mechanism; redesign with stronger arm separation and rerun.

Gate 3 — Floor/ceiling (question calibration). Thresholds: control success proportion must be ≤ 0.50; treatment success proportion must be < 1.00 with at least 2 treatment subjects scoring ≤ 8/10. If control success ≥ 0.60: the questions are answerable without retrieval → trial INVALID, rewrite questions to be corpus-dependent and rerun. (Treatment ceiling alone does not invalidate; it is reported.)

Gate 4 — Scoring reliability. Threshold: an independent second scorer, blind to arm, re-scores 100% of answers; Cohen's kappa between scorers must be ≥ 0.80. If it fires (kappa < 0.80): all disagreements are adjudicated against the locked rubric by a third blind rater, and kappa is recomputed; if still < 0.80 the trial is INVALID (unreliable measurement) and must be rescored from scratch after rubric repair.

Gate 5 — Attrition/exclusion. Threshold: if more than 2 of 20 subjects ( >10%) fail to complete all 10 questions or are excluded for protocol violations, the gate fires → trial INVALID (attrition threatens randomization). Report the exclusions and rerun with the same fixed n.

Gate interaction: if any INVALID gate fires, the confirmatory test may be computed for the record but must not be presented as a test of H1.

6. PRE-LAUNCH AUDIT CHECKLIST

Every item below must be checked and signed off BEFORE the first subject is spawned. If any item fails, launch is blocked until it passes.

[ ] 1. Corpus presence: /corpus/notes/ exists and contains exactly the 10 planted notes NOTE-K01 through NOTE-K10, each openable and readable. Record the note count.
[ ] 2. Answer-key coverage: 100% of the 10 rubric answers (all facts in Section 3) are present in the corpus notes, verified by string match against note text.
[ ] 3. Novelty probe: one probe subject with NO corpus access and the control brief answers the 10 questions; probe score must be ≤ 2/10. If > 2/10, the facts leak from general knowledge — rewrite the leaking questions and re-probe.
[ ] 4. Control-brief text audit: the exact control brief text in Section 2 is verified to contain none of the strings "retriev", "consult", "look up", "read the notes", "before answering", "available resources". Record the check.
[ ] 5. Treatment-brief text audit: the exact treatment brief text in Section 2 is verified to contain the three ordered steps, the "Do not skip Step 1" prohibition, and the per-answer citation requirement. Record the check.
[ ] 6. Randomization locked: a balanced assignment list (10 T, 10 C) is generated in advance by an independent random draw; the list is sealed and subjects are assigned in spawn order. Record the seed or draw record.
[ ] 7. Answer key and rubric locked: the Section 3 answer key and the scoring rubric (including accepted variants and the ≥7/10 success threshold) are written to a file and its SHA-256 hash recorded before any subject runs. No edits after launch.
[ ] 8. Scorer blinding: the scoring procedure strips arm labels before answers reach scorers; verify with a dry run on one sample answer packet.
[ ] 9. Subject freshness: every subject is fresh — no prior exposure to this corpus, these questions, or any earlier run of this trial. Record the freshness attestation per subject.
[ ] 10. Fixed-n commitment: n = 20 is fixed; no interim analysis is scheduled and no stopping rule exists. Record the commitment in the run log before spawning subject 1.
