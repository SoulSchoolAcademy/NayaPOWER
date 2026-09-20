# NayaNET — Permissioned Federation Protocol v1

**STATUS:** CANONICAL DESIGN / NOT YET PRODUCTION IMPLEMENTED
**PURPOSE:** Define how independent private Naya Power Superbrains can connect without surrendering private memory or control.

## 1. Core law

> **PRIVATE BRAINS. PERMISSIONED BRIDGES. PROVENANCE-PRESERVED KNOWLEDGE. COLLECTIVE INTELLIGENCE BY CHOICE.**

NayaNET is a federation layer, not a shared raw-memory database.

Each person owns an independent Naya Power Superbrain. Federation is an explicit capability granted by that user.

## 2. What is shared

The default unit of federation is **knowledge**, not raw memory.

Possible share scopes:

- Public Knowledge — intentionally public.
- Network Learning — selected lessons contributed without exposing personal identity or source details.
- Shared Smart Note — one explicitly selected note/event.
- Shared Project — a defined project namespace.
- Capability — a Naya-to-Naya service/request channel.
- Collective CIS — aggregated/synthesized network learning.

Private conversations, credentials, raw personal memory, private identities, private projects, and personal CIS remain local unless separately authorized.

## 3. Simple user experience

The first version should feel like a few clear controls, not a technical configuration console.

### Connection

**NayaNET → Connect Naya**

Show:

- what connecting means;
- what never becomes shared by default;
- what the user can permit;
- how permissions can be revoked.

### Permission presets

- **OFF** — no federation.
- **LEARN** — contribute selected lessons to collective learning; no identity/source disclosure by default.
- **SHARE** — share explicitly selected knowledge/projects.
- **COLLABORATE** — allow defined Naya-to-Naya collaboration.
- **NETWORK** — enable the full set of permitted network capabilities.

Each preset must be explainable in plain language before activation.

## 4. Consent transaction

**DISCOVER → EXPLAIN → SELECT SCOPE → AUTHORIZE → RECORD CONSENT → ESTABLISH BRIDGE → VERIFY → RECEIPT**

Authorization is explicit, scoped, auditable, revocable, and time-bounded where appropriate.

No hidden enrollment.

## 5. Bridge contract

A federation bridge should expose capabilities rather than raw storage.

Conceptually:

```text
NAYA A
  │
  │ permissioned request
  ▼
FEDERATION BRIDGE
  │
  ├── authorize
  ├── scope
  ├── minimize
  ├── transform/anonymize where permitted
  ├── provenance
  ├── verify
  ├── rate-limit
  ├── audit
  └── revoke
  │
  ▼
NAYA B / NETWORK
```

## 6. Network learning privacy rule

The proposed default for collective learning is:

> **Share the lesson, not the person.**

When a user enables LEARN, the system may contribute an approved, privacy-filtered intelligence artifact to collective CIS without revealing the user's identity, raw conversation, private note, or source context unless explicitly authorized.

This requires a real privacy transformation layer before it can be called production-safe. It must not be implemented as a simple text scrubber.

## 7. Collective CIS

Network CIS must distinguish:

- personal intelligence;
- shared intelligence;
- network intelligence;
- inference;
- consensus;
- disagreement;
- confidence;
- provenance class.

Collective summaries must never overwrite a person's local truth.

The network may say:

> "Across the network, a recurring lesson was X."

It must not silently imply:

> "Everyone believes X."

## 8. Daily network intelligence

Once federation is operational, NayaNET can produce a Daily Network Intelligence Report:

- lessons contributed;
- recurring patterns;
- emerging opportunities;
- corrections;
- successful approaches;
- unresolved disagreements;
- collective next opportunities.

It should publish the network's learned intelligence, not private user histories.

## 9. Revocation

A user must be able to revoke a bridge or scope with one clear action.

Revocation stops future access. It cannot retroactively erase knowledge already intentionally released to a network unless the storage/retention contract explicitly supports deletion. This limitation must be disclosed before consent.

## 10. Technical evolution

The first implementation should not depend on GitHub as the permanent runtime federation transport.

GitHub can serve as the development/source-control and configuration layer. Production NayaNET should eventually use authenticated APIs and a dedicated federation service or protocol with:

- identity/key management;
- scoped authorization;
- signed requests;
- encryption in transit and at rest;
- audit logs;
- consent records;
- revocation;
- rate limits;
- privacy transformation;
- provenance;
- replay protection;
- versioned contracts.

## 11. Architecture sequence

**PERSONAL SUPERBRAIN → LOCAL CIS → VERIFIED NETWORK-ELIGIBLE KNOWLEDGE → PERMISSIONED BRIDGE → NETWORK CIS → DAILY NETWORK INTELLIGENCE**

The personal brain remains useful and complete if federation is disabled.

## 12. Security gate

NayaNET must not be marketed as privacy-preserving federation until the actual implementation proves:

- consent enforcement;
- scope enforcement;
- authentication;
- authorization;
- encryption;
- provenance;
- privacy filtering;
- revocation;
- auditability;
- isolation;
- abuse resistance.

**Design is not implementation. Implementation is not verified production safety.**

## 13. Product principle

Make federation feel like a simple permission button to the human while keeping the complexity inside the bridge architecture.

**Simple outside. Sophisticated inside. Explicit always.**
