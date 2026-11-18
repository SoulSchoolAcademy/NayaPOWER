# RECORD CORRECTIONS — Free Entry (/free), Inspector Sweep #3, Fix 14

**Round:** Inspector Sweep #3 fix round, 2026-11-17 · **Seat:** Fix Coordinator acting
as maker (see the maker report §9 — no independent checker seat could be spawned).
**Subject:** the F4 record (`~/workspace/team-nitro/pricing-fix-20261117/MAKER-REPORT.md`
+ `CHECKER-VERDICT.md`), as the inspector's Fix 14 asked. No page change for these
items — record only, except where Fix 5 changed the shipped bytes (item 3).

## 1. "145 ids" — the F4 record is CORRECT; the inspector is wrong

The inspector's Fix 14 says the F4 record's "145 ids" is wrong because "the file has
24 ids, 0 duplicates". The inspector conflated the two files:

- `fixed-entry.html`: **24 ids, 0 duplicates** — verified this round (and now 29 ids,
  0 duplicates, after the certificate harvest added `certInfoBtn`, `certInfoReader`,
  `certInfoClose`, `certInfoProg`, `certInfoNext`).
- `fixed-walk.html`: **145 ids, 0 duplicates** — verified this round against the F4
  file (`pricing-fix-20261117/fixed-walk.html`).

The F4 record's "145 ids" refers to the walk file. It stands. Do NOT "correct" the
F4 record on this point. Sources: `pricing-fix-20261117/MAKER-REPORT.md:83,163`,
`CHECKER-VERDICT.md:108`.

## 2. "Rowan Hale Nº 000784 / Milo Fern Nº 000785" — stands as the F4 live record

The F4 `CHECKER-VERDICT.md:75–77` records live verification of these two
certificates (`checkfresh17d` 06:45 UTC, `checkfresh17e` 06:46 UTC). A static read
cannot re-prove them, and this round performed no live claim write and no
probe-row cleanup (no authority for either). Status: **stands as the F4 checker's
live record — not re-verified here, not disproven.**

## 3. Veil "1st click dismisses only, 2nd fires ENTER" — true only for covered geometry

The F4 record's veil claim does not match the shipped bytes. The F4 probe
(`probe-veil-mouse.py`, real mouse at 635px) only proved the **covered** geometry:
the install card sat over ENTER's centre, so the click died on the common-ancestor
rule. The shipped bytes were `pointer-events:none` on `.install-veil` with a button
exemption in the pointerdown handler — so wherever the install card did NOT cover
it, ENTER fired — and claimed — on the **first** click under the visible veil.

This round changed the shipped bytes (Fix 5): the veil now intercepts
(`pointer-events:auto`) — the first click dismisses only, never reaches the
control beneath, at every geometry. Proven by real mouse click at ENTER's centre
with the veil up: 0 claim calls, veil dismissed. The F4 claim is corrected to:
"dismisses-only only where the card covers the control; uncovered controls fired
on first click." Sources: F4 veil claims `CHECKER-VERDICT.md:87–99`,
`MAKER-REPORT.md:61–73`.

## 4. ".logo-hero does not exist" — it does

The inspector's Fix 4 premise ("openModal copies a `.logo-hero` that does not
exist — give the card a real src") is wrong. `.logo-hero` exists (the seal `<img>`
with the embedded 512×512 crystal-N JPEG); `openModal` copying its `src` into
`#installLogo` already worked. The real Fix 4 defect was only the manifest icons
404 + `theme_color`. The install card also gained an icon fallback
(`icons/apple-touch-icon.png`) so it never renders an empty logo box.

## 5. What this round did NOT re-prove (named, not hidden)

- The taken/certified states **live** (file:// cannot reach `/api/claim`; staging
  serves the pre-fix bytes). The face-scroll rule covers the taken state too, but
  that is reasoning from the selector, not a live measurement.
- The live `/api/claim` GET (staging still serves the pre-fix bytes; the fix
  changes no API path).
- The certificate harvest's behaviour **in a browser** (trophy render, reader
  open/close, typing, fit with the agreement line): the VM browsers died
  (Chromium SIGTRAP, Firefox launch failure) after the 14-fixes measurements were
  banked and before the harvest measurements could run. Static verification of
  the harvest is complete (guards, JS compile, checker at baseline — see the
  maker report §11 and the checker verdict); the behavioural proofs are owed to
  the independent checker and the captain's eye, which the brief requires anyway.
