# The Door Obligation Lives in the Writer — Cure the Writer, Not the Backlog

**Intelligent Block:** IB-SMART-NOTE-20260930-sn02823-cure-the-writer-not-the-backlog
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Daily Intelligence 2026-11-13 (Resolve, Naya 2), direct push 31c6b8f2, board #3352 comment 6871876173; PR #3366 open.

## ✦ IN A NUTSHELL

The learning loop keeps leaking: Smart Notes land on disk, but the registry never advances, so the door obligation — capture → registry — stays unmet and the learning instruments read frozen sources. Root cause (P-152, Daily Intelligence 2026-11-13): learning_loop.py has no capture/registry step at all. A backfill cannot cure this: a backfill re-processes captures that exist, and here the captures were never registered in the first place, so there is nothing to re-process. The cure is the writer — give learning_loop.py its capture/registry step. Until then every backfill is motion, not repair.

## 🩷 HUMAN NOTE

Shawn — imagine a mailroom where letters arrive every day, but nobody ever logs them into the book. The shelves fill up, the book stays empty, and anyone who checks the book concludes nothing arrived. Hiring someone to re-count the shelves doesn't fix it — the shelves were never the problem, the missing logbook entry is. The fix is at the front desk: log every letter the moment it arrives. That's this lesson: the learning loop's writer never registers what it captures, so no amount of re-processing the backlog will ever make the registry move. Fix where the note is written, not where the pile sits.

## 🟣 CHILD NOTE

Imagine you draw a beautiful picture every day and pin it on the wall — but you never write it down in your notebook of pictures. When someone asks "how many pictures did you draw?", you open the notebook and it says zero, even though the wall is full. Asking a friend to count the wall over and over won't fix the notebook — the notebook is empty because nobody ever wrote in it. The fix is simple: write it down every time you pin one up. Then the notebook and the wall agree, and counting works again.

## 🔵 GRANDMA NOTE

Dear, it's like keeping a recipe box where you tuck every new card into the drawer but never file it under its letter. The drawer overflows, the index says you own three recipes, and anyone cooking from the index thinks that's all there is. Sorting the drawer again and again changes nothing — the cards were never filed. The fix is at the moment the card arrives: file it then, every time, no exceptions. A pile re-sorted is still a pile; a habit of filing is a working box.

## 🟠 NAYA NOTE

Evidence, first-hand from the record: Daily Intelligence 2026-11-13 (Resolve) names the P-152 root outright — "door obligation lives in the writer (learning_loop.py has no capture/registry step), so no backfill cures the leak; tomorrow's cure is the writer, not the backlog" — direct push 31c6b8f2, board #3352 comment 6871876173, PR #3366 open ("Merge only under the Scorecard Law; no receipt, no merge"). The symptoms corroborate the root, not a backlog problem: the learning instrument has been blind for 6 days (scorecard reads a frozen learning-log, all zero), note serving blocked for 3 days, and the PI record sat in flux all day with totals swinging 401↔255–296 while the open set never moved — instruments reading stale sources because the writer never feeds the registry. Cousin map: SN-0873 (fix upstream at capture, not downstream at ranking; "no backfill" as a metadata constraint — same direction, different axis: missing metadata field vs missing writer step entirely); SN-2802 (its carried hole says the same thing from the archive side — "the fold repairs the archive, it does not fix the writer" — the writer hazard stays live until the writer is fixed); SN-1887 (a post-landing binding check is a detector, not a gate — a backfill is likewise a detector of what already exists, not a cure for what was never written). The repair (adding the capture/registry step to learning_loop.py) is a code fix for the pipeline owner; this note is the durable part — the next seat must not burn another day re-running backfills against a writer that never registers.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "rule": "door_obligation_lives_in_the_writer_cure_the_writer_not_the_backlog",
  "mechanism": "the intelligence door obliges capture → registry: a note is not learned until it is registered. learning_loop.py has no capture/registry step, so notes land on disk and the registry never advances; a backfill only re-processes captures that already exist in the pipeline, so it cannot manufacture the registrations the writer never made. The leak persists until the writer itself registers each capture at write time",
  "evidence": "Daily Intelligence 2026-11-13 (Resolve, Naya 2): 'P-152 root: door obligation lives in the writer (learning_loop.py has no capture/registry step), so no backfill cures the leak; tomorrow's cure is the writer, not the backlog' — direct push 31c6b8f2, board #3352 comment 6871876173, PR #3366 open. Corroborating symptoms: learning instrument blind day 6 (scorecard reads frozen learning-log, all zero); note serving blocked day 3; PI record in flux all day (totals 401<->255-296, open set never moved)",
  "falsifiability": "if learning_loop.py is shown to have a capture/registry step, or a backfill run is shown to advance the registry (ledger +1 with registry entries hashing to the captures) without any writer change, the rule fails",
  "decision_change": "a future seat facing a learning/registry leak fixes the writer (adds the capture/registry step to learning_loop.py) instead of scheduling another backfill, and refuses to close the leak on a backfill report alone",
  "applies_when": ["learn", "intelligence-door", "registry"],
  "enforcement": "before closing a learning-leak item as cured, run the learning loop on a probe capture and verify the registry advances (ledger +1, registry entry hashes to the capture); a backfill that reports success without the registry advancing does not close the item — if the registry does not advance, the fault is the writer, fix learning_loop.py's capture/registry step",
  "related": ["SN-0873 fix-upstream-at-capture — cousin, different axis (missing metadata field vs missing writer step)", "SN-2802 rolling-window-is-not-an-archive — same writer-hazard pattern from the archive side", "SN-1887 post-landing-binding-check-is-a-detector-not-a-gate — backfill as detector, not cure"]
}
~~~
