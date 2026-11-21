-- Live filing: trigger-helper functions the checker found unfiled — 8 functions
-- Supabase filing round 2026-11-21, Seat 4 (TRIGGER HELPERS, follow-on to CHECKER-VERDICT FAIL).
-- Branch: supabase/filing-20261121-functions.
-- Source: LIVE definitions captured first-hand 2026-11-21 via Supabase Management API
--   POST /v1/projects/dahisasgpfvziswqvmvm/database/query — pg_get_functiondef / pg_get_triggerdef.
--   Read-only capture. No live writes were made. Definitions below are verbatim live
--   bytes (CREATE OR REPLACE FUNCTION as returned by pg_get_functiondef), in the
--   checker's table order; only this header and per-function provenance comments added.
-- WHY THIS FILE EXISTS (CHECKER-VERDICT.md): Seat 1's table migrations create these
--   10 trigger attachments inside IF NOT EXISTS (pg_trigger...) guards — the guard
--   protects replays but NOT a fresh build, where the guard passes and
--   CREATE TRIGGER ... EXECUTE FUNCTION <missing>() errors at the first one
--   (payments_fill_owner, in 180000). This file's 170000 timestamp puts it BEFORE
--   the table files (180000+) in fresh-apply order, so all 8 functions are defined
--   before the first table trigger guard runs.
-- NOTE: naya_notes_touch_updated_at carries a SECOND live attachment the checker
--   table did not list — naya_notes_touch_updated_at_bu BEFORE UPDATE ON naya_notes
--   (found by Seat 4's own q2 read, 9 live rows, not 8). It is filed here too: the
--   naya_notes table already has repo source (20261022204500_naya_notes_v1.sql,
--   which creates NO trigger), so the guarded CREATE below is safe on a fresh
--   apply and closes a real live-vs-repo gap instead of leaving it.
-- NOTE: trg_file_note calls auto_categorize_note (filed by Seat 2 in 190004). That is
--   safe at creation time: PL/pgSQL bodies are not resolved until first execution,
--   so no ordering problem on a fresh apply.
-- NOTE (scope limit, stated honestly): a fresh-apply diff against a test database is
--   NOT in scope for this round (coordinator brief).
-- Inventory: CHECKER-VERDICT.md §"The 8 unfiled trigger functions"; DATABASE.md §(c).

-- ---------------------------------------------------------------------------
-- guard_hub_smart_notes_delete()
--   live: public.guard_hub_smart_notes_delete — SECURITY INVOKER (default), language plpgsql, kind f, volatile v
--   purpose: Guard on hub_smart_notes deletes: trigger hub_smart_notes_delete_guard on hub_smart_notes. (Hub smart notes)
--   captured: pg_get_functiondef(guard_hub_smart_notes_delete) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.guard_hub_smart_notes_delete()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$ BEGIN IF current_setting('naya.feed_maintenance', true) IS DISTINCT FROM 'on' THEN RAISE EXCEPTION 'hub_smart_notes deletes are guarded: set naya.feed_maintenance=on in a deliberate maintenance session'; END IF; RETURN OLD; END; $function$;

-- ---------------------------------------------------------------------------
-- naya_notes_touch_updated_at()
--   live: public.naya_notes_touch_updated_at — SECURITY INVOKER (default), language plpgsql, kind f, volatile v
--   purpose: Stamp updated_at on media_notes AND naya_notes changes: triggers media_notes_touch on media_notes + naya_notes_touch_updated_at_bu on naya_notes. (Media notes / Naya Notes)
--   captured: pg_get_functiondef(naya_notes_touch_updated_at) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.naya_notes_touch_updated_at()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
begin
  new.updated_at = now();
  return new;
end $function$;

-- ---------------------------------------------------------------------------
-- touch_updated_at()
--   live: public.touch_updated_at — SECURITY INVOKER (default), language plpgsql, kind f, volatile v
--   purpose: Stamp updated_at on smart_notes changes: trigger trg_smart_notes_touch on smart_notes. (Smart notes)
--   captured: pg_get_functiondef(touch_updated_at) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.touch_updated_at()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$function$;

-- ---------------------------------------------------------------------------
-- trg_file_note()
--   live: public.trg_file_note — SECURITY INVOKER (default), language plpgsql, kind f, volatile v
--   purpose: Auto-file a smart note on insert/update (calls auto_categorize_note, filed in 190004): trigger trg_auto_file_note on smart_notes. (Smart Vault auto-file)
--   captured: pg_get_functiondef(trg_file_note) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.trg_file_note()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
BEGIN
  PERFORM public.auto_categorize_note(NEW.id);
  RETURN NEW;
END;
$function$;

-- ---------------------------------------------------------------------------
-- payments_fill_owner()
--   live: public.payments_fill_owner — SECURITY DEFINER, language plpgsql, kind f, volatile v
--   purpose: BEFORE INSERT on payments: fill the owner from the payment link/page. SECURITY DEFINER. (Payments)
--   captured: pg_get_functiondef(payments_fill_owner) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.payments_fill_owner()
 RETURNS trigger
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
declare
  p record;
begin
  select owner_alias, owner_id into p
  from public.payment_links where id = new.link_id;
  if not found then
    raise exception 'payment link % does not exist', new.link_id
      using errcode = 'foreign_key_violation';
  end if;
  new.owner_alias := p.owner_alias;
  new.owner_id := p.owner_id;
  return new;
end;
$function$;

-- ---------------------------------------------------------------------------
-- work_items_state_changed()
--   live: public.work_items_state_changed — SECURITY INVOKER (default), language plpgsql, kind f, volatile v
--   purpose: Stamp state_changed_at on every work_items state change: trigger trg_work_items_state_changed on work_items. (Smart Ledger / project ops)
--   captured: pg_get_functiondef(work_items_state_changed) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.work_items_state_changed()
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
-- work_items_transition_log()
--   live: public.work_items_transition_log — SECURITY INVOKER (default), language plpgsql, kind f, volatile v
--   purpose: Log every work_items state transition into work_transitions: trigger trg_work_items_transition_log on work_items. (Smart Ledger / project ops)
--   captured: pg_get_functiondef(work_items_transition_log) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.work_items_transition_log()
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
-- work_items_packet_law()
--   live: public.work_items_packet_law — SECURITY INVOKER (default), language plpgsql, kind f, volatile v
--   purpose: Enforce the packet law on work_items (constraint trigger): trigger work_items_packet_law_trg on work_items. (Smart Ledger / project ops)
--   captured: pg_get_functiondef(work_items_packet_law) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.work_items_packet_law()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
DECLARE st text;
BEGIN
  SELECT state INTO st FROM public.work_items WHERE id = NEW.id;
  IF st = 'needs_shawn' AND NOT EXISTS (
       SELECT 1 FROM public.queue_packets qp
       WHERE qp.item_id = NEW.id
          OR (qp.project_id = NEW.project_id AND qp.item_key = NEW.item_key)) THEN
    RAISE EXCEPTION 'needs_shawn refused: no queue packet for item %', NEW.item_key;
  END IF;
  RETURN NULL;
END $function$;

-- ---------------------------------------------------------------------------
-- TRIGGER ATTACHMENTS (live pg_trigger / pg_get_triggerdef, 2026-11-21)
-- Each trigger is created ONLY IF MISSING on its table (no DROP, no replace).
-- Seat 1's table migrations (180000+) create the same attachments inside their own
-- IF NOT EXISTS guards; on a fresh apply this file runs first, so those guards see
-- the trigger already present and skip. On a replay against live, these guards skip
-- because the triggers already exist live.
-- live: hub_smart_notes_delete_guard ON hub_smart_notes -> guard_hub_smart_notes_delete()
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_trigger
    WHERE tgname = 'hub_smart_notes_delete_guard'
      AND tgrelid = 'public.hub_smart_notes'::regclass
      AND NOT tgisinternal
  ) THEN
    CREATE TRIGGER hub_smart_notes_delete_guard BEFORE DELETE ON public.hub_smart_notes FOR EACH ROW EXECUTE FUNCTION guard_hub_smart_notes_delete();
  END IF;
END $$;
-- live: media_notes_touch ON media_notes -> naya_notes_touch_updated_at()
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_trigger
    WHERE tgname = 'media_notes_touch'
      AND tgrelid = 'public.media_notes'::regclass
      AND NOT tgisinternal
  ) THEN
    CREATE TRIGGER media_notes_touch BEFORE UPDATE ON public.media_notes FOR EACH ROW EXECUTE FUNCTION naya_notes_touch_updated_at();
  END IF;
END $$;
-- live: naya_notes_touch_updated_at_bu ON naya_notes -> naya_notes_touch_updated_at()
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_trigger
    WHERE tgname = 'naya_notes_touch_updated_at_bu'
      AND tgrelid = 'public.naya_notes'::regclass
      AND NOT tgisinternal
  ) THEN
    CREATE TRIGGER naya_notes_touch_updated_at_bu BEFORE UPDATE ON public.naya_notes FOR EACH ROW EXECUTE FUNCTION naya_notes_touch_updated_at();
  END IF;
END $$;
-- live: trg_smart_notes_touch ON smart_notes -> touch_updated_at()
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_trigger
    WHERE tgname = 'trg_smart_notes_touch'
      AND tgrelid = 'public.smart_notes'::regclass
      AND NOT tgisinternal
  ) THEN
    CREATE TRIGGER trg_smart_notes_touch BEFORE UPDATE ON public.smart_notes FOR EACH ROW EXECUTE FUNCTION touch_updated_at();
  END IF;
END $$;
-- live: trg_auto_file_note ON smart_notes -> trg_file_note()
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_trigger
    WHERE tgname = 'trg_auto_file_note'
      AND tgrelid = 'public.smart_notes'::regclass
      AND NOT tgisinternal
  ) THEN
    CREATE TRIGGER trg_auto_file_note AFTER INSERT ON public.smart_notes FOR EACH ROW EXECUTE FUNCTION trg_file_note();
  END IF;
END $$;
-- live: payments_fill_owner ON payments -> payments_fill_owner()
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_trigger
    WHERE tgname = 'payments_fill_owner'
      AND tgrelid = 'public.payments'::regclass
      AND NOT tgisinternal
  ) THEN
    CREATE TRIGGER payments_fill_owner BEFORE INSERT ON public.payments FOR EACH ROW EXECUTE FUNCTION payments_fill_owner();
  END IF;
END $$;
-- live: trg_work_items_state_changed ON work_items -> work_items_state_changed()
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_trigger
    WHERE tgname = 'trg_work_items_state_changed'
      AND tgrelid = 'public.work_items'::regclass
      AND NOT tgisinternal
  ) THEN
    CREATE TRIGGER trg_work_items_state_changed BEFORE UPDATE ON public.work_items FOR EACH ROW EXECUTE FUNCTION work_items_state_changed();
  END IF;
END $$;
-- live: trg_work_items_transition_log ON work_items -> work_items_transition_log()
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_trigger
    WHERE tgname = 'trg_work_items_transition_log'
      AND tgrelid = 'public.work_items'::regclass
      AND NOT tgisinternal
  ) THEN
    CREATE TRIGGER trg_work_items_transition_log AFTER INSERT OR UPDATE OF state ON public.work_items FOR EACH ROW EXECUTE FUNCTION work_items_transition_log();
  END IF;
END $$;
-- live: work_items_packet_law_trg ON work_items -> work_items_packet_law()
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_trigger
    WHERE tgname = 'work_items_packet_law_trg'
      AND tgrelid = 'public.work_items'::regclass
      AND NOT tgisinternal
  ) THEN
    CREATE CONSTRAINT TRIGGER work_items_packet_law_trg AFTER INSERT OR UPDATE OF state ON public.work_items DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION work_items_packet_law();
  END IF;
END $$;
