# Agreement distill fix-4 — MAKER REPORT

**Round:** Agreement distill fix-4 (Team Nitro) — six phone-width (390×844) presentation defects from the fix-3 captain's eye.
**Maker:** Naya Nitro Narzan. **Dispatched:** 2026-11-20 ~08:47Z. **Branch:** `walkthrough/agreement-distill-fix4-20261119`, from fix-3 tip `dc262be69cb2c4e0eec6ec923a85f7eae5fafacb`.
**Branch tip:** the filing commit — see the maker handoff to the coordinator (the report is filed in that commit, so it cannot name its own sha; the filed blob shas are in §9).
**Staged link:** https://naya-walk-beginning-staging.nayapower.workers.dev/ (fix-4b bytes; PUT 2026-11-20 09:48:40Z, `WELCOME_ASSETS` KV binding re-declared and preserved).
**No merge, no live deploy, no message to the user.**

## 0. Activation (read before any design work)

Read in full: `THE-NAYA-DESIGN-LAWS.md`, `THE-PLAYBOOK.md`, `DESIGN-INTELLIGENCE-REPORT.md`, `THE-ANATOMY-OF-A-SMART-APP-PAGE.md`, `THE-HEART-OF-THE-MACHINE.md`, `~/workspace/team-nitro/AGENTS.md`, and the fix-3 eye report (`walkthrough-agreement-distill-fix3-20261119/eye/EYE-REPORT.md`, 11,910 B) plus its phone screenshots. Base reproduced on fix-3 bytes first (screenshots + rects), then fixed, then re-proven on fixed bytes. All edits are CSS/layout-only at `≤480px`, in the files' existing phone-width rules — harvest first, no rebuild, no redesign, no new page. No flow JS touched; no board content, certificate-name logic, claim-gate timer, anthem/Listen wiring, or desktop rule touched.

## 1. Base verification (fix-3 bytes, before any edit)

Fix-3 tip re-verified via `gh-direct.py` (GET git ref): `dc262be69cb2c4e0eec6ec923a85f7eae5fafacb`. All six base files fetched via the git blob API and verified size + sha256 — ALL OK:

| File | Bytes | sha256 (fix-3) |
|---|---|---|
| agreement-unfold-fixed.html | 142,120 | `50876fff8caa79ee…` |
| welcome-staged.html | 1,929,575 | `3874b7ebcc6b95e…` |
| walk-beginning-fixed.html | 4,363,264 | `ef98226767ddbb50…` |
| identity-fixed.html | 402,647 | `51776174b59cee4a…` |
| walk-beginning-staging-worker.js | 8,459,261 | `cc46798578df4c9b…` |
| build-v23-staging-worker.py | 93,731 | `f6107678a0e9eef…` |

Staging confirmed serving fix-3 bytes before the fix (curl, browser UA, 2026-11-20 ~08:53Z). VM browser: Playwright Firefox headless, alive throughout (re-tested each leg).

Base reproduction (driver `maker/work/probe-fix4-base.py`, log `maker/work/proof-base/fix4-base.json`): all six defects reproduced with measured rects; zero console errors on base.

## 2. The six defects — before / after (all at 390×844, fix-4b bytes unless noted)

### A. Identity — hero name covers the certificate title — FIXED (two passes)

- **Base:** title `[22,282,368,299]`, name `[19,268,371,320]`, overlap 17px × 346px; read "CERTIFICAT[Shawn]AGREEMENT".
- **Fix-4 pass:** at `≤480px` the hero shrinks 52px → 28px (`clamp(1.75rem, 7.2vw, 2rem)`) and the name-bearing zone gains 16px (`margin-top` on `.face-center` for `.taken` / `.is-certified` / `.has-name` plaques). The title cleared (overlap 0) — but the verification screenshot caught the hero now covering the in-flow line "This certifies that" (2356 px² overlap, taken state). The 48px slot between title and center cannot hold both a 20px line and a 28px name: a live-CSS experiment (shrink the line to 13px + more margin) still left 828 px² overlap; hiding the line while the hero shows gives 0/0/0.
- **Fix-4b:** at `≤480px`, `.cert-certifies` hides while the hero shows (`.taken` / `.is-certified` / `.has-name` only). The line still shows with no name (plain state: `display:block`, `[133,294,257,314]`, "This certifies that").
- **Proven (taken state, `fix4-verify2.json` step A-taken-final):** input `shawn`, hero `Shawn`, `data-text="Shawn"`, name font 28.06px, name `[19,301,371,329]`, title `[22,282,368,299]`, line `display:none`, name–title overlap **0**, name–line overlap **0**, name–wrapper overlap **0**, wrapper–status overlap **0**, `scrollWidth == innerWidth == 390`. Screenshot: `maker/work/proof-fix4/fix4b-A-identity.png`. Plain state: `maker/work/proof-fix4/fix4b-A-plain.png`.

### B. Walk door — corner jewels cover the heading's ends — FIXED

- **Base:** h1 `[18,14,372,85]`, crests TL/TR `[8,8,84,84]` / `[306,8,382,84]`, 4620 px² overlap each side; read "elcome starts with y…" / "certificate."
- **Fix:** at `≤480px`, `#step-door .p3-question` gets 80px side padding (in the walk file's existing v7 MOBILE FIT `@media (max-width:480px)` block; other steps untouched — their headings sit below the flank header).
- **Proven:** padding computes `80px / 80px`; the heading's four text-line rects span x 127–263; **text-line vs crest overlap 0** (the h1 border box still spans the full width — padding lives inside it, so the border-box overlap is not the measure; the text lines are). Screenshot: `maker/work/proof-fix4/fix4b-B-door.png`. Door hold + Continue re-proven below (§4).

### C. Identity — "already claimed" banner first line clipped at both edges — FIXED

- **Base:** read "hat alias is already claimed. If it i…" — bottom corner crests (76px) clipped the first line at both edges; the bottom-center frame stone covered the middle ("d◆vice").
- **Fix:** at `≤480px`, `.hub-note.taken-note` gets 76px side padding, and the bottom-center frame stone hides while the taken note shows (`.cert-plaque.taken .frame-stone { display:none }` — taken state only, phone only; the stone is aria-hidden decoration).
- **Proven:** note text "That alias is already claimed. If it is yours, use your device key below — a name alone never opens it."; 5 line rects spanning x 103–287; **line-vs-crest overlap 0**; `noteTextClipped: false` (`scrollWidth == clientWidth == 350`); stone `display:none`. Screenshot: `maker/work/proof-fix4/fix4b-C-banner.png`. Note: the note *box* still overlaps the crests' lower corners (pre-existing — the box sat there on base too); the *text* clears, which is the defect.

### D. Final board — "Congratulations" runs under the orb / avatar — FIXED (two passes)

- **Base:** unfold title 25px `[40,89,230,149]`; deck title 25px `[76,168,300,221]`; final "s" hidden under the purple diamond orb (unfold) / the speak-face photo (deck).
- **Fix-4 pass FAILED on verification:** my 22px rules never applied. Diagnosis (DOM facts probe): the unfold board-37 title is `.frame-title`, not `.ib-title` (governed by `.frame-title{font-size:25px!important}`), and the deck/letter title is governed by `body.af-deck-on #deckBody .ib-title{font-size:25px!important}` ((1,2,1)). Both first-attempt rules lost the cascade.
- **Fix-4b:** board-37-scoped rules that win: unfold `article[data-beat="37"] .frame-title{font-size:22px!important}` ((0,2,1)!important); welcome `body.af-deck-on #deckBody article[data-beat="37"] .ib-title{font-size:22px!important}` ((1,3,2)!important, covers deck AND letter — both carry `body.af-deck-on` and `#deckBody`). Board 37 only; all other boards keep 25px.
- **Proven:** unfold title font **22px**, `[40,89,230,142]`; deck title font **22px**, `[76,170,300,216]`; letter title font **22px**. The only remaining title-box overlaps are containers/decoration (full-viewport frames, orbit rings, the top-left `af-corner` on the box corner) and — on the deck — the speak-face photo overlapping the h2 *box* by 1040 px²; the glyphs end ~x243 while the photo starts at x274 (**31px clear**). Read by eye in the screenshots: "Congratulations" complete on all three views, final "s" visible. Screenshots: `maker/work/proof-fix4/fix4b-D-unfold37.png`, `fix4b-E-deck37.png`, `fix4b-letter37.png`.

### E. Deck final board — big photo covers the text box's last lines — FIXED

- **Base:** the sign photo sat over the nutshell's last lines ("This is how we roll, and I'm so glad…" partly hidden). Unfold board 37 had no such overlap.
- **Fix:** at `≤480px`, the deck/letter sign frame gains `margin-top:64px` (stage view only; unfold untouched).
- **Proven:** deck nutshell `[30,234,300,502]`, sign photo `[72,511,258,697]`, **overlap 0 (9px clear)**; letter nutshell `[30,312,300,640]`, photo `[72,733,258,919]`, **overlap 0**. All nutshell lines read whole in the screenshots. Note (pre-existing, unchanged): the photo overflows its 52px frame and nicks the top of the footer caption "· NayaNET · The Deck" — the base screenshot shows the same nick at the same relative position (photo and caption move together with the frame); out of scope for this round, named here so it is not mistaken for a regression.

### F. Footer links row cut at right edge — CONFIRMED SCROLLABLE, no code change

- **Proven (twice, base + fix-4b):** `#fpLegal .fp-legal-links` nav `[8,798,382,836]`, `scrollWidth 1064 > clientWidth 374`, `flex-wrap: nowrap`, `overflow-x: auto`; programmatic `scrollLeft 0 → 60` works; 12 links reachable by scrolling. A mouse drag did not scroll the strip — that is standard overflow-strip behaviour (mouse drag selects; the strip scrolls by touch swipe / wheel / scrollbar), not a defect. No wrap was needed; no change made.

## 3. What the round changed (files + shas)

All changes are CSS/layout-only at `≤480px`. No flow JS, no board content, no F9 code, no desktop rule touched. (`FIX4` markers: identity 2, walk 1, unfold 1, welcome 2; `FIX3` markers preserved: 13 / 2 / 1 / 5.)

| File (repo path) | Fix-3 bytes | Fix-4b bytes | sha256 (fix-4b) |
|---|---|---|---|
| `team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html` | 142,120 | 142,532 | `a3b3907f2f80d09a14c1e7e8bfb7a00c63332a7b26ac2707912c39436e177b98` |
| `team-nitro/walk-v23-assembly-20261114/welcome-staged.html` | 1,929,575 | 1,930,937 | `237af4d4d5d3ac3f6c001ba770bc6bcbc90433aedd002ab5103a6e3b10672cbf` |
| `team-nitro/walk-v23-assembly-20261114/walk-beginning-fixed.html` | 4,363,264 | 4,363,683 | `856d392c439ebb5cb97aac27f34abc3b97b52b8b6bdc55b50abac9768e198b4d` |
| `team-nitro/walk-v23-assembly-20261114/identity-fixed.html` | 402,647 | 404,147 | `fef65d2cdbf2f1e8c096548df9adcdb465ac38a628f299c8e7cee2fb57703f52` |
| `team-nitro/walk-v23-assembly-20261114/walk-beginning-staging-worker.js` | 8,459,261 (`cc467985…`) | 8,463,045 | `a76a67c8e1a366ab9ce5bd91f69596139ef4674d78870cdecee695c24fe64912` |
| `team-nitro/walk-v23-assembly-20261114/build-v23-staging-worker.py` | 93,731 (`f6107678…`) | 95,815 | `31eae8862ca9cd98ff7df8b454af98ee734bb2f2dcbe592d00b3bb28fc286d98` |

Worker rebuild: `build-v23-staging-worker.py` in default mode, run twice — byte-identical both times (`a76a67c8…`). The worker was rebuilt because its inputs changed (walk/identity/welcome/unfold); the template is untouched (`61002d15…`). Staging PUT carried `--meta` with the `WELCOME_ASSETS` KV binding (`namespace_id 1cf80db6183245d19dd5296645a12bd0`); bindings re-read after the PUT and still present. Staging curl-verified after the PUT: all four routes serve the fix-4b shas (`/identity.html fef65d2c…`, `/welcome 856d392c…`, `/agreement a3b3907f…`, `/ 237af4d4…`).

## 4. F9 regression (fix-4b bytes, unless noted)

Driver: `maker/work/probe-fix4-verify2.py` (log `maker/work/proof-fix4/fix4-verify2.json`) + `probe-fix4-1920.py` + `probe-fix4-img.py`. All at 390×844 except where 1920 is named.

- **Paired alias** `?name=Shawn&alias=Shawn`: input `shawn`, hero `Shawn`, `data-text="Shawn"` — 390 and 1920. ✓
- **Name-only** `?name=Shawn`: input empty, hero empty/hidden — 390 and 1920. ✓
- **Plain** (no params): hero empty/hidden; "This certifies that" still shows. ✓
- **Door holds 10 s untouched, no timer**: visible steps stay `["step-door"]` — 390 and 1920. ✓
- **Continue → step-1**: after the 10 s hold — 390 and 1920. ✓
- **Unfold 1→37 by real tap**: counters sequential 1/37…37/37. ✓
- **Deck 1→37 → bridge**: sequential; end buttons "Enter NayaNET ◆" / "Read the Collective Agreement ◆" present; Enter reaches the bridge. ✓
- **Letter 1→37 → bridge**: sequential 1/37…37/37; board 37 title 22px, nutshell–photo overlap 0. ✓
- **Bridge pair**: "Read the agreement" → `/agreement`, counter `1 / 37`; "Begin the visual story" → deck, counter `1 / 37` (reloaded bridge in the same context; the pair shows again from the persisted agree state). ✓
- **Console errors:** the final verify run logged 2 `console.error` entries, both "Image corrupt or truncated" for `welcome-0.jpg` (proof-host asset). Investigated, not a page defect: the file fetches byte-identical twice (310,452 B, valid JPEG, starts `FFD8`, ends `FFD9`, 1448×1086); a targeted re-check loads it cleanly on deck, letter and agreement with **0 console errors** (img `complete:true, naturalWidth:1448`). The two errors were a one-off truncated transfer during that run; no image or URL was touched by this round (CSS-only). Base and fix-4 verify runs: 0 console errors.
- **Desktop 1920:** identity paired name–title overlap 0; the certifies line stays `display:block` at 1920 (the hide is phone-scoped); the desktop name–line em-box overlap is 1224 px² — identical to base, the line tucking under the name by design, and the eye declared desktop clean. No desktop rule changed.

## 5. Laws — §11 check in writing + checker delta

`check-design-laws.py` run on each changed file, base vs fixed:

| File | Base FAIL / WARN | Fix-4b FAIL / WARN | Delta |
|---|---|---|---|
| identity-fixed.html | 11 / 2 | 11 / 2 | 0 |
| walk-beginning-fixed.html | 128 / 8 | 128 / 8 | 0 |
| agreement-unfold-fixed.html | 1 / 2 | 1 / 2 | 0 |
| welcome-staged.html | 83 / 4 | 83 / 4 | 0 |

The FAILs are all pre-existing checker noise (the word "gray" inside comments, and sub-17px fonts throughout the base files) — none introduced by this round; the delta is 0 on every file.

**§11 check, in writing.** (1) Text laws: the one deliberate deviation is the board-37 title at **22px** at `≤480px` only (headlines are 25 per §2.3). It is named and justified: at 25px the single unbreakable word "Congratulations" runs under the orb/avatar on every final board; at 22px it clears on unfold, deck and letter with room to spare. The welcome file already uses 24px titles at phone; 22px is the minimal size that fits, board-37-only, phone-only. No other text size changed. (2) No gray: no color changed anywhere. (3) No mid-glyph breaks: `overflow-wrap:break-word` was considered and rejected (§6) — the fix is a size change, not a slice. (4) Real objects / one light / elevation: untouched — no element restyled, only spacing and sizes at phone width. (5) Harvest first: every fix edits the files' existing phone-width rules; nothing rebuilt, nothing redesigned, no new page, no new element. (6) Don't remove/move/touch what wasn't asked: desktop rules untouched; F9 code untouched; the only removals are decorative (the bottom-center frame stone while the taken note shows; the "This certifies that" line while the hero shows — both phone-only, both aria-hidden or sentence-duplicative, both still present in every other state). (7) The eye is the final gate: every defect is proven by measured rects (zero overlap / no clipping) AND read by eye in the screenshots listed in §2 — including the two first-pass failures (D rules that never applied; the A line collision) that the verification caught and the fix-4b pass corrected.

## 6. What was NOT proven / not done

- **Fix-3 state machine (`run-fix3.js`, 139/139) was not re-run.** The F9 surface it covers is proven instead by the live probes in §4 (same behaviours, both widths, real taps, zero console errors on re-check). Do not claim 139/139.
- **F mouse-drag test:** a mouse drag did not scroll the footer strip (see §2 F) — standard overflow-strip behaviour; scrollability is proven programmatically.
- **Caption nick (pre-existing):** the sign photo nicks the top of "· NayaNET · The Deck" on deck board 37, identically on base and fixed bytes (see §2 E).
- **The round ran long** (dispatched ~08:47Z; the fix-4 → verify → fix-4b → re-verify loop closed ~11:35Z). The extra time was the two verification-caught failures in §2 (D cascade, A line) — each was fixed and re-proven rather than shipped on a first-pass claim.

## 7. Work scripts (in `maker/work/`)

`fetch-base.py`, `fix4.js`, `fix4b.js`, `update-build-script.js`, `update-build-script-b.js`, `staging-meta.json`, `probe-fix4-base.py`, `probe-fix4-detail.py`, `probe-fix4-verify.py`, `probe-fix4-facts.py`, `probe-fix4-linefix.py`, `probe-fix4-verify2.py`, `probe-fix4-1920.py`, `probe-fix4-caption.py`, `probe-fix4-img.py`. Proof logs: `proof-base/fix4-base.json`, `proof-base/fix4-base-detail.json`, `proof-fix4/fix4-verify.json`, `proof-fix4/fix4-facts.json`, `proof-fix4/fix4-verify2.json`. Screenshots: `proof-base/fix4-base-*.png` (7), `proof-fix4/fix4-verify-*.png` (7), `proof-fix4/fix4b-*.png` (8), `proof-fix4/fix4-exp-*.png` (2).

## 8. Handoff to the coordinator

Branch `walkthrough/agreement-distill-fix4-20261119` from `dc262be6`; staged link https://naya-walk-beginning-staging.nayapower.workers.dev/ (fix-4b bytes, verified by curl sha). All six defects proven fixed at 390 with measured rects + screenshots; F9 regression passes at 390 and 1920; laws delta 0; §11 check above. Ready for the captain's eye. The one thing I would flag for the eye: the 2px gap between the hero name and the certificate title in the taken state (name top 301 vs title bottom 299) — overlap is 0 and it reads clean in the screenshot, but it is tight.

## 9. Filing record (git blob shas — content hashes, verified against `git hash-object`)

| Repo path | Bytes | sha256 | git blob sha |
|---|---|---|---|
| `team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html` | 142,532 | `a3b3907f…` | `1f0b04747e3315be6f1b619c1411e5e14fbdc1bb` |
| `team-nitro/walk-v23-assembly-20261114/welcome-staged.html` | 1,930,937 | `237af4d4…` | `daac9e3af610cb5df21917d5c0057e595d51ccde` |
| `team-nitro/walk-v23-assembly-20261114/walk-beginning-fixed.html` | 4,363,683 | `856d392c…` | `2f7a5e3ef599e00cb39c1e577bcb42563cd7ed81` |
| `team-nitro/walk-v23-assembly-20261114/identity-fixed.html` | 404,147 | `fef65d2c…` | `b3e5af088ef1d516079d96eeaa61d811d7889b8e` |
| `team-nitro/walk-v23-assembly-20261114/walk-beginning-staging-worker.js` | 8,463,045 | `a76a67c8…` | `97ec7eed101b3ee96a733a777ef6c8c88ac71131` |
| `team-nitro/walk-v23-assembly-20261114/build-v23-staging-worker.py` | 95,815 | `31eae886…` | `37a0078f86b4a3d9a91cff8f75e44493c90f5a8c` |

(The report itself is filed in the same commit; its blob sha is recorded in the maker handoff — it cannot list its own hash.)

Work scripts filed under `team-nitro/walkthrough-agreement-distill-fix4-20261119/maker/work/`: `fetch-base.py`, `fix4.js`, `fix4b.js`, `update-build-script.js`, `update-build-script-b.js`, `staging-meta.json`, `probe-fix4-base.py`, `probe-fix4-detail.py`, `probe-fix4-verify.py`, `probe-fix4-facts.py`, `probe-fix4-linefix.py`, `probe-fix4-verify2.py`, `probe-fix4-1920.py`, `probe-fix4-caption.py`, `probe-fix4-img.py`. Filed via the git-data API (blob API — the contents API returns EMPTY for files over 1 MB); filed blob shas verified against local `git hash-object` and by a fresh tree read after filing.
