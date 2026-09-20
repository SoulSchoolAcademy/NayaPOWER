-- NayaNET Space Membership V1
-- Canonical identity: auth.users.id = public.members.id
-- Canonical Space: public.nayanet_spaces
-- Membership is current-state projection; cognition events preserve join/leave history.

create table public.nayanet_space_members (
  id uuid primary key default gen_random_uuid(),
  space_id uuid not null references public.nayanet_spaces(id) on delete cascade,
  member_id uuid not null references public.members(id) on delete cascade,
  role text not null default 'member' check (role in ('owner','member')),
  status text not null default 'active' check (status in ('active','left','revoked')),
  joined_at timestamptz not null default now(),
  left_at timestamptz null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (space_id, member_id)
);

create index nayanet_space_members_space_status_idx
  on public.nayanet_space_members(space_id, status, joined_at desc);
create index nayanet_space_members_member_status_idx
  on public.nayanet_space_members(member_id, status, joined_at desc);

alter table public.nayanet_space_members enable row level security;

create policy nayanet_space_members_self_read
  on public.nayanet_space_members
  for select to authenticated
  using (member_id = auth.uid());

create policy nayanet_space_members_shared_read
  on public.nayanet_space_members
  for select to authenticated
  using (
    status = 'active'
    and exists (
      select 1 from public.nayanet_spaces s
      where s.id = nayanet_space_members.space_id
        and s.visibility = 'shared'
        and (
          exists (
            select 1 from public.nayanet_space_members me
            where me.space_id = s.id
              and me.member_id = auth.uid()
              and me.status = 'active'
          )
          or nayanet_space_members.member_id = auth.uid()
        )
    )
  );

create or replace function public.nayanet_space_members_touch()
returns trigger
language plpgsql
set search_path = public
as $$
begin
  new.updated_at := now();
  if new.status = 'active' then
    new.left_at := null;
  elsif new.left_at is null then
    new.left_at := now();
  end if;
  return new;
end;
$$;

create trigger nayanet_space_members_touch
before update on public.nayanet_space_members
for each row execute function public.nayanet_space_members_touch();

create or replace function public.nayanet_space_owner_membership()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
begin
  insert into public.nayanet_space_members(space_id, member_id, role, status)
  values (new.id, new.owner_member_id, 'owner', 'active')
  on conflict (space_id, member_id)
  do update set role='owner', status='active', left_at=null, updated_at=now();
  return new;
end;
$$;

create trigger nayanet_space_owner_membership
after insert on public.nayanet_spaces
for each row execute function public.nayanet_space_owner_membership();

insert into public.nayanet_space_members(space_id, member_id, role, status)
select id, owner_member_id, 'owner', 'active'
from public.nayanet_spaces
on conflict (space_id, member_id)
do update set role='owner', status='active', left_at=null, updated_at=now();

create or replace function public.nayanet_join_space(p_space_id uuid)
returns jsonb
language plpgsql
security definer
set search_path = public
as $$
declare
  v_member uuid := auth.uid();
  v_space public.nayanet_spaces;
  v_row public.nayanet_space_members;
  v_event_id text;
  v_event jsonb;
begin
  if v_member is null then raise exception 'AUTH_REQUIRED'; end if;
  select * into v_space from public.nayanet_spaces where id = p_space_id for share;
  if v_space.id is null then raise exception 'SPACE_NOT_FOUND'; end if;
  if v_space.visibility <> 'shared' and v_space.owner_member_id <> v_member then
    raise exception 'SPACE_JOIN_NOT_ALLOWED';
  end if;

  select * into v_row from public.nayanet_space_members
  where space_id = p_space_id and member_id = v_member for update;

  if v_row.id is not null and v_row.status = 'active' then
    return jsonb_build_object('status','ALREADY_MEMBER','membership',to_jsonb(v_row),'space_id',p_space_id,'member_id',v_member);
  end if;

  if v_row.id is null then
    insert into public.nayanet_space_members(space_id,member_id,role,status,joined_at,left_at)
    values(p_space_id,v_member,'member','active',now(),null)
    returning * into v_row;
  else
    update public.nayanet_space_members
      set status='active', joined_at=now(), left_at=null, updated_at=now()
      where id=v_row.id returning * into v_row;
  end if;

  v_event_id := 'space-join-' || p_space_id::text || '-' || v_member::text || '-' || extract(epoch from v_row.joined_at)::bigint::text;
  v_event := jsonb_build_object(
    'event_id',v_event_id,'type','relationship','classification','observation',
    'title','NayaNET Space membership joined',
    'content','Authenticated member joined a shared Smart Space.',
    'source','nayanet-space-membership','status','active','actor','human','confidence',1,
    'tags',jsonb_build_array('smart-space','membership','join'),
    'schema_version','NAYANET_SPACE_MEMBERSHIP_V1',
    'metadata',jsonb_build_object('space_id',p_space_id,'member_id',v_member,'role',v_row.role,'status',v_row.status)
  );
  perform public.nayanet_record_cognition_event(
    'NayaNET',v_event,'space_join',
    'Authenticated member becomes an active member of the shared Space.',
    'Membership row persisted as active.','[]'::jsonb
  );

  return jsonb_build_object('status','JOINED','membership',to_jsonb(v_row),'space_id',p_space_id,'member_id',v_member,'event_id',v_event_id);
end;
$$;

create or replace function public.nayanet_leave_space(p_space_id uuid)
returns jsonb
language plpgsql
security definer
set search_path = public
as $$
declare
  v_member uuid := auth.uid();
  v_row public.nayanet_space_members;
  v_event_id text;
  v_event jsonb;
begin
  if v_member is null then raise exception 'AUTH_REQUIRED'; end if;
  select * into v_row from public.nayanet_space_members
  where space_id = p_space_id and member_id = v_member for update;
  if v_row.id is null then raise exception 'MEMBERSHIP_NOT_FOUND'; end if;
  if v_row.status = 'left' then
    return jsonb_build_object('status','ALREADY_LEFT','membership',to_jsonb(v_row),'space_id',p_space_id,'member_id',v_member);
  end if;
  if v_row.status = 'revoked' then
    return jsonb_build_object('status','ALREADY_REVOKED','membership',to_jsonb(v_row),'space_id',p_space_id,'member_id',v_member);
  end if;

  update public.nayanet_space_members
    set status='left', left_at=now(), updated_at=now()
    where id=v_row.id returning * into v_row;

  v_event_id := 'space-leave-' || p_space_id::text || '-' || v_member::text || '-' || extract(epoch from v_row.left_at)::bigint::text;
  v_event := jsonb_build_object(
    'event_id',v_event_id,'type','relationship','classification','observation',
    'title','NayaNET Space membership left',
    'content','Authenticated member left a Smart Space.',
    'source','nayanet-space-membership','status','active','actor','human','confidence',1,
    'tags',jsonb_build_array('smart-space','membership','leave'),
    'schema_version','NAYANET_SPACE_MEMBERSHIP_V1',
    'metadata',jsonb_build_object('space_id',p_space_id,'member_id',v_member,'role',v_row.role,'status',v_row.status)
  );
  perform public.nayanet_record_cognition_event(
    'NayaNET',v_event,'space_leave',
    'Authenticated member leaves the Smart Space.',
    'Membership row transitioned to left.','[]'::jsonb
  );

  return jsonb_build_object('status','LEFT','membership',to_jsonb(v_row),'space_id',p_space_id,'member_id',v_member,'event_id',v_event_id);
end;
$$;

revoke all on function public.nayanet_join_space(uuid) from public;
grant execute on function public.nayanet_join_space(uuid) to authenticated;
revoke all on function public.nayanet_leave_space(uuid) from public;
grant execute on function public.nayanet_leave_space(uuid) to authenticated;

drop policy if exists nayanet_spaces_shared_read on public.nayanet_spaces;
create policy nayanet_spaces_shared_read
  on public.nayanet_spaces
  for select to authenticated
  using (visibility = 'shared' or owner_member_id = auth.uid());
