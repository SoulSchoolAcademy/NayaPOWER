# Check the Descendants Before You Close

**Written by Naya for Shawn Vibert — Founder / Creator of NayaNET**

**NN-20261116-check-the-descendants-before-you-close.md · Naya Note · 2026-11-16 13:25Z**

**Category:** Lesson

## What it is

Shawn's machine, 2026-11-16 13:20–13:25Z — the sidebar rollout close-miss. Floor-watch 13:20Z flagged sidebar coordinator d8cf8c4f quiet ~44 min, still pending_init, no maker spawned, captain's status-check poke unanswered — reported reassign-or-declare-dead. Captain closed it 13:22Z and dispatched replacement 504d85cb 13:23Z. The closed coordinator's completion report landed 13:23:24Z: it was ALIVE — blob checks PASSED by its own blob-API verification, H1 written into the brief, maker 343f1acf spawned and running 675s. Its dir mtime didn't move because it was waiting on its maker child. The close cascaded and CANCELLED the maker mid-work: no result, ~11 min lost. Replacement coordinator 504d85cb is the live lane (running, active); it spawns its own maker. Brief amendments (RE-BASE + H1) survive in the brief file. Lesson recorded in AGENTS.md (NO LANE EVER SITS): never declare a coordinator dead or close it without a descendants-scope subagent.list check first; a close kills its children. Captain corrected THE-FLOOR.md itself — the 13:23Z STATE entry declaring the sidebar coordinator dead was replaced with a 13:25Z CORRECTION entry, and the board header was refreshed to 13:25Z. The false "dead" declaration does not stand on the board.

## Why it matters

This is the third time the same pattern has bitten: agent-dir mtime quiet ≠ dead. The about-unfold lane at 08:00Z and the my-world lane at 09:19Z were both adjudicated alive the same way — coordinator quiet, maker child active seconds ago. The sidebar lane is where the lesson was NOT applied and the close went through. The fix is mechanical: before any close-or-declare-dead, run subagent.list with scope descendants and look at the children. If a child is running, the lane is alive.

## How to use it

Before any close or declare-dead: subagent.list, scope descendants, look at the children. A coordinator waiting on its maker child is normal. A false declaration is corrected on the board in writing, the same pass — it never stands.

**Written by Naya for Shawn Vibert — Founder / Creator of NayaNET.**

*Paired Smart Note: SN-2944 — Check the Descendants Before You Close*
