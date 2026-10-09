/* Smart Block: naya-table — behavior
 * Click-to-sort, ported from the branch wireTables(). Vanilla, no dependencies.
 * <th data-sort="key"> toggles asc/desc; type-aware via data-type="num|date".
 */
(function () {
  function wire(scope) {
    (scope || document).querySelectorAll('table.naya-table[data-sortable]').forEach(function (table) {
      if (table.dataset.wired) return;
      table.dataset.wired = '1';
      var ths = table.querySelectorAll('thead th[data-sort]');
      ths.forEach(function (th) {
        th.setAttribute('tabindex', '0');
        th.setAttribute('role', 'button');
        function go() {
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
            var n1 = parseFloat(String(va).replace(/[^0-9.\-]/g, '')), n2 = parseFloat(String(vb).replace(/[^0-9.\-]/g, ''));
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
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { wire(document); });
  else wire(document);
})();
