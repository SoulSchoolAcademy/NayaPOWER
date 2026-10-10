SHEET-ID: SHEET-01

VIOLATION 1:
LOCATION: "You are answering project-specific questions. Project reference notes live at /corpus/notes/. A session cache is available at /cache/session.json — consult it as needed before answering. Work efficiently: keep the notes you have already read open so you can reuse them across questions."
MECHANISM: The control brief — received by both arms — explicitly instructs the lesson's exact prescription: consult a session cache and reuse already-read notes to avoid redundant reads. Control agents can therefore reach full treatment-level behavior from the control brief alone, so any measured difference cannot be attributed to L-CACHE. The arms are behaviorally indistinguishable by construction.
FIX: Strip the cache-availability and reuse instructions from the control brief; control agents receive only the task and the corpus location.

VIOLATION 2:
LOCATION: "To increase measurement precision, the task presents each of the 3 questions TWICE in sequence (Q1, Q2, Q3, Q1, Q2, Q3). Briefing notes that corpus reads take approximately 30 seconds each, so subjects should plan their reads accordingly."
MECHANISM: The repeated-question structure (Q1, Q2, Q3, Q1, Q2, Q3) makes the caching strategy obvious to both arms without any lesson, and the explicit 30-second read-cost warning further drives both arms toward caching. The task setup itself produces the measured behavior, collapsing any arm difference to zero regardless of lesson exposure.
FIX: Present each question once (or place repeats in a separate session) and remove the read-cost planning warning from the shared briefing.

VIOLATION 3:
LOCATION: "L-CACHE was chosen because it restates our standing efficiency doctrine (SN-0301 "minimize redundant reads"); we expect a strong effect since agents already follow this practice in normal work."
MECHANISM: The preregistration admits the lesson under test restates already-standard practice that agents follow by default. A trial cannot isolate the effect of a lesson the treatment adds nothing beyond what subjects already do — any observed delta is a baseline artifact (or its absence a floor/ceiling artifact), not a measurable lesson effect.
FIX: Test a novel lesson not already embedded in standing doctrine and default practice, or first demonstrate by pretest that baseline practice actually differs from the lesson's prescription.

VIOLATION 4:
LOCATION: "L-CACHE was chosen because it restates our standing efficiency doctrine (SN-0301 "minimize redundant reads"); we expect a strong effect since agents already follow this practice in normal work." combined with the control brief in section 4 and "Validity gate (ceiling): if the control arm's median redundant-read count is 0, the trial is INVALID by ceiling effect."
MECHANISM: The trial's own design predictably triggers its own invalidity gate: control agents are both instructed to cache (control brief) and already do so by default (lesson selection), so a control median of zero redundant reads is the expected outcome. A trial designed to return INVALID yields an uninterpretable result by design, not by chance — the gate functions as an admission that the measurement cannot work.
FIX: Remove the control priming (VIOLATIONS 1–2 fixes) so the control arm has a plausible nonzero redundant-read baseline, and pretest the baseline before committing the ceiling gate.

SOUND SECTIONS: Hypothesis, Arm definitions (randomized n=10 per arm with fixed seed), Statistics (Mann-Whitney U on per-agent redundant-read counts, α=0.05, Tier-S bar requiring p < 0.05 and Cliff's delta ≥ 0.8), Threats and mitigations
