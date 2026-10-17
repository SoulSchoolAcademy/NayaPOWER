SHEET-ID: SHEET-15

VIOLATION 1:
LOCATION: "A session cache is available at /cache/session.json — consult it as needed before answering."
MECHANISM: Invalid mode 3 — availability contamination. The control arm must not see the cache path in a caching-isolation trial: merely mentioning that a session-cache path exists drives cache use in uninstructed agents (the brief's own lesson text cites Trial-06: control 9.0/9 with a neutral path mention vs Trial-04R cold 0.0/9 without it). Any treatment-control difference in caching behavior is therefore contaminated by the brief itself, not by L-CACHE.
FIX: Remove the cache-path sentence from the control brief entirely; mention only the corpus location (/corpus/notes/).

VIOLATION 2:
LOCATION: "Work efficiently: keep the notes you have already read open so you can reuse them across questions."
MECHANISM: Invalid mode 2 — leaky control briefing. This states the lesson's prescription ("Cache retrieval results within a session to avoid redundant corpus reads") in near-verbatim functional form: reuse what you already read instead of re-reading it. The control arm is directly briefed into the lesson's behavior, so the lesson's marginal effect on the control-vs-treatment contrast is unmeasurable by construction.
FIX: Delete the sentence. Replace with a prescription-free neutral instruction, e.g. "Answer all 6 questions in order."

VIOLATION 3:
LOCATION: "corpus reads take approximately 30 seconds each, so subjects should plan their reads accordingly."
MECHANISM: Invalid mode 2 — leaky control briefing (implication). A stated per-read cost plus an instruction to "plan their reads accordingly" implies the lesson's prescription (minimize/redundant-read avoidance) to both arms through the shared task setup, compressing the treatment effect toward zero regardless of L-CACHE. Per the lesson's own rule, briefing content that implies the prescription contaminates the control.
FIX: State the 30-second read cost as a neutral scheduling parameter without the read-planning directive, or remove it; the repeated-question structure alone already makes caching meaningful.

VIOLATION 4:
LOCATION: "L-CACHE was chosen because it restates our standing efficiency doctrine (SN-0301 "minimize redundant reads"); we expect a strong effect since agents already follow this practice in normal work."
MECHANISM: Invalid modes 1 (derivability ceiling) and 4 (doctrine redundancy). The lesson restates standing doctrine agents already follow, so the control arm can reach the prescription from standing doctrine alone — the lesson's marginal effect is unmeasurable. Precedent cited in the lesson: Trial-08 unanimous 20/20 ceiling when measuring an already-learned principle. The preregistration's expectation of "a strong effect since agents already follow this practice" inverts the requirement: already-followed practice is exactly what invalidates the isolation.
FIX: Select a lesson not encoded in standing doctrine (SN-0301 or otherwise) and not inferable from doctrine or task setup; run the required lesson-free pilot pre-check before launch. (The §5 ceiling validity gate detects this post-hoc but does not repair selection.)

SOUND SECTIONS: §1 hypothesis (clean causal claim, matched outcome), §3 repeated-question task design (Q1–Q3 presented twice makes redundant-read measurement meaningful), §4 treatment-arm delivery (L-CACHE framed as retrieved corpus note, matching a retrieval design), §5 statistics (Mann-Whitney U with α=0.05, Tier-S bar, and the median-0 ceiling INVALID gate — sound post-hoc tripwire), §6 threats and mitigations (seeded randomization; complete session logs)
