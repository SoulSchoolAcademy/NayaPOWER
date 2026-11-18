# MAKER REPORT — Pricing Fix Round (2026-11-17)
**Round:** BRIEF-PRICING-FIX-20261117 · **Date:** 2026-11-17 ~06:01–06:40Z
**Maker:** Naya Nitro Narzan · **Branch:** `pricing-f4-free-entry-20261116` (PR open, unmerged)
**Base:** taken-fix tip — `/free` 311,426 B, sha256 `3d5b913f117b90a1fdd3e72347f8458c4de4429972eb05a38c6fb118f7fbf285`
**Staged:** https://naya-pricing-free-staging.nayapower.workers.dev/free
**Nothing live, no merge.** The live step stays HELD until this round's eye passes.

## 0. Base reproduction — EXACT, before any edit

`repro-base.py` regenerates the tip in memory from the filed build chain
(F4 builder + F4 fix + follow-on + Marcellus swap + taken fix) and compares
to the staged bytes:

| Artifact | Reproduced in memory | Staged live | Match |
|---|---|---|---|
| `/free` entry | 311,426 B, sha256 `3d5b913f…` | 200, 311,426 B, sha256 `3d5b913f…` | **EXACT** |
| `/free/walk` | 3,292,257 B, sha256 `2370eae2…` | (unchanged base) | **EXACT** |

No edit was made from a guessed base. The build script (`build-fix.py`)
re-asserts both base shas and that live staged `/free` still serves the
tip entry before patching anything (on rebuild it also accepts this
round's own previous fixed entry, since live already serves it).

## What changed — entry +47/−4 lines, walk +30/−7 lines

### Item 1 — Long taken name wraps mid-word at 635 — FIXED
Taken name: `white-space:nowrap` + narrow-width font cap
(`@media (max-width:700px)` → `clamp(1.65rem, 6.2vw, 2.5rem)`) +
a JS shrink-to-fit (`fitTakenName`, called on every input, every state
change, resize, and font load) that steps the size down until the
one-line name fits its row. Only ever shrinks, never grows; only runs
in the taken state. Gated on the taken state only.

### Item 2 — Descender overlap at desktop — FIXED
Taken name: `line-height:1.14; padding-bottom:.14em; margin-bottom:10px`
— the Marcellus descenders (p, g, y, j) now clear the alias-box top
border below at both widths. (At 635 the eye measured a 16px gap
already; the fix holds there too.)

### Item 3 — Fresh-cert name echo — ROOT CAUSE FOUND + FIXED
**Root cause, proven in the worker code:** the claim POSTs
`name = rawName || prettyName(alias)`; at a fresh entry `rawName` is
empty, so the registry row's name IS the alias echo — and
`/api/welcome/complete` only stores the completion record in KV, it
never updates the identity row. The walk never saved its typed name
anywhere the entry reads: step-1 answers live only in `S.answers.about`
and the names-page title only in `S.pageNames`. On reload the 'own'
restore preferred `certRegalia.name` (registry echo) over localStorage.
That is why desktop (which arrived with a spaced `?name=`) showed the
spaced name while 635 (alias-only entry) showed the echo — same code,
different inputs, not a width bug.
**Fix, both ends:** (a) the walk adopts a name-like typed answer — step 1
("Tell me who you are") and the names-page personal title — into
`ID.name` + `localStorage nayanet_smart_name` (so the completion payload
carries it too); a name-like answer is 1–4 words, ≤40 chars,
letters/spaces/hyphen/apostrophe/period only — a sentence stays an
answer, never a name. (b) The entry's 'own' restore prefers the
walk-saved local name over the registry echo whenever it differs from
the echo. Both widths now run the same rule and agree.

### Item 4 — Install veil — FIXED
(a) The auto-show never fires over a finished (`is-certified`) or taken
document. (b) `stampCertificate` and the own/taken state change close
an open veil at once (hide only — automatic closes do NOT write the
user's dismiss key). (c) The veil is pointer-transparent (CSS, card
still clickable) and ANY first interaction dismisses it
(pointerdown/keydown) — only the card's own BUTTONS are exempt.
**Honest correction inside this round:** the first shape exempted all
clicks inside the card — but the centered card sits over ENTER, so an
ENTER click landed on the card and was exempted; a real-mouse probe
caught the veil never dismissing. The guard now exempts buttons only.
The dismissing click does not also fire the control beneath it; the
next click acts — the brief's "dismiss on first interaction" shape.
(d) Opening the veil no longer locks body scroll. The invite itself is
unchanged (same card, same 3-lifetime-auto-show cap, same dismiss keys,
manual open via the corner button still works).

### Item 5 — Duplicate id="enterBtn-14" — FIXED
The walk's step-names section reused step-14's ids — not one but three
duplicates (`enterBtn-14`, `playBtn-14`, `enterNote-14`). All three are
renamed in the names section (`enterBtn-names` / `playBtn-names` /
`enterNote-names`) and `wireNames` + `resetNamesEnter` use the new ids.
Step 14 keeps `enterBtn-14`. Live check: 145 ids in the walk, zero
duplicates.

### Item 6 — FILE THE BYTES — DONE (closes the taken-state filing gap)
The fixed entry bytes AND the fixed walk bytes are filed on the branch
(see Filing below) — verifiable by blob sha. No more "bytes only on
staging".

## What stands (untouched, asserted in the build)
- Taken flow (green "already claimed", start-over, no new rows from
  taken checks) · fresh claim flow · Marcellus on the certificate.
- Certified CSS rules byte-identical (asserted: every old
  `.cert-plaque.is-certified` rule and every old `.cert-name` rule
  present unchanged in the new entry).
- `/free/walk` base unchanged in shape: only the item-3/5 edits above
  (walk diff +30/−7 lines); pricing v78 unchanged (see below).

## New bytes (staged + filed)
- `/free` entry: **315,878 B**, sha256
  `06b08242c72e9d0b8f28037df3b93e74c5955e6702f358d0a07fff799edf58fd`
- `/free/walk`: **3,293,555 B**, sha256
  `46bc52e54ac02e87cdad0ae2924ce35555671333ce3c7cd96676f17d86253fa1`
- Staging worker: **3,630,970 B**, sha256
  `59e658353c079ca4ce3f8c7f8d37341efdd9bec92770bee22c1c77e48761fb90`
  (gzip 2,548,752 B, under the 10 MB limit; read-back MATCH)
- `/sw.js` 567 B sha `abac2ab5…` · `/manifest.webmanifest` 581 B sha
  `b4abd81c…` (live verbatim, unchanged) · `/free/hub` 302 → nayanet.app
- Pricing v78: **11,360,503 B** sha `ca2eafeb…` **UNCHANGED** (live check
  on its own staging worker)

## Live verification — all six items (Playwright Chromium via forwarder)
Probe: `probe-fix.py` + `probe-veil-mouse.py`; results `probe-fix.json`;
screenshots `shots-fix/`. **Zero console errors across all runs.**

### Item 1 — taken long name one line — PASS
`alexanderchristopherbennett` (29 chars), glyph Range rects = 1 line:
- 635×900: font 39.37px, `scrollWidth <= clientWidth`, fits. Screenshot
  `taken-long-635x900.png`: one line, clear, glowing, readable.
- 1440×900: font 78.4px, fits. Screenshot `taken-long-1440x900.png`:
  one line, glowing.
- Short alias `takenfixshort`: one line at both widths.

### Item 2 — descender clearance — PASS (measured on glyphs, not boxes)
Range-rect glyph bottom vs alias-box top: **635: 14px clear** (glyph
bottom 321, box top 335); **1440: 17px clear** (425 vs 442).
Screenshots read with my own eyes: at desktop the "p" descenders sit
well above the green alias-box border at both widths. `captainlivecheck1`
was not re-claimed (its row belongs to another lane); the proof uses the
29-char name, which carries the same descenders (p) at both widths, and
the short alias.

### Item 3 — fresh cert shows the walk's typed name — PASS, both widths agree
New alias `fixfresh17c` → walk, step 1 typed "Poppy Green":
localStorage `nayanet_smart_name` = "Poppy Green" immediately after
step 1; completion payload `name` = "Poppy Green"; end slide reached.
Reload at **635**: certificate **"Poppy Green"**, Nº **000782**,
certified November 17, 2026 · 06:32 UTC. Same identity at **1440**:
**"Poppy Green"**, same Nº/date. Screenshots `fresh-635-cert.png`,
`fresh-1440-cert.png` — Marcellus, glowing, no veil.
(An earlier probe run claimed `fixfresh17a` and walked it, but died
before the reload check when its device key died with the closed
context; the reload proof uses `fixfresh17c`. A second consolidated
run re-proved the same with `fixfresh17c`, Nº 000782.)

### Item 4 — install veil — PASS
- Taken document: veil never shows (auto-show gate) — still hidden
  after 7s at both widths, `install.shows` untouched.
- Certified document: veil never shows after reload — still hidden
  after 7s at both widths.
- Stamp: veil up at claim → `veilHiddenAtStamp=True` (stamp closes it).
- Composing: veil auto-shows at 5s; a **real mouse click** on ENTER
  dismisses it (dismissed=1), and the **next** click activates ENTER
  ("Enter alias to continue."). Start-over from taken works
  (neutral, keys cleared).
- Note for the checker: Playwright locator clicks refuse a covered
  element, so the ENTER-through-veil proof uses real mouse clicks
  (`page.mouse`), not locator clicks — that is stricter than a human,
  not a page fact.

### Item 5 — duplicate ids — PASS
Walk: 145 ids, **zero duplicates**; `enterBtn-14` ×1 (step 14),
`enterBtn-names` ×1 (names page).

### Scroll / ENTER at 635 — PASS
635×349 taken (long): ENTER below the fold at load (y550–608); user
wheel → plaque scrollTop 0→22, scrollY 0→511, ENTER y17–75 in viewport;
click on ENTER's visible part (below the 50px sticky top bar) shows the
taken hubNote ("That alias is already claimed on another device…").

### Fresh regression — PASS
Fresh certificate (own-device restore) at 390/635/1440 in prior rounds
is unchanged in shape; this round's fresh claim (above) is the live
regression, and the certified CSS rules are asserted byte-identical.

## Filing
- Branch: `pricing-f4-free-entry-20261116` — commit on top of tip
  `fc6f70b0`, no merge, nothing live. Files on the branch (this round's
  folder, under `TEAM-NITRO/pricing-fix-20261117/`): this report,
  `build-fix.py`, `probe-fix.py`, `probe-veil-mouse.py`,
  `fixed-entry.html` (**the fixed /free bytes**, 315,878 B),
  `fixed-walk.html` (**the fixed /free/walk bytes**, 3,293,555 B).
- Filing script: `file-fix-to-github.py` (git data API: blobs → tree →
  commit → ref PATCH; verifies the ref and blob read-backs by sha256).
- **Filed commit SHA: `e6bf9a87fbe80f33515f9117516375deec6c334b`** (on top
  of tip `fc6f70b0`; ref verified; all 6 blobs read-back MATCH).
  Fixed entry blob `069dc721e14d16ed487ff239df3824d54308cade`
  (sha256 `06b08242…`); fixed walk blob
  `69187bb3db00a6bcbaaa5c9b6ef79aab1f41416b` (sha256 `46bc52e5…`).

## Test Supabase rows (Shawn's hand for cleanup)
- `fixfresh17a` (claimed + walked, cert Nº unknown — device key lost
  with its probe context), `fixfresh17b` (claimed + walked, Nº 000781),
  `fixfresh17c` (claimed + walked, Nº 000782) — three new rows this
  round, all "Poppy Green". Plus the eye's Nº 000779 (`eyefresh635j`)
  and the reserved-but-unfinished `eyefresh635a–h`. No delete attempted.
- Taken checks created no new rows (certs 753/755 reused).

## What I could not prove
- `captainlivecheck1` at desktop was not re-run live (its row belongs
  to another lane; the descender proof uses the 29-char name's own "p"
  descenders at both widths instead). The checker may re-run it.
- The veil's first-click-dismiss means the dismissing click does not
  also fire ENTER — a citizen clicks ENTER once (veil vanishes) and
  again (ENTER acts). That is the brief's sanctioned shape, not a bug,
  but the checker should confirm it reads fine to the eye.
