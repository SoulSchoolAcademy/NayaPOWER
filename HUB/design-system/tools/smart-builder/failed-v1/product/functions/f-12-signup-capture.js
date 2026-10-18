/* NayaFunction: f-12-signup-capture v1.0.0
   What: join/subscribe form — validates fields, captures to localStorage,
     shows a real success state
   Activation: <div data-fn="f-12-signup-capture" data-fn-config='{...}'></div>
   Config: {
     title: string,               // board heading (default "Join us")
     subtitle: string,           // one-line pitch under the heading
     button_text: string,        // submit label (default "Join")
     success_title: string,      // success heading (default "You're in!")
     success_message: string,    // success line — {name} is replaced with the sign-up's name
     fields: [ {                 // * REQUIRED — non-empty
       name: string,             // * form field key
       label: string,            // * visible label
       type: string,             // text | email | tel (default text)
       required: boolean,        // default false
       placeholder: string
     } ],
     storage_key: string         // localStorage key (default "naya_fn_f12_signup")
   }
   Ready behavior: full capture flow client-side — per-field inline validation
     (required + email format), sign-ups persisted to localStorage as an array,
     live "N already joined" count restored on reload. No backend needed.
   Connected behavior: none (reserved key `connected`).
   Backend twin: none.
*/
(function(){
'use strict';
var NF = window.NayaFunctions = window.NayaFunctions || {};
NF._r = NF._r || {};
NF.register = NF.register || function(id, def){ if (!NF._r[id]) NF._r[id] = def; };

var CSS = [
'.nf-f12{--nf-accent:#a06bff;--obs:#0b0d14;--raise:#121623;--white:#ffffff;--silver:#c9c9d4;--slate:#8a8a99;--line:rgba(255,255,255,.12);',
'font-family:Inter,ui-sans-serif,system-ui,sans-serif;color:var(--silver);font-size:15px;line-height:1.5}',
'.nf-f12 *{box-sizing:border-box}',
'.nf-f12 .nf-board{background:linear-gradient(180deg,var(--raise),var(--obs));border:1px solid var(--line);border-radius:20px;',
'padding:26px 22px;box-shadow:0 18px 44px rgba(0,0,0,.5),inset 0 1px 0 rgba(255,255,255,.06);position:relative;overflow:hidden}',
'.nf-f12 .nf-rail{position:absolute;left:0;top:0;bottom:0;width:5px;background:var(--nf-accent);box-shadow:0 0 14px var(--nf-accent)}',
'.nf-f12 .nf-kicker{font-size:11px;letter-spacing:.22em;text-transform:uppercase;font-weight:700;color:#ffffff;margin-bottom:10px}',
'.nf-f12 h3{color:#ffffff;font-size:22px;margin:0 0 6px;font-weight:600}',
'.nf-f12 .nf-sub{color:var(--silver);font-size:14px;margin:0 0 18px}',
'.nf-f12 .nf-field{margin-bottom:14px}',
'.nf-f12 .nf-field label{display:block;font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--silver);margin-bottom:8px;font-weight:600}',
'.nf-f12 .nf-field input{width:100%;background:#0a0a0f;border:1.5px solid rgba(255,255,255,.35);border-radius:12px;',
'color:#ffffff;font-size:16px;padding:12px 14px;outline:none;transition:border-color .18s,box-shadow .18s}',
'.nf-f12 .nf-field input:focus{border-color:var(--nf-accent);box-shadow:0 0 0 1px var(--nf-accent),0 0 14px rgba(160,107,255,.35)}',
'.nf-f12 .nf-field input.bad{border-color:#ff5e6c;box-shadow:0 0 0 1px #ff5e6c}',
'.nf-f12 .nf-ferr{display:none;margin-top:6px;color:#ffffff;font-size:13px;padding-left:10px;border-left:3px solid #ff5e6c}',
'.nf-f12 .nf-ferr.show{display:block}',
'.nf-f12 .nf-btn{display:block;width:100%;margin-top:6px;background:#0a0a0f;border:2px solid #ffffff;color:#ffffff;',
'border-radius:999px;padding:14px 18px;font-size:16px;font-weight:700;cursor:pointer;letter-spacing:.04em;',
'transition:border-color .18s,box-shadow .18s,transform .12s;box-shadow:0 8px 22px rgba(0,0,0,.45),inset 0 1px 0 rgba(255,255,255,.08)}',
'.nf-f12 .nf-btn:hover{border-color:var(--nf-accent);box-shadow:0 0 22px rgba(160,107,255,.5),inset 0 1px 0 rgba(255,255,255,.08);transform:translateY(-1px)}',
'.nf-f12 .nf-btn:active{transform:translateY(1px)}',
'.nf-f12 .nf-count{margin-top:14px;font-size:13px;color:var(--slate);text-align:center}',
'.nf-f12 .nf-count b{color:#ffffff;font-weight:700}',
'.nf-f12 .nf-done{text-align:center;padding:10px 4px}',
'.nf-f12 .nf-check{width:64px;height:64px;border-radius:50%;margin:0 auto 14px;border:2px solid #2fe89e;',
'display:flex;align-items:center;justify-content:center;font-size:30px;color:#ffffff;box-shadow:0 0 24px rgba(47,232,158,.5);background:#0a0a0f}',
'.nf-f12 .nf-detail{color:var(--silver);font-size:14px;margin:6px 0}',
'.nf-f12 .nf-detail b{color:#ffffff;font-weight:600}',
'.nf-f12 .nf-ghost{background:transparent;border:1.5px solid rgba(255,255,255,.35);color:#ffffff;border-radius:999px;',
'padding:10px 20px;font-size:14px;font-weight:600;cursor:pointer;margin-top:14px;transition:border-color .18s,box-shadow .18s}',
'.nf-f12 .nf-ghost:hover{border-color:var(--nf-accent);box-shadow:0 0 12px rgba(160,107,255,.35)}',
'.nf-f12 .nf-failsoft{padding:18px;border-radius:14px;border:1px dashed rgba(255,255,255,.3);color:#ffffff;font-size:14px}'
].join('');

var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
function escapeHtml(s){
  return String(s == null ? '' : s).replace(/[&<>"']/g, function(c){
    return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
  });
}
function load(key){ try { var v = localStorage.getItem(key); return v ? JSON.parse(v) : []; } catch (e) { return []; } }
function save(key, v){ try { localStorage.setItem(key, JSON.stringify(v)); } catch (e) {} }

NF.register('f-12-signup-capture', {
  version: '1.0.0',
  activate: function(root, config){
    config = config || {};
    root.classList.add('nf-f12');
    var st = document.createElement('style');
    st.textContent = CSS;
    root.appendChild(st);

    var key = config.storage_key || 'naya_fn_f12_signup';
    var fields = [];
    if (Array.isArray(config.fields)) {
      for (var i = 0; i < config.fields.length; i++) {
        var f = config.fields[i] || {};
        if (typeof f.name === 'string' && f.name && typeof f.label === 'string' && f.label) {
          var t = (typeof f.type === 'string' && /^(text|email|tel)$/.test(f.type)) ? f.type : 'text';
          fields.push({ name: f.name, label: f.label, type: t, required: !!f.required, placeholder: typeof f.placeholder === 'string' ? f.placeholder : '' });
        }
      }
    }
    var listeners = [];
    function on(el, ev, fn){ el.addEventListener(ev, fn); listeners.push([el, ev, fn]); }

    // Fail soft: a form with no fields is a lie — say so honestly.
    if (!fields.length) {
      root.insertAdjacentHTML('beforeend',
        '<div class="nf-board"><div class="nf-rail"></div><div class="nf-failsoft">This sign-up form has no fields configured — the page owner still needs to set it up.</div></div>');
      return { destroy: function(){} };
    }

    function render(){
      root.innerHTML = '';
      root.appendChild(st);
      var b = document.createElement('div');
      b.className = 'nf-board';
      var form = fields.map(function(f){
        var inputType = f.type === 'tel' ? 'tel' : (f.type === 'email' ? 'email' : 'text');
        return '<div class="nf-field"><label for="nf12-' + escapeHtml(f.name) + '">' + escapeHtml(f.label) +
          (f.required ? ' · required' : '') + '</label>' +
          '<input id="nf12-' + escapeHtml(f.name) + '" type="' + inputType + '" data-f="' + escapeHtml(f.name) + '"' +
          (f.placeholder ? ' placeholder="' + escapeHtml(f.placeholder) + '"' : '') +
          ' maxlength="200" autocomplete="' + (f.type === 'email' ? 'email' : (f.type === 'tel' ? 'tel' : 'off')) + '">' +
          '<div class="nf-ferr" data-e="' + escapeHtml(f.name) + '"></div></div>';
      }).join('');
      b.innerHTML =
        '<div class="nf-rail"></div>' +
        '<div class="nf-kicker">Sign up</div>' +
        '<h3>' + escapeHtml(config.title || 'Join us') + '</h3>' +
        '<p class="nf-sub">' + escapeHtml(config.subtitle || 'Leave your details — you are in from the moment you tap the button.') + '</p>' +
        '<form data-frm="signup" novalidate>' + form +
        '<button class="nf-btn" type="submit">' + escapeHtml(config.button_text || 'Join') + '</button></form>' +
        '<p class="nf-count" data-r="count"></p>';
      root.appendChild(b);
      paintCount();

      function paintCount(){
        var n = load(key).length;
        b.querySelector('[data-r="count"]').innerHTML = n
          ? '<b>' + n + '</b> ' + (n === 1 ? 'person has' : 'people have') + ' already joined on this device'
          : 'Be the first to join on this device';
      }
      function fieldErr(name, msg){
        var inp = b.querySelector('[data-f="' + name + '"]');
        var e = b.querySelector('[data-e="' + name + '"]');
        if (msg) { inp.classList.add('bad'); e.textContent = msg; e.classList.add('show'); }
        else { inp.classList.remove('bad'); e.textContent = ''; e.classList.remove('show'); }
      }

      on(b.querySelector('[data-frm="signup"]'), 'submit', function(ev){
        ev.preventDefault();
        var record = {};
        var ok = true;
        var firstName = '';
        for (var i = 0; i < fields.length; i++) {
          var f = fields[i];
          var inp = b.querySelector('[data-f="' + f.name + '"]');
          var val = (inp.value || '').trim();
          fieldErr(f.name, '');
          if (f.required && !val) { fieldErr(f.name, 'This one is required — fill it in.'); ok = false; }
          else if (val && f.type === 'email' && !EMAIL_RE.test(val)) { fieldErr(f.name, 'That email does not look right — check it.'); ok = false; }
          record[f.name] = val;
          if (/name/i.test(f.name) && val && !firstName) firstName = val;
        }
        if (!ok) return;
        record.at = Date.now();
        var all = load(key); all.push(record); save(key, all);
        renderDone(firstName || 'friend');
      });

      function renderDone(name){
        root.innerHTML = '';
        root.appendChild(st);
        var b2 = document.createElement('div');
        b2.className = 'nf-board';
        var msg = (config.success_message || 'Welcome aboard, {name} — you are officially in.')
          .replace(/\{name\}/g, escapeHtml(name));
        b2.innerHTML =
          '<div class="nf-rail"></div><div class="nf-done">' +
          '<div class="nf-check">✓</div>' +
          '<div class="nf-kicker">' + escapeHtml(config.success_title || "You're in!") + '</div>' +
          '<p class="nf-detail">' + msg + '</p>' +
          '<p class="nf-detail">Your details are saved on this device — nothing was sent anywhere.</p>' +
          '<button class="nf-ghost" data-act="again">Sign up another</button>' +
          '</div>';
        root.appendChild(b2);
        on(b2.querySelector('[data-act="again"]'), 'click', render);
      }
    }

    render();
    return { destroy: function(){
      for (var i = 0; i < listeners.length; i++) {
        try { listeners[i][0].removeEventListener(listeners[i][1], listeners[i][2]); } catch (e) {}
      }
      listeners = [];
      try { root.classList.remove('nf-f12'); } catch (e) {}
    } };
  }
});
})();
