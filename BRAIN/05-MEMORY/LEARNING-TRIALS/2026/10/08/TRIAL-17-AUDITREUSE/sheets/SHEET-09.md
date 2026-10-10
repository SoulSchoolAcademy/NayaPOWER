SHEET-ID: SHEET-09
VIOLATION 1:
LOCATION: "**Lesson selection:** L-CACHE was chosen because it restates our standing efficiency doctrine (SN-0301 "minimize redundant reads"); we expect a strong effect since agents already follow this practice in normal work."
MECHANISM: Mode 4 (doctrine redundancy). The lesson encodes an already-learned principle that agents already follow in normal work, so both arms will perform identically and the lesson's marginal effect is unmeasurable — the Trial-08 unanimous-ceiling failure. The preregistration's expectation of a "strong effect" contradicts its own premise.
FIX: Test a lesson not encoded in standing doctrine; pilot it against the lesson-free default first.
VIOLATION 2:
LOCATION: "Work efficiently: keep the notes you have already read open so you can reuse them across questions."
MECHANISM: Mode 2 (leaky control briefing). The control brief directly states L-CACHE's prescription (reuse already-read notes across repeated questions), so the control arm receives the treatment content. Any between-arm difference is washed out by construction.
FIX: Delete that sentence from the control brief; give the control no reuse instruction.
VIOLATION 3:
LOCATION: "A session cache is available at /cache/session.json — consult it as needed before answering."
MECHANISM: Mode 3 (availability contamination). In a caching-isolation trial, merely mentioning the session-cache path drives cache use in uninstructed agents (Trial-06 analogue); the control must not see the cache path.
FIX: Remove the cache-path mention from the control brief; the control works without knowing the cache exists.
VIOLATION 4:
LOCATION: "the task presents each of the 3 questions TWICE in sequence (Q1, Q2, Q3, Q1, Q2, Q3). Briefing notes that corpus reads take approximately 30 seconds each, so subjects should plan their reads accordingly."
MECHANISM: Mode 1 (derivability ceiling). The task setup (questions repeated verbatim) plus the stated read cost lets the control arm derive the caching prescription from general reasoning and standing efficiency doctrine alone, making the lesson's marginal effect unmeasurable. No lesson-free pilot pre-check is reported.
FIX: Pilot the task with a lesson-free default before launch; proceed only if the pilot control performs redundant reads.
SOUND SECTIONS: Section 1 hypothesis (clear directional claim), Section 5 statistics (primary outcome, Mann-Whitney U, Tier-S bar, and the ceiling validity gate treating control-median-0 as INVALID), Section 6 randomization with fixed seed (20261017) and log-based read counting, treatment-arm delivery (L-CACHE framed as a retrieved corpus note).
