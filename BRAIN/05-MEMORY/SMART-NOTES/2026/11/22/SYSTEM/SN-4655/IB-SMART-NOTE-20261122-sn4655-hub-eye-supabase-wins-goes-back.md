# Hub Eye — Supabase-Wins Goes Back

SN-4655 · SYSTEM / HUB EYE — SUPABASE-WINS GOES BACK

**Created:** 2026-11-22 23:17Z

**Kinds:** System · Verification · Hub

## Hook

The staged Hub fix passed its checker and the captain's eye — then the real-browser eye walked it and it goes back. Supabase wins on a full page load and loses everywhere else: the baked cards vanish, the back button reverts to baked-only, and one short ID silently opens the wrong note.

## Nutshell

Supabase-wins is half proven: on a full page load the live feed wins and the live cards render whole — but the baked cards do NOT survive the poll. After the poll the feed is live-only (sn4611, sn4467, sn3701…); sn4650 and sn4649 vanish from every batch. Returning via the in-app "Back to Hub feed" reverts to baked-only for 50s or more — Supabase-wins holds only on full page load, not on hash navigation. And sn4610 collides: the short ID resolves to the Baked-In / lock-in note (20261121-sn4610) instead of the Library note (20261122-sn4610), so users silently get the wrong note. The feed's Library card is sn4611 and opens correctly; sn4467 routes correctly, not to SN-4588; there is no crash. The failure copy still misleads — "That note isn't here / It may have been retired" — with a dead "Try again" button. Fix round 2 is dispatched (lane hub-supabase-wins-20261122/). No true 390px was claimed — the cloud route ran 1919 then 573px.

## Human

Think of it like two piles of cards — the fresh live ones and the older baked ones. When the page loads fresh, the live pile wins and everything shows. But the moment the page polls for new cards, the baked pile disappears — two cards just vanish. And if you go back to the feed using the button inside the app instead of reloading the page, you're back to the old pile for almost a minute. On top of that, one card's short name points at the wrong card entirely — you tap it expecting one note and get a different one, with nothing telling you. The fix round is already running; the eye caught it before his eye had to.

## Child

The live cards win when the page loads fresh — but then the older cards disappear! Two cards vanish! And the back button shows you the old cards for almost a minute! One card's short name opens the WRONG note! The fix round is already running!

## Grandma

It's like this, love — when the page loads fresh, the new cards win and everything shows, dear! But then the older cards disappear — two of them just vanish, love! And the back button inside the app shows you the old cards for almost a minute! And one card's short name opens the wrong note entirely, dear, with nothing telling you! The fix round is already running, love — the eye caught it before his eye had to!

## Naya

Prove Supabase-wins on every navigation, not just on full page load: full load, hash navigation, in-app back, and the poll after load — the baked cards must survive all four, or the win is not a win. Short IDs must resolve to exactly one note: sn4610 colliding between the Baked-In note and the Library note is a silent wrong-note defect, and the feed's Library card being sn4611 does not excuse it. Failure copy must tell the truth and its button must work: "That note isn't here / It may have been retired" with a dead "Try again" misleads twice over. A fix round is not done on a staged pass — it is done when the real-browser eye walks the whole flow and the baked cards survive it. Never claim a viewport you did not run: no true 390px was claimed here, and the route (1919 then 573px) is stated, not smoothed over.

## What it means

1. **SUPABASE-WINS IS HALF PROVEN:** full page load wins; the poll after load loses the baked cards. A win on one navigation is not a win.
2. **BAKED CARDS MUST SURVIVE:** sn4650 and sn4649 vanishing from every batch after the poll is the defect — live-only is not the feed, it is half the feed.
3. **HASH NAVIGATION IS A NAVIGATION:** in-app "Back to Hub feed" reverting to baked-only for 50s+ means the win does not hold where citizens actually go back.
4. **A SHORT ID MUST MEAN ONE NOTE:** sn4610 resolving to the wrong note, silently, is the same class of defect as the SN-4590 duplicate — one name, one thing, or the feed lies.
5. **FAILURE COPY MUST NOT MISLEAD:** "It may have been retired" for a note that is right there, plus a dead retry button, tells the citizen the system lost something it has.
6. **THE EYE WALKS THE WHOLE FLOW:** the staged pass and the captain's eye did not catch this; the real-browser eye walking load, poll, back, and open did. The walk is the proof.

## Why it matters

1. Without the baked cards surviving, every poll quietly deletes notes from the feed — and the citizen never sees an error, only an absence.
2. Without hash navigation holding, the most common way back to the feed shows stale cards for a minute — and stale is what he notices first.
3. Without one-note-per-ID, a tap opens the wrong wisdom with no warning — and the citizen trusts the wrong note.
4. Without honest failure copy, a live note looks retired — and a dead retry button teaches the citizen that trying again does nothing.
5. Without the whole-flow eye, a staged pass ships a half win — and his eye finds the missing half.
6. Without stating the viewport honestly, a 573px walk gets reported as a phone walk — and the phone is never actually checked.

## What changes now

1. Fix round 2 (hub-supabase-wins-20261122/) makes baked cards survive the poll, the back button, and the hash navigation — all four, or it goes back again.
2. sn4610's collision is cured so the short ID resolves to exactly one note.
3. The failure copy tells the truth and "Try again" works — or the copy goes.
4. Every Hub fix round is eye-walked on the whole flow — load, poll, back, open — in a real browser, before it is called done.
5. Viewports are stated as run — 1919 then 573px here — never claimed as a phone width that was never walked.
