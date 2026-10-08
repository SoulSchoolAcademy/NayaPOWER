PREREGISTRATION-DESIGN

TRIAL: L-RETRIEVE-1 — Mandatory Smart Note retrieval at decision time vs. unprompted baseline

1. HYPOTHESIS

Behavioral effect isolated: mandating that a subject retrieve relevant Smart Notes from a corpus BEFORE answering project-specific questions raises the subject-level success rate on those questions, relative to a baseline subject who receives no retrieval instruction and no corpus access.

Precise statement: Let p_t = proportion of treatment-arm subjects who answer at least 8 of 10 project-specific questions correctly, and p_c = the same proportion in the control arm. H1: p_t > p_c. H0 (null): p_t = p_c. The mechanism under test is corpus retrieval at decision time — not general knowledge, reasoning ability, or motivation — because all answers are invented project facts present only in the corpus (see Section 3). The lesson is supported only if the Tier-S bar in Section 4 is met AND all validity gates in Section 5 pass.

2. ARM DEFINITIONS

Trap audit of the draft control brief: the draft ("Project reference notes are available at: /corpus/notes/ — consult them as needed before answering. Answer thoroughly using all available resources.") mentions the corpus in the CONTROL arm, invites consultation, and pushes "all available resources." This contaminates the control — both arms would be nudged toward retrieval, collapsing the contrast. The draft is REJECTED and rewritten. Final briefs below contain no corpus mention in the control.

Control arm brief (exact text):
"You are answering project-specific questions about Project Meridian. Answer each of the 10 questions below directly, as completely as you can, using your own best judgment. Provide one answer per question, numbered 1 to 10."

Treatment arm brief (exact text):
"You are answering project-specific questions about Project Meridian. Smart Notes relevant to these questions are stored in the corpus at /corpus/notes/. BEFORE answering any question, you MUST first search the corpus, read the relevant Smart Notes, and identify the facts needed to answer. Only after completing this retrieval step, answer each of the 10 questions using the facts you retrieved. Provide one answer per question, numbered 1 to 10."

The ONLY differences between arms are: (a) the treatment mandates retrieval from the corpus before answering; (b) the treatment environment grants read access to /corpus/notes/ while the control environment has no such path. Subjects are fresh, independent, and have no prior exposure to the corpus, questions, or answer key.

Corpus (10 notes, one key fact each, exactly as stored):
- note-A.txt: "Project Meridian launch budget approved at $412,000 on 2026-03-14."
- note-B.txt: "Authentication protocol chosen after the 2026-05-02 review: Falcon-7, over Kestrel-2."
- note-C.txt: "Retry policy: cap of 11 attempts; backoff base 340 ms."
- note-D.txt: "Vendor contract renewed: Bluepine Logistics at $88,500 per year."
- note-E.txt: "Incident on 2026-06-19 was caused by the relay cache purge, not the database failover."
- note-F.txt: "Staging environment is named zephyr-staging, in region eu-west-2."
- note-G.txt: "Weekly sync moved from Tuesday to Thursday at 14:00 UTC."
- note-H.txt: "Escalation owner is Dana Whitfield (not the on-call lead)."
- note-I.txt: "Data retention policy: 400 days for telemetry, 90 days for session logs."
- note-J.txt: "API v2 deprecation date: 2026-11-30."

3. TASK/QUESTIONS

Each subject answers the same 10 questions, numbered 1-10, in one session. Answer key and note mapping:

1. What was the approved launch budget for Project Meridian? -> $412,000 (note-A)
2. Which authentication protocol was chosen after the May 2026 review? -> Falcon-7 (note-B)
3. What is the configured retry cap, in number of attempts? -> 11 (note-C)
4. What is the backoff base, in milliseconds? -> 340 (note-C)
5. With which vendor was the logistics contract renewed? -> Bluepine Logistics (note-D)
6. What caused the incident on 2026-06-19? -> relay cache purge (note-E)
7. What is the name of the staging environment? -> zephyr-staging (note-F)
8. Who is the escalation owner? -> Dana Whitfield (note-H)
9. How many days is telemetry retained under the data retention policy? -> 400 (note-I)
10. On what date is API v2 deprecated? -> 2026-11-30 (note-J)

Scoring: binary per question (1 = correct, 0 = incorrect) against the key, with normalization: case-insensitive; numerics stripped of "$", ",", and whitespace; dates accepted as ISO (2026-11-30) or unambiguous written form ("November 30, 2026"); name answers require exact tokens ("Dana Whitfield" both tokens). Subject score = sum/10. Subject SUCCESS = score >= 8/10. Scoring is performed blind: the scorer receives only numbered answers with no arm labels.

Primary outcome: proportion of successful subjects per arm (p_t, p_c). Secondary descriptive only: per-question accuracy rates — no inferential claims (no multiple testing).

4. STATISTICS

Test: Fisher's exact test, two-sided, on the 2x2 table [treatment successes, treatment failures; control successes, control failures]. Alpha = 0.05. Effect size: Cohen's h = 2*arcsin(sqrt(p_t)) - 2*arcsin(sqrt(p_c)).

Tier-S bar: the lesson L-RETRIEVE is claimed supported ONLY IF two-sided Fisher's exact p < 0.05 AND Cohen's h >= 1.4, computed on the primary outcome proportions. The primary test is run exactly once, after all data are collected and all validity gates in Section 5 pass. No interim analysis, no peeking, no re-running after a miss. n = 10 subjects per arm (20 total), fixed before launch; replacements only under gate V5.

5. VALIDITY GATES

Gates V1, V2, V5, V6 are checked after data collection but before the primary test; V3, V4 are computed from the data immediately before the test. If any gate fires INVALID, the trial is discarded, no inferential claim is made, and the prescribed remedy is executed.

V1 — Treatment compliance: at least 8 of 10 treatment subjects must show retrieval evidence (a retrieval step or corpus/note citation preceding their answers). If fewer than 8 comply -> INVALID. Remedy: revise the treatment brief, do not analyze, re-run.

V2 — Control purity: 0 control subjects may reference the corpus, Smart Notes, or retrieval. If 1 or more does -> INVALID (contamination). Remedy: discard, strengthen environment isolation, re-run.

V3 — Floor: treatment success proportion p_t must be >= 0.40. If p_t < 0.40 -> INVALID (corpus does not contain usable answers). Remedy: redesign the corpus, do not analyze.

V4 — Ceiling: control success proportion p_c must be <= 0.30. If p_c > 0.30 -> INVALID (questions answerable without retrieval). Remedy: redesign questions, do not analyze.

V5 — Completeness: a subject answering fewer than 10 questions is excluded and replaced; maximum 2 replacements per arm. If more than 2 replacements are needed in either arm -> INVALID (environment/tooling fault). Remedy: audit the spawning environment before any re-run.

V6 — Freshness and blinding: any subject with prior exposure to the corpus, questions, or answer key is excluded and replaced. If the scorer is unblinded to arm assignment before scoring -> re-score with a blinded scorer; if re-scoring is impossible -> INVALID.

6. PRE-LAUNCH AUDIT CHECKLIST

All checks are performed and logged before any subject is spawned. The trial does not start until every item passes.

A1. Corpus file audit: /corpus/notes/ exists, is readable from the treatment environment, and contains exactly the 10 note files listed in Section 2; each note contains exactly one key fact. File list logged.

A2. Coverage audit: every question maps to exactly one note; every answer-key string appears verbatim in its note (verified by exact-string search); coverage = 100%. Question-to-note mapping table logged.

A3. Brief audit: the draft control brief's trap (corpus mention + "consult as needed" + "all available resources") was identified and the brief rewritten. The final control brief contains none of the words "corpus", "notes", "retrieve", "resources" (verified by word search). The final treatment brief contains the mandatory "BEFORE answering" retrieval instruction. Both briefs logged verbatim.

A4. Non-guessability audit: all answers are invented entities (proper names, exact numbers, dates) with no basis in general knowledge; an independent reviewer confirms none of the 10 answers can be derived by reasoning alone without the corpus.

A5. Environment isolation: the control environment has no /corpus/notes/ path; the treatment environment has read access. Verified by a probe command in each environment, results logged.

A6. Freshness: all 20 subject IDs logged; none has prior exposure to the corpus, questions, or answer key.

A7. Randomization: arm assignment by seeded shuffle; seed and full assignment log committed before spawning.

A8. Scoring rubric frozen: binary per-question key with the normalization rules from Section 3; scorer receives only numbered answers, no arm labels; rubric committed.

A9. Analysis script frozen: computes the 2x2 table, two-sided Fisher's exact p, and Cohen's h; alpha = 0.05; script committed and will be run exactly once after gates pass.

A10. Sample-size and no-peeking rules frozen: n = 10 per arm; replacement rules per V5; no interim analysis or data inspection before all subjects complete.
