/* NayaFunction: cart v1.0.0
   What: Piece cart — Select adds with size pill, qty +/- , inline per-piece notes, remove.
   Activation: <div data-fn="cart" data-fn-config='{}'></div>
   Config: { emptyMessage } — every key documented, all optional unless marked *
   Ready behavior: fully client-side. Injects its own minimal item-row CSS (guarded,
     idempotent) so unit-rendered rows work on any host page; host cart chrome untouched.
   Connected behavior: none
   Backend twin: none
*/
(function(){
'use strict';
var NF = window.NayaFunctions = window.NayaFunctions || {};
NF._r = NF._r || {};
NF.register = NF.register || function(id, def){
  if (NF._r[id]) return; // one function, one implementation — never double-register
  NF._r[id] = def;
};
NF.get = NF.get || function(id){ return NF._r[id] || null; };

// Cartitem row CSS harvested verbatim from ultimate-intake.html (lines 525-534)
// so unit-rendered rows look right on any host page. White text per Law 1.
var CART_CSS =
 '.cartitem{background:#050507;border:1px solid rgba(255,255,255,.25);border-radius:14px;padding:12px;' +
 'box-shadow:inset 0 3px 12px rgba(0,0,0,.7)}' +
 '.cartitem .cname{color:#fff;font-weight:700;font-size:14px}' +
 '.cartitem .cmeta{font-size:11px;color:rgba(248,247,251,.55);margin:3px 0 8px}' +
 '.cartitem input.cnote{width:100%;box-sizing:border-box;background:#0B0D12;border:1px solid rgba(255,255,255,.25);' +
 'border-radius:8px;color:#fff;font-size:12px;padding:8px;margin-bottom:8px}' +
 '.crow{display:flex;align-items:center;gap:10px}' +
 '.qtybtn{background:transparent;border:1px solid rgba(255,255,255,.4);color:#fff;width:30px;height:30px;border-radius:8px;' +
 'cursor:pointer;font-size:16px}' +
 '.cremove{background:none;border:none;color:#ff5e6c;font-size:15px;cursor:pointer;margin-left:auto}';

NF.register('cart', {
  version: '1.0.0',
  // items() exposes the live cart for sibling units (contract-draft.collect()).
  items: function(){ return NF._cartItems || []; },
  activate: function(root, config){
    config = config || {};
    if (root.dataset.nfBound_cart) return { destroy: function(){} };
    root.dataset.nfBound_cart = '1';

    function $(id){ return root.querySelector('#' + id); }
    var fab = $('cartFab'), drawer = $('cartDrawer'), itemsBox = $('cartItems'),
        count = $('cartCount'), closeBtn = $('closeCart');
    var cards = root.querySelectorAll('.pcard');
    // Fail soft: no cart surface at all → nothing to wire (L-2026-10-17-004).
    if (!fab || !drawer || !itemsBox || !count || !cards.length) return { destroy: function(){} };

    // Guarded idempotent style injection for unit-rendered rows.
    if (!document.getElementById('nf-cart-css')){
      var st = document.createElement('style');
      st.id = 'nf-cart-css'; st.textContent = CART_CSS;
      document.head.appendChild(st);
    }

    var EMPTY = config.emptyMessage || 'Your cart is empty \u2014 tap Select on any piece.';
    var cart = NF._cartItems = []; // shared singleton: contract-draft reads via NF.get('cart').items()
    var prevBindings = [];

    function remember(el, prop){ prevBindings.push([el, prop, el[prop]]); }
    function sizeOf(card){ var b = card.querySelector('.szpill.on'); return b ? b.dataset.s : 'M'; }
    function findItem(model, size){ return cart.find(function(i){ return i.model === model && i.size === size; }); }
    function openCart(){ drawer.classList.add('open'); }

    // renderCart harvested verbatim from ultimate-intake.html; scoped to root.
    function renderCart(){
      count.textContent = cart.reduce(function(a,i){ return a + i.qty; }, 0);
      itemsBox.innerHTML = cart.length ? '' :
        '<p style="opacity:.5;padding:20px;color:#fff">' + EMPTY + '</p>';
      cart.forEach(function(i, x){
        var d = document.createElement('div');
        d.className = 'cartitem'; d.dataset.model = i.model; d.dataset.size = i.size;
        d.innerHTML = '<div class="cname"></div><div class="cmeta"></div>' +
          '<input class="cnote" placeholder="Note for Naya\u2026" value="">' +
          '<div class="crow"><button class="qtybtn" data-q="-1">\u2212</button>' +
          '<span style="color:#fff">\u00d7' + i.qty + '</span>' +
          '<button class="qtybtn" data-q="1">+</button><button class="cremove">\u2715 remove</button></div>';
        d.querySelector('.cname').textContent = i.name;
        d.querySelector('.cmeta').textContent = i.model + ' \u00b7 size ' + i.size;
        var note = d.querySelector('.cnote'); note.value = i.note || '';
        note.oninput = function(){ i.note = note.value; };
        d.querySelectorAll('.qtybtn').forEach(function(q){
          q.onclick = function(){ i.qty += parseInt(q.dataset.q, 10); if (i.qty < 1) cart.splice(x, 1); renderCart(); };
        });
        d.querySelector('.cremove').onclick = function(){ cart.splice(x, 1); renderCart(); };
        itemsBox.appendChild(d);
      });
    }

    // Piece cards harvested verbatim from ultimate-intake.html; scoped to root.
    // (.seg-tab/.tog-chip/.pstage handlers skipped — those classes exist only in
    // ultimate's page, not on the host; L-2026-10-17-004.)
    cards.forEach(function(card){
      card.querySelectorAll('.szpill').forEach(function(b){
        remember(b, 'onclick');
        b.onclick = function(){
          card.querySelectorAll('.szpill').forEach(function(x){ x.classList.remove('on'); });
          b.classList.add('on');
          var z = card.querySelector('.zoom');
          if (z) z.style.transform = 'scale(' + b.dataset.z + ')';
        };
      });
      var sel = card.querySelector('.btn-select');
      if (sel){
        remember(sel, 'onclick');
        sel.onclick = function(){
          var m = card.dataset.model, n = card.dataset.name, s = sizeOf(card);
          var ex = findItem(m, s);
          if (ex){ ex.qty++; } else { cart.push({model: m, name: n, size: s, qty: 1, note: ''}); }
          sel.classList.add('picked'); sel.textContent = 'In cart \u2713';
          renderCart();
        };
      }
      var notes = card.querySelector('.btn-notes');
      if (notes){
        remember(notes, 'onclick');
        notes.onclick = function(){
          var m = card.dataset.model, s = sizeOf(card);
          var it = findItem(m, s);
          if (!it){ it = {model: m, name: card.dataset.name, size: s, qty: 1, note: ''}; cart.push(it); }
          renderCart(); openCart();
          var inp = root.querySelector('.cartitem[data-model="' + m + '"][data-size="' + s + '"] .cnote');
          if (inp) inp.focus();
        };
      }
    });

    remember(fab, 'onclick');
    fab.onclick = function(){ drawer.classList.toggle('open'); };
    if (closeBtn){ remember(closeBtn, 'onclick'); closeBtn.onclick = function(){ drawer.classList.remove('open'); }; }

    renderCart();
    root.setAttribute('data-nf-cart', 'bound');

    return { destroy: function(){
      prevBindings.forEach(function(p){ p[0][p[1]] = p[2]; });
      cart.length = 0;
      delete root.dataset.nfBound_cart;
      root.removeAttribute('data-nf-cart');
    } };
  }
});
})();
