SHEET-ID: SHEET-14
VIOLATION 1:
LOCATION: "L-CACHE was chosen because it restates our standing efficiency doctrine (SN-0301 "minimize redundant reads"); we expect a strong effect since agents already follow this practice in normal work."
MECHANISM: Doctrine redundancy (invalid mode 4): the lesson under test is already encoded in standing doctrine and "agents already follow this practice in normal work," so both arms will reach the same behavior and the lesson's marginal effect is unmeasurable — the text predicts a "unanimous ceiling" outcome rather than a testable effect.
FIX: Select a lesson not already encoded in standing doctrine or normal practice.

VIOLATION 2:
LOCATION: "A session cache is available at /cache/session.json — consult it as needed before answering."
MECHANISM: Availability contamination (invalid mode 3): the control brief — which both arms receive — mentions the session-cache path; per the retrieved lesson, merely mentioning the path drives cache use in uninstructed agents, contaminating the control arm and collapsing the arm contrast.
FIX: Delete the cache-path mention from the control brief; only the treatment arm may see the cache path.

VIOLATION 3:
LOCATION: "Work efficiently: keep the notes you have already read open so you can reuse them across questions."
MECHANISM: Leaky control briefing (invalid mode 2): this sentence, given to the control arm, states the lesson's prescription (reuse already-read notes across questions = cache within a session), so control agents receive the treatment's effect through the shared brief.
FIX: Delete the sentence and give the control arm neutral instructions only.

VIOLATION 4:
LOCATION: "Briefing notes that corpus reads take approximately 30 seconds each, so subjects should plan their reads accordingly."
MECHANISM: Derivability ceiling (invalid mode 1): the task briefing itself tells both arms that reads are costly and should be "plan[ned]," enabling the lesson-free control arm to reach the lesson's prescription (avoid redundant reads) from the task setup alone, making the lesson's marginal effect unmeasurable.
FIX: Remove the read-cost cue and framing from the briefing; run the required pre-launch pilot of the task against the lesson-free default.
SOUND SECTIONS: Hypothesis, arm definition sentence (treatment receives L-CACHE + control brief), Statistics (validity gate for ceiling effect is a sound fail-safe), Threats and mitigations
