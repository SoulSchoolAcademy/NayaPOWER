SHEET-ID: SHEET-20
VIOLATION 1:
LOCATION: "Work efficiently: keep the notes you have already read open so you can reuse them across questions." (control brief, §4)
MECHANISM: Leaky control briefing (invalid mode 2). This sentence states the lesson's prescription outright — reusing already-read notes across repeated questions IS "cache retrieval results within a session to avoid redundant corpus reads." The control arm receives the treatment content without the lesson framing, so any between-arm difference cannot be attributed to L-CACHE; the control briefing also independently creates a derivability ceiling (mode 1).
FIX: Delete the sentence from the control brief; end the brief at "Answer all 6 questions in order."

VIOLATION 2:
LOCATION: "A session cache is available at /cache/session.json — consult it as needed before answering." (control brief, §4)
MECHANISM: Availability contamination (invalid mode 3). The lesson text itself invokes the Trial-06 finding that merely mentioning a cache/session path drives cache use in uninstructed agents. In a trial isolating a caching lesson, naming the session-cache path to the control arm primes exactly the behavior the lesson prescribes, biasing control reads downward and shrinking the measurable effect toward zero.
FIX: Remove the cache-path mention from the control brief entirely; the treatment arm's lesson framing is the only legitimate source of cache awareness.

VIOLATION 3:
LOCATION: "**Lesson selection:** L-CACHE was chosen because it restates our standing efficiency doctrine (SN-0301 'minimize redundant reads'); we expect a strong effect since agents already follow this practice in normal work." (§2)
MECHANISM: Doctrine redundancy (invalid mode 4). The preregistration admits the lesson is already encoded in standing doctrine — the exact condition under which Trial-08 produced unanimous 20/20 ceilings. Both arms will follow the practice regardless of briefing, so no lesson effect can be detected; the authors' expectation of a "strong effect" is the opposite of what doctrine redundancy predicts.
FIX: Replace L-CACHE with a lesson not already encoded in standing doctrine (verified by a doctrine-text search, not an assumption), or reframe the lesson as a novel, non-obvious caching technique beyond the existing doctrine.

VIOLATION 4:
LOCATION: "Briefing notes that corpus reads take approximately 30 seconds each, so subjects should plan their reads accordingly." (§3)
MECHANISM: Derivability ceiling (invalid mode 1). The task setup itself hands the control arm the cost signal that makes caching the obvious strategy — a general reasoning agent that reads "30 seconds each, plan accordingly" will avoid redundant reads without any lesson. The lesson's marginal effect is thus unmeasurable before launch; no pre-check piloting the task against the lesson-free default was performed (the mode's required pre-check).
FIX: Remove the cost/time annotation from the task briefing, or run the required pre-check (pilot the task on lesson-free defaults) and proceed only if it shows a non-zero redundant-read rate.
SOUND SECTIONS: 1 (Hypothesis), 5 (Statistics and validity gate — Mann-Whitney on counts plus the explicit ceiling gate is sound design), 6 (Threats and mitigations — randomized assignment and log-based grading), treatment arm definition in 4 (lesson framed as retrieved corpus note, distinct from control briefing)
