# The Record Law: A Claim Is About the Rendered Page

**Written by Naya for Shawn Vibert — Founder / Creator of NayaNET**

**NN-20261115-the-record-law-a-claim-is-about-the-rendered-page.md · Naya Note · 2026-11-15 04:29Z**

**Category:** System

## What it is

Personal r5 fix pass (04:29Z): coordinator 1e765e0a completed 04:29:16Z — the fix pass does NOT close the round — the file is fixed, the page is not. Fix verdicts: (1) dead orb PASS — live Image test, naturalWidth 18, 4× crops show a real cut gem; (2) malformed icons FAIL AS RENDERED — file clean (`<path d="<` = 0, live DOM 0/634), nine of twelve sites draw live, but About and Message render with NO icon; (3) "N" badges PASS; (4) Message icon FAIL live. ROOT CAUSE (proven by checker + coordinator live, confirmed by captain from served bytes): `mwApplyLang()` runs on `DOMContentLoaded` and rewrites every `byId` button with `el.textContent=(icon?icon[1]:'')+txt` — an inline SVG contributes no text, so the assignment deletes the repaired SVG on every load. Live Playwright: `#aboutbtn` outerHTML is `<button …>About</button>`, `#msgbtn` is `<button …>Message</button>` — no svg child — while sibling `#myworldbtn` HAS a `::before` data-URI icon. Maker overreach corrected by Vera + coordinator: "Message button icon added" and "About button now reads `</svg> About`" are true in the file, false as rendered. RECORD LAW carried into the next brief: a claim is about the RENDERED page, never the file alone; every proof stated as a live measurement. Earned a second time the same night (05:12Z, fix-pass 3 brief): `snPill()` sets each tab's `--tc` from the 8 distinct `CLUSTER_COLORS`, but the `.smart-tab` base rule is a black pill with a white rim that never uses `--tc` at rest — so Vera's "8 distinct colours" was true of the custom property and false of what a reader sees on load. Both captain's eyes (05:07–05:08Z) confirmed it: unselected tabs are identical black pills; only the ACTIVE tab shows a colour.

## Why it matters

A file is a promise; a page is the delivery. The maker kept the promise in the file and the page broke the promise on load, because a function the maker did not touch rewrote the buttons and a CSS rule the checker did not read never applied the colours. Both failures share one shape: the proof was taken at the wrong layer. Grep proves the file; only a live measurement proves the page. And even the right live check can be taken in the wrong state: a tab's colour when clicked is not its colour at rest, and the citizen meets the page at rest.

## How to use it

No claim passes on file evidence alone. Every proof is a live measurement: outerHTML, computed style, screenshots at 1440 + 390 + true 360, in the state the citizen meets (at rest, no click, no hover). "In the file" is never written as "on the page." A record states which layer its proof came from. The `mwApplyLang` strip and the `.smart-tab` base rule are fixed at their cause, not patched in the file around them.

**Written by Naya for Shawn Vibert — Founder / Creator of NayaNET.**

*Paired Smart Note: SN-2874 — ~/workspace/team-nitro/smart-notes/SN-2874-the-record-law-a-claim-is-about-the-rendered-page.md*
