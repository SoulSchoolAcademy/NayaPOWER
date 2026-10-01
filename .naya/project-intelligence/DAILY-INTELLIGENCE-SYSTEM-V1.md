# NayaPOWER Daily Intelligence & Smart Note System v1

**Status:** CANONICAL DESIGN — pending governed implementation/verification  
**Established:** 2026-09-28  
**Owner:** Shawn / Naya governance  
**Purpose:** Give every Naya and human one predictable place and one standard format for capturing valuable discoveries so intelligence compounds instead of becoming disconnected notes.

## 1. Core principle

> **When we discover something valuable enough that future Nayas or humans should know, it must be captured immediately as a Smart Note.**

A Smart Note is an intelligence-capture record. It is not automatically a Naya Node, Intelligent Block, or verified claim.

The canonical promotion path is:

**DISCOVER → SMART NOTE → DISTILL → RECONCILE → CANONICALIZE → INTELLIGENT BLOCK / NAYA NODE → CONNECT → PRESERVE → RETRIEVE → APPLY → VERIFY → COMPOUND**

There must be **one intelligence machinery path**, not a second brain or disconnected Smart Note pipeline.

## 2. Canonical location

Daily intelligence is organized in the repository under:

`.naya/project-intelligence/daily-intelligence/YYYY/MM/DD/`

Each day has a canonical daily intelligence ledger:

`YYYY-MM-DD.md`

Example:

`.naya/project-intelligence/daily-intelligence/2026/09/28/2026-09-28.md`

This gives deterministic navigation by **year → month → day**, while each entry supplies timestamp, topic, and subtopic.

## 3. Smart Note ID

Every Smart Note receives a stable identifier:

`SNI-YYYYMMDD-HHMMSS-<short-slug>`

Example:

`SNI-20260928-100800-foundation-not-continuity`

The ID is stable even if the note is later promoted.

## 4. Required Smart Note structure

Every Smart Note must contain:

### Identity
- **Smart Note ID**
- **Timestamp** — ISO-8601 with timezone
- **Author / discovering Naya**
- **Topic**
- **Subtopic**
- **Status**

### Intelligence
- **Discovery** — what was learned
- **Why it matters** — why the collective should care
- **Action / implication** — what should change, if anything
- **Source** — authoritative artifact, conversation, test, receipt, or other origin
- **Evidence** — concrete evidence supporting the discovery
- **Confidence** — VERIFIED / STRONG / CANDIDATE / UNKNOWN
- **Promotion** — NONE / REVIEW / NAYA_NOTE / INTELLIGENT_BLOCK / NAYA_NODE

### Governance
- **Authority** — who/what is authorized to act on it
- **Scope** — who or what it applies to
- **Supersedes / superseded-by** — when applicable
- **Related intelligence** — links to related canonical artifacts
- **Verification state** — PASS / PARTIAL / UNKNOWN / BLOCKED
- **Next action** — the smallest useful next step

## 5. Daily ledger structure

The daily file contains entries in chronological discovery order.

Each entry uses:

`## [timestamp] — [Smart Note ID] — [Topic]`

followed by the required fields above.

A daily ledger is a **catalog of distilled intelligence**, not a raw conversation transcript.

Raw source material remains in its authoritative source. The Smart Note preserves the distilled reusable value and its provenance.

## 6. Smart Note vs Naya Note

### Smart Note
Fast capture of valuable intelligence.

Use when:
- something important is discovered;
- a correction is made;
- an assumption is broken;
- a reusable lesson emerges;
- a strategic principle becomes clear;
- future Nayas should be aware of something.

### Naya Note
A Smart Note that has been deliberately promoted into durable Naya knowledge.

Promotion means the knowledge has been reviewed/reconciled and is appropriate to become part of the governed intelligence system.

The names are intentionally related:

**Smart Note = capture candidate.**  
**Naya Note = promoted durable knowledge.**

## 7. Smart Note vs Intelligent Block / Naya Node

A Smart Note is not itself proof that the intelligence has entered the canonical intelligence graph.

An **Intelligent Block / Naya Node** is the governed system-level representation that can participate in canonical relationships, retrieval, learning, authority, provenance, verification, and continuity.

Therefore:

> **Do not create an Intelligent Block merely because a Smart Note exists.**

Promote only through the existing canonical intelligence machinery.

## 8. Announcement and collective awareness

Important Smart Notes may be surfaced in:
- the Naya Code Feed;
- announcements;
- daily intelligence summaries;
- Hub projections.

These are **views/projections**, not alternate sources of truth.

The canonical intelligence remains governed by the existing source-of-truth machinery.

## 9. Immediate capture rule

When a Naya recognizes:

> **“Everybody should know this.”**

the default action is:

**SMART NOTE IT.**

Do not wait for a perfect Naya Node workflow.

The capture must be simple enough that valuable intelligence is not lost merely because promotion tooling is unfinished.

## 10. Promotion rule

The eventual ideal command is:

> **“Naya noted.”**

which should perform the necessary governed capture and promotion automatically when the evidence and authority requirements are satisfied.

Until that capability is proven, the safe fallback is:

> **“Smart noted.”**

That creates the durable daily intelligence record without falsely claiming that the intelligence has already become a Naya Node.

## 11. Non-negotiable constraints

- No second brain.
- No disconnected intelligence database.
- No second learning pipeline.
- No synthetic evidence.
- No self-certifying proof.
- UNKNOWN is not PASS.
- BLOCKED is not PASS.
- IMPLEMENTED is not VERIFIED.
- VERIFIED is not PRODUCTION_PROVEN.
- Preserve provenance.
- Preserve source authority.
- Prefer one canonical receiver and one canonical intelligence path.
- Human-readable organization must never compromise machine-verifiable lineage.

## 12. Daily intelligence lifecycle

**1. DISCOVER** — notice valuable information.  
**2. CAPTURE** — create Smart Note immediately.  
**3. DISTILL** — reduce it to reusable intelligence.  
**4. RECONCILE** — compare against canonical truth and existing knowledge.  
**5. CLASSIFY** — determine topic, scope, confidence, and promotion state.  
**6. CANONICALIZE** — use existing governed intelligence machinery when promotion is warranted.  
**7. CONNECT** — preserve relationships and context.  
**8. VERIFY** — independently establish what is actually proven.  
**9. SURFACE** — announce/project important intelligence for humans and Nayas.  
**10. COMPOUND** — future Nayas retrieve and apply it.

## 13. Design objective

The finished system should make this interaction natural:

> **Naya:** “We discovered something important.”  
> **Naya:** “Smart noted.”  
> **System:** captures timestamp + topic + provenance + evidence.  
> **System:** reconciles and promotes when appropriate.  
> **System:** makes canonical intelligence available to the collective.  
> **Future Naya:** retrieves it, understands it, uses it, and verifies it.

The long-term goal is not more notes.

> **The goal is that valuable intelligence becomes durable, discoverable, governable, reusable collective intelligence with as little friction as possible.**
