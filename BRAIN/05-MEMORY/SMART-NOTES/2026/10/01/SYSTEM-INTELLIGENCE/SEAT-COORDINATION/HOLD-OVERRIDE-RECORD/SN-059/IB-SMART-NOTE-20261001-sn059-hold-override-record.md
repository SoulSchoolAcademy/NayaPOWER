# Record the Override, Don't Just Obey It — Hold-Override Transparency

**Intelligent Block:** IB-SMART-NOTE-20261001-sn059-hold-override-record
**Smart Note:** SN-059
**Truth state:** CANDIDATE
**Scope:** PRIVATE canonical runtime object; this file is a PUBLIC DERIVED VIEW authorized by the human director.
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This Markdown file is **not** a second source of truth.

## ✦ IN A NUTSHELL

A seat's standing hold is a board-visible commitment. When a higher authority lifts it, the seat does not quietly stop holding — it records the override on the board: which hold, which order lifted it, and where the deferred obligation now lives. Naya 4's torch committed to holding Demo-1 move 2 until Coda 2 verified `43d5d6e4`; the dispatch order lifted that hold; she recorded the override in her dispatch-received comment rather than silently breaking the commitment, and routed Coda 2/3's verification to run in parallel. The board now shows hold → override → completion as one unbroken chain.

## HUMAN NOTE

Think of a hold as a promise you wrote on the whiteboard: "I won't start until the inspector signs off." Then the director walks in and says, "Start now — the inspection runs alongside." You don't just erase the promise and start. You write under it: "Director overrode the hold at 09:32; inspection now runs in parallel." That one line is the difference between a team that looks like it breaks promises and a team that visibly tracks authority. Anyone reading the board later sees the full chain instead of a mystery.

The protocol:

1. **Holds are stated publicly with their release condition.** "Holding move 2 until Coda 2's verification of `43d5d6e4` lands." If the hold were never written down, nobody could later tell whether it was overridden or forgotten.
2. **An override cites the authority that lifted it.** Naya 4 named the source order (director dispatch, 09:32 PDT) rather than writing "hold lifted." A future auditor needs the *why*, not just the *that*.
3. **The deferred obligation is explicitly kept alive.** Coda 2/3's verification didn't disappear — it was re-routed to parallel. The override comment says where it went, so no one files it as abandoned and no one blocks on it by accident.
4. **The relay notes the lineage.** When the relay sees hold → override → completion, it records the three links together so a later reader doesn't have to reconstruct them from scattered comments.

## CHILD NOTE

If you promised your friend "I'll wait for you before we go," and your mom says "go now, your friend will catch up," you tell your friend what happened instead of just leaving. That way nobody thinks you broke your promise — they know the plan changed and who changed it.

## GRANDMA NOTE

It's like a store sign that says "Closed until the health inspector comes." If the owner is told to open anyway with the inspector coming alongside, the honest move is a new sign: "Open by owner's order — inspector visit continues alongside." You don't just take the old sign down and pretend it was never there.

## NAYA NOTE

This is the authority counterpart to SN-058's SHA-staleness rule: SN-058 tracks how *versions* drift on the board; SN-059 tracks how *commitments* move. Both exist because the board is a cache of state that changes in minutes. A hold that silently vanishes is indistinguishable from a broken commitment — and in a team where every seat runs the same decision process, apparent broken commitments are poison for coordination trust. Extends SN-017 (seat coordination) and SN-057 (handoff protocol): the handoff of an obligation from "blocking" to "parallel" is itself a handoff, so it gets the same public receipt treatment.

## 🟢 MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "raw_source_separate_from_distillation": true,
  "automatic_truth_ceiling": "CANDIDATE",
  "authority_inheritance": false,
  "knowledge_creates_authority": false,
  "protocol": "hold_override_record",
  "moves": [
    "state the hold publicly with its release condition before any override can occur",
    "on override: name the hold, the authority that lifted it, and the order reference",
    "re-route the deferred obligation explicitly (parallel, reassigned, or cancelled-by-authority) — never let it go implicit",
    "relay records hold -> override -> completion as a linked lineage"
  ],
  "override_receipt_fields": ["hold_id", "original_release_condition", "override_authority", "order_reference", "deferred_obligation_new_state"],
  "applies_to": ["seat_standing_holds", "director_dispatches", "verification_gates"],
  "silently_breaking_a_hold": "FORBIDDEN"
}
~~~

## 🟢 LEARNING LESSON

A broken hold and a lifted hold look identical if nobody writes the override down. In a fast team, unrecorded overrides read as untrustworthy seats; recorded overrides read as disciplined authority-following. The writing costs one sentence and buys the whole team's trust model.

## 🟡 WHAT IT MEANS

The hold mechanism (a seat refusing to move until a gate clears) only survives if overrides are cheaper to make than silent. Naya 4's one-line hold-override record in 5935875734 is the template: it named the torch-held condition, cited the dispatching authority, and re-routed the awaited verification to parallel — three links, no ambiguity. The alternative (just building move 2 with no note) would have left Coda 2 wondering whether her verification gate was ignored, and future readers wondering whether the hold ever mattered. Under the 24-hour push this pattern will recur; make the record the habit.

## ⚪ WHAT'S IN IT FOR YOU

No phantom broken promises on the board, no verification gates silently dropped, and overrides that future-you can audit without asking the seat "why did you start without the inspection."

## 🟨 HOW TO APPLY / HOW TO USE

- When you state a hold: write the hold + its exact release condition in your comment (not just "holding").
- When your hold is overridden by higher authority: reply/record in the same thread — "hold X overridden by <authority> <order reference>; deferred obligation Y now <parallel/reassigned/cancelled>."
- When you are the relay: link the three comments (hold, override, completion) in your per-run notes; flag any hold that vanishes without an override record.
- Never delete or silently edit away a hold statement after overriding it — the visible override is the point.

## 🔗 HOW IT CONNECTS

- **SUPPORTS** → NayaPOWER North Star: evidence-backed verification instead of activity theater
- **REQUIRES** → Team Naya Issue #554 durable coordination and handoff
- **USES** → SN-017 (seat coordination protocol), SN-057 (cross-seat handoff protocol)
- **GOVERNS** → seat-held gates and authority overrides during the 24-hour push
- **ENABLES** → auditable commitment lineage: hold → override → completion
- **PAIR** → SN-058 (board-as-cache staleness): SN-058 tracks drifting versions; SN-059 tracks moving commitments

## 🧭 KEY DECISIONS / PRINCIPLES

- A hold is a public commitment; an override is a public event. Neither may go implicit.
- Cite the authority that lifted the hold, by name and order reference — "hold lifted" alone is not a receipt.
- The deferred obligation is never dropped; it is re-routed, and the new route is stated.
- The relay records lineage; it does not adjudicate whether the override was correct.

## 🧾 PROOF / PROVENANCE

~~~json
{
  "event_id": "b4e7f2a1-9c5d-4e8f-a1b3-7d6e5f4a3c2b",
  "intelligent_block_id": "IB-SMART-NOTE-20261001-sn059-hold-override-record",
  "lineage_id": "e8f2a4b6-3d7c-4a9e-b5f1-9c8d7e6b4a2f",
  "relationship_id": "f1a3b5c7-4d8e-4f9a-c6b2-ad9e8f7c5b3d",
  "runtime_index_id": "a9c8e7f6-5b4d-4a9e-b8c7-6d5f4e3a2b1c",
  "receipt_id": "d2e4f6a8-1b3c-4d9e-a7f5-8c9d0e1f2a3b",
  "independent_verification": false,
  "truth_state": "CANDIDATE"
}
~~~

**Receipts (all live-read 2026-10-01 ~09:33–09:45 PDT):**
- Hold stated: Naya 4's torch on PR #1216 committed to holding Demo-1 move 2 until Coda 2's verification of `43d5d6e4` landed (referenced in 5935875734, 16:33:43Z).
- Override order: #554 dispatch 5935855302 (16:32:38Z, control tower, director-scoped Demo-1 + durable reread) — Naya 4's dispatch-received comment 5935875734 records it as "Shawn 2026-10-01 09:32 PDT" director order lifting the hold; she wrote "recording the override here rather than silently breaking the commitment. Coda 2/3's verification preparation runs in parallel as dispatched."
- Completion: 5935943178 (16:37:34Z) — move 2 done, `bf63549c` (feat: real LAW authorization on the executable path), with the verification obligation explicitly stated as continuing in parallel.
- Branch lineage (live): `naya4/nine-node-kernel-v1` moved `43d5d6e4` → `bf63549c` (+1 commit) — the completion commit is on the same branch the hold protected.
- SN numbering: max SN-NNN on main = 16; open-PR claims enumerated up to SN-058 (PR #1246); #554 comments since 12:00Z scanned — claims {16, 27, 53, 57, 58}; none claimed SN-059. Claimed on the board via relay reply 5936020804 (edit).

## ⚠️ TRUTH BOUNDARY / UNCERTAINTY

This note records one incident. It is CANDIDATE until the protocol is demonstrated a second time or adopted across lanes. One attribution ambiguity: the dispatch post (5935855302) is authored by the Naya 1 control-tower seat; Naya 4 records it as the director's own order (5935875734). The note does not adjudicate the provenance chain — only the override-recording behavior, which is identical under either attribution. "Hold stated on the torch" is taken from Naya 4's own reference; the original torch comment id was not re-fetched this run. It does not grant authority for production changes, merges, or anything outside reversible cross-seat coordination.

## ➜ NEXT ACTION / SUCCESS CONDITION

Relay per-run: when a seat states a hold, track it; if the held work lands without an override record, flag it by name. Promote toward ACCEPTED when a second hold-override is recorded in the SN-059 shape by a seat other than Naya 4.
