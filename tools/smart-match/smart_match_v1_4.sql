-- Smart Match — SQL twin, regenerated to CURRENT math (v1.5, 2026-10-24).
-- Supersedes smart_match_v1.sql (v1) and the v1.3 twin. NOT deployed — for the wiring lanes.
-- Mirrors smart_match.py v1.5: weights 40/25/20/15; topics/goals =
-- 50% raw (phrase+word blended) + 50% concept coverage (concept tier silent
-- when neither side hits the taxonomy); offers<->needs and wants use the
-- signature overlap (terms + concepts + stemmed content words); surface
-- requires >= 2 signals; value adjusts rank only, never the %.
-- v1.5 mirror fixes (HARDENING-ELITE-V2-2026-10-24, item 7 — full mapping
-- table lives there): one unified stopword set applied to RAW words in
-- every tier (sm_stopwords); plural-before-ing stemming identical to
-- Python; cross signature words require length > 3 (was: all length > 2);
-- coefficient inputs are deduplicated (concatenated signature arrays
-- could previously double-count and push a coefficient above 1);
-- glue-only phrases carry no signal (sm_terms_content); output now
-- carries 'parts' and 'signals' as channel NAMES, as Python does.
-- KNOWN REMAINING DIVERGENCES (named, deliberate): (1) value_b here is a
-- bare numeric — Python v1.5 accepts only a verified-value RECORD
-- ({state: VERIFIED|FINAL, value}); the SQL signature predates the record
-- contract and changing it is a wiring-lane API decision. (2) Postgres
-- round() is half-away-from-zero, Python round() is banker's rounding —
-- exact .5 boundaries of the weighted sum can differ by 1 point.
-- (3) 'reasons' are not produced (would need shared-element returns from
-- every helper). (4) Non-array jsonb inputs error here; Python degrades.

create or replace function public.sm_stopwords() returns setof text language sql immutable as
$$ select unnest(array['a','about','all','an','and','any','are','as','at','be','been','but','by','can','could','do','does','for','from','had','has','have','he','help','her','his','how','if','in','into','is','it','its','more','most','need','needs','no','not','of','on','only','or','other','others','our','over','own','people','person','same','she','so','some','someone','such','than','that','the','their','them','then','they','this','to','under','want','wants','was','we','were','what','when','who','will','with','would','you','your']) $$;

create or replace function public.sm_terms(a jsonb) returns setof text language sql immutable as
$$ select distinct value from jsonb_array_elements_text(coalesce(a, '[]'::jsonb)) $$;

create or replace function public.sm_stem(w text) returns text language sql immutable as
$$ with s1 as (select case
     when length(w) > 4 and w like '%ies' then left(w, length(w)-3) || 'y'
     when length(w) > 3 and w like '%s' and w not like '%ss' then left(w, length(w)-1)
     else w end as x),
   s2 as (select case when length(x) > 5 and x like '%ing' then left(x, length(x)-3) else x end as y from s1)
   select case when length(y) > 3 and right(y,1) = substring(y from length(y)-1 for 1)
               and (select length(x) > 5 and x like '%ing' from s1)
          then left(y, length(y)-1) else y end from s2 $$;

create or replace function public.sm_words(a jsonb) returns setof text language sql immutable as
$$ select distinct public.sm_stem(w) from (select regexp_split_to_table(lower(value), '[,[:space:]]+') as w
     from jsonb_array_elements_text(coalesce(a, '[]'::jsonb))) s
   where length(w) > 2 and w not in (select * from public.sm_stopwords()) $$;

create or replace function public.sm_sig_words(a jsonb) returns setof text language sql immutable as
$$ select distinct public.sm_stem(w) from (select regexp_split_to_table(lower(value), '[,[:space:]]+') as w
     from jsonb_array_elements_text(coalesce(a, '[]'::jsonb))) s
   where length(w) > 3 and w not in (select * from public.sm_stopwords()) $$;

create or replace function public.sm_terms_content(a jsonb) returns setof text language sql immutable as
$$ select value from jsonb_array_elements_text(coalesce(a, '[]'::jsonb))
   where exists (select 1 from public.sm_words(jsonb_build_array(value))) $$;

create or replace function public.sm_concepts(a jsonb) returns setof text language sql immutable as
$$ select distinct m.concept from (values
     ('building','MAKING'),('creation','MAKING'),('templates','MAKING'),('apps','MAKING'),('step 7','MAKING'),('app creation','MAKING'),
     ('execution','SHIPPING'),('delivery','SHIPPING'),('ship','SHIPPING'),('waves','SHIPPING'),('build loop','SHIPPING'),
     ('testing','PROVING'),('validation','PROVING'),('quality','PROVING'),('quality control','PROVING'),('evidence','PROVING'),('proof','PROVING'),('verification','PROVING'),('audit','PROVING'),
     ('integration','CONNECTING'),('systems','CONNECTING'),('network','CONNECTING'),('coordination','CONNECTING'),('the platform','CONNECTING'),
     ('voice','SPEAKING'),('speech','SPEAKING'),('audio','SPEAKING'),('streaming','SPEAKING'),('synthesis','SPEAKING'),('ear test','SPEAKING'),
     ('mail','TALKING'),('messaging','TALKING'),('communication','TALKING'),('conversation','TALKING'),('questions','TALKING'),('answers','TALKING'),('listening','TALKING'),('scheduling','TALKING'),
     ('distillation','THINKING'),('essence','THINKING'),('reflection','THINKING'),('learning','THINKING'),('analysis','THINKING'),('critical thinking','THINKING'),('root cause','THINKING'),('derivation','THINKING'),('project intelligence','THINKING'),
     ('blockers','CLEARING'),('problem solving','CLEARING'),('conflict resolution','CLEARING'),('risk','CLEARING'),('risk review','CLEARING'),('reliability','CLEARING'),('unblocking','CLEARING'),
     ('strategy','GUIDING'),('project leadership','GUIDING'),('orientation','GUIDING'),('home','GUIDING'),('long-term strategy','GUIDING'),('design','GUIDING'),
     ('performance rulings','DECIDING'),('governance','DECIDING'),('decisions','DECIDING'),
     ('smart notes','PUBLISHING'),('feed','PUBLISHING'),('publishing','PUBLISHING'),('flow','PUBLISHING'),('publishing path','PUBLISHING'),('notes','PUBLISHING'),
     ('citizens','PEOPLE'),('usage','PEOPLE'),('readers','PEOPLE'),('material','PEOPLE')
   ) as m(term, concept)
   where m.term in (select * from public.sm_terms(a)) $$;

create or replace function public.sm_coeff(a text[], b text[]) returns numeric language sql immutable as
$$ with da as (select distinct unnest(a) as x), db as (select distinct unnest(b) as x)
   select case when (select count(*) from da) = 0 or (select count(*) from db) = 0 then 0
     else (select count(*) from da join db using (x))::numeric
          / least((select count(*) from da), (select count(*) from db)) end $$;

create or replace function public.sm_family(a jsonb, b jsonb) returns numeric language sql immutable as
$$ with p as (select public.sm_coeff(array(select * from public.sm_terms_content(a)), array(select * from public.sm_terms_content(b))) as phrase,
                     public.sm_coeff(array(select * from public.sm_words(a)), array(select * from public.sm_words(b))) as word,
                     public.sm_coeff(array(select * from public.sm_concepts(a)), array(select * from public.sm_concepts(b))) as concept,
                     (select count(*) from public.sm_concepts(a)) as ca,
                     (select count(*) from public.sm_concepts(b)) as cb)
   select case when ca=0 and cb=0 then 0.5*phrase + 0.5*word
               else 0.5*(0.5*phrase + 0.5*word) + 0.5*concept end from p $$;

create or replace function public.sm_cross(a jsonb, b jsonb) returns numeric language sql immutable as
$$ select public.sm_coeff(
     array(select distinct x from (select * from public.sm_terms_content(a) union all select * from public.sm_concepts(a) union all select * from public.sm_sig_words(a)) u(x)),
     array(select distinct x from (select * from public.sm_terms_content(b) union all select * from public.sm_concepts(b) union all select * from public.sm_sig_words(b)) u(x))) $$;

create or replace function public.smart_match(a jsonb, b jsonb, value_b numeric default null)
returns jsonb language sql immutable as
$$ with parts as (select public.sm_family(a->'topics', b->'topics') as topics,
                         public.sm_family(a->'goals', b->'goals') as goals,
                         (public.sm_cross(a->'offers', b->'needs') + public.sm_cross(b->'offers', a->'needs'))/2.0 as offers_needs,
                         (public.sm_cross(a->'wants', coalesce(b->'topics','[]'::jsonb) || coalesce(b->'offers','[]'::jsonb))
                        + public.sm_cross(b->'wants', coalesce(a->'topics','[]'::jsonb) || coalesce(a->'offers','[]'::jsonb)))/2.0 as wants),
   rel as (select (0.40*topics + 0.25*goals + 0.20*offers_needs + 0.15*wants) as s from parts)
   select jsonb_build_object(
     'score', round(100 * rel.s),
     'rank', case when value_b is null then round(100 * rel.s)
                  else round(100 * rel.s * (0.9 + 0.1*value_b)) end,
     'signals', to_jsonb(array(select v.s from (values ('topics',1),('goals',2),('offers_needs',3),('wants',4)) as v(s, o)
                        where (case v.s when 'topics' then parts.topics when 'goals' then parts.goals
                                        when 'offers_needs' then parts.offers_needs else parts.wants end) > 0
                        order by v.o)),
     'surface', (parts.topics>0)::int + (parts.goals>0)::int + (parts.offers_needs>0)::int + (parts.wants>0)::int >= 2,
     'parts', jsonb_build_object('topics', round(parts.topics, 2), 'goals', round(parts.goals, 2),
                                 'offers_needs', round(parts.offers_needs, 2), 'wants', round(parts.wants, 2)),
     'signal_coverage_percent', round(100 * ((case when parts.topics>0 then 0.40 else 0 end)
                                           + (case when parts.goals>0 then 0.25 else 0 end)
                                           + (case when parts.offers_needs>0 then 0.20 else 0 end)
                                           + (case when parts.wants>0 then 0.15 else 0 end))),
     'calibrated', true) from parts, rel $$;
