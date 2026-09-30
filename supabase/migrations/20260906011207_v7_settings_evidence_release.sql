alter table public.v7_profiles add column if not exists settings jsonb not null default '{}'::jsonb;
create or replace function public.v7_update_profile_settings(p_settings jsonb)
returns public.v7_profiles
language plpgsql security definer set search_path=public
as $$
declare r public.v7_profiles;
begin
 if auth.uid() is null then raise exception 'AUTHENTICATED_SESSION_REQUIRED'; end if;
 update public.v7_profiles set settings=coalesce(p_settings,'{}'::jsonb) where user_id=auth.uid() returning * into r;
 if not found then
   insert into public.v7_profiles(user_id,alias,settings) values(auth.uid(),'Naya'||substr(md5(auth.uid()::text),1,8),coalesce(p_settings,'{}'::jsonb)) returning * into r;
 end if;
 return r;
end;$$;
revoke all on function public.v7_update_profile_settings(jsonb) from public;
grant execute on function public.v7_update_profile_settings(jsonb) to authenticated;
