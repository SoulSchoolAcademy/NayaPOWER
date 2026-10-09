/* Smart Block: cookie-banner — show/dismiss + consent persistence */

(function () {
  var KEY = 'naya-consent';
  document.querySelectorAll('.ck').forEach(function (banner) {
    var accept = banner.querySelector('[data-ck-accept]');
    var decline = banner.querySelector('[data-ck-decline]');

    function hide(choice) {
      try { localStorage.setItem(KEY, JSON.stringify({ choice: choice, at: new Date().toISOString() })); } catch (e) {}
      banner.classList.remove('is-on');
      banner.dispatchEvent(new CustomEvent('ck:choice', { bubbles: true, detail: { choice: choice } }));
    }

    var stored = null;
    try { stored = localStorage.getItem(KEY); } catch (e) {}
    if (!stored) {
      // Small delay so it doesn't fight the page entrance
      setTimeout(function () { banner.classList.add('is-on'); }, 900);
    }
    if (accept) accept.addEventListener('click', function () { hide('accepted'); });
    if (decline) decline.addEventListener('click', function () { hide('declined'); });
  });
})();
