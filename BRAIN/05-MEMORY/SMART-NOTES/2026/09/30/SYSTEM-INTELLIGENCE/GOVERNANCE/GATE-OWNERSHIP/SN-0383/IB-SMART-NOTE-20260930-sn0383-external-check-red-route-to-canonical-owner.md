# External Checks RED Across Unrelated Commits Are the External App's Problem — Classify Ownership, Fail Closed, Route to the Canonical Owner

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0383-external-check-red-route-to-canonical-owner
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

On 2026-10-05 the Cloudflare `Workers Builds: maxresults` and `maxess-e01` checks failed repository-wide on recent main commits and blocked PR #1495. The Naya 3 lane classified before repairing: both checks are emitted by the external **Cloudflare Workers and Pages** GitHub App — neither worker name exists in NayaPOWER source or config, both fail identically on unrelated main commits, and neither is required by the active GitHub rulesets. Classification: `UNRESOLVED_COMPETING_EXTERNAL_RELEASE_LANE / FAIL-CLOSED` — a repository-wide Cloudflare project-association problem, not a PR code defect. The exact release-authority decision was routed to the canonical owner (issue #255): prove or repair each Worker as canonical, or disconnect/retire its NayaPOWER Git association. #1495 stayed HOLD. No check was spoofed, no code was patched to chase the red.

## 🩷 HUMAN NOTE

When the red light is on every dashboard including the ones you never touched, the machine isn't telling you about your work — it's telling you about its own wiring. Resist the urge to fix your code to make someone else's gauge stop flashing. The right move is a classification: is this mine, or is this the platform's? If it's the platform's, write that down plainly, hand it to the people who own the platform's wiring, and keep your change parked. Hold is a decision, not a delay.

## 🟣 CHILD NOTE

If every car on the street has a flat tire, the problem isn't your car — it's the road. Don't change your tire to fix the road. Tell the people who fix roads, and wait.

## 🔵 GRANDMA NOTE

When a problem shows up everywhere at once, it belongs to the thing that's everywhere — not to your one little piece. Name the real owner, hand it to them in writing, and don't touch what isn't yours to fix.

## 🟠 NAYA NOTE

My reflex when a PR is red is to look at my code first. The standing correction: read the red *horizontally* before reading it vertically. If the same check fails identically across recent unrelated main commits, and the check's emitter is an external GitHub App absent from repo source/config and not required by rulesets, stop: this is an external release-authority defect. Classify it, route the exact decision to the canonical owner, HOLD the merge, and never spoof a check to make green. The evidence law extends to gates: a gate you don't own produces no evidence about your code.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "rule": "classify_check_ownership_before_repairing_when_red_is_repository_wide",
  "signals": ["check_emitter_is_external_github_app", "check_name_absent_from_repo_source_and_config", "fails_identically_on_unrelated_main_commits", "not_required_by_active_rulesets"],
  "action": "classify_UNRESOLVED_COMPETING_EXTERNAL_RELEASE_LANE_fail_closed_route_exact_decision_to_canonical_owner_hold_merge_no_spoof",
  "evidence": "NayaPOWER#1354 comments 6000736256 (infra handoff), 6000831716 (Workers RED correctly classified, #1495 HOLD), 2026-10-05",
  "owner": "NayaPOWER#255 release-authority issue"
}
~~~
