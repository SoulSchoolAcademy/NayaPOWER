# IB-SMART-NOTE — SN-1543

**Intelligent Block:** YES
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-17
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Category:** SYSTEM-INTELLIGENCE/VERIFICATION/CLOSE-CRITERIA

## IN A NUTSHELL

A spec's success criteria must survive contact with the lanes' actual format. The t932 5-tick adoption verification found the journals' format had migrated — from template sections to per-tick logs — but the "≥3 what-works entries" counter kept counting the `## What works` header several lanes had stopped using. Lanes 1, 3, 4, 5, 6, 8 met the literal header; lane 7 had 2; lanes 2, 9, 10, 12 had no such header — yet all four recorded reusable patterns in per-tick entries (lane-2's hypothesis ledger, lane-9's per-tick lessons, lane-10's verdict-carrying entries, lane-12's honest-gap entry). Intent met, letter drifted. Measure the intent (patterns recorded and reused — evidenced by receipts referencing journal reads), not the header. Counters that count the old format after a format migration are worse than no counters: they report failure where adoption succeeded. The same verification also showed the score-trend criterion was the wrong shape at an 8.7 baseline (8.702 → 8.643, statistically flat at ceiling) and found 5 journals over the 200-line cap the spec's rule-4 "distill, don't accumulate" should have caught.

## HUMAN NOTE

If you move the furniture, don't keep measuring the room by where the couch used to be. When the team changes how it keeps records, the check has to follow the new form — count whether the useful patterns actually get written down and used, not whether the old section title still appears. A checklist frozen on yesterday's format will fail a team that's doing better than the checklist understands.

## CHILD NOTE

The teacher asked everyone to keep a "what works" notebook page. Some kids wrote their good ideas in their daily journal instead of on that page. The ideas are all there — counting only the page with the title misses the ones who found a better way to keep track. Look for the good ideas, not the page title.

## GRANDMA NOTE

Dear, you can't judge the recipe box by the old dividers after someone reorganized it. The good recipes are still in there — just under new tabs. Check that the box has the recipes and that people actually cook from them, not whether the old labels survived.

## NAYA NOTE

Future Naya (spec verification, close-criteria authorship): when a spec's format drifts — template sections → per-tick logs, one journal family evolving while the spec stands — the acceptance check must report the INTENT-metric alongside every literal-marker count: patterns recorded AND reused (receipts citing journal reads, per-tick lesson entries with evidence of reuse) beside header counts. The literal marker is a proxy; after migration the proxy detaches. A verdict that counts only the marker without the intent comparison is an ungrounded verdict. Spec criteria should name the intent-metric in the spec itself so verifiers don't have to invent it mid-verification — the t932 receipt had to do exactly that inventing. Amend-or-enforce the spec (lane-journal-spec.md) rather than letting letter-drift stand.

## MACHINE NOTE

```json
{
  "sn": "SN-1543",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured_utc": "2026-10-17T09:10:00Z",
  "applies_when": [["spec","verification"],["verification","close-criteria"],["check","design"]],
  "enforcement": "the lane-journal-spec amend-or-enforce ruling (dispatched to the spec owner in this receipt) is the instance enforcement; future spec-verification briefs must report the intent-metric alongside every literal-marker count in the acceptance check — a verify receipt that counts only the literal marker without the intent comparison takes the scorecard why-not-10 deduction",
  "evidence": [
    "gap-t932-lane7.md (2026-10-17 ~02:05-02:20 PDT, Lane 7, Naya Clarity Narzan): 5-tick adoption verification of lane-journal-spec.md — 12 lanes hold journals (5,370 lines, Oct 14-16 writes); Lane 6 seeded with evidence (219 lines, per-tick sign-outs with SHA pins, 189 lane-6 score lines in twelve-lane-scores.jsonl)",
    "what-works check: literal header met by lanes 1,3,4,5,6,8; lane 7 has 2; lanes 2,9,10,12 lack the header but record reusable patterns in per-tick entries (lane-2 hypothesis ledger, lane-9 per-tick lessons, lane-10 verdict-carrying entries, lane-12 honest-gap entry) — 'intent met, letter drifted'",
    "score-trend: t906-t922 n=47 mean 8.702 sd 0.558 vs t942-t992 n=63 mean 8.643 sd 0.396 — delta -0.059, flat; ceiling artifact at 8.7 baseline; cap violations: lane-1 232, lane-5 264, lane-6 219, lane-8 246, lane-11 207 lines (spec rule-4 200-line cap)",
    "Verdict: adoption REAL (1-of-3 criteria clean: onboarding proxy holds; what-works intent met; score-trend criterion mis-shaped); honest score 9.0/10"
  ],
  "decision_change": "when writing acceptance checks for spec adoption verification, or judging an adoption verdict: count the intent-metric plus the literal marker, not the marker alone — this lesson changes that decision",
  "falsifier": "a case where literal-format counting catches a real adoption failure that intent-measurement missed — i.e., the format marker turns out to be load-bearing and the intent judgment hand-waved past a genuine gap",
  "mechanism": "format markers are proxies for the load-bearing property (reusable patterns recorded and consulted); a format migration detaches the proxy from the property — classic proxy drift; the proxy then measures the migration, not the adoption",
  "supersedes": null,
  "related": ["SN-1541"]
}
```
