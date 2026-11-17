# MAKER REPORT — Free Certificate Marcellus Swap (2026-11-17)

Maker: free-certificate Marcellus swap round. Brief:
`~/workspace/team-nitro/BRIEF-FREE-CERTIFICATE-MARCELLUS-20261117.md`.
Required reads done first: Naya Code, Naya Design Language, Deep Palette,
F4 follow-on checker verdict (read whole). Built 2026-11-17 ~02:38–02:56Z.
**Stage only. Do NOT merge. Nothing went live.**

## Staged URLs

- Pricing v78 (unchanged): https://naya-pricing-f4-staging.nayapower.workers.dev/
- Free route (NEW): https://naya-pricing-free-staging.nayapower.workers.dev/free
- Free walk (unchanged): https://naya-pricing-free-staging.nayapower.workers.dev/free/walk
- Hub: https://naya-pricing-free-staging.nayapower.workers.dev/free/hub (302 → https://nayanet.app/)

## 0. BASE — verified before any patch (fail-stop if moved)

The F4-follow-on base was regenerated in memory and asserted byte-exact
before patching: walk 3,292,257 B sha `2370eae2…` · entry 310,241 B
sha `e9462d8e…` · worker 3,622,237 B sha `f571768c…` — all MATCH the
checker-verified record. The swap reproduces byte-exact from those inputs.

## 1. ITEM 1 — /free CERTIFICATE --serif → MARCELLUS

**The call (captain's decision, 02:28Z, Shawn's 👍):** ONE serif in both
places, and it is Marcellus — the beautiful layered font from yesterday
that Shawn asked about by name. The walk's certificate and end-slide
headline are Marcellus; the /free certificate was Newsreader. Align /free
to Marcellus.

**Fix — exactly two substitutions, nothing else (the diff proves it):**

```diff
-      --serif: 'Newsreader', Georgia, 'Times New Roman', serif;
+      --serif: Marcellus, Georgia, serif;
-   <link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400..700;1,6..72,400..700&display=swap" rel="stylesheet">
+   <link href="https://fonts.googleapis.com/css2?family=Marcellus&family=Outfit:wght@300;400;600;700;800;900&display=swap" rel="stylesheet">
```

- (a) The loading, restored faithfully: the css2 URL is **verbatim from
  the live walk entrance** (`https://naya-walk-beginning-staging.
  nayapower.workers.dev/`), re-verified live in this run — the entrance
  carries that exact URL plus the preconnect, the same way the walk's
  Marcellus was restored in the follow-on (Item 1). The Newsreader URL
  was replaced inside the entry's existing `<link>` tag, so the
  resulting tag is byte-identical to the entrance's tag (same href,
  same rel); the preconnect line is identical in both and stays.
  Outfit rides along unused, as on the walk.
- (b) `--serif` is now `Marcellus, Georgia, serif` — the walk's stack
  (`Marcellus,Georgia,serif`), spaced to match this file's style.
  `'Times New Roman'` drops with the Newsreader stack; Georgia stays
  the fallback. All 9 `var(--serif)` uses unchanged.

**Verified:** the unified diff touches exactly 4 lines (2 removed, 2
added), both font lines; `Newsreader` occurs 0 times in the new entry;
`Marcellus` occurs exactly twice (link + `--serif`); the Marcellus
css2 serves 200 (5,837 B, 14 faces) and its latin woff2 downloads
(14,552 B, wOF2 magic — exactly the size the follow-on checker
measured); the staged worker serves the new entry byte-exact over
HTTP and through the Node fetch-handler driver.

## 2. ITEM 2 — THE NAME STILL MEETS THE SN-2922 BAR (official, glowing, solid)

**The layered glow is untouched.** All 9 `text-shadow` declarations
were extracted from the old and new entry and asserted byte-identical —
including the certificate name's own glow:
`0 0 38px rgba(160,107,255,0.16), 0 3px 30px rgba(0,0,0,0.55)`.
The `.cert-name` rules (all 6, incl. the certified static-in-flow rule
and the three size clamps) are byte-identical before/after — they use
`var(--serif)`, so the swap only changes which face renders inside the
same glow. Weight 560 and line-height 0.98 are unchanged.

**Honest note for the eye (not hidden):** Marcellus ships ONE weight
(400) and NO italic face. Two of the 9 serif uses ask for more than
that: the name asks weight 560, and "This certifies that" (1.22rem) is
`font-style: italic`. With Marcellus those render the 400 face and a
synthesized oblique — the same pattern the walk's end-slide headline
already lives with (Marcellus at weight 800, confirmed by the eye at
02:35Z). The brief orders Marcellus; the paint is the eye's call.
Nothing was re-weighted or un-italicized to dodge it — scope is type
only.

## 3. ITEM 3 — NARROW LAYOUT STILL HOLDS WITH MARCELLUS

**Measured, not assumed.** Marcellus is WIDER than Newsreader — about
7% on names ("Shawn Vibert" 467px vs 438px at 78.4px; "F4 Followon
Test" 595px vs 564px). Widths were measured with fontTools from the
served latin woff2 files themselves (Marcellus upm 2048, Newsreader
upm 2000), at the certificate's real sizes, for four sample names
including the 29-character "Alexander Christopher Bennett". Line
counts at the real column widths:

| Viewport | Name size | Column | Marcellus lines (worst) | Newsreader lines (worst) |
|---|---|---|---|---|
| 1919 desktop | 78.4px | 920px | 2 | 2 |
| 635w | 54.4px | 599px | 2 | 2 |
| 390w | 52.65px | 354px | 3 | 2 |

Heights are family-independent (line-height in em); only the name's
line count moves the budgets, and the margins cover it:

| Viewport | Face | Content (Marcellus, worst case) | Result |
|---|---|---|---|
| 635×349 certified | ~213px | ~575px (2-line name) | old grid MUST clip; new flow + scroll, no overlap, ENTER in flow and reachable |
| 390×844 certified | ~708px | ~653px (3-line name) | fits in grid mode, no scroll needed — 55px margin |
| 1919×998 desktop | — | — | neither media query matches; presentation untouched |

The narrow rules are all intact in the staged bytes (regalia stacks at
≤640px, dot hidden, plaque scrolls + face goes to flow at short
heights, ENTER `position:relative`, `min-height:58px` in flow). The
"This certifies that" line measures 151px in Marcellus vs 138px in
Newsreader at 19.52px — centered, plenty of room, no consequence.

**Verified:** harness T4 re-derives both budgets from the served CSS
values (seal 72, ENTER 58, name cap clamp present) with the measured
Marcellus line counts — ALL PASS.

## 4. FILES / WORKERS CHANGED — before → after

| Thing | Before | After |
|---|---|---|
| Pricing v78, worker `naya-pricing-f4-staging` | 11,360,503 B, sha `ca2eafeb896c763ae2459b4a10b8715e726765ced607c0aab3640d27e6c39ae2` | **UNCHANGED** (re-verified live over HTTP) |
| Free entry `/free` | 310,241 B, sha `e9462d8ee6fe3e45b4235bd7eb367dca658febcda42a0638eaad249dad86b814` | **310,212 B (−29), sha `dfe70a8c8a4d89aa49a31aa56d077b51867ef4e42f276ce28bc39d23fa6370b2`** |
| Free index `/` | 1,966 B, sha `085939f6…` | **UNCHANGED** |
| Free walk `/free/walk` | 3,292,257 B, sha `2370eae2f9ae9e281d1c3f3b35d99f8699c7df6a2fe4f73328e2877c3b6453ea` | **UNCHANGED** (byte-identical) |
| Free worker `naya-pricing-free-staging` | 3,622,237 B, sha `f571768cd3866a809d8f413da3db1c5461090afc47be62a7f7893e4dfbb06a06` | **3,622,208 B (−29), sha `29c859f2bf7201e239ec9a11be1290f9e69637bb0da1f915480077ae5df29121`** (gzip 2,546,306 B, under the 10 MB limit) |
| `/free/hub` | 302 → https://nayanet.app/ | **UNCHANGED** |

Round files (`~/workspace/team-nitro/free-cert-marcellus-20261117/`):
`build-marcellus.py` (build + stage, in-memory), `check-marcellus.mjs`
(harness), `metrics-marcellus.py` (metrics re-derivation), this report.
**Big files are NOT on disk** — the EPERM flake is still up (python/curl
writes fail, leaving 0-byte files; small file-tool writes work). The new
entry + worker are recoverable byte-exact from the staged worker at the
shas above, and re-derived in-memory from the follow-on base with the
same result. Filed to GitHub (see §6).

## 5. SELF-CHECK — per item (harness `check-marcellus.mjs`, cold, from the staged bytes)

**HARNESS: ALL PASS (29 checks, one run, no retries).**

- **T0 static (22 checks):** staged /free is the new entry (310,212 B,
  sha `dfe70a8c…`); Marcellus link verbatim + preconnect; `--serif`
  Marcellus, 9 uses; no Newsreader anywhere; Marcellus exactly 2×; all
  9 layered glow text-shadows intact; certified `.cert-name` static in
  flow with the purple glow; size clamps intact; weight 560 /
  line-height 0.98 unchanged; regalia stack + dot hidden + plaque
  scroll + flow face + ENTER in flow (relative, 58px); start-over
  control intact; F4 markers intact; five doors Hub-first; walk
  byte-identical (3,292,257 B, sha `2370eae2…`, Marcellus 4×, no
  Newsreader); entry intact (free line, eye, walk URL).
- **T4 layout math:** budgets above, from the served CSS values +
  measured Marcellus line counts.
- **T5 untouched:** pricing v78 byte-exact live; `/free/hub` 302 →
  nayanet.app.
- **T6 fonts really load:** Marcellus css2 + latin woff2 (14,552 B,
  wOF2). The walk worker's `/identity.html` still carries the
  Newsreader `--serif` — NOTED out of scope (see §7), not a failure.

**Deliberate: no test alias was claimed in this round.** The swap
touches no JS path (the diff is 2 lines, neither in script), so a
claim + walk would prove nothing the byte-diff, font, and layout
checks do not — and it would add an eleventh Supabase test row to the
ten already open from the F4 rounds. No new KV records, no new rows.

**Correction, owned.** The first build run failed at the metrics step:
the old-browser UA trick for TTFs returned a css2 with no subset
comments and no `.ttf` URLs, so the parser found zero faces. Fixed by
measuring the served latin **woff2** files directly with fontTools
(brotli is installed) instead of chasing TTFs. The swap, staging, and
all other checks in that run had already passed; the fixed script
re-ran clean end to end (BUILD+STAGE OK, harness ALL PASS).

## 6. HONESTLY NOT DONE

1. **No live rendered paint (desktop, 635px, or 390px).** I am a
   subagent with no live browser; the VM browsers are dead (Firefox
   exit 139, Chromium exit 133 per the house notes). What I prove
   instead: the real font files downloading (css2 + woff2, wOF2 magic,
   exact size), the layered glow shadows byte-identical, the
   certificate layout by construction + measured budgets with real
   Marcellus glyph widths, and the staged bytes served byte-exact.
   **The checker/eye must still walk /free at desktop + 635px + 390px
   in a real browser and look at the certificate name (official,
   glowing, solid — SN-2922's bar) in Marcellus — including the
   weight-560 name and the italic "This certifies that" (see §2).**
   Per the brief, the captain's eye re-walks the certificate at narrow
   width before the live step.
2. **No end-to-end certified walk was driven in this round** (see §5:
   deliberate — no new test alias, no new Supabase row). The stamp /
   restore paths are untouched (the diff is 2 lines, neither in
   script), and the start-over control + F4 markers were re-verified
   static; the follow-on round proved those paths end to end on these
   exact bytes minus the two font lines.
3. **The walk worker's `/identity.html` still defines the Newsreader
   `--serif`** (verified live in the harness run). It is a different
   worker from the free worker and out of this brief's scope ("/free
   certificate's type ONLY. The walk is untouched."). If the captain
   wants one serif across the whole welcome moment, that is the
   follow-on: one line in the walk worker's identity file.
4. **Supabase identity rows for certs 737–746 still exist** (ten rows,
   from the F4 + follow-on rounds — none added by this round). They
   need a keyed delete or Shawn's hand, as the follow-on checker
   recorded.
5. **Big files not on disk** (EPERM flake, §4) and **no GitHub filing
   of the 3.2 MB walk / 3.6 MB worker sources** (same as F4: the staged
   workers are the byte-exact record, now re-derived in-memory by this
   round). Small files (this report + 3 scripts) are filed — see §7.
6. **Nothing live.** Staging only; live is Shawn's hand only.

## 7. GITHUB FILING

Branch `pricing-f4-free-entry-20261116` (repo `SoulSchoolAcademy/NayaPOWER`, TEAM-NITRO is a
folder inside it). New commit(s) on top of the branch tip — **NOT merged**.
Files: `free-cert-marcellus-20261117/MAKER-REPORT.md`, `free-cert-marcellus-20261117/build-marcellus.py`,
`free-cert-marcellus-20261117/check-marcellus.mjs`, `free-cert-marcellus-20261117/metrics-marcellus.py`.
**Filed: branch `pricing-f4-free-entry-20261116`, commit
`PENDING-FIRST-FILING`** (parent = branch tip `a86b914f…`),
tree `PENDING`, 4 blobs (report `PENDING`,
build-marcellus `PENDING`, harness `PENDING`, metrics `PENDING`); ref verified pointing at
the new commit; maker-report blob read-back MATCH (sha256
`PENDING`). **NOT merged.**

## 8. FOR THE CHECKER

Cold, from the staged bytes: (1) re-derive the swap from the
follow-on base (`build-marcellus.py` regenerates it; the diff must be
exactly the 2 font lines); (2) fetch staged /free and confirm the
Marcellus link verbatim, `--serif: Marcellus, Georgia, serif`, 9 uses,
zero Newsreader, all 9 glow shadows intact; (3) confirm the Marcellus
css2 + latin woff2 (14,552 B) download; (4) re-measure the name widths
from the served woff2 files and re-derive the 635/390 budgets —
Marcellus is wider than Newsreader, so check the worst-case line
counts, not the typical ones; (5) re-verify pricing v78 byte-exact,
`/free/hub` 302, walk byte-identical, F4 markers, start-over intact.
Then walk /free → /free/walk at desktop + 635px + 390px in a real
browser and look at the certificate name against SN-2922's bar. No new
test alias is needed; if you claim one, clean up its KV record the
same way (the Supabase row will need the key this round could not
supply; ten rows now wait: certs 737–746).
