/* IDENTITY — the bridge, rebuilt in the premium material language.
   The old page was a flat form; this is the same trust, elevated. */

function IdentityView() {
  const { el, Icons } = window.NayaUI;
  const v = el('div', 'identity');
  const alias = 'Shawn'; // resolved from the runtime identity when connected
  v.innerHTML = `
    <div class="identity-card">
      <div class="identity-emblem" role="img" aria-label="Identity emblem"></div>
      <div class="kicker" style="justify-content:center">IDENTITY · THE BRIDGE</div>
      <h1>Who is stepping in?</h1>
      <p class="lede">NayaNET knows who you are before it shows you anything. Identity here is a relationship — private by default, shared only by your choice.</p>
      <div class="alias-preview">
        <span class="avatar" role="img" aria-label="Your avatar"></span>
        <span><b>${alias}</b> · verified device · this session only</span>
      </div>
      <div class="cta-row"></div>
      <p class="privacy-line">NOTHING LEAVES THIS DEVICE WITHOUT YOUR SAY-SO.<br>NO TRACKING · NO ADS · NO SILENT COPIES</p>
    </div>
  `;
  const row = v.querySelector('.cta-row');
  const enter = el('button', 'btn', `${Icons.icon('check')}<span>Enter the Hub</span>`);
  enter.style.setProperty('--btn-accent', '#9d75ff');
  enter.addEventListener('click', () => {
    try { sessionStorage.setItem('nayanet.identityAck', '1'); } catch {}
    window.NayaRouter.navigate('/hub');
  });
  const back = el('button', 'btn btn-ghost', `<span>Back</span>`);
  back.style.setProperty('--btn-accent', '#9d75ff');
  back.addEventListener('click', () => window.NayaRouter.navigate('/welcome'));
  row.append(enter, back);
  return v;
}
window.IdentityView = IdentityView;
