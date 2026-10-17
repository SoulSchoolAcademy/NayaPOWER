# 🔱 NayaNET Smart App Rooms — Living Contract Registry

**Status:** HUMAN-DIRECTOR-DIRECTED TARGET CONTRACT — 2026-10-02  
**Runtime truth:** SPECIFICATION, NOT PRODUCTION PROOF

This directory is the canonical **room-specific layer** underneath:

- [Master Room Specification](../NAYANET-SMART-APP-ROOM-SPEC-V1.md)
- [Naya Design Masterclass](../NAYA-DESIGN-MASTERCLASS-V1.md)
- [Hub Design Contract](../DESIGN-CONTRACT.md)
- [Machine Room Contracts](../NAYANET-SMART-APP-ROOMS-V1.json)

## Purpose

The master specification defines the common laws.

The machine contract defines deterministic room identity and build metadata.

**These living records define how the Main Show and each individual room should actually be understood, composed, designed, interacted with, tested, scored and evolved.**

**Main Show law:** the Intelligent Hub Home is the entry projection of the Smart Feed experience. It is not a second intelligence surface, not a second store, and not a room-drawer destination.

They are not production proof. A room document can be complete while the corresponding interface is still unimplemented or runtime-unverified.

## Registry

| # | Room | Route | Contract |
|---|---|---|---|
| 00 | **Intelligent Hub Home / Main Show** | `/hub` | [Hub Home](./00-HUB-HOME.md) |
| 01 | **Smart Feed** | `/feed` | [Smart Feed](./01-FEED.md) |
| 02 | **Your Intelligence Today** | `/today` | [Your Intelligence Today](./02-TODAY.md) |
| 03 | **Your Reports** | `/reports` | [Your Reports](./03-REPORTS.md) |
| 04 | **Intelligent Library** | `/library` | [Intelligent Library](./04-LIBRARY.md) |
| 05 | **Smart Connect** | `/connect` | [Smart Connect](./05-CONNECT.md) |
| 06 | **Smart Ledger** | `/ledger` | [Smart Ledger](./06-LEDGER.md) |
| 07 | **Your Connections** | `/connections` | [Your Connections](./07-CONNECTIONS.md) |
| 08 | **Smart Lists** | `/lists` | [Smart Lists](./08-LISTS.md) |
| 09 | **Smart Mail** | `/mail` | [Smart Mail](./09-MAIL.md) |
| 10 | **Smart Spaces** | `/spaces` | [Smart Spaces](./10-SPACES.md) |
| 11 | **Settings** | `/settings` | [Settings](./11-SETTINGS.md) |

## Living-record law

Every room document carries:

**intent → experience → surface → intelligence → interaction → states → responsive → accessibility → performance → metrics → proof → open decisions → working notes**

When a room changes, update the room record with:

**DATE → OBSERVATION → EVIDENCE → DECISION → CHANGE → SCORE EFFECT → LESSON → NEXT TEST**

## Governance

- A room document may become more specific than the master spec.
- It may **not** contradict the master design law or canonical runtime truth.
- Open decisions remain open until authoritative evidence or Human Director decision closes them.
- A beautiful render does not graduate a room.
- A room cannot graduate below **D1 = 10.0** and **D2–D8 ≥ 9.5**.
- No score may be asserted without evidence.
- All material defects go to **Issue #554**.
- Graduation qualification is governed by **Issue #1310**.

## Build order

The current dependency-aware build sequence remains governed by the master room specification. Room documents do not independently reorder the product unless evidence changes the dependency graph.

> **One house. One Main Show. Eleven rooms. One intelligence. Twelve living contracts.**
