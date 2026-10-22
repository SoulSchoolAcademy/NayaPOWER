/* js/mission-room.js — MISSION: THE LIVING LIST room.
   The program's visual home (Shawn's order 2026-10-22 22:21Z; registry
   amendment 22:24Z; claim-aging + activation mechanisms 22:32Z).

   DATA PATH (the Reports-room pattern, with its honesty defect removed):
   at open, the room fetches the registry's published projection
   (WORK-ITEMS.json) and STATE-CORE.json from the live/mission-state
   branch — the single-writer state-core publish on its 10-minute tick.
   There is NO baked fallback in this file: if the live read fails, the
   room says so loudly and shows nothing rather than something stale or
   invented. Stale state LOOKS stale (banner past 25 minutes).

   Registry laws rendered here, enforced at publish by the builder:
   states are exactly QUEUED · CLAIMED · IN PROGRESS · VERIFYING ·
   DONE+PROVEN · BLOCKED · NEEDS SHAWN; DONE+PROVEN requires a proof
   link that resolves; BLOCKED names blocker + blocker-owner; claim
   aging is visible and idle claims carry a STALLED marker; drift
   (registry vs GitHub reality) is flagged on its row. */
(function () {
  'use strict';

  var CORE_URL = 'https://raw.githubusercontent.com/SoulSchoolAcademy/NayaPOWER/refs/heads/live/mission-state/STATE-CORE.json';
  var ITEMS_URL = 'https://raw.githubusercontent.com/SoulSchoolAcademy/NayaPOWER/refs/heads/live/mission-state/WORK-ITEMS.json';
  var BOARD_URL = 'https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2793';
  var LIST_URL = 'https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2953';
  var STALE_AFTER_S = 25 * 60;

  var SECTION_ORDER = ['IN PROGRESS', 'CLAIMED', 'VERIFYING', 'BLOCKED', 'NEEDS SHAWN', 'QUEUED', 'DONE+PROVEN'];
  var SECTION_TITLES = {
    'IN PROGRESS': 'In Motion Right Now',
    'CLAIMED': 'Claimed',
    'VERIFYING': 'Verifying — built, being checked',
    'BLOCKED': 'Blocked — Named Plainly',
    'NEEDS SHAWN': "Needs Your Hands, Shawn",
    'QUEUED': 'Queued, In Order',
    'DONE+PROVEN': 'Done + Proven'
  };

  function h(doc, tag, cls, text) {
    var el = doc.createElement(tag);
    if (cls) el.setAttribute('class', cls);
    if (text != null) el.textContent = text;
    return el;
  }
  function link(doc, href, text, cls) {
    var a = h(doc, 'a', cls, text);
    a.setAttribute('href', href);
    a.setAttribute('target', '_blank');
    a.setAttribute('rel', 'noopener');
    return a;
  }
  function fmtDur(s) {
    if (s == null) return '';
    if (s < 3600) return Math.max(1, Math.round(s / 60)) + 'm';
    if (s < 86400) return (s / 3600).toFixed(1).replace(/\.0$/, '') + 'h';
    return (s / 86400).toFixed(1).replace(/\.0$/, '') + 'd';
  }
  function injectCss(doc) {
    if (doc.getElementById('mission-room-css')) return;
    var css = [
      '.mission-wrap{max-width:1060px;margin:0 auto;padding:8px 4px 40px;color:var(--ink,#eef)}',
      '.mission-fresh{font-size:13px;opacity:.85;margin:6px 0 14px}',
      '.mission-stale{background:#5a1616;border:1px solid #ff6b6b;color:#ffd7d7;border-radius:12px;padding:12px 16px;font-weight:600;margin:10px 0}',
      '.mission-error{background:#5a1616;border:1px solid #ff6b6b;color:#ffd7d7;border-radius:12px;padding:18px;margin:14px 0}',
      '.mission-counts{display:flex;flex-wrap:wrap;gap:10px;margin:12px 0 20px}',
      '.mission-count{border:1px solid rgba(255,255,255,.16);border-radius:14px;padding:10px 16px;min-width:104px;background:rgba(255,255,255,.04)}',
      '.mission-count b{font-size:26px;display:block;line-height:1.05}',
      '.mission-count span{font-size:12px;letter-spacing:.06em;text-transform:uppercase;opacity:.8}',
      '.mission-count.warn{border-color:#ffb020;color:#ffd98a}',
      '.mission-sec{margin:26px 0 6px;font-size:19px}',
      '.mission-item{border:1px solid rgba(255,255,255,.12);border-radius:14px;padding:12px 16px;margin:8px 0;background:rgba(255,255,255,.03)}',
      '.mission-item .rank{font-weight:700;opacity:.65;margin-right:8px}',
      '.mission-item .ttl{font-weight:650;font-size:15.5px}',
      '.mission-chip{display:inline-block;font-size:11px;letter-spacing:.05em;border:1px solid rgba(255,255,255,.25);border-radius:999px;padding:1px 8px;margin-left:8px;vertical-align:2px}',
      '.mission-chip.stalled{border-color:#ff6b6b;color:#ff9c9c;font-weight:700}',
      '.mission-meta{font-size:13px;opacity:.85;margin-top:4px}',
      '.mission-note{font-size:13.5px;margin-top:6px;opacity:.92}',
      '.mission-drift{color:#ffb0b0;font-size:13px;margin-top:5px;font-weight:600}',
      '.mission-blocker{color:#ffd98a;font-size:13.5px;margin-top:5px}',
      '.mission-filters{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0}',
      '.mission-fbtn{cursor:pointer;border:1px solid rgba(255,255,255,.22);background:transparent;color:inherit;border-radius:999px;padding:3px 12px;font-size:12.5px}',
      '.mission-fbtn.on{background:rgba(255,255,255,.16)}',
      '.mission-ev{font-size:13.5px;padding:6px 0;border-bottom:1px solid rgba(255,255,255,.07)}',
      '.mission-panel{border:1px dashed rgba(255,255,255,.25);border-radius:14px;padding:14px 16px;margin:22px 0;font-size:14px}'
    ].join('\n');
    var st = doc.createElement('style');
    st.setAttribute('id', 'mission-room-css');
    st.textContent = css;
    (doc.head || doc.documentElement).appendChild(st);
  }

  function renderInto(doc, root, items, core) {
    injectCss(doc);
    root.textContent = '';
    var wrap = h(doc, 'div', 'mission-wrap');
    root.appendChild(wrap);

    var nowS = Math.floor(Date.now() / 1000);
    var genS = items && items.generated_utc ? Math.floor(Date.parse(items.generated_utc) / 1000) : null;
    var ageS = genS ? nowS - genS : null;

    var fresh = h(doc, 'div', 'mission-fresh');
    if (genS) {
      fresh.textContent = 'State compiled ' + items.generated_utc + ' (' + fmtDur(ageS) + ' ago) · source: the Living List registry, published by the single-writer state-core tick (every 10 minutes) · tip ' +
        (core && core.tip ? core.tip.short : '—');
    } else {
      fresh.textContent = 'State compilation time unknown — treat with caution.';
    }
    wrap.appendChild(fresh);
    if (ageS != null && ageS > STALE_AFTER_S) {
      wrap.appendChild(h(doc, 'div', 'mission-stale',
        '⚠ THIS STATE IS STALE — last compiled ' + fmtDur(ageS) + ' ago. The tick may be down; do not work from this page until it refreshes.'));
    }

    var c = (items && items.counts) || {};
    var counts = h(doc, 'div', 'mission-counts');
    function countBox(n, label, warn) {
      var b = h(doc, 'div', 'mission-count' + (warn ? ' warn' : ''));
      b.appendChild(h(doc, 'b', '', String(n == null ? 0 : n)));
      b.appendChild(h(doc, 'span', '', label));
      counts.appendChild(b);
    }
    countBox(c['DONE+PROVEN'], 'Done + proven');
    countBox((c['IN PROGRESS'] || 0) + (c['CLAIMED'] || 0), 'In motion');
    countBox(c['VERIFYING'], 'Verifying');
    countBox(c['BLOCKED'], 'Blocked');
    countBox(c['QUEUED'], 'Queued');
    countBox(c['NEEDS SHAWN'], "Needs Shawn's hands");
    if (items.stalled_claims) countBox(items.stalled_claims, '⚠ Stalled claims', true);
    if (items.drift_flags) countBox(items.drift_flags, '⚠ Drift flags', true);
    wrap.appendChild(counts);

    var list = (items.items || []).slice().sort(function (a, b) { return (a.rank || 9999) - (b.rank || 9999); });

    // THE QUEUE IN ORDER — the ranked top of the one queue, before the
    // state sections. Activation reads from here: own claims, then the top.
    var open = list.filter(function (it) { return it.state !== 'DONE+PROVEN'; });
    if (open.length) {
      wrap.appendChild(h(doc, 'h3', 'mission-sec', 'Up Next — The Queue In Order'));
      open.slice(0, 8).forEach(function (it) {
        var line = h(doc, 'div', 'mission-ev');
        line.appendChild(h(doc, 'span', '', '#' + it.rank + ' — ' + it.title + ' · ' + it.state + (it.owner ? ' · ' + it.owner : '') + (it.stalled ? ' · ⚠ STALLED' : '')));
        wrap.appendChild(line);
      });
    }

    // Program filter — programs are views over ONE queue, never separate queues.
    var programs = [];
    list.forEach(function (it) { if (it.program && programs.indexOf(it.program) < 0) programs.push(it.program); });
    var filters = h(doc, 'div', 'mission-filters');
    var bodyBox = h(doc, 'div', '');
    var current = 'ALL';
    function draw() {
      bodyBox.textContent = '';
      SECTION_ORDER.forEach(function (state) {
        var rows = list.filter(function (it) { return it.state === state && (current === 'ALL' || it.program === current); });
        if (!rows.length) return;
        bodyBox.appendChild(h(doc, 'h3', 'mission-sec', SECTION_TITLES[state] + ' (' + rows.length + ')'));
        rows.forEach(function (it) { bodyBox.appendChild(itemEl(doc, it)); });
      });
      if (!bodyBox.childNodes.length) bodyBox.appendChild(h(doc, 'p', '', 'Nothing in this view.'));
    }
    function fbtn(label, val) {
      var b = h(doc, 'button', 'mission-fbtn' + (val === 'ALL' ? ' on' : ''), label);
      b.setAttribute('type', 'button');
      if (b.addEventListener) b.addEventListener('click', function () {
        current = val;
        var kids = filters.childNodes;
        for (var i = 0; i < kids.length; i++) kids[i].setAttribute('class', 'mission-fbtn');
        b.setAttribute('class', 'mission-fbtn on');
        draw();
      });
      return b;
    }
    filters.appendChild(fbtn('All programs', 'ALL'));
    programs.forEach(function (p) { filters.appendChild(fbtn(p, p)); });
    wrap.appendChild(filters);
    wrap.appendChild(bodyBox);
    draw();

    // Completions + activity stream (registry events; ledger state stated honestly).
    wrap.appendChild(h(doc, 'h3', 'mission-sec', 'Just Completed + Activity'));
    var evs = items.events || [];
    if (!evs.length) wrap.appendChild(h(doc, 'p', '', 'No state changes recorded yet.'));
    evs.forEach(function (ev) {
      var line = h(doc, 'div', 'mission-ev');
      var txt = (ev.at || '') + ' — ' + ev.id + ' ' + (ev.from ? (ev.from + ' → ') : 'entered at ') + ev.to + ' · ' + ev.title;
      line.appendChild(h(doc, 'span', '', txt));
      if (ev.ledger) line.appendChild(h(doc, 'div', 'mission-meta', 'Smart Ledger: ' + ev.ledger));
      wrap.appendChild(line);
    });
    var src = h(doc, 'p', 'mission-meta',
      'Completions source: the Living List registry event stream (state-core tick diff). ' + (items.ledger_note || ''));
    wrap.appendChild(src);

    // Add / note path — the write venues stay the board + THE LIST.
    var panel = h(doc, 'div', 'mission-panel');
    panel.appendChild(h(doc, 'strong', '', 'Add an item or a note: '));
    panel.appendChild(h(doc, 'span', '', 'this page is the read surface. Items and notes enter on '));
    panel.appendChild(link(doc, BOARD_URL, 'the board (#2793)'));
    panel.appendChild(h(doc, 'span', '', ' or '));
    panel.appendChild(link(doc, LIST_URL, 'THE LIST (#2953)'));
    panel.appendChild(h(doc, 'span', '', ' — the registry is triaged from there and reflects here within one 10-minute tick. Activation contract: read your own claimed rows first, then claim from the top of the queue.'));
    wrap.appendChild(panel);
    return wrap;
  }

  function itemEl(doc, it) {
    var box = h(doc, 'div', 'mission-item');
    var head = h(doc, 'div', '');
    head.appendChild(h(doc, 'span', 'rank', '#' + it.rank));
    head.appendChild(h(doc, 'span', 'ttl', it.title));
    var chip = h(doc, 'span', 'mission-chip', it.state);
    head.appendChild(chip);
    if (it.stalled) head.appendChild(h(doc, 'span', 'mission-chip stalled', '⚠ STALLED CLAIM'));
    box.appendChild(head);
    var meta = [];
    if (it.program) meta.push(it.program);
    if (it.owner) meta.push('owner: ' + it.owner);
    if (it.claim_age_s != null) meta.push('claimed ' + fmtDur(it.claim_age_s) + ' ago');
    if (it.idle_s != null && (it.state === 'CLAIMED' || it.state === 'IN PROGRESS')) meta.push('last moved ' + fmtDur(it.idle_s) + ' ago');
    if (meta.length) box.appendChild(h(doc, 'div', 'mission-meta', meta.join(' · ')));
    if (it.state === 'BLOCKED' && it.blocker) {
      box.appendChild(h(doc, 'div', 'mission-blocker', '⛔ ' + it.blocker + (it.blocker_owner ? ' — blocker owner: ' + it.blocker_owner : '')));
    }
    if (it.note) box.appendChild(h(doc, 'div', 'mission-note', it.note));
    if (it.state === 'DONE+PROVEN' && it.proof) {
      var p = h(doc, 'div', 'mission-meta');
      p.appendChild(h(doc, 'span', '', 'Proof: '));
      p.appendChild(link(doc, it.proof, it.proof.replace('https://github.com/SoulSchoolAcademy/NayaPOWER/', '')));
      if (it.proof_check) p.appendChild(h(doc, 'span', '', ' · proof link ' + it.proof_check));
      if (it.verified_by) p.appendChild(h(doc, 'span', '', ' · verified by ' + it.verified_by));
      box.appendChild(p);
    }
    (it.drift || []).forEach(function (d) {
      box.appendChild(h(doc, 'div', 'mission-drift', '⚠ drift: ' + d));
    });
    return box;
  }

  function renderError(doc, root, err) {
    injectCss(doc);
    root.textContent = '';
    var box = h(doc, 'div', 'mission-error');
    box.appendChild(h(doc, 'strong', '', 'THE LIVING LIST COULD NOT BE LOADED. '));
    box.appendChild(h(doc, 'span', '', 'The live registry read failed (' + (err && err.message ? err.message : err) + '). Nothing is shown rather than something stale or invented — this room has no baked fallback. '));
    box.appendChild(link(doc, BOARD_URL, 'Open the board (#2793)'));
    box.appendChild(h(doc, 'span', '', ' · '));
    box.appendChild(link(doc, LIST_URL, 'Open THE LIST (#2953)'));
    root.appendChild(box);
    return box;
  }

  function load(doc, root, fetchFn) {
    root.textContent = '';
    root.appendChild(h(doc, 'p', 'mission-fresh', 'Loading the Living List — live read at open…'));
    var bust = '?t=' + Math.floor(Date.now() / 60000);
    return Promise.all([
      fetchFn(ITEMS_URL + bust, { cache: 'no-store' }).then(function (r) { if (!r.ok) throw new Error('WORK-ITEMS HTTP ' + r.status); return r.json(); }),
      fetchFn(CORE_URL + bust, { cache: 'no-store' }).then(function (r) { if (!r.ok) throw new Error('STATE-CORE HTTP ' + r.status); return r.json(); })
    ]).then(function (res) {
      if (!res[0] || !Array.isArray(res[0].items)) throw new Error('registry payload malformed');
      return renderInto(doc, root, res[0], res[1]);
    }).catch(function (err) { return renderError(doc, root, err); });
  }

  var api = { renderInto: renderInto, renderError: renderError, load: load, fmtDur: fmtDur };

  if (typeof window !== 'undefined') {
    window.NayaMissionRoom = api;
    window.NayaRooms = window.NayaRooms || {};
    window.NayaRooms.mission = function () {
      var root = document.createElement('div');
      load(document, root, function (u, o) { return window.fetch(u, o); });
      return root;
    };
    // Standalone preview support: a page carrying #mission-root renders there.
    if (typeof document !== 'undefined' && document.getElementById && document.getElementById('mission-root')) {
      load(document, document.getElementById('mission-root'), function (u, o) { return window.fetch(u, o); });
    }
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
})();
