# Dependency Order V1

**Status:** CANONICAL BUILD CONTRACT

## Required causal order
`IDENTITY → GOVERNANCE → SCHEMA → MANIFEST → PERSISTENCE → RETRIEVAL → RELATIONSHIP ROUTING → ACTION → OBSERVATION → VERIFICATION → LEARNING → SUCCESSOR → INTERFACE`

## Law
Downstream status cannot be PASS merely because an upstream artifact is documented. Every gate needs its own current evidence.

## Critical chain
`PERSISTENCE + IDENTITY + GOVERNANCE → RETRIEVE → APPLY → ACT → OBSERVE → VERIFY → LEARN → HANDOFF → CONTINUE`

## Acceptance
A dependency graph names the artifact/runtime boundary for each edge and prevents false downstream PASS when a critical upstream gate is UNKNOWN or BLOCKED.
