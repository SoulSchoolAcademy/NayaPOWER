/* Smart Block JS: lens-tabs
 * Specimen wiring: single-select lens behavior matching .active semantics.
 */
(function () {
  document.querySelectorAll('.lens-tabs').forEach(function (bar) {
    bar.addEventListener('click', function (e) {
      var tab = e.target.closest('.lens-tab');
      if (!tab) return;
      bar.querySelectorAll('.lens-tab').forEach(function (t) {
        t.classList.remove('active');
        t.setAttribute('aria-selected', 'false');
      });
      tab.classList.add('active');
      tab.setAttribute('aria-selected', 'true');
    });
  });
})();
