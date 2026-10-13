# A Relay Hands Evidence, Never a Merge: Verification Authority Ends Where the Merge Decision Starts

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0749-relay-evidence-not-authority
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6073479189 (Naya 2 [RELAY] to Naya 4, SELF-driver completion, 2026-10-08 20:11 PDT) — full exact-tip verification of PR #1933 (open, non-draft, head `naya4/self-identity-trial-v2` @ `8faac0c5`, base == exact live main tip `504378c4`, additive 3 files/0 deleted, mergeable: true) with one open gate: "CI still concluding — mergeable_state `unstable`; merge stays the protocol's call, not this relay's."

## ✦ IN A NUTSHELL

Naya 2's relay on the SELF driver was textbook: exact-tip parent confirmed against live main, additive-only verified, mergeability checked — and then the relay stopped exactly where it must stop. It did not say "merge it." It said the remaining gate (CI concluding, mergeable_state unstable) and named the merge decision's true owner: the protocol, the merging seat, not the relaying seat.

A relay is an evidence handoff, not an authority transfer. The verifying seat reports what was checked, what the evidence says, and which gates remain open — then ends. The receiving seat (or the Scorecard Law protocol it runs) owns the merge decision. Merging by relay — reading a verifier's green as an implied "go" — collapses two independent roles into one and silently breaks the receipt chain: the scorecard would name the merger while the judgment was the relayer's. The discipline is explicit: end every relay with "here's the evidence, here's what's still open, here's whose call it is." This is the cross-seat twin of "never duplicate another lane" — you also never decide for another lane.

## 🩷 HUMAN NOTE

Shawn — a small discipline note from tonight's SELF relay. Naya 2 verified Naya 4's SELF work down to the exact commit, then deliberately did NOT merge it, saying plainly: "the merge stays the protocol's call, not this relay's." That's the rule we're locking in: whoever verifies hands over the evidence and stops; the receiving seat makes the merge call. Nobody merges by implication, and nobody's judgment gets silently spent by somebody else's signature.

## 🟣 CHILD NOTE

Imagine your friend checks your homework and says, "I looked at every answer — they all look right, and your teacher hasn't finished grading yet." That's helpful! But your friend doesn't turn in your homework for you — that's YOUR decision, because you're the one in the class. A "relay" works the same way: one teammate checks the work carefully, then hands it back with a note saying what they found and what's still waiting. The decision to finish belongs to the person who owns the job, not the person who checked it.

## 👵 GRANDMA NOTE

Grandma, think of it like this: your neighbor tastes your soup and says, "The seasoning is perfect, but it's still on the stove — it needs ten more minutes." She doesn't serve it herself — that's your kitchen, your call. She gave you the facts: it's seasoned well, and it's not done yet. The lesson: the person who checks hands you the facts and stops. The person who owns the pot decides when to serve. If checkers start serving, nobody knows whose judgment the meal was.

## 🟣 NAYA NOTE

The relay is the team's narrowest contract: evidence in, authority out. Naya 2's relay form — evidence, then the explicit boundary sentence "merge stays the protocol's call, not this relay's" — should be the template. Any relay that omits the boundary sentence is incomplete, because silence lets the receiver mistake a verification for permission. A verifier's green is a fact about the past; a merge is a decision about the future, and decisions belong to the owner of the future state — the receiving seat running its scorecard.

## ⚙️ MACHINE NOTE

```json
{
  "id": "SN-0749",
  "slug": "relay-evidence-not-authority",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/OPERATING-DOCTRINE/TEAM-PROTOCOL",
  "evidence": [
    {"type": "board_comment", "ref": "SoulSchoolAcademy/NayaPOWER#1354 comment 6073479189"},
    {"type": "pull_request", "ref": "SoulSchoolAcademy/NayaPOWER#1933"}
  ],
  "lesson": "A relay is an evidence handoff, not an authority transfer. The verifying seat reports evidence and names remaining gates, then stops; the merge decision stays with the protocol/merging seat. End every relay with an explicit boundary sentence.",
  "cold_successor_rule": "When you relay verification to another seat: list evidence, list open gates, and write one boundary sentence naming whose call the merge is. Never let a green verification be read as a merge instruction."
}
```
