/* NayaFunction: smart-mail v1.0.0
   What: Compose smart mail — drafts + outbox in localStorage, broadcast to a list.
   Activation: <div data-fn="smart-mail" data-fn-config='{...}'></div>
   Config: {
     recipients: [{name, email}]  address book shown in the To picker and broadcast list
     draftsKey: localStorage key for drafts (default 'naya.smartmail.drafts.v1')
     outboxKey: localStorage key for sent mail (default 'naya.smartmail.outbox.v1')
     title: heading text (default 'Smart Mail')
   } — all optional.
   Ready behavior: compose → send lands in the outbox, save-draft → drafts; drafts
     load back into the composer and delete; broadcast queues one copy per checked
     recipient. Everything works on this device with zero backend.
   Connected behavior: none — the `connected` key is reserved. Connecting a real mail
     account would make Send actually deliver; until then Send queues on this device.
   Backend twin: builder-review/HUB/design-system/tools/smart-builder/functions/feature_smart_mail.py
     (noted here only — this unit is fully client-side and never calls it).
   Consent line (ready vs connected never conflated): the copy states plainly that
     mail is queued on this device and that connecting an account is what sends.
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

var UNIT = 'smart-mail';
var UNIT_COLOR = '#3fb8ff'; /* Law 9 token — one color job per unit */

function esc(s){
  return String(s == null ? '' : s).replace(/[&<>"']/g, function(c){
    return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];
  });
}
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
function fmtTime(ts){
  try { return new Date(ts).toLocaleString(); } catch(e){ return ''; }
}
function uid(prefix){ return prefix + '-' + Date.now().toString(36) + '-' + Math.floor(Math.random()*1e6).toString(36); }
function cssOnce(){
  if (document.querySelector('style[data-nf-css="smart-mail"]')) return;
  var st = document.createElement('style');
  st.setAttribute('data-nf-css','smart-mail');
  st.textContent = [
    '.nf-mail{font-family:Inter,system-ui,sans-serif;color:#fff;background:#0a0a0d;',
    ' border:1px solid rgba(255,255,255,.14);border-radius:14px;padding:14px 16px;',
    ' box-shadow:0 10px 30px rgba(0,0,0,.55), inset 0 1px 0 rgba(255,255,255,.06);}',
    '.nf-mail h3{margin:0 0 4px;font-size:18px;font-weight:700;color:#fff;}',
    '.nf-mail .nf-sub{font-size:14px;color:#fff;opacity:.75;margin:0 0 12px;}',
    '.nf-mailtabs{display:flex;gap:8px;margin-bottom:12px;flex-wrap:wrap;}',
    '.nf-mailtab{background:#101014;color:#fff;border:1.5px solid rgba(255,255,255,.35);',
    ' border-radius:999px;padding:10px 16px;font-size:14px;min-height:44px;cursor:pointer;}',
    '.nf-mailtab:hover{border-color:' + UNIT_COLOR + ';}',
    '.nf-mailtab.active{border-color:' + UNIT_COLOR + ';box-shadow:0 0 16px -4px ' + UNIT_COLOR + ';}',
    '.nf-mail label{display:block;font-size:14px;color:#fff;margin:10px 0 4px;}',
    '.nf-mail input,.nf-mail select,.nf-mail textarea{width:100%;box-sizing:border-box;',
    ' background:#141419;color:#fff;border:1px solid rgba(255,255,255,.25);',
    ' border-radius:8px;padding:10px;font-size:14px;font-family:inherit;}',
    '.nf-mail textarea{min-height:110px;resize:vertical;}',
    '.nf-mail input:focus,.nf-mail select:focus,.nf-mail textarea:focus{outline:none;border-color:' + UNIT_COLOR + ';}',
    '.nf-mail .nf-rowbtns{display:flex;gap:8px;margin-top:12px;flex-wrap:wrap;}',
    '.nf-btn{background:#141419;color:#fff;border:1.5px solid rgba(255,255,255,.35);',
    ' border-radius:10px;padding:10px 14px;font-size:14px;min-height:44px;cursor:pointer;}',
    '.nf-btn:hover{border-color:' + UNIT_COLOR + ';box-shadow:0 0 14px -4px ' + UNIT_COLOR + ';}',
    '.nf-btn.danger:hover{border-color:#ff5e6c;box-shadow:0 0 14px -4px #ff5e6c;}',
    '.nf-mailitem{border:1px solid rgba(255,255,255,.14);border-radius:10px;padding:10px 12px;',
    ' margin:8px 0;background:#0d0d11;}',
    '.nf-mailitem .t{font-size:18px;font-weight:700;color:#fff;margin:0 0 2px;}',
    '.nf-mailitem .m{font-size:14px;color:#fff;opacity:.75;margin:0;}',
    '.nf-mailitem .b{font-size:14px;color:#fff;margin:6px 0;white-space:pre-wrap;word-break:break-word;}',
    '.nf-badge{display:inline-block;font-size:14px;color:#fff;border:1px solid ' + UNIT_COLOR + ';',
    ' border-radius:999px;padding:2px 10px;margin-left:8px;opacity:.9;}',
    '.nf-mail .nf-status{font-size:14px;color:#fff;opacity:.85;margin:10px 2px 0;min-height:20px;}',
    '.nf-mail .nf-empty{font-size:14px;color:#fff;opacity:.6;padding:18px 4px;}',
    '.nf-bc-row{display:flex;align-items:center;gap:10px;padding:10px 4px;',
    ' border-bottom:1px solid rgba(255,255,255,.1);}',
    '.nf-bc-row input{width:20px;height:20px;accent-color:' + UNIT_COLOR + ';}',
    '.nf-bc-row .n{font-size:18px;font-weight:700;color:#fff;}',
    '.nf-bc-row .e{font-size:14px;color:#fff;opacity:.7;}',
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
    var draftsKey = config.draftsKey || 'naya.smartmail.drafts.v1';
    var outboxKey = config.outboxKey || 'naya.smartmail.outbox.v1';
    var people = Array.isArray(config.recipients) ? config.recipients : [];
    var listeners = [];
    function on(el, ev, fn){ el.addEventListener(ev, fn); listeners.push([el, ev, fn]); }

    var view = 'compose';
    var drafts = storeGet(draftsKey, []);
    var outbox = storeGet(outboxKey, []);

    root.innerHTML = '';
    var wrap = document.createElement('div');
    wrap.className = 'nf-mail';
    var h = document.createElement('h3');
    h.textContent = config.title || 'Smart Mail';
    wrap.appendChild(h);
    var sub = document.createElement('p');
    sub.className = 'nf-sub';
    sub.textContent = 'Write it, send it, broadcast it — every word stays yours.';
    wrap.appendChild(sub);
    var tabsBar = document.createElement('div');
    tabsBar.className = 'nf-mailtabs';
    wrap.appendChild(tabsBar);
    var body = document.createElement('div');
    wrap.appendChild(body);
    var status = document.createElement('p');
    status.className = 'nf-status';
    status.setAttribute('aria-live','polite');
    wrap.appendChild(status);
    var consent = document.createElement('p');
    consent.className = 'nf-consent';
    consent.textContent = 'Ready now: compose, drafts and outbox work fully on this device. Connect a mail account to send for real — "connected" is off, so Send queues here instead of delivering.';
    wrap.appendChild(consent);
    root.appendChild(wrap);

    function say(msg){ status.textContent = msg; }
    function persist(){ storeSet(draftsKey, drafts); storeSet(outboxKey, outbox); }

    function renderTabs(){
      tabsBar.innerHTML = '';
      [['compose','Compose'],['drafts','Drafts (' + drafts.length + ')'],['outbox','Outbox (' + outbox.length + ')'],['broadcast','Broadcast']]
      .forEach(function(t){
        var b = document.createElement('button');
        b.type = 'button';
        b.className = 'nf-mailtab' + (view === t[0] ? ' active' : '');
        b.textContent = t[1];
        on(b, 'click', function(){ view = t[0]; render(); });
        tabsBar.appendChild(b);
      });
    }

    function render(){ renderTabs(); body.innerHTML = '';
      if (view === 'compose') renderCompose();
      else if (view === 'drafts') renderDrafts();
      else if (view === 'outbox') renderOutbox();
      else renderBroadcast();
    }

    var toSel, subjIn, bodyIn;
    function renderCompose(){
      var lb = document.createElement('label'); lb.textContent = 'To';
      toSel = document.createElement(people.length ? 'select' : 'input');
      if (people.length) {
        people.forEach(function(p){
          var o = document.createElement('option');
          o.value = p.name || p.email || '';
          o.textContent = (p.name || p.email || '') + (p.email ? ' <' + p.email + '>' : '');
          toSel.appendChild(o);
        });
      } else { toSel.placeholder = 'Name or address'; }
      body.appendChild(lb); body.appendChild(toSel);
      var ls = document.createElement('label'); ls.textContent = 'Subject';
      subjIn = document.createElement('input'); subjIn.placeholder = 'Subject';
      body.appendChild(ls); body.appendChild(subjIn);
      var lm = document.createElement('label'); lm.textContent = 'Message';
      bodyIn = document.createElement('textarea'); bodyIn.placeholder = 'Write your message…';
      body.appendChild(lm); body.appendChild(bodyIn);
      var row = document.createElement('div'); row.className = 'nf-rowbtns';
      var send = document.createElement('button'); send.type = 'button';
      send.className = 'nf-btn primary'; send.textContent = 'Send';
      on(send, 'click', function(){
        var to = (toSel.value || '').trim();
        var msg = bodyIn.value.trim();
        if (!to) { say('Pick or type a recipient first.'); return; }
        if (!msg) { say('Write the message before sending.'); bodyIn.focus(); return; }
        outbox.unshift({ id: uid('mail'), to: to, subject: subjIn.value.trim(), body: msg, ts: Date.now(), broadcast: false });
        persist();
        subjIn.value = ''; bodyIn.value = '';
        say('Queued to ' + to + ' — in your outbox on this device.');
        render();
      });
      var save = document.createElement('button'); save.type = 'button';
      save.className = 'nf-btn'; save.textContent = 'Save draft';
      on(save, 'click', function(){
        var to = (toSel.value || '').trim();
        var msg = bodyIn.value.trim();
        if (!to && !msg && !subjIn.value.trim()) { say('Nothing to save yet — write something first.'); return; }
        drafts.unshift({ id: uid('draft'), to: to, subject: subjIn.value.trim(), body: msg, ts: Date.now() });
        persist();
        say('Draft saved — find it under Drafts.');
        render();
      });
      row.appendChild(send); row.appendChild(save);
      body.appendChild(row);
    }

    function mailItem(m, actions){
      var d = document.createElement('div');
      d.className = 'nf-mailitem';
      var t = document.createElement('p'); t.className = 't';
      t.textContent = (m.subject || '(no subject)');
      if (m.broadcast) { var bd = document.createElement('span'); bd.className = 'nf-badge'; bd.textContent = 'broadcast'; t.appendChild(bd); }
      var meta = document.createElement('p'); meta.className = 'm';
      meta.textContent = 'To ' + (m.to || '—') + ' · ' + fmtTime(m.ts);
      var b = document.createElement('p'); b.className = 'b'; b.textContent = m.body || '';
      d.appendChild(t); d.appendChild(meta); d.appendChild(b);
      var row = document.createElement('div'); row.className = 'nf-rowbtns';
      actions.forEach(function(a){
        var btn = document.createElement('button'); btn.type = 'button';
        btn.className = 'nf-btn' + (a.danger ? ' danger' : '');
        btn.textContent = a.label;
        on(btn, 'click', function(){ a.fn(m); });
        row.appendChild(btn);
      });
      d.appendChild(row);
      return d;
    }

    function renderDrafts(){
      if (!drafts.length) { var e = document.createElement('p'); e.className = 'nf-empty'; e.textContent = 'No drafts yet — compose something and save it.'; body.appendChild(e); return; }
      drafts.forEach(function(m){
        body.appendChild(mailItem(m, [
          { label: 'Load', fn: function(d){
              view = 'compose'; render();
              toSel.value = d.to || '';
              subjIn.value = d.subject || '';
              bodyIn.value = d.body || '';
              say('Draft loaded into the composer.');
          }},
          { label: 'Delete', danger: true, fn: function(d){
              drafts = drafts.filter(function(x){ return x.id !== d.id; });
              persist(); render(); say('Draft deleted.');
          }}
        ]));
      });
    }

    function renderOutbox(){
      if (!outbox.length) { var e = document.createElement('p'); e.className = 'nf-empty'; e.textContent = 'Outbox is empty — sent mail queues here.'; body.appendChild(e); return; }
      outbox.forEach(function(m){
        body.appendChild(mailItem(m, [
          { label: 'Delete', danger: true, fn: function(d){
              outbox = outbox.filter(function(x){ return x.id !== d.id; });
              persist(); render(); say('Removed from outbox.');
          }}
        ]));
      });
    }

    function renderBroadcast(){
      if (!people.length) {
        var e = document.createElement('p'); e.className = 'nf-empty';
        e.textContent = 'No recipient list on this page yet — add recipients to the smart-mail config to broadcast.';
        body.appendChild(e); return;
      }
      var intro = document.createElement('p');
      intro.className = 'nf-sub';
      intro.textContent = 'One message, every checked person. Broadcasts queue on this device — they deliver when mail is connected.';
      body.appendChild(intro);
      var checks = [];
      people.forEach(function(p){
        var r = document.createElement('label');
        r.className = 'nf-bc-row';
        var c = document.createElement('input');
        c.type = 'checkbox'; c.checked = true; /* default-on per Shawn's 21:32Z rule */
        var nm = document.createElement('span'); nm.className = 'n'; nm.textContent = p.name || p.email || 'Someone';
        var em = document.createElement('span'); em.className = 'e'; em.textContent = p.email || '';
        r.appendChild(c); r.appendChild(nm); r.appendChild(em);
        body.appendChild(r);
        checks.push({ p: p, c: c });
      });
      var lm = document.createElement('label'); lm.textContent = 'Broadcast message';
      var ta = document.createElement('textarea'); ta.placeholder = 'Message for everyone checked…';
      body.appendChild(lm); body.appendChild(ta);
      var row = document.createElement('div'); row.className = 'nf-rowbtns';
      var go = document.createElement('button'); go.type = 'button';
      go.className = 'nf-btn primary'; go.textContent = 'Broadcast';
      on(go, 'click', function(){
        var msg = ta.value.trim();
        if (!msg) { say('Write the broadcast message first.'); ta.focus(); return; }
        var chosen = checks.filter(function(x){ return x.c.checked; });
        if (!chosen.length) { say('Check at least one recipient.'); return; }
        chosen.forEach(function(x){
          outbox.unshift({ id: uid('mail'), to: x.p.name || x.p.email, subject: '(broadcast)', body: msg, ts: Date.now(), broadcast: true });
        });
        persist(); ta.value = '';
        say('Broadcast queued to ' + chosen.length + ' ' + (chosen.length === 1 ? 'person' : 'people') + ' — in your outbox on this device.');
        render();
      });
      row.appendChild(go);
      body.appendChild(row);
    }

    render();
    say('Compose to begin — everything stays on this device until mail is connected.');

    return {
      destroy: function(){
        listeners.forEach(function(l){ try { l[0].removeEventListener(l[1], l[2]); } catch(e){} });
        root.innerHTML = '';
      }
    };
  }
});
})();
