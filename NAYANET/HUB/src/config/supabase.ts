const DEFAULT_SUPABASE_URL='https://dahisasgpfvziswqvmvm.supabase.co';
// Publishable Supabase key: intentionally client-safe and never a service-role/secret key.
const DEFAULT_SUPABASE_PUBLISHABLE_KEY='sb_publishable_oQFKOYFuJ9bT-E9QkJUb4g_lAUyInue';
export const SUPABASE_URL=import.meta.env.VITE_SUPABASE_URL||DEFAULT_SUPABASE_URL;
export const SUPABASE_PUBLISHABLE_KEY=import.meta.env.VITE_SUPABASE_PUBLISHABLE_KEY||DEFAULT_SUPABASE_PUBLISHABLE_KEY;
