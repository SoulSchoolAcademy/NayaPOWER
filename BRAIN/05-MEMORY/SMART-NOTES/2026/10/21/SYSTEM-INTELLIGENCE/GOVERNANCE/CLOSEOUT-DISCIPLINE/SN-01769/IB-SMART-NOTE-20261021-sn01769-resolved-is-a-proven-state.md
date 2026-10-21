Intelligent Block: SN-01769
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-21
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

"Resolved" is a proven state, not an asserted one. The 2026-10-21 issue audit of all 32 open issues held RESOLVED at 0 — honestly — because every "fixed" claim found either left production-deployment proof outstanding or was absorbed into a superseded close. Issue #1102 is the canonical case: all five flagged SECURITY DEFINER functions were hardened in main and the Oct-6 advisor showed the consent-trigger hole gone, yet the issue stays REAL because the hardening's production deployment was never proven and the same pull found a new anon-executable trigger function. "Fixed" describes the code; "resolved" describes the world; they decouple at the production boundary. A "fixed" claim stays REAL until end-to-end closure evidence exists.

## 🩷 HUMAN NOTE

A doctor doesn't discharge a patient because the prescription was written — she discharges when the follow-up scan is clean. The audit found two real repairs (#1102's five hardened functions, #255's already-closed contamination blocker) and classified neither as RESOLVED: one because the fix was proven only in main, not in production; the other because its closure belonged inside a superseded close. Counting either as "resolved" would have moved a number on the scoreboard while leaving the actual hole unverified — the exact pattern Shawn's completion law forbids ("running and in use with receipts," not "fixed on paper"). Under the no-backlog law, a premature RESOLVED is backlog in disguise: it removes the issue from attention while the risk is still live.

## 🟣 CHILD NOTE

Your homework isn't done when you write the answers — it's done when the teacher checks them. Writing the fix is the homework; seeing it live in the real world is the teacher's checkmark. Don't put the star on your own paper.

## 🔵 GRANDMA NOTE

Don't count the harvest before it's in the barn. The seed packet promising tomatoes is not a tomato on the table. An issue is resolved when the world changed, not when someone said the work was done.

## 🟠 NAYA NOTE

Triage rule for every issue audit under the no-backlog law: an audit row classifies as RESOLVED only when its Proof/evidence cell shows end-to-end closure evidence — the fix in the code AND the proof in the world it runs in (production deployment, verified absence of the hole, no successor gap). A "fixed in main" row with production proof owed is REAL. A fixed claim carried inside a superseded close is DEAD/SUPERSEDED. The audit template's RESOLVED counter increments only on rows meeting the bar; the honest 0 from the 2026-10-21 audit is the reference example. Never inflate RESOLVED to make a report look better — the reopen rate is the falsifier.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "premature-resolved-inflation",
  "evidence": {
    "receipts": "hidden_files/issue-audit-2026-10-21.md (2026-10-21 ~09:20-09:35 PDT, all 32 open issues classified VENUE/RESOLVED/REAL/DEAD against live bytes): counts VENUE/STANDING 23, REAL 5, DEAD/SUPERSEDED 4, RESOLVED 0. #1102 REAL row: five flagged SECURITY DEFINER functions hardened in main (comment 5922030229), Oct-6 live advisor showed the consent-trigger hole GONE from production (comment 6021292338) — yet same pull found a NEW anon-executable trigger function (nayanet_execution_receipt_to_smart_ledger()) and production deployment of the hardening was still 'pending' at last report; no closure evidence since 2026-10-06. #1741 REAL row: pipeline never completed end-to-end (PR #2776 still open). Audit pass 2 explicitly held RESOLVED at 0 rather than inflating #1102 into it."
  },
  "decision_change": "Future issue triage under the no-backlog law classifies 'fixed' claims as REAL, not RESOLVED, until end-to-end closure evidence is shown; the RESOLVED counter is a proof-gated count, never a vibes count.",
  "falsifiability": "Track the reopen rate: if future audits count RESOLVED liberally and no counted issue ever reopens on missing production proof, the bar is stricter than needed and can be relaxed. If a prematurely-counted RESOLVED ever reopens (like #1102 would have), the rule paid for itself.",
  "mechanism": "Status words are accountability states. 'Fixed' describes the code artifact; 'resolved' describes the world the code runs in. They decouple at the production boundary (the completion law's 'running and in use with receipts' is the world side). Counting code-state as world-state deletes the issue's accountability while the risk is live.",
  "applies_when": ["issue", "triage", "no-backlog", "closeout"],
  "enforcement": "The issue-audit close pass: every audit-table row carries a Proof/evidence cell; the director tick rejects any RESOLVED increment on a row whose evidence lacks end-to-end closure proof (code fix + production proof + verified absence of the hole). The paste-ready close-reason column is the enforcement surface — a close reason without the closure evidence is bounced.",
  "coincidence_check": "cousins SN-1085 (never close what you cannot prove superseded — the byte-level close bar), SN-1166 (superseded means strictly-superior replacement), SN-1768 (retire-by-proof drain record). Distinct leg: binds the RESOLVED *status word* to end-to-end closure evidence under the no-backlog law — not supersession proof, not drain procedure."
}
~~~
