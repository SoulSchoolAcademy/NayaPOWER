# BLIND VERIFY REPORT — Hub Cleanup (remove Search pill + Intelligence-live banner)

- Verifier: Role 3 (blind), independent. Read-only on both subject files; no edits, no rebuild, no PR, no merge/deploy.
- Date: 2026-11-06 ~06:34–07:00Z
- Source (BEFORE): `live-index.html` — 5,503,605 B, 9,045 lines, sha256 `144a07c9be2f21301abea168ec664ff8967976295ab2d7337dde138b9689af80` — MATCHES brief.
- Cleaned (AFTER): `cleaned-index.html` — 5,500,995 B, 8,989 lines, sha256 `b65530049f1b611daf826dcb796c3646765c4f379b20035465734834a7a4f814` — MATCHES brief.
- Spec: `SCOUT-INVENTORY.md` read. Build script `remove-pill-banner.py` read (reference only).
- Method: Playwright + Firefox, served over local HTTP (ports 8123/8124), desktop 1920x1080 and phone 390x844, scroll 0 + scrolled + bottom, DOM probes + rendered-text search + screenshots + real clicks.

## VERDICT: PASS — all 6 checks pass, with evidence below.

## Static (source-level) findings
- Live: `naya-command-trigger` 3 hits, `feed-provenance` 5 hits, `feed-provenance-line` 3 hits, `naya-provenance-style` 1 hit.
- Cleaned: `naya-command-trigger` 0 hits; `.feed-provenance` CSS 0; `naya-provenance-style` 0; banner element creation gone.
- Cleaned remaining hits are guarded no-op writers ONLY: `getElementById('feed-provenance-line')` x2 (lines 3831, 3849), `fixProvenance` (3828, `if(!line) return;` inside try/catch), `updateFeedProvenance` (5891, guarded per spec), and the string literal `'Intelligence live …'` inside fixProvenance (line 3835) — a JS string, NOT rendered text (confirmed by rendered-text search: false in cleaned).
- Cleaned KEPT: `NayaSearchPalette` 1, `installHotkey` 1, `mountPalette` 1, `chassisSearch` 1.

## 1. CONTROL — PASS (with one harness fix, disclosed)
- Banner control (no stub needed): live renders `#feed-provenance-line` = 1, rendered text "Intelligence live — 381 Smart Notes · updated Oct 26, 2026" visible at top of feed, desktop + phone (screenshots `live-control-desktop-scroll0.png`, `live-control-phone-scroll0.png`). Note: 381 locally (live-registry fetch 404s locally, so the baked 381 notes show) vs 361 on production — count source differs, element is the same.
- Pill control, first attempt: live showed pill = 0. Root cause found by reading the code: the IIFE at live line 8991 does `if (!window.NayaSearch || !document.body) return;` and `js/naya-search.js` 404s on localhost, so the IIFE exits before creating the pill. This is a LOCAL harness limitation, not a property of either file.
- Pill control, fixed: staged byte-copies of both HTML files in `/tmp/hubverify-stage/` plus a minimal verifier stub `js/naya-search.js` (only `mountPalette` / `installHotkey` / `createStore`, copied from the IIFE's own usage; subject files untouched). With the stub, live renders the pill: desktop rect x=1803.65 y=932 w=100.35 h=43, visible, text "Search"; phone rect x=285.65 y=690 w=92.35 h=44, visible (screenshots `live-stub-desktop-scroll0.png`, `live-stub-phone-scroll0.png` — pill visible bottom-right in both). Control is therefore valid for BOTH elements.

## 2. GONE in cleaned — PASS (DOM + eye + rendered text, both viewports)
- DOM: `.naya-command-trigger` = 0, `#feed-provenance-line` = 0, `.feed-provenance` = 0, no button with exact text "Search" (only the main search input placeholder remains), at scroll 0, scrolled, and bottom, desktop + phone.
- Rendered text (exact phrases): "Intelligence live" = false, "Smart Notes · updated" = false, "Intelligence as of" = false, "repository snapshot" = false — in cleaned at both viewports (all true in live).
- Eye: `cleaned-desktop-scroll0.png` / `cleaned-phone-scroll0.png` / `cleaned-stub-desktop-scroll0.png` / `cleaned-stub-phone-scroll0.png` — no banner strip, hero sits higher (hero top: live 143 → cleaned 85 desktop; 157 → 81 phone), no empty gap where the banner was; no pill bottom-right in scroll0, scrolled, or bottom shots.
- Pill-spot click: clicking where the pill was (desktop 1860,920 / phone equivalent) in cleaned opened nothing (`__stubPaletteOpened` stayed 0) and produced 0 new page errors.
- Geometry: page scroll height shrank by exactly the banner's height — desktop 682599 → 682541 (−58px), phone 1758028 → 1757952 (−76px). No other layout shift.

## 3. STAYS still work in cleaned — PASS
- Present in DOM at both viewports: `#chassisSearch` = 1, `.hero` = 1, lens tabs = 3 [COLLECTIVE, PERSONAL, ACTIVITY], `.smart-tab` filter pills = 97, `.intel-board` = 381 (after settle), `.eco-bb-btn` = 12, `.notif-seg` = 3 (MAIL / ACTIVITY / SPACES).
- Search: typed "checklist" into `#chassisSearch` on cleaned desktop — value held, first board "Decide by the Checklist — Every Time" (screenshot `cleaned-interact-desktop-search.png`).
- Tabs: PERSONAL clicked on cleaned desktop AND phone — `aria-current` flips true, URL becomes `#/hub/feed-personal`, boards 381 → 5 (personal feed). COLLECTIVE clicked back — `aria-current` true, URL back, boards climb back to 381 (see §3 note). Screenshots `cleaned-3c-desktop-tab-personal.png`, `cleaned-3c-phone-tab-personal.png`.
- Filter pill: "Start Here" clicked on cleaned desktop AND phone — boards → 1 (screenshot `cleaned-3d-desktop-filter.png`).
- Palette kept: `window.NayaSearchPalette` = object in cleaned (stub round); Ctrl-K opened the palette in cleaned at both viewports (`__stubPaletteOpened` = 1). The pill removal did NOT kill the palette or hotkey.
- Boards settle note (NOT a defect): boards render in chunks — after a tab switch, counts read 144 @1s → 288 @3s → 381 @6s. The same progressive rendering appears in the live file (early reads of 336/288 in cleaned, 381 after settle in both). Final counts identical: 381 boards, live and cleaned, both viewports.

## 4. Viewports + scroll — PASS
- Desktop 1920x1080 and phone 390x844; scroll 0, scrolled (feed/boards), bottom of page; screenshot at every combination for both files (24 screenshots total, listed below).

## 5. Errors — PASS: 0 console errors, 0 page errors
- 0 console errors and 0 page errors on cleaned at both viewports in every run (rounds 1, 2, 3c, 3d), and 0 on live too — no NEW error, no pre-existing error at all.
- Failed requests (expected, identical in live and cleaned, NOT failures): `/feed-live.json` HTTP 404 (x3 per load — expected locally, brief says so), `/js/naya-search.js` HTTP 404 (round 1 only — fixed by the stub in round 2), `/icons/apple-touch-icon.png` and `/icons/naya-icon-192.png` HTTP 404 (missing local icons; the install modal references the 192 icon). All pre-existing/local-only, identical in both files.
- Guarded writers verified harmless: `fixProvenance` returns early on missing element (and is try/catch-wrapped); no error was thrown in any run, including the 400ms `watch()` interval and the 1200/3000ms timeouts.

## 6. No NEW visible defect — PASS
- Compared live vs cleaned screenshots side by side at every viewport/scroll: no layout crash, no overlap introduced, no missing section. Hero simply sits higher where the banner was.
- Pre-existing observations (identical in live, NOT caused by this removal):
  - "Install NayaNET" modal auto-appears over the page on first load in both files (it blocked Playwright pointer clicks until dismissed via its "Not now" button `#naya-install-later`; dismissal verified, overlay `display:none` after).
  - Board text runs under the fixed bottom bar at the very bottom of the viewport in both files (visible in live and cleaned scrolled/bottom shots alike).
  - At bottom-of-page, the sticky top bar overlaps the top of the last board's header ("Naya Note" peeking under INTELLIGENT HUB) — pixel-identical in `live-control-desktop-bottom.png` and `cleaned-desktop-bottom.png`.

## Files (all under /home/hatch/workspace/team-nitro/hub-cleanup/verify/)
- Report: `VERIFY-REPORT.md` (this file)
- Probe data: `probe-results.json` (round 1, no stub), `probe-results-stub.json` (round 2, stub), `interact-cleaned-interact-desktop.json`, `interact-cleaned-3c-desktop.json`, `interact-cleaned-3c-phone.json`, `interact-cleaned-3d-desktop.json`
- Harnesses: `render-verify.py`, `render-verify2.py`, `render-verify3.py`, `render-verify3b.py`, `render-verify3c.py`, `render-verify3d.py`
- Screenshots (24): `live-control-desktop-scroll0.png`, `live-control-desktop-scrolled.png`, `live-control-desktop-bottom.png`, `live-control-phone-scroll0.png`, `live-control-phone-scrolled.png`, `live-control-phone-bottom.png`, `live-stub-desktop-scroll0.png`, `live-stub-desktop-bottom.png`, `live-stub-phone-scroll0.png`, `live-stub-phone-bottom.png`, `cleaned-desktop-scroll0.png`, `cleaned-desktop-scrolled.png`, `cleaned-desktop-bottom.png`, `cleaned-phone-scroll0.png`, `cleaned-phone-scrolled.png`, `cleaned-phone-bottom.png`, `cleaned-stub-desktop-scroll0.png`, `cleaned-stub-desktop-bottom.png`, `cleaned-stub-phone-scroll0.png`, `cleaned-stub-phone-bottom.png`, `cleaned-interact-desktop-search.png`, `cleaned-3c-desktop-tab-personal.png`, `cleaned-3c-phone-tab-personal.png`, `cleaned-3d-desktop-filter.png`
- Local test servers on ports 8123/8124 stopped after the runs. Stub stage dir `/tmp/hubverify-stage/` (byte-copies + stub js only; the two subject files in hub-cleanup/ were never written to — sha256 re-verified unchanged at the end).
