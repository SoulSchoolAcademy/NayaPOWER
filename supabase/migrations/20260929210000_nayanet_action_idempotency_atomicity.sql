alter table public.nayanet_execution_receipts
  add column if not exists idempotency_key text;

create unique index if not exists nayanet_execution_receipts_action_idempotency_uidx
  on public.nayanet_execution_receipts(user_id, project_id, action, idempotency_key)
  where idempotency_key is not null;
