SHEET-ID: SHEET-02
VIOLATION 1:
LOCATION: "L-CACHE was chosen because it restates our standing efficiency doctrine (SN-0301 "minimize redundant reads"); we expect a strong effect since agents already follow this practice in normal work."
MECHANISM: Doctrine redundancy (invalid mode 4). A lesson already encoded in standing doctrine produces unanimous ceilings (Trial-08: 20/20 both arms) — "agents already follow this practice" predicts both arms will cache regardless of the lesson, making the lesson's marginal effect unmeasurable.
FIX: Select a lesson NOT already encoded in standing doctrine; require a pre-check that the lesson is novel to subjects.
VIOLATION 2:
LOCATION: "A session cache is available at /cache/session.json — consult it as needed before answering."
MECHANISM: Leaky control briefing (invalid mode 2) and availability contamination (invalid mode 3). The control brief itself states and exemplifies the lesson's prescription ("cache retrieval results within a session"), and per Trial-06, merely mentioning a session-cache path drives cache use in uninstructed agents — the control arm will cache because the brief told it to, not because of the lesson.
FIX: Delete the session-cache sentence from the control brief; the control arm must not see the cache path in a caching-isolation trial.
VIOLATION 3:
LOCATION: "Work efficiently: keep the notes you have already read open so you can reuse them across questions."
MECHANISM: Leaky control briefing (invalid mode 2). This states the lesson's prescription ("reuse results within a session to avoid redundant reads") directly in the control brief, contaminating the control arm with the exact behavior under test.
FIX: Replace with a neutral efficiency instruction (e.g., "Work efficiently.") that does not describe or imply reusing reads.
VIOLATION 4:
LOCATION: "Briefing notes that corpus reads take approximately 30 seconds each, so subjects should plan their reads accordingly."
MECHANISM: Derivability ceiling (invalid mode 1). With repeated questions presented twice in sequence and an explicit 30-second read cost, the control arm can reach the lesson's prescription (cache/reuse within session) from the task setup and general reasoning alone — the required pre-check (pilot the task against the lesson-free default) was skipped.
FIX: Pilot the task with lesson-free subjects before launch; if the lesson-free default already avoids redundant reads, redesign the task (e.g., remove the explicit cost cue and repeated-sequence structure) until the ceiling no longer holds.
SOUND SECTIONS: 1. Hypothesis; 5. Statistics (primary outcome, Mann-Whitney test, Tier-S bar, and the ceiling-effect validity gate, which correctly names the failure mode); 6. Threats and mitigations (randomization seed, complete session logs for grading).
