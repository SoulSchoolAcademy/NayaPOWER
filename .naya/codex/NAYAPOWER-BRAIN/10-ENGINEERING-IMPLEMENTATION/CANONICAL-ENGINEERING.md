# 10 — Canonical Engineering & Implementation

## Engineering principle
A design is not complete because it exists in Markdown. The system must work through the real execution boundary and be independently verified.

## Repository
GitHub is the primary engineering workspace and durable implementation record. Contracts, control-plane state, code, tests, projections and evidence have different authority levels.

## TDD execution
For behavior changes:
1. establish current main;
2. restore the relevant canonical contracts;
3. create or identify the smallest failing assertion;
4. make the smallest compatible repair;
5. rerun focused tests;
6. inspect the final diff for identity/schema/projection violations;
7. verify runtime when required;
8. record evidence and hand off.

## Canonical receiver
The live canonical Smart Note receiver is the identity boundary. Repository code must never manufacture IB identities locally.

## Proof boundaries
Source → build → deploy → live runtime → observed behavior are separate evidence boundaries.

## Current engineering objective
Converge the working Hub, canonical Smart Note/IB lifecycle, retrieval and sender→receiver→Hub path into one coherent user journey while preserving governance and continuity.

## Anti-patterns
No duplicate authorities. No alternate Smart Note format. No UI theater. No runtime claim from source inspection alone. No polish before working architecture. No repeating failed routes without new evidence. No acknowledgement-only completion when executable work is known.
