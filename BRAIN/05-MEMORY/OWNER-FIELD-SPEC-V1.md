# OWNER-FIELD SPEC V1 — block attribution for the knowledge corpus

w192, Naya Beta (KNOW). Canonical definition of the `owner` field added to the
three knowledge schemas. One distributed truth: every block attributable to a
named Naya; never null; never invented.

## The three schemas and their homes

| Corpus | Schema id | Canonical files | owner addition |
|---|---|---|---|
| IB-SMART-NOTE capture | `naya.smart-note-capture.v2` → **v3** | `.naya/capture/*.json` (writers: runtime receiver `v7-smart-note-canonical`) | top-level `owner` + `owner_basis` |
| Projection index | `naya.smart-note-projection-index.v1` → **v2** | `.naya/memory/smart-notes/index.json` (writer: `tools/smart_link.py` `generate()`) | per-entry `owner` + `owner_basis`; top `version` 1.0 → 2.0 |
| BRAIN index blocks | `naya.brain.real_tree.v1` → **v2** | `BRAIN/REAL-TREE.json` (writer: `tools/regenerate_brain_index.py`; gate: `tests/test_brain_index_freshness.py`) | per-entry `owner` + `owner_basis`; regen tool MUST emit owner (spec of the mechanical field update in §5) |

## Field definition

- `owner`: a named Naya identity. Values: a seat name (`Naya Alpha`…`Naya Mu`),
  a lead name (`Naya Clarity Narzan`, `Naya Verity Narzan`, `Naya Resolve Narzan`),
  or the collective `Naya` (Shawn's ruling: IB owners = NAYA — intelligent blocks
  belong to the collective unless provenance names a seat). NEVER null, NEVER "".
- `owner_basis`: HOW the owner was determined — `provenance` | `area_lead` | `collective`.
  A cold reader re-runs the rule on the bytes and must get the same answer; the
  basis tells them which rule fired. This is what makes the field honest instead
  of decorative (P-003: never fabricate provenance).

## Derivation rules (ordered — first match wins)

1. **provenance**: the block's own provenance bytes name a Naya seat. Sources:
   capture `source.captured_by` (e.g. "Naya 2 (scribe)"), `intelligence`/`source`
   ingest notes citing a seat, index-entry `backfill`/`provenance` notes citing
   a seat. Seat names normalize: `Naya 2` → `Naya Verity Narzan`? NO — do not
   invent mapping. `captured_by` free text that does not resolve to a current
   named seat → rule 3. Verbatim seat text that IS a current seat name → that seat.
2. **collective**: the block is an Intelligent Block in the IB capture corpus and
   no provenance names a seat → `owner: "Naya"`, basis `collective` (Shawn's ruling).
3. **area_lead**: no provenance, not IB-corpus → owner = area lead of the owning
   BRAIN domain, per DOMAIN_OWNER v1 below. For capture/index entries: owning
   domain = first path segment under `BRAIN/` in `projection_path` / entry path;
   entries with no BRAIN path → `TEAM` (Naya Kappa, operations) — recorded as
   basis `area_lead`, domain `UNMAPPED`.

## DOMAIN_OWNER v1 (BRAIN domain → area lead; PROPOSED — needs lead confirmation)

| Domain | Owner | Area |
|---|---|---|
| 00-ACTIVATION | Naya Gamma | ACT |
| 01-GOVERNANCE | Naya Delta | LAW |
| 02-ARCHITECTURE | Naya Beta | KNOW |
| 03-KERNEL | Naya Beta | KNOW |
| 04-INTELLIGENCE | Naya Zeta | Intelligent Blocks |
| 05-MEMORY | Naya Beta | KNOW |
| 06-PROOF | Naya Epsilon | VERIFY |
| 07-LEARNING | Naya Alpha | LEARN |
| 08-SUCCESSION | Naya Iota | SUCCESSOR |
| 09-EVOLUTION | Naya Alpha | LEARN |
| 10-INTERFACES | Naya Mu | Human Value |
| 11-KNOWLEDGE | Naya Beta | KNOW |
| 12-ENGINEERING | Naya Lambda | INFRA |
| 90-OPERATIONS | Naya Kappa | TEAM |
| 99-ARCHIVE | Naya Kappa | TEAM |

Non-BRAIN paths (`.naya/`, `tools/`, root docs): `.naya/` → Naya Kappa (TEAM,
operations infrastructure); `tools/` → Naya Lambda (INFRA); repo-root contract
docs (`0000-*`, `CONSTITUTION/`) → Naya Delta (LAW). Same basis: `area_lead`.

## Idempotency contract (the verification ladder, rung 3)

`tools/owner_backfill.py` implements these rules. Re-running it on an already
backfilled corpus produces ZERO diff: if `owner`+`owner_basis` exist and match
the derivation, the file is untouched. A run is verified by: run → apply →
run again → empty diff (prove, don't claim).

## §5 — regen-tool companion (REQUIRED, not optional)

Adding `owner` to REAL-TREE entries changes what `tools/regenerate_brain_index.py`
produces. Its `--check` compares against the generator's own output, and
`tests/test_brain_index_freshness.py` asserts freshness — so the generator MUST
be updated to emit `owner`/`owner_basis` per this spec in the same commit as the
backfill, or the check fails as drift. Same for `tools/smart_link.py::generate()`
(index writer): new entries get owner at generation time per these rules.
DONE w202 (Beta): `generate()` emits owner/owner_basis via shared
`derive_real_tree()` from `tools/owner_backfill.py` (path-only), fail-closed,
never silently ownerless; 3 pinning tests in `tests/test_smart_link_generator.py`.
MEASURED w202 (Beta, at this head): index backfill vs the shared derivation
agrees on 631/632 index entries. The one divergence is
`IB-SMART-NOTE-20261014-sn0797` — stored `owner: Naya Mu`, basis `provenance`
(spec rule 1: the entry's provenance bytes name the seat), while `generate()`'s
path-only derivation (rule 3) would emit Naya Beta. `derive_real_tree()`
implements rule 3 only; rules 1–2 are not wired into `generate()`.
DONE w203 (Beta, lane 4): `generate()` now routes through the FULL ordered
derivation — `tools/smart_link.py` imports `derive_index_entry()` and feeds it
the existing entry's provenance/backfill bytes (exactly what a backfill
re-apply reads), so emission==backfill by construction. For brand-new paths
with no stored bytes, rule 1 cannot fire and the derivation honestly falls
through to area_lead — no invented provenance; the backfill pass self-heals
any owner whose pipeline-added provenance names a seat. MEASURED w203: on
all 583 projection-shaped entries, emission == backfill-derivation == stored
owner (0 divergences); 49 non-projection entries are refused by generate()'s
shape gate by design. Regression tripwire added:
`test_generate_fires_rule1_on_existing_entry_provenance` (+ a new-path
stays-path-only test). Extension point: if a future caller passes `capture`
AND the receiver persists its provenance bytes into the entry, the probe can
include capture bytes — until then, only stored bytes are consulted (P-011).
What this update does NOT claim: it does not change DOMAIN_OWNER v1 values;
it does not re-certify the 3 w200 pinning tests beyond their stated scope
(wiring, not mapping values).

## What this does NOT claim

- It does not attribute authorship — it attributes OWNERSHIP (accountability).
  A reconstruction's owner is "Naya"/area-lead, not "who wrote the thought."
- It does not resolve ambiguous historical `captured_by` text to new seat names;
  unresolvable text → area_lead, basis recorded, no silent invention.
- DOMAIN_OWNER v1 is a proposed mapping, not ratified truth; entries derived
  from it carry basis `area_lead` precisely so a correction re-derives cleanly.
