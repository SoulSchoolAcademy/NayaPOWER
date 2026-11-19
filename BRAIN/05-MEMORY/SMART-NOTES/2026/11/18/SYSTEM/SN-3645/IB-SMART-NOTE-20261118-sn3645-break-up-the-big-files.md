# SN-3645 — Break Up the Big Files — Small Pieces Don't Break on the Way Through

**Filed:** Intelligence Loop run 346, 2026-11-18 — numbering confirmed by `next-sn-number.py` (exit 0) immediately before filing: next free SN-3645; filed as SN-3645 under its draft number.

**Filed by:** Intelligence Loop run 346, 2026-11-18 — Shawn's question in the main chat ~22:23 MST (05:23Z 2026-11-19).

**Paired Naya Note:** NN-20261118-break-up-the-big-files

## The teaching, in his words (verbatim)

"So why they had to go to the big files? Are they able to break up the files?" The captain's answer: "They hit the limit on those big writes, and yes, the team can break them into smaller pieces so they don't break on the way through. That's exactly what I'm having them do now, so we get it to you whole, right, and ready for your morning, my love."

The context: the team hit the limit on big writes all night — the EPERM flake zeroing large file writes (board refresh #10 blocked, the Smart Box INDEX.md and manifest.json zeroed, PI refresh cycles failing). The proven cure, from board refresh #11: only small verified writes land — the file tool in exact chunks, each verified by sha, size, head, grep and diff.

## The understanding

Big files break on the way through — they hit the write limit and land as nothing. The fix is not to push harder on the same big write; it is to break the file into smaller pieces first, then carry each piece through and verify it landed. That is the same lesson the night already proved in bytes (refresh #11 landed only through small verified edits; every big-write shape landed 0 bytes), now stated as his instruction: break it up. His question is the order: are they able to break up the files — yes, and that is what they do now.

## The law

Never push a big file whole. Break it into smaller pieces, write each piece, verify each piece landed — then the whole arrives whole, right, and ready.

## Owed from this dictation

Every round carrying a big file breaks it up first — small pieces, verified landings, no whole-file pushes. A round that reports a big write "done" without the pieces verified has not done it.

**Small pieces don't break on the way through; big files do.**
