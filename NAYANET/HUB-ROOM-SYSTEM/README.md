# NayaNET Hub Room System

This directory is the durable product contract and working-memory system for the software rooms rendered inside the canonical NayaNET Hub middle workspace.

These are not separate pages. They are feature applications projected into the Hub workspace while the canonical Hub shell remains intact.

## Immutable shell contract
- Preserve the canonical Hub shell, visual language, navigation, identity, authentication, runtime boundary, and release contract.
- The middle workspace is the application surface.
- The left navigation is navigation, not a second application shell.
- Naya is represented by the compact identity block in the upper-right corner; a permanent full-height right rail is not required by this contract.
- The room may use the full available width beneath the search/header region.
- Do not remove, regress, or redesign previously completed rooms when implementing a later room.
- A room implementation must be additive and bounded to its own feature contract.

## Durable working memory
`CURRENT-WORKING-MEMORY.md` is the active intelligence memory for the current Hub room sub-project.

Its job is to preserve high-value conversation intelligence that would otherwise disappear when a chat ends: decisions, reasoning, discoveries, corrections, constraints, rejected approaches, unresolved questions, and next actions.

**The human does not need to say “take a note” for durable project intelligence to be captured.** During active project work, Naya should recognize when a conversation has produced information that future implementation or recall materially depends on and distill it into the appropriate durable location.

Working memory is organized by project → room → workstream. It informs implementation but never overrides canonical source or verified evidence.

## Memory / truth hierarchy
1. System truth — architecture and governance.
2. Project truth — Hub shell, runtime, release and proof contracts.
3. Room truth — Product + UX + Intelligence Contract.
4. Working memory — active reasoning and decisions.
5. Evidence — source SHAs, proof runs, artifacts, runtime observations and receipts.

When these conflict, verified evidence and explicit current decisions govern.

## Room list
1. Your Intelligence Today
2. Your Reports
3. Intelligent Library
4. Smart Connect
5. Smart Ledger
6. Your Connections
7. Smart Lists
8. Smart Mail
9. Smart Spaces
10. Settings

## Smart Connect technical doors
GitHub App, MCP, REST/OpenAPI, Webhooks, SDK, A2A, MCP Apps.

## Delivery law
Every room moves through: SPECIFIED → IMPLEMENTED → DEPLOYED → PROVEN → FROZEN.

A later room cannot erase or silently redefine an earlier room. The room registry and completed-room ledger are the control record.

## Agent operating law
Before acting on a room:
1. Read `CURRENT-WORKING-MEMORY.md`.
2. Read `ROOM-REGISTRY.md`.
3. Read the target room contract.
4. Inspect current implementation and current evidence.
5. Make the smallest causal change that advances the target.
6. Prove the target and confirm frozen-room regression safety.
7. Distill newly learned durable intelligence back into working memory and the relevant contract.

Never rely on conversation memory alone when the information can be made durable in the repository.
