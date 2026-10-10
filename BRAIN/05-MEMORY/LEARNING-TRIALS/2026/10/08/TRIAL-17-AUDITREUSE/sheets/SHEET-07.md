SHEET-ID: SHEET-07

VIOLATION 1:
LOCATION: "L-CACHE was chosen because it restates our standing efficiency doctrine (SN-0301 "minimize redundant reads"); we expect a strong effect since agents already follow this practice in normal work."
MECHANISM: Doctrine redundancy (invalid mode 4). The lesson is already encoded in standing doctrine that control agents follow in normal work, so the trial measures an already-learned principle — the analogue of Trial-08's 20/20 unanimous ceiling, where no marginal effect is observable.
FIX: Select a lesson that is novel relative to standing doctrine, or withdraw the trial.

VIOLATION 2:
LOCATION: "You are answering project-specific questions. Project reference notes live at /corpus/notes/. A session cache is available at /cache/session.json — consult it as needed before answering. Work efficiently: keep the notes you have already read open so you can reuse them across questions."
MECHANISM: Availability contamination (invalid mode 3, caching analogue) and leaky control briefing (invalid mode 2). Merely mentioning the session-cache path in the control brief drives cache use in uninstructed agents, and the instruction "keep the notes you have already read open so you can reuse them across questions" states the lesson's prescription directly, contaminating the control arm so any measured difference cannot be attributed to L-CACHE.
FIX: Remove the cache-path mention and the reuse instruction from the control brief; the control arm must see neither the cache path nor any caching prescription.

VIOLATION 3:
LOCATION: "the task presents each of the 3 questions TWICE in sequence (Q1, Q2, Q3, Q1, Q2, Q3)"
MECHANISM: Derivability ceiling (invalid mode 1). Identical questions repeated back-to-back let the control arm reach the lesson's prescription ("avoid redundant reads") from the task setup and general reasoning alone, so the lesson's marginal behavioral effect is unmeasurable; the required pilot of the task against the lesson-free default was not performed.
FIX: Redesign the task so the caching opportunity is not structurally obvious (e.g., questions with partial overlap rather than verbatim repetition), and pilot it against the lesson-free default before launch.

VIOLATION 4:
LOCATION: "Briefing notes that corpus reads take approximately 30 seconds each, so subjects should plan their reads accordingly."
MECHANISM: Derivability ceiling (invalid mode 1). Telling both arms that reads are expensive and to "plan their reads accordingly" is task-setup pressure that directly implies avoiding redundant reads, giving the control arm the lesson's prescription without L-CACHE.
FIX: Remove the cost framing from the briefing, or keep a neutral cost statement that does not cue read-planning behavior, and verify the change in the lesson-free pilot.

SOUND SECTIONS: Hypothesis, Lesson definition, Primary outcome definition, Statistical test (Mann-Whitney U, α=0.05, Tier-S bar), Randomized arm assignment (seed 20261017), Grader based on complete session logs
