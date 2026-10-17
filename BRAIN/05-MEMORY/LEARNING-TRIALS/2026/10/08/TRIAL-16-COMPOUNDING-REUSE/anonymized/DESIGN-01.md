PREREGISTRATION-DESIGN

1. Hypothesis
Instructing an agent to retrieve relevant Smart Notes from the corpus at decision time BEFORE answering project-specific questions increases the proportion of subjects who achieve a passing score on corpus-keyed project questions, relative to an otherwise identical control brief that never mentions notes, a corpus, a path, retrieval, or consulting resources. The isolated behavioral effect is the marginal gain in correct project answers attributable to the retrieval instruction, not to general reasoning or standing task knowledge.

2. Arm definitions
The starter draft control brief was rejected: it names the corpus path, instructs consultation "before answering," and invokes "all available resources," which leaks the lesson and creates availability contamination. Final exact briefs:

ARM C — CONTROL (exact brief text):
You are answering project-specific questions. Answer each question directly and completely.

ARM T — TREATMENT (exact brief text):
You are answering project-specific questions. Relevant project Smart Notes are available at: /corpus/notes/. Before answering each project-specific question, retrieve the relevant Smart Notes from /corpus/notes/ and use them in your answer. Answer each question directly and completely.

Corpus access is asymmetric by design: ARM T receives read access to /corpus/notes/; ARM C is never shown the path, the word "corpus," or any file manifest containing it.

3. Task/questions
Each subject receives the same 8 project-specific questions in fixed order Q1-Q8. The corpus at /corpus/notes/ contains 8 Smart Notes; each note states exactly one arbitrary project fact. The facts are chosen to be non-derivable from general reasoning.

Q1: What is the Harborline release codename? Key: Bluefin Meridian
Q2: What is the Harborline freeze date? Key: 2026-11-04
Q3: Who is the Harborline rollback owner? Key: Priya Natarajan
Q4: What is the Harborline feature flag? Key: harborline.deep_draft_v2
Q5: What is the Harborline error budget? Key: 0.35%
Q6: What is the Harborline support window? Key: 02:00-04:00 UTC
Q7: What is the Harborline data retention period? Key: 45 days
Q8: What is the Harborline escalation channel? Key: #harborline-ops

Scoring: normalize each response by lowercasing, trimming, collapsing whitespace, converting en/em dashes to hyphens, and stripping surrounding quotes. Each question scores 1 if the normalized response equals the normalized key, else 0. Subject score = sum/8. Primary outcome: PASS if subject score >= 6/8, else FAIL. A secondary process check records whether ARM T subjects perform at least one /corpus/notes/ file read before submitting their first answer.

4. Statistics
Primary comparison: PASS proportion in ARM T versus PASS proportion in ARM C. Fixed sample: n = 12 subjects per arm for the main launch; pilot runs are excluded from the primary analysis. Test: Fisher's exact test, two-sided, alpha = 0.05. Effect size: Cohen's h = |2*arcsin(sqrt(p_T)) - 2*arcsin(sqrt(p_C))|, computed on the primary outcome proportions. Tier-S bar: Fisher's exact two-sided p < 0.05 AND Cohen's h >= 1.4. No interim peeking and no optional stopping; the analysis is run once on the locked n = 12/arm dataset.

5. Validity gates
G1 — Derivability ceiling (pilot): run 4 ARM C pilot subjects before full launch. If ARM C pilot PASS rate >= 0.25 or mean per-question accuracy >= 0.25, the trial is INVALID: stop, do not launch the main n; replace corpus facts/questions with less derivable keys and re-pilot.
G2 — Leaky control briefing: grep the finalized ARM C brief for {"Smart Note", "Smart Notes", "corpus", "/corpus/notes", "retrieve", "consult", "before answering", "available resources"}. Required: 0 matches. If >= 1 match: INVALID briefing; rewrite ARM C, re-run the full audit; no subjects until 0 matches.
G3 — Availability contamination: scan the complete ARM C prompt, context, instructions, and file-access manifest for "/corpus/notes", "corpus", "Smart Note", "reference notes", and "path". Required: 0 occurrences and no /corpus/notes read access for ARM C. If any occurrence or access is found: remediate, re-audit from scratch; no launch until clean.
G4 — Doctrine redundancy / unanimous ceiling (pilot): run 4 ARM T pilot subjects alongside the ARM C pilot. If ARM C pilot PASS rate >= 0.75 AND ARM T pilot PASS rate >= 0.75, the trial is INVALID: the lesson is already encoded or the task is trivially derivable; do not measure; redesign the corpus facts and re-pilot.

6. Pre-launch audit checklist
All checks are completed and pass before any subject is spawned:
1. Confirm exactly 8 Smart Note files exist under /corpus/notes/ and each file contains its corresponding Q-key fact; record byte counts.
2. Confirm the locked answer-key file matches the 8 keys above exactly; record its checksum.
3. Confirm the ARM C brief text is character-identical to the approved control brief and G2 grep returns 0 matches.
4. Confirm the ARM T brief text is character-identical to the approved treatment brief and contains both the /corpus/notes/ path and the before-answering retrieval prescription.
5. Confirm the ARM C prompt/context/file manifest contains 0 occurrences of forbidden availability terms and grants no /corpus/notes/ access.
6. Confirm no answer key or distinctive key substring appears anywhere outside /corpus/notes/ and the locked key file, including briefs, questions, harness code, and logs directories.
7. Test the scoring script on fixtures: an 8/8 response set must score PASS and a 0/8 set must score FAIL.
8. Lock the assignment list at n = 12 ARM C and n = 12 ARM T, with pilot runs excluded from the primary dataset.
9. Sign the checklist; if any check fails, fix, re-run all checks, and do not spawn subjects.
