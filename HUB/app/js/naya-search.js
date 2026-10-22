/*
 * naya-search.js — Command + universal search for the Hub
 * (Best-of-Best map element #12, build-order step 13 — the Linear
 * lesson: one place to find and do anything).
 *
 * One search surface over the object types that exist: people (the
 * timeline read model's identity registry), Smart Notes, Naya Notes,
 * Smart Mail threads, and Smart Links. The service is the
 * search_universal RPC (migration 20261022210000_universal_search_v1):
 * ranking and owner isolation live THERE, behind the caller's JWT —
 * this module never sends an owner identity, because there is nothing
 * a client may say about whose objects it may see.
 *
 * What this module provides:
 *   - parseQuery / parseVoiceIntent: the pure query logic. Voice entry
 *     ("Naya, find Maria") and typed entry converge on ONE query here,
 *     so the spoken path can never drift from the typed path.
 *   - rankResults / groupByType / normalizeResult: the merge of the
 *     service's ranked rows into the one result set the palette shows —
 *     cross-type, deduped, capped, each result carrying its action.
 *   - createStore({ supabaseUrl, anonKey, getAccessToken, fetchImpl }):
 *     REST transport in the bridge's pattern. Without an authenticated
 *     session token every call refuses with { not_verified } and sends
 *     NOTHING — search never fakes a result. The Hub wires the session
 *     through window.NayaSearchSession when the auth lane provides one.
 *   - mountPalette(bodyEl, opts): the command palette — input, dictation
 *     (Web Speech API where present, honestly absent where not), the
 *     ranked results, full keyboard flow (arrows / Enter / Esc).
 *   - installHotkey(doc, openFn): Cmd-K / Ctrl-K parity (feature 5).
 *
 * Dual runtime like supabase-bridge.js and naya-notes.js: browser
 * (window.NayaSearch) and Node (module.exports) share this one file.
 */
(function (global) {
  'use strict';

  var MAX_QUERY = 200;
  var DEFAULT_LIMIT = 20;
  var MAX_LIMIT = 50;

  // The five object types, in the order groups render. The service's
  // merged ranking is the primary order; grouping is a lens, not a
  // re-rank.
  var TYPES = ['person', 'smart_note', 'naya_note', 'mail_thread', 'smart_link'];
  var TYPE_LABELS = {
    person: 'People',
    smart_note: 'Smart Notes',
    naya_note: 'Naya Notes',
    mail_thread: 'Smart Mail',
    smart_link: 'Smart Links',
  };
  // Where an open_room / open_person action lands in the Hub router
  // (#/hub/:room). smart_link results carry open_url instead.
  var TYPE_ROOMS = {
    person: 'connections',
    smart_note: 'feed',
    naya_note: 'lists',
    mail_thread: 'mail',
  };

  // ── Pure query logic ──────────────────────────────────────────────

  function parseQuery(raw) {
    var q = String(raw == null ? '' : raw).replace(/\s+/g, ' ').trim();
    if (!q) return { ok: false, reason: 'empty' };
    if (q.length > MAX_QUERY) return { ok: false, reason: 'too_long' };
    return { ok: true, query: q };
  }

  // Voice intent: the wake word and the intent verbs are packaging,
  // not query. "Naya, find Maria" / "find Maria" / "search for Maria" /
  // "show me Maria" / "look up Maria" all reduce to the query "Maria".
  // A transcript with no intent packaging passes through whole — it is
  // still a search, never a dead end.
  var VOICE_PREFIXES = [
    /^naya[,\s]+find\s+/i,
    /^naya[,\s]+search\s+(for\s+)?/i,
    /^naya[,\s]+show\s+me\s+/i,
    /^naya[,\s]+look\s+up\s+/i,
    /^naya[,\s]+open\s+/i,
    /^naya[,\s]+/i,
    /^find\s+/i,
    /^search\s+(for\s+)?/i,
    /^show\s+me\s+/i,
    /^look\s+up\s+/i,
    /^open\s+/i,
  ];

  function parseVoiceIntent(transcript) {
    var raw = String(transcript == null ? '' : transcript).replace(/\s+/g, ' ').trim();
    if (!raw) return { intent: 'none', query: '' };
    // A bare wake word is an address, not a search.
    if (/^naya[,.!?\s]*$/i.test(raw)) return { intent: 'none', query: '' };
    for (var i = 0; i < VOICE_PREFIXES.length; i++) {
      if (VOICE_PREFIXES[i].test(raw)) {
        var rest = raw.replace(VOICE_PREFIXES[i], '').trim();
        // A bare wake word ("Naya") leaves nothing to search for.
        if (!rest) return { intent: 'none', query: '' };
        return { intent: 'search', query: rest };
      }
    }
    return { intent: 'search', query: raw };
  }

  // ── Result shaping ────────────────────────────────────────────────

  // The service row shape is the contract (docs/universal-search.md).
  // normalizeResult coerces defensively and derives the action when a
  // row arrives without one, so a result is never rendered dead.
  function normalizeResult(row) {
    if (!row || typeof row !== 'object') return null;
    var type = String(row.object_type || '');
    if (TYPES.indexOf(type) === -1) return null;
    var kind = String(row.action_kind || '');
    var target = row.action_target == null ? '' : String(row.action_target);
    if (!kind) {
      if (type === 'smart_link') { kind = 'open_url'; }
      else if (type === 'person') { kind = 'open_person'; target = target || String(row.object_id || ''); }
      else { kind = 'open_room'; target = TYPE_ROOMS[type] || ''; }
    }
    return {
      type: type,
      id: row.object_id == null ? '' : String(row.object_id),
      title: String(row.title || ''),
      snippet: String(row.snippet || ''),
      score: typeof row.score === 'number' ? row.score : 0,
      occurred_at: row.occurred_at || null,
      action: { kind: kind, target: target },
    };
  }

  // The one ranked set: normalize, dedupe by (type, id) keeping the
  // strongest, sort score desc then recency desc, cap. Rows without an
  // id dedupe by (type, title) — a wall note has no id to key on.
  function rankResults(rows, limit) {
    var cap = Math.min(Math.max(1, limit || DEFAULT_LIMIT), MAX_LIMIT);
    var seen = {};
    var out = [];
    (rows || []).forEach(function (row) {
      var r = normalizeResult(row);
      if (!r) return;
      var key = r.type + '|' + (r.id || r.title);
      if (seen[key]) return;
      seen[key] = true;
      out.push(r);
    });
    out.sort(function (a, b) {
      if (b.score !== a.score) return b.score - a.score;
      var ta = a.occurred_at ? Date.parse(a.occurred_at) : 0;
      var tb = b.occurred_at ? Date.parse(b.occurred_at) : 0;
      return tb - ta;
    });
    return out.slice(0, cap);
  }

  function groupByType(results) {
    var groups = {};
    (results || []).forEach(function (r) {
      if (!groups[r.type]) groups[r.type] = [];
      groups[r.type].push(r);
    });
    return TYPES.filter(function (t) { return groups[t]; })
      .map(function (t) { return { type: t, label: TYPE_LABELS[t], results: groups[t] }; });
  }

  // The default action runner: the palette's Enter. open_room and
  // open_person route in the Hub (#/hub/:room, carrying the object ref
  // in the action for the room to consume); open_url opens the link.
  // A wiring may replace this with opts.onAction.
  function defaultAction(result, env) {
    env = env || {};
    var loc = env.location || global.location;
    var open = env.open || (typeof global.open === 'function' ? global.open.bind(global) : null);
    if (!result || !result.action) return { acted: false, reason: 'no_action' };
    var kind = result.action.kind;
    var target = result.action.target || '';
    if (kind === 'open_url') {
      if (open && target) { open(target, '_blank', 'noopener'); return { acted: true, via: 'open_url' }; }
      return { acted: false, reason: 'no_opener' };
    }
    if (kind === 'open_person') {
      if (loc) { loc.hash = '#/hub/connections'; return { acted: true, via: 'open_person', ref: target }; }
      return { acted: false, reason: 'no_location' };
    }
    if (kind === 'open_room') {
      var room = target || TYPE_ROOMS[result.type] || '';
      if (loc && room) { loc.hash = '#/hub/' + room; return { acted: true, via: 'open_room', ref: result.id }; }
      return { acted: false, reason: 'no_location' };
    }
    return { acted: false, reason: 'unknown_kind' };
  }

  // Keyboard navigation as pure math, so the palette's flow is testable
  // without a DOM: wrap-around in both directions, -1 = nothing active.
  function moveActive(index, delta, count) {
    if (!count) return -1;
    if (index < 0) return delta >= 0 ? 0 : count - 1;
    return ((index + delta) % count + count) % count;
  }

  // ── Store (transport injected; session required) ──────────────────

  function createStore(opts) {
    opts = opts || {};
    var fetchImpl = opts.fetchImpl || (typeof fetch !== 'undefined' ? fetch : null);
    var base = String(opts.supabaseUrl || '').replace(/\/$/, '') + '/rest/v1/rpc/search_universal';

    function sessionToken() {
      try {
        return typeof opts.getAccessToken === 'function' ? opts.getAccessToken() : null;
      } catch (e) {
        return null;
      }
    }

    function notVerified(reason) {
      return { not_verified: true, reason: reason };
    }

    return {
      // The request body is { p_query, p_limit } and NOTHING else:
      // identity rides the JWT alone. There is no owner field a caller
      // could spoof — that absence is the isolation boundary's client
      // half, and the tests pin it.
      search: function (rawQuery, searchOpts) {
        var parsed = parseQuery(rawQuery);
        if (!parsed.ok) return Promise.resolve({ invalid: true, reason: parsed.reason, results: [] });
        var token = sessionToken();
        if (!token) return Promise.resolve({ not_verified: true, reason: 'no_session', results: [] });
        var limit = Math.min(Math.max(1, (searchOpts && searchOpts.limit) || DEFAULT_LIMIT), MAX_LIMIT);
        return fetchImpl(base, {
          method: 'POST',
          headers: {
            apikey: opts.anonKey,
            Authorization: 'Bearer ' + token,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ p_query: parsed.query, p_limit: limit }),
        }).then(function (res) {
          if (!res.ok) return { not_verified: true, reason: 'http_' + res.status, results: [] };
          return res.json().then(function (rows) {
            return { results: rankResults(rows, limit) };
          });
        });
      },
    };
  }

  // ── Dictation ─────────────────────────────────────────────────────
  // Same injected-recognition pattern as naya-notes.js: support is
  // detected, never assumed; the transcript routes through
  // parseVoiceIntent so voice and typing share one query path.

  function createDictation(opts) {
    opts = opts || {};
    var Ctor = opts.recognitionCtor !== undefined
      ? opts.recognitionCtor
      : (global.SpeechRecognition || global.webkitSpeechRecognition || null);
    return {
      supported: !!Ctor,
      start: function (onText, onState) {
        if (!Ctor) return null;
        var rec = new Ctor();
        rec.lang = opts.lang || 'en-US';
        rec.interimResults = false;
        rec.continuous = false;
        rec.onresult = function (event) {
          for (var i = event.resultIndex; i < event.results.length; i++) {
            if (event.results[i].isFinal) {
              onText(event.results[i][0].transcript.trim());
            }
          }
        };
        rec.onend = function () { if (onState) onState('idle'); };
        rec.onerror = function () { if (onState) onState('idle'); };
        if (onState) onState('listening');
        rec.start();
        return rec;
      },
    };
  }

  // ── The command palette ───────────────────────────────────────────

  function mountPalette(bodyEl, opts) {
    opts = opts || {};
    var doc = bodyEl.ownerDocument || bodyEl;
    var store = opts.store;
    var dictation = opts.dictation || createDictation();
    var onAction = typeof opts.onAction === 'function'
      ? opts.onAction
      : function (result) { return defaultAction(result); };

    var style = doc.createElement('style');
    style.textContent =
      '.ns-overlay{position:fixed;inset:0;z-index:1200;display:none;' +
      'background:rgba(5,4,10,.62);backdrop-filter:blur(3px)}' +
      '.ns-overlay.open{display:block}' +
      '.ns-panel{max-width:640px;margin:9vh auto 0;background:#12101d;color:inherit;' +
      'border:1px solid rgba(157,117,255,.4);border-radius:16px;overflow:hidden;' +
      'box-shadow:0 24px 60px rgba(0,0,0,.6)}' +
      '.ns-row{display:flex;gap:8px;align-items:center;padding:12px}' +
      '.ns-input{flex:1;background:rgba(255,255,255,.05);border:1px solid rgba(157,117,255,.35);' +
      'border-radius:10px;color:inherit;padding:10px 12px;font:inherit;font-size:15px}' +
      '.ns-btn{background:linear-gradient(135deg,#9d75ff,#00c8ff);color:#0b0b14;border:0;' +
      'border-radius:10px;padding:9px 13px;font:inherit;font-size:13px;font-weight:700;cursor:pointer}' +
      '.ns-btn[disabled]{opacity:.45;cursor:default}' +
      '.ns-btn.listening{background:linear-gradient(135deg,#ffd75e,#ff5e8a)}' +
      '.ns-state{padding:0 14px 10px;font-size:12.5px;color:#a7a7c9}' +
      '.ns-results{max-height:52vh;overflow:auto;padding:0 8px 10px}' +
      '.ns-group{font-size:11px;letter-spacing:.14em;color:#a7a7c9;padding:10px 8px 4px}' +
      '.ns-item{display:block;width:100%;text-align:left;background:none;border:0;color:inherit;' +
      'border-radius:10px;padding:9px 10px;font:inherit;cursor:pointer}' +
      '.ns-item .ns-title{font-size:14px;display:block;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}' +
      '.ns-item .ns-snippet{font-size:12px;color:#a7a7c9;display:block}' +
      '.ns-item.active{background:rgba(157,117,255,.18)}';
    bodyEl.appendChild(style);

    var overlay = doc.createElement('div');
    overlay.className = 'ns-overlay';
    overlay.innerHTML =
      '<div class="ns-panel" role="dialog" aria-modal="true" aria-label="Command search">' +
      '<div class="ns-row">' +
      '<input class="ns-input" data-ns="input" type="search" placeholder="Find a person, note, thread, link… (or tap the mic)" aria-label="Search your world" autocomplete="off">' +
      '<button type="button" class="ns-btn" data-ns="mic">Speak</button>' +
      '</div>' +
      '<div class="ns-state" data-ns="state" role="status"></div>' +
      '<div class="ns-results" data-ns="results" role="listbox"></div>' +
      '</div>';
    bodyEl.appendChild(overlay);

    var q = function (name) { return overlay.querySelector('[data-ns="' + name + '"]'); };
    var input = q('input'), stateEl = q('state'), zone = q('results'), micBtn = q('mic');
    var results = [];
    var active = -1;
    var debounce = null;

    if (!dictation.supported) {
      micBtn.disabled = true;
      micBtn.textContent = 'Voice unavailable here';
    }

    function setState(msg) { stateEl.textContent = msg; }

    function render() {
      zone.innerHTML = '';
      var flat = 0;
      groupByType(results).forEach(function (group) {
        var head = doc.createElement('div');
        head.className = 'ns-group';
        head.textContent = group.label.toUpperCase();
        zone.appendChild(head);
        group.results.forEach(function (r) {
          var idx = flat++;
          var item = doc.createElement('button');
          item.type = 'button';
          item.className = 'ns-item' + (idx === active ? ' active' : '');
          item.setAttribute('role', 'option');
          var title = doc.createElement('span');
          title.className = 'ns-title';
          title.textContent = r.title || '(untitled)';
          var snippet = doc.createElement('span');
          snippet.className = 'ns-snippet';
          snippet.textContent = r.snippet || '';
          item.appendChild(title);
          item.appendChild(snippet);
          item.addEventListener('click', function () { activate(r); });
          item.addEventListener('mousemove', function () {
            if (active !== idx) { active = idx; render(); }
          });
          zone.appendChild(item);
        });
      });
    }

    function activate(result) {
      if (!result) return;
      close();
      onAction(result);
    }

    function runSearch() {
      if (!store) { setState('Search is not wired in this surface yet.'); return; }
      var parsed = parseQuery(input.value);
      if (!parsed.ok) {
        results = []; active = -1; render();
        setState(parsed.reason === 'too_long' ? 'That search is too long.' : '');
        return;
      }
      setState('Searching…');
      store.search(parsed.query).then(function (out) {
        if (out && out.not_verified) {
          results = []; active = -1; render();
          setState('Sign in to search your world. Nothing is searched — or shown — without your session.');
          return;
        }
        results = (out && out.results) || [];
        active = results.length ? 0 : -1;
        render();
        setState(results.length ? '' : 'No matches in your world for “' + parsed.query + '”.');
      });
    }

    input.addEventListener('input', function () {
      if (debounce) clearTimeout(debounce);
      debounce = setTimeout(runSearch, 120);
    });
    input.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowDown') { e.preventDefault(); active = moveActive(active, 1, results.length); render(); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); active = moveActive(active, -1, results.length); render(); }
      else if (e.key === 'Enter') { e.preventDefault(); if (active >= 0 && results[active]) activate(results[active]); }
      else if (e.key === 'Escape') { e.preventDefault(); close(); }
    });
    overlay.addEventListener('click', function (e) { if (e.target === overlay) close(); });

    micBtn.addEventListener('click', function () {
      dictation.start(function (transcript) {
        var intent = parseVoiceIntent(transcript);
        if (intent.query) {
          input.value = intent.query;
          runSearch();
        } else {
          setState('I heard you — say what to find, like “find Maria”.');
        }
      }, function (state) {
        micBtn.classList.toggle('listening', state === 'listening');
        micBtn.textContent = state === 'listening' ? 'Listening…' : 'Speak';
      });
    });

    function open() {
      overlay.classList.add('open');
      setTimeout(function () { input.focus(); input.select(); }, 0);
      if (input.value.trim()) runSearch();
    }
    function close() { overlay.classList.remove('open'); }
    function isOpen() { return overlay.classList.contains('open'); }

    return { open: open, close: close, isOpen: isOpen, runSearch: runSearch };
  }

  // Cmd-K parity (feature 5): ⌘K on macOS, Ctrl-K elsewhere — one
  // handler, installed on the document, removable.
  function installHotkey(doc, openFn) {
    function handler(e) {
      var key = String(e.key || '').toLowerCase();
      if (key === 'k' && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        openFn();
      }
    }
    doc.addEventListener('keydown', handler);
    return function uninstall() { doc.removeEventListener('keydown', handler); };
  }

  // ── Exports ─────────────────────────────────────────────────────────

  var api = {
    TYPES: TYPES,
    TYPE_LABELS: TYPE_LABELS,
    TYPE_ROOMS: TYPE_ROOMS,
    MAX_QUERY: MAX_QUERY,
    DEFAULT_LIMIT: DEFAULT_LIMIT,
    parseQuery: parseQuery,
    parseVoiceIntent: parseVoiceIntent,
    normalizeResult: normalizeResult,
    rankResults: rankResults,
    groupByType: groupByType,
    defaultAction: defaultAction,
    moveActive: moveActive,
    createStore: createStore,
    createDictation: createDictation,
    mountPalette: mountPalette,
    installHotkey: installHotkey,
  };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  global.NayaSearch = api;
})(typeof window !== 'undefined' ? window : globalThis);
