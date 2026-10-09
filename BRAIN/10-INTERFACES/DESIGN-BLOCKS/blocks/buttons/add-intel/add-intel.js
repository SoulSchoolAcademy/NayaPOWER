/* add-intel.js — wires every .add-intel entry point to the composer.
   Clicking the pill dispatches a bubbling CustomEvent('add-intel:open') on the button
   so any page can open its composer without touching this file:
     document.addEventListener('add-intel:open', e => openComposer(e.detail.source));
   Event delegation: buttons added to the DOM later work automatically. */
(function () {
  'use strict';

  document.addEventListener('click', function (e) {
    var el = (e.target && e.target.closest) ? e.target.closest('.add-intel') : null;
    if (!el) return;
    el.dispatchEvent(new CustomEvent('add-intel:open', {
      bubbles: true,
      detail: { source: el }
    }));
  });
})();
