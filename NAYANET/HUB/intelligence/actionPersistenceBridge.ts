import { rememberIntelligence } from './cognition';

type PersistedState = {
  favorite?: boolean;
  save?: boolean;
  like?: boolean;
  love?: boolean;
  rating?: number;
  comments?: string[];
  links?: string[];
  space?: { id?: string; name?: string; purpose?: string; visibility?: string; created_at?: string };
};

const PREFIX = 'nayanet:smart-feed-board:v4:';
const BRIDGE_FLAG = '__nayanetSmartFeedActionBridgeInstalled';
const ACTION_KEYS = ['favorite', 'save', 'like', 'love', 'rating', 'comments', 'links', 'space'] as const;

type ActionKey = (typeof ACTION_KEYS)[number];

function changedActions(before: PersistedState, after: PersistedState): ActionKey[] {
  return ACTION_KEYS.filter((key) => JSON.stringify(before?.[key] ?? null) !== JSON.stringify(after?.[key] ?? null));
}

function describeAction(key: ActionKey, after: PersistedState): string {
  if (key === 'rating') return `Rated intelligence ${after.rating ?? 0}/5.`;
  if (key === 'comments') return `Added a contextual comment to the intelligence.`;
  if (key === 'links') return `Updated connected intelligence links.`;
  if (key === 'space') return `Created or updated a Smart Space draft for the intelligence.`;
  return `${key.toUpperCase()} intelligence: ${after[key] ? 'ON' : 'OFF'}.`;
}

function install() {
  const target = window as typeof window & Record<string, unknown>;
  if (target[BRIDGE_FLAG]) return;
  target[BRIDGE_FLAG] = true;

  const originalSetItem = window.localStorage.setItem.bind(window.localStorage);
  window.localStorage.setItem = (key: string, value: string) => {
    const previous = key.startsWith(PREFIX) ? window.localStorage.getItem(key) : null;
    originalSetItem(key, value);

    if (!key.startsWith(PREFIX) || previous === value || !window.NayaNetCognition) return;

    let before: PersistedState = {};
    let after: PersistedState = {};
    try {
      before = previous ? JSON.parse(previous) : {};
      after = JSON.parse(value);
    } catch {
      return;
    }

    const eventId = key.slice(PREFIX.length);
    const actions = changedActions(before, after);
    actions.forEach((action) => {
      void rememberIntelligence({
        event_id: `${eventId}:action:${action}:${Date.now()}`,
        title: `Smart Feed ${action} action`,
        content: describeAction(action, after),
        source: 'nayanet-hub.smart-feed',
        project: 'NayaNET',
        status: 'active',
        actor: 'human',
        tags: ['intelligent-hub', 'smart-feed', 'activity', action],
        metadata: {
          event_id: eventId,
          action,
          persisted_state: after,
          persistence_boundary: 'nayanet-cognitive-engine',
        },
      }).catch(() => undefined);
    });
  };
}

if (typeof window !== 'undefined') {
  if (window.NayaNetCognition) install();
  else window.addEventListener('nayanet:cognition-ready', install, { once: true });
}
