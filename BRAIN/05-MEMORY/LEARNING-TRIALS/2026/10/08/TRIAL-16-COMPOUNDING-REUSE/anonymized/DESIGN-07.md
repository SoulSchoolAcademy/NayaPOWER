PREREGISTRATION-DESIGN
Trial ID: L-RETRIEVE-1
Lesson under test: L-RETRIEVE — "Retrieve relevant Smart Notes from the corpus at decision time BEFORE answering project-specific questions."

1. Hypothesis
The isolated behavioral effect is the pre-answer retrieval mandate: instructing a subject to retrieve relevant Smart Notes from /corpus/notes/ at decision time BEFORE writing any part of an answer causes a higher proportion of subjects to reach high accuracy (≥4 of 5 correct) on corpus-dependent project-specific questions than instructing subjects to answer from internal knowledge with retrieval prohibited. Corpus availability (same path, same notes, same questions, same scoring, same time limits) is held constant across arms; only the retrieval directive varies. Predicted direction: treatment high-accuracy proportion ≥ 0.65; control high-accuracy proportion ≤ 0.05.

2. Arm definitions
DRAFT CONTROL BRIEF AUDIT (traps found, all removed in the rewrite): (a) "consult them as needed" makes retrieval optional rather than controlled, so control subjects may retrieve and collapse the treatment contrast; (b) "before answering" modifies an optional consultation instead of enforcing a retrieval-then-answer sequence; (c) "using all available resources" authorizes non-corpus resources, contaminating the corpus-only manipulation; (d) "Project reference notes" does not name the Smart Notes corpus, diverging from L-RETRIEVE.

T-RETRIEVE brief (treatment) — exact text delivered:
"You are answering project-specific questions. For EACH question, BEFORE you write, draft, outline, or begin any part of your answer: retrieve relevant Smart Notes from the corpus at /corpus/notes/ that bear on the question. Do not produce any answer content until retrieval is complete. After retrieving, answer the question using the retrieved Smart Notes. If no relevant Smart Note exists for a question, write 'No relevant note found' and then answer from your own knowledge."

C-NORETRIEVE brief (control) — exact text delivered (rewritten):
"You are answering project-specific questions. Answer each question directly from your own internal knowledge, beginning your answer immediately. Do NOT retrieve, open, consult, quote, or reference any notes, corpus, files, documents, or external resources at any point — before, during, or after answering."

3. Task/questions
Each subject receives 5 project-specific questions drawn randomly without replacement from a locked pool of 20. Every question is factual (a name, date, decision, or quantity) whose single correct answer is derivable ONLY from 1–2 designated gold Smart Notes in /corpus/notes/; the gold note IDs per question are recorded in a locked answer key before launch. Subjects answer in a fixed response box, one attempt per question, no revision after submission, 10 minutes total. Scoring: each answer is binary — 1 if the response contains the gold answer exactly or as an unambiguous paraphrase per the locked rubric, 0 otherwise. Scoring is performed by a rater blinded to arm assignment. Subject-level primary outcome: HIGH-ACCURACY = 1 if ≥4 of 5 answers score 1, else 0. Retrieval behavior is logged independently (subject_id, note_id, timestamp) as a manipulation check, not as the primary outcome.

4. Statistics
Primary test: Fisher's exact test, two-sided, on the 2×2 contingency table (arm: T-RETRIEVE vs C-NORETRIEVE) × (outcome: high-accuracy vs not). Alpha = 0.05, single pre-specified analysis, no interim looks, computed once after data lock. Effect size: Cohen's h on the two high-accuracy proportions (h = 2·arcsin(√p_treatment) − 2·arcsin(√p_control)). Tier-S bar (PASS requires BOTH): Fisher's exact two-sided p < 0.05 AND Cohen's h ≥ 1.4. Sample size: n = 30 subjects per arm (60 total), chosen so the predicted rates (0.65 vs 0.05, h ≈ 1.53) clear the Tier-S bar with margin. Report both statistics with 95% confidence intervals regardless of outcome.

5. Validity gates (numeric thresholds; each is checked before the primary test is run)
V1 — Treatment compliance: ≥80% of treatment subjects must log retrieval of ≥1 gold note timestamped before their first answer submission. If <80%: manipulation failed — DO NOT run the primary test; report INCONCLUSIVE (manipulation failure) and re-run.
V2 — Control contamination: ≤10% of control subjects may log any retrieval/consultation event. If >10%: contrast compromised — invalidate the run; report and re-run with tighter enforcement.
V3 — Question calibration: control-arm high-accuracy rate must be ≤15%. If >15%: questions are guessable without notes — drop the offending questions, rebuild the pool, re-run; do not analyze.
V4 — Scoring reliability: on a random 20% of answers double-scored, Cohen's κ ≥ 0.80. If <0.80: adjudicate disagreements and re-score all answers before any analysis.
V5 — Attrition: ≤10% blank or non-submitted answers per arm. If exceeded: report, replace subjects, re-run; do not impute.
V6 — Data lock: primary statistics are computed exactly once after all 60 subjects complete and all gates pass. Any re-computation after seeing results is a protocol violation and must be disclosed.

6. Pre-launch audit checklist (all must be checked before any subject is spawned)
[ ] Control brief text verified to contain no corpus path, no "as needed", no "all available resources", and an explicit no-retrieval prohibition; diffed against the draft to confirm all four traps removed.
[ ] Treatment brief verified to mandate retrieval BEFORE any answer content and to name "Smart Notes" and /corpus/notes/.
[ ] Locked answer key and scoring rubric committed (hash recorded), with gold Smart Note IDs for all 20 questions.
[ ] Calibration pilot run (n = 10, control brief only): high-accuracy rate ≤15% and no single question answered correctly by >30% of pilot subjects.
[ ] Corpus reachable from both arms; every access emits (subject_id, note_id, timestamp); control-arm accesses are logged as contamination events.
[ ] Retrieval-before-answer ordering verifiable: log timestamps provably precede answer-submission timestamps.
[ ] Random 1:1 assignment to arms with allocation concealed until brief delivery; scorer blinded to arm.
[ ] Analysis script dry-run on synthetic data reproduces Fisher's exact two-sided p and Cohen's h correctly.
[ ] No shared state, chat history, or prompt leakage between subjects; both brief texts frozen and their hashes recorded.
[ ] Pre-registration document itself frozen and hashed before the first subject is spawned.
