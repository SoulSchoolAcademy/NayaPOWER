/* Smart Block JS: eco-bottombar
 * Specimen wiring for the .eco-menu open state (mirrors Hub semantics:
 * .eco-plus[aria-expanded] toggles .eco-menu.open).
 */
(function () {
  var plus = document.getElementById('demo-plus');
  var menu = document.getElementById('demo-eco-menu');
  if (!plus || !menu) return;
  plus.addEventListener('click', function () {
    var open = plus.getAttribute('aria-expanded') === 'true';
    plus.setAttribute('aria-expanded', String(!open));
    menu.classList.toggle('open', !open);
  });
})();
