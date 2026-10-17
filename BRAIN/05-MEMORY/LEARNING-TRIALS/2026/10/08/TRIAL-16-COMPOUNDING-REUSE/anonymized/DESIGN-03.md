PREREGISTRATION-DESIGN

1. Hypothesis
Subjects instructed to retrieve relevant Smart Notes from /corpus/notes/ at decision time BEFORE answering project-specific questions will achieve a higher subject-level success rate than subjects given the same corpus availability without a before-answering retrieval directive. Subject-level success is defined as scoring >=8 out of 10 on retrieval-first correct answers (Section 3). The isolated behavioral effect is mandatory retrieval-before-answering, holding corpus availability constant across arms.

2. Arm definitions
Each subject receives exactly one of the following briefs, verbatim, with no additional instructions.

CONTROL brief (rewritten; original draft audited and rejected):
"You are answering project-specific questions. Project reference notes are available at: /corpus/notes/. Answer each question directly and completely."

Audit note on the draft: the draft said "consult them as needed before answering" and "using all available resources." "As needed" makes retrieval optional and unsequenced, and "all available resources" is vague; both would confound the lesson. The rewrite keeps corpus availability identical to treatment while removing optional/vague retrieval language.

TREATMENT brief:
"You are answering project-specific questions. Project reference notes are available at: /corpus/notes/. At decision time, BEFORE answering each question, retrieve the relevant Smart Notes from /corpus/notes/ for that question. First write the note IDs you retrieved, then answer using those notes. Do not answer from memory before retrieving."

3. Task/questions
Subjects: 40 fresh subjects, 20 per arm, randomly assigned, no prior exposure to the corpus or questions.
Task: each subject answers the same 10 project-specific questions in fixed order. Every question is answerable only from one or more specific Smart Notes in /corpus/notes/. Subjects may access /corpus/notes/ and no other external resources. Each response must show work order: retrieval entries (note IDs, timestamped) appear before the final answer.
Scoring (per question, 0 or 1): 1 point only if (a) the final answer matches the locked rubric/answer key AND (b) the response lists relevant note IDs BEFORE the final answer and those notes support the answer. Otherwise 0.
Subject success: total score >= 8/10.
Primary outcome: proportion of successful subjects per arm (treatment vs control).
Secondary outcomes (descriptive only): mean per-question score per arm; retrieval-first response rate per arm.

4. Statistics
Primary test: Fisher's exact test, two-sided, on the 2x2 table (arm: treatment/control x subject success: yes/no). Alpha = 0.05.
Effect size: Cohen's h on the two success proportions, h = |2*arcsin(sqrt(p_treatment)) - 2*arcsin(sqrt(p_control))|.
Tier-S bar: the lesson is supported ONLY if Fisher's exact two-sided p < 0.05 AND Cohen's h >= 1.4 on the primary outcome proportions. Both must hold.
Sample size: n = 20 per arm (40 total), fixed before launch. One pre-specified primary test; no interim analyses; no optional stopping.

5. Validity gates
G1 Corpus coverage: two independent auditors verify all 10 questions each have >=1 supporting note in /corpus/notes/ and a unique rubric answer. Threshold: 10/10. If <10/10, fix corpus/questions and re-audit; no subject is spawned until 10/10.
G2 Brief fidelity: the exact brief text delivered to each subject must match Section 2 character-for-character (verified by hash). Threshold: 100% match. If any deviation, halt, fix delivery, and discard any data collected under the wrong brief.
G3 Treatment manipulation check: treatment retrieval-first compliance = share of treatment question-responses listing note IDs before the final answer. Threshold: >=80%. If below, the manipulation failed: stop, report a null/failed-manipulation result, do not claim lesson support.
G4 Control separation check: control retrieval-first rate = share of control question-responses showing retrieval before answering. Threshold: <=35%. If above, isolation failed (controls spontaneously perform the lesson): abort the primary claim, report data as exploratory only, redesign the task/corpus.
G5 Data integrity: share of responses with complete ordered logs (retrieval entries timestamped before final answer, or explicit no-retrieval record). Threshold: >=95% of responses usable. Responses failing this are invalid and excluded; if >20% of all responses are invalid, the trial is invalid and must be rerun.
G6 No peeking: zero interim computations of the primary test before all 40 subjects complete. If any interim primary analysis occurs, the trial is invalid and must be rerun.

6. Pre-launch audit checklist
All checks must pass before any subject is spawned:
- /corpus/notes/ exists, is readable, and contains the finalized note files; record file count and hashes.
- Question-to-note mapping sheet is locked: each of the 10 questions lists its supporting note IDs; auditor sign-off recorded.
- Answer key and scoring rubric are locked and hashed; the hash is recorded in the preregistration record.
- Both arm briefs verified character-for-character against Section 2 (hash match); delivery mechanism tested with a dry run.
- Subject freshness confirmed: each subject completes a no-prior-exposure declaration for the corpus and questions; anyone exposed is excluded and replaced.
- Logging verified: retrieval actions record note IDs with timestamps preceding final answers in a dry run; ordering is machine-checkable.
- Random assignment procedure (20/20) is fixed and recorded; assignment list is generated before launch.
- Analysis script is pre-written and dry-run on synthetic data: computes Fisher's exact two-sided p and Cohen's h exactly as in Section 4.
- Blinding/roles recorded: scorers score against the locked rubric without seeing arm labels where feasible; any unblinded role is documented.
- Data store and backup location confirmed writable; raw response logs will be preserved unaltered.
