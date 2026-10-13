# Smart Connect — Open Doors (AI-language spec)

*Exact values, procedures, constraints. Same truth as the `.human.md` telling; this file is what builders implement against.*

## SOURCES OF TRUTH

- Human telling: `BRAIN/10-INTERFACES/SMART-CONNECT-OPEN-DOORS.human.md`
- Machine schema: `BRAIN/10-INTERFACES/SMART-CONNECT-OPEN-DOORS.machine.json`
- Reference implementation: `tools/smart_connect.py`
- Proof gate: `tests/test_smart_connect_open_doors.py`
- Door declarations (upstream, do NOT re-specify): `BRAIN/10-INTERFACES/0001-SMART-DOOR-CONTRACT-V1.{md,json}`, `0002-SMART-DOOR-REGISTRY-V1.json`
- Prior art (different substance): app-era `nayanet_smart_connect_participation` table + `nayanet_smart_connect` RPC — account/consent layer, untouched.

## DATA RECORDS (exact fields)

```
door:        {door_id, name, protocol, open: bool, closed_reason?}
connection:  {connection_id, name, door_id, opened_at, terms_version: "L253-v1",
              stats: {lessons, compounds}}
lesson:      {lesson_id, connection_id, text, essence: [tokens], captured_at,
              status: INTAKE|MERGED|ELEVATED, duplicate: bool, door_id, canonical_id?}
compound:    {compound_id, kind: MERGE|ELEVATE, lesson_ids: [..], canonical_id,
              resulting_artifact, cycle, at}
cycle:       {cycle_id: "cyc-NNN", at, intake_processed, merged, elevated,
              compounds_total, flags: [{kind, lesson_id, detail}]}
```

- `lesson_id` = `les-` + sha256(`connection_id | essence-tokens`)[:8] (content-addressed per connection).
- `compound_id` = `cmp-` + sha256(`kind | lesson_ids | at`)[:8].
- `resulting_artifact`: MERGE → `living-note:<canonical_lesson_id>`; ELEVATE → `law-proposal:<canonical_lesson_id>` (a proposal to the approval system, NOT canon).

## CONSTANTS (tuned synthetically — calibration open)

- `MERGE_SIMILARITY = 0.7` — Jaccard over normalized token sets (`_essence`: lowercase alphanumeric tokens, deduped, sorted). Two INTAKE lessons merge iff Jaccard(essence_a, essence_b) >= 0.7. **TODO: calibrate against the live registry corpus before production wiring.**
- `ELEVATE_MIN_CLUSTER = 2` — a merged canonical group of ≥2 lessons proposes an ELEVATE compound, once per canonical id.

## PROCEDURES

**register_door(door_id, name, protocol):** declares (or refreshes the declaration of) a door. A declaration refresh NEVER reopens a harm-closed door and never erases `closed_reason` — reopening is a recorded decision taken only via **reopen_door(door_id, reason)**, the sole reopen path.

**register_connection(name, door_id):** never refuses (G1). If `door_id` unknown or closed → reroute to the first open declared door. If none open → `ValueError("no open doors")` — an all-closed registry is a recorded-door-closure defect, never silently permitted.

**append_lesson(connection_id, text, door_id=None):** unknown connection → `ValueError`. Instant: status INTAKE, `duplicate: False`, no gate (G2, Law 4). Re-submission of identical text by the same connection resolves to the existing lesson id and is marked `duplicate: true`; it does NOT increment the connection's lesson count and does NOT create a second lesson record (polarity). The seam name for this call is `lesson_intake.append` (B-44's intake UX calls it over the seam; the module method is `append_lesson`).

**run_cycle():** processes all INTAKE lessons.
1. MERGE: greedy cluster on Jaccard ≥ 0.7. Clusters of ≥2 → all members MERGED with `canonical_id` = earliest-captured member; one MERGE compound recorded, per-connection compound stats incremented. Lone lessons stay INTAKE — never faked MERGED (polarity).
2. ELEVATE: merged lessons grouped by `canonical_id`. `canonical_id` is resolved against the lesson registry and must be MERGED or ELEVATED — a dangling canonical is flagged (`dangling_canonical_id`) and skipped, never minted. Groups of ≥ `ELEVATE_MIN_CLUSTER` with no prior ELEVATE compound for that canonical id → one ELEVATE compound recorded, per-connection compound stats incremented (so `compound_count` always agrees with the compounds list — Law 6); members become ELEVATED.
3. Fail-closed: a MERGED lesson lacking `canonical_id` (corrupted state) is skipped and recorded in `cycle.flags` (`{kind: "missing_canonical_id", lesson_id, detail}`); the cycle completes — no KeyError, no fake compound.

**feedback_for(connection_id):** unknown connection → `ValueError`. Returns `{connection_id, lessons: [ids], compounds: [ids sorted], compound_count, cycles_run}` (G4).

## FAIL-CLOSED SURFACE

| Input | Behavior |
|---|---|
| unknown `connection_id` on append/feedback | `ValueError` (not KeyError, not silent create) |
| chosen door unknown/closed | reroute to first open door; none open → `ValueError` |
| lesson missing `canonical_id` at ELEVATE stage | skip + `cycle.flags` entry; cycle completes |
| lesson with dangling `canonical_id` at ELEVATE stage (points at nothing, or at a non-canonical) | skip + `dangling_canonical_id` in `cycle.flags`; cycle completes; zero compounds cite it |
| duplicate submission | one record, `duplicate: true`, no stat inflation |
| contributor with zero contributions | compound_count 0, compounds [], no leak into others' compounds |

## GUARANTEE ↔ PROOF-CASE MAP

- G1 open doors → `test_g1_open_doors` (registration returns conn id on declared door; reroute from closed door), `test_closed_door_survives_reregister` (re-register never reopens a harm-closed door), `test_reopen_door_explicit` (`reopen_door()` is the only, recorded reopen path)
- G2 instant capture → `test_g2_instant_capture`
- G3 no free compound → `test_g3_compound_recorded` + `test_g3_negative_no_free_compound` + `test_compound_count_matches_compounds` (`compound_count` always agrees with the compounds list)
- G4 visible in one cycle → `test_g4_visible_in_one_cycle`
- Polarity (dedupe, no fake merge, no double compound) → `test_polarity_dedupe_no_double_compound`, `test_polarity_lesson_survives`, `test_duplicate_flag_initialized` (first-append record carries `duplicate: false`)
- Corrupted-state fail-closed → `test_fail_closed_corrupted_merge` (the Builder hardening; regression-proven against Host's wave-12 version), `test_fail_closed_dangling_canonical` (round-2 hardening: dangling canonical never mints a compound)
- Unknown-connection fail-closed → `test_fail_closed_unknown_connection`

## CONSTRAINTS

1. Synthetic reference only: in-memory state + local JSONL/JSON evidence. Zero production writes, zero DB, zero dashboard actions.
2. Never re-specify door contracts; door declarations are upstream (Smart Door contract/registry).
3. Never touch B-44's intake UX; the seam contract above is the only coupling.
4. ELEVATE proposes; canonization belongs to the automated approval gates (G6).
5. The merge hold (#2459) is lifted, but this PR stays draft for Naya 4 review; the merge lane owns any merge — no self-merge.
