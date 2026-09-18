# Naya Dream / Replay P0

Naya Dream is the Naya-native replay boundary for controlled counterfactual reasoning over verified history.

P0 is deliberately conservative:
- authenticated ownership comes from Supabase auth.uid();
- source history comes from canonical cognition events and execution receipts;
- replay never mutates source history;
- replay performs no action;
- replay grants no authority;
- replay is SIMULATED;
- persistence is idempotent per human and idempotency key;
- RLS limits replay rows to their owner.

Flow:
NAME-FIRST identity
→ authenticated Supabase user
→ owner-scoped cognition
→ source event
→ optional matching execution receipt
→ immutable world snapshot
→ baseline/counterfactual replay
→ deterministic verification record
→ owner-scoped persistence

P0 is not autonomous self-improvement, production mutation, or promotion.
Those future capabilities remain behind Naya Power governance.

The production Edge Function naya-dream-replay was inspected directly and mirrored into this repository so GitHub becomes the auditable source-of-truth for the deployed function.
