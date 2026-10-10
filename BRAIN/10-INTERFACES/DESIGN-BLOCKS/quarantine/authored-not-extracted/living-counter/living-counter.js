/* Smart Block JS: living-counter
 * Count-up on entry. Reads data-to / data-decimals / data-prefix / data-suffix.
 * No dependencies. Honors prefers-reduced-motion (jumps to final).
 */
(function () {
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function format(to, decimals, prefix, suffix) {
    var n = Number(to).toLocaleString('en-US', {
      minimumFractionDigits: decimals, maximumFractionDigits: decimals
    });
    return (prefix || '') + n + (suffix || '');
  }

  function countUp(el) {
    var to = parseFloat(el.getAttribute('data-to') || '0');
    var decimals = parseInt(el.getAttribute('data-decimals') || '0', 10);
    var prefix = el.getAttribute('data-prefix') || '';
    var suffix = el.getAttribute('data-suffix') || '';
    if (reduce) { el.textContent = format(to, decimals, prefix, suffix); return; }
    var dur = 1400, t0 = null;
    function tick(t) {
      if (!t0) t0 = t;
      var p = Math.min(1, (t - t0) / dur);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = format(to * eased, decimals, prefix, suffix);
      if (p < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }

  function watch() {
    var nums = document.querySelectorAll('.lc-num[data-to]');
    if (!('IntersectionObserver' in window)) { nums.forEach(countUp); return; }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          var card = e.target.closest('.sg-card');
          if (card) card.classList.add('lit');
          countUp(e.target);
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.35 });
    nums.forEach(function (n) { io.observe(n); });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', watch);
  else watch();
})();
