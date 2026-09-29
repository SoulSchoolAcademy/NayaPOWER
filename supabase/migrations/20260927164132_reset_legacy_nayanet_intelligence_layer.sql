
do $$
declare r record;
begin
  -- Remove the old Naya application/intelligence schema objects.
  -- Keep public.members as the existing identity bridge used by auth.
  for r in
    select tablename
    from pg_tables
    where schemaname='public'
      and tablename <> 'members'
  loop
    execute format('drop table if exists public.%I cascade', r.tablename);
  end loop;

  for r in
    select viewname
    from pg_views
    where schemaname='public'
  loop
    execute format('drop view if exists public.%I cascade', r.viewname);
  end loop;

  -- Remove old public RPCs/triggers except the auth -> members identity hook.
  for r in
    select p.oid,
           n.nspname,
           p.proname,
           pg_get_function_identity_arguments(p.oid) as args
    from pg_proc p
    join pg_namespace n on n.oid=p.pronamespace
    where n.nspname='public'
      and p.proname <> 'handle_new_user'
  loop
    execute format('drop function if exists %I.%I(%s) cascade',
                   r.nspname, r.proname, r.args);
  end loop;
end $$;
