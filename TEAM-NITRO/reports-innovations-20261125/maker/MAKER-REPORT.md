# MAKER REPORT — Reports in Innovations format (2026-11-25)

Maker round, one-hour max. Started 2026-11-25 ~18:37 MST (01:37 UTC), staged ~18:54 MST (01:54 UTC).

## Receipts

- **Staged link:** https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO%2Freports-innovations-20261125%2Freports.html&ref=reports-innovations-20261125&cb=f89e376c20dc608d4d3eae0fa85d28cfdd5d5790
- **cb:** `f89e376c20dc608d4d3eae0fa85d28cfdd5d5790` (branch tip commit)
- **sha256:** `fe7fe13852cc3b2267d8660ab835333af00f3ed8ce42ea56ecd370497ade694f`
- **Size:** 39,479,655 B
- **Branch:** `reports-innovations-20261125` (repo SoulSchoolAcademy/NayaPOWER)
- **Commit (tip):** `f89e376c20dc608d4d3eae0fa85d28cfdd5d5790` (second commit; first commit `8b974c5a7a93d52968e358f557fd486942600b5a`)
- **Blob:** `e0f7ef0efcc21a6d443f48a2d43842bdd3c6f920` (git blob sha1, verified: blob-API read-back size 39,479,655; staged curl size + sha256 identical to the filed bytes)
- **File:** `TEAM-NITRO/reports-innovations-20261125/reports.html`
- **Build script:** `maker/build-reports.cjs` (local workdir only; reruns the whole build from the harvested sources)
- **Live `nayanet.app/rooms/reports` untouched. Nothing live, nothing to Shawn.**

## What was read first (per Shawn's order)

`THE-NAYA-DESIGN-LAWS.md`, `THE-PLAYBOOK.md`, `DESIGN-INTELLIGENCE-REPORT.md`, `THE-ULTIMATE-ORIENTATION.md`, `THE-ANATOMY-OF-A-SMART-APP-PAGE.md` — all read before any work.

## Harvest (never invented)

| Source | Receipt |
|---|---|
| Innovations fix9 master | `https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO%2Ftop-ten-innovations-20261123%2Finnovations.html&ref=eye-verdict-fix-20261124-fix9&cb=c0f45470a6b50c18f9c2b381ace5cf4055faa1be` — 38,342,271 B, sha256 `23e4f14a357bc843551b19fd379873f7111f7f23fb3447ba868f8f5d43d8d9b8` (matches the brief exactly) |
| Live Reports room | `https://nayanet.app/rooms/reports` — 354,774 B, sha256 `1be90139fdf64dfbbd8d6adf8e3818c047e3827f3a1741753eed0c8a33bdad08` (matches the brief exactly). Its real content: only 2 sample daily reports (Sep 30, Oct 1) + 1 weekly (W40); the rest it reads live from Supabase. |
| Supabase daily reports (READ ONLY — no rows touched) | Table `hub_daily_intelligence_reports`, 58 rows, 2026-09-27 → 2026-11-23, every row with `body_md` (1,100,460 B JSON). Read through the same public anon key the live page itself uses. |
| SN-4866 (latest daily, 2026-11-24) | Canonical file `BRAIN/05-MEMORY/SMART-NOTES/2026/11/24/REPORT/SN-4866/IB-SMART-NOTE-20261124-sn4866-daily-intelligence-report-2026-11-24.md` (11,377 B). Not in Supabase yet — that is why the live room does not show Nov 24. |
| Nov 24 notes SN-4853–SN-4865 | 13 canonical files under `BRAIN/05-MEMORY/SMART-NOTES/2026/11/24/LESSON/SN-48xx/`, parsed verbatim into the viewer. |

## The build — what is in the deck

- **60 slides, newest first:** 59 daily reports (Nov 24 SN-4866 first, then Nov 23 → Sep 27 from Supabase) + Weekly W40 last. Each slide = the report's date + title + nutshell (harvested: Nutshell section, else "The big shift", else first paragraph — never invented).
- **Flip-through:** the fix9 deck mechanics untouched (Back/Forward, cover, depth tap-in). `GROUPS` replaced wholesale; frame code otherwise byte-identical except the named swaps below. Proof: 3,215 of 3,334 lines in the built file are verbatim lines from fix9; the differing lines are the GROUPS data block, the retitles, the END/portal change, the eye-fix CSS block, and the drawer/viewer JS.
- **Highlighted viewer (the matrix):** tapping a slide's red N opens the depth view with that report's sections in matrix order where they exist (Nutshell → What It Means → Why It Matters → How to Apply, labelled "How to Apply — what changes now" with its true name kept). On the Nov 24 report the depth view also lists all 13 notes as buttons; tapping one opens the fullscreen matrix viewer (`openNoteViewer`) with the note's full matrix in the required order: In a Nutshell → What It's Not → Child → Grandma → What It Means → Why It Matters → How It Connects → How to Apply → What's In It For You, each with its GitHub path + Hub link + live-status line.
- **Sidebar (two ways in, 1 of 2):** a ☰ drawer (top-left, obsidian ball button) with a **Reports** entry (flip through them all), a **Daily Intelligence Report** entry (latest, Nov 24, 2026), a **day dropdown** (dropdowns over walls of tags — 60 days as a `<select>`, not a wall of links), and Calendar / Intel Today / Hub / Dashboard / Personal.
- **Calendar (two ways in, 2 of 2 — this page's half):** every report's depth carries a "See this day in the Calendar" section with the link `https://nayanet.app/calendar?day=YYYY-MM-DD`, and this page RECEIVES `?day=` / `&day=` / `#day=` on arrival and opens that day's slide (code present; see NOT-DONE for the unproven part). The calendar's own receiving end is specced below, not built (per the brief).
- **Shawn's Innovations eye fixes (2026-11-25 ~18:13–18:22 MST), carried:** bigger N on every board (64px, up from 32px centre / 40px boards — override `#reports-eye-fixes-20261125`); centered text (headings, subheadlines, body on boards); subheads 20px / body 18px with NOTHING below 18px on the boards (override rules; see the checker note below for the inherited frame declarations); one size system, one grid (centered, single scale on boards); full-screen corner icons remade as real objects (obsidian ball, radial gradient, white 2.6-stroke glyph, 46px, slow 60s orbit ring — never a flat thin outline); full screen = the SAME template just full screen (`#fsView` edge-to-edge: 100% width, 100dvh, radius 0, same template); the END board uses the same slide template; the end goes back to the LOGIN — `goToPortal()` and `beginAgain()` both now navigate to `https://nayanet.app/`, the end button reads "Back to login", the end N's aria-label reads "Back to login — the portal, nayanet.app", and "Back to The template" is now "Back to the reports". Zero user-visible "Begin again" (2 hits remain, both code comments — one inherited from fix9, one in my own fix note). One red centerpiece per view: the red N only; my additions add no red.

## Maker self-check (in writing)

- Flip-through works — NOT browser-proven. Static proof only: `GROUPS` JSON parses (60 groups), all 5 inline `<script>` blocks pass `node --check`, `renderSlide`/`openDepth` untouched from fix9. The checker must tap through it.
- A report opens in the highlighted viewer with the full matrix — NOT browser-proven (same caveat). Static proof: depth sections present in order per group (Nov 24: Nutshell / What It Means / Why It Matters / How to Apply — what changes now / Hook / Human / Child / Grandma / Naya / shape note / full report); `openNoteViewer` + depth note-button injection present in code; all 13 note matrices parsed (see below).
- Daily reports present by day — YES, by bytes: 59 daily slides, dates Sep 27 → Nov 24, 2026, newest first; each slide title carries its date.
- Sidebar entries land — NOT browser-proven. Static proof: drawer markup + `goSlide` wiring + day `<select>` present.
- Calendar links carry correct `&day=` URLs — the canonical forms are in the build (drawer note + per-report depth section); the receiving-end code (`dayFromUrl`, `jumpToDay`) is present. NOT browser-proven.
- 0 page errors — NOT proven. No live browser exists in this seat; no render was run. The checker must establish this.
- Design-laws check — see below. Violations named plainly, with laws cited.

## Design-laws check (`check-design-laws.py`) — build vs fix9 baseline

- **fix9 baseline: 29 violations, 0 warnings — exit 1.**
- **Reports build: 29 violations, 3 warnings — exit 1.**
- **The 29 are IDENTICAL, line for line, inherited from the fix9 frame** (gray `--dim`/`--muted` variables §2.2, and sub-17px `font-size` declarations §2.3 down to 8.5px, lines 165–1135 of the frame CSS). My build introduces ZERO new violations: my added CSS uses only 18px/20px and white text. The eye order ("nothing below 18px anywhere on the boards") IS met on the boards by the later override rules — but the machine checker greps declarations, so the frame's original sub-17px rules still flag. Fixing the checker result means a frame-level CSS pass on fix9 itself, not a Reports-round rewrite; I did not rewrite the frame, per harvest law (§11, §14).
- **The 3 warnings are false positives from harvested content, not CSS:** the Nov 23 report body contains the prose phrase "color: on tonight's tip…" (line 1589 of the built file, inside embedded report text). The checker flags it "by eye" as a possible text color; it is report prose, not a style. Named here so the checker does not chase it.

## Live-before-delivery — the note links, honestly

SN-4866 itself says delivery of the Nov 24 report is **HELD**: "the report's notes must be LIVE on the Hub, where he can see and open them, before the report is sent — and the Hub is not yet live with the new presentation." The staged page obeys that: it never claims the Nov 24 report is delivered.

- **SN-4853–SN-4865 (13 lessons):** filed on GitHub, verified by read-back per SN-4866. The viewer links each to its canonical GitHub path (`BRAIN/05-MEMORY/SMART-NOTES/2026/11/24/LESSON/SN-48xx/...`) and to `https://nayanet.app/hub` (the feed). **No per-note deep link to a live Hub note exists** — the live room links only to the Hub feed, never to a single note — and that gap is stated in the viewer, not hidden. Hub liveness of these notes was NOT verified by me (no browser); SN-4866's HELD status is carried verbatim.
- **SN-4852:** a TEST note — carried as a status item in the viewer, never as a lesson (per SN-4866).
- **SN-4841–SN-4851: NOT live and named, not hidden.** SN-4866: "not on GitHub — Supabase-only rows with github_path null." They are not listed as live notes anywhere in the build.
- **SN-4731–SN-4746:** SN-4866 records a missed Hub rebake (in the table, not on the Hub). Carried as owed, not claimed done.

## Matrix completeness (counted, not claimed)

- Each Nov 24 note fills **6 of 9** matrix slots from its canonical file (Nutshell, Child, Grandma, What It Means, Why It Matters, How to Apply ["What changes now"]). The other 3 — **What It's Not, How It Connects, What's In It For You — do not exist in the canonical notes** and are shown in the viewer as named holes ("Not filed in this note — nothing invented to fill it"). The brief's "every section filled" cannot be met without inventing text; harvest law (§11) wins and the holes are named. Filling those three slots across the notes is a distillation-round job, not a maker-round invention.
- Report-level depth: daily briefings are not intelligent blocks. Their depth shows their own sections in matrix order where present, then their remaining sections, then an "About this report's shape" note naming the matrix slots that report does not carry, then the full report text (capped at 3,000 chars with a pointer to the live room).

## Calendar-intake SPEC (the receiving end — for the calendar round, not built here)

The staged Calendar cannot receive `&day=` today (no date intake, no live table read). What it needs:

1. **URL shape (live):** `https://nayanet.app/calendar?day=YYYY-MM-DD` (first param `?day=`; appended as `&day=` when the calendar URL already carries a query string). Staged equivalent: the staged calendar URL + `&day=YYYY-MM-DD`. The Reports side already speaks this: its day links are `https://nayanet.app/rooms/reports?day=YYYY-MM-DD` (live) and the staged copy accepts `&day=`.
2. **On arrival, the calendar MUST:** parse `day`, validate strict `YYYY-MM-DD` (reject anything else and fall back to today, saying so); open the month containing that day; open that day's day-view (the 13 doors); highlight that day; never silently reset to today; preserve the day across Back/Forward.
3. **The day's Reports door** in the day-view must link back to `https://nayanet.app/rooms/reports?day=YYYY-MM-DD` for that same day (the round trip).
4. **A day with no report** must still open its day view and say "No report filed that day" — never a dead end, never a silent redirect, never an invented report.
5. **Data:** to mark which days HAVE reports, the calendar needs a live read of `hub_daily_intelligence_reports.report_date` (the same table the live Reports room reads) or of the filed daily reports. Until that read exists, it must accept the day and show the day view anyway, marking report availability as unknown rather than inventing it.
6. **NOT in this round:** the calendar was not rebuilt, per the brief. This spec is the handoff.

## DONE vs NOT-DONE

**DONE:** harvested frame + content (all receipts above); 60-slide flip-through deck; highlighted matrix viewer (depth + per-note viewer, Nov 24 notes); sidebar drawer with Reports + Daily Intelligence Report entries + day dropdown; `?day=`/`&day=` intake on the Reports side; per-day Calendar links in every report; Shawn's Nov 25 eye fixes carried (bigger N, centered text, 18px floor on boards, real-object fullscreen icons, edge-to-edge fullscreen, END → login, no return-to-template path); GitHub filing + blob verification + staged-link byte verification; design-laws check run against baseline.

**NOT-DONE (with reasons, never silence):**
1. **No browser proof of anything interactive** — flip-through taps, viewer taps, sidebar jumps, `?day=` landing, 0 page errors, phone/desktop rendering. Reason: this seat has no live browser. The checker must tap-test every one; nothing here is claimed proven by a render.
2. **Per-note full matrices only for Nov 24** (13 notes). The other 58 days' notes have no per-note matrix in this build; their viewer shows the day's full report text. Reason: harvesting ~58 days × ~13 notes exceeds the one-hour max; the mechanism and the Nov 24 proof are in place for a follow-on harvest round.
3. **Matrix holes** (3 of 9 slots per Nov 24 note; more per daily briefing) — named above, never filled with invented text.
4. **Calendar receiving end** — specced above, not built (per the brief).
5. **Design-laws machine check still FAILs (29, inherited)** — see above; a frame-level pass is owed.
6. **No monthly/yearly slides** — the live room files no monthly/yearly samples as data; inventing them would break harvest law.
7. **Weekly is one slide (W40)** with no sections — that is exactly what the live room files for it.

## Violations / defects named (design laws cited)

- §2.2 / §2.3: 29 machine-checkable violations inherited from the fix9 frame (gray `--dim`/`--muted` text variables; text down to 8.5px in frame chrome). The boards are overridden to ≥18px, but the frame declarations remain. Frame-level fix owed.
- §16: matrix holes (What It's Not / How It Connects / What's In It For You missing from the canonical Nov 24 notes; more missing per daily briefing). Named in the viewer and in the depth "shape" note, never papered over.
- §11 (prove it): all interactive behavior is statically verified only — no browser proof in this round. Stated, not softened.
- Cover images keep their Innovations alts ("Naya Windows…") — harvested images reused as the deck's pictures; their alt text describes the image, not the report. A Reports-cover image pass is owed if Shawn wants his own cover art; nothing was redrawn.
