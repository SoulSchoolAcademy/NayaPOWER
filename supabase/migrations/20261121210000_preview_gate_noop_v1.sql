-- Preview-gate proof migration (PREVIEW-ONLY -- never merge to main).
-- Harmless, idempotent: creates a probe table on the preview branch only,
-- so the gate can prove a migration applied without touching production.
CREATE TABLE IF NOT EXISTS public.preview_gate_probe (
  id bigint PRIMARY KEY,
  note text NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now()
);
INSERT INTO public.preview_gate_probe (id, note)
VALUES (1, 'preview-gate-noop-20261121')
ON CONFLICT (id) DO NOTHING;
GRANT SELECT ON public.preview_gate_probe TO anon;
