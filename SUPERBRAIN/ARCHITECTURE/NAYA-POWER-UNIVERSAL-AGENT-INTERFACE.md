# Naya Power — Universal Agent Interface V1

**Status:** IMPLEMENTATION BASELINE  
**Protocol:** `naya-power-agent-interface/v1`  
**Purpose:** Provide one vendor-neutral boundary through which an external AI model or agent can connect to the Naya Power Superbrain without creating a competing authority.

## Product principle

**Naya Power is the Superbrain operating system; the host model/agent is replaceable.**

A host may be ChatGPT, Claude, Gemini, an open-source model, a custom agent, a coding agent, or another capable AI system. The interface must not require a specific model vendor or storage vendor.

The host supplies model/tool capability. Naya Power supplies the operating intelligence layer: context, protocols, continuity, evidence discipline, learning, and compounding.

## Boundary ownership

The universal interface owns only **transport and normalization**.

It MUST NOT become the authority for:

- human mission qualification;
- priority selection;
- execution authorization;
- tool execution;
- evidence verification;
- Note Event persistence;
- Smart Note promotion;
- CSI compounding decisions;
- NayaNET federation authorization.

Existing canonical authorities retain those responsibilities.

## Canonical flow

`HOST AGENT → UNIVERSAL INTERFACE → EXISTING NAYA POWER AUTHORITIES`

A consequential path may continue through:

`MISSION → PRIORITY → TORCH → EXECUTION → EVIDENCE → LEARNING → PROMOTION → CSI → FUTURE EXECUTION`

The interface is a bridge into that chain, not a replacement for it.

## Minimum input contract

```json
{
  "protocol": "naya-power-agent-interface/v1",
  "agent_id": "stable-host-agent-identity",
  "host": "host-system-name",
  "model": "optional-model-identity",
  "session_id": "session-identity",
  "request_id": "unique-request-identity",
  "input": "human or agent request",
  "mission_ref": "optional opaque mission reference",
  "source_refs": ["optional provenance references"],
  "capabilities": ["available capabilities"],
  "constraints": ["known constraints"]
}
```

`request_id` binds a response to one request and provides the minimum correlation primitive needed for safe retries and duplicate-response handling. It is an identifier, not a persistence store.

`mission_ref` is intentionally opaque. The interface does not qualify or authorize a mission.

`source_refs` preserve provenance without making the interface a memory store.

## Result contract

Every result must carry the originating `agent_id`, `session_id`, and `request_id` so consumers can reject cross-session or cross-request confusion.

The interface may transport:

- `ACCEPTED`
- `COMPLETED`
- `FAILED`
- `UNKNOWN`

A `COMPLETED` transport status does **not** mean `VERIFIED`. Verification remains the responsibility of the canonical evidence/verification authority.

## Storage neutrality

Naya Power must not assume that all knowledge lives in GitHub.

Possible source substrates include:

- GitHub/Git repositories for code, laws, protocols, receipts, and versioned control state;
- Google Drive for human documents and knowledge;
- databases/object stores for application data;
- other authorized systems through adapters.

The substrate is not itself the intelligence authority. Meaningful knowledge must enter the canonical event/provenance architecture according to its governing authority.

## Production adapter requirements

Any production adapter must establish, outside this pure boundary:

1. authenticated host identity;
2. explicit human/organization authorization;
3. least-privilege capability scope;
4. provenance for imported information;
5. revocation;
6. auditability;
7. privacy/isolation boundaries;
8. replay/idempotency protection;
9. rate/resource controls;
10. safe handling of untrusted host output.

These are requirements for adapter integration, not reasons to expand this transport boundary into another authority.

## Acceptance

A compatible host must be able to connect without requiring Naya Power to know its vendor-specific internals.

The interface is successful when:

- identity is preserved;
- request correlation is preserved;
- request meaning is preserved;
- provenance is preserved;
- constraints are preserved;
- unknown remains unknown;
- no authority is silently transferred;
- no memory is written by the interface;
- no verification claim is manufactured;
- existing canonical authorities remain the owners of their decisions.

## Customer activation relationship

This interface is an **internal kernel boundary**, not one of the customer-facing activation documents.

The planned customer activation package remains separate. The 20 activation documents should be generated only after the activation contract and kernel interfaces are sufficiently stable to avoid repeated customer-facing rewrites.

The final activation package should teach a customer how to connect and activate Naya Power without exposing unnecessary internal architecture.

## Future implementation path

`universal envelope → host-specific adapters → authenticated integration → canonical mission/priority path → execution/evidence → learning/CSI`

Do not build one adapter per vendor until the neutral contract is proven. Prefer a small adapter interface plus conformance tests.
