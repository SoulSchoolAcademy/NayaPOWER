# Sampler Report — Learning Loop v1 Wake-Up Run (2026-10-22)

Lane E (Bullseye execution), from Naya Nitro's activation-readiness
analysis, Axis 3 / build-plan step 11. Base tip: `d390730b3`.

## In a nutshell

The verification harness (`tools/lesson_verification.py`, asleep since
its 2026-10-10 pilot) ran tonight against the first three declared
behavior changes filed under the Lesson Law — SN-0815, SN-0816, SN-1787.
Each declared change now carries a battery of novel cases in
`tools/lesson_verification/batteries/`, authored from the declaration's
own falsifier conditions. Novelty passed on all three batteries
(mechanically enforced: no case replays its origin incident). Scored
blind with the harness's deterministic judge: **declared-change
transcripts held 6/9 cases; replaced-behavior transcripts were caught
3/3.** The loop's first joint is connected: declaration (prose) →
declared_change row (data) → battery (test) → verdict (published here).

## Finding #1 — the registry gate cannot see tonight's lessons yet

`verify --registry .naya/memory/smart-notes/index.json` exits 2 for all
three batteries: *"cannot verify an unregistered lesson."* The three
notes are published on main as files, but the projection index (655
entries) holds **no entries for SN-0815, SN-0816, SN-1787 (or SN-1788)** —
the pages landed ahead of their capture→registry rows (the same drift
the brain-drive measured at 00:01Z, and the same class the drift ratchet
test `test_live_repository_drift_never_grows_per_class` is currently
red for on main: published_pages_without_registry_entry 1 → 5). The
scored runs below therefore ran without `--registry`, and this report
names the gap instead of papering over it. The cure path is the door's
own backfill (capture-side), plus — from this lane's PR — the extractor
in `tools/smart_note_v2.py`, which attaches `declared_change` to every
future registry entry at write time and scans the published corpus into
`.naya/memory/smart-notes/declared-changes.json` (query returns all
three of tonight's declarations as structured rows today).

## Method (and its honest limits)

Subjects are **authored transcripts**, the 2026-10-10 pilot's method:
per battery, two transcripts enacting the declared change and one
enacting the behavior it replaces. The verdicts therefore prove the
batteries *discriminate* the declared behavior from the replaced one on
novel problems, scored blind — they do not prove any live seat behaved
either way in production. The default judge is lexical (word-boundary
signal matching): deterministic and auditable, crude by design. Live
subject sampling (a seat answering scenarios cold) and a semantic judge
remain follow-on work for the weekly sampler, as does scheduling —
step 11's remaining parts (Tau scheduling; Chi verification).

## Results

| Lesson | Novelty | Cases | Held | Caught (old behavior) | Battery verdict |
|---|---|---|---|---|---|
| SN-0815 — file the lesson note the same session | OK (3 fingerprints avoided) | 3 | N1, N2 | N3 (lesson left in a summary + memory) | FAIL 2/3 |
| SN-0816 — verify claims at the primary source | OK (4 avoided) | 3 | N1, N2 | N3 (self-reported claim forwarded as-is) | FAIL 2/3 |
| SN-1787 — the Lesson Law (classification) | OK (3 avoided) | 3 | N1, N2 | N3 (chat-only lesson marked learned) | FAIL 2/3 |

A battery's verdict is FAIL whenever any case fails — by design. Read
with the method above, the run's meaning is: **every transcript that
enacted the declared change passed; every transcript that enacted the
replaced behavior failed, on both missing must-signals and present
anti-signals.** Full per-criterion reports were produced by the harness
(`report_sn-0815.json` / `report_sn-0816.json` / `report_sn-1787.json`,
schema `naya.lesson-verification-report.v1`) and are reproducible:

```
python3 tools/lesson_verification.py check-novelty --battery tools/lesson_verification/batteries/sn-0815-lesson-filing-standard.json
python3 tools/lesson_verification.py verify --battery tools/lesson_verification/batteries/sn-0815-lesson-filing-standard.json --responses tools/lesson_verification/pilot/responses_sn-0815.json
# (same shape for sn-0816-verify-at-primary-source / sn-1787-the-lesson-law)
```

## What this closes, and what it does not

Closes: declared changes are data (extractor + registry + query);
batteries exist for the first post-Oct-10 lessons; the sampler has run
once and published held/failed counts. Does not close: the index.json
backfill for the four drifted notes (door/capture lane's mechanism —
the ratchet test stays red until it lands); the weekly sampler schedule
(Tau, step 11); live-subject sampling; the bridge census dispositions
(this lane's census is published separately on Learning board #1713);
the distillation cadence (step 12, another lane's item).
