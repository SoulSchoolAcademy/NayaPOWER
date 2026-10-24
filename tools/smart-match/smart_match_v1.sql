-- STATUS: v1 math - SUPERSEDED by smart_match.py v1.2 (two-tier family scoring). Regenerate before any deployment.
-- Smart Match v1 — SQL twin of the reference implementation (smart_match_v1.py).
-- Naya Power, SET B / engine end, 2026-10-24. NOT deployed — for the wiring lanes.
--
-- One logic, everywhere: entities carry a declared profile vector as jsonb:
--   {"topics": [...], "goals": [...], "offers": [...], "needs": [...], "wants": [...]}
-- Published v1 weights (Lock Packet, Issue #3029):
--   topics 40% · goals 25% · offers<->needs 20% · desired connections 15%
-- A suggestion surfaces only on >= 2 independent signals. The matcher only
-- ever sees declared signals of findable entities; the caller excludes
-- private / opted-out / non-discoverable candidates before scoring.

create or replace function public.smart_match_overlap(a jsonb, b jsonb)
returns numeric language sql immutable as $$
  with A as (select distinct value as v from jsonb_array_elements_text(coalesce(a, '[]'::jsonb))),
       B as (select distinct value as v from jsonb_array_elements_text(coalesce(b, '[]'::jsonb)))
  select case when (select count(*) from A) = 0 or (select count(*) from B) = 0 then 0
              else (select count(*) from A join B using (v))::numeric
                   / least((select count(*) from A), (select count(*) from B)) end
$$;

create or replace function public.smart_match_v1(a jsonb, b jsonb)
returns jsonb language sql immutable as $$
  with parts as (
    select
      public.smart_match_overlap(a->'topics', b->'topics')                                        as topics,
      public.smart_match_overlap(a->'goals',  b->'goals')                                         as goals,
      (public.smart_match_overlap(a->'offers', b->'needs')
       + public.smart_match_overlap(b->'offers', a->'needs')) / 2.0                               as offers_needs,
      public.smart_match_overlap(a->'wants', coalesce(b->'topics','[]'::jsonb)
                                             || coalesce(b->'offers','[]'::jsonb))                 as wants
  )
  select jsonb_build_object(
    'score', round(100 * (0.40*topics + 0.25*goals + 0.20*offers_needs + 0.15*wants)),
    'parts', jsonb_build_object('topics', round(topics,2), 'goals', round(goals,2),
                                'offers_needs', round(offers_needs,2), 'wants', round(wants,2)),
    'signals', (select jsonb_agg(k) from (values
                  (case when topics > 0 then 'topics' end),
                  (case when goals > 0 then 'goals' end),
                  (case when offers_needs > 0 then 'offers_needs' end),
                  (case when wants > 0 then 'wants' end)) s(k) where k is not null),
    'surface', (topics>0)::int + (goals>0)::int + (offers_needs>0)::int + (wants>0)::int >= 2
  ) from parts
$$;
