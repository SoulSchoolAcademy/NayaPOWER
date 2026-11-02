/*
 * naya-notes.js — Naya Notes for the Hub (Best-of-Best map element #15, Hub half).
 *
 * Naya Notes are NOT Smart Notes. Smart Notes are intelligence objects with
 * layers, fed to the brain. Naya Notes are a person's own quick captures —
 * private, plain, and never sent to the brain or any wall. The store is
 * public.naya_notes (migration 20261022204500_naya_notes_v1.sql), RLS
 * owner-only: there is no anonymous path to these rows, by design.
 *
 * What this module provides:
 *   - validateNote / groupByCategory / categoriesOf / copyTextFor:
 *     the pure logic (unit-tested in tests/naya_notes.test.mjs).
 *   - createStore({ supabaseUrl, anonKey, getAccessToken, fetchImpl }):
 *     REST transport in the bridge's pattern. Without an authenticated
 *     session token every call refuses with { not_verified } — the Hub
 *     never fakes a save. The Hub wires the session through
 *     window.NayaNotesSession (a function returning the user's JWT or
 *     null) when the auth lane provides one; the flagship app — which has
 *     real auth — is the fully live home (map step 16).
 *   - mountPanel(bodyEl, opts): the Lists-room surface — capture with
 *     dictation from day one (Web Speech API where present, honestly
 *     absent where not), category + list fields, the notes list grouped
 *     by category with per-note Copy, and a category filter.
 *
 * Dual runtime like supabase-bridge.js: browser (window.NayaNotes) and
 * Node (module.exports) share this one file.
 */
(function (global) {
  'use strict';

  var DEFAULT_CATEGORY = 'General';
  var MAX_TEXT = 4000;

  // ── Pure logic ──────────────────────────────────────────────────────

  function validateNote(input) {
    var text = String((input && input.text) || '').trim();
    if (!text) return { ok: false, reason: 'empty' };
    if (text.length > MAX_TEXT) return { ok: false, reason: 'too_long' };
    var category = String((input && input.category) || '').trim() || DEFAULT_CATEGORY;
    var list = String((input && input.list) || '').trim();
    return {
      ok: true,
      note: {
        text: text,
        category: category,
        list_name: list || null,
      },
    };
  }

  function groupByCategory(notes) {
    var groups = {};
    (notes || []).forEach(function (n) {
      var key = n.category || DEFAULT_CATEGORY;
      if (!groups[key]) groups[key] = [];
      groups[key].push(n);
    });
    return groups;
  }

  function categoriesOf(notes) {
    return Object.keys(groupByCategory(notes)).sort();
  }

  // The copy contract (element #15): the note's text, and when it carries
  // a list, the list rides along so a paste lands with its context.
  function copyTextFor(note) {
    if (!note) return '';
    var text = String(note.text || '');
    if (note.list_name) return text + '\n— List: ' + note.list_name;
    return text;
  }

  // ── Store (transport injected; session required) ────────────────────

  function createStore(opts) {
    opts = opts || {};
    var fetchImpl = opts.fetchImpl || (typeof fetch !== 'undefined' ? fetch : null);
    var base = String(opts.supabaseUrl || '').replace(/\/$/, '') + '/rest/v1/naya_notes';

    function sessionToken() {
      try {
        return typeof opts.getAccessToken === 'function' ? opts.getAccessToken() : null;
      } catch (e) {
        return null;
      }
    }

    function headers(token) {
      return {
        apikey: opts.anonKey,
        Authorization: 'Bearer ' + token,
        'Content-Type': 'application/json',
      };
    }

    function notVerified() {
      return { not_verified: true, reason: 'no_session' };
    }

    return {
      // Every method refuses — visibly — without a session. A capture that
      // was not saved is never reported as saved.
      list: function () {
        var token = sessionToken();
        if (!token) return Promise.resolve(notVerified());
        return fetchImpl(base + '?select=*&order=created_at.desc', {
          headers: headers(token),
        }).then(function (res) {
          if (!res.ok) return { not_verified: true, reason: 'http_' + res.status };
          return res.json();
        });
      },
      add: function (input) {
        var v = validateNote(input);
        if (!v.ok) return Promise.resolve({ invalid: true, reason: v.reason });
        var token = sessionToken();
        if (!token) return Promise.resolve(notVerified());
        var row = {
          owner_alias: opts.ownerAlias,
          owner_id: opts.ownerId || null,
          text: v.note.text,
          category: v.note.category,
          list_name: v.note.list_name,
        };
        return fetchImpl(base, {
          method: 'POST',
          headers: Object.assign(headers(token), { Prefer: 'return=representation' }),
          body: JSON.stringify(row),
        }).then(function (res) {
          if (!res.ok) return { not_verified: true, reason: 'http_' + res.status };
          return res.json().then(function (rows) { return { saved: true, note: rows[0] }; });
        });
      },
    };
  }

  // ── Dictation ───────────────────────────────────────────────────────
  // SpeechRecognition is injected so tests (and non-supporting browsers)
  // exercise the same code path. Support is detected, never assumed.

  function createDictation(opts) {
    opts = opts || {};
    var Ctor = opts.recognitionCtor !== undefined
      ? opts.recognitionCtor
      : (global.SpeechRecognition || global.webkitSpeechRecognition || null);
    return {
      supported: !!Ctor,
      // onText(finalText) fires per finalized phrase; onState('listening'|'idle')
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

  // ── The Lists-room panel ────────────────────────────────────────────

  function mountPanel(bodyEl, opts) {
    opts = opts || {};
    var doc = bodyEl.ownerDocument;
    var store = opts.store;
    var dictation = opts.dictation || createDictation();

    var style = doc.createElement('style');
    style.textContent =
      '.nn-wrap{display:grid;gap:10px}' +
      '.nn-row{display:flex;gap:8px;flex-wrap:wrap;align-items:flex-start}' +
      '.nn-text{flex:1 1 260px;min-height:64px;background:rgba(255,255,255,.04);' +
      'border:1px solid rgba(157,117,255,.35);border-radius:12px;color:inherit;' +
      'padding:10px 12px;font:inherit;font-size:14px}' +
      '.nn-input{background:rgba(255,255,255,.04);border:1px solid rgba(157,117,255,.35);' +
      'border-radius:10px;color:inherit;padding:8px 10px;font:inherit;font-size:13px}' +
      '.nn-btn{background:linear-gradient(135deg,#9d75ff,#00c8ff);color:#0b0b14;border:0;' +
      'border-radius:10px;padding:9px 14px;font:inherit;font-size:13px;font-weight:700;cursor:pointer}' +
      '.nn-btn[disabled]{opacity:.45;cursor:default}' +
      '.nn-mic.listening{background:linear-gradient(135deg,#ffd75e,#ff5e8a)}' +
      '.nn-state{font-size:12.5px;color:var(--ink-dim,#a7a7c9)}' +
      '.nn-note{border:1px solid rgba(157,117,255,.22);border-radius:12px;padding:10px 12px}' +
      '.nn-note p{margin:0 0 6px;font-size:14px;line-height:1.55;white-space:pre-wrap}' +
      '.nn-meta{display:flex;gap:8px;flex-wrap:wrap;font-size:11.5px;color:var(--ink-dim,#a7a7c9)}' +
      '.nn-copy{background:none;border:1px solid rgba(157,117,255,.4);color:inherit;' +
      'border-radius:8px;padding:3px 9px;font:inherit;font-size:11.5px;cursor:pointer}';
    bodyEl.appendChild(style);

    var wrap = doc.createElement('div');
    wrap.className = 'nn-wrap';
    wrap.innerHTML =
      '<div class="nn-row">' +
      '<textarea class="nn-text" data-nn="text" placeholder="Capture a thought — it stays yours. Not a Smart Note; never the brain, never the wall."></textarea>' +
      '</div>' +
      '<div class="nn-row">' +
      '<input class="nn-input" data-nn="category" placeholder="Category (General)">' +
      '<input class="nn-input" data-nn="list" placeholder="List (optional)">' +
      '<button type="button" class="nn-btn nn-mic" data-nn="mic">Dictate</button>' +
      '<button type="button" class="nn-btn" data-nn="save">Save note</button>' +
      '<select class="nn-input" data-nn="filter"><option value="">All categories</option></select>' +
      '</div>' +
      '<div class="nn-state" data-nn="state" role="status"></div>' +
      '<div class="nn-list" data-nn="list-zone"></div>';
    bodyEl.appendChild(wrap);

    var q = function (name) { return wrap.querySelector('[data-nn="' + name + '"]'); };
    var textEl = q('text'), stateEl = q('state'), zone = q('list-zone');
    var micBtn = q('mic'), saveBtn = q('save'), filterEl = q('filter');

    if (!dictation.supported) {
      micBtn.disabled = true;
      micBtn.textContent = 'Dictation unavailable here';
    }

    function setState(msg) { stateEl.textContent = msg; }

    function render(notes) {
      var chosen = filterEl.value;
      var visible = chosen ? notes.filter(function (n) { return (n.category || DEFAULT_CATEGORY) === chosen; }) : notes;
      zone.innerHTML = '';
      var groups = groupByCategory(visible);
      Object.keys(groups).sort().forEach(function (cat) {
        var head = doc.createElement('div');
        head.className = 'nn-meta';
        head.innerHTML = '<span></span>';
        head.firstChild.textContent = cat.toUpperCase();
        zone.appendChild(head);
        groups[cat].forEach(function (note) {
          var card = doc.createElement('article');
          card.className = 'nn-note';
          var p = doc.createElement('p');
          p.textContent = note.text;
          var meta = doc.createElement('div');
          meta.className = 'nn-meta';
          var when = doc.createElement('span');
          when.textContent = note.created_at ? new Date(note.created_at).toLocaleString() : '';
          meta.appendChild(when);
          if (note.list_name) {
            var ln = doc.createElement('span');
            ln.textContent = 'List: ' + note.list_name;
            meta.appendChild(ln);
          }
          var copy = doc.createElement('button');
          copy.type = 'button';
          copy.className = 'nn-copy';
          copy.textContent = 'Copy';
          copy.addEventListener('click', function () {
            var text = copyTextFor(note);
            if (global.navigator && global.navigator.clipboard) {
              global.navigator.clipboard.writeText(text);
            }
            copy.textContent = 'Copied';
            setTimeout(function () { copy.textContent = 'Copy'; }, 1200);
          });
          meta.appendChild(copy);
          card.appendChild(p);
          card.appendChild(meta);
          zone.appendChild(card);
        });
      });
      // Refresh the filter options from what exists.
      var current = filterEl.value;
      filterEl.innerHTML = '<option value="">All categories</option>';
      categoriesOf(notes).forEach(function (cat) {
        var o = doc.createElement('option');
        o.value = cat;
        o.textContent = cat;
        filterEl.appendChild(o);
      });
      filterEl.value = current;
    }

    var allNotes = [];
    function refresh() {
      if (!store) { setState('Notes store not wired in this surface yet.'); return; }
      store.list().then(function (result) {
        if (!Array.isArray(result)) {
          allNotes = [];
          zone.innerHTML = '';
          setState('Sign in to see your Naya Notes. Capture is ready — saving waits for your session, and nothing is ever saved silently.');
          return;
        }
        allNotes = result;
        setState(result.length ? '' : 'No notes yet. Capture the first one above.');
        render(allNotes);
      });
    }

    micBtn.addEventListener('click', function () {
      dictation.start(function (phrase) {
        textEl.value = (textEl.value ? textEl.value.replace(/\s*$/, ' ') : '') + phrase;
      }, function (state) {
        micBtn.classList.toggle('listening', state === 'listening');
        micBtn.textContent = state === 'listening' ? 'Listening…' : 'Dictate';
      });
    });

    saveBtn.addEventListener('click', function () {
      if (!store) { setState('Notes store not wired in this surface yet.'); return; }
      store.add({
        text: textEl.value,
        category: q('category').value,
        list: q('list').value,
      }).then(function (result) {
        if (result && result.saved) {
          textEl.value = '';
          q('category').value = '';
          q('list').value = '';
          setState('Saved — yours alone.');
          refresh();
        } else if (result && result.invalid) {
          setState(result.reason === 'empty' ? 'Write or dictate something first.' : 'That note is too long (max ' + MAX_TEXT + ' characters).');
        } else {
          setState('Not saved — no signed-in session. Your text is still above; nothing was sent anywhere.');
        }
      });
    });

    filterEl.addEventListener('change', function () { render(allNotes); });
    refresh();
    return { refresh: refresh };
  }

  // ── Exports ─────────────────────────────────────────────────────────

  var api = {
    DEFAULT_CATEGORY: DEFAULT_CATEGORY,
    MAX_TEXT: MAX_TEXT,
    validateNote: validateNote,
    groupByCategory: groupByCategory,
    categoriesOf: categoriesOf,
    copyTextFor: copyTextFor,
    createStore: createStore,
    createDictation: createDictation,
    mountPanel: mountPanel,
  };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  global.NayaNotes = api;
})(typeof window !== 'undefined' ? window : globalThis);
