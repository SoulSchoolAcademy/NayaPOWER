SHEET-ID: SHEET-05

VIOLATION 1:
LOCATION: "> You are answering project-specific questions. Project reference notes live at /corpus/notes/. A session cache is available at /cache/session.json — consult it as needed before answering. Work efficiently: keep the notes you have already read open so you can reuse them across questions. Answer all 6 questions in order."
MECHANISM: The control brief explicitly states the lesson's prescription ("keep the notes you have already read open so you can reuse them across questions" = L-CACHE's "cache retrieval results within a session to avoid redundant corpus reads"). Because BOTH arms receive this brief, the control arm receives the lesson, destroying the isolation of the lesson's effect — any treatment-vs-control difference cannot be attributed to L-CACHE, and since the treatment arm also receives the brief's prescription on top of the lesson, even a treatment effect would be confounded by it.
FIX: Remove the caching prescription from the control brief. Give both arms a neutral brief (e.g., "Answer all 6 questions in order using /corpus/notes/.") with no mention of the session cache or reusing reads.

VIOLATION 2:
LOCATION: "**Lesson selection:** L-CACHE was chosen because it restates our standing efficiency doctrine (SN-0301 "minimize redundant reads"); we expect a strong effect since agents already follow this practice in normal work."
MECHANISM: The lesson restates already-standard practice that the subject population already follows by default. The control arm is therefore expected to emit the lesson's behavior without the lesson, so the trial cannot measure the lesson's effect — the preregistration itself predicts a no-delta/ceiling outcome, contradicting its own validity-gate design. Any observed delta could only reflect noise or confounds, making a positive result uninterpretable.
FIX: Select a lesson that is non-obvious and not part of standing doctrine — e.g., a project-specific retrieval heuristic agents would not apply by default — so the control arm plausibly lacks the lesson's prescription.

SOUND SECTIONS: Section 1 Hypothesis, Section 3 Task (repeat structure is legitimate transfer design), Section 5 Statistics (including the ceiling validity gate), Section 6 Threats and mitigations
