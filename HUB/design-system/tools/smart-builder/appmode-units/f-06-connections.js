/* NayaFunction: connections v1.0.0
   What: Your people — a searchable list with real reach actions.
   Activation: <div data-fn="connections" data-fn-config='{...}'></div>
   Config: {
     people: [{id, name, role, color, phone, note}]  your people
     storageKey: localStorage key for sent messages (default 'naya.connections.messages.v1')
     title: heading text (default 'Connections')
   } — all optional.
   Ready behavior: search filters the list live; Message opens an inline composer and
     stores the sent note on this device; Details expands the person's note; Call
     appears only when the person has a real phone number (a genuine tel: link).
     Nothing decorative pretends to reach someone it cannot.
   Connected behavior: none — the `connected` key is reserved. Connecting accounts
     would deliver messages for real; until then they are stored on this device.
   Backend twin: builder-review/HUB/design-system/tools/smart-builder/functions/feature_community.py
     (noted here only — this unit is fully client-side and never calls it).
   Consent line: copy states the people list lives on this device and messages are
     stored locally until accounts are connected — ready vs connected never conflated.
   Lesson L-2026-10-17-004: every control below is bound to DOM this unit creates.
   Lesson L-2026-10-17-002: the Call link is rendered only for a real number —
     no dead reach actions.
*/
(function(){
'use strict';
var NF = window.NayaFunctions = window.NayaFunctions || {};
NF._r = NF._r || {};
NF.register = NF.register || function(id, def){
  if (NF._r[id]) return;
  NF._r[id] = def;
};

var UNIT = 'connections';
var UNIT_COLOR = '#40d3bb'; /* Law 9 token — one color job per unit */

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
  if (document.querySelector('style[data-nf-css="connections"]')) return;
  var st = document.createElement('style');
  st.setAttribute('data-nf-css','connections');
  st.textContent = [
    '.nf-conn{font-family:Inter,system-ui,sans-serif;color:#fff;background:#0a0a0d;',
    ' border:1px solid rgba(255,255,255,.14);border-radius:14px;padding:14px 16px;',
    ' box-shadow:0 10px 30px rgba(0,0,0,.55), inset 0 1px 0 rgba(255,255,255,.06);}',
    '.nf-conn h3{margin:0 0 4px;font-size:18px;font-weight:700;color:#fff;}',
    '.nf-conn .nf-sub{font-size:14px;color:#fff;opacity:.75;margin:0 0 12px;}',
    '.nf-search{width:100%;box-sizing:border-box;background:#141419;color:#fff;',
    ' border:1px solid rgba(255,255,255,.25);border-radius:8px;padding:10px;font-size:14px;',
    ' font-family:inherit;margin-bottom:8px;}',
    '.nf-search:focus{outline:none;border-color:' + UNIT_COLOR + ';}',
    '.nf-person{border:1px solid rgba(255,255,255,.14);border-radius:10px;padding:12px 14px;',
    ' margin:10px 0;background:#0d0d11;}',
    '.nf-person .prow{display:flex;align-items:center;gap:12px;}',
    '.nf-avatar{width:44px;height:44px;border-radius:50%;background:var(--pc);flex:0 0 auto;',
    ' display:flex;align-items:center;justify-content:center;font-size:18px;font-weight:700;',
    ' color:#fff;box-shadow:0 0 14px -4px var(--pc);}',
    '.nf-person .pn{font-size:18px;font-weight:700;color:#fff;margin:0;}',
    '.nf-person .pr{font-size:14px;color:#fff;opacity:.7;margin:0;}',
    '.nf-actions{display:flex;gap:8px;margin-top:10px;flex-wrap:wrap;}',
    '.nf-btn{background:#141419;color:#fff;border:1.5px solid rgba(255,255,255,.35);',
    ' border-radius:10px;padding:10px 14px;font-size:14px;min-height:44px;cursor:pointer;',
    ' text-decoration:none;display:inline-block;}',
    '.nf-btn:hover{border-color:' + UNIT_COLOR + ';box-shadow:0 0 14px -4px ' + UNIT_COLOR + ';}',
    '.nf-btn.primary{border-color:' + UNIT_COLOR + ';}',
    '.nf-msgbox{display:none;margin-top:10px;}',
    '.nf-msgbox.open{display:block;}',
    '.nf-msgbox textarea{width:100%;box-sizing:border-box;background:#141419;color:#fff;',
    ' border:1px solid rgba(255,255,255,.25);border-radius:8px;padding:10px;font-size:14px;',
    ' min-height:70px;font-family:inherit;resize:vertical;}',
    '.nf-msgbox textarea:focus{outline:none;border-color:' + UNIT_COLOR + ';}',
    '.nf-note{font-size:14px;color:#fff;opacity:.9;margin:8px 0 0;display:none;}',
    '.nf-note.open{display:block;}',
    '.nf-conn .nf-status{font-size:14px;color:#fff;opacity:.85;margin:10px 2px 0;min-height:20px;}',
    '.nf-conn .nf-empty{font-size:14px;color:#fff;opacity:.6;padding:18px 4px;}',
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
    var key = config.storageKey || 'naya.connections.messages.v1';
    var people = Array.isArray(config.people) ? config.people : [];
    var listeners = [];
    function on(el, ev, fn){ el.addEventListener(ev, fn); listeners.push([el, ev, fn]); }

    var query = '';
    root.innerHTML = '';
    var wrap = document.createElement('div');
    wrap.className = 'nf-conn';
    var h = document.createElement('h3');
    h.textContent = config.title || 'Connections';
    wrap.appendChild(h);
    var sub = document.createElement('p');
    sub.className = 'nf-sub';
    sub.textContent = 'Your people — find them fast, reach them for real.';
    wrap.appendChild(sub);
    var search = document.createElement('input');
    search.className = 'nf-search';
    search.placeholder = 'Search people…';
    search.setAttribute('aria-label','Search people');
    wrap.appendChild(search);
    var listBox = document.createElement('div');
    wrap.appendChild(listBox);
    var status = document.createElement('p');
    status.className = 'nf-status';
    status.setAttribute('aria-live','polite');
    wrap.appendChild(status);
    var consent = document.createElement('p');
    consent.className = 'nf-consent';
    consent.textContent = 'Ready now: your people list lives on this device, and messages you send are stored here. Connect your accounts to reach people for real (connected is off).';
    wrap.appendChild(consent);
    root.appendChild(wrap);

    function say(msg){ status.textContent = msg; }

    on(search, 'input', function(){ query = search.value.trim().toLowerCase(); render(); });

    function initial(name){
      name = (name || '?').trim();
      return name.charAt(0).toUpperCase();
    }

    function personCard(p){
      var card = document.createElement('div');
      card.className = 'nf-person';
      var prow = document.createElement('div'); prow.className = 'prow';
      var av = document.createElement('div'); av.className = 'nf-avatar';
      av.style.setProperty('--pc', p.color || UNIT_COLOR);
      av.textContent = initial(p.name);
      var who = document.createElement('div');
      var pn = document.createElement('p'); pn.className = 'pn'; pn.textContent = p.name || 'Someone';
      var pr = document.createElement('p'); pr.className = 'pr'; pr.textContent = p.role || '';
      who.appendChild(pn); who.appendChild(pr);
      prow.appendChild(av); prow.appendChild(who);
      card.appendChild(prow);

      var note = document.createElement('p'); note.className = 'nf-note';
      note.textContent = p.note || 'No notes yet.';
      card.appendChild(note);

      var msgbox = document.createElement('div'); msgbox.className = 'nf-msgbox';
      var ta = document.createElement('textarea');
      ta.placeholder = 'Message to ' + (p.name || 'them') + '…';
      ta.setAttribute('aria-label','Message to ' + (p.name || 'them'));
      var sendRow = document.createElement('div'); sendRow.className = 'nf-actions';
      var sendBtn = document.createElement('button');
      sendBtn.type = 'button'; sendBtn.className = 'nf-btn primary'; sendBtn.textContent = 'Send message';
      on(sendBtn, 'click', function(){
        var text = ta.value.trim();
        if (!text) { say('Write the message first.'); ta.focus(); return; }
        var msgs = storeGet(key, []);
        msgs.unshift({ id: uid('msg'), to: p.name || '', text: text, ts: Date.now() });
        storeSet(key, msgs);
        ta.value = '';
        msgbox.classList.remove('open');
        say('Message to ' + (p.name || 'them') + ' saved on this device.');
      });
      var cancelBtn = document.createElement('button');
      cancelBtn.type = 'button'; cancelBtn.className = 'nf-btn'; cancelBtn.textContent = 'Cancel';
      on(cancelBtn, 'click', function(){ msgbox.classList.remove('open'); });
      sendRow.appendChild(sendBtn); sendRow.appendChild(cancelBtn);
      msgbox.appendChild(ta); msgbox.appendChild(sendRow);
      card.appendChild(msgbox);

      var actions = document.createElement('div'); actions.className = 'nf-actions';
      var msgBtn = document.createElement('button');
      msgBtn.type = 'button'; msgBtn.className = 'nf-btn'; msgBtn.textContent = '✉ Message';
      on(msgBtn, 'click', function(){
        var open = msgbox.classList.toggle('open');
        if (open) setTimeout(function(){ ta.focus(); }, 50);
      });
      actions.appendChild(msgBtn);
      var detBtn = document.createElement('button');
      detBtn.type = 'button'; detBtn.className = 'nf-btn'; detBtn.textContent = 'Details';
      on(detBtn, 'click', function(){
        var open = note.classList.toggle('open');
        detBtn.textContent = open ? 'Hide' : 'Details';
      });
      actions.appendChild(detBtn);
      if (p.phone) { /* L-2026-10-17-002: real number or no call action at all */
        var call = document.createElement('a');
        call.className = 'nf-btn';
        call.href = 'tel:' + String(p.phone).replace(/[^+\d]/g, '');
        call.textContent = '📞 Call';
        actions.appendChild(call);
      }
      card.appendChild(actions);
      return card;
    }

    function render(){
      listBox.innerHTML = '';
      var shown = people.filter(function(p){
        if (!query) return true;
        var hay = ((p.name || '') + ' ' + (p.role || '')).toLowerCase();
        return hay.indexOf(query) >= 0;
      });
      if (!people.length) {
        var e = document.createElement('p'); e.className = 'nf-empty';
        e.textContent = 'No people on this page yet — add them to the connections config.';
        listBox.appendChild(e); return;
      }
      if (!shown.length) {
        var n = document.createElement('p'); n.className = 'nf-empty';
        n.textContent = 'No one matches "' + search.value.trim() + '".';
        listBox.appendChild(n); return;
      }
      shown.forEach(function(p){ listBox.appendChild(personCard(p)); });
    }

    render();
    say(people.length ? 'Search to filter, Message to reach out.' : 'Add people to the connections config to begin.');

    return {
      destroy: function(){
        listeners.forEach(function(l){ try { l[0].removeEventListener(l[1], l[2]); } catch(e){} });
        root.innerHTML = '';
      }
    };
  }
});
})();
