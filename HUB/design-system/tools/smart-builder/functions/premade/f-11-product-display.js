/* NayaFunction: f-11-product-display v1.0.0
   What: one product card — price, quantity, buy flow, local order confirmation
   Activation: <div data-fn="f-11-product-display" data-fn-config='{...}'></div>
   Config: {
     name: string,               // * product name
     tagline: string,            // one-line pitch
     price: number,              // * price in currency units
     currency: string,           // symbol (default "$")
     features: string[],         // bullet list of features
     button_text: string,        // buy button label (default "Buy now")
     note: string,               // small line under the board
     storage_key: string         // localStorage key (default "naya_fn_f11_product")
   }
   Ready behavior: full buy flow client-side — quantity stepper, live total,
     buy button, order confirmation with reference (ORD-XXXXXX), order
     persisted to localStorage. No backend needed.
   Connected behavior: none (reserved key `connected`).
   Backend twin: none.
*/
(function(){
'use strict';
var NF = window.NayaFunctions = window.NayaFunctions || {};
NF._r = NF._r || {};
NF.register = NF.register || function(id, def){ if (!NF._r[id]) NF._r[id] = def; };

var CSS = [
'.nf-f11{--nf-accent:#e84fff;--obs:#0b0d14;--raise:#121623;--white:#ffffff;--silver:#c9c9d4;--slate:#8a8a99;--line:rgba(255,255,255,.12);',
'font-family:Inter,ui-sans-serif,system-ui,sans-serif;color:var(--silver);font-size:15px;line-height:1.5}',
'.nf-f11 *{box-sizing:border-box}',
'.nf-f11 .nf-board{background:linear-gradient(180deg,var(--raise),var(--obs));border:1px solid var(--line);border-radius:20px;',
'padding:26px 22px;box-shadow:0 18px 44px rgba(0,0,0,.5),inset 0 1px 0 rgba(255,255,255,.06);position:relative;overflow:hidden}',
'.nf-f11 .nf-rail{position:absolute;left:0;top:0;bottom:0;width:5px;background:var(--nf-accent);box-shadow:0 0 14px var(--nf-accent)}',
'.nf-f11 .nf-kicker{font-size:11px;letter-spacing:.22em;text-transform:uppercase;font-weight:700;color:#ffffff;margin-bottom:10px}',
'.nf-f11 h3{color:#ffffff;font-size:24px;margin:0 0 6px;font-weight:600}',
'.nf-f11 .nf-tag{color:var(--silver);font-size:15px;margin:0 0 14px}',
'.nf-f11 .nf-feats{list-style:none;margin:0 0 6px;padding:0}',
'.nf-f11 .nf-feats li{position:relative;padding:6px 0 6px 26px;color:var(--silver);font-size:14px}',
'.nf-f11 .nf-feats li:before{content:"◆";position:absolute;left:2px;color:var(--nf-accent);font-size:12px;top:10px}',
'.nf-f11 .nf-buyrow{display:flex;align-items:center;justify-content:space-between;gap:14px;margin-top:18px;flex-wrap:wrap}',
'.nf-f11 .nf-stepper{display:flex;align-items:center;gap:10px}',
'.nf-f11 .nf-stbtn{width:38px;height:38px;border-radius:50%;background:#0a0a0f;border:1.5px solid rgba(255,255,255,.55);',
'color:#ffffff;font-size:20px;font-weight:700;cursor:pointer;line-height:1;transition:border-color .18s,box-shadow .18s;box-shadow:0 6px 14px rgba(0,0,0,.4)}',
'.nf-f11 .nf-stbtn:hover{border-color:var(--nf-accent);box-shadow:0 0 12px rgba(232,79,255,.45)}',
'.nf-f11 .nf-qty{color:#ffffff;font-size:18px;font-weight:700;min-width:28px;text-align:center}',
'.nf-f11 .nf-total{color:#ffffff;font-size:24px;font-weight:700}',
'.nf-f11 .nf-total small{display:block;font-size:12px;color:var(--slate);font-weight:400;letter-spacing:.08em;text-transform:uppercase}',
'.nf-f11 .nf-btn{display:block;width:100%;margin-top:14px;background:#0a0a0f;border:2px solid #ffffff;color:#ffffff;',
'border-radius:999px;padding:14px 18px;font-size:16px;font-weight:700;cursor:pointer;letter-spacing:.04em;',
'transition:border-color .18s,box-shadow .18s,transform .12s;box-shadow:0 8px 22px rgba(0,0,0,.45),inset 0 1px 0 rgba(255,255,255,.08)}',
'.nf-f11 .nf-btn:hover{border-color:var(--nf-accent);box-shadow:0 0 22px rgba(232,79,255,.5),inset 0 1px 0 rgba(255,255,255,.08);transform:translateY(-1px)}',
'.nf-f11 .nf-btn:active{transform:translateY(1px)}',
'.nf-f11 .nf-done{text-align:center;padding:10px 4px}',
'.nf-f11 .nf-check{width:64px;height:64px;border-radius:50%;margin:0 auto 14px;border:2px solid #2fe89e;',
'display:flex;align-items:center;justify-content:center;font-size:30px;color:#ffffff;box-shadow:0 0 24px rgba(47,232,158,.5);background:#0a0a0f}',
'.nf-f11 .nf-ref{display:inline-block;margin:12px 0;padding:10px 20px;border-radius:12px;background:#0a0a0f;',
'border:1.5px solid var(--nf-accent);color:#ffffff;font-size:20px;font-weight:700;letter-spacing:.12em;box-shadow:0 0 16px rgba(232,79,255,.35)}',
'.nf-f11 .nf-detail{color:var(--silver);font-size:14px;margin:4px 0}',
'.nf-f11 .nf-detail b{color:#ffffff;font-weight:600}',
'.nf-f11 .nf-ghost{background:transparent;border:1.5px solid rgba(255,255,255,.35);color:#ffffff;border-radius:999px;',
'padding:10px 20px;font-size:14px;font-weight:600;cursor:pointer;margin-top:14px;transition:border-color .18s,box-shadow .18s}',
'.nf-f11 .nf-ghost:hover{border-color:var(--nf-accent);box-shadow:0 0 12px rgba(232,79,255,.35)}',
'.nf-f11 .nf-failsoft{padding:18px;border-radius:14px;border:1px dashed rgba(255,255,255,.3);color:#ffffff;font-size:14px}'
].join('');

function hashRef(s){
  var h = 5381;
  for (var i = 0; i < s.length; i++) h = ((h << 5) + h + s.charCodeAt(i)) >>> 0;
  return h.toString(36).toUpperCase().padStart(6, '0').slice(-6);
}
function escapeHtml(s){
  return String(s == null ? '' : s).replace(/[&<>"']/g, function(c){
    return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
  });
}
function load(key){ try { var v = localStorage.getItem(key); return v ? JSON.parse(v) : []; } catch (e) { return []; } }
function save(key, v){ try { localStorage.setItem(key, JSON.stringify(v)); } catch (e) {} }
function money(cur, n){ return cur + (Math.round(n * 100) / 100).toFixed(2); }

NF.register('product-display', {
  version: '1.0.0',
  activate: function(root, config){
    config = config || {};
    root.classList.add('nf-f11');
    var st = document.createElement('style');
    st.textContent = CSS;
    root.appendChild(st);

    var name = typeof config.name === 'string' ? config.name : '';
    var price = (typeof config.price === 'number' && isFinite(config.price) && config.price >= 0) ? config.price : NaN;
    var cur = config.currency || '$';
    var features = Array.isArray(config.features) ? config.features.filter(function(f){ return typeof f === 'string' && f; }) : [];
    var key = config.storage_key || 'naya_fn_f11_product';
    var listeners = [];
    function on(el, ev, fn){ el.addEventListener(ev, fn); listeners.push([el, ev, fn]); }

    // Fail soft: without a real name and price there is nothing honest to sell.
    if (!name || isNaN(price)) {
      root.insertAdjacentHTML('beforeend',
        '<div class="nf-board"><div class="nf-rail"></div><div class="nf-failsoft">This product is missing its name or price — the page owner still needs to set it up.</div></div>');
      return { destroy: function(){} };
    }

    var qty = 1;

    function render(){
      root.innerHTML = '';
      root.appendChild(st);
      var b = document.createElement('div');
      b.className = 'nf-board';
      b.innerHTML =
        '<div class="nf-rail"></div>' +
        '<div class="nf-kicker">Product</div>' +
        '<h3>' + escapeHtml(name) + '</h3>' +
        (config.tagline ? '<p class="nf-tag">' + escapeHtml(config.tagline) + '</p>' : '') +
        (features.length ? '<ul class="nf-feats">' + features.map(function(f){ return '<li>' + escapeHtml(f) + '</li>'; }).join('') + '</ul>' : '') +
        '<div class="nf-buyrow">' +
          '<div class="nf-stepper">' +
            '<button class="nf-stbtn" data-act="dec" aria-label="Decrease quantity">−</button>' +
            '<span class="nf-qty" data-r="qty">' + qty + '</span>' +
            '<button class="nf-stbtn" data-act="inc" aria-label="Increase quantity">+</button>' +
          '</div>' +
          '<div class="nf-total"><small>Total</small><span data-r="total">' + escapeHtml(money(cur, price)) + '</span></div>' +
        '</div>' +
        '<button class="nf-btn" data-act="buy">' + escapeHtml(config.button_text || 'Buy now') + '</button>' +
        (config.note ? '<p class="nf-tag" style="margin:12px 0 0;font-size:13px">' + escapeHtml(config.note) + '</p>' : '');
      root.appendChild(b);

      function paint(){
        b.querySelector('[data-r="qty"]').textContent = qty;
        b.querySelector('[data-r="total"]').textContent = money(cur, qty * price);
      }
      var acts = b.querySelectorAll('[data-act]');
      for (var i = 0; i < acts.length; i++) on(acts[i], 'click', function(ev){
        var act = ev.currentTarget.getAttribute('data-act');
        if (act === 'inc') { qty = Math.min(99, qty + 1); paint(); }
        else if (act === 'dec') { qty = Math.max(1, qty - 1); paint(); }
        else if (act === 'buy') { buy(); }
      });

      function buy(){
        var ref = 'ORD-' + hashRef(name + '|' + qty + '|' + price + '|' + Date.now());
        var order = { ref: ref, name: name, qty: qty, unit: price, total: Math.round(qty * price * 100) / 100, currency: cur, at: Date.now() };
        var all = load(key); all.push(order); save(key, all);
        root.innerHTML = '';
        root.appendChild(st);
        var b2 = document.createElement('div');
        b2.className = 'nf-board';
        b2.innerHTML =
          '<div class="nf-rail"></div><div class="nf-done">' +
          '<div class="nf-check">✓</div>' +
          '<div class="nf-kicker">Order confirmed</div>' +
          '<div class="nf-ref">' + ref + '</div>' +
          '<p class="nf-detail"><b>' + qty + '× ' + escapeHtml(name) + '</b> — ' + escapeHtml(money(cur, qty * price)) + '</p>' +
          '<p class="nf-detail">Your order is saved on this device. The seller will be in touch to arrange payment and delivery.</p>' +
          '<button class="nf-ghost" data-act="again">Buy another</button>' +
          '</div>';
        root.appendChild(b2);
        on(b2.querySelector('[data-act="again"]'), 'click', function(){ qty = 1; render(); });
      }
    }

    render();
    return { destroy: function(){
      for (var i = 0; i < listeners.length; i++) {
        try { listeners[i][0].removeEventListener(listeners[i][1], listeners[i][2]); } catch (e) {}
      }
      listeners = [];
      try { root.classList.remove('nf-f11'); } catch (e) {}
    } };
  }
});
})();
