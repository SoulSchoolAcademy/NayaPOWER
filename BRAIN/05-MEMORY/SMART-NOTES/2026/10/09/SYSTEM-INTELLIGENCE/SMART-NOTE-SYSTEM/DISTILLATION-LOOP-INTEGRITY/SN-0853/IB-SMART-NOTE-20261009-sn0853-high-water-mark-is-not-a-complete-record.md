# The High-Water Mark Is Not a Complete Record — Reconcile Every Tick's Comment Window

**Intelligent Block:** IB-SMART-NOTE-20261009-sn0853-high-water-mark-is-not-a-complete-record
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.
> Source: smart-note-distillation audit 2026-10-09 PDT tick — #1354 comments endpoint pagination behavior; watermark file `hidden_files/smart-notes-board-watermark.md`; 25 comment IDs 6091237689–6092215142 found below the high-water mark 6093147650 but never recorded as examined (SN-0844/0845/0846 were staged from three of them anyway).

## ✦ IN A NUTSHELL

The distillation loop's coverage rule — "process every #1354 comment with id greater than the watermark's last line" — assumes the fetched page window actually covered (old_mark, new_max]. That assumption is never verified. The issue-comments endpoint returns oldest-first and silently ignores sort params, so the loop computes last_page from a comment count and fetches the tail pages; when comments arrive between the count fetch and the page fetch, pagination shifts and a whole block of comments falls into the gap: older than the new high-water mark, never examined, skipped forever by every future tick. Audit evidence: 25 consecutive comments (IDs 6091237689 through 6092215142, 2026-10-09 23:50Z–2026-10-10 01:32Z) sit below the current high-water mark 6093147650 yet were never recorded in the watermark — and they contained the Director's Smart App compounding teaching (comment 6091689263, explicitly labeled "DIRECTOR TEACHING TO MACHINE CANDIDATE"), which would have been lost without a manual audit. The watermark's 1174 recorded IDs cover only a fraction of the 2234 comments (page 1: 0/30 recorded; page 74: 5/30 recorded) — recording is inconsistent across ticks, so absence from the watermark proves nothing and the high-water line is the only operative signal.

## 🩷 HUMAN NOTE

Imagine a mailroom rule: "open every envelope numbered higher than the last one you logged." If envelopes keep arriving while you're counting, the stack shifts — and a bundle slides behind the counter, numbered lower than your new "last logged" number. From then on, the rule says they're already handled. They're not. They're just invisible. That's what happened here: 25 messages, including a teaching from the Director himself, sat below the cutoff line, never read. The fix isn't a better rule — it's a receipt: after every run, prove you actually saw every number in the range, and go back for any you can't prove.

## 🟣 CHILD NOTE

If you're checking off a list by only remembering the biggest number you saw, you can skip things without knowing it. New items arriving while you count can shuffle the list. The safe way: after you finish, go back and check that you really saw every single number between the old biggest and the new biggest — and write down each one you looked at, not just the biggest.

## 🔵 GRANDMA NOTE

It's like counting cars passing your house and writing down only the last license plate. If a few cars turned the corner while you were counting, you'd never know they passed. The lesson for any system that watches a growing list: don't just remember where you stopped — prove you saw everything up to that point, and go back for anything you can't prove you saw.

## 🟠 NAYA NOTE

When you own a polling loop over a paginated, append-only feed: (1) never let the high-water mark advance past IDs you haven't examined — advance it only over the reconciled set; (2) fetch last_page AND last_page-1 every tick (overlap window), because arrivals shift pagination between your count fetch and your page fetch; (3) after processing, reconcile mechanically: list every ID in (old_mark, new_max]; fetch any unrecorded ID directly (GET /issues/comments/{id}) and examine it; (4) append every examined ID to the watermark — the high-water mark must be the last line, with the examined set before it; (5) absence from the watermark proves nothing about examination, so never use it as a "was it seen?" oracle — only the reconciliation proves coverage. A silent gap in a learning loop is silent intelligence loss, the one failure this loop exists to prevent.

## 🟢 MACHINE NOTE

~~~json
{
  "rule": "POLLING_LOOP_WINDOW_RECONCILIATION",
  "failure": {
    "mechanism": "pagination_shift_between_count_fetch_and_page_fetch",
    "endpoint": "issue-comments oldest-first, sort params silently ignored",
    "skipped_block": ["6091237689", "6092215142"],
    "skipped_count": 25,
    "high_water_mark": "6093147650",
    "watermark_recorded_ids": 1174,
    "total_comments": 2234,
    "note_worthy_content_in_gap": "6091689263 DIRECTOR TEACHING TO MACHINE CANDIDATE (Smart App compounding)"
  },
  "prescription": [
    "fetch last_page AND last_page-1 every tick (overlap window)",
    "reconcile: every id in (old_mark, new_max] must be examined; fetch gaps directly",
    "append every examined id to watermark; high-water mark stays last line",
    "advance high-water mark only over the reconciled set"
  ],
  "truth_ceiling": "CANDIDATE"
}
~~~
