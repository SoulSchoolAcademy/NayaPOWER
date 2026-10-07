-- ============================================================================
-- NayaPOWER cold-retrieve search substrate v1
-- Adds keyword-search infrastructure to nayanet_intelligent_blocks.
-- Consumed by: supabase/functions/nayanet-intelligence-retrieve (Edge Function)
--              via public.nayanet_retrieve_blocks().
--
-- Design: trigger-maintained tsvector (english) with positional weights:
--   A = high-signal fields (title/essence/summary/name when present)
--   B = body fields (text/lesson/decision/observation) + applicable_scope
--   C = full content JSON as text (catch-all; robust to unknown keys)
-- GIN index for @@ queries. Backfill included. Read-only for callers:
-- retrieval never creates authority (see Edge Function contract).
-- ============================================================================

-- 1. search_vector column ----------------------------------------------------
alter table public.nayanet_intelligent_blocks
  add column if not exists search_vector tsvector;

-- 2. GIN index ----------------------------------------------------------------
create index if not exists nayanet_ib_search_vector_gin
  on public.nayanet_intelligent_blocks using gin (search_vector);

-- 3. Trigger function (single source of the weighting contract) ---------------
create or replace function public.nayanet_ib_refresh_search_vector()
returns trigger
language plpgsql
set search_path = ''
as $$
begin
  new.search_vector :=
    setweight(to_tsvector('english',
      coalesce(new.content->>'title','')   || ' ' ||
      coalesce(new.content->>'essence','') || ' ' ||
      coalesce(new.content->>'summary','') || ' ' ||
      coalesce(new.content->>'name','')
    ), 'A')
    ||
    setweight(to_tsvector('english',
      coalesce(new.content->>'text','')        || ' ' ||
      coalesce(new.content->>'lesson','')      || ' ' ||
      coalesce(new.content->>'decision','')   || ' ' ||
      coalesce(new.content->>'observation','') || ' ' ||
      coalesce(new.applicable_scope::text,'')
    ), 'B')
    ||
    setweight(to_tsvector('english', coalesce(new.content::text,'')), 'C');
  return new;
end;
$$;

-- 4. Trigger -------------------------------------------------------------------
drop trigger if exists nayanet_ib_search_vector_trg on public.nayanet_intelligent_blocks;
create trigger nayanet_ib_search_vector_trg
  before insert or update of content, applicable_scope
  on public.nayanet_intelligent_blocks
  for each row
  execute function public.nayanet_ib_refresh_search_vector();

-- 5. Backfill (direct assignment; does not touch updated_at) --------------------
update public.nayanet_intelligent_blocks
set search_vector =
  setweight(to_tsvector('english',
    coalesce(content->>'title','')   || ' ' ||
    coalesce(content->>'essence','') || ' ' ||
    coalesce(content->>'summary','') || ' ' ||
    coalesce(content->>'name','')
  ), 'A')
  ||
  setweight(to_tsvector('english',
    coalesce(content->>'text','')        || ' ' ||
    coalesce(content->>'lesson','')      || ' ' ||
    coalesce(content->>'decision','')   || ' ' ||
    coalesce(content->>'observation','') || ' ' ||
    coalesce(applicable_scope::text,'')
  ), 'B')
  ||
  setweight(to_tsvector('english', coalesce(content::text,'')), 'C')
where search_vector is null;

-- 6. Applicability match: fraction of context keys echoed in applicable_scope --
--    Neutral 0.5 when either side is empty (no signal, not a penalty). ---------
create or replace function public.nayanet_applicability_match(
  p_scope jsonb,
  p_context jsonb
)
returns numeric
language sql
immutable
set search_path = ''
as $$
  select case
    when p_context is null or p_context = '{}'::jsonb then 0.5
    when p_scope   is null or p_scope   = '{}'::jsonb then 0.5
    else coalesce((
      select avg(case when (p_scope ->> t.k) = t.v then 1.0 else 0.0 end)
      from jsonb_each_text(p_context) as t(k, v)
    ), 0.5)
  end;
$$;

-- 7. Truth weight: the understanding lifecycle is a retrieval signal ------------
--    LEARNED > APPLIED > VERIFIED > DISTILLED > INTERPRETED > CONTEXTUALIZED >
--    CANDIDATE. Non-servable statuses score 0 (excluded upstream anyway). -------
create or replace function public.nayanet_truth_weight(
  p_state text,
  p_status text
)
returns numeric
language sql
immutable
set search_path = ''
as $$
  select case
    when p_status in ('SUPERSEDED','DELETED') then 0.0
    else case p_state
      when 'LEARNED'        then 1.00
      when 'APPLIED'        then 0.90
      when 'VERIFIED'       then 0.85
      when 'DISTILLED'      then 0.80
      when 'INTERPRETED'    then 0.60
      when 'CONTEXTUALIZED' then 0.50
      when 'CANDIDATE'      then 0.30
      else 0.40
    end
  end;
$$;

-- 8. The retrieval RPC ----------------------------------------------------------
--    p_query   : free-text context query (websearch syntax accepted).
--                Empty/NULL = cold-start default: most trusted recent blocks.
--    p_owner_id: owner scope (RLS still applies for user callers).
--    p_limit   : 1..50, default 10.
--    p_context : jsonb context matched against applicable_scope.
--    Returns jsonb array of blocks with score + score_breakdown + why.
--    Relationship expansion (GAP C) happens in the Edge Function, which owns
--    the graph vocabulary (mirrors nayanet-know-runtime/know.ts).
-- ------------------------------------------------------------------------------
create or replace function public.nayanet_retrieve_blocks(
  p_query text,
  p_owner_id uuid,
  p_limit integer default 10,
  p_context jsonb default '{}'::jsonb
)
returns jsonb
language plpgsql
set search_path = ''
as $$
declare
  v_q       text    := nullif(btrim(coalesce(p_query, '')), '');
  v_tsquery tsquery := case when v_q is not null
                            then websearch_to_tsquery('english', v_q) end;
  v_lim     integer := greatest(1, least(coalesce(p_limit, 10), 50));
  v_ctx     jsonb   := coalesce(p_context, '{}'::jsonb);
  v_out     jsonb;
begin
  if p_owner_id is null then
    raise exception 'NAYANET_RETRIEVE_OWNER_REQUIRED';
  end if;

  with candidates as (
    select
      b.intelligent_block_id,
      b.status,
      b.understanding_state,
      b.owner_scope,
      b.applicable_scope,
      b.content,
      b.connections,
      b.superseded_by_block_id,
      b.evidence_refs,
      b.provenance,
      b.updated_at,
      case when v_tsquery is not null
           then ts_rank(b.search_vector, v_tsquery)
           else 0.0::real end                                            as text_rank,
      public.nayanet_applicability_match(b.applicable_scope, v_ctx)      as app_match,
      public.nayanet_truth_weight(b.understanding_state, b.status)       as truth_w,
      exp(-extract(epoch from (now() - b.updated_at)) / 7776000.0)       as recency
    from public.nayanet_intelligent_blocks b
    where b.owner_id = p_owner_id
      and b.status in ('ACTIVE', 'DURABLE', 'RELEASED')
      and (v_tsquery is null or b.search_vector @@ v_tsquery)
  ),
  scored as (
    select
      c.*,
      (0.50 * c.text_rank
       + 0.25 * c.app_match
       + 0.15 * c.truth_w
       + 0.10 * c.recency)::numeric                                      as score
    from candidates c
  ),
  ranked as (
    select s.*, row_number() over (order by s.score desc, s.updated_at desc) as rn
    from scored s
  )
  select coalesce(jsonb_agg(
    jsonb_build_object(
      'block_id',           r.intelligent_block_id,
      'status',             r.status,
      'understanding_state',r.understanding_state,
      'owner_scope',        r.owner_scope,
      'applicable_scope',   r.applicable_scope,
      'content',            r.content,
      'connections',        r.connections,
      'superseded_by_block_id', r.superseded_by_block_id,
      'evidence_refs',      r.evidence_refs,
      'provenance',         r.provenance,
      'updated_at',         r.updated_at,
      'score',              round(r.score::numeric, 4),
      'score_breakdown',    jsonb_build_object(
                              'text_rank',   round(r.text_rank::numeric, 4),
                              'applicability', round(r.app_match::numeric, 4),
                              'truth_weight',  round(r.truth_w::numeric, 4),
                              'recency',       round(r.recency::numeric, 4)),
      'why',                case when v_tsquery is not null
                                 then jsonb_build_array('text_match')
                                 else jsonb_build_array('cold_start_default') end
                           || case when r.app_match >= 0.75
                                   then jsonb_build_array('applicable_to_context')
                                   else '[]'::jsonb end
                           || case when r.understanding_state in ('LEARNED','APPLIED','VERIFIED')
                                   then jsonb_build_array('truth_state:' || r.understanding_state)
                                   else '[]'::jsonb end
    )
    order by r.rn
  ), '[]'::jsonb)
  into v_out
  from ranked r
  where r.rn <= v_lim;

  return v_out;
end;
$$;

-- Least-privilege: the Edge Function calls this with the service_role client
-- after OIDC-verifying the caller. No direct grant to anon/authenticated.
revoke all on function public.nayanet_retrieve_blocks(text, uuid, integer, jsonb) from public;
revoke all on function public.nayanet_applicability_match(jsonb, jsonb) from public;
revoke all on function public.nayanet_truth_weight(text, text) from public;
