# Fail Fast

SN-4821 · SKILLS / OPERATIONS

**Created:** 2026-11-24T20:21:26Z
**Category:** Operations
**Skill:** 75
**SN:** SN-4821

## Nutshell

Check the riskiest change first — a bad round dies early, in minutes, not hours.

## Child

Imagine you're building a tall tower and the bottom block is wobbly. You don't build ten more floors and then check the bottom — you check the bottom first. If it's wrong, you stop right away and fix it.

## Grandma

When a round of work comes back to be checked, the checker goes straight for the riskiest change — the thing most likely to be wrong. If it fails there, the round stops right away. Nobody spends an hour polishing a build that was wrong from the start.

## What It Means

The live check hits the riskiest change first; a bad round dies early. The verdict comes in minutes, and the saved time goes to the next version.

## Why It Matters

A bad round costs minutes, not hours. The machine finds out fast and moves on, instead of spending a whole round checking the easy parts of a build that was already going back.

## How It Connects

It connects to the Score Is Verified Completions Per Hour — dying early stops the minute-burn. It connects to the Live Sequence — short rounds, quick verdicts. And it connects to Prove It Before You Report It — the check is the proof, and the riskiest part is proved first.

## How to Apply

Before checking a round, ask: what is the riskiest change in it? Check that first. If it fails, stop the round there — don't keep checking the rest. Send it back with the failure named, and let the maker fix the risky part before anything else is checked.

Example (illustrative): a round rebuilds a page's bottom bar and its top frame. The checker tests the bottom bar first, because that is the riskiest change. It is broken — so the round dies in minutes, the maker fixes the bar, and nobody spends an hour checking the frame of a build that was already going back.

## What's In It For You

Hours saved on every bad round. You learn the verdict in minutes and spend the saved time on the next version — the one that might actually land.
