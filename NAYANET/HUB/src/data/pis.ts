import type {IntelligentEvent} from '../intelligence/types';

export type PISFeed = {
  schema_version: string;
  generated_at: string;
  source: string;
  event_count: number;
  events: IntelligentEvent[];
};

const PIS_URL = '/intelligence/pis-feed.json';

export async function loadPrimaryIntelligence(): Promise<PISFeed> {
  const response = await fetch(PIS_URL, {cache: 'no-store'});
  if (!response.ok) throw new Error(`PIS_FEED_HTTP_${response.status}`);
  const payload = (await response.json()) as PISFeed;
  if (!payload || !Array.isArray(payload.events)) throw new Error('PIS_FEED_INVALID');
  return payload;
}

export function sortPrimaryIntelligence(events: IntelligentEvent[]): IntelligentEvent[] {
  return [...events].sort((a, b) => Date.parse(b.created_at) - Date.parse(a.created_at));
}
