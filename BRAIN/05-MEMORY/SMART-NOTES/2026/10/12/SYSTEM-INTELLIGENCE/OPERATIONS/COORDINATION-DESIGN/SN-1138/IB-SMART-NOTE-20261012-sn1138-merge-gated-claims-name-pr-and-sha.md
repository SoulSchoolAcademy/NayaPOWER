# A Merge Landed Is Not MY Merge Landed — Merge-Gated Claims Name the PR Number + Head SHA They Gate On

**Intelligent Block:** IB-SMART-NOTE-20261012-sn1138-merge-gated-claims-name-pr-and-sha
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** [LEARNING EVENT · DISTILLATION V2] #2175 comment 6135839165 (2026-10-13 ~01:05Z) — L271 (F1, team): verify's 00:28 handoff announced the B-30 post-merge check as due after a merge event; the landed merge was #2459 (the revert), not #2492 (the B-30 repair, still OPEN). Wire caught it at 00:31; verify owned the correction at 00:39 — no churn, but the false trigger fired. Promoted to standing law this run (AGENTS.md). Win patterns WP-18/WP-19 same window (F2) — name the RED, close the RED with evidence — same family: identity before inference.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A merge event is not one thing — it is one specific PR, at one specific head SHA, carrying one specific content delta. Verify's 00:28 handoff heard "a merge landed" and announced the B-30 post-merge check as due. But the merge that landed was #2459 — the revert of #2455 — not #2492, the B-30 repair, which was still OPEN. The check fired on the wrong identity. Wire caught it three minutes later, verify owned the correction, and no repair was wasted — but the false trigger proves the hazard: acting on "a merge landed" without naming WHICH merge is how a post-merge check certifies the wrong delta, or how a repair lane re-verifies a tip that never contained its fix. The durable rule: **a merge-gated claim names the PR number + head SHA it gates on — prove the identity, not just the event.** A handoff that says "post-merge check due after #2459 @ dd6f2d92" cannot misfire on #2492's merge tomorrow.

## 🩷 HUMAN NOTE

Shawn — one quiet near-miss tonight worth keeping as law. A lane announced a post-merge check was due because "a merge landed" — but the merge that landed was the revert (#2459), not the repair the check was waiting for (#2492, still open). The team caught it in eleven minutes and nothing was wasted, but the pattern is the dangerous one: merge events are cheap to announce and expensive to misattribute. The rule on the wall now: nobody acts on "a merge landed" — they act on "PR #NNNN @ head SHA", named in the claim itself. Prove the identity of the event, not just that an event happened.

## 🟣 CHILD NOTE

Imagine you're waiting for YOUR package to arrive, and the doorbell rings. You open the door and sign for it — but it was the neighbor's package. The doorbell rang, but you never checked the name on the box. That's what happened here: a merge rang the doorbell, and the check ran — but it was the wrong merge's doorbell. The fix is simple: always read the name on the box. Every merge-gated claim must say exactly WHICH merge (its number and its fingerprint) before anyone acts on it.

## 👵 GRANDMA NOTE

It's like a hospital paging "surgery done, patient can go home" — but you have to ask WHICH patient. If the nurse means the patient in room 2459 and you send home the patient in room 2492, someone gets hurt. A page that just says "surgery done" is an announcement; a page that says "patient in room 2459, surgery done" is an instruction you can act on. Every merge-gated claim must name the patient — the PR number and the exact commit fingerprint — so no one acts on the wrong one's good news.

## 🤖 NAYA NOTE

Merge events are identities, not vibes. In a merge-dense window — revert PRs, re-stamps, repair PRs landing minutes apart — "a merge landed" is an announcement with zero actionable content; the same event string can gate five different checks for five different PRs. The discipline: the claim carries its own identity — PR number + head SHA — before any downstream action fires. "Post-merge check due: #2459 @ dd6f2d92 (revert of #2455)" cannot be misattributed to #2492; "a merge landed" can. Verify's 00:28→00:39 sequence is the proof that the detection path works (wire caught it, verify owned it, no churn) — and also the proof that the false trigger is real. Cost of the rule: one line in every merge-gated claim. Cost of skipping it: certifying the wrong delta, re-verifying the wrong tip, and silent confidence in a check that never ran against its subject. Cousin: SN-1059 (gates authorize the act, not the artifacts) — identity first, inference second.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-1138",
  "lesson": "merge-gated-claims-name-pr-and-sha",
  "rule": "A merge-gated claim names the PR number + head SHA it gates on; prove the identity of the merge event, not just that an event occurred, before any downstream check fires.",
  "failure_class": "merge-event misattribution",
  "evidence": {
    "learning_event": "#2175 comment 6135839165 (2026-10-13 ~01:05Z): L271 (F1, team) — verify's 00:28 handoff announced B-30 post-merge check due after a merge event; landed merge was #2459 (revert), not #2492 (B-30 repair, still OPEN)",
    "correction": "wire caught it 00:31; verify owned the correction 00:39 — no churn, but the false trigger fired",
    "standing_law": "promoted to AGENTS.md as standing law this run"
  },
  "repair_doctrine": "Every merge-gated claim carries 'PR #NNNN @ <head-sha> (<what it is>)' in the claim itself; a claim without the identity is an announcement, not a trigger",
  "related": ["SN-1059", "SN-1137"]
}
```
