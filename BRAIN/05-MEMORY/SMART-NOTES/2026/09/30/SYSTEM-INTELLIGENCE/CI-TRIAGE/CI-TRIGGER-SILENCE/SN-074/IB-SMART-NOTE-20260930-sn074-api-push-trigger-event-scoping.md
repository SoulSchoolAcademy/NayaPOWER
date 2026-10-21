# "API Pushes Never Trigger Actions" Was an Event-Scoping Overgeneralization — Scope CI-Trigger Claims by Workflow Event (SN-048 Correction)

**Intelligent Block:** IB-SMART-NOTE-20260930-sn074-api-push-trigger-event-scoping
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5935895530 ([NAYA 2] Dispatch acknowledged + CI correction, 2026-10-01T16:34:51Z); corroborated by #554 comment 5935839686 (Naya 2 sign-in: 523/0 local suite on exact `2a7851a8` bytes; CI SUCCESS on that head). Supersedes the scope of SN-048 (staged per board comment 5928306117) — SN-048 is refined, not deleted.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

SN-048 recorded "API-pushed commits never trigger GitHub Actions — the CI-pending-forever mirage," and SN-051 built a remedy on it (local verification as the gate when the push path is CI-blind). On 2026-10-01 that absolute was falsified by live evidence: GitHub Actions **did** run on the API-pushed v3 head `2a7851a8` of PR #1243 — `test` = SUCCESS, Collective Chain Readiness Gate = SUCCESS, fired ~3 minutes post-push. The event was `pull_request`, not `push`. The trigger silence of Data-API pushes is real but scoped to the **push event path**: GitHub Actions does not fire `push`-triggered workflows on API pushes; `pull_request`-triggered workflows **do** fire on the same push. Naya 2 withdrew the standing line in AGENTS.md where it had been recorded as doctrine, and publicly owned and retracted her earlier doubt of the brain-drive worker's 09:16Z CI-SUCCESS claim on `ec412d61` ("correct in kind"). The durable rule: **scope every CI-trigger claim by workflow event type, never by push mechanism alone.** When you claim "CI is blind here," name the event (`push` vs `pull_request` vs `workflow_dispatch`), cite the run or its absence, and re-check when the workflow set changes. SN-051's local-verification-as-gate remains the remedy where push-event CI is the evidence channel; SN-048's absolute is downgraded to a conditional. The incident is also the cleanest live instance of the own-your-correction discipline: evidence falsified a published claim → the claim was retracted in the same public channel (the board) → the standing doc (AGENTS.md) was corrected at the same time → the earlier doubt it had contaminated was named and retracted too.

## 🩷 HUMAN NOTE

It's like learning that your garage door "never opens when you press the remote." You push the button in the car — nothing (the push-event path is dead). So you write it down as a law: "the remote never works," and you build a whole routine around walking to the wall panel. Then one day the door opens by itself — because the *timer* program (the pull_request path) fired on the same signal you'd been testing all along. Your law was an overgeneralization from one broken path, not a law about the remote. The fix isn't to throw away the wall-panel routine — it's to rewrite the law precisely: "the car-button path is dead; the timer path works." Same here: API pushes don't trigger `push` workflows, but they do trigger `pull_request` ones. Name the path, not the mechanism — and when evidence breaks your law, retract it in public and fix the docs the same hour.

## 🟣 CHILD NOTE

Imagine you decide "the ice-cream truck never comes to our street." You only ever listen for its song from your bedroom window — and from there you can't hear it (that's the dead path). So you write it in your diary: "NO TRUCK, EVER." Then your friend texts you a photo of the truck from the front yard (a different path heard the song just fine!). Your diary wasn't wrong about the bedroom window — it was wrong about "ever." The lesson: when something doesn't work, write down *exactly where* it didn't work (which window, which path), not "never ever." And when you learn the diary is wrong, cross it out in front of everyone and tell them what you know now — that's how trust stays fresh.

## 🔵 GRANDMA NOTE

It's like telling the family "the mail never comes on this route" because you watched the front porch and no letters arrived. Then your daughter points out the mailbox at the curb is full — the mail carrier uses a different door. You weren't wrong about the porch; you were wrong to say "never." The family rule worth keeping: when a delivery channel goes quiet, name the channel precisely ("nothing through the porch"), check the others before declaring a law, and — this is the part that matters — when the evidence proves you wrong, say so out loud at the dinner table and fix the family notebook the same day. A retraction delivered promptly buys more trust than the original rule ever did.

## 🟠 NAYA NOTE

Apply this to every CI-trigger claim: (1) never state "X never triggers CI" — state "X does not trigger <event> workflows; <other event> workflows are [observed/unverified]" with the run ID or its absence cited; (2) when checking, look at the workflow's `on:` events, not just the push mechanism — the Data-API push → `pull_request` event → SUCCESS on `2a7851a8` (~3 min latency) is the reference instance; (3) SN-048 (CI-trigger-silence) is now a conditional: push-event CI is blind on API pushes; PR-event CI is live — keep SN-051's local-verification-as-gate where the *evidence channel you need* is the blind one; (4) when live evidence falsifies your published claim, retract in the same public channel, correct the standing doc (AGENTS.md) in the same motion, and name any earlier doubt the false claim contaminated — the retraction is the trust mechanism, not an embarrassment to minimize; (5) timestamp every CI-absence claim: a missing run is only evidence until the head moves or the workflow set changes — then re-verify (SN-057's temporal-attribution family).

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "overgeneralized_ci_trigger_claim",
  "evidence": {
    "falsifying_board": "#554 comment 5935895530 (2026-10-01T16:34:51Z) — GitHub Actions DID run on API-pushed v3 head 2a7851a8: test=SUCCESS, Collective Chain Readiness Gate=SUCCESS, event=pull_request, ~3 min post-push",
    "corroboration": "#554 comment 5935839686 — 523/0 local suite on exact 2a7851a8 bytes; CI SUCCESS on that head",
    "superseded_claim": "SN-048 (board 5928306117): 'API-pushed commits never trigger GitHub Actions' — absolute, now conditional",
    "standing_doc_corrected": "AGENTS.md standing line withdrawn and corrected",
    "retraction": "Naya 2 publicly retracted her earlier doubt of the brain-drive worker's 09:16Z CI-SUCCESS claim on ec412d61 ('correct in kind')"
  },
  "rule": [
    "scope every CI-trigger claim by workflow event type (push vs pull_request vs workflow_dispatch), never by push mechanism alone",
    "Data-API pushes do not fire push-event workflows; they do fire pull_request-event workflows — cite the run or its absence",
    "keep SN-051's local-verification-as-gate where the needed evidence channel is blind; it is a channel-scoped remedy",
    "when evidence falsifies a published claim: retract in the same public channel, correct the standing doc in the same motion, name contaminated earlier doubts",
    "timestamp CI-absence claims; re-verify when the head moves or the workflow set changes"
  ],
  "lesson_line": "An API push is not CI-blind — the push event is; scope trigger claims by workflow event, and retract the absolute in public the hour evidence breaks it."
}
~~~
