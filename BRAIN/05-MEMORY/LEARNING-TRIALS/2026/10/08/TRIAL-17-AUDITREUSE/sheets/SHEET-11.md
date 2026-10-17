SHEET-ID: SHEET-11
VIOLATION 1:
LOCATION: "**Lesson selection:** L-CACHE was chosen because it restates our standing efficiency doctrine (SN-0301 "minimize redundant reads"); we expect a strong effect since agents already follow this practice in normal work."
MECHANISM: Doctrine redundancy (invalid mode 4). The lesson under test is already encoded in standing doctrine, so both arms should perform at ceiling regardless of the treatment — per the lesson, lessons already encoded in standing doctrine produce unanimous ceilings (Trial-08: 20/20 both arms). The preregistration even admits the contamination ("agents already follow this practice in normal work"), which means any measured difference cannot be attributed to the lesson's marginal effect and a null difference cannot distinguish "lesson inert" from "everyone already learned."
FIX: Select a lesson that is NOT already encoded in standing doctrine, and verify non-redundancy by auditing standing doctrine for equivalent prescriptions before finalizing.

VIOLATION 2:
LOCATION: "> You are answering project-specific questions. Project reference notes live at /corpus/notes/. A session cache is available at /cache/session.json — consult it as needed before answering. Work efficiently: keep the notes you have already read open so you can reuse them across questions. Answer all 6 questions in order."
MECHANISM: Leaky control briefing (invalid mode 2). "Keep the notes you have already read open so you can reuse them across questions" states the lesson's own prescription — avoid redundant corpus reads by reusing already-read notes — directly to the control arm, and "Work efficiently" reinforces it. The control arm is therefore taught the treatment's content; the trial measures nothing about L-CACHE's marginal effect.
FIX: Remove the prescription sentence and the "Work efficiently" prompt from the control brief (retain only neutral task instructions and the question list).

VIOLATION 3:
LOCATION: "A session cache is available at /cache/session.json — consult it as needed before answering."
MECHANISM: Availability contamination (invalid mode 3, caching analogue). The lesson explicitly warns that for caching trials, merely mentioning a session-cache path drives cache use in uninstructed agents. The control brief names the cache path and directs subjects to consult it, so control-arm cache use no longer reflects absence of the lesson — the control is instructed into the treated behavior, destroying treatment/control separation.
FIX: Remove all mention of the session-cache path from the control brief; if a cache exists in the environment, keep it invisible to control-arm subjects and log its use only via session logs.

VIOLATION 4:
LOCATION: "Briefing notes that corpus reads take approximately 30 seconds each, so subjects should plan their reads accordingly."
MECHANISM: Derivability ceiling (invalid mode 1). Even apart from the brief leaks, telling subjects that corpus reads are costly (~30 seconds) and to "plan their reads accordingly" gives the control arm everything needed to derive the caching prescription from general reasoning alone — any competent agent minimizes expensive repeated reads without needing L-CACHE. Combined with section 2's admission that agents "already follow this practice," the control arm can reach the lesson's prescription from the task setup, making the lesson's marginal effect unmeasurable.
FIX: Remove the cost-and-planning hint from the task description, and run the required pre-check: pilot the task against the lesson-free default before launch to confirm control agents do not spontaneously cache.

SOUND SECTIONS: Hypothesis, Statistics (primary outcome, test, Tier-S bar, and stated ceiling-validity gate), Arm definitions structure (n=10 per arm, treatment-receives-both framing), Threats and mitigations
