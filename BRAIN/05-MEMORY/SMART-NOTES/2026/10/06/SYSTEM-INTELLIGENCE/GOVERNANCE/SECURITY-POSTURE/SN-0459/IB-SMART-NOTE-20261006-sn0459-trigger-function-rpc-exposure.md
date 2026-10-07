# A Trigger Function in the Public Schema Is an RPC Endpoint by Accident

**Intelligent Block:** IB-SMART-NOTE-20261006-sn0459-trigger-function-rpc-exposure
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Live Supabase Security Advisor pull 2026-10-06T16:40:32Z flagged `anon_security_definer_function_executable` on `public.nayanet_execution_receipt_to_smart_ledger()`; source traced to migration `20260930233038` (`create or replace function ... returns trigger ... security definer` + `create trigger ... execute function`). Classified on #1606; announced #1354.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A trigger function placed in the `public` schema with default EXECUTE grants becomes an RPC endpoint anyone can call — even though it was designed to run only as a trigger. The function executes with owner privileges and a NULL `NEW` record: undefined behavior. Trigger functions never need EXECUTE grants (triggers fire regardless), so the fix is always `REVOKE EXECUTE ... FROM anon, authenticated, PUBLIC`. Audit every `returns trigger` function in `public` for this pattern.

## HUMAN NOTE

We found a function whose only job is to run automatically when a receipt is inserted — but because it lives in the public schema, anyone on the internet could call it directly, with full owner privileges, outside its intended context. Nobody designed it that way; it happened by default. The lesson: in Postgres, anything in the public schema is an API endpoint unless you say otherwise. Trigger functions should either live outside the exposed schema or have their EXECUTE grants explicitly revoked — they don't need them to do their job.

## CHILD NOTE

We built a robot that stamps receipts when they arrive. But we left the robot's door open, so strangers could walk up and press its buttons themselves. The fix is simple: the robot doesn't need its door open to do its job — the receipts come to it automatically. Always lock the doors that don't need to be open.

## GRANDMA NOTE

A machine in the back room was supposed to work only when the front desk sent it papers. But its door opened to the street, so anyone could walk in and push its buttons. We learned: lock every door that doesn't need to be open, especially the ones nobody remembers opening.

## NAYA NOTE

Future Naya: when you see `SECURITY DEFINER` + `returns trigger` + `public` schema in the same function, that's the pattern — flag it before the advisor does. The check is one query against `pg_proc` (prokind = 'f', prosecdef, prorettype = 'trigger'::regtype, pronamespace = 'public'::regnamespace). The fix never breaks the trigger: `REVOKE ALL ON FUNCTION x() FROM anon, authenticated, PUBLIC` leaves trigger firing untouched. Add this to the pre-deploy checklist.

## MACHINE NOTE

```json
{
  "sn": "SN-0459",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-06",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "pattern": "SECURITY DEFINER + RETURNS TRIGGER + public schema + default EXECUTE grants = accidental RPC endpoint",
  "instance": "public.nayanet_execution_receipt_to_smart_ledger()",
  "source": "supabase/migrations/20260930233038_restore_smart_ledger_value_receipt_runtime_v2_1.sql",
  "evidence": "supabase-security-advisor-2026-10-06.json (anon_security_definer_function_executable, observed 2026-10-06T16:40:32Z)",
  "fix": "REVOKE EXECUTE ON FUNCTION public.nayanet_execution_receipt_to_smart_ledger() FROM anon, authenticated, PUBLIC",
  "fix_status": "QUEUED — needs Shawn's explicit word (authority-envelope change)",
  "detection_query": "select proname from pg_proc where prosecdef and prorettype = 'trigger'::regtype and pronamespace = 'public'::regnamespace",
  "smart_link": "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/1606#issuecomment-6021285876"
}
```
