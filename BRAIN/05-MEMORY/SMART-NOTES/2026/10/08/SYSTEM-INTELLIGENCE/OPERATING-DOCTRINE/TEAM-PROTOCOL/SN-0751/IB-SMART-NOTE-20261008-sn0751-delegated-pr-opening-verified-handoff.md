# Delegated PR Opening Is a Verified Handoff — SHA-Match Before You Open

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0751-delegated-pr-opening-verified-handoff
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6073843122 (Naya 5, 2026-10-09T03:45:44Z, PAT 403 on PR ops, asks Naya 4 to open); #1354 comment 6073904532 (Naya 5 human-value branch, asks Naya 4 to open PR); #1354 comment 6073928780 (Naya 5 voice branch, asks Naya 4 to open PR); #1354 comment 6073963827 (Naya 4, 2026-10-09T03:58:00Z, verified all five branch SHAs match her #1354 claims, opened #1937/#1938/#1939/#1940); #1354 comment 6074100435 (Naya 2 relay: all four heads byte-match, merges stay scorecard-gated).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

On 2026-10-08/09 Naya 5 pushed five working branches across four lanes (eng-gates CI fix, truth-guard liveness, human-value events, voice-block why-lines, plus convergence-D already on PR #1882) but her PAT 403s on PR operations — she cannot open PRs or merge herself. The standing convention held: she posted each branch's exact head SHA on #1354 and asked Naya 4 to open the PRs. What Naya 4 did next is the lesson: she **verified all five branch SHAs match her #1354 claims first, then opened** #1937, #1938, #1939, and #1940. She opened zero merges — "scorecard receipts required per the Scorecard Law" — and noted PR #1882 still needs one other seat's independent validation, routing that ask to the Learning lane (#1865) instead of absorbing it.

The protocol, written for a cold successor:

1. **The blocked seat posts the evidence, not just the ask.** Branch name, exact head SHA, tree-verified statement, what the branch does, what remains gated (Naya 5's pattern: "I will not self-merge without the required independent validation + no-objection window").
2. **The opening seat verifies before opening.** Resolve each named branch's head on the remote and byte-compare against the claimed SHA. A mismatch means the claim and the branch diverged — stop and report, never open on a stale claim. Naya 2's relay then re-verified the set independently.
3. **Open is not merge.** PR-opening carries zero merge authority. Merges stay under the Scorecard Law: written scorecard receipt, independent validation, no-objection window.

Opening a PR for another seat is not a favor — it is a verified handoff. The SHA check is what makes it trustworthy: without it, the opener is rubber-stamping a claim they never checked.

## 🩷 HUMAN NOTE

Shawn, Naya 5's permissions can't open pull requests, so she pushes her branches and posts the exact commit IDs on the board, asking Naya 4 to open the PRs. The lesson: Naya 4 doesn't just open them — she checks each branch's commit ID matches what Naya 5 claimed before opening, and opening is still not merging — merges wait for the written scorecards. It's a verified handoff, not a favor.

## 🟣 CHILD NOTE

Think of it like a relay race where one runner can't put the baton in the box herself. She hands the baton to a teammate with a note saying exactly which baton it is. The teammate doesn't just drop it in the box — she first checks the note matches the baton in her hand. If it doesn't match, something went wrong and she stops. And putting the baton in the box is not finishing the race — the race still needs the judges' scorecards. Match the note to the baton. Then, and only then, put it in the box.

## 👵 GRANDMA NOTE

Grandma, one of the team members can't open the official request forms herself, so she posts her work and says exactly which version it is, and asks a teammate to file the forms. The teammate doesn't file blindly — she checks the version number matches what was claimed, every single time. And filing the form is not the same as approving the work — that still needs the written scorecards. The rule: check the number against the claim, file the form, and never confuse filing with approving.

## 🟣 NAYA NOTE

This is the delegation companion to SN-0749 (relay = evidence, not authority): a delegated PR opening is an evidence-checked handoff, not an authority transfer and not a courtesy. The three-step form — claim (branch + exact SHA + gates remaining), verify (remote head == claimed SHA), open (no merge) — should be the template any seat uses when filing for another. It also degrades safely: if the SHA mismatches, the opener stops with a report instead of filing a PR for bytes nobody verified. Pair with the no-self-merge discipline the blocked seat posted: blocked on PR ops does not relax independent-validation or no-objection requirements; it routes them through another seat.

## ⚙️ MACHINE NOTE

```json
{
  "id": "SN-0751",
  "slug": "delegated-pr-opening-verified-handoff",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/OPERATING-DOCTRINE/TEAM-PROTOCOL",
  "evidence": [
    {"type": "board_comment", "ref": "SoulSchoolAcademy/NayaPOWER#1354 comment 6073843122"},
    {"type": "board_comment", "ref": "SoulSchoolAcademy/NayaPOWER#1354 comment 6073963827"},
    {"type": "board_comment", "ref": "SoulSchoolAcademy/NayaPOWER#1354 comment 6074100435"},
    {"type": "pull_request", "ref": "SoulSchoolAcademy/NayaPOWER#1937"},
    {"type": "pull_request", "ref": "SoulSchoolAcademy/NayaPOWER#1938"},
    {"type": "pull_request", "ref": "SoulSchoolAcademy/NayaPOWER#1939"},
    {"type": "pull_request", "ref": "SoulSchoolAcademy/NayaPOWER#1940"}
  ],
  "lesson": "When a seat cannot open PRs, another seat opens them — but opening is a verification act: byte-compare each branch head SHA against the claiming seat's board post before opening, and open carries zero merge authority. Merges stay scorecard-gated.",
  "cold_successor_rule": "When asked to open a PR for another seat's branch: resolve the branch head on the remote, compare byte-for-byte with their posted SHA, open only on match, and never merge — route the merge through the Scorecard Law protocol. A mismatch is a stop-and-report, not a file-anyway."
}
```
