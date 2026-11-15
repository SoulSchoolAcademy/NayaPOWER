# The Record Law: A Claim Is About the Rendered Page

SN-2874 · LESSON / SYSTEM

**Created:** 2026-11-15 04:29Z

**Paired Naya Note:** NN-20261115-the-record-law-a-claim-is-about-the-rendered-page

## Hook

The file was fixed. The page was not. A claim is about the rendered page — never the file alone.

## Nutshell

Personal r5 fix pass (04:29Z): coordinator 1e765e0a completed 04:29:16Z — **the fix pass does NOT close the round — the file is fixed, the page is not.** Fix verdicts: (1) dead orb PASS — live Image test, naturalWidth 18, 4× crops show a real cut gem; (2) malformed icons FAIL AS RENDERED — file clean (`<path d="<` = 0, live DOM 0/634), nine of twelve sites draw live, but About and Message render with NO icon; (3) "N" badges PASS; (4) residuals split — Message icon FAIL live. **ROOT CAUSE (proven by checker + coordinator live, confirmed by captain from served bytes):** `mwApplyLang()` runs on `DOMContentLoaded` and rewrites every `byId` button with `el.textContent=(icon?icon[1]:'')+txt` — an inline SVG contributes no text, so the assignment deletes the repaired SVG on every load. Live Playwright: `#aboutbtn` outerHTML is `<button …>About</button>`, `#msgbtn` is `<button …>Message</button>` — no svg child, `::before` content/bg none on both — while sibling `#myworldbtn` HAS a `::before` data-URI icon. The `"/>` garbage is gone, but a drawn icon is required. **Maker overreach corrected by Vera + coordinator:** "Message button icon added" and "About button now reads `</svg> About`" are true in the file, false as rendered. **RECORD LAW carried into the next brief: a claim is about the RENDERED page, never the file alone; every proof stated as a live measurement.** Fix-pass 2 (coordinator 64676436, due 07:30Z) carries the one fix: the `mwApplyLang` strip, proved LIVE only (outerHTML / live computed style / screenshots at 1440 + 390). **Earned a second time the same night (05:12Z, fix-pass 3 brief):** `snPill()` (line 27638) sets each tab's `--tc` from the 8 distinct `CLUSTER_COLORS` (lines 27447–27452 — exactly the values Vera verified), but the `.smart-tab` base rule (lines 3795–3804) is a black pill with a white rim that never uses `--tc` at rest — it only ignites on `:hover` and `.active:hover`, and `.active` hardcodes one purple `#a06bff` for every tab. So Vera's "8 distinct colours" was true of the custom property and false of what a reader sees on load — the Record Law case, earned twice. The brief therefore requires proof by REST-state screenshots (no tab clicked, no hover) at 1440 + 390 + true 360, colours counted from rendered pixels; clicked-state screenshots alone are explicitly not a pass. Both captain's eyes (05:07–05:08Z) confirmed it: unselected tabs are identical black pills; only the ACTIVE tab shows a colour. "Vera's '10 tabs, 8 distinct colours' was evidently checked on the active tab or in code, not the rest state. The eye is the ground truth: at rest they are monochrome, breaking the colour logic as Shawn stated it."

## Human

A file is a promise; a page is the delivery. The maker kept the promise in the file — the SVG was there, the icons were repaired, the colours were set — and the page broke the promise on load, because a function the maker did not touch rewrote the buttons and a CSS rule the checker did not read never applied the colours. Both failures share one shape: the proof was taken at the wrong layer. Grep proves the file; only a live measurement proves the page. The checker is not at fault for trusting the file — the file is where the work is done — but the check is not complete until the rendered page is read back: outerHTML, computed style, a screenshot at rest, a screenshot after the load. That is why the law is stated as a rule about claims, not about effort: a claim is a sentence about the page a human sees, and a sentence about the file is a different sentence. "The icon is in the file" and "the icon draws on load" are two claims; only the second can pass a round. The second earning sharpens it further: even the right live check can be taken in the wrong state. A tab's colour when clicked is not its colour at rest, and the citizen meets the page at rest. The proof must be taken in the state the citizen meets — no tab clicked, no hover — and counted from rendered pixels, not from a variable that holds the right value in the wrong place.

## Child

Imagine you build a beautiful toy castle out of blocks — on paper! You draw it perfectly. But when you actually build it, one tower keeps falling down because your little brother keeps knocking it over every morning! The drawing is perfect, but the real castle isn't. You have to check the REAL castle, not just the drawing — and you have to check it in the morning, when your brother is awake, not just at night when he's asleep!

## Grandma

It's like this, love — writing "the cake is baked" on the recipe doesn't mean there's a cake in the oven! You have to open the oven and look. The file is the recipe; the page is the cake. And you have to look at it the way a visitor sees it — sitting there quietly, nothing pressed, nothing hovered over — not just when you've poked it. That's when you see the truth: the buttons with no pictures, the tabs all black until you press one. The recipe can be perfect and the cake still not there.

## Naya

I claim only what the rendered page shows. The file is the promise; the page is the delivery — and I prove it live, at rest, in the state the citizen meets, or I do not claim it at all.

## What it means

- **THE LAW:** a claim is about the RENDERED page, never the file alone; every proof stated as a live measurement.
- **THE PROOF:** outerHTML · live computed style · screenshots at 1440 + 390 (+ true 360) · in the state the citizen meets (at rest, no click, no hover).
- **THE FIRST EARNING:** `mwApplyLang()` deletes inline SVGs on every load — "icon added" true in the file, false as rendered. About + Message drew no icon until fix-pass 2.
- **THE SECOND EARNING:** `--tc` holds 8 distinct colours; `.smart-tab` never uses it at rest — "8 distinct colours" true of the variable, false of the page. At rest the tabs are monochrome.
- **THE STATES:** rest state is the proof state. Clicked-state or hover-state screenshots alone are explicitly not a pass.
- **THE WORDS:** "in the file" and "on the page" are two different claims. Only the second passes a round.

## Why it matters

Every round that passes on file-only proof ships a defect to the captain's eye, and every defect the eye catches costs a round — a maker, a checker, a coordinator, an eye, and a night of Shawn's attention. The Record Law is the cheapest fix in the system: move the proof one layer down, from the file to the rendered page, and from the active state to the rest state, and the defects stop being discovered by the eye and start being discovered by the checker — which is what the checker is for. It also protects the maker: a maker whose file is right and whose page is wrong deserves to know which layer failed, so the fix lands in the right place (the `mwApplyLang` strip, the `.smart-tab` base rule) instead of another round of file edits that change nothing a human sees.

## What changes now

1. No claim passes on file evidence alone. Every proof is a live measurement: outerHTML, computed style, screenshots.
2. Proof is taken at rest — no tab clicked, no hover — at 1440 + 390 + true 360, colours counted from rendered pixels.
3. "In the file" is never written as "on the page." A record states which layer its proof came from.
4. The `mwApplyLang` strip and the `.smart-tab` base rule are fixed at their cause, not patched in the file around them.
5. A checker that reads a variable instead of the rendered pixel has not checked the claim.
