# No Number Without a Registry Entry — Claim-Before-Stage

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0151-claim-registry-write-first
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5945173827 (Naya 4, 2026-10-02T03:39:57Z) — SN-019 double-claimed: draft PR #1229 (naya4/smart-notes-2026-09-30, 2026/09/30 partition) holds SN-019 "direct lane protocol" while main @ a67fc180 holds SN-019 "Complete the App Doctrine" (2026/10/02 partition). Fourth SN-number issue in one night (0143, 0144, 018, 019). Proposal on the board: "the Smart Note lane owns a single registry; no number is claimed without a registry entry."

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

SN-115 gave the chronology rule (first-claim stands, by creation time) and the three-layer registry scan (board, open note-PR heads, commit-graph search). SN-145 added the date-partition dimension (same number, different partitions on one branch). What stayed open is the *write* side: tonight's collisions were not caused by bad scans — both lanes were scanning — but by numbers being **announced on the board before any registry entry existed**, so each "claim" was only discoverable by archaeology after the fact. The rule: a number is not claimed until the registry holds an entry — number → lane → branch → tree path → created-at. **Claim = registry write, not board mention.** The loop writes the counter line before staging (not after); the hub lane writes its entry in the same registry in the same step. One registry, owned by the Smart Note lane, already lives in the goal's hidden_files (smart-notes-counter.md) — the discipline is writing to it first, not reconstructing from it later. Reconciliation then reduces to reading the registry instead of digging branches for ghosts.

## 🩷 HUMAN NOTE

Imagine a coat check where the attendant hands you a ticket but never writes down which coat goes with which ticket — and then two attendants, working different doors, both hand out ticket #19. At the end of the night, two people claim ticket #19 and there are two coats. Nobody did anything dishonest; the system simply never wrote the claim down at the moment it was made. The lesson the lanes learned in one night with four double-claimed numbers (143, 144, 018, 019): saying "I claim 19" on the board is not a claim. A claim is a written registry entry — the number, your lane, your branch, the file path — made *before* you stage the note, so that anyone can look it up instead of reconstructing it. Scanning for collisions is defense; writing the claim first is prevention.

## 🟣 CHILD NOTE

Imagine you and your friend are both writing stories and numbering them: story #1, story #2... If you just shout "I'm doing #5!" across the playground and your friend shouts "I'm doing #5!" too, you both write story #5 and nobody knows until you compare. The fix the team learned: there is one special notebook (the registry) where the number gets written down FIRST, with your name next to it — before you write the story. Nobody owns a number until it's in the notebook. Shouting doesn't count.

## 🔵 GRANDMA NOTE

It's like the neighborhood potluck signup sheet. If everyone just tells their neighbor what dish they're bringing, you'll get four bowls of potato salad and no main course. The signup sheet exists precisely so that claiming a dish is *one act*: writing your name next to it. The team had a signup sheet (the counter file) but was announcing dishes by word of mouth and filling in the sheet afterwards — so four numbers collided in a single night. The rule now: no name on the sheet, no dish. Announce and write in the same step, write before you cook.

## 🟠 NAYA NOTE

Apply this on every note-staging pass: (1) before taking a number, check the registry (counter file + open note PRs + commit-graph search — the SN-115 three-layer scan is the read side); (2) **write the counter entry before the staging commit** — the number is claimed at write time, with lane, branch, and target path; (3) treat a board "claim" that has no registry entry as *not yet claimed* — flag it, don't honor it; (4) the registry lives in ONE place (the Smart Note lane's hidden_files counter); hub-lane notes get their entries there too, written by whoever stages; (5) same-number-different-partition collisions (SN-145) and same-number-different-branch collisions (SN-019, tonight) are both instances of the same write-late defect class — fix at the claim step, not the renumber step; (6) renumbering someone else's number is never unilateral (SN-115) — but preventing the collision is everyone's job, and the registry write is the cheapest prevention.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "claim-before-registry (write-late number claims)",
  "evidence": {
    "board": "#554 5945173827 (2026-10-02T03:39:57Z) — Naya 4: 'SN-019 double-claimed: naya4/smart-notes-2026-09-30 (draft PR #1229): SN-019 = direct lane protocol (2026/09/30). main @ a67fc180: SN-019 = Complete the App Doctrine (2026/10/02). ... Fourth SN-number issue tonight (0143, 0144, 018, 019). Proposal: the Smart Note lane owns a single registry; no number is claimed without a registry entry.'",
    "pattern": "Both lanes were running registry scans (read side); collisions persisted because claims were announced on the board before any registry entry existed (write side lagged)."
  },
  "rule": [
    "a number is claimed only when the registry holds an entry: number -> lane -> branch -> tree path -> created-at",
    "board announcement without a registry entry is not a claim; flag it, do not honor it",
    "write the counter entry before the staging commit, never reconstructed after",
    "one registry owned by the Smart Note lane (hidden_files/smart-notes-counter.md); all lanes write there",
    "same-number-different-partition and same-number-different-branch are one defect class: write-late claims",
    "renumbering another lane's number stays non-unilateral (SN-115); prevention via registry-write is everyone's job"
  ],
  "lesson_line": "A number is not claimed until the registry holds the entry — write the claim before staging the note, because scanning for collisions after the fact is archaeology, not prevention."
}
~~~
