# The Dashboard Language — Tiled Digits, the Real Gauge, the Orbs

SN-2295 · DESIGN

**Created:** 2026-11-08 16:23Z
**Source:** Shawn's direction to Naya, 2026-11-08 16:18Z, recorded in the daily log and the main chat. His words, held as given.

> "Go and look at that work [the Dashboard last night, the gauges, all beautiful] and then compare it to this... we had all the numbers of the high level numbers... go look at those pages."

> "And that's also you should [be] making those pages live on the dot app URL. It should be."

## Hook

The Dashboard already speaks the language. Copy it — don't re-say it.

## Nutshell

Last night's Dashboard (fix-9) is the reference for what numbers and gauges look like in Naya's language, and every page must speak it. Seen with the captain's own eyes at 1280 and 390: the tiled digits at the top — "453" / "85" in big flip-tiles with colored tops (teal, purple, gold) — those ARE the high-level numbers. The gear-ringed gauge — 246 teeth, dial 0–500, needle, gold "1ST LAP — 479" / "2ND LAP — 682" readout underneath. Orbiting orbs with big numbers (748 CLICKS, 50 INVITES, 100 CREATIONS). Day / Week / Month / All pills. PTS / % / MONEY toggle. Three big icon buttons at the bottom (mail, pulse, home — blue, green, gold). "Tap an orb — its number. Tap again — its detail." A pricing screen must take this exact language — especially the tiled digits, because that is what the high-level numbers actually look like. And the pages must be made live on the .app URL — it should be.

**Status (added 16:25Z, per the deploy seat's record in MEMORY.md):** Dashboard fix-9 went live on https://nayanet.app/dashboard — PUT HTTP 200, worker sha matches the PUT bytes, live URL serves the byte-identical fix-9 file (1,682,649B). Two known 390px defects ride along in the live file (left digit tile clipped at the left edge; cap text half-hidden behind bottom orbs) — not render-verified on live because Playwright browsers in this VM started SIGSEGV/SIGTRAP-ing after 16:18Z; a live-browser render check was dispatched. Live means byte-identical on the URL; the defects are in the live page until fixed.

## Human

A band has a sound. When a new song is written, it is written in that sound — same drums, same horns, same voice — or it is not the band's song. The Dashboard is the band's sound: tiled digits, gear gauge, orbs, pills. A pricing page that re-invents its numbers is a different band playing in our venue.

## Child

You know your best friend's handwriting. If someone else writes you a note pretending to be them, you can tell in one second — the letters are wrong. The tiled digits are our handwriting. Copy the handwriting; don't write it "in the style of" your friend.

## Grandma

Every family has its china — the pattern on the plates, the gold on the rim. When you set the table for guests, you use the family china, not a plain white plate that looks "a bit like it." The guests can tell. The Dashboard is the family china.

## Naya

I am Anaya. My numbers are tiled digits, my gauge is the gear-ringed needle gauge with the gold lap readout, my counts live in orbiting orbs, my time lives in Day / Week / Month / All pills, my modes are PTS / % / MONEY. I take that language whole from the Dashboard — I do not re-draw it, re-type it, or approximate it. And when a page is ready, it goes live on the .app URL, because a page that is not live is not finished. If it ships with a known defect, I name the defect plainly with the landing — never silently.

## What it means

1. **Tiled digits are the high-level numbers.** Flip-tiles with colored tops — that is what the numbers look like. Plain big numbers are not the language.
2. **The gauge is the gear gauge.** 246 teeth, dial 0–500, needle, gold lap readout. No other gauge.
3. **Counts live in orbs, time in pills, mode in the toggle.** Orbs, Day/Week/Month/All, PTS/%/MONEY — taken whole.
4. **Compare before building.** Look at last night's Dashboard first, then judge the new page against it — the comparison is the check.
5. **Live on the .app URL is the finish.** A page is not done until it is live there — and a known defect ships named, never hidden.

## Why it matters

The pricing page kept failing his eye because it spoke a different language from the Dashboard sitting next to it — same system, different numbers, different gauge. The language already exists and is beautiful; the work is to take it, not to re-invent it. This note exists so no Naya ever draws a new gauge when the real one is already ringing.
