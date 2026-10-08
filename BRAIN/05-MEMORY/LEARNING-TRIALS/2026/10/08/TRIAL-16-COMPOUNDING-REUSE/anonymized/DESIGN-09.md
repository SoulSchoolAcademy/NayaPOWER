PREREGISTRATION-DESIGN

1. Hypothesis
Lesson under test (L-RETRIEVE): "Retrieve relevant Smart Notes from the corpus at decision time BEFORE answering project-specific questions."
Behavioral effect isolated: the marginal increase in correct application of corpus Smart Note content at decision time that is attributable to an explicit instruction to retrieve relevant Smart Notes before answering, holding the questions fixed.
H1: Agents instructed to retrieve relevant Smart Notes from the corpus before answering (treatment) show a higher proportion of subjects reaching the PASS criterion than agents given the same questions with no retrieval instruction and no mention of any corpus or notes (control).
H0: The PASS proportions are equal across arms.
The test is two-sided per the Tier-S bar; a success claim additionally requires the treatment proportion to be the higher one.

2. Arm definitions
The two briefs are identical except for the retrieval paragraph, which appears only in the treatment brief. The six questions (Section 3) are appended identically to both briefs.

CONTROL BRIEF (exact text):
"You are answering project-specific questions.

Answer each question directly and concisely, in your own words. Base your answers on your own reasoning.

Questions:
[The six project-specific questions defined in Section 3, appended here verbatim, identical for both arms.]"

TREATMENT BRIEF (exact text):
"You are answering project-specific questions.

Before answering, retrieve the relevant Smart Notes from the corpus at /corpus/notes/ and use them to inform your answers. Do not answer from general reasoning alone -- check the corpus first, then answer.

Answer each question directly and concisely.

Questions:
[The six project-specific questions defined in Section 3, appended here verbatim, identical for both arms.]"

Note on the starter draft: the draft control brief was REJECTED. It named the corpus path "/corpus/notes/" (availability contamination, L16 mode 3: a neutral path mention drove control retrieval to 9.0/9 vs 0.0/9 cold) and it instructed subjects to "consult them as needed before answering" (leaky prescription, L16 mode 2). The rewritten control brief above contains no corpus path, no mention of notes, and no retrieval instruction.

3. Task/questions
Each subject, in a single fresh session, answers the same six project-specific questions in one response.
Question construction: each question asks for one specific recorded project fact or decision (e.g., a named threshold, an approved fallback, a designated owner, a recorded constraint) that appears in exactly one Smart Note in the corpus at /corpus/notes/ and is not stated anywhere in the brief. The six questions map to six distinct notes.
Scoring: each answer is scored binary by a scorer blinded to arm assignment, against a rubric locked before launch. For each question the rubric quotes the required answer element from its mapped note and lists acceptable paraphrases. Score 1 if the required element is present and correctly applied to the question; score 0 otherwise, including ambiguous, partial, or hedged answers that do not commit to the element.
Subject-level outcome: PASS = at least 5 of 6 answers scored 1. FAIL = 4 or fewer.
Primary outcome: the proportion of subjects reaching PASS, per arm.

4. Statistics
Test: Fisher's exact test, two-sided, on the 2x2 table of subject outcome (PASS / FAIL) by arm (treatment / control).
Alpha: 0.05.
Tier-S bar: a success claim requires BOTH Fisher's exact two-sided p < 0.05 AND Cohen's h >= 1.4 on the PASS proportions, where h = 2*arcsin(sqrt(p_treatment)) - 2*arcsin(sqrt(p_control)), with p_treatment > p_control.
Sample size: N = 20 subjects per arm, fixed in advance, assigned by a pre-generated randomization list. No interim analyses and no peeking; both statistics are reported regardless of outcome. Pilot subjects (Section 5, Gate 1) are excluded from the 20 per arm.

5. Validity gates
Gate 1 -- Derivability ceiling (pre-launch pilot, L16 mode 1). Run the exact six questions against 6 lesson-free pilot agents briefed with the control brief (no corpus mention, no retrieval instruction). FIRES if total pilot correct answers >= 2 out of 36 (pilot accuracy >= 5.6%) OR any single question is answered correctly by >= 2 of the 6 pilot subjects. On fire: replace the compromised question(s) with new non-derivable questions and re-run the pilot once. If the second pilot also fires, ABORT the trial as INVALID -- the lesson's marginal effect is unmeasurable on this task set.
Gate 2 -- Leaky control briefing (pre-launch audit, L16 mode 2). Run grep -iE '\bretriev\w*|\bcorpus\b|\bnotes?\b|\bconsult\w*|\breference\b|\bavailable\b|\bresources?\b|before answering|look[\s-]?up' against the final control brief file. Threshold: exactly 0 matches. On fire (>0 matches): rewrite the control brief, re-run the audit; the trial cannot launch until the count is 0.
Gate 3 -- Availability contamination (pre-launch audit, L16 mode 3). (a) grep -F '/corpus' across ALL control-side materials (brief, task prompt, system prompt): threshold 0 matches. (b) diff of control brief vs treatment brief: threshold is exactly one added block (the retrieval paragraph) and zero other differences. On fire: remove the leak / align the briefs; the trial cannot launch until both checks pass.
Gate 4 -- Unanimous ceiling / floor (post-data, L16 mode 4). FIRES if both arms' PASS proportions are >= 0.90 (ceiling: lesson not isolatable, consistent with doctrine redundancy) OR both are <= 0.10 (floor: task too hard for retrieval to move). On fire: the trial is reported as INVALID/UNINFORMATIVE -- not as a null effect and not as a success -- with the observed proportions published.

6. Pre-launch audit checklist
All checks are performed and recorded BEFORE any subject (pilot or main) is spawned:
1. Questions and rubric locked: the six questions are fixed verbatim; each maps to exactly one existing Smart Note file under /corpus/notes/; the rubric quotes the required answer element from each mapped note. Verify by listing /corpus/notes/ and opening each mapped note.
2. Draft control brief formally rejected and replaced; rejection reason recorded (corpus path mention = L16 mode 3; "consult them as needed before answering" = L16 mode 2).
3. Gate 2 grep audit on the final control brief returns 0 matches; command and output archived.
4. Gate 3(a): grep -F '/corpus' over all control-side materials returns 0 matches; command and output archived.
5. Gate 3(b): diff of control vs treatment brief shows exactly one added block (the retrieval paragraph), zero other differences; diff output archived.
6. Gate 1 derivability pilot completed with 6 lesson-free agents; thresholds checked; pilot raw outputs archived and excluded from the main N.
7. Scorer rubric locked; scorer is blinded to arm assignment; scoring sheet prepared with one binary column per question.
8. Randomization list for 20 subjects per arm generated before the first main spawn; analysis script (Fisher's exact two-sided + Cohen's h) written and dry-run on synthetic data.
9. Raw subject outputs will be saved to persistent storage before scoring begins.
10. Final sign-off: Gates 1-3 green and all items above recorded; only then spawn subjects.
