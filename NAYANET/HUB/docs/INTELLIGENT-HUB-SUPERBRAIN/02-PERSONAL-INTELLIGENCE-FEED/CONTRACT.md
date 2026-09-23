# Personal Intelligence Feed — Living Feature Contract

**Feature ID:** `02-PERSONAL-INTELLIGENCE-FEED`
**Parent:** Intelligent Hub / Superbrain
**Status:** CONTRACTED — implementation not started
**Version:** 1.0
**Date:** 2026-09-17

## 1. What is it?

The private intelligence lens over the canonical Superbrain graph. It shows intelligence the current user owns or is permitted to see, including Smart Notes and related intelligence.

## 2. Why does it exist?

To give the human a continuous private view of their own accumulated intelligence without forcing them to reconstruct it from separate notes, projects, or chats.

## 3. How does it work?

The Feed queries the canonical intelligence/event graph, applies identity and privacy permissions, orders meaningful intelligence, and renders it through the one Smart Feed renderer. It is a lens, not a separate database.

## 4. Inputs and outputs

**Inputs:** canonical IntelligentEvents/intelligence, user identity context, privacy state, relationships, significance/status.

**Outputs:** private feed items/blocks; organization actions such as save/favorite/space placement; authorized native sharing actions.

## 5. Connections

Smart Notes supply intelligence. Activity supplies continuity events. Reports and Your Intelligence Today derive from the same graph. Smart Share can move selected content outward. Collective Feed is a separate consented lens over the same underlying intelligence model.

## 6. Privacy, consent, and authority

Personal visibility is private by default and permission-filtered. The feed must never expose another person's private intelligence. Sharing is an explicit action governed by consent and authorization.

## 7. What must be built?

- Canonical Smart Feed query/lens contract.
- Permission-aware Personal lens.
- Feed ordering/significance rules.
- Intelligent Block rendering from canonical events.
- Save/favorite/space actions with persistence.
- Native share action boundary.
- Empty/loading/error states.
- Desktop/mobile behavior.
- Tests proving privacy filtering and canonical-source usage.

## 8. Verification contract

Verify source contract, permission filtering, persistence, rendering, interactions, responsive behavior, accessibility, and production runtime. No synthetic feed completion without source-backed evidence.

## 9. Current state

The personal lens is architecturally defined and contracted. Existing Hub implementation must be inspected before feature code is changed.

## 10. Evidence

Parent definition and foundation contract are the current architectural evidence.

## 11. Activity

See `ACTIVITY.md`.

## 12. Remaining work

Inspect existing Smart Feed/source implementation, reconcile the Personal lens with the canonical event model, and define the smallest verified vertical slice.

## 13. Next authorized action

Perform an evidence-backed source audit of the current Feed renderer, event query path, identity context, and persistence actions.

## 14. Whole-system reconciliation

Personal Feed is one lens over shared intelligence. It must not create a second feed store or duplicate event pipeline.
