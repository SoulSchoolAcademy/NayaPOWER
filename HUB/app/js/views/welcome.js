/* WELCOME — the portal. Preserves the 108-jewel unity motif without the monolith. */
function WelcomeView() {
  const { el, Icons } = window.NayaUI;
  const v = el('div', 'welcome');
  v.innerHTML = `
    <div class="welcome-portal-stage" aria-hidden="true">
      <div class="welcome-orbit"></div>
      <div class="welcome-unity-orbit"><span class="welcome-unity-light"></span></div>
      <div class="portal-jewel"></div>
    </div>
    <div class="kicker">NAYANET · THE INTELLIGENT HUB</div>
    <h1>One brain.<br>Many doors.</h1>
    <p class="lede">NayaNET is the governed experience layer where intelligence becomes useful — remembered, connected, proven, and beautifully present.</p>
    <div class="cta-row"></div>
    <div class="foot">PRIVATE BY DEFAULT · SHARED BY CHOICE · COLLECTIVE BY CONSENT</div>
  `;
  const orbit=v.querySelector('.welcome-orbit');
  const colors=['#9d75ff','#6675ff','#4f8ff7','#55b9ee','#40d3bb','#35e0a1','#55e39a','#b8ee57','#f1d75a','#e8c766','#ff9a5a','#ff7a3d','#ff5e6c','#d86cff'];
  for(let i=0;i<108;i++){
    const jewel=document.createElement('span');
    jewel.className='welcome-orbit-jewel';
    jewel.style.setProperty('--a',(i*(360/108))+'deg');
    jewel.style.setProperty('--j',colors[i%colors.length]);
    jewel.style.setProperty('--s',String(.76+(i%7)*.045));
    orbit.appendChild(jewel);
  }
  const row = v.querySelector('.cta-row');
  const enter = el('button', 'btn', `${Icons.icon('arrow')}<span>Enter NayaNET</span>`);
  enter.style.setProperty('--btn-accent', '#d86cff');
  enter.addEventListener('click', () => window.NayaRouter.navigate('/identity'));
  const meaning = el('button', 'btn btn-ghost', `${Icons.icon('core')}<span>How the Hub works</span>`);
  meaning.style.setProperty('--btn-accent', '#9d75ff');
  meaning.addEventListener('click', () => {
    window.NayaUI.toast('One governed intelligence substrate. Eleven room lenses. Search retrieves; rooms project; Doors connect; Law constrains; Verify proves.', '#9d75ff', 6500);
  });
  row.append(enter, meaning);
  return v;
}
window.WelcomeView = WelcomeView;
