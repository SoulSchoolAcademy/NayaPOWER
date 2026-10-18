/* NayaFunction: f-10-menu-display v1.0.0
   What: menu with real items + prices from config, quantity steppers, running
     order with total, place-order flow with confirmation
   Activation: <div data-fn="f-10-menu-display" data-fn-config='{...}'></div>
   Config: {
     title: string,               // board heading (default "Menu")
     currency: string,            // symbol (default "$")
     note: string,               // small line under the board
     storage_key: string,         // localStorage key (default "naya_fn_f10_menu")
     items: [ {                  // * REQUIRED — non-empty
       name: string,              // * item name
       description: string,       // one-line description
       price: number              // * price in currency units
     } ]
   }
   Ready behavior: full ordering flow client-side — add/remove quantities, live
     total, cart restored from localStorage, order confirmation with reference
     (ORD-XXXXXX), order persisted locally. No backend needed.
   Connected behavior: none (reserved key `connected`).
   Backend twin: none.
*/
(function(){
'use strict';
var NF = window.NayaFunctions = window.NayaFunctions || {};
NF._r = NF._r || {};
NF.register = NF.register || function(id, def){ if (!NF._r[id]) NF._r[id] = def; };

var CSS = [
'.nf-f10{--nf-accent:#ff9a5a;--obs:#0b0d14;--raise:#121623;--white:#ffffff;--silver:#c9c9d4;--slate:#8a8a99;--line:rgba(255,255,255,.12);',
'font-family:Inter,ui-sans-serif,system-ui,sans-serif;color:var(--silver);font-size:15px;line-height:1.5}',
'.nf-f10 *{box-sizing:border-box}',
'.nf-f10 .nf-board{background:linear-gradient(180deg,var(--raise),var(--obs));border:1px solid var(--line);border-radius:20px;',
'padding:26px 22px;box-shadow:0 18px 44px rgba(0,0,0,.5),inset 0 1px 0 rgba(255,255,255,.06);position:relative;overflow:hidden}',
'.nf-f10 .nf-rail{position:absolute;left:0;top:0;bottom:0;width:5px;background:var(--nf-accent);box-shadow:0 0 14px var(--nf-accent)}',
'.nf-f10 .nf-kicker{font-size:11px;letter-spacing:.22em;text-transform:uppercase;font-weight:700;color:#ffffff;margin-bottom:10px}',
'.nf-f10 h3{color:#ffffff;font-size:22px;margin:0 0 6px;font-weight:600}',
'.nf-f10 .nf-sub{color:var(--silver);font-size:14px;margin:0 0 6px}',
'.nf-f10 .nf-item{display:flex;align-items:center;gap:14px;padding:14px 4px;border-bottom:1px solid var(--line)}',
'.nf-f10 .nf-item:last-of-type{border-bottom:none}',
'.nf-f10 .nf-mid{flex:1;min-width:0}',
'.nf-f10 .nf-name{color:#ffffff;font-size:16px;font-weight:600;margin:0}',
'.nf-f10 .nf-desc{color:var(--slate);font-size:13px;margin:2px 0 0}',
'.nf-f10 .nf-price{color:#ffffff;font-size:16px;font-weight:700;white-space:nowrap}',
'.nf-f10 .nf-stepper{display:flex;align-items:center;gap:8px}',
'.nf-f10 .nf-stbtn{width:34px;height:34px;border-radius:50%;background:#0a0a0f;border:1.5px solid rgba(255,255,255,.55);',
'color:#ffffff;font-size:18px;font-weight:700;cursor:pointer;line-height:1;transition:border-color .18s,box-shadow .18s;box-shadow:0 6px 14px rgba(0,0,0,.4)}',
'.nf-f10 .nf-stbtn:hover{border-color:var(--nf-accent);box-shadow:0 0 12px rgba(255,154,90,.45)}',
'.nf-f10 .nf-qty{color:#ffffff;font-size:16px;font-weight:700;min-width:24px;text-align:center}',
'.nf-f10 .nf-order{margin-top:18px;border:1.5px solid rgba(255,255,255,.2);border-radius:16px;padding:16px;box-shadow:inset 0 2px 10px rgba(0,0,0,.5);background:#0a0a0f}',
'.nf-f10 .nf-otitle{font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:#ffffff;font-weight:700;margin:0 0 10px}',
'.nf-f10 .nf-line{display:flex;justify-content:space-between;align-items:center;padding:6px 0;color:var(--silver);font-size:14px}',
'.nf-f10 .nf-line b{color:#ffffff;font-weight:600}',
'.nf-f10 .nf-rm{background:transparent;border:none;color:var(--slate);cursor:pointer;font-size:13px;padding:2px 6px}',
'.nf-f10 .nf-rm:hover{color:#ffffff;text-decoration:underline}',
'.nf-f10 .nf-empty{color:var(--slate);font-size:14px;text-align:center;padding:8px 0}',
'.nf-f10 .nf-total{display:flex;justify-content:space-between;align-items:center;border-top:1px solid var(--line);margin-top:10px;padding-top:12px}',
'.nf-f10 .nf-total span{color:#ffffff;font-weight:700;font-size:15px}',
'.nf-f10 .nf-total b{color:#ffffff;font-weight:700;font-size:20px}',
'.nf-f10 .nf-btn{display:block;width:100%;margin-top:14px;background:#0a0a0f;border:2px solid #ffffff;color:#ffffff;',
'border-radius:999px;padding:14px 18px;font-size:16px;font-weight:700;cursor:pointer;letter-spacing:.04em;',
'transition:border-color .18s,box-shadow .18s,transform .12s;box-shadow:0 8px 22px rgba(0,0,0,.45),inset 0 1px 0 rgba(255,255,255,.08)}',
'.nf-f10 .nf-btn:hover{border-color:var(--nf-accent);box-shadow:0 0 22px rgba(255,154,90,.5),inset 0 1px 0 rgba(255,255,255,.08);transform:translateY(-1px)}',
'.nf-f10 .nf-btn:active{transform:translateY(1px)}',
'.nf-f10 .nf-btn[disabled]{opacity:.4;cursor:not-allowed;transform:none;box-shadow:none}',
'.nf-f10 .nf-err{display:none;margin-top:10px;padding:10px 14px;border-radius:12px;background:rgba(255,94,108,.08);',
'border-left:4px solid #ff5e6c;color:#ffffff;font-size:14px}',
'.nf-f10 .nf-err.show{display:block}',
'.nf-f10 .nf-done{text-align:center;padding:10px 4px}',
'.nf-f10 .nf-check{width:64px;height:64px;border-radius:50%;margin:0 auto 14px;border:2px solid #2fe89e;',
'display:flex;align-items:center;justify-content:center;font-size:30px;color:#ffffff;box-shadow:0 0 24px rgba(47,232,158,.5);background:#0a0a0f}',
'.nf-f10 .nf-ref{display:inline-block;margin:12px 0;padding:10px 20px;border-radius:12px;background:#0a0a0f;',
'border:1.5px solid var(--nf-accent);color:#ffffff;font-size:20px;font-weight:700;letter-spacing:.12em;box-shadow:0 0 16px rgba(255,154,90,.35)}',
'.nf-f10 .nf-detail{color:var(--silver);font-size:14px;margin:4px 0}',
'.nf-f10 .nf-detail b{color:#ffffff;font-weight:600}',
'.nf-f10 .nf-ghost{background:transparent;border:1.5px solid rgba(255,255,255,.35);color:#ffffff;border-radius:999px;',
'padding:10px 20px;font-size:14px;font-weight:600;cursor:pointer;margin-top:14px;transition:border-color .18s,box-shadow .18s}',
'.nf-f10 .nf-ghost:hover{border-color:var(--nf-accent);box-shadow:0 0 12px rgba(255,154,90,.35)}',
'.nf-f10 .nf-failsoft{padding:18px;border-radius:14px;border:1px dashed rgba(255,255,255,.3);color:#ffffff;font-size:14px}'
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
function load(key){ try { var v = localStorage.getItem(key); return v ? JSON.parse(v) : null; } catch (e) { return null; } }
function save(key, v){ try { localStorage.setItem(key, JSON.stringify(v)); } catch (e) {} }
function money(cur, n){ return cur + (Math.round(n * 100) / 100).toFixed(2); }

NF.register('f-10-menu-display', {
  version: '1.0.0',
  activate: function(root, config){
    config = config || {};
    root.classList.add('nf-f10');
    var st = document.createElement('style');
    st.textContent = CSS;
    root.appendChild(st);

    var key = config.storage_key || 'naya_fn_f10_menu';
    var cur = config.currency || '$';
    var items = [];
    if (Array.isArray(config.items)) {
      for (var i = 0; i < config.items.length; i++) {
        var it = config.items[i] || {};
        if (typeof it.name === 'string' && it.name && typeof it.price === 'number' && isFinite(it.price) && it.price >= 0) {
          items.push({ name: it.name, description: typeof it.description === 'string' ? it.description : '', price: it.price });
        }
      }
    }
    var listeners = [];
    function on(el, ev, fn){ el.addEventListener(ev, fn); listeners.push([el, ev, fn]); }

    if (!items.length) {
      root.insertAdjacentHTML('beforeend',
        '<div class="nf-board"><div class="nf-rail"></div><div class="nf-failsoft">The menu is being updated — check back soon.</div></div>');
      return { destroy: function(){} };
    }

    var saved = load(key) || {};
    var cart = {};
    for (var k in saved) { if (saved.hasOwnProperty(k) && items[+k] && saved[k] > 0) cart[k] = Math.floor(saved[k]); }

    function persist(){ save(key, cart); }
    function count(){ var n = 0; for (var k in cart) n += cart[k]; return n; }
    function total(){ var t = 0; for (var k in cart) t += cart[k] * items[+k].price; return t; }

    function render(){
      root.innerHTML = '';
      root.appendChild(st);
      var b = document.createElement('div');
      b.className = 'nf-board';
      var rows = items.map(function(it, i){
        var q = cart[i] || 0;
        return '<div class="nf-item">' +
          '<div class="nf-mid"><p class="nf-name">' + escapeHtml(it.name) + '</p>' +
          (it.description ? '<p class="nf-desc">' + escapeHtml(it.description) + '</p>' : '') + '</div>' +
          '<span class="nf-price">' + escapeHtml(money(cur, it.price)) + '</span>' +
          '<div class="nf-stepper">' +
          '<button class="nf-stbtn" data-act="dec" data-i="' + i + '" aria-label="Remove one ' + escapeHtml(it.name) + '">−</button>' +
          '<span class="nf-qty" data-q="' + i + '">' + q + '</span>' +
          '<button class="nf-stbtn" data-act="inc" data-i="' + i + '" aria-label="Add one ' + escapeHtml(it.name) + '">+</button>' +
          '</div></div>';
      }).join('');
      b.innerHTML =
        '<div class="nf-rail"></div>' +
        '<div class="nf-kicker">Order</div>' +
        '<h3>' + escapeHtml(config.title || 'Menu') + '</h3>' +
        '<p class="nf-sub">' + escapeHtml(config.note || 'Tap + to build your order — everything is priced below.') + '</p>' +
        '<div data-r="items">' + rows + '</div>' +
        '<div class="nf-order"><p class="nf-otitle">Your order</p>' +
        '<div data-r="lines"></div>' +
        '<div class="nf-total"><span>Total</span><b data-r="total">' + escapeHtml(money(cur, 0)) + '</b></div>' +
        '<button class="nf-btn" data-act="order">Place order</button>' +
        '<div class="nf-err" data-e="err"></div></div>';
      root.appendChild(b);
      paintLines();

      var acts = b.querySelectorAll('[data-act]');
      for (var a = 0; a < acts.length; a++) on(acts[a], 'click', function(ev){
        var t = ev.currentTarget;
        var act = t.getAttribute('data-act');
        var i = +t.getAttribute('data-i');
        if (act === 'inc') { cart[i] = (cart[i] || 0) + 1; paintQty(); }
        else if (act === 'dec') { cart[i] = Math.max(0, (cart[i] || 0) - 1); if (!cart[i]) delete cart[i]; paintQty(); }
        else if (act === 'rm') { delete cart[i]; paintQty(); }
        else if (act === 'order') { placeOrder(); }
        persist(); paintLines();
      });

      function paintQty(){
        for (var k in cart) { /* noop — lines repaint covers */ }
        var qs = b.querySelectorAll('[data-q]');
        for (var q = 0; q < qs.length; q++) {
          qs[q].textContent = cart[+qs[q].getAttribute('data-q')] || 0;
        }
      }
      function paintLines(){
        var holder = b.querySelector('[data-r="lines"]');
        var ks = Object.keys(cart);
        if (!ks.length) {
          holder.innerHTML = '<div class="nf-empty">Nothing here yet — tap + on anything above.</div>';
        } else {
          holder.innerHTML = ks.map(function(k){
            var it = items[+k];
            return '<div class="nf-line"><b>' + cart[k] + '× ' + escapeHtml(it.name) + '</b>' +
              '<span>' + escapeHtml(money(cur, cart[k] * it.price)) +
              ' <button class="nf-rm" data-act="rm" data-i="' + k + '">remove</button></span></div>';
          }).join('');
          var rms = holder.querySelectorAll('[data-act="rm"]');
          for (var r = 0; r < rms.length; r++) on(rms[r], 'click', function(ev){
            delete cart[+ev.currentTarget.getAttribute('data-i')]; persist(); paintLines(); paintQty();
          });
        }
        b.querySelector('[data-r="total"]').textContent = money(cur, total());
        b.querySelector('[data-act="order"]').disabled = !ks.length;
      }
      function placeOrder(){
        if (!count()) {
          var e = b.querySelector('[data-e="err"]');
          e.textContent = 'Your order is empty — add something first.';
          e.classList.add('show');
          return;
        }
        var ref = 'ORD-' + hashRef(JSON.stringify(cart) + '|' + Date.now());
        var lines = Object.keys(cart).map(function(k){
          return { name: items[+k].name, qty: cart[k], line: Math.round(cart[k] * items[+k].price * 100) / 100 };
        });
        var orders = load(key + ':orders') || [];
        orders.push({ ref: ref, lines: lines, total: Math.round(total() * 100) / 100, currency: cur, at: Date.now() });
        save(key + ':orders', orders);
        cart = {}; persist();
        renderDone(ref, lines);
      }
      function renderDone(ref, lines){
        root.innerHTML = '';
        root.appendChild(st);
        var b2 = document.createElement('div');
        b2.className = 'nf-board';
        b2.innerHTML =
          '<div class="nf-rail"></div><div class="nf-done">' +
          '<div class="nf-check">✓</div>' +
          '<div class="nf-kicker">Order confirmed</div>' +
          '<div class="nf-ref">' + ref + '</div>' +
          lines.map(function(l){ return '<p class="nf-detail"><b>' + l.qty + '×</b> ' + escapeHtml(l.name) + ' — ' + escapeHtml(money(cur, l.line)) + '</p>'; }).join('') +
          '<p class="nf-detail">Total <b>' + escapeHtml(money(cur, lines.reduce(function(a, l){ return a + l.line; }, 0))) + '</b></p>' +
          '<button class="nf-ghost" data-act="again">Start a new order</button>' +
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
      try { root.classList.remove('nf-f10'); } catch (e) {}
    } };
  }
});
})();
