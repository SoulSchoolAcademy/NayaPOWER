# CAPTAIN'S EYE — Agreement distill fix-5

**Staged host:** `https://naya-walk-beginning-staging.nayapower.workers.dev/`
**Branch:** `walkthrough/agreement-distill-fix5-20261119`, tip `f38e63402823ef884e439a9ed6e4550a7f2e296a` (filing commit; fix commit `b048f002`, parent fix-4 tip `d5003b2f`)
**Eye dates:** 2026-11-20, 12:28–12:50 UTC. Playwright Firefox in this VM, real taps, phone 390×844 first, then desktop 1920×1080. Firefox was alive for every leg (re-tested at the start; it never died in this round).
**Evidence:** `~/workspace/team-nitro/walkthrough-agreement-distill-fix5-20261119/eye/` — 4 driver passes (`work/eye-drive1.py`, `work/eye-drive1b.py`, `work/eye-drive1c.py`, `work/eye-drive2.py`), logs `eye-log1.json`, `eye-log1b.json`, `eye-log1c.json`, `eye-log2.json`, byte proof `work/eye-blob-verify.json`, laws outputs `work/eye-laws-base-welcome.txt` / `work/eye-laws-fix5-welcome.txt`, 28 screenshots (`eye-01` … `eye-35`, minus one deleted mislabel — see §8).

## VERDICT: PASS

The fix-4 checker's go-back is answered in full. Defect F is fixed on both footer strips at 390 — all 12 links reachable on the bridge (proven by real tap through the full citizen flow, twice) and on the intro strip (proven on the true intro render in a fresh browser). Desktop 1920 is unchanged link-for-link. F9 passes at 390 and 1920. Defects A–E still hold, re-measured by my own probes. Laws delta 0. Zero console errors in every leg.

| Item | Verdict |
|---|---|
| F — footer links reachable at 390 (bridge, real tap) | **PASS** (12/12; was 7/12 on base) |
| F — intro strip (fresh browser, true intro render) | **PASS** (12/12; see the activation note) |
| Desktop 1920 regression | **PASS** (row still centred, 87px symmetric margins, no overflow) |
| F9 regression (390 + 1920) | **PASS** (unfold/deck/letter 1→37 sequential, bridge pair both ways, 0 console errors) |
| A–E re-check | **PASS** (all re-measured; numbers match fix-4) |
| Byte leg (6 files, fresh blob reads) | **PASS** (6/6: tree blob, size, sha256, git hash) |
| Laws delta | **PASS** (83/4 both sides, diff empty) |

## 1. BYTE VERIFICATION — all six files match (my own reads)

Fresh git blob-API reads via `gh-direct.py` (never the contents API), against the branch tip. My own script: `work/eye-verify-blobs.py`, log `work/eye-blob-verify.json`. Tip matches `f38e6340`; chain is `f38e6340` → `b048f002` → `d5003b2f` (the tip is a filing commit on top of the fix commit, as the coordinator stated — the "parentMatch: false" in my log is my check comparing the tip's direct parent to the fix-4 tip; the chain is correct).

| File | Bytes | sha256 (first 16) | Blob | Match |
|---|---|---|---|---|
| agreement-unfold-fixed.html | 142,532 | a3b3907f2f80d09a | 1f0b04747e3315be6… | ✓ |
| welcome-staged.html | 1,930,947 | 57ebe2d295b494eb | 00082c3d65801997f… | ✓ |
| walk-beginning-fixed.html | 4,363,683 | 856d392c439ebb5c | 2f7a5e3ef599e00c… | ✓ |
| identity-fixed.html | 404,147 | fef65d2cdbf2f1e8 | b3e5af088ef1d516… | ✓ |
| walk-beginning-staging-worker.js | 8,463,055 | c9bc8fedcbad3299 | 0413500982bc14df… | ✓ |
| build-v23-staging-worker.py | 96,371 | 7ce1a895051cd6e4 | 2299b99155e44225… | ✓ |

Staging curl (browser UA, my own): `/` → `57ebe2d2…` (1,930,947 B), `/identity.html` → `fef65d2c…` (404,147 B), `/welcome` → `856d392c…` (4,363,683 B), `/agreement` → `a3b3907f…` (142,532 B). The staged host serves fix-5 bytes on every route. Fix-4 welcome fetched for the laws base: blob `daac9e3a…`, 1,930,937 B, sha256 `237af4d4…` — matches the checker's stated fix-4 sha.

## 2. DEFECT F AT 390×844 — PASS

### Bridge — proven by real tap (drive 1c, the re-run)

My first bridge attempt (drive 1b) returned "no nav" — `#fpLegal .fp-legal-links` had not rendered within my 2500ms wait after the "I agree" tap. That was my wait, not the page: the re-run (drive 1c) waits for the selector (it arrived at **3.4 s**) and then sweeps. The checker hit the same class of wait on its first staged leg. Full citizen path: `/agreement` → Next 1→37 sequential → "I agree" → `/?stage=bridge`.

- Strip: `scrollWidth 1754`, `clientWidth 374`, `maxScroll 1380`, `justify-content: safe center`, `nowrap`.
- **All 12 links reachable, 0 unreachable (viewport AND strip criteria):**

| Link | First fully inside |
|---|---|
| Terms of Service | scrollLeft 0 — [12,142] at load |
| Privacy Policy | scrollLeft 0 — [162,275] |
| Cookie Policy | scrollLeft 50 |
| Refund Policy | scrollLeft 150 |
| Acceptable Use | scrollLeft 300 |
| Community Guidelines | scrollLeft 500 |
| Copyright / DMCA | scrollLeft 650 |
| Ambassador Terms | scrollLeft 850 |
| Membership & Billing | scrollLeft 1000 |
| Young Citizens | scrollLeft 1150 |
| Accessibility | scrollLeft 1300 |
| Disclaimer | scrollLeft 1380 (max) — [285,378] |

- At `scrollLeft = 0` the strip opens on "Terms of Service / Privacy Policy / Cookie Polic…" (`eye-26-bridge-s0.png`). At max scroll it ends on "Young Citizens / Accessibility / Disclaimer", all whole (`eye-27-bridge-smax.png`). 0 console errors.
- The same numbers came back a second time in drive 1 through the agreed-state restore path (identical scrollWidth, maxScroll, reachability) — two independent measurements agree to the pixel.

### Intro strip — PASS, on the true intro render in a fresh browser (drive 1b)

- Cold `/` in a **fresh browser**: `#fpLegal` `display:none`. `?stage=intro`: `display:none`. Both re-confirmed — the honest limit stands: no citizen click in the filed bytes opens the intro view directly (the walk end offers deck/letter only; the login offers the unfold). That is a flow question for a later round, not a defect in this fix.
- Diagnostic activation on the cold `/` load via the page's own `window.__fpStage.enter()`: body `fp-stage-on fp-intro fp-dialed`, `#fpLegal` display `block`, choice pills ("Begin the visual story" / "Read the agreement") visible.
- On that real intro render: `scrollWidth 1754`, `clientWidth 374`, `maxScroll 1380`, `justify-content: safe center`, **all 12 links reachable, unreachable 0** — Terms `[12,142]` at scrollLeft 0, Disclaimer `[285,378]` at max, identical numbers to the bridge. Screenshots `eye-24-intro-s0.png` / `eye-25-intro-smax.png` show the choice view with the strip opening on Terms.
- **My own correction, stated plainly:** my drive-1 intro "cold" measurement read `display:block` — contaminated, because that browser context had already agreed in the letter leg and the page restores the agreed bridge stage on a cold load. The fresh-browser leg above is the true cold measurement. I do not rest on the contaminated one.

### Desktop 1920 — no regression (drive 2)

- Bridge: `scrollWidth == clientWidth == 1904` (no overflow), `safe center`, first link left 87, last link right 1833 — symmetric 87px margins, identical to base link-for-link. Screenshot `eye-35-desk-bridge.png`: all 12 links in one centred row. **Desktop unchanged.**

## 3. F9 REGRESSION — 390 and 1920, my own taps

| Check | 390 | 1920 | Result |
|---|---|---|---|
| Identity paired `?name=Shawn&alias=Shawn` | input `shawn`, hero `Shawn`, `data-text="Shawn"`, shown | same (hero `[500,388,1420,472]`, matching fix-4) | ✓ |
| Identity name-only `?name=Shawn` | input empty, hero empty/hidden | — (390 only) | ✓ |
| Identity plain (no params) | hero hidden; "This certifies that" shows | — (390 only) | ✓ |
| Door holds 10 s untouched | still `["step-door"]` after 10 s | still `["step-door"]` after 10 s | ✓ |
| Continue → step-1 | `["step-1"]` after tap | `["step-1"]` after tap | ✓ |
| Unfold 1→37 by real tap | sequential 1/37…37/37 | sequential 1/37…37/37 | ✓ |
| Deck 1→37 → bridge | sequential 37/37; "Enter NayaNET ◆" → bridge, pair shows | — (390 only) | ✓ |
| Letter 1→37 → bridge | sequential 37/37; "I agree ◆" → bridge, AGREED marker true | — (390 only) | ✓ |
| Bridge pair both ways | "Begin the visual story" → deck 1/37; "Read the agreement" → `/agreement` 1/37 | pair present, both pills readable | ✓ |
| Anthem + Listen | anthem expands its opening words; Listen (aria "Play — read the agreement with Naya") expands "Naya's reading arrives with her video" — visible twice in `eye-23-after-listen.png`; no video/audio element (wiring queues behind this round) | — (390 only) | ✓ |
| Console errors | 0 `pageerror` / console errors on every 390 leg | 0 on the desktop leg | ✓ |

**Unfold selector correction, stated plainly:** my drive-1 unfold walk recorded only "1 / 37" — because I drove `#fpNextBtn`, which **does not exist** on `/agreement` (my dump proves `fpNextBtnExists: false`). The unfold's controls are the text buttons "Next ◆" / "Keep reading ◆" / "‹ Back ◆". That was my selector error, not a page defect. Drive 1b re-walked with the text-"Next" button and recorded sequential 1→37. The mislabelled `eye-07-unfold-board37.png` (actually board 1) was deleted rather than left as false evidence; the real board-37 shot is `eye-17-unfold-board37.png`.

**Listen text-check correction:** my drive-1 `listenText` check returned false because I searched for a straight apostrophe — the page uses ’ (U+2019). The screenshot proves the note expands ("Naya's reading arrives with her video." appears twice). The aria-label click itself succeeded.

## 4. DEFECTS A–E RE-CHECK — all still hold (390, my own probes)

| Defect | Re-measure (fix-5) | Verdict |
|---|---|---|
| A — hero name covers certificate title | Name 28px `[19,301,371,329]`; title `[22,282,368,299]`; **overlap 0; gap 2px**; `.cert-certifies` `display:none` in the taken state. Screenshot `eye-02-identity-paired.png`: "CERTIFICATE OF COLLECTIVE AGREEMENT" whole, "Shawn" below it, clean. | **PASS** |
| B — door heading behind corner jewels | Padding 80px/80px; heading 4 lines x127–263; **crest overlap 0 on all 4 lines**. Screenshot `eye-04-door.png`: "Welcome starts with your certificate." whole, both pills visible. | **PASS** |
| C — "already claimed" banner clipped | Banner 5 lines x103–287; **line-vs-crest overlap 0 on all 5**; frame stone `display:none`; stone overlap 0. | **PASS** |
| D — "Congratulations" under orb / photo | Unfold: title 22px, line 1 ends x217, orb `.frame-icon` starts x238 — **21px clear**. Deck: title 22px, line 1 ends x234, face photo starts x274 — **40px clear**. Letter: visible title **24px**, lines end x274, face photo starts x274 — **0px, touching, not overlapping** (visible-only face `[274,204,338,268]`, matching the checker). Screenshots `eye-17/20/21` show all three reading whole. | **PASS** (see note) |
| E — deck photo covers text-box last lines | Deck nutshell `[30,232,300,500]` vs photo `[72,509,258,695]` — **overlap 0 (9px clear)**. Letter nutshell vs photo **overlap 0**. Screenshot `eye-20-deck37.png`: the text box reads whole, the big photo sits below it. | **PASS** |

**D letter note:** the letter's visible title line 1 ends exactly at the photo's left edge (x274 = x274). Pre-existing state — 24px on base and on fix-5, byte-identical, measured identically by the fix-4 checker, who passed it. Touching at the boundary, not covered; the screenshot shows the letter end state reading clean. It is not a fix-5 regression and not a go-back item; it is named here so the 0px is on the record. (My drive-1 letter face rect `[0,0,0,0]` hit a hidden copy of the face element — the same trap the checker hit first; the re-measure with visible-only elements gives the numbers above.)

**Pre-existing caption nick (fix-4 flag (d)) — confirmed unchanged:** the sign photo still nicks the top of the "· NayaNET · The Deck" caption on deck 37 (visible in `eye-20-deck37.png`). Byte-identical files, out of scope, not a regression.

**Desktop 1920 note:** unfold board-37 title 25px `[516,122,1236,152]`, orb `[1252,88,1320,156]` — 16px clear. Screenshot `eye-34-desk-unfold37.png`: "Congratulations — you're hired" whole, centred, clear of orb and photo.

## 5. LAWS — §11 check in writing + eye delta

`check-design-laws.py` run on the fix-4 welcome (my own blob fetch) vs the fix-5 welcome (my own blob fetch). Outputs `work/eye-laws-base-welcome.txt` / `work/eye-laws-fix5-welcome.txt` — 88 lines each, filename-normalized diff empty:

| File | Base FAIL / WARN | Fix-5 FAIL / WARN | Delta |
|---|---|---|---|
| welcome-staged.html | 83 / 4 | 83 / 4 | 0 |

The FAILs are pre-existing checker noise (sub-17px fonts throughout the base files; the word "gray" inside comments). None introduced by this round. Delta 0.

**§11 check, in writing:**
- **Five gates:** (1) Right — the round restores five unreachable legal links to the citizen reading at phone width; nothing harmful. (2) Truly needed — the fix-4 checker's go-back named exactly this defect with measured rects. (3) Mine to do — this check is verification only; no merge, no deploy, no message to the user. (4) Now — the round is staged and the staged host is proven to serve it. (5) Prove it — every claim above carries a measured rect, a log line, or a screenshot I took myself and read with my own eyes.
- **Real objects, one light, elevation, alive on hover:** untouched by this round — no element restyled, only the alignment of one strip. The pages read as real objects throughout (obsidian boards, the red N seal, jewel corners, the Naya photo, the purple/green pills with deep rims). Pass.
- **Type 25/19/17, no grey text:** no text size or colour changed anywhere; the footer links keep their 13px size (pre-existing, counted in the 83 — out of scope for this round, which is charged with reachability only). The 22px board-37 deviation from fix-4 stands as accepted. Pass.
- **Harvest first, compose never create:** the fix edits the file's existing strip rules; nothing rebuilt, nothing redesigned, no new page, no new element. Pass.
- **Don't remove/move what he didn't ask to touch:** desktop rules untouched (1920 geometry proves it link-for-link); F9 code untouched; defects A–E untouched (all re-proven above). Pass.
- **Read as a reader:** I walked the whole flow top to bottom at 390 as a citizen would — root, identity, door, unfold 1→37, deck, letter, bridge — and read every screenshot I took. The footer strip now opens on "Terms of Service" and ends on "Disclaimer", all whole, at both ends of the scroll, on the bridge and on the intro choice view and on the staged host. A citizen swiping the strip reaches every link: the strip scrolls smoothly from Terms to Disclaimer with no dead zone and no link left behind the left edge. The certificate reads clean, the door heading reads whole, the final boards read whole. It reads clean.
- **Button destinations double-checked:** every button on the walk lands where it should — unfold → bridge, deck → bridge, letter → bridge, door Continue → step-1, pair → deck/agreement, "Read the collective agreement" → `/agreement`, "I agree" → bridge. No dead ends, no stale pages. Pass.
- **Phone first:** proven phone-first at 390, desktop confirmed unchanged at 1920. Pass.

**Scorecard (honest):** the page is a 10 on the F acceptance as written — all 12 links reachable on both strips, desktop unchanged, F9 intact, A–E holding, laws delta 0. The remaining known pre-existing items (the 83 laws-checker FAILs, the deck caption nick, the letter title's 0px touch, the intro's missing citizen click-path, the slow bridge-stage render on the remote host) are unchanged from fix-4b and out of this round's scope.

## 6. WHAT WAS NOT PROVEN / OPEN ITEMS

- **The intro strip was not reached by a citizen click** (see §2). No click in the filed bytes opens the intro view directly; it is proven through the page's own stage entry + real render, plus the identical bridge rule proven by real tap. If the captain wants a click path to the intro view, that is a flow question for a later round.
- **The fix-3 state machine (139/139) was not re-run.** The F9 surface it covers is proven instead by the live probes in §3 at both widths, by real tap (including stabilized sequential walks 1→37 on unfold, deck, and letter).
- **The bridge stage JS renders `#fpLegal` slowly on the remote host** (3.4 s / 3.9 s waits needed in my two bridge legs; a 2.5 s wait missed it once). A wait, not a page defect — the strip renders and sweeps clean once present. Named so the next seat does not mistake it for a missing strip.
- **My drive-1 mistakes are on the record, not hidden:** the `#fpNextBtn` selector on `/agreement` (no such element), the contaminated intro "cold" reading (agreed-state restore), the straight-apostrophe Listen check, the deleted mislabelled screenshot. Each is corrected above with its own re-run; nothing in this verdict rests on a first attempt.

## 7. EVIDENCE

All under `~/workspace/team-nitro/walkthrough-agreement-distill-fix5-20261119/eye/` (screenshots are mine throughout):

- **Logs (JSON):** `eye-log1.json` (drive 1 — phone, with the selector miss), `eye-log1b.json` (drive 1b — unfold/deck/letter/anthem/intro), `eye-log1c.json` (drive 1c — bridge re-run), `eye-log2.json` (drive 2 — desktop).
- **Byte + laws proof:** `work/eye-blob-verify.json`, `work/eye-laws-base-welcome.txt`, `work/eye-laws-fix5-welcome.txt`, plus the fetched file copies (`work/eye-fix5-*.html`, `work/eye-fix5-*.js`, `work/eye-fix5-*.py`, `work/eye-fix4-welcome-staged.html`).
- **Drivers (mine):** `work/eye-verify-blobs.py`, `work/eye-drive1.py`, `work/eye-drive1b.py`, `work/eye-drive1c.py`, `work/eye-drive2.py`.
- **Screenshots — phone 390:** `eye-01-root-390.png`, `eye-02-identity-paired.png`, `eye-03-banner.png`, `eye-04-door.png`, `eye-05-after-continue.png`, `eye-06-unfold-board1.png`, `eye-11-letter37.png`, `eye-12-after-anthem.png`, `eye-13-after-listen.png`, `eye-14-intro-s0.png`, `eye-15-intro-smax.png`, `eye-16-unfold-board1.png`, `eye-17-unfold-board37.png`, `eye-18-bridge-s0.png`, `eye-19-bridge-smax.png`, `eye-20-deck37.png`, `eye-21-letter37.png`, `eye-22-after-anthem.png`, `eye-23-after-listen.png`, `eye-24-intro-s0.png`, `eye-25-intro-smax.png`, `eye-26-bridge-s0.png`, `eye-27-bridge-smax.png`.
- **Screenshots — desktop 1920:** `eye-30-desk-root.png`, `eye-31-desk-identity.png`, `eye-32-desk-door.png`, `eye-33-desk-unfold1.png`, `eye-34-desk-unfold37.png`, `eye-35-desk-bridge.png`.

## 8. HANDOFF

**Verdict: PASS.** Defect F is fixed: all 12 footer links are reachable at 390 on the bridge (real tap, twice) and on the intro strip (real render in a fresh browser), desktop 1920 is unchanged link-for-link, F9 passes at 390 and 1920 with 0 console errors, A–E re-measure clean, bytes 6/6 verified, laws delta 0. The staged link verified is https://naya-walk-beginning-staging.nayapower.workers.dev/ (fix-5 bytes on all four routes). The one honest limit is the intro strip's citizen click-path: no click in the filed bytes opens the intro view directly, so it is proven through the page's own stage entry and the identical bridge rule — stated in §2 and §6, not hidden. Ready for the captain's next step. No merge, no live deploy, no message to the user from this seat.
