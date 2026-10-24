-- Smart Match — SQL twin, regenerated to CURRENT math (v1.4, 2026-10-24).
-- Supersedes smart_match_v1.sql (v1) and the v1.3 twin. NOT deployed — for the wiring lanes.
-- Mirrors smart_match.py exactly: weights 40/25/20/15; topics/goals =
-- 50% raw (phrase+word blended) + 50% concept coverage (concept tier silent
-- when neither side hits the taxonomy); offers<->needs and wants use the
-- signature overlap (terms + concepts); surface requires >= 2 signals;
-- value adjusts rank only, never the %.

create or replace function public.sm_terms(a jsonb) returns setof text language sql immutable as
$$ select distinct value from jsonb_array_elements_text(coalesce(a, '[]'::jsonb)) $$;

create or replace function public.sm_stem(w text) returns text language sql immutable as
$$ select case
     when length(w) > 5 and w like '%ing' then regexp_replace(left(w, length(w)-3), '(.)\1$', '\1')
     when length(w) > 4 and w like '%ies' then left(w, length(w)-3) || 'y'
     when length(w) > 3 and w like '%s' and w not like '%ss' then left(w, length(w)-1)
     else w end $$;

create or replace function public.sm_words(a jsonb) returns setof text language sql immutable as
$$ select distinct public.sm_stem(w) from (select regexp_split_to_table(lower(value), '[^a-z0-9]+') as w
     from jsonb_array_elements_text(coalesce(a, '[]'::jsonb))) s where length(w) > 2 $$;

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
$$ select case when coalesce(array_length(a,1),0)=0 or coalesce(array_length(b,1),0)=0 then 0
     else (select count(*) from unnest(a) x join unnest(b) y on x=y)::numeric
          / least(array_length(a,1), array_length(b,1)) end $$;

create or replace function public.sm_family(a jsonb, b jsonb) returns numeric language sql immutable as
$$ with p as (select public.sm_coeff(array(select * from public.sm_terms(a)), array(select * from public.sm_terms(b))) as phrase,
                     public.sm_coeff(array(select * from public.sm_words(a)), array(select * from public.sm_words(b))) as word,
                     public.sm_coeff(array(select * from public.sm_concepts(a)), array(select * from public.sm_concepts(b))) as concept,
                     (select count(*) from public.sm_concepts(a)) as ca,
                     (select count(*) from public.sm_concepts(b)) as cb)
   select case when ca=0 and cb=0 then 0.5*phrase + 0.5*word
               else 0.5*(0.5*phrase + 0.5*word) + 0.5*concept end from p $$;

create or replace function public.sm_cross(a jsonb, b jsonb) returns numeric language sql immutable as
$$ select public.sm_coeff(
     array(select * from public.sm_terms(a)) || array(select * from public.sm_concepts(a))
       || array(select * from public.sm_words(a) except select * from public.sm_words('["help","want","wants","need","needs","people","person","someone","others","with","from","that","this","more"]'::jsonb)),
     array(select * from public.sm_terms(b)) || array(select * from public.sm_concepts(b))
       || array(select * from public.sm_words(b) except select * from public.sm_words('["help","want","wants","need","needs","people","person","someone","others","with","from","that","this","more"]'::jsonb))) $$;

create or replace function public.smart_match(a jsonb, b jsonb, value_b numeric default null)
returns jsonb language sql immutable as
$$ with parts as (select public.sm_family(a->'topics', b->'topics') as topics,
                         public.sm_family(a->'goals', b->'goals') as goals,
                         (public.sm_cross(a->'offers', b->'needs') + public.sm_cross(b->'offers', a->'needs'))/2.0 as offers_needs,
                         (public.sm_cross(a->'wants', coalesce(b->'topics','[]'::jsonb) || coalesce(b->'offers','[]'::jsonb))
                        + public.sm_cross(b->'wants', coalesce(a->'topics','[]'::jsonb) || coalesce(a->'offers','[]'::jsonb)))/2.0 as wants)
   select jsonb_build_object(
     'score', round(100 * (0.40*topics + 0.25*goals + 0.20*offers_needs + 0.15*wants)),
     'rank', case when value_b is null then round(100 * (0.40*topics + 0.25*goals + 0.20*offers_needs + 0.15*wants))
                  else round(100 * (0.40*topics + 0.25*goals + 0.20*offers_needs + 0.15*wants) * (0.9 + 0.1*value_b)) end,
     'signals', (topics>0)::int + (goals>0)::int + (offers_needs>0)::int + (wants>0)::int,
     'surface', (topics>0)::int + (goals>0)::int + (offers_needs>0)::int + (wants>0)::int >= 2) from parts $$;
