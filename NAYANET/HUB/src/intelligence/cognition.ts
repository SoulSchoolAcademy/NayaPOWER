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

type RuntimeEvent = CognitiveEventInput & {
  event_id: string;
  created_at?: string;
  metadata?: Record<string, unknown>;
};

type CognitiveApi = {
  init: (project?: string) => Promise<CognitivePersistence>;
  recordPersistent: (input: CognitiveEventInput) => Promise<{persisted?: boolean; persistence: CognitivePersistence}>;
  persistence: () => CognitivePersistence;
  verify: () => {valid: boolean; events: number; receipts: number; indexed: boolean; persistence: CognitivePersistence};
  handoff: (reason?: string, project?: string) => unknown;
};

type SpaceMember={id?:string;space_id?:string;member_id:string;role?:string;status?:string;joined_at?:string;left_at?:string;source_type?:string;source_id?:string;display_name?:string;smart_name?:string};
type DreamReplay={id?:string;event_id?:string;status?:string;summary?:string;description?:string;[key:string]:unknown};

type AssistantRuntimeApi = {
  init: () => Promise<{authenticated?: boolean}>;
  snapshot: () => {authenticated?: boolean; user_id?: string};
  record: (input: CognitiveEventInput) => Promise<unknown>;
  retrieve: (eventId?: string) => Promise<RuntimeEvent[]>;
  retrieveSmartFeedActions: (sourceEventId: string) => Promise<RuntimeEvent[]>;
  listSpaceMembers: (spaceId: string) => Promise<SpaceMember[]>;
  listDreamReplays: () => Promise<DreamReplay[]>;
  dreamReplay: (input?: {event_id?: string; idempotency_key?: string}) => Promise<DreamReplay>;
  recordLearningEvidence: (input: {claim: string; target_id?: string; source_event_id?: string; provenance?: string; verification_method?: string}) => Promise<unknown>;
  createSpace: (input: {name: string; purpose: string; visibility?: 'private'|'shared'}) => Promise<{id: string; name: string; purpose: string; visibility: string; created_at: string}>;
  saveConnection: (targetMemberId: string, spaceId: string) => Promise<unknown>;
  createSmartList: (name: string) => Promise<unknown>;
  listSmartLists: () => Promise<unknown[]>;
  smartFeed: (input?: {stream?: string; limit?: number; before?: string|null}) => Promise<unknown>;
  smartFeedAction: (input?: {action?: string; stream?: string|null; source_id?: string|null; publication_id?: string|null; interaction?: string|null}) => Promise<unknown>;
  publishSmartFeed: (input: {sourceEventId: string; sourceTitle?: string; sourceContent?: string}) => Promise<unknown>;
};

declare global {
  interface Window {
    NayaNetCognition?: CognitiveApi;
    NayaAssistantRuntime?: AssistantRuntimeApi;
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

export async function persistSmartFeedAction(input: {
  sourceEventId: string;
  action: string;
  value: unknown;
  state: Record<string, unknown>;
}) {
  const runtime = window.NayaAssistantRuntime;
  if (!runtime) throw new Error('ASSISTANT_RUNTIME_UNAVAILABLE');
  const session = runtime.snapshot();
  if (!session?.authenticated) throw new Error('AUTH_REQUIRED');
  const eventId = crypto.randomUUID();
  const result = await runtime.record({
    event_id: eventId,
    title: 'Smart Feed ' + input.action + ' action',
    content: JSON.stringify({
      source_event_id: input.sourceEventId,
      action: input.action,
      value: input.value,
    }),
    source: 'nayanet-hub.smart-feed.action',
    project: 'NayaNET',
    status: 'active',
    actor: 'human',
    tags: ['intelligent-hub', 'smart-feed', 'action', input.action],
    metadata: {
      source_event_id: input.sourceEventId,
      action: input.action,
      value: input.value,
      state: input.state,
      persistence_boundary: 'authenticated-cognition',
    },
  });
  const payload = result as {receipt?: {id?: string; receipt_id?: string}; state?: {revision?: number}; event?: {event_id?: string}} | null;
  const receiptId = payload?.receipt?.receipt_id || payload?.receipt?.id || '';
  return {eventId, receiptId, revision: payload?.state?.revision, result};
}

export async function retrieveSmartFeedActions(sourceEventId: string) {
  const runtime = window.NayaAssistantRuntime;
  if (!runtime) throw new Error('ASSISTANT_RUNTIME_UNAVAILABLE');
  if (!runtime.snapshot()?.authenticated) {
    await new Promise<void>((resolve) => {
      let settled = false;
      const finish = () => {
        if (settled) return;
        settled = true;
        window.removeEventListener('naya-auth-state', onAuthState);
        window.clearTimeout(timer);
        resolve();
      };
      const onAuthState = (event: Event) => {
        const detail = (event as CustomEvent<{authenticated?: boolean}>).detail;
        if (detail?.authenticated) finish();
      };
      const timer = window.setTimeout(finish, 10000);
      window.addEventListener('naya-auth-state', onAuthState);
      if (runtime.snapshot()?.authenticated) finish();
    });
  }
  if (!runtime.snapshot()?.authenticated) return [];
  return runtime.retrieveSmartFeedActions(sourceEventId);
}

export async function createCanonicalPrivateSpace(input: {name: string; purpose: string}) {
  const runtime = window.NayaAssistantRuntime;
  if (!runtime) throw new Error('ASSISTANT_RUNTIME_UNAVAILABLE');
  const session = runtime.snapshot();
  if (!session?.authenticated) throw new Error('AUTH_REQUIRED');
  const name = input.name.trim();
  const purpose = input.purpose.trim();
  if (!name || !purpose) throw new Error('SPACE_NAME_AND_PURPOSE_REQUIRED');
  const space = await runtime.createSpace({name, purpose, visibility: 'private'});
  if (!space?.id) throw new Error('CANONICAL_SPACE_ID_NOT_RETURNED');
  return space;
}

export async function createCanonicalConnection(input: {targetMemberId: string; spaceId: string}) {
  const runtime = window.NayaAssistantRuntime;
  if (!runtime) throw new Error('ASSISTANT_RUNTIME_UNAVAILABLE');
  const session = runtime.snapshot();
  if (!session?.authenticated) throw new Error('AUTH_REQUIRED');
  const targetMemberId = input.targetMemberId.trim();
  const spaceId = input.spaceId.trim();
  if (!targetMemberId || !spaceId) throw new Error('TARGET_MEMBER_AND_SHARED_SPACE_REQUIRED');
  if (targetMemberId === (session as {user_id?: string}).user_id) throw new Error('CONNECTION_TARGET_MUST_BE_DIFFERENT_MEMBER');
  const result = await runtime.saveConnection(targetMemberId, spaceId);
  const payload = result as {connection_id?: string; id?: string; connection?: {id?: string}} | null;
  const connectionId = payload?.connection_id || payload?.id || payload?.connection?.id || '';
  if (!connectionId) throw new Error('CANONICAL_CONNECTION_ID_NOT_RETURNED');
  return {connectionId, result};
}
