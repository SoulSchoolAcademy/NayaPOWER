# 04 — Smart Connect

## Product job
Give humans one clear, governed place to connect NayaNET to external systems without confusing connection with authority.

## Seven doors
1. GitHub App
2. MCP
3. REST/OpenAPI
4. Webhooks
5. SDK
6. A2A
7. MCP Apps

## Presentation
A prominent connection room with seven large door cards/rows. Each has purpose, current state, Connect, Configure, Verify, authority scope, privacy note, and evidence/provenance.

## State model
NOT CONNECTED → CONNECTED → AUTHENTICATED → AUTHORIZED → HEALTHY.
Also support DEGRADED, BLOCKED, REVOKED, EXPIRED, FAILED, DISCONNECTED.

## Rules
Connection does not grant authority. Authentication does not grant authorization. Verification uses actual evidence. Credentials/secrets are never displayed as content.

## Proof
Each door reports observed state and verification evidence. The room must not imply production readiness for an uninstalled or unverified integration.
