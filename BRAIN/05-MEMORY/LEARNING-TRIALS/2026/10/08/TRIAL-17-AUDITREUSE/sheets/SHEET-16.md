SHEET-ID: SHEET-16
VIOLATION 1:
LOCATION: "L-CACHE was chosen because it restates our standing efficiency doctrine (SN-0301 'minimize redundant reads'); we expect a strong effect since agents already follow this practice in normal work."
MECHANISM: Doctrine redundancy (invalid mode 4): the lesson is already encoded in standing doctrine, so both arms will ceiling — the marginal behavioral effect is unmeasurable by construction (cf. Trial-08: 20/20 both arms). The "strong effect" expectation is also incoherent with agents "already follow[ing] this practice in normal work."
FIX: Select a lesson not already encoded in standing doctrine and not already followed in normal work.
VIOLATION 2:
LOCATION: "consult it as needed before answering. Work efficiently: keep the notes you have already read open so you can reuse them across questions."
MECHANISM: Leaky control briefing (invalid mode 2): the control brief states the lesson's prescription — reusing already-read notes across questions within a session IS caching retrieval results to avoid redundant corpus reads — contaminating the control arm and invalidating the treatment-vs-control contrast.
FIX: Remove this sentence from the control brief; give no instruction implying note reuse or efficiency across questions.
VIOLATION 3:
LOCATION: "Project reference notes live at /corpus/notes/. A session cache is available at /cache/session.json"
MECHANISM: Availability contamination (invalid mode 3): per the lesson's caching-trial analogue, merely mentioning a session-cache path drives cache use in uninstructed agents (cf. Trial-06: control 9.0/9 with a neutral path mention vs Trial-04R cold 0.0/9 without it), inflating control-arm cache use and suppressing the measured difference even after the prescriptive wording is removed.
FIX: Omit the cache path (and corpus path) from the control brief; the control must not see the cache path in a caching-isolation trial.
VIOLATION 4:
LOCATION: "Briefing notes that corpus reads take approximately 30 seconds each, so subjects should plan their reads accordingly."
MECHANISM: Derivability ceiling (invalid mode 1): the control arm can reach the lesson's prescription from the task setup and general reasoning alone — a stated per-read cost plus repeated questions makes "reuse notes / plan reads" derivable without the lesson, so the marginal effect is unmeasurable; the required pre-check (piloting the task against the lesson-free default) is absent.
FIX: Delete the read-cost note from the briefing and pilot the task against the lesson-free default before launch; launch only if the pilot shows a non-zero control redundant-read baseline.
SOUND SECTIONS: §1 hypothesis, §5 statistics (outcome, test, Tier-S bar, ceiling validity gate), §6 threats and mitigations
