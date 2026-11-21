-- Preview-gate fail-closed proof (PREVIEW-ONLY -- never merge to main).
-- Deliberately invalid: references a table that does not exist.
-- The gate must fail on THIS file and apply nothing after it.
SELECT * FROM public.preview_gate_nonexistent_table_xyz;
