PREREGISTRATION-DESIGN

1. HYPOTHESIS
Treatment agents who are explicitly instructed to retrieve relevant Smart Notes from the learning corpus at decision time BEFORE answering project-specific questions will answer more project-specific questions correctly (by using note-derived facts unavailable from general reasoning) than control agents who receive no retrieval instruction and no mention of the corpus. The isolated behavioral effect is: retrieval-first behavior at decision time, attributable to the lesson prescription alone.

2. ARM DEFINITIONS
Arm T (treatment) brief, in full:
"You are answering project-specific questions. Before answering, FIRST retrieve relevant Smart Notes from the corpus at: /corpus/notes/. Search the corpus for notes relevant to each question and read them BEFORE forming your answer. Only after consulting the retrieved notes, answer each question thoroughly using the notes you found."
Arm C (control) brief, in full:
"You are answering project-specific questions. Answer each question thoroughly based on your own knowledge."
Note: the draft starter brief was rejected. It stated "Project reference notes are available at: /corpus/notes/ — consult them as needed before answering," which violates L16 modes 2 and 3 (leaky control briefing + availability contamination): mentioning the corpus path drives retrieval in uninstructed agents. The control brief above contains no corpus path, no mention of notes, and no retrieval directive.

3. TASK / QUESTIONS
Subjects receive 8 project-specific questions. Each question asks for a fact that (a) is present in at least one corpus Smart Note, and (b) cannot be answered correctly from general reasoning or publicly known information alone. Question bank is built by selecting facts from 8 distinct corpus notes; each question names the project context and asks for the specific recorded fact (e.g., a recorded parameter value, a recorded decision, a recorded threshold). Scoring: binary per question — 1 point if the answer contains the note-derived fact matching the answer key, 0 otherwise. Subject-level primary outcome: subject is a "success" if they answer >= 6 of 8 questions correctly; otherwise a "non-success." Primary proportions: p_T = success proportion in Arm T, p_C = success proportion in Arm C. Secondary outcome: mean per-question score per arm.

4. STATISTICS
Primary test: Fisher's exact test (two-sided) on the 2x2 table (arm x success/non-success). Alpha = 0.05. Tier-S bar: BOTH conditions must hold — (a) Fisher's exact two-sided p < 0.05, AND (b) Cohen's h >= 1.4 computed on the primary outcome proportions (h = 2*arcsin(sqrt(p_T)) - 2*arcsin(sqrt(p_C))). Planned sample: 20 subjects per arm (40 total). Hypothesis direction: p_T > p_C. If Tier-S bar is not met, the trial reports "no demonstrated behavioral effect," not a partial pass.

5. VALIDITY GATES
Gate V1 — Derivability ceiling (pilot). Before launch, run 6 pilot subjects on the 8 questions under the exact Arm C brief (no lesson, no path). Compute pilot success proportion. If pilot success proportion >= 0.40 (i.e., >= 6/8 correct by 40%+ of pilot subjects without the lesson), the task is derivable from standing doctrine/general reasoning and the trial is INVALID — halt, do not launch; redesign the question bank with less-derivable facts.
Gate V2 — Leaky control briefing (audit). Before launch, grep the Arm C brief text against the lesson's key content terms: {"corpus", "retrieve", "Smart Note", "note", "consult", "before answering", "path", "/corpus"}. Any match = leak. On leak: rewrite the control brief and re-run the grep until zero matches; do not launch with any match.
Gate V3 — Availability contamination (manipulation check). Post-trial, in the debrief survey ask each control subject: "Were you aware of a notes corpus or note repository available for this task?" If > 10% of control subjects answer yes, the control arm was contaminated; the trial is INVALID regardless of the statistics — report as invalid, do not claim an effect.
Gate V4 — Doctrine redundancy (ceiling check). If both arms achieve >= 90% success (i.e., >= 18/20 successes in each arm), the lesson is already encoded/redundant and the trial is INVALID — unanimous ceiling observed; report as invalid, do not claim an effect.
Gate V5 — Floor check. If Arm T success proportion <= 20% (<= 4/20), the treatment manipulation failed (instruction not followed or corpus unusable); trial is INVALID — investigate the corpus/access path before any re-run.
On any gate firing INVALID: no effect is claimed, no statistics are interpreted as evidence for the lesson, and the result is reported as an invalid trial with the gate named.

6. PRE-LAUNCH AUDIT CHECKLIST
C1. Run the 6-subject pilot under the exact Arm C brief; compute pilot success proportion; confirm < 0.40 (Gate V1).
C2. Grep the Arm C brief for all Gate V2 terms; confirm zero matches; record the grep output.
C3. Grep the Arm T brief to confirm it contains the lesson prescription ("retrieve", "corpus at: /corpus/notes/", "BEFORE forming your answer"); confirm all three present.
C4. Verify each of the 8 questions against the answer key: the keyed fact is present in the corpus note cited for that question; confirm with a quoted citation per question.
C5. Verify each of the 8 questions is non-derivable: confirm with the pilot results (C1) that pilot subjects did not answer them from general knowledge.
C6. Confirm sample plan: 20 subjects per arm, 40 total, random assignment, subjects blinded to other arm and to the lesson being tested.
C7. Confirm the corpus path /corpus/notes/ is accessible to Arm T subjects only, and no subject sees the other arm's brief.
C8. Confirm the statistical plan is registered as stated: Fisher's exact two-sided, alpha 0.05, Tier-S bar = p < 0.05 AND Cohen's h >= 1.4, no interim peeks.
C9. Confirm the debrief contamination question (Gate V3) is in the post-trial survey.
C10. Confirm none of the investigators has shown subjects either brief before launch; briefs are locked and hash-recorded before the first subject is spawned.
