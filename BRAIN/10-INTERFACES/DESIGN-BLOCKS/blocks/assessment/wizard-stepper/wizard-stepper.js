/* Smart Block: wizard-stepper — step navigation wiring */

(function () {
  document.querySelectorAll('.wz').forEach(function (root) {
    var steps = Array.prototype.slice.call(root.querySelectorAll('.wz-step'));
    var panels = Array.prototype.slice.call(root.querySelectorAll('.wz-panel'));
    var i = 0;

    function render() {
      steps.forEach(function (s, k) {
        s.classList.toggle('is-now', k === i);
        s.classList.toggle('is-done', k < i);
        var node = s.querySelector('.wz-node');
        if (node) node.setAttribute('aria-current', k === i ? 'step' : 'false');
      });
      panels.forEach(function (p, k) { p.classList.toggle('is-on', k === i); });
      root.dispatchEvent(new CustomEvent('wz:step', { bubbles: true, detail: { step: i, total: steps.length } }));
    }

    root.addEventListener('click', function (e) {
      var back = e.target.closest('[data-wz-back]');
      var next = e.target.closest('[data-wz-next]');
      var node = e.target.closest('.wz-node');
      if (back) { i = Math.max(0, i - 1); render(); }
      else if (next) { i = Math.min(steps.length - 1, i + 1); render(); }
      else if (node) {
        var li = node.closest('.wz-step');
        var k = steps.indexOf(li);
        if (k <= i || li.classList.contains('is-done')) { i = k; render(); }
      }
    });

    render();
  });
})();
