/* NayaFunction: smart-tabs v1.0.0
   What: Scrolling ribbon of favorite pages/apps/URLs — add, edit, remove, persist.
   Activation: <div data-fn="smart-tabs" data-fn-config='{...}'></div>
   Config: {
     tabs: [{id, label, url, state}]  seed tabs, shown until the user saves their own
     storageKey: localStorage key (default 'naya.smarttabs.v1')
     title: heading text (default 'Smart Tabs')
     showStatus: show the live status line (default true)
   } — all optional.
   Ready behavior: full ribbon works on this device — click navigates (opens the tab's
     URL), the dots-menu cycles priority/favorite and edits/removes the tab, + Add
     creates one. Everything persists in localStorage.
   Connected behavior: none — the `connected` key is reserved for a future account sync.
   Backend twin: builder-review/HUB/design-system/tools/smart-builder/functions/feature_smart_tabs.py
     (noted here only — this unit is fully client-side and never calls it).
   Reachable-everywhere: the assembler mounts this unit in the shared chrome of every
     page — the ribbon persists per storageKey and follows the user page to page.
   Harvest: Naya_Design_Element_Set_N4.html section 10 (pill ribbon, heart/star states,
     + Add, status line). Lesson L-2026-10-17-002: a tab navigates ONLY when it has a
     real URL — a tab with no destination says so instead of being a dead link.
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
    '.nf-btn.primary{border-color:' + UNIT_COLOR + ';}',
    '.nf-btn.danger:hover{border-color:#ff5e6c;box-shadow:0 0 14px -4px #ff5e6c;}',
    '.nf-consent{font-size:14px;color:#fff;opacity:.6;margin:10px 0 0;}'
  ].join('\n');
  document.head.appendChild(st);
}

function tabColor(i){ return PALETTE[(i * 3 + 1) % PALETTE.length]; } /* spaced hues — Law 4 */
function uid(prefix){ return prefix + '-' + Date.now().toString(36) + '-' + Math.floor(Math.random()*1e6).toString(36); }

NF.register(UNIT, {
  version: '1.0.0',
  activate: function(root, config){
    config = config || {};
    if (!root) return { destroy: function(){} };
    cssOnce();
    var key = config.storageKey || 'naya.smarttabs.v1';
    var showStatus = config.showStatus !== false;
    var listeners = [];
    function on(el, ev, fn){ el.addEventListener(ev, fn); listeners.push([el, ev, fn]); }

    var tabs = storeGet(key, null);
    if (!Array.isArray(tabs)) {
      tabs = Array.isArray(config.tabs) ? config.tabs.slice() : [];
    }
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
    sub.textContent = 'Your favorites follow you everywhere — click a tab to go, ⋯ to change it.';
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
    function persist(){ storeSet(key, tabs); }

    function stateMark(t){
      if (t.state === 'heart') return ' 💜';
      if (t.state === 'star') return ' ⭐';
      return '';
    }

    function render(){
      row.innerHTML = '';
      tabs.forEach(function(t, i){
        var b = document.createElement('button');
        b.type = 'button';
        b.className = 'nf-smtab' + (t.id === activeId ? ' active' : '');
        b.style.setProperty('--tc', tabColor(i));
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
      if (t.url) {
        say('Opening ' + (t.label || 'tab') + '…');
        try { window.open(t.url, '_blank', 'noopener'); }
        catch(e){ say('Could not open the link — the address may be blocked here.'); }
      } else {
        say('"' + (t.label || 'Tab') + '" has no destination yet — open ⋯ and add a URL.');
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
      var urlIn = field('Destination URL', t ? (t.url || '') : '', 'https://…');
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
      destroy: function(){
        listeners.forEach(function(l){ try { l[0].removeEventListener(l[1], l[2]); } catch(e){} });
        listeners = [];
        root.innerHTML = '';
      }
    };
  }
});
})();
