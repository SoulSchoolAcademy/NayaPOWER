# Auto-Match Convergence — 2026-10-24

ONE canonical auto-match engine, composed from the three audited prototypes onto
main `39796760e143dab3b6b10a3126bf7b123cd631ea`. The v1.4 Welcome Engine line is
canonical: same published weights (Lock Packet, Issue #3029 — topics .40 /
goals .25 / offers_needs .20 / wants .15), same score contract
(score / rank / signals / surface ≥2 / parts / reasons), extended with the
concept taxonomy, word tier, light stemming, symmetric wants, and
value-adjusts-rank-only. No carried code file was modified — every carried file
is byte-identical to its source blob.

## Sources

- PRIMARY `naya-power/welcome-engine-v1` @ `f1a6808d7d392435b9d033b148029b40f358850d`
- SECONDARY `naya-power/smart-match-v1-engine` @ `eed70d87643767cd141e53640164e109a60d92dc`
- REFERENCE ONLY `naya/citizen-discovery-automatch-core-20261023` @ `82441644a5d78e575f700b2d42dfc5060b9985fb` (not carried — see below)

## Carried

From the primary line, byte-identical:

- `tools/welcome-engine/welcome_engine.py` — build_vector / generate_pages / activate
- `tools/welcome-engine/smart_match.py` — THE engine (v1.4 math)
- `tools/welcome-engine/declared_vectors.py` — declared SEATS / PROJECTS vectors
- `tools/welcome-engine/calibrate.py` — weight calibration against the golden set
- `tools/welcome-engine/golden_set.py` — 12 synthetic citizens, known right answers
- `tools/welcome-engine/test_smart_match.py` — 9 tests
- `tools/welcome-engine/test_welcome_engine.py` — 14 tests
- `tools/welcome-engine/DEMO-RECEIPTS.json`, `tools/welcome-engine/SCORECARD-WELCOME-ENGINE.md` — lineage evidence
- `tools/smart-match/smart_match_v1_4.sql` — SQL twin of the v1.4 math.
  **NOT deployed** (its own header says so) — carried as a file only; deployment
  rides the production gate.

From the secondary line, byte-identical:

- `tools/smart-match/FIRST-RUN-2026-10-24.md` — the v1 engine's first run over
  the live declared population; evidence the primary line lacks
- `tools/smart-match/SCORECARD.md` — the scorecard loop that drove v1 → v1.2

## Dropped, and why

- Secondary `tools/smart-match/smart_match.py` (v1.2) and
  `smart_match_v1_1.py` (v1.1) — intermediate versions on the same lineage;
  v1.4's own history records the fixes that supersede them (v1.1 dilution flaw,
  v1.3 word tier, v1.4 stemming).
- Secondary `tools/smart-match/smart_match_v1.py` (v1, literal tokens) —
  algorithmically subsumed by v1.4; its inline SEATS/PROJECTS data verified
  AST-equal to `declared_vectors.py`, so it contributes nothing unique.
- Secondary `tools/smart-match/declared_vectors.py` — the identical blob
  (`a24a3da1…`) exists on both branches; the canonical copy lives with the
  engine in `tools/welcome-engine/`, where every import expects it.
- Secondary `tools/smart-match/test_smart_match.py` (8 tests) — a strict
  subset of the primary's 9: diff shows the primary file is the same suite
  plus `test_word_tier_bridges_free_vocabulary`. Carrying both would duplicate
  8 tests verbatim.
- Primary `tools/smart-match/smart_match_v1_3.sql` and secondary
  `tools/smart-match/smart_match_v1.sql` — SQL twins superseded by
  `smart_match_v1_4.sql` per its own header.

## Test evidence (actual runs at this converged layout, battery-venv python)

- `test_smart_match.py`: **9/9 passed**
- `test_welcome_engine.py`: **14/14 passed**
- `golden_set.py`: **12 passed, 0 failed**
- `calibrate.py`: current weights score 12 right / 0 wrong on the golden set
  and appear in the calibration grid — the published .40/.25/.20/.15 weights
  are evidence-checked, not just asserted
- `smart_match.py` __main__: ranked matches with reasons over the declared
  seats × projects population (e.g. Power → NayaPOWER space, 57%, 4 signals)

## Not carried: the discovery walk (reference branch)

Tree's `HUB/citizen-discovery-core.js` is NOT merged. What it provides that
this engine line lacks — recorded for the wiring step:

- The 10-question intake session itself: stateful answer / skip / back / edit
  over its own field set (about, interests, mission, vision, goals, motto,
  business, offer, space_topics, looking_for), emitting a
  `citizen-discovery-v1` packet.
- The consent machinery: private-by-default, per-field public flags, editing
  an answer revokes its earlier consent, and a discovery opt-in gate — no
  matching at all without opt-in; non-public / opted-out / self / blocked
  candidates are never ranked. The Python engine scores whatever vector it is
  handed; consent enforcement currently lives only in this walk.
- Content organization: `classifyPublicItem` / `organizePublicItems`
  auto-file public items into categories without duplicating or moving
  objects (the spaces/mail auto-organization surface). No equivalent exists
  in the Python line.
- Its output contract: `estimated_relevance_percent` +
  `signal_coverage_percent` + an explicit `uncalibrated: true` honesty flag.
  The v1.4 engine returns score / rank / parts / reasons with golden-set
  calibration behind the weights, but has no coverage % and no uncalibrated
  flag.
- Draft generation from the packet (`makeDrafts` → personal / business /
  space UNPUBLISHED_PREVIEW drafts) and the three input modes
  (speak / type / ask-AI-to-draft) at the UI level.

Its 18 test blocks / 68 asserts (counted from the file) were not run: nothing
of the walk is carried in this branch, per the convergence scope.
