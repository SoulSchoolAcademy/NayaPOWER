alter table public.nayanet_smart_connect_participation
  add column if not exists consent_state text not null default 'pending';

do $$
begin
  if not exists (
    select 1 from pg_constraint
    where conname='nayanet_smart_connect_participation_consent_state_check'
      and conrelid='public.nayanet_smart_connect_participation'::regclass
  ) then
    alter table public.nayanet_smart_connect_participation
      add constraint nayanet_smart_connect_participation_consent_state_check
      check (consent_state in ('pending','explicit','revoked'));
  end if;
end;
$$;

create or replace function public.nayanet_require_explicit_smart_connect_consent()
returns trigger
language plpgsql
security definer
set search_path=''
as $$
begin
  if new.status='active' and new.consent_state is distinct from 'explicit' then
    raise exception 'SMART_CONNECT_CONSENT_REQUIRED';
  end if;
  if new.status='revoked' and new.consent_state is distinct from 'revoked' then
    new.consent_state:='revoked';
  end if;
  if tg_op='UPDATE' then
    if new.status='active' and new.external_bindings is distinct from old.external_bindings and new.consent_state is distinct from 'explicit' then
      raise exception 'SMART_CONNECT_BINDING_CONSENT_REQUIRED';
    end if;
  end if;
  return new;
end;
$$;

drop trigger if exists nayanet_smart_connect_consent_boundary on public.nayanet_smart_connect_participation;
create trigger nayanet_smart_connect_consent_boundary
before insert or update on public.nayanet_smart_connect_participation
for each row execute function public.nayanet_require_explicit_smart_connect_consent();

create or replace function public.nayanet_smart_connect(p_door text)
returns jsonb
language plpgsql
security definer
set search_path=''
as $$
begin
  raise exception 'SMART_CONNECT_CONSENT_REQUIRED';
end;
$$;

create or replace function public.nayanet_smart_connect(p_door text,p_consent_state text)
returns jsonb
language plpgsql
security definer
set search_path=''
as $$
declare
  v_actor uuid := auth.uid();
  v_door text := lower(trim(p_door));
  v_consent text := lower(trim(coalesce(p_consent_state,'')));
  v_row public.nayanet_smart_connect_participation;
begin
  if v_actor is null then raise exception 'AUTH_REQUIRED'; end if;
  if v_door not in ('github_app','mcp','rest_openapi','webhooks','sdk','a2a','mcp_apps') then
    raise exception 'SMART_CONNECT_DOOR_INVALID';
  end if;
  if v_consent is distinct from 'explicit' then raise exception 'SMART_CONNECT_CONSENT_REQUIRED'; end if;

  select * into v_row
  from public.nayanet_smart_connect_participation
  where member_id=v_actor and door=v_door
  for update;

  if v_row.id is not null and v_row.status='active' then
    if v_row.consent_state is distinct from 'explicit' then
      update public.nayanet_smart_connect_participation
      set consent_state='explicit',updated_at=now()
      where id=v_row.id
      returning * into v_row;
    end if;
    return jsonb_build_object(
      'schema','NAYANET_SMART_CONNECT_PARTICIPATION_V1',
      'status','ALREADY_CONNECTED',
      'participation',to_jsonb(v_row),
      'authority','UNCHANGED',
      'publication','NOT_GRANTED',
      'consent_state','explicit',
      'identity','PRIVATE_BY_DEFAULT',
      'wisdom_sharing','DEFAULT'
    );
  end if;

  if v_row.id is null then
    insert into public.nayanet_smart_connect_participation(member_id,door,consent_state)
    values(v_actor,v_door,'explicit')
    returning * into v_row;
  else
    update public.nayanet_smart_connect_participation
       set status='active',
           consent_state='explicit',
           wisdom_sharing='default',
           personal_intelligence='private',
           personal_activity='private',
           identity_visibility='private',
           smart_spaces='enabled',
           revoked_at=null,
           updated_at=now()
     where id=v_row.id
     returning * into v_row;
  end if;

  return jsonb_build_object(
    'schema','NAYANET_SMART_CONNECT_PARTICIPATION_V1',
    'status','CONNECTED',
    'participation',to_jsonb(v_row),
    'authority','UNCHANGED',
    'publication','NOT_GRANTED',
    'consent_state','explicit',
    'identity','PRIVATE_BY_DEFAULT',
    'wisdom_sharing','DEFAULT'
  );
end;
$$;

create or replace function public.nayanet_smart_disconnect(p_door text)
returns jsonb
language plpgsql
security definer
set search_path=''
as $$
declare
  v_actor uuid := auth.uid();
  v_door text := lower(trim(p_door));
  v_row public.nayanet_smart_connect_participation;
begin
  if v_actor is null then raise exception 'AUTH_REQUIRED'; end if;
  if v_door not in ('github_app','mcp','rest_openapi','webhooks','sdk','a2a','mcp_apps') then
    raise exception 'SMART_CONNECT_DOOR_INVALID';
  end if;
  select * into v_row
  from public.nayanet_smart_connect_participation
  where member_id=v_actor and door=v_door
  for update;
  if v_row.id is null then raise exception 'SMART_CONNECT_PARTICIPATION_NOT_FOUND'; end if;
  if v_row.status='revoked' then
    return jsonb_build_object('schema','NAYANET_SMART_CONNECT_PARTICIPATION_V1','status','ALREADY_DISCONNECTED','participation',to_jsonb(v_row),'authority','UNCHANGED');
  end if;
  update public.nayanet_smart_connect_participation
     set status='revoked',consent_state='revoked',revoked_at=now(),updated_at=now()
   where id=v_row.id
   returning * into v_row;
  return jsonb_build_object('schema','NAYANET_SMART_CONNECT_PARTICIPATION_V1','status','DISCONNECTED','participation',to_jsonb(v_row),'authority','UNCHANGED');
end;
$$;

revoke all on function public.nayanet_smart_connect(text) from public;
grant execute on function public.nayanet_smart_connect(text) to authenticated;
revoke all on function public.nayanet_smart_connect(text,text) from public;
grant execute on function public.nayanet_smart_connect(text,text) to authenticated;
revoke all on function public.nayanet_smart_disconnect(text) from public;
grant execute on function public.nayanet_smart_disconnect(text) to authenticated;
