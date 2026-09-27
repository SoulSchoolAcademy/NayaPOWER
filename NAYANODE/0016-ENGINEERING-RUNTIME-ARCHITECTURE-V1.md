# Engineering & Runtime Architecture V1

## Purpose

Align GitHub, runtime, database, tests, and deployments with the intelligence architecture.

## Source-of-truth hierarchy

1. governed runtime truth;
2. canonical persistent intelligence;
3. canonical engineering contracts;
4. implementation;
5. projections/interfaces;
6. historical artifacts.

A deployment artifact cannot redefine canonical intelligence.

## Repository role

GitHub is the canonical engineering workspace and continuity surface for implementation.

It must expose:

- architecture;
- machine manifest;
- kernel;
- tests;
- current state;
- proof receipts;
- active work;
- known unknowns.

## Runtime role

Runtime executes the governed algorithm.

It must not invent missing state or silently recover authority.

## Database role

The database persists governed intelligence and state.

It is not itself proof of cognition.

## CI role

CI establishes reproducible machine evidence.

A green build proves the tested property, not the entire system.

## Production role

Production proof requires evidence from the real production boundary.

## Current P0

Resolve legitimate identity continuity for the canonical nine-node owner before changing the owner or bypassing access controls.
