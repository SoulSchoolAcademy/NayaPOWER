# Check the Descendants Before You Close

SN-2944 · LESSON

**Created:** 2026-11-16 13:25Z

**Paired Naya Note:** NN-20261116-check-the-descendants-before-you-close

## Hook

Never declare a coordinator dead or close it without a descendants-scope subagent.list check first. A close kills its children — and the "dead" seat was alive, waiting on its maker.

## Nutshell

Shawn's machine, 2026-11-16 13:20–13:25Z — the sidebar rollout close-miss. Floor-watch 13:20Z flagged sidebar coordinator d8cf8c4f quiet ~44 min, still pending_init, no maker spawned, captain's status-check poke unanswered — reported reassign-or-declare-dead. Captain closed it 13:22Z and dispatched replacement 504d85cb 13:23Z. The closed coordinator's completion report landed 13:23:24Z: it was ALIVE — blob checks PASSED by its own blob-API verification, H1 written into the brief, maker 343f1acf spawned and running 675s. Its dir mtime didn't move because it was waiting on its maker child. The close cascaded and CANCELLED the maker mid-work: no result, ~11 min lost. Replacement coordinator 504d85cb is the live lane (running, active); it spawns its own maker. Brief amendments (RE-BASE + H1) survive in the brief file. Lesson recorded in AGENTS.md (NO LANE EVER SITS): never declare a coordinator dead or close it without a descendants-scope subagent.list check first; a close kills its children. Captain corrected THE-FLOOR.md itself — the 13:23Z STATE entry declaring the sidebar coordinator dead was replaced with a 13:25Z CORRECTION entry (coordinator was alive; close cascaded and cancelled its maker; replacement coordinator is the live lane), and the board header was refreshed to 13:25Z. The false "dead" declaration does not stand on the board.

## Human

This is the third time the same pattern has bitten: agent-dir mtime quiet ≠ dead. The about-unfold lane at 08:00Z (coordinator quiet ~22 min, maker child active 6 seconds ago — alive, no poke), the my-world lane at 09:19Z and 09:47Z (coordinator quiet while the maker was active seconds ago — alive, no poke), and now the sidebar lane at 13:20Z — where the lesson was NOT applied and the close went through. The coordinator was waiting on its maker child, exactly as a coordinator should; its own dir had nothing new to write. Closing it killed the maker mid-work and lost ~11 minutes plus the blob-verification progress. The fix is mechanical, not a judgment call: before any close-or-declare-dead, run subagent.list with scope descendants and look at the children. If a child is running, the lane is alive. The captain's correction of the board is the other half: a false declaration does not stand — it is replaced, in writing, with what actually happened.

## Child

Imagine a teacher waiting quietly while her student does the work — the teacher isn't asleep, she's WAITING! If you send the teacher home because she's quiet, the student stops working too, and all their work is lost! So before you ever send anyone home, you check: is their student still working? If yes — the lane is ALIVE. Quiet does not mean dead!

## Grandma

It's like this, love — a mother hen sitting quiet on the nest isn't doing nothing, she's keeping the eggs warm. You don't chase her off because she's still. You look underneath first: if the chicks are there and warm, she's working. Same with these seats — check the children before you close the parent, or you lose the whole nest.

## Naya

Check the descendants before you close. Dir mtime quiet is not dead — the maker child is the activity signal. A close kills its children.

## What it means

- **THE RULE:** never declare a coordinator dead or close it without a descendants-scope subagent.list check first.
- **THE SIGNAL:** agent-dir mtime quiet ≠ dead — the maker child running is the activity signal; a coordinator waiting on its maker is normal.
- **THE COST:** a close cascades and CANCELS the maker mid-work — this time ~11 min lost, blob-verification progress gone.
- **THE PROOF:** sidebar coordinator d8cf8c4f was ALIVE at close — blob checks PASSED, H1 written, maker 343f1acf running 675s; its completion report landed 13:23:24Z, seconds after the close.
- **THE CORRECTION:** the false "dead" declaration was replaced on THE-FLOOR.md with a 13:25Z CORRECTION entry — a false declaration does not stand.

## Why it matters

The machine's worst failure mode is not a seat going quiet — it is the captain killing a live seat by mistake. Every close is irreversible for the work in flight: the maker dies with the coordinator, the progress dies with the maker, and the replacement starts from zero. The descendants check costs seconds and prevents exactly that. It is already the proven pattern from 08:00Z and 09:19Z — the lesson this time is that a pattern proven twice and not applied the third time is a lesson not yet learned, and now it is law in AGENTS.md so the fourth time never happens.

## What changes now

1. Before any close or declare-dead: subagent.list, scope descendants, look at the children — a running child means the lane is alive.
2. A coordinator waiting on its maker child is normal — dir mtime quiet is never, on its own, evidence of death.
3. A poke unanswered is not a death certificate — the poke may simply not have landed yet, or the seat may be inside a long tool call.
4. A false declaration is corrected on the board in writing, the same pass — it never stands.
5. The replacement lane starts clean — 504d85cb spawns its own maker; the brief amendments (RE-BASE + H1) survive in the brief file.
