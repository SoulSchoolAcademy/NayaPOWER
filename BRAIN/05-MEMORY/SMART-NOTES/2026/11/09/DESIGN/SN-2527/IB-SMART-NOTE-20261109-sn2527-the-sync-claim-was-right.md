# The Sync Claim Was Right — It Was Edge Lag

SN-2527 · DESIGN / SYNC

**Created:** 2026-11-09 16:25Z

**Source:** Intelligence Loop run 49 live-feed check, 2026-11-09 ~16:25Z, closing run 48's open correction item. No new dictation from Shawn this window — this is the loop's own verification practice, corrected by its own evidence.

## Hook

A sync claim the live bytes contradicted was not wrong — the check was just too early. Give a claim thirty minutes before you call it false.

## Nutshell

- **RUN 48'S CHECK (~15:56Z):** the live feed (`https://nayanet.app/feed-live.json`, HTTP 200, 4,661,866B, `count` 600) showed SN-2512–2518 at 0 — contradicting the sync hook's ~15:48Z claim that SN-2512–2518 were synced and the feed rebuilt to 607 cards. Run 48 held it as OWED, not as a defect: "either edge propagation lag or a redeploy that hasn't landed."
- **THIS RUN'S CHECK (~16:25Z):** the live feed (HTTP 200, 4,761,924B, `count` 615) shows SN-2512–2526 each exactly once. +15 cards = exactly SN-2512–2526. The claim was right.
- **THE LAG:** the notes landed sometime between the 15:56Z check and the 16:25Z check — up to ~30 minutes after the hook's claim. The 16:06Z sync run reported 0 new notes (1,491 unchanged) — the notes were already in Supabase; what lagged was the feed landing, not the sync.
- **CLOSES RUN 48'S OWED ITEM:** SN-2512–2518 in the feed — now CLOSED, proven from the live bytes, not from the hook's claim.
- **UNCHANGED:** sn2505 0 (open PR #3307 only), sn2395 2, sn2050/sn2051 0 (his call), `generated_from` still reads `registry@03e470aa`.

## Human

Last run, the numbers said the sync hook was wrong: it claimed seven notes were live, and the live feed said zero. The loop did the right thing then — it held the item open instead of declaring a failure. This run the same live feed says all fifteen notes are there, each exactly once. The hook was never wrong; the check was just too early. A page served from the edge takes time to catch up — up to half an hour, in this case — and a check taken minutes after the claim will always look like a contradiction. The lesson is about patience in verification: a claim contradicted by live bytes minutes later is "not yet landed", not "false". You re-check after thirty minutes, and only then do you call it a defect.

## Child

Imagine your friend says "I put your toy on the shelf" and you run over and the shelf looks empty — but the toy was still on its way up the stairs. You wait a little, you look again, and there it is. The friend was right; you just looked too soon. That's what happened here: the notes were on their way, and the first look was too early.

## Grandma

Dear, sometimes you check the oven too soon and think the bread hasn't risen, love — but it just needed a little more time. That's what happened with these notes, dear. The first look said they weren't there, but they were simply on their way, and half an hour later there they all were, right where they belonged. Patience, love — look again before you worry.

## Naya

This connects to SN-2419 (The Feed Sync Recovered — The Live Feed Is the Truth) and sharpens it: the live feed is the truth, and timing is part of the truth. A live check is a photograph, not a verdict — it shows the state at one instant, and the state at one instant can lag the claim by up to thirty minutes. The loop's discipline is to hold the contradiction as an open item ("owed, re-check next run") rather than upgrading it into a defect, and the evidence this run vindicates that discipline: the owed item closed itself. The failure mode this guards against is the false alarm — declaring the sync broken, dispatching a repair seat, and spending the team's time on a lag that would have resolved itself. The rule is simple: a claim contradicted by live bytes is "not yet landed" until a re-check thirty minutes later still contradicts it.

## What it means

- **A SYNC CLAIM CONTRADICTED BY LIVE BYTES MINUTES LATER IS "NOT YET LANDED", NOT "FALSE."** Re-check after ~30 minutes before calling it a defect.
- **EDGE LAG IS REAL AND MEASURABLE:** up to ~30 minutes here (claim ~15:48Z, absent at 15:56Z, present at ~16:25Z).
- **THE LIVE FEED IS STILL THE TRUTH** — but a live check is a photograph of one instant, and timing is part of the truth.
- **RUN 48'S OWED ITEM IS CLOSED:** SN-2512–2518 (and SN-2519–2526) are Hub-live, proven from the bytes.

## Why it matters

False alarms cost the team real work: a declared sync failure would dispatch a repair seat, file a defect, and pull the captain's attention — all for a lag that resolves itself. The loop's job is to tell the difference between "broken" and "not yet", and the only way to tell is to wait and look again. This note is the calibration for every future check: thirty minutes of patience before a contradiction becomes a defect.

## What changes now

- The loop re-checks a contradicted sync claim after ~30 minutes before declaring it a defect; "owed, re-check next run" stays the holding state.
- Next loop run re-checks: SN-2527 in the feed on the next sync; the feed count holds at 615 or grows with new filings.
