# NAYA POWER — HUB EVENT INTEGRATION / PIS ADAPTER CONTRACT V1

DATE: 2026-09-12
STATUS: CANONICAL INTEGRATION CONTRACT V1
NUMBER: 45

## PURPOSE
Connect the Cross-System Event Contract (#39) to the Hub without allowing adapters to become competing sources of truth.

## 1. PIPELINE

SOURCE → EVENT ENVELOPE → ADAPTER → NORMALIZED INTELLIGENCE → SMART NOTE → FEED PROJECTION → HUB VIEW.

## 2. ADAPTER ROLE

Adapters translate source-specific structures into canonical semantic fields. They may enrich, classify, summarize, or derive learning, but must preserve source identity and distinguish derived interpretation from source fact.

## 3. PIS

The Personal Intelligence System may provide user-specific retrieval, context, relationships, preferences, and learning. PIS-derived content must be marked as derived/personal context and must not overwrite canonical source truth.

## 4. EVENT IDENTITY

Adapters preserve event_id, source_event_id, causation_id, and correlation_id wherever available. Reprocessing must be idempotent.

## 5. VERIFICATION

Adapter output is not automatically verified. Verification status travels with the data and can only advance through qualifying evidence.

## 6. HUB CONSUMPTION

The Hub consumes canonical normalized events, not arbitrary adapter UI payloads. This keeps all lenses consistent.

## 7. FAILURE

An unavailable adapter yields DEGRADED/UNKNOWN state rather than fabricated content. Source data remains recoverable.

## 8. ACCEPTANCE

At least one real source event must traverse source → event → adapter → Smart Note → feed projection and remain traceable to its source identity.
