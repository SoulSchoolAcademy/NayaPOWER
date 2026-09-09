# Naya Superbrain Temporal Index

**Recorded:** 2026-09-09 11:15 PT  
**Status:** IMPLEMENTED · ACTIVE

## Purpose

Give every Naya user's Superbrain one fast temporal retrieval surface without creating a second source of truth.

## Canonical rule

The index is a **derived retrieval index**. Source records remain authoritative. The index may point to a source; it may never override it.

## Indexed dimensions

- owner
- source table
- source object ID
- object type
- title/subject/action
- event time
- created time
- updated time
- status
- project
- revision
- metadata

## Canonical object types

`SOURCE · DECISION · EVENT · STATE · RECEIPT · LESSON · PLAN · HANDOFF · REFERENCE · ARCHIVE`

## Retrieval principle

Default ordering favors the newest relevant intelligence while preserving lineage. Search can combine time, type, project, status, topic/source metadata, and revision.

## Automatic indexing

The database automatically indexes changes from the core Naya cognition state, execution receipts, Naya notes, Smart Note events, and Smart Note receipts.

## Cleanup principle

Do not delete historical intelligence merely because it is old. Archive or supersede it when appropriate, with the reason and timestamp preserved.

## Outcome

The Superbrain becomes progressively easier to search as intelligence accumulates instead of becoming a larger undifferentiated pile of notes.
