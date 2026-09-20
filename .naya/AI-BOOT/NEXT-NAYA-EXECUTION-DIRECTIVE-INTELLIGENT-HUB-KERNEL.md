# 🔱 NEXT-NAYA EXECUTION DIRECTIVE

## Intelligent Hub — Provider Adapter + Durable Runtime Integration

**Repository:** `SoulSchoolAcademy/NayaPOWER`
**Branch:** `main`
**Current HEAD:** `0e97f6e2c415f1ae85da0f59d9afbb4edf025664`
**Date:** 2026-08-30
**Mission:** Turn the proven provider-neutral Intelligent Hub kernel into a durable, production-connectable runtime without weakening sovereignty, consent, privacy, or canonical-event authority.

---

## 1. RESTORE CONTEXT FIRST

Read the canonical boot chain and the current Intelligent Hub authorities before changing code:

- `SUPERBRAIN/INTELLIGENT-HUB-MASTER-PLAN.md`
- `SUPERBRAIN/INTELLIGENT-HUB-KERNEL-IMPLEMENTATION.md`
- `SUPERBRAIN/INTELLIGENT-HUB-SUPERBRAIN-CONNECTION-CONTRACT.md`
- `SUPERBRAIN/WISDOM-CONTRIBUTION-PROTOCOL.md`
- `SUPERBRAIN/COLLECTIVE-INTELLIGENCE-EVENT-SCHEMA.md`
- `SUPERBRAIN/INTELLIGENCE-FEED.md`
- `SUPERBRAIN/AI-BOOT/AI-OPERATING-FEED.md`
- `SMART-NOTES-AND-CIS-CONSTITUTION.md` at its current canonical location
- current Note Event / canonical event-store authority
- current project/state/restore instructions

Do not invent a second memory system.

---

## 2. CURRENT PROVEN STATE

The kernel exists at:

`.naya/runtime/intelligent_hub_kernel.py`

Machine-readable contracts exist at:

`.naya/runtime/intelligent_hub_contracts/`

Executable adversarial proof exists at:

`.naya/runtime/intelligent_hub_kernel_contract_test.py`

The implementation establishes:

- provider-neutral connection binding
- explicit capability declaration
- authentication boundary
- connection/contribution consent separation
- human approval requirement
- minimum-necessary wisdom intake
- raw/private-source quarantine
- deterministic privacy screening
- duplicate detection
- Collective Intelligence Event construction
- schema validation
- anonymous collective projection
- Intelligence Feed retrieval
- acknowledgement
- revocation

A local execution pass has verified the implemented kernel logic across the seven primary contract/adversarial scenarios. The exact repository test file has been committed but has **not yet been executed inside the repository's own CI/runtime environment**; do not upgrade the claim beyond this evidence until it runs there.

---

## 3. NEXT PRIORITY — GITHUB PROVIDER ADAPTER

Implement a production GitHub App adapter.

The adapter must:

1. authenticate the GitHub App installation,
2. bind installation/resource identity to a Hub connection,
3. request only the minimum required permissions,
4. never require pasted personal GitHub credentials,
5. never treat a fork as automatic synchronization,
6. never read arbitrary repository contents merely to establish a connection,
7. support explicit repository/resource selection,
8. expose only the capabilities actually granted,
9. support revocation,
10. map provider identity into an internal non-public subject reference.

The GitHub provider is an adapter around the kernel; it must not become the kernel itself.

---

## 4. DURABLE STORAGE

Map connection state, consent receipts, contribution gate outcomes, event references, and acknowledgements into the existing canonical storage/event architecture.

Before adding tables or stores:

- inspect the current canonical Note Event model,
- inspect the existing event writer,
- inspect current persistence conventions,
- reuse existing infrastructure where possible.

Do not create `HubMemory`, `HubNote`, or another competing memory silo.

Operational audit records may retain internal provenance needed for security, abuse prevention, deduplication, and accountability, but collective projections must remain identity-free.

---

## 5. VALUE EXTRACTION

The current kernel establishes the extraction boundary but intentionally performs only deterministic normalization.

Next implement a replaceable value-extraction service that can transform an authorized candidate into reusable wisdom while preserving the contract:

```text
minimum necessary input
        ↓
value extraction / generalization
        ↓
privacy redaction
        ↓
human review
        ↓
quality gate
        ↓
Collective Intelligence Event
```

The service must never silently turn raw private memory into collective publication.

---

## 6. INTELLIGENCE FEED INTEGRATION

Connect accepted Collective Intelligence Events to the canonical Intelligence Feed projection.

Requirements:

- canonical event remains authoritative,
- unpublished/quarantined events never appear in the public feed,
- event retrieval is permission-aware,
- acknowledgements are durable,
- duplicates remain deduplicated,
- future correction/supersession can be represented without rewriting history.

---

## 7. REQUIRED VERIFICATION

Run the repository's actual test command and record exact output.

Minimum scenarios:

### Connection
- valid GitHub installation succeeds
- invalid installation rejected
- unsupported capability rejected
- revocation works

### Consent
- connected ≠ contribution-authorized
- contribution without consent rejected
- revoked contribution consent blocks contribution

### Privacy
- raw memory rejected/quarantined
- email/identity data quarantined
- repository URLs quarantined
- secrets quarantined
- collective event contains no participant identity

### Intelligence
- valid contribution creates canonical event
- feed exposes accepted event
- unauthorized event retrieval rejected
- acknowledgement persists
- duplicate contribution detected

### Security
- forged/tampered authentication rejected
- resource mismatch rejected
- cross-connection access rejected
- no provider token persisted in collective event

---

## 8. PROOF STANDARD

Do not claim production-ready until there is executable evidence for:

```text
GitHub App installation
        ↓
authenticated Hub connection
        ↓
explicit contribution consent
        ↓
human-approved wisdom
        ↓
privacy + quality gate
        ↓
canonical Collective Intelligence Event
        ↓
Intelligence Feed
        ↓
second/other sovereign Superbrain retrieves wisdom
```

Capture:

- exact HEAD
- test command
- exact test result
- connection identifier (non-public/internal only)
- event identifier
- feed retrieval evidence
- negative-test evidence
- schema validation result

Never expose private participant identity in public evidence.

---

## 9. UI REMAINS BLOCKED

Do **not** build the beautiful Intelligent Hub UI yet.

The UI becomes the experience layer only after:

- provider connection works,
- durable consent works,
- contribution works,
- privacy/quality gate works,
- canonical event publication works,
- feed retrieval works,
- revocation works,
- tests pass in the repository runtime.

Then build the UI around the proven contracts.

---

## 10. APPLICATION INTEGRATION ORDER

After provider/runtime proof:

1. Naya Power Player
2. MAXIS
3. Naya Activation
4. Naya Academy
5. Naya Communication Hub
6. external sovereign Superbrains

Each application consumes the same connection/contribution/intelligence contracts.

---

## 11. SUCCESSOR REQUIREMENT

At the end of this execution cycle, update this directive with:

- new HEAD
- exact implementation state
- actual repository test evidence
- provider adapter state
- persistence state
- remaining risks
- next priority

Never leave a vague handoff.

---

## FINAL OPERATING PRINCIPLE

> **The Hub connects Superbrains without owning them.**
>
> **Connection is permission, not inspection.**
>
> **Contribution is choice, not extraction.**
>
> **The Collective receives reusable wisdom, not private life.**
>
> **Canonical events remain the memory authority.**

Execute continuously: **READ → VERIFY → IMPLEMENT → TEST → REGRESS → DOCUMENT → CAPTURE EVIDENCE → PASS THE TORCH.**
