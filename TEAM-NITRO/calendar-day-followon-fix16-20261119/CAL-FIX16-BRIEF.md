# CALENDAR FIX-16 BRIEF — nav pills clipped + the phone-width pass (2026-11-20)

## Base (verified by the coordinator)
- Base: fix-15 branch `calendar/day-followon-fix15-20261119`, tip `cf9e1132e4540e978fb5b94255b438b91bb149e9` (parent = fix-14 tip `5904e481471c8439149b116a14dfd74bec266569`)
- File: `TEAM-NITRO/day-view-v18-fix-20261117/the-ultimate-calendar-v18-fix.staged.html`
- Blob: `76539677f05b71729d96ae108b56ce7ddca95503`, 401,766 B, sha256 `958788c30b53e61f4848c533dee1adf21db084bd9d13d6ae94995135d7134d3e`
  (coordinator re-derived via the git blob API: size + sha256 match exactly)
- Fix-15's work stands: weather pill clears day-teach + store line at 390 (7-day sweep, both font states), Worlds 2×3 readable, laws 0/28 delta 0, 0 page errors. Do not touch them.
- New branch: `calendar/day-followon-fix16-20261119`
- Records: `~/workspace/team-nitro/calendar-day-followon-fix16-20261119/`
- Staged only. No merge, no live deploy, no link to Shawn.

## Activation (read first, before any edit)
`~/workspace/team-nitro/THE-NAYA-DESIGN-LAWS.md` · `THE-PLAYBOOK.md` · `DESIGN-INTELLIGENCE-REPORT.md` · `THE-ANATOMY-OF-A-SMART-APP-PAGE.md` · `THE-HEART-OF-THE-MACHINE.md` · `~/workspace/team-nitro/AGENTS.md`. After the work, the §11 check in writing + the checker script + the eye. Laws delta 0.

## The fix-15 eye verdict (the whole reason for this round)
Captain's eye, cloud browser (browser-task 5a4a919e, agent 6b6a06a1, completed 01:56:09Z).
DESKTOP PASSES: wisdom reads whole on all 7 days (Nov 15–21) with the weather pill clear of the text; Your Worlds row reads whole (six tiles, full labels, no clipping/overlap); greeting correct — "Good evening, Shawn." with live clock; whole 9-block deck and month view read well.
PHONE WIDTH NOT VERIFIED: the cloud browser window was fixed at 1920×999 and could not be shrunk — the phone-width check at the heart of fix-15 remains unproven (browser limit, not a page verdict).
NEW DESKTOP DEFECT: the bottom navigation pills ("‹ prev day", "Keep reading ◆", "next day ›") are clipped at the bottom edge of the day-view card on every block of every day, and the page does not scroll to reveal them (buttons still work, text legible).
Minor: month grid shows a sixth row of empty unnumbered cells (Dec 1–5).

## Scope — one defect, one unproven leg, one minor, one regression sweep

### Item 1 — Bottom nav pills clipped, page will not scroll (THE defect)
The pills' bottoms are sliced off at the day-view card's bottom edge on EVERY block of EVERY day at 1920×999, and there is no way to bring them fully into view — the page does not scroll.
**Read this before you touch anything:** fix-15's maker DELIBERATELY pushed the wisdom nav below the fold (`#dayScroll #wisdomBanner.sb-nav{margin-top:160px!important}`) claiming it was "reachable by one deck scroll". The eye proves that claim false on the filed bytes — the page does not scroll to reveal them. Do not repeat that mechanism. Find the ROOT CAUSE: why do the pills sit below the card's edge, AND why can't scrolling reach them? (Suspects to check, not conclusions: the nav lives inside a container with `overflow:hidden` and no scroll path; the deck scrolls but the nav is outside the scrollable region; the card's height is fixed and the nav overflows it; a margin pushes the nav past the card's clipping edge while the scroll container ends above it. Measure, don't guess.)
**The fix (maker's choice of mechanism):** the three pills read WHOLE at rest on every block of every day at 1920 AND 390 — bottoms not sliced, no scroll needed to see them — with the weather pill still one line and 4px clear and the day-teach + store line still whole at rest on all seven days at 390. If the honest fix is "the nav must live inside the scrollable deck" or "the card must grow / the deck must scroll", do that. Do not nudge pixels and hope; do not hide the pills; do not shrink the quote below its 32px sweet spot to buy room.

### Item 2 — REAL phone-width pass at 390 (the unproven heart of fix-15)
Fix-15's desktop leg passed, but phone width was NEVER verified. VM browsers are alive again (probe 07:32Z, re-confirmed 01:59 MST) — this leg runs in VM Playwright Firefox at 390×844, by real tap.
Prove on the FIXED bytes at 390: wisdom whole all 7 days Nov 15–21 in BOTH font states (fonts-loaded Great Vibes vs no-webfont fallback — the no-font state is the worst case, ~107px tighter on Sat 21), day-teach + store line whole at rest, weather pill one line 4px clear, Your Worlds six tiles readable (labels whole, no cover overlap), greeting true to the time of day, whole 9-block deck reads well, no clipping anywhere, no horizontal overflow (scrollW 390).

### Item 3 — Month-grid sixth row (minor, eye-flagged)
A sixth row of empty unnumbered cells (Dec 1–5). Inspect it, ADJUDICATE IN WRITING whether it is actually wrong, fix only if it is genuinely wrong. A month grid showing the next month's leading days as empty cells may be correct by design — do not "fix" a correct grid. If it IS wrong (cells that should not exist at all, per §7 "the next month's numbers do not bleed in — the other month's numbers are GONE entirely"), fix it by the same rule.

### Item 4 — Full fix-15 regression at 1920 AND 390
Wisdom whole, greeting correct, Worlds row whole, deck reads well, every button lands on the right place (BUTTON DESTINATIONS RULE: click through the buttons and verify each lands current and relevant, not stale, not a dead end — a page passes only when its buttons go where they should). Keep-reading last-slide behaviour, journal empty-state line in full at 1920, news badges 0, worlds-row badges real-or-gone (fix-14's five nulls intact), elite-booking logic intact (only-open times, 15/30/60, +60-min notice, +30-min buffer, no full slot list), seven day covers byte-identical to fix-15, 0 page errors in both font states.

## Verify-first (maker) + independent checker
- Maker: reproduce the defect on the BASE bytes first (render at 1920 AND 390: the nav pills clipped on every block, page not scrolling — measure the geometry: pill rect vs card rect vs scroll container, and WHY scroll can't reach them), then fix, then re-prove on the fixed bytes before filing.
- Checker (independent, did not build): re-derive the byte-diff from the filed blob (should be only this repair on top of the fix-15 tip); render at **1920 AND 390**; nav pills whole at rest on every block of every day at both widths; **7-day sweep at 390** (days 15–21, both font states, day-teach + store line whole at rest, weather pill one line 4px clear); **whole-deck walk at 390** (all 9 slides in order, Your Worlds geometry, cover overlap none); wisdom judged by eye at 1920 (48px, beautiful) and 390; greeting true to the time of day; month-grid adjudication checked against the bytes; laws delta 0; inline JS parses; staged link serves the filed blob (sha256 match from the checker's own fetch).
- Verdict: PASS or GOES BACK, with the evidence. The captain's eye follows the checker. No link to Shawn until it reads whole on a phone too.

## Filing (maker)
- Fetch the base via the git blob API (`gh-direct.py` only — NEVER the GitHub connector tools, they pop approval cards). Verify size + sha256 against the brief before editing.
- File the fixed HTML onto the new branch `calendar/day-followon-fix16-20261119` via `gh-direct.py` (contents API returns EMPTY content for files >1 MB — this file is ~402 KB, fine — but verify via the git blob API, never contents-GET alone; never stage multi-MB base64 payloads to disk — pipe base64 → jq via process substitution; the `gh-app-api` token cache truncates to 0 bytes repeatedly — fall back to `gh-direct.py`).
- Verify the filed blob by fresh blob-API read-back (size + sha256), then curl the staged link with a browser User-Agent and confirm the staged bytes hash to the filed blob.
- Write MAKER-REPORT.md in `~/workspace/team-nitro/calendar-day-followon-fix16-20261119/maker/` with: filing identity (branch, tip, blob, size, sha256, staged link), defect reproduction (geometry, root cause), the fix (mechanism + why), re-proof tables (1920 + 390, 7-day sweep both font states, deck walk, month-grid adjudication), laws delta 0, §11 check in writing, scorecard, files. Keep proof (scripts + screenshots) under `maker/proof/`.

## Environment warnings (proven, do not re-learn)
- VM browsers flap (dead/alive); re-test before any browser leg. Render legs run in VM Playwright Firefox at 1920 AND phone 390 (the cloud browser is fixed ~1920 — it cannot do the phone leg). Chromium in the VM needs the localhost forwarder (`~/workspace/project-intelligence/proof/pi-h1-evidence/h1-proxy-forwarder.py`, 127.0.0.1:18080) + `ignore_https_errors=True`; kill it after use. Firefox in the VM silently never fires Supabase reads on some sections — not relevant here (this page is self-contained), but judge only what the browser actually rendered.
- EPERM write flake: verify every write by size + sha; Python writes EPERM/0-byte — use Node or the file tool; never `python3 … > file` (exits 120 silently); never move a temp over a live file unchecked; stage under `~/workspace/`, never /tmp.
- The calendar file is ~402 KB: check its size first and edit byte-safely (Buffer ops). A string round-trip once silently dropped 35,444 B from the 10.4 MB Personal file — never round-trip a big file through strings blindly; verify by sha after every rebuild.
- VM clock is UTC — the greeting in any in-VM render follows the VM's clock, not MST.
- READ AS A READER: read the page top to bottom as a reader at both widths and call it broken when it doesn't present well, even if every part ticks. Do not remove or move anything the brief didn't ask to touch. The page he sees is the scope.
- One hour max for the edit round. Prove every tap before filing.
