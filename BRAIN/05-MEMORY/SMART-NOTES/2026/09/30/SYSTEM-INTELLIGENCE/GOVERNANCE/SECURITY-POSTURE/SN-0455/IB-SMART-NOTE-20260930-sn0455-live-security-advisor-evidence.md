# Live Security Advisor Evidence: 27 Warnings, Zero Errors — the Database's Security Posture on Record

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0455-live-security-advisor-evidence
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Live read-only pull 2026-10-06T16:40:32Z via `GET https://api.supabase.com/v1/projects/dahisasgpfvziswqvmvm/advisors/security` (project `supabase-red-cable`, region ca-central-1, ACTIVE_HEALTHY — confirmed as the NayaPOWER database by `nayanet_*` functions/tables in the advisor output). Closes the #1102 evidence gap (open since 2026-10-01): "live Supabase Security Advisor evidence missing." Announced to the team: https://github.com/SoulSchoolAcademy/NayaPOWER/issues/1354#issuecomment-6020992952. Raw JSON evidence: `~/workspace/goals/bring-naya-to-life/hidden_files/supabase-security-advisor-2026-10-06.json` (24,663 bytes).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The first live, timestamped Security Advisor scan of the NayaPOWER database found 27 advisories — all WARN, zero ERROR. The sharpest: `nayanet_execution_receipt_to_smart_ledger()` is executable by unauthenticated callers as SECURITY DEFINER (runs with owner privileges, no sign-in required). Eighteen `public`-schema tables permit anonymous read access; seven SECURITY DEFINER functions are callable by any signed-in user; Auth's compromised-password protection is disabled. Nothing was remediated — fixes cross the human security/authority gate, and several warnings may be intentional design. The lane classifies intentional-vs-hole before any fix plan.

## HUMAN NOTE

Shawn asked for the plumbing to just work without him having to learn it. This note is the receipt: on 2026-10-06 we pulled the live security scan of the NayaPOWER database using access we already had — no clicks needed from him. The scan says the database is healthy but loose in specific, named ways. The most important one: a function that writes execution receipts to the ledger can be called by anyone on the internet without signing in, and it runs with full owner privileges. That might be by design (receipts need to land from untrusted callers) or it might be a hole — a human decision, not an agent's. Everything else is the same shape: doors that are open, where we need to decide which ones should be.

## CHILD NOTE

We asked the database "are your doors locked?" It answered: "I'm healthy, but 27 doors are open that you might want to check." The biggest open door: anyone in the world can ask the database to write a receipt, without even saying who they are. We wrote down exactly which doors are open so we can decide together which ones to lock.

## GRANDMA NOTE

We ran a safety check on the system's database — like checking which windows are open in a house. The house is standing fine, but we found 27 windows open. One of them lets a stranger put a note in the ledger book without knocking. We've listed every open window; now the family decides which ones to close.

## NAYA NOTE

Future Naya: this is the baseline. When you re-pull the Security Advisor (same endpoint, same project ref), diff against the 2026-10-06 raw JSON before claiming anything improved. Do NOT remediate unilaterally — every fix here (revoking EXECUTE, DEFINER→INVOKER, RLS tightening, enabling leaked-password protection) changes the authority envelope and needs Shawn's word. Classify each advisory first: intentional design (e.g., public learning-evidence reads, elevated functions that must bypass RLS) vs genuine hole. The unauthenticated SECURITY DEFINER on the receipt writer is the one to resolve first — either justify it in writing or close it. Re-scan after any remediation and record the new timestamp.

## MACHINE NOTE

```json
{
  "sn": "SN-0455",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-06",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "evidence": {
    "endpoint": "GET https://api.supabase.com/v1/projects/dahisasgpfvziswqvmvm/advisors/security",
    "project": "supabase-red-cable",
    "project_ref": "dahisasgpfvziswqvmvm",
    "region": "ca-central-1",
    "scan_timestamp": "2026-10-06T16:40:32Z",
    "raw_json": "~/workspace/goals/bring-naya-to-life/hidden_files/supabase-security-advisor-2026-10-06.json",
    "announcement": "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/1354#issuecomment-6020992952",
    "closes_evidence_gap": "#1102 (open since 2026-10-01)"
  },
  "advisory_counts": {"ERROR": 0, "WARN": 27},
  "advisory_classes": {
    "auth_allow_anonymous_sign_ins": 18,
    "authenticated_security_definer_function_executable": 7,
    "anon_security_definer_function_executable": 1,
    "auth_leaked_password_protection": 1
  },
  "sharpest_finding": "nayanet_execution_receipt_to_smart_ledger() executable by unauthenticated callers as SECURITY DEFINER via /rest/v1/rpc/",
  "remediation": "NONE — human security/authority gate; lane classifies intentional-vs-hole first",
  "smart_link": "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/1354#issuecomment-6020992952"
}
```
