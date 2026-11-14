# Existence-Check First, Then Recency-Check — A Gap Brief's First Move Is "Is the Named Thing Still Alive?"

**Intelligent Block:** IB-SMART-NOTE-20260930-sn02824-existence-check-first-then-recency-check
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** learning-events-2026-11-14-02.md (hourly learning review, 2026-11-14 ~02:20 PST); CORE-PRINCIPLES.md CANDIDATE 1053; gap-t1152-lane8.md, gap-lane-scorer-20261114-0200-lane10.md, gap-lane-scorer-20261114-0200-lane2.md, gap-lane-scorer-20261114-0150-lane7.md (all 9.5/10).

## ✦ IN A NUTSHELL

Three gap receipts in one hour closed month-stale gaps by falsification or supersession instead of by the named fix — the briefs were wrong about the world, not about the fix. The brief said PR #2429 was never opened; it was opened 2026-10-12 and closed superseded 23 minutes later because the rename had already landed via merged #2428, byte-identical — re-merging would have regressed 5,313 lines. The t1032 heal branch never had a PR at all; superseding #2437 merged 2026-10-12. Successor-reuse had already been tested Oct 12 (delta 0.0). The rule: a gap brief is a snapshot; the world moves after filing. A gap filing carries a filing-time "world-moved?" check, and an executor checks existence before state, recency before instruments, and the full grep before the brief's list.

## 🩷 HUMAN NOTE

Shawn — imagine being handed a repair ticket written a month ago that says "the back door was never installed." You go to install it, but the door was installed a month ago, and installing it again would rip out the wall. The ticket wasn't lying when it was written; the house changed after it was written. Three tickets in one hour were exactly that: the world had already decided them. The fix is a habit, not a tool: before touching anything, ask "is the thing this ticket names still alive, and what happened since the ticket was written?" — check the live world first, then the ticket.

## 🟣 CHILD NOTE

Imagine your teacher gives you a note that says "the library book was never returned." You go to return it — but your friend already returned it last month, and returning it again would mean taking a book that isn't yours. The note was true when it was written, but the world changed. Always check the real world first: is the book still out? What happened since the note was written? Then decide what to do.

## 🔵 GRANDMA NOTE

Dear, it's like getting a letter that says the fence was never mended — but your neighbor mended it weeks ago, and mending it again would tear down good work. The letter was honest when it was posted; the garden moved on. Before you lift a hammer, walk out and look: is the fence still broken? What changed since the letter was written? Look first, then work — never work from the letter alone.

## 🟠 NAYA NOTE

Sources: learning-events-2026-11-14-02.md (CANDIDATE 1053, filed 2026-11-14 ~02:20 PST). gap-t1152-lane8.md (9.5/10): the brief said the PR was never opened; PR #2429 WAS opened 2026-10-12 and closed superseded 23 minutes later because the rename had already landed via merged #2428, byte-identical, and re-merging would regress 5,313 lines. gap-lane-scorer-20261114-0200-lane10.md (9.5/10): the t1032 heal branch never had a PR, its head ran exactly one check (Supabase Preview, skipped), it was never merged and never reviewed anywhere (superseding #2437 merged 2026-10-12, 0 reviews). gap-lane-scorer-20261114-0200-lane2.md (9.5/10): successor-reuse was already tested Oct 12 (t1302: delta 0.0, blinded-confirmed by an independent scorer + Lane-1 certification), and the 1.0 delta's fragility is now a number (Newcombe 95% CI [0.070, 1.000], Fisher p approx 0.33). Corollary from gap-lane-scorer-20261114-0150-lane7.md (9.5/10): a grep is the test, not the line list — the brief named 5 "zero scored receipts" lines, the grep found 10, including lane-12.md:30, self-contradicting in one breath. Cousins: CANDIDATE 153 (dispatch-time pin check — the 60-second existence re-probe at dispatch), CANDIDATE 1051 / SN-2795 (a check name is not a suite — name the failing step first). This note is the executor's first move before any step.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "rule": "existence_check_first_then_recency_check",
  "mechanism": "a gap brief is a snapshot taken at filing time; the world keeps moving after filing - PRs open and close, branches merge, measurements get re-tested. An executor that trusts the brief without re-probing acts on a world that no longer exists, and the failure is silent because the brief's claims were true when written. Re-probing existence (PR/branch state via live GET) and recency (what happened since the parent) at execution time converts the snapshot back into a live claim before any fix is applied",
  "evidence": "learning-events-2026-11-14-02.md (CANDIDATE 1053): gap-t1152-lane8.md (9.5/10) - brief said PR never opened; PR #2429 WAS opened 2026-10-12 and closed superseded 23 minutes later, rename already landed via merged #2428 byte-identical, re-merging would regress 5,313 lines; gap-lane-scorer-20261114-0200-lane10.md (9.5/10) - t1032 heal branch never had a PR, head ran exactly one check (Supabase Preview, skipped), never merged or reviewed, superseding #2437 merged 2026-10-12 with 0 reviews; gap-lane-scorer-20261114-0200-lane2.md (9.5/10) - successor-reuse already tested Oct 12 (t1302: delta 0.0, blinded-confirmed by an independent scorer + Lane-1 certification), 1.0 delta fragility now a number (Newcombe 95% CI [0.070, 1.000], Fisher p approx 0.33); corollary gap-lane-scorer-20261114-0150-lane7.md (9.5/10) - brief named 5 'zero scored receipts' lines, grep found 10 including lane-12.md:30",
  "falsifiability": "a gap filed with a world-moved check that still reaches the queue stale would show the check insufficient; an executor closing a gap by the named fix without first checking whether the world already decided it - and being right - would show the re-probe unnecessary for that class",
  "decision_change": "any future gap filing carries a filing-time 'world-moved?' check; any executor's first move is existence before state, recency before instruments, and the full grep before the brief's list - a gap is closed by falsification or supersession when the world already decided it, never by the named fix",
  "applies_when": ["gap", "stale-brief", "executor"],
  "enforcement": "a gap receipt must quote its execution-time existence + recency re-probe (live PR/branch GET and full grep) before any fix is applied; a receipt that closes a gap by the named fix without that quoted re-probe is scored as a stale-brief miss by the lane scorer",
  "related": ["SN-2795 a-check-name-is-not-a-suite (CANDIDATE 1051) - sibling: name the failing step first; this note is the executor's first move before any step", "CANDIDATE 153 dispatch-time pin check - the 60-second existence re-probe at dispatch; this note extends the re-probe to gap filing and execution"]
}
~~~
