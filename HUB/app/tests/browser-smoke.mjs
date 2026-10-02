import { chromium } from 'playwright';
import fs from 'node:fs/promises';

const base = process.env.HUB_TEST_URL || 'http://127.0.0.1:4173/HUB/app/index.html';
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
  const desktop = await browser.newPage({ viewport: { width: 1440, height: 900 }, reducedMotion: 'no-preference' });
  await desktop.goto(base+'#/welcome');
  await desktop.waitForSelector('.welcome');
  const jewels = await desktop.locator('.welcome-orbit-jewel').count();
  if (jewels !== 108) failures.push('welcome: expected 108 orbit jewels, got '+jewels);
  await inspectPage(desktop,'welcome');
  await desktop.screenshot({ path:'HUB/app/test-artifacts/00-welcome-desktop.png', fullPage:true });

  await desktop.goto(base+'#/identity');
  await desktop.waitForSelector('.identity-card');
  const identityText = await desktop.locator('.identity-card').innerText();
  if (/Shawn\s*·\s*verified device/i.test(identityText)) failures.push('identity: hardcoded verified Shawn identity regressed');
  await inspectPage(desktop,'identity');
  await desktop.screenshot({ path:'HUB/app/test-artifacts/01-identity-desktop.png', fullPage:true });

  for (let i=0;i<rooms.length;i++) {
    const [id,title] = rooms[i];
    await desktop.goto(base+'#/hub/'+id);
    await desktop.waitForSelector('.room-title');
    const actual=(await desktop.locator('.room-title').innerText()).trim();
    if(actual!==title) failures.push(id+': title mismatch '+actual);
    const rails=await desktop.locator('nav.rail').count();
    if(rails!==1) failures.push(id+': expected one rail, got '+rails);
    await inspectPage(desktop,id);
    await desktop.screenshot({ path:`HUB/app/test-artifacts/${String(i+2).padStart(2,'0')}-${id}-desktop.png`, fullPage:true });
  }
  await desktop.close();

  const mobile = await browser.newPage({ viewport:{ width:390,height:844 }, reducedMotion:'reduce' });
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

  for (const [id,title] of rooms) {
    await mobile.goto(base+'#/hub/'+id);
    await mobile.waitForSelector('.room-title');
    const actual=(await mobile.locator('.room-title').innerText()).trim();
    if(actual!==title) failures.push('mobile '+id+': title mismatch');
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
console.log('HUB BROWSER QA PASSED: welcome + identity + 11 rooms + mobile drawer + horizontal-overflow checks');
