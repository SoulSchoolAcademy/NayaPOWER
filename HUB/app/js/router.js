/* ═══════════════════════════════════════════════════════════════════
   ROUTER — hash routes. WELCOME → IDENTITY → INTELLIGENT HUB.
   #/welcome · #/identity · #/hub · #/hub/:room
   ═══════════════════════════════════════════════════════════════════ */

const Router = (() => {
  const routes = {};
  let current = null;

  function parse() {
    const h = location.hash.replace(/^#\/?/, '');
    const [path] = h.split('?');
    const segs = path.split('/').filter(Boolean);
    return segs;
  }

  function navigate(path) {
    if (location.hash === '#' + path) render();
    else location.hash = '#' + path;
  }

  function on(pattern, handler) { routes[pattern] = handler; }

  function render() {
    const segs = parse();
    const outlet = document.getElementById('app');
    outlet.innerHTML = '';
    let key = segs.join('/');
    let handler = routes[key];
    let params = {};
    if (!handler) {
      // try parametric: hub/:room
      if (segs[0] === 'hub' && segs[1]) {
        handler = routes['hub/:room'];
        params = { room: segs[1] };
        key = 'hub/:room';
      }
    }
    if (!handler) handler = routes['*'];
    current = key;
    const view = handler(params) || document.createElement('div');
    outlet.appendChild(view);
    const main = outlet.querySelector('.main');
    if (main) { main.setAttribute('tabindex', '-1'); }
    window.scrollTo(0, 0);
  }

  window.addEventListener('hashchange', render);

  return { on, navigate, render, parse };
})();

window.NayaRouter = Router;
