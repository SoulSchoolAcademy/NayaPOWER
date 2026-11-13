# SCORECARD — Auto-Translate Third-Surface Fix (Area #41, Maker Wrena/BUILD)

**Round:** third-surface fix · **Date:** 2026-11-13 · **Score: 8 / 10** (one scorecard cycle, self-scored honestly against the brief's Done section).

## What Done required vs what is proven

| Done item | Status | Evidence |
|---|---|---|
| Every remaining English fixed label on the charged surfaces speaks es/fr/de (Notes composer, feed chrome, German leftovers incl. bottom-bar SPACES, Dashboard view as it appears on this page) | **Done, byte-proven** | Dict 266 → 791 keys/language (525 new + 2 fixes); `mwTr` guards 81 → 603; `data-mw-tr` 196 → 364; diff 239 hunks, all in charged surfaces; no hunks elsewhere |
| Nothing left in English except proper names and the citizen's own words | **Done, byte-proven** | Same counts; proper names (`Dashboard`, `Smart Mail`, `Smart Links`, `NayaNET`) kept by dict evidence; citizen words untouched (Translate tap mechanism unchanged) |
| First-hand inventory counted, listed in the record, then closed | **Done** | Record §4 lists the inventory by surface; the rep tags in `build-third-surface.py` are the machine-readable close-list |
| Judgment calls by the proper-names rule with evidence stated | **Done** | Record §5 (`Naya Notes` is chrome; `Dashboard` proper name; Cover-Button German verified, no change; `&rsquo;` bug fixed) |
| Translate tap re-proven end to end on BOTH a Smart Note and a Naya Note | **NOT done by this seat — owed** | VM browsers dead (Chromium headless-shell launch fails immediately; Firefox SIGSEGV / Chromium SIGTRAP). Mechanism unchanged, but the re-proof itself must run on the staged link by checker/captain |
| Staged only — new branch from F1 tip, no merge/PR/live/mail | **Done** | Branch `personal/auto-translate-third-surface-fix-20261113` from `f8bf4d67…`; one commit; nothing merged, no PR, no live touch, no mail |
| Staged link same bytes as local (sha re-verified at round end) | **Done by construction, re-verify owed** | Staged link carries `cb=ce42cec8d4c18f6b89eccab8ff20d7b9a6221ee2` (page blob sha, computed from built bytes); checker/captain re-verifies staged bytes vs local sha |
| Record + scorecard written | **Done** | This file + `RECORD-AUTO-TRANSLATE-THIRD-SURFACE-FIX-20261113.md` in `~/workspace/team-nitro/auto-translate-20261113/` |
| No regressions (Settings/tabs/rail/+/bottom bar switch; card labels read es/fr/de; pill settles; language persists; Translate tap untouched) | **Protected by construction, eye-proof owed** | No change to any of those code paths; rendered proof cannot run in this VM — owed on the staged link |

## Why 8 and not 10

- **+8 earned:** the build is complete and byte-verified end to end — 791-key dictionary with assertions, 603 guard sites, 36/36 script blocks parsing (after hunting and fixing 5 quoting faults the node parse exposed), a 239-hunk diff confined to the charged surfaces, staged link with the real blob sha, and a record that names every gap and follow-on instead of hiding them.
- **−2 withheld:** the brief names the Translate tap re-proof explicitly, and rendered proof (eye check, 390/1440/360 overflow, zero console errors) is part of Done — none of it could run in this VM because the browsers are dead. A maker score of 10 would claim proof that does not exist. The 2 points are the checker/captain's to award on the staged link: if the tap proves on both note types and the page reads clean at phone width with no console errors, this round is a 10.

## Self-check (three passes, in the round's own terms)

1. **Is every label closed?** Yes by count (791 keys, 603 guards, 239 hunks) and by surface (record §4). Two labels the first inventory missed (`Home`/`Dashboard` keys, `Lists`/`Scheduler`/`Reports` fallback) were found by verification and closed in the same round.
2. **Is the page still a working page?** Yes by parse (36/36 blocks, 0 failures, 0 literal-`tr(` leaks) and by construction (no change to switch/navigation/Translate paths). Rendered proof is owed, not claimed.
3. **Is anything hidden?** No — the record names the unproven items (§9), the dead code left alone (§6), the follow-ons (§10), the flake damage (`dict-final.json` still 0 bytes), and the filing shape (§1: commit sha lives in the handoff, not in the filed record, so no placeholder is printed).
