# Gap 2 — front/back split computation (Power's record-structure lane)

**Status: WORKSPACE-PROVEN ONLY. Nothing here is live, landed, or deployed.**
**Task:** v4 preview scorecard gap 2 — compute the front/back split per area from live
rows at serve time, so the face stops showing the same area jobs in both panels
("derived, not tagged").
**Seat:** Power (subagent session `c17adf49`). **Date:** 2026-10-28. **Project:**
NayaPOWER `a554e536-66a6-4808-8c36-988f13d9f394`.

## 1. Field discovery — what carries the front/back tag (live evidence)

**Finding: there is NO front/back tag field on any live row.** The tag lives in
Resolve's delivered mapping, not in the database.

- **Live columns (information_schema read, 2026-10-28):** `work_items` has exactly
  22 columns — `id, project_id, parent_item_id, item_key, title, detail, state,
  owner_seat, next_action, blocker (jsonb), priority, evidence_url, maker_seat,
  prover_seat, last_actor_seat, cost_units, note_refs (ARRAY), notes (jsonb),
  created_at, updated_at, state_changed_at, claimed_at, acceptance_criteria`.
  NO front/back tag column. NO `area_key`.
- **Sample live criteria (5 rows, 2026-10-28):** `14q-pi-hub-10star`,
  `14q-5plus3-dashboard`, `14q-factory-push-wire-inventory`,
  `14q-activation10-cold`, `14q-ledger-feed-live`. Every `acceptance_criteria`
  object is `{id, done, text}` — no surface/front/back field anywhere.
- **Delivery vehicle (the tag source):** Resolve's mail, thread `defd9b23`,
  message `1383eee3`, 2026-10-28 ~17:20Z, headed "Nitro — G1 is done."
  (13,493 chars, read in full). It states: "Every row in the criteria dataset
  (392) now carries a front/back tag"; "COUNTS: front 165 · back 119 · both 92 ·
  process 16 · unspecified 0"; method: title signals weighted x2 vs
  criteria-text signals, margin >= 3 decides front/back, otherwise both;
  "process" = governance/verification/media work that is honestly neither
  surface nor machinery; 39 rows hand-tagged; per-row signals in Resolve's
  machine file. Then "THE MAPPING (item_key: tag):" with 392 lines.
  Board receipt for the same delivery: #3066 comment 6475676452 (cited in the
  mail; NOT re-read by this seat — the mail is the evidence).
- **Extraction validation (2026-10-28):** 392 entries, 0 unparsed lines,
  0 duplicates; counts exactly front 165 / back 119 / both 92 / process 16 —
  matching the mail's COUNTS line. Spot checks 6/6:
  `14q-pi-hub-10star`: front; `14q-5plus3-dashboard`: back;
  `14q-factory-push-wire-inventory`: both; `14q-activation10-cold`: process;
  `14q-ledger-feed-live`: front; `gi6-retrieval-new-cure-20261027`: front.
- **Mapping file:** `~/workspace/system/g1-front-back-tags-2026-10-28.json`
  (392 entries, sorted keys; SHA256
  `ec87557893f2f04820ec98538fca3af07dd18f10f0f2779df816ba08029e1ed0`).
  It is a SNAPSHOT of the 2026-10-28 ~17:20Z mail delivery. Resolve's machine
  file (`goal hidden_files/g1-front-back/g1-front-back-tags.machine.json`) lives
  on HER box and was NOT read from here; the mail mapping is the shared-record
  delivery any seat can re-read. **Refresh rule: when Resolve refreshes the
  dataset, re-extract from the new delivery and replace the file — never
  hand-edit tags.**
- **Unmapped rows are real, and growing:** the mapping covers 392 keys. Rows
  created after the snapshot are untagged by construction. At the first live
  run: 2 unmapped (`waste-nitro-wave-dispatcher-2026-10-28`, created
  2026-10-28 09:56:57Z; `waste-heartbeat-2026-10-28`, 09:42:01Z). At the final
  run: 5 unmapped — the same 2 plus 3 new queued rows created 2026-10-28
  17:53:10–11Z (`one-scheduler-two-faces`, `link-law-duplicate-collapse`,
  `needs-shawn-hands-face`), all with EMPTY criteria arrays. Untagged is a
  snapshot-lag state, not a data error — and the computation counts it
  separately, never silently assigned.

## 2. Computation definition (frozen — do not redesign without new evidence)

**Function:** `compute_front_back_split(rows, tag_mapping=None, area_mapping=None)`
in `~/workspace/system/b1-serve-ready-2026-10-28.py` (new section only;
`serve()` / `build_response()` / `shape_items()` / `compute_per_app()` untouched).
Rows are RAW record rows (`item_key, state, acceptance_criteria, updated_at`).

- **"Done" (criteria-done)** = `acceptance_criteria` is a non-empty list AND every
  element is an object with `done === True` (strict boolean). Anything else —
  no criteria, empty criteria, non-list criteria, any element missing
  `done=True` (including string `"true"` and non-dict elements) — is NOT done.
- **State `done_proven`** is reported separately per bucket (`done_proven` field)
  and must never be conflated with criteria-done. The two definitions differ by
  exactly 9 adjudication rows (see §4).
- **Buckets are disjoint per area:** front / back / both / process / untagged.
  "both" = one row belonging to BOTH face lists. "process" = Resolve's
  definition (governance/verification/media work, honestly neither surface nor
  machinery). Tag values outside {front, back, both, process} — including
  "unspecified" and any unknown string — land in untagged. Untagged is never
  silently assigned.
- **Derived list views (what the face displays):** front_list = front + both;
  back_list = back + both, each with counts AND item_key lists. The views
  overlap by design (both rows appear in both lists: 92 rows project-wide) and
  must never be summed back into the total. List totals (257 + 211 = 468)
  exceed the row total (397) by exactly the both count — that is correct, not
  an error.
- **Area:** `work_items` has no `area_key`, so grouping takes an area mapping
  `{item_key: area}` as input; any key absent from it (or no mapping supplied)
  lands in "unplaced" — never a guessed area. When the FILL pipeline lands a
  canonical area mapping, the same function distributes the split with no code
  change. The per-area shape is complete; the area values are honestly
  unplaced until that mapping lands.
- **Dedup:** first row seen per item_key wins; callers must pre-order rows
  `updated_at DESC NULLS LAST` (same precondition as `shape_items`).
- **Invariants (asserted by tests):** per-area buckets sum = area total; sum
  over areas = unique; done_proven summed over buckets = project done_proven.
- **Companions:** `is_criteria_done(row)`; `load_tag_mapping(path)` (missing
  file → `{}`, malformed/non-object → raises; values NOT validated at load —
  unknown values fall into untagged at compute time);
  `fetch_live_rows_with_criteria()` (read-only, paged, cascade 50 → 25 → 10,
  limit-10 up to 3 attempts with 2s pacing).
- **CLI:** `python3 workspace/system/b1-serve-ready-2026-10-28.py --tag-mapping
  <file> [--area-mapping <file>]` prints `TAG_MAPPING:` + `FRONT_BACK:` JSON,
  then normal serve output; on fetch failure it prints `FRONT_BACK_ERROR:` and
  exits 1 (never a snapshot).
- **Serve-time wiring note:** `serve()` / `build_response()` were deliberately
  NOT changed (their fetch does not select `acceptance_criteria` and their
  envelope shape is frozen for the existing tests). Wiring the split into the
  merged worker's `/pi/api/items` response is Nitro's landing-lane step,
  reusing `compute_front_back_split` + a criteria-inclusive fetch, behind the
  landing gate (A11/C5/publisher/pulse/cure + Nitro re-check + consensus +
  Shawn cold-open tap). Until then this is workspace-proven only.

## 3. Tests — full output

**Test file:** `~/workspace/system/test-front-back-split-2026-10-28.py`
(SHA256 `db7e37415aa0699d83fb2ed3b75018a4432d2ca4d25786f6f983aa13d0b434d9`).
Run from `~` as `python3 workspace/system/test-front-back-split-2026-10-28.py`;
exit 0 only if every check passes.

**Final run (session `proc_09465981997e`, ~27 min): ALL_PASS: True.**

Fixtures 14/14 PASS:
- S1 buckets partition (front=4 back=1 both=1 process=1 untagged=7 total=14);
  S1b reconciliation block all true.
- S2 done rule (including: an untagged row with all-done criteria still counts
  as done — the done rule reads criteria only, never the tag); S2b strict-True
  matrix (missing done key, empty list, missing criteria, non-list criteria,
  non-dict element, string "true" all NOT done).
- S3 state-vs-criteria split (done_proven=2, front.dp=1); S4 dedup first-wins;
  S5 unknown/`unspecified`/missing tag → untagged (7 rows); S6 area buckets
  (Area A=2, Area B=2, unplaced=10); S6b area sums; S7 list views
  (front_list=5, back_list=2, overlap exactly the both row); S8a/b/c loader
  (drop-in, missing→{}, malformed→raises); S9 empty input totals=0.

Live checks, final run — all PASS:
- L1 live-read-no-duplicates raw=397 unique=397.
- L2 mapping-file-counts keys=392 counts={back: 119, process: 16, both: 92,
  front: 165}.
- L3 key-sets mapped_live=392 unmapped=5 (the 5 keys listed in §1).
- L4 live-buckets expected={front: 165, back: 119, both: 92, process: 16,
  untagged: 5} got=(165,119,92,16,5) total=397 dp=24.
- L4b live-recon-block recon={unique: 397, buckets_sum_equals_unique: True,
  done_proven_sum_equals_unique_done_proven: True, per_area_totals_sum: 397,
  per_area_sums_match: True}.
- L5 bucket-done-bounded untagged.done=0, untagged.items=[the 5 keys].
- L6 live-area-unplaced-only areas=['unplaced'].
- L7 cli-tag-mapping-matches attempts=2 rc=0 fb_total=397 fresh_unique=397.
  (First CLI attempt yielded no FRONT_BACK line in a flaky transport window;
  the read-only second attempt succeeded. The flakiness is a transport
  property, not a computation property — see history below.)

**History (reported, not hidden):**
- Earlier run: L7 failed twice — first a fixed page-40 read failed on chunked
  transport (fixed in the test by a page-size cascade 40 → 25 → 10 + 1s
  pacing), then a diagnosis run progressed 18 pages at limit 10 (offsets 0–170)
  and failed at offset=180 with "no JSON block … after second attempt" and
  EMPTY stdout (pure transport failure in a bad window, not a data pathology).
  Fixes: module `_read_criteria_page` limit-10 attempts 2 → 3 (2s pacing),
  cascade 50 → 25 → 10 unchanged, exhaustion still raises loudly; test L7 gets
  one deliberate second CLI run if the first yields no FRONT_BACK line
  (read-only, no side effects).
- Baseline drift 394 → 397 mid-task (3 new rows, §1) first surfaced as
  "failures" of hardcoded-baseline assertions. The test was reworked to be
  baseline-agnostic: expected buckets recomputed independently from mapping +
  live key set; baselines REPORTED with read time, never asserted fixed. The
  computation was never wrong; the assertions were. This is why the live
  checks now survive record growth.
- Transport flakiness is systemic to the `sb-api` chunked-read path in bad
  windows (also seen in the regression runs, §5). Readers retry and fail
  loudly; the CLI/test retry once; `serve()` fails closed with 503 by design
  (never a stale snapshot).

## 4. Reconciliation numbers (final run — fresh read inside that run)

- Baseline: raw=397, unique=397, done_proven=24. (Prior baseline 394/24; the
  +3 is the live seat work in §1, all queued, all empty-criteria.)
- Buckets: front 165 total / 4 criteria-done; back 119 / 4; both 92 / 6;
  process 16 / 1; untagged 5 / 0; **total 397; criteria-done total 15;
  done_proven total 24.**
- Derived list views: front_list 257 total / 10 criteria-done (165+92, 4+6);
  back_list 211 / 10 (119+92, 4+6). 257 + 211 = 468 = 397 + 92 (both) — correct.
- Overlap (live SQL, strict jsonb `true`, independent of the Python rule): of
  the 24 done_proven rows, exactly 15 are fully criteria-done; the 9 that are
  not are exactly the 9 adjudication rows — `gap-a1`, `gap-a11`, `gap-a5`,
  `gap-c3`, `gap-d10`, `gap-d11`, `gap-d12`, `gap-d13`, `gap-d17`. Since total
  criteria-done is also 15, criteria-done (15) is a subset of done_proven (24);
  the SQL strict-`true` check and the Python strict-`True` rule agree at 15.
- Per-bucket done_proven, DERIVED (tag mapping joined to the 24 done_proven
  keys from the live SQL — stated as derived, not a direct read): front 7,
  back 8, both 7, process 2, untagged 0 (sums to 24). Therefore front_list
  done_proven = 14 (7+7) and back_list done_proven = 15 (8+7).
- No double count, no dropped rows: buckets sum = unique (397); done_proven
  sum = 24; per-area sums match; per-area keys = {"unplaced"} only (no area
  mapping yet — see §6).

## 5. Regression — existing module test (no regression attributable to this task)

File `~/workspace/system/test-b1-serve-ready-2026-10-28.py` (NOT modified).
- Run 1: fixtures F1–F6b, P1–P6 ALL PASS; L0 serve-200 FAILED with 503
  ("no JSON block in page offset=335 after second attempt") — the same
  transport family, in the untouched `serve()` fetch path through the core
  reader. It failed closed by design (503, never a stale snapshot).
- Run 2: P1–P6 PASS; **L0 serve-200 PASSED (status=200)** — confirming run 1
  was transient transport, not a regression. The run then crashed in the
  harness's OWN independent live read (not the module) with the same
  chunked-transport error after 3 attempts. That crash proves nothing about
  the module; it re-proves the transport window was bad at that moment.
- The extension touched no existing function (new section + CLI flags only);
  module SHA256 `0ed914ca56721556ba0262289a3b71f479c542d455efedb2c63b5e59a60aef33`
  (after the retry-budget fix); core module NOT MODIFIED, SHA256
  `496416cce7728d4efe4c3c864283b1a32b54837135c8433b2c21c4cd7eda6722`
  before, during, and after all work.
- A third run was deliberately NOT chased: it would only re-prove transport
  flakiness. The verdict above is the honest one.

## 6. Exactly what the face needs to display (inputs for Nitro's face beat)

Per area (once the area mapping lands; today the only area is "unplaced"):
- **front_list {done, total, items}** — front + both rows, criteria-done count,
  item_key list. Project-wide today: done=10, total=257.
- **back_list {done, total, items}** — back + both rows. Project-wide today:
  done=10, total=211.
- **process {done, total, items}** — neither surface nor machinery, shown as its
  own honest third group, never folded into front or back. Today: done=1,
  total=16.
- **untagged {count, items}** — rows outside the mapping snapshot, counted
  separately, never silently assigned. Today: count=5, items=[the 5 keys in §1].
  The face should show this count honestly (e.g. "5 awaiting tags") rather
  than hiding it.
- **Percentages are criteria-done ÷ total per list** — front_list 10/257 =
  3.9%, back_list 10/211 = 4.7% (project-wide today). These must NOT be
  confused with the state-based "M of N proven done" (front_list done_proven
  14/257 = 5.4%, back_list 15/211 = 7.1%) — different definitions, different
  numbers; if both appear, label them differently.
- **Both rows appear in both lists by design** (92 rows project-wide); the
  face must never sum the two list totals into a row total.
- The function returns all of the above per area plus project totals plus the
  reconciliation block; the face consumes `per_area[area].front_list`,
  `.back_list`, `.process`, `.untagged` directly.

## 7. Still open (not this task, not hidden)

1. Canonical area mapping from the FILL pipeline — until it lands, per-area
   output is honestly "unplaced".
2. Merged-worker wiring of the split into `/pi/api/items` (Nitro's landing
   lane, behind the landing gate: A11/C5/publisher/pulse/cure + Nitro re-check
   + consensus + Shawn cold-open tap).
3. Phone rendering check of the split display (unverified) + link-target
   activation checks.
4. Mapping refresh when Resolve refreshes the dataset (re-extract, never
   hand-edit; the 5 untagged rows are the current lag).
5. Minor doc nit: the module docstring's importable list does not yet name the
   new functions (the section header documents them fully). Left untouched
   deliberately so the delivered module is exactly the tested one.
6. Transport flakiness in the `sb-api` chunked-read path: retries + fail-loud
   / fail-closed behavior are the current mitigation; a root fix to the
   reader belongs to whoever owns that path, not this task.
