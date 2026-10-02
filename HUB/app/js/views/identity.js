/* IDENTITY — the recognition/trust bridge. Never invents a verified identity. */
function IdentityView() {
  const { el, Icons } = window.NayaUI;
  const R = window.NayaRuntime;
  const ident = R.identitySnapshot ? R.identitySnapshot() : { state: 'not_verified', display_name: 'You', detail: 'Identity runtime not connected' };
  const verified = ['verified','ready','active','authorized'].includes(String(ident.state||'').toLowerCase());
  const v = el('div', 'identity');
  v.innerHTML = `
    <div class="identity-card">
      <div class="identity-emblem" role="img" aria-label="Identity emblem"></div>
      <div class="kicker" style="justify-content:center">IDENTITY · THE BRIDGE</div>
      <h1>${verified ? 'Welcome back.' : 'Identity boundary.'}</h1>
      <p class="lede">${verified
        ? 'NayaNET resolved the current governed identity before opening the intelligence.'
        : 'The governed identity runtime is not connected in this browser session. You can enter the Hub in a limited, honest mode; private or consequential capability stays unavailable.'}</p>
      <div class="alias-preview">
        <span class="avatar" role="img" aria-label="Identity avatar"></span>
        <span><b>${escapeHtml(ident.display_name||'You')}</b> · ${escapeHtml(verified ? (ident.detail||'governed identity') : 'NOT VERIFIED · LIMITED SESSION')}</span>
      </div>
      <div class="cta-row"></div>
      <p class="privacy-line">PRIVATE BY DEFAULT · SHARED BY CHOICE · COLLECTIVE BY CONSENT<br>IDENTITY STATE IS NEVER INVENTED BY THE INTERFACE</p>
    </div>`;
  const row = v.querySelector('.cta-row');
  const enter = el('button', 'btn', `${Icons.icon(verified?'check':'lock')}<span>${verified?'Enter the Hub':'Enter Limited Hub'}</span>`);
  enter.style.setProperty('--btn-accent', '#9d75ff');
  enter.addEventListener('click', () => {
    try { sessionStorage.setItem('nayanet.identityAck', verified ? 'verified' : 'limited'); } catch {}
    window.NayaRouter.navigate('/hub');
  });
  const back = el('button', 'btn btn-ghost', '<span>Back</span>');
  back.style.setProperty('--btn-accent', '#9d75ff');
  back.addEventListener('click', () => window.NayaRouter.navigate('/welcome'));
  row.append(enter, back);
  return v;
  function escapeHtml(x){return String(x??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
}
window.IdentityView = IdentityView;
