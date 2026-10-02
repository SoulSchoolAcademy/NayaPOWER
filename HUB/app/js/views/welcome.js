/* WELCOME — the portal. Close to the beloved baseline, rebuilt clean. */

function WelcomeView() {
  const { el, Icons } = window.NayaUI;
  const v = el('div', 'welcome');
  v.innerHTML = `
    <div class="portal-jewel" role="img" aria-label="NayaNET portal jewel"></div>
    <div class="kicker">NAYANET · THE INTELLIGENT HUB</div>
    <h1>One brain.<br>Many doors.</h1>
    <p class="lede">NayaNET is the governed network where human, machine, and AI intelligence meet — remembered, connected, and proven. Step through.</p>
    <div class="cta-row"></div>
    <div class="foot">PRIVATE BY DEFAULT · SHARED BY CHOICE · COLLECTIVE BY CONSENT</div>
  `;
  const row = v.querySelector('.cta-row');
  const enter = el('button', 'btn', `${Icons.icon('arrow')}<span>Enter NayaNET</span>`);
  enter.style.setProperty('--btn-accent', '#d86cff');
  enter.addEventListener('click', () => window.NayaRouter.navigate('/identity'));
  const peek = el('button', 'btn btn-ghost', `<span>Take the tour</span>`);
  peek.style.setProperty('--btn-accent', '#9d75ff');
  peek.addEventListener('click', () => window.NayaRouter.navigate('/hub'));
  row.append(enter, peek);
  return v;
}
window.WelcomeView = WelcomeView;
