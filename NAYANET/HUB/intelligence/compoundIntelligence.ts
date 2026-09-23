import { supabase } from '../identity/session';

export type ProjectIntelligenceRestore = {
  ok?: boolean;
  action?: string;
  result?: Record<string, unknown>;
  error?: string;
};

export async function restoreProjectIntelligence(): Promise<ProjectIntelligenceRestore | null> {
  const { data: { session } } = await supabase.auth.getSession();
  if (!session) return null;

  const { data, error } = await supabase.functions.invoke('nayanet-compound-intelligence', {
    body: { action: 'restore' },
  });

  if (error) throw error;
  if (!data || data.ok !== true) throw new Error(String(data?.error || 'PROJECT_INTELLIGENCE_RESTORE_FAILED'));
  return data as ProjectIntelligenceRestore;
}
