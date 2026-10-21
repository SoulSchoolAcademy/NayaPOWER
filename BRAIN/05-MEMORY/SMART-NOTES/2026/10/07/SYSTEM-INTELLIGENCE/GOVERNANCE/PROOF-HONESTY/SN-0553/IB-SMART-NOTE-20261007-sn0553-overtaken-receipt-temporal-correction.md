# The Overtaken Receipt — When the Tip Outruns Your Receipt, Publish a Temporal Correction

**Intelligent Block:** IB-SMART-NOTE-20261007-sn0553-overtaken-receipt-temporal-correction
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-07
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A receipt written before re-resolution is a claim about the future. If the tip moves and the action is already done by another hand before you execute, never let the stale receipt stand — publish a temporal correction that reclassifies it as a post-hoc record, explicitly disclaims authorship of the completed action, and names what the record actually shows. GitHub recording a merge under an account does not establish which interaction caused it.

## 🩷 HUMAN NOTE

Imagine writing a permission slip saying "I authorize this door to be opened," then walking over and finding the door already open and someone else's hand on the knob. You don't file the permission slip as if you opened the door. You tear it up, write "the door was already open," and give the credit where it's actually due. That's what happened here: a scorecard receipt said "MERGE PR #1746 by squash" as if it were a pre-merge authorization, but when the seat re-resolved at action time, main had already moved and #1746 had already merged. The seat published a correction saying so, refused to take credit, and treated its own earlier receipt as a historical record — not an authorization. That honesty is the whole lesson.

## 🟣 CHILD NOTE

If you wrote on a note "I'm going to open the door!" but your sister already opened it, you don't pretend you opened it. You write a new note: "The door was already open. My note was too late. I didn't do it."

## 🔵 GRANDMA NOTE

If you left a note on the fridge saying you'll do the dishes, and you come home and your neighbor already did them, you cross out your note and write "already done — not me." You never take credit for dishes you didn't wash, and you never leave the old note lying around to confuse everyone.

## 🟠 NAYA NOTE

SN-0493 says a decision expires when the tip moves — re-verify at action time. This is the other half of that law: the case where you fail to catch it in time and your pre-action receipt lands AFTER the action is already done. The prescription: (1) quote or cite your prior receipt; (2) state the live resolution with exact evidence — new main SHA, merge timestamp, which account GitHub records; (3) explicitly disclaim: "I do not claim this seat performed or authorized that already-completed action"; (4) reclassify the receipt as a post-hoc scorecard record. Never silently leave a pre-action receipt standing when the action preceded it — in a multi-seat system with a human director who can act at any moment, an uncorrected stale receipt reads as a false authorship claim. This is the same honesty that closes every receipts-dispute in one turn: evidence about what actually happened replaces a claim about what was going to happen.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "hard_boundaries": [
    "DO_NO_HARM",
    "CAPABILITY_DOES_NOT_CREATE_AUTHORITY",
    "RETRIEVAL_DOES_NOT_CREATE_AUTHORITY",
    "LEARNING_DOES_NOT_CREATE_AUTHORITY",
    "PRIVATE_BY_DEFAULT_SHARED_BY_CHOICE_COLLECTIVE_BY_CONSENT_PUBLIC_BY_DECISION"
  ],
  "law": "OVERTAKEN_RECEIPT_TEMPORAL_CORRECTION",
  "rule": "A pre-action receipt overtaken by a moved tip must be corrected in the open: quote it, state the live resolution (SHA, time, recorded account), disclaim authorship of the completed action, and reclassify it as a post-hoc record. Never let a stale receipt stand as authorization.",
  "evidence": [
    "#1354 comment 6042809521 (pre-merge scorecard receipt for PR #1746, written 2026-10-07T17:06:56Z)",
    "#1354 comment 6042860627 (temporal correction: #1746 already merged 2026-10-07T17:06:40Z at main 7aabf0d4120b65503cd8bec032120f91e0bc47b4; authorship disclaimed)"
  ],
  "raw_source_separate_from_distillation": true,
  "refines": ["SN-0493"],
  "proof_frontier": "Mechanical gate: refuse to post a receipt containing an authorization verb (MERGE/DEPLOY/AUTHORIZE) unless the tip was re-resolved inside the same action window."
}
~~~

## 🟢 LEARNING LESSON

The failure to prevent: letting a pre-action receipt stand uncorrected after the action was completed by someone else — which in a multi-seat system reads as a false authorship claim. A cold successor must know that receipts are temporal: they describe intent at time T and must be re-anchored or retracted when T moves.

## 🟡 WHAT IT MEANS

Receipts are not monuments. When the tip moves under a receipt, the honest move is fast: correct it, disclaim it, reclassify it. The correction costs one comment and buys permanent provenance integrity.

## ⚪ WHAT'S IN IT FOR YOU

No false authorship claims, no provenance disputes, no "who actually merged this" arguments. The record always says exactly what happened, and who is and isn't claiming it.

## 🟨 HOW TO APPLY / HOW TO USE

Apply whenever you write a pre-action receipt (scorecard, authorization, merge decision): re-resolve the tip in the same breath as execution; if the action already completed, skip execution and publish the temporal correction instead. Never execute an overtaken decision "to be useful."

## 🔗 HOW IT CONNECTS

- **REFINES** → SN-0493 — A Decision Expires When the Tip Moves (receipt-layer corollary)
- **APPLIES_TO** → Scorecard Law merge protocol (pre-merge receipts)
- **APPLIES_TO** → SN-0351 — sign-in/out discipline

## 🧭 KEY DECISIONS / PRINCIPLES

- A receipt is a claim about time T; if the tip moved, the receipt's authority is void until re-resolved.
- An account name on a GitHub merge record is not evidence of which interaction caused it.
- The correction is part of the receipt, not an apology for it — publish it where the receipt landed.
