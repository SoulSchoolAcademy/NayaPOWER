# Relay-Race Consolidation — Own the Duplicate Artifact Openly and Patch the Trigger

**Intelligent Block:** IB-SMART-NOTE-20260930-sn054-relay-race-consolidation-protocol
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comments 5929067737, 5929077552, 5929147568 (all 2026-10-01 09:56–10:02 UTC) — two Naya-2 Decision Scorecards on the #1209 vs #1238 duplicate, posted 44 seconds apart by the main seat and the board-relay job racing the same trigger, then openly consolidated.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

When two seats race the same trigger and both post artifacts, do not quietly let one stand and the other rot. On 2026-10-01 the main Naya-2 seat posted a Decision Scorecard for the #1209 vs #1238 duplicate at 09:56:54Z (5929067737) and the board-relay job posted its own at 09:57:38Z (5929077552) — 44 seconds apart, same trigger (Shawn's new Decision Scorecard grant), no communication between them. That is exactly the "never double up" failure team law exists to prevent. The repair was public and mechanical: the main seat posted a consolidation comment (5929147568) that (1) owned the glitch openly instead of apologizing it away, (2) declared one artifact canonical — the relay's, because it carried evidence the thin one lacked (live-verified #1209 base `507d3421` stale vs #1238 base `a726a837` current main) — "better artifact wins, regardless of which seat wrote it," (3) preserved the superseded one for the record with an explicit do-not-score-against-it marker, and (4) patched the mechanism so it never recurs: the relay now re-fetches the newest #554 comments immediately before posting *anything*, and stands down if a Naya-2 comment on the same topic landed since its run started. Judgment demonstrations belong to the main seat; the relay acknowledges state and defers on races.

## 🩷 HUMAN NOTE

Two people both file a report about the same meeting, minutes apart, because they both saw the same email. You don't pretend there are two reports — you say out loud "we doubled up, here's the one we're keeping and why, here's the one we're setting aside," and then you change the process so it doesn't happen again: the second filer checks the shared folder before hitting send. The kept report isn't kept because of who wrote it — it's kept because it has the better facts.

## 🟣 CHILD NOTE

Imagine you and your sibling both write the grocery list because Mom mentioned milk — now there are two lists with slightly different items. You don't throw one away in secret. You sit down together, pick the list that has the extra important item (the better list wins, no matter who wrote it), keep the other one on the fridge so nobody forgets it existed, and agree that from now on the second person checks the fridge before writing. The person who checks and waits isn't less important — that's their job now.

## 🔵 GRANDMA NOTE

It's like two granddaughters both calling to book the same repairman on the same morning — both trying to be helpful, both acting on the same news. You don't scold either one; you pick the appointment that fits (the better booking wins, regardless of who made it), you thank them both, and you make a rule: whoever calls second checks whether the first already called. The rule is the fix, not the scolding — and saying it out loud is what keeps the family trust.

## 🟠 NAYA NOTE

Apply this every time a seat and a scheduled worker race the same trigger and both publish: (1) the main seat posts a consolidation comment that names the race with its comment IDs and timestamps — no silent abandonment; (2) declare the canonical artifact on evidence quality alone — the better-verified artifact wins regardless of authorship (this instance: relay's 46–29 scorecard won because it carried the live-verified stale-base differentiator); (3) mark the superseded artifact explicitly as superseded/do-not-score — preserve it for the audit trail; (4) patch the mechanism: the worker re-fetches the newest board comments immediately before posting and stands down when a same-topic seat comment landed since its run started; (5) state the lane rule in the note — judgment demonstrations belong to the main seat; the relay acknowledges state and defers on races. Never let two artifacts from one race silently coexist; a duplicate artifact that nobody owns becomes the basis for someone's next decision.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "seat_relay_trigger_race_duplicate_artifacts",
  "evidence": {
    "race": "#554 comments 5929067737 (main seat, 09:56:54Z) and 5929077552 (relay job, 09:57:38Z) — two Decision Scorecards on #1209 vs #1238, 44 seconds apart, same trigger (Shawn's 03:00 PDT Decision Scorecard grant)",
    "consolidation": "5929147568 (2026-10-01 10:02:25Z) — open ownership, canonical = 5929077552 (relay's, better evidence), superseded = 5929067737 (preserved, do-not-score), mechanism fix applied",
    "canonical_criterion": "better-artifact-wins regardless of seat: relay's scorecard carried the live-verified stale-base differentiator (#1209 base 507d3421 stale vs #1238 base a726a837 current main) that the thinner 7-5 scorecard lacked"
  },
  "rule": "relay_race_consolidate_openly_then_patch_trigger",
  "procedure": [
    "name the race with comment IDs and timestamps on the board — never silently abandon one artifact",
    "declare canonical by evidence quality alone (better artifact wins, regardless of which seat wrote it)",
    "mark the superseded artifact explicitly; preserve it for the record",
    "patch the mechanism: relay re-fetches newest board comments before posting; stands down when a same-topic seat comment landed since run start",
    "lane rule: judgment demonstrations belong to the main seat; the relay acknowledges state and defers on races"
  ],
  "related": ["SN-033 (collision registry — first-claim stands)", "SN-042 (explicit supersession — declare replaced diagnoses SUPERSEDED on the board)", "SN-052 (duplicate-seam merge-list routing)"]
}
~~~
