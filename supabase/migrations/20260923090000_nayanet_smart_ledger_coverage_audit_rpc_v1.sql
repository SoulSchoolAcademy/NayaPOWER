-- NayaNET Smart Ledger Coverage Audit RPC (READ-ONLY)
-- Scope: Priority #2 legacy cognition-event disposition.
-- Contract: returns AGGREGATES ONLY. No row data, no content, no identifiers of any member are leaked.
-- Access: EXECUTE granted to authenticated only. The function body is SECURITY DEFINER so it can
--        traverse owner-scoped truth stores without exposing them to any caller's RLS.
-- Idempotent: create or replace. Safe to re-run.

create or replace function public.nayanet_smart_ledger_coverage_audit()
returns jsonb
language plpgsql
security definer
set search_path = public, extensions
as $$
declare
  v_cognition_total bigint;
  v_ledgered bigint;
  v_first_ledgered timestamptz;
  v_cohort_local bigint;
  v_cohort_fingerprint text;
  v_audit jsonb;
  v_missing_columns text[];
begin
  -- Defensive schema guard: fail deterministically at the FIRST missing column.
  select array_agg(x.c) into v_missing_columns
  from (
    values
      ('public'::text,'nayanet_cognition_events'::text,array['id','type','classification','source']::text[]),
      ('public'::text,'nayanet_smart_ledger'::text,array['source_table','source_id','event_at']::text[])
  ) as t(schema_name, table_name, cols),
  lateral unnest(t.cols) as x(c)
  where not exists (
    select 1 from information_schema.columns c
    where c.table_schema = t.schema_name
      and c.table_name = t.table_name
      and c.column_name = x.c
  );
  if v_missing_columns is not null and array_length(v_missing_columns,1) > 0 then
    raise exception 'COVERAGE_SCHEMA_MISMATCH missing=%', v_missing_columns;
  end if;

  select count(*) into v_cognition_total from public.nayanet_cognition_events;
  select count(distinct sl.source_id) into v_ledgered
    from public.nayanet_smart_ledger sl
   where sl.source_table = 'nayanet_cognition_events';
  select min(sl.event_at) into v_first_ledgered
    from public.nayanet_smart_ledger sl
   where sl.source_table = 'nayanet_cognition_events';

  -- Cohort definition (exact predicate, non-destructive):
  --   nayanet_cognition_events.id has NO Smart Ledger row where
  --   source_table = 'nayanet_cognition_events' AND source_id = cohort.id::text
  -- Cohort fingerprint: sha256 over sorted cohort source_ids. Leaks nothing (digest only).
  select count(*),
         coalesce(encode(extensions.digest(string_agg(c.id::text, '|' order by c.id::text), 'sha256'), 'hex'), '')
    into v_cohort_local, v_cohort_fingerprint
    from public.nayanet_cognition_events c
   where not exists (
     select 1 from public.nayanet_smart_ledger sl
      where sl.source_table = 'nayanet_cognition_events'
        and sl.source_id = c.id::text
   );

  select jsonb_build_object(
    'schema','NAYANET_SMART_LEDGER_COVERAGE_AUDIT_V1',
    'generated_at', now(),
    'cognition_total', v_cognition_total,
    'ledgered_cognition', v_ledgered,
    'unlinked_cognition', v_cognition_total - v_ledgered,
    'cohort_local', v_cohort_local,
    'cohort_fingerprint_sha256', v_cohort_fingerprint,
    'first_ledgered_cognition_at', v_first_ledgered,
    'rls', 'aggregates_only_no_row_data',
    'unlinked_groups', coalesce((
      select jsonb_agg(jsonb_build_object(
               'type', g.type,
               'classification', g.classification,
               'source', g.source,
               'count', g.n
             ) order by g.n desc, g.source)
      from (
        select c.type, c.classification, c.source, count(*) as n
          from public.nayanet_cognition_events c
         where not exists (
           select 1 from public.nayanet_smart_ledger sl
            where sl.source_table = 'nayanet_cognition_events'
              and sl.source_id = c.id::text
         )
         group by c.type, c.classification, c.source
      ) g
    ),'[]'::jsonb)
  ) into v_audit;

  return v_audit;
end;
$$;

revoke all on function public.nayanet_smart_ledger_coverage_audit() from public;
grant execute on function public.nayanet_smart_ledger_coverage_audit() to authenticated;