/* NayaFunction: smart-tabs v1.1.4
   What: Scrolling ribbon of favorite pages/apps/URLs — add, edit, remove, persist.
   Standard: ships on EVERY app (Shawn 2026-10-18) — personal pages included.
     Machine check: an app without the Tabs bar is incomplete.
   Activation: <div data-fn="smart-tabs" data-fn-config='{...}'></div>
   Config: {
     tabs: [{id, label, url, state}]  seed tabs, shown until the user saves their own
       (also accepts {route, heart, star} shape — normalized on load)
     storageKey: localStorage key (default 'naya.smarttabs.v1' — SHARED across all
       pages so the ribbon follows the user everywhere)
     routeMap: {word: url}  synonyms — "mail" → Smart Mail, "reports" → Reports…
       A tab with no URL resolves through the map; words, not URLs, for humans.
     onNavigate: function(url, tab)  host router hook. Default: http(s) opens a
       new tab; anything else goes to location.href (host router territory).
     title: heading text (default 'Smart Tabs')
     showStatus: show the live status line (default true)
     compact: true → bar mode — just the scrolling pill row (no heading,
       sub, or consent chrome), for sticky header bars
     destinations: [{label, url}]  places within the host app — the editor
       offers them as a dropdown ("Pick a place in this app…") alongside
       the free URL field, so a tab can point anywhere in the app or
       anywhere on the web
     color: one accent hex for this mount (Law 9 token) — every tab ignites
       in it instead of the per-tab spectrum. One app, one bar color.
     spectrum: true → pill colors walk the Law-10 spectrum BY POSITION —
       purple, blue, green, gold, orange, red, magenta, back to purple.
       Takes precedence over `color`.
     drift: true → the row scrolls slowly on its own (ambient), pausing on
       touch/hover/focus; honors prefers-reduced-motion.
   } — all optional.
   Ready behavior: full ribbon works on this device — click navigates (through the
     host hook), the dots-menu cycles priority/favorite and edits/removes the tab,
     + Add creates one. Hearts sort first, then stars — the most important tabs
     literally rise to the top. Everything persists in localStorage and every
     mutation fires a 'smarttabs-change' event on the mount root.
   Connected behavior: none — the `connected` key is reserved for a future account sync.
   Backend twin: builder-review/HUB/design-system/tools/smart-builder/functions/feature_smart_tabs.py
     (noted here only — this unit is fully client-side and never calls it).
   Reachable-everywhere: the assembler mounts this unit in the shared chrome of every
     page — the ribbon persists per storageKey and follows the user page to page.
   Harvest: v1.1.4 re-skins the pill + ⋯ menu VERBATIM from the Hub
   (~/workspace/user/files/index-2.html `.smart-tab` / `.tab-menu` — "SmartTabs v9
   pill language (Naya 4's port)"): dark pill, bold label, per-tab --tc, white light
   idle, own color ignites on hover with translateY(-2px) + inset glow; ⋯ opens a
   fixed-position labeled menu (Edit / Set Purple Heart / Set Gold Star / Remove)
   with smart placeNear positioning. Earlier provenance: Naya_Design_Element_Set_N4
   section 10; Shawn's SmartTabs v9 kit architecture (routeMap, heart-first sort,
   onNavigate, shared storageKey, change events); lists.html ribbon.
   Lesson L-2026-10-17-002: a tab navigates ONLY when it has a real destination —
     URL or routeMap hit. A tab with neither says so instead of being a dead link.
*/
(function(){
'use strict';
var NF = window.NayaFunctions = window.NayaFunctions || {};
NF._r = NF._r || {};
NF.register = NF.register || function(id, def){
  if (NF._r[id]) return; // one function, one implementation — never double-register
  NF._r[id] = def;
};

var UNIT = 'smart-tabs';
var UNIT_COLOR = '#e84fff'; /* Law 9 token — one color job per unit (Law 5) */
var PALETTE = ['#e84fff','#a06bff','#3fb8ff','#2fe89e','#ffbf3d','#40d3bb','#6675ff','#ff9a5a']; /* Law 9 verbatim tokens */
/* Law 10 spectrum walk, by position: purple → blue → green → gold → orange → red → magenta → purple… */
var SPECTRUM = ['#a06bff','#3fb8ff','#2fe89e','#ffbf3d','#ff9a5a','#ff5e6c','#e84fff'];

/* Default synonyms: words humans type → real destinations. Hosts extend via config.routeMap. */
var DEFAULT_ROUTES = {
  'smart feed':'#feed', 'feed':'#feed',
  'today':'#today', 'intelligence today':'#today',
  'reports':'#reports', 'report':'#reports',
  'library':'#library',
  'connect':'#connect', 'smart connect':'#connect',
  'ledger':'#ledger', 'smart ledger':'#ledger',
  'connections':'#connections',
  'lists':'#lists', 'smart lists':'#lists',
  'mail':'#mail', 'smart mail':'#mail',
  'spaces':'#spaces', 'smart spaces':'#spaces',
  'settings':'#settings'
};

function esc(s){
  return String(s == null ? '' : s).replace(/[&<>"']/g, function(c){
    return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];
  });
}
function storeGet(key, fallback){
  try {
    var raw = window.localStorage.getItem(key);
    if (raw == null) return fallback;
    return JSON.parse(raw);
  } catch(e){ return fallback; }
}
function storeSet(key, val){
  try { window.localStorage.setItem(key, JSON.stringify(val)); return true; }
  catch(e){ return false; }
}
/* Stable color per tab: color is the tab's identity — it must NOT shift when
   hearts/stars re-sort the ribbon. Hash the id, not the index. */
function tabColor(id){
  var h = 0, s = String(id || '');
  for (var i = 0; i < s.length; i++) h = ((h * 31) + s.charCodeAt(i)) | 0;
  return PALETTE[Math.abs(h) % PALETTE.length];
}
function uid(prefix){ return prefix + '-' + Date.now().toString(36) + '-' + Math.floor(Math.random()*1e6).toString(36); }
/* Normalize both data shapes: ours {url, state} and the kit's {route, heart, star}. */
function normTab(t){
  t = t || {};
  var state = t.state || null;
  if (!state) {
    if (t.heart) state = 'heart';
    else if (t.star) state = 'star';
  }
  return { id: t.id || uid('tab'), label: t.label || 'Tab', url: t.url || t.route || '', state: state };
}
function routeFrom(label, map){
  var k = String(label || '').trim().toLowerCase();
  return map[k] || '';
}
function cssOnce(){
  if (document.querySelector('style[data-nf-css="smart-tabs"]')) return;
  var st = document.createElement('style');
  st.setAttribute('data-nf-css','smart-tabs');
  st.textContent = [
    '.nf-tabs{font-family:Inter,system-ui,sans-serif;color:#fff;background:#0a0a0d;',
    ' --st-accent:#e84fff;',
    ' border:1px solid rgba(255,255,255,.14);border-radius:14px;padding:14px 16px;',
    ' box-shadow:0 10px 30px rgba(0,0,0,.55), inset 0 1px 0 rgba(255,255,255,.06);}', /* Law 15 depth */
    '.nf-tabs h3{margin:0 0 4px;font-size:18px;font-weight:700;color:#fff;}', /* Law 16 size */
    '.nf-tabs .nf-sub{font-size:14px;color:#fff;opacity:.75;margin:0 0 12px;}',
    '.nf-tabs-row{display:flex;gap:10px;overflow-x:auto;padding:6px 2px 10px;',
    ' scrollbar-width:thin;-webkit-overflow-scrolling:touch;}',
    /* ——— Pill skin HARVESTED VERBATIM from the Hub (index-2.html `.smart-tab`:
       "SmartTabs v9 pill language (Naya 4's port)") — dark pill, bold label,
       per-tab --tc, white light idle, own color ignites on hover. ——— */
    '.nf-smtab{flex:0 0 auto;display:inline-flex;align-items:center;gap:10px;',
    ' padding:12px 20px;border-radius:999px;cursor:pointer;user-select:none;',
    ' border:2px solid rgba(255,255,255,.45);background:rgba(0,0,0,.55);',
    ' color:#fff;font-family:inherit;font-weight:900;font-size:13px;letter-spacing:.03em;',
    ' white-space:nowrap;min-height:44px;',
    /* Law 15 sharpened x3 (Shawn 2026-10-18): multi-layered depth, coming out of the screen —
       the Hub's depth grammar (inset light + inset carve + ambient + drop).
       Rest = NICE visible white light, never a faint hairline. */
    ' box-shadow:inset 0 1px 0 rgba(255,255,255,.35), inset 0 -3px 8px rgba(0,0,0,.5),',
    ' 0 0 18px rgba(255,255,255,.18), 0 10px 26px rgba(0,0,0,.6);',
    ' border:2px solid rgba(255,255,255,.8);',
    ' transition:box-shadow .25s, border-color .2s, text-shadow .25s, transform .18s;}',
    '.nf-smtab:hover,.nf-smtab:focus-visible{border-color:var(--tc);outline:none;',
    ' transform:translateY(-3px) scale(1.03);',
    ' box-shadow:inset 0 1px 0 rgba(255,255,255,.4), inset 0 -2px 6px rgba(0,0,0,.35),',
    ' 0 0 32px -2px var(--tc), 0 0 0 2px var(--tc) inset, 0 14px 32px rgba(0,0,0,.6);',
    ' text-shadow:0 0 12px var(--tc);}',
    '.nf-smtab.active{border-color:rgba(255,255,255,.6);',
    ' box-shadow:0 0 16px rgba(255,255,255,.18), inset 0 1px rgba(255,255,255,.15);}',
    '.nf-smtab.loved{box-shadow:inset 0 1px rgba(255,255,255,.3), inset 0 0 0 2px rgba(160,107,255,.6), 0 0 22px -2px #a06bff, 0 8px 22px rgba(0,0,0,.55);}',
    '.nf-smtab.starred{box-shadow:inset 0 1px rgba(255,255,255,.3), inset 0 0 0 2px rgba(255,191,61,.6), 0 0 22px -2px #ffbf3d, 0 8px 22px rgba(0,0,0,.55);}',
    /* Hub's `.sn-more`: the ⋯ is a real button, white at rest */
    '.nf-smtab .sn-more{border:0;background:rgba(255,255,255,.1);color:#fff;border-radius:8px;',
    ' padding:3px 9px;cursor:pointer;font-size:13px;line-height:1.5;font-family:inherit;',
    ' transition:background .2s;min-height:0;}',
    '.nf-smtab .sn-more:hover{background:rgba(255,255,255,.22);}',
    '.nf-smtab.add{border-style:dashed;color:rgba(255,255,255,.75);}',
    /* ——— ⋯ menu: Hub's `.tab-menu` pattern, fixed popover, labeled rows ——— */
    '.nf-tabmenu{position:fixed;z-index:1000;display:none;',
    ' background:linear-gradient(180deg,#121827,#0e1424);',
    ' border:1px solid rgba(255,255,255,.18);border-radius:12px;',
    ' box-shadow:0 18px 40px rgba(0,0,0,.5);min-width:220px;}',
    '.nf-tabmenu .mi{padding:10px 12px;border-bottom:1px solid rgba(255,255,255,.08);',
    ' cursor:pointer;color:#fff;font-weight:800;font-size:13px;font-family:inherit;}',
    '.nf-tabmenu .mi:last-child{border-bottom:none;}',
    '.nf-tabmenu .mi:hover{background:rgba(255,255,255,.06);}',
    '.nf-tabs-status{font-size:14px;color:#fff;opacity:.85;margin:6px 2px 0;min-height:20px;}',
    '.nf-tabs-ed{display:none;margin-top:10px;border:1px solid rgba(255,255,255,.16);',
    ' border-radius:10px;padding:12px;background:#0d0d11;}',
    '.nf-tabs-ed.open{display:block;}',
    '.nf-tabs-ed label{display:block;font-size:14px;color:#fff;margin:8px 0 4px;}',
    '.nf-tabs-ed input{width:100%;box-sizing:border-box;background:#141419;color:#fff;',
    ' border:1px solid rgba(255,255,255,.25);border-radius:8px;padding:10px;font-size:14px;}',
    '.nf-tabs-ed input:focus{outline:none;border-color:var(--st-accent);}',
    '.nf-tabs-ed select:focus{outline:none;border-color:var(--st-accent);}',
    '.nf-tabs-rowbtns{display:flex;gap:8px;margin-top:12px;flex-wrap:wrap;}',
    '.nf-btn{background:#141419;color:#fff;border:1.5px solid rgba(255,255,255,.35);',
    ' border-radius:10px;padding:10px 14px;font-size:14px;min-height:44px;cursor:pointer;}',
    '.nf-btn:hover{border-color:var(--st-accent);box-shadow:0 0 14px -4px var(--st-accent);}',
    '.nf-btn.primary{border-color:var(--st-accent);}',
    '.nf-btn.danger:hover{border-color:#ff5e6c;box-shadow:0 0 14px -4px #ff5e6c;}',
    '.nf-consent{font-size:14px;color:#fff;opacity:.6;margin:10px 0 0;}',
    /* compact bar mode — the ribbon as a bare scrolling strip */
    '.nf-tabs.nf-compact{background:transparent;border:none;border-radius:0;padding:6px 0;box-shadow:none;}',
    '.nf-tabs.nf-compact .nf-tabs-row{padding:6px 2px;}',
    '.nf-tabs.nf-compact .nf-tabs-status{font-size:12px;margin:2px 2px 0;}',
    '.nf-tabs-ed select{width:100%;box-sizing:border-box;background:#141419;color:#fff;',
    ' border:1px solid rgba(255,255,255,.25);border-radius:8px;padding:10px;font-size:14px;margin:8px 0 4px;}',
    /* the pill anchors the Hub-pattern menu only via placeNear (fixed positioning) */
    '.nf-smtab{position:relative;}'
  ].join('\n');
  document.head.appendChild(st);
}

NF.register(UNIT, {
  version: '1.1.4',
  activate: function(root, config){
    config = config || {};
    if (!root) return { destroy: function(){} };
    cssOnce();
    var key = config.storageKey || 'naya.smarttabs.v1';
    var showStatus = config.showStatus !== false;
    var compact = config.compact === true;
    var accent = config.color || null; /* one bar color for this app (Law 9 token) */
    var destinations = Array.isArray(config.destinations) ? config.destinations : [];
    var routeMap = {};
    var k;
    for (k in DEFAULT_ROUTES) routeMap[k] = DEFAULT_ROUTES[k];
    if (config.routeMap) for (k in config.routeMap) routeMap[k] = config.routeMap[k];
    var onNavigate = (typeof config.onNavigate === 'function') ? config.onNavigate
      : function(url){
          if (/^https?:\/\//i.test(url)) { try { window.open(url, '_blank', 'noopener'); } catch(e){} }
          else { window.location.href = url; }
        };
    var listeners = [];
    function on(el, ev, fn){ el.addEventListener(ev, fn); listeners.push([el, ev, fn]); }

    var tabs = storeGet(key, null);
    if (!Array.isArray(tabs)) {
      tabs = Array.isArray(config.tabs) ? config.tabs.slice() : [];
    }
    tabs = tabs.map(normTab);
    var activeId = null;
    var editingId = null; /* null = add mode, string = edit mode */

    root.innerHTML = '';
    var wrap = document.createElement('div');
    wrap.className = 'nf-tabs' + (compact ? ' nf-compact' : '');
    if (accent) wrap.style.setProperty('--st-accent', accent);
    if (!compact) {
      var h = document.createElement('h3');
      h.textContent = config.title || 'Smart Tabs';
      wrap.appendChild(h);
      var sub = document.createElement('p');
      sub.className = 'nf-sub';
      sub.textContent = 'Your favorites follow you everywhere — click a tab to go, ⋯ to change it. Type a word like "mail" and it finds the way.';
      wrap.appendChild(sub);
    }
    var row = document.createElement('div');
    row.className = 'nf-tabs-row';
    row.setAttribute('role','tablist');
    row.setAttribute('aria-label', config.title || 'Smart Tabs');
    wrap.appendChild(row);
    var status = document.createElement('p');
    status.className = 'nf-tabs-status';
    status.setAttribute('aria-live','polite');
    if (showStatus) wrap.appendChild(status);
    var ed = document.createElement('div');
    ed.className = 'nf-tabs-ed';
    wrap.appendChild(ed);
    if (!compact) {
      var consent = document.createElement('p');
      consent.className = 'nf-consent';
      consent.textContent = 'Ready now — tabs live on this device. Connect your NayaNET account to carry them across devices (connected is off).';
      wrap.appendChild(consent);
    }
    root.appendChild(wrap);

    function say(msg){ if (showStatus) status.textContent = msg; }
    function persist(){
      storeSet(key, tabs);
      try {
        root.dispatchEvent(new CustomEvent('smarttabs-change', { detail: tabs.slice(), bubbles: true }));
      } catch(e){}
    }
    /* Hearts first, then stars, then insertion order — the most important
       tabs literally rise to the top. */
    function sorted(){
      return tabs.slice().sort(function(a, b){
        var pa = (a.state === 'heart' ? 2 : 0) + (a.state === 'star' ? 1 : 0);
        var pb = (b.state === 'heart' ? 2 : 0) + (b.state === 'star' ? 1 : 0);
        return pb - pa;
      });
    }
    function stateMark(t){
      if (t.state === 'heart') return ' 💜';
      if (t.state === 'star') return ' ⭐';
      return '';
    }
    function destination(t){
      if (t.url) return t.url;
      return routeFrom(t.label, routeMap);
    }

    function render(){
      row.innerHTML = '';
      closeTabMenu();
      var useSpectrum = config.spectrum === true;
      sorted().forEach(function(t, i){
        var b = document.createElement('button');
        b.type = 'button';
        b.className = 'nf-smtab' + (t.id === activeId ? ' active' : '')
          + (t.state === 'heart' ? ' loved' : '') + (t.state === 'star' ? ' starred' : '');
        b.style.setProperty('--tc', useSpectrum ? SPECTRUM[i % SPECTRUM.length] : (accent || tabColor(t.id)));
        b.setAttribute('role','tab');
        b.setAttribute('data-id', t.id);
        var lab = document.createElement('span');
        lab.textContent = (t.label || 'Tab') + stateMark(t);
        b.appendChild(lab);
        /* Hub's `.sn-more`: a real button — white at rest, never a dead span */
        var more = document.createElement('button');
        more.type = 'button';
        more.className = 'sn-more';
        more.textContent = '⋯';
        more.setAttribute('aria-label','Tab options — edit, heart, star, remove');
        more.title = 'Edit, heart, star or remove';
        on(more, 'click', function(e){ e.stopPropagation(); openTabMenu(t, b); });
        b.appendChild(more);
        on(b, 'click', function(){ navigate(t); });
        row.appendChild(b);
      });
      var add = document.createElement('button');
      add.type = 'button';
      add.className = 'nf-smtab add';
      add.style.setProperty('--tc', accent || UNIT_COLOR);
      add.textContent = '＋ Add';
      on(add, 'click', function(){ closeTabMenu(); openEditor(null); });
      row.appendChild(add);
    }

    /* ——— ⋯ menu: the Hub's `.tab-menu` pattern, harvested verbatim —
       fixed-position popover with labeled rows (Edit / Set Purple Heart /
       Set Gold Star / Remove), smart placeNear positioning so it never
       falls off-screen. Closes on outside click or Escape. ——— */
    var tabMenu = null, tabMenuTab = null;
    function closeTabMenu(){
      if (tabMenu && tabMenu.parentNode) tabMenu.parentNode.removeChild(tabMenu);
      tabMenu = null; tabMenuTab = null;
    }
    function findTab(id){
      for (var i = 0; i < tabs.length; i++) if (tabs[i].id === id) return tabs[i];
      return null;
    }
    /* Hub's placeNear: below the anchor, flips above near the viewport
       bottom, clamps horizontally — the menu is always fully visible. */
    function placeNear(anchor, pop, pad){
      pad = pad || 8;
      pop.style.visibility = 'hidden';
      pop.style.display = 'block';
      var r;
      try { r = anchor.getBoundingClientRect(); }
      catch(e){ r = { left: pad, top: pad, bottom: pad + 40, right: pad + 200 }; }
      var pw = pop.offsetWidth || 220, ph = pop.offsetHeight || 190;
      var x = r.left;
      try {
        if (x + pw > window.innerWidth - pad) x = window.innerWidth - pw - pad;
        if (x < pad) x = pad;
        var y = r.bottom + 8;
        if (y + ph > window.innerHeight - pad) y = r.top - ph - 8;
        if (y < pad) y = pad;
      } catch(e){ var y = pad; }
      pop.style.left = x + 'px';
      pop.style.top = y + 'px';
      pop.style.visibility = '';
    }
    function openTabMenu(t, anchor){
      closeTabMenu();
      if (!t || !anchor) return;
      tabMenuTab = t;
      var m = document.createElement('div');
      m.className = 'nf-tabmenu';
      m.setAttribute('role','menu');
      [['edit','\u270F\uFE0F Edit'],['heart','\uD83D\uDC9C Set Purple Heart'],
       ['star','\u2B50 Set Gold Star'],['remove','\u2715 Remove']].forEach(function(pair){
        var mi = document.createElement('div');
        mi.className = 'mi';
        mi.textContent = pair[1];
        mi.setAttribute('role','menuitem');
        on(mi, 'click', function(){ tabMenuAction(pair[0]); });
        m.appendChild(mi);
      });
      document.body.appendChild(m);
      tabMenu = m;
      placeNear(anchor, m, 8);
    }
    function tabMenuAction(act){
      var t = tabMenuTab;
      closeTabMenu();
      if (!t) return;
      if (act === 'edit') { openEditor(t.id); }
      else if (act === 'heart' || act === 'star') {
        var cur = t.state === act ? null : act;
        t.state = cur;
        persist(); render();
        say('"' + t.label + '"' + (cur === 'heart' ? ' has the \uD83D\uDC9C purple heart — it rises to the front.'
          : cur === 'star' ? ' has the \u2B50 gold star.' : ' is a plain tab again.'));
      }
      else if (act === 'remove') {
        tabs = tabs.filter(function(x){ return x.id !== t.id; });
        if (activeId === t.id) activeId = null;
        persist(); render();
        say('Removed "' + t.label + '".');
      }
    }
    /* Outside click / Escape closes the tab menu. */
    function tabMenuOutside(e){
      if (!tabMenu) return;
      var n = e.target;
      while (n) { if (n === tabMenu) return; n = n.parentNode; }
      closeTabMenu();
    }
    function tabMenuEsc(e){ if ((e.key === 'Escape' || e.keyCode === 27) && tabMenu) closeTabMenu(); }
    if (typeof document.addEventListener === 'function') {
      document.addEventListener('click', tabMenuOutside);
      listeners.push([document, 'click', tabMenuOutside]);
      document.addEventListener('keydown', tabMenuEsc);
      listeners.push([document, 'keydown', tabMenuEsc]);
    }

    /* Ambient drift: the row scrolls slowly in one direction and wraps around —
       a gentle marquee, never ping-ponging back. Pauses on touch/hover/focus;
       honors prefers-reduced-motion. */
    var driftTimer = null, driftPoke = 0;
    function driftReduced(){
      try { return window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches; }
      catch(e){ return false; }
    }
    function driftTick(){
      if (document.hidden || driftReduced()) return;
      if (Date.now() - driftPoke < 6000) return;
      var m = row.scrollWidth - row.clientWidth;
      if (m <= 4) return;
      var n = row.scrollLeft + 0.8;
      if (n >= m) n = 0; /* wrap: the ribbon flows one way, endlessly */
      row.scrollLeft = n;
    }
    if (config.drift === true && typeof setInterval === 'function' && !driftReduced()) {
      driftTimer = setInterval(driftTick, 40);
      ['pointerenter','pointerdown','focusin','touchstart','wheel'].forEach(function(t){
        var poke = function(){ driftPoke = Date.now(); };
        row.addEventListener(t, poke, { passive: true });
        listeners.push([row, t, poke]);
      });
    }

    function navigate(t){
      activeId = t.id;
      render();
      var dest = destination(t);
      if (dest) {
        say('Opening ' + (t.label || 'tab') + '…');
        try { onNavigate(dest, t); }
        catch(e){ say('Could not go there — the destination may be blocked here.'); }
      } else {
        say('"' + (t.label || 'Tab') + '" has no destination yet — open ⋯ and add a URL or a known word.');
      }
    }

    function openEditor(id){
      editingId = id;
      var t = null;
      if (id) {
        for (var i = 0; i < tabs.length; i++) if (tabs[i].id === id) t = tabs[i];
      }
      ed.classList.add('open');
      ed.innerHTML = '';
      var title = document.createElement('p');
      title.style.cssText = 'margin:0 0 4px;font-size:18px;font-weight:700;color:#fff;';
      title.textContent = t ? 'Edit tab' : 'Add a tab';
      ed.appendChild(title);
      function field(labelText, value, ph){
        var lb = document.createElement('label');
        lb.textContent = labelText;
        var inp = document.createElement('input');
        inp.value = value || '';
        inp.placeholder = ph || '';
        ed.appendChild(lb); ed.appendChild(inp);
        return inp;
      }
      var nameIn = field('Name', t ? t.label : '', 'e.g. SoulSchool');
      var urlIn = field('Destination — URL or a word like "mail"', t ? (t.url || '') : '', 'https://… or just a word');
      if (destinations.length) {
        var dlb = document.createElement('label');
        dlb.textContent = '…or pick a place in this app';
        var dsel = document.createElement('select');
        var opt0 = document.createElement('option');
        opt0.value = ''; opt0.textContent = 'Pick a place in this app…';
        dsel.appendChild(opt0);
        destinations.forEach(function(d){
          var o = document.createElement('option');
          o.value = d.url || ''; o.textContent = d.label || d.url || '';
          if (t && t.url && t.url === o.value) o.selected = true;
          dsel.appendChild(o);
        });
        on(dsel, 'change', function(){
          if (dsel.value) {
            urlIn.value = dsel.value;
            var d = null;
            destinations.forEach(function(x){ if (x.url === dsel.value) d = x; });
            if (d && d.label && !nameIn.value.trim()) nameIn.value = d.label;
          }
        });
        ed.appendChild(dlb); ed.appendChild(dsel);
      }
      var rowBtns = document.createElement('div');
      rowBtns.className = 'nf-tabs-rowbtns';
      function mkBtn(txt, cls, fn){
        var b = document.createElement('button');
        b.type = 'button'; b.className = 'nf-btn ' + (cls || ''); b.textContent = txt;
        on(b, 'click', fn); rowBtns.appendChild(b); return b;
      }
      if (t) {
        var stateLabel = t.state === 'heart' ? '💜 Priority — tap to make ⭐ Favorite'
          : t.state === 'star' ? '⭐ Favorite — tap to clear' : 'Plain — tap to mark 💜 Priority';
        mkBtn(stateLabel, '', function(){
          t.state = t.state === 'heart' ? 'star' : (t.state === 'star' ? null : 'heart');
          persist(); render(); openEditor(t.id);
          say('"' + t.label + '"' + (t.state === 'heart' ? ' is now a 💜 priority.' : t.state === 'star' ? ' is now a ⭐ favorite.' : ' is a plain tab again.'));
        });
      }
      mkBtn(t ? 'Save' : 'Add tab', 'primary', function(){
        var name = nameIn.value.trim();
        var url = urlIn.value.trim();
        if (!name) { say('Give the tab a name first.'); nameIn.focus(); return; }
        if (t) { t.label = name; t.url = url; say('Saved "' + name + '".'); }
        else {
          tabs.push({ id: uid('tab'), label: name, url: url, state: null });
          say('Added "' + name + '" — it now rides this ribbon everywhere.');
        }
        persist(); render(); closeEditor();
      });
      if (t) {
        mkBtn('Remove', 'danger', function(){
          tabs = tabs.filter(function(x){ return x.id !== t.id; });
          if (activeId === t.id) activeId = null;
          persist(); render(); closeEditor();
          say('Removed "' + t.label + '".');
        });
      }
      mkBtn('Close', '', closeEditor);
      ed.appendChild(rowBtns);
      setTimeout(function(){ nameIn.focus(); }, 50);
    }
    function closeEditor(){ ed.classList.remove('open'); ed.innerHTML = ''; editingId = null; }

    render();
    if (!tabs.length) say('No tabs yet — tap ＋ Add to pin your first favorite.');
    else say('Click a tab to go there, ⋯ to change it.');

    return {
      list: function(){ return tabs.map(normTab); },
      destroy: function(){
        listeners.forEach(function(l){ try { l[0].removeEventListener(l[1], l[2]); } catch(e){} });
        listeners = [];
        try { if (driftTimer) clearInterval(driftTimer); } catch(e){}
        driftTimer = null;
        try { closeTabMenu(); } catch(e){}
        root.innerHTML = '';
      }
    };
  }
});
})();
