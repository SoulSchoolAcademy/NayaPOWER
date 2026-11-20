# CAL-FIX18 — MAKER BRIEF

**Round:** Calendar day-followon fix-18 · **Date:** 2026-11-20 (Shawn live on a voice call, walking the Calendar day view)
**Coordinator:** Team Nitro (fix-18) · **Status:** maker to spawn

## 1. Identity — verify before you touch anything

| Item | Value |
|---|---|
| Base branch | `calendar/day-followon-fix17-20261119`, tip `a955d7fa2299a6667ba70215dd4347c1de80386e` (verified live by the coordinator: commit message "Calendar day-view fix-17: eye record — PASS, Change cover clear at 390 in all four legs; staged link serves filed blob f4c05109") |
| Base file | `TEAM-NITRO/day-view-v18-fix-20261117/the-ultimate-calendar-v18-fix.staged.html` |
| Base blob | `f4c05109531f8b737891a43f6ea6bdcef84eddc9`, **410,236 B**, sha256 `1f798b65dfa557a4e4e20472e3d56e2bda29fd69912481338b3bb6b2bc602887` (verified by the coordinator from a fresh blob-API read: size + sha256 match exactly) |
| New branch | `calendar/day-followon-fix18-20261120` (create from the fix-17 tip; the coordinator verified no fix-18 branch exists yet) |
| Work in ONE file only | `TEAM-NITRO/day-view-v18-fix-20261117/the-ultimate-calendar-v18-fix.staged.html` |
| Staged link (after filing) | `https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/day-view-v18-fix-20261117/the-ultimate-calendar-v18-fix.staged.html&ref=calendar/day-followon-fix18-20261120&cb=<new-blob>` |
| Local base copy | `~/workspace/team-nitro/calendar-day-followon-fix18-20261120/brief/fix17-base.html` (410,236 B, sha256 verified above — start from this file, byte for byte) |

**Read first, before any edit:**
- `~/workspace/team-nitro/calendar-day-followon-fix17-20261119/checker/CHECKER-REPORT.md` — the fix-17 acceptance shape; §8 carries the probe lessons (2s settle waits, per-slide targeting via the dots, VM clock is UTC, measure against viewport/content never a scroll container, browser-flap rule).
- `~/workspace/team-nitro/calendar-day-followon-fix17-20261119/maker/MAKER-REPORT.md` — how fix-17 was built (one 3,100 B CSS block appended before `</style>`; `fixed-minus-block == base`).
- `~/workspace/team-nitro/calendar-day-followon-fix17-20261119/maker/proof/fix17-block.css` — the fix-17 block; your fix builds on it, never rewrites it.
- `~/workspace/team-nitro/calendar-day-followon-fix17-20261119/checker/proof/prove17c.py` + `daysweep17c.py` + `focus17.py` — the four-leg sweep/deck/buttons harness (reuse/extend for your own proof).

## 2. The design law — read before you build

**Read FIRST, before any design work, in this order:**
1. `~/workspace/team-nitro/THE-NAYA-DESIGN-LAWS.md` — THE RULE BOOK (Shawn's order 2026-11-17 15:15Z). MUST / MUST NOT, the text laws, the 25/19/17 scale, the §11 check. If it conflicts with anything else, it wins unless Shawn's newer word says otherwise. The coordinator has read it for this round; you read it yourself before you build.
2. `~/workspace/team-nitro/THE-PLAYBOOK.md` (the HOW)
3. `~/workspace/team-nitro/DESIGN-INTELLIGENCE-REPORT.md` (the WHY)
4. `~/workspace/team-nitro/THE-ANATOMY-OF-A-SMART-APP-PAGE.md` (the MAP) with `~/workspace/team-nitro/THE-HEART-OF-THE-MACHINE.md` (why the map works)
5. `~/workspace/team-nitro/THE-ULTIMATE-ORIENTATION.md` (who we are)
6. `~/workspace/team-nitro/THE-ARMY-TRAINING.md` (how the army works)
7. Smart Block doctrine **SN-3336** · The Icon Is the Standard **SN-3337** (the emblem `NAYA_ICON.png` is the north star for all art — every element judged against it; real objects, real materials, real light with volume, real depth; nothing flat).

**The laws that bind this round:** harvest first, never invent — take the working thing verbatim; don't touch what he didn't ask to touch (this round touches ONLY the two header items in §4 — no slide, no nav, no wording, no color, no font size anywhere else); the page he sees is the scope; read as a reader; do it right the first time; §11 check in writing in your maker report (the five gates + the design check — which reference object, hover every object, gray-text grep, size grep, flow check). A maker report without the §11 answers is incomplete. If a law and this brief conflict, the law wins — stop, name the conflict, follow the law.

## 3. Where the header lives — exact anchors (verified by the coordinator from the filed fix-17 bytes)

The day-view header is the **`.official-headliner`**, built in JS by `head.innerHTML` (base file ~line 4211–4224). Its parts:

- **Left — `hl-left`:** weekday in script + day digit tiles ("Friday" + "20"). Stays exactly where it is.
- **Centre — `hl-center` > `hl-monthline`:** `<span class="hl-script">MONTH</span>` + `dayDigitsHTML(year)` + ` · <span style="white-space:nowrap">dayDigitsHTML(DAY_FREQ[day]) + " Hz"</span>` — i.e. today it renders "November 2026 · 396 Hz". The script "November" is the certificate script face (Great Vibes, FIX11 item 14); "2026" is the harvested Dashboard digit tiles (FIX12 item 1).
- **Centre, below the monthline — `hl-timewrap`:** the world clock button + clock tool. Stays where it is.
- **Right — `stats-btn` "Your Stats" + the `sigpiece` orb.** Stay exactly where they are.
- **"BACK TO MONTH"** (top left) and the month screen's own `monthName` ("November 2026", base ~line 3088, the MONTH screen header) are NOT in scope — the month header is already centred via `monthcentre`. Do not touch either.

The wisdom line lives in `#dayTeach` (base ~line 4238): `"<strong>Friday · 396 Hz · red</strong> — The day of the ground — the root, 396 Hz. Stand firm; finish what stands."` — **untouched, byte-identical.** The `WISDOM` quote text is untouched. `DAY_FREQ`, `DAY_COLORS`, `DAY_MEANING` data are untouched.

## 4. The fix list — exactly two items, Shawn's words 2026-11-20 ~08:06–08:07 MST, from his screenshot of Friday Nov 20, 2026, 8:04 AM

### Item 1 — "November 2026" centered at the top of the header, with MORE spacing between "November" and "2026"

- The month-year line becomes the centered title line at the top of the header. Keep the existing styling — script "November" + digit-tile "2026", harvested, just re-centered and spaced. Add clear visible spacing between "November" and "2026" so it reads nice and clean as one centered title line.
- Spacing is calculated (multiples of 8px, laws §4) — never eyeballed. Name the gap value in your report and show it measured at both widths.
- The time row below stays where it is; "Friday 20" stays left; BACK TO MONTH stays left; Your Stats + orb stay right. Only the month-year line moves to centered-top and gains spacing.
- Do NOT change the month or year styling, color, or size — re-centre and re-space only.

### Item 2 — Remove the "396 HZ" digit tiles from the top header entirely

- Delete the ` · <span style="white-space:nowrap">dayDigitsHTML(DAY_FREQ[d.getDay()], dc) + " Hz"</span>` segment from the `hl-monthline` (and nothing else in that line).
- Shawn's reason: 396 Hz is already mentioned three times on the page (header tiles + twice in the wisdom line below). The header mention is the redundant one.
- Do NOT move it into Your Stats. Do NOT touch any other 396 Hz mention — the wisdom line (`#dayTeach`, two mentions) stays exactly as it is, and the `WISDOM` quote stays exactly as it is.

## 5. What stands — do not break, re-prove (the fix-17 win)

- Fix-17 Change-cover geometry: floating pill `top:40px`, wisdom hide at ≤560px (`#dayScroll:has(#wisdomBanner.on)>.cover-change{display:none!important}`) — byte-identical, re-proven by the fix-17 eye in all four legs.
- All covers (COVER_DAY + WISDOM) byte-identical; the deck, the nav, booking logic, badges — everything else byte-identical.
- Nav pills whole at rest on every block of every day at 1920 and 390, both browsers and both font states (7/7 sweep + 9/9 deck). Buttons proven by real taps at 390 Firefox (Keep-reading, prev-day, BACK TO MONTH → 42/30/12, Book a time opens booking calendar, Smart Meet opens meet mode, Change cover opens native file picker).
- Greeting true to VM clock (VM clock is UTC — greetings read against UTC, not MST).
- Laws: fix-17 base 0 FAIL / 28 WARN — delta must be 0.
- 0 page errors in all four legs.

## 6. Probe lessons — recorded so nobody re-learns them (fix-17 checker §8)

- **Slide transitions take >900ms to settle.** Wait **≥2s after every deck navigation** or rects read ~9px low mid-animation.
- **Day re-opens on the last-viewed slide** (state kept) — per-slide targeting must force the slide via the dots (`#dayScroll .sb-dots button`), not by re-opening the day and stepping.
- **VM clock is UTC** — greetings read against UTC, not MST.
- **Measure overlap against the viewport/content, never against a scroll container.**
- Firefox in this VM = no-webfont fallback (worst case; `document.fonts` empty). Chromium 156 needs the localhost forwarder (`~/workspace/project-intelligence/proof/pi-h1-evidence/h1-proxy-forwarder.py`, 127.0.0.1:18080) + `ignore_https_errors=True`; kill the forwarder by PID when done (never `pkill -f` — it SIGTERMs your own shell). VM browsers flap — re-test at the start of your round; if a browser is dead, say so plainly and do not claim that leg's proof.
- Reuse the fix-17 checker harness where it fits — adapt, don't rebuild from scratch.

## 7. Filing — the established path (no shortcuts)

- File with `~/workspace/team-nitro/gh-direct.py` (in-memory token, never touches the cache). `gh-app-api`'s token cache truncates to 0 bytes repeatedly (EPERM signature) — if it fails that way, use `gh-direct.py`.
- Git blob API for the file (410 KB — the contents API returns EMPTY content above 1 MB; use the blob API for read-back verification regardless). Pipe the base64 payload via process substitution — **never stage a multi-MB payload to disk** (EPERM flake). Never use the helper's `--file` mode for branch filings (it omits the branch field).
- Verify by FRESH blob-API read-back after the commit: branch tip, parent, blob, size, sha256 all match your local fixed file. Rebuild-from-base check: fixed-minus-your-block == base. Staged link: curl with a browser User-Agent, size + sha256 must match the filed blob.
- **EPERM flake:** verify every write by size + sha; Python writes can exit 0 and land 0 bytes; Node writes can EPERM too in a flake window; the file tool lands reliably. Never `python3 ... > file` (exits 120 silently). Never move a temp over a live file unchecked. Stage under `~/workspace/`, never /tmp (restarts wipe it).
- Never write a token or PEM to a log, a file, or a command line.
- Round dir: `~/workspace/team-nitro/calendar-day-followon-fix18-20261120/` — maker report at `maker/MAKER-REPORT.md`, proof scripts + screenshots under `maker/proof/`. The coordinator has already created `brief/` (with the verified base copy) and the `maker/`, `checker/`, `record/` dirs.

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
- Per-item proof: "November 2026" centeredness measured at 1920 AND 390 (header centre vs viewport centre, in px) + the November↔2026 gap measured at both widths; no "396 HZ" anywhere in the header at either width (measured, not grepped — rendered header text + element census); wisdom line's two 396 Hz mentions untouched (byte + render check).
- Screenshots read as a reader (day view 1920 + 390, header close) — name what the reader sees.
- Laws delta (real `check-design-laws.py`, both sides) + §11 check in writing.
- Anything thin, pre-existing, or unproven — named plainly, never hidden.

No merge, no live deploy, no message to the user. The independent checker follows your filing; the captain's eye follows only a PASS. Note: Shawn may add more calendar items while this round runs — the captain holds the round from shipping until he confirms the list is complete; your job is to land this round's two items, proven, and report back.

---

## ADDENDUM — Item 3 (Shawn, 2026-11-20 ~08:10 MST, live eye on the Notifications slide, slide 1)

Shawn's words: *"I don't know why you have the change cover thing in the corner. You don't need that. There's no cover to change on this page."*

### Item 3 — The floating "Change cover" pill stays ONLY on slides where a cover is actually visible to change

- Remove the "Change cover" pill from the **Notifications slide** (slide 1).
- Check **every other slide the same way** — any slide with no visible cover loses the pill. The pill remains ONLY where a cover is actually visible to change (e.g. the wisdom slide, where the day's cover is the board's background).
- Mechanism is the maker's call, but it must be a real per-slide rule (slide state drives visibility), not a one-slide hardcode that leaves the same defect on the next slide. The fix-17 geometry (floating pill `top:40px`, wisdom hide at ≤560px) is the placement law — item 3 is about WHEN the pill shows, not where it sits.
- The "Change cover" function itself is unchanged where the pill remains: tap still opens the native file picker, the chosen photo still becomes that day's cover only (FIX11 item 15).

### Acceptance addition (checker must prove)

- Per-slide census at **1920 AND 390**: on every slide of the 9-slide deck, the pill is present exactly where a cover is visibly shown, and absent everywhere else. Notifications slide: pill absent at both widths, both browsers.
- The wisdom slide at 390 in both font states still passes the fix-17 proof (pill clear of the weather pill's band; pill hidden when `#wisdomBanner.on` at ≤560px per the fix-17 rule).
- No other bytes changed: fixed-minus-block == base for everything outside the three items.

### Holds and scope

- Items 1 and 2 (§4) are unchanged.
- **Hold the round from shipping until the captain confirms the list is complete.** Shawn may add more calendar items while this round runs.
- The ultimate appointment creator is a SEPARATE round, not this one — do not fold it in.
