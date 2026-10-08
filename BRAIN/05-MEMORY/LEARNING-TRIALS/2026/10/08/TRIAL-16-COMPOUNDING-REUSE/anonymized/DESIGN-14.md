PREREGISTRATION-DESIGN

1. Hypothesis
Among naive agents with no prior project knowledge, being instructed to retrieve relevant Smart Notes from the learning corpus at decision time BEFORE answering project-specific questions increases the per-subject pass rate on five corpus-dependent questions. Formal hypothesis: the treatment-arm pass proportion exceeds the control-arm pass proportion, where “pass” means at least 4 of 5 answers match the preregistered answer keys. The behavioral effect isolated is the marginal effect of retrieval-before-answering instruction, not general reasoning ability.

2. Arm definitions
CONTROL BRIEF (verbatim):
"You are answering project-specific questions. Answer each question thoroughly using your own reasoning. Provide concise, accurate answers."

TREATMENT BRIEF (verbatim):
"You are answering project-specific questions. Before answering, retrieve relevant Smart Notes from the learning corpus at: /corpus/notes/. First retrieve and read the notes relevant to the questions; then answer using what you retrieved. Provide concise, accurate answers."

The draft control brief’s sentence mentioning “Project reference notes are available at: /corpus/notes/” is REJECTED because it leaks corpus availability to the control arm. The control arm must not see the corpus path.

3. Task/questions
Each subject answers the same five questions about the fictional “Aurora Relay” project. Correct answers are arbitrary project facts present only in the corpus notes; they are not inferable from general reasoning.

Q1: What is the maximum production-queue batch size for Aurora Relay?
Key: 4,096 messages.

Q2: What is the exact Aurora Relay rollback command, and from which directory must it be run?
Key: `relay rollback --target stable`, from `ops/`.

Q3: How long are Aurora Relay hot logs retained?
Key: 72 hours.

Q4: Who is second in the Aurora Relay on-call escalation order?
Key: Okafor.

Q5: When does each Aurora Relay deploy freeze begin?
Key: Thursday at 17:00 UTC.

Scoring: each question is scored 1 if the answer matches the key materially, else 0. Maximum 5. Primary subject-level outcome: PASS if total ≥ 4; otherwise FAIL. Scoring is done blind to arm using the locked rubric and keys. Two independent scorers adjudicate disagreements; the adjudicated score is final.

4. Statistics
Primary analysis: Fisher’s exact test, two-sided, on the 2×2 table of arm (treatment vs control) by outcome (pass vs fail). Alpha = 0.05. Effect size: Cohen’s h = |2·arcsin(√p_treatment) − 2·arcsin(√p_control)|. Planned sample size: 12 subjects per arm, 24 total, randomly assigned, with no interim analysis and no replacement after assignment. Tier-S bar: Fisher’s exact two-sided p < 0.05 AND Cohen’s h ≥ 1.4.

5. Validity gates
Gate 1 — Derivability ceiling. Pilot 10 naive lesson-free agents with the control brief before launch. If pilot pass rate > 10% (>1/10), the task is INVALID: lesson’s marginal effect is unmeasurable; halt launch and redesign questions with less-derivable arbitrary facts.
Gate 2 — Leaky control briefing. Case-insensitive grep of the final control brief for: corpus, retriev, smart note, /corpus, notes/, available at. If any hit ≥ 1, the control brief is contaminated: rewrite it, re-grep, and do not launch until hits = 0.
Gate 3 — Availability contamination. Assertion over all control-arm materials: occurrences of “/corpus/notes” must = 0. If ≥ 1 occurrence is found, quarantine the affected control materials, rebuild them, and re-audit before launch.
Gate 4 — Doctrine redundancy. If pilot pass rate ≥ 90% (≥9/10), the questions measure already-known/derivable facts: trial INVALID; do not launch.
Gate 5 — Control-arm contamination during the trial. If any control subject reports seeing the corpus path or notes, that subject’s response is excluded and reported. If ≥ 2 control subjects are contaminated, the trial is INVALID and results are not used for Tier-S claims.
Gate 6 — Corpus/key integrity. At launch, every answer key must match its corpus note byte-for-byte. If any key/corpus mismatch exists, freeze launch until repaired and re-audited.

6. Pre-launch audit checklist
- [ ] Pilot completed with n=10 naive agents using the final control brief; pilot pass rate ≤ 1/10 recorded.
- [ ] Control brief grepped with the Gate 2 term list; hits = 0; grep output saved.
- [ ] All control-arm materials asserted to contain 0 occurrences of “/corpus/notes”; assertion output saved.
- [ ] Treatment brief contains the retrieval-before-answering instruction and the corpus path; brief text frozen and hash-recorded.
- [ ] Five corpus notes verified present at /corpus/notes/ and each answer key verified byte-identical to its note.
- [ ] Questions, keys, scoring rubric, n=12 per arm, alpha=0.05, and Tier-S bar locked; any later change requires a new preregistration version.
- [ ] Random assignment procedure, subject isolation (no cross-arm communication), and blind scoring procedure documented.
- [ ] No subject spawned until all boxes above are checked and evidence files are saved.
