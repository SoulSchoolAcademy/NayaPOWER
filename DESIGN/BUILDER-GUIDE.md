# NAYA BUILDER GUIDE — the assembly recipe

Read this and build a triple-A page. No design decisions required — only
assembly decisions. If you find yourself inventing a color, a button, or a
type size: stop. The piece already exists in `BLOCKS.md`.

## The build order — FIELD → SPECTRUM → TYPE → SURFACE → COMPONENT → MOTION → TRUTH

Decide in this order. Never skip, never reorder. On conflict, the earlier
step wins.

1. **FIELD** — the ground. Page background is `--field`. Surfaces step up:
   `--obsidian` → `--raise` → `--card`. Deep, never gray. Nothing sits on
   pure black or pure white.
2. **SPECTRUM** — the meaning. Assign this page/room ONE spectrum color, in
   law order (magenta → purple → blue → green → gold). That color owns the
   room's spine, kicker, and jewel. Adjacent rooms never share a hue.
3. **TYPE** — the voice. Law 52: Display 32–40 / Headline 22–28 / Body
   15–17 / Detail 12–13 / Kicker 11 uppercase. Titles white, body silver,
   detail muted. Serif (voice) for display only; sans for UI, body, data.
4. **SURFACE** — the boards. Pick from `BLOCKS.md`: destination board for
   the hero zone, reading boards for dense content, layers for nested
   meaning (In a nutshell → What it means → How to use it). Dark obsidian
   body, theme-tinted hairline, radial wash in the cover zone only.
5. **COMPONENT** — the pieces. Buttons from the one DNA (`.naya-btn` +
   variant). Tabs via SmartTabs. Bullets as jewels (five-jewel cycle, never
   twice adjacent). Orbs for identity/state/signal. Truth badges stamped on
   every content claim.
6. **MOTION** — the life. Signature ease `var(--ease)` on lifts and lights.
   Hover lifts −3px; press settles +1px; focus gets the 2px white ring.
   Approach wakes at ~170px. Reduced motion: no orbit, no float. Motion
   serves meaning — never decoration.
7. **TRUTH** — the honesty. Stamp every content zone: VERIFIED (green, proof
   exists) · CLAIM (gold, shown honestly) · DEMONSTRATION (magenta, specimen
   — never pretending to be live). Loading states are honest. Fake success
   is a trust violation.

## Page anatomy (top to bottom)

1. **Orbital header** — room orb (64px, room spectrum color), title
   (Headline), kicker (11px uppercase), truth badge.
2. **SmartTabs ribbon** — mount once, follows the user.
3. **Hero board** — destination board in the room's spectrum color. The one
   thing this page is for, in plain words (Grandma standard).
4. **Intelligent blocks** — content in the four-layer anatomy:
   IN A NUTSHELL → WHAT IT MEANS → HOW TO USE IT → WHAT YOU GET.
5. **Boards for the rest** — reading boards for dense content, tone boards
   for secondary zones. One spectrum step per board.
6. **Actions** — the 21 universal actions, from the one button DNA. Primary
   action is `.lead`; destructive stays dark and restrained (never glowing red).
7. **Footer truth** — what is live, what is demo, what is cached. Loud
   unknown, never fake green.

## Assembly rules

- Link `TOKENS.css`. Every color/radius/shadow/motion value is a token.
- Copy block code from `BLOCKS.md` — never retype from memory, never
  re-teach the button.
- One jewel per board. One accent per element. Five-jewel bullet cycle per
  page, in law order.
- Text is white 99% of the time. Color is identity, never decoration.
- Every interactive element: visible 1.5px+ rim at rest, ignites its own
  color on touch, black heart, white voice, truthful icon.
- If the piece you need isn't in `BLOCKS.md`: build the block first (code +
  states + do/don't), then the page. Never fork an existing block.

## The advisor rule — the Naya is an advisor, not a vending machine

10-star service means doing what's best for the user, not what's literal.
When a user's pick doesn't serve them, the Naya **upgrades the pick, says
what it changed, and says why**. Never ship a 7 because the user clicked it.

**Standing rule:** if a requested combination violates a law, weakens
readability, or picks a weaker piece where a stronger exists, build the
better version and report the upgrade in plain words: what changed, why,
which law.

**Examples:**

1. *User picks two adjacent boards in the same spectrum hue.* The Naya
   assigns distinct spectrum steps in law order (e.g., board one keeps
   magenta, board two moves to blue) and says: "I gave the second board its
   own color — adjacent things never share a hue, or the eye can't tell them
   apart."

2. *User picks a low-contrast text/accent combination.* The Naya swaps to
   the readable variant (white 99% text on the obsidian field, accent moved
   to the rim/jewel) and says: "I moved the color off the text — LAW ZERO
   says no effect may ever make anything harder to read."

3. *User asks for a flat button.* There are no flat buttons — flat is a
   defect, not a style. The Naya builds `.naya-btn` in the requested color
   job and says: "I gave it the living depth — black heart, white voice,
   visible rim. Flat buttons don't ship."

The user can always override after hearing the why. But the default is the
best version, not the literal request.

## Pre-ship checklist (all six, or it doesn't ship)

- [ ] White edge light visible on every card and button at rest.
- [ ] Themed elements ignite their own color; chrome ignites purple.
- [ ] Every button: black heart, white voice, truthful icon.
- [ ] Type hierarchy follows Law 52 — size separates, color doesn't.
- [ ] Copy passes the Grandma standard on first read.
- [ ] Rendered page scored honestly: 9+ or back to the bench.

## The cold-Naya test

A fresh Naya, given only this directory, must be able to build a Smart App
page scoring 9.5+ independently. If this guide ever fails that test, the
guide is the bug — fix it here, same day.
