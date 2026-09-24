-- Legacy Cognition Disposition Enum & Contract V1
-- Scope: Priority #2 legacy cognition-event disposition (non-destructive).
-- Contract: defines explicit disposition enum and reversible annotation table.
-- Does NOT mutate original nayanet_cognition_events rows.
-- Access: owner-scoped via RLS; audit via SECURITY DEFINER RPC.

-- Disposition enum: exhaustive, non-extensible without migration.
create type public.nayanet_legacy_cognition_disposition as enum (
  'LEGITIMATE_LEDGERABLE_HISTORICAL',
  'ALREADY_REPRESENTED_ELSEWHERE',
  'INTENTIONALLY_EXCLUDED',
  'NEEDS_REVIEW'
);

-- Disposition annotation table: one row per legacy cognition event.
-- Preserves original cognition rows unchanged.
-- Reversible: rows can be deleted/updated without affecting source truth.
create table if not exists public.nayanet_legacy_cognition_disposition (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  owner_id uuid not null references auth.users(id),
  cognition_event_id uuid not null,
  disposition public.nayanet_legacy_cognition_disposition not null,
  rationale text not null,
  classified_by uuid not null references auth.users(id),
  cohort_fingerprint_sha256 text not null,
  constraint nayanet_legacy_cognition_disposition_unique unique (cognition_event_id)
);

-- RLS: owners can read their own dispositions; SECURITY DEFINER RPC for audits.
alter table public.nayanet_legacy_cognition_disposition enable row level security;
drop policy if exists nayanet_legacy_cognition_disposition_select_own on public.nayanet_legacy_cognition_disposition;
create policy nayanet_legacy_cognition_disposition_select_own on public.nayanet_legacy_cognition_disposition
  for select to authenticated using (owner_id = auth.uid());
revoke insert, update, delete on public.nayanet_legacy_cognition_disposition from anon, authenticated;

-- Update trigger
create or replace function public.nayanet_update_updated_at() returns trigger language plpgsql set search_path=public,extensions as $$
begin
  new.updated_at = now();
  return new;
end; $$;

drop trigger if exists nayanet_legacy_cognition_disposition_updated_at on public.nayanet_legacy_cognition_disposition;
create trigger nayanet_legacy_cognition_disposition_updated_at
  before update on public.nayanet_legacy_cognition_disposition
  for each row execute function public.nayanet_update_updated_at();

-- Audit RPC: returns aggregate disposition counts + fingerprint verification.
-- SECURITY DEFINER so it can traverse owner-scoped truth without leaking row data.
create or replace function public.nayanet_legacy_cognition_disposition_audit()
returns jsonb
language plpgsql
security definer
set search_path = public, extensions
as $$
declare
  v_missing_columns text[];
  v_total bigint;
  v_classified bigint;
  v_unclassified bigint;
  v_groups jsonb;
  v_audit jsonb;
  v_cohort_fingerprint text;
begin
  -- Defensive schema guard
  select array_agg(x.c) into v_missing_columns
  from (
    values
      ('public'::text,'nayanet_cognition_events'::text,array['id']::text[]),
      ('public'::text,'nayanet_smart_ledger'::text,array['source_table','source_id']::text[]),
      ('public'::text,'nayanet_legacy_cognition_disposition'::text,array['cognition_event_id','disposition','cohort_fingerprint_sha256']::text[])
  ) as t(schema_name, table_name, cols),
  lateral unnest(t.cols) as x(c)
  where not exists (
    select 1 from information_schema.columns c
    where c.table_schema = t.schema_name
      and c.table_name = t.table_name
      and c.column_name = x.c
  );
  if v_missing_columns is not null and array_length(v_missing_columns,1) > 0 then
    raise exception 'DISPOSITION_SCHEMA_MISMATCH missing=%', v_missing_columns;
  end if;

  -- Cohort fingerprint (must match coverage audit)
  select coalesce(encode(extensions.digest(string_agg(c.id::text, '|' order by c.id::text), 'sha256'), 'hex'), '')
    into v_cohort_fingerprint
    from public.nayanet_cognition_events c
   where not exists (
     select 1 from public.nayanet_smart_ledger sl
      where sl.source_table = 'nayanet_cognition_events'
        and sl.source_id = c.id::text
   );

  -- Total legacy cohort
  select count(*) into v_total
    from public.nayanet_cognition_events c
   where not exists (
     select 1 from public.nayanet_smart_ledger sl
      where sl.source_table = 'nayanet_cognition_events'
        and sl.source_id = c.id::text
   );

  -- Classified count
  select count(*) into v_classified
    from public.nayanet_legacy_cognition_disposition d
    where d.cohort_fingerprint_sha256 = v_cohort_fingerprint;

  v_unclassified := v_total - v_classified;

  -- Grouped by disposition
  select coalesce(jsonb_agg(jsonb_build_object(
               'disposition', g.disposition,
               'count', g.n
             ) order by g.disposition), '[]'::jsonb)
    into v_groups
    from (
      select d.disposition::text as disposition, count(*) as n
        from public.nayanet_legacy_cognition_disposition d
       where d.cohort_fingerprint_sha256 = v_cohort_fingerprint
       group by d.disposition
    ) g;

  select jsonb_build_object(
    'schema', 'NAYANET_LEGACY_COGNITION_DISPOSITION_AUDIT_V1',
    'generated_at', now(),
    'cohort_fingerprint_sha256', v_cohort_fingerprint,
    'cohort_total', v_total,
    'classified', v_classified,
    'unclassified', v_unclassified,
    'groups', v_groups,
    'complete', (v_unclassified = 0)
  ) into v_audit;

  return v_audit;
end; $$;

revoke all on function public.nayanet_legacy_cognition_disposition_audit() from public;
grant execute on function public.nayanet_legacy_cognition_disposition_audit() to authenticated;

comment on type public.nayanet_legacy_cognition_disposition is 'Exhaustive disposition enum for pre-ledger cognition events. No row data is mutated; classification is recorded in nayanet_legacy_cognition_disposition table.';
comment on table public.nayanet_legacy_cognition_disposition is 'Reversible disposition annotations for legacy cognition events (pre-2026-09-19). Original cognition rows are never modified.';