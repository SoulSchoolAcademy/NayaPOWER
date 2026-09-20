# Naya Brain Organization Contract

**Recorded:** 2026-09-09 11:08 PT  
**Status:** CANONICAL · ACTIVE  
**Scope:** Every Naya user Superbrain

## North Star

Make intelligence easy to capture, date, find, understand, verify, improve, and carry forward.

## Organization law

Every newly created or materially changed intelligence object MUST carry `created_at`, `updated_at`, `event_time` when applicable, `timezone`, `object_type`, `status`, source references when applicable, a project/scope identifier when applicable, and a revision for mutable state.

Human-readable records SHOULD contain a visible recorded timestamp.

## Time is metadata, not truth

A missing date/time is a quality warning, not automatic proof that an object is obsolete. Existing undated material is classified as `LEGACY_UNDATED` until reviewed. It is never silently deleted solely because it lacks a timestamp.

## Lifecycle

`CAPTURE → TIMESTAMP → CLASSIFY → LINK → VERIFY → USE → LEARN → REVISE → ARCHIVE`

## Canonical object classes

`SOURCE`, `DECISION`, `EVENT`, `STATE`, `RECEIPT`, `LESSON`, `PLAN`, `HANDOFF`, `REFERENCE`, `ARCHIVE`.

## Relevance rules

- Current truth outranks historical intent.
- Verified evidence outranks assertions.
- Newer state does not automatically invalidate older evidence.
- Obsolete material is archived with a reason and timestamp when its historical value remains.
- Duplicate representations must point to one canonical authority.
- Derived views are never competing sources of truth.

## Superbrain retrieval contract

Search/retrieval must support `time + type + project + status + source + topic + revision`, making the newest relevant state easy to find while preserving lineage.

## Cleanup rule

Optimization removes noise, duplication, stale presentation layers, dead controls, and competing authorities — not information merely because it is old. Destructive deletion requires evidence that an object is redundant, erroneous, prohibited, or explicitly disposable.

## Universal handoff

Every active project exposes where we are, what happened, what is verified, what is unknown, what matters, what changed, what remains, the exact next action, evidence, and timestamp/revision.

## Model standard

This contract is the organizational pattern for Naya Power activation and Superbrain construction. The objective is maximum useful intelligence per unit of complexity.
