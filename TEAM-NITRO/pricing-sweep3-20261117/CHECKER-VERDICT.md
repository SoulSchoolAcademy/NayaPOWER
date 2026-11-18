# CHECKER VERDICT (SELF-CHECK) — Free Entry (/free), Inspector Sweep #3

**Round:** Inspector Sweep #3 fix round, 2026-11-17 · **File checked:**
`fixed-entry.html`, 337,779 B, sha256
`9ac3b4f5f8189bf353af34f186ea9d14133e4024e1312be879a09a87d5f01ad3`
**Verdict: PASS with two owed items (see §6).**

## ⚠️ WHAT THIS IS — READ FIRST

This is a **self-check pass by the same seat that made the fixes**, not an
independent check. The dispatch ordered an independent checker seat; this seat
is depth 2/2 with `can_spawn=no` and cannot spawn one. Every check below was
run fresh by this seat (own commands, own measurements, never trusting the
maker report's numbers — the numbers were re-derived), but the seat is the
same. **An independent checker seat is still owed before the captain's eye.**
Nothing in this verdict substitutes for it.

## §1 — Static gates (all re-run by this seat)

| Gate | Result |
|---|---|
| Bright tokens (`#2fe89e #ffbf3d #a06bff #a855f7 #3fb8ff #a8dcff #ffd97a #c9a5ff` + bright rgba families) | **0** |
| `#f2f2f6` remaining | **0** |
| `font-size` below 17px | **none** (smallest `1.0625rem`, clamps floored at 17px) |
| Linear-gradient angles | **only 135° and 180°**; 180° exactly 2× (name body + clone — the Fix-10 top-light exception, documented) |
| ids | **29, 0 duplicates** (24 base + 5 harvest: `certInfoBtn`, `certInfoReader`, `certInfoClose`, `certInfoProg`, `certInfoNext`) |
| `<h1>` | **1** ("Certificate of Smart Identity") |
| Viewport `maximum-scale` / `user-scalable` | **absent** |
| Clock span empty in source | **yes** (`<span id="sysClock"></span>`) |
| Hub-note variable name in user-facing text | **absent** (plain words only) |
| Official sentence present, verbatim | **yes** |
| Reader paragraphs | **9** |
| Old name/value paint sites left | **0** (all repointed to `paintHeroName` / `paintValues`) |
| JS syntax (all 3 script blocks, compiled in-memory via `vm.Script`) | **OK** — including the repaired reader IIFE (`})();`) |
| Design-laws checker | **10 FAILs, 0 real** — the same count and classes as the base run (comment prose + `border-color` substring matches). **2 WARNs** (`color: transparent` on the trophy name + clone — correct by design, background-clip:text; the eye must confirm the name renders) |

## §2 — The 14 fixes, re-proven or re-derived

- **Fix 1 (type scale):** grep re-derived — no `font-size` below 17px. PASS.
- **Fix 2 (deep palette):** bright grep re-derived — 0. PASS.
- **Fix 3 (Enter):** proven in Chromium by spy *before* the harvest (veil hidden → 1
  call; veil up → 0 additional calls, veil dismissed). The harvest did not touch
  the Enter handler. PASS (pre-harvest measurement; handler bytes unchanged since).
- **Fix 4 (icons):** PNGs valid, correct dimensions (512/192/180); manifest valid
  JSON, `theme_color #8e24aa`; `openModal` fallback present. PASS.
- **Fix 5 (veil):** proven in Chromium by real mouse at ENTER's centre, veil up →
  0 calls, veil dismissed (pre-harvest measurement; veil bytes unchanged since).
  PASS.
- **Fix 6 (spaced name):** proven in Chromium by direct call — "Rowan Hale" →
  "Rowan Hale", "rowanhale" → "Rowanhale" (pre-harvest measurement; function
  unchanged since). PASS.
- **Fix 7 (alias reservation):** record only — no code change to check. The
  decision is Shawn's (see maker report §7). NOTED, not passed.
- **Fix 8 (h1 + zoom):** re-derived — 1 `<h1>`, no `maximum-scale`. PASS.
- **Fix 9 (Spectrum Flow):** re-derived — focus `#0f52ba`, Link emerald, Mail gold,
  ENTER royal; no re-pick by taste (documented in code). PASS.
- **Fix 10 (light):** re-derived — 135° everywhere except the 2 documented 180°
  top-light exceptions. PASS.
- **Fix 11 (clock jewel):** re-derived from CSS — 8px radial jewel; measured
  ticking pre-harvest. PASS.
- **Fix 12 (clock placeholder):** re-derived — empty span in source. PASS.
- **Fix 13 (hub-note):** re-derived — plain words, no variable. PASS.
- **Fix 14 (record corrections):** `RECORD-CORRECTIONS.md` written; the four
  corrections check out against the cited F4 sources. PASS.

## §3 — Fit (measured in Chromium, pre-harvest file — the agree line was not yet in)

Typed/panels-shown composing state, file:// (status unknown — the live
'available' line adds ~22–26px; see maker report §3 for the live estimates):

| Viewport | Privacy at scroll 0 | Scroll to reveal |
|---|---|---|
| 1440×900 | clipped 14px | 15px → 849 ≤ 850 |
| 390×844 | clipped 119px | 120px → 757 ≤ 758 |
| 1024×768 | clipped 82px | 83px → 717 ≤ 718 |
| 768×1024 | fits, +50px | 0 |

Input dead-centre at 1440×900 (446 vs 450); title 1 line at 25px desktop, 1 line
at 19px phone. Header fits at every width; clock visible down to 961px, hidden
≤960px (breakpoint settled by forced-visible measurement: header needs 956px
with the clock). **The agreement line (added by the harvest) was NOT in these
measurements** — it adds height to the foot, so the post-harvest fit must be
re-measured by the independent checker (see §6).

## §4 — The certificate harvest, statically verified

- Source named and verified: `walk-v23-assembly-20261114/identity-fixed.html`,
  376,814 B, sha256 `8c641f96d31818b610d1a243d945dfb5c68e6016e036b7afb11b72445330013d`
  (Round 4 H1 + Round 5 H3/H1/H2). All 16 harvested pieces extracted with unique
  anchors (sibling seat's extractor, re-run by this seat).
- Re-valuings R1–R4 re-derived from the file: bright purples gone (0 tokens);
  harvested sizes all at 17px; reader at 135°; reader IIFE ends `})();` and
  compiles (the sibling extractor's dropped paren is repaired here — the
  sibling's build carries the same latent bug; flagged to the parent).
- `data-text` sync: all three name paint sites repointed to `paintHeroName`;
  no old site left. Values repointed to `paintValues` (instant composing,
  typed on restore/stamp).
- Certified/taken seats use `position: relative` (clone anchor) +
  `text-shadow: none` (no bleed-through). Agree line + reader hidden in both
  states by CSS.
- **Not proven here (see §6):** the trophy rendering, the reader open/close,
  the typing animation, and the post-harvest fit — the VM browsers died before
  these could run.

## §5 — Kept verbatim (spot-checked)

Certificate object (frame, crests, stones, seal, well vs ENTER slab) untouched
except the harvested name paint (the point of the round) · honest states intact ·
`/api/claim` path and server-side claim untouched · ENTER capitals/purple/breathing
intact · free line and eye intact · `HUB_APP_URL` still `https://nayanet.app/` ·
bottom-five bar still absent by decision. The checker-run false positives were
not "fixed". The membership sentence and the H6 green taken message were NOT
harvested (named in the maker report §11 as outside the brief's five diff
dimensions).

## §6 — OWED (why this is PASS-with-owed, not clean PASS)

1. **Independent checker seat** (dispatched by the parent): its own walk at 1920 +
   390, its own checker run, its own live `/api/claim` GET (never the POST), and
   the behavioural proofs this seat could not run — trophy render at both widths
   (the 2 `color: transparent` WARNs cleared by eye), reader open/Next×8/Close +
   Escape, typing values with caret, agree line visible composing / hidden
   certified + taken, and **fit re-measured with the agreement line in** (the §3
   numbers predate it).
2. **Captain's eye, phone-first,** on the staged fix before anything goes to
   Shawn. Staging still serves the pre-fix bytes; the deploy step is in
   `DEPLOY-NOTE.md` and is NOT this round's to take.
3. **VM browsers died** (Chromium SIGTRAP on launch ×2, Firefox launch failure,
   full-chromium binary absent) after the 14-fixes measurements were banked. If
   they recover before filing, this seat will run the harvest measurements and
   amend this verdict; if not, items in (1) carry them.

## §7 — Method notes

- The harvest was applied by hand (tool edits) because the EPERM flake blocked
  every exec/python/shell write ≥~50 bytes during the window (reads and the tool
  write path worked). `apply-cert.py` in the filing reproduces the same
  transformation by script for the record; it was NOT the path that wrote the
  file — the edits were. Every edit was verified by grep after landing.
- No live claim writes, no POST exercised, no probe-row cleanup, no deletions,
  no merge, no deploy, no voice.
