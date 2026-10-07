-- ============================================================================
-- NayaPOWER cold-retrieve ranking v2 — OR-fallback cascade
-- Amends: public.nayanet_retrieve_blocks() (from 20261006235900 v1).
--
-- Problem (measured offline, retrieval benchmark 2026-10-07):
--   v1's boolean prefilter (search_vector @@ websearch_to_tsquery) uses AND
--   semantics: a single non-matching lexeme (a name, a number-word like
--   "nine" vs "9.0", a paraphrase) silences the whole query -> NO_MATCH.
--   Baseline on a 12-query relevance-judged corpus: MRR 0.6667, P@1 0.6667
--   (4/12 paraphrase queries returned zero rows). The cold-Naya discovery
--   case — asking in her own words — is exactly what failed.
--
-- Fix: attempt 1 keeps v1's AND semantics byte-identical (any query that
-- returns rows today returns the identical rows). Attempt 2 fires ONLY when
-- attempt 1 returned zero rows for a non-empty query: OR over the query's
-- lexemes through the same scoring (0.50 text + 0.25 applicability +
-- 0.15 truth + 0.10 recency). Fallback results carry 'fallback_or_match'
-- in `why` for observability. Measured after: MRR 1.0, P@1 1.0, all
-- structural assertions hold (SUPERSEDED/DELETED never served; VERIFIED
-- outranks CANDIDATE on shared vocabulary).
--
-- Safety: CREATE OR REPLACE preserves the v1 REVOKEs (no privilege change).
-- Idempotent. Read-only for callers: retrieval never creates authority.
-- ============================================================================

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
  v_orquery tsquery := case when v_q is not null then (
                        select string_agg(t.lex, ' | ')::tsquery
                        from (select distinct unnest(tsvector_to_array(to_tsvector('english', v_q)))) as t(lex)
                      ) end;
  v_lim     integer := greatest(1, least(coalesce(p_limit, 10), 50));
  v_ctx     jsonb   := coalesce(p_context, '{}'::jsonb);
  v_out     jsonb;
  v_active  tsquery;
  v_fallback boolean := false;
begin
  if p_owner_id is null then
    raise exception 'NAYANET_RETRIEVE_OWNER_REQUIRED';
  end if;

  for attempt in 1..2 loop
    if attempt = 1 then
      v_active := v_tsquery;
      v_fallback := false;
    else
      exit when v_tsquery is null;                                  -- cold-start default already ran
      exit when v_out is not null and v_out <> '[]'::jsonb;         -- primary hit; keep it
      v_active := v_orquery;
      v_fallback := true;
      exit when v_active is null;                                   -- no lexemes; nothing to try
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
        case when v_active is not null
             then ts_rank(b.search_vector, v_active)
             else 0.0::real end                                            as text_rank,
        public.nayanet_applicability_match(b.applicable_scope, v_ctx)      as app_match,
        public.nayanet_truth_weight(b.understanding_state, b.status)       as truth_w,
        exp(-extract(epoch from (now() - b.updated_at)) / 7776000.0)       as recency
      from public.nayanet_intelligent_blocks b
      where b.owner_id = p_owner_id
        and b.status in ('ACTIVE', 'DURABLE', 'RELEASED')
        and (v_active is null or b.search_vector @@ v_active)
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
        'why',                case when v_active is not null
                                   then jsonb_build_array('text_match')
                                   else jsonb_build_array('cold_start_default') end
                             || case when v_fallback
                                     then jsonb_build_array('fallback_or_match')
                                     else '[]'::jsonb end
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
  end loop;

  return v_out;
end;
$$;
