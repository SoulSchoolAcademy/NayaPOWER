/*
 * smart-lists.js — Smart Lists for the Hub (Best-of-Best map element #16,
 * build-order step 15; categories per element #19).
 *
 * Smart Lists are groupings of what matters: Smart Notes by topic, people,
 * projects, messages, Naya Notes. Until now two device-local worlds existed
 * — the flagship's localStorage `os.lists.<alias>` and the Hub's
 * localStorage `naya.smartlist` — and neither could see the other. This
 * module reads and writes the ONE server store (public.smart_lists +
 * public.smart_list_items, migration 20261022223000_smart_lists_v1.sql),
 * owner-scoped by RLS with no anonymous path. The flagship template sources
 * are under another lane's freeze; the flagship wires this same store in
 * its own later step.
 *
 * An item is a TYPED reference — (kind, ref) — never a copy and never a
 * foreign key. Removing an item removes only the membership; the Smart
 * Note, Naya Note, person, thread, or link it points at is untouched, by
 * construction. Naya Notes (element #15) are first-class items from day
 * one: kind 'naya_note', ref = the note's id.
 *
 * What this module provides:
 *   - validateList / validateItem / groupListsByCategory /
 *     categoriesOfLists / orderItems / movePlan: the pure logic
 *     (unit-tested in tests/smart_lists.test.mjs).
 *   - planDeviceImport(raw): converts a device-local list world (Hub
 *     `naya.smartlist` shape, or the flagship list shape) into store
 *     drafts. The importer RUN is a follow-up; this is the agreed shape.
 *   - createStore({ supabaseUrl, anonKey, getAccessToken, fetchImpl }):
 *     REST transport in the bridge's pattern. Without an authenticated
 *     session token every call refuses with { not_verified } — the Hub
 *     never fakes a save.
 *   - mountPanel(bodyEl, opts): the Lists-room surface — create and
 *     categorize lists, add typed items, reorder, remove.
 *
 * Dual runtime like naya-notes.js: browser (window.SmartLists) and Node
 * (module.exports) share this one file.
 */
(function (global) {
  'use strict';

  var DEFAULT_CATEGORY = 'General';
  var MAX_TITLE = 200;
  var MAX_CATEGORY = 80;
  var MAX_LABEL = 300;
  var MAX_REF = 512;
  var MAX_TEXT = 4000;

  // The typed-item vocabulary — mirrors the smart_list_items_kind CHECK
  // constraint in the migration. The contract test fails if they drift.
  var ITEM_KINDS = ['smart_note', 'naya_note', 'person', 'mail_thread', 'smart_link', 'text'];
  var KIND_LABELS = {
    smart_note: 'Smart Note',
    naya_note: 'Naya Note',
    person: 'Person',
    mail_thread: 'Mail thread',
    smart_link: 'Smart Link',
    text: 'Text',
  };

  // ── Pure logic ──────────────────────────────────────────────────────

  function validateList(input) {
    var title = String((input && input.title) || '').trim();
    if (!title) return { ok: false, reason: 'empty_title' };
    if (title.length > MAX_TITLE) return { ok: false, reason: 'title_too_long' };
    var category = String((input && input.category) || '').trim() || DEFAULT_CATEGORY;
    if (category.length > MAX_CATEGORY) return { ok: false, reason: 'category_too_long' };
    return { ok: true, list: { title: title, category: category } };
  }

  function validateItem(input) {
    input = input || {};
    var kind = String(input.kind || '');
    if (ITEM_KINDS.indexOf(kind) === -1) return { ok: false, reason: 'bad_kind' };
    var label = String(input.label || '').trim();
    if (label.length > MAX_LABEL) return { ok: false, reason: 'label_too_long' };
    if (kind === 'text') {
      var text = String(input.text || '').trim();
      if (!text) return { ok: false, reason: 'empty_text' };
      if (text.length > MAX_TEXT) return { ok: false, reason: 'text_too_long' };
      return {
        ok: true,
        item: { item_kind: 'text', item_ref: null, label: label || null, text: text },
      };
    }
    var ref = String(input.ref || '').trim();
    if (!ref) return { ok: false, reason: 'empty_ref' };
    if (ref.length > MAX_REF) return { ok: false, reason: 'ref_too_long' };
    return {
      ok: true,
      item: { item_kind: kind, item_ref: ref, label: label || ref, text: null },
    };
  }

  function groupListsByCategory(lists) {
    // Null-prototype map: category names are owner-chosen text and
    // validateList accepts names like '__proto__', 'constructor' or
    // 'toString'. On a plain {} those keys resolve through
    // Object.prototype — 'constructor' reads back as the inherited
    // function (truthy, no .push) and throws; '__proto__' assignment
    // silently retargets the prototype instead of creating a group.
    // Object.create(null) makes every category an own, inert key.
    var groups = Object.create(null);
    (lists || []).forEach(function (l) {
      var key = l.category || DEFAULT_CATEGORY;
      if (!groups[key]) groups[key] = [];
      groups[key].push(l);
    });
    return groups;
  }

  function categoriesOfLists(lists) {
    return Object.keys(groupListsByCategory(lists)).sort();
  }

  // Display order for items: position first, then arrival, then id —
  // deterministic even when positions tie (imports, legacy rows).
  function orderItems(items) {
    return (items || []).slice().sort(function (a, b) {
      var pa = a.position || 0, pb = b.position || 0;
      if (pa !== pb) return pa - pb;
      var ca = a.created_at || '', cb = b.created_at || '';
      if (ca !== cb) return ca < cb ? -1 : 1;
      return String(a.id || '') < String(b.id || '') ? -1 : 1;
    });
  }

  function nextPosition(items) {
    var max = -1;
    (items || []).forEach(function (it) {
      if (typeof it.position === 'number' && it.position > max) max = it.position;
    });
    return max + 1;
  }

  // A reorder is a swap with the neighbour in display order. Returns the
  // position updates to persist ([{id, position}, ...]) or [] when the
  // move is a no-op (already at the edge, unknown id).
  function movePlan(items, itemId, delta) {
    var ordered = orderItems(items);
    var idx = -1;
    ordered.forEach(function (it, i) { if (it.id === itemId) idx = i; });
    if (idx === -1) return [];
    var swap = idx + (delta < 0 ? -1 : 1);
    if (swap < 0 || swap >= ordered.length) return [];
    var a = ordered[idx], b = ordered[swap];
    var pa = a.position || 0, pb = b.position || 0;
    if (pa === pb) { pb = pa + 1; } // tied positions: separate them first
    return [
      { id: a.id, position: pb },
      { id: b.id, position: pa },
    ];
  }

  // ── Device-local import planning ────────────────────────────────────
  // The importer run itself is a follow-up (it must execute on the device
  // that holds the local data). This planner fixes the import SHAPE:
  //   { lists: [{ title, category, items: [{kind, ref, label, text,
  //     provenance}] }], notes: [string] }
  // `provenance` is plan-level only; the store does not persist it.

  function planDeviceImport(raw) {
    var notes = [];
    if (!raw || typeof raw !== 'object') {
      return { lists: [], notes: ['unrecognized: not an object'] };
    }
    // Hub shape: { saved: [{ id, kind, title, savedAt }] } — one implicit
    // saved-boards list. Its entries reference boards, which are not one
    // of the store's typed kinds; they import as text items carrying the
    // title, with the board reference kept in provenance.
    if (Array.isArray(raw.saved)) {
      var items = raw.saved.map(function (e) {
        return {
          kind: 'text', ref: null,
          label: String(e.title || e.id || 'Saved item'),
          text: String(e.title || e.id || 'Saved item'),
          provenance: 'hub naya.smartlist saved: id=' + String(e.id || '') +
            ' kind=' + String(e.kind || '') +
            (e.savedAt ? ' savedAt=' + String(e.savedAt) : ''),
        };
      });
      notes.push('hub: ' + items.length + ' saved entr' + (items.length === 1 ? 'y' : 'ies') +
        ' planned as text items; board references preserved in provenance only.');
      return {
        lists: [{ title: 'Saved on this device', category: 'Imported', items: items }],
        notes: notes,
      };
    }
    // Flagship shape (map Part 2: real CRUD lists of plain-text items):
    // accept [{ name|title, items: [string | {text|label}] }] under a
    // `lists` key, a bare array of the same, or a { name: [items] } map.
    var srcLists = null;
    if (Array.isArray(raw.lists)) srcLists = raw.lists;
    else if (Array.isArray(raw)) srcLists = raw;
    else {
      var keys = Object.keys(raw).filter(function (k) { return Array.isArray(raw[k]); });
      if (keys.length) {
        srcLists = keys.map(function (k) { return { title: k, items: raw[k] }; });
      }
    }
    if (!srcLists) return { lists: [], notes: ['unrecognized: no saved/lists shape found'] };
    var lists = srcLists.map(function (l) {
      var its = (l.items || []).map(function (it) {
        var text = typeof it === 'string' ? it : String((it && (it.text || it.label)) || '');
        return { kind: 'text', ref: null, label: text || null, text: text, provenance: 'flagship os.lists' };
      }).filter(function (it) { return it.text; });
      return {
        title: String(l.title || l.name || 'Imported list'),
        category: String(l.category || 'Imported'),
        items: its,
      };
    });
    notes.push('flagship: ' + lists.length + ' list(s) planned as text items; ' +
      'the exact on-device shape is re-verified against the flagship sources when that lane unfreezes.');
    return { lists: lists, notes: notes };
  }

  // ── Store (transport injected; session required) ────────────────────

  function createStore(opts) {
    opts = opts || {};
    var fetchImpl = opts.fetchImpl || (typeof fetch !== 'undefined' ? fetch : null);
    var root = String(opts.supabaseUrl || '').replace(/\/$/, '') + '/rest/v1';
    var listsUrl = root + '/smart_lists';
    var itemsUrl = root + '/smart_list_items';

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

    function call(url, init, token) {
      return fetchImpl(url, init).then(function (res) {
        if (!res.ok) return { not_verified: true, reason: 'http_' + res.status };
        return res;
      });
    }

    return {
      // Every method refuses — visibly — without a session. A change
      // that was not saved is never reported as saved.
      lists: function () {
        var token = sessionToken();
        if (!token) return Promise.resolve(notVerified());
        return call(listsUrl + '?select=*&order=position.asc,created_at.asc',
          { headers: headers(token) }, token)
          .then(function (res) { return res.json ? res.json() : res; });
      },
      addList: function (input) {
        var v = validateList(input);
        if (!v.ok) return Promise.resolve({ invalid: true, reason: v.reason });
        var token = sessionToken();
        if (!token) return Promise.resolve(notVerified());
        var row = {
          owner_alias: opts.ownerAlias,
          owner_id: opts.ownerId || null,
          title: v.list.title,
          category: v.list.category,
          position: (input && typeof input.position === 'number') ? input.position : 0,
        };
        return call(listsUrl, {
          method: 'POST',
          headers: Object.assign(headers(token), { Prefer: 'return=representation' }),
          body: JSON.stringify(row),
        }, token).then(function (res) {
          if (!res.json) return res;
          return res.json().then(function (rows) { return { saved: true, list: rows[0] }; });
        });
      },
      updateList: function (id, patch) {
        patch = patch || {};
        var clean = {};
        if (patch.title !== undefined) {
          var v = validateList({ title: patch.title, category: patch.category });
          if (!v.ok) return Promise.resolve({ invalid: true, reason: v.reason });
          clean.title = v.list.title;
          if (patch.category !== undefined) clean.category = v.list.category;
        } else if (patch.category !== undefined) {
          var cat = String(patch.category).trim() || DEFAULT_CATEGORY;
          if (cat.length > MAX_CATEGORY) return Promise.resolve({ invalid: true, reason: 'category_too_long' });
          clean.category = cat;
        }
        if (typeof patch.position === 'number') clean.position = patch.position;
        if (!Object.keys(clean).length) return Promise.resolve({ invalid: true, reason: 'empty_patch' });
        var token = sessionToken();
        if (!token) return Promise.resolve(notVerified());
        clean.updated_at = new Date().toISOString();
        return call(listsUrl + '?id=eq.' + encodeURIComponent(id), {
          method: 'PATCH',
          headers: Object.assign(headers(token), { Prefer: 'return=representation' }),
          body: JSON.stringify(clean),
        }, token).then(function (res) {
          if (!res.json) return res;
          return res.json().then(function (rows) { return { updated: true, list: rows[0] }; });
        });
      },
      // Deleting a list deletes its membership rows with it (FK cascade).
      // It can never delete a referenced object — items hold no FK to them.
      removeList: function (id) {
        var token = sessionToken();
        if (!token) return Promise.resolve(notVerified());
        return call(listsUrl + '?id=eq.' + encodeURIComponent(id), {
          method: 'DELETE', headers: headers(token),
        }, token).then(function (res) {
          return res.not_verified ? res : { removed: true };
        });
      },
      items: function (listId) {
        var token = sessionToken();
        if (!token) return Promise.resolve(notVerified());
        return call(itemsUrl + '?select=*&list_id=eq.' + encodeURIComponent(listId) +
          '&order=position.asc,created_at.asc', { headers: headers(token) }, token)
          .then(function (res) { return res.json ? res.json() : res; });
      },
      addItem: function (listId, input) {
        var v = validateItem(input);
        if (!v.ok) return Promise.resolve({ invalid: true, reason: v.reason });
        var token = sessionToken();
        if (!token) return Promise.resolve(notVerified());
        var row = {
          list_id: listId,
          owner_alias: opts.ownerAlias,
          owner_id: opts.ownerId || null,
          item_kind: v.item.item_kind,
          item_ref: v.item.item_ref,
          label: v.item.label,
          text: v.item.text,
          position: (input && typeof input.position === 'number') ? input.position : 0,
        };
        return call(itemsUrl, {
          method: 'POST',
          headers: Object.assign(headers(token), { Prefer: 'return=representation' }),
          body: JSON.stringify(row),
        }, token).then(function (res) {
          if (!res.json) return res;
          return res.json().then(function (rows) { return { saved: true, item: rows[0] }; });
        });
      },
      moveItem: function (id, position) {
        var token = sessionToken();
        if (!token) return Promise.resolve(notVerified());
        return call(itemsUrl + '?id=eq.' + encodeURIComponent(id), {
          method: 'PATCH',
          headers: Object.assign(headers(token), { Prefer: 'return=representation' }),
          body: JSON.stringify({ position: position }),
        }, token).then(function (res) {
          if (!res.json) return res;
          return res.json().then(function (rows) { return { updated: true, item: rows[0] }; });
        });
      },
      // Removes ONLY the membership row (DELETE on smart_list_items).
      // The referenced object is never called, never deleted.
      removeItem: function (id) {
        var token = sessionToken();
        if (!token) return Promise.resolve(notVerified());
        return call(itemsUrl + '?id=eq.' + encodeURIComponent(id), {
          method: 'DELETE', headers: headers(token),
        }, token).then(function (res) {
          return res.not_verified ? res : { removed: true };
        });
      },
    };
  }

  // ── The Lists-room panel ────────────────────────────────────────────

  function mountPanel(bodyEl, opts) {
    opts = opts || {};
    var doc = bodyEl.ownerDocument;
    var store = opts.store;

    var style = doc.createElement('style');
    style.textContent =
      '.sl-wrap{display:grid;gap:10px}' +
      '.sl-row{display:flex;gap:8px;flex-wrap:wrap;align-items:flex-start}' +
      '.sl-input{background:rgba(255,255,255,.04);border:1px solid rgba(157,117,255,.35);' +
      'border-radius:10px;color:inherit;padding:8px 10px;font:inherit;font-size:13px}' +
      '.sl-btn{background:linear-gradient(135deg,#9d75ff,#00c8ff);color:#0b0b14;border:0;' +
      'border-radius:10px;padding:9px 14px;font:inherit;font-size:13px;font-weight:700;cursor:pointer}' +
      '.sl-btn[disabled]{opacity:.45;cursor:default}' +
      '.sl-ghost{background:none;border:1px solid rgba(157,117,255,.4);color:inherit;' +
      'border-radius:8px;padding:3px 9px;font:inherit;font-size:11.5px;cursor:pointer}' +
      '.sl-state{font-size:12.5px;color:var(--ink-dim,#a7a7c9)}' +
      '.sl-cat{font-size:11.5px;color:var(--ink-dim,#a7a7c9);letter-spacing:.06em;margin-top:6px}' +
      '.sl-list{border:1px solid rgba(157,117,255,.22);border-radius:12px;padding:9px 12px;' +
      'display:flex;gap:8px;align-items:center;cursor:pointer}' +
      '.sl-list.sel{border-color:rgba(0,200,255,.7)}' +
      '.sl-list b{font-size:14px}' +
      '.sl-item{border:1px solid rgba(157,117,255,.22);border-radius:12px;padding:9px 12px;' +
      'display:flex;gap:8px;align-items:center}' +
      '.sl-kind{font-size:11px;border:1px solid rgba(157,117,255,.4);border-radius:999px;padding:2px 8px}' +
      '.sl-item span.txt{flex:1;font-size:13.5px}';
    bodyEl.appendChild(style);

    var wrap = doc.createElement('div');
    wrap.className = 'sl-wrap';
    wrap.innerHTML =
      '<div class="sl-row">' +
      '<input class="sl-input" data-sl="new-title" placeholder="New list — e.g. Launch guests">' +
      '<input class="sl-input" data-sl="new-category" placeholder="Category (General)">' +
      '<button type="button" class="sl-btn" data-sl="create">Create list</button>' +
      '</div>' +
      '<div class="sl-state" data-sl="state" role="status"></div>' +
      '<div data-sl="lists-zone"></div>' +
      '<div data-sl="items-zone"></div>';
    bodyEl.appendChild(wrap);

    var q = function (name) { return wrap.querySelector('[data-sl="' + name + '"]'); };
    var stateEl = q('state'), listsZone = q('lists-zone'), itemsZone = q('items-zone');
    var allLists = [], allItems = [], selectedId = null;

    function setState(msg) { stateEl.textContent = msg; }
    function noSession(result) { return result && result.not_verified; }

    function renderLists() {
      listsZone.innerHTML = '';
      var groups = groupListsByCategory(allLists);
      Object.keys(groups).sort().forEach(function (cat) {
        var head = doc.createElement('div');
        head.className = 'sl-cat';
        head.textContent = cat.toUpperCase();
        listsZone.appendChild(head);
        groups[cat].forEach(function (list) {
          var row = doc.createElement('div');
          row.className = 'sl-list' + (list.id === selectedId ? ' sel' : '');
          var b = doc.createElement('b');
          b.textContent = list.title;
          row.appendChild(b);
          var del = doc.createElement('button');
          del.type = 'button';
          del.className = 'sl-ghost';
          del.textContent = 'Delete list';
          del.addEventListener('click', function (ev) {
            ev.stopPropagation();
            if (!store) return;
            store.removeList(list.id).then(function (res) {
              if (noSession(res)) { setState('Not deleted — no signed-in session. Nothing was sent anywhere.'); return; }
              if (selectedId === list.id) { selectedId = null; allItems = []; }
              setState('List deleted. Its items were memberships only — everything they pointed at still exists.');
              refresh();
            });
          });
          row.appendChild(del);
          row.addEventListener('click', function () {
            selectedId = list.id;
            renderLists();
            refreshItems();
          });
          listsZone.appendChild(row);
        });
      });
    }

    function renderItems() {
      itemsZone.innerHTML = '';
      if (!selectedId) return;
      var list = allLists.filter(function (l) { return l.id === selectedId; })[0];
      var title = doc.createElement('div');
      title.className = 'sl-cat';
      title.textContent = 'IN ' + (list ? list.title.toUpperCase() : 'LIST');
      itemsZone.appendChild(title);

      var addRow = doc.createElement('div');
      addRow.className = 'sl-row';
      var kindSel = doc.createElement('select');
      kindSel.className = 'sl-input';
      kindSel.setAttribute('data-sl', 'kind');
      ITEM_KINDS.forEach(function (k) {
        var o = doc.createElement('option');
        o.value = k;
        o.textContent = KIND_LABELS[k];
        kindSel.appendChild(o);
      });
      var valueInput = doc.createElement('input');
      valueInput.className = 'sl-input';
      valueInput.setAttribute('data-sl', 'value');
      var labelInput = doc.createElement('input');
      labelInput.className = 'sl-input';
      labelInput.setAttribute('data-sl', 'label');
      labelInput.placeholder = 'Label (optional)';
      var addBtn = doc.createElement('button');
      addBtn.type = 'button';
      addBtn.className = 'sl-btn';
      addBtn.textContent = 'Add item';
      function syncPlaceholder() {
        valueInput.placeholder = kindSel.value === 'text'
          ? 'Write the item…'
          : 'Paste the ' + KIND_LABELS[kindSel.value] + ' id / reference';
      }
      kindSel.addEventListener('change', syncPlaceholder);
      syncPlaceholder();
      addBtn.addEventListener('click', function () {
        if (!store) { setState('Lists store not wired in this surface yet.'); return; }
        var kind = kindSel.value;
        var input = kind === 'text'
          ? { kind: kind, text: valueInput.value, label: labelInput.value }
          : { kind: kind, ref: valueInput.value, label: labelInput.value };
        input.position = nextPosition(allItems);
        store.addItem(selectedId, input).then(function (res) {
          if (res && res.saved) {
            valueInput.value = '';
            labelInput.value = '';
            setState('Item added.');
            refreshItems();
          } else if (res && res.invalid) {
            setState('That item is not valid yet (' + res.reason.replace(/_/g, ' ') + ').');
          } else {
            setState('Not added — no signed-in session. Nothing was sent anywhere.');
          }
        });
      });
      addRow.appendChild(kindSel);
      addRow.appendChild(valueInput);
      addRow.appendChild(labelInput);
      addRow.appendChild(addBtn);
      itemsZone.appendChild(addRow);

      orderItems(allItems).forEach(function (item) {
        var row = doc.createElement('div');
        row.className = 'sl-item';
        var chip = doc.createElement('span');
        chip.className = 'sl-kind';
        chip.textContent = KIND_LABELS[item.item_kind] || item.item_kind;
        var txt = doc.createElement('span');
        txt.className = 'txt';
        txt.textContent = item.item_kind === 'text' ? (item.text || '') : (item.label || item.item_ref || '');
        var up = doc.createElement('button');
        up.type = 'button'; up.className = 'sl-ghost'; up.textContent = '↑';
        up.addEventListener('click', function () { applyMove(item.id, -1); });
        var down = doc.createElement('button');
        down.type = 'button'; down.className = 'sl-ghost'; down.textContent = '↓';
        down.addEventListener('click', function () { applyMove(item.id, 1); });
        var rm = doc.createElement('button');
        rm.type = 'button'; rm.className = 'sl-ghost'; rm.textContent = 'Remove';
        rm.addEventListener('click', function () {
          if (!store) return;
          store.removeItem(item.id).then(function (res) {
            if (noSession(res)) { setState('Not removed — no signed-in session. Nothing was sent anywhere.'); return; }
            setState('Removed from the list. The ' + (KIND_LABELS[item.item_kind] || 'item') + ' itself is untouched.');
            refreshItems();
          });
        });
        row.appendChild(chip);
        row.appendChild(txt);
        row.appendChild(up);
        row.appendChild(down);
        row.appendChild(rm);
        itemsZone.appendChild(row);
      });
    }

    function applyMove(itemId, delta) {
      if (!store) return;
      var plan = movePlan(allItems, itemId, delta);
      if (!plan.length) return;
      var chain = Promise.resolve();
      plan.forEach(function (step) {
        chain = chain.then(function () { return store.moveItem(step.id, step.position); });
      });
      chain.then(function () { refreshItems(); });
    }

    function refreshItems() {
      if (!store || !selectedId) { renderItems(); return; }
      store.items(selectedId).then(function (result) {
        if (!Array.isArray(result)) { allItems = []; renderItems(); return; }
        allItems = result;
        renderItems();
      });
    }

    function refresh() {
      if (!store) { setState('Lists store not wired in this surface yet.'); return; }
      store.lists().then(function (result) {
        if (!Array.isArray(result)) {
          allLists = [];
          listsZone.innerHTML = '';
          itemsZone.innerHTML = '';
          setState('Sign in to see your Smart Lists. Creation is ready — saving waits for your session, and nothing is ever saved silently.');
          return;
        }
        allLists = result;
        setState(result.length ? '' : 'No lists yet. Create the first one above.');
        renderLists();
        if (selectedId) refreshItems();
      });
    }

    q('create').addEventListener('click', function () {
      if (!store) { setState('Lists store not wired in this surface yet.'); return; }
      store.addList({
        title: q('new-title').value,
        category: q('new-category').value,
        position: allLists.length,
      }).then(function (res) {
        if (res && res.saved) {
          q('new-title').value = '';
          q('new-category').value = '';
          selectedId = res.list.id;
          setState('List created.');
          refresh();
        } else if (res && res.invalid) {
          setState('That list is not valid yet (' + res.reason.replace(/_/g, ' ') + ').');
        } else {
          setState('Not saved — no signed-in session. Nothing was sent anywhere.');
        }
      });
    });

    refresh();
    return { refresh: refresh };
  }

  // ── Exports ─────────────────────────────────────────────────────────

  var api = {
    DEFAULT_CATEGORY: DEFAULT_CATEGORY,
    MAX_TITLE: MAX_TITLE,
    MAX_CATEGORY: MAX_CATEGORY,
    MAX_LABEL: MAX_LABEL,
    MAX_REF: MAX_REF,
    MAX_TEXT: MAX_TEXT,
    ITEM_KINDS: ITEM_KINDS,
    KIND_LABELS: KIND_LABELS,
    validateList: validateList,
    validateItem: validateItem,
    groupListsByCategory: groupListsByCategory,
    categoriesOfLists: categoriesOfLists,
    orderItems: orderItems,
    nextPosition: nextPosition,
    movePlan: movePlan,
    planDeviceImport: planDeviceImport,
    createStore: createStore,
    mountPanel: mountPanel,
  };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  global.SmartLists = api;
})(typeof window !== 'undefined' ? window : globalThis);
