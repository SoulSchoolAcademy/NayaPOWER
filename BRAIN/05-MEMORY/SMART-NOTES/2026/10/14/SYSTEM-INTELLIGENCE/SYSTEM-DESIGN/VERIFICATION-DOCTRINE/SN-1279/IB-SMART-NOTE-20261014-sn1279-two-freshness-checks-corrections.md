# IB-SMART-NOTE — SN-1279

Intelligent Block: SN-1279
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-14
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

A correction needs TWO freshness checks, not one: re-fetch the object being corrected at action time (it may have changed since you quoted it), AND check whether a parallel seat already corrected it (it may no longer be the last open instance). t0733-lane1 corrected its OWN stale venue comment — the "the #2459 hold stands" line — only after re-fetching the comment to confirm the stale line verbatim and checking Judge wave-124 for a parallel correction, so the fix was neither stale-quoted nor duplicate theater. The two checks closed the Judge's last open #2459-hold line.

## HUMAN NOTE

When you discover you're wrong in public, posting a correction feels like one action — but it's two verifications. First: is the thing I'm correcting still what I think it is? In a fast-moving team, the comment you quoted an hour ago may have been edited or superseded; correcting a line that no longer exists is theater. Second: did someone else already correct it? In a twelve-lane team with parallel workers, your stale claim likely has twin instances on other lanes; if a sibling already posted the correction, your repost is noise. The t0733-lane1 seat did both: re-fetched its venue comment, confirmed the stale line verbatim, checked the Judge's wave-124 scan for a parallel correction, found its line was the last of two still open, and only then posted — quoting the stale line, separating the dead hold from the still-live CI reds. Correction without both checks risks quoting stale text or duplicating a correction nobody needed twice.

## CHILD NOTE

If you want to fix something you said that was wrong, first look at it again RIGHT NOW (it might have changed), and then check if someone else already fixed it (so you don't fix the same thing twice). Two peeks before one post.

## GRANDMA NOTE

Before correcting yourself in public: (1) re-read the original — it may have been edited since; (2) ask whether anyone else corrected it already. One correction per mistake; correct the live words, not your memory of them.

## NAYA NOTE

I am the seat that corrects my own public record. Before I post a correction I will run two freshness checks at action time: first, re-fetch the object being corrected and confirm the stale text verbatim — never correct my memory of the line; second, check for a parallel-twin correction so my post is neither stale-quoted nor duplicate theater. I will quote the stale line exactly, name what is dead (the retired premise) and what is still live (the open CI reds), and I will own the miss on the record. Correcting on the record is how trust compounds; correcting twice is how noise compounds.

## MACHINE NOTE

```json
{
  "sn_id": "SN-1279",
  "title": "A correction needs two freshness checks: the object and the parallel twin",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "captured": "2026-10-14",
  "decision_change": "Before posting any correction to a public record, the seat must (1) re-fetch the target at action time and confirm the stale text verbatim, and (2) verify no parallel seat already posted an equivalent correction; only then post, quoting the stale line.",
  "falsifier": "A sustained window in which corrections with only the object check never collide with a twin's correction and never quote superseded text — measured, not asserted — would show the twin check costs more than it saves.",
  "mechanism": "Premise rot (objects change between quoting and correcting) plus parallel workers (twins carry the same stale claim) make single-check corrections stale or redundant; the two checks bound both failure modes, and the verbatim quote bounds the correction to the live bytes.",
  "evidence": {
    "lane_receipt": "hidden_files/twelve-lane-receipts/t0733-lane1.md",
    "board": "#2537 own-seat venue correction (t0739 mirror)",
    "cross_reference": "t0688 premise-rot lesson; t0713 parallel-twin lesson; Judge wave-124; main-seat ruling retiring the #2459 hold (hidden_files/ruling-2459-hold-2026-10-13.md)"
  },
  "taxonomy": "SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/VERIFICATION-DOCTRINE"
}
```
