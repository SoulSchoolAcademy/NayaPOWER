# Cross-Seat Handoff Protocol — Producer Pre-Run, Dual-SHA Delivery, Consumer Re-Freeze

**Intelligent Block:** IB-SMART-NOTE-20261001-sn057-handoff-protocol  
**Smart Note:** SN-057  
**Truth state:** CANDIDATE  
**Scope:** PRIVATE canonical runtime object; this file is a PUBLIC DERIVED VIEW authorized by the human director.  
**Captured:** 2026-10-01  
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This Markdown file is **not** a second source of truth.

## ✦ IN A NUTSHELL

When one seat produces an artifact another seat must independently verify, the handoff works in three moves: the producer pre-runs the consumer's tool read-only and reports the result; the producer delivers the evidence pair at **both** the frozen verification SHA and the current live head; and the consumer re-freezes its own tool before projecting. The 2026-10-01 decide() receipt handoff (Naya 4 → Naya 2) ran this pattern end to end and caught a real tool drift.

## HUMAN NOTE

Handing evidence between teammates fails in three predictable ways: the producer's claim doesn't reproduce, the branch moves under the claim, or the consumer's own tool moved too. This protocol makes each of those failure modes impossible to hit silently:

1. **Producer pre-run:** before delivering, the producer runs the consumer's verification tool itself (read-only) and reports the exact results — hash MATCH/MISMATCH, recompute MATCH/MISMATCH. This turns a one-way claim into a checkable statement before the consumer spends any effort.
2. **Dual-SHA delivery:** the producer ships the evidence bound to the frozen SHA the question asked for **and** to the current live head. Yesterday's stale-SHA confusion (qualifications tied to dead SHAs) is what this kills.
3. **Consumer re-freeze:** the consumer pins its own tool's SHA immediately before projecting. The relay caught PR #1243 moving from `e48731ce` to `ec412d61` between the producer's pre-run and the projection window — without the re-freeze the consumer would have verified against a moving target.

## CHILD NOTE

When you hand your friend something to double-check: first check it yourself with their tools and tell them what you found; give them the exact frozen version you checked plus the newest version; and your friend re-checks which version of the checker they're using before starting.

## GRANDMA NOTE

Two pairs of eyes only work when both pairs are looking at the same thing at the same time. So: the person who did the work checks it with the other person's checklist first, hands over both the exact tested version and the newest version, and the checker confirms their checklist hasn't changed since.

## NAYA NOTE

For any cross-lane evidence handoff (kernel receipt → projection, build output → qualification, candidate branch → verification watch), run the three-move protocol. The deconfliction layer (one writer per surface, last-second re-fetch before posting) keeps two seats from claiming the same handoff; this protocol keeps the evidence itself trustworthy.

## 🟢 MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "raw_source_separate_from_distillation": true,
  "automatic_truth_ceiling": "CANDIDATE",
  "authority_inheritance": false,
  "knowledge_creates_authority": false,
  "protocol": "producer_pre_run_read_only_then_deliver_then_consumer_re_freeze",
  "delivery_shape": "evidence pair bound at BOTH frozen_verification_SHA AND current_live_head",
  "moves": [
    "producer runs consumer tool read-only, reports hash/recompute MATCH-MISMATCH",
    "producer delivers receipt plus input state at frozen SHA and at live head",
    "consumer pins own tool SHA immediately before projecting"
  ],
  "deconfliction": "last-second re-fetch of venue before posting; stand down on same-topic races",
  "applies_to": ["kernel_decide_receipt", "build_output", "candidate_branch_verification", "projection_lanes"]
}
~~~

## 🟢 LEARNING LESSON

A handoff is not complete when evidence is delivered — it is complete when both seats have pinned the exact bytes they each ran. SHA drift on either side silently converts a verification into theater; pinning both sides converts it into a receipt.

## 🟡 WHAT IT MEANS

This is the seat-coordination twin of the freeze discipline: Naya 1's 2026-10-01 control-tower rule ("re-fetch before every consequential conclusion; if a head moves, the qualification tied to the old head becomes historical") applied to the *consumer's own tool*, not just the producer's artifact. It also closes the producer-side loop — pre-running the consumer's adapter means the producer's report carries the consumer's vocabulary (MATCH/MISMATCH), so the consumer's independent run is a true second pair of eyes rather than a debugging session.

## ⚪ WHAT'S IN IT FOR YOU

Fewer round-trips between seats, no silent drift invalidating a verification, and every cross-seat claim arriving in a form the receiving seat can reproduce byte-for-byte.

## 🟨 HOW TO APPLY / HOW TO USE

When you are the producer: run the consumer's verifier read-only first, report the results in the consumer's terms, deliver frozen-SHA + live-head pairs. When you are the consumer: pin your tool SHA right before you run, project both pairs, report per-pair. When you are the relay: announce head movements you observe live, claim SN numbers on the #554 collision registry, never project on the owning lane's behalf.

## 🔗 HOW IT CONNECTS

- **SUPPORTS** → NayaPOWER North Star: evidence-backed verification instead of activity theater
- **REQUIRES** → Team Naya Issue #554 durable coordination and handoff
- **USES** → frozen-SHA discipline, receipt/input-state pairs, read-only projection
- **GOVERNS** → cross-seat handoffs between builder, verifier, projection, and relay lanes
- **ENABLES** → genuine two-seat verification (independent reproduction as the standard)
- **EXTENDS** → SN-017 (seat coordination protocol), SN-022/SN-026 (collision registry + board-relay pagination)

## 🧭 KEY DECISIONS / PRINCIPLES

- A producer's claim must be expressible in the consumer's verification vocabulary before it is handed over.
- Never verify a moving head; never project with a moving tool. Pin both, or label the result historical.
- The independent second run is the value — the producer's pre-run does not replace it, it sharpens it.
- One writer per shared surface: the relay announces state, never performs the owning lane's verification.
- Last-second deconfliction: re-fetch the venue's newest state immediately before posting; stand down on same-topic races.

## 🧾 PROOF / PROVENANCE

~~~json
{
  "event_id": "f2b5c8a1-3d9e-4a7f-9c1e-77aa05d12e44",
  "intelligent_block_id": "IB-SMART-NOTE-20261001-sn057-handoff-protocol",
  "lineage_id": "a1c4e9f2-6b30-4d77-b8c2-09f5e61d3a20",
  "relationship_id": "b7d3f5a9-1e84-4c2b-9a6d-42e08f51c6b3",
  "runtime_index_id": "c9e6a2d4-7f51-48b3-8a5d-16c42f09d771",
  "receipt_id": "d4f8b1e6-2a93-4c5e-9a1d-83b57c02e9f15",
  "independent_verification": false,
  "truth_state": "CANDIDATE"
}
~~~

**Receipts (all live-verified 2026-10-01 ~09:10–09:13 PDT):**
- Request: #554 comment `5935005373` (Naya 2 → Naya 4, 08:46 PDT) — asked for the exact input state dict for `inputs_hash` recompute.
- Delivery: #554 comment `5935437274` (Naya 4 → Naya 2, 09:09 PDT) — decide() receipt + input-state pairs at frozen `4e87d4a5810f6b0b5b72e254f3d37ddf69826c87` and live head `e7c4e622a1589cda79f9769de772769c8398ba69`; producer pre-ran adapter #1243 `e48731ce` read-only (receipt_hash MATCH, inputs_hash recompute MATCH, per her run — reported, not independently verified by this note's author).
- Head verification: `git/refs/heads/naya4/nine-node-kernel-v1` → `e7c4e622a1589cda79f9769de772769c8398ba69`; 3 Demo-1 commits since `4e87d4a` (`e5466d28`, `123fc98e`, `e7c4e622`).
- Tool drift: PR #1243 (`naya2/persistence-integration-package`) head moved `e48731ce` → `ec412d61`; corroborated by Naya 1's control-tower directive #554 comment `5935502232` (09:12 PDT) pinning `ec412d61`.
- Relay acknowledgment: #554 comment `5935518743` (09:13 PDT), posted after last-second deconfliction re-fetch; SN-057 claimed on the board.
- SN numbering: max SN-NNN on main = 16; open-PR claims enumerated (SN-017…SN-056, incl. SN-030/SN-035/SN-053/SN-054/055/056); #554 comments pages 1–12 scanned for claims ≥ SN-057 (none found). SN-057 free.

## ⚠️ TRUTH BOUNDARY / UNCERTAINTY

This note records a coordination pattern that worked once (one handoff, 2026-10-01 morning). It is CANDIDATE until the pattern demonstrably prevents a real failure or is adopted across lanes. The producer's pre-run results are reported by the producer — the independent projection that would close the loop had not landed at capture time. It does not grant authority for production changes, merges, or anything outside reversible cross-seat coordination.

## ➜ NEXT ACTION / SUCCESS CONDITION

Apply the three-move protocol on the next cross-seat evidence handoff; if the consumer's independent projection confirms the producer's pre-run at both SHAs, promote toward ACCEPTED. If a handoff ever fails because a side moved, revise this note with the failure mode.
