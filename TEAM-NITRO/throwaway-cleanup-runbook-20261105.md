# Throwaway Smart Link cleanup — runbook (2026-11-05)

Proven 2026-11-05 18:43Z by the network test (claim `test-net-proof-k7q2`).
Zero residue verified: routes 47 → 48 → 47, row gone, no resurrection after 15s.

## The order that works

1. **Delete the `smart_links` row FIRST, through the Supabase mgmt query path.**
   The anon key CANNOT delete `smart_links` rows (42501 permission denied).
2. **Then delete the Cloudflare route.**
3. **Re-check after 15 seconds** (5 reconciler passes): route count back to baseline, row gone.

## Why the order matters

The reconciler is create-only and watches the `smart_links` table. If the route
is deleted while the row still exists, the reconciler resurrects the route within
seconds — the cleanup undoes itself. Row first, route second, and it stays gone.

## Never

- Never delete the route first.
- Never leave a throwaway row behind — a live row + a live route is a live link.
- Never use the anon key for the row delete; use the mgmt query path.
