# Applicability Consumer Contract V1 — what retrieval must read, how it must rank

**Owner:** Naya Beta (KNOW) · **Consumer:** Naya Theta (Retrieval)
**Status:** reviewed-ready for Theta's wiring · **Date:** 2026-10-12
**Producer:** `tools/applicability.py` v2.0 (`produce()` / `stamp_entry()`)
**Reference implementation:** `tools/applicability.py::rank_adjust()` + `apply_ranking()` — port one-to-one.

---

## 1. The problem in one sentence

Retrieval currently returns what *matches*. This contract makes it return what *applies*: a match that is expired, out of scope for the caller's context, or replaced by a newer record must demote or resolve — never win silently.

## 2. What retrieval must READ (the six fields)

Every knowledge record carries `applicability` (schema v2.0, validated by
`tools/applicability.py::validate()`). Retrieval reads all six fields:

| Field | Type | Meaning for retrieval |
|---|---|---|
| `areas` | list of 12 area codes | *where it applies*: LEARN, KNOW, ACT, LAW, VERIFY, BLOCKS, DECISION, RETRIEVAL, SUCCESSOR, TEAM, INFRA, HUMAN_VALUE |
| `task_contexts` | list of domain tags | *where it applies*: cold-retrieve, briefing, scorecard, merge-gate, dispatch, capture, verify, trial, successor-handoff, human-value |
| `law_refs` | list of refs | informational; retrieval may surface, never filters on these alone |
| `freshness` | {valid_from, valid_until\|null, ttl_days, assessed_at} | *when it applies*. `valid_until=null` = timeless: applicability ends only via supersession, never by the clock |
| `supersession` | {superseded_by\|null, supersedes:[...]} | *what replaces it*. If `superseded_by` is set, this record is not current |
| `confidence` / `needs_review` / `source` | float / bool / str | *how much to trust the tag itself*: heuristic tags below 0.5 confidence, or `needs_review=true`, demote |

### Mapping onto the existing read surfaces (no new tables)

- **Python registry path** (`tools/smart_note_v2.py`): read `entry["applicability"]` directly. If absent, `produce()` computes it deterministically (memoized in `filter_entries`); treat absent as `needs_review` (fail closed), never as fresh.
- **TypeScript block path** (`supabase/functions/nayanet-intelligence-retrieve/`): read the columns already selected by `index.ts`:
  - `applicable_scope` ↔ `areas` + `task_contexts`
  - `superseded_by_block_id` ↔ `supersession.superseded_by`
  - `updated_at` + `provenance` ↔ `freshness.valid_from` (until a `valid_until` column is added; the DB-side stamping of freshness is **THETA-NEXT-2** below)

## 3. The ranking rule (exact — port verbatim)

For each candidate record, retrieval computes:

```
final_score = base_match_score × multiplier
```

`multiplier` and the `servable` flag come from this rule, in this order:

1. **Supersession (hard).** If `supersession.superseded_by` is set:
   `servable=false`, `multiplier=0.0`. The record must NOT be served as current
   knowledge. Resolve to the lineage head instead (step 5).
2. **Expired.** If `freshness.valid_until` is set and `valid_until < now`:
   `multiplier ×= 0.1`. Stale knowledge demotes hard — the old answer is
   usually the wrong answer.
3. **Out of scope.** If the caller named areas and/or contexts and the record
   matches *none* of them: `multiplier ×= 0.25`. Retrieval still surfaces it
   (visibility beats silence), but it cannot outrank in-scope answers.
4. **Unreviewed / low confidence.** If `needs_review`: `multiplier ×= 0.5`.
   Else if `confidence < 0.5`: `multiplier ×= 0.8`.
5. **Missing metadata is fail-closed.** No `applicability` tag → treat as
   `needs_review` (`multiplier ×= 0.5`). Unknown applicability is never
   treated as fresh, in-scope, or current.

Sort by `final_score` descending. Keep the `reasons` list per record (the
reference implementation emits strings like `expired:2026-11-20`,
`out_of_scope`, `superseded_by:IB-...`) and surface them in the score
breakdown — retrieval that cannot explain a demotion is retrieval that cannot
be debugged.

## 4. Supersession resolution (exact)

- Follow `superseded_by` links, at most **3 hops**, with a visited-set
  cycle guard. Stop early on a missing head; keep the last resolvable record.
- Aggregate at the head: the head inherits the **best base score** among its
  lineage members, carries `via_lineage: [member ids]`, and is ranked once.
  The members are never ranked separately. (This is what `expandBlock`'s
  lineage step already does at the block level — the contract extends the
  same discipline to applicability-ranked candidates.)
- A chain that points at a non-servable head is a data bug: resolve to the
  deepest servable ancestor and emit reason `supersession_head_unservable`.

## 5. What this does NOT change

- Base match scoring is untouched: applicability multiplies, never replaces.
- No new authority is created: a demoted record is still visible (multiplier
  0.1/0.25), just ranked below what applies. Only supersession removes a
  record from "current" — and supersession links are human/lane-approved data
  (`tools/applicability_supersession.json`), not derived.
- Default retrieval behavior with no caller scope is unchanged: rules 2 and 4
  still apply (stale and unreviewed demote), rule 3 is a no-op.

## 6. Remaining retrieval-side wiring (Theta's next tasks, named)

- **THETA-NEXT-1 — port `rank_adjust()` into `retrieve.ts`.** The Python
  reference is the spec; the port must produce identical multipliers on the
  contract test vectors in `tests/test_applicability_v2.py`
  (`TestRankingReference`). Retrieval is Theta's area — the KNOW side does
  not touch her files.
- **THETA-NEXT-2 — stamp freshness into the block read surface.** Today
  `index.ts` reads `updated_at`; the contract needs `valid_until` per block.
  Options: a migration adding the column, or deriving it from
  `provenance.applicability.freshness`. Theta's call.
- **THETA-NEXT-3 — wire caller scope through.** The Python side already
  accepts `areas`/`task_contexts` (`smart_note_v2.retrieve(..., areas=...,
  task_contexts=...)`); the TS entry point needs the equivalent parameters
  so rule 3 (out-of-scope demotion) can fire.
- **THETA-NEXT-4 — supersession registry source.** The JSON registry is the
  interim source of truth; the durable home is the block lineage table.
  Until then, the retrieve function reads the JSON (checked into the repo,
  auditable in the owning commit).

## 7. Verification (how Theta proves the port)

1. Run `tests/test_applicability_v2.py` — the contract vectors must hold in
   the TS port with identical multipliers (0.1 / 0.25 / 0.5 / 0.8 / 0.0).
2. A superseded record must resolve to its head with `via_lineage` populated,
   and the superseded record must never appear as a current answer.
3. An expired record (`valid_until` in the past) must rank below an
   otherwise-identical fresh record.
4. A record with no applicability metadata must demote (fail closed), never
   rank as fresh.

## 8. What this does NOT claim

- It does not claim the heuristic tags are correct — that is what the
  confidence ladder and `needs_review` are for, and the contract demotes
  accordingly.
- It does not claim the supersession registry is complete — it is empty
  today by design; the first links land as the review lane approves them.
- It does not change what retrieval is authorized to serve: the edge-level
  V2 gates (status, temporal, consent, applicability) from the canonical
  `connect_selector` still apply first. This contract ranks what those gates
  admit.
