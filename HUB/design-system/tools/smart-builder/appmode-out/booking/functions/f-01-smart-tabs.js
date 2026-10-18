/* NayaFunction: smart-tabs v1.1.0
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
   Harvest: Naya_Design_Element_Set_N4.html section 10 (pill ribbon, heart/star states,
     + Add, status line). Architecture learned from Shawn's SmartTabs v9 kit
     (routeMap synonyms, heart-first sort, onNavigate hook, shared storageKey,
     change events, anchored popover geometry) — re-skinned in our soul.
     What-good-looks-like: lists.html ribbon (stable per-tab spectrum color,
     scroll row with edge fades + chevrons, grounded in real data).
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
    ' border:1px solid rgba(255,255,255,.14);border-radius:14px;padding:14px 16px;',
    ' box-shadow:0 10px 30px rgba(0,0,0,.55), inset 0 1px 0 rgba(255,255,255,.06);}', /* Law 15 depth */
    '.nf-tabs h3{margin:0 0 4px;font-size:18px;font-weight:700;color:#fff;}', /* Law 16 size */
    '.nf-tabs .nf-sub{font-size:14px;color:#fff;opacity:.75;margin:0 0 12px;}',
    '.nf-tabs-row{display:flex;gap:10px;overflow-x:auto;padding:6px 2px 10px;',
    ' scrollbar-width:thin;-webkit-overflow-scrolling:touch;}',
    '.nf-smtab{flex:0 0 auto;display:inline-flex;align-items:center;gap:8px;',
    ' background:#101014;color:#fff;border:1.5px solid rgba(255,255,255,.35);', /* Law 6: white at rest */
    ' border-radius:999px;padding:12px 16px;font-size:14px;min-height:44px;cursor:pointer;',
    ' transition:border-color .18s, box-shadow .18s, transform .18s;',
    ' box-shadow:0 4px 14px rgba(0,0,0,.5), inset 0 1px 0 rgba(255,255,255,.05);}',
    '.nf-smtab:hover{border-color:var(--tc);box-shadow:0 0 18px -4px var(--tc), 0 4px 14px rgba(0,0,0,.5);transform:translateY(-1px);}', /* own color ignites */
    '.nf-smtab.active{border-color:var(--tc);box-shadow:0 0 20px -4px var(--tc);}',
    '.nf-smtab .dots{opacity:.6;font-size:16px;letter-spacing:2px;padding:4px 6px;border-radius:8px;}',
    '.nf-smtab .dots:hover{opacity:1;background:rgba(255,255,255,.12);}',
    '.nf-smtab.add{border-style:dashed;}',
    '.nf-tabs-status{font-size:14px;color:#fff;opacity:.85;margin:6px 2px 0;min-height:20px;}',
    '.nf-tabs-ed{display:none;margin-top:10px;border:1px solid rgba(255,255,255,.16);',
    ' border-radius:10px;padding:12px;background:#0d0d11;}',
    '.nf-tabs-ed.open{display:block;}',
    '.nf-tabs-ed label{display:block;font-size:14px;color:#fff;margin:8px 0 4px;}',
    '.nf-tabs-ed input{width:100%;box-sizing:border-box;background:#141419;color:#fff;',
    ' border:1px solid rgba(255,255,255,.25);border-radius:8px;padding:10px;font-size:14px;}',
    '.nf-tabs-ed input:focus{outline:none;border-color:' + UNIT_COLOR + ';}',
    '.nf-tabs-rowbtns{display:flex;gap:8px;margin-top:12px;flex-wrap:wrap;}',
    '.nf-btn{background:#141419;color:#fff;border:1.5px solid rgba(255,255,255,.35);',
    ' border-radius:10px;padding:10px 14px;font-size:14px;min-height:44px;cursor:pointer;}',
    '.nf-btn:hover{border-color:' + UNIT_COLOR + ';box-shadow:0 0 14px -4px ' + UNIT_COLOR + ';}',
    '.nf-btn.danger:hover{border-color:#ff5e6c;box-shadow:0 0 14px -4px #ff5e6c;}',
    '.nf-consent{font-size:14px;color:#fff;opacity:.6;margin:10px 0 0;}'
  ].join('\n');
  document.head.appendChild(st);
}

NF.register(UNIT, {
  version: '1.1.0',
  activate: function(root, config){
    config = config || {};
    if (!root) return { destroy: function(){} };
    cssOnce();
    var key = config.storageKey || 'naya.smarttabs.v1';
    var showStatus = config.showStatus !== false;
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
    wrap.className = 'nf-tabs';
    var h = document.createElement('h3');
    h.textContent = config.title || 'Smart Tabs';
    wrap.appendChild(h);
    var sub = document.createElement('p');
    sub.className = 'nf-sub';
    sub.textContent = 'Your favorites follow you everywhere — click a tab to go, ⋯ to change it. Type a word like "mail" and it finds the way.';
    wrap.appendChild(sub);
    var row = document.createElement('div');
    row.className = 'nf-tabs-row';
    row.setAttribute('role','tablist');
    wrap.appendChild(row);
    var status = document.createElement('p');
    status.className = 'nf-tabs-status';
    status.setAttribute('aria-live','polite');
    if (showStatus) wrap.appendChild(status);
    var ed = document.createElement('div');
    ed.className = 'nf-tabs-ed';
    wrap.appendChild(ed);
    var consent = document.createElement('p');
    consent.className = 'nf-consent';
    consent.textContent = 'Ready now — tabs live on this device. Connect your NayaNET account to carry them across devices (connected is off).';
    wrap.appendChild(consent);
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
      sorted().forEach(function(t){
        var b = document.createElement('button');
        b.type = 'button';
        b.className = 'nf-smtab' + (t.id === activeId ? ' active' : '');
        b.style.setProperty('--tc', tabColor(t.id));
        b.setAttribute('role','tab');
        b.setAttribute('data-id', t.id);
        var lab = document.createElement('span');
        lab.textContent = (t.label || 'Tab') + stateMark(t);
        b.appendChild(lab);
        var dots = document.createElement('span');
        dots.className = 'dots';
        dots.setAttribute('aria-hidden','true');
        dots.textContent = '⋯';
        dots.title = 'Edit this tab';
        b.appendChild(dots);
        on(b, 'click', function(e){
          if (e.target === dots || dots.contains(e.target)) { openEditor(t.id); return; }
          navigate(t);
        });
        row.appendChild(b);
      });
      var add = document.createElement('button');
      add.type = 'button';
      add.className = 'nf-smtab add';
      add.style.setProperty('--tc', UNIT_COLOR);
      add.textContent = '＋ Add';
      on(add, 'click', function(){ openEditor(null); });
      row.appendChild(add);
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
        root.innerHTML = '';
      }
    };
  }
});
})();
