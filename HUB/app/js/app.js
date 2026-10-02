/* APP — boot.
   Entry lives OUTSIDE the app now:
     WELCOME (the marketing front door) → IDENTITY → INTELLIGENT HUB.

   The Hub keeps the visitor logged in on this device/browser:
   a stored identity boots straight into the Hub; no identity sends
   the visitor back to the front door. The identity is a remembered
   device-local profile (name + smart alias) — never a verified
   credential, and the interface must never claim otherwise. */

(function () {
  'use strict';

  /* ——— The one deployment seam ———
     WELCOME_URL: the canonical front door. The identity handoff
     arrives as ?name=…&alias=… (consumed once, then scrubbed). */
  var WELCOME_URL = 'https://welcome.nayanet.app/';
  var LS_IDENTITY = 'nayanet.identity.v1';

  function readIdentity() {
    try {
      var raw = localStorage.getItem(LS_IDENTITY);
      if (!raw) return null;
      var id = JSON.parse(raw);
      return (id && (id.name || id.alias)) ? id : null;
    } catch (e) { return null; }
  }

  function writeIdentity(id) {
    try { localStorage.setItem(LS_IDENTITY, JSON.stringify(id)); } catch (e) {}
  }

  /* One-time handoff from the identity page. Consumed, stored, then
     scrubbed from the address bar so it can't be bookmarked or
     forwarded with someone else's name in it. */
  function consumeHandoff() {
    var q;
    try { q = new URLSearchParams(location.search); } catch (e) { return null; }
    var name = (q.get('name') || '').trim();
    var alias = (q.get('alias') || '').trim().toLowerCase().replace(/[^a-z0-9]/g, '');
    if (!name && !alias) return null;
    var id = {
      name: name || alias || 'Pioneer',
      alias: alias || 'pioneer',
      at: new Date().toISOString()
    };
    writeIdentity(id);
    try {
      var url = new URL(location.href);
      url.search = '';
      history.replaceState(null, '', url.toString());
    } catch (e) {}
    return id;
  }

  var R = window.NayaRuntime;
  var Router = window.NayaRouter;

  /* NOTE: handlers must RETURN the view — an arrow with a braced body
     discards it and the router renders an empty div (bare #/hub did
     exactly that before this fix). */
  Router.on('hub', function () { return window.HubView({ room: 'feed' }); });
  Router.on('hub/:room', function (params) { return window.HubView(params); });
  /* Unknown in-app routes land in the Hub — the front door lives outside. */
  Router.on('*', function () { return window.HubView({ room: 'feed' }); });

  var identity = consumeHandoff() || readIdentity();
  if (!identity) {
    /* No identity on this device/browser — back to the front door. */
    location.href = WELCOME_URL;
    return;
  }
  window.NayaIdentity = identity;
  window.NayaWelcomeUrl = WELCOME_URL;

  if (!location.hash) location.hash = '#/hub';
  Router.render();

  if (window.NayaInstallPrompt) window.NayaInstallPrompt.maybeShow();

  // Debug surface for the team — read-only introspection.
  window.NayaHub = {
    version: R.version,
    rooms: R.ROOMS.map(function (r) { return r.id; }),
    doors: R.DOORS.map(function (d) { return { id: d.id, status: d.status }; }),
    stateFor: R.stateFor,
    identity: { name: identity.name, alias: identity.alias }
  };
})();
