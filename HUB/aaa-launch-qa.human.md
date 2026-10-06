# The AAA Launch Checklist

**STATUS: PROPOSED — candidate acceptance methodology for the 10/10 bar. Awaiting Shawn's review. Not law. Nothing is gated on it until he says so.**

---

Shawn, the HMC Button Spec's second half is a complete product launch QA methodology — 19 sections, A through S. The product references inside are dated (Groove checkout, free trials, the old player); the *methodology* is timeless, and the distillation says it applies directly to our 10/10 bar. This is the proposal to adopt it.

## The methodology in your own words

The closing standard from the material — proposed as the build loop's definition of done:

> "We define the full system, implement from one source of truth, test every visible feature, record every failure, and do not call it complete until the checklist passes."

That sentence is the 10/10 bar in your own words. The proposal is to quote it in the build loop's definition of done.

## The 19 sections (what each one checks)

- **A. First impression** — a first-time visitor knows what to press without explanation
- **B. Button system** — every control follows the button standard, all states work
- **C. Desktop layout** — 1024–1920px, no overlap, no breakage
- **D. Mobile layout** — 320–430px, identity preserved, not collapsed into generic
- **E. Audio engine** — sound plays correctly, controls respond
- **F. Search** — finds what it should, handles what it shouldn't
- **G. Playlists / queue / favourites** — the collection mechanics work end to end
- **H. Install** — the install path works on real devices
- **I. Request-a-topic** — the request path works and is answered
- **J. Share** — sharing works, links land where they promise
- **K. Content / artwork** — every piece of content and art is correct and present
- **L. Welcome journey** — the entrance works first-try for a stranger
- **M. Demo / full editions** — both editions behave as promised
- **N. Purchase journey** — money flows work, receipts exist
- **O. QA inventory** — every visible feature tested, every viewport covered
- **P. Analytics** — the measurement is actually measuring
- **Q. Social / nav hub** — navigation and social surfaces work
- **R. Accessibility + trust** — keyboard, focus, reduced-motion, and the honesty standard (NOT_VERIFIED over fake content)
- **S. Performance** — fast, no layout thrash, weight earned

## The key rule

Pass conditions are **behavioral, not cosmetic**. Section A doesn't ask "does it look good" — it asks "does a first-time visitor know what to press without explanation." That's the difference between a checklist that gates quality and one that gates vibes. Section R's accessibility checks and Section M's edition checks were already flagged for the identity rebuild and the Reveal's 37-slide verification pass.

## What this would change if you ratify it

1. The 19-section checklist becomes the standing acceptance methodology for the Hub's 10/10 pass and future launches — "do not call it complete until the checklist passes."
2. Your closing-standard sentence becomes the build loop's quoted definition of done.
3. It extends the existing contract's acceptance section (§29 of HUB/DESIGN-CONTRACT.md) — the eight-dimension scorecard stays; this is the *launch* methodology that sits under it.

## Source

Distilled 2026-10-06 from your legacy library (`~/workspace/distillations/hmc-batch-1/01-button-spec.md` + `02-hmc-standard.md`; the AAA methodology lives in the HMC Button Spec's second half). Machine twin: `aaa-launch-qa.machine.json`. Builder instructions: `aaa-launch-qa.ai.md`. All three carry the same truth — PROPOSED, awaiting your word.
