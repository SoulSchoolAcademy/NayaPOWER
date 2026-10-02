/* APP — boot. WELCOME → IDENTITY → INTELLIGENT HUB. */

(async function () {
  const R = window.NayaRuntime;
  const Router = window.NayaRouter;

  try {
    await R.ready;
  } catch (err) {
    const outlet = document.getElementById('app');
    outlet.innerHTML = '<main class="main"><section class="state-panel"><h1>Hub contract unavailable</h1><p>The canonical room contract could not be loaded. Nothing was guessed.</p></section></main>';
    console.error(err);
    return;
  }

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
