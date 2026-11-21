-- Live filing: remembering trigger functions + their attachments — 2 functions
-- Supabase filing round 2026-11-21, Seat 2 (FUNCTIONS). Branch: supabase/filing-20261121-functions.
-- Source: LIVE definitions captured first-hand 2026-11-21 via Supabase Management API
--   POST /v1/projects/dahisasgpfvziswqvmvm/database/query — pg_get_functiondef / pg_get_triggerdef.
--   Read-only capture. No live writes were made. Definitions below are verbatim live
--   bytes (CREATE OR REPLACE FUNCTION as returned by pg_get_functiondef), grouped by
--   area; only this header and per-function provenance comments were added.
-- The Smart Ledger remembering machinery. Trigger attachments are created only if missing (no DROP anywhere); attachment rows below are the live pg_get_triggerdef bytes.
-- NOTE (scope limit, stated honestly): a fresh-apply diff against a test database is
--   NOT in scope for this round (coordinator brief). These migrations assume the
--   live-only tables they read exist — Seat 1's table filings on the same filing
--   branch supply them; apply tables first on a fresh rebuild.
-- Inventory: DATABASE.md §(b) B1/B2 + §(c); INVENTORY.md §3.2 / §3.4 (64 riders).

-- ---------------------------------------------------------------------------
-- items_state_changed()
--   live: public.items_state_changed — SECURITY INVOKER (default), language plpgsql, kind f, volatile v
--   purpose (DATABASE.md): The remembering trigger function: stamps state_changed_at on every item state change. (Smart Ledger)
--   captured: pg_get_functiondef(items_state_changed) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.items_state_changed()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
begin
  if new.state is distinct from old.state then
    new.state_changed_at := now();
  end if;
  return new;
end $function$;

-- ---------------------------------------------------------------------------
-- items_transition_log()
--   live: public.items_transition_log — SECURITY INVOKER (default), language plpgsql, kind f, volatile v
--   purpose (DATABASE.md): Logs every item state transition (from -> to + proof) into work_transitions. (Smart Ledger)
--   captured: pg_get_functiondef(items_transition_log) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.items_transition_log()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
begin
  if tg_op = 'INSERT' then
    insert into public.work_transitions(item_id, item_key, project_id, from_state, to_state, actor_seat, proof_url)
    values (new.id, new.item_key, new.project_id, null, new.state,
            coalesce(new.last_actor_seat, new.owner_seat, 'system'), new.evidence_url);
  elsif new.state is distinct from old.state then
    insert into public.work_transitions(item_id, item_key, project_id, from_state, to_state, actor_seat, proof_url)
    values (new.id, new.item_key, new.project_id, old.state, new.state,
            coalesce(new.last_actor_seat, new.owner_seat, 'system'), new.evidence_url);
  end if;
  return null;
end $function$;

-- ---------------------------------------------------------------------------
-- TRIGGER ATTACHMENTS (live pg_trigger / pg_get_triggerdef, 2026-11-21)
-- Each trigger is created ONLY IF MISSING on its table (no DROP, no replace).
-- live: trg_items_state_changed ON project_intel_items -> items_state_changed()
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_trigger
    WHERE tgname = 'trg_items_state_changed'
      AND tgrelid = 'public.project_intel_items'::regclass
      AND NOT tgisinternal
  ) THEN
    CREATE TRIGGER trg_items_state_changed BEFORE UPDATE ON public.project_intel_items FOR EACH ROW EXECUTE FUNCTION items_state_changed();
  END IF;
END $$;
-- live: trg_items_transition_log ON project_intel_items -> items_transition_log()
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_trigger
    WHERE tgname = 'trg_items_transition_log'
      AND tgrelid = 'public.project_intel_items'::regclass
      AND NOT tgisinternal
  ) THEN
    CREATE TRIGGER trg_items_transition_log AFTER INSERT OR UPDATE OF state ON public.project_intel_items FOR EACH ROW EXECUTE FUNCTION items_transition_log();
  END IF;
END $$;
