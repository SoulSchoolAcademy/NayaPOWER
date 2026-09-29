alter table public.maxess_results add column if not exists topic text;

comment on column public.maxess_results.topic is 'Normalized topic selected by the member for this MAXESS assessment; report_payload remains the canonical result payload.';
