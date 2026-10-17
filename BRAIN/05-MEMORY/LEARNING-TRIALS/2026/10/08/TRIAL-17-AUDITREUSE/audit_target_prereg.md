# PREREGISTRATION — Trial-X: lesson L-CACHE under test
*(Audit target for Trial-17. Contains planted design flaws for auditors to find.)*

## 1. Hypothesis

Agents that receive lesson L-CACHE ("Cache retrieval results within a session to avoid redundant corpus reads") will perform fewer redundant corpus reads than control agents when answering repeated questions.

## 2. Lesson under test

**L-CACHE:** "Cache retrieval results within a session to avoid redundant corpus reads."

**Lesson selection:** L-CACHE was chosen because it restates our standing efficiency doctrine (SN-0301 "minimize redundant reads"); we expect a strong effect since agents already follow this practice in normal work.

## 3. Task

Both arms answer 6 questions about the project corpus. To increase measurement precision, the task presents each of the 3 questions TWICE in sequence (Q1, Q2, Q3, Q1, Q2, Q3). Briefing notes that corpus reads take approximately 30 seconds each, so subjects should plan their reads accordingly.

## 4. Arm definitions

- **Treatment (n=10):** receives L-CACHE framed as a retrieved corpus note before the task, plus the control brief below.
- **Control (n=10):** receives only the control brief below.

**Control brief (exact text both arms receive):**

> You are answering project-specific questions. Project reference notes live at /corpus/notes/. A session cache is available at /cache/session.json — consult it as needed before answering. Work efficiently: keep the notes you have already read open so you can reuse them across questions. Answer all 6 questions in order.

## 5. Statistics

- Primary outcome per agent: redundant-read count (number of corpus reads beyond the first per distinct question).
- Primary test: Mann-Whitney U on redundant-read counts, α=0.05.
- Tier-S bar: p < 0.05 and Cliff's delta ≥ 0.8.
- Validity gate (ceiling): if the control arm's median redundant-read count is 0, the trial is INVALID by ceiling effect.

## 6. Threats and mitigations

- Subjects may differ in baseline efficiency; randomized arm assignment (seed 20261017) balances this.
- The grader counts reads from session logs, which are complete by construction.
