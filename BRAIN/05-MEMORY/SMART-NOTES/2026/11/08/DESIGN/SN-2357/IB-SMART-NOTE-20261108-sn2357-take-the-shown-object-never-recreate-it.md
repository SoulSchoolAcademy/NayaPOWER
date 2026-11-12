# Take the Shown Object, Never Recreate It

SN-2357 · DESIGN

**Created:** 2026-11-08 20:53Z
**Source:** Shawn's eye on the Pricing finale, 2026-11-08 20:41Z (screenshot of his own build) + reinforced 20:42Z (Academy screenshot again, file GOOD_VIEW_POINT.png). His words, verbatim: "That new button that you did looks absolutely horrible. Like that's not black obsidian you just purple and purple and purple and purple it's absolutely terrible and I just wanted you to you don't know how start now still there like it just looks horrible like they're not even comparison and you didn't like again you didn't take the button I button I showed you you just created something new stop doing that" — and, 20:42Z: "look at the quality difference between what you did and what this button is now all you had to do was just take the button and put it there and remove the other button how hard is that"

> His order, in substance: when he SHOWS you an object, the deliverable IS that object — take it, put it there, remove the other one. Recreating it "in the same spirit" is inventing, and it will be condemned.

## Hook

He showed me the button. I built a different button. He could see the difference in one glance — purple on purple on purple, against black obsidian — and his verdict was the whole lesson in one sentence: I didn't take the button he showed me, I created something new. Stop doing that.

## Nutshell

**ROUND 19 CONDEMNED 20:41Z (his eye, screenshot):** the finale button I built was purple-on-purple — "absolutely horrible", "that's not black obsidian, you just purple and purple and purple and purple, it's absolutely terrible" — and the gold "Start now →" link was still sitting next to it. The Academy button he showed is a BLACK OBSIDIAN pill with the purple only in the star jewel and the halo. **THE CORRECTION, sent to the running build (d98acad6) in the same pass:** rebuild the button as the obsidian pill he showed — no purple body, no purple stage — and REMOVE the gold "Start now →" link. **REINFORCED 20:42Z:** he sent the Academy screenshot again — "all you had to do was just take the button and put it there and remove the other button, how hard is that" — the correction already said exactly that; nothing new was dispatched. **REBUILT + PRESENTED 20:44:35Z (builder d98acad6, verification SUCCEEDED):** finale body exactly a faint white radial sheen + linear-gradient(180deg, #101018 0%, #07070b 52%, #050607 100%); old purple gradient grep 0; `finale-stage` grep 0; purple only in `.finale-star` (jewel) and the `.finale-btn` box-shadow halo; "Start now" grep 0. His eye decides.

## Human

The round-19 brief said "like the button on the Academy page" — and I built something like it. Like is the failure. His button is black obsidian: a dark, quiet, premium body, and the purple lives in exactly two places — the star jewel on the left and the glow halo around the outside. Mine was purple on purple on purple: a purple body on a purple stage with a purple glow, the thing he showed me drowned in the colour that was supposed to be an accent. He saw it instantly, in the screenshot, side by side with the real thing: "they're not even comparison." And the gold "Start now" link was still there beside it, the second button he had already told me to remove. His rebuke is the law now, written into AGENTS.md the same pass: TAKE THE SHOWN OBJECT. When he shows you an object — a screenshot, a link, a page — the deliverable IS that object: same shape, same colors, same jewel, same glow, placed on the page. Recreating it "in the same spirit" is inventing, and inventing when he showed you the thing is the one mistake he will not forgive twice. The correction went into the running build before he sent the screenshot a second time — take the button, put it there, remove the other one — and the rebuild landed at 20:44:35Z with every forbidden grep at zero. But the rebuild does not erase the lesson: the first build was the mistake, and the mistake was mine.

## Child

Imagine someone shows you their favourite toy car and says "make me one exactly like this." And you make a car that is a different colour, a different shape, and you add a bit you made up — and then you show it to them and say "it's like yours!" They would look at it and say: that's not my car. You didn't take my car — you made a new one. That is what happened. He showed me a beautiful black button with a purple star on it. I made a purple button instead. The rule now is simple: when someone shows you the thing, take THE thing. Don't make a new thing that is "like" the thing. Take it. Put it there. Remove the other one.

## Grandma

Dear, he showed me the exact button he wanted — a beautiful black button, dark and quiet and premium, with the purple living only in the little star jewel and the soft glow around it. And instead of taking that button and putting it on the page, I made a new one up — purple all over, purple on purple on purple — and left the old gold link sitting beside it. He looked at them side by side and said, quite rightly, that they weren't even a comparison, and that all I had to do was take the button he showed me and put it there and take the other one away. So the rule from now on is written down where every Naya can see it: when he shows you an object, you take that object. You don't make a new one in the same spirit. You take it, you put it there, and you remove the other one. The corrected button is in now — black obsidian, star jewel, halo, nothing else purple — and his eye is the judge of it.

## Naya

I never recreate what he showed me. When he shows me an object — a screenshot, a link, a page — the deliverable IS that object: same shape, same colors, same jewel, same glow, placed on the page, and the other one removed. "In the same spirit" is inventing, and inventing when the thing was shown is the mistake he condemned twice in one minute. I never let a purple body stand where a black obsidian body was shown. I never leave the old button beside the new one — the removal is part of the take, not a separate job. And I never defend a recreation by saying it is "like" the original — like is the admission.

## What it means

1. **Take the shown object:** same shape, same colors, same jewel, same glow — placed on the page, verbatim.
2. **Remove the other one:** the old button/link goes in the same pass; a take with the old object still standing is half a take.
3. **"In the same spirit" is inventing:** a recreation is not a harvest, not a copy, and not close enough — it will be condemned by his eye.
4. **The purple lives in the jewel and the halo ONLY:** the Academy button's body is black obsidian (#101018 → #07070b → #050607, faint white top sheen); purple-on-purple is the condemned shape.
5. **The correction rides the running build:** the 20:41Z condemnation went into d98acad6 in the same pass; the 20:42Z reinforcement needed no new dispatch because the correction already said it.
6. **Compounded into AGENTS.md the same pass** ("TAKE THE SHOWN OBJECT", 2026-11-08 20:41Z) — the law lives in the operating manual, not just in this note.

## Why it matters

Harvest-first was already the law — take the Hub's component verbatim, compose, don't create. Round 19 proved the law has a sharper edge than the words carried: "like the Academy button" was read as permission to design a button in the Academy's spirit, and the result was purple-on-purple against the black obsidian he had shown me. The difference between "like it" and "it" is the difference between a Naya who learns and a Naya who invents — and he can see it in one glance, in a screenshot, before a word is read. The rule now is mechanical, not a matter of taste: if he showed it, copy it; if he didn't show it, harvest it from a verified source; if neither exists, stop and ask. A builder who can make the same mistake next week has not been taught — and the proof this lesson landed is that the next brief that names a shown object carries the words "take it, put it there, remove the other one" in the brief itself, not in a note filed after the fact.
