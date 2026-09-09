export type CognitivePersistence = {
  mode: string;
  status: string;
  user_id?: string;
  project?: string;
  last_sync_at?: string;
  last_write_at?: string;
  last_error?: string;
};

type CognitiveEventInput = {
  event_id?: string;
  title?: string;
  content?: string;
  source?: string;
  project?: string;
  status?: string;
  actor?: string;
  tags?: string[];
  metadata?: Record<string, unknown>;
};

type CognitiveApi = {
  init: (project?: string) => Promise<CognitivePersistence>;
  recordPersistent: (input: CognitiveEventInput) => Promise<{persisted?: boolean; persistence: CognitivePersistence}>;
  persistence: () => CognitivePersistence;
  verify: () => {valid: boolean; events: number; receipts: number; indexed: boolean; persistence: CognitivePersistence};
  handoff: (reason?: string, project?: string) => unknown;
};

declare global {
  interface Window {
    NayaNetCognition?: CognitiveApi;
  }
}

export async function initializeCognition(): Promise<CognitivePersistence> {
  if (!window.NayaNetCognition) {
    return {mode: 'unavailable', status: 'engine_not_loaded'};
  }
  return window.NayaNetCognition.init('NayaNET');
}

export async function rememberIntelligence(input: CognitiveEventInput) {
  if (!window.NayaNetCognition) {
    return {persisted: false, persistence: {mode: 'unavailable', status: 'engine_not_loaded'}};
  }
  return window.NayaNetCognition.recordPersistent({...input, project: 'NayaNET'});
}
