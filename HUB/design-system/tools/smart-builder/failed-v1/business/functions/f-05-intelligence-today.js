/* NayaFunction: intelligence-today v1.0.0
   What: Daily briefing board — renders briefing items with date-awareness.
   Activation: <div data-fn="intelligence-today" data-fn-config='{...}'></div>
   Config: {
     items: [{date, time, title, detail, kind}]
       date: 'YYYY-MM-DD' for a dated item, or 'daily' for a recurring-daily item
       kind: 'verified' | 'stated' | 'alert' | 'note' (drives the LED dot color)
     title: heading text (default 'Intelligence Today')
   } — all optional.
   Ready behavior: renders today's briefing from config — dated items whose date is
     today plus recurring 'daily' items. Dated items for other days appear under an
     "Earlier" disclosure. With no items for today the board says so honestly —
     it never invents a briefing.
   Connected behavior: none — the `connected` key is reserved. Connecting an
     intelligence source would refresh the briefing live; until then it reads the
     page's own data.
   Backend twin: builder-review/HUB/design-system/tools/smart-builder/functions/feature_intelligence_today.py
     (noted here only — this unit is fully client-side and never calls it).
   Consent line: copy states the briefing renders from this page's data and that
     connecting a source refreshes it live — ready vs connected never conflated.
   Lesson L-2026-10-17-004: every control below is bound to DOM this unit creates.
   Deterministic: same config + same calendar day → same board.
*/
(function(){
'use strict';
var NF = window.NayaFunctions = window.NayaFunctions || {};
NF._r = NF._r || {};
NF.register = NF.register || function(id, def){
  if (NF._r[id]) return;
  NF._r[id] = def;
};

var UNIT = 'intelligence-today';
var UNIT_COLOR = '#ffbf3d'; /* Law 9 token — one color job per unit; gold = shown (Law 2) */
var KIND_COLORS = { verified: '#2fe89e', stated: '#3fb8ff', alert: '#ff5e6c', note: '#a06bff' };

function pad(n){ return (n < 10 ? '0' : '') + n; }
function todayISO(){
  var d = new Date();
  return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate());
}
function longDate(){
  try { return new Date().toLocaleDateString(undefined, { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }); }
  catch(e){ return todayISO(); }
}
function cssOnce(){
  if (document.querySelector('style[data-nf-css="intelligence-today"]')) return;
  var st = document.createElement('style');
  st.setAttribute('data-nf-css','intelligence-today');
  st.textContent = [
    '.nf-intel{font-family:Inter,system-ui,sans-serif;color:#fff;background:#0a0a0d;',
    ' border:1px solid rgba(255,255,255,.14);border-radius:14px;padding:14px 16px;',
    ' box-shadow:0 10px 30px rgba(0,0,0,.55), inset 0 1px 0 rgba(255,255,255,.06);}',
    '.nf-intel h3{margin:0 0 2px;font-size:18px;font-weight:700;color:#fff;}',
    '.nf-intel .nf-date{font-size:14px;color:#fff;opacity:.75;margin:0 0 12px;}',
    '.nf-brief{border:1px solid rgba(255,255,255,.14);border-radius:10px;padding:12px 14px;',
    ' margin:10px 0;background:#0d0d11;}',
    '.nf-brief .bh{display:flex;align-items:center;gap:10px;margin-bottom:4px;}',
    '.nf-led{width:12px;height:12px;border-radius:50%;background:var(--kc);flex:0 0 auto;',
    ' box-shadow:0 0 10px var(--kc);}', /* LED dot carries the color — never the text */
    '.nf-brief .bt{font-size:18px;font-weight:700;color:#fff;margin:0;}',
    '.nf-brief .btime{font-size:14px;color:#fff;opacity:.6;}',
    '.nf-brief .bd{font-size:14px;color:#fff;opacity:.92;margin:6px 0 0;}',
    '.nf-earlier{margin-top:12px;border:1px solid rgba(255,255,255,.14);border-radius:10px;',
    ' background:#0d0d11;}',
    '.nf-earlier summary{font-size:18px;font-weight:700;color:#fff;cursor:pointer;padding:12px 14px;}',
    '.nf-earlier .ebody{padding:0 14px 12px;}',
    '.nf-intel .nf-empty{font-size:14px;color:#fff;opacity:.6;padding:18px 4px;}',
    '.nf-refresh{background:#141419;color:#fff;border:1.5px solid rgba(255,255,255,.35);',
    ' border-radius:10px;padding:10px 14px;font-size:14px;min-height:44px;cursor:pointer;margin-top:8px;}',
    '.nf-refresh:hover{border-color:' + UNIT_COLOR + ';box-shadow:0 0 14px -4px ' + UNIT_COLOR + ';}',
    '.nf-intel .nf-status{font-size:14px;color:#fff;opacity:.85;margin:10px 2px 0;min-height:20px;}',
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
    var listeners = [];
    function on(el, ev, fn){ el.addEventListener(ev, fn); listeners.push([el, ev, fn]); }

    var items = Array.isArray(config.items) ? config.items : [];
    var today = todayISO();

    root.innerHTML = '';
    var wrap = document.createElement('div');
    wrap.className = 'nf-intel';
    var h = document.createElement('h3');
    h.textContent = config.title || 'Intelligence Today';
    wrap.appendChild(h);
    var dateLine = document.createElement('p');
    dateLine.className = 'nf-date';
    dateLine.textContent = longDate();
    wrap.appendChild(dateLine);
    var board = document.createElement('div');
    wrap.appendChild(board);
    var status = document.createElement('p');
    status.className = 'nf-status';
    status.setAttribute('aria-live','polite');
    wrap.appendChild(status);
    var consent = document.createElement('p');
    consent.className = 'nf-consent';
    consent.textContent = 'Ready now: the briefing renders from this page\u2019s data. Connect an intelligence source to refresh it live (connected is off).';
    wrap.appendChild(consent);
    root.appendChild(wrap);

    function say(msg){ status.textContent = msg; }

    function briefEl(it){
      var d = document.createElement('div');
      d.className = 'nf-brief';
      var head = document.createElement('div'); head.className = 'bh';
      var led = document.createElement('span'); led.className = 'nf-led';
      led.style.setProperty('--kc', KIND_COLORS[it.kind] || KIND_COLORS.stated);
      var t = document.createElement('p'); t.className = 'bt'; t.textContent = it.title || 'Untitled';
      head.appendChild(led); head.appendChild(t);
      d.appendChild(head);
      if (it.time) { var tm = document.createElement('p'); tm.className = 'btime'; tm.textContent = it.time; d.appendChild(tm); }
      if (it.detail) { var bd = document.createElement('p'); bd.className = 'bd'; bd.textContent = it.detail; d.appendChild(bd); }
      return d;
    }

    function render(){
      board.innerHTML = '';
      var todays = [], earlier = [];
      items.forEach(function(it){
        if (it.date === 'daily' || it.date === today) todays.push(it);
        else earlier.push(it);
      });
      if (!todays.length) {
        var e = document.createElement('p'); e.className = 'nf-empty';
        e.textContent = 'No briefing items for today yet — the board stays honest, not busy.';
        board.appendChild(e);
      }
      todays.forEach(function(it){ board.appendChild(briefEl(it)); });
      if (earlier.length) {
        var det = document.createElement('details');
        det.className = 'nf-earlier';
        var sum = document.createElement('summary');
        sum.textContent = 'Earlier (' + earlier.length + ')';
        var eb = document.createElement('div'); eb.className = 'ebody';
        earlier.forEach(function(it){
          var it2 = { time: it.time, title: it.title, detail: (it.date ? it.date + ' · ' : '') + (it.detail || ''), kind: it.kind };
          eb.appendChild(briefEl(it2));
        });
        det.appendChild(sum); det.appendChild(eb);
        board.appendChild(det);
      }
      var refresh = document.createElement('button');
      refresh.type = 'button'; refresh.className = 'nf-refresh';
      refresh.textContent = '↻ Re-check';
      on(refresh, 'click', function(){
        today = todayISO();
        render();
        say('Briefing re-checked for ' + longDate() + ' — ' + todays.length + ' item' + (todays.length === 1 ? '' : 's') + ' today.');
      });
      board.appendChild(refresh);
    }

    render();
    say(items.length ? 'Briefing loaded.' : 'Nothing scheduled in this briefing yet.');

    return {
      destroy: function(){
        listeners.forEach(function(l){ try { l[0].removeEventListener(l[1], l[2]); } catch(e){} });
        root.innerHTML = '';
      }
    };
  }
});
})();
