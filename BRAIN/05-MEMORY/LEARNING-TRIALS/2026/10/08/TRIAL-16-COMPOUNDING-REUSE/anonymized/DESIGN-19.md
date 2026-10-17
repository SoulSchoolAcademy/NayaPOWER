PREREGISTRATION-DESIGN

================================================================
PREREGISTRATION — Trial 11: Retrieval-Before-Answering (L-RETRIEVE)
Lesson under test: L-RETRIEVE — "Retrieve relevant Smart Notes from
the corpus at decision time BEFORE answering project-specific
questions."
Method lesson applied: L16 (behavioral-trial validity gates from
Trials 05–10, 2026-10-07).
================================================================

1. HYPOTHESIS
----------------------------------------------------------------
Precise behavioral effect being isolated: Instructing a subject to
retrieve relevant Smart Notes from the corpus at decision time,
before answering project-specific questions, causes a higher
proportion of subjects to give correct answers than identical
subjects who are never instructed to retrieve and never shown the
corpus path.

The marginal effect measured is the lesson's own prescription —
pre-answer retrieval of the corpus — and nothing else. The control
arm is designed so that no part of the lesson leaks into it: it
receives no corpus path, no retrieval instruction, no mention that
reference material exists, and a task that cannot be solved from
general reasoning alone (see Validity gates).

Null hypothesis (H0): the pass proportions are equal in the two
arms. Alternative (H1): the treatment arm's pass proportion is
higher. Claimed effect: pre-answer retrieval instruction, applied
to a retrieval-possible-but-unguessable task.

2. ARM DEFINITIONS
----------------------------------------------------------------
Both briefs are written out in full. Neither arm knows there are
two arms. Subjects are independent; no subject sees the other
brief.

ARM T (treatment) — brief text, exact:
"You are answering project-specific questions. At decision time,
BEFORE answering, retrieve the relevant Smart Notes from the
corpus at /corpus/notes/. Read the notes that bear on each
question first, then answer thoroughly using what you retrieved."

ARM C (control) — brief text, exact (rewritten from the starter
draft; see audit note):
"You are answering project-specific questions. Answer thoroughly."

AUDIT NOTE ON THE STARTER DRAFT: The starter draft — "Project
reference notes are available at: /corpus/notes/ — consult them as
needed before answering" — was rejected for two recorded invalid
modes. (i) Availability contamination (L16 mode 3): merely
mentioning that a corpus/path exists drove retrieval in
uninstructed agents (observed: control 9.0/9 with a neutral path
mention vs cold 0.0/9 without it). For a retrieval-isolation trial
the control arm must not see the corpus path. (ii) Leaky control
briefing (L16 mode 2): "consult them as needed" states the lesson's
prescription (consult-before-answering), contaminating the control
arm. The rewritten control brief contains no path, no corpus
mention, and no retrieval language. This was verified by the grep
audit in section 6.

Corpus state: the corpus at /corpus/notes/ contains the Smart
Notes whose answers the task questions require (see section 3).
Both arms run in the same environment; the only difference between
arms is the brief.

3. TASK / QUESTIONS
----------------------------------------------------------------
Each subject receives 6 project-specific questions, fixed wording,
same order, in both arms. Every question's correct answer is
present in exactly one corpus Smart Note and is not inferable from
the question text, the brief, or general reasoning (established by
the derivability-ceiling pilot in section 5: lesson-free subjects
must score mean <= 1/6).

The six questions (each asks for a project-specific fact recorded
only in one corpus note):
  Q1. What is the freeze deadline recorded in the launch-schedule
      note for the Q3 rollout?
  Q2. Which module does the incident-review note flag as the
      cause of the November 2 outage?
  Q3. What is the approved budget figure for the analytics
      rebuild, as recorded in the budget note?
  Q4. Which two partners are named in the partnership note as
      signed for the pilot program?
  Q5. What is the retention window (in days) stated in the
      data-retention note for raw event logs?
  Q6. What version number does the release note assign to the
      hotfix deployed on October 5?

Scoring: each answer is scored correct (1) or incorrect (0)
against a pre-written rubric listing the exact acceptable answer
for each question. Scoring is performed by a scorer blind to arm
assignment. Primary subject-level outcome: PASS = at least 4 of
6 correct (score >= 4); FAIL = 3 or fewer. Per-question scores
and retrieval evidence (any corpus note quoted or cited in the
subject's answer) are recorded as secondary data.

Derivability floor check: before launch, the exact Q1–Q6 set is
piloted on lesson-free default subjects (no brief, no path);
proceed only if their mean score is <= 1/6 (section 5).

4. STATISTICS
----------------------------------------------------------------
- Primary outcome: binary per-subject PASS/FAIL (>= 4/6 correct).
- Test: Fisher's exact test, two-sided, on the 2x2 table of arm
  (T vs C) by outcome (PASS vs FAIL).
- Alpha: 0.05 (two-sided).
- Tier-S bar (pre-committed): the trial counts as a SUCCESS only
  if BOTH hold: (a) Fisher's exact two-sided p < 0.05, AND
  (b) Cohen's h >= 1.4 computed on the two PASS proportions
  (h = 2*arcsin(sqrt(p_T)) - 2*arcsin(sqrt(p_C))).
  If either condition fails, the trial is reported as NON-SUCCESS;
  no post-hoc rescoring, no re-thresholding.
- Sample size: n = 20 subjects per arm (40 total), pre-fixed.
  (Reference calibration: p_T = 0.90 vs p_C = 0.05 gives
  h = 2*arcsin(0.949) - 2*arcsin(0.224) ≈ 2.50 - 0.45 ≈ 2.05,
  which clears the Tier-S bar; the bar therefore demands a large,
  near-floor-to-near-ceiling separation, not a marginal gap.)
- Randomization: subjects are assigned to arms by a pre-generated
  random sequence, alternating concealment; arm label recorded but
  hidden from the scorer.
- No interim analyses; no peeking; all 40 subjects run before any
  scoring.

5. VALIDITY GATES
----------------------------------------------------------------
A gate firing means the trial does not launch (pre-launch gates)
or its result is declared invalid (launch gate). Each gate states
a numeric threshold and its consequence.

GATE V1 — Derivability ceiling (L16 mode 1). Pre-launch pilot:
5 lesson-free default subjects (no brief, no corpus path) take
Q1–Q6. Threshold: if their mean score > 1/6, the task is
derivable without the lesson and the trial is INVALID — do not
launch; rewrite the questions to be corpus-specific and re-pilot.

GATE V2 — Leaky control briefing (L16 mode 2). Grep the exact
control brief text for the stems: retriev, corpus, notes, path,
/corpus, consult, before answer. Threshold: if total matches > 0,
the control brief is leaky — do not launch; rewrite the brief and
re-run the grep to zero matches before proceeding.

GATE V3 — Availability contamination (L16 mode 3). Pre-launch
cold check: 5 subjects receive the exact control brief and take
the task; record how many quote or cite any corpus note.
Threshold: if > 0 of 5 retrieve or cite a corpus note, the
corpus is leaking through another channel (or the task prompts
it) — do not launch; find and close the leak, re-run the cold
check to 0/5.

GATE V4 — Doctrine redundancy (L16 mode 4). After V1 passes:
pilot the exact task on 5 subjects given the treatment brief; if
both arms in the pilots sit at unanimous ceilings or floors in a
way showing the lesson is already encoded in standing doctrine
(treatment mean = 6/6 AND control mean >= 5/6, i.e., no measurable
headroom), the lesson is already learned — do not launch; the
lesson cannot be measured by this instrument.

GATE V5 — Floor/ceiling separation pre-check. Using the V1 and V4
pilot means: require pilot control mean <= 1/6 AND pilot
treatment mean >= 4/6. If either fails, the instrument cannot
produce a Tier-S-sized separation — do not launch; redesign the
task.

GATE V6 — Brief integrity at launch. On launch day, re-diff the
briefs actually served against the exact texts in section 2.
Threshold: any character-level difference — halt, restore the
exact texts, and restart that arm's subjects. No exceptions.

6. PRE-LAUNCH AUDIT CHECKLIST
----------------------------------------------------------------
Every check is performed before any subject is spawned. Each is a
concrete, pass/fail operation.

[1] Corpus content lock: verify that each of Q1–Q6 has its
correct answer present in exactly one Smart Note at
/corpus/notes/ and in no other note the subject could reach.
Record the note filename and answer for each question.

[2] Derivability pilot (Gate V1): run 5 lesson-free default
subjects on Q1–Q6; compute mean score; pass iff mean <= 1/6.

[3] Control-brief grep audit (Gate V2): run
grep -Ei 'retriev|corpus|notes|path|/corpus|consult|before answer'
on the exact control brief text; pass iff zero matches. Save the
grep output as the audit receipt.

[4] Cold-arm contamination check (Gate V3): run 5 subjects on the
exact control brief; pass iff 0 of 5 quote or cite any corpus
note.

[5] Treatment-brief pilot (Gate V4/V5): run 5 subjects on the
exact treatment brief; pass iff treatment mean >= 4/6 and control
pilot mean >= 5/6 does not hold (i.e., lesson not doctrine-
redundant, and separation exists).

[6] Brief text freeze: hash both exact briefs (sha256); record
hashes in the launch log. Gate V6 re-diffs at launch.

[7] Scorer blinding: confirm the scoring rubric contains only
acceptable answers and no arm labels; confirm the scorer receives
anonymized, shuffled answers with arm labels stripped.

[8] Randomization pre-generation: generate the 40-subject
arm-assignment sequence with a recorded seed before any subject
is spawned; store the seed and sequence in the launch log.

[9] Subject independence: confirm no subject shares context,
memory, or transcript with any other subject; each subject is
spawned fresh with only its arm's brief and the task.

[10] Corpus path scope: confirm the treatment brief's path
(/corpus/notes/) is reachable by treatment subjects and that
control subjects receive no environment variable, hint, or
directory listing that reveals it.

[11] Stop-condition review: confirm in writing that all five
pre-launch gates (V1–V5) passed with numeric results logged, and
that any gate failure would have halted launch per section 5.

Launch is authorized only when all 11 checks pass and their
receipts are recorded. Any failure of a gate at any point —
including after partial subject runs — invalidates the trial;
partial data are discarded, not analyzed.
