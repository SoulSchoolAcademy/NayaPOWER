/* Smart Block JS: lv-btn
 * Source: Naya_5_Beautiful_Button_set.html
 */

function copyCode(id) {
  const el = document.getElementById(id);
  navigator.clipboard.writeText(el.innerText).then(() => {
    const btn = event.target; const old = btn.textContent;
    btn.textContent = 'Copied ✓'; setTimeout(() => btn.textContent = old, 1600);
  });
}
/* Living system JS — proximity + cursor sheen (160px, rAF-throttled) */
(function () {
  'use strict';
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var els = Array.prototype.slice.call(document.querySelectorAll('.lv-btn, .seg-tab, .like-pill, .act-chip, .tog-chip, .day-dot, .send-cta'));
  if (!els.length) return;
  var raf = null, lastX = -9999, lastY = -9999;
  function update() {
    raf = null;
    for (var i = 0; i < els.length; i++) {
      var el = els[i];
      var wrap = el.closest('.lv-wrap') || el;
      if (el.disabled) continue;
      var r = el.getBoundingClientRect();
      if (r.bottom < -180 || r.top > window.innerHeight + 180) { wrap.classList.remove('lv-aware'); continue; }
      var dx = Math.max(r.left - lastX, 0, lastX - r.right);
      var dy = Math.max(r.top - lastY, 0, lastY - r.bottom);
      var dist = Math.sqrt(dx * dx + dy * dy);
      var aware = dist < 160;
      if (aware !== wrap.classList.contains('lv-aware')) wrap.classList.toggle('lv-aware', aware);
      if (aware || el.matches(':hover')) {
        el.style.setProperty('--mx', ((lastX - r.left) / Math.max(r.width, 1) * 100).toFixed(1) + '%');
        el.style.setProperty('--my', ((lastY - r.top) / Math.max(r.height, 1) * 100).toFixed(1) + '%');
      }
    }
  }
  document.addEventListener('pointermove', function (e) {
    lastX = e.clientX; lastY = e.clientY;
    if (!raf) raf = requestAnimationFrame(update);
  }, { passive: true });
  document.addEventListener('pointerleave', function () {
    els.forEach(function (el) { (el.closest('.lv-wrap') || el).classList.remove('lv-aware'); });
  });
})();