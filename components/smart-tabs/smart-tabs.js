/* ============================================================================
 * SmartTabs v9.0.0 — standalone kit
 * The universal favorites ribbon that follows the user across every page.
 *
 * Install:
 *   <link rel="stylesheet" href="smart-tabs.css">
 *   <div id="smarttabs"></div>
 *   <script src="smart-tabs.js"></script>
 *   <script>
 *     const tabs = SmartTabs.mount('#smarttabs', {
 *       storageKey: 'my_app_shortcuts',   // shared across pages = ribbon stays in sync
 *       onNavigate: (route) => { document.querySelector(route)?.scrollIntoView({behavior:'smooth'}); },
 *       routeMap: { 'home': '#top' }       // keyword → route synonyms
 *     });
 *   </script>
 *
 * API:
 *   tabs.list()                  → [{ id, label, route, heart, star }, …]
 *   tabs.set(arrayOfShortcuts)   → replace wholesale
 *   tabs.add({ id, label, route, heart, star })
 *   tabs.remove(id)
 *
 * Law: one component, every page. The ribbon follows the user.
 * ========================================================================== */
(function (global) {
  'use strict';

  var DEF = {
    storageKey: 'nayapower_smarttabs',
    initial: [],
    routeMap: {},
    addLabel: '＋ Add',
    onNavigate: function (route) {
      var t = document.querySelector(route);
      if (t) t.scrollIntoView({ behavior: 'smooth' });
    }
  };

  function el(html) {
    var d = document.createElement('div');
    d.innerHTML = html.trim();
    return d.firstChild;
  }

  function placeNear(anchor, panel, oy) {
    oy = oy || 8;
    var r = anchor.getBoundingClientRect();
    var W = panel.offsetWidth || 280, H = panel.offsetHeight || 160;
    panel.style.left = Math.min(window.innerWidth - W - 8, Math.max(8, r.left)) + 'px';
    panel.style.top = Math.min(window.innerHeight - H - 8, r.bottom + oy) + 'px';
  }

  function mount(selector, options) {
    var root = typeof selector === 'string' ? document.querySelector(selector) : selector;
    if (!root) return null;
    var o = Object.assign({}, DEF, options || {});

    var row = el('<div class="sn-row" role="navigation" aria-label="Smart Tabs"></div>');
    root.appendChild(row);
    var menu = el('<div class="sn-menu" role="menu"><div class="mi" data-act="edit">✏️ Edit</div><div class="mi" data-act="heart">💜 Set Purple Heart</div><div class="mi" data-act="star">⭐ Set Gold Star</div><div class="mi" data-act="remove">✕ Remove</div></div>');
    var pop = el('<div class="sn-pop" role="dialog"><h3 class="sn-pop-title">Edit Shortcut</h3><div class="row"><label>Label <input class="sn-in-label" placeholder="e.g., The Laws"></label></div><div class="row"><label>Route or #anchor <input class="sn-in-route" placeholder="#laws"></label></div><div class="toggles"><div class="tgl sn-tgl-heart">💜 Purple Heart</div><div class="tgl sn-tgl-star">⭐ Gold Star</div></div><div class="ft"><button class="sn-btn sn-cancel">Cancel</button><button class="sn-btn primary sn-save">Save</button></div></div>');
    document.body.appendChild(menu);
    document.body.appendChild(pop);

    var shortcuts;
    try {
      var s = JSON.parse(localStorage.getItem(o.storageKey));
      shortcuts = (s && Array.isArray(s)) ? s : o.initial.slice();
    } catch (e) { shortcuts = o.initial.slice(); }

    var targetId = null, createMode = false;

    function save() {
      try { localStorage.setItem(o.storageKey, JSON.stringify(shortcuts)); } catch (e) {}
    }

    function resolveRoute(route) {
      return o.routeMap[route] || route;
    }

    function render() {
      row.innerHTML = '';
      shortcuts.slice().sort(function (A, B) {
        return ((B.heart ? 2 : B.star ? 1 : 0) - (A.heart ? 2 : A.star ? 1 : 0));
      }).forEach(function (s) {
        var cls = 'sn-pill' + (s.heart ? ' heart' : (s.star ? ' star' : ''));
        var pill = el('<div class="' + cls + '" data-id="' + s.id + '"><span class="sn-label"></span>' + (s.heart ? '💜' : (s.star ? '⭐' : '')) + ' <button class="sn-more" aria-label="Edit">⋯</button></div>');
        pill.querySelector('.sn-label').textContent = s.label;
        pill.onclick = function (e) {
          if (e.target.classList.contains('sn-more')) return;
          e.preventDefault();
          o.onNavigate(resolveRoute(s.route), s);
        };
        var openMenu = function (e) {
          e.preventDefault();
          targetId = s.id;
          placeNear(pill, menu, 6);
          menu.style.display = 'block';
        };
        pill.oncontextmenu = openMenu;
        pill.querySelector('.sn-more').onclick = openMenu;
        row.appendChild(pill);
      });
      var addBtn = el('<div class="sn-pill add"><span class="sn-label">' + o.addLabel + '</span></div>');
      addBtn.onclick = function (e) {
        e.preventDefault();
        targetId = null;
        createMode = true;
        openEditor(addBtn, { label: '', route: '', heart: false, star: false }, 'Add Shortcut');
      };
      row.appendChild(addBtn);
    }

    function openEditor(anchor, preset, title) {
      pop.querySelector('.sn-pop-title').textContent = title;
      var inLabel = pop.querySelector('.sn-in-label'), inRoute = pop.querySelector('.sn-in-route');
      var tH = pop.querySelector('.sn-tgl-heart'), tS = pop.querySelector('.sn-tgl-star');
      inLabel.value = preset.label || '';
      inRoute.value = preset.route || '';
      tH.classList.toggle('on', !!preset.heart);
      tS.classList.toggle('on', !!preset.star);
      tH.onclick = function () { tH.classList.toggle('on'); if (tH.classList.contains('on')) tS.classList.remove('on'); };
      tS.onclick = function () { tS.classList.toggle('on'); if (tS.classList.contains('on')) tH.classList.remove('on'); };
      placeNear(anchor, pop, 6);
      pop.style.display = 'block';
      pop.querySelector('.sn-cancel').onclick = function () { pop.style.display = 'none'; };
      pop.querySelector('.sn-save').onclick = function () {
        var v = {
          label: (inLabel.value || '').trim() || 'New',
          route: (inRoute.value || '').trim(),
          heart: tH.classList.contains('on'),
          star: tS.classList.contains('on')
        };
        if (v.heart) v.star = false;
        if (v.star) v.heart = false;
        if (createMode) {
          shortcuts.push(Object.assign({ id: 'sc-' + Date.now() }, v));
        } else {
          var i = shortcuts.findIndex(function (x) { return x.id === targetId; });
          if (i >= 0) shortcuts[i] = Object.assign({}, shortcuts[i], v);
        }
        save(); render(); pop.style.display = 'none';
      };
    }

    menu.addEventListener('click', function (e) {
      var mi = e.target.closest('.mi');
      if (!mi) return;
      var act = mi.dataset.act;
      menu.style.display = 'none';
      var i = shortcuts.findIndex(function (x) { return x.id === targetId; });
      if (act === 'edit' && i >= 0) {
        createMode = false;
        openEditor(row.querySelector('[data-id="' + targetId + '"]'), shortcuts[i], 'Edit Shortcut');
      }
      else if (act === 'heart' && i >= 0) { shortcuts[i] = Object.assign({}, shortcuts[i], { heart: true, star: false }); save(); render(); }
      else if (act === 'star' && i >= 0) { shortcuts[i] = Object.assign({}, shortcuts[i], { heart: false, star: true }); save(); render(); }
      else if (act === 'remove' && i >= 0) { shortcuts.splice(i, 1); save(); render(); }
    });

    function closePanels() { menu.style.display = 'none'; pop.style.display = 'none'; }
    document.addEventListener('click', function (e) {
      if (!row.contains(e.target) && !menu.contains(e.target) && !pop.contains(e.target)) closePanels();
    });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closePanels(); });

    render();

    // Public API
    return {
      list: function () { return shortcuts.slice(); },
      set: function (arr) { shortcuts = (arr || []).slice(); save(); render(); },
      add: function (sc) {
        sc = Object.assign({ id: 'sc-' + Date.now() }, sc || {});
        shortcuts.push(sc); save(); render();
        return sc.id;
      },
      remove: function (id) {
        var i = shortcuts.findIndex(function (x) { return x.id === id; });
        if (i >= 0) { shortcuts.splice(i, 1); save(); render(); return true; }
        return false;
      }
    };
  }

  global.SmartTabs = { mount: mount, version: '9.0.0' };
})(typeof window !== 'undefined' ? window : this);
