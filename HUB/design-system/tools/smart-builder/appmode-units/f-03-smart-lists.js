/* NayaFunction: smart-lists v1.0.0
   What: Create lists; add notes, contacts and topics as items; check them off.
   Activation: <div data-fn="smart-lists" data-fn-config='{...}'></div>
   Config: {
     lists: [{id, name, items: [{id, text, type, done}]}]  seed lists
     storageKey: localStorage key (default 'naya.smartlists.v1')
     title: heading text (default 'Smart Lists')
   } — all optional.
   Ready behavior: create/rename-free lists, add typed items (note/contact/topic),
     check off, delete items and lists — all persisted in localStorage, zero backend.
   Connected behavior: none — the `connected` key is reserved.
   Backend twin: builder-review/HUB/design-system/tools/smart-builder/functions/feature_smart_list.py
     (noted here only — this unit is fully client-side and never calls it).
   Consent line: the copy states the lists live on this device; connecting an account
     would sync them — ready vs connected never conflated.
   Lesson L-2026-10-17-004: every control below is bound to DOM this unit creates.
*/
(function(){
'use strict';
var NF = window.NayaFunctions = window.NayaFunctions || {};
NF._r = NF._r || {};
NF.register = NF.register || function(id, def){
  if (NF._r[id]) return;
  NF._r[id] = def;
};

var UNIT = 'smart-lists';
var UNIT_COLOR = '#2fe89e'; /* Law 9 token — one color job per unit */
var TYPES = ['note','contact','topic'];

function storeGet(key, fallback){
  try {
    var raw = window.localStorage.getItem(key);
    if (raw == null) return fallback;
    var v = JSON.parse(raw);
    return Array.isArray(v) ? v : fallback;
  } catch(e){ return fallback; }
}
function storeSet(key, val){
  try { window.localStorage.setItem(key, JSON.stringify(val)); return true; }
  catch(e){ return false; }
}
function uid(prefix){ return prefix + '-' + Date.now().toString(36) + '-' + Math.floor(Math.random()*1e6).toString(36); }
function cssOnce(){
  if (document.querySelector('style[data-nf-css="smart-lists"]')) return;
  var st = document.createElement('style');
  st.setAttribute('data-nf-css','smart-lists');
  st.textContent = [
    '.nf-lists{font-family:Inter,system-ui,sans-serif;color:#fff;background:#0a0a0d;',
    ' border:1px solid rgba(255,255,255,.14);border-radius:14px;padding:14px 16px;',
    ' box-shadow:0 10px 30px rgba(0,0,0,.55), inset 0 1px 0 rgba(255,255,255,.06);}',
    '.nf-lists h3{margin:0 0 4px;font-size:18px;font-weight:700;color:#fff;}',
    '.nf-lists .nf-sub{font-size:14px;color:#fff;opacity:.75;margin:0 0 12px;}',
    '.nf-listpills{display:flex;gap:8px;overflow-x:auto;padding:4px 2px 10px;}',
    '.nf-listpill{flex:0 0 auto;background:#101014;color:#fff;border:1.5px solid rgba(255,255,255,.35);',
    ' border-radius:999px;padding:10px 16px;font-size:14px;min-height:44px;cursor:pointer;white-space:nowrap;}',
    '.nf-listpill:hover{border-color:' + UNIT_COLOR + ';}',
    '.nf-listpill.active{border-color:' + UNIT_COLOR + ';box-shadow:0 0 16px -4px ' + UNIT_COLOR + ';}',
    '.nf-addrow{display:flex;gap:8px;margin:10px 0;flex-wrap:wrap;}',
    '.nf-lists input,.nf-lists select{background:#141419;color:#fff;border:1px solid rgba(255,255,255,.25);',
    ' border-radius:8px;padding:10px;font-size:14px;font-family:inherit;}',
    '.nf-lists input:focus,.nf-lists select:focus{outline:none;border-color:' + UNIT_COLOR + ';}',
    '.nf-addrow input{flex:1 1 180px;}',
    '.nf-btn{background:#141419;color:#fff;border:1.5px solid rgba(255,255,255,.35);',
    ' border-radius:10px;padding:10px 14px;font-size:14px;min-height:44px;cursor:pointer;}',
    '.nf-btn:hover{border-color:' + UNIT_COLOR + ';box-shadow:0 0 14px -4px ' + UNIT_COLOR + ';}',
    '.nf-btn.primary{border-color:' + UNIT_COLOR + ';}',
    '.nf-btn.danger:hover{border-color:#ff5e6c;box-shadow:0 0 14px -4px #ff5e6c;}',
    '.nf-item{display:flex;align-items:center;gap:10px;padding:10px 4px;',
    ' border-bottom:1px solid rgba(255,255,255,.1);}',
    '.nf-item input[type=checkbox]{width:22px;height:22px;accent-color:' + UNIT_COLOR + ';flex:0 0 auto;}',
    '.nf-item .txt{flex:1 1 auto;font-size:18px;color:#fff;word-break:break-word;}',
    '.nf-item.done .txt{text-decoration:line-through;opacity:.55;}',
    '.nf-item .typetag{font-size:14px;color:#fff;border:1px solid rgba(255,255,255,.3);',
    ' border-radius:999px;padding:2px 10px;opacity:.85;flex:0 0 auto;}',
    '.nf-item .del{background:none;border:none;color:#fff;opacity:.55;font-size:18px;cursor:pointer;padding:8px;}',
    '.nf-item .del:hover{opacity:1;color:#ff5e6c;}',
    '.nf-progress{font-size:14px;color:#fff;opacity:.75;margin:8px 2px;}',
    '.nf-lists .nf-status{font-size:14px;color:#fff;opacity:.85;margin:10px 2px 0;min-height:20px;}',
    '.nf-lists .nf-empty{font-size:14px;color:#fff;opacity:.6;padding:18px 4px;}',
    '.nf-listhead{display:flex;align-items:center;justify-content:space-between;gap:8px;margin-top:6px;}',
    '.nf-listhead .lname{font-size:18px;font-weight:700;color:#fff;margin:0;}',
    '.nf-consent{font-size:14px;color:#fff;opacity:.6;margin:10px 0 0;}'
  ].join('\n');
  document.head.appendChild(st);
}

NF.register(UNIT, {
  version: '1.0.0',
  activate: function(root, config){
    config = config || {};
    if (!root) return { destroy: function(){} };
    cssOnce();
    var key = config.storageKey || 'naya.smartlists.v1';
    var listeners = [];
    function on(el, ev, fn){ el.addEventListener(ev, fn); listeners.push([el, ev, fn]); }

    var lists = storeGet(key, null);
    if (!Array.isArray(lists)) {
      lists = Array.isArray(config.lists) ? JSON.parse(JSON.stringify(config.lists)) : [];
    }
    var activeId = lists.length ? lists[0].id : null;

    root.innerHTML = '';
    var wrap = document.createElement('div');
    wrap.className = 'nf-lists';
    var h = document.createElement('h3');
    h.textContent = config.title || 'Smart Lists';
    wrap.appendChild(h);
    var sub = document.createElement('p');
    sub.className = 'nf-sub';
    sub.textContent = 'Organize anything — notes, contacts, topics — and check them off as you go.';
    wrap.appendChild(sub);
    var pills = document.createElement('div');
    pills.className = 'nf-listpills';
    wrap.appendChild(pills);
    var listBody = document.createElement('div');
    wrap.appendChild(listBody);
    var status = document.createElement('p');
    status.className = 'nf-status';
    status.setAttribute('aria-live','polite');
    wrap.appendChild(status);
    var consent = document.createElement('p');
    consent.className = 'nf-consent';
    consent.textContent = 'Ready now: lists live on this device. Connect your account to sync them everywhere (connected is off).';
    wrap.appendChild(consent);
    root.appendChild(wrap);

    function say(msg){ status.textContent = msg; }
    function persist(){ storeSet(key, lists); }
    function active(){ for (var i = 0; i < lists.length; i++) if (lists[i].id === activeId) return lists[i]; return null; }

    function render(){
      pills.innerHTML = '';
      lists.forEach(function(l){
        var b = document.createElement('button');
        b.type = 'button';
        b.className = 'nf-listpill' + (l.id === activeId ? ' active' : '');
        var done = (l.items || []).filter(function(x){ return x.done; }).length;
        b.textContent = l.name + ' (' + done + '/' + (l.items || []).length + ')';
        on(b, 'click', function(){ activeId = l.id; render(); });
        pills.appendChild(b);
      });
      var np = document.createElement('button');
      np.type = 'button';
      np.className = 'nf-listpill';
      np.textContent = '＋ New list';
      on(np, 'click', openNewList);
      pills.appendChild(np);
      renderList();
    }

    function openNewList(){
      listBody.innerHTML = '';
      var row = document.createElement('div');
      row.className = 'nf-addrow';
      var inp = document.createElement('input');
      inp.placeholder = 'List name (e.g. Launch day)';
      inp.setAttribute('aria-label','New list name');
      var add = document.createElement('button');
      add.type = 'button'; add.className = 'nf-btn primary'; add.textContent = 'Create';
      var cancel = document.createElement('button');
      cancel.type = 'button'; cancel.className = 'nf-btn'; cancel.textContent = 'Cancel';
      on(add, 'click', function(){
        var name = inp.value.trim();
        if (!name) { say('Name the list first.'); inp.focus(); return; }
        var l = { id: uid('list'), name: name, items: [] };
        lists.push(l); activeId = l.id;
        persist(); render();
        say('List "' + name + '" created — add your first item.');
      });
      on(cancel, 'click', renderList);
      on(inp, 'keydown', function(e){ if (e.key === 'Enter') add.click(); });
      row.appendChild(inp); row.appendChild(add); row.appendChild(cancel);
      listBody.appendChild(row);
      setTimeout(function(){ inp.focus(); }, 50);
    }

    function renderList(){
      listBody.innerHTML = '';
      var l = active();
      if (!l) {
        var e = document.createElement('p'); e.className = 'nf-empty';
        e.textContent = 'No lists yet — tap ＋ New list to start one.';
        listBody.appendChild(e); return;
      }
      l.items = l.items || [];
      var head = document.createElement('div');
      head.className = 'nf-listhead';
      var nm = document.createElement('p'); nm.className = 'lname'; nm.textContent = l.name;
      var delList = document.createElement('button');
      delList.type = 'button'; delList.className = 'nf-btn danger'; delList.textContent = 'Delete list';
      on(delList, 'click', function(){
        lists = lists.filter(function(x){ return x.id !== l.id; });
        activeId = lists.length ? lists[0].id : null;
        persist(); render();
        say('List "' + l.name + '" deleted.');
      });
      head.appendChild(nm); head.appendChild(delList);
      listBody.appendChild(head);

      var addRow = document.createElement('div');
      addRow.className = 'nf-addrow';
      var inp = document.createElement('input');
      inp.placeholder = 'Add an item…';
      inp.setAttribute('aria-label','New item text');
      var typeSel = document.createElement('select');
      typeSel.setAttribute('aria-label','Item type');
      TYPES.forEach(function(t){
        var o = document.createElement('option'); o.value = t;
        o.textContent = t.charAt(0).toUpperCase() + t.slice(1);
        typeSel.appendChild(o);
      });
      var add = document.createElement('button');
      add.type = 'button'; add.className = 'nf-btn primary'; add.textContent = 'Add';
      on(add, 'click', function(){
        var text = inp.value.trim();
        if (!text) { say('Type the item first.'); inp.focus(); return; }
        l.items.push({ id: uid('item'), text: text, type: typeSel.value, done: false });
        persist(); renderList();
        say('Added to "' + l.name + '".');
      });
      on(inp, 'keydown', function(e){ if (e.key === 'Enter') add.click(); });
      addRow.appendChild(inp); addRow.appendChild(typeSel); addRow.appendChild(add);
      listBody.appendChild(addRow);

      var itemsBox = document.createElement('div');
      if (!l.items.length) {
        var ne = document.createElement('p'); ne.className = 'nf-empty';
        ne.textContent = 'Nothing here yet — add your first item above.';
        itemsBox.appendChild(ne);
      }
      l.items.forEach(function(it){
        var row = document.createElement('div');
        row.className = 'nf-item' + (it.done ? ' done' : '');
        var cb = document.createElement('input');
        cb.type = 'checkbox'; cb.checked = !!it.done;
        cb.setAttribute('aria-label', 'Check off: ' + it.text);
        on(cb, 'change', function(){
          it.done = cb.checked;
          persist(); renderList(); render();
          say(it.done ? 'Checked off.' : 'Unchecked — back on the list.');
        });
        var txt = document.createElement('span'); txt.className = 'txt'; txt.textContent = it.text;
        var tag = document.createElement('span'); tag.className = 'typetag'; tag.textContent = it.type || 'note';
        var del = document.createElement('button');
        del.type = 'button'; del.className = 'del'; del.textContent = '×';
        del.setAttribute('aria-label','Delete item: ' + it.text);
        on(del, 'click', function(){
          l.items = l.items.filter(function(x){ return x.id !== it.id; });
          persist(); renderList(); render();
          say('Item removed.');
        });
        row.appendChild(cb); row.appendChild(txt); row.appendChild(tag); row.appendChild(del);
        itemsBox.appendChild(row);
      });
      listBody.appendChild(itemsBox);
      var done = l.items.filter(function(x){ return x.done; }).length;
      var prog = document.createElement('p');
      prog.className = 'nf-progress';
      prog.textContent = done + ' of ' + l.items.length + ' done';
      listBody.appendChild(prog);
    }

    render();
    say(lists.length ? 'Pick a list, add items, check them off.' : 'Create your first list to begin.');

    return {
      destroy: function(){
        listeners.forEach(function(l){ try { l[0].removeEventListener(l[1], l[2]); } catch(e){} });
        root.innerHTML = '';
      }
    };
  }
});
})();
