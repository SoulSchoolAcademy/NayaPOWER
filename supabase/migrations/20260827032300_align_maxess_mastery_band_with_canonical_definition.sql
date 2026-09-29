ALTER TABLE public.maxess_results DROP CONSTRAINT IF EXISTS maxess_results_mastery_band_check;
ALTER TABLE public.maxess_results ADD CONSTRAINT maxess_results_mastery_band_check CHECK (mastery_band = ANY (ARRAY['foundation'::text, 'developing'::text, 'advancing'::text, 'mastery'::text]));
