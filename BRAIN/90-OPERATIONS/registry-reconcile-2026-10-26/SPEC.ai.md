# Registry Reconcile — SPEC.ai (exact procedure for the cure lane)

Basis: live main tip `57866113ca22c48c1580db8489ca8e35b88d6682`. All counts
below were measured at that tip (raw bytes via contents/raw at the ref;
checker and audit run in a depth-1 checkout of the exact SHA; page hashes
independently re-verified from raw.githubusercontent bytes, 12/12 MATCH,
0 mismatch). PI: `resolve-registry-reconcile-sn0594`. Governing law: L659
(one reconciled artifact), L663 (worktree discipline), L662 (served-title
proof), L670 (verifier = distinct seat/login).

## 0. Measured state at basis tip

| Surface | Value |
|---|---|
| `.naya/memory/smart-notes/index.json` | 879,903 bytes; sha256 `4778ec49bafdcdfa…906ae0e` |
| entries | 728 (700 retrieval-eligible, 28 inactive tombstones) |
| `corpus_manifest_hash` | stored `ef5a71d637e5fd8c8c0781add0e55b644f9700d08b5155660b99f482d41250b2` == recomputed via `_corpus_manifest_hash` → **CONSISTENT** |
| `sequence_policy.next_sequence` | 1870 |
| serialization | `json.dumps(doc, indent=2, ensure_ascii=False) + "\n"` — byte-identical round-trip PROVEN (this is the fixer's `_atomic_write_json(indent=2)` form) |
| captures on disk | 719 · published `.md` pages 722 · door-scope canonical pages 701 |
| door check full mode | exit 1 · **1 defect** (C1) · 1 twin warning (C4) |
| `audit_registry` | defect_total 50 (see spec.machine.json for per-class) |
| pytest `tests/test_brain_index_freshness.py` | 13/13 at basis |
| live serve | `/s/sn0833` → collider B title · `/s/sn1852` → first-claim A title · `/s/sn0594`,`/s/sn0593` → no `<title>` captured |

## 1. Defect census (classes; full per-entry lists in spec.machine.json)

- **C1 PAGE_HASH_STALE ×1 (the blocking defect).** SN-0594 (entry idx 528,
  IB `IB-SMART-NOTE-20261001-hub-is-intelligence-projection-dup0594`,
  SUPERSEDED tombstone, `page_hash: null` by B-51 design) — but its tombstone
  pointer page still exists on disk:
  `BRAIN/05-MEMORY/SMART-NOTES/2026/10/02/SYSTEM-INTELLIGENCE/HUB-INTELLIGENCE-ARCHITECTURE/INPUT-OUTPUT-PROJECTION-MODEL/SN-0594/IB-SMART-NOTE-20261001-hub-is-intelligence-projection-dup0594.md`,
  sha256 `881b8b91afb2eab04673fa754b738699a45f54fa10bfea04d173f2788e80da29`.
  Page = 24-line pointer (2026-10-04 integrity fix); its embedded
  `canonical_path` is itself stale (names a non-existent SN-0594 path; true
  canonical = SN-0593's page, sha256 `8ad25cbc…f8ff8`, entry hash MATCH).
  Mechanism: `check_pages` is page-driven and lifecycle-blind; entry has
  `content_hash` (capture exists, no HASH_MISMATCH) and `page_hash=None ≠
  sha256(page)` → PAGE_HASH_STALE. Only 1 of 28 tombstones has a page on disk.
- **C2 dual-ACTIVE smart_note_id ×2 ids / 4 entries.** SN-0833: A
  `…sn0833-learn-grow-compound-first-mistake-law` first commit `063456a8c7`
  2026-10-23T02:42:53Z; B `…sn0833-the-only-mistake-is-the-missing-note`
  `66c9e01c4f` 02:43:40Z (+47s). SN-1852: A `…sn1852-the-only-mistake`
  `bc546b0bb2` 02:42:55Z; B `…sn1852-error-becomes-learning` `2e0104160b`
  02:43:38Z (+43s). All 4 page_hashes verified MATCH; all 4 captures exist;
  4 distinct content_hashes (distinct objects). `/s/sn0833` serves B today.
- **C3 duplicate intelligent_block_id ×1.** IB
  `IB-SMART-NOTE-20261001-hub-is-intelligence-projection` held by idx 527
  (SN-0593, ACTIVE) and idx 74 (SN-018, SUPERSEDED tombstone). Hazards:
  `check_pages.entries = {ib: e}` shadowing; `_update_registry_locked`
  replace-by-IB would delete idx 74 on any SN-0593 re-capture.
- **C4 twin projection ×1 (checker TWIN, non-blocking).** SN-01773 IB at two
  paths, divergent bytes: bound A `…/2026/10/21/SYSTEM/governance/SN-01773/…`
  sha256 `290f4125…5b3a7f` == entry page_hash; unbound B
  `…/2026/10/21/SYSTEM-INTELLIGENCE/GOVERNANCE/FINISH-BEFORE-CREATE/SN-01773/…`
  sha256 `6d1abfbf…eac`, 6,385 vs 8,078 chars, 70 diff lines (older rendering).
- **C5 retired tombstones ×28 (NOT defects).** All
  `index_validation=RETIRED_UNVALIDATABLE`, `lifecycle_state=SUPERSEDED`, no
  page_hash; 28/28 carry `superseded_by_capture_id` + `supersession_reason`
  (vanish-guard compliant); 18 shadow a duplicated id (ACTIVE sibling holds
  it), 10 standalone. 12 carry placeholder successors
  (`(successor … not yet ingested)`) — evidence debt, listed in machine twin.
- **C6 numeric-format collision ×1 (record-only).** Number 346 as `SN-0346`
  (ACTIVE, idx 247) and `SN-346` (SUPERSEDED, idx 682). Unique-ids gate is
  path-based; one page path exists → no gate impact.
- **C7 hashless content_hash ×28 entries + 19 unregistered captures
  (DIRECTOR-GATED, out of cure scope).** 22 legacy eligible + 6 tombstone
  entries lack `content_hash` (removed by PR #1401). Coupled: no entry hash
  ⇒ captures cannot hash-reconcile (19 unregistered, incl. SN-9998/SN-9999
  live-fire fixture captures). Drift ratchet pins 28/20, green. Restoration
  is a Human Director decision per `tests/test_smart_note_registry_drift.py`
  docstring. **The cure MUST NOT touch this class.**
- **C8 audit-only orphan pages ×3 groups (out of cure scope).** SN-0842
  founding-portrait (identity lane), legacy `smart-note.md` v7 group,
  `the-naya-tool-set.md`. Not door-scope pages.

## 2. Canonical tooling — what it does and does NOT do

`tools/check_door_obligation.py` (757 lines at basis):
- CHECK full mode: `discover_pages` (IB-*.md under BRAIN/05-MEMORY/SMART-NOTES;
  same-IB multi-path → canonical = fewest path segments, rest = TWIN warnings,
  printed only, never defects) + `check_pages` (per canonical page, entry by
  IB: NO_ENTRY / NO_CAPTURE / HASH_MISMATCH / PAGE_HASH_STALE) +
  `tombstone_class` (git-history ids with no page/capture/entry — needs FULL
  history; a depth-1 clone under-reports it).
- CHECK `--range A..B` (CI contract, `.github/workflows/door-obligation.yml`:
  PR = delta hard-fail; push = delta + non-blocking full scan + guard battery
  pytest): additionally runs `tools/check_smart_note_unique_ids.check` —
  DUPLICATE_PUBLIC_ID fires only for numbers TOUCHED by added/renamed paths.
  Historical collisions (C2, C4) are grandfathered until touched.
- FIX `--fix [--ids] [--with-regen]`: builds capture+entry FROM a page for
  pages missing them (`build_capture`/`build_entry`, hashes via snv2 —
  `_canonical_content_hash`, `_page_file_hash`); recomputes manifest via
  `snv2._corpus_manifest_hash(entries)`; bumps `next_sequence`; writes the
  registry with `_atomic_write_json(indent=2)`. Refusals by design: pageless
  ids (LAW lane), content_hash conflicts (human lane).
- **The fixer does NOT:** re-stamp `page_hash` on pre-existing entries (its
  own cure text: "the fixer does this only for entries it generated") —
  therefore **C1 cannot be cured by `--fix`**; delete pages; renumber ids;
  re-key IBs; touch SUPERSEDED entries; resolve twins. C1/C3/C4 cures are
  file/entry surgery + the canonical seal regen in §3, nothing else.

`tools/smart_note_v2.py`:
- `_corpus_manifest_hash(entries)` = sha256 of
  `json.dumps(entries, sort_keys=True, separators=(",",":"), ensure_ascii=False)`.
  The ONLY permitted way to recompute the seal in the cure: import and call.
- `_page_file_hash(path)` = sha256 of raw page bytes. Single hash authority.
- `_validate_index_against_corpus`: eligible = lifecycle NOT in
  {SUPERSEDED, ARCHIVED, REVOKED, RETIRED}; checks shape/containment/existence,
  duplicate IB or projection_path among eligible, page_hash present+matching
  among eligible, manifest over the FULL list. It NEVER checks smart_note_id
  uniqueness (C2 passes it today) and skips tombstones entirely.
- `_assert_smart_note_id_available`: writer-side only — blocks NEW claims on
  an owned id; existing collisions block nothing until claimed again.
- `_update_registry_locked`: replaces entries by IB, re-sorts entries by
  `(smart_note_id, intelligent_block_id)`, recomputes manifest — the cure's
  edited file must match this canonical ordering.
- `audit_registry`: whole-surface audit; note its `duplicate_smart_note_ids`
  class actually groups by **content_hash** and therefore reports 0 for C2 —
  no existing tool enumerates duplicate smart_note_id strings. This census
  gap is itself a finding (the cure's step 1 adds the count as a script, not
  a new tool).

## 3. Per-entry dispositions

| Entry | Disposition | Rule / evidence |
|---|---|---|
| SN-0594 page (C1) | **DELETE file** (primary). Entry + capture stay. Fallback: set entry `projection_path` + `page_hash=881b8b91…` (bind-the-tombstone). | Anomaly vs 27 page-less tombstone siblings; pointer is itself stale; vanish guard satisfied via entry+capture. Decider: cure lane; fallback if lane refuses deletions. |
| SN-0833 B (C2) | **RENUMBER** by its owning lane to allocator-issued id (expected SN-1870 at spec time — allocator decides at run time). Re-file capture with explicit new id + renumber provenance (old id, commits `063456a8c7`/`66c9e01c4f`); render new projection via snv2; DELETE old B page same commit; ADD tombstone entry (IB `…sn0833-the-only-mistake-is-the-missing-note` + `-dup0833` suffix — dup0594 precedent), SUPERSEDED, `superseded_by_capture_id` = new capture id, reason = collision renumber. | First-claim stands (A 02:42:53Z). Renumber is the colliding lane's act, never the spec's (SN-1863→SN-1864 precedent). |
| SN-1852 B (C2) | **RENUMBER**, identical pattern (expected SN-1871). | First-claim A 02:42:55Z vs B 02:43:38Z. |
| SN-0833 A, SN-1852 A | KEEP id, untouched bytes. | First claims. Post-cure `/s/sn0833` must serve A. |
| SN-018 tombstone idx 74 (C3) | **RE-KEY** `intelligent_block_id` → `IB-SMART-NOTE-20261001-hub-is-intelligence-projection-dup0018`. No other field changes. | dup0594 suffix precedent; ends IB shadowing. |
| SN-0593 idx 527 (C3) | Untouched. | Live holder of the IB. |
| SN-01773 twin B page (C4) | **DELETE file**. IB keeps entry + capture + canonical page A. | Same block, one canonical home (checker rule); A is hash-bound. |
| 28 tombstones (C5) | KEEP verbatim (except idx 74 IB re-key). | Guards skip by design; provenance record. |
| C6, C7, C8 | NO ACTION in this artifact. | C6 board question; C7 Director-gated; C8 other lanes. |

New-number discipline: numbers are allocated INSIDE `registry_transaction`
by `_allocate_from_registry`/explicit-claim at execution; the landed
artifact records the numbers actually issued. If 1870/1871 are taken by the
time the cure runs, the allocator's next free numbers are correct by
construction — never re-aim the spec.

## 4. Ordered procedure (single landing, L659)

0. **Preconditions.** PI item claimed by cure lane; verifier (distinct seat,
   distinct login per L670) named BEFORE work starts. Full-history checkout
   (checker `tombstone_class` and the vanish guard read `git log`; depth-1
   voids both). Worktree per L663: fresh, or verified-clean
   (status empty + HEAD == live tip re-anchored via `GET /git/refs/heads/main`
   immediately before starting).
1. **Freeze the census in the worktree.** Run: full door check `--json`,
   `audit_registry()`, freshness pytest. Counts must equal §0 baselines;
   any drift = stop, re-measure, amend the spec — do not proceed on a stale
   census. Also run the string-level duplicate census (no tool exists):
   count `smart_note_id` strings and IB strings over entries; expect
   dup ids {20 ids: 18 tombstone-shadowed + SN-0833 + SN-1852}, dup IB ×1.
2. **Renumber preparations (colliding lanes).** For each B note: new capture
   authored by its lane (same intelligence; `source` records renumber
   provenance incl. both commit ids); reserve the new id via
   `reserve_smart_note_id` inside the transaction at landing time (step 5),
   not before.
3. **File deletions** (in the landing commit, step 5): SN-0594 tombstone
   page; SN-01773 twin B page; old SN-0833 B page; old SN-1852 B page.
   (B pages are deleted only in the same commit that lands their renumbered
   successors — no window where the intelligence exists at neither address.
   The vanish guard evaluates the landed tree, where each B block persists
   under its new id + tombstone entry.)
4. **Registry surgery** — a single script, run once, that: loads index.json;
   (a) re-keys idx-74's IB (C3); (b) appends the two renumber tombstone
   entries (C2); (c) leaves every other entry byte-identical — PROVE by
   field-level diff of old vs new entry lists: only the enumerated entries
   differ; (d) re-sorts entries by `(smart_note_id, intelligent_block_id)`
   (the writer's canonical order); (e) recomputes `corpus_manifest_hash` by
   importing `tools/smart_note_v2._corpus_manifest_hash` (never a local
   reimplementation in the landed path); (f) writes via the fixer's form —
   `json.dumps(doc, indent=2, ensure_ascii=False) + "\n"`.
   **FORBIDDEN:** any other `json.dump` settings (indent=1 or
   ensure_ascii=True produce a ~47KB phantom diff — measured); hand-editing
   the manifest hex; touching C7 entries.
   The renumbered B entries themselves are written by the canonical door
   flow (step 5 executes capture + `update_registry`, which sets their
   `page_hash` from the rendered pages and the manifest again) — order:
   surgery script runs FIRST on a copy, then door flow for the two new
   notes, then deletions staged, then ONE commit. If the door flow's own
   manifest recompute and the surgery script's disagree, stop — the door
   flow is the authority.
5. **One-commit landing.** All of: 4 file deletions, 2 new captures, 2 new
   projection pages, edited index.json, plus brain-index regen output from
   `tools/regenerate_brain_index.py` (set `refs/remotes/origin/main` to the
   live tip in the worktree first — regen basis = merge-base; stale
   origin/main writes a lagging basis). Push via the door (Git Data API:
   blobs→tree→commit→ref; re-read the main ref INSIDE the push script and
   abort if it moved; app-token PATCH for `refs/heads/main`; verify
   ref == commit after).
6. **Pre-push battery in the worktree** (must ALL pass on the exact bytes
   being landed — §5). Only then push.

## 5. Acceptance battery (cure lane pre-push; distinct seat re-runs at the landed head)

1. `python3 tools/check_door_obligation.py --json` → exit 0; defects 0;
   twins 0; tombstones 0 new (SN-0594 remains registered → never enters the
   tombstone class).
2. Manifest: recompute `_corpus_manifest_hash(entries)` from landed bytes ==
   stored value (CONSISTENT).
3. `smart_note_v2._validate_index_against_corpus(registry)` → no SystemExit.
4. `smart_note_v2.audit_registry()` → every class ≤ §0 baseline
   (entries_without_hash stays 28, captures_unregistered stays 19 — C7 is
   out of scope and must be UNCHANGED, not silently "improved").
5. Pytest: `tests/test_brain_index_freshness.py` 13/13 ·
   `tests/test_smart_note_registry_drift.py` pass (ratchet ≤; no pin edits
   needed — no audit class shrinks) ·
   `tests/test_ratified_intelligence_cannot_vanish.py` pass ·
   `tests/test_door_obligation.py` pass.
6. Entry-once assertions: each `smart_note_id` string held by exactly ONE
   ACTIVE entry (28 ids remain intentionally dual with their tombstones —
   assert instead: exactly one non-SUPERSEDED holder per id); every
   `intelligent_block_id` unique across all entries.
7. Delta self-check: `check_door_obligation.py --range <parent>..<cure>`
   exit 0 (the cure's own CI contract; added paths carry only new ids).
8. Post-land live proof (L662), after the hub picks up the new tip:
   `/s/sn0833` title == "Learn, Grow, Compound — The First-Mistake Law";
   `/s/sn1852` title unchanged (A); `/s/<new id>` titles == the two
   renumbered notes; `/s/sn0594` does NOT serve SN-0593's note content;
   `/s/sn01773` serves the note from canonical A.
9. Distinct-seat sign-off recorded against the exact landed SHA (L659/L670).
   A same-login review is a draft, not the verdict.

## 6. Rollback

The cure is one commit with one parent. Revert path: build a restore commit
from the parent tree for exactly the touched paths (index.json, the 4
deleted pages restored, the 2 new captures/pages + 2 tombstone entries
removed — i.e., `git revert` semantics executed via the same door mechanics,
never a force-push). Post-restore battery must show the §0 baseline EXACTLY
(1 door defect, manifest `ef5a71d6…`, freshness 13/13) — landing anywhere
else means the rollback itself drifted; stop and escalate. No production,
database, or serving state is involved; the hub re-serves from the restored
tip on its normal cycle.

## 7. Ambiguities the spec does NOT decide (route to board / Director)

1. **Sub-minute first-claim (C2).** Both margins (47s, 43s) fall inside one
   landing wave — concurrent claims, not sequential theft. The spec applies
   first-claim-stands, but if the board prefers the served note (B) to keep
   SN-0833, swap A/B roles in §3 — procedure identical. Named question, not
   a silent choice.
2. **C1 fallback choice** (delete page vs bind entry) — cure lane decides;
   spec recommends delete (consistency + the pointer is stale), bind is
   acceptable and still fully green.
3. **C7 content-hash restoration semantics** — Director decision (PR #1401
   history; drift-test docstring). Includes whether SN-9998/SN-9999 fixture
   captures get a ratified test-id carve-out (LAW lane, per the checker's
   tombstone doctrine).
4. **C6 SN-346/SN-0346** — naming hygiene question for the board; any cure
   would renumber either a live note or history, both disproportionate to a
   zero-gate-impact ambiguity.
5. **12 placeholder successors (C5)** — whether to backfill real successor
   capture ids for the `(successor … not yet ingested)` tombstones is a
   provenance-repair project of its own; listed per-entry in
   spec.machine.json (`placeholder_successor: true`).

## 8. Evidence index

Raw artifacts beside this spec (`raw/`): `index.json` (tip bytes),
`check_door_obligation.py`, `smart_note_v2.py`,
`check_smart_note_unique_ids.py`, `door-obligation.yml`, the three guard
test files; `door_check_full.json` (checker output at basis);
depth-1 checkout retained at `wt/` during authoring (disposable).
