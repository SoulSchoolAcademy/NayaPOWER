# Smart Feed — AI Builder Spec

**Read first:** parent Hub contracts + this room's FUNCTIONAL-SPEC + DESIGN-CONTRACT.

## Intent

Build the canonical live intelligence stream. The room must express real mode changes, relevance and provenance; it is the raw/current layer that Today later synthesizes.

## Build order

1. Preserve the shared Hub shell and Naya context.
2. Implement the room's five layers: ORIENTATION → CURRENT STATE → INTELLIGENCE → ACTION → PROOF.
3. Build the signature instrument before secondary controls.
4. Bind controls to governed runtime operations or honest unavailable states.
5. Preserve canonical object identity across handoffs.
6. Implement loading/empty/blocked/unauthorized/not-verified/verified/error/offline/unknown/disabled.
7. Prove keyboard, responsive, reduced-motion, performance and back/forward continuity.

## Required components / views

- FeedModeSelector
- SpaceContext
- NewSinceLastVisit
- IntelligenceStream
- IntelligenceObject
- WhyAmISeeingThis
- ObjectActionDeck
- ProgressiveFilters

## Primary causal actions

- OPEN
- ASK_NAYA
- CAPTURE_SMART_NOTE
- SAVE_FAVORITE
- ADD_TO_LIST
- OPEN_EVIDENCE
- SHARE_CONNECT_IF_AUTHORIZED

## Data / runtime

Canonical intelligence/events via governed runtime. Ranking inputs may include relevance, recency, active Space, relationships, goals and verified learning, but must be explainable.

## Anti-patterns

- social-media clone
- engagement bait or vanity metrics
- mysterious ranking with no explanation
- fake live motion
- dense filter dashboard

## Acceptance proof

- switching COLLECTIVE/PERSONAL/ACTIVITY changes real data
- why-am-I-seeing-this is explainable
- provenance is inspectable
- object handoffs preserve canonical ID
- scroll/return context restores
- quiet/empty/offline states remain honest

Self-score does not close the gate. Independent review required.
