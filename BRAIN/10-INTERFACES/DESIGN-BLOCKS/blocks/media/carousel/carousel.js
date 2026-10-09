/* Smart Block: carousel — slide wiring (arrows, dots, swipe, autoplay) */

(function () {
  document.querySelectorAll('.cr').forEach(function (root) {
    var track = root.querySelector('.cr-track');
    var slides = Array.prototype.slice.call(root.querySelectorAll('.cr-slide'));
    var dots = Array.prototype.slice.call(root.querySelectorAll('.cr-dot'));
    var prev = root.querySelector('.cr-prev');
    var next = root.querySelector('.cr-next');
    var i = 0, timer = null;
    var autoplay = root.hasAttribute('data-autoplay');
    var delay = parseInt(root.getAttribute('data-autoplay') || '5000', 10);

    function go(n) {
      i = (n + slides.length) % slides.length;
      track.style.transform = 'translateX(' + (-i * 100) + '%)';
      dots.forEach(function (d, k) { d.classList.toggle('is-on', k === i); });
      root.dispatchEvent(new CustomEvent('cr:change', { bubbles: true, detail: { index: i } }));
    }
    function stop() { if (timer) { clearInterval(timer); timer = null; } }
    function start() { if (autoplay && !timer) timer = setInterval(function () { go(i + 1); }, delay); }

    if (prev) prev.addEventListener('click', function () { stop(); go(i - 1); start(); });
    if (next) next.addEventListener('click', function () { stop(); go(i + 1); start(); });
    dots.forEach(function (d, k) { d.addEventListener('click', function () { stop(); go(k); start(); }); });

    // Touch swipe
    var x0 = null;
    root.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; stop(); }, { passive: true });
    root.addEventListener('touchend', function (e) {
      if (x0 === null) return;
      var dx = e.changedTouches[0].clientX - x0;
      if (Math.abs(dx) > 40) go(i + (dx < 0 ? 1 : -1));
      x0 = null; start();
    }, { passive: true });

    root.addEventListener('mouseenter', stop);
    root.addEventListener('mouseleave', start);

    go(0); start();
  });
})();
