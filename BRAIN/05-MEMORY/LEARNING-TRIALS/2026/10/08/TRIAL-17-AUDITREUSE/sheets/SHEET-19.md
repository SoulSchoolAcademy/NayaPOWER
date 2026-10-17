SHEET-ID: SHEET-19

VIOLATION 1:
LOCATION: "A session cache is available at /cache/session.json — consult it as needed before answering."
MECHANISM: Leaky control briefing (invalid mode 2) plus availability contamination (invalid mode 3). The control brief — given to BOTH arms — explicitly directs agents to the session-cache path and tells them to consult it. Per the retrieved lesson's Trial-06 evidence, merely mentioning a cache path drives cache use in uninstructed agents, and this goes further by actively instructing it. The control arm will cache because it was told to, suppressing arm separation and collapsing the lesson's measurable marginal effect to zero.
FIX: Remove the cache-path sentence from the control brief entirely; the cache path may appear only inside the treatment arm's retrieved L-CACHE note.

VIOLATION 2:
LOCATION: "Work efficiently: keep the notes you have already read open so you can reuse them across questions."
MECHANISM: Leaky control briefing (invalid mode 2). This sentence states the lesson's prescription verbatim — avoid redundant reads by reusing already-read material — inside the brief both arms receive. The control arm is thus briefed with the lesson's content, contaminating it; any measured difference between arms cannot be attributed to the retrieved lesson.
FIX: Delete the sentence from the control brief; a neutral brief should state only the task ("Answer all 6 questions in order.") with no efficiency prescriptions.

VIOLATION 3:
LOCATION: "L-CACHE was chosen because it restates our standing efficiency doctrine (SN-0301 "minimize redundant reads"); we expect a strong effect since agents already follow this practice in normal work."
MECHANISM: Doctrine redundancy (invalid mode 4). The preregistration openly admits the lesson duplicates standing doctrine SN-0301 and that agents already practice it. Per the Trial-08 precedent cited in the lesson (20/20 both arms), this guarantees unanimous ceiling behavior — the trial would measure recall of already-learned doctrine, not the lesson's marginal effect, and the expected "strong effect" is an artifact of that redundancy.
FIX: Select a lesson that is absent from standing doctrine; if L-CACHE must be used, first demonstrate via the required pre-check that agents do not already follow it in the default condition.

VIOLATION 4:
LOCATION: "Briefing notes that corpus reads take approximately 30 seconds each, so subjects should plan their reads accordingly."
MECHANISM: Derivability ceiling (invalid mode 1). Handing both arms the cost rationale (30s per read) lets the control arm derive the caching prescription from the task setup alone via general reasoning, independent of the retrieved lesson. The lesson's marginal effect becomes unmeasurable, and the required pre-check — piloting the task against the lesson-free default — is absent.
FIX: Remove the read-time note from the briefing given to either arm, and run the required pilot of the task against the lesson-free default before launch.

SOUND SECTIONS: Hypothesis (states a testable marginal-effect claim), Statistics (primary outcome, Mann-Whitney U, α=0.05, Tier-S bar all pre-specified), ceiling validity gate (control median redundant-read count = 0 → INVALID is a correct mode-1 tripwire), randomization with recorded seed, grader reading from complete session logs
