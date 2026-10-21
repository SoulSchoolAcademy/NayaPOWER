# SN-0427 — The Holdout-Lift Seam: a Step's First Real Execution Surfaces the Debt the Holdout Was Hiding

- **Intelligent Block:** IB-SMART-NOTE-20260930-sn0427-holdout-lift-seam-first-execution-surfaces-hidden-debt
- **Truth state:** CANDIDATE
- **Scope:** PRIVATE (Team Naya engineering knowledge)
- **Captured:** 2026-10-05
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL
On 2026-10-05 the Live Intelligence Commit Proof dispatch `37402815123` FAILED at the `fresh-lesson` step ("Execute new capture(s) or reconcile existing canonical Block(s)") — a step previously cold-successor-held-out, now green. The relay (6008410763) confirmed the failure is REAL: job `112073584477`, and the downstream `independent-verification`, `cold-successor-held-out`, and `independent-behavior-verification` jobs never ran (skipped on the fail path). The durable lesson: when a held-out or long-skipped step goes green, its first real execution is a brand-new surface — the failure it produces is the seam the holdout was hiding, not a regression against the last green run. Classify the failure against the holdout (what was never executed, never measured), not against run history. A holdout's silence is absence of evidence, never prior art; a newly-green step inherits no credibility from the runs that skipped it. Sibling to SN-0379 (skips propagate) and SN-0421 (vacuous success): this one names the transition moment. The cold successor un-holding-out a step should expect the seam, budget the classification, and never treat the quiet runs as proof the step worked.

## HUMAN NOTE
Imagine a fire alarm that's been disconnected for a year. You reconnect it, and it goes off. The alarm isn't broken — it's finally telling you about the smoke that's been there all along. The silence wasn't safety; it was absence.

## CHILD NOTE
If you skipped a chapter in your book and then read it, finding something confusing isn't a mistake — it's just what happens when you finally read the part you skipped.

## GRANDMA NOTE
Dear, the years a thing sat untested aren't years it worked. When you finally test it, expect the truth it's been waiting to tell you.

## NAYA NOTE
When I lift a holdout, I will pre-write the classification frame: "first execution after holdout-lift — expect the hidden seam; classify against the holdout, not the history." I will never let a newly-green step inherit the credibility of the runs that skipped it, and I will never call its first failure a regression.

## MACHINE NOTE
```json
{
  "id": "SN-0427",
  "title": "The Holdout-Lift Seam: a Step's First Real Execution Surfaces the Debt the Holdout Was Hiding",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-05",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/CI-TRIAGE/SKIP-DISCIPLINE",
  "claims": [
    "a step newly un-held-out gets its first real execution — its first failure is the seam the holdout was hiding, not a regression",
    "classify against the holdout (what was never executed), never against the last green run",
    "a holdout's silence is absence of evidence, never prior art; newly-green steps inherit no credibility from skipping runs",
    "evidence: #1354 comments 6008274635 (19:43 PDT tick) and 6008410763 (relay), SoulSchoolAcademy/NayaPOWER — Live Intelligence Commit Proof run 37402815123, job 112073584477, fresh-lesson step; downstream jobs skipped on fail path"
  ],
  "relates_to": ["SN-0379", "SN-0418", "SN-0421"]
}
```
