-- 20261121183000_schema_packet_grants_event_store_v1.sql
--
-- Schema packet §2 + §3, filed as ONE migration (packet §6.1: "one migration
-- carrying §3 + the grants").
--
-- SOURCE: dashboard/ledger-mechanics-20261121/SCHEMA-PACKET.md (23,870 B,
-- sha 51c0aad4…). §3 (event store table + function) is VERBATIM from the
-- packet; §2 grants are verbatim except the three named conditional grants
-- below. No Hub DDL, no backfill, no invite-send unblocker, no §4 — the
-- trigger already rides its own filed migration
-- (20261113024500_ledger_trigger_work_items_done_proven_v1.sql).
--
-- ORDER: §3 first, then §2. §2.2 (SELECT on naya_action_events) and §2.6
-- (EXECUTE on the §3 function) cannot run before §3 creates those objects.
--
-- ONE FILE, not two: packet §6.1 allows either; one file keeps the grants
-- and the objects they grant on in a single atomic apply.
--
-- NAMED DEVIATION — CONDITIONAL GRANTS (§2.1, §2.4, §2.5):
-- Three grant targets have NO CREATE in the migration chain on main
-- (verified first-hand 2026-11-21; see MAKER-REPORT-STEP1.md):
--   naya_category_prototypes (§2.1) — 0 repo hits; live-only table.
--   smart_link_joins (§2.4) — 1 repo hit, a staging-worker script, no CREATE.
--   smart_mail_threads / smart_mail_messages (§2.5) — live-only tables.
-- A bare GRANT on any of them fails a fresh/preview database with
-- "relation does not exist" and breaks the chain rebuild. CREATE IF NOT
-- EXISTS was rejected: it would invent column definitions the packet does
-- not authorize, and guessed shapes would shadow the true live definitions
-- already captured on branch supabase/filing-20261121
-- (20261121180000 money / 20261121180200 vault / 20261121180300 social).
-- So each of these grants runs inside a DO block that fires only when the
-- table exists (to_regclass check) and RAISEs a NOTICE otherwise. On
-- production the tables exist live, so the grants fire. On a fresh database
-- they no-op until the filing branch lands. The grant text itself is
-- verbatim; only the wrapper is added.
-- This file's timestamp (20261121183000) sorts AFTER the three table-CREATE
-- files the conditional grants depend on (20261121180000 money /
-- 20261121180200 vault / 20261121180300 social). The filing branch's maximum
-- is 20261121190009 (later function filings only), so the CREATEs still run
-- before this migration and all three conditional grants fire.
--
-- ROLLBACK: DROP FUNCTION public.nayanet_record_ledger_event_by_alias(text,
-- text, text, text, jsonb); DROP TABLE public.naya_action_events; REVOKE
-- the §2 grants. Dropping naya_action_events drops the Dashboard's own
-- event log; no ledger chain rows are touched — ledger_entries is only
-- GRANTed SELECT here, never written.

-- §3 — THE EVENT STORE: one table + one function (packet §3, verbatim).

-- Citizen-action events: the Dashboard's one event store.
CREATE TABLE IF NOT EXISTS public.naya_action_events (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  owner_alias text NOT NULL,
  event_type text NOT NULL,
  source_table text NOT NULL,
  source_id text NOT NULL,
  metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
  created_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS naya_action_events_alias_type_idx
  ON public.naya_action_events (owner_alias, event_type, created_at DESC);
CREATE INDEX IF NOT EXISTS naya_action_events_source_idx
  ON public.naya_action_events (source_table, source_id);

-- Row-level security: anon may insert its own alias's events and read them
-- back. (Adjust the policy name/shape to the project's RLS conventions at
-- apply time; the rule is the point: anon INSERT + SELECT, alias-scoped.)
ALTER TABLE public.naya_action_events ENABLE ROW LEVEL SECURITY;
CREATE POLICY naya_action_events_anon_insert ON public.naya_action_events
  FOR INSERT TO anon WITH CHECK (true);
CREATE POLICY naya_action_events_anon_select ON public.naya_action_events
  FOR SELECT TO anon USING (true);

-- The one write path, alias-native. This is the function the page already
-- calls (NAYA_LEDGER.record): sb.rpc('nayanet_record_ledger_event_by_alias',
-- { p_owner_alias, p_event_type, p_source_table, p_source_id, p_metadata }).
-- It returns the inserted row. No UUID is invented: the alias IS the owner
-- key, exactly as the page's other tables use it.
CREATE OR REPLACE FUNCTION public.nayanet_record_ledger_event_by_alias(
  p_owner_alias text,
  p_event_type text,
  p_source_table text,
  p_source_id text,
  p_metadata jsonb DEFAULT '{}'::jsonb
)
RETURNS public.naya_action_events
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path TO 'public'
AS $function$
DECLARE
  v_row public.naya_action_events;
BEGIN
  IF p_owner_alias IS NULL OR btrim(p_owner_alias) = '' THEN
    RAISE EXCEPTION 'p_owner_alias is required';
  END IF;
  IF p_event_type IS NULL OR btrim(p_event_type) = '' THEN
    RAISE EXCEPTION 'p_event_type is required';
  END IF;
  INSERT INTO public.naya_action_events
    (owner_alias, event_type, source_table, source_id, metadata)
  VALUES
    (p_owner_alias, p_event_type, p_source_table, p_source_id,
     COALESCE(p_metadata, '{}'::jsonb))
  RETURNING * INTO v_row;
  RETURN v_row;
END;
$function$;

-- §2 — GRANTS (packet §2, in packet order; §2.1, §2.4, §2.5 conditional
-- per the named deviation in the header — grant text verbatim inside).

-- 1. THE RED-SPIKE FIX + the post/save/board-open/comment unblocker.
--    Every smart_notes insert fires a trigger writing here. Without this,
--    no wall post, save, board-open or comment can ever land.
--    CONDITIONAL (named deviation, see header): fires only if the table exists.
DO $$
BEGIN
  IF to_regclass('public.naya_category_prototypes') IS NOT NULL THEN
    EXECUTE 'GRANT INSERT, UPDATE ON public.naya_category_prototypes TO anon';
  ELSE
    RAISE NOTICE 'schema-packet §2.1 skipped: public.naya_category_prototypes does not exist in this database';
  END IF;
END
$$;

-- 2. The Dashboard reads its own citizen-action events (packet table, §3).
GRANT SELECT ON public.naya_action_events TO anon;

-- 3. The Dashboard reads the work chain for the Ledger view + Stayed.
--    Writes stay trigger-only: NO INSERT grant on ledger_entries, ever.
--    The trigger (§4) is the only writer.
GRANT SELECT ON public.ledger_entries TO anon;

-- 4. Joins become auditable: the Dashboard reads smart_link_joins back
--    instead of trusting only the daily_stats rollup.
--    CONDITIONAL (named deviation, see header): fires only if the table exists.
DO $$
BEGIN
  IF to_regclass('public.smart_link_joins') IS NOT NULL THEN
    EXECUTE 'GRANT SELECT ON public.smart_link_joins TO anon';
  ELSE
    RAISE NOTICE 'schema-packet §2.4 skipped: public.smart_link_joins does not exist in this database';
  END IF;
END
$$;

-- 5. The sync engine's messenger leg + the visitor message flow.
--    CONDITIONAL (named deviation, see header): each fires only if its table exists.
DO $$
BEGIN
  IF to_regclass('public.smart_mail_threads') IS NOT NULL THEN
    EXECUTE 'GRANT INSERT ON public.smart_mail_threads TO anon';
  ELSE
    RAISE NOTICE 'schema-packet §2.5 skipped: public.smart_mail_threads does not exist in this database';
  END IF;
  IF to_regclass('public.smart_mail_messages') IS NOT NULL THEN
    EXECUTE 'GRANT INSERT ON public.smart_mail_messages TO anon';
  ELSE
    RAISE NOTICE 'schema-packet §2.5 skipped: public.smart_mail_messages does not exist in this database';
  END IF;
END
$$;

-- 6. The packet function (§3) is callable from the page.
GRANT EXECUTE ON FUNCTION public.nayanet_record_ledger_event_by_alias(text, text, text, text, jsonb) TO anon;

-- 7. The older NIA event table: read-only for the Dashboard.
GRANT SELECT ON public.nayanet_smart_ledger TO anon;
