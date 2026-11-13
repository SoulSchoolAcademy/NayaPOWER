# SCORECARD — Auto-Translate Repair Fix (Area #41, Maker Wrena/BUILD)

**Round:** repair fix · **Date:** 2026-11-13 · **Branch:** `personal/auto-translate-repair-fix-20261113` · **Staged only.**

**Self-score: 8/10.** One honest cycle against the brief's Done section. The 2 points are withheld for the checker/captain to award on rendered proof — they are not claimed here.

## Done-section scorecard

| Done item (brief) | Result | Evidence |
|---|---|---|
| Step 0: edit starts from the tip bytes (`f9f58cc7…`) | **PASS in substance, FAIL in letter** — the local worktree file was never restored (60+ flake-blocked attempts; file is 0 bytes, flake damage). The build fetches the tip blob from GitHub in memory and asserts its sha before any edit, so the edited bytes ARE the tip bytes. | Record §2. Build asserts base sha `f9f58cc7…` on every run. |
| F1 `Plugged into this world` h3 closed | **PASS** | `data-mw-tr="dash"` span, line 6426; inventory: 1 occurrence, GUARDED. |
| F2 three TnTacho `setCap` captions closed | **PASS** | All three routed through `mwTr`; `frame()` cache reset re-paints on switch; inventory: all GUARDED. |
| F3 `renderLinks` no-clicks empty state closed | **PASS** | Else-branch routed through `mwTr`; inventory: GUARDED. |
| F4 three `renderBars` `Busiest:`/quiet-stretch sites + missing keys | **PASS** | All three assignments + both 10285 suffixes routed; 7 new keys; inventory: all GUARDED. |
| F5 funnel `conv('of recorded invites joined')` closed | **PASS, plus the builder whole** | `conv` + `stage('Joined')` + 4 truth branches routed; 2 new keys; inventory: GUARDED. |
| F6 old `#plusmenu` items + `Add` label + button titles, or prove which menu is live | **PASS** | `#plusbtn` opens `#plusmenu` (wiring verified); all 4 items + label + button aria/title marked; 4 new keys; `#fcPlusMenu` aria-label + `#os-list-add` closed as adjacent exact-label sites. |
| F7 `#avedit` `Change picture` / `Edit photo` closed | **PASS** | `data-mw-aria` + `data-mw-title` added; both keys added; inventory: GUARDED. |
| F8 `Video`/`Voice note` save-path bake closed | **PASS** | Empty title stored; guarded display fallback fires; only consumer verified (`cardHTML`). |
| F9 wall `Untitled note` + `bestSave` closed | **PASS** | Both sites routed through `mwTr` at render; inventory: GUARDED. |
| F10 `Hide breakdown` toggle closed | **PASS** | Toggle routed + T() re-sync reads panel state; key added; inventory: GUARDED. |
| Every missing key added in es/fr/de | **PASS** | 16 new keys, 807/language, 0 empty, key sets identical. |
| Inventory counted the checker's way, before AND after | **PASS** | Before: the ten as the checker named them. After: 218 GUARDED / 63 UNGUARDED, every UNGUARDED line triaged in record §8. |
| Nothing else changes | **PASS** | Diff 56 hunks: 28 site reps + 28 dict insertions; no hunks outside the charged surfaces + dict span. No Settings panel, card labels, F1 word, gear/panel, fidelity-line, or follow-on changes. |
| No live touch, no merge, no PR | **PASS** | Staged only; new branch from the third-surface tip. |
| Translate tap works end to end (Smart Note + Naya Note) | **NOT PROVEN — owed** | VM browsers dead; not run by this seat. Owed to checker/captain on the staged link. |
| Zero overflow 390/1440/360, zero console errors | **NOT PROVEN — owed** | Same. Cloud browser is 1920px and cannot resize. |
| No-regression battery by eye | **NOT PROVEN — owed** | Same. |
| `dict-final.json` restored | **NOT DONE — owed, recorded** | 0 bytes, flake damage; durable sources named in record §9; every exec write route to that path is blocked. |

## The score, honestly

- **8/10 for the build:** the ten are closed by the byte inventory, the dictionary grew cleanly, the diff is tight, the parse is clean, and every gap I found along the way is named in the record instead of hidden.
- **2 points withheld** for the checker/captain to award on rendered proof (Translate tap both note kinds, overflow at 390/1440/360, zero console errors, no-regression battery, whole-page sense check). The last round's lesson stands: rendered proof cannot retroactively pass a round, and a byte pass cannot stand in for it — so the 2 points stay unclaimed until the eye check runs.
- **What would have made it 10/10 from this seat:** a rendered pass of the staged link in es/fr/de and a completed `dict-final.json` restore. Both were blocked by the environment (dead VM browsers, EPERM flake), not by the work — and both are named as owed, with the exact evidence, rather than claimed.

## Self-Check Law — one cycle, in brief

Three checks of my own work: (1) the build's exact-count reps + node parse + inventory re-run; (2) the diff hunk-by-hunk against the tip (every hunk mapped to an F-site or a dict insertion); (3) the full UNGUARDED triage, line by line, in record §8. The seven pre-merge questions are answered in writing in record §10. No merge in this round.
