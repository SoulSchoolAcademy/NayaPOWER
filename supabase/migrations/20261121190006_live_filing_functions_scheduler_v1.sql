-- Live filing: scheduler RPCs — 7 functions
-- Supabase filing round 2026-11-21, Seat 2 (FUNCTIONS). Branch: supabase/filing-20261121-functions.
-- Source: LIVE definitions captured first-hand 2026-11-21 via Supabase Management API
--   POST /v1/projects/dahisasgpfvziswqvmvm/database/query — pg_get_functiondef / pg_get_triggerdef.
--   Read-only capture. No live writes were made. Definitions below are verbatim live
--   bytes (CREATE OR REPLACE FUNCTION as returned by pg_get_functiondef), grouped by
--   area; only this header and per-function provenance comments were added.
-- Scheduled-message lifecycle + the runner (fire / claim-due / next-fire).
-- NOTE (scope limit, stated honestly): a fresh-apply diff against a test database is
--   NOT in scope for this round (coordinator brief). These migrations assume the
--   live-only tables they read exist — Seat 1's table filings on the same filing
--   branch supply them; apply tables first on a fresh rebuild.
-- Inventory: DATABASE.md §(b) B1/B2 + §(c); INVENTORY.md §3.2 / §3.4 (64 riders).

-- ---------------------------------------------------------------------------
-- fire_scheduled_messages()
--   live: public.fire_scheduled_messages — SECURITY DEFINER, language plpgsql, kind f, volatile v
--   purpose (DATABASE.md): Fire due scheduled messages (the scheduler's runner). (Scheduler)
--   captured: pg_get_functiondef(fire_scheduled_messages) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.fire_scheduled_messages()
 RETURNS integer
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
declare
  cand record;
  r record;
  tgt text;
  th_id uuid;
  ids jsonb;
  nxt timestamptz;
  fired int := 0;
begin
  for cand in
    select id from public.scheduled_messages
    where (status = 'pending' and fire_at <= now())
       or (status = 'firing' and updated_at < now() - interval '10 minutes')
    order by fire_at asc
    limit 20
  loop
    update public.scheduled_messages
       set status = 'firing', updated_at = now()
     where id = cand.id and status in ('pending', 'firing')
     returning * into r;
    if not found then continue; end if;
    begin
      ids := '[]'::jsonb;
      -- space targets: one thread addressed to the space alias
      for tgt in
        select e ->> 'id' from jsonb_array_elements(r.recipients) as e
        where e ->> 'kind' = 'space'
      loop
        insert into public.smart_mail_threads (subject, from_alias, to_alias, preview)
        values (r.subject, r.owner_alias, tgt, left(r.body, 120)) returning id into th_id;
        insert into public.smart_mail_messages (thread_id, from_alias, body)
        values (th_id, r.owner_alias, r.body);
        ids := ids || jsonb_build_array(th_id);
      end loop;
      -- person targets: direct people + contact-list members (snapshotted)
      for tgt in
        select e ->> 'id' from jsonb_array_elements(r.recipients) as e
        where e ->> 'kind' = 'person'
        union
        select m from jsonb_array_elements(r.recipients) as e,
                      jsonb_array_elements_text(e -> 'memberIds') as m
        where e ->> 'kind' = 'clist'
      loop
        insert into public.smart_mail_threads (subject, from_alias, to_alias, preview)
        values (r.subject, r.owner_alias, tgt, left(r.body, 120)) returning id into th_id;
        insert into public.smart_mail_messages (thread_id, from_alias, body)
        values (th_id, r.owner_alias, r.body);
        ids := ids || jsonb_build_array(th_id);
      end loop;
      if jsonb_array_length(ids) = 0 then
        raise exception 'no deliverable recipients';
      end if;
      if r.recur is not null and coalesce(r.recur ->> 'freq', 'once') <> 'once' then
        nxt := public.next_fire_time(r.recur, now());
        if nxt is null then raise exception 'could not compute next occurrence'; end if;
        update public.scheduled_messages
           set status = 'pending', fire_at = nxt, fired_at = now(),
               result = ids, attempts = 0, last_error = null, updated_at = now()
         where id = r.id;
      else
        update public.scheduled_messages
           set status = 'fired', fired_at = now(), result = ids, updated_at = now()
         where id = r.id;
      end if;
      fired := fired + 1;
    exception when others then
      update public.scheduled_messages
         set status = case when attempts + 1 >= 5 then 'error' else 'pending' end,
             attempts = attempts + 1, last_error = sqlerrm, updated_at = now()
       where id = r.id;
    end;
  end loop;
  return fired;
end
$function$;

-- ---------------------------------------------------------------------------
-- next_fire_time(rule jsonb, after_ts timestamp with time zone)
--   live: public.next_fire_time — SECURITY INVOKER (default), language plpgsql, kind f, volatile i
--   purpose (DATABASE.md): When a scheduled message next fires. (Scheduler)
--   captured: pg_get_functiondef(next_fire_time) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.next_fire_time(rule jsonb, after_ts timestamp with time zone)
 RETURNS timestamp with time zone
 LANGUAGE plpgsql
 IMMUTABLE
AS $function$
declare
  tz text := coalesce(rule ->> 'tz', 'UTC');
  tm time := (rule ->> 'time')::time;
  freq text := rule ->> 'freq';
  local_after timestamp := after_ts at time zone tz;
  cand timestamp;
  d date;
  i int;
  days int[];
  dom int;
begin
  if freq = 'daily' then
    cand := local_after::date + tm;
    if cand <= local_after then cand := cand + interval '1 day'; end if;
    return cand at time zone tz;
  elsif freq = 'weekly' then
    select array_agg(x::int) into days from jsonb_array_elements_text(rule -> 'days') as x;
    if days is null then days := array[1]; end if;
    for i in 0..7 loop
      d := local_after::date + i;
      if extract(dow from d)::int = any(days) then
        cand := d + tm;
        if cand > local_after then return cand at time zone tz; end if;
      end if;
    end loop;
    return null;
  elsif freq = 'monthly' then
    for i in 0..1 loop
      d := (date_trunc('month', local_after) + (i || ' month')::interval)::date;
      if coalesce((rule ->> 'lastDay')::boolean, false) then
        d := (d + interval '1 month - 1 day')::date;
      else
        dom := least(coalesce((rule ->> 'dayOfMonth')::int, 15),
                     extract(day from (d + interval '1 month - 1 day'))::int);
        d := d + (dom - 1);
      end if;
      cand := d + tm;
      if cand > local_after then return cand at time zone tz; end if;
    end loop;
    return null;
  end if;
  return null;
end
$function$;

-- ---------------------------------------------------------------------------
-- sched_cancel(p_token text, p_id uuid)
--   live: public.sched_cancel — SECURITY DEFINER, language plpgsql, kind f, volatile v
--   purpose (DATABASE.md): Cancel a scheduled message. (Scheduler)
--   captured: pg_get_functiondef(sched_cancel) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.sched_cancel(p_token text, p_id uuid)
 RETURNS boolean
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
DECLARE v_owner text;
BEGIN
  v_owner := public.owner_alias_for(p_token);
  IF v_owner = '' THEN RAISE EXCEPTION 'not authorized'; END IF;
  UPDATE public.scheduled_messages
  SET status = 'cancelled', updated_at = now()
  WHERE id = p_id AND owner_alias = v_owner AND status = 'scheduled';
  RETURN FOUND;
END $function$;

-- ---------------------------------------------------------------------------
-- sched_claim_due(p_limit integer)
--   live: public.sched_claim_due — SECURITY DEFINER, language sql, kind f, volatile v
--   purpose (DATABASE.md): Claim due scheduled messages (runner lease). (Scheduler)
--   captured: pg_get_functiondef(sched_claim_due) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.sched_claim_due(p_limit integer)
 RETURNS SETOF scheduled_messages
 LANGUAGE sql
 SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
  UPDATE public.scheduled_messages m
  SET status = 'firing',
      attempts = m.attempts + 1,
      updated_at = now()
  WHERE m.id IN (
    SELECT id FROM public.scheduled_messages
    WHERE (status = 'scheduled' AND fire_at <= now())
       OR (status = 'firing' AND updated_at < now() - interval '5 minutes')
    ORDER BY fire_at
    LIMIT LEAST(COALESCE(p_limit, 200), 1000)
    FOR UPDATE SKIP LOCKED
  )
  RETURNING m.*
$function$;

-- ---------------------------------------------------------------------------
-- sched_create(p_token text, p_kind text, p_subject text, p_body text, p_recipients jsonb, p_fire_at timestamp with time zone, p_recur jsonb)
--   live: public.sched_create — SECURITY DEFINER, language plpgsql, kind f, volatile v
--   purpose (DATABASE.md): Create a scheduled message. (Scheduler)
--   captured: pg_get_functiondef(sched_create) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.sched_create(p_token text, p_kind text, p_subject text, p_body text, p_recipients jsonb, p_fire_at timestamp with time zone, p_recur jsonb)
 RETURNS uuid
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
DECLARE
  v_owner text;
  v_id uuid;
  v_list_id uuid;
BEGIN
  v_owner := public.owner_alias_for(p_token);
  IF v_owner = '' THEN RAISE EXCEPTION 'not authorized'; END IF;

  IF p_kind NOT IN ('post','mail','message','reminder','announcement') THEN
    RAISE EXCEPTION 'bad kind';
  END IF;
  IF p_fire_at IS NULL OR p_fire_at < now() - interval '2 minutes' THEN
    RAISE EXCEPTION 'fire_at must be in the future';
  END IF;
  IF p_recipients IS NULL OR jsonb_typeof(p_recipients) <> 'object' THEN
    RAISE EXCEPTION 'recipients must be a JSON object';
  END IF;
  IF p_recur IS NOT NULL THEN
    IF jsonb_typeof(p_recur) <> 'object'
       OR NOT (p_recur->>'freq' IN ('once','daily','weekly','monthly')) THEN
      RAISE EXCEPTION 'bad recur';
    END IF;
  END IF;

  -- If targeting a Smart List, it must be the owner's own list
  -- (prevents scheduling blasts to someone else's audience).
  IF p_recipients ? 'list_id' THEN
    BEGIN
      v_list_id := (p_recipients->>'list_id')::uuid;
    EXCEPTION WHEN others THEN
      RAISE EXCEPTION 'bad list_id';
    END;
    IF NOT EXISTS (SELECT 1 FROM public.smart_lists
                   WHERE id = v_list_id AND owner_alias = v_owner) THEN
      RAISE EXCEPTION 'not authorized';
    END IF;
  END IF;

  -- Page target, when present, must be a real page kind + non-empty alias.
  IF p_recipients ? 'page' THEN
    IF NOT ((p_recipients->>'page') IN ('personal','business','space'))
       OR COALESCE(p_recipients->>'alias','') = '' THEN
      RAISE EXCEPTION 'bad page target';
    END IF;
  END IF;

  INSERT INTO public.scheduled_messages
    (owner_alias, kind, subject, body, recipients, fire_at,
     recur, status, attempts)
  VALUES
    (v_owner, p_kind, NULLIF(p_subject,''), COALESCE(p_body,''),
     p_recipients, p_fire_at, COALESCE(p_recur, '{"freq":"once"}'::jsonb),
     'scheduled', 0)
  RETURNING id INTO v_id;
  RETURN v_id;
END $function$;

-- ---------------------------------------------------------------------------
-- sched_list(p_token text, p_from date, p_to date)
--   live: public.sched_list — SECURITY DEFINER, language sql, kind f, volatile s
--   purpose (DATABASE.md): List scheduled messages. (Scheduler)
--   captured: pg_get_functiondef(sched_list) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.sched_list(p_token text, p_from date, p_to date)
 RETURNS SETOF scheduled_messages
 LANGUAGE sql
 STABLE SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
  SELECT m.* FROM public.scheduled_messages m
  WHERE m.owner_alias = public.owner_alias_for(p_token)
    AND public.owner_alias_for(p_token) <> ''
    AND m.fire_at::date BETWEEN COALESCE(p_from, m.fire_at::date)
                            AND COALESCE(p_to,   m.fire_at::date)
  ORDER BY m.fire_at DESC
$function$;

-- ---------------------------------------------------------------------------
-- sched_my_lists(p_token text)
--   live: public.sched_my_lists — SECURITY DEFINER, language sql, kind f, volatile s
--   purpose (DATABASE.md): List my scheduled-message lists. (Scheduler)
--   captured: pg_get_functiondef(sched_my_lists) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.sched_my_lists(p_token text)
 RETURNS jsonb
 LANGUAGE sql
 STABLE SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
  SELECT COALESCE(jsonb_agg(jsonb_build_object(
      'id', l.id, 'title', l.title,
      'members', (SELECT COUNT(*) FROM public.smart_list_items i
                  WHERE i.list_id = l.id AND i.item_kind = 'person'))
      ORDER BY l.position, l.created_at), '[]'::jsonb)
  FROM public.smart_lists l
  WHERE l.owner_alias = public.owner_alias_for(p_token)
    AND public.owner_alias_for(p_token) <> ''
$function$;
