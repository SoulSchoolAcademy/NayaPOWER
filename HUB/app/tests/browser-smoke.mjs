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

  const today = await browser.newPage({ viewport:{ width:1440,height:900 }, reducedMotion:'no-preference' });
  await today.addInitScript(() => {
    window.NayaAssistantRuntime = {
      intelligenceToday: async () => ({
        state: 'ready',
        data: {
          truth_state: 'TEST_FIXTURE',
          now: { id:'IB-TODAY-NOW', type:'now', title:'Close the reference experience loop', summary:'One dominant current situation, grounded in the controlled browser fixture.', truth_state:'TEST_FIXTURE' },
          next: [{ id:'IB-TODAY-NEXT', type:'next', title:'Run the independent visual challenge', summary:'Hand the rendered reference to the judging seat after the build.', truth_state:'TEST_FIXTURE' }],
          watch: [{ id:'IB-TODAY-WATCH', type:'watch', title:'Runtime parity is still open', summary:'Do not promote browser-fixture success into production proof.', truth_state:'TEST_FIXTURE' }],
          learned: [{ id:'IB-TODAY-LEARNED', type:'learned', title:'Distillation beats metric density', summary:'The room should explain the few things that matter, not mirror the Feed.', truth_state:'TEST_FIXTURE' }],
          waiting: [{ id:'IB-TODAY-WAITING', type:'waiting', title:'Human taste acceptance', summary:'Final visual acceptance remains outside this automated test.', truth_state:'TEST_FIXTURE' }],
          recent_proof: [{ id:'RCPT-TODAY-1', receipt_id:'RCPT-TODAY-1', type:'proof', title:'Browser contract fixture', summary:'Controlled proof that the Today composition can render all canonical sections.', truth_state:'TEST_FIXTURE' }],
          reflection: 'The room is useful when the human can understand the day without reconstructing it.',
        }
      }),
      retrieveIntelligentBlock: async ({id}) => ({
        state:'ready',
        data:{id,title:'Retrieved canonical context',summary:'Controlled browser retrieval fixture for '+id+'.',truth_state:'TEST_FIXTURE'}
      }),
      searchIntelligence: async () => ({
        state:'ready',
        data:{answer:'Controlled Naya support fixture: inspect the evidence, then take the next authorized step.',truth_state:'TEST_FIXTURE'}
      })
    };
  });
  await today.goto(base+'#/hub/today');
  await today.waitForSelector('.today-now');
  const todayHead=(await today.locator('.today-now h3').innerText()).trim();
  if(todayHead!=='Close the reference experience loop') failures.push('today-contract: NOW hierarchy did not render canonical current item');
  const arcCount=await today.locator('.today-arc-step').count();
  if(arcCount!==6) failures.push('today-contract: expected six intelligence-arc steps, got '+arcCount);
  for(const section of ['next','watch','learned','waiting','proof']){
    if(await today.locator('#today-'+section).count()!==1) failures.push('today-contract: missing '+section+' section');
  }
  const actionHeight=await today.getByRole('button',{name:'Ask Naya to help'}).first().evaluate(el=>el.getBoundingClientRect().height);
  if(actionHeight<44) failures.push('today-contract: action target below 44px ('+actionHeight+')');
  await today.getByRole('button',{name:'Ask Naya to help'}).first().click();
  await today.waitForSelector('.today-inspector:not([hidden])');
  const supportText=await today.locator('.today-inspector').innerText();
  if(!/next move support/i.test(supportText)) failures.push('today-contract: Ask Naya causal response did not reach inspector');
  await inspectPage(today,'today-contract');
  await today.screenshot({ path:'HUB/app/test-artifacts/14-today-contract-desktop.png', fullPage:true });
  await today.close();

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
