/* APP — boot. WELCOME → IDENTITY → INTELLIGENT HUB. */

(function () {
  const R = window.NayaRuntime;
  const Router = window.NayaRouter;

  Router.on('welcome', () => window.WelcomeView());
  Router.on('identity', () => window.IdentityView());
  Router.on('hub', () => window.HubView({ room: 'feed' }));
  Router.on('hub/:room', params => window.HubView(params));
  Router.on('*', () => window.WelcomeView());

  // First visit → the portal. Returning identity-ack'd visitor → the Hub.
  if (!location.hash) {
    let ack = null;
    try { ack = sessionStorage.getItem('nayanet.identityAck'); } catch {}
    location.hash = ack ? '#/hub' : '#/welcome';
  }

  Router.render();

  // Debug surface for the team — read-only introspection.
  window.NayaHub = {
    version: R.version,
    rooms: R.ROOMS.map(r => r.id),
    doors: R.DOORS.map(d => ({ id: d.id, status: d.status })),
    stateFor: R.stateFor,
    contractFor: id => window.NayaRoomContract.get(id),
    activeRoom: () => R.roomSocket.active(),
    socketTrace: () => R.roomSocket.trace(),
  };
})();
