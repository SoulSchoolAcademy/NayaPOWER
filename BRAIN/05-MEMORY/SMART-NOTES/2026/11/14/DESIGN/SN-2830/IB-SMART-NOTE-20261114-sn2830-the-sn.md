# The Sn-

SN-2830 · DESIGN

**Created:** 2026-11-14 22:12Z

**Kinds:** Honor · Multiplication · Craft · Knowledge

> "The Hub uploads again with the file-storage link intact, and the live Hub serves the new notes. But the fix found something larger than the 400: the live Hub reads the live feed, not the baked page — and the feed was a full day stale. Even a perfect upload could never have shown a new note, because the page was reading from a feed whose newest card was from yesterday. 131 notes were missing — not just tonight's four."

## Hook

The 400 was the locked door. Behind it was the real fault: the live page never read the baked page at all — it read a feed that was a day stale, so 131 notes were invisible no matter how good the upload was.

## Nutshell

**THE FAULT (sync 22:01Z + 22:31Z, third occurrence same fault):** Cloudflare HTTP 400, error 10305 "Cannot use an assets binding without assets" — the 21:47Z bindings fix declared an ASSETS binding on a script-only PUT with no assets uploaded. Live worker untouched (clean rejection), Hub stale, will NOT self-heal. **THE FIX (DONE 22:45Z):** a new 3-phase Direct Upload deployer (`factory-pipeline/deploy_hub_assets.py`: upload session → asset upload → script PUT with ASSETS binding + config); `deploy.py` branches on hub; `sync-smart-notes.py` patched so every future sync uses it. Dry-run proven on a scratch worker (`hub-dryrun-20261108`, deleted). **THE DEEPER FIND (bigger than the 400):** the live Hub reads `feed-live.json`, NOT the baked page — the deployed feed's newest card was SN-2248 (Nov 7), a full day stale, so even a perfect bake could never show a new note. New `build_feed_live.py` added all 131 missing cards (SN-2249–SN-2379) in the feed's own shape; feed 336 → 467. **CONVERGENCE NOW REAL (Resolve's option b):** one upload carries repo code + config + fresh data. **WRANGLER NOT USED:** no API token available to the seat (env has none, no wrangler config) and the raw token must never be extracted from the connector; the API route uses the registered connection throughout. **SEAT SCORE:** 8/10. **TOLD TO SHAWN** in chat the same pass. **STILL OPEN:** (1) wrangler as the canonical path — token plumbing to the runner, a later decision; (2) the registry itself stale since Nov 7 — a separate job; (3) the next cron sync redeploy through the fixed path is unproven until it fires. **RELATED:** SN-2377 (my patch broke it); SN-2374 (carry the binding); SN-2375 (the re-bake fault); SN-2366 (answer her, don't escalate — the bindings origin); SN-2346 (permission is revocable — the token rule the wrangler decision must respect).

Across 10 notes, the thread is: sn-, never, related.

## Human

The Hub is fixed, and it is bigger than the four notes. The upload works again — the file-storage link is intact, the ASSETS binding is on the live worker, the same upload run twice with no refusal. But when the seat dug in, it found something larger than the refusal: the live Hub was reading from a feed whose newest card was from yesterday. A perfect upload could never have shown a new note, because the page never read the baked page at all. One hundred and thirty-one notes were missing — not just tonight's four. The fix brought all of them back: the pitch, the letter, the entrance removal, the one-shot charge, all of them, on the live Hub now. Three things are still open, and they are named, not hidden: the wrangler route as the canonical path needs token plumbing, a later decision — and the token is never to be extracted from the connector; the registry is stale since November 7, a separate job; and the next automatic sync has not run through the fixed path yet, so the first automatic run is still ahead. The fix itself is proven live. The automatic proof is owed.

## Child

Imagine you were told to take down the old "hello" sign — and you took down the WHOLE sign, every nail, every screw, every bit of paint, and the wall underneath is perfect! That's what happened: the old welcome banner is completely gone — all 33 special pieces, the buttons, the moving parts, everything — and the page still works beautifully. The letter is still there, word for word, and now the page goes: letter, then the prices. Three little things are left: nobody has pressed the letter's button in real life yet, the page's name at the top still says the old hello, and one other version of the page hasn't been checked yet!

## Grandma

Dear, it's a story about a fix that was bigger than the fault, dear. The Hub wouldn't upload — the door was locked — and when the seat fixed the lock, dear, they found the real problem behind it: the page was reading yesterday's paper, not today's. A whole day of notes was missing, dear — one hundred and thirty-one of them — and no perfect upload could ever have shown them, because the page never looked at the upload at all. So the fix brought the paper up to date too, dear, and now all tonight's notes are on the live Hub, every one of them. Three things are still owed, dear, and they're named, not hidden: the other way in needs its key sorted, the list is out of date, and the next automatic run hasn't happened yet to prove the new door works on its own. Told to Shawn the same pass, dear.

## Naya

I never welcome twice — the letter already is the welcome (her portrait, the welcome, the button), so a second welcome strip is a repeat, and repeats go. I never keep the old door beside the new one — one start door, at the end of the letter, right where the reader asks for it. I never let a slim version of the same thing survive — a slim welcome is still the same welcome twice. I remove altogether, and the page flows letter, then chart.

## What it means

1. **The deeper find:** the live Hub reads `feed-live.json`, NOT the baked page — the deployed feed was a day stale (newest SN-2248, Nov 7); `build_feed_live.py` added all 131 missing cards (SN-2249–SN-2379); feed 336 → 467.
2. **The proof:** live bindings show ASSETS; live feed 467 cards with SN-2371–SN-2374; root 200; /s/sn0131 + /smart-notes/sn0131 302; /sw.js 200; repeat deploy no 400 (0 buckets, same etag). Seat score 8/10.
3. **The one item owed:** the button landing centered after the final beat — code-proven by two seats (inspection b094ab25), never run-proven by a live tap-through; 0 probe acts captured; recommended probe at 1440×900 and 390×844, 6 taps + whole-letter read, scrollY + rects recorded.
4. **Still open:** wrangler as the canonical path (token plumbing, later decision — raw token never extracted from the connector); registry stale since Nov 7 (separate job); next cron sync redeploy through the fixed path unproven until it fires.
5. **Still owed:** live tap-through of the letter's button (code-proven only, 0 acts ever — carried from v41); `<title>` still "Welcome to Naya World — NayaNET" (his eye's call: keep or retitle); .space-build-cvm variant unscanned.
6. **One shot, not ten.** Prepare until the shot cannot miss, then take it — a stranger opens the page, laughs in 2 seconds, knows in seconds this is real, what it is, how it works, why it is awesome, why they will love her; she is full-featured; share awesomeness and get paid; the button is right there — no risk, free, jump in the Bugatti — and they tap it. A stranger becomes a citizen.

## Why it matters

1. "Remove it altogether" is a call that is easy to give and easy to half-do — a slimmed banner, a hidden banner, a banner left in the code for later. This seat did the altogether version: every selector, every keyframe, every listener, gone, and the page proved it by flowing cleanly without them. That is what makes the removal real instead of cosmetic — the page cannot grow the entrance back by accident, because there is nothing left to grow from. And the three owed items are the proof standard doing its job on a job well done: the tap-through that has never happened, the title that still says the old hello, the variant nobody scanned. A 9/10 that names its own gaps is worth more than a 10/10 that hides them.
2. The difference between a pitch and a letter is the difference between being told and being welcomed. A statement on a page asks for attention; a letter from the founder gives it — sealed, signed, framed like a plaque, funny, warm, real — and it earns the reading line by line instead of demanding it all at once. And the ending is the whole point: a letter that ends with the button is a door, not a speech — the reader never has to go looking for what to do next, because the doing is right there, where the feeling is warmest. That is what "show, don't tell" means in practice: the form does the persuading, the words do the welcoming, and the button does the inviting. Get any one of the three wrong — the wrong form, the wrong order, the button anywhere but the end — and the beautiful words wreck themselves. Get them right, and the introduction is the experience.
3. A fix that breaks the deploy is not a failed fix — it is a fix whose risk was named, whose failure was clean, and whose repair was already scoped. That is the difference between a fault and a disaster: the live worker was untouched because the rejection was clean, the Hub's staleness is bounded because the next sync re-proves it, and the repair path was written before the fault happened because SN-2374 said the words out loud. The lesson is the order of operations: a binding is a promise of assets, and a PUT that promises without delivering is refused — so the deploy must either upload the assets or invoke the tool that does. And the rule that rides with it — never drop the binding to clear the error — is the one that keeps a quick clear from becoming a quiet return to the original fault.
4. A system that injects user content into its own code must treat every byte as hostile until it is escaped — not the fields someone remembered, all of them. The three tags were not an attack; they were a sentence about a truncated override, written in good faith, and the bake broke on good faith because it trusted the bodies. The fix is total because it has to be: one unescaped field is the same failure, next time from a different note. And the overwrite-before-check is the fault that would have hurt worst — a broken canonical on disk, invisible while the live page looked fine — which is why the order of the steps is itself the lesson: check, then write, never the other way round.

## What changes now

1. Count verified valuable actions daily — each one named, each one linked to its proof — in the Daily Intelligence Report. That count is the headline of the day.
2. Every future dispatch goes through the pipeline — brief, build, verify, file, report — in order, each stage proven before the next. Doing everything at once is how the year was lost.
3. The board stays true: every lane shows a seat or its queue place, updated the moment a lane starts, finishes, or stalls — and a sitting lane gets a seat the same pass it is found.
4. The captain scores herself honestly every day in the daily log: what sat, for how long, and who caught it — me, the pulse, or Shawn. If Shawn caught it, the score is not a 10.
5. Every brief names the unit it must produce and carries the gates, the Bullseye, the Brand, and the North Star, so every seat knows the standard before they start.
