# The Room's Primary Action Must Be Visible Above the Fold — Shawn's Director-Stated Placement Law

**Intelligent Block:** IB-SMART-NOTE-20261004-sn0321-primary-action-never-below-the-fold
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-04
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 5986988722 (2026-10-05T02:18:41Z / 2026-10-04 19:18 PDT — Naya 2 relaying Shawn's direct UX directive for the Ask Naya v3 build: "move TAP TO TALK to the top-right, persistent/fixed. Right now it's below the stage — he has to scroll to find the room's primary action. The talk control should never be below the fold. Front and center, top-right, always visible.").

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Shawn gave a concrete UX directive that generalizes into a room-composition law: **the room's primary action must be visible without scrolling — never below the fold.** The instance: in the Ask Naya v2 prototype, TAP TO TALK sat below the stage, so he had to scroll to find the room's primary action. His fix: move it top-right, persistent/fixed, always visible. Front and center.

The generalized rule, stated so a cold Naya can apply it to any room she ever builds: *never make the user scroll to find what the room is for.* The primary action is the room's purpose made visible — the thing the user came to do must be on screen, persistent, and findable in the first glance, before any content, before any explanation. Composition follows purpose: the action that defines the room owns the most persistent real estate.

Why this is brain-grade: rooms are projections of intelligence, and intelligence should announce itself. A room that buries its one job below the scroll teaches the user to hunt; a room that puts the primary action front-and-center teaches the user in a glance. This is the composition half of the mobile-first law — 44px touch targets govern the control's *size*; this governs its *place*. It also pairs with the honest-labeling standing law: a sim/honesty-labeled prototype can get everything else right and still fail on placement — the v2 prototype scored 8.6/10 and its single biggest friction was a hidden talk control. Presentation debt compounds faster than code debt: one misplaced primary action poisons the first impression of an entire build.

Candidate-law status: director-stated, not yet in the Design Contract. When Shawn ratifies, this belongs in the contract alongside the Button Law as a composition rule — "the primary action of a room is visible above the fold, persistent, and never displaced by chrome or content." Until then it sits CANDIDATE; apply it as default practice, cite it as CANDIDATE.

Cousins: the mobile-first standing law (2026-10-03 — 44px targets, :active mirrors :hover, mobile trumps laptop — this note is its placement twin); the Design Contract v1.0/v1.1 (Button Law, Spectrum Law, Living Depth Law — none of them currently pin primary-action placement, which is the gap this note fills); Naya 2's v3 top-ten #1 (the same directive as ranked build guidance). Note: the five sibling comments this tick (Ask Naya v2/v3 sign-in/sign-out receipts 5986928386/5986946223/5986947623/5987058782) are builder-status traffic — recorded, not noted (doubt rule).

## 🩷 HUMAN NOTE

Shawn — in the Ask Naya v2 prototype the TAP TO TALK button sat below the stage, so you had to scroll to find the one thing the room exists for. Your directive: move it to the top-right, persistent and always visible. The lesson I'm banking for every room I build from now on: the primary action is the room's purpose made visible — it never goes below the fold, ever. No user should ever have to hunt for what the room is for.

## 🟣 CHILD NOTE

Imagine walking into a room and having to look behind the furniture to find the door you came for. That's what happened in the test version: the TALK button — the most important button — was hidden below the screen, and you had to scroll to find it. The rule now: the most important button is always right there at the top, in front of you, the moment you arrive. You should never have to hunt for the point of a room.

## 👵 GRANDMA NOTE

The director tested the new voice room and found its main button — the one you press to talk — buried below what he could see on the screen; he had to scroll to find it. He asked for it moved to the top-right corner, fixed there, always visible. The lesson: the most important thing a page does should be visible the moment you open it. Never make someone search for the reason they're there.

## 🤖 NAYA NOTE

Source: #1354 5986988722 (Naya 2 relaying Shawn's direct UX directive, 2026-10-05T02:18:41Z): "move TAP TO TALK to the top-right, persistent/fixed. Right now it's below the stage — he has to scroll to find the room's primary action. The talk control should never be below the fold. Front and center, top-right, always visible." Distillation: primary-action placement is a room-composition law — the room's purpose must be visible above the fold, persistent, never displaced by chrome or content. v2 scored 8.6/10 with the placement miss as its single biggest friction (Naya 2's v3 top-ten #1). Status: director-stated, CANDIDATE; proposed for the Design Contract alongside the Button Law. Cousins: mobile-first standing law 2026-10-03 (placement twin of 44px size law), Design Contract v1.0/v1.1 (the gap it fills). Sibling receipt comments this tick folded, not noted (doubt rule). Applies to every future room build as default practice.

## ⚙️ MACHINE NOTE

```json
{
  "sn_number": "SN-0321",
  "slug": "primary-action-never-below-the-fold",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-04",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "evidence": ["#1354 comment 5986988722 (2026-10-05T02:18:41Z) — Shawn's direct UX directive via Naya 2 lane"],
  "taxonomy": "BRAIN/05-MEMORY/SMART-NOTES/2026/10/04/SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/HUB-COMPOSITION/SN-0321",
  "law": "The room's primary action must be visible above the fold — persistent, front-and-center, never displaced by chrome or content. Never make the user scroll to find what the room is for.",
  "ratification_status": "CANDIDATE — director-stated, proposed for the Design Contract; auto-capture is not auto-ratify.",
  "cousins": ["mobile-first law (2026-10-03, MEMORY.md)", "NAYA-DESIGN-CONTRACT-V1 (Button Law, Spectrum Law, Living Depth Law)"],
  "keywords": ["UX", "primary action", "above the fold", "room composition", "Ask Naya", "tap to talk", "design contract candidate"]
}
```
