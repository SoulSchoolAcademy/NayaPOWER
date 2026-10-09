/* Smart Block: lv-ambient — byte-true from Naya  Elite Buttons N5.html */
/* ==========================================================================
   LIVING.JS — proximity awareness for the living system
   One system, no forks. Buttons AND boards share it.
   - 160px proximity → .lv-aware (wake up before touch)
   - --mx/--my → cursor light position on the element
   - --lx/--ly + body.lv-lit → the page receives the element's light
   ========================================================================== */
(function () {
  'use strict';
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  var els = Array.prototype.slice.call(document.querySelectorAll('.lv-btn, .lv-board'));
  if (!els.length) return;

  /* ambient wash layer — the page catching the light */
  var ambient = document.createElement('div');
  ambient.className = 'lv-ambient';
  ambient.setAttribute('aria-hidden', 'true');
  document.body.appendChild(ambient);

  var raf = null, lastX = -9999, lastY = -9999;

  function accentOf(el) {
    var wrap = el.closest('.lv-wrap');
    var src = wrap || el;
    var rgb = getComputedStyle(src).getPropertyValue('--lv-accent-rgb').trim();
    return rgb || '160,107,255';
  }

  function update() {
    raf = null;
    var lit = false, best = null, bestDist = 1e9;
    for (var i = 0; i < els.length; i++) {
      var el = els[i];
      var wrap = el.classList.contains('lv-btn') ? (el.closest('.lv-wrap') || el) : el;
      if (el.disabled) continue;
      var r = el.getBoundingClientRect();
      if (r.bottom < -180 || r.top > window.innerHeight + 180) {
        wrap.classList.remove('lv-aware'); continue;
      }
      var dx = Math.max(r.left - lastX, 0, lastX - r.right);
      var dy = Math.max(r.top - lastY, 0, lastY - r.bottom);
      var dist = Math.sqrt(dx * dx + dy * dy);
      var aware = dist < 160;
      var was = wrap.classList.contains('lv-aware');
      if (aware !== was) wrap.classList.toggle('lv-aware', aware);
      if (aware || el.matches(':hover')) {
        var mx = ((lastX - r.left) / Math.max(r.width, 1) * 100);
        var my = ((lastY - r.top) / Math.max(r.height, 1) * 100);
        el.style.setProperty('--mx', mx.toFixed(1) + '%');
        el.style.setProperty('--my', my.toFixed(1) + '%');
      }
      if (aware && dist < bestDist) { bestDist = dist; best = el; }
      if (el.matches(':hover')) { best = el; bestDist = -1; lit = true; }
    }
    if (best) {
      lit = true;
      document.documentElement.style.setProperty('--lv-wash-rgb', accentOf(best));
      document.documentElement.style.setProperty('--lx', lastX + 'px');
      document.documentElement.style.setProperty('--ly', lastY + 'px');
    }
    document.body.classList.toggle('lv-lit', lit);
  }

  document.addEventListener('pointermove', function (e) {
    lastX = e.clientX; lastY = e.clientY;
    if (!raf) raf = requestAnimationFrame(update);
  }, { passive: true });

  document.addEventListener('pointerleave', function () {
    lastX = -9999; lastY = -9999;
    els.forEach(function (el) {
      var wrap = el.classList.contains('lv-btn') ? (el.closest('.lv-wrap') || el) : el;
      wrap.classList.remove('lv-aware');
    });
    document.body.classList.remove('lv-lit');
  });

  /* touch: brief wake flash */
  els.forEach(function (el) {
    el.addEventListener('touchstart', function () {
      var wrap = el.classList.contains('lv-btn') ? (el.closest('.lv-wrap') || el) : el;
      wrap.classList.add('lv-aware');
      setTimeout(function () { wrap.classList.remove('lv-aware'); }, 600);
    }, { passive: true });
  });
})();
