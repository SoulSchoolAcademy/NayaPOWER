-- Corrective migration: restore the execution-receipt -> intelligence notification trigger.
-- Root cause found 2026-09-21: the notification migration source contained the trigger,
-- but the managed database had the function and tables without the trigger attached.
-- This migration restores the missing causal edge without creating another event store.

drop trigger if exists nayanet_execution_receipt_to_intelligence_notification
on public.nayanet_execution_receipts;

create trigger nayanet_execution_receipt_to_intelligence_notification
after insert on public.nayanet_execution_receipts
for each row
execute function public.nayanet_emit_intelligence_notification_from_receipt();
