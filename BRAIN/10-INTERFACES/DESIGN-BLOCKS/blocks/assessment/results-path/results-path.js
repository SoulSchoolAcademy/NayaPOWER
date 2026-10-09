/* Smart Block: results-path — the results journey reveal.
   Phases arrive in stages via IntersectionObserver (`.revealed`), and the
   score number counts up to its final value. Reduced motion gets the final
   state instantly — the arrival is a courtesy, never a gate. */
(function () {
  'use strict';

  var REDUCED = window.matchMedia &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function revealPhase(phase) {
    if (phase.classList.contains('revealed')) { return; }
    phase.classList.add('revealed');
    // Count the score up once its phase arrives.
    var num = phase.querySelector('.score-number[data-count-to]');
    if (num && !num._counted) {
      num._counted = true;
      countUp(num, parseInt(num.getAttribute('data-count-to'), 10) || 0);
    }
  }

  function countUp(el, target) {
    if (REDUCED) {
      el.textContent = String(target);
      return;
    }
    var duration = 1100;
    var start = null;
    function frame(now) {
      if (start === null) { start = now; }
      var t = Math.min((now - start) / duration, 1);
      // easeOutCubic — fast start, gentle landing.
      var eased = 1 - Math.pow(1 - t, 3);
      el.textContent = String(Math.round(eased * target));
      if (t < 1) { requestAnimationFrame(frame); }
    }
    requestAnimationFrame(frame);
  }

  function observe() {
    var phases = Array.prototype.slice.call(
      document.querySelectorAll('.results-path .results-phase')
    );
    if (!phases.length) { return; }
    if (REDUCED || !('IntersectionObserver' in window)) {
      phases.forEach(revealPhase);
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          revealPhase(entry.target);
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.18 });
    phases.forEach(function (phase) { io.observe(phase); });
  }

  function revealAll() {
    Array.prototype.slice.call(
      document.querySelectorAll('.results-path .results-phase')
    ).forEach(revealPhase);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', observe);
  } else {
    observe();
  }

  window.ResultsPath = {
    reveal: revealPhase,
    revealAll: revealAll,
    reobserve: observe
  };
})();
