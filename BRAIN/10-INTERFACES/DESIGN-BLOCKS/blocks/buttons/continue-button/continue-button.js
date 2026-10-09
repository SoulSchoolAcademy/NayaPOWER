/* Smart Block: continue-button — the assessment continue CTA.
   Watches each `.continue-button` for the disabled→enabled transition and
   plays the one-time `.ready` breath: the moment continuing becomes possible,
   the button says so. Purely presentational — it never changes disabled state. */
(function () {
  'use strict';

  function breathe(btn) {
    btn.classList.remove('ready');
    // Restart the animation if it is already mid-breath.
    void btn.offsetWidth;
    btn.classList.add('ready');
  }

  function arm(btn) {
    if (btn._cbArmed) { return; }
    btn._cbArmed = true;
    if (typeof MutationObserver === 'function') {
      var obs = new MutationObserver(function (mutations) {
        for (var i = 0; i < mutations.length; i++) {
          if (mutations[i].attributeName === 'disabled' && !btn.disabled) {
            breathe(btn);
          }
        }
      });
      obs.observe(btn, { attributes: true, attributeFilter: ['disabled'] });
    }
    btn.addEventListener('animationend', function (event) {
      if (event.animationName === 'cb-ready') {
        btn.classList.remove('ready');
      }
    });
  }

  function armAll() {
    Array.prototype.slice.call(
      document.querySelectorAll('.continue-button')
    ).forEach(arm);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', armAll);
  } else {
    armAll();
  }

  window.ContinueButton = {
    arm: arm,
    armAll: armAll,
    breathe: breathe
  };
})();
