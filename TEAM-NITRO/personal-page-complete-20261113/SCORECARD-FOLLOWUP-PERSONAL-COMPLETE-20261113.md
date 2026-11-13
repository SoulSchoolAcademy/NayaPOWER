# SCORECARD — Personal page complete FOLLOW-UP round (2026-11-13)

## What it is

The ONE scorecard cycle for the follow-up round (maker DONE 9/10 build / 8/10 proof + checker PASS 8/10 in round 1 — below 9, so it goes back in). Ten loves, ten don't-loves, ten ways to 10x the value, ten solutions applied now. The cycle is the decision record for the follow-up build: Defect 1 (both drawers stranded), the two record corrections, the Public-tab widening + keyword pull, and the four fetching-browser sub-proofs as the captain's leg.

## Why it matters

The checker proved the seven items and both sharpenings are built — what failed is a real regression (the drawers lost their only openers), two false statements in the record, and the Public tab's owner-scoped query. The cycle below is what the follow-up fixes, and what it deliberately does not fix, with the reason named.

## How to apply it

Read the ten solutions — each one maps to a hunk in `build-followup.py` / `diff-followup.txt`. The don't-loves that survive are carried into the record as named gaps, not hidden.

---

## 10 loves

1. The Spaces seg becomes the left drawer's opener — the checker's exact failing test (tap at 360 navigated away to `nayanet.app/#/hub/spaces`), fixed in the page's own language, in place.
2. A fifth bottom-bar seg opens the right drawer (Smart Factory + memberships) — same tile language, same glow, no floating pluses, no new chrome.
3. The Public tab finally pulls the collective — item 5's bullseye as Shawn dictated it (any topic, type a keyword, changeable).
4. The keyword pull rides the existing popup + `NayaSmartBar.onSearch` hook — no invented visible search bar, popup-only law kept.
5. The fixture rows are real rows in the real table, pulled by the real query — the feed is never faked.
6. The Personal tab is untouched in behavior — the owner filter stays, so the owner's wall cannot regress.
7. The wall's P6 verification filter is reused verbatim for the collective — no new filter logic, no new markers.
8. The record corrections are surgical strikes plus truth statements, not rewrites.
9. The captain's leg is a procedure with exact expected numbers (Public 6 / garden 2 / harvest 1 / pill 245 / Naya 14) — checkable in minutes on a fetching browser.
10. The no-regressions diff names every hunk — the seven items + pill restyle still pass.

## 10 don't-loves

1. The bottom-bar tiles must shrink to 46px at ≤400px to fit five segs — the bar gets smaller on phones.
2. The Hub shell carries no search to harvest (0 hits for every search identifier) — the "harvest" is the mechanism already on Personal; the opener button is new.
3. The owner's Personal wall honestly renders 0 cards — all 4 of the owner's wall-kind rows are P6-filtered verification artifacts.
4. The fixture rows must stay in the live table until the captain's leg runs — a cleanup debt, not a clean finish.
5. Anon RLS readability of other owners' rows is unproven from here — the widening could still be blocked at the policy layer.
6. The popup's result links go nowhere (`#`) — clicking a result only closes the popup onto the already-filtered feed.
7. The keyword filter lives in the painter, not the query — a 500-row client filter, not server search.
8. The search button is a new control in the feed header — one more thing on the page.
9. The Spaces seg's old behavior (navigate away to hub/spaces) is gone — a citizen who used it as a shortcut now gets a drawer.
10. The four fetching-browser sub-proofs still cannot be run here — the round ends with an owed leg again.

## 10 ways to 10x the value

1. Real citizens' notes in the Public feed — once citizens post, the collective is alive, not fixtures.
2. Server-side keyword search (PostgREST `ilike` on content) instead of the 500-row client filter.
3. A real presence feed (online-now) so "live" means online, not endpoint-matched.
4. Search results that jump to the card (scroll + light it) instead of dead `#` links.
5. The drawers' links closing the drawer after tap — in-page links leave it open today.
6. Public-feed Smart Tabs by topic, not just author — the ribbon already grows from the notes.
7. The pill number proven live (245) — closing the last points gap.
8. Smart Lists render proven on the fetching browser — the last mechanism gap.
9. Zero console errors on the fetching browser — the environmental stop fully cleared.
10. The same drawer + public treatment cloned to Business/Space from these bytes (Clone Law).

## 10 solutions now

1. Spaces seg → left drawer in place (no navigation); the drawer-close guard exempts the two drawer segs.
2. Fifth `eco` seg → right drawer, same tile language; phone tiles 46px at ≤400px (still above the 44px tap floor).
3. `pcToggleDrawer` / `pcCloseDrawers` exposed from the drawer IIFE; the hidden plus buttons reuse the one path.
4. `pcLoadPublicWall`: collective `smart_notes` read (no owner filter, 500 newest), P6 filter reused verbatim.
5. `mwPaintWallPosts` keeps two stores (owner vs collective) + keyword filter + honest meta line.
6. `mwBuildFeedPills` grows the ribbon from the collective on the Public tab (author pills from other citizens).
7. `NayaSmartBar.onSearch` wired to `pcSetPublicKeyword` + matching-note results in the popup dropdown.
8. A Search button at the top of the feed opens the existing centered popup — no visible bar.
9. Three fixture rows (`garden` ×2, `harvest` ×1, alias `pcfollowup20261113`) left in place for the captain's leg, named in the record.
10. Record corrections struck + the captain's-leg procedure with exact expected values written in; the Naya Notes dead-client line fixed (same NayaAuth-first resolution the Lists room already uses).

## Gates re-run (before filing)

1. **Is it right?** Yes — the drawers work again, the Public feed pulls the collective honestly, nothing is faked, nothing live is touched.
2. **Is it what they truly need?** Yes — the checker's Defect 1 + the captain's ruled items (tab order kept as built, Public widened, keyword pull present).
3. **Is it mine to do?** Yes — maker seat for the follow-up, lane branch, staged only; no merge, no deploy, no PR, no live tap; the fixture rows are test rows in the shared table, named for deletion after the captain's leg.
4. **Is now the time?** Yes — tip `a7b55ab5` verified first-hand, staged SHA re-read fresh before editing, live Personal re-curled unchanged.
5. **Can I prove it?** Yes, except where the record says otherwise — every number below is a Playwright measurement or a service-key read, and the four fetching-browser sub-proofs are named as the captain's leg with exact expected values instead of claimed.

---

## Final self-score — after the staged verification (2026-11-13)

**Build 10/10 · Proof 8/10 — follow-up items 1–3 done and measured; item 4 remains the captain's leg.**

- **Item 1 (Defect 1) — done, 10/10.** Both drawers open in place at 390/1440/360 on the staged link (URL unchanged every tap), backdrop tap and Escape close everywhere, re-tap close at 1440. Left box (0,0) 300×844 at all widths; right box (90,0) @390, (1140,0) @1440, (60,0) @360. Eye-checked at 390 (drawer open, 8 links as elevated boards, page dimmed). The re-tap failure found by the first probe run is fixed in pass 2 (bar rises above the scrim, open seg lights).
- **Item 2 (record corrections) — done, 10/10.** Both false statements struck in place with the truth stated: drawers were both stranded (left never reachable via the Spaces seg); seed nutshells are from the filed notes on main, not the Hub shell.
- **Item 3 (Public widened + keyword pull) — done, 10/10 on the mechanism.** Staged stub proof with the real table rows: Public 6 cards / 4 voices → `garden` 2 → `harvest` 1 → cleared 6 → Personal 2 (owner store intact). Hub-search finding named honestly: 0 hits in the shell, so the harvested mechanism is the one already on the page; the only new control is the Search button opening the existing centered popup. The collective pull on a fetching browser is the captain's leg — the RLS question is open and named.
- **Item 4 (four sub-proofs) — NOT proven here, 0/4, the captain's leg.** Procedure + exact expected values written in the record: (a) Personal 0 cards + placeholder (26 rows in the table, 4 wall rows P6-filtered), Public 6, Naya 14; (b) pill 245, gauge 49.0%; (c) Lists "Saved on this device"; (d) 0 console errors, 0 page errors. Staged here: 42/60/42 console errors, all failed external fetches from this VM, 0 page errors.
- **No regressions — 10/10.** 15 + 4 hunks only; seven original items + pill restyle re-proven on staged at all three widths (buttons equal ±0 px, gear ⚙️, no name/cover intersection, tabs in order, feed line literal, rail 20/0 `<img>`, overflow 0). Staged SHA `4872414a…` re-read fresh, byte-identical to local. Live Personal `992ab18c…` and live Hub `0c8628d5…` unchanged.
- **Why proof is 8, not 10:** the four sub-proofs need a fetching browser and are owed; the fixture rows stay in the table until that leg runs (cleanup debt, named in the record with ids and the deletion instruction); the anon RLS readability of other owners' rows is unproven from here.

## Evidence

- Staged link: https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/personal-page-complete-20261113/personal-complete.html&ref=personal/personal-page-complete-20261113&cb=bab47fb67
- Staged SHA (curl, fresh): `4872414a1d428a940a4e12ac31c419f999843a2fde072a9ac91d09b42051c666`, 1,555,404 B — matches the local file.
- `verify-staged-followup.json` · `verify-followup.json` · `followup-*.png` · `staged-followup-*.png` (lane dir + branch).
- Commits on `personal/personal-page-complete-20261113`: `bab47fb67` (build + probes + scorecard, pushed, remote tip verified) · record/scorecard touch-up follows as a second commit.
