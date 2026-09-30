# NayaPOWER Smart Door / Smart Connect Contract V1

**Purpose:** one capability interface for external systems without creating a second authority or intelligence system.

## Core law

> **Doors expose what Naya can do. LAW decides what Naya may do. ACT does it. VERIFY checks what happened.**

A Smart Door MUST NOT own:
- authority;
- truth state;
- durable intelligence;
- identity;
- policy;
- learning.

## Minimal Door envelope

Each Door declares: provider, capabilities, operations, consequence class, required authority action, identity method, data classes, health, cost/rate hints, and audit/verification expectations.

## Examples

GitHub Connect, MCP Connect, AI Connect, Supabase/Data Connect, Email, Calendar, Voice, Web, and Naya-to-Naya all use the same contract.

A connected capability being technically available is **not** evidence that the current Naya is authorized to invoke it.

## Runtime flow

`NEED → CONNECT discovers Door → LAW evaluates permission → ACT invokes Door → OBSERVE → VERIFY`

The Door registry is discoverability metadata, not permission.
