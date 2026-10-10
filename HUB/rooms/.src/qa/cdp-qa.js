/* Full QA: interactions + full-page screenshots, desktop & mobile. Cache-busted. */
const CDP = 'http://localhost:9333';
const FILE = 'file:///home/hatch/workspace/your_files/nayanet-hub.html';
const OUT = '/tmp/hubqa';
async function putNew() { const r = await fetch(CDP + '/json/new', { method: 'PUT' }); return r.json(); }
function connect(wsUrl) {
  return new Promise((res, rej) => {
    const ws = new WebSocket(wsUrl); let id = 0; const pending = new Map();
    const api = { send(m, p = {}) { return new Promise((rs, rj) => { const i = ++id; pending.set(i, { rs, rj }); ws.send(JSON.stringify({ id: i, method: m, params: p })); }); }, close() { ws.close(); } };
    ws.onopen = () => res(api); ws.onerror = rej;
    ws.onmessage = (m) => { const d = JSON.parse(m.data); if (d.id && pending.has(d.id)) { const { rs, rj } = pending.get(d.id); pending.delete(d.id); d.error ? rj(new Error(d.error.message)) : rs(d.result); } };
  });
}
const sleep = (ms) => new Promise(r => setTimeout(r, ms));
async function shot(api, name) {
  const r = await api.send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true });
  require('fs').writeFileSync(OUT + '/' + name + '.png', Buffer.from(r.data, 'base64'));
  console.log('shot:', name);
}
(async () => {
  const cb = Date.now();
  const t = await putNew();
  const api = await connect(t.webSocketDebuggerUrl);
  await api.send('Page.enable'); await api.send('Runtime.enable');
  await api.send('Page.navigate', { url: FILE + '?cb=' + cb });
  await sleep(9000);

  // ---- interactions (no in-page reload inside evaluate) ----
  const inter = await api.send('Runtime.evaluate', {
    expression: `(async () => {
      const sleep = ms => new Promise(r => setTimeout(r, ms));
      const res = [];
      const click = async sel => { const el = document.querySelector(sel); if (!el) return 'MISSING:'+sel; el.click(); await sleep(1200); return 'ok'; };
      await click('[data-page="share"]');
      res.push('door-scope:' + await click('[data-hub-action="door-scope"]'));
      res.push('door-confirm:' + await click('[data-hub-action="door-confirm"]'));
      const receipts1 = (JSON.parse(localStorage.getItem('nayapower-hub') || '{}').receipts || []).length;
      res.push('receipts-after-door:' + receipts1);
      await click('[data-page="connections"]');
      const inp = document.querySelector('#hubConnName');
      res.push('conn-input:' + !!inp);
      if (inp) { inp.value = 'QA Bot'; document.querySelector('#hubConnKind').value = 'Naya'; }
      res.push('conn-add:' + await click('[data-hub-action="conn-add"]'));
      const conns = (JSON.parse(localStorage.getItem('nayapower-hub') || '{}').conns || []).length;
      res.push('conns-count:' + conns);
      await click('[data-page="lists"]');
      res.push('list-fav:' + await click('[data-hub-action="list-fav"]'));
      await click('[data-page="settings"]');
      const motion = document.querySelector('[data-hub-check="reduce-motion"]');
      res.push('motion-check:' + !!motion);
      await click('[data-page="mail"]');
      await sleep(800);
      res.push('mail-notify:' + !!document.querySelector('[data-hub-check="mail-notify"]'));
      return res;
    })()`, awaitPromise: true, returnByValue: true });
  (inter.result.value || []).forEach(l => console.log(' ', l));

  // ---- persistence across reload (separate step) ----
  await api.send('Page.navigate', { url: FILE + '?cb=' + cb + '#/ledger' });
  await sleep(9000);
  const after = await api.send('Runtime.evaluate', {
    expression: `(async () => { const sleep = ms => new Promise(r => setTimeout(r, ms)); await sleep(2000);
      const d = JSON.parse(localStorage.getItem('nayapower-hub') || '{}');
      const ws = document.getElementById('nayaIntelligenceWorkspace');
      return 'receipts:' + (d.receipts || []).length + ' ledger-hubstate:' + ws.innerHTML.includes('hub-state'); })()`,
    awaitPromise: true, returnByValue: true });
  console.log(' persistence after reload ->', after.result.value);

  // ---- full-page screenshots, all rooms ----
  await api.send('Emulation.setDeviceMetricsOverride', { width: 1440, height: 900, deviceScaleFactor: 1, mobile: false });
  await api.send('Page.navigate', { url: FILE + '?cb=' + cb });
  await sleep(9000);
  const rooms = ['today', 'reports', 'library', 'share', 'ledger', 'connections', 'lists', 'mail', 'spaces', 'settings'];
  for (const r of rooms) {
    await api.send('Runtime.evaluate', { expression: `document.querySelector('[data-page="${r}"]').click()` });
    await sleep(2500);
    await shot(api, 'room-' + r);
  }
  // ---- mobile ----
  await api.send('Emulation.setDeviceMetricsOverride', { width: 390, height: 844, deviceScaleFactor: 2, mobile: true });
  await api.send('Page.navigate', { url: FILE + '?cb=' + cb });
  await sleep(9000);
  await shot(api, 'mobile-feed');
  await api.send('Runtime.evaluate', { expression: `document.querySelector('[data-page="library"]').click()` });
  await sleep(2500);
  await shot(api, 'mobile-library');
  await api.send('Runtime.evaluate', { expression: `document.querySelector('[data-page="settings"]').click()` });
  await sleep(2500);
  await shot(api, 'mobile-settings');
  console.log('QA DONE');
  api.close();
})().catch(e => { console.error('QA FAILED:', e.message); process.exit(1); });
