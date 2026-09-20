# NAYA ACTIONS

**Status:** CANONICAL EXECUTION RECORD LAYER

`.naya/actions/` contains durable `NAYA_ACTION_V1` records: the atomic objects of governed intelligence execution.

## Authority

This directory does not create a new constitution or governance state machine.

It is subordinate to:

1. `.naya/codex/11-RUNTIME-CONSTITUTION.md`
2. `.naya/control-plane/MAP.json`
3. `.naya/control-plane/STATE.json`
4. `.naya/control-plane/BLOCKS.json`
5. `.naya/control-plane/PROOF.json`
6. `.naya/control-plane/GOVERNANCE-KERNEL.json`
7. Existing canonical execution/continuity laws

## Purpose

A `NAYA_ACTION_V1` record preserves:

`MISSION → INTENT → UNDERSTANDING → AUTHORITY → PLAN → ACTION → OBSERVATION → EVIDENCE → VERIFICATION → RESULT → LEARNING → MEMORY → PROVENANCE → NEXT ACTION`

The action record is the durable bridge between execution and successor continuity.

## State

The `state` field uses the existing NayaPOWER governance states. It does not define a competing state machine. Legal transitions remain governed by `.naya/control-plane/GOVERNANCE-KERNEL.json`.

## Rule

An action must never claim verification without claim-appropriate evidence. A blocked or unknown runtime boundary remains blocked or unknown. Historical evidence cannot certify a newer source state.

## First proof

`NAYA-ACTION-2026-09-15-SMART-BOARD-001.json` is the first NAYA_ACTION_V1 proof record. It captures the Smart Board mission, the prior mission-invalid prototype route, the resulting lesson, and the single next executable inspection action.
