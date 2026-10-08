SHEET-ID: SHEET-03

VIOLATION 1:
LOCATION: "L-CACHE was chosen because it restates our standing efficiency doctrine (SN-0301 "minimize redundant reads"); we expect a strong effect since agents already follow this practice in normal work."
MECHANISM: Doctrine redundancy (invalid mode 4). The lesson is admitted to restate an already-encoded standing principle that agents "already follow in normal work." Lessons already learned by standing doctrine produce unanimous ceilings (cf. Trial-08: 20/20 both arms), so the control arm is expected to perform like the treatment arm — the lesson's marginal effect is unmeasurable and any between-arm difference cannot be attributed to the lesson.
FIX: Select a lesson that is novel relative to standing doctrine — i.e., not encoded in any ratified note or established practice — and verify its novelty by grep of the doctrine/notes corpus before launch.

VIOLATION 2:
LOCATION: "Work efficiently: keep the notes you have already read open so you can reuse them across questions."
MECHANISM: Leaky control briefing (invalid mode 2). This control-brief text — given to BOTH arms — states the lesson's prescription ("Cache retrieval results within a session to avoid redundant corpus reads") in operational form: keep what you read, reuse it, don't re-read. The control arm is contaminated; both arms receive the prescription, so any treatment-control difference cannot isolate the lesson's effect.
FIX: Remove the instruction from the control brief (both arms then get a neutral brief); apply the required pre-launch audit by grepping the control brief against the lesson's key content and confirming no overlap.

VIOLATION 3:
LOCATION: "A session cache is available at /cache/session.json — consult it as needed before answering."
MECHANISM: Availability contamination (invalid mode 3). The control arm — which in this caching trial must not be primed to cache — is told that a session-cache path exists and invited to consult it. Merely mentioning the cache path drives cache use in uninstructed agents, contaminating the control arm's baseline caching behavior; the control arm then no longer represents the lesson-free default.
FIX: Remove the cache-path mention and the consult instruction from the control brief; the control arm must not see the cache path.

SOUND SECTIONS: Hypothesis, Task, Statistics (including the ceiling validity gate), Threats and mitigations
