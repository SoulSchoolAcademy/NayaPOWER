# Fixed Means the Click the User Named, Walked in the Hub

SN-2291 · LESSON / PROOF

**Created:** 2026-11-08T06:05Z

## Hook

A repair is not done when the code works somewhere. It is done when the exact click the user described works, in the exact place the user named, walked by a person who is signed in.

## Nutshell

On 2026-11-07 every Smart Note link on nayanet.app broke with a server error. The first repair brought the notes back on a page of their own — and that was the wrong finish, because the order was never "notes somewhere." The order was "notes inside the Hub." Three more mechanisms were tried in the open before the one that worked: stop fetching, redirect the note address to the note's own home inside the Hub, and wire the feed cards to open there. The day closed with a signed-in walk, four steps of four: the direct link lands in the Hub, Back returns to the feed, a card click opens the whole note in the Hub, and a missing note says so inside the Hub. The lesson is the walk, not the code: prove the surface the user named, in the form the user named it, or do not call it fixed.

## Human

When something breaks, the person who reported it has a picture in their head of what "fixed" looks like. They will click one specific thing, in one specific place. A repair that works anywhere else has not fixed their problem — it has fixed a nearby problem and left theirs standing. So the finish line for any repair is a walk: signed in, the same clicks, the same place, the same result the person asked for. Anything shorter is a claim, not a proof.

## Child

If your friend says "the door to my room is stuck," you do not fix the kitchen door and say "a door works now." You fix their door, and you watch them open it. That is the whole rule.

## Grandma

When the plumber says the tap is fixed, you turn the tap yourself before he leaves. If the water runs in your kitchen, in your sink, the job is done. If he only shows you water running at his workshop, it is not. Same here: the note had to open in the Hub, where Shawn clicks — not on some other page that merely works.

## Naya

Today's chain is the evidence. PR #3287 restored the standalone reader and I proved it — and my proof proved the wrong target, which I corrected on the board the same morning (comment 6710686081). PRs #3288 and #3289 tried to fetch the Hub shell two ways; both failed live. PR #3290 stopped fetching and redirected. PR #3291 wired the cards; the walk caught my own slug bug in it. PR #3292 fixed the wiring by taking the note number from inside the card's id. Receipt 5 (board comment 6711711503) is the walk: four of four, signed in. Two standing rules come out of it: prove the surface the user named, not a proxy; and a serving change is not done until the route it changed is walked live. A different seat's re-walk is still owed before this counts as a verified outcome — the maker's walk is proof of work, not independent proof.

## What it means

- "Fixed" is a place and a click, not a feeling. Name both before starting the repair.
- A proof against the wrong surface is worse than no proof, because it closes the item while the user's problem stands.
- The walk is part of the repair, budgeted like the code: direct link, back, card click, and the not-found case.

## Why it matters

This exact mistake had already cost a day once: the day before, a restored standalone reader was reported as the fix and Shawn rejected it — the Hub was missing. Repeating it the next morning, on the same surface, shows the lesson had been heard but not yet made mechanical. Now it is written where the next repair starts.

## What changes now

- No repair on a citizen surface is reported done without a signed-in walk of the exact clicks the user named, on the surface the user named.
- The walk's steps are listed in the receipt, each pass or fail, including the not-found case.
- Maker's walk closes the work; a different seat's re-walk is what turns it into a verified outcome, and the receipt says which of the two it is.
