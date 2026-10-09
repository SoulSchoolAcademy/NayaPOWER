/* ==========================================================================
   NAYA SMART BLOCKS — canonical behaviors (naya-blocks.js)
   Small, dependency-free utilities shared by every block on the page.
   toast() · copyHTML() · tabs() · sortable tables · ⌘K command palette.
   ========================================================================== */
(function (global) {
  'use strict';

  /* ---------------- Toast (truthful, transient) ---------------- */
  // showToast(message, tone) — tone: 'quiet' | 'verified' | 'claim' | 'demo'
  var toastRoot = null, toastTimer = null;
  function ensureToastRoot() {
    if (!toastRoot) {
      toastRoot = document.createElement('div');
      toastRoot.className = 'naya-toast-root';
      toastRoot.setAttribute('role', 'status');
      toastRoot.setAttribute('aria-live', 'polite');
      document.body.appendChild(toastRoot);
    }
    return toastRoot;
  }
  function toast(msg, tone) {
    var root = ensureToastRoot();
    clearTimeout(toastTimer);
    var t = document.createElement('div');
    t.className = 'naya-toast' + (tone ? ' is-' + tone : '');
    var dot = document.createElement('span');
    dot.className = 'naya-toast-dot';
    var span = document.createElement('span');
    span.className = 'naya-toast-msg';
    span.textContent = msg;
    t.appendChild(dot); t.appendChild(span);
    root.innerHTML = '';
    root.appendChild(t);
    requestAnimationFrame(function () { t.classList.add('show'); });
    toastTimer = setTimeout(function () {
      t.classList.remove('show');
      setTimeout(function () { if (t.parentNode) t.parentNode.removeChild(t); }, 320);
    }, 1800);
  }

  /* ---------------- Copy (code + HTML) ---------------- */
  function copyText(text, label, done) {
    function fallback() {
      var ta = document.createElement('textarea');
      ta.value = text; ta.setAttribute('readonly', '');
      ta.style.position = 'fixed'; ta.style.opacity = '0';
      document.body.appendChild(ta); ta.select();
      var ok = false;
      try { ok = document.execCommand('copy'); } catch (e) { ok = false; }
      document.body.removeChild(ta);
      return ok;
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(function () {
        toast((label || 'Copied') + ' — ready to paste', 'verified');
        if (done) done(true);
      }, function () {
        var ok = fallback();
        toast(ok ? (label || 'Copied') + ' — ready to paste' : 'Copy failed — select it yourself', ok ? 'verified' : 'claim');
        if (done) done(ok);
      });
    } else {
      var ok = fallback();
      toast(ok ? (label || 'Copied') + ' — ready to paste' : 'Copy failed — select it yourself', ok ? 'verified' : 'claim');
      if (done) done(ok);
    }
  }
  // Delegate: any [data-copy-html] button copies the outerHTML of the sibling .block-stage
  function wireCopyButtons(scope) {
    (scope || document).addEventListener('click', function (e) {
      var btn = e.target.closest('[data-copy-html]');
      if (!btn) return;
      var stage = btn.closest('.block-demo') ? btn.closest('.block-demo').querySelector('.block-stage') : null;
      if (!stage) { toast('Nothing to copy here', 'claim'); return; }
      var name = btn.getAttribute('data-copy-html') || 'Block';
      copyText(stage.innerHTML.trim(), name + ' HTML');
      btn.classList.add('copied');
      setTimeout(function () { btn.classList.remove('copied'); }, 1200);
    });
  }

  /* ---------------- Tabs (segmented / pill nav) ---------------- */
  // wireTabs(containerSelector): [role=tablist] with [role=tab] + [data-panel] panes
  function wireTabs(scope) {
    (scope || document).querySelectorAll('[role="tablist"]').forEach(function (list) {
      var tabs = Array.prototype.slice.call(list.querySelectorAll('[role="tab"]'));
      if (!tabs.length || list.dataset.wired) return;
      list.dataset.wired = '1';
      tabs.forEach(function (tab, i) {
        tab.setAttribute('tabindex', tab.getAttribute('aria-selected') === 'true' ? '0' : '-1');
        tab.addEventListener('click', function () { select(i); });
        tab.addEventListener('keydown', function (ev) {
          var j = i;
          if (ev.key === 'ArrowRight' || ev.key === 'ArrowDown') j = (i + 1) % tabs.length;
          else if (ev.key === 'ArrowLeft' || ev.key === 'ArrowUp') j = (i - 1 + tabs.length) % tabs.length;
          else if (ev.key === 'Home') j = 0;
          else if (ev.key === 'End') j = tabs.length - 1;
          else return;
          ev.preventDefault(); select(j); tabs[j].focus();
        });
      });
      function select(j) {
        tabs.forEach(function (t, k) {
          var on = k === j;
          t.setAttribute('aria-selected', on ? 'true' : 'false');
          t.setAttribute('tabindex', on ? '0' : '-1');
          var paneId = t.getAttribute('aria-controls');
          if (paneId) { var pane = document.getElementById(paneId); if (pane) pane.hidden = !on; }
        });
      }
    });
  }

  /* ---------------- Sortable tables ---------------- */
  // wireTables(): <th data-sort> toggles asc/desc; type-aware via data-type="num|date"
  function wireTables(scope) {
    (scope || document).querySelectorAll('table.naya-table[data-sortable]').forEach(function (table) {
      if (table.dataset.wired) return;
      table.dataset.wired = '1';
      var ths = table.querySelectorAll('thead th[data-sort]');
      ths.forEach(function (th) {
        th.setAttribute('tabindex', '0');
        th.setAttribute('role', 'button');
        function go() {
          var key = th.getAttribute('data-sort');
          var idx = Array.prototype.indexOf.call(th.parentNode.children, th);
          var dir = th.getAttribute('aria-sort') === 'ascending' ? -1 : 1;
          ths.forEach(function (o) { o.removeAttribute('aria-sort'); o.classList.remove('sorted'); });
          th.setAttribute('aria-sort', dir === 1 ? 'ascending' : 'descending');
          th.classList.add('sorted');
          var tbody = table.querySelector('tbody');
          var rows = Array.prototype.slice.call(tbody.querySelectorAll('tr'));
          rows.sort(function (a, b) {
            var va = a.children[idx].getAttribute('data-value') || a.children[idx].textContent.trim();
            var vb = b.children[idx].getAttribute('data-value') || b.children[idx].textContent.trim();
            var n1 = parseFloat(va.replace(/[^0-9.\-]/g, '')), n2 = parseFloat(vb.replace(/[^0-9.\-]/g, ''));
            var cmp = (!isNaN(n1) && !isNaN(n2) && String(n1).length > 1) ? n1 - n2 : String(va).localeCompare(String(vb));
            return cmp * dir;
          });
          rows.forEach(function (r) { tbody.appendChild(r); });
        }
        th.addEventListener('click', go);
        th.addEventListener('keydown', function (ev) { if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); go(); } });
      });
    });
  }

  /* ---------------- ⌘K command palette ---------------- */
  // wirePalette({ items: [{label, hint, run}], openKey })
  function wirePalette(opts) {
    var o = Object.assign({ items: [], openHint: '⌘K' }, opts || {});
    var backdrop = document.createElement('div');
    backdrop.className = 'naya-palette-backdrop';
    backdrop.hidden = true;
    var panel = document.createElement('div');
    panel.className = 'naya-palette';
    panel.setAttribute('role', 'dialog');
    panel.setAttribute('aria-label', 'Command palette');
    panel.innerHTML =
      '<div class="naya-palette-search">' +
      '<svg viewBox="0 0 16 16" width="16" height="16" aria-hidden="true"><circle cx="7" cy="7" r="5" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M11 11l3.5 3.5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>' +
      '<input class="naya-palette-input" type="text" placeholder="Ask Naya, or jump somewhere…" autocomplete="off" spellcheck="false">' +
      '<span class="naya-kbd">esc</span></div>' +
      '<div class="naya-palette-list" role="listbox"></div>';
    backdrop.appendChild(panel);
    document.body.appendChild(backdrop);
    var input = panel.querySelector('.naya-palette-input');
    var list = panel.querySelector('.naya-palette-list');
    var cursor = 0, filtered = [];

    function render() {
      list.innerHTML = '';
      cursor = Math.min(cursor, Math.max(0, filtered.length - 1));
      filtered.forEach(function (item, i) {
        var row = document.createElement('div');
        row.className = 'naya-palette-item' + (i === cursor ? ' active' : '');
        row.setAttribute('role', 'option');
        row.setAttribute('aria-selected', i === cursor ? 'true' : 'false');
        var label = document.createElement('span'); label.className = 'naya-palette-label'; label.textContent = item.label;
        row.appendChild(label);
        if (item.hint) { var h = document.createElement('span'); h.className = 'naya-palette-hint'; h.textContent = item.hint; row.appendChild(h); }
        row.addEventListener('click', function () { choose(i); });
        list.appendChild(row);
      });
      if (!filtered.length) {
        var empty = document.createElement('div');
        empty.className = 'naya-palette-empty';
        empty.textContent = 'Nothing matches — yet. Naya is always learning.';
        list.appendChild(empty);
      }
    }
    function applyFilter() {
      var q = input.value.trim().toLowerCase();
      filtered = o.items.filter(function (it) {
        return !q || it.label.toLowerCase().indexOf(q) !== -1 || (it.hint && it.hint.toLowerCase().indexOf(q) !== -1);
      });
      cursor = 0; render();
    }
    function choose(i) {
      var item = filtered[i];
      if (!item) return;
      close();
      if (typeof item.run === 'function') item.run();
    }
    function open() {
      backdrop.hidden = false;
      input.value = ''; applyFilter();
      requestAnimationFrame(function () { input.focus(); });
    }
    function close() { backdrop.hidden = true; }
    document.addEventListener('keydown', function (e) {
      var mod = e.metaKey || e.ctrlKey;
      if (mod && e.key.toLowerCase() === 'k') { e.preventDefault(); backdrop.hidden ? open() : close(); }
      if (!backdrop.hidden && e.key === 'Escape') close();
    });
    input.addEventListener('input', applyFilter);
    input.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowDown') { e.preventDefault(); cursor = Math.min(cursor + 1, filtered.length - 1); render(); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); cursor = Math.max(cursor - 1, 0); render(); }
      else if (e.key === 'Enter') { e.preventDefault(); choose(cursor); }
    });
    backdrop.addEventListener('click', function (e) { if (e.target === backdrop) close(); });
    return { open: open, close: close, setItems: function (items) { o.items = items; } };
  }

  /* ---------------- Segmented demo behavior (CSS-only markup helper) ---------------- */
  function init(scope) {
    wireCopyButtons(scope);
    wireTabs(scope);
    wireTables(scope);
  }

  global.NayaBlocks = {
    toast: toast,
    copyText: copyText,
    wireTabs: wireTabs,
    wireTables: wireTables,
    wirePalette: wirePalette,
    init: init,
    version: '1.0.0'
  };
})(typeof window !== 'undefined' ? window : this);
