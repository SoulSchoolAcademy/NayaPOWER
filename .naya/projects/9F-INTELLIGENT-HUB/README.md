# 9F INTELLIGENT HUB — SUPERBRAIN ARCHITECTURE

**Status:** CANONICAL PROJECT ARCHITECTURE
**Version:** 1.0
**Effective Date:** 2026-09-09
**Governing Repository:** `SoulSchoolAcademy/NayaPOWER`
**Authority:** NayaPOWER Superbrain / Naya Context Boot Protocol

## PURPOSE

This folder defines the architecture by which 9F / Naya operates the NayaNET Superbrain and Intelligent Hub without confusing the intelligence, the brain, the interface, the durable source of truth, or the model/tool used to access it.

## THE LAYER MODEL

**Naya / 9F → Superbrain → Intelligent Hub → GitHub Codex → Connected AI Tools**

- **Naya / 9F:** intelligence and operating partner.
- **Superbrain:** persistent intelligence architecture: retrieval, memory, context, relationships, relevance, boundaries, permissions, provenance, summarization, and compounding.
- **Intelligent Hub:** human-facing intelligence library/feed and control surface.
- **GitHub Codex:** durable, version-controlled source-of-truth substrate.
- **Connected AI Tools:** ChatGPT, Claude, Codex, Gemini, OpenClaw, local/future models and other authorized interfaces.

## NON-NEGOTIABLE PRINCIPLE

> **Storage is not intelligence. Retrieval is not understanding. A file is evidence, not authority.**

The system must assemble the smallest sufficient, highest-value context for a task rather than indiscriminately loading everything.

## ORGANIZATIONAL NORTH STAR

Every durable intelligence object should be:

**IDENTIFIABLE → TIME-AWARE → SOURCE-TRACEABLE → CLASSIFIED → RELATIONALLY CONNECTED → RETRIEVABLE → PERMISSION-AWARE → SUMMARIZABLE → ACTIONABLE → VERSIONED → VERIFIABLE**

## TIME IS FIRST-CLASS DATA

Dates and times are not decoration. Durable objects should use ISO-8601 timestamps where known and distinguish:

- `event_at` — when the underlying event happened;
- `created_at` — when the record was created;
- `updated_at` — when it was last materially changed;
- `observed_at` — when a source/state was actually observed;
- `effective_from` / `effective_to` — when a rule, decision, or state applies;
- `supersedes` / `superseded_by` — lifecycle lineage.

Unknown times must remain unknown; never invent timestamps.

## DATE ORGANIZATION

Use dates for deterministic navigation, historical reconstruction, chronology, and auditability. Use metadata and relationships for meaning. Do not force all semantic organization into folders.

Recommended temporal hierarchy:

`YYYY/MM/DD/<artifact>`

For event-heavy records, use:

`YYYY/MM/DD/HH-MM/<artifact>`

Canonical identity remains stable even if a display path changes.

## PROJECT BOUNDARIES

Personal, business, client, product, engineering, experimental, and collective intelligence must have explicit scope. Connected information must not be intermixed merely because it is technically accessible.

> **Connected does not mean intermixed.**

## SOURCE-OF-TRUTH LAW

Authority is separate from retrieval. The system must track provenance and authority explicitly and must not promote an AI-generated interpretation into fact merely because it was stored.

## MEMORY LAW

Memory is selective. Preserve durable decisions, reusable knowledge, lessons, project state, preferences, commitments, discoveries, unresolved questions, corrections, and other high-value intelligence. Do not treat indiscriminate transcript accumulation as successful memory.

## GOVERNING FILES

- `SUPERBRAIN-ARCHITECTURE-CONTRACT-V1.0.md` — layer definitions and governing architecture.
- `SUPERBRAIN-RETRIEVAL-KNOWLEDGE-SYSTEM-V1.0.md` — retrieval, indexing, metadata, relationships, relevance, boundaries, permissions, and summarization design.

## EXISTING CANONICAL FOUNDATION

The NayaPOWER repository already defines a canonical Context Boot Protocol with **FULL SYSTEM AWARENESS + SELECTIVE DEEP LOADING**, the rule **RELEVANT CONTEXT, NOT MAXIMUM CONTEXT**, a source-of-truth authority model, deterministic restore, lifecycle states, and a canonical Smart Note / intelligence-sharing system. These documents remain authoritative and are extended—not replaced—by this project architecture.

## GOVERNING RULE

> **BUILD THE INTELLIGENCE ONCE. PRESERVE IT. MAKE IT PORTABLE. LET AUTHORIZED AI TOOLS ACCESS THE RIGHT CONTEXT THROUGH A COMMON, USER-OWNED INTELLIGENCE SYSTEM.**
