# An Absence Claim Cites Its Query — a Claim About a Query Is Not a Claim About the World

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01711-absence-claim-cites-its-query
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-19
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 19:38 PDT distillation tick (2026-10-19) from hidden_files/learning-events-2026-10-20-02.md (CANDIDATE 700, mirror lesson from twelve-lane-receipts/t0960-lane10.md). No new #1354 comments were read this tick (#1354 at GitHub's 2500-comment hard cap; commenting disabled 2026-10-10; director pass is the single reader).

## ✦ IN A NUTSHELL

t0955 recorded tip 1a1c22d32 as UNVERIFIABLE: "no core runs at tip-time." That is a claim about a query's result, not about the world — and the world answered differently. t0960 re-queried the check-runs API with the same query and found runs 39220810284 + 39220810297, created at tip-time, both failing with the identical brain-index DRIFT signature. The tip was RED; the label was the bug. The lane caught its own mislabel only because it re-ran the query instead of inheriting the verdict. The rule: **every absence claim in a receipt carries the exact query that produced it — endpoint, parameters, window, result count — so the next seat re-fires it instead of copying the verdict.** An inherited absence verdict with no re-fire is a rumor wearing the shape of evidence. This is distinct from SN-0361 (pin revision + exact command at claim time): that lesson grounds the claim when made; this lesson governs what the NEXT seat does with it — re-execute, never inherit.

## 🩷 HUMAN NOTE

Shawn — small evidence lesson from the verify lane: one receipt labeled a tip "unverifiable — no test runs existed," but the next seat re-ran the same query and found two failed runs the first query had missed — the tip was actually broken, and the label was wrong. The fix is simple: whenever a receipt claims something *doesn't* exist, it must say exactly what query it ran (where, what parameters, what window, what it got back) — so the next person re-runs the check instead of just copying the conclusion. Filed as Smart Note candidate SN-01711.

## 🟣 CHILD NOTE

Saying "there's no milk in the fridge" is really saying "I looked in the fridge and didn't see milk." If your brother just copies your words without looking himself, he might miss the milk hiding behind the juice — and now two people believe the wrong thing. The rule: when you say something isn't there, write down exactly where you looked and how — so the next person looks again themselves instead of just believing you.

## 🔵 GRANDMA NOTE

A "nothing there" claim is only as good as the search that produced it. The team learned the hard way: one report said a software release had no test results, so it couldn't be judged — but the next person re-ran the exact same search and found two failed tests. The release was broken; the first report was the problem. Now the rule is: whenever you report that something is missing, you write down exactly how you searched, so the next person can run the same search fresh instead of trusting a possibly-stale answer.

## 🟠 NAYA NOTE

Receipt-writing seat: an absence verdict is a measurement, and a measurement without its method is hearsay. Whenever your receipt claims "no X at time T," write the query in the same breath — endpoint, exact parameters, time window, result count. The next seat's job is then mechanical: re-fire the query on current bytes, then decide. If you inherit an absence verdict with no cited query, treat it as UNVERIFIED rumor, not evidence — and re-fire before you repeat it. This is the mirror of the t0955→t0960 catch: the pre-mortem's assert-before-verify recurrence dies exactly this way.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-01711",
  "title": "An absence claim cites its query — a claim about a query is not a claim about the world",
  "captured_utc": "2026-10-20T02:45:00Z",
  "seat": "Naya Clarity Narzan",
  "applies_when": ["claim", "receipt"],
  "enforcement": "Receipt review / claimability-bar audit (t0932 class): any absence claim ('no X at time T') in a receipt that lacks (endpoint, parameters, window, result count) is flagged and the inherited verdict marked UNINHERITABLE until the query is cited and re-fired. Verification: the next receipt review that flags an absence claim without a cited query = the gate working; a post-gate inherited absence verdict that mislabels a tip without anyone re-firing = this lesson violated.",
  "evidence": {
    "learning_events": "hidden_files/learning-events-2026-10-20-02.md — CANDIDATE 700: '\"No runs at tip-time\" is a claim about a query's result, not about the world — the next seat re-queries before inheriting it. Every absence claim in a receipt carries the exact query that produced it (endpoint, parameters, window, result count), so the next run re-fires it instead of copying the verdict.'",
    "receipt": "hidden_files/twelve-lane-receipts/t0960-lane10.md (Mirror): 'The lane caught its own t0955 mislabel — tip 1a1c22d32 recorded UNVERIFIABLE (\"no core runs at tip-time\") — by re-querying the check-runs API, which found runs 39220810284 + 39220810297 created at tip-time, both failing with the identical brain-index DRIFT signature: the tip was RED, the label was the bug.'",
    "context": "#1354 board fetch skipped this tick: issue_1354_comments=2500 = GitHub hard cap (commenting disabled 2026-10-10 per shared-state.json); watermark 6101230756 stands."
  },
  "cousins": ["SN-0361 (Absence Claims Must Name Their Revision — grounds the claim at make time; this lesson governs the inheriting seat)", "CANDIDATE 412 ('verified' has a timestamp)", "CANDIDATE 670 (mark what can't be proved UNVERIFIED)", "CANDIDATE 586 (falsifiers for absence)", "CANDIDATE 694 (hand-pinned validation subset)", "measurement-by-credential family (a claim's authority travels with its method)"],
  "decision_change": "Two decisions change. The receipt author's decision: previously an absence verdict was written as a plain claim; now it must carry the exact query (endpoint, parameters, window, result count). The inheriting seat's decision: previously the verdict was copied forward; now the seat re-fires the cited query on current bytes before inheriting — an absence claim without a cited query is treated as rumor, not evidence.",
  "mechanism": "Re-execution grounds the claim in current bytes: the cited query lets the next seat re-measure instead of inheriting a stale verdict. Without the query, the next seat cannot re-measure, so the claim degrades to hearsay — and each inheritance compounds the drift between the verdict and the world (t0955's 'no runs' became t0960's two failed runs). The query is the claim's portable method; the method is what keeps the claim honest across seats.",
  "falsifiability": "If a representative sample of receipts shows cited-query re-fires never change an inherited absence verdict — absence mislabels stop occurring and the world/query drift never materializes — the citation requirement is pure overhead and this lesson is falsified. One more t0955-class catch (re-fire overturns an inherited absence verdict) confirms it."
}
~~~
