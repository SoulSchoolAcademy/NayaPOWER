# RECORD — WALK NAMES PAGE 10/10 (presentation round)

**Round:** walk/names-page-10-20261112
**Maker:** Walk Names Page maker seat. **Captain:** Naya Nitro Narzan (coordinator).
**Base:** staged walk v22 (`walk-beginning-fixed.html`, sha `227a667e…`, 3,363,931 B — re-measured first-hand 02:36Z; served `/welcome` curl-verified identical the same minute).
**Result:** `walk-beginning-fixed.html`, **3,365,275 B, sha256 `a3510446170380e48a99803e6b6617a01eee99b263ce1d34fd0cf0d313c83d94`**.
**Brief:** `~/workspace/team-nitro/BRIEF-WALK-NAMES-PAGE-10-20261112.md` (9/9 first run).
**Branch:** `walk/names-page-10-20261112` (from live main tip `091961ba4149628191d143c5eccd2c0e5251109c`, read first-hand via `gh-direct.py` 02:39Z — same tip Q10 read at 01:56Z).
**Work dir:** `~/workspace/team-nitro/walk-names-page-10-20261112/`
**Status:** BUILT + LOCALLY PROVEN 99/99 — **DEPLOY STOPPED** (see §Deploy stop). No checker dispatched (honest 7/10 — below 9, reported to the coordinator, Q10 precedent).

## The bullseye (one line)

The names page feels like being handed your new world on a silver platter — three real world-cards, one clear hero action, nothing else to read.

## Shawn's verdict (his words, quoted verbatim — never softened)

> "So I went to the whole thing I'm impressed with is this one I think on the most part I would scorecard the whole system for conversion and trustworthiness and feel and vibe with this page it just doesn't pop it doesn't feel like a beautiful presentation like here like it doesn't feel like I'm you should be serving them like serving on silver platter here's your pages click here to view or or click click the button below to activate like to build the pages maybe less text maybe more spacing more just it just feel like something that's like a a trillion dollar high tech offering them their new new world pages and just doesn't have that feel right there's something missing to this do you see that so figure it out and make it right."

## What changed (exact — presentation only, names step only)

Edit script `edit-names-10.py` (17 asserted replacements, each count==1) + two
one-line follow-ups by hand (label-eye lane, then 48px→44px). Diff vs the v22
backup: **69 changed lines in 12 hunks** — CSS names block, names HTML,
`wireNames` only. Nothing else in the file moves (see §No-regressions).

1. **Three real world-cards.** `.p3-namecard`: padding 18px→**28px**; border
   1px white-ish→**2px solid own-color** (`rgba(var(--nc-rgb),.55)`);
   radial top glow in its own color (harvested from Q10's `.p3-choice`);
   `--nc-rgb` added to each card's inline style (personal `160,107,255` ·
   business `47,232,158` · space `255,191,61`). Hover/focus-within: lift
   −3px→**−4px**, glow `0 0 44px var(--nc)` (Q10 level, was 34px `ncglow`).
2. **Breathing room.** `.p3-namecards` gap 14px→**28px**, margin-bottom 16px→
   **28px**. Phone (≤480px): gap **20px**, card padding **20px**.
3. **Column.** `#step-names .p3-main{max-width:1120px}` (was 680px) —
   measured **1120px** at 1440.
4. **Less text.** The three `<div class="p3-nc-note">` lines and the
   `<p class="p3-names-smart">` explainer are **cut** (0 remaining in the
   file). Subtitle shortened to one plain line: "Your pages are being born
   right now. Give each one its name — the address is set automatically."
   (The Smart Link meaning lives behind the eye — `BOARD_INFO` already says
   it.) Title + subtitle + nutshell only (L3).
5. **Big readable text.** Name inputs 14.5px→**18px** desktop / **17px** phone
   (`#step-names .p3-nc-input`). Address inputs + prefix 13.5px→**16px**.
   Nutshell 13.5px→**16px, opacity 1.0**. Subtitle **18px** white. Label
   11px→**16px** (with a 44px right lane so the eye never touches it —
   self-check round 1 find, see below). Progress **16px** white opacity 1.
   Hero button **20px** desktop / **18px** phone. NAYA wordmark **16px** on
   this step (its global ≤360px rule is 15px — the sweep caught it).
6. **No gray, proven.** Dead gray declarations removed in place: subtitle
   `rgba(255,255,255,.72)`→`#fff`; the `.p3-nc-note` /
   `.p3-names-smart` rules deleted with their elements; the three S2
   color-override lines deleted as dead. `.p3-progress` fixed on this step
   by a scoped override (`#step-names .p3-progress{font-size:16px;color:#fff;opacity:1}`).
   The **base** `.p3-progress` rule (12px, `rgba(232,232,236,.55)`) still
   stands for the building + end steps — out of this round's scope, named in
   §Known not-10, not silently left.
7. **One hero action.** `#enterBtn-11` relabelled **"Build my pages"** — same
   id, same wiring (save, advance to building), hero size, elite and lit like
   the walk's best button. It is the only `.p3-enter` on the step (count 1).
8. **The View/Enter affordance (maker's sense-check call).** No separate View
   button was added: the pages do not exist yet, so a View button would be a
   dead promise. Instead the card itself is the affordance, two ways, both
   proven by clicking: (a) tapping anywhere on a card except its inputs and
   eye **focuses that card's name input** and lights the card
   (focus-within) — 12 new JS lines in `wireNames`; (b) the address row is
   the live **view** of the URL — real editable input, lights white on focus,
   whatever is typed becomes the URL. The eye stays the nutshell button only.
9. **Build script.** `build-beginning-staging-worker.py`: walk-sha assert
   moved `227a667e`→**`a3510446`** (never deleted). The worker template needs
   no other change — it carries the walk only through the `__WALK__` embed +
   the assert. Worker rebuilt from the script: **4,344,625 B, sha256
   `1b2ff1e27846ab2a7d7f524a2f77066c8cefeb409af26d6ce43df2b2bcd21b60`**,
   embedded walk byte-identical to the filed file (verified by extraction +
   hash), `recordJoin` 3×, `wbf-naya-a.jpg` present, "Build my pages" 1×.

## The five 19:59Z rulings — re-proven on this build

| # | Ruling | This build |
|---|---|---|
| 1 | Every board lights up on hover | **PROVEN rendered.** Rest-vs-hover at 1440/390/360, 3/3 cards: `:hover` true, lift ty −4.0, `0 0 44px` glow in the card's own color (rgb asserted per card). Screenshots `names-probe-shots/names-{1440,390,360}-hover-{personal,business,space}.png`. Eye-checked: the business card visibly glows green at 1440. |
| 2 | URL preview is a real editable input, lights white, typed text becomes the URL, slug live | **PROVEN by typing.** Business name "Green Box Farm" → address `green-box-farm` live; custom address `my-biz` → slug `my-biz`, and it sticks when the name changes again; custom personal address `mike8` → slug `mike8`. All read from `window.__walkState.pageNames`. Focus-white is the S2 rule, untouched. |
| 3 | NO gray text anywhere on the page | **PROVEN by `getComputedStyle` on every visible text node** of the step at 1440/390/360: every node computes to full white or its board's own color, ≥16px, opacity 1.0 — zero bad nodes at all three widths (`names-results.json`). Placeholders white/opacity 1 at 18px/17px. |
| 4 | Nutshell + eye on each board | **PROVEN by clicking.** Each eye opens `boardModal` with its title + exactly 3 lines (personal/business/space, verbatim `BOARD_INFO`). Nutshells 16px/opacity 1, eye-checked readable. |
| 5 | Building links click through to real created pages | **UNRUN on this build — STOPPED, not faked.** The wiring is unchanged (diff-proven) and S2 proved it on the S2 build — but on THIS build the click-through needs the staged worker, and the deploy is stopped (see §Deploy stop). The hero click IS proven locally (names hidden → building shown); the local building step then shows "Something went wrong" because `completeWalk()` POSTs to `/api/welcome/complete`, which 404s on the local static server — a local artifact, adjudicated, not a product defect. Ruling 5 + the end-slide world cards + Box read-back wait for the v23 deploy. |

## Measurements (every number from §DONE FIRST, with the probe that produced it)

Probe: `names-probe.py` (Playwright Firefox, local static server serving the
edited walk file — the staged deploy is stopped, so the probe loads the filed
bytes, not the staged URL). **99/99 PASS, 0 FAIL** (`names-results.json`).
Firefox launched and measured fine in this window (02:41–02:47Z) — the dead
reports from 01:40Z are stale for this window; the flake had cleared (python
writes + browser launches both worked).

| Measurement | 1440 | 390 | 360 | Bar |
|---|---|---|---|---|
| Names column (`.p3-main` width) | 1120px | 390px (full width) | 360px (full width) | ≥1100 / full−margins |
| Card gap | 28px (rowGap + box) | 20px | 20px | ≥28 / ≥20 |
| Card padding | 28px ×3 | 20px ×3 | 20px ×3 | ≥28 / ≥20 |
| Name input text | 18px ×3 | 17px ×3 | 17px ×3 | ≥18 / ≥17 |
| Address input text | 16px ×3 | 16px ×3 | 16px ×3 | ≥16 |
| Address prefix text | 16px ×3 | 16px ×3 | 16px ×3 | ≥16 |
| Nutshell | 16px / opacity 1 ×3 | same | same | ≥16 / 1.0 |
| Subtitle | 18px | 18px | 18px | ≥18 |
| Labels | 16px ×3 | 16px ×3 | 16px ×3 | ≥16 |
| Progress ("Name your pages") | 16px | 16px | 16px | ≥16 |
| Hero button | 20px "Build my pages" | 18px | 18px | hero |
| Visible text-node sweep (color/size/opacity) | 0 bad | 0 bad | 0 bad | 0 bad |
| Placeholders | white/1/18px | white/1/17px | white/1/17px | white/1 |
| `.p3-nc-note` / `.p3-names-smart` count | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 |
| `.p3-enter` count on the step | 1 | 1 | 1 | 1 |
| Hover light (3 cards) | 3/3 | 3/3 | 3/3 | 3/3 |
| Eye modals (3 lines each) | 3/3 | 3/3 | 3/3 | 3/3 |
| Card-click focuses name input | 3/3 | 3/3 | 3/3 | 3/3 |
| Horizontal overflow scroll 0 / scrolled | 0 / 0 | 0 / 0 | 0 / 0 | 0 |
| Page errors (JS exceptions) | 0 | 0 | 0 | 0 |
| Console errors | 0* | 0* | 0* | 0 |

\* Excluding local-server 404s for worker-only routes (`/naya-a.jpg`,
`/naya-b.jpg`, `/naya-c.jpg`, `/favicon.ico`) — the local server has no KV
pictures and no worker APIs; those 404s are probe artifacts, listed in
`names-results.json`, not product errors. No console error of any other kind.

**Static verification (python read of the filed file, 02:47Z):**
- Walk 3,365,275 B, sha `a3510446…`; `node --check` OK on the single inline
  script (3,197,109 chars, re-checked after the label fix).
- Counts: 3 `.p3-namecard` · 30 `.p3-choice` (Q10 intact) · 0 "Do you want
  A, B or C?" · 2 `enterBtn-11` (HTML + JS query) · `recordJoin` 0 in the
  walk file (it lives in the worker template — 3× there, verified).
- Diff vs v22 backup: 69 lines, 12 hunks, names step only (see §No-regressions).

## No-regressions (proven by doing, never by reading the code)

- Each name input edits and the address slug follows live until the citizen
  edits the address itself — **proven by typing** (1440 leg; behavior is
  width-independent, `wireNames.refresh()` untouched).
- Each address input is real and editable, lights white on focus (S2 rule,
  untouched), whatever is typed becomes the URL — **proven by typing**
  (`my-biz`, `mike8`).
- Each eye opens its modal with the three lines — **proven by clicking**,
  3/3 at all widths.
- The hero button advances to the building page — **proven by clicking**
  (names hidden, building shown, all widths). The completion POST behind it
  is a staged leg (see ruling 5).
- The ten questions, the certificate/new-account fix, and the end slide are
  untouched — **proven by diff**: the 12 changed hunks are the names CSS
  block, the names HTML, and the `wireNames` card-click addition. Heal /
  pair / restore gates never opened. Q10 question presentation untouched
  (30 choices, 0 old lines, example texts byte-identical by diff).
- Box mapping untouched — `wireNames.refresh()` / `save()` / `S.pageNames`
  shape unchanged by diff; `S.pageNames` read back from
  `window.__walkState` in the probe with the three titles + slugs.
- Naya speaks on the page — the play button (`#playBtn-11`) and its wiring
  are untouched by diff; the voice path itself is S2-proven, not re-proven
  here (no real-voice test in this round — Shawn's, as before).

## §Deploy stop — the leg that did not run (escalated, never bypassed)

**STOPPED, by the brief's deploy-order warning + the coordinator's order.**
The Q10 probe has **NOT run**: no `q10-results.json` exists in the Q10 work
dir (checked 02:38Z), and the live staging `/welcome` still serves v22
(3,363,931 B, sha `227a667e…`, curl-verified 02:36Z). A deploy of this build
now would break the Q10 probe's byte comparison (served bytes would no longer
equal the filed Q10 walk), and the two-line join fix rides the Q10 maker's
next deploy (v23) after that probe — deploying over it risks reverting the
merged `recordJoin`. So: **no Cloudflare PUT was made, no deployment id
exists for this build, the staged walk still serves v22.** The worker for
this build is generated + verified byte-identical to the filed file
(sha `1b2ff1e2…`) and ready to deploy the moment the captain coordinates v23
with the Q10 maker after the probe lands. The staged link below is therefore
the CURRENT staged walk (v22), not this build — stated plainly, not dressed up.

**What the captain must coordinate:** Q10 probe runs → v23 deploy carries
this names build (walk sha `a3510446…`, worker sha `1b2ff1e2…`) + the
two-line join fix → staged end-to-end re-proof (ruling 5, building links,
end-slide cards, Box read-back, full walk from the login page) → checker.

## Self-checks ×3 (each found NEW things)

- **Round 1** (eye-check of the 99/99 run-1 screenshots + label geometry):
  F1 — **the 16px label touches the eye at phone widths** (measured: label
  div right edge overlaps the eye's left edge by 30px at 360/390; the glyphs
  kissed by ~1px — MY round's doing, the 11px→16px raise). Fix:
  `#step-names .p3-nc-label{padding-right:48px}` — text centers clear of
  the eye lane. F2 — **hover-timing probe artifact**: run-1's business hover
  read mid-transition (ty −0.2 at 700ms); re-check proved the settled state
  (ty −4, 44px own-color glow at 1200ms). Fix: probe settles 1200ms, not
  700ms — the product was right, the probe was impatient. Re-ran: 99/99.
- **Round 2** (eye-check of the run-2 screenshots, post label fix): F3 —
  the 48px lane wraps "YOUR PERSONAL PAGE" to two lines at 360 (clean but
  awkward beside one-line BUSINESS/SPACE). Fix: 44px — one line again, 16px
  clearance to the eye at 360 (measured on the text range, not the div).
  F4 — the local building screenshot shows "Something went wrong building
  your world." — adjudicated: the local static server has no
  `/api/welcome/complete`, so `completeWalk()` fails there by design; on
  staging the same POST succeeds (S2 proved it). Not a product defect; the
  staged leg is what proves it on this build. Re-ran: 99/99 on final bytes.
- **Round 3** (brief-line coverage + design-contract gate + this record):
  no new defects. Every DONE FIRST line maps to a passing probe check except
  ruling 5 / the staged end-to-end, which are named as UNRUN (deploy stop),
  never claimed. Gate (a)–(i) + H1–H5 + L1–L7 below.

## Design-contract gate (a)–(i) + H1–H5 + L1–L7

- (a) zero white/light backgrounds — PASS (obsidian throughout; screenshots
  at 1440/390/360 show no light background).
- (b) every element raised/elevated — PASS (cards 28px padded, own-color
  2px border + top edge + radial glow + deep shadow; hero button elite, lit).
- (c) gauges/numbers alive — PASS (the addresses are live: slugs update as
  you type, proven by typing; the hero button is lit).
- (d) no text-in-image — PASS (no words baked into any picture; Naya's
  portrait carries no text; h1/subtitle/nutshells are live text).
- (e) no bare text blocks — PASS (title + subtitle + nutshell live in cards;
  no wall of bare text — screenshots).
- (f) no look-alike — PASS (three colors, three labels, three addresses;
  told apart at a glance — screenshots).
- (g) `##` format — PASS (this record is written in `##` sections).
- (h) no dictation-blunt phrases — PASS (subtitle is plain warm words;
  Shawn's verdict is quoted verbatim only where labeled as his words).
- (i) title+subtitle+nutshell + faces alternate — PASS (each card: label +
  name + address + one nutshell + eye; Naya's face + play button on the step;
  the three question-step faces alternate A/B/C, untouched).
- H1 a child reads every word on a laptop — PASS (1440 sweep 0 bad +
  screenshot eye-checked).
- H2 a child reads every word on a phone — PASS (390/360 sweep 0 bad +
  screenshots eye-checked).
- H3 the three cards are told apart at a glance — PASS (color + name +
  address — screenshots).
- H4 every card lights up on hover in its own color — PASS (3/3 at all
  widths, computed + eye-checked).
- H5 the one hero button is unmissable and every behavior still works —
  PARTIAL: the button is proven (label, size, advance); the local behaviors
  are proven (slug, eye, card-click); the staged end-to-end behaviors are
  UNRUN (deploy stop) — named, never claimed.
- L1 stranger test — PARTIAL (a cold stranger reads the step in seconds
  locally — screenshots; the cold full walk from the login page is UNRUN
  staged).
- L2 perfect-words law — PASS (his verdict quoted verbatim, labeled his
  words, never softened; the bullseye is one line).
- L3 title+subtitle+nutshell — PASS (subtitle one line; nutshells only).
- L4 Naya speaks, faces alternate — PASS (play button + portrait on the
  step, wiring untouched; question faces alternate, untouched).
- L5 test in his head — CANNOT PASS YET (would he call this a
  trillion-dollar offering on his laptop, first look? The rendered shape
  answers every item in his verdict; his eye is the final gate and the
  staged page is not yet this build — this record does not claim his verdict).
- L6 `##` sections — PASS (see (g)).
- L7 one ultimate ten — NOT YET (one page, one bar; the staged leg is
  unproven until v23 lands. No almost is filed as a ten).

## The seven pre-merge questions (in writing — honest answers)

NOTE: no merge in this round — staged only, per the brief. The maker does
NOT merge; the staged work waits for the captain's coordination + double-check
+ Shawn's eye + his tap. These answers are the law's record.
1. **Did I check my own work three times? YES** — round 1 (label-eye
   overlap, hover-timing artifact), round 2 (label wrap → 44px, building
   error screen adjudicated), round 3 (brief-line coverage, design-contract
   gate). Each round found NEW things.
2. **Is it 9 or better by my own honest score? NO — honest 7/10 for the
   ROUND (the BUILD is 10/10 on its local rendered evidence, 99/99).**
   The round's done bar requires the staged deploy + staged end-to-end
   proof, and that leg is stopped by the deploy-order warning. Below-9 work
   never reaches the checker — no checker is dispatched; this record goes to
   the coordinator with the stop named (Q10 precedent).
3. **What could this break?** The staged worker ONLY — and nothing was
   deployed, so nothing is broken. The filed walk changes the names step
   only (diff-proven, 12 hunks). If v23 deploys it: the staged walk's names
   step (new presentation), the staging worker (new embedded walk +
   unchanged join code + unchanged picture routes). Nothing live touched: no
   live nayanet worker, no live walk, no pricing, no mail, no money, no
   credentials, no destructive action, no privacy change. Rollback: redeploy
   the v22 worker (filed blob on the Q10 branch, deployment `2dcc6ecb…`).
4. **Are the automatic checks green? PARTIAL — green where run, unrun where
   blocked.** Probe 99/99 green · `node --check` green · build-script
   assertions green (walk/identity/welcome shas) · worker embed byte-identical
   green. The staged/deploy checks are UNRUN (deploy stop), not green.
   An unrun check is a stop, not a pass.
5. **Does it follow the ultimate objectives (five gates)? PARTIAL — gate 5
   is not yet yes for the ROUND.** Gate 1 (right?) yes — answers Shawn's
   verdict item by item, harms nothing, touches no protected gate. Gate 2
   (what they truly need?) yes — readable text, distinction, light, space,
   one clear button, exactly what he named. Gate 3 (mine to do?) yes —
   captain-dispatched maker seat, staged only. Gate 4 (now?) yes for the
   build, correctly NO for the deploy — the wise path was to stop, not to
   break the Q10 probe. Gate 5 (can I prove it?) LOCALLY yes (99/99
   rendered + shas + diff); STAGED not yet. Four yes + one partial = do not
   call it done.
6. **Did I prove it with real measurements? PARTIAL.** Local rendered
   measurements — yes (99/99, screenshots, shas, diff, byte-identical
   worker). Staged measurements — NO, not yet (deploy stop).
7. **Is there anything in here not ten out of ten that I'm knowingly leaving?
   YES — named, never silent.** (a) Not staged; ruling 5 + building links +
   end-slide cards + Box read-back + full login walk unrun on this build
   (deploy stop). (b) The `.p3-progress` base rule is still 12px gray for
   the building + end steps (out of scope; the names step is fixed by a
   scoped override). (c) The hero button sits below the fold at 1440 (three
   tall cards push it down; the citizen reaches it after naming the third
   card — natural flow, not a defect per the brief, named so the captain
   sees it). (d) Name inputs are empty in the local probe (no alias in a
   fresh local load; in a real walk the personal name prefills with the
   alias and business with the first words of `biz_do`). (e) The local probe
   404s on worker-only routes (`/naya-a.jpg` etc.) — adjudicated artifacts.
   (f) The h1's doubled-quote look is the text-shadow glow (S2's
   adjudication, stands — not re-litigated). (g) The corner-gem frame
   ornaments overlap the step edges at scroll-top (pre-existing, all steps,
   end-slide record's note — not this round's).

## Six anti-repeat items (brief §5, verbatim in spirit)

- Never paste dictation verbatim — the meaning is taken; only his operative
  words are quoted, labeled as his.
- Never use the word 'blockchain' — it does not appear in this work or record.
- Never invent a component when the harvested one exists — end-slide world
  card + pricing board + harvested os-input + the walk's own eye and hero
  button; the card-click affordance reuses the existing inputs, no new part.
- Never report done from scroll-0 checks alone — the probe measures scroll 0
  AND scrolled at every width.
- Never claim without a live measurement — every claim above carries a probe
  check, a sha, or a screenshot; the staged claims are explicitly NOT made.
- Never present work without a live link — the staged link below is live and
  curl-verified, and it is labeled v22, not this build. No link = not done,
  and this build has no staged link yet — stated, not hidden.

## Test aliases (for the joint walk test-row cleanup; nothing deleted by this round)

**None.** The probe ran against a local static server with a throwaway
browser context: no claim was made, no completion was posted, no Box row,
project row, or page was created anywhere. There is nothing to clean up.
(LocalStorage in the throwaway contexts held only `__walkState` for the
`yourname` fallback; the contexts are destroyed.)

## Filed blobs (branch `walk/names-page-10-20261112`, verified by read-back)

- Branch created from live main tip `091961ba4149628191d143c5eccd2c0e5251109c`
  (read first-hand 2026-11-13 ~02:39Z).
- `walk-questions-10-20261112/walk-beginning-fixed.html` — 3,365,275 B,
  sha `a3510446…` (blob + read-back in the receipt).
- `walk-questions-10-20261112/build-beginning-staging-worker.py` — 32,582 B,
  walk-sha assert `a3510446` (blob + read-back in the receipt).
- `walk-questions-10-20261112/walk-beginning-staging-worker.js` —
  4,344,625 B, sha `1b2ff1e2…` (blob + read-back in the receipt; generated by
  the build script from the filed walk, embed byte-identical).
- Record + scorecard + receipt + probe + results in
  `walk-names-page-10-20261112/` (blobs + read-back in the receipt).
- Screenshots (`names-probe-shots/`, 15 PNGs) stay in the work dir, not
  filed to the branch — the checker re-runs its own probes.

## NOT-DONE (named, never hidden)

1. **The deploy (v23) is stopped** — Q10 probe has not run; deploy only
   when the captain coordinates it with the Q10 maker after the probe lands.
2. **Staged end-to-end proof on this build** — ruling 5 (building links +
   end-slide world cards click through to real created pages with the
   citizen's typed words), Box read-back word for word, full walk from the
   login page at 1440 + 390 — all wait for the v23 deploy.
3. **Checker verdict + captain's double-check** — held (honest 7/10, below
   9); the coordinator dispatches the checker after the staged proof lands.
4. **The `.p3-progress` base 12px gray** on the building + end steps —
   out of scope, named in Q7(b); a later round may fix it globally.
5. **No merge, no PR, no live deploy** — staged only, waits for the
   captain's double-check + Shawn's eye + his tap.
