# MAKER RECORD — AGREEMENT FIX PASS 2 (fix pass → fix pass 2), 2026-11-15

Maker: Naya Nitro Narzan (maker seat). Due 2026-11-15T07:30Z (captain-confirmed). Staging only — nothing merged, nothing live.
Base: fix-pass file, 3,494,589 B, sha256 `ae1bd0bab0dbefb9351fe4ef430b5ddbf4a182571097706b28f42bb9acd1d1ff` (verified first-hand before editing; baseline copy kept at `walk-beginning-fixed-ae1bd0ba-baseline.html`).
Brief: `BRIEF-AGREEMENT-FIXPASS2-20261115.md` (check-brief 9/9). Face library: `NAYA-FACE-LIBRARY.md` (15 distinct pictures). Words source (only): `COLLECTIVE-AGREEMENT-OFFICIAL-20261115.md`.
Editor: `edit-agreement-fixpass2.py` (13 asserted exactly-once replacements, temp-file write + `os.replace` in the same directory, never truncate-first). Verifier: `verify-agreement-fixpass2.py`. Browser probe: `proof-fixpass2-drive.py` (drive pattern harvested from the fix-pass `proof-fixpass-drive.py`).

## DELIVERABLE

- Walk: `~/workspace/team-nitro/walk-v23-assembly-20261114/walk-beginning-fixed.html`
- Bytes: **3,494,890** · sha256: **`4ffeb0b495a3130a5df7679e1a57bc56776477cf7d577ccece1ee4654f10ffc9`**
- Staged URL: **https://naya-walk-beginning-staging.nayapower.workers.dev/welcome**
- Served bytes verified byte-exact by curl, TWICE: 3,494,890 B, sha `4ffeb0b4…` (fetch 1 + fetch 2, both match the local file).
- Deploy: in-memory build via `deploy-v4f-memory.py` (proven v4f path), PUT HTTP 200 to worker `naya-walk-beginning-staging`, account `b5e2a51b3e883f7722287c5f51b1196b`, modified `2026-11-15T04:59:56Z`, deployment `78a7dcf0e5614bae9ba336666301b046`. Builder assert at `build-v23-staging-worker.py` updated to the new walk sha (same pattern as the fix-pass maker).
- New KV key (fix pass 2 only): `wbf-agmt-sign2.png` = `Naya.png` (2,054,581 B, sha `b63d7b3e002b…`), uploaded by `kv-put-agreement-fixpass2-sign2.py` (HTTP 200); serves live at `/agmt-sign2.png` (curl: HTTP 200, 2,054,581 B, sha matches the library file and matches served `/agmt-b06.png` byte-for-byte — same picture, as designed). New key only; the old `wbf-agmt-sign.jpg` key stays in KV, unreferenced. All other portraits were already in KV under `wbf-agmt-*`.
- Git branch (durable record): `agreement/fix-round-20261115-fixpass-2` in `~/workspace/nayapower-repo` (NayaPOWER), branched from the fix-pass branch tip (`agreement/fix-round-20261115-fixpass`, commit `e13a44695`); commit holds the edited walk file + baseline + this record + the edit/verify/probe/KV scripts + the builder-assert change + `proof-fixpass2/` evidence. Not pushed. (The repo's unrelated dirty working-tree state — `HUB/walk/worker.js`, `tools/welcome-engine/*`, `interfaces/front-door/welcome.html` — was left untouched; only the fix-pass-2 paths were added.)

## FIX 1 — PORTRAIT REPEATS (the corrected rule, built to the letter)

### The reassignment (scorecarded) — which file goes where, and why

Board portraits (6 changes; the other 13 board portraits untouched):
- **Beat 37: b10 → b12.** b10 must leave boards entirely (b09 keeps the Q3 opener, so at most one of {b09, b10} is on boards). b12's other board is 55 — 18 boards apart, the widest spacing available for this slot. b00 was forbidden here (the deed note on beat 36 carries b00; a b00 board at 37 would make the note photo equal an adjacent board's portrait). b01 was forbidden (the cost note on beat 37 itself carries b01 — own-board collision). b02 was forbidden (beat 36 is b02; adjacent boards would share a portrait).
- **Beat 58: b06 → b00.** The Q1 opener (beat 11) is b06, so beat 58 cannot keep it. b00's other board is 43, 15 apart; its only note (deed, beat 36) is far from 58. Outdoor city/water close-up, visibly different framing from its neighbours 55 (b12 full-body) and 61 (b01 studio).
- **Beat 61: b04 → b01.** The Q2 opener (beat 18) is b04, so beat 61 cannot keep it. b01's other board is 46, 15 apart. Black-background golden side-light; the skeptic note on 61 carries b04 (hand-to-face) — board and note are different pictures by eye.
- **Beat 64: b09 → b02.** The Q3 opener (beat 25) is b09, so beat 64 cannot keep it — and b09 must total at most 2. b02's other board is 36, 28 apart, the longest pair spacing on the page. Outdoor jacket, bracketed by studio boards 61 (b01) and 67 (b03).
- **Beat 67: b08 → b03.** The beat-78 opener is b08, so beat 67 cannot keep it. b03's other board is 49, 18 apart. Black-background; neighbours 64 (b02 outdoor) and 70 (b07) differ.
- **Beat 73: b10 → b05.** b10's second board slot, reassigned with 37. b05's other board is 52, 21 apart; neighbours 70 (b07) and 76 (b11) differ.

Note photo (1 change):
- **Land note (beat 27): b09 → b04.** The land note sits two boards after the b09 opener — the densest point of the old white-lace cluster. b04 (hand-to-face) is the most instantly distinguishable portrait at 44px and non-Warm; its other appearances (opener 18, job note 52) are 9 and 25 boards away. The alternative (b10) would have kept a Warm face two boards after the Warm opener. b04 now illustrates 2 notes (land + job, 25 apart) — the one sanctioned double, moved off b09.

Signing photo (1 change):
- **`/agmt-sign.jpg` → `/agmt-sign2.png` (Naya.png, new KV key).** The old signing photo is Naya_Narzan.jpg, Warm session. The donor had to be non-Warm AND keep its picture-total at most 3. I inspected the two candidates first-hand: **Naya_Profile_white.jpg (the hook photo) was REJECTED** — it is the same outdoor session as b09 (long wavy hair, gold necklace, hills/city/water behind her), so it would have moved the cluster to the signing, not broken it. **Naya.png is the only non-Warm donor whose picture-total stays ≤ 3** (board 11 + collective note + sign = 3): hair-up close-up, gold earrings, light indoor background — visibly a different photograph from b09 at signing size. Every other non-Warm donor would push its picture-total to 4.

### The counts (file audit, served bytes, .jpg AND .png)

- src totals: b00 3 · b01 3 · b02 3 · b03 3 · b04 3 · b05 3 · b06 2 · b07 3 · b08 2 · **b09 2** · b10 1 · b11 3 · b12 3 · top 1 · sign2 1. **No file totals more than 3; b09 totals 2.** Total b-occurrences 34 (19 boards + 14 notes + 1 summary-board portrait).
- Board portraits (19, unchanged in number): 11 b06 · 18 b04 · 25 b09 · 36 b02 · 37 b12 · 40 b11 · 43 b00 · 46 b01 · 49 b03 · 52 b05 · 55 b12 · 58 b00 · 61 b01 · 64 b02 · 67 b03 · 70 b07 · 73 b05 · 76 b11 · 78 b08. Per-file board counts: max 2 (b00, b01, b02, b03, b05, b11, b12 at 2; the rest at 1). **Openers unique as boards** (b06/b04/b09/b08 appear on no other board). **b10 on zero boards.** **b09 on one board only** (the opener).
- §4 faced beats (36–77): **36, 37, 40, 43, 46, 49, 52, 55, 58, 61, 64, 67, 70, 73, 76 — 15 of 42, unchanged**; every 3-board window in 36–77 contains a face (machine-checked, all 40 windows). No two adjacent boards share a portrait (the only consecutive faced pair, 36 b02 + 37 b12, carries different files).
- Note photos (14): collective b06 · land **b04** · business b11 · deed b00 · cost b01 · joining b03 · privacy b05 · vault b10 · save b12 · job b04 · earn b07 · skeptic b08 · cap b09 · hold b02. Max 2 notes per file (b04 the one double). **No note photo equals its own board's portrait (14/14) and no note photo equals an adjacent board's portrait (14/14)** — checked per note against parent beat ±1, including the two changed adjacencies (deed note b00 vs new board 37 b12; cost note b01 vs new own board 37 b12).
- The 34th b-occurrence, named: the summary board `dealAgreementSummary` carries a `deal-beat-photo` b07 (line 1534 of the base file) — not a rendered board portrait, unchanged by this pass. b07 totals 3 (board 70 + earn note + summary).
- Live (360px): all 19 board portraits + all 14 note photos loaded (`complete && naturalWidth > 0`), 148px at 360px, 244px at 1440px, srcs exactly as listed above. Signing photo `/agmt-sign2.png` loaded, 260px at 360px (1.76× the 148px board photo), 388px at 1440px (1.59× the 244px board photo).

### Same-session neighbours — stated plainly, not hidden

The library has ~4 sessions (outdoor b00/b02/b12 + top; black studio b01/b03/b05; Warm b08/b09/b10/b11; hand-to-face b04; NAYA_POWER b07) for 15 faced slots in the every-third-board §4 run — same-session boards 3 apart are arithmetically unavoidable, and the fix-pass arrangement had the same property (studio b01/b03/b05 on three consecutive faced slots 46/49/52; Warm b10/b11 on 37/40). What this pass removes is what the eyes failed: **same-file** repeats (closest same-file board pair is now 15 boards apart, was 39 for b09 and 43 for b04) and the white-lace cluster (b09 once on boards, b10 zero, sign non-Warm). Closest same-session pair I introduced: b12 at 55 → b00 at 58 (3 apart, outdoor) — b12 is a full-body framing, b00 a close-up, and they read as different photographs at page size (eye-read below). If the captain wants same-session separation too, that needs new photographs from Shawn — the 10× version, not this pass.

### Eye-reads at 360px (page size, the captain's measure)

- Board 58 (b00): outdoor city/water close-up, round lit photo, white text, corner gems inside — clean.
- Board 64 (b02): outdoor close-up, different head angle and expression from b00 — a different photograph, same session (see the same-session note above).
- Board 37 (b12): outdoor full-body framing, trees both sides — reads as a wider shot than the close-ups.
- Board 73 (b05): black-background studio portrait — clearly different from the outdoor boards around it.
- Land note open (b04): hand-to-face at 44px, unmistakably different from the b09 opener two boards above.
- Signing (b06): hair-up close-up with gold earrings on a light background, dominating its green-lit frame — visibly a different photograph from b09's Warm outdoor shot.
- Board 57 bold at body size (see Fix 3); plain-text view clean (see Fix 2).

## FIX 2 — STRAY " i" IN THE PLAIN-TEXT VIEW

- **The fix:** `plainLetterText()` read each `<p>`'s `textContent`, which includes the eye button's "i" (the button sits inside the sentence `<p>`, 14 of them). New helper `plainParaText(el)` clones the paragraph, removes its `<button>`s, then reads text; both board branches use it. The summary branch has no buttons and is untouched. **No board words change** — the sentence multiset and ordered list are identical baseline→edited (verified by file audit).
- **Live proof (the measurement, on the rendered page — not a grep):** at 360px, the plain-text view carries **0 lines ending in a stray " i"** (347 lines read); at 1440px, also **0**. Head: "THE COLLECTIVE AGREEMENT / Between NayaNET and you." Tail: exactly **"nayanet.app — enter."** Whole letter in order: all 231 board paragraph-texts appear in order in the live plain text, 0 missing. Eye-read (`proof-fixpass2/plaintext-360.png`): the letter reads clean end to end, no stray characters.
- Probe note (learning-loop): my first probe run failed on `#letterAll` because the button hides once all 83 boards are read — the plain-text check has to run from the hook state, before unfolding (the same reason Vera ran plain text as its own run). Fixed by reordering the probe; the page itself is unchanged.

## FIX 3 — TINY SMALL-CAPS (Q4 22/42, 28/42)

- **The fix:** `.ib-nutshell b` renders at 12px / .16em letter-spacing. Beats 57 (the whole board is one long bold supporting sentence) and 63 (the substantive money sentence is bold) now carry a scoped rule — `[data-beat="57"] .ib-nutshell b, [data-beat="63"] .ib-nutshell b { font-size: 17px; letter-spacing: normal; line-height: 1.65; }` — so they read at the page's body size. The base rule is byte-identical for every other board.
- **Live proof:** computed bold size at 360px — beat 57: **17px / normal spacing**; beat 63: **17px / normal spacing**; controls beat 37 and beat 45: still **12px / 1.92px** (unchanged by design). Same at 1440px (57/63: 17px; 37: 12px). Eye-read at 360px (`proof-fixpass2/board57-bold-360.png`): beat 57's sentence reads as clean body text, same size as the body around it.
- **Why the other bold lines stay (stated plainly):** the other `<b>` lines are short declarations and emphasis closers both eyes passed ("Joining NayaNET costs you nothing." beat 37; "We're not a company that sells your personal information." beat 45; "I want you to understand the logic…" beat 61 as a closing emphasis after a plain opening line). A page-wide restyle would change ~20 passed boards for a look-at item that names two. If the captain wants all bold at body size, that is one ruling away — the scoped rule is the place to widen it.
- **Screenshot miss, stated plainly:** the beat-63 screenshot captured the hook instead of the board (the scroll settled at the top). Beat 63 is proven by computed style (17px at 360 + 1440) and by the shared CSS rule with beat 57 (eye-read) — not by its own screenshot.

## NO-REGRESSION — WHAT I VERIFIED MYSELF, AND HOW

- **File audit (`verify-agreement-fixpass2.py`, run THREE times, identical, FAILS: NONE):** all 83 boards 1–4 sentences by Vera's method (max 4, min 1, total 234; list identical to Vera's published list); sentence multiset identical baseline→edited; ordered board sentences identical; Official word-multiset — zero board words outside the Official, zero Official words missing; the two ITEM-1-RULING phrases stand ×1 each ("governed by the applicable published agreements", "the intended default is seven days"); founders line verbatim ×1; "bonus" = 0 · "blockchain" = 0 · v4 hedged forms 0 · "I'm not an LLM" ×1 · "$25" ×2 · "$20" = 0 · "nayanet.app — enter." ×1 · "double points" ×1 · "THE ROYAL MANUSCRIPT" = 0 · "Ready to sign" = 0 · `letterPreview` = 0; beat 0 carries no portrait.
- **Diff scope:** baseline→edited is 29 +/- lines — exactly the 13 intended replacements (6 board portraits, 1 note photo, 1 sign src, 3 plain-text lines, 1 CSS block of 3 lines) and nothing else. Every other byte is identical to the fix-pass verified build.
- **Served-bytes audit:** the same verifier run on the fetched served bytes — FAILS: NONE.
- **Proven live on the staged bytes (driven from the login page, 360×800 then 1440×900, zero console/page errors both runs):** keep-reading 82 clicks / 83 boards · dots 83, label "ALL TEN STEPS · READ" · agree frame visible after the final click · eyes open 14/14 (tap 1: note visible, top in view; tap 2 closes — measured on all 14) · overflow 0 at true 360px hook + unfolded (scrollWidth = innerWidth) and at 1440px hook + unfolded · signing 260 vs board 148 = 1.76× at 360px, 388 vs 244 = 1.59× at 1440px · all 19 board portraits + all 14 note photos loaded with the new srcs.
- **Not probed by me in this pass:** 390px and 1920px viewports (360 + 1440 probed; the changed parts use the already-proven beat-36 pattern and the same CSS at all widths). The seal, skip, plain-text download, jump pills, and agree-via-Enter paths were not re-driven by me — they are byte-identical to the fix-pass build (raw diff) except where the 13 changes interact (plain-text view re-proven live above; signing photo re-proven live above); Vera re-sweeps them. Stated plainly, not claimed.

## THE SEVEN SELF-CHECK QUESTIONS (answered in writing)

1. **Most intelligent?** Yes — the reassignment is the smallest change that satisfies every count in the corrected rule (6 board swaps + 1 note swap + 1 sign swap, no faceless drops, no renumbering); the plain-text fix strips button text at the one place it leaks instead of rebuilding the letter; the small-caps fix is scoped to the two named boards instead of restyling ~20 passed boards.
2. **Most logical?** Yes — every change follows from a counted or eye-confirmed failure: b04/b09 same-file board repeats from the served-file grep; the b09/b10/sign cluster from the captain's eye; the 14 stray " i" lines from both eyes' plain-text reads; the 12px bold from the computed style.
3. **Most sensible?** Yes — a reader scrolling §4 now meets a different file at least every third board with no same-file repeat closer than 15 boards, the signing photo is a different session from the white-lace picture that remains, the plain-text letter reads clean, and the two money sentences read at body size.
4. **Full scope?** Yes — login-to-signing whole flow driven at phone + desktop, all 83 boards counted by sentences, all 14 notes audited for own + adjacent collisions, all 19 board portraits + 14 note photos checked loaded live, served bytes re-audited, branch filed. Nothing scoped to the diff.
5. **Consequences?** First order: the staged agreement page changes in 29 diff lines. Second order: Vera re-checks items 1–3 + the guards at page size, then the captain double-checks, then Shawn's eye. The live site is untouched; only the staging worker + one new KV key changed. A reader who had the old page cached sees the new one on next load (no versioned URLs changed; the old sign key stays in KV, unreferenced).
6. **Pros and cons?** Pros: all four opener repeats gone by the corrected rule; b09 down to 2 total uses; the white-lace cluster broken at the signing (non-Warm photo, picture-total 3); plain text word-perfect; two money sentences at body size; Official words untouched (proven by multiset + order). Cons: b04 now illustrates 2 notes (land + job) — the sanctioned double moves, it does not disappear (14 notes over 13 files forces one); same-session neighbours remain in the dense §4 run (stated above with the numbers — needs new photographs to fully fix); the hook photo shares b09's outdoor session (pre-existing, out of this pass's scope — flagged, not fixed); the kind-label wrap at 360px persists (pre-existing, brief says not this pass). Strongest case against my preference: minting the sign under a new key for Naya.png means the signing photo is the same picture as board 11 and the collective note — but it is the only non-Warm donor that keeps the picture-total at 3, and its other two appearances are a section opener 70+ boards earlier and a 44px tap-opened note, while the alternative (the white file) would have kept the Warm cluster at the signing itself.
7. **Best possible choice?** Against the ultimate objective (the reader understands the agreement in seconds, trusts it, and sees Naya throughout without the page reading as repetition): yes. The letter is still the Official's words in order, every board 1–4 sentences, faces alternating as far as 15 pictures allow, the plain text clean, the money sentences at body size, every control re-proven live. Scored: all three fixes proven in this record with their measurements; the no-regression guards proven by byte-identity plus live re-proof of the interacting behaviours.

## CANON — THE HIGHEST LEVEL (ten checks)

1. REAL OBJECT — pass: the 6 new board portraits use the harvested `.deal-beat-photo` treatment verbatim from beat 36; the sign photo keeps its green-lit elevated frame; the note photo keeps the harvested quote-photo treatment.
2. JEWELRY, NOT DOTS — pass: untouched (eyes, gems, seal byte-identical); new portraits carry the same lit ring as the existing ones.
3. ELEVATED, NEVER FLAT — pass: no flat element added; portraits are the elevated round form; the 57/63 restyle changes type size only.
4. COLOUR SPEAKS — pass: §4 boards keep their purple tone; portraits carry the tone border from the harvested rule.
5. ALIVE NUMBERS — pass: "Board N of 83" live, 83 dots lighting in order, 82 clicks — re-proven live.
6. NUTSHELL FIRST — pass: every board 1–4 sentences, max 4, total 234 — unchanged by this pass, re-proven.
7. MOTION THAT MEANS SOMETHING — pass: reveal, eye open + scroll-into-view, all re-proven live; no new motion added.
8. ACTIVE INTELLIGENCE — partial (as the round stated): rail jumps + plain-text + skip anticipate the reader; no new inference claimed.
9. HARVEST, NEVER INVENT — pass: portraits from the face library (incl. the one new KV key for the library's own Naya.png); board-photo placement harvested byte-for-byte from beat 36; zero new components; the plain-text fix reuses the existing builder.
10. PROVEN BY EYE — pass at 360px (boards 37/58/64/73, land note open, signing, beat 57, plain-text view — all eye-read in this record) and by measurement at 1440px (overflow, sizes, clicks, plain text, bold sizes); 390/1920 are Vera's to confirm by eye.

## WHAT I COULD NOT PROVE (stated plainly, never claimed)

- The 2,124 headline word count as a single number — same standing note as the round (the sentence/word-level verbatim proof stands in its place).
- The seal, skip, plain-text download, jump pills, and agree-via-Enter paths were not re-driven by me in this pass — they are byte-identical to the fix-pass build (raw diff) and ride Vera's re-sweep.
- 390px and 1920px viewports were not probed by me (360 + 1440 were); the changed parts reuse the beat-36 pattern already proven at all four widths by the round.
- Beat 63's screenshot captured the hook instead of the board (scroll settled at the top); beat 63 is proven by computed style at both widths + the shared rule with beat 57, not by its own screenshot.

## PROBE NOTES (learning-loop: three stops, three fixes, all in the probe — never in the page)

1. `#letterAll` hides once all 83 boards are read — the plain-text check must run from the hook state, before unfolding. (Same reason Vera ran plain text as its own run.) Fixed by reordering the probe.
2. The PWA install veil (`#installVeil` on the identity page) pops up on a timer and intercepts clicks; a plain Playwright click on "Not now" times out because the veil is hidden at first. Fixed by polling for the veil and JS-clicking `#installLater` until it is gone.
3. `#dealPlainClose` reports not-visible at 360px (and a leftover duplicate close-click in the probe fired after the overlay was already closed). Fixed by closing with Escape (the page's own keydown handler) and removing the duplicate.

## FIVE GATES (before the deploy)

1. **Is it right?** Yes — staging only, live untouched; the words are Shawn's ratified Official, verbatim, in order.
2. **Is it what they truly need?** Yes — the reader needs the long §4 run to feel like Naya talking to them with a different face each time, the plain-text letter to read clean, and the money sentences to read at body size.
3. **Is it mine to do?** Yes — the fix-pass-2 brief names me maker; the staging deploy + one new KV key are the brief's own path. Nothing live, no money, no credentials, no destruction.
4. **Is now the time?** Yes — due 07:30Z; Vera's focused re-check is next in the same pass (continuous cycle law).
5. **Can I prove it?** Yes — all three fixes, each with its measurement in this record (portrait audit on served bytes, live plain-text read at two widths, computed bold sizes at two widths, live drive at two widths, served-bytes audit); what I could not prove is listed under its own heading, never claimed.

## EVIDENCE INDEX (DURABLE)

- Maker record (this file): `~/workspace/team-nitro/walk-v23-assembly-20261114/MAKER-RECORD-AGREEMENT-FIXPASS2-20261115.md`
- Edited walk: `walk-beginning-fixed.html` (3,494,890 B, sha `4ffeb0b4…`) · baseline: `walk-beginning-fixed-ae1bd0ba-baseline.html`
- Edit script: `edit-agreement-fixpass2.py` · KV upload: `kv-put-agreement-fixpass2-sign2.py` · verifier: `verify-agreement-fixpass2.py`
- Browser probe: `proof-fixpass2-drive.py` · results: `proof-fixpass2/probe-360-1440.json` (aliases fixpass2360d, fixpass21440a)
- Screenshots eye-read (360px): `proof-fixpass2/board37-b12-360.png` · `proof-fixpass2/board58-b00-360.png` · `proof-fixpass2/board64-b02-360.png` · `proof-fixpass2/board73-b05-360.png` · `proof-fixpass2/board57-bold-360.png` · `proof-fixpass2/note-land-b04-360.png` · `proof-fixpass2/signing-360.png` · `proof-fixpass2/plaintext-360.png` · `proof-fixpass2/hook-360.png`
- Served bytes re-fetched: `/tmp/served-fp2-1.html` + `/tmp/served-fp2-2.html` (3,494,890 B, sha `4ffeb0b4…`, both fetches)
- Served-bytes audit run: `/tmp/svc-check2/` (full verifier on the fetched bytes — FAILS: NONE)
- Sign donor inspection: `Naya_Profile_white.jpg` (rejected — same outdoor session as b09) and `Naya.png` (chosen) viewed first-hand at full size before the swap
