# NayaPOWER — Intelligent Hub Superbrain Connection Contract v1

**STATUS:** CANONICAL / ACTIVE DESIGN CONTRACT
**EFFECTIVE:** 2026-08-30
**SCOPE:** Intelligent Hub ↔ sovereign Superbrain connections

## Purpose

Define the stable interface by which an Intelligent Hub can connect a person's Superbrain without taking ownership of the Superbrain, exposing private memory, or turning repository synchronization into the collective-intelligence mechanism.

## Core law

> **CONNECT THE SUPERBRAIN. DO NOT ABSORB THE SUPERBRAIN.**

A connected Superbrain remains sovereign. The Hub receives only the minimum authorized capability and data required for the requested operation.

## Connection model

```text
Human
  ↓ explicit authentication + consent
Intelligent Hub
  ↓ authorized connection
Superbrain Adapter
  ↓ least-privilege interface
User's Superbrain

Optional:
  ↓ explicit contribution authorization
Wisdom Contribution Protocol
  ↓
Collective Intelligence Event
```

## GitHub implementation

For GitHub-backed Superbrains, the preferred connection mechanism is a **Naya Intelligent Hub GitHub App**. The user authenticates with GitHub, installs/authorizes the App, selects the intended Superbrain repository, and grants only the required repository permissions.

A fork MAY be used to obtain an independently owned Superbrain. A fork is **not** the synchronization mechanism between Superbrains.

The Hub MUST NOT require a pasted GitHub password or personal access token as the normal connection path.

## Connection object

A connection MUST represent:

- `connection_id`
- `owner_subject` — Hub-internal subject identifier; never placed in collective intelligence objects
- `provider` — e.g. `github`
- `installation_id` or provider-equivalent authorization reference
- `resource_id` — selected repository/resource
- `capabilities`
- `consent_scope`
- `status`
- `created_at`
- `updated_at`
- `revoked_at` when revoked

Provider credentials/tokens are secrets and MUST NOT be stored in notes, feed entries, collective events, or client code.

## Capability boundary

The connection MUST support explicit capability grants rather than implicit full-repository access. Example capabilities:

- `read_superbrain_metadata`
- `read_authorized_wisdom_scope`
- `submit_wisdom_candidate`
- `receive_collective_updates`

No capability is implied by another capability.

## Privacy boundary

The Hub MUST NOT assume access to:

- private conversations
- private notes outside the authorized scope
- unrelated repositories
- personal history
- projects not selected by the user
- credentials/secrets
- raw Superbrain memory beyond the authorized contribution scope

The collective layer MUST NOT require identity, repository URLs, or raw source content.

## Revocation

A user MUST be able to revoke the connection and/or collective participation. Revocation stops future authorized operations. Previously published collective events remain governed by their own provenance and correction/supersession rules; revocation does not silently rewrite history.

## Failure and truth states

Connection state MUST distinguish at minimum:

`PENDING → CONNECTED → DEGRADED → REVOKED`

Unknown/unverified provider state MUST remain `UNKNOWN`; the Hub MUST NOT claim a live connection without evidence.

## Non-goals

This contract does not define authentication UX, provider-specific API implementation, scoring, collective ranking, or the internal storage engine. Those are adapters/components beneath this stable boundary.

## Relationship to other contracts

- Wisdom contribution is governed by `SUPERBRAIN/WISDOM-CONTRIBUTION-PROTOCOL.md`.
- Collective objects are governed by `SUPERBRAIN/COLLECTIVE-INTELLIGENCE-EVENT-SCHEMA.md`.
- Canonical memory remains governed by `.naya/codex/SMART-NOTES-AND-CIS-CONSTITUTION.md`.

**Acceptance principle:** a Superbrain can participate in the network without surrendering sovereignty.