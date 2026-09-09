# 10 — OPEN DECISIONS BEFORE CODING

**Project date:** 2026-09-09
**Purpose:** identify only the decisions that materially affect implementation so they are resolved before the new Hub is built.

These are not a questionnaire that blocks progress. The existing blueprint is sufficient to begin architectural work. These are the remaining choices that should be explicitly locked before the affected room is implemented.

## 1. CURRENT HUB SOURCE

**Decision:** The new Hub has NO legacy authoritative source.

The 2026-09-08 4:52 Hub is a frozen reference only.

The new implementation must receive a new canonical source path/name created for the fresh build. The old 2026-09-08 file is never edited to become the new Hub.

## 2. LEGACY `NAYANETHUBONE` MATERIAL

The repository contains historical NAYANETHUBONE material. It is not current authority for the new Hub.

Treatment:
- retain as historical evidence unless explicitly archived/deleted later
- never silently deploy it
- never let an old workflow consume it

## 3. OLD `9F 1.html`

The requested old `9F 1.html` artifact was not found by the repository search performed during this setup under that exact naming.

Therefore it has NOT been deleted blindly.

Action before deletion: identify the exact repository path if it exists under another filename. Once positively identified as the obsolete `9F 1.html`, it may be deleted as historical/obsolete material.

## 4. HOME ORIENTATION

Lock as required product content:
- personalized greeting
- current time
- current date
- country/locale
- concise intelligence statement
- privacy statement

The statement must remain visible unless a future explicit product decision changes it.

## 5. INTELLIGENCE STATEMENT

Working product principle to preserve:

**MORE INTELLIGENCE. LESS WASTE.**

If an exact earlier wording is recovered from a source artifact and differs, preserve the recovered canonical wording instead of guessing.

## 6. PRIVACY STATEMENT

Required principle:

**PRIVATE BY DEFAULT · SHARED BY CHOICE · COLLECTIVE BY CONSENT · PUBLIC BY DECISION**

This is both product language and architecture law.

## 7. SMART FEED MODES

Required conceptual modes:
- Personal Intelligence
- Collective Intelligence
- Activity Feed

Decision still required: whether these are tabs, segmented control, filter modes, or a composed feed with explicit sections.

Recommended default: one feed surface with a clear mode selector, preserving one canonical event model underneath.

## 8. INTELLIGENT BLOCK EXPANSION

Required conceptual layers are locked:

WISDOM → HUMAN → CHILD → GRANDMA → NAYA → MACHINE → WEAVER → LESSON / MEANING / ACTION

Decision still required: whether all layers are expanded by default or whether secondary perspectives progressively expand.

Recommended: Wisdom + compact source/status visible by default; deeper perspectives progressively expandable, while preserving one-glance comprehension.

## 9. SMART SPACE

The name exists in the broader product concept, but its exact responsibility is not sufficiently locked in the audited reference.

Before coding Smart Space, define:
- object model
- relationship to Lists
- relationship to Groups
- relationship to projects/workspaces
- permissions
- navigation placement
- persistence

Do not invent this room during implementation.

## 10. NAYA IDENTITY / ACCOUNT

The reference contains a Naya portrait and user avatar but does not establish a complete production identity/account contract.

Before implementing account behavior, define:
- authentication source
- profile source
- Naya identity binding
- user identity binding
- avatar source
- alias
- logout/account management

## 11. PRODUCTION INTELLIGENCE BACKEND

The reference proves local intelligence behavior, not a complete production Superbrain connection.

Before connecting Naya production services, define:
- endpoint
- authentication
- event ID contract
- request schema
- response schema
- receipt schema
- timeout
- retry
- failure state
- privacy boundary
- persistence ownership

## 12. PRODUCTION SEARCH

Local search behavior is understood.

Before semantic search is implemented, define:
- index owner
- embeddings/semantic provider if any
- privacy filters
- ranking contract
- provenance
- pagination
- permission filtering

## 13. SMART MAIL TRANSPORT

The reference preserves drafts locally but does not prove production delivery.

Before send is implemented, define:
- transport provider
- authenticated sender identity
- inbound protocol
- outbound protocol
- message ID
- delivery receipt
- failure/retry
- attachments
- spam/security controls

## 14. COLLECTIVE BACKEND

Before real contribution is implemented, define:
- de-identification boundary
- consent record
- contribution event ID
- revocation behavior
- retention
- moderation/trust
- public vs collective visibility

## 15. MOBILE NAVIGATION

Reference pattern is Home / Notes / Reports / Intel / Mail.

Decision: where do Collective, Evidence, Connections, Settings and Smart Space live on mobile?

Recommended: preserve five high-frequency destinations plus a clearly labeled More/Menu surface for the rest.

## 16. TOPBAR

Required:
- current context
- search access
- connection/trust state
- Naya access
- account access if enabled

Decision: exact control order and whether search is full-width or opens as a command surface.

## 17. LOWER BAR

Locked contents:
- SMART NOTES
- NO DEAD ENDS
- CONTEXT LAW
- 10-STAR SERVICE
- ADAPTIVE LEARNING

Exact report destinations are preserved in the Page/Interaction maps.

## 18. VISUAL DESIGN

Locked direction:
- premium
- cinematic
- editorial
- architectural
- dimensional
- tactile
- black/obsidian foundation
- purple intelligence light
- white typography
- restrained sapphire/green/gold semantics

No generic SaaS card wall.

## 19. IMPLEMENTATION METHOD

Build in vertical slices, not by modifying everything at once:

1. architecture + source boundary
2. shell
3. topbar + welcome
4. sidebar
5. lower bar
6. search
7. Smart Note model
8. Smart Feed renderer
9. Personal/Collective/Activity modes
10. each secondary room one at a time
11. Naya adapter
12. persistence adapter
13. production verification

After each slice:

**SOURCE → BUILD → RUNTIME → SCREEN → INTERACTION → PERSISTENCE → REGRESSION**

## 20. THE QUESTIONS EVERY ENGINEER MUST ANSWER

Before touching a room, the engineer must be able to answer:

- What is this?
- Why does it exist?
- What does the user see?
- What data does it consume?
- What data does it create?
- Where is that data stored?
- What does clicking it do?
- What function handles it?
- What state changes?
- Where does the user go next?
- What persists?
- What is the failure state?
- What is the privacy state?
- What is the verification state?
- What does desktop look like?
- What does mobile look like?
- How do we test it?
- How do we know the exact production runtime is displaying it?

If the answer is unknown, the work stops for that room—not for the whole project—and the unknown is explicitly resolved.
