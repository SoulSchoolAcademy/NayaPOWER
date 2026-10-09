/* Smart Block: naya-drawer — behavior
 * Vanilla open/close: no framework, no NayaBlocks dependency.
 */
(function () {
  function wire(scope) {
    (scope || document).querySelectorAll('[data-drawer-open]').forEach(function (btn) {
      var id = btn.getAttribute('data-drawer-open');
      var drawer = document.getElementById(id);
      if (!drawer || btn.dataset.wired) return;
      btn.dataset.wired = '1';
      var backdrop = drawer.previousElementSibling;
      function open() {
        drawer.hidden = false;
        if (backdrop && backdrop.classList.contains('naya-drawer-backdrop')) backdrop.hidden = false;
        btn.setAttribute('aria-expanded', 'true');
      }
      function close() {
        drawer.hidden = true;
        if (backdrop && backdrop.classList.contains('naya-drawer-backdrop')) backdrop.hidden = true;
        btn.setAttribute('aria-expanded', 'false');
      }
      btn.addEventListener('click', open);
      drawer.querySelectorAll('[data-drawer-close]').forEach(function (c) { c.addEventListener('click', close); });
      if (backdrop && backdrop.classList.contains('naya-drawer-backdrop')) backdrop.addEventListener('click', close);
      document.addEventListener('keydown', function (ev) { if (ev.key === 'Escape' && !drawer.hidden) close(); });
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { wire(document); });
  else wire(document);
})();
