# Merge provenance — canonical block catalog

How `block-catalog.json` and `index-by-use-case.json` are built, so a cold
successor can reproduce them from this branch alone. No workspace-local files
are needed for the base catalog.

## Inputs — `fragments/`

| file | records | built by | sources mined |
|---|---|---|---|
| `catalog-frag-a.json` | 276 | t0905 extraction (Lane 5 Seeker) | Naya_Design_Elements_N2.html (94), Naya_Design_Element_Set_N4.html (65), Naya_Beautiful_Button_Set_N4.html (43), Naya_Jewel_Library_-_N5.html (33), Naya_Design_Standard_Showcase__1.html (24), Naya__Elite_Buttons_N5.html (17) |
| `catalog-frag-b.json` | 220 | t0906 extraction (Lane 5 Seeker) | Naya_Ultimate_Design_System_-_Naya_2.html (150), Naya_Lego_Blocks_N4.html (61), Naya_Smart_Hub_Design.html (5), Naya_Epic_Elements_-_Lego_pieces_N5.html (4) |
| `catalog-frag-c.json` | 2 | gap-t0907 promotion (Lane 5 Seeker) | Naya_Ultimate_Design_System_-_Naya_2.html (2) — the two specimen-backed HAVEs promoted to production blocks: settings row → NAYA-FRM-007, media player → NAYA-MED-001 |

Each record carries `source_file` + `temp_id`; merged records carry a `sources`
list preserving both. The design-language source HTML files live at
`HUB/design-system/library/{blocks,buttons}/` on this branch.

## The merge — `tools/merge-catalog.py`

Repo-local, deterministic twin of the original t0907 merge script. Run from this
directory:

```
python3 tools/merge-catalog.py
```

It reads the three fragments (498 raw records), resolves 28 UNCAT records
(color-token demos and image assets excluded with written justification;
checkbox row → FRM; spectrum swatch buttons → BTN), folds byte-identical
duplicates, assigns deterministic `NAYA-<CAT>-<NNN>` model numbers (per-category
sort by normalized name + first temp_id), and writes `block-catalog.json` and
`index-by-use-case.json`.

Reproduction check (run 2026-10-16, seeds 0/1/42/99 — all identical):

```
block-catalog.json       459 records  sha256 89bfc298a791c3710e7090774d4317d4e0553c87b992c27ba7e9a7296c0a6fc
index-by-use-case.json   17 keys      sha256 3ecd40503c2c453da3057048a916ee5dd60b81655779aeaed669aa0018c20a36
```

**Determinism note (gap-gap-t0907 root fix):** the original merge script joined
multi-source `notes` from a Python `set`, whose iteration order depends on
`PYTHONHASHSEED` — three runs gave three different SHAs. Commit `1ec4e1a`'s
`block-catalog.json` was one such seed-lottery draw (3 of 459 records carry a
`notes`-join order that no seed reproduces canonically). This script sorts the
join; output is now seed-independent. The fix was applied to the
workspace-local original (`t0907-merge-catalog.py`) as well.

## Boundary: the 19 domain-family records

Commit `35131afe3c68` ("ingest: 19 domain-family blocks (CAL/PAY/ONB/CHT/CMT) —
catalog 459→478") added 19 records on top of the base catalog. Those records'
merge inputs are **not** on this branch — the ingest commit touched only the
three output files. What this means for reproduction:

- `fragments/` + `tools/merge-catalog.py` reproduce the **459-record base**
  exactly (verified: tip catalog minus the 19 `NAYA-{CAL,PAY,ONB,CHT,CMT}-*`
  records equals the re-merged base in all model numbers, names, categories,
  tags, use-cases, html, css_classes, and sources; 3 records differ in
  `notes`-join order only — the `1ec4e1a` seed-lottery residue named above).
- The 19 family records' provenance (their extraction inputs and ingest
  pipeline) is still owed by the ingesting run. Until it lands, a cold
  successor can reproduce the base and must take the 19 family records as
  committed bytes.

## What is NOT machine-generated

- `coverage.md` is hand-maintained. The script prints coverage-candidate matches
  to stdout for manual review; the HAVE/GAP judgments live in `coverage.md`.
- The render verification of the two promoted blocks (NAYA-FRM-007, NAYA-MED-001
  render pixel-identical to their source nodes under the design-system CSS) is
  evidenced in the lane receipt
  `hidden_files/twelve-lane-receipts/gap-gap-t0907-lane5.md`, not on this branch.

## Lineage pointers

- Original workspace-local merge script: `t0907-merge-catalog.py` (lane-executor
  workspace; same logic, workspace paths, same determinism fix applied).
- Extractors (re-extraction, not re-merge): `t0905-extract-a.py`,
  `t0906-extract-b.py` — workspace-local; the fragments above are their
  checked-in outputs.
- PR: #2713 (`naya4/hubdrive-block-catalog` → `naya4/design-system-v1`), open,
  unmerged.
