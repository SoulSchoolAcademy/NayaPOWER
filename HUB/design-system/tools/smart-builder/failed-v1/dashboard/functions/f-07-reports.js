/* NayaFunction: reports v1.0.0
   What: Daily / weekly / monthly switcher rendering report cards from config data.
   Activation: <div data-fn="reports" data-fn-config='{...}'></div>
   Config: {
     reports: {
       daily:   [{title, value, delta, note}],
       weekly:  [{title, value, delta, note}],
       monthly: [{title, value, delta, note}]
     }
     title: heading text (default 'Reports')
   } — all optional.
   Ready behavior: the three-period switcher renders the report cards for the chosen
     period from config. A period with no data says so honestly — the unit never
     invents numbers.
   Connected behavior: none — the `connected` key is reserved. Connecting analytics
     would fill these cards with live numbers; until then they read the page's data.
   Consent line: copy states the reports render from this page's data and that
     connecting analytics makes them live — ready vs connected never conflated.
   Lesson L-2026-10-17-004: every control below is bound to DOM this unit creates.
   Deterministic: same config → same cards, in config order.
*/
(function(){
'use strict';
var NF = window.NayaFunctions = window.NayaFunctions || {};
NF._r = NF._r || {};
NF.register = NF.register || function(id, def){
  if (NF._r[id]) return;
  NF._r[id] = def;
};

var UNIT = 'reports';
var UNIT_COLOR = '#6675ff'; /* Law 9 token — one color job per unit */
var PERIODS = [['daily','Daily'],['weekly','Weekly'],['monthly','Monthly']];

function cssOnce(){
  if (document.querySelector('style[data-nf-css="reports"]')) return;
  var st = document.createElement('style');
  st.setAttribute('data-nf-css','reports');
  st.textContent = [
    '.nf-reports{font-family:Inter,system-ui,sans-serif;color:#fff;background:#0a0a0d;',
    ' border:1px solid rgba(255,255,255,.14);border-radius:14px;padding:14px 16px;',
    ' box-shadow:0 10px 30px rgba(0,0,0,.55), inset 0 1px 0 rgba(255,255,255,.06);}',
    '.nf-reports h3{margin:0 0 4px;font-size:18px;font-weight:700;color:#fff;}',
    '.nf-reports .nf-sub{font-size:14px;color:#fff;opacity:.75;margin:0 0 12px;}',
    '.nf-switch{display:flex;gap:8px;margin-bottom:12px;flex-wrap:wrap;}',
    '.nf-swbtn{background:#101014;color:#fff;border:1.5px solid rgba(255,255,255,.35);',
    ' border-radius:999px;padding:10px 18px;font-size:14px;min-height:44px;cursor:pointer;}',
    '.nf-swbtn:hover{border-color:' + UNIT_COLOR + ';}',
    '.nf-swbtn.active{border-color:' + UNIT_COLOR + ';box-shadow:0 0 16px -4px ' + UNIT_COLOR + ';}',
    '.nf-rcard{border:1px solid rgba(255,255,255,.14);border-radius:10px;padding:12px 14px;',
    ' margin:10px 0;background:#0d0d11;}',
    '.nf-rcard .rt{font-size:18px;font-weight:700;color:#fff;margin:0 0 4px;}',
    '.nf-rcard .rv{font-size:24px;font-weight:700;color:#fff;margin:0 0 4px;}',
    '.nf-delta{display:inline-block;font-size:14px;color:#fff;border-radius:999px;',
    ' padding:2px 10px;margin-left:8px;}',
    '.nf-delta.up{border:1px solid #2fe89e;color:#fff;}', /* green = proven movement */
    '.nf-delta.down{border:1px solid #ff5e6c;color:#fff;}',
    '.nf-rcard .rn{font-size:14px;color:#fff;opacity:.75;margin:6px 0 0;}',
    '.nf-reports .nf-empty{font-size:14px;color:#fff;opacity:.6;padding:18px 4px;}',
    '.nf-reports .nf-status{font-size:14px;color:#fff;opacity:.85;margin:10px 2px 0;min-height:20px;}',
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
    var data = config.reports || {};
    var period = 'daily';
    var listeners = [];
    function on(el, ev, fn){ el.addEventListener(ev, fn); listeners.push([el, ev, fn]); }

    root.innerHTML = '';
    var wrap = document.createElement('div');
    wrap.className = 'nf-reports';
    var h = document.createElement('h3');
    h.textContent = config.title || 'Reports';
    wrap.appendChild(h);
    var sub = document.createElement('p');
    sub.className = 'nf-sub';
    sub.textContent = 'Your world, measured — pick a period and see it.';
    wrap.appendChild(sub);
    var sw = document.createElement('div');
    sw.className = 'nf-switch';
    sw.setAttribute('role','tablist');
    wrap.appendChild(sw);
    var cards = document.createElement('div');
    wrap.appendChild(cards);
    var status = document.createElement('p');
    status.className = 'nf-status';
    status.setAttribute('aria-live','polite');
    wrap.appendChild(status);
    var consent = document.createElement('p');
    consent.className = 'nf-consent';
    consent.textContent = 'Ready now: reports render from this page\u2019s data. Connect analytics to make them live (connected is off).';
    wrap.appendChild(consent);
    root.appendChild(wrap);

    function say(msg){ status.textContent = msg; }

    function cardEl(r){
      var d = document.createElement('div');
      d.className = 'nf-rcard';
      var t = document.createElement('p'); t.className = 'rt'; t.textContent = r.title || 'Report';
      var v = document.createElement('p'); v.className = 'rv'; v.textContent = (r.value == null ? '—' : r.value);
      if (r.delta) {
        var dl = document.createElement('span');
        var down = /^-/.test(String(r.delta).trim());
        dl.className = 'nf-delta ' + (down ? 'down' : 'up');
        dl.textContent = r.delta;
        v.appendChild(dl);
      }
      d.appendChild(t); d.appendChild(v);
      if (r.note) { var n = document.createElement('p'); n.className = 'rn'; n.textContent = r.note; d.appendChild(n); }
      return d;
    }

    function render(){
      sw.innerHTML = '';
      PERIODS.forEach(function(p){
        var b = document.createElement('button');
        b.type = 'button';
        b.className = 'nf-swbtn' + (period === p[0] ? ' active' : '');
        b.setAttribute('role','tab');
        b.textContent = p[1];
        on(b, 'click', function(){
          period = p[0];
          render();
          var n = (data[period] || []).length;
          say(p[1] + ' reports — ' + n + ' card' + (n === 1 ? '' : 's') + '.');
        });
        sw.appendChild(b);
      });
      cards.innerHTML = '';
      var list = data[period] || [];
      if (!list.length) {
        var e = document.createElement('p'); e.className = 'nf-empty';
        e.textContent = 'No ' + period + ' reports yet — the page stays honest instead of inventing numbers.';
        cards.appendChild(e); return;
      }
      list.forEach(function(r){ cards.appendChild(cardEl(r)); });
    }

    render();
    say('Showing daily reports — switch periods above.');

    return {
      destroy: function(){
        listeners.forEach(function(l){ try { l[0].removeEventListener(l[1], l[2]); } catch(e){} });
        root.innerHTML = '';
      }
    };
  }
});
})();
