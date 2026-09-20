# NayaNET Durable Cognition Backend

## Status
IMPLEMENTED · VERIFIED IN SUPABASE

## Project

Supabase project: `supabase-red-cable`
Project ref: `dahisasgpfvziswqvmvm`

## Purpose

Provide the durable counterpart to the Hub's browser cognition state so the persistent cognitive execution protocol is not limited to one browser's localStorage.

## Tables

### `public.nayanet_project_cognition_state`

One current state per authenticated user and project.

- `user_id`
- `project_id`
- `revision`
- `state` JSONB
- `status`
- `created_at`
- `updated_at`

Unique boundary: `(user_id, project_id)`.

### `public.nayanet_execution_receipts`

Immutable execution receipts tied to the cognition revision.

- `user_id`
- `project_id`
- `revision`
- `action`
- `expected_result`
- `observed_result`
- `status`
- `evidence` JSONB
- `learning` JSONB
- `created_at`

Unique boundary: `(user_id, project_id, revision)`.

## Atomic transition

`public.nayanet_commit_cognition(...)` performs optimistic revision checking, advances the cognition revision, writes the new state, and records the execution receipt as one database transaction.

A stale writer fails with `COGNITION_REVISION_CONFLICT` instead of silently overwriting newer state.

## Security

Both tables use Row Level Security and are restricted to the authenticated owner's `user_id = auth.uid()` boundary. The commit function is `SECURITY INVOKER` and executable by authenticated users.

## Truth boundary

The backend is infrastructure evidence, not proof that the Hub is already connected to it. Frontend authentication and exact runtime wiring remain separate release gates.

## Success condition

A successor Naya must be able to load the latest revision, identify the prior action/result/evidence/learning, continue the next action, and fail safely on stale revision writes.
