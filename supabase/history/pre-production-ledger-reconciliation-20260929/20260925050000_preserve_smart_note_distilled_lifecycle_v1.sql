-- Preserve the canonical Smart Note lifecycle boundary:
-- persistence/receipt verification is not the same claim as Intelligent Block lifecycle verification.
DO $$
declare
  def text;
begin
  select pg_get_functiondef(p.oid)
    into def
    from pg_proc p
    join pg_namespace n on n.oid=p.pronamespace
   where n.nspname='public'
     and p.proname='v7_create_smart_note'
     and pg_get_function_arguments(p.oid) like '%p_subject text%'
   limit 1;

  if def is null then
    raise exception 'v7_create_smart_note signature not found';
  end if;

  def := replace(
    def,
    E'    to_jsonb(\'VERIFIED\'::text),\n    true\n  );',
    E'    to_jsonb(coalesce(v_intelligent_block->''lifecycle''->>''stage'',''DISTILLED'')::text),\n    true\n  );'
  );

  def := replace(
    def,
    E'  v_intelligent_block := jsonb_set(\n    v_intelligent_block,\n    ''{lifecycle,verified_at}'',\n    to_jsonb(v_now),\n    true\n  );',
    E'  v_intelligent_block := jsonb_set(\n    v_intelligent_block,\n    ''{lifecycle,verified_at}'',\n    ''null''::jsonb,\n    true\n  );'
  );

  execute def;
end $$;