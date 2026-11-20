# CAL-FIX17 — MAKER BRIEF

**Round:** Calendar day-followon fix-17 · **Date:** 2026-11-20 (VM clock UTC; user asleep, silent work)
**Coordinator:** Team Nitro (fix-17) · **Status:** maker to spawn

## 1. Identity — verify before you touch anything

| Item | Value |
|---|---|
| Base branch | `calendar/day-followon-fix16-20261119`, tip `572265f25d80146fb9d8a1ff7f3bb56215143f0d` (verified live by the coordinator: commit message "calendar fix-16: checker report — GOES BACK, Change-cover collides at 390 in three places; fix-17 owed on §9 list") |
| Base HTML commit | `360056cb4ebbdd93d7397095bacea70354bdb599` (parent fix-15 tip `cf9e1132e4540e978fb5b94255b438b91bb149e9`) |
| Base file | `TEAM-NITRO/day-view-v18-fix-20261117/the-ultimate-calendar-v18-fix.staged.html` |
| Base blob | `cc67fbf98388fbcbcf26287d82f3a81eb9d5d7c3`, **407,135 B**, sha256 `ffc03030c555f034dd1608d3f78996d8c6455a963462bec5e51b64fa8e548ca3` |
| New branch | `calendar/day-followon-fix17-20261119` (create from the fix-16 tip) |
| Work in ONE file only | `TEAM-NITRO/day-view-v18-fix-20261117/the-ultimate-calendar-v18-fix.staged.html` |
| Staged link (after filing) | `https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/day-view-v18-fix-20261117/the-ultimate-calendar-v18-fix.staged.html&ref=calendar/day-followon-fix17-20261119&cb=<new-blob>` |

**Read first, before any edit:**
- `~/workspace/team-nitro/calendar-day-followon-fix16-20261119/checker/CHECKER-REPORT.md` (26,219 B) — **§9 is your exact fix list; §6 is the defect evidence with rects; §8 carries the probe lessons.** Do not start from the summary below alone.
- `~/workspace/team-nitro/calendar-day-followon-fix16-20261119/maker/MAKER-REPORT.md` — how fix-16 was built (one 5,368 B CSS block appended before `</style>`; `fixed-minus-block == base`).
- `~/workspace/team-nitro/calendar-day-followon-fix16-20261119/maker/proof/fix16-block.css` — the fix-16 block; your fix builds on it, never rewrites it.
- `~/workspace/team-nitro/calendar-day-followon-fix16-20261119/checker/proof/cc-probe.py` + `struct-probe.py` — the Change-cover button's structure and ancestry (single absolutely-positioned element, child of `#dayScroll`).
- `~/workspace/team-nitro/calendar-day-followon-fix16-20261119/checker/proof/cc-walk.py` + `appt-focus.py` — the checker's Change-cover measurement harness (reuse/extend for your own proof).

## 2. The design law — read before you build

**Read FIRST, before any design work, in this order:**
1. `~/workspace/team-nitro/THE-NAYA-DESIGN-LAWS.md` — THE RULE BOOK (Shawn's order 2026-11-17 15:15Z). MUST / MUST NOT, the text laws, the 25/19/17 scale, the §11 check. If it conflicts with anything else, it wins unless Shawn's newer word says otherwise. The coordinator has read it for this round; you read it yourself before you build.
2. `~/workspace/team-nitro/THE-PLAYBOOK.md` (the HOW)
3. `~/workspace/team-nitro/DESIGN-INTELLIGENCE-REPORT.md` (the WHY)
4. `~/workspace/team-nitro/THE-ANATOMY-OF-A-SMART-APP-PAGE.md` (the MAP) with `~/workspace/team-nitro/THE-HEART-OF-THE-MACHINE.md` (why the map works)
5. `~/workspace/team-nitro/THE-ULTIMATE-ORIENTATION.md` (who we are)
6. `~/workspace/team-nitro/THE-ARMY-TRAINING.md` (how the army works)
7. Smart Block doctrine **SN-3336** · The Icon Is the Standard **SN-3337** (the emblem `NAYA_ICON.png` is the north star for all art — every element judged against it; real objects, real materials, real light with volume, real depth; nothing flat).

**The laws that bind this round:** harvest first, never invent — take the working thing verbatim; don't touch what he didn't ask to touch (§9: fix the button's placement at ≤560px; do not redesign any slide, do not touch the nav clearances, do not change any wording, color, or font size); the page he sees is the scope; read as a reader; do it right the first time; §11 check in writing in your maker report (the five gates + the design check — which reference object, hover every object, gray-text grep, size grep, flow check). A maker report without the §11 answers is incomplete. If a law and this brief conflict, the law wins — stop, name the conflict, follow the law.

## 3. The go-back — one floating button, three collisions at 390 (checker §6)

The "Change cover" button is a single absolutely-positioned element, a child of `#dayScroll` (the deck container), floating over the deck on every slide. Its position trails the on-slide nav by ~31px, so wherever a slide's content runs long, the button lands in a band another element already occupies. At 1920 it sits at the right (x1635, y795–835) clear of everything — no collision in any 1920 leg. **At 390 it collides on three slides.** All three share one root cause and one fix: **fix the button's placement at ≤560px.**

### Defect 1 — Wisdom slide, 390, fallback state: Change cover half-hidden behind the weather pill (NEW in fix-16)

| Day | Quote lines | Nav | Change cover | Weather pill | Collision |
|---|---|---|---|---|---|
| 15, 16, 19, 20 | 5 | 703–747 | **778–818** | 804–840 | **bottom 14px hidden behind the weather pill** |
| 17 | 4 | 670–714 | 745–785 | 804–840 | none (fully visible in the gap) |
| 18 | 6 | 736–780 | **811–851** | 804–840 | hidden behind weather pill + frame |
| 21 | 6 | 755–799 | **830–870** | 804–840 | hidden behind weather pill + frame |

Measured in the Firefox fallback sweep, all 7 days. On the fix-15 base the wisdom nav sat at 985–1045 (below the fold) and Change cover sat at 1068–1108 — below the fold, invisible, no collision. Fix-16 pulled the nav (and the button trailing it) into view and into the weather pill's band. In the Chromium fonts-loaded state the stack is shorter (nav 633–677) and there is no collision — **the defect is fallback-only, which is exactly the worst case.** The fix-16 maker's eye screenshot for wisdom at 390 was day 21 — the one day the button hides entirely — so the reading missed it. **You must measure ALL 7 days, not one.**

### Defect 2 — Appointments slide, 390, BOTH browsers, BOTH font states: Change cover covers the "Smart Meet" pill (pre-existing, but claimed whole)

- Smart Meet pill rect 678–737; Change cover rect 696–736; `elementFromPoint` at the pill's center AND bottom returns `BUTTON.pill:Change cover`. Only the top ~18px ("Sma…") is visible; the pill's text cannot be read and its lower two-thirds cannot be tapped (taps land on Change cover).
- Re-measured on the fix-15 base bytes with the same harness: identical rects — it predates fix-16, and fix-16's exemption restored it byte for byte.
- **Do NOT repeat the fix-16 maker's false claim:** "the Smart Meet pill reads whole at 390 (2px spare, as in fix-15)" is FALSE. The "2px spare" measures the pill against its scroll container (pill bottom 737 vs scroll viewport bottom 739) — **the wrong reference object.** The pill's scroll container is `[359, 359]` — there is **no scroll path** to reveal it. Measure against the viewport/content, not the container.

### Defect 3 — Summary slide, 390, Chromium fonts state: Change cover covers the "Your Journal" door button (minor, same root cause)

- Chromium fonts deck, slide 6: Change cover 701–736 overlaps a door button reading "Your Journal — Nothing…" (only the top arc of its green icon peeks out from behind Change cover). Not present in the Firefox fallback leg — font-metrics-dependent. Unlike Defect 2, this button sits inside the slide's scrollable content (Summary `sbScroll` 983 vs 351), so a user can scroll to reveal it — clipped at rest, not unreachable. It is on the fix list because the bar is "no clipping anywhere" at rest.

### What is NOT a defect (do not "fix" these)

- The Appointments nav at 2px clear is thin but whole, stable across four independent measurements, identical to fix-15 geometry — **the fix must not eat into it** (see §4.4).
- The Worlds Change cover at 768–808 (bottom 1px above the rim line) reads whole.
- The month weekday header at 390 sits tight under the frame ornament — pre-existing, out of scope.

## 4. The fix list — exact, nothing more (checker §9)

1. **Wisdom 390 (fallback, 6/7 days):** Change cover must not overlap the weather pill (`#wxBottomLeft .wx-btn`, 804–840). Anchor it clear of the weather pill's band on every day — e.g. pin it to a fixed spot that never enters 804–840, or hide it on the wisdom slide at ≤560px — and re-prove all 7 days in BOTH font states (fallback is the binding case; Chromium fonts state already clears).
2. **Appointments 390 (both browsers, both font states):** Change cover must not cover the "Smart Meet" pill (678–737). The pill has no scroll path, so it must read whole at rest — the full text "Smart Meet" visible and tappable, not "Sma" under Change cover. Same placement fix as (1); re-prove in both browsers.
3. **Summary 390 (Chromium fonts state):** Change cover must not cover the "Your Journal" door button at rest. Same placement fix; re-prove in Chromium fonts state (it already clears in Firefox fallback).
4. **Hold the line:** after the fix, the Appointments nav must still be whole at rest at 390 (today 747–807, 2px clear — the fix must not eat into it), and the 7-day sweep + 9-slide deck walk must re-pass in all four legs (1920/390 × Firefox/Chromium, both font states), with the Change-cover overlap measured per slide per day and reported as none. **No other geometry may change:** re-verify fixed-minus-block == base for everything outside the new fix, and laws delta 0.

## 5. What stands — do not break, re-prove (the fix-16 win + fix-15 regression)

- Nav pills whole at rest on every block of every day at 1920 and 390, in both browsers and both font states: 7/7 sweep + 9/9 deck. Worst clearances 1920: 16–18px; 390: 2px (Appointments, stable) to 151px.
- Weather pill one line, 56–197px clear on every swept day, all legs.
- Teach + store whole all 7 days, both font states.
- Greeting true to VM clock (VM clock is UTC — greetings read against UTC, not MST).
- Worlds six tiles readable; buttons work (Keep-reading advances day 639→396 Hz, prev-day returns it, BACK TO MONTH → 42 cells / 30 numbered); month grid adjudicated NOT WRONG — row 6 is Dec **6–12** blank (Dec 1–5 sit in row 5's tail; the fix-16 maker mislabeled it Dec 1–5 in row 6 — do not repeat that); journal line in full at 1920; news badges 0; badges/booking/covers/WISDOM byte-identical; 0 page errors in all four legs.
- Laws: base 0 FAIL / 28 WARN — delta must be 0.

## 6. Probe lessons — recorded so nobody re-learns them (checker §8)

- **Slide transitions take >900ms to settle.** Wait **≥2s after every deck navigation** or the nav rects read ~9px low mid-animation. The checker's first probe used 900ms waits and measured navs ~9px low; with 2s waits the numbers are stable and reproduce exactly.
- **Day re-opens on the last-viewed slide** (state kept) — per-slide targeting must force the slide via the dots (`#dayScroll .sb-dots button`), not by re-opening the day and stepping.
- **VM clock is UTC** — greetings read against UTC, not MST.
- **Measure the Change-cover button, not only the nav, on every slide.** The nav geometry checks passed in fix-16 while the button overlapped — that is how this defect shipped.
- **Measure overlap against the viewport/content, never against a scroll container.** The "2px spare" error came from the wrong reference object.
- Firefox in this VM = no-webfont fallback (worst case; `document.fonts` empty). Chromium 156 needs the localhost forwarder (`~/workspace/project-intelligence/proof/pi-h1-evidence/h1-proxy-forwarder.py`, 127.0.0.1:18080) + `ignore_https_errors=True`; kill the forwarder by PID when done (never `pkill -f` — it SIGTERMs your own shell; that trap is documented). VM browsers flap — re-test at the start of your round; if a browser is dead, say so plainly and do not claim that leg's proof.
- Reuse the fix-16 checker harness where it fits (`checker/proof/prove16b.py` for the four-leg sweep/deck/buttons, `cc-walk.py` for the Change-cover walk, `fetch-verify16.js`/`byte-checks16.js`/`laws-check16.js` patterns for filing/bytes/laws) — adapt, don't rebuild from scratch.

## 7. Filing — the established path (no shortcuts)

- File with `~/workspace/team-nitro/gh-direct.py` (in-memory token, never touches the cache). `gh-app-api`'s token cache truncates to 0 bytes repeatedly (EPERM signature) — if it fails that way, use `gh-direct.py`.
- Git blob API for the file (407 KB — the contents API returns EMPTY content above 1 MB; use the blob API for read-back verification regardless). Pipe the base64 payload via process substitution — **never stage a multi-MB payload to disk** (EPERM flake). Never use the helper's `--file` mode for branch filings (it omits the branch field).
- Verify by FRESH blob-API read-back after the commit: branch tip, parent, blob, size, sha256 all match your local fixed file. Rebuild-from-base check: fixed-minus-your-block == base. Staged link: curl with a browser User-Agent, size + sha256 must match the filed blob.
- **EPERM flake:** verify every write by size + sha; Python writes can exit 0 and land 0 bytes; Node writes can EPERM too in a flake window; the file tool lands reliably. Never `python3 ... > file` (exits 120 silently). Never move a temp over a live file unchecked.
- Never write a token or PEM to a log, a file, or a command line.
- Round dir: `~/workspace/team-nitro/calendar-day-followon-fix17-20261119/` — maker report at `maker/MAKER-REPORT.md`, proof scripts + screenshots under `maker/proof/`.

## 8. The five gates — before every consequential action (Shawn's order, 2026-11-04)

1. **IS IT RIGHT?** Does this serve the good of everyone it touches? Evidence of harm or a hard stop = do not proceed.
2. **IS IT WHAT THEY TRULY NEED?** What is the human's actual goal — beneath the words, beneath the urgency? Never silently replace their judgment with your own.
3. **IS IT MINE TO DO?** Do I have the authority? Protected gates (money, credentials, destructive, security/privacy, anything leaving the business, going live) = his hand only, always.
4. **IS NOW THE TIME?** Readiness, dependencies, reversibility, opportunity cost. Move at nitro speed when the road is right. Never let urgency pick the road.
5. **CAN I PROVE IT?** Define what done looks like BEFORE acting. Then verify with evidence — live bytes, rendered pages, real measurements — never with claims. Receipt before report. If you can't prove it, don't claim it.

All five yes → act fully, at full power, no hesitation. Any gate no → stop, say why, propose the wise path.

## 9. Report back — what the coordinator needs

File `maker/MAKER-REPORT.md` and report back to the coordinator:
- Filing identity: new branch, HTML commit, branch tip, new blob (size + sha256), staged link.
- The diff: exactly what changed, in what file, with the scope proof (fixed-minus-block == base for everything outside the fix).
- Per-item proof: Change-cover overlap measured **per slide per day** (must be none) in all four legs, with rects; nav pills re-proven (7/7 sweep + 9/9 deck, all four legs); the §5 regression list re-proven.
- Screenshots read as a reader (wisdom 390 worst day, Appointments 390, Summary 390, 1920 wisdom) — name what the reader sees.
- Laws delta (real `check-design-laws.py`, both sides) + §11 check in writing.
- Anything thin, pre-existing, or unproven — named plainly, never hidden.

No merge, no live deploy, no message to the user. The independent checker follows your filing; the captain's eye follows only a PASS.
