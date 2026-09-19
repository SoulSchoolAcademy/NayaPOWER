# ACTION 10 — PRODUCTION CLOSURE

## MISSION

Run the final real-human authenticated acceptance proof. Do not replace it with database simulation.

## A→T

A. Human A authenticates.
B. A creates shared Space.
C. Space creation Activity/Ledger observed.
D. Human B authenticates separately.
E. B discovers the shared Space.
F. B JOINs.
G. Membership survives reload.
H. A/B explicitly save each other as Connections.
I. Connection provenance is correct.
J. Connection is added to Smart List.
K. List survives reload.
L. List removal leaves Connection intact.
M. Valid authority is established.
N. Smart Mail sends through Cloudflare/Supabase.
O. Receiver verifies.
P. Receipt/cognition/Ledger lineage is observed.
Q. Identical replay produces no duplicate.
R. B leaves/relation is revoked.
S. Mail/access is attempted again.
T. Server denies the now-ineligible action.

Then:
- unrelated C attempts protected operations;
- verify denial and no leakage;
- record exact IDs/timestamps;
- update all feature records;
- update Team Naya;
- mark LIVE VERIFIED only if every boundary passes.

## HARD RULES

No synthetic final proof. No credential extraction. No UI-only success. No database-only substitute. No authority bypass.

If browser control is unavailable, record exactly that tooling boundary and keep the subsystem NOT VERIFIED.
