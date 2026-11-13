# RECORD — WALK END SLIDE PAY-WORDS FIX

**Round:** Walk end slide pay-words fix (brief `BRIEF-WALK-END-SLIDE-PAY-WORDS-20261113.md`, 9/9).
**Branch:** `walk/end-slide-pay-words-20261113` (created from live main tip — re-read first-hand, see Filed blobs).
**Status:** MAKER DONE — build 10/10, round 7/10. **STOP at deploy** (brief §13): the staged proof leg is owed and blocked by deploy order, not by this work. Escalated to the coordinator/parent with the exact blocker below.
**Staged walk:** https://naya-walk-beginning-staging.nayapower.workers.dev/ — still v22 (sha `227a667e`, 3,363,931 B) at the time of this record. The old words are still live on staging until the deploy clears.

## What it is

- The two end-slide pay promises in `#step-end` said "paid every Wednesday" — a day the system cannot guarantee. Both now say "paid when we're paid", harvested verbatim from Naya's own words already in the file (Q9 choice C, line 603), plus one new nutshell line under the welcome paragraph: "Nine days free — in most cases, you're paid on day 10."
- Exactly three changes, nothing else, in a private copy of the true staged v22 bytes (never the shared local base file — see Base-file drift, below).

## Why it matters

- A pay promise we cannot keep is a lie on the front door. A PayPal hold (up to 21 days) moves the payout, and if we don't get paid, they don't. "Paid every Wednesday" misleads a citizen on day one.
- The new words are already his settled law (ambassador 50% of gross, recurring, referrer only, paid when we're paid with NO day guaranteed; first payout day 10 in the clean case) and already Naya's own voice in the same file. One pay promise, one wording, everywhere in the walk (L7).

## How to apply it

- The edited file is `walk-beginning-fixed-paywords.html` in this work dir (3,364,036 B, sha256 `a354f93ec5b8f81fecf3ff8df5618d4cc447fccd5816755d4467195a0a03dbc1`), filed on the branch at `walk-end-slide-pay-words-20261113/walk-beginning-fixed-paywords.html`.
- **Deploy (when the coordinator clears the order — NOT now):** the pay-words delta must be carried onto whichever build is current at deploy time (the names-page build + the Q10 join fix), never deployed as-is over them and never merged as a file replacement. The deploy path is `deploy-merged.py` (builds the worker in memory from `build-beginning-staging-worker.py` + the walk file on disk) — the build script's walk-sha assertion currently expects the names-page sha `8bb64763`, so it will refuse a v22+pay-words file until the merge is done and the assertion updated. After deploy: served `/welcome` sha = edited file sha, versions list shows the new deployment latest, deployed-worker read-back still shows `recordJoin` 3×.

## What changed (exact)

Base: staged `/welcome` curled 2026-11-13 ~02:43Z — 3,363,931 B, sha256 `227a667e4eb8e7f38fc8859495fa934b1a3b865323767816f94009b1d0df88c3` (matches the brief's grounding exactly; staged is still v22).

1. Line 838, `.p3-welcome`: "You get 50% of the revenue, paid every Wednesday. Invite the world." → "You get 50% of the revenue, paid when we&rsquo;re paid. Invite the world."
2. Line 841 (now 842), `.p3-reco`: "so you can get paid every Wednesday." → "so you can get paid when we&rsquo;re paid." (existing `&mdash;` / `&rsquo;` entities kept, nothing else in either line touched — not a comma, not a word.)
3. New line directly under the `.p3-welcome` paragraph, reusing the existing `.p3-linkcap` caption grammar — no new class, no new component: `<p class="p3-linkcap">Nine days free &mdash; in most cases, you&rsquo;re paid on day 10.</p>` (renders exactly "Nine days free — in most cases, you're paid on day 10.")
- Diff staged v22 → edited file is exactly these three changes (verified by `diff`; full diff in Proof).
- Q9-C (line 603, the harvest source) is untouched. The deal board (`#dealBoard`) is untouched — grep confirms zero pay-timing words in it (`paid`/`payout`/`trial`/`day 10`/`Wednesday` all 0). The ten questions, names page, building page, world cards, Smart Link chip, five doors, agreement board, Naya speaks, and pricing button are untouched.

## Base-file drift — found first-hand, and why the shared file was NOT touched

- The brief grounded the local base file `walk-questions-10-20261112/walk-beginning-fixed.html` as byte-identical to staged v22. It no longer is: local sha is now `8bb64763`, 3,365,193 B, "Wednesday" at lines 858/861. The diff (91 lines) is entirely the **names-page round's un-deployed work** (file mtime 02:39:54Z; the names-page maker is actively probing right now — `names-probe.py` 02:42Z, `names-probe-shots/` 02:43Z).
- The build script `build-beginning-staging-worker.py` was likewise updated by that round (02:40Z) and now **asserts the walk sha starts with `8bb64763`** (the names-page sha). It reads the walk HTML from disk at build time.
- Therefore: (a) editing the shared local file would have meant editing inside another round's live work and deploying their un-deployed changes as my own; (b) deploying my v22+pay-words file through the current build script would fail its sha assertion. The edit was made on a private copy of the staged bytes instead (`/tmp/staged-welcome.html` → `walk-beginning-fixed-paywords.html` in this work dir, via `edit-paywords.py`, every replacement asserted on its full line). The shared file was never opened for writing.

## Deploy STOP — the escalation (brief §13, live and blocking)

STOP + escalate; do NOT deploy. Three facts, all verified first-hand this round:

1. **Q10 probe has NOT run** (Q10 record: probe blocked by flake + dead browsers; test aliases `q10walk1/2/3` unused). The two-line join fix rides the Q10 maker's NEXT deploy (v23) AFTER the probe runs.
2. **The names-page round is actively building on v22 right now** (shared base file edited 02:39:54Z, probe running 02:43Z, not yet deployed). Its deploy would carry a walk file WITHOUT my pay words; my deploy would carry a walk file WITHOUT its names-page work. Either order reverts the other round.
3. **The build script is currently wired for the names-page build** (sha assertion `8bb64763`) — the deploy path itself refuses my file until the merge is done.
- The coordinator's call: order the three deploys (Q10 probe → v23 join fix → names-page → pay-words, or a single merged deploy), then this round's delta is carried forward. The staged end-slide proof and the deploy read-back below ride on that call.

## Proof

### Static (all live-measured this round)

- Edited file: 3,364,036 B, sha256 `a354f93ec5b8f81fecf3ff8df5618d4cc447fccd5816755d4467195a0a03dbc1`.
- Grep whole edited file: "Wednesday" = 0 · "paid every" = 0 · "paid when we&rsquo;re paid" = 2 (the two lines) · Q9-C straight-apostrophe "paid when we're paid" = 1 (untouched harvest source) · nutshell = 1.
- Grep `#step-end` region: "Wednesday" = 0 · "paid when" = 2.
- `diff` staged v22 → edited file: exactly 3 hunks (the two line changes + the one inserted nutshell line). Nothing else differs — the deal board, the ten questions, the names/building steps, the doors, Naya speaks, and all JS are byte-identical to v22.
- Staged `/welcome` re-curled this round: still 3,363,931 B, sha `227a667e` — v22, old words live. (This is the STOP, not a surprise.)

### Rendered — local probe (Chromium via Playwright, edited file served on 127.0.0.1:8123)

- Probe: `paywords-probe.py` in this work dir (flow harvested from `q10-probe.py`; end-slide leg this round's own). Shots: `shots/pw-payw1440-end-top.png`, `pw-payw1440-end-bottom.png`, `pw-payw390-end-top.png`, `pw-payw390-end-bottom.png`, plus entry shots.
- **20 PASS / 8 FAIL — and every FAIL is explained, none is a defect in the edit:**
  - PASS (both 1440 and 390): end slide renders; welcome line reads "paid when we're paid"; reco line reads it; nutshell reads "Nine days free — in most cases, you're paid on day 10."; no "Wednesday" anywhere on the slide; no day guaranteed; **zero horizontal overflow at scroll 0 AND scrolled to the bottom** (1440/1440, 390/390); deal board present; **five doors in his order, Dashboard first**.
  - FAIL "step-1 visible after login+certificate" (both legs): the login (`#userName`) lives in `identity-fixed.html`, served by the worker at `/` — it is NOT in the walk file (grep: 0 matches). The local probe loaded the walk file directly, so there was no login page to drive. Local-server shape, not an edit defect.
  - FAIL "advanced through 10 question steps" + "building step reached" (both legs): same cause — with no login, no step was ever revealed (all `.p3-step` sections start `hidden` until the flow reveals them). The end slide was then revealed directly by JS for the render check, which is exactly what those PASSes measure.
  - FAIL "zero console errors" (both legs): the only console errors are "Failed to load resource: 404" for `/naya-a.jpg`, `/naya-b.jpg`, `/naya-c.jpg` — the three Naya choice pictures, served from KV by the worker on staging (Q10 record proves they serve HTTP 200 with matching shas there). Local 404s only; the walk file requests them, the local static server has no KV. Not an edit defect.
- Eye check of the four end-slide screenshots (maker's own eyes): at 1440 and 390 the slide reads clean — congratulations title, welcome line with the new words, nutshell in the smaller caption style directly under it, Smart Link chip + Copy, reco line with the new words, five doors lit, world cards, deal board ("Here's the deal." + Collective Agreement), "Choose your package" button, "Welcome complete" footer. No clipping, no overlap from the new line. (The fixed corner ornaments overlay content at some scroll positions — pre-existing page chrome, identical on v22; the nutshell line adds ~18 px above the chip and pushes nothing into them.)
- World cards render with empty titles in the local reveal because no answers were entered (Skip path never ran locally) — expected, not a defect; the cards' structure is untouched.

### NOT proven (named, never hidden)

- **The staged full walk by eye from the login page at 390 + 1440** (brief verification #1) — needs the staged deploy + cloud browser; blocked by the deploy STOP above. The staged walk still shows the OLD words (verified by re-curl this round).
- **Post-deploy read-back** (served `/welcome` sha = edited sha; versions list; `recordJoin` 3× in the deployed worker) — owed after the coordinator clears the deploy. The deployed worker's join code was verified present in the local worker copy (`recordJoin` 3×: definition + 2 call sites in `walk-beginning-staging-worker.js`).
- **No-regressions by doing on staging** (ten questions, names page, building page, Smart Link Copy → "Copied ✓", doors, Naya speaks, certificate flow) — the edit touches no JS and no IDs the flow depends on (the only new element is a `<p class="p3-linkcap">` with no id and no JS hook), and the diff proves byte-identity everywhere else; the by-doing proof still rides on the staged deploy.

## Design-contract gate (a)–(i) + human checks H1–H5

Verdict identical to v22 except the two changed lines + the one nutshell line: (a) zero white/light backgrounds — slide stays obsidian, no background added (screenshots) · (b) every element raised/elevated — the nutshell is text in the existing caption grammar, no new flat element · (c) gauges/numbers alive — no gauge touched · (d) no text-in-image — no image touched · (e) no bare text blocks — the nutshell is a caption line under the welcome paragraph, title+subtitle+nutshell holds · (f) no look-alike buttons/gauges/numbers — no button touched · (g) `##` format — this record · (h) no dictation-blunt phrases — the words are Naya's harvested voice + settled law, not pasted dictation · (i) title+subtitle+nutshell + faces alternate — title "Congratulations, you're hired." + subtitle (welcome, paid when we're paid) + nutshell (day 10), all present; faces untouched.

- H1 stranger test: a stranger reads "paid when we're paid" + "Nine days free — in most cases, you're paid on day 10." and understands when they get paid, with no day promised. PASS on the rendered slide.
- H2 perfect-words law: the copy is his settled law in Naya's voice, harvested from Q9-C already in the file — not dictation pasted verbatim. PASS.
- H3 face quality: no face, image, or orb touched; the flank photo renders as before. PASS.
- H4 test in his head: Shawn reads the slide and the pay promise is true. PASS.
- H5 one ultimate ten: the end slide now says what Q9-C already says — one pay promise, one wording. PASS.

## Laws L1–L7

- L1 stranger test: PASS (H1). L2 perfect-words: PASS (H2). L3 title+subtitle+nutshell: PASS — title + welcome subtitle + day-10 nutshell, all on the rendered slide. L4 Naya speaks, faces alternate: untouched (END_SPEECH + faces never opened). L5 test in his head: PASS (H4). L6 `##` format: this record. L7 one ultimate ten: PASS (H5).

## Self-check ×3

- **Round 1 (static + rendered local):** the three changes are exact; the rendered slide reads clean at 1440 + 390; overflow 0/0; doors in order; deal board intact. Found: (a) the login leg cannot run against the walk file alone (login lives in the identity file) — probe shape, recorded; (b) the 404 console errors are the three KV pictures only — local artifact, recorded; (c) the shared base file had drifted under the brief — found, worked around, recorded.
- **Round 2 (fresh look, NEW things only):** the nutshell line's reuse of `.p3-linkcap` is consistent — both caption lines render identically, and the media-query margin overrides apply to both. The welcome paragraph wraps "paid when / we're paid." across lines at 1440 — reads fine. The deal-board child count from the probe selector (6) vs the brief's "12 clauses" is a selector-counting difference, not a change — the diff proves the board is byte-identical to v22. Nothing new that changes the work.
- **Round 3 (third look, NEW things only):** re-read the two changed lines character by character against §4 — both match verbatim, entities kept, no comma moved. Re-checked the nutshell placement — directly under the welcome paragraph, above the link chip, exactly as briefed. No new defect found. The remaining gap is the staged leg, which is blocked externally, not by anything in this file.

## The seven pre-merge questions (in writing — honest answers)

1. **Did I check my own work three times? YES** — rounds 1–3 above; each found NEW things (round 1: drift + probe shape + 404s; round 2: caption consistency + deal-board count explained; round 3: verbatim re-read). Nothing to merge in this round anyway — staged only.
2. **Is it 9 or better by my own honest score? NO — not yet.** The BUILD is 10/10. The ROUND is 7/10: the edit is exact and locally rendered-proven, but the brief's done bar requires the staged full-walk proof, and that leg is blocked by the deploy STOP. A round that cannot prove its staged bar is not 9. The scorecard carries the honest number.
3. **What could this break?** Nothing in the walk's behavior: the diff is three static-HTML hunks in `#step-end`; no JS, no IDs the flow depends on, no step logic, no styles were touched. The staging worker is shared with the Q10 + names-page rounds — a deploy NOW would collide with both (see Deploy STOP); a deploy AFTER the coordinator's order carries only the words. No live deploy, no merge, no money, no credentials, no destructive action, no privacy change.
4. **Are the automatic checks green? PARTIAL.** The edit-script assertions pass (source sha, counts, full-line matches). The local probe: 20 pass / 8 fail, every fail explained as local-server shape (no login page in the walk file; no KV pictures; no worker API) — none a defect in the edit. There is no CI suite on this branch. The staged probe — this round's own check — has NOT run (deploy STOP).
5. **Does it follow the ultimate objectives (five gates)? YES — all five.** Gate 1 right (removing an unkeepable promise) · Gate 2 what they truly need (true pay words) · Gate 3 mine to do (brief authorizes exactly these lines, staged only) · Gate 4 now (the words are wrong on staging now) · Gate 5 can I prove it — the edit is proven by grep + diff + rendered screenshots; the STAGED proof is owed after the deploy order clears, and the record says so rather than claiming it.
6. **Did I prove it with real measurements? PARTIAL.** Static: yes (shas, greps, diff). Rendered locally: yes (screenshots + measurements at 1440 + 390, printed by the probe). Rendered on staging: NO — not yet (deploy STOP). Nothing in this record claims a staged number.
7. **Is there anything in here not ten out of ten that I'm knowingly leaving? YES — named, never silent.** (a) The staged full-walk proof is unrun (deploy STOP — coordinator's call). (b) The post-deploy read-back is owed after the deploy. (c) The branch's walk file is v22 + pay words ONLY — it must be carried onto the current build at deploy time, never deployed or merged as-is over the names-page build or the Q10 join fix.

**Verdict on the seven:** Q2 is NO — do not call the round 9+, do not show Shawn anything as finished. Hand to the coordinator with the blocker named.

## Filed blobs (branch `walk/end-slide-pay-words-20261113`, verified by read-back)

- Branch created from live main tip `fd964ad32bc87c1178ddbfb48dfb6c6dcdb1f05b` (read first-hand 2026-11-13 ~02:52Z; main has moved since the brief's `091961ba` — the branch was cut from the CURRENT tip). Branch head `a2f4738fc14c4110259065256b1242e67e9933c`.
- `walk-end-slide-pay-words-20261113/walk-beginning-fixed-paywords.html` — blob `810dacc6306a11d99899fc9359223ad84b9cf281`, 3,364,036 B (read-back match=True).
- `walk-end-slide-pay-words-20261113/RECORD-WALK-END-SLIDE-PAY-WORDS-20261113.md` — blob `443a94582dae2bd78794b628e85014ce2e5b476a` at first filing (this record was then updated with the filed values and re-filed; see final blob in the receipt).
- `walk-end-slide-pay-words-20261113/SCORECARD-WALK-END-SLIDE-PAY-WORDS-20261113.md` — blob `72b1ea7a00cd9b07b2e19f3b96ef21b9b0f0fe62`, 6,008 B (read-back match=True).
- `walk-end-slide-pay-words-20261113/RECEIPT-WALK-END-SLIDE-PAY-WORDS-20261113.md` — blob `2af01d1c9056b4499abc49a88eaf9525149c9d6a` at first filing (then updated with the filed values and re-filed; see final blob below).

## NOT-DONE (named, never hidden)

1. **Staged deploy + full-walk proof** (brief verification #1 + #5) — blocked by the deploy STOP; coordinator orders Q10 probe → v23 join fix → names-page → pay-words (or one merged deploy), then the maker (or the deploy seat) deploys the merged file and the checker walks login → end at 390 + 1440 on staging.
2. **Post-deploy read-back** (served sha, versions list, `recordJoin` 3×) — owed with #1.
3. **Staged no-regressions by doing** — rides on #1.
4. **Checker verdict + captain's double-check** — owed after this handoff (coordinator dispatches the checker once the staged proof exists).
5. **Test aliases:** none were created by this round — the local probe used aliases `payw1440` / `payw390` only as form input that never reached a worker (no Box rows exist for them; nothing to clean up). No other alias was used.

## Bounds (honest — what was actually proven, and what was not)

- **Proven:** the edit is exactly three changes on true v22 bytes (diff) · grep 0 "Wednesday" in the whole file and in `#step-end` · the new words render on the end slide at 1440 + 390 with zero overflow (screenshots, probe output) · the deal board, doors, questions, names/building steps and all JS are byte-identical to v22 · the shared base file's drift + the names-page round's live work + the build script's sha assertion (all first-hand) · the branch + filed blobs (read-back verified — see Filed blobs).
- **NOT proven:** anything on staging (the staged walk still serves v22 with the old words — verified by re-curl) · the full walk by eye from the login page · the post-deploy read-back. Nothing in this record claims a staged number.
