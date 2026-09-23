# Hub Room System — System Update

Date: 2026-09-23
Repository: SoulSchoolAcademy/NayaPOWER
Scope: Canonical NayaNET Hub middle-workspace product system

## Decision
The ten Hub features are now a defined room system. Each feature has a durable product specification stored in GitHub, and the Hub renders that feature as software inside the middle workspace.

## Why
The Hub must evolve without repeatedly losing earlier work. The implementation agent must have an authoritative contract for what belongs in each room, how it behaves, what data it may use, and what must remain untouched.

## Shell decision
The permanent right-side Naya rail is not a required part of the room architecture. Naya should remain present as a compact identity/assistant block in the upper-right area. Removing unused right-rail real estate is an approved product direction, but it is a shell-level change and must be handled separately from individual room implementation so room work cannot accidentally destabilize the shell.

The middle workspace beneath the search/header region is the primary application canvas. A room should feel like real software displayed there, not a separate website or page.

## Seven Smart Connect doors
GitHub App, MCP, REST/OpenAPI, Webhooks, SDK, A2A, and MCP Apps. Each door must eventually expose connection state, configuration path, verification path, authority boundary, and evidence.

## Sequential implementation law
Rooms are implemented one at a time in registry order unless explicitly re-authorized. When a room reaches PROVEN/FROZEN, its contract and proof become a checkpoint. Later work may extend shared infrastructure, but may not silently remove, replace, or visually regress a frozen room.

## Required agent behavior
When asked to implement a room, the implementation agent must:
- read the registry and system update first;
- read the target room contract;
- inspect current Hub source rather than guessing;
- preserve already-frozen room behavior;
- make bounded changes;
- test the target room and the Hub shell;
- report exact evidence;
- update the registry only with observed truth.

## First implementation target
01 — Your Intelligence Today.
