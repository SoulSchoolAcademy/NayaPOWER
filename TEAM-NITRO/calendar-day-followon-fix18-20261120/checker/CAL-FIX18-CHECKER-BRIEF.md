# CAL-FIX18 — CHECKER BRIEF

**Round:** Calendar day-followon fix-18 · **Date:** 2026-11-20 (Shawn live on a voice call, walking the Calendar day view)
**Coordinator:** Team Nitro (fix-18) · **Status:** checker to spawn — maker filed, verify independently

## 1. Identity — verify from fresh bytes, never from the maker's word

| Item | Value |
|---|---|
| Base branch | `calendar/day-followon-fix17-20261119`, tip `a955d7fa2299a6667ba70215dd4347c1de80386e` |
| Base file | `TEAM-NITRO/day-view-v18-fix-20261117/the-ultimate-calendar-v18-fix.staged.html` |
| Base blob | `f4c05109531f8b737891a43f6ea6bdcef84eddc9`, **410,236 B**, sha256 `1f798b65dfa557a4e4e20472e3d56e2bda29fd69912481338b3bb6b2bc602887` |
| Fix-18 branch | `calendar/day-followon-fix18-20261120` |
| Fix-18 commit (maker's claim — VERIFY) | `ffd220c7d7d54fbbfc08c82ceed793ce1b0968a3`, parent = fix-17 tip |
| Fix-18 blob (maker's claim — VERIFY) | `f7b14ce75d590738a9efb87a4fa056ee98f3561d`, **413,386 B**, sha256 `52ff950fb4dfeb942415c96ee2af393b815e06e9019c77a9758121a9f40770cc` |
| Staged link (maker's claim — VERIFY) | `https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/day-view-v18-fix-20261117/the-ultimate-calendar-v18-fix.staged.html&ref=calendar/day-followon-fix18-20261120&cb=f7b14ce75d590738a9efb87a4fa056ee98f3561d` |

**Your first act:** fetch the filed blob via the git blob API AND curl the staged link with a browser User-Agent. Size + sha256 must match the maker's claimed blob on both. If they don't match, stop and report it — do not proceed to render checks on bytes that aren't the filed bytes.

**Read first, before any check:**
- `~/workspace/team-nitro/calendar-day-followon-fix18-20261120/brief/CAL-FIX18-BRIEF.md` (the maker brief + addendum — the three items, the anchors, the acceptance).
- `~/workspace/team-nitro/calendar-day-followon-fix18-20261120/maker/MAKER-REPORT.md` — the maker's claims. **Read it to know what to re-prove, never to take its word.** Your probes are your own; a claim is proven only when YOUR measurement lands it.
- `~/workspace/team-nitro/THE-NAYA-DESIGN-LAWS.md` (the rule book — read FIRST, before any design judgment), then `~/workspace/team-nitro/THE-PLAYBOOK.md`, `~/workspace/team-nitro/DESIGN-INTELLIGENCE-REPORT.md`, `~/workspace/team-nitro/THE-ANATOMY-OF-A-SMART-APP-PAGE.md` with `~/workspace/team-nitro/THE-HEART-OF-THE-MACHINE.md`, `~/workspace/team-nitro/THE-ULTIMATE-ORIENTATION.md`, `~/workspace/team-nitro/THE-ARMY-TRAINING.md`. Smart Block doctrine SN-3336 · The Icon Is the Standard SN-3337.
- Fix-17 harness (reuse/extend, don't rebuild): `~/workspace/team-nitro/calendar-day-followon-fix17-20261119/checker/proof/prove17c.py`, `daysweep17c.py`, `focus17.py`. The maker's harness is under `~/workspace/team-nitro/calendar-day-followon-fix18-20261120/maker/proof/` — you may read it for method, but your probes must be your own runs on the filed bytes.

## 2. What you must prove (all four legs: 1920 + 390 × Firefox fallback + Chromium fonts-loaded; 0 page errors everywhere)

### Item 1 — "November 2026" centered at the top of the header, more spacing
- Monthline renders as ONE line, "November 2026", at both widths, both browsers. Measure: centre offset (monthline cx − viewport centre) in px; November→2026 gap in px; line count.
- Neighbours untouched: "Friday 20" left; time row directly under the monthline, centred; BACK TO MONTH left; Your Stats + orb right.
- **Read as a reader:** does "November 2026" read as the centered title line at the top of the header at 390 AND 1920? Shawn's words were "center it at the top of the header". The maker did NOT reorder (monthline stays in its column above the time row; "Friday 20" keeps its place) and names this as a judgment call in its §2. Judge it: if the result does not read as "centered at the top of the header" at either width, that is a GOES BACK with the exact reorder needed — do not wave it through because the numbers are 0px.

### Item 2 — "396 HZ" gone from the top header, wisdom untouched
- Rendered header text contains no `HZ` / `396` at either width, either browser (element census on the rendered DOM, not a grep — the header 396 was runtime-rendered from `DAY_FREQ`).
- Wisdom line (`#dayTeach`) byte-identical AND rendered identical, both 396 Hz mentions intact. `WISDOM` quote untouched. Month screen `monthName` untouched.

### Item 3 — "Change cover" pill only where a cover is actually visible
- **Per-slide census on the filed bytes, all four legs:** pill shown/hidden per slide (0 Wisdom, 1 Notifications, 2 Journal, 3 Worlds, 4 News Hub, 5 Appointments, 6 Summary, 7 Naya Notes, 8 Smart Notes). Notifications pill-absent at both widths, both browsers. Pill hit-testable where shown.
- **Your own cover-visibility measurement:** do NOT take the maker's census on trust. Measure per slide, per width, whether the cover is actually visible (the maker's pixel-diff cover-on vs cover-off method is documented in its §1 including two false methods — hash-only and global-freeze — that lie; do not repeat them, and do not trust a method you haven't validated yourself).
- **Adjudication point 1 (the maker's open question — decide it):** the maker found the cover is rim-only at 1920 even on Wisdom and Worlds (plainly visible only at 390), yet kept the pill on Wisdom + Worlds at both widths, arguing (a) the addendum names Wisdom as keeper without width qualification, (b) those are the cover's slides by design, (c) a width-dependent pill would kill the function on desktop. Rule on this: does the pill on Wisdom/Worlds at 1920 satisfy item 3's "actually visible to change" bar, or does it fail it? Give a verdict with your own 1920 measurements, not a shrug. If it fails, the fix is exact (what changes, where).
- **Adjudication point 2:** at ≤560px the pill now shows on only one slide (Worlds) — Wisdom hidden per fix-17, the rest per item 3. Confirm the combined outcome is what the two instructions produce, and name it plainly either way.
- Tap test: pill opens the native file picker where it remains (Wisdom 1920, Worlds 1920 + 390); hidden/not clickable elsewhere.

### Scope + fix-17 hold
- Scope proof (your own): fixed-minus-maker's-block + Hz-reinsert == base; COVER_DAY / WISDOM / DAY_FREQ / monthName / booking / badges byte-identical; fix-17 block intact.
- Fix-17 hold: 7/7 wisdom sweep + 9/9 deck at 390 FF and 1920 Cr; buttons by real tap (Keep-reading advances day, prev-day returns it, BACK TO MONTH → 42/30/12); Appointments nav 2px clear held; month grid 42/30/12, row 6 blank; 0 page errors.
- **Adjudication point 3:** at 390 in the Firefox fallback the maker reports the monthline is 280px wide in a 240px column, overflowing 20px a side into clear black field, `docScrollW` stays 390. Verify: no horizontal scroll, no clipping of any neighbour, reads clean as one line in both font states. If it clips or scrolls, GOES BACK.
- **Adjudication point 4:** the 390 header compresses 32px (monthline 2 lines → 1) and the deck moves up with it. Verify deck geometry whole in all four legs — no new collision, no clipped nav, Change-cover clearances held.

## 3. Laws + §11

- Run the real `check-design-laws.py` (`~/workspace/team-nitro/check-design-laws.py`) on base and fixed. Laws delta must be 0. Report the FAIL/WARN counts on both sides.
- §11 check in writing in your report (five gates + design check). A checker report without it is incomplete.
- Read the page as a reader, top to bottom, at 1920 and 390, in both font states — screenshots named and read, not just filed.

## 4. Probe lessons — recorded so nobody re-learns them (fix-17 checker §8 + fix-18 maker §1)

- Slide transitions take >900ms to settle — wait **≥2s after every deck navigation**.
- Day re-opens on the last-viewed slide — per-slide targeting via the dots (`#dayScroll .sb-dots button`).
- VM clock is UTC — greetings read against UTC, not MST.
- Measure overlap against the viewport/content, never against a scroll container.
- Firefox in this VM = no-webfont fallback (worst case). Chromium 156 needs the localhost forwarder (`~/workspace/project-intelligence/proof/pi-h1-evidence/h1-proxy-forwarder.py`, 127.0.0.1:18080) + `ignore_https_errors=True`; kill the forwarder by PID when done (never `pkill -f`). VM browsers flap — re-test at the start of your round; if a browser is dead, say so plainly and do not claim that leg's proof.
- Pixel-diff cover census: hash-only comparison lies (ambient animation drift); a global `*{animation-play-state:paused}` style tag lies worse (freezes slide entrances at opacity 0). The maker's corrected method is pixel counts with a drift baseline, animations paused per-slide via `document.getAnimations()` after the settle, no persistent style tag. Validate your own method before trusting its numbers.

## 5. Filing — the established path

- `~/workspace/team-nitro/gh-direct.py` only (in-memory token; `gh-app-api`'s token cache truncates under the EPERM flake). Blob API for read-back. Verify every write by size + sha. Never `python3 … > file` (exits 120 silently). Never move a temp over a live file unchecked. Stage under `~/workspace/`, never /tmp.
- Never write a token or PEM to a log, a file, or a command line.
- Round dir: `~/workspace/team-nitro/calendar-day-followon-fix18-20261120/` — checker report at `checker/CHECKER-REPORT.md`, proof scripts + screenshots under `checker/proof/`.

## 6. Verdict + report back

File `checker/CHECKER-REPORT.md` and report back to the coordinator with a verdict of **PASS** or **GOES BACK**:
- Filing verification (branch tip, blob, staged sha — match or mismatch).
- Per-item proof with YOUR measurements (rects, px, census tables), all four legs.
- Your ruling on adjudication points 1–4, each with its evidence.
- Laws delta + §11 check in writing.
- Fix-17 hold re-proof.
- Anything thin, pre-existing, or unproven — named plainly, never hidden.
- If GOES BACK: the exact fix list (what changes, where, measured how) — one item per line, nothing vague.

No merge, no live deploy, no message to the user. The captain's eye follows only a PASS. The round is held from shipping until the captain confirms the list is complete.
