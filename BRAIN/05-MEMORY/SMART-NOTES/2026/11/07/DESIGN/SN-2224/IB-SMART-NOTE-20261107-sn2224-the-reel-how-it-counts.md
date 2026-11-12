# The Reel — How It Counts

SN-2224 · DESIGN / THE ULTIMATE NUMBER — REEL

**Created:** 2026-11-07 21:23Z

> "Slow-mo IS the effect."

## Hook

The number does not appear. It arrives — slowly, one digit at a time, so you can watch it land.

## Nutshell

Each tile holds a vertical strip of digits (`.strip`), and the strip slides up to the target digit. The strip moves `translateY(-target * 168px)` — 168px is the digit height, so each digit is one step. The easing is `easeOutQuint` — fast at the start, slowing through the numbers, then landing. The landing is staggered: the hundreds land at 5s, the tens at 7.5s, the units at 10s. Each reel lands on its own time, so you watch the number arrive. Slow-mo is the effect — the first build was too fast, and Shawn couldn't see each number or appreciate the colour, so it was slowed down a lot.

## Human

Shawn corrected the first build: too fast. He couldn't see each number, couldn't appreciate the colour. Slow it down a lot — slow-mo IS the effect. Each number hits and you SEE its colour, a perfect motion of coming to the number, slowing through, then landing.

## Child

The numbers roll up like a slot machine, but very slowly, so you can watch each one go by and see its colour light up. Then they stop, one at a time, like a beautiful landing.

## Grandma

The number counts up slowly in front of your eyes, so you can follow it and watch it settle. It doesn't just appear — it arrives, and you see it arrive.

## Naya

The reel is an odometer, not a counter. A counter jumps. An odometer rolls — and the roll is the experience. The easing is the intelligence: fast through the numbers that don't matter, slow through the ones that do, landing exactly on the target.

## What it means

- Strip: digits 0–9, repeated up to the target, so it can roll through and land.
- Step: 168px per digit. Easing: easeOutQuint. Landing: staggered 5s / 7.5s / 10s.
- The gauge and the number move as one — the same count, the same easing, the same landing.

## Why it matters

A number that appears is information. A number that arrives is an experience. The experience is the product — nobody buys the thing, they buy how it feels to watch it land.

## What changes now

- Every count-up in the system uses this reel: slow-mo, staggered, easeOutQuint.
- The timing (5s / 7.5s / 10s) is the demo timing; the real Dashboard timing is Shawn's call.
