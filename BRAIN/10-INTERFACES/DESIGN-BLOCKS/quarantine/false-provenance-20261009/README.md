# Quarantine: False Provenance (2026-10-09)

## Why these blocks are here

These 14 blocks were marked `provenance=EXTRACTED` / `status=APPROVED_SOURCE` with
`source: Naya_Lego-blocks.html`. Independent verification (2026-10-09) proved their
`.nl-*` selectors appear in **zero** of Shawn's 15 DESIGN/ HTML source files.

They are authored inventions wearing extracted provenance. PR #1992's quarantine
checked file references but missed selector-level fidelity.

## Blocks quarantined

nl-bar, nl-ccard, nl-chart, nl-field, nl-iconbtn, nl-modal, nl-playbtn, nl-player,
nl-search, nl-sheet, nl-switch, nl-table, nl-toast, nl-toggle-row

## What this is NOT

- Not deleted. All files preserved here.
- Not a judgment on quality. Some may be good blocks.
- Not permanent. Shawn may re-extract from true source or approve as authored.

## To restore

Either:
1. Re-extract from Shawn's actual source files with byte-verified selectors, OR
2. Get Shawn's explicit approval to mark as `provenance=AUTHORED` / `status=CANDIDATE`

## Related

- Parity checker report: #1354
- PR #1992 (first quarantine — file-level, missed selector-level)
- nav-orb and stage were initially flagged but VERIFIED to have source provenance
  (.nav-orb in 2 files, .stage in 10 files) — they were NOT quarantined.
