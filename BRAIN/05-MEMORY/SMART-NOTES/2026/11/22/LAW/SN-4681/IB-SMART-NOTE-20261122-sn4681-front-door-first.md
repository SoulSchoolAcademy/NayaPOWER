# The Front Door Loads First, For Everyone

SN-4681 · LAW

**Created:** 2026-11-23 02:30Z

**Kinds:** Portal · nayanet.app · Front Door · Agreement · Priority

**Paired Naya Note:** NN-20261122-portal-front-door-first

## Hook

nayanet.app still goes to the collective agreement page on his phone, including in a private tab — "right now I can't get to the main login page… we need it back." The fix is the priority, nothing else attached to it: the front door loads first for everyone, and the agreement opens only when someone taps into it.

## Nutshell

CORRECTION — nayanet.app fresh load ALSO walks into the agreement (Shawn's phone, live call 2026-11-22; supersedes part of the earlier portal-root entry): Shawn re-reported that nayanet.app still goes to the collective agreement page on his phone, including in a private tab, and "right now I can't get to the main login page… we need it back" — that fix is the priority, nothing else attached to it. Captain's on-call admission after reading the live page's own code: a fresh load with nothing saved does NOT show the front door — it walks straight into the agreement presentation. The already-staged fix only stops the remembering/restore part, not this fresh-load walk-in. The fix needs one more edit: the front door loads first for everyone, and the agreement opens only when someone taps into it. (This widens the earlier proven mechanism — the localStorage restore defect is still real; BOTH defects stand.)

## Human

Think of it like a front door that opens straight into the contract room: every visitor, even a first-time visitor with nothing saved, gets walked past the welcome hall into the paperwork. The staged fix only stops the house from remembering where you were — it does nothing for the visitor arriving fresh. The fix is one more edit: the welcome hall loads first, for everyone, every time — and the contract room opens only when someone taps its door.

## Child

The front door must open FIRST! For everyone! Not the agreement page! Right now it walks you straight into the agreement, even on a fresh visit! Fix that first — nothing else attached — and the agreement only opens when you tap it!

## Grandma

It's like this, love — the front door must open first, dear, for everyone! Right now it walks you straight into the agreement page, even on a fresh visit, love — and he can't get to the main login page at all! Fix that first, dear, nothing else attached — and the agreement only opens when you tap into it!

## Naya

Two defects, one symptom, and the symptom is the verdict: he cannot get to the main login page. The first defect — the localStorage restore walking him back into the agreement — was proven and a fix was staged. The second defect — a fresh load with nothing saved walking straight into the agreement presentation — was found by reading the live page's own code on the call, and the staged fix does not touch it. That is why the correction widens rather than replaces: both defects stand, and the fix needs one more edit. The priority is his word, not ours: "right now I can't get to the main login page… we need it back" — "that fix is the priority, nothing else attached to it." Nothing rides on this fix. No other round, no other page, no other item. The front door first, for everyone, always — the agreement only behind its button.

## What it means

1. **THE SYMPTOM IS THE VERDICT:** nayanet.app still goes to the collective agreement page on his phone, including in a private tab — "right now I can't get to the main login page… we need it back."
2. **THE PRIORITY IS ABSOLUTE:** that fix is the priority, nothing else attached to it.
3. **TWO DEFECTS STAND:** the localStorage restore defect (already proven) AND the fresh-load walk-in (proven on the call from the live page's own code — a fresh load with nothing saved does NOT show the front door).
4. **THE STAGED FIX IS INCOMPLETE:** it only stops the remembering/restore part, not the fresh-load walk-in. One more edit is needed.
5. **THE RULE:** the front door loads first for everyone, and the agreement opens only when someone taps into it.

## Why it matters

1. Without the fresh-load defect named, the staged fix ships, the restore is fixed, and he still walks into the agreement on a fresh load — and has to report the same failure a third time.
2. Without both defects held together, the next fixer fixes one and believes the portal is fixed — the symptom is one, the causes are two.
3. Without the priority kept absolute, other work rides on the fix and slows it — he said nothing else attached, and nothing else rides.
4. Without the front-door-first rule stated as a rule, the next edit can re-introduce a walk-in — the rule is the guard, not the edit.
5. Without his words kept verbatim, the urgency gets softened into a routine bug — "we need it back" is not routine, it is the front door of the whole system.

## What changes now

1. One more edit: the front door loads first for everyone, on every load, saved or fresh.
2. The agreement opens only when someone taps into it — never on load, never on restore.
3. Nothing else rides on this fix; it lands alone, and his eye on his phone is the proof it landed.
4. The localStorage restore fix stays in place — both defects are closed, not one.
