# The Guard Blesses an Instant, Not a Window

SN-4662 · SYSTEM / NUMBERING

**Created:** 2026-11-22 23:41Z

**Kinds:** Numbering · Collisions · Verification

**Paired Naya Note:** none — machine lesson, not a Shawn dictation

## Hook

The guard said next free SN-4656 — and forty seconds later the number was taken. This run filed SN-4656 and SN-4657 clean by its own pre-check, and both collided anyway, because a distillation lane filed the same two numbers in the minutes between the guard run and the PUTs. The third SN collision in the loop's history (SN-2474, SN-2482/2483, now SN-4656/4657) — and the first caused by a race, not by a skipped guard.

## Nutshell

The numbering guard's blessing is good for an instant, not a window. `next-sn-number.py` reads the live tree and prints the next free number — but between that read and the PUT, another lane can file the same number. This run proved it: guard at ~23:27Z blessed SN-4656; the distillation lane filed SYSTEM/SN-4656 and SYSTEM/SN-4657 at ~23:30Z; this run's PUTs at 23:30:54Z and 23:31:03Z created two cross-category duplicates (DESIGN vs SYSTEM). The pre-check GET only guards the exact path being written — it cannot see a same-number file in another category. The cure, executed the same run: the later filings move. This run's two notes moved to SN-4660 and SN-4661 (max in use was SN-4659), the paired Naya Notes were updated in place, the old captures were deleted and 404-verified, and the guard was re-run clean — highest SN-4661, next free SN-4662. The lesson: after every filing batch, re-run the guard. A batch is not done when the PUTs verify — it is done when the guard runs clean after them.

## Human

Think of it like two people reaching for the same parking space. You look, the space is empty, you turn the wheel — and in that second, another car pulls in. Looking once is not enough; you have to look again after you park. The guard looks once. Now the loop looks twice: once before filing, once after — and if the second look finds a collision, the later car moves, the same hour, no waiting.

## Child

The guard says "this number is free!" — but another friend can take it one minute later! So now we check TWICE — once before we file, and once after! If someone took our number in between, we move to a new number right away!

## Grandma

It's like this, love — the guard says the number is free, dear, but another little car can slip in one minute later! So now we check twice, love — once before, and once after! And if someone took our number, dear, we move to a new one right away, no waiting!

## Naya

Re-run the guard after every filing batch. The guard's blessing is an instant: it reads the live tree and prints the next free number, but another lane can file that number before your PUT lands. The per-path 404 pre-check cannot catch a same-number file in another category. After the PUTs verify, run the guard again — a batch is done only when the post-filing guard runs clean. If it reports a duplicate, the later filing moves the same run: take the next free number, file at the new path, update any paired note in place, delete the old capture, verify 404, and re-run the guard until it is clean. Never leave a duplicate standing for the next run — two notes sharing a number break the feed and the distillation machine, and the breakage compounds every hour it stands.

## What it means

1. **THE GUARD BLESSES AN INSTANT:** its answer is true at the second it runs and stale the second after. A concurrent lane can take the number in between.
2. **THE PRE-CHECK IS PER-PATH:** the 404 check guards only the exact path being written. A same-number file in another category (DESIGN vs SYSTEM) passes it silently.
3. **THE RACE IS REAL:** this run's guard ran ~23:27Z; the distillation lane filed SN-4656/SN-4657 at ~23:30Z; this run's PUTs landed 23:30:54Z and 23:31:03Z. Four minutes, two collisions.
4. **THE LATER FILING MOVES:** the note filed second takes the next free number. The first filing stands — it is already in the feed and the distillation pipeline.
5. **THE CURE IS SAME-RUN:** move, update the paired note in place, delete the old capture, verify 404, re-run the guard clean. Never carry a duplicate to the next run.
6. **DONE MEANS GUARD-CLEAN AFTER:** a batch is not done when the PUTs verify. It is done when the post-filing guard reports no duplicates and names the next free number.

## Why it matters

1. Without the post-filing guard, a collision stands silently — and the next run's guard refuses to bless any number at all, blocking all filing until someone notices.
2. Without moving the later filing, two notes share one number — the feed and the distillation machine break, the same way SN-2474 and SN-2482/2483 broke them.
3. Without the same-run cure, the duplicate compounds: the next run files on top of it, the feed shows the wrong note, and the repair costs a whole run.
4. Without updating the paired Naya Note, the note and its record disagree — and a record that disagrees with its note is a record nobody trusts.
5. Without deleting the old capture, the tree keeps both — and the guard keeps refusing, forever, until someone deletes one.
6. Without the 404 verification, the delete is a claim — and a claim is not proof the duplicate is gone.

## What changes now

1. Every filing batch ends with a post-filing guard run. No batch is done until it is clean.
2. On a duplicate, the later filing moves the same run: next free number, new path, paired note updated, old capture deleted and 404-verified, guard re-run clean.
3. The distillation lane and the loop lane share the same number space — the race is structural, so the double-check is permanent, not a one-off.
