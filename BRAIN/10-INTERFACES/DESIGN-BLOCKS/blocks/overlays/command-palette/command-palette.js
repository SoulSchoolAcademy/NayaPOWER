/* Smart Block: command-palette — ⌘K wiring (filter, keyboard nav, actions) */

(function () {
  document.querySelectorAll('.cp').forEach(function (palette) {
    var backdrop = document.querySelector('.cp-backdrop');
    var input = palette.querySelector('.cp-input');
    var items = Array.prototype.slice.call(palette.querySelectorAll('.cp-item'));
    var none = palette.querySelector('.cp-none');
    var active = 0;

    function open() {
      palette.classList.add('is-on');
      if (backdrop) backdrop.classList.add('is-on');
      if (input) { input.value = ''; filter(''); input.focus(); }
    }
    function close() {
      palette.classList.remove('is-on');
      if (backdrop) backdrop.classList.remove('is-on');
    }
    function isOpen() { return palette.classList.contains('is-on'); }

    function visible() { return items.filter(function (el) { return el.style.display !== 'none'; }); }

    function filter(q) {
      q = q.trim().toLowerCase();
      var n = 0;
      items.forEach(function (el) {
        var hit = !q || el.textContent.toLowerCase().indexOf(q) > -1;
        el.style.display = hit ? '' : 'none';
        if (hit) n++;
      });
      if (none) none.style.display = n ? 'none' : '';
      active = 0;
      paint();
    }

    function paint() {
      var v = visible();
      v.forEach(function (el, k) { el.classList.toggle('is-active', k === active); });
      if (v[active]) v[active].scrollIntoView({ block: 'nearest' });
    }

    function run(el) {
      if (!el) return;
      close();
      palette.dispatchEvent(new CustomEvent('cp:run', {
        bubbles: true,
        detail: { action: el.dataset.action, label: el.querySelector('.cp-label').textContent.trim() }
      }));
    }

    if (input) input.addEventListener('input', function () { filter(input.value); });
    if (input) input.addEventListener('keydown', function (e) {
      var v = visible();
      if (e.key === 'ArrowDown') { e.preventDefault(); active = Math.min(v.length - 1, active + 1); paint(); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); active = Math.max(0, active - 1); paint(); }
      else if (e.key === 'Enter') { run(v[active]); }
      else if (e.key === 'Escape') { close(); }
    });

    palette.addEventListener('click', function (e) {
      var el = e.target.closest('.cp-item');
      if (el) run(el);
    });
    if (backdrop) backdrop.addEventListener('click', close);

    // Global ⌘K / Ctrl+K
    document.addEventListener('keydown', function (e) {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        isOpen() ? close() : open();
      }
      if (e.key === 'Escape' && isOpen()) close();
    });

    // Expose opener
    palette._cpOpen = open;
    filter('');
  });
})();
