SHEET-ID: SHEET-08

VIOLATION 1:
LOCATION: "**Lesson selection:** L-CACHE was chosen because it restates our standing efficiency doctrine (SN-0301 "minimize redundant reads"); we expect a strong effect since agents already follow this practice in normal work."
MECHANISM: The preregistration admits the lesson is already standard practice that agents follow by default. A lesson restating what agents already do adds nothing; any measured arm difference cannot be attributed to the lesson (and control will likely floor at zero redundant reads, tripping the ceiling gate).
FIX: Select a lesson that is not already standing practice and not already followed by default.

VIOLATION 2:
LOCATION: "Work efficiently: keep the notes you have already read open so you can reuse them across questions."
MECHANISM: The control brief states the lesson's prescription directly (retain already-read notes for reuse) without the lesson's content. Control reaches the measured behavior from the brief alone, so any arm difference can only come from the note-framing, not from the lesson — the lesson's effect is unisolated.
FIX: Delete that sentence from the control brief.

VIOLATION 3:
LOCATION: "A session cache is available at /cache/session.json — consult it as needed before answering."
MECHANISM: The setup itself provides both the session-cache mechanism and an instruction to use it, given to both arms via the shared control brief. The distinctive behavior the lesson prescribes is handed to control by the setup, collapsing the treatment/control distinction and driving the measured behavior independently of the lesson.
FIX: Remove the session-cache mention and instruction from the control brief; provide cache availability only within the treatment's lesson note if needed.

VIOLATION 4:
LOCATION: "To increase measurement precision, the task presents each of the 3 questions TWICE in sequence (Q1, Q2, Q3, Q1, Q2, Q3)."
MECHANISM: The repeated-question structure telegraphs the optimal strategy to control subjects — any agent seeing Q1 reappear can infer reuse without the lesson, so the setup itself drives the measured behavior rather than the lesson.
FIX: Randomize question order and do not disclose the repetition structure.

VIOLATION 5:
LOCATION: "Briefing notes that corpus reads take approximately 30 seconds each, so subjects should plan their reads accordingly."
MECHANISM: Disclosing the read cost plus "plan their reads accordingly" nudges both arms toward read-avoidance (caching) independent of the lesson, compressing both arms toward zero redundant reads and erasing the measurable treatment margin.
FIX: Remove the cost disclosure and planning instruction from the briefing.

SOUND SECTIONS: 1. Hypothesis; 5. Statistics (Mann-Whitney U, Tier-S bar, ceiling validity gate); 6. Threats and mitigations
