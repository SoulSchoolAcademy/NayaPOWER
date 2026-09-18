/* NayaNET Intelligent Block — canonical sender/receiver foundation v1 */
(function (global) {
  'use strict';

  const PERSPECTIVES = [
    { key: 'human', label: 'HUMAN NOTE', icon: '👤', tone: 'magenta', featured: false },
    { key: 'child', label: 'CHILD NOTE', icon: '👶', tone: 'purple', featured: false },
    { key: 'grandma', label: 'GRANDMA NOTE', icon: '👵', tone: 'indigo', featured: false },
    { key: 'naya', label: 'NAYA NOTE', icon: '✨', tone: 'sapphire', featured: false },
    { key: 'machine', label: 'MACHINE NOTE', icon: '⚙️', tone: 'green', featured: false }
  ];

  const STORAGE_KEY = 'nayanet:intelligence-events:v1';

  function text(value) {
    return typeof value === 'string' ? value.trim() : '';
  }

  function escapeHtml(value) {
    return text(value)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function normalizePerspective(value) {
    if (typeof value === 'string') return { text: text(value) };
    if (!value || typeof value !== 'object') return null;
    const result = { text: text(value.text) };
    if (text(value.author)) result.author = text(value.author);
    return result.text ? result : null;
  }

  function normalize(event) {
    if (!event || typeof event !== 'object') throw new Error('INTELLIGENCE_EVENT_INVALID');
    const id = text(event.id);
    if (!id) throw new Error('INTELLIGENCE_EVENT_ID_REQUIRED');

    const perspectives = {};
    PERSPECTIVES.forEach(function (definition) {
      const normalized = normalizePerspective(event.perspectives && event.perspectives[definition.key]);
      if (normalized) perspectives[definition.key] = normalized;
    });

    return {
      id,
      createdAt: text(event.createdAt) || new Date().toISOString(),
      source: event.source && typeof event.source === 'object' ? { ...event.source } : { type: 'unknown' },
      scope: event.scope === 'collective' ? 'collective' : 'personal',
      subject: text(event.subject),
      nutshell: text(event.nutshell),
      perspectives,
      lesson: text(event.lesson),
      howToUse: text(event.howToUse),
      interactions: event.interactions && typeof event.interactions === 'object' ? { ...event.interactions } : {}
    };
  }

  function readState() {
    try {
      const parsed = JSON.parse(global.localStorage.getItem(STORAGE_KEY) || '{}');
      return parsed && typeof parsed === 'object' ? parsed : {};
    } catch (_) {
      return {};
    }
  }

  function writeState(state) {
    try { global.localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); } catch (_) {}
  }

  function receive(event) {
    const normalized = normalize(event);
    const state = readState();
    const existed = Boolean(state[normalized.id]);
    state[normalized.id] = normalized;
    writeState(state);
    return {
      status: existed ? 'DUPLICATE_IDEMPOTENT' : 'RECEIVED_STORED',
      event: normalized
    };
  }

  function perspectiveHtml(definition, value) {
    if (!value || !value.text) return '';
    const author = value.author ? '<span class="intelligence-perspective-author">' + escapeHtml(value.author) + '</span>' : '';
    return '<section class="intelligence-perspective intelligence-perspective-' + definition.key + '" data-tone="' + definition.tone + '">' +
      '<div class="intelligence-perspective-head"><span class="intelligence-perspective-icon" aria-hidden="true">' + definition.icon + '</span><h4>' + definition.label + '</h4>' + author + '</div>' +
      '<p>' + escapeHtml(value.text).replace(/\n/g, '<br>') + '</p>' +
      '</section>';
  }

  function render(event) {
    const normalized = normalize(event);
    const perspectiveMarkup = PERSPECTIVES.map(function (definition) {
      return perspectiveHtml(definition, normalized.perspectives[definition.key]);
    }).join('');

    const nutshell = normalized.nutshell ? '<section class="intelligence-feature intelligence-nutshell"><div class="intelligence-feature-head"><span aria-hidden="true">🌟</span><h3>IN A NUTSHELL</h3></div><p>' + escapeHtml(normalized.nutshell).replace(/\n/g, '<br>') + '</p></section>' : '';
    const lesson = normalized.lesson ? '<section class="intelligence-feature intelligence-lesson"><div class="intelligence-feature-head"><span aria-hidden="true">💡</span><h3>LESSON</h3></div><p>' + escapeHtml(normalized.lesson).replace(/\n/g, '<br>') + '</p></section>' : '';
    const howToUse = normalized.howToUse ? '<section class="intelligence-feature intelligence-how-to-use"><div class="intelligence-feature-head"><span aria-hidden="true">🧭</span><h3>HOW TO USE IT</h3></div><p>' + escapeHtml(normalized.howToUse).replace(/\n/g, '<br>') + '</p></section>' : '';

    return '<article class="intelligent-block intelligent-block-v1" data-intelligence-id="' + escapeHtml(normalized.id) + '" data-scope="' + normalized.scope + '">' +
      nutshell + perspectiveMarkup + lesson + howToUse +
      '</article>';
  }

  function receiveAndRender(event, mount) {
    const result = receive(event);
    if (!mount || typeof mount.innerHTML !== 'string') throw new Error('INTELLIGENCE_RENDER_TARGET_REQUIRED');
    mount.innerHTML = render(result.event);
    return { ...result, status: result.status === 'DUPLICATE_IDEMPOTENT' ? 'RENDERED_IDEMPOTENT' : 'RECEIVED_NORMALIZED_RENDERED' };
  }

  global.NayaIntelligence = Object.freeze({
    version: '1.0.0',
    perspectives: PERSPECTIVES,
    normalize,
    receive,
    render,
    receiveAndRender,
    storageKey: STORAGE_KEY
  });
})(window);
