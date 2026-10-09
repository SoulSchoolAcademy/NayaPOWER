/* Smart Block: data/accordion — toggle, single-open mode, animated height */
(function () {
  'use strict';

  function closeItem(item) {
    var body = item.querySelector('.acc-body');
    var head = item.querySelector('.acc-head');
    item.classList.remove('acc-open');
    if (body) body.style.maxHeight = '0px';
    if (head) head.setAttribute('aria-expanded', 'false');
  }

  function openItem(item) {
    var body = item.querySelector('.acc-body');
    var head = item.querySelector('.acc-head');
    item.classList.add('acc-open');
    if (body) body.style.maxHeight = body.scrollHeight + 'px';
    if (head) head.setAttribute('aria-expanded', 'true');
  }

  function init(root) {
    var items = root.querySelectorAll('.acc-item');
    var single = root.hasAttribute('data-single');

    for (var i = 0; i < items.length; i++) {
      (function (item) {
        var head = item.querySelector('.acc-head');
        var body = item.querySelector('.acc-body');
        if (!head || !body) return;

        head.setAttribute('aria-expanded', item.classList.contains('acc-open') ? 'true' : 'false');

        head.addEventListener('click', function () {
          var isOpen = item.classList.contains('acc-open');
          if (single && !isOpen) {
            for (var j = 0; j < items.length; j++) {
              if (items[j] !== item) closeItem(items[j]);
            }
          }
          if (isOpen) closeItem(item); else openItem(item);
          root.dispatchEvent(new CustomEvent('acc-toggle', {
            bubbles: true,
            detail: { open: !isOpen, item: item }
          }));
        });
      })(items[i]);
    }

    // Pre-opened items: size the animated height
    for (var k = 0; k < items.length; k++) {
      if (items[k].classList.contains('acc-open')) openItem(items[k]);
    }

    // Re-size open bodies when the window changes (e.g. 360px → desktop)
    window.addEventListener('resize', function () {
      for (var m = 0; m < items.length; m++) {
        if (items[m].classList.contains('acc-open')) {
          var b = items[m].querySelector('.acc-body');
          if (b) b.style.maxHeight = b.scrollHeight + 'px';
        }
      }
    });
  }

  function boot() {
    var roots = document.querySelectorAll('[data-acc]');
    for (var i = 0; i < roots.length; i++) init(roots[i]);
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
