PREREGISTRATION-DESIGN

1. Hypothesis

L-RETRIEVE ("Retrieve relevant Smart Notes from the corpus at decision time BEFORE answering project-specific questions") has a causal behavioral effect: subjects explicitly instructed to retrieve relevant notes from the corpus at decision time will produce answers measurably more consistent with the corpus note content on project-specific questions than subjects who receive no retrieval instruction and no mention of any corpus. The isolated effect is the marginal gain in note-consistent answering attributable to the explicit retrieval-before-answering instruction, measured on questions whose correct answers exist only in the corpus notes and cannot be reached from standing doctrine or general reasoning.

2. Arm definitions

CONTROL arm — exact brief text (final, audited; contains no corpus path, no "notes", no "retriev", no "corpus", no instruction to consult anything):
---
"You are answering questions about a fictional project scenario. Answer each question as accurately and completely as you can based on your own reasoning. Do not browse the web. Take your time on each answer."
---

TREATMENT arm — exact brief text (contains the L-RETRIEVE prescription verbatim plus the corpus path):
---
"You are answering questions about a fictional project scenario. Before answering each question, FIRST retrieve the relevant Smart Notes from the corpus at /corpus/notes/ — search the corpus for notes relevant to the question, read them, and base your answer on what they say. Answer each question as accurately and completely as you can. Do not browse the web."
---

NOTE ON THE DRAFT CONTROL BRIEF: The supplied draft ("Project reference notes are available at: /corpus/notes/ — consult them as needed before answering.") was REJECTED. It violates L16 mode 3 (availability contamination: merely mentioning the corpus path drives retrieval in uninstructed agents; observed control 9.0/9 with a neutral path mention vs cold 0.0/9 without it) and mode 2 (leaky control briefing: "consult them as needed before answering" states the lesson's prescription — retrieve before answering). The control brief above was rewritten from scratch and contains none of the lesson's content.

3. Task/questions

Subjects each receive 6 fictional project-scenario questions. Each question's correct answer is stated in exactly one corpus note and is a project-specific fact or rule that does not appear in standing doctrine and is not inferable by general reasoning (e.g., "What is the failure threshold that triggers the circuit-breaker in the billing pipeline?" — answer: a specific value found only in note N3).

Scoring: two blind raters, unaware of arm assignment, score each answer independently against a fixed rubric derived from the source note:
- 1 = note-consistent (contains the corpus-specified fact/prescription with correct value),
- 0.5 = partially consistent (correct direction, wrong or missing specifics),
- 0 = inconsistent or absent.
Raters reconcile disagreements by discussion; inter-rater agreement (exact) must be >= 0.80 on a 20% overlap sample or scoring is repeated.

Primary outcome: per-subject note-consistent proportion = (total score across 6 questions) / 6. A subject counts as "success" if this proportion >= 0.67 (i.e., >= 4 of 6 effectively correct). Arm-level outcome = number of successes / arm size.

4. Statistics

- Test: Fisher's exact two-sided test on the 2x2 contingency table (success/failure x control/treatment), on the primary outcome as defined above.
- Alpha: 0.05.
- Tier-S bar: Fisher's exact two-sided p < 0.05 AND Cohen's h >= 1.4 on the primary outcome proportions (computed on the two arm success proportions). Both conditions must hold.
- Planned sample size: 12 subjects per arm (n=24), randomized to arms by sealed random allocation at spawn time.

5. Validity gates — with numeric thresholds and what happens when each fires

GATE V1 — Derivability ceiling (L16 mode 1). BEFORE launch, pilot 6 lesson-free default agents (no L-RETRIEVE, no corpus, no corpus path) on the exact 6 questions. Threshold: if the pilot mean note-consistent proportion >= 0.30, OR any single pilot subject reaches >= 0.67, the task is derivable without the lesson and the trial is INVALID. Action: trial halted; questions rewritten to be strictly corpus-dependent; re-pilot required before any launch.

GATE V2 — Leaky control briefing (L16 mode 2). BEFORE launch, grep the final control brief against the lesson's key content. Forbidden tokens/patterns (case-insensitive): "retriev", "note", "corpus", "/corpus", "before answering", "consult", "reference notes", "look up", "search". Threshold: ZERO matches permitted. Action: any match => control brief rejected and rewritten; audit repeated until zero matches before any subject is spawned.

GATE V3 — Availability contamination (L16 mode 3). The control brief must not mention any corpus, path, note repository, or retrieval affordance of any kind. Verified by the same grep audit as V2 plus manual reading of the full control brief by the trial designer. Threshold: zero corpus/path affordance references. Action: any reference found => INVALID launch state; control brief reverted to the clean version above; re-audit before spawning.

GATE V4 — Doctrine redundancy (L16 mode 4). BEFORE launch, pilot 5 agents briefed with standing doctrine only (no corpus, no path, no lesson) on the 6 questions. Threshold: if >= 4 of 5 pilot subjects reach success level (>= 0.67), the lesson's content is already encoded in standing doctrine and the trial is INVALID. Action: trial halted permanently for this lesson; no re-run with the same question set.

GATE V5 — Post-hoc ceiling check. After data collection, if both arms reach >= 90% success rate (unanimous ceiling), the result is classified INVALID (unanimous ceilings cannot distinguish lesson effect from redundancy/derivability), regardless of the p-value. Action: no Tier-S claim; finding reported as invalid trial with recommendation to redesign questions.

6. Pre-launch audit checklist

Before any subject is spawned, the trial designer verifies and records each item with a timestamped note:
1. [ ] Final control brief printed verbatim and grep-audited (V2/V3): zero matches on all forbidden tokens; audit output saved.
2. [ ] Final treatment brief printed verbatim: contains the L-RETRIEVE prescription and the exact corpus path /corpus/notes/.
3. [ ] All 6 questions + scoring rubrics finalized; each rubric answer cites the exact source note ID and quotes the corpus fact it depends on.
4. [ ] Derivability pilot (V1, n=6 lesson-free agents) completed: mean proportion and max recorded; below thresholds.
5. [ ] Doctrine-redundancy pilot (V4, n=5 doctrine-only agents) completed: successes < 4/5.
6. [ ] Raw-data store prepared: committed branch path for all subject transcripts, rubric scores, and rater reconciliation notes (no evidence stored in ephemeral locations).
7. [ ] Randomization procedure fixed: sealed random allocation, arm size 12/12, allocation log committed.
8. [ ] Scorer blinding procedure fixed: transcripts stripped of arm labels and brief text before scoring; rater agreement threshold (>= 0.80 exact on 20% overlap) documented.
9. [ ] Tier-S decision rule locked: Fisher's exact two-sided p < 0.05 AND Cohen's h >= 1.4 on primary outcome proportions; no peeking at partial data.
10. [ ] V5 post-hoc ceiling rule acknowledged in writing before launch.

All six gates must pass (V1–V4, plus the V2/V3 grep audit, plus the checklist) before the first subject is spawned.
