PREREGISTRATION-DESIGN

1. HYPOTHESIS
The lesson under test is L-RETRIEVE: "Retrieve relevant Smart Notes from the corpus at decision time BEFORE answering project-specific questions."
Precise behavioral hypothesis: subjects who are explicitly briefed to retrieve relevant Smart Notes from the project corpus before answering project-specific questions will produce a higher rate of factually correct answers — where correctness depends on corpus-specific facts that are not derivable from general reasoning or standing knowledge — than subjects who receive no retrieval instruction and no corpus access. The isolated effect is the marginal behavioral gain of *retrieval-before-answering* as a decision-time procedure, holding the question set and scoring fixed.

2. ARM DEFINITIONS
The two arms differ ONLY in the brief text below. No other materials, paths, or mentions differ.

TREATMENT ARM BRIEF (full text):
"You are answering project-specific questions. Before answering, you MUST retrieve relevant Smart Notes from the project corpus at this location: /corpus/notes/. Search the corpus for notes relevant to each question, read them, and let what you find guide your answers. Retrieval comes FIRST — do not answer any question from memory or general knowledge without checking the corpus first. After retrieving, answer each question thoroughly, using what you found in the notes."

CONTROL ARM BRIEF (full text):
"You are answering project-specific questions. Answer each question as best you can using your own knowledge and reasoning. Answer thoroughly."

Design note: the draft control brief was rejected. It stated "Project reference notes are available at: /corpus/notes/ — consult them as needed," which violates L16 mode 3 (availability contamination: a neutral path mention drives uninstructed retrieval, observed 9.0/9 control vs 0.0/9 cold) and mode 2 (leaky control briefing). The control arm therefore sees no corpus path, no mention of notes, and no retrieval instruction anywhere in any material shown to it.

3. TASK / QUESTIONS
Subjects receive 9 project-specific questions (Q1–Q9). Each question's correct answer depends on a distinct, specific Smart Note present in /corpus/notes/ (note IDs mapped one-to-one, e.g., Q1 -> NOTE-101, Q2 -> NOTE-102, ..., Q9 -> NOTE-109). The required facts are idiosyncratic to this project (e.g., specific decisions, dates, numbers, names from the notes) and are not answerable from general knowledge, standing doctrine, or task setup — verified by the derivability pilot in Section 5.
Scoring: each question is scored binary — CORRECT (1) if the answer matches the note-derived key exactly on the checked fact(s), INCORRECT (0) otherwise. Partial credit is not given. Primary subject-level outcome: PASS if >= 7 of 9 questions are correct; FAIL otherwise. The primary outcome proportion per arm is the pass rate (number passing / number of subjects). A secondary item-level analysis reports mean per-question correctness, but the Tier-S bar applies to the subject-level pass-rate comparison only.

4. STATISTICS
- Test: Fisher's exact test, two-sided, on the 2x2 table (arm: treatment vs control; outcome: pass vs fail).
- Alpha: 0.05.
- Tier-S bar (both must hold): Fisher's exact two-sided p < 0.05 AND Cohen's h >= 1.4 on the primary outcome proportions, where h = 2*arcsin(sqrt(p_treatment)) - 2*arcsin(sqrt(p_control)).
- Planned sample: 10 subjects per arm (n=10 treatment, n=10 control), run as independent fresh subjects. Illustrative Tier-S pass: control 0/10 pass vs treatment 8/10 pass -> Fisher two-sided p = 0.0007, h = 2.214 >= 1.4.

5. VALIDITY GATES (numeric thresholds; fire = trial halted and result reported as INVALID, not PASS/FAIL)
- Gate G1 — Derivability ceiling (L16 mode 1). Before launch, pilot the 9 questions with 5 lesson-free subjects given the control brief and no corpus access. FIRES if any pilot subject answers any question correctly (>0 correct on any item), or if pilot mean correctness exceeds 0.05. On fire: rewrite the offending questions against harder corpus-specific facts and re-pilot; the trial does not launch until G1 passes.
- Gate G2 — Control-brief leak audit (L16 mode 2). Grep the final control brief and every other control-arm-visible string for the tokens: corpus, notes, retrieve, retrieval, consult, reference, /corpus, available, before answering (as an instruction), search. FIRES if any hit count > 0. On fire: rewrite the control materials and re-audit; no subject is spawned until zero hits.
- Gate G3 — Control-arm corpus blindness (L16 mode 3). Log every subject's tool/file access. FIRES if >= 1 control subject accesses /corpus/notes/ or mentions the corpus path in its output. On fire: the control arm is contaminated — stop, investigate the leak source, fix materials, and restart with fresh subjects; contaminated runs are discarded, not pooled.
- Gate G4 — Doctrine-redundancy / unanimous ceiling (L16 mode 4). FIRES if control-arm pass rate >= 0.90 or if treatment-arm pass rate <= control-arm pass rate with both arms >= 0.90 (i.e., >= 18 of 20 subjects pass). On fire: the lesson's prescription is already reachable without the instruction — the trial is INVALID and the lesson is marked doctrine-redundant for this task class.
- Gate G5 — Corpus completeness. FIRES if any of NOTE-101 through NOTE-109 is missing or unreadable from /corpus/notes/ at subject-runtime. On fire: restore the corpus and re-verify before launch; no partial-corpus runs are counted.

6. PRE-LAUNCH AUDIT CHECKLIST
Each item must be verified and logged before the first subject is spawned:
[ ] A1. Corpus check: all 9 target notes (NOTE-101..NOTE-109) exist, readable, and contain the keyed facts for Q1–Q9.
[ ] A2. Brief freeze: treatment and control briefs locked; diff confirms they differ only as specified in Section 2.
[ ] A3. G2 leak grep run on control brief + all control-visible strings; recorded result: zero hits on all listed tokens.
[ ] A4. G1 derivability pilot complete (5 lesson-free subjects, control brief, no corpus); recorded result: 0/45 item-correct, all gates documented.
[ ] A5. Access logging verified: a canary probe confirms subject file/tool access is logged and /corpus/notes/ reads are attributable per subject.
[ ] A6. Randomization plan recorded: 20 fresh subjects, random 1:1 assignment to arms, no subject sees the other arm's brief.
[ ] A7. Scoring key frozen: per-question binary key published before launch; scorer is blind to arm assignment.
[ ] A8. No other shared material (harness text, task preamble, error messages) mentions a corpus, notes, or retrieval instruction; A8 verified by the same G2 token grep.
