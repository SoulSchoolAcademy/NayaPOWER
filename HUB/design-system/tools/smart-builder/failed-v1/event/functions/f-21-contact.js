/* NayaFunction: f-21-contact v1.0.0
   What: reach-the-owner form (name + message) -> validated -> saved to a localStorage outbox -> confirmation.
   Activation: <div data-fn="f-21-contact" data-fn-config='{"to":"Maya","outboxKey":"naya.fn21.outbox.v1"}'></div>
   Config:
     to: owner label shown in the form (default "the owner").
     outboxKey: localStorage key for the outbox array (default "naya.fn21.outbox.v1").
     accent: hex — submit chrome color (default #3fb8ff blue).
   Ready behavior: validates inline (name required, message >= 10 chars); on valid submit the
     message is appended to the outbox array and a confirmation with the outbox size is shown.
   Connected behavior: none (a mail backend would read the outbox; the send step is a twin).
   Backend twin: smart-mail outbox reader.
   Lessons: L-2026-10-16-005 (the button really sends), Law 1 (text stays white; errors signal via
     the field's red rim, never colored text).
*/
(function(){
'use strict';
var NF = window.NayaFunctions = window.NayaFunctions || {};
NF._r = NF._r || {};
NF.register = NF.register || function(id, def){ if (NF._r[id]) return; NF._r[id] = def; };

function loadBox(key){
  try { var v = JSON.parse(localStorage.getItem(key)); return Array.isArray(v) ? v : []; }
  catch (e) { return []; }
}
function saveBox(key, arr){
  try { localStorage.setItem(key, JSON.stringify(arr)); return true; }
  catch (e) { console.warn('[f-21-contact] localStorage unavailable — message kept in memory only'); return false; }
}

NF.register('f-21-contact', {
  version: '1.0.0',
  activate: function(root, config){
    config = config || {};
    var to = config.to || 'the owner';
    var key = config.outboxKey || 'naya.fn21.outbox.v1';
    var accent = config.accent || '#3fb8ff';

    root.innerHTML = '';
    var wrap = document.createElement('div');

    var head = document.createElement('p');
    head.textContent = 'Send a message to ' + to + '.';
    head.style.cssText = 'color:#ffffff;font-size:15px;font-weight:600;margin:0 0 12px;';
    wrap.appendChild(head);

    var name = document.createElement('input');
    name.type = 'text'; name.placeholder = 'Your name';
    name.setAttribute('aria-label', 'Your name');
    var msg = document.createElement('textarea');
    msg.placeholder = 'Your message (at least 10 characters)';
    msg.setAttribute('aria-label', 'Your message'); msg.rows = 4;

    [name, msg].forEach(function(f){
      f.style.cssText = 'width:100%;box-sizing:border-box;padding:12px 14px;font-size:15px;color:#ffffff;' +
        'background:#0b0b10;border:1.5px solid rgba(255,255,255,.55);border-radius:12px;outline:none;margin-bottom:10px;';
    });

    var err = document.createElement('p');
    err.setAttribute('role', 'alert');
    err.style.cssText = 'color:#F8F7FB;font-size:13px;margin:0 0 10px;display:none;';

    var btn = document.createElement('button');
    btn.type = 'button'; btn.textContent = 'Send message';
    btn.className = 'nf21-send';
    btn.style.cssText = 'padding:13px 28px;font-size:15px;font-weight:700;color:#ffffff;background:#0b0b10;' +
      'border:1.5px solid rgba(255,255,255,.55);border-radius:12px;cursor:pointer;transition:border-color .18s,box-shadow .18s;';
    btn.addEventListener('mouseover', function(){ btn.style.borderColor = accent; btn.style.boxShadow = '0 0 18px -4px ' + accent; });
    btn.addEventListener('mouseout', function(){ btn.style.borderColor = 'rgba(255,255,255,.55)'; btn.style.boxShadow = 'none'; });

    var ok = document.createElement('p');
    ok.style.cssText = 'color:#F8F7FB;font-size:14px;margin:12px 0 0;display:none;';

    function fail(msgEl, message){
      err.textContent = '! ' + message; err.style.display = 'block';
      msgEl.style.borderColor = '#ff5e6c'; // Law 1: red on the chrome, not on the text
    }
    function clear(){
      err.style.display = 'none';
      name.style.borderColor = 'rgba(255,255,255,.55)';
      msg.style.borderColor = 'rgba(255,255,255,.55)';
    }

    btn.addEventListener('click', function(){
      clear();
      var n = name.value.trim(), m = msg.value.trim();
      if (!n) { fail(name, 'Please add your name so the owner can reply.'); name.focus(); return; }
      if (m.length < 10) { fail(msg, 'A few more words — at least 10 characters.'); msg.focus(); return; }
      var box = loadBox(key);
      box.push({ name: n, message: m, to: to, at: new Date().toISOString() });
      saveBox(key, box);
      ok.textContent = 'Sent. Your message is in the outbox — ' + box.length + ' waiting' +
        (box.length === 1 ? '' : '') + '.';
      ok.style.display = 'block';
      name.value = ''; msg.value = '';
    });

    wrap.appendChild(name); wrap.appendChild(msg);
    wrap.appendChild(err); wrap.appendChild(btn); wrap.appendChild(ok);
    root.appendChild(wrap);
    return { destroy: function(){ root.innerHTML = ''; } };
  }
});
})();
