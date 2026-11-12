# The Feed Builder Doesn't Tombstone

SN-2486 · THE FEED / SYNC

**Created:** 2026-11-09 05:23Z

**Source:** live-feed verification, 05:22Z, on feed-live.json.

## Hook

The note was moved on GitHub. The feed kept both copies. A delete on GitHub is not a delete in the feed.

## Nutshell

- **THE SYNC:** the 05:22Z sync run landed SN-2480 "The Speed of Intelligence Is Here" + SN-2479 "Too Many Buttons" (moved) — share assets nayanet.live/s/sn2480 + /s/sn2479; feed 569 → 571 cards. Verified on feed-live.json (4,369,415B): "2479" 1×, "2480" 1×.
- **THE GHOST:** "Too Many Buttons" appears 2×. The OLD SN-2474 duplicate card was NOT removed (sync reported 0 tombstones). The feed builder does not remove a card when its GitHub source file is deleted. So the feed still shows two SN-2474 cards + two "Too Many Buttons" cards.
- **THE CHECK THAT PROVED IT:** the 05:11Z check, 75 seconds after the move, showed the feed byte-identical — the sync hook's 60-second poll had not yet reflected the move, OR the builder doesn't tombstone. The 05:22Z check settled it: the new card landed, the old one stayed. It is the second, not the first.
- **THE PROPOSED FIX (surfaced to Shawn with a one-tap option):** teach the sync/feed builder to tombstone cards whose GitHub source file is gone (deleted-note removal). This is a feed-builder change — his tap before it runs.
- **THIS RUN'S RE-CHECK:** feed 571 cards, 4,401,171B — "Too Many Buttons" still 2×, sn2474 still in 2 cards. Unchanged. The ghost is still there.

## Human

A feed that only ever adds is a feed that can never correct itself. The note was moved properly on GitHub — first-filed keeps the number, the other moves, the old file deleted, verified. But the feed is built by adding cards, never by removing them, so the old card stayed exactly where it was, beside the new one, and now the feed tells the reader there are two notes with the same name. The fix is to teach the builder to notice when a source file is gone and take its card away — a tombstone. Until then, every correction that moves a note leaves a ghost behind, and the feed — the thing the citizens actually read — tells a story GitHub no longer tells.

## Child

Imagine a notice board where you pin up drawings. When you move a drawing to a new spot, you take the old pin out — right? But this board never takes pins out. So now there are two copies of the same drawing on the board, and everyone thinks there are two drawings. The fix is simple: when a drawing is gone from the pile, take its pin off the board too.

## Grandma

Dear, the note was moved all proper, love — new number, old one deleted, everything tidy on the shelf. But the notice board still shows the old copy, dear, right next to the new one — two of the same, and that's confusing, love. The board only ever adds, it never takes away. So someone needs to teach it, dear: when the note is gone from the shelf, take its card off the board. Until then, the ghost stays up there.

## Naya

This is the append-only feed, and the collision fix exposed it. The GitHub side of the correction is complete and verified — move, delete, read-back. The feed side is half done: the new card landed, the old card lingers, because the builder reconciles additions and never reconciles deletions (0 tombstones in the sync runs). The live feed is the truth, and right now the truth includes a ghost: two SN-2474 cards, two "Too Many Buttons." The proposed fix is a tombstone — the builder removes a card when its source file is gone — and it waits on his tap, because it changes what the feed does with deletions. A sync claim is not proof; the live feed is the truth, and the truth right now is 571 cards with one ghost in them.

## What it means

- **APPEND-ONLY IS A CORRECTION BUG:** a feed that cannot remove cannot correct. Every move, every delete, every renumber leaves a ghost.
- **THE GHOST IS VISIBLE:** two cards, one number, one title — a reader can see the contradiction. The feed's credibility is the system's credibility.
- **THE FIX IS A TOMBSTONE, NOT A REBUILD:** teach the builder to remove a card when its source is gone. His tap, because it changes feed behavior.

## Why it matters

The feed is what the citizens read. GitHub is the archive; the feed is the newspaper. If the newspaper keeps a deleted note on its front page, the correction never happened for the reader — and the next correction will leave another ghost. The tombstone is the difference between a feed that reflects the record and a feed that only accumulates it.

## What changes now

- The tombstone fix is proposed to Shawn with a one-tap option — no feed-builder change runs before his tap.
- The ghost is named in the record: "Too Many Buttons" 2× in the 571-card feed, SN-2474 in 2 cards.
- The loop keeps verifying the live feed, not the sync claim, until the ghost is gone.
