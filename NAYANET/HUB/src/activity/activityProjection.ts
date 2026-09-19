import { supabase } from '../identity/session';

export type FeatureActivity = {
  event_id: string;
  effective_at: string;
  session_id: string;
  claim_id: string;
  action_id: string;
  decision_id: string;
  authority_id: string;
  actor_id: string;
  run_id: string;
  subject: string;
  summary: string;
  evidence: unknown[];
  next_action: string;
  successor: string;
  execution_receipt_id: string | null;
  created_at: string;
};

export async function loadFeatureActivity(options: {
  feature?: string;
  from?: string;
  to?: string;
  limit?: number;
} = {}): Promise<FeatureActivity[]> {
  let query = supabase
    .from('nayanet_team_activity')
    .select('event_id,effective_at,session_id,claim_id,action_id,decision_id,authority_id,actor_id,run_id,subject,summary,evidence,next_action,successor,execution_receipt_id,created_at')
    .order('effective_at', { ascending: false })
    .limit(options.limit ?? 200);

  if (options.feature?.trim()) query = query.ilike('subject', '%' + options.feature.trim() + '%');
  if (options.from) query = query.gte('effective_at', options.from);
  if (options.to) query = query.lt('effective_at', options.to);

  const { data, error } = await query;
  if (error) throw new Error(error.message);
  return (data || []) as FeatureActivity[];
}

export function groupActivity(records: FeatureActivity[]) {
  const years = new Map<string, Map<string, Map<string, Map<string, FeatureActivity[]>>>>();
  for (const record of records) {
    const date = new Date(record.effective_at);
    if (Number.isNaN(date.getTime())) continue;
    const year = String(date.getFullYear());
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const session = record.session_id || record.event_id;
    if (!years.has(year)) years.set(year, new Map());
    const months = years.get(year)!;
    if (!months.has(month)) months.set(month, new Map());
    const days = months.get(month)!;
    if (!days.has(day)) days.set(day, new Map());
    const sessions = days.get(day)!;
    if (!sessions.has(session)) sessions.set(session, []);
    sessions.get(session)!.push(record);
  }
  return years;
}
