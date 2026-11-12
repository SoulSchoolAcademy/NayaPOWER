# Pricing Round 7 Fix3 — Parts Manifest
**Filed:** 2026-11-07. **Fix3 file:** `~/workspace/verify-pricing-v6/pricing-round7-fix3-work.html` (sha256 `e97815a26bb3a3e8e7dcd013f9a02c437db3c6f9474038f722824652e34f96c6`, 335410 bytes / 2,867 lines (script count; `wc -l` 2866 — trailing-newline count)).
**Parent:** fix2 (`pricing-round7-fix2-work.html`, sha256 `71fb1cdb20abfd31f8f7ca13a2bbda5b3f79c73a659a4f6c7980684219180c53`, 304108 bytes / 2,703 lines) — FROZEN, never edited in this pass. The fix3 file is a copy of fix2 with F25 + F26 + Addition 21 applied, regenerated twice from the fix2 copy (the phone-close trims were corrected from measured base values, not guessed ones — see below).
**Minting Law:** every new part this pass is named, filed, and inventoried — GitHub `BRAIN/10-INTERFACES/DESIGN-BLOCKS/pricing-round7-fix3/` + local `~/workspace/smart-factory/pricing-round7-fix3/` + `PARTS-REGISTRY.md` — the same pass it is used.

## Parts filed in this pass (1 file)
1. `smart-tabs-rail.md` — Smart Tabs — Capsule-Pill Rail (Addition 21)

## Fixes with no new part (recorded in BUILD-REPORT-ROUND7-FIX3.md, not filed as parts)
- **F25** Demo card note clears the fold (compaction of the demo-done state: speedo 260→232, gauge/card/sub/way margins, card padding 16→12, note margin 12→8; phone speedo 200→184) — a repair of the filed `demo-three-questions.md`, not a new part.
- **F26** Systems orbit clears the fold (orbit 680→620px, orbit margin-bottom 28→20, systems-sub margin 24→16, systems-img margin 24→0) — a repair of the filed systems orbit, not a new part.
- **Phone close stack trims** (the rail's +24px absorbed: grid gap 8→4, grid margin-bottom 12→6, question + rec-line margins →4, banner-bottom margin 20→8) — a repair, not a new part. The first draft trimmed the WRONG base values (read off stale rules: offer pad 10, question 12, rec 10) and the button landed at 808–856, 12px over the fold; the correction measured the true fix2 base (offer pad 8, question 6, rec 4) and the button landed at exactly 844 (zero slack); the banner trim bought the final 12px slack (784–832). The lesson is filed in the build report: measure the base, don't read it off a stale rule.

## Build history (this pass)
- Fix3 sha `0e5b411c…` (334,893 bytes) — first build: F25 + F26 + Smart Tabs, keyboard test failing on a harness bug.
- Fix3 sha `203bd292…` (335,221 bytes) — regenerated from the fix2 copy with the corrected phone-close trims; self-check run 4: close button at exactly 844 (zero slack).
- Fix3 sha `e97815a2…` (335,410 bytes) — regenerated from the fix2 copy with the banner-bottom margin trim; self-check run 5: ALL PASS (close button 784–832, 12px slack). This is the final file.
