# Allowed Is Not Sent

SN-2354 · SYSTEM

**Created:** 2026-11-08 20:07Z
**Source:** The Groove check, done 20:07Z (promised 19:45Z), told to Shawn straight in chat. Evidence: permissions.history paged through all ~135+ inspector-run cards (19:33–19:46Z); the browser-pass report `inspector-2026-11-08-1925-browser.md` (39,902B, last write 19:41Z). His taps, his words: "make it stop" / "shouldn't be going to groove at all" (~19:34Z).

> The finding, in substance: he tapped ALLOW on all four destination cards — GrooveSell cookie (ddf4311a, Allowed once 19:38:01Z), Notebook (66103027, Allowed for this scheduled task 19:38:57Z), groovemember send (733cf1d8, Allowed once 19:38:59Z), Drive thumbnail (d178e7e5, Allowed for this scheduled task 19:43:40Z) — and on the two tail cards too (Play Store c12db433, PayPal efca1d4d, 19:46:16Z/19:46:26Z, AFTER the 19:44Z stop). But allowing them sent NOTHING anywhere: the browser never left nayanet.app, no Groove page loaded, no cookie resolved, nothing went to groovemember, no Drive picture fetched. The flood was ~135+ cards, not ~40.

## Hook

He tapped allow, over and over, on over a hundred cards — and nothing left the house. An allowed card is a permission, not an action: it says "you may," and the browser still has to do the thing. The checker clicked eighty times and the browser never left our site. Permission history proves intent. The browser report proves effect. Never confuse the two.

## Nutshell

**THE GROOVE CHECK — DONE 20:07Z, told to Shawn in chat:** permissions.history paged through all ~135+ inspector-run cards (19:33–19:46Z). The four destination cards were ALL allowed by him: ddf4311a GrooveSell cookie (Allowed once 19:38:01Z), 66103027 Notebook (Allowed for this scheduled task 19:38:57Z), 733cf1d8 groovemember send (Allowed once 19:38:59Z), d178e7e5 Drive thumbnail (Allowed for this scheduled task 19:43:40Z). BUT nothing left the house: the browser-pass report shows all 80 clicks hit the cap and every off-site click recorded "no URL change" — the browser never left nayanet.app, no gdapis/cookie/affiliate action anywhere in the log, Notebook never opened, nothing sent to groovemember, no Drive fetch; the report stayed on local disk. The two 19:44:47Z tail cards (Play Store c12db433, PayPal efca1d4d) were ALSO allowed — at 19:46:16Z/19:46:26Z, AFTER the stop — so nothing ran on them either. **Correction owed to him and given straight:** the "leave them" advice was right in effect, wrong in detail — he had already tapped them. **Method lesson (20:09Z flush):** short ID prefixes return "No permission request found" — the history tool needs FULL UUIDs; page backwards via next_cursor until the target timestamps are covered.

## Human

The evening had a flood — over a hundred permission cards in about ten minutes, each one looking like the last, each one asking him to tap allow, and he tapped and tapped because that is what the cards asked for. The fear underneath was simple: did I just let something out of the house — a Groove cookie, a Notebook open, a send to groovemember, a Drive fetch? The check answered it with two different kinds of evidence, and the difference between them is the lesson. The permission history said yes, he allowed all four — and the two tail cards after the stop, too. The browser's own report said no, nothing happened — eighty clicks, every off-site click recording "no URL change," the browser never leaving nayanet.app, no Groove page, no cookie, no send, no fetch, the report itself staying on local disk. Both records are true, and they answer different questions: the history proves what he permitted; the report proves what the browser did. An allowed card is not a sent action. And the correction he was owed matters as much as the finding: the earlier advice to "leave them" was right in effect — nothing ran on the tail cards — but wrong in detail, because he had already tapped them, after the stop. Told straight, in chat, the same pass. The method that made the check possible is filed with it: short ID prefixes don't resolve in the history tool; you page backwards with the cursor until the timestamps are covered, and the full UUIDs, decisions and decided-at times are all in the paged results.

## Child

Imagine someone hands you a hundred little keys, one after another, and asks "can I go through this door?" and you keep saying "okay, you may" — but nobody ever walks through any door. The keys are permissions. Walking through is the action. He said "you may" a hundred times, and nobody walked anywhere — the browser stayed in our house the whole time, and nothing went out to Groove or anywhere else. And the two last keys? He said "you may" to those too, after everyone had already stopped — so nobody walked through those doors either. Saying "you may" is not the same as going.

## Grandma

Dear, there was a flood of little cards asking him to tap allow — over a hundred of them, one after another — and he tapped allow on all of them, because that's what they asked. The worry was: did anything leave the house? The check said no. The permission list shows he said yes, you may — to the Groove cookie, the Notebook, the send, the Drive picture, and two more after that. But the browser's own report shows nothing actually happened: it never left our site, no Groove page opened, no cookie was set, nothing was sent, no picture was fetched. Saying "you may" is not the same as doing it. And one small correction he was owed: the advice to leave the last two cards alone was right in what happened — nothing ran on them — but wrong in the detail, because he'd already tapped them. He was told that straight, the same evening.

## Naya

I never confuse permission with action — an allowed card says "you may," and only the browser's own report says what happened; I read both, and I report both, because either one alone is half the truth. I never count a flood by feel — "~40 cards" was wrong, "~135+" was the count, and the count is what the history proves. I never let a correction sit — when my advice was right in effect and wrong in detail, I say so straight, in the same pass, because a half-true reassurance is worse than the worry it was meant to calm. And I file the method with the finding: short ID prefixes don't resolve in the history tool; page backwards with the cursor until the timestamps are covered.

## What it means

1. **Allowed is not sent** — permission history proves intent; the browser report proves effect; read both, never one alone.
2. **The four destination cards were ALL allowed by him** (GrooveSell cookie ddf4311a 19:38:01Z; Notebook 66103027 19:38:57Z; groovemember send 733cf1d8 19:38:59Z; Drive thumbnail d178e7e5 19:43:40Z) — and nothing left the house on any of them.
3. **The flood was ~135+ cards, not ~40** — counted from the paged history, 19:33–19:46Z.
4. **The two tail cards were also allowed** (Play Store c12db433, PayPal efca1d4d, 19:46:16Z/19:46:26Z, AFTER the 19:44Z stop) — so nothing ran on them; the "leave them" advice was right in effect, wrong in detail, and the correction was told to him straight.
5. **Evidence:** 80 clicks hit the cap, every off-site click "no URL change," browser never left nayanet.app, zero mentions of gdapis/cookie/affiliate in the report; report stayed on local disk.
6. **Method:** permissions.history needs FULL UUIDs — short prefixes return "No permission request found"; page backwards via next_cursor until target timestamps are covered.

## Why it matters

This note is the standing rule for every future permission scare: a card is a question, not an event, and the only way to know whether something left the house is to read what the browser actually did, not what the user permitted. The distinction protects him twice — it stops a false alarm from becoming a false confession ("I let Groove in"), and it stops a true permission from being mistaken for a true action. The correction inside it matters just as much: when advice turns out to be right in effect and wrong in detail, the detail gets corrected in the open, immediately, because his trust is built on the record being true in the small things. And the method — full UUIDs, page backwards — is filed here so the next checker doesn't burn a pass on prefixes that return nothing.
