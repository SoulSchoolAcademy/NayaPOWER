/* eco-dock.js — toggle the central plus menu: aria-expanded, Escape + outside close. */
(function () {
  'use strict';

  var dock = document.querySelector('.eco-dock');
  if (!dock) return;

  var plus = dock.querySelector('.eco-plus');
  var menu = dock.querySelector('.eco-menu');
  if (!plus || !menu) return;

  function setOpen(open) {
    plus.setAttribute('aria-expanded', String(open));
  }

  function isOpen() {
    return plus.getAttribute('aria-expanded') === 'true';
  }

  plus.addEventListener('click', function () {
    setOpen(!isOpen());
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && isOpen()) {
      setOpen(false);
      plus.focus();
    }
  });

  document.addEventListener('pointerdown', function (e) {
    if (isOpen() && !dock.contains(e.target)) {
      setOpen(false);
    }
  });

  menu.addEventListener('click', function (e) {
    var action = e.target.closest('button[data-action]');
    if (action) {
      setOpen(false);
      dock.dispatchEvent(new CustomEvent('eco:action', {
        bubbles: true,
        detail: { action: action.getAttribute('data-action') }
      }));
    }
  });

  /* quick-switcher active state: click sets .is-active (demo default; app router owns this in production) */
  dock.querySelectorAll('.eco-item').forEach(function (item) {
    item.addEventListener('click', function () {
      dock.querySelectorAll('.eco-item.is-active').forEach(function (el) {
        el.classList.remove('is-active');
        el.removeAttribute('aria-current');
      });
      item.classList.add('is-active');
      item.setAttribute('aria-current', 'page');
    });
  });
})();
