/* HUB SHELL v2.1 — browser smoke. Asserts the director's shell contract:
   two quiet "+" corner controls · room drawer on desktop (10 rooms, never
   Smart Feed) · rooms popup menu on mobile · ecosystem popup menu (8, never
   a top pill nav) · feed-as-main-show · ONE sticky mode zone ·
   nav law (backdrop, Escape, scroll lock, focus trap/restore). */
import { chromium } from 'playwright-core';
import fs from 'node:fs/promises';

const CHROME = process.env.CHROME_PATH || '/home/hatch/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome';
const base = process.env.HUB_TEST_URL || 'http://127.0.0.1:4173/HUB/app/index.html';
const rooms = [
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

const browser = await chromium.launch({ headless: true, executablePath: CHROME });
let failures = [];
async function inspectPage(page, label) {
  const errors = [];
  page.on('console', msg => { if (msg.type() === 'error') errors.push('console: '+msg.text()); });
  page.on('pageerror', err => errors.push('pageerror: '+err.message));
  await page.waitForTimeout(150);
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  if (overflow > 2) errors.push('horizontal overflow '+overflow+'px');
  if (errors.length) failures.push(label+': '+errors.join(' | '));
}
const note = (cond, msg) => { if (!cond) failures.push(msg); };

try {
  const desktop = await browser.newPage({ viewport: { width: 1440, height: 900 }, reducedMotion: 'no-preference' });
  await desktop.goto(base+'#/welcome');
  await desktop.waitForSelector('.welcome');
  const jewels = await desktop.locator('.welcome-orbit-jewel').count();
  note(jewels === 108, 'welcome: expected 108 orbit jewels, got '+jewels);
  await inspectPage(desktop,'welcome');
  await desktop.screenshot({ path:'HUB/app/test-artifacts/00-welcome-desktop.png', fullPage:true });

  await desktop.goto(base+'#/identity');
  await desktop.waitForSelector('.identity-card');
  const identityText = await desktop.locator('.identity-card').innerText();
  if (/Shawn\s*·\s*verified device/i.test(identityText)) failures.push('identity: hardcoded verified Shawn identity regressed');
  await inspectPage(desktop,'identity');

  /* ——— Main Show: #/hub and #/hub/feed are the same full-bleed feed ——— */
  for (const hash of ['#/hub','#/hub/feed']) {
    await desktop.goto(base+hash);
    await desktop.waitForSelector('.main-show');
    note(await desktop.locator('.corner-tl').count() === 1, hash+': missing top-left corner control');
    note(await desktop.locator('.corner-tr').count() === 1, hash+': missing top-right corner control');
    note(await desktop.locator('nav.rail').count() === 0, hash+': persistent rail must be gone');
    note(await desktop.locator('.mode-zone').count() === 1, hash+': missing the one sticky mode zone');
    note(await desktop.locator('.mode-btn').count() === 3, hash+': expected 3 mode buttons');
    const activeMode = await desktop.locator('.mode-btn.active').innerText();
    note(/Collective/i.test(activeMode), hash+': default mode should be Collective, got '+activeMode.trim().split('\n')[0]);
    note(await desktop.locator('.feed-mount[data-mode="collective"]').count() === 1, hash+': feed mount missing data-mode');
    note(await desktop.locator('.room-head').count() === 0, hash+': main show must not render a title wall');
    await inspectPage(desktop,'mainshow'+hash.replace('#/','-'));
    await desktop.screenshot({ path:`HUB/app/test-artifacts/02-mainshow${hash.replace('#/','-')}-desktop.png`, fullPage:true });
  }

  /* ——— Room drawer: 10 rooms, never Smart Feed ——— */
  await desktop.goto(base+'#/hub');
  await desktop.locator('.corner-tl').click();
  await desktop.waitForSelector('#roomsDrawer.open');
  const roomNames = await desktop.locator('#roomsDrawer .drawer-name').allInnerTexts();
  note(roomNames.length === 10, 'room drawer: expected 10 rooms, got '+roomNames.length);
  note(!roomNames.some(n => /smart feed/i.test(n)), 'room drawer: Smart Feed must not be a drawer entry');
  note(await desktop.locator('.backdrop.show').count() === 1, 'room drawer: backdrop must show');
  const lock = await desktop.evaluate(() => document.body.classList.contains('drawer-open'));
  note(lock, 'room drawer: scroll lock missing');
  await desktop.screenshot({ path:'HUB/app/test-artifacts/03-rooms-drawer-desktop.png' });
  // Escape closes and restores focus to the corner control
  await desktop.keyboard.press('Escape');
  await desktop.waitForTimeout(120);
  note(await desktop.locator('#roomsDrawer.open').count() === 0, 'room drawer: Escape did not close');
  const focused = await desktop.evaluate(() => document.activeElement && document.activeElement.className);
  note(/corner-tl/.test(focused||''), 'room drawer: focus not restored to corner, got '+focused);
  await inspectPage(desktop,'drawer-law');

  /* ——— Ecosystem popup menu: the director's eight, never a top pill nav ——— */
  await desktop.locator('.corner-tr').click();
  await desktop.waitForSelector('#ecoMenu.open');
  const ecoNames = await desktop.locator('#ecoMenu .popup-name').allInnerTexts();
  for (const want of ['Home','NayaPOWER','5-Day Challenge','Enter Free','Powercast','White Paper','About Us','Login'])
    note(ecoNames.includes(want), 'eco menu: missing '+want);
  const pending = await desktop.locator('#ecoMenu .popup-item.pending').count();
  note(pending === 6, 'eco menu: expected 6 LINK PENDING rows, got '+pending);
  note(await desktop.locator('.backdrop.show').count() === 1, 'eco menu: backdrop must show');
  await desktop.screenshot({ path:'HUB/app/test-artifacts/04-eco-menu-desktop.png' });
  // Home navigates internally and closes the menu
  await desktop.locator('#ecoMenu .popup-item', { hasText: 'Home' }).click();
  await desktop.waitForTimeout(120);
  note(desktop.url().includes('#/hub') && !desktop.url().includes('#/hub/'), 'eco menu: Home did not navigate to main show');
  note(await desktop.locator('#ecoMenu.open').count() === 0, 'eco menu: did not close after Home');
  // Escape closes the menu and restores focus to the "+" control
  await desktop.locator('.corner-tr').click();
  await desktop.waitForSelector('#ecoMenu.open');
  await desktop.keyboard.press('Escape');
  await desktop.waitForTimeout(120);
  note(await desktop.locator('#ecoMenu.open').count() === 0, 'eco menu: Escape did not close');
  const ecoFocused = await desktop.evaluate(() => document.activeElement && document.activeElement.className);
  note(/corner-tr/.test(ecoFocused||''), 'eco menu: focus not restored to corner, got '+ecoFocused);

  /* ——— Mode switching re-mounts the feed in the new mode ——— */
  await desktop.goto(base+'#/hub');
  await desktop.locator('.mode-btn', { hasText: 'Personal' }).click();
  await desktop.waitForSelector('.feed-mount[data-mode="personal"]');
  const personalActive = await desktop.locator('.mode-btn.active').innerText();
  note(/Personal/i.test(personalActive), 'mode zone: Personal did not activate');

  /* ——— Room pages keep their quiet header ——— */
  for (let i=0;i<rooms.length;i++) {
    const [id,title] = rooms[i];
    await desktop.goto(base+'#/hub/'+id);
    await desktop.waitForSelector('.room-title');
    const actual=(await desktop.locator('.room-title').innerText()).trim();
    note(actual===title, id+': title mismatch '+actual);
    note(await desktop.locator('.mode-zone').count() === 0, id+': mode zone must never appear in a room');
    await inspectPage(desktop,id);
    await desktop.screenshot({ path:`HUB/app/test-artifacts/${String(i+10).padStart(2,'0')}-${id}-desktop.png`, fullPage:true });
  }
  await desktop.close();

  /* ——— Mobile: "+" buttons drive everything ——— */
  const mobile = await browser.newPage({ viewport:{ width:390,height:844 }, reducedMotion:'reduce' });
  await mobile.goto(base+'#/hub/feed');
  await mobile.waitForSelector('.corner-tl');
  // Rooms open as an anchored popup menu on mobile — never the drawer
  await mobile.locator('.corner-tl').click();
  await mobile.waitForSelector('#roomsMenu.open');
  note(await mobile.locator('#roomsDrawer.open').count() === 0, 'mobile: drawer must not open on mobile');
  const mobileRoomNames = await mobile.locator('#roomsMenu .popup-name').allInnerTexts();
  note(mobileRoomNames.length === 10, 'mobile rooms menu: expected 10 rooms, got '+mobileRoomNames.length);
  note(!mobileRoomNames.some(n => /smart feed/i.test(n)), 'mobile rooms menu: Smart Feed must not be a menu entry');
  await mobile.screenshot({ path:'HUB/app/test-artifacts/20-rooms-menu-mobile.png' });
  const target=mobile.locator('#roomsMenu .popup-item').filter({hasText:'Your Connections'});
  await target.click();
  await mobile.waitForTimeout(120);
  note(mobile.url().includes('#/hub/connections'), 'mobile: room selection did not navigate');
  note(await mobile.locator('#roomsMenu.open').count() === 0, 'mobile: menu did not close after selection');
  await inspectPage(mobile,'mobile-connections');
  await mobile.screenshot({ path:'HUB/app/test-artifacts/21-connections-mobile.png', fullPage:true });
  // Ecosystem "+" menu on mobile; focus trap: tab from first item stays inside
  await mobile.locator('.corner-tr').click();
  await mobile.waitForSelector('#ecoMenu.open');
  await mobile.locator('#ecoMenu .popup-item').first().focus();
  await mobile.keyboard.press('Tab');
  const trapped = await mobile.evaluate(() => document.activeElement && document.activeElement.closest('#ecoMenu') !== null);
  note(trapped, 'mobile: focus escaped the open menu');
  await mobile.screenshot({ path:'HUB/app/test-artifacts/22-eco-menu-mobile.png' });
  await mobile.keyboard.press('Escape');
  await mobile.close();
} finally {
  await browser.close();
}

if (failures.length) {
  console.error('HUB BROWSER QA FAILED');
  for (const failure of failures) console.error(' -', failure);
  process.exit(1);
}
console.log('HUB BROWSER QA PASSED: welcome + identity + main show + rooms drawer + popup menus + nav law + 10 rooms + mobile');
