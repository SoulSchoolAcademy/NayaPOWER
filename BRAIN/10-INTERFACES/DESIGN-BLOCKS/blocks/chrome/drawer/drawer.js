/* Smart Block JS: drawer
 * Source: Naya Smart Hub Design.html — openDrawer()/closeDrawer() verbatim.
 */
(function () {
  var shell = document.getElementById('demo-shell');
  var btn = document.getElementById('demo-drawer-btn');
  var backdrop = document.getElementById('demo-backdrop');
  if (!shell || !btn) return;
  function openDrawer() {
    shell.classList.add('drawer-open');
    document.body.classList.add('drawer-open');
    btn.setAttribute('aria-expanded', 'true');
  }
  function closeDrawer() {
    shell.classList.remove('drawer-open');
    document.body.classList.remove('drawer-open');
    btn.setAttribute('aria-expanded', 'false');
  }
  btn.addEventListener('click', function () {
    shell.classList.contains('drawer-open') ? closeDrawer() : openDrawer();
  });
  if (backdrop) backdrop.addEventListener('click', closeDrawer);
})();
