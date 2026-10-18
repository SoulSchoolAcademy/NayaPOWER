/* NayaFunction: f-09-booking v1.0.0
   What: appointment booking — pick a day, pick a slot, enter a name, get a confirmed reference
   Activation: <div data-fn="f-09-booking" data-fn-config='{...}'></div>
   Config: {
     title: string,              // board heading (default "Book an appointment")
     service_name: string,       // what is being booked (default "Appointment")
     days: string[] | {date,label}[],  // * REQUIRED — ISO dates "2026-10-19" or {date,label} pairs
     slots: string[],            // * REQUIRED — time slots, e.g. ["09:00","10:30"]
     duration_min: number,       // shown on the confirmation (default 30)
     note: string,               // small line under the board
     storage_key: string         // localStorage key (default "naya_fn_f09_booking")
   }
   Ready behavior: full flow client-side — day/slot/name selection, deterministic
     reference (BK-XXXXXX), booking persisted to localStorage; latest booking
     restored on reload. No backend needed.
   Connected behavior: none (reserved key `connected`).
   Backend twin: none.
*/
(function(){
'use strict';
var NF = window.NayaFunctions = window.NayaFunctions || {};
NF._r = NF._r || {};
NF.register = NF.register || function(id, def){ if (!NF._r[id]) NF._r[id] = def; };

var CSS = [
'.nf-f09{--nf-accent:#3fb8ff;--obs:#0b0d14;--raise:#121623;--white:#ffffff;--silver:#c9c9d4;--slate:#8a8a99;--line:rgba(255,255,255,.12);',
'font-family:Inter,ui-sans-serif,system-ui,sans-serif;color:var(--silver);font-size:15px;line-height:1.5}',
'.nf-f09 *{box-sizing:border-box}',
'.nf-f09 .nf-board{background:linear-gradient(180deg,var(--raise),var(--obs));border:1px solid var(--line);border-radius:20px;',
'padding:26px 22px;box-shadow:0 18px 44px rgba(0,0,0,.5),inset 0 1px 0 rgba(255,255,255,.06);position:relative;overflow:hidden}',
'.nf-f09 .nf-rail{position:absolute;left:0;top:0;bottom:0;width:5px;background:var(--nf-accent);box-shadow:0 0 14px var(--nf-accent)}',
'.nf-f09 .nf-kicker{font-size:11px;letter-spacing:.22em;text-transform:uppercase;font-weight:700;color:#ffffff;margin-bottom:10px}',
'.nf-f09 h3{color:#ffffff;font-size:22px;margin:0 0 6px;font-weight:600}',
'.nf-f09 .nf-sub{color:var(--silver);font-size:14px;margin:0 0 18px}',
'.nf-f09 .nf-step{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:#ffffff;opacity:.85;margin:18px 0 10px;font-weight:700}',
'.nf-f09 .nf-days{display:flex;gap:10px;flex-wrap:wrap}',
'.nf-f09 .nf-day{flex:1 1 0;min-width:104px;background:#0a0a0f;border:1.5px solid rgba(255,255,255,.55);color:#ffffff;',
'border-radius:14px;padding:10px 6px;cursor:pointer;text-align:center;transition:border-color .18s,box-shadow .18s,transform .12s;box-shadow:0 6px 16px rgba(0,0,0,.4)}',
'.nf-f09 .nf-day:hover{transform:translateY(-2px);border-color:#ffffff}',
'.nf-f09 .nf-day .nf-dow{display:block;font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--silver)}',
'.nf-f09 .nf-day .nf-dnum{display:block;font-size:20px;font-weight:700;color:#ffffff}',
'.nf-f09 .nf-day.is-sel{border-color:var(--nf-accent);box-shadow:0 0 0 1px var(--nf-accent),0 0 18px rgba(63,184,255,.45)}',
'.nf-f09 .nf-slots{display:grid;grid-template-columns:repeat(auto-fill,minmax(88px,1fr));gap:10px}',
'.nf-f09 .nf-slot{background:#0a0a0f;border:1.5px solid rgba(255,255,255,.55);color:#ffffff;border-radius:12px;padding:10px 4px;',
'cursor:pointer;font-size:14px;font-weight:600;transition:border-color .18s,box-shadow .18s;box-shadow:0 6px 16px rgba(0,0,0,.4)}',
'.nf-f09 .nf-slot:hover{border-color:#ffffff}',
'.nf-f09 .nf-slot.is-sel{border-color:var(--nf-accent);box-shadow:0 0 0 1px var(--nf-accent),0 0 16px rgba(63,184,255,.45)}',
'.nf-f09 .nf-field{margin-top:6px}',
'.nf-f09 .nf-field label{display:block;font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--silver);margin-bottom:8px;font-weight:600}',
'.nf-f09 .nf-field input{width:100%;background:#0a0a0f;border:1.5px solid rgba(255,255,255,.35);border-radius:12px;',
'color:#ffffff;font-size:16px;padding:12px 14px;outline:none;transition:border-color .18s,box-shadow .18s}',
'.nf-f09 .nf-field input:focus{border-color:var(--nf-accent);box-shadow:0 0 0 1px var(--nf-accent),0 0 14px rgba(63,184,255,.35)}',
'.nf-f09 .nf-err{display:none;margin-top:10px;padding:10px 14px;border-radius:12px;background:rgba(255,94,108,.08);',
'border-left:4px solid #ff5e6c;color:#ffffff;font-size:14px}',
'.nf-f09 .nf-err.show{display:block}',
'.nf-f09 .nf-btn{display:block;width:100%;margin-top:16px;background:#0a0a0f;border:2px solid #ffffff;color:#ffffff;',
'border-radius:999px;padding:14px 18px;font-size:16px;font-weight:700;cursor:pointer;letter-spacing:.04em;',
'transition:border-color .18s,box-shadow .18s,transform .12s;box-shadow:0 8px 22px rgba(0,0,0,.45),inset 0 1px 0 rgba(255,255,255,.08)}',
'.nf-f09 .nf-btn:hover{border-color:var(--nf-accent);box-shadow:0 0 22px rgba(63,184,255,.5),inset 0 1px 0 rgba(255,255,255,.08);transform:translateY(-1px)}',
'.nf-f09 .nf-btn:active{transform:translateY(1px)}',
'.nf-f09 .nf-done{text-align:center;padding:10px 4px}',
'.nf-f09 .nf-check{width:64px;height:64px;border-radius:50%;margin:0 auto 14px;border:2px solid #2fe89e;',
'display:flex;align-items:center;justify-content:center;font-size:30px;color:#ffffff;box-shadow:0 0 24px rgba(47,232,158,.5);background:#0a0a0f}',
'.nf-f09 .nf-ref{display:inline-block;margin:12px 0;padding:10px 20px;border-radius:12px;background:#0a0a0f;',
'border:1.5px solid var(--nf-accent);color:#ffffff;font-size:20px;font-weight:700;letter-spacing:.12em;box-shadow:0 0 16px rgba(63,184,255,.35)}',
'.nf-f09 .nf-detail{color:var(--silver);font-size:14px;margin:4px 0}',
'.nf-f09 .nf-detail b{color:#ffffff;font-weight:600}',
'.nf-f09 .nf-ghost{background:transparent;border:1.5px solid rgba(255,255,255,.35);color:#ffffff;border-radius:999px;',
'padding:10px 20px;font-size:14px;font-weight:600;cursor:pointer;margin-top:14px;transition:border-color .18s,box-shadow .18s}',
'.nf-f09 .nf-ghost:hover{border-color:var(--nf-accent);box-shadow:0 0 12px rgba(63,184,255,.35)}',
'.nf-f09 .nf-failsoft{padding:18px;border-radius:14px;border:1px dashed rgba(255,255,255,.3);color:#ffffff;font-size:14px}'
].join('');

function hashRef(s){
  var h = 5381;
  for (var i = 0; i < s.length; i++) h = ((h << 5) + h + s.charCodeAt(i)) >>> 0;
  return h.toString(36).toUpperCase().padStart(6, '0').slice(-6);
}
function fmtDay(iso){
  var d = new Date(iso + 'T12:00:00');
  if (isNaN(d.getTime())) return null;
  var dow = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'][d.getDay()];
  var mon = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][d.getMonth()];
  return { dow: dow, num: d.getDate(), mon: mon, full: dow + ', ' + mon + ' ' + d.getDate() };
}
function normDays(raw){
  var out = [];
  if (!Array.isArray(raw)) return out;
  for (var i = 0; i < raw.length; i++) {
    var it = raw[i];
    if (typeof it === 'string') { var f = fmtDay(it); if (f) out.push({ date: it, dow: f.dow, num: f.num, mon: f.mon, full: f.full }); }
    else if (it && typeof it.date === 'string') {
      var f2 = fmtDay(it.date);
      out.push({ date: it.date, dow: f2 ? f2.dow : '', num: f2 ? f2.num : it.date, mon: f2 ? f2.mon : '', full: it.label || (f2 ? f2.full : it.date) });
    }
  }
  return out;
}
function load(key){ try { var v = localStorage.getItem(key); return v ? JSON.parse(v) : []; } catch (e) { return []; } }
function save(key, v){ try { localStorage.setItem(key, JSON.stringify(v)); } catch (e) {} }

NF.register('f-09-booking', {
  version: '1.0.0',
  activate: function(root, config){
    config = config || {};
    root.classList.add('nf-f09');
    var st = document.createElement('style');
    st.textContent = CSS;
    root.appendChild(st);

    var key = config.storage_key || 'naya_fn_f09_booking';
    var days = normDays(config.days);
    var slots = Array.isArray(config.slots) ? config.slots.filter(function(s){ return typeof s === 'string' && s; }) : [];
    var title = config.title || 'Book an appointment';
    var service = config.service_name || 'Appointment';
    var dur = (typeof config.duration_min === 'number') ? config.duration_min : 30;
    var listeners = [];

    function on(el, ev, fn){ el.addEventListener(ev, fn); listeners.push([el, ev, fn]); }

    if (!days.length || !slots.length) {
      root.insertAdjacentHTML('beforeend',
        '<div class="nf-board"><div class="nf-rail"></div><div class="nf-failsoft">Booking is unavailable right now — the calendar has no days or time slots configured.</div></div>');
      return { destroy: function(){} };
    }

    var sel = { day: null, slot: null };

    function showLatest(existing){
      root.innerHTML = '';
      root.appendChild(st);
      var b = document.createElement('div');
      b.className = 'nf-board';
      b.innerHTML =
        '<div class="nf-rail"></div><div class="nf-done">' +
        '<div class="nf-check">✓</div>' +
        '<div class="nf-kicker">Booking confirmed</div>' +
        '<div class="nf-ref">' + existing.ref + '</div>' +
        '<p class="nf-detail"><b>' + escapeHtml(existing.service) + '</b> · ' + escapeHtml(existing.dayLabel) + ' at ' + escapeHtml(existing.slot) + '</p>' +
        '<p class="nf-detail">Booked for <b>' + escapeHtml(existing.name) + '</b> · ' + existing.dur + ' min</p>' +
        '<button class="nf-ghost" data-act="again">Book another slot</button>' +
        '</div>';
      root.appendChild(b);
      on(b.querySelector('[data-act="again"]'), 'click', renderFlow);
    }

    function escapeHtml(s){
      return String(s == null ? '' : s).replace(/[&<>"']/g, function(c){
        return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
      });
    }

    function renderFlow(){
      sel = { day: null, slot: null };
      root.innerHTML = '';
      root.appendChild(st);
      var b = document.createElement('div');
      b.className = 'nf-board';
      var dayBtns = days.map(function(d, i){
        return '<button class="nf-day" data-day="' + i + '"><span class="nf-dow">' + d.dow + '</span>' +
          '<span class="nf-dnum">' + d.num + '</span><span class="nf-dow">' + d.mon + '</span></button>';
      }).join('');
      var slotBtns = slots.map(function(s){
        return '<button class="nf-slot" data-slot="' + escapeHtml(s) + '">' + escapeHtml(s) + '</button>';
      }).join('');
      b.innerHTML =
        '<div class="nf-rail"></div>' +
        '<div class="nf-kicker">' + escapeHtml(service) + '</div>' +
        '<h3>' + escapeHtml(title) + '</h3>' +
        '<p class="nf-sub">' + (escapeHtml(config.note || 'Pick a day, pick a time — your spot is held the moment you confirm.')) + '</p>' +
        '<div class="nf-step">1 · Pick a day</div><div class="nf-days">' + dayBtns + '</div>' +
        '<div class="nf-step">2 · Pick a time</div><div class="nf-slots">' + slotBtns + '</div>' +
        '<div class="nf-step">3 · Your name</div>' +
        '<div class="nf-field"><input type="text" data-in="name" placeholder="e.g. Shawn Vibert" autocomplete="name" maxlength="80"></div>' +
        '<div class="nf-err" data-e="err"></div>' +
        '<button class="nf-btn" data-act="confirm">Confirm booking</button>';
      root.appendChild(b);

      function markDay(){ var btns = b.querySelectorAll('.nf-day');
        for (var i = 0; i < btns.length; i++) btns[i].classList.toggle('is-sel', sel.day === +btns[i].getAttribute('data-day')); }
      function markSlot(){ var btns = b.querySelectorAll('.nf-slot');
        for (var i = 0; i < btns.length; i++) btns[i].classList.toggle('is-sel', sel.slot === btns[i].getAttribute('data-slot')); }
      function fail(msg){ var e = b.querySelector('[data-e="err"]'); e.textContent = msg; e.classList.add('show'); }

      var dbs = b.querySelectorAll('.nf-day');
      for (var i = 0; i < dbs.length; i++) on(dbs[i], 'click', function(ev){
        sel.day = +ev.currentTarget.getAttribute('data-day'); markDay();
      });
      var sbs = b.querySelectorAll('.nf-slot');
      for (var j = 0; j < sbs.length; j++) on(sbs[j], 'click', function(ev){
        sel.slot = ev.currentTarget.getAttribute('data-slot'); markSlot();
      });
      on(b.querySelector('[data-act="confirm"]'), 'click', function(){
        var name = (b.querySelector('[data-in="name"]').value || '').trim();
        if (sel.day === null) { fail('Pick a day first.'); return; }
        if (!sel.slot) { fail('Pick a time slot.'); return; }
        if (!name) { fail('Tell us the name to hold the booking under.'); return; }
        var d = days[sel.day];
        var ref = 'BK-' + hashRef(d.date + '|' + sel.slot + '|' + name.toLowerCase());
        var booking = { ref: ref, service: service, day: d.date, dayLabel: d.full, slot: sel.slot, name: name, dur: dur, at: Date.now() };
        var all = load(key); all.push(booking); save(key, all);
        showLatest(booking);
      });
    }

    var existing = load(key);
    if (existing.length) showLatest(existing[existing.length - 1]);
    else renderFlow();

    return { destroy: function(){
      for (var i = 0; i < listeners.length; i++) {
        try { listeners[i][0].removeEventListener(listeners[i][1], listeners[i][2]); } catch (e) {}
      }
      listeners = [];
      try { root.classList.remove('nf-f09'); } catch (e) {}
    } };
  }
});
})();
