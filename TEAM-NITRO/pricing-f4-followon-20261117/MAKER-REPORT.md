# MAKER REPORT — Pricing F4 Follow-on: Marcellus + certificate narrow + start over + certificate type (2026-11-17)

Maker: pricing F4 follow-on round. Brief: `~/workspace/team-nitro/BRIEF-PRICING-F4-FOLLOWON-20261117.md`
plus the 02:08Z amendment (certificate layered type, item 4). Required reads done first:
Playbook, Design Intelligence Report, Naya Design Language, Naya Code, Deep Palette,
F4 fix brief, F4 maker report + checker verdict (read whole). Built 2026-11-17 ~02:07–02:25Z.
**Stage only. Do NOT merge. Nothing went live.**

## Staged URLs

- Pricing v78 (unchanged): https://naya-pricing-f4-staging.nayapower.workers.dev/
- Free route: https://naya-pricing-free-staging.nayapower.workers.dev/free
- Free walk: https://naya-pricing-free-staging.nayapower.workers.dev/free/walk
- Hub: https://naya-pricing-free-staging.nayapower.workers.dev/free/hub (302 → https://nayanet.app/)

## 0. BASE — verified before any patch (fail-stop if moved)

The F4-fix base was regenerated in memory and asserted byte-exact before patching:
walk 3,291,949 B sha `04ec6218…` · entry 307,918 B sha `e0534a61…` · worker 3,619,556 B
sha `83aa4090…` — all MATCH the F4 record. The follow-on build reproduces byte-exact
from those inputs (re-derived independently in the verification pass, same shas).

## 1. ITEM 1 — MARCELLUS FONT ON THE WALK

**Finding (proven, not guessed).** The live walk's `/welcome` names
`Marcellus,Georgia,serif` 7 times but loads it **nowhere**: 0 `@font-face`, 0 Google
Fonts links, 0 `@import`, 0 woff — on `/welcome` itself. The loading lives on the walk
worker's **main entrance** (`/`): a verbatim Google Fonts link — preconnect +
`css2?family=Marcellus&family=Outfit:wght@300;400;600;700;800;900&display=swap` — so
`/welcome` renders Marcellus from that page's load/cache. The staged free walk lost
both the family and the loading in the F4 regeneration (system sans + monospace only).

**Fix (free walk only, nothing invented):**
- (a) the entrance's link tag, **verbatim**, into the free walk's `<head>`
  (Outfit rides along unused — its woff2 never downloads since no rule names it).
- (b) `font-family:Marcellus,Georgia,serif` on the walk's display type — `.p3-question`
  (headlines), `.p3-congrats` (end-slide headline), `.p3-welcome` (intro paragraphs).
  The live walk's Marcellus uses are headlines (30/24px) + intro/letter beats (19px),
  so these three base rules are the faithful mapping; the live walk's `.deal-*` /
  `.letter-beat` classes do not exist in the free walk's older source. The family is
  set once on each base rule; the size-only media rules carry it through.

**Verified:** staged walk bytes carry the exact link + all three rules; the Marcellus
css2 serves 200 and its latin woff2 downloads (14,552 B, wOF2 magic — harness T6);
the executed walk reaches the end slide with the `.p3-congrats` headline present
(harness T1). Rendered serif paint still needs the captain's eye (see §7).

## 2. ITEM 2 — /free CERTIFICATE AT NARROW WIDTHS

**Root cause (from the served bytes).** The certified document is a fixed 3-row grid
(`.identity-face` absolute, rows 0.84fr/auto/1.16fr, plaque `overflow:hidden`). At
635×349 the face is only **~213px** tall (349 − top bar 50 − footer 50 − stage padding
36, all three measured from the served CSS) while the certified content is **~523px**
(seal 72 + title ~15 + jewels ~30 + certifies ~20 + name ~54 + status ~20 + 2 boxes
~124 + regalia stacked ~40 + ENTER 58 + start-over 40 + gaps ~50). The head row
(~66px) cannot hold seal 94px + title + certifies, so the head's overflowing content
paints down over the giant name ("welcome back" line, "This certifies that"); the foot
row (~113px) cannot hold status + 2 boxes + regalia + ENTER (~230px), so ENTER is
pushed below the plaque edge and clipped — invisible. The regalia line (Nº + date,
~571px at desktop spacing) is one flex row that cannot fit a 354px column at 390px.
That is every overlap the eye reported, from one mechanism: content taller/wider
than a fixed grid that clips instead of flowing.

**Fix (certified state only; desktop 1919×998 matches neither gate, so its
presentation is byte-identical in behavior):**
- (a) `@media (max-width:640px)` — the regalia **stacks** (column, dot hidden, each
  line centered, letter-spacing tightened); no side-by-side collision is possible.
- (b) `@media (max-height:700px)` — the certified face leaves the fixed grid and
  becomes normal flow (static flex column, centered, `min-height:100%`) inside a
  scrolling plaque (`overflow-y:auto`); the seal steps down to 72px. Content that
  cannot fit **scrolls instead of overlapping**; ENTER stays in flow and reachable.
  When content fits, nothing scrolls and the composition reads the same.
- Nothing else moves: same copy, same boxes, same seal, same ENTER, same name.

**Layout budgets (harness T4, from the served CSS):**

| Viewport | Face | Content | Result |
|---|---|---|---|
| 635×349 certified | ~213px | ~523px | old grid MUST clip (~310px); new flow + scroll, no overlap, ENTER reachable |
| 390×844 certified | ~708px | ~550px | fits in grid mode, no scroll; regalia stacked (one-line ~571px > 354px column) |
| 1919×998 certified | — | — | neither media query matches; presentation untouched |

**Verified:** the rules are present in the staged entry bytes; the budgets are computed
from the served values (harness T4, ALL PASS). Rendered paint at 635/390 still needs
the captain's eye (see §7) — this is layout math + structure, not a rendered screenshot.

## 3. ITEM 3 — START OVER CONTROL

**Finding (proven).** The walk persists in localStorage — `nayanet_smart_alias` /
`nayanet_smart_name` / `nayanet_vault_key` (identity), `naya_welcome_right_v1`
(answers + reveal), `nayanet_free_entry` (flag); sessionStorage `nayanet_user_name` +
`nayanet_pending_route`. Boot with a saved reveal jumps straight to the end slide;
`?reset=1` does **nothing** — there is no reset handling anywhere (the only `reset`
hits are the F4 `resetNamesEnter`). A completed walk genuinely could not restart.

**Fix.** A small quiet **"Use a different alias"** ghost button under ENTER on /free
(white text, hairline white border, pill, uppercase — secondary to ENTER's purple,
does not disturb the certificate). It is visible **only in the certified state**,
CSS-gated on `.cert-plaque.is-certified` — no JS hook into the stamp/restore paths,
so it is correct whether certification came from a fresh stamp or a silent restore.
Click clears exactly the five localStorage keys + the two sessionStorage keys and
reloads: /free boots back to the composing claim form, a new alias can be claimed,
ENTER hands a fresh walk at step 1. The old alias stays claimed in the registry (its
row is never deleted); this device simply forgets it — the device key is minted fresh
on the next claim, exactly as `activateAndRedirect` already does for a missing key.
The clearing is surgical: an unrelated key (`nayanet_install_done`) survives the
click (harness T2).

**Verified end to end (harness T1→T2→T3, real network, real endpoints):** fresh alias
A claimed via the real `POST /api/claim`, full 14-step walk driven through the real
served script, real build completes into the five doors, completion record stored
server-side; the start-over script (extracted from the staged /free bytes) executed
against a seeded completed state clears all seven keys, leaves the install flag,
reloads exactly once; fresh alias B claimed via the real `POST /api/claim` boots at
step-1 — not the end slide, not the door — and advances to step-2 as a live fresh
walk. No link that lands on the end slide again anywhere in the path.

## 4. ITEM 4 — CERTIFICATE LAYERED TYPE (amendment 02:08Z)

**Finding 1 — Newsreader does NOT load today (confirmed, not just named).**
`/free`'s `--serif` is `'Newsreader', Georgia, 'Times New Roman', serif` (9
`var(--serif)` uses, layered glow text-shadows) — but there is **no `@font-face` and
no webfont link** on `/free` or on the walk worker's `/identity.html`. The certificate
renders in **Georgia** today. Memory already recorded this on 2026-10-21
("Newsreader not web-loaded — Georgia renders"). **Fix:** preconnect + Google Fonts
css2 for Newsreader (`ital,opsz,wght@0,6..72,400..700;1,6..72,400..700` — covering the
certificate's 400–700 weights **and the italic** "This certifies that" uses) into
`/free`'s `<head>`. `--serif` itself is **unchanged**; all 9 uses unchanged.
**Verified live:** css2 200 (6 `@font-face` blocks, italic included), latin woff2 200,
146,872 B, wOF2 magic (harness T6 + build run).

**Finding 2 — ONE serif for the certificate: the canonical file is /free.**
The canonical layered certificate is `/free` (identity v2.4, Shawn-accepted
2026-10-20, SN-2922 bar: the name official, glowing, solid) — its serif is
**Newsreader**. The walk worker's `/identity.html` defines the **same** `--serif`
(verified read-only — out of scope, already aligned). The staged walk holds **no
certificate card** (0 `cert-*` classes; the live walk's Marcellus lives on the
DEAL/agreement presentation, not a certificate), so there is no second certificate
serif in scope to align: the walk's display type stays Marcellus per item 1, the
certificate's type stays Newsreader per this item — each canonical in its own file.
**Open question, flagged not decided:** if the captain wants the walk's end-slide
headline in Newsreader too (one serif across the whole welcome moment, not just the
certificate), that is one line — say so and it is done; it was not silently decided
here because item 1 (his 02:05Z question) orders Marcellus for the walk's display type.

## 5. FILES / WORKERS CHANGED — before → after

| Thing | Before | After |
|---|---|---|
| Pricing v78, worker `naya-pricing-f4-staging` | 11,360,503 B, sha `ca2eafeb896c763ae2459b4a10b8715e726765ced607c0aab3640d27e6c39ae2` | **UNCHANGED** (re-verified live over HTTP) |
| Free entry `/free` | 307,918 B, sha `e0534a61441dd6f4f643b79a74a9d1a8479c8c41cb2d6abf126d3b7fd87eb1ab` | **310,241 B (+2,323), sha `e9462d8ee6fe3e45b4235bd7eb367dca658febcda42a0638eaad249dad86b814`** |
| Free index `/` | 1,966 B, sha `085939f6…` | **UNCHANGED** |
| Free walk `/free/walk` | 3,291,949 B, sha `04ec6218783e949690cb832c57e5d02e38ed304e7f2f164ddea8b67167c6ba78` | **3,292,257 B (+308), sha `2370eae2f9ae9e281d1c3f3b35d99f8699c7df6a2fe4f73328e2877c3b6453ea`** |
| Free worker `naya-pricing-free-staging` | 3,619,556 B, sha `83aa4090852cb3fd58dfaaaccb337d428662a2b88ff9314caf803d1ec1678cbc` | **3,622,237 B (+2,681), sha `f571768cd3866a809d8f413da3db1c5461090afc47be62a7f7893e4dfbb06a06`** (gzip 2,546,313 B, under the 10 MB limit) |
| `/free/hub` | 302 → https://nayanet.app/ | **UNCHANGED** |

Round files (`~/workspace/team-nitro/pricing-f4-followon-20261117/`):
`build-followon.py` (build + stage, in-memory), `check-followon.mjs` (harness),
`cleanup-followon.py` (KV + Supabase cleanup), this report, plus small explore scripts.
**Big files are NOT on disk** — the EPERM flake is still up (python/curl writes fail,
leaving 0-byte files; small file-tool writes work). The new walk + entry + worker are
recoverable byte-exact from the staged workers at the shas above, and re-derived
in-memory from the F4 base with the same result. Filed to GitHub (see §6).

## 6. SELF-CHECK — per item (harness `check-followon.mjs`, executes the real served scripts)

**Harness: ALL PASS** (two full runs; the second run is the filed one — see the note
below on the corrected footer measurement).

- **T0 static (26 checks):** Marcellus link verbatim + 3 family rules on the walk, no
  Newsreader on the walk; Newsreader link + `--serif` intact + 9 uses on /free, no
  Marcellus on /free; certified regalia stack + dot hidden + plaque scroll + flow
  face + static name + ENTER in flow; start-over present, gated, placed under ENTER,
  clears the walk key, reloads; F4 markers intact; five doors Hub-first; play button
  glow-only (no `<audio>`, no `new Audio`, no `.play(`); entry intact (free line,
  eye, walk URL).
- **T1 fresh walk, alias A (real network):** claimed `f4followonazhqggl` (cert 743)
  via the real `POST /api/claim`; boot at step-1; all 14 steps driven (answer typed,
  Enter clicked, next step appears); names Enter → building visible → real build
  completes into `buildDone` → "See your pages" → end slide, five doors, Marcellus
  headline present; completion payload alias matches; completion record stored
  server-side.
- **T2 start-over:** the script block extracted from the staged /free bytes, executed
  against a seeded completed state — all 7 keys cleared, install flag survives,
  reload fired exactly once.
- **T3 fresh walk, alias B:** claimed `f4followonbuxubaf` (cert 744) via the real
  `POST /api/claim`; boots at step-1 (not the end slide, not the door); step-1 Enter
  advances to step-2; no completion record yet for B.
- **T4 layout math:** budgets above, from the served CSS values.
- **T5 untouched:** pricing v78 byte-exact live; `/free/hub` 302 → nayanet.app.
- **T6 fonts really load:** Marcellus css2 + latin woff2 (14,552 B, wOF2); Newsreader
  css2 + latin woff2 (146,872 B, wOF2) including the italic face; the walk worker's
  `/identity.html` carries the identical `--serif` definition.

**Correction, owned.** The first harness run passed with a wrong assumption baked into
one T4 check: the footer height was estimated at ~28px. Measuring the served CSS
showed the bottom bar is 50px, so the 635×349 face is ~213px (not ~235px) and the
390×844 face ~708px (not ~730px). Both conclusions stand — and are stronger with the
real numbers (content ~523px vs a 213px face; ~550px vs 708px). The harness was
corrected to the measured values and **re-run in full — ALL PASS** (second run's
aliases: A `f4followonazhqggl` cert 743, B `f4followonbuxubaf` cert 744). The filed
harness carries the corrected numbers.

**Cleanup (all five test aliases):** KV completion records for `f4followonpywcejrz`
(build run, cert 740), `f4followonanhpytt` (first harness A, cert 741),
`f4followonbyekytr` (first harness B, cert 742), `f4followonazhqggl` (cert 743),
`f4followonbuxubaf` (cert 744) — **all DELETE 200, all verify 404**. (Two cleanup
runs hit the workers.dev chunked-transfer drop on urllib verifies; the script was
switched to curl verifies and completed cleanly — the drops were transport flakes,
not delete failures.)

## 7. HONESTLY NOT DONE

1. **Supabase identity rows for certs 740, 741, 742, 743, 744 still exist.** The anon
   DELETE returns 200 with `[]` — zero rows deleted (RLS filters it), exactly as in
   the F4 round. They join the F4 round's open rows (certs 737, 738, 739): **eight
   test rows now need a keyed delete or Shawn's hand** (737 f4captaincheck ·
   738 f4check9cpncugw · 739 f4checkcbi3t1em · 740 f4followonpywcejrz ·
   741 f4followonanhpytt · 742 f4followonbyekytr · 743 f4followonazhqggl ·
   744 f4followonbuxubaf). KV side is fully clean; no test alias resolves to any
   test pages (completion records are gone; the `/<alias>` redirect is a catch-all
   that 302s for any string, per the F4 checker — it never read KV).
2. **No live rendered paint (desktop, 635px, or 390px).** I am a subagent with no live
   browser; the VM browsers are dead (Firefox exit 139, Chromium exit 133 per the
   house notes) and jsdom could not be installed. What I prove instead: the real
   served scripts executed end to end (all 14 steps, real build, doors, start-over,
   fresh walk), the font files actually downloading (css2 + woff2, wOF2 magic), and
   the certificate layout by construction + measured budgets (flow layout cannot
   overlap; stacked regalia cannot collide; ENTER is in flow). **The checker/eye
   must still walk /free → /free/walk at desktop + 635px + 390px in a real browser
   and look at the certificate name (official, glowing, solid — SN-2922's bar) and
   the end-slide headline in the serif family.**
3. **The live walk source still serves the old walk** (no serif at all on the live
   site's walk; Marcellus loads only via its entrance page's link, so a cold load
   of `/welcome` falls back to Georgia). Fixing the live walk source is a walk-round
   job — this round touched only the free copy, as briefed. Nothing here goes live;
   live is Shawn's hand only.
4. **Big files not on disk** (EPERM flake, §5) and **no GitHub filing of the 3.2 MB
   walk / 3.6 MB worker sources** (same as F4: the staged workers are the byte-exact
   record, now re-derived in-memory by this round). Small files (this report + 3
   scripts) are filed — see §6.
5. **Open question for the captain** (§4): walk end-slide headline in Newsreader too,
   or Marcellus as briefed? One line either way; flagged, not decided.

## 8. GITHUB FILING

Branch `pricing-f4-free-entry-20261116` (repo `SoulSchoolAcademy/NayaPOWER`, TEAM-NITRO is a
folder inside it). New commit on top of the branch tip — **NOT merged**.
Files: `pricing-f4-followon-20261117/MAKER-REPORT.md`, `pricing-f4-followon-20261117/build-followon.py`,
`pricing-f4-followon-20261117/check-followon.mjs`, `pricing-f4-followon-20261117/cleanup-followon.py`.
**Filed: branch `pricing-f4-free-entry-20261116`, commit
`a4cbeffc01f2119598c96fde815f06079a9086d8`** (parent = branch tip `c0c3f78a…`),
tree `ef91f2f3bd30576222cb03fdb77630b63506425c`, 4 blobs (report `ec71407c…`,
build-followon `067f639a…`, harness `999b11e3…`, cleanup `a9fdabe5…`); ref verified pointing at
the new commit; maker-report blob read-back MATCH (sha256
`0dc3de3c23cb683f81520bd15f841e650d5753c3e61b1b615a6ef61b2a05ea29`). **NOT merged.**
Amendment commit **`6a2533d1c7374bfb51906345ff852df0897080bc`** (tree
`5c997307fc6706d9903649e0d61420e78ede0917`) re-filed the same four files with this §8
filled in (first filing above); its maker-report blob read-back MATCH (sha256
`50e8be045586ed64dddb0d1e943829f77a9a74721187615ca1d16dab0a2c40ae`). **NOT merged.**

## 9. FOR THE CHECKER

Cold, from the staged bytes: (1) claim a fresh test alias at `/free`, watch the
certificate render (name in Newsreader once the font arrives — check
`document.fonts` if your harness can, else the network: the css2 + woff2 must be
fetched); (2) at 635×349 and 390px, confirm the certified document reads clean —
regalia stacked, no overlap, ENTER visible/reachable (scroll at short heights is
the designed behavior, not a failure); (3) click "Use a different alias", claim
another alias, walk from step 1; (4) drive the walk end to end at desktop + 390px
and confirm the end-slide headline renders in the serif family; (5) re-verify
pricing v78 byte-exact, `/free/hub` 302, F4 markers, play button glow-only. Then
clean up your own test alias the same way (KV DELETE + Supabase row — the row will
need the key this round could not supply; eight rows now wait: certs 737–744).
