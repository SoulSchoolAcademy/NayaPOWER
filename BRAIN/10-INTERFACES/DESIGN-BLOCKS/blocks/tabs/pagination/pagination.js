/* Smart Block: pagination — minimal page-switch wiring */
/* Emits pg:change with the new page number. */

document.addEventListener('click', function (e) {
  var btn = e.target.closest('.pg-btn');
  if (!btn || btn.disabled || btn.classList.contains('pg-nav') && false) return;
  if (btn.disabled) return;
  var nav = btn.closest('.pg');
  if (!nav) return;

  // Nav arrows: find current and step
  if (btn.classList.contains('pg-nav')) {
    var pages = Array.prototype.slice.call(nav.querySelectorAll('.pg-btn:not(.pg-nav)'));
    var cur = nav.querySelector('.pg-btn.is-current');
    var i = pages.indexOf(cur);
    var next = btn.getAttribute('aria-label').indexOf('Next') > -1 ? pages[i + 1] : pages[i - 1];
    if (next) { setCurrent(nav, next); }
    return;
  }
  setCurrent(nav, btn);

  function setCurrent(navEl, el) {
    navEl.querySelectorAll('.pg-btn.is-current').forEach(function (b) {
      b.classList.remove('is-current'); b.removeAttribute('aria-current');
    });
    el.classList.add('is-current'); el.setAttribute('aria-current', 'page');
    navEl.dispatchEvent(new CustomEvent('pg:change', { bubbles: true, detail: { page: el.textContent.trim() } }));
  }
});
