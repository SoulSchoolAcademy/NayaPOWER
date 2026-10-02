import { chromium } from 'playwright';
import fs from 'node:fs/promises';

const base = process.env.HUB_TEST_URL || 'http://127.0.0.1:4173/HUB/app/index.html';
const WELCOME_URL = 'https://welcome.nayanet.app/';
const rooms = [
  ['feed','Smart Feed'],
  ['today','Your Intelligence Today'],
  ['reports','Your Reports'],
  ['library','Intelligent Library'],
  ['connect','Smart Connect'],
  ['ledger','Smart Ledger'],
  ['connections','Your Connections'],
  ['lists','Smart Lists'],
  ['mail','Smart Mail'],
  ['spaces','Smart Spaces'],
  ['settings','Settings'],
];
await fs.mkdir('HUB/app/test-artifacts', { recursive: true });

const browser = await chromium.launch({ headless: true });
let failures = [];
async function inspectPage(page, label) {
  const errors = [];
  page.on('console', msg => { if (msg.type() === 'error') errors.push('console: '+msg.text()); });
  page.on('pageerror', err => errors.push('pageerror: '+err.message));
  await page.waitForTimeout(120);
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  if (overflow > 2) errors.push('horizontal overflow '+overflow+'px');
  if (errors.length) failures.push(label+': '+errors.join(' | '));
}

try {
  /* ——— ENTRY FLOW: no identity → back to the front door ——— */
  const entry = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  let redirectTarget = null;
  await entry.route(WELCOME_URL + '**', route => { redirectTarget = route.request().url(); return route.abort(); });
  await entry.goto(base+'#/hub');
  await entry.waitForTimeout(2500);
  if (!(redirectTarget && redirectTarget.startsWith(WELCOME_URL))) failures.push('entry: no-identity visit did not redirect to the front door, target='+redirectTarget);
  await entry.close();

  /* ——— ENTRY FLOW: handoff ?name=&alias= → Hub, URL scrubbed, chip shows alias ——— */
  const desktop = await browser.newPage({ viewport: { width: 1440, height: 900 }, reducedMotion: 'no-preference' });
  await desktop.goto(base+'?name=Test%20User&alias=tester');
  await desktop.waitForSelector('.room-title');
  const title = (await desktop.locator('.room-title').innerText()).trim();
  if (title !== 'Smart Feed') failures.push('entry: handoff did not boot the Hub feed, title='+title);
  if (desktop.url().includes('name=')) failures.push('entry: handoff query was not scrubbed from the URL');
  const chip = await desktop.locator('.identity-chip .id-label').innerText();
  if (chip.trim() !== 'tester') failures.push('entry: identity chip shows "'+chip+'" instead of the alias');
  await inspectPage(desktop,'entry-handoff');
  await desktop.screenshot({ path:'HUB/app/test-artifacts/00-entry-handoff-desktop.png', fullPage:true });

  /* ——— ENTRY FLOW: install pop-up appears until installed ——— */
  await desktop.waitForSelector('.install-pop', { timeout: 8000 }).catch(()=>{});
  if (!(await desktop.locator('.install-pop').count())) failures.push('entry: install pop-up did not appear');
  else {
    const popText = await desktop.locator('.install-pop').innerText();
    if (!/Add to Home Screen/i.test(popText)) failures.push('entry: install pop-up lacks home-screen guidance');
    await desktop.screenshot({ path:'HUB/app/test-artifacts/01-install-pop-desktop.png' });
    await desktop.locator('.install-later').click(); /* session dismiss only */
    if (await desktop.locator('.install-pop').count()) failures.push('entry: install pop-up did not dismiss');
  }
  /* installed flag → never again */
  await desktop.evaluate(() => localStorage.setItem('nayanet.appInstalled.v1','1'));
  await desktop.reload();
  await desktop.waitForSelector('.room-title');
  await desktop.waitForTimeout(4500);
  if (await desktop.locator('.install-pop').count()) failures.push('entry: install pop-up reappeared after install flag set');

  /* ——— ENTRY FLOW: stored identity → straight back in ——— */
  await desktop.evaluate(() => localStorage.removeItem('nayanet.appInstalled.v1'));
  await desktop.goto(base+'#/hub/feed');
  await desktop.waitForSelector('.room-title');
  if (!desktop.url().includes('#/hub')) failures.push('entry: stored identity did not boot straight into the Hub');

  /* ——— ENTRY FLOW: sign out (two taps) → front door ——— */
  let signoutTarget = null;
  await desktop.route(WELCOME_URL + '**', route => { signoutTarget = route.request().url(); return route.abort(); });
  await desktop.locator('.identity-chip').click();
  await desktop.locator('.identity-chip').click();
  await desktop.waitForTimeout(2500);
  if (!(signoutTarget && signoutTarget.startsWith(WELCOME_URL))) failures.push('entry: sign-out did not return to the front door, target='+signoutTarget);
  await desktop.close();

  /* ——— ROOMS (with a stored identity so the gate passes) ——— */
  const app = await browser.newPage({ viewport: { width: 1440, height: 900 }, reducedMotion: 'no-preference' });
  await app.addInitScript(() => localStorage.setItem('nayanet.identity.v1', JSON.stringify({ name:'QA', alias:'qa' })));
  for (let i=0;i<rooms.length;i++) {
    const [id,expected] = rooms[i];
    await app.goto(base+'#/hub/'+id);
    await app.waitForSelector('.room-title');
    const actual=(await app.locator('.room-title').innerText()).trim();
    if(actual!==expected) failures.push(id+': title mismatch '+actual);
    const rails=await app.locator('nav.rail').count();
    if(rails!==1) failures.push(id+': expected one rail, got '+rails);
    await inspectPage(app,id);
    await app.screenshot({ path:`HUB/app/test-artifacts/${String(i+2).padStart(2,'0')}-${id}-desktop.png`, fullPage:true });
  }
  await app.close();

  const mobile = await browser.newPage({ viewport:{ width:390,height:844 }, reducedMotion:'reduce' });
  await mobile.addInitScript(() => localStorage.setItem('nayanet.identity.v1', JSON.stringify({ name:'QA', alias:'qa' })));
  await mobile.goto(base+'#/hub/feed');
  await mobile.waitForSelector('.rail-toggle');
  await mobile.locator('.rail-toggle').click();
  if(!(await mobile.locator('.shell').evaluate(el=>el.classList.contains('rail-open')))) failures.push('mobile: drawer did not open');
  const target=mobile.locator('.rail-btn').filter({hasText:'Your Connections'});
  await target.click();
  await mobile.waitForTimeout(80);
  if(!mobile.url().includes('#/hub/connections')) failures.push('mobile: room selection did not navigate');
  if(await mobile.locator('.shell').evaluate(el=>el.classList.contains('rail-open'))) failures.push('mobile: drawer did not close after selection');
  await inspectPage(mobile,'mobile-connections');
  await mobile.screenshot({ path:'HUB/app/test-artifacts/20-connections-mobile.png', fullPage:true });

  for (const [id,expected] of rooms) {
    await mobile.goto(base+'#/hub/'+id);
    await mobile.waitForSelector('.room-title');
    const actual=(await mobile.locator('.room-title').innerText()).trim();
    if(actual!==expected) failures.push('mobile '+id+': title mismatch');
    await inspectPage(mobile,'mobile-'+id);
  }
  await mobile.screenshot({ path:'HUB/app/test-artifacts/21-settings-mobile.png', fullPage:true });
  await mobile.close();
} finally {
  await browser.close();
}

if (failures.length) {
  console.error('HUB BROWSER QA FAILED');
  for (const failure of failures) console.error(' -', failure);
  process.exit(1);
}
console.log('HUB BROWSER QA PASSED: entry flow (redirect/handoff/chip/install/sign-out) + 11 rooms + mobile drawer + horizontal-overflow checks');
