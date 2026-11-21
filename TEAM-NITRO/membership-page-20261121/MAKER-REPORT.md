# MAKER REPORT — Membership page 2026-11-21

**To:** the captain. **NOT to Shawn.**
**Page:** the membership page — one frame, with the cover in it. Shawn's order, today.
**Staged link (verified first-hand):** https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/membership-page-20261121/membership-page.html&ref=membership/page-20261121&cb=46c44481c36d25b0a081833db7552c35cbacd2fa
**Branch:** `membership/page-20261121` · **Commit:** `f85df46fae0d4452d39f61550f98187ebabf362d` · **Blob:** `46c44481c36d25b0a081833db7552c35cbacd2fa` · **238,066 B** · **sha256 `1e569e11bfbc98b8206e328ae25512dfe20ff76e54f0282fd6528f0c5e9cdf44`**
**Staged bytes:** HTTP 200, 238,066 B, sha256 exact match, `cmp` identical to the filed bytes.
**No merge, no PR, no live touch.** The old fix-8 page is not a source and its link is not delivered.

## THE FIVE GATES
1. **Is it right?** Yes — the page is the frame that works, taken byte-for-byte, with the courses' own data in it. Nothing invented: where data is missing (Masterclass lessons, FAC videos, audio recordings) the page says so honestly instead of faking it.
2. **Is it what they truly need?** Yes — the entrance Shawn settled today: cover frame → table-of-contents frame (one button per lesson) → lesson frame-by-frame; nothing below the TOC; toggle MIXED (default) / ALL VIDEO / ALL AUDIO; no all-text view.
3. **Is it mine to do?** Yes — Shawn ordered the page today; the build stays inside the brief (no login wiring, no payments, no live touch, no bottom bar added — the one-bar question is the captain's call).
4. **Is now the time?** Yes — the frame source, the cover model, and the course data were all harvested and verified before building; the page files cleanly to a new branch.
5. **Can I prove it?** Yes — see below. Byte diff PASS, static audit PASS, design-laws delta 0, render PASS at phone + desktop with a real click-walk, staged link verified first-hand.

## §11 DESIGN CHECK (in writing)
- **Byte diff** (`verify-byte-diff.js`, exit 0 — **PASS**): head styles identical (45,943 B, sha `cb4de85cbf83`); `.naya-frame` div identical; main open tag identical (sha `c716ad0b3717`); `#deckControls` identical (sha `0379f45b6211`); frame scripts differ in exactly the 5 documented word adaptations in `frame-adaptations.json`; header words adapted; 8 scripts total (7 frame + 1 membership).
- **Static audit** (`audit-static.js`, exit 0 — **PASS**): 90 beats; TOC buttons 5 (Academy) + 0 (Masterclass, honest empty room) + 9 (FAC); zero `<a>` tags anywhere on the page; all 26 static `data-mem-go` targets in range; 14 `data-mem-begin` buttons; mode sets correct for every lesson (Academy mixed cover+video+text, video cover+video, audio cover+audio; FAC mixed cover+video+4 text, video cover+video, audio cover+audio).
- **Design-laws machine check** (`check-design-laws.py`): built page 1 violation + 2 warnings; frame source 1 violation + 2 warnings — **delta 0**. The 1 violation is the word "gray" inside the frame's own CSS comment ("is one quiet line, white, nothing gray") — pre-existing in the frame source, a grep false positive, not gray text. The 2 warnings are pre-existing (`color:` in a comment, `color:transparent` on the seal-mark gradient text). New `fpMembership` CSS adds zero violations (font sizes 17/19/24/20px only — 24/20 are the ✦ jewel glyph; no gray).
- **Render** (`render-probe.py`, exit 0 — **PASS**), Playwright Chromium via the localhost forwarder, staged URL:
  - Phone 390×844 + desktop 1440×900: title "Memberships — NayaNET"; 90 beats; exactly 1 `.frame-now`; 6 cover boards (3 page + 3 course); **no horizontal overflow** (scrollWidth 390 / 1440 exactly); **0 JS exceptions**; **0 failed requests to the page's own host** (naya-proof-host — every face, cover, and logo loaded).
  - Click-walk (phone, every step by real click): page cover → Enter Academy → course cover (beat 1) → Enter → TOC (beat 2, 5 buttons) → lesson 1 → lesson cover (beat 3, title "🔱 ACTIVATE YOU / EXPERIENCE ME! Day #1 of the Naya POWER Academy.🔱") → Begin → watch beat (beat 4, YouTube iframe present, player chrome + video title visible) → Back → ALL VIDEO → Begin → watch beat → Next → lesson 2 cover (beat 7, text/audio beats skipped) → Lessons → TOC (beat 2) → lesson 1 → ALL AUDIO → Begin → Listen beat (beat 6) → Lessons → TOC (beat 2). Every transition landed exactly where the brief says.
  - Screenshots (lane): `render-phone-00-cover.png`, `render-phone-01-course-cover.png`, `render-phone-02-toc.png`, `render-phone-03-lesson-cover.png`, `render-phone-04-watch.png`, `render-phone-05-video-next.png`, `render-phone-06-audio.png`, `render-desktop-00-cover.png`. Full log: `render-log.json`.
  - Seen with my own eye in the screenshots: obsidian frame, gold rim, purple jewel, progress pill "1 / 90", "Hello. I'm Naya. Listen to the memberships", "Three courses. One frame. Pick a course — and begin.", the Academy cover art, TOC "Choose your lesson" with numbered day buttons, Back / Next / Keep reading / Lessons in the foot row, footer "nayanet.app — enter. Memberships — learn, grow, and build at hyper speed."

## PROVEN vs UNPROVEN — stated plainly
**Proven:** everything above — byte diff, static audit, design-laws delta, render at both widths with the full click-walk, staged link first-hand.
**Not proven in this VM (environmental, not page failures):** the YouTube player pixels and the Google Fonts. This VM's egress proxy MITMs TLS, so Chromium reports `ERR_CERT_AUTHORITY_INVALID` for `fonts.googleapis.com`, `www.youtube-nocookie.com`, and `i.ytimg.com` (10 failed requests per viewport, all third-party, all the same cause). The page's own assets all loaded; the YouTube embed still rendered its title card in the screenshot. The frame source carries the same external dependencies. A real browser — his eye — is the proof for the player and the fonts.
**Frame-inherited behaviour, noted not fixed (One-Build Law — the frame is not redesigned):** the topbar title truncates long lesson titles ("🔱 ACTIVATE YOU / EXPI…") — the frame's own `.frame-title` ellipsis; the full title reads on the lesson cover and the sub reads below the video.

## OPEN POINTS (for the captain's call)
a. The frame carries no bottom bar; none added (brief scope). The Eleven Laws law-3 one-bar question (ADD · PERSONAL · BUSINESS · WORLDS · ECOSYSTEM · CONNECT) is the captain's call.
b. wirePlay's 15-paragraph agreement speech is carried verbatim as dead code (its listener is severed by wireFrame8's clone — the frame's own F4 comment proves it). A membership reading is NOT invented; replace it only when one is recorded.
c. Academy day 3/5 nutshells keep filed maker-note wording verbatim ("Headline from the Academy's own five-day progression; the video's own title shows in the player.") — harvested data, not reworded.
d. Login/feature-page wiring follows after Personal is unfrozen (not this round). Payments not built (ladder is context only).

## LANE FILES
`~/workspace/team-nitro/membership/page-20261121/` — `membership-page.html` · `build-membership-page.js` · `verify-byte-diff.js` · `audit-static.js` · `render-probe.py` · `render-log.json` · `render-*.png` (8) · `beat-index.json` · `frame-adaptations.json` · `course-data.json` · `sa-cover-harvest.css` · `frame-source-agreement.html` · `cover-model-personal.html` · `course-data-source.html` · `file-membership-page.py` · `diag-toc.py` · `BRIEF-MEMBERSHIP-PAGE-20261121.md` · `HARVEST-MANIFEST.md` · `MAKER-REPORT.md` (this file).
