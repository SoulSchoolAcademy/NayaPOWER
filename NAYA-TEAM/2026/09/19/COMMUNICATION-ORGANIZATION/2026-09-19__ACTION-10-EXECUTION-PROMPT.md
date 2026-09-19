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


## EXECUTION UPDATE — 2026-09-19 10:24 PDT

### DONE
- Browser control is now genuinely available through the existing isolated authenticated Wave browser CDP session on the authorized desktop.
- Human A authenticated session was observed on the deployed Cloudflare Hub.
- A real shared Space was created through the authenticated runtime: `04ee4dc8-bc73-47df-a1de-162570f6a56e`.
- Space creation produced a real `SMART_SPACE` Ledger event: `294b64e3-f77c-465a-855a-79ae613b5b7e` at `2026-09-19T17:24:06.677743Z`.
- Owner membership was created: `b46d73d4-a678-4197-b4fa-8687359efc5a`, status `active`, source `space_owner`.
- A production RLS defect was found during live Space context retrieval: recursive `nayanet_space_members_shared_read` policy.
- The defect was fixed and applied as migration `20260919172900_fix_space_members_rls_recursion`.
- Source migration committed to GitHub at `a59cf18cf8c735307b6388c6f2dc9fa695b4dec8`.
- Post-fix live Cloudflare Space projection succeeds with no recursion error.

### NOT PROVEN
- Distinct authenticated Human B session.
- B discovery/JOIN/reload membership proof.
- A↔B mutual Connections/provenance.
- Smart List add/remove persistence.
- Valid authority establishment between A/B.
- Real receiver-side Smart Mail verification.
- Replay idempotency across the real A/B transaction.
- Leave/revoke denial.
- Unrelated C isolation.

### CURRENT BLOCKER
The available authorized desktop currently exposes one legitimate authenticated NayaNET session through the isolated Wave browser (A). There is no second pre-authenticated legitimate human session available to execute B. No credentials were extracted or reused, and no synthetic B was created.

### CONTINUATION REQUIREMENT
Provide a second legitimate authenticated human session in a separate browser profile/session. Once that session exists, continue immediately from the existing Space ID above; do not recreate the Space and do not substitute database simulation.

### HARD RULE
The subsystem remains **NOT VERIFIED** until A→T passes with a distinct authenticated B and the unauthorized C denial proof.