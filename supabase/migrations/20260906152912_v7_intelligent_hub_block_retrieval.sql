create or replace function public.v7_list_smart_note_events()
returns setof jsonb
language sql
security definer
set search_path to 'public'
as $$
  select jsonb_build_object(
    'event_id', e.id,
    'subject', e.subject,
    'event_type', e.event_type,
    'privacy_state', e.privacy_state,
    'status', e.status,
    'created_at', e.created_at,
    'artifacts', coalesce((
      select jsonb_object_agg(lower(replace(a.artifact_type,'_NOTE','')), jsonb_build_object(
        'type', a.artifact_type,
        'content', a.content,
        'artifact_url', a.artifact_url,
        'created_at', a.created_at
      )) from public.smart_note_artifacts a where a.event_id=e.id
    ), '{}'::jsonb),
    'intelligent_block', coalesce((
      select t.intelligent_block from public.v7_smart_note_transactions t
      where t.user_id=auth.uid() and t.evidence->>'event_id'=e.id::text
      order by t.created_at desc limit 1
    ), '{}'::jsonb),
    'evidence', coalesce((
      select t.evidence from public.v7_smart_note_transactions t
      where t.user_id=auth.uid() and t.evidence->>'event_id'=e.id::text
      order by t.created_at desc limit 1
    ), '{}'::jsonb),
    'receipt', (
      select jsonb_build_object('status', r.status, 'receipt_url', r.receipt_url, 'verification', r.verification, 'created_at', r.created_at)
      from public.smart_note_receipts r where r.event_id=e.id limit 1
    )
  )
  from public.smart_note_events e
  where e.member_id = auth.uid()
  order by e.created_at desc;
$$;

revoke execute on function public.v7_list_smart_note_events() from anon;
revoke execute on function public.v7_list_smart_note_events() from public;
grant execute on function public.v7_list_smart_note_events() to authenticated;

create or replace function public.v7_list_smart_notes()
returns setof public.v7_smart_note_transactions
language sql
security definer
set search_path to 'public'
as $$
  select * from public.v7_smart_note_transactions
  where user_id = auth.uid()
  order by created_at desc;
$$;
revoke execute on function public.v7_list_smart_notes() from anon;
revoke execute on function public.v7_list_smart_notes() from public;
grant execute on function public.v7_list_smart_notes() to authenticated;
