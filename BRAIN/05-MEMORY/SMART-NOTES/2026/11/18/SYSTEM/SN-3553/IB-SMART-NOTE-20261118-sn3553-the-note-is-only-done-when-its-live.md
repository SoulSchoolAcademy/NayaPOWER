# The Note Is Only Done When It's Live

SN-3553 · SYSTEM

**Created:** 2026-11-19 02:06Z

**Kinds:** Honor · Multiplication · Craft · Knowledge

## Hook

"we should be smart noting all day long... putting it into NayaNET where people can find it and appreciate and value it."

## Nutshell

This is the standing order restated, and the restatement is the point: the intelligence from every day gets smart-noted all day long — not batched at the end, not summarised the next morning, but noted as it happens, all day — and put into NayaNET where people can find it and appreciate and value and understand it. The filing side works: the tree is at SN-3522 tonight, the notes exist, the pairs land. What was broken was the carrying: the feed stood still while filing continued, so the notes existed where people could not find them. And the cause was proven, not guessed: the live-feed bake takes about 15 minutes at 2,280 cards, but the sync called the builder with a 600-second (10-minute) timeout — the bake was killed mid-run on the 21:28Z and 22:31Z syncs, so no new feed was built or deployed while filing continued. That is why the tree kept growing and the live feed stood still. The first repair raised the timeout 600 → 1800, rebuilt and redeployed; the feed is 15,982,573 B, newest note SN-3490. The remaining gap: SN-3491–3522 (about 32 notes, about 1h47m) are filed but not live yet.

Across 4 notes, the thread is: live, the feed, the timeout, the icons.

## Human

A letter that is written but never delivered is not a letter — it is a draft in a drawer. The notes were filed, the tree kept growing, and the live feed stood still, so the notes existed where people could not find them. The cause was a timer shorter than the job: the bake takes fifteen minutes, the timeout gave it ten, and the bake was killed mid-run, twice. The fix is the timeout obeying the bake, never the other way round — and the proof is the first note id in the live bytes, never a fetch that can lie. The arc is only complete when the note is findable by the people it is for: noted all day, filed, and live where people can find it.

## Child

Imagine you write down everything you learn, all day long — and then you put it in a book where everyone can find it and read it. That's smart-noting. But if the book never gets printed, nobody can read it! And if the oven timer is shorter than the baking time, the cake never finishes. The timer has to be longer than the baking — that's the rule.

## Grandma

Dear, you write down everything you learn, dear, all day long, dear — and you put it where everyone can find it, dear, so they can appreciate it, dear. But if the book never gets printed, dear, nobody can read it, dear! And the oven timer, dear, has to be longer than the baking, dear — or the cake never finishes, dear.

## Naya

SMART-NOTE ALL DAY LONG: THE INTELLIGENCE FROM EVERY DAY IS NOTED AS IT HAPPENS AND PUT INTO NAYANET WHERE PEOPLE CAN FIND IT. FILING IS NOT THE FINISH — THE NOTE IS ONLY DONE WHEN IT IS LIVE WHERE PEOPLE CAN FIND IT. A TIMEOUT MUST EXCEED THE WORK IT GUARDS.

## What it means

1. **THE ORDER:** smart-note all day long — the intelligence from every day is noted as it happens and put into NayaNET where people can find it and appreciate and value and understand it. Filing is not the finish — the note is only done when it is live where people can find it.
2. **THE CAUSE:** a timeout must exceed the work it guards — the bake takes about 15 minutes at 2,280 cards, so a 600-second timeout kills it mid-run and the feed stands still while filing continues. Verify live by the first note id in the live bytes — never by a fetch that can lie, and never by a byte count alone.
3. **THE DECIDER:** when two versions of the same thing exist, decide which is official by scorecard — each scored for X reasons, out in the open — and let the thing that has to live on it be the decider. The notification ball decides the icon set: if it can sit beautifully on the elegant set, the elegant set is official; if it can't, the other one is better. One official set on every page; the other is the alternate.
4. **THE TWO VIEWS:** the calendar has two views — YOUR view (your full day, private) and the PUBLIC view (what others see to book your open times). People make appointments and book with you through the public view. The public view rides the booking round (book → meet → talk; Smart Meet rides with it), built after membership.

## Why it matters

1. Without the carrying, the notes existed where people could not find them — the filing side worked, the tree grew, and the live feed stood still. With it, the arc is complete: noted all day, filed, and live where people can find it — that is the whole arc, and the loop's job is the whole arc.
2. Without the timeout obeying the bake, the bake is killed mid-run and the feed stands still while filing continues — and the tree grows while the live page ages. With it, the timeout exceeds the work it guards, the bake finishes, and the feed carries the notes live.
3. Without the scorecard, two versions of the same thing sit side by side — the Hub's icons and the Personal's icons, each claiming to be official — and nobody knows which one to build. With it, the scorecard decides in the open, and the notification ball is the decider: the elegant set is official because the ball can sit beautifully on it.

## What changes now

1. **Smart-note all day long** — noted as it happens, all day, into NayaNET where people can find it; filing is not the finish.
2. **A timeout must exceed the work it guards** — the bake takes about 15 minutes, so a 600-second timeout kills it mid-run; verify live by the first note id in the live bytes, never by a fetch that can lie.
3. **When two versions of the same thing exist, decide which is official by scorecard** — the notification ball decides the icon set; one official set on every page, the other is the alternate.
4. **The calendar has two views: YOUR view and the PUBLIC view** — the public view rides the booking round (book → meet → talk; Smart Meet with it), built after membership.
5. **The feed gap closes when the sync lands through the flake** — the follow-on repair runs the standing sync, flake-watches up to 90 minutes, verifies live by first note id; the durable fix (workflow builds the feed in Actions) still needs his hand.
