/* ═══════════════════════════════════════════════════════════════════
   HUB CHASSIS — the 509 structure. One shell, one nav model, one room
   outlet. Enhances the 509 laboratory structure per the Human Director's
   2026-10-02 ruling: fixed left rail, plus-button ecosystem menu (no pill
   bar), mobile plus-button room drawer, the feed as the main show.

   The chassis never invents intelligence. Rooms render through it.
   A room may own one lens at shell level via NayaChassis.setLens(node)
   (the Main Show's Collective/Personal/Activity lens lives here, never
   duplicated inside the room).
   ═══════════════════════════════════════════════════════════════════ */

  /* Smart Tab state lives at IIFE level so the active tab survives room re-renders. */
  var activeSmartTab = 'all';
  var tabPopCloser = null;

function HubView(params) {
  const { el, Icons, toast, StatePanel } = window.NayaUI;
  const R = window.NayaRuntime;
  const C = window.NayaContent || null;
  const activeRoom = params.room || 'feed';
  /* Feed streams ride the room param: feed (collective), feed-personal, feed-activity.
     All three resolve to the feed room; the stream selects the lens. */
  const feedStream = activeRoom === 'feed-personal' ? 'personal'
    : activeRoom === 'feed-activity' ? 'activity' : (activeRoom === 'feed' ? 'collective' : null);
  const roomId = feedStream ? 'feed' : activeRoom;
  const room = R.ROOMS.find(r => r.id === roomId) || R.ROOMS[0];

  const shell = el('div', 'shell');

  /* ——— LEFT RAIL · fixed room navigation ——— */
  const rail = el('aside', 'rail left');
  rail.setAttribute('aria-label', 'Hub rooms');
  const brand = el('div', 'brand');
  brand.innerHTML = '<img src="../icon-192.png" alt="NayaNET mark"><div><b>NAYANET</b><small>INTELLIGENT HUB</small></div>';
  const nav = el('nav', 'nav');
  nav.setAttribute('aria-label', 'Intelligence rooms');
  R.ROOMS.forEach(r => {
    const b = el('button', 'nav-btn' + (r.id === room.id ? ' active' : ''));
    b.style.setProperty('--nav', r.accent);
    b.innerHTML = '<span class="ico">' + Icons.icon(r.icon) + '</span><span class="lbl">' + esc(r.name) + '</span>';
    b.setAttribute('aria-current', r.id === room.id ? 'page' : 'false');
    b.addEventListener('click', () => { closeDrawer(); window.NayaRouter.navigate('/hub/' + r.id); });
    nav.appendChild(b);
  });
  const priv = el('div', 'private', 'PRIVATE BY DEFAULT<br>SHARED BY CHOICE<br>COLLECTIVE BY CONSENT');
  rail.append(brand, nav, priv);

  /* ——— MAIN ——— */
  const main = el('main', 'main');
  main.setAttribute('aria-label', room.name);

  /* Topbar: rooms-plus (mobile) · title · ecosystem plus menu (top-right).
     The SOURCE·VISIBLE pill is gone — the top-right corner belongs to the menu. */
  const top = el('header', 'top');
  const roomsPlus = el('button', 'rooms-plus', Icons.icon('plus'));
  roomsPlus.setAttribute('aria-label', 'Open room navigation');
  roomsPlus.setAttribute('aria-expanded', 'false');
  roomsPlus.addEventListener('click', () => (shell.classList.contains('drawer-open') ? closeDrawer() : openDrawer()));
  const title = el('div', 'top-title', '<b>INTELLIGENT HUB</b>');
  const spacer = el('div', 'top-spacer');
  spacer.setAttribute('aria-hidden', 'true');
  const pluswrap = el('div', 'pluswrap');
  const plusBtn = el('button', 'plus-btn', Icons.icon('plus'));
  plusBtn.setAttribute('aria-label', 'Ecosystem destinations');
  plusBtn.setAttribute('aria-expanded', 'false');
  plusBtn.setAttribute('aria-haspopup', 'true');
  const plusMenu = el('div', 'plusmenu');
  plusMenu.hidden = true;
  plusMenu.setAttribute('role', 'menu');
  plusMenu.innerHTML = '<div class="pm-head">DESTINATIONS</div>';
  ECOSYSTEM.forEach(([label, href]) => {
    const a = el('a', 'pluslink');
    a.href = href; a.target = '_blank'; a.rel = 'noopener'; a.setAttribute('role', 'menuitem');
    a.innerHTML = '<span>' + esc(label) + '</span><span class="ext" aria-hidden="true">↗</span>';
    plusMenu.appendChild(a);
  });
  plusBtn.addEventListener('click', e => { e.stopPropagation(); toggleMenu(); });
  pluswrap.append(plusBtn, plusMenu);
  top.append(roomsPlus, title, spacer, pluswrap);

  /* Ask Naya — chassis-level retrieval. One contextual-Naya interface. */
  const searchWrap = el('section', 'searchWrap');
  searchWrap.innerHTML =
    '<div class="searchRow" role="search">' +
    '<span class="search-ico" aria-hidden="true">' + Icons.icon('search') + '</span>' +
    '<input type="search" id="chassisSearch" placeholder="Ask the intelligence…" aria-label="Ask the intelligence" autocomplete="off">' +
    '</div><div class="searchHint">Ask Naya — retrieval across retained intelligence. Answers carry their sources.</div>';
  const searchInput = searchWrap.querySelector('input');
  searchInput.addEventListener('keydown', async e => {
    if (e.key === 'Enter' && searchInput.value.trim()) {
      searchInput.setAttribute('aria-busy', 'true');
      try {
        const res = await R.search(searchInput.value.trim(), { room: room.id });
        if (!res.ok) toast(res.message || 'No verified answer is available.', room.accent);
        else showSearchResult(res);
      } finally { searchInput.removeAttribute('aria-busy'); }
    }
  });

  /* ═══ SMART TABS — topic navigation generated from the notes themselves.
     System tabs (All + every topic present in this lens) are permanent.
     Human tabs are named views saved on this device only (localStorage):
     add, retarget (replace), or delete. Per the canonical Smart Tab law,
     tabs are navigation intent — never intelligence storage — and
     human-created tabs are visually distinguished from system tabs. ═══ */
  const SMART_TAB_KEY = 'nayanet.feed.smartTabs.v1';

  function readHumanTabs() {
    try { const t = JSON.parse(localStorage.getItem(SMART_TAB_KEY)); return Array.isArray(t) ? t : []; }
    catch (e) { return []; }
  }
  function writeHumanTabs(t) { try { localStorage.setItem(SMART_TAB_KEY, JSON.stringify(t)); } catch (e) { /* private mode — tabs stay session-only */ } }
  function topicSlug(s) { return 't-' + String(s).toLowerCase().replace(/[^a-z0-9]+/g, '-'); }
  function closeTabManager() {
    document.querySelectorAll('.tab-pop').forEach(p => p.remove());
    if (tabPopCloser) { document.removeEventListener('click', tabPopCloser); tabPopCloser = null; }
  }

  function smartTabStrip(lensNotes, allNotes) {
    const seen = [];
    lensNotes.forEach(n => (n.topics || []).forEach(t => { if (!seen.includes(t)) seen.push(t); }));
    const sysTabs = [{ id: 'all', label: 'All', topic: null, kind: 'system' }]
      .concat(seen.map(t => ({ id: topicSlug(t), label: t, topic: t, kind: 'system' })));
    const tabs = sysTabs.concat(readHumanTabs().map(h => ({ id: h.id, label: h.label, topic: h.topic, kind: 'human' })));
    if (!tabs.some(t => t.id === activeSmartTab)) activeSmartTab = 'all';

    const bar = el('div', 'smart-tabs');
    bar.setAttribute('role', 'tablist');
    bar.setAttribute('aria-label', 'Smart Tabs — filter the feed by topic');
    const rerender = () => window.NayaRouter.render();
    tabs.forEach(t => {
      const b = el('button', 'smart-tab' + (t.id === activeSmartTab ? ' active' : '') + (t.kind === 'human' ? ' is-human' : ''));
      b.setAttribute('role', 'tab');
      b.setAttribute('aria-selected', t.id === activeSmartTab ? 'true' : 'false');
      b.title = t.kind === 'human'
        ? 'Your tab · shows ' + t.topic + ' · saved on this device'
        : (t.topic ? 'Topic · ' + t.topic : 'The full feed — everything, newest first');
      b.innerHTML = '<span>' + esc(t.label) + '</span>' + (t.kind === 'human' ? '<i class="human-dot" aria-hidden="true"></i>' : '');
      b.addEventListener('click', () => { closeTabManager(); activeSmartTab = t.id; rerender(); });
      bar.appendChild(b);
    });
    const add = el('button', 'smart-tab add-tab');
    add.setAttribute('aria-label', 'Add, retarget, or delete your tabs');
    add.title = 'Add, retarget, or delete your tabs';
    add.innerHTML = '<span aria-hidden="true">+</span>';
    add.addEventListener('click', (ev) => { ev.stopPropagation(); openTabManager(bar, add, sysTabs, allNotes, rerender); });
    bar.appendChild(add);
    return { bar, tabs };
  }

  function openTabManager(bar, addBtn, sysTabs, allNotes, rerender) {
    closeTabManager();
    const human = readHumanTabs();
    const allTopics = [];
    allNotes.forEach(n => (n.topics || []).forEach(t => { if (!allTopics.includes(t)) allTopics.push(t); }));
    const used = new Set(sysTabs.map(t => t.topic).concat(human.map(h => h.topic)));
    const unused = allTopics.filter(t => !used.has(t));

    const pop = el('div', 'tab-pop');
    pop.setAttribute('role', 'dialog');
    pop.setAttribute('aria-label', 'Manage your smart tabs');
    let html = '<b class="tab-pop-title">Add a tab</b>';
    html += unused.length
      ? '<div class="tab-pop-list">' + unused.map(t =>
          '<button type="button" class="tab-pop-add" data-topic="' + esc(t) + '"><span aria-hidden="true">+ </span>' + esc(t) + '</button>').join('') + '</div>'
      : '<p class="tab-pop-note">Every topic already has a tab in this view.</p>';
    html += '<b class="tab-pop-title">Your tabs</b>';
    if (human.length) {
      html += '<div class="tab-pop-list">' + human.map((h, i) =>
        '<div class="tab-pop-row">' +
          '<span class="tab-pop-name">' + esc(h.label) + '</span>' +
          '<select data-retarget="' + i + '" aria-label="Replace what ' + esc(h.label) + ' shows">' +
            allTopics.map(t => '<option value="' + esc(t) + '"' + (t === h.topic ? ' selected' : '') + '>' + esc(t) + '</option>').join('') +
          '</select>' +
          '<button type="button" class="tab-pop-del" data-del="' + i + '" aria-label="Delete ' + esc(h.label) + '">×</button>' +
        '</div>').join('') + '</div>';
    } else {
      html += '<p class="tab-pop-note">No custom tabs yet. Yours live on this device only — never in the shared intelligence.</p>';
    }
    pop.innerHTML = html;

    pop.addEventListener('click', (ev) => {
      const addB = ev.target.closest('[data-topic]');
      if (addB) {
        const topic = addB.getAttribute('data-topic');
        const h = readHumanTabs();
        const tab = { id: 'human-' + Date.now().toString(36), label: topic, topic };
        h.push(tab); writeHumanTabs(h);
        activeSmartTab = tab.id;
        closeTabManager(); rerender(); return;
      }
      const delB = ev.target.closest('[data-del]');
      if (delB) {
        const h = readHumanTabs();
        const gone = h.splice(+delB.getAttribute('data-del'), 1)[0];
        writeHumanTabs(h);
        if (gone && activeSmartTab === gone.id) activeSmartTab = 'all';
        closeTabManager(); rerender();
      }
    });
    pop.addEventListener('change', (ev) => {
      const sel = ev.target.closest('[data-retarget]');
      if (!sel) return;
      const h = readHumanTabs();
      const i = +sel.getAttribute('data-retarget');
      if (h[i]) { h[i].topic = sel.value; h[i].label = sel.value; writeHumanTabs(h); }
      closeTabManager(); rerender();
    });
    pop.addEventListener('keydown', (ev) => {
      if (ev.key === 'Escape') { closeTabManager(); addBtn.focus(); }
    });
    /* Fixed to the viewport: the tab strip scrolls horizontally, which would
       clip an absolutely-positioned child. */
    document.body.appendChild(pop);
    pop.style.position = 'fixed';
    const r = addBtn.getBoundingClientRect();
    pop.style.top = Math.min(r.bottom + 8, window.innerHeight - 320) + 'px';
    pop.style.left = Math.max(8, Math.min(r.left - 240, window.innerWidth - 346)) + 'px';
    tabPopCloser = (ev) => {
      if (!pop.contains(ev.target) && ev.target !== addBtn && !addBtn.contains(ev.target)) closeTabManager();
    };
    setTimeout(() => document.addEventListener('click', tabPopCloser), 0);
  }


  /* Shell lens slot — owned by the room, positioned by the chassis. */
  const lensSlot = el('div', 'shell-lens');
  lensSlot.hidden = true;

  /* Room outlet — the feed room IS the Main Show: hero, full-width lens,
     layered intelligence boards. Other rooms render their head + renderer. */
  const outlet = el('div', 'room-outlet');
  if (room.id === 'feed') outlet.appendChild(mainShow(room, C, feedStream || 'collective'));
  else {
    const head = el('div', 'room-head');
    head.style.setProperty('--room-accent', room.accent);
    head.innerHTML =
      '<div class="kicker">' + esc(room.kicker) + '</div>' +
      '<h2>' + esc(room.name) + '</h2>' +
      '<p>' + esc(roomDesc(room.id)) + '</p>';
    outlet.appendChild(head);
  }
  const body = el('div', 'room-body');
  body.style.setProperty('--room-accent', room.accent);
  body.setAttribute('aria-live', 'polite');
  const renderer = window.NayaRooms && window.NayaRooms[room.id];
  if (renderer) {
    try { body.appendChild(renderer()); }
    catch (err) { body.appendChild(roomError(room, err)); }
  } else body.appendChild(notVerified(room));
  outlet.appendChild(body);

  main.append(top, searchWrap, lensSlot, outlet);

  /* ——— RIGHT RAIL · Naya presence (wide screens) ——— */
  const right = el('aside', 'rail right');
  right.setAttribute('aria-label', 'Naya');
  right.appendChild(nayaCard());

  /* ——— Mobile drawer backdrop ——— */
  const backdrop = el('div', 'drawer-backdrop');
  backdrop.setAttribute('aria-hidden', 'true');
  backdrop.addEventListener('click', closeDrawer);

  shell.append(rail, main, right, backdrop);

  /* Chassis API — exactly one shell-level lens. */
  window.NayaChassis = window.NayaChassis || {};
  window.NayaChassis.setLens = node => {
    lensSlot.innerHTML = '';
    if (node) { lensSlot.appendChild(node); lensSlot.hidden = false; }
    else lensSlot.hidden = true;
  };
  window.NayaChassis.room = room;
  window.NayaChassis.closeDrawer = closeDrawer;

  ensureGlobalKeys();
  return shell;

  /* ——— internals ——— */
  function openDrawer() {
    shell.classList.add('drawer-open');
    document.body.classList.add('drawer-open');
    roomsPlus.setAttribute('aria-expanded', 'true');
    const f = nav.querySelector('.nav-btn');
    if (f) f.focus();
  }
  function closeDrawer() {
    shell.classList.remove('drawer-open');
    document.body.classList.remove('drawer-open');
    roomsPlus.setAttribute('aria-expanded', 'false');
  }
  function toggleMenu() {
    const willOpen = plusMenu.hidden;
    plusMenu.hidden = !willOpen;
    plusBtn.setAttribute('aria-expanded', String(willOpen));
    if (willOpen) { const f = plusMenu.querySelector('.pluslink'); if (f) f.focus(); }
  }
  function closeMenu() {
    if (!plusMenu.hidden) { plusMenu.hidden = true; plusBtn.setAttribute('aria-expanded', 'false'); }
  }
  function ensureGlobalKeys() {
    if (window.__nayaChassisKeys) return;
    window.__nayaChassisKeys = true;
    document.addEventListener('click', e => {
      if (!e.target.closest('.pluswrap')) {
        document.querySelectorAll('.plusmenu').forEach(m => { m.hidden = true; });
        document.querySelectorAll('.plus-btn').forEach(b => b.setAttribute('aria-expanded', 'false'));
      }
    });
    document.addEventListener('keydown', e => {
      if (e.key !== 'Escape') return;
      document.querySelectorAll('.plusmenu').forEach(m => { m.hidden = true; });
      const open = document.querySelector('.shell.drawer-open');
      if (open) {
        open.classList.remove('drawer-open');
        document.body.classList.remove('drawer-open');
        const t = open.querySelector('.rooms-plus');
        if (t) { t.setAttribute('aria-expanded', 'false'); t.focus(); }
      }
    });
  }

  /* ═══ THE MAIN SHOW — hero, full-width lens, layered intelligence boards ═══ */
  function mainShow(rm, content, stream) {
    const wrap = el('div', 'main-show');

    /* — Hero — */
    const hour = new Date().getHours();
    const greet = hour < 12 ? 'Good morning' : hour < 18 ? 'Good afternoon' : 'Good evening';
    // Identity comes from the canonical chassis identity model — never a hardcoded name.
    let who = '';
    try {
      const id = R.identitySnapshot && R.identitySnapshot();
      if (id && id.display_name && id.display_name !== 'You') who = ', ' + id.display_name;
    } catch (e) { /* identity unavailable — fall back to neutral greeting */ }
    const hero = el('section', 'hero');
    hero.style.setProperty('--room-accent', rm.accent);
    hero.innerHTML =
      '<div class="eyebrow">NAYANET · HUMAN-FACING INTELLIGENCE</div>' +
      '<h1>' + greet + esc(who) + '.</h1>' +
      '<p class="hero-sub">Your intelligence, as it exists now — newest understanding first.</p>' +
      '<p class="hero-prov">Snapshot projection · main 10190133 · nothing fabricated</p>';
    wrap.appendChild(hero);

    /* — Lens: three compact buttons in one row, real navigation — */
    const lens = el('nav', 'lens-tabs');
    lens.setAttribute('aria-label', 'Feed lens');
    const tabs = [
      ['collective', 'COLLECTIVE', 'The shared intelligence stream', '/hub/feed'],
      ['personal', 'PERSONAL', 'What is yours — your directives, your philosophy', '/hub/feed-personal'],
      ['activity', 'ACTIVITY', 'What is happening — chronological', '/hub/feed-activity'],
    ];
    tabs.forEach(([key, label, sub, path]) => {
      const b = el('button', 'lens-tab' + (stream === key ? ' active' : ''));
      b.setAttribute('aria-current', stream === key ? 'true' : 'false');
      b.setAttribute('aria-label', label + ' — ' + sub);
      b.title = sub;
      b.innerHTML = '<b>' + label + '</b>';
      b.addEventListener('click', () => window.NayaRouter.navigate(path));
      lens.appendChild(b);
    });
    wrap.appendChild(lens);

    /* — Boards — */
    const feed = el('div', 'show-feed');
    const FI = window.NayaFeedIntelligence;
    if (!FI || !FI.notes || !FI.notes.length) {
      feed.appendChild(el('div', 'empty-instrument',
        '<strong>The Main Show is not connected.</strong><p>Layered feed intelligence is unavailable in this package.</p>'));
    } else if (stream === 'activity') {
      feed.appendChild(activityStream(content));
    } else {
      const lensNotes = stream === 'personal' ? FI.notes.filter(n => n.personal) : FI.notes;
      /* Smart Tabs: the strip is generated from this lens's notes, so a
         re-baked snapshot with new notes/topics automatically grows tabs. */
      const tabbed = smartTabStrip(lensNotes, FI.notes);
      wrap.appendChild(tabbed.bar);
      const active = tabbed.tabs.find(t => t.id === activeSmartTab) || tabbed.tabs[0];
      const notes = active.topic ? lensNotes.filter(n => (n.topics || []).includes(active.topic)) : lensNotes;
      if (!notes.length) {
        const elsewhere = active.topic ? FI.notes.filter(n => (n.topics || []).includes(active.topic)).length : 0;
        const emptyTitle = active.topic ? 'No ' + esc(active.topic) + ' here.' : 'Nothing here yet.';
        const emptyBody = active.topic
          ? (elsewhere
              ? 'There ' + (elsewhere === 1 ? 'is 1' : 'are ' + elsewhere) + ' in the full stream — this lens holds none.'
              : 'Nothing in this snapshot carries that topic.')
          : 'No personal intelligence is marked in this snapshot.';
        feed.appendChild(el('div', 'empty-instrument',
          '<strong>' + emptyTitle + '</strong><p>' + emptyBody + '</p>'));
      }
      notes.forEach((n, i) => feed.appendChild(intelBoard(n, i)));
      const prov = el('p', 'show-prov',
        'Boards project the Smart Note snapshot at main 10190133 · fetched 2026-10-02 · ' +
        'topics derived at bake time · canonical source: BRAIN/05-MEMORY/SMART-NOTES in the NayaPOWER repo');
      feed.appendChild(prov);
    }
    wrap.appendChild(feed);
    return wrap;
  }

  /* — Activity stream: chronological, from the snapshot's derived Today items — */
  function activityStream(content) {
    const wrap = el('div', 'activity-stream');
    const items = (content && content.today && (content.today.now || []).concat(content.today.next || [])) || [];
    if (!items.length) {
      wrap.appendChild(el('div', 'empty-instrument',
        '<strong>No activity recorded.</strong><p>This snapshot carries no activity items.</p>'));
      return wrap;
    }
    items.forEach((t, i) => {
      const row = el('div', 'activity-row');
      row.innerHTML =
        '<span class="activity-dot" aria-hidden="true"></span>' +
        '<div><b>' + esc(t.title || t.text || 'Activity') + '</b>' +
        (t.detail ? '<p>' + esc(t.detail) + '</p>' : '') + '</div>';
      wrap.appendChild(row);
    });
    return wrap;
  }

  /* — One intelligence board: rotating board tone, per-layer colors, elevated — */
  function intelBoard(note, idx) {
    const b = el('article', 'intel-board tone-' + note.tone);
    b.setAttribute('aria-label', 'Smart Note ' + note.id);

    const head = el('div', 'ib-head');
    head.innerHTML =
      '<span class="ib-jewel" aria-hidden="true"></span>' +
      '<span class="ib-kind">SMART NOTE</span>' +
      '<span class="ib-id">' + esc(note.id) + '</span>' +
      '<span class="ib-truth">CANDIDATE</span>';
    b.appendChild(head);

    const title = el('h2', 'ib-title', esc(note.title));
    b.appendChild(title);

    const layers = el('div', 'ib-layers');
    note.layers.forEach(L => {
      const layer = el('div', 'ib-layer layer-' + L.color + (L.tier === 'deeper' ? ' is-deeper' : ''));
      const lh = el('button', 'ib-layer-head');
      lh.setAttribute('aria-expanded', L.tier === 'primary' ? 'true' : 'false');
      lh.innerHTML =
        '<span class="ib-dot" aria-hidden="true"></span>' +
        '<b>' + esc(L.name) + '</b>' +
        '<span class="ib-chev" aria-hidden="true">▾</span>';
      const lb = el('div', 'ib-layer-body');
      lb.innerHTML = md(L.body);
      if (L.tier !== 'primary') lb.hidden = true;
      else lh.classList.add('open');
      lh.addEventListener('click', () => {
        const open = lb.hidden;
        lb.hidden = !open;
        lh.classList.toggle('open', open);
        lh.setAttribute('aria-expanded', String(open));
      });
      layer.append(lh, lb);
      layers.appendChild(layer);
    });
    b.appendChild(layers);

    const foot = el('div', 'ib-foot');
    foot.innerHTML = '<span>' + esc(note.source) + '</span>';
    b.appendChild(foot);
    return b;
  }

  /* Minimal markdown: escape first, then bold/italic/lists/breaks. */
  function md(text) {
    let t = esc(text);
    t = t.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    t = t.replace(/(^|\W)\*([^*\n]+)\*/g, '$1<em>$2</em>');
    t = t.replace(/`([^`]+)`/g, '<code>$1</code>');
    const lines = t.split('\n');
    let html = '', inList = false;
    lines.forEach(line => {
      const m = line.match(/^\s*[-•]\s+(.*)/);
      if (m) {
        if (!inList) { html += '<ul>'; inList = true; }
        html += '<li>' + m[1] + '</li>';
      } else {
        if (inList) { html += '</ul>'; inList = false; }
        if (line.trim()) html += '<p>' + line.trim() + '</p>';
      }
    });
    if (inList) html += '</ul>';
    return html || '<p></p>';
  }

  function nayaCard() {
    const wrap = el('div');
    const card = el('div', 'naya-card');
    card.innerHTML =
      '<div class="naya-face" aria-hidden="true"><span>N</span></div>' +
      '<h2>Naya</h2><div class="naya-sub">TRUSTED THINKING PARTNER</div>' +
      '<div class="naya-block"><b>WHAT NAYA IS DOING</b>' +
      '<p>Surfacing the highest-signal intelligence from the repository snapshot — newest understanding first.</p></div>' +
      '<div class="naya-block"><b>WHY THIS MATTERS</b>' +
      '<p>The Hub should reduce the work required to understand intelligence — not add another place to manage.</p></div>' +
      '<div class="naya-actions">' +
      '<button class="btn" data-act="ask"><span>ASK NAYA</span></button>' +
      '<button class="btn btn-ghost" data-act="today"><span>WHAT SHOULD I KNOW?</span></button>' +
      '</div>';
    card.querySelector('[data-act="ask"]').addEventListener('click', () => {
      const s = document.getElementById('chassisSearch');
      if (s) { s.scrollIntoView({ block: 'nearest', behavior: 'smooth' }); s.focus(); }
    });
    card.querySelector('[data-act="today"]').addEventListener('click', () => window.NayaRouter.navigate('/hub/today'));
    const trust = el('div', 'rail-card');
    trust.innerHTML = '<b>TRUST STATE</b><p>Source content is marked separately from interpretation. Snapshot-pinned; no remote result is fabricated in this package.</p>';
    wrap.append(card, trust);
    return wrap;
  }

  function showSearchResult(res) {
    const payload = res.data ?? res;
    const list = window.NayaRoomKit ? window.NayaRoomKit.items(payload) : [];
    const prev = outlet.querySelector('.global-search-result');
    if (prev) prev.remove();
    const panel = el('section', 'board global-search-result');
    panel.style.setProperty('--room-accent', room.accent);
    panel.innerHTML =
      '<div class="board-head"><div class="board-icon">' + Icons.icon('search') + '</div>' +
      '<div><div class="board-title">Ask the intelligence</div>' +
      '<div class="board-sub">Sourced retrieval · ' + esc(room.name) + ' context</div></div></div>' +
      '<div class="board-body"></div>';
    const pb = panel.querySelector('.board-body');
    const summary = payload.summary || payload.answer || payload.text || '';
    if (summary) {
      const p = el('p', 'search-answer', esc(summary));
      pb.appendChild(p);
    }
    if (list.length && window.NayaRoomKit) {
      const lw = el('div', 'intelligence-list');
      list.slice(0, 8).forEach(x => lw.appendChild(window.NayaRoomKit.intelCard(x, room.accent)));
      pb.appendChild(lw);
    }
    if (!summary && !list.length) {
      pb.appendChild(el('div', 'empty-instrument', '<strong>No verified answer returned.</strong><p>The runtime connected, but returned no displayable intelligence.</p>'));
    }
    const dismiss = el('button', 'btn btn-ghost mini', '<span>Dismiss</span>');
    dismiss.style.setProperty('--btn-accent', room.accent);
    dismiss.addEventListener('click', () => panel.remove());
    pb.appendChild(dismiss);
    outlet.insertBefore(panel, body);
    panel.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
  }

  function notVerified(rm) {
    const c = R.NOT_VERIFIED_COPY || { title: 'Not verified', body: 'This surface is not connected to verified intelligence.' };
    return StatePanel({
      accent: rm.accent, icon: 'lock', title: c.title, body: c.body,
      actions: [{ label: 'System health', icon: 'core', ghost: true,
        onClick: () => window.NayaRouter.navigate('/hub/settings') }],
    });
  }
  function roomError(rm, err) {
    return StatePanel({
      accent: rm.accent, icon: 'alert',
      title: 'This room failed to render',
      body: 'The room renderer threw an error. Nothing was fabricated in its place. ' +
            'Technical detail: ' + esc(err && err.message ? err.message : String(err)),
      actions: [{ label: 'Reload the Hub', icon: 'core',
        onClick: () => window.NayaRouter.navigate('/hub/' + rm.id) }],
    });
  }
  function esc(x) {
    return String(x ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  }
  function roomDesc(id) {
    return {
      feed: 'One stream of everything the collective intelligence wants you to see — newest understanding first.',
      today: 'Your day, answered by the intelligence. What matters, what changed, what deserves you.',
      reports: 'Proof, not promises. Every report carries its evidence and its receipts.',
      library: 'Everything retained, organized by what it means — not where it happened to land.',
      connect: 'One brain. Many doors. Choose how you — or your agents, apps, and systems — step into the same intelligence.',
      ledger: 'Every contribution, valued. The accountability layer of the collective mind.',
      connections: 'Humans, AIs, and machines you share intelligence with — each on your terms.',
      lists: 'Living lists that stay current because the intelligence behind them does.',
      mail: 'Your messages, understood — triaged by meaning, not just recency.',
      spaces: 'Rooms inside the Hub for projects, people, and ideas that belong together.',
      settings: 'Your Hub, your rules. Identity, privacy, doors, preferences — and System Health.'
    }[id] || '';
  }
}

/* Ecosystem destinations — real addresses. The pill bar is gone;
   the plus button is the only ecosystem surface. */
const ECOSYSTEM = [
  ['HOME', 'https://hmclibrary.groovemember.net/home'],
  ['NAYA POWER', 'https://academy.nayanet.app/'],
  ['“5” DAY CHALLENGE', 'https://academy.nayanet.app/'],
  ['ENTER FREE', 'https://humanmaximuscodex.groovesell.com/checkout/08fba2cbd6488ef4d2cc82b52d361dab'],
  ['POWERCAST', 'https://nayanet.groovepages.com/powerplayer'],
  ['WHITE PAPER', 'https://nayanet.groovepages.com/whitepaper'],
  ['ABOUT US', 'https://nayanet.groovepages.com/aboutus'],
  ['HMC LOGIN', 'https://hmclibrary.groovemember.net/login'],
];

window.HubView = HubView;
