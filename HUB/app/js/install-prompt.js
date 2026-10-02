/* INSTALL PROMPT — the "install the app" reminder, living inside the Hub.
   It pops up until the app is actually installed, then goes away for good.
   - Captures beforeinstallprompt and holds it for the Install button.
   - appinstalled + standalone display-mode set the permanent installed flag.
   - Dismissing ("Not now" / ×) hides it for this session only — it does
     NOT count as installed, so the reminder returns next visit.
   - Where the platform offers no install prompt (e.g. iOS Safari), the
     pop-up shows the honest manual steps instead of a dead button. */

(function () {
  'use strict';

  var LS_INSTALLED = 'nayanet.appInstalled.v1';
  var deferredPrompt = null;
  var dismissedThisSession = false;

  function isInstalled() {
    try { if (localStorage.getItem(LS_INSTALLED) === '1') return true; } catch (e) {}
    try {
      if (window.matchMedia && window.matchMedia('(display-mode: standalone)').matches) return true;
      if (window.navigator.standalone === true) return true; /* iOS home-screen web app */
    } catch (e) {}
    return false;
  }

  function markInstalled() {
    try { localStorage.setItem(LS_INSTALLED, '1'); } catch (e) {}
    var n = document.querySelector('.install-pop');
    if (n) n.remove();
  }

  /* Capture early — the event fires on page load, before maybeShow runs. */
  window.addEventListener('beforeinstallprompt', function (e) {
    e.preventDefault();
    deferredPrompt = e;
  });
  window.addEventListener('appinstalled', markInstalled);

  function maybeShow() {
    if (isInstalled() || dismissedThisSession) return;
    if (document.querySelector('.install-pop')) return;
    var shown = false;
    function show() {
      if (shown) return;
      shown = true;
      /* A short beat so the Hub lands before the reminder appears. */
      setTimeout(render, 1400);
    }
    if (deferredPrompt) { show(); return; }
    /* Give the platform a moment to offer its install prompt; otherwise
       fall back to the honest manual instructions. */
    function onPrompt() {
      window.removeEventListener('beforeinstallprompt', onPrompt);
      show();
    }
    window.addEventListener('beforeinstallprompt', onPrompt);
    setTimeout(function () {
      window.removeEventListener('beforeinstallprompt', onPrompt);
      show();
    }, 2800);
  }

  function render() {
    if (isInstalled() || dismissedThisSession) return;
    if (document.querySelector('.install-pop')) return;
    var native = !!deferredPrompt;

    var overlay = document.createElement('div');
    overlay.className = 'install-pop';
    overlay.setAttribute('role', 'dialog');
    overlay.setAttribute('aria-modal', 'true');
    overlay.setAttribute('aria-label', 'Install the NayaNET app');
    overlay.innerHTML =
      '<div class="install-card">' +
        '<button type="button" class="install-x" aria-label="Not now">×</button>' +
        '<div class="install-gem" aria-hidden="true">◇</div>' +
        '<h2>Install the NayaNET app</h2>' +
        '<p>' + (native
          ? 'Add the Intelligent Hub to your home screen for one-tap entry.'
          : 'Add the Intelligent Hub to your home screen: open your browser\u2019s share menu and choose \u201CAdd to Home Screen\u201D.') + '</p>' +
        '<div class="install-actions">' +
          (native ? '<button type="button" class="install-go">Install app</button>' : '') +
          '<button type="button" class="install-later">Not now</button>' +
        '</div>' +
      '</div>';

    function dismiss() {
      dismissedThisSession = true; /* session only — the reminder returns next visit */
      overlay.remove();
    }
    overlay.querySelector('.install-x').addEventListener('click', dismiss);
    overlay.querySelector('.install-later').addEventListener('click', dismiss);
    overlay.addEventListener('click', function (e) { if (e.target === overlay) dismiss(); });

    var go = overlay.querySelector('.install-go');
    if (go) go.addEventListener('click', function () {
      if (!deferredPrompt) return;
      var p = deferredPrompt;
      deferredPrompt = null;
      try {
        p.prompt();
        if (p.userChoice && p.userChoice.then) {
          p.userChoice.then(function (choice) {
            if (choice && choice.outcome === 'accepted') markInstalled();
          }).catch(function () {});
        }
      } catch (e) {}
    });

    document.body.appendChild(overlay);
    var focusTarget = go || overlay.querySelector('.install-later');
    if (focusTarget) focusTarget.focus();
  }

  window.NayaInstallPrompt = {
    maybeShow: maybeShow,
    markInstalled: markInstalled,
    isInstalled: isInstalled
  };
})();
