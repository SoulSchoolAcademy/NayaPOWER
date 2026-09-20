# NayaPOWER Activation Capability Matrix
## GitHub-only activation vs NayaNET-managed runtime

**Date:** 2026-09-19  
**Status:** CANONICAL WORKING MATRIX — v1  
**Repository:** `SoulSchoolAcademy/NayaPOWER`

### Purpose

Answer one product question precisely:

> **What does a person actually get when they activate NayaPOWER with a GitHub repository, without managing their own Supabase project?**

This matrix separates:
- what is already structurally/runtime proven;
- what can be delivered through the managed NayaNET runtime;
- what can live in the user's GitHub repository;
- what still requires engineering or proof;
- what belongs to the Power Portal rather than ordinary activation.

### Architecture decision

**Ordinary activation must NOT require the user to create or administer Supabase.**

The intended boundary is:

`USER → GitHub NayaPOWER repo → NayaNET authenticated runtime → managed persistence/services → Hub projections`

GitHub is the user's inspectable engineering/control substrate. NayaNET-managed services provide application runtime, authentication, persistence, communications, intelligence processing, and advanced services. The Hub remains a projection/interaction layer, not a second source of truth.

A future GitHub App should use the minimum repository permissions required and let the user choose the repositories it can access. GitHub's installation model supports repository-scoped permissions and separate installation/authorization boundaries.

---

## Capability matrix

| Feature | UI / experience | Runtime | Persistence / source of truth | Authorization | Verification | Activated GitHub-only user | Current status |
|---|---|---|---|---|---|---|---|
| **Personal Intelligence** | Your Intelligence Today / personal feed | PIS + managed Naya runtime | Canonical intelligence/event substrate | User identity + owner boundary | Retrieval/provenance/identity tests exist; full live product journey still needs proof | **YES — managed runtime required** | 🟢 Core, integration incomplete |
| **Collective Intelligence** | Smart Share / collective discovery | Shared intelligence service | Canonical intelligence + visibility/consent | Owner + sharing/consent | Privacy/provenance architecture exists; full multi-user runtime proof needed | **YES — managed runtime required** | 🟡 Needs end-to-end proof |
| **Activity** | Activity feed | Canonical event → Activity projection | Canonical event store; Activity is projection | Actor/owner | Execution evidence/closure exists in architecture; automatic universal closure remains a known gap | **YES** | 🟢 Strong substrate; closure needs completion |
| **Reports** | Your Report / intelligence reports | Report projection/aggregation | Canonical intelligence/events | Owner | Report truth must trace to canonical evidence | **YES — managed runtime** | 🟡 Product/runtime integration needed |
| **Smart Notes** | Capture, read, save, retrieve, reuse | Smart Note/CIS/PIS pipeline | Canonical Smart Note/intelligence substrate | Owner + visibility | Canonical identity, timestamp, provenance, privacy, verification invariants have passed in IH-03 | **YES** | 🟢 Core capability |
| **Smart Share** | Share intelligence / discover shared intelligence | Sharing/projection service | Same Smart Note identity; no duplicate intelligence store | Explicit sharing/consent | Must prove visibility, provenance, revocation/supersession | **YES — managed runtime** | 🟡 Architecture defined; full product proof needed |
| **Smart Lists** | Organize Smart Notes into lists/categories | List projection/query layer | Canonical Smart Notes; list membership is metadata | Owner | Identity/provenance must remain attached | **YES** | 🟡 Architecture defined; implementation/proof needed |
| **Smart Mail** | One-to-one and future group/page messaging | `nayanet-smart-mail` Edge Function + receipt substrate | Canonical execution receipts + intelligence | Authenticated sender/receiver + owner/project/policy gates | Real sender/receiver lifecycle and policy lineage proven; value comparison currently NOT_PROVEN | **YES — managed runtime** | 🟢 Engine real; Hub UX still needs integration |
| **Contacts** | Contact list / select recipient | Contact/identity service | Canonical identity/contact relationship data | Owner + sharing boundaries | Identity/recipient correctness required | **YES — managed runtime** | 🟡 Product engine needs completion |
| **Smart Spaces** | Turn Smart Note into living group/room | Shared-space service + messaging/event pipeline | Canonical intelligence/events; no duplicate truth store | Owner + membership + posting rights | Must prove membership, privacy, message delivery, intelligence creation | **YES — managed runtime** | 🟠 Concept/contract strong; runtime substantially incomplete |
| **Dream** | Dream/reasoning experience | NayaNET-managed reasoning service | Candidate outputs must return to canonical intelligence only after governance | User + action authority; Dream is never judge | Candidate/authority separation is established; user-facing Dream journey not fully proven | **YES — managed runtime** | 🟡 Infrastructure/concept exists; product integration incomplete |
| **Settings** | Identity, privacy, notifications, sharing, preferences | Managed auth/profile/settings services | Canonical identity + user preferences | User-authenticated | Settings changes must have observable effect | **YES** | 🟡 Needs capability contract + UX completion |
| **Naya Play** | ▶ on an intelligent block | Naya Voice/TTS service | No new intelligence store; playback references canonical content | User/session | Must prove correct content, identity, access, and playback | **YES — managed runtime** | 🟠 Voice capability exists; Hub integration not complete |
| **Search** | Meaning/relationship retrieval | Managed retrieval/search | Canonical intelligence/events | Owner + visibility | Provenance and visibility must survive retrieval | **YES** | 🟡 Architecture defined; full product proof needed |
| **Connections** | Relationship graph between intelligence/people/events | Relationship/query service | Canonical IDs + relationship index | Visibility/owner rules | Relationship identity and stale/superseded handling needed | **YES** | 🟡 Navigation/index substrate exists; user product needs completion |
| **Your Intelligence Today** | Main landing intelligence surface | PIS + report/activity/retrieval projections | Canonical intelligence | User identity | Freshness/provenance + retrieval | **YES** | 🟢 Strong architectural foundation; live UX closure needed |
| **Your Report** | Historical intelligence interpretation | Aggregation/report service | Canonical events/intelligence | User | Evidence-linked interpretation | **YES** | 🟡 Needs product completion |
| **Intelligence Library** | Browse retained intelligence | Retrieval/projection layer | Canonical Smart Notes | Owner/visibility | Identity/provenance | **YES** | 🟢 Concept and substrate strong |
| **Advanced policy evolution** | Mostly invisible to ordinary user | Policy/governance runtime | Policy + execution receipts | Explicit authorization | Paired comparison + adversarial verification | **MANAGED ONLY** | 🟠 Engine proven mechanically; improvement not yet proven |
| **GitHub governed execution** | Eventually Naya action → GitHub | GitHub App/adapter + webhooks | GitHub + canonical receipts | GitHub installation + repository scope + Naya authority | Must prove action/result/webhook/verification | **YES after GitHub App activation** | 🟡 Infrastructure exists; App loop still to build/prove |
| **Power Portal / full engineering controls** | Developer/governance cockpit | Full NayaPOWER control plane | Repository + managed runtime | Shawn/admin authority | Full governance/evidence suite | **NO — special/admin surface** | 🟢 Deliberately broader than ordinary activation |

---

# Activation boundary

## What a normal person should NOT have to do

They should **not** need to:

- create a Supabase project;
- configure database tables;
- write RLS policies;
- deploy Edge Functions;
- understand migrations;
- manage service credentials;
- configure Cloudflare;
- understand policy receipts;
- operate the governance kernel.

That complexity belongs behind NayaNET.

## What they SHOULD do

The target activation should be approximately:

1. Create a free GitHub account if needed.
2. Create their `NayaPOWER` repository.
3. Start NayaPOWER activation.
4. Install/authorize the Naya GitHub App when it is ready.
5. Select the NayaPOWER repository.
6. Complete identity/consent.
7. Naya initializes the canonical activation documents.
8. User enters the Intelligent Hub.
9. Smart Notes, Intelligence Today, Activity, Reports, Library, Smart Lists, communication, and other available capabilities are immediately usable.

GitHub App installation should be repository-scoped where possible. GitHub explicitly supports choosing only selected repositories during installation and distinguishes installation permissions from user authorization. citeturn0search0turn0search1

---

# Three capability tiers

## Tier 1 — Activated NayaPOWER

The ordinary human experience.

**Target:**

- Smart Notes
- Your Intelligence Today
- Personal Intelligence
- Activity
- Your Report
- Intelligence Library
- Smart Lists
- Smart Share
- Contacts
- Smart Mail
- Smart Spaces
- Connections
- Search
- Naya Play
- core Naya guidance/continuity
- privacy/sharing/settings

**No user-managed Supabase.**

---

## Tier 2 — Managed Advanced NayaPOWER

Still no user-managed infrastructure.

Adds:

- Dream
- advanced intelligence processing
- advanced learning
- governed external actions
- policy-aware execution
- richer collective intelligence
- automation/scheduling
- GitHub execution
- deeper verification

NayaNET operates the machinery.

---

## Tier 3 — Power Portal

Administrative / engineering / research environment.

Adds:

- governance engineering;
- policy experiments;
- adversarial evaluation;
- deployment control;
- control-plane management;
- source/runtime proof;
- GitHub engineering operations;
- Superbrain research;
- experimental capabilities.

This is intentionally more powerful than a customer's NayaPOWER.

---

# Critical architectural law

The activation package must create **one user's Superbrain**, not a second mini-version of the NayaPOWER architecture.

The user's repository should establish:

`IDENTITY + GOVERNANCE + CONTINUITY + LOCAL/INSPECTABLE INTELLIGENCE CONTRACTS`

while NayaNET supplies:

`AUTH + PERSISTENCE + RUNTIME + COMMUNICATION + REASONING + RETRIEVAL + ADVANCED SERVICES`

The two layers must remain connected by canonical identity and provenance.

---

# What is proven today

### Proven / strong

- Canonical Smart Note identity and replay invariants.
- Timestamp/provenance/privacy/verification invariants for the canonical Smart Note transaction.
- Authenticated persistence/retrieval/action/observation/verification lifecycle.
- Fresh-context retrieval/render continuity.
- Real Smart Mail sender/receiver execution.
- Policy identity in execution receipts.
- Policy comparison lineage enforcement.
- Receipt-swap adversarial rejection.
- Managed Supabase runtime can support authenticated users without requiring the end user to administer the project. Supabase supports authenticated user identities and RLS-controlled access; anonymous auth is also technically available but should not be confused with durable user identity. citeturn0search4turn0search7

### Not yet proven

- A clean fresh-user activation from empty GitHub repository to usable Superbrain.
- Every Hub sidebar feature working end-to-end for a fresh activated user.
- Smart Spaces complete runtime.
- Contacts complete runtime.
- Smart Lists complete runtime.
- Smart Share complete multi-user runtime.
- Naya Play integrated across intelligent blocks.
- Scheduler.
- Full Dream product surface.
- Full learning → future decision loop.
- Full GitHub App installation → governed action → webhook → verification loop.
- Universal automatic Activity closure at every consequential execution boundary.
- Windows-local activation/recovery because the current repository has a Windows-invalid tracked filename.

---

# Definition of "Activated NayaPOWER works"

A fresh user passes activation only when:

`EMPTY GITHUB REPO`
→ `ACTIVATION`
→ `IDENTITY`
→ `AUTHENTICATION`
→ `CANONICAL INTELLIGENCE`
→ `SMART NOTE`
→ `PERSONAL FEED`
→ `ACTIVITY`
→ `REPORT`
→ `RETRIEVAL`
→ `SHARE / MAIL / SPACE`
→ `VERIFIED CONSEQUENCE`
→ `LEARNING`
→ `FRESH NAYA`
→ `CONTINUE`

works without the user operating Supabase.

---

# Immediate build order

### P0 — Activation contract

Create the actual activation package/spec that turns an empty GitHub repository into a canonical NayaPOWER repository.

### P0 — Runtime identity bridge

Bind:

`GitHub account/repository ↔ Naya identity ↔ managed runtime identity`

without creating duplicate identity systems.

### P0 — Core user journey

Prove:

`ACTIVATE → SMART NOTE → INTELLIGENCE TODAY → ACTIVITY → REPORT → RETRIEVE`

with a fresh user.

### P1 — Communications

Complete:

`CONTACT → SMART MAIL → RECEIVER → ACTIVITY → INTELLIGENCE`

then:

`SMART NOTE → SMART SPACE → MEMBERS → MESSAGE → NEW INTELLIGENCE`

### P1 — Organization

Complete Smart Lists + Connections + Search.

### P1 — Naya experience

Integrate Dream and Naya Play.

### P1 — GitHub App

Build:

`NAYA → AUTHORIZED GITHUB ACTION → GITHUB → WEBHOOK → RECEIVER → VERIFY → ACTIVITY → LEARN`

### P2 — Scheduling

Add recurring intelligence/actions only after the execution loop is proven.

---

# Human authority still matters

The system should automate infrastructure, not silently invent human values.

For human value, use the existing responsible-value model and extend it with inspectable human outcome dimensions such as:

- quality achieved;
- usefulness;
- time/effort saved;
- goal progress;
- clarity gained;
- learning gained;
- connection created;
- care/respect/understanding;
- harm avoided;
- cost incurred;
- risk incurred.

The system can score these consistently, but the human-defined meaning of "valuable" remains an explicit product/governance contract rather than something a candidate policy gets to redefine.

---

# Final answer to the product question

> **What does somebody get when they activate NayaPOWER?**

They should get **their own persistent Superbrain experience without becoming a database administrator.**

Their GitHub repository gives them an inspectable, durable control/intelligence substrate.

NayaNET gives them the managed machinery that makes that substrate **alive**.

And the Intelligent Hub gives them the human experience:

**capture → understand → remember → connect → use → share → communicate → verify → learn → continue.**

That is the activation product.

The Power Portal can remain substantially more powerful. That is not a problem; it is the **engineering/governance superset** from which the consumer NayaPOWER experience is safely exposed.

---

## Current matrix verdict

**Architecture: READY**

**Core Smart Note/Personal Intelligence foundation: PROVEN**

**Managed-runtime/no-user-Supabase model: VIABLE**

**Full activated-user product: NOT YET PROVEN**

**GitHub App activation: NEXT MAJOR BRIDGE**

**Smart Spaces / Contacts / Lists / Share / Naya Play: NEED IMPLEMENTATION + END-TO-END PROOF**

**Supabase setup for ordinary users: NOT REQUIRED BY THE TARGET ARCHITECTURE**

**Next executable action:** build the **fresh-user activation transaction** against an empty test GitHub repository, then prove the first complete user journey before expanding the remaining Hub features.
