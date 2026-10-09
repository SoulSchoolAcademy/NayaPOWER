/* Smart Block: nl-sw — byte-true from Naya Epic Elements - Lego pieces N5.html */
/* Spectrum demo — click a swatch, the board re-fires */
document.getElementById('swatches').addEventListener('click', function (e) {
  var b = e.target.closest('.sw'); if (!b) return;
  document.getElementById('demoBoard').style.setProperty('--c', b.dataset.c);
  document.getElementById('demoName').textContent = b.dataset.name;
});
/* Orbs are static markup now — no JS needed. */
/* Living buttons — proximity + cursor sheen (160px, rAF-throttled) */
(function () {
  'use strict';
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var els = Array.prototype.slice.call(document.querySelectorAll('.lv-btn'));
  if (!els.length) return;
  var raf = null, lastX = -9999, lastY = -9999;
  function update() {
    raf = null;
    for (var i = 0; i < els.length; i++) {
      var elb = els[i];
      var wrap = elb.closest('.lv-wrap') || elb;
      if (elb.disabled) continue;
      var r = elb.getBoundingClientRect();
      if (r.bottom < -180 || r.top > window.innerHeight + 180) { wrap.classList.remove('lv-aware'); continue; }
      var dx = Math.max(r.left - lastX, 0, lastX - r.right);
      var dy = Math.max(r.top - lastY, 0, lastY - r.bottom);
      var dist = Math.sqrt(dx * dx + dy * dy);
      var aware = dist < 160;
      if (aware !== wrap.classList.contains('lv-aware')) wrap.classList.toggle('lv-aware', aware);
      if (aware || elb.matches(':hover')) {
        elb.style.setProperty('--mx', ((lastX - r.left) / Math.max(r.width, 1) * 100).toFixed(1) + '%');
        elb.style.setProperty('--my', ((lastY - r.top) / Math.max(r.height, 1) * 100).toFixed(1) + '%');
      }
    }
  }
  document.addEventListener('pointermove', function (e) {
    lastX = e.clientX; lastY = e.clientY;
    if (!raf) raf = requestAnimationFrame(update);
  }, { passive: true });
  document.addEventListener('pointerleave', function () {
    els.forEach(function (elb) { (elb.closest('.lv-wrap') || elb).classList.remove('lv-aware'); });
  });
})();
/* SmartTabs demo */
SmartTabs.mount('#smarttabs-demo', {
  storageKey: 'naya_ultimate_smarttabs',
  initial: [
    { id: 'sc-1', label: 'Buttons', route: '#buttons', heart: true, star: false },
    { id: 'sc-2', label: 'SmartTabs', route: '#smarttabs', heart: false, star: true },
    { id: 'sc-3', label: 'Spectrum', route: '#spectrum', heart: false, star: false },
    { id: 'sc-4', label: 'The Laws', route: '#laws', heart: false, star: false }
  ]
});
