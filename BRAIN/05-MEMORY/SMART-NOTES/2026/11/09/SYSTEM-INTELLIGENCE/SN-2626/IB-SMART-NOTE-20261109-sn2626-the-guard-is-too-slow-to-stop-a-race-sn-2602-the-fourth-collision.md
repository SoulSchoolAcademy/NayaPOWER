# SN-2626 — The Guard Is Too Slow to Stop a Race: SN-2602, the Fourth Collision

## Hook
Two notes filed under SN-2602 five seconds apart — both seats did the right thing, and the number still collided.

## Nutshell
At 23:26:15Z on 2026-11-09 the distillation machine filed SN-2602 "The Right" (PRICING — distilled 10 notes to one, commit 30fecd87). At 23:26:20Z the noting seat filed SN-2602 "Push-button simple — worlds, not websites" (SYSTEM-INTELLIGENCE, commit 630a501e). Two different notes, two different folders, one number, five seconds apart. Per the Numbering Law, first-filed keeps the number: the machine's "The Right" (23:26:15Z) keeps SN-2602; the noting seat's "Push-button simple" re-filed under a fresh number — and it did: SN-2622 "Push-Button Simple: Worlds, Not Websites" (commit 179cd3be, 2026-11-10 00:14:37Z), live in the Hub feed from the 00:17Z sync (share asset nayanet.live/s/sn2622). The duplicate was deleted (commit 98e2eae2, 23:31:37Z) and its deletion is confirmed in the sync's 404 list. The cause is not carelessness: the guard (next-sn-number.py) takes ~16 minutes to read the live tree, so it cannot see a filing that lands while it is still reading. The run-60 guard fix — descend into each SN directory, every SN-named file its own claim — closed the stale-number gap (two files, one directory, invisible). The same-minute race is the gap that remains: two seats, each with a fresh guard result, filing in the same minute. The enforcement that closes it is the file-time check: if the number is taken when you file, stop, re-run the guard, take the next free one.

## Human
The machine's note, "The Right", distills ten notes into one — the orbs-as-bullets order, the digit colors, the closing question, the honest math — the thread of the letter's rebuild. The noting seat's note, "Push-button simple", is his vision in his words: "We're going to make building and using the internet literally push button simple. And awesome." — an app is way more powerful than a website, "something that does something rather than sit there like a billboard", worlds built in minutes not months, land and a ready-built house and a vehicle for peanuts, and half a peanut back for telling your friends. Both notes are real. Both deserve their numbers. Only one can be 2602. The noting seat's guard and the machine's filing crossed in the same minute — neither seat was wrong, the window was.

## Child
Imagine two kids both ask the teacher, "Can I be number 12?" — and the teacher is still counting the class, so she says yes to both. Then there are two number 12s. Nobody cheated. The teacher just needs to check the list right before she writes the name down, not ten minutes before.

## Grandma
Dear, two good notes both got the same number, love — five seconds apart, neither one at fault. The slow checker couldn't see the other one coming, dear. So the rule now is: check again at the very moment you file, love — not just when you start.

## Naya
I am Anaya. Four collisions in one night, and each one taught the same lesson a little sharper: the number is the identity, and the identity must be checked at the moment it is given, not minutes before. The guard is my memory of the tree — and a memory that is sixteen minutes old is not the tree. I check again before I write. That is the whole fix.

## What it means
- **FIRST-FILED KEEPS THE NUMBER:** the machine's "The Right" (23:26:15Z) is SN-2602. The noting seat's "Push-button simple" moved — and landed as SN-2622 (commit 179cd3be), live in the feed.
- **A SLOW GUARD IS A STALE GUARD:** ~16 minutes of tree-reading means a same-minute race is invisible to it. The guard prevents stale-number collisions, not races.
- **THE FILE-TIME CHECK IS THE ENFORCEMENT:** before the PUT, verify the number is still free; if it is taken, stop, re-run the guard, take the next free one. A 422 on an existing path is the machine telling you the race happened — listen to it.
- **FOUR COLLISIONS IN ONE NIGHT (SN-2278, SN-2474, SN-2482/2483, SN-2592, SN-2596, SN-2600, SN-2602):** the pattern is not a seat failing — it is a system that files fast and checks slow. The fix is mechanical, in the filing step, not in asking seats to be more careful.

## Why it matters
A collision breaks the feed and the distillation machine — two notes, one number, and every downstream count, link, and essence entry points at the wrong one. Each collision costs a delete, a re-file, a re-bake, and a run's worth of untangling. The fourth collision in one night says the enforcement is still not in the machine where the filing happens. Until the file step checks, the next fast night collides again.

## What changes now
- The re-file LANDED as SN-2622 (commit 179cd3be, 00:14:37Z) and is live in the Hub feed (00:17Z sync; share asset nayanet.live/s/sn2622). The owed item is CLOSED — verified from the bytes this run.
- This run's own filings check the live tree immediately before the PUT (not only the guard result) and re-guard on any conflict — the lesson applied in the same pass that records it.
- The loop records the collision class in the PI board note: guard-slow race, distinct from the run-60 stale-directory gap (already fixed).
- The "Push-button simple" note enters the essence under SN-2622, not SN-2602 — its coverage entry is SN-2622.
