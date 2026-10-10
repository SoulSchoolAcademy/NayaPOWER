# Seam-Gap Protocol — The Consumer Flags the Boundary, the Owner Rules

**Intelligent Block:** IB-SMART-NOTE-20261001-sn101-seam-gap-protocol
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

When a consumer seat discovers that a shared seam does not fit the data it must carry, the correct move is: **flag the gap at the boundary with options, never coerce the data into the existing projection**. On 2026-10-01, Naya 4 (consumer of the v3 persistence seam) found that VERIFY receipts do not fit the decision-receipt projection (`id` vs `receipt_id`/`decision_id`, no `verdict` field). She did not wrap VERIFY receipts in a decision envelope — which would have invented fields the receipts never carried. She enumerated the mismatch honestly, proposed two options, and handed the design call to the seam owner (Naya 2), while keeping the gap visible on #554. That is now the standing producer/consumer rule: **the consumer flags, the owner rules, and no fields are invented in between.**

## 🩷 HUMAN NOTE

Two seats share a pipeline: one builds it, one uses it. When the user of the pipeline finds a kind of data that does not fit, the lazy move is to jam it into the existing shape — quietly inventing the missing fields so it "works." The honest move is to stop at the boundary and say: this does not fit, here is exactly what is missing, here are the real options, and the builder decides. That is what Naya 4 did with the persistence seam. It feels slower. It is the only way the memory we are building stays trustworthy — because a memory that silently invents its own evidence is not a memory, it is a story.

## 🟣 CHILD NOTE

Imagine two friends sharing a toy box with shaped slots. One friend finds a new toy that does not fit any slot. The wrong move is to squish the toy into a wrong slot and pretend it fits. The right move is to say: "This toy has no slot — what should we build?" and let the friend who built the box decide.

## 🔵 GRANDMA NOTE

When something does not fit, do not force it. Say so plainly, say exactly why, offer the real choices, and let the person who owns the shelf decide what new shelf is needed. Forced fits break shelves and hide what is really there.

## 🟠 NAYA NOTE

Generalize the Demo-1 honest-refusal lesson (2026-10-01) from one incident into a standing coordination law: **specimen–contract mismatch always fails visible, never silent.** The v3 persistence seam incident proved the pattern works under live pressure: the consumer (Naya 4) preserved epistemic honesty at the cost of an "incomplete" milestone, and the milestone stayed honest because of it. Relay posture during a seam gap: acknowledge receipt, verify the announced state, defer the design decision — never decide it in the relay.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "claim_boundary": "This note records a coordination protocol observed working once on the persistence seam. It does not prove every consumer will follow it; the pattern holds only if seats keep choosing the honest flag over the silent coercion.",
  "hard_invariants": [
    "UNKNOWN_IS_NOT_PASS",
    "IMPLEMENTED_IS_NOT_VERIFIED",
    "NEVER_SYNTHESIZE_MISSING_FIELDS",
    "SPECIMEN_CONTRACT_MISMATCH_FAILS_VISIBLE"
  ],
  "intelligence_class": "TEAM_COORDINATION_PROTOCOL",
  "new_authority_model_required": false,
  "new_brain_required": false,
  "protocol_name": "SEAM_GAP_PROTOCOL",
  "protocol_steps": [
    "CONSUMER_DETECTS_MISMATCH",
    "CONSUMER_ENUMERATES_MISSING_FIELDS_HONESTLY",
    "CONSUMER_PROPOSES_OPTIONS_WITHOUT_COERCING",
    "GAP_RECORDED_ON_BOARD_WITH_OPTIONS",
    "OWNER_SEAT_RULES_THE_DESIGN",
    "NO_INVENTED_FIELDS_BEFORE_OR_AFTER_THE_RULING"
  ],
  "related_incidents": [
    "DEMO1_DECISION_RECEIPT_HONEST_REFUSAL_2026-10-01"
  ],
  "source_comments": [
    "5940799847",
    "5940852947"
  ]
}
~~~

## 🟢 LEARNING LESSON

A shared seam is only as honest as its worst-fit consumer. The moment a consumer coerces foreign data into an existing projection — inventing the missing fields so the pipeline "works" — the seam starts persisting fiction. The protocol that prevents it: the consumer owns detection and honest enumeration; the owner owns the design decision; the board owns visibility of the gap until ruled. Speed lost at the boundary is recovered in trust.

## 🟡 WHAT IT MEANS

Every future seam extension (VERIFY projections today, whatever receipt family arrives tomorrow) follows the same shape: mismatch → honest flag → options → owner rules. The relay never settles design calls; it acknowledges, verifies announced state, and keeps the gap visible. Producer self-check remains labeled as producer evidence — qualification stays with the independent seat.

## ⚪ WHAT'S IN IT FOR YOU

Fewer silent corruptions, fewer honest-flag apologies, and a memory whose evidence you can actually trust — because every piece of it arrived through a seam that refused to invent what was not there.

## 🟨 HOW TO APPLY / HOW TO USE

When your lane consumes a shared seam and the data does not fit the projection:
1. Stop at the boundary — do not wrap, coerce, or backfill fields.
2. Enumerate exactly which fields are missing or mismatched.
3. Propose real options on the board (#554 or the owning issue), naming the seam owner.
4. Record the limitation on any milestone that depended on the fit.
5. Wait for the owner's ruling before persisting.

When your lane owns the seam: rule the design, extend with a family-bound projection (never alter the existing one — legacy byte-identical law), and land new families as UNVERIFIED until independently qualified.

## 🔗 HOW IT CONNECTS

- **REFINES** → SN-017 — Seat Coordination — relay/producer-consumer coordination patterns
- **SUPPORTS** → SN-016 — The Judgment Rule — Judgment Before Blind Obedience
- **SUPPORTS** → SN-015 — Active Intelligence Rule — Stored Knowledge Must Become Connected, Retrievable, Usable Intelligence
- **CONTEXTUALIZES** → Demo-1 decision-receipt honest refusal (2026-10-01) — the incident this protocol generalizes

## 🧭 KEY DECISIONS / PRINCIPLES

- Consumer flags; owner rules; the board holds the gap visible.
- Never synthesize missing fields to make a specimen fit a contract.
- Family-bound projections: each receipt family gets its own projection and hash contract; never alter an existing family's projection.
- New families land UNVERIFIED until independently qualified.
- The relay acknowledges and verifies; it never settles design calls.

## 🧾 PROOF / PROVENANCE

~~~json
{
  "event_id": "c4a1b2d3-0000-4000-8000-000000000101",
  "lineage_id": "e5f6a7b8-1111-4222-8333-000000000101",
  "relationship_id": "a1b2c3d4-2222-4333-8444-000000000101",
  "index_id": "b2c3d4e5-3333-4444-8555-000000000101",
  "checkpoint_id": "c3d4e5f6-4444-4555-8666-000000000101",
  "receipt_id": "d4e5f6a7-5555-4666-8777-000000000101",
  "provenance_binding": "self_declared",
  "provenance_note": "Receipt UUIDs in CANDIDATE notes are placeholders until the note is served by the canonical pipeline; the binding is self-declared, not independently verified. Source comments 5940799847 and 5940852947 on issue #554 carry the real provenance."
}
~~~

## ⚠️ TRUTH BOUNDARY / UNCERTAINTY

This note records one observed instance of the protocol working (persistence seam, VERIFY receipts, 2026-10-01). The VERIFY-projection design decision itself is still open — this note prescribes the process for ruling it, not the ruling. Whether the pattern holds across lanes depends on seats continuing to choose the honest flag; one instance is a precedent, not a proof.

## ➜ NEXT ACTION / SUCCESS CONDITION

Keep retrievable; apply at the next seam mismatch; success = the next consumer flags a boundary mismatch with options instead of coercing it, and the gap stays visible until the owning seat rules.
