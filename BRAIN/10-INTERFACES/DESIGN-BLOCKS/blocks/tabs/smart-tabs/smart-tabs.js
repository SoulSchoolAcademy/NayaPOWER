/* Smart Block JS: smart-tabs
 * Specimen wiring: single-select tab behavior matching .active semantics.
 * (The Hub's full tab-pop editor is app logic; the popover shell ships in CSS.)
 */
(function () {
  document.querySelectorAll('.smart-tabs').forEach(function (bar) {
    bar.addEventListener('click', function (e) {
      if (e.target.closest('.sn-more')) return;
      var tab = e.target.closest('.smart-tab');
      if (!tab) return;
      bar.querySelectorAll('.smart-tab').forEach(function (t) {
        t.classList.remove('active');
        t.setAttribute('aria-selected', 'false');
      });
      tab.classList.add('active');
      tab.setAttribute('aria-selected', 'true');
    });
  });
})();
