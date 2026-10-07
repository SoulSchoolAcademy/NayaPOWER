# 0015 — Security Acknowledgments V1

**Status:** living record. **Purpose:** every anonymous-surface or
privilege-elevating database posture that is INTENTIONAL is named here with
its internal gate and evidence. Silence is not acknowledgment: anything not
listed here and not in `tools/safety_grant_allowlist.json` is a hole, and
CI (`tools/safety_anon_grant_gate.py`) fails the build on new ones.

Born from the 2026-10-06 Security Advisor 27-warning classification
(#1606) and Naya 5's 2026-10-08 live follow-through verification.

## Intentional SECURITY DEFINER functions (authenticated EXECUTE)

Each function below runs with owner privileges but validates the caller
internally. The EXECUTE grant to `authenticated` is deliberate; the
function body is the real gate. Verified against repo migrations at main
`00f50bb` and live ACLs 2026-10-08.

| Function | Internal gate (evidence) | Live ACL 2026-10-08 |
|---|---|---|
| `nayanet_intelligence_commit(...)` | requires `auth.uid()`; validates authority grant via `nayanet_validate_authority_grant`; rejects subject mismatch | authenticated only |
| `nayanet_smart_connect(text)` / `(text,text)` | raises AUTH_REQUIRED without `auth.uid()`; door allowlist enforced | authenticated only |
| `nayanet_smart_disconnect(text)` | requires `auth.uid()`; participation lookup bound to caller | authenticated only |
| `nayanet_validate_authority_grant(...)` | read-only grant checks; it IS the validator | authenticated only |
| `nayanet_evolve_package_successor(...)` | **#1655**: `p_owner_id` must equal `auth.uid()` (EVOLVE_CALLER_NOT_OWNER) | authenticated only |
| `v7_create_smart_note(...)` | raises unless `auth.uid()` is set AND equals `p_user_id` (`20260905232321`, reaffirmed in latest definition `20260925042110`) | authenticated + anon (see below) |

## Anon-reachable DEFINER functions — live state 2026-10-08

| Function | Live anon? | Assessment |
|---|---|---|
| `v7_create_smart_note(...)` | YES (live ACL: PUBLIC + anon) | Fail-closed inside the function: raises without a JWT bound to `p_user_id`. Repo already revoked anon EXECUTE (`20260906082117`, `20260906082129`); live is behind (deploy pending). Residual risk: LOW while the internal gate stands. |
| `verify_smart_note(uuid)` | YES (live ACL: PUBLIC + anon) | **GENUINE HOLE (live only).** SECURITY DEFINER, WRITES (`smart_note_events.status`, `smart_note_receipts`) with NO auth check — any unauthenticated caller can flip event VERIFIED/INCOMPLETE and mint verification receipts. Repo revoked anon EXECUTE (`20260906082117`); live is behind (deploy pending). Residual risk: MEDIUM — verification receipts are trust-bearing. Remediation staged in `DRAFT-20261008-safety-live-remediation.sql` (needs Shawn's word). |
| `nayanet_execution_receipt_to_smart_ledger()` | NO (live ACL: postgres + service_role) | CLOSED. Revocation migration `20261006133000` applied live. |

## Intentional anon table reads

| Table | Grant | Gate |
|---|---|---|
| `nayanet_intelligence_publications` | anon SELECT | RLS enabled; policy `collective_publication_read` restricts to `status='published' AND consent_state='explicit'`. Consent-gated public surface by design. Also the sole entry in `tools/safety_grant_allowlist.json`. |

## Closed / disproven findings (2026-10-08 live verification)

- **"18 anon-reachable table policies"** — DISPROVEN. Live `pg_policies`: zero policies grant to `anon` across all 18 tables; RLS enabled on all 18. The 18x `auth_allow_anonymous_sign_ins` advisor WARNs are the AUTH CONFIG toggle (anonymous sign-ins allowed), not per-table policies. Remaining item: the toggle itself → dashboard setting, needs Shawn's word.
- **Trigger-function anon EXECUTE (#1/#2)** — CLOSED live.
- **`auth_leaked_password_protection`** — still disabled → dashboard toggle, needs Shawn's word (one-toggle hardening, no downside).

## Open items needing Shawn's explicit word (NOT auto-fixed)

1. **3 tables RLS-disabled with anon FULL grants** (`smart_note_events`, `smart_note_artifacts`, `smart_note_receipts`): live ACL `anon=arwdDxtm`, RLS off. Repo intent is RLS-on + owner policies + no anon/authenticated grants (`20260906143937`, `20260906082117`) — pure source↔live drift. Per Naya 1 (2026-10-08): needs Shawn's security decision, NOT auto-fixed (live capture path dependency). Staged remediation: `DRAFT-20261008-safety-live-remediation.sql`.
2. **Anonymous sign-ins toggle** (18x advisor WARN) — dashboard auth setting.
3. **Leaked-password protection** (1x advisor WARN) — dashboard auth setting.
4. **Deploy pipeline** — repo-side safety fixes (revocations, #1655) are merged but production application is pending; deploy auth needs Shawn.

## Fail-closed enforcement now in CI

- `tools/safety_anon_grant_gate.py` + `.github/workflows/safety-grant-gate.yml`: any new `GRANT ... TO anon/PUBLIC` in migrations without an allowlist entry fails the build. The `verify_smart_note` class of regression cannot land silently again.
