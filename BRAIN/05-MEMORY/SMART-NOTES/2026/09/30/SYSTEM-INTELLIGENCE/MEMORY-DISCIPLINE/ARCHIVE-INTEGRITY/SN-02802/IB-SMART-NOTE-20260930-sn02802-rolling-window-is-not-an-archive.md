# A Rolling-Window File Is Not an Archive — Fold by Lineage-Union, Guard with a Deletion-Count Audit

**Intelligent Block:** IB-SMART-NOTE-20260930-sn02802-rolling-window-is-not-an-archive
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** distill-daily-20261114-lane10.md (Lane 10 Librarian, 2026-11-14 05:38–05:57 PST), 9.5/10; PR #3372 (head f121b8cf); merged file sha256 ceb0b87b3dead417ffe36c5bdf298dc5402ae9162cc2ac723d28edb6b7b4c280.

## ✦ IN A NUTSHELL

Main's mission state was 3 days stale, and the branch file that was supposed to carry the live snapshots had silently lost one: the 2026-11-14 03:12 PST snapshot exists only in commit ec22342 — the 03:43 refresh wrote from a pre-03:12 read and dropped it, and the rolling window never noticed. The repair walked all 229 file revisions, unioned the snapshot blocks, took each block's last-seen text, and recovered 141 snapshots missing from main (137 newer than main's newest + 4 gap-fillers). The rule: a rolling-window file is not an archive — never trust its latest copy as the whole history. Fold by lineage-union, and guard the fold with a deletion-count audit: a fold that only adds must delete exactly the head line.

## 🩷 HUMAN NOTE

Shawn — imagine a whiteboard where someone copies the last 21 entries fresh every half hour. One morning they copy from a photo taken before the newest entry was written — and that entry is gone from the board forever, with nobody noticing, because the board only ever holds the latest 21. The fix isn't a better photo: it's keeping every photo ever taken and merging them all, so nothing written can ever fall out of the pile. And before you hang the merged board, you count the eraser strokes: you only meant to erase the title line, so if 19 lines vanished, something went wrong — stop, fix it, re-check. That's this lesson: a rolling window forgets by design, history lives in the revisions, and the deletion count is the tripwire that proves the merge only added.

## 🟣 CHILD NOTE

Imagine you keep a sticker book, but every day you copy only your 21 favorite stickers onto a fresh page and throw the old page away. One day you copy from yesterday's page before your newest sticker was stuck on — and that sticker is gone, and nobody remembers it was ever there. The smart way: keep every page you ever made, and when you want the full collection, lay all the pages side by side and pick up every sticker from every page. And count before you finish: if you only meant to take away the title at the top, but 19 stickers are missing, you made a mistake — start over and check again.

## 🔵 GRANDMA NOTE

Dear, it's like the recipe box where you only keep the 21 newest cards on top and toss the rest each week. One week you tidy from an old pile, before your newest recipe was added — and that recipe is gone for good, because the box never kept a copy. The fix is simple: never throw a card away, and when you rebuild the box, go through every card you've ever had and keep the latest version of each one. And before you close the lid, count: you only meant to replace the label on the front, so if 19 cards are missing, something's wrong — open it back up and look. A box that forgets is not a memory; the whole history is.

## 🟠 NAYA NOTE

Source: distill-daily-20261114-lane10.md (2026-11-14 05:38–05:57 PST), 9.5/10. Main 72f656a0, BRAIN/CURRENT-MISSION-STATE.md 2,236 lines / 138 snapshot blocks, newest 2026-11-11 05:12 PST. Branch origin/naya/mission-state tip 4a813ed (05:11 PST refresh), 323 lines / 21 blocks. Deepened the shallow clone (2 rounds) so lineage reached Nov 9; walked all 229 file revisions and unioned the blocks: 279 distinct snapshots; 141 missing from main (137 newer than main's newest + 4 gap-fillers Nov 9 12:47 / 13:15 / 13:46, Nov 10 21:15). The lost block: 2026-11-14 03:12 PST exists only in commit ec22342; the 03:43 refresh (051c3fc) wrote from a pre-03:12 read and dropped it. Text rule: 12 snapshots had a transient first draft corrected by a later refresh — the fold uses each snapshot's last-seen text; all 138 archived blocks verified byte-identical to the branch canonical text (0 diffs), so the fold is purely additive. Own bug caught by the guard: dict(main_seq) keyed by separator, not header — the git-diff deletion audit showed 19 deletions (head + 18 blank lines) instead of the expected 1; fixed to {h: sep for sep, h in main_seq} and re-verified. Merged file sha256 ceb0b87b3dead417ffe36c5bdf298dc5402ae9162cc2ac723d28edb6b7b4c280 — 279 blocks, 4,720 lines, head 2026-11-14 05:11 PST, oldest 2026-11-07 19:08 PST; diff vs main 2,397 insertions, 1 deletion (the old head line only). Commit f121b8cf, PR #3372 (open, mergeable true, created 2026-11-14T13:55:49Z). Carried hole: the branch's stale-read refresh hazard is still live — the next refresh could drop another snapshot the same way; the fold repairs the archive, it does not fix the writer.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "rule": "rolling_window_is_not_an_archive_fold_by_lineage_union",
  "mechanism": "a rolling-window writer reads the window, then writes a refresh computed from that read; any block appended between the read and the write is silently dropped, and because the window keeps only the latest N blocks the dropped block never returns. Git history retains every revision, so unioning blocks across all revisions recovers dropped blocks, and last-seen text wins because later refreshes correct transient first drafts. A pure-add fold's diff must delete exactly the head line, so the deletion count catches keying bugs (separator-keyed dict deleted 19 lines instead of 1) before commit",
  "evidence": "distill-daily-20261114-lane10.md (2026-11-14 05:38-05:57 PST, 9.5/10): 229 file revisions walked, 279 distinct snapshots unioned, 141 recovered as missing from main (137 newer + 4 gap-fillers); lost block 2026-11-14 03:12 PST exists only in commit ec22342, dropped by the 03:43 refresh (051c3fc) writing from a pre-03:12 read; merged file sha256 ceb0b87b3dead417ffe36c5bdf298dc5402ae9162cc2ac723d28edb6b7b4c280, diff vs main 2,397 insertions / 1 deletion; PR #3372 head f121b8cf",
  "falsifiability": "if a lineage-union fold were shown to lose a block that a latest-snapshot copy preserved, or a fold passing the deletion-count audit still lost content, the rule fails; if a rolling-window writer is proven to read-then-write atomically with no window between read and write, the stale-read hazard does not apply to that writer and the fold may trust its latest copy",
  "decision_change": "a future seat folding a rolling-window file into an archive walks every file revision and unions the blocks (last-seen text per block) instead of copying the latest snapshot, and runs the deletion-count audit before committing",
  "applies_when": ["archive", "snapshot-fold", "stale-read"],
  "enforcement": "before committing a snapshot fold, run the diff deletion-count audit: git diff must show exactly 1 deletion (the old head line) for a pure-add fold; more deletions means rebuild, never commit; then re-parse the committed file and verify every archived block byte-identical and in strict ISO time order",
  "related": ["SN-2801 shrink-receipt-to-delta — same family of verify-before-commit audits, different axis: brevity of a repeated receipt vs integrity of an archive fold"]
}
~~~
