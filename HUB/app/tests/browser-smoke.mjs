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
  ['settings','Settings']
];

const feedFixtures = [
  {
    id:'ib-personal-1',
    mode:'personal',
    type:'DECISION',
    truth_state:'VERIFIED',
    title:'Choose the next highest-value move',
    why_now:'This decision is blocking the next verified build step.',
    source:{name:'NayaPOWER',id:'source-1'},
    created_at:'2026-10-02T15:00:00Z',
    layers:{
      nutshell:'The strongest next move is the smallest action that unlocks verified progress.',
      human:'You asked for the Hub to get out of your way and show what matters.',
      naya:'Distill the decision before presenting choices.',
      means:'One clear action beats a wall of equally loud options.',
      value:'Less cognitive load and faster forward motion.'
    },
    action:{label:'Record decision',kind:'decide'},
    related:['ib-personal-2'],
    people:['Shawn'],
    context:{report:'Today'}
  },
  {
    id:'ib-personal-2',
    mode:'personal',
    type:'KNOWLEDGE',
    truth_state:'VERIFIED',
    title:'The Hub is a projection, not the brain',
    why_now:'This keeps interface work from creating a shadow truth store.',
    source:'Contract Stack',
    layers:{
      nutshell:'Canonical intelligence stays underneath; the Hub makes it human-visible.'
    }
  },
  {
    id:'ib-collective-1',
    mode:'collective',
    type:'SHARED WISDOM',
    truth_state:'VERIFIED',
    title:'Collective intelligence without identity leakage',
    why_now:'Shared intelligence should preserve consent and privacy.',
    source:'NayaNET Collective',
    layers:{
      nutshell:'Share the intelligence deliberately without exposing private identity.'
    }
  },
  {
    id:'ib-activity-1',
    mode:'activity',
    type:'EVENT',
    truth_state:'ACTIVE',
    title:'Hub convergence pass is running',
    why_now:'This is the current meaningful activity on the project.',
    source:'NayaPOWER',
    layers:{
      nutshell:'The Main Show is being tested against the current design law and runtime boundaries.'
    }
  }
];

await fs.mkdir('HUB/app/test-artifacts', { recursive: true });

const browser = await chromium.launch({ headless: true });
const failures = [];

function fail(message){ failures.push(message); }

async function installRuntime(page){
  await page.addInitScript(fixtures => {
    window.NayaPowerRuntime = {
      identity:{
        state:'verified',
        display_name:'Shawn',
        detail:'TEST_FIXTURE'
      },
      smartFeed: async () => ({
        state:'ready',
        data:{items:fixtures}
      }),
      searchIntelligence: async payload => {
        window.__lastSearchPayload=payload;
        return {
          state:'ready',
          data:{
            answer:'The highest-value item is the decision currently blocking the next verified build step.',
            items:[fixtures[0]],
            query:payload.query,
            intelligent_block_id:payload.intelligent_block_id||null
          }
        };
      },
      performIntelligenceAction: async payload => ({
        state:'ready',
        data:{
          status:'VERIFIED',
          receipt:{receipt_id:'test-receipt-001'},
          payload
        }
      }),
      retrieveIntelligentBlock: async ({id}) => ({
        state:'ready',
        data:fixtures.find(item=>item.id===id)||null
      })
    };
  }, feedFixtures);
}

async function inspectPage(page,label){
  const overflowReport=await page.evaluate(()=>{
    const root=document.documentElement;
    const overflow=root.scrollWidth-root.clientWidth;
    const offenders=[...document.querySelectorAll('body *')].map(el=>{
      const r=el.getBoundingClientRect();
      return {
        tag:el.tagName,
        cls:String(el.className||'').slice(0,90),
        left:Math.round(r.left),
        right:Math.round(r.right),
        width:Math.round(r.width)
      };
    }).filter(x=>x.right>window.innerWidth+2||x.left<-2)
      .sort((a,b)=>(b.right-window.innerWidth)-(a.right-window.innerWidth))
      .slice(0,8);
    return {overflow,offenders};
  });
  if(overflowReport.overflow>2) fail(
    label+': horizontal overflow '+overflowReport.overflow+'px · offenders '+JSON.stringify(overflowReport.offenders)
  );
}

async function assertNoTinyText(page,label){
  const tiny=await page.evaluate(()=>{
    const root=document.querySelector('.feed-stage');
    if(!root) return [];
    return [...root.querySelectorAll('p,span,button,input,strong,h1,h2,h3')].filter(el=>{
      const style=getComputedStyle(el);
      const visible=style.display!=='none'&&style.visibility!=='hidden'&&el.getClientRects().length;
      if(!visible||!String(el.textContent||el.value||'').trim()) return false;
      return parseFloat(style.fontSize)<11;
    }).map(el=>({
      tag:el.tagName,
      cls:el.className,
      size:getComputedStyle(el).fontSize,
      text:String(el.textContent||el.value||'').trim().slice(0,50)
    }));
  });
  if(tiny.length) fail(label+': sub-11px visible text '+JSON.stringify(tiny.slice(0,6)));
}

async function assertTouchTargets(page,label){
  const small=await page.evaluate(()=>{
    const root=document.querySelector('.feed-stage');
    if(!root) return [];
    return [...root.querySelectorAll('button,[role="button"]')].filter(el=>{
      const style=getComputedStyle(el);
      if(style.display==='none'||style.visibility==='hidden'||!el.getClientRects().length) return false;
      const rect=el.getBoundingClientRect();
      return rect.height<44;
    }).map(el=>({
      cls:el.className,
      height:Math.round(el.getBoundingClientRect().height),
      text:String(el.textContent||'').trim().slice(0,50)
    }));
  });
  if(small.length) fail(label+': sub-44px interactive target '+JSON.stringify(small.slice(0,6)));
}

async function assertMainShow(page,label){
  await page.waitForSelector('.snap-board');

  if(await page.locator('nav.rail').count()) fail(label+': legacy persistent rail exists');

  const corners=await page.locator('.corner-btn').count();
  if(corners!==2) fail(label+': expected two corner controls, got '+corners);

  const drawers=await page.locator('.drawer').count();
  if(drawers!==2) fail(label+': expected two drawers, got '+drawers);

  const leftText=(await page.locator('.drawer-left').innerText()).toUpperCase();
  if(leftText.includes('SMART FEED')) fail(label+': Smart Feed appears in the room drawer');

  const productLinks=await page.locator('.drawer-right a[href]').count();
  if(productLinks!==8) fail(label+': expected 8 real product destinations, got '+productLinks);

  const modeZones=await page.locator('.mode-zone').count();
  if(modeZones!==1) fail(label+': expected one shell-owned mode zone, got '+modeZones);
  if(await page.locator('.feed-modebar').count()) fail(label+': duplicate feed-owned mode chrome exists');

  const startScroll=await page.evaluate(()=>Math.round(window.scrollY));
  if(startScroll>2) fail(label+': page moved without the user on first load, scrollY='+startScroll);

  await page.evaluate(()=>window.scrollTo(0,420));
  await page.waitForTimeout(50);
  const top=await page.locator('.mode-zone').evaluate(el=>Math.round(el.getBoundingClientRect().top));
  if(top<63) fail(label+': sticky mode zone collides with the topbar, top='+top);
  await page.evaluate(()=>window.scrollTo(0,0));

  const greeting=(await page.locator('.feed-greeting').innerText()).trim();
  if(!/Good (morning|afternoon|evening), Shawn/.test(greeting)){
    fail(label+': verified fixture identity was not recognized in greeting: '+greeting);
  }

  if(await page.locator('.snap-hero').count()!==1) fail(label+': expected exactly one dominant intelligence object');
  if(!(await page.locator('.snap-board').first().evaluate(el=>el.classList.contains('snap-hero')))) fail(label+': first ranked intelligence is not the focal object');

  await page.locator('.mode-btn[data-mode="personal"]').click();
  await page.waitForFunction(
    () => document.querySelector('.sb-title')?.textContent.includes('Choose the next highest-value move')
  );

  const personalTone=await page.locator('.snap-board').first().evaluate(
    el=>el.style.getPropertyValue('--tone').trim()
  );
  if(personalTone!=='var(--magenta)'){
    fail(label+': personal decision should use human/magenta semantics, got '+personalTone);
  }

  await page.locator('.mode-btn[data-mode="collective"]').click();
  await page.waitForFunction(
    () => document.querySelector('.sb-title')?.textContent.includes('Collective intelligence')
  );
  const collectiveTone=await page.locator('.snap-board').first().evaluate(
    el=>el.style.getPropertyValue('--tone').trim()
  );
  if(collectiveTone!=='var(--teal)'){
    fail(label+': collective/network intelligence should use connection/teal semantics, got '+collectiveTone);
  }

  await page.locator('.mode-btn[data-mode="activity"]').click();
  await page.waitForFunction(
    () => document.querySelector('.sb-title')?.textContent.includes('Hub convergence')
  );
  const activityTone=await page.locator('.snap-board').first().evaluate(
    el=>el.style.getPropertyValue('--tone').trim()
  );
  if(activityTone!=='var(--green)'){
    fail(label+': active event should use living/green semantics, got '+activityTone);
  }

  await page.locator('.mode-btn[data-mode="personal"]').click();
  const origin=page.locator('.snap-board').first();
  await origin.focus();
  await page.evaluate(()=>window.scrollTo(0,240));
  const originScroll=await page.evaluate(()=>Math.round(window.scrollY));
  await origin.click();
  await page.waitForSelector('.note-view:not([hidden])');

  if(await page.locator('.mode-zone:visible').count()){
    fail(label+': shell mode zone should recede while reading one intelligence object');
  }

  const bodySizes=await page.evaluate(()=>{
    const selectors=['.nlayer-text','.note-why span','.ask-sub','.ask-v','.ev-chain li'];
    return selectors.flatMap(selector=>[...document.querySelectorAll(selector)].filter(el=>{
      const style=getComputedStyle(el);
      return style.display!=='none'&&el.getClientRects().length&&parseFloat(style.fontSize)<16;
    }).map(el=>({selector,size:getComputedStyle(el).fontSize,text:el.textContent.trim().slice(0,45)})));
  });
  if(bodySizes.length) fail(label+': body copy below 16px floor '+JSON.stringify(bodySizes));

  const related=page.locator('.note-related .note-tool').filter({hasText:'Related'});
  if(await related.count()){
    await related.first().click();
    await page.waitForFunction(
      () => document.querySelector('.note-title')?.textContent.includes('Hub is a projection')
    );
    await page.locator('.note-back').click();
    await page.waitForSelector('.feed-river:not([hidden])');
    await page.waitForFunction(expected=>Math.abs(Math.round(window.scrollY)-expected)<=2,originScroll);
    const relatedReturnId=await page.evaluate(()=>document.activeElement?.dataset?.intelligenceId||'');
    if(relatedReturnId!=='ib-personal-1'){
      fail(label+': related intelligence return did not restore origin focus, got '+relatedReturnId);
    }
    await page.locator('.snap-board').first().click();
    await page.waitForSelector('.note-view:not([hidden])');
  }else{
    fail(label+': fixture related intelligence was not rendered');
  }

  const askBlock=page.locator('.note-tool').filter({hasText:'Ask Naya'});
  await askBlock.click();
  await page.waitForSelector('.ask-panel.open');
  const askContextId=await page.locator('.ask-panel').getAttribute('data-intelligence-id');
  if(askContextId!=='ib-personal-1') fail(label+': block Ask Naya lost canonical context id '+askContextId);
  await page.locator('.ask-input').fill('What should I do next?');
  await page.locator('.ask-go').click();
  await page.waitForFunction(()=>window.__lastSearchPayload?.intelligent_block_id==='ib-personal-1');
  const searchPayload=await page.evaluate(()=>window.__lastSearchPayload);
  if(searchPayload?.context?.intelligent_block_id!=='ib-personal-1'){
    fail(label+': governed search did not receive canonical block context '+JSON.stringify(searchPayload));
  }
  const contextBoundary=(await page.locator('.ask-boundary').innerText()).toLowerCase();
  if(!contextBoundary.includes('ib-personal-1')) fail(label+': Ask Naya did not expose canonical context boundary');
  await page.evaluate(()=>document.querySelector('.ask-panel')?.classList.remove('open'));

  const action=page.locator('.note-tool-primary');
  if(await action.count()){
    await action.click();
    await page.waitForFunction(
      () => document.querySelector('.note-action-status')?.textContent.includes('test-receipt-001')
    );
  }else{
    fail(label+': fixture action was not rendered');
  }

  await page.locator('.note-tool').filter({hasText:'Inspect evidence'}).click();
  await page.waitForSelector('.ev-drawer.open');
  await page.locator('.ev-retrieve').click();
  await page.waitForFunction(
    () => document.querySelector('.ev-runtime-result')?.textContent.includes('Canonical runtime returned')
  );
  await page.locator('.ev-close').click();

  await page.locator('.note-back').click();
  await page.waitForSelector('.feed-river:not([hidden])');
  await page.waitForTimeout(50);
  const restoredScroll=await page.evaluate(()=>Math.round(window.scrollY));
  if(Math.abs(restoredScroll-originScroll)>2){
    fail(label+': returning from canonical object lost river scroll context '+originScroll+' -> '+restoredScroll);
  }
  const restoredId=await page.evaluate(()=>document.activeElement?.dataset?.intelligenceId||'');
  if(restoredId!=='ib-personal-1'){
    fail(label+': returning from canonical object did not restore focus to origin, got '+restoredId);
  }

  await page.locator('.feed-ask').click();
  await page.locator('.ask-input').fill('What needs my attention?');
  await page.locator('.ask-go').click();
  await page.waitForFunction(
    () => document.querySelector('.ask-result')?.textContent.includes('highest-value item')
  );
  const boundary=(await page.locator('.ask-boundary').innerText()).toLowerCase();
  if(!boundary.includes('governed runtime')) fail(label+': Ask Naya did not identify governed runtime provenance');

  await assertNoTinyText(page,label);
  await assertTouchTargets(page,label);

  const opener=page.locator('.corner-left');
  await opener.focus();
  await opener.click();
  if((await page.locator('.shell').getAttribute('data-drawer'))!=='left'){
    fail(label+': left drawer did not open');
  }
  await page.keyboard.press('Escape');
  if(await page.locator('.shell').getAttribute('data-drawer')){
    fail(label+': Escape did not close the drawer');
  }
  const focusLabel=await page.evaluate(()=>document.activeElement?.getAttribute('aria-label')||'');
  if(focusLabel!=='Open room navigation'){
    fail(label+': drawer did not restore focus to its opener');
  }

  await inspectPage(page,label);
}

try{
  const desktop=await browser.newPage({
    viewport:{width:1440,height:900},
    reducedMotion:'no-preference'
  });
  await installRuntime(desktop);

  const desktopErrors=[];
  desktop.on('console',message=>{
    if(message.type()==='error') desktopErrors.push('console: '+message.text());
  });
  desktop.on('pageerror',error=>desktopErrors.push('pageerror: '+error.message));

  await desktop.goto(base+'#/welcome');
  await desktop.waitForSelector('.welcome');
  const jewels=await desktop.locator('.welcome-orbit-jewel').count();
  if(jewels!==108) fail('welcome: expected 108 orbit jewels, got '+jewels);
  await inspectPage(desktop,'welcome');
  await desktop.screenshot({
    path:'HUB/app/test-artifacts/00-welcome-desktop.png',
    fullPage:true
  });

  await desktop.goto(base+'#/identity');
  await desktop.waitForSelector('.identity-card');
  const identityText=await desktop.locator('.identity-card').innerText();
  if(/Shawn\s*·\s*verified device/i.test(identityText)){
    fail('identity: hardcoded verified Shawn identity regressed');
  }
  await inspectPage(desktop,'identity');
  await desktop.screenshot({
    path:'HUB/app/test-artifacts/01-identity-desktop.png',
    fullPage:true
  });

  await desktop.goto(base+'#/hub/feed');
  await desktop.waitForSelector('.snap-board');
  await desktop.screenshot({
    path:'HUB/app/test-artifacts/02-feed-first-paint-desktop.png',
    fullPage:false
  });
  await assertMainShow(desktop,'feed-desktop');
  await desktop.screenshot({
    path:'HUB/app/test-artifacts/02-feed-desktop.png',
    fullPage:true
  });

  for(let i=1;i<rooms.length;i++){
    const [id,title]=rooms[i];
    await desktop.goto(base+'#/hub/'+id);
    await desktop.waitForSelector('.room-title');
    const actual=(await desktop.locator('.room-title').innerText()).trim();
    if(actual!==title) fail(id+': title mismatch '+actual);
    if(await desktop.locator('nav.rail').count()) fail(id+': legacy rail regressed');
    if(await desktop.locator('.corner-btn').count()!==2) fail(id+': corner shell missing');
    await inspectPage(desktop,id);
    await desktop.screenshot({
      path:'HUB/app/test-artifacts/'+String(i+2).padStart(2,'0')+'-'+id+'-desktop.png',
      fullPage:true
    });
  }

  if(desktopErrors.length) fail('desktop runtime errors: '+desktopErrors.join(' | '));
  await desktop.close();

  const mobile=await browser.newPage({
    viewport:{width:390,height:844},
    reducedMotion:'reduce'
  });
  await installRuntime(mobile);

  const mobileErrors=[];
  mobile.on('console',message=>{
    if(message.type()==='error') mobileErrors.push('console: '+message.text());
  });
  mobile.on('pageerror',error=>mobileErrors.push('pageerror: '+error.message));

  await mobile.goto(base+'#/hub/feed');
  await mobile.waitForSelector('.snap-board');
  await mobile.screenshot({
    path:'HUB/app/test-artifacts/20-feed-first-paint-mobile.png',
    fullPage:false
  });
  await assertMainShow(mobile,'feed-mobile');
  await mobile.screenshot({
    path:'HUB/app/test-artifacts/20-feed-mobile.png',
    fullPage:true
  });

  await mobile.locator('.corner-left').click();
  if((await mobile.locator('.shell').getAttribute('data-drawer'))!=='left'){
    fail('mobile: room drawer did not open');
  }
  const target=mobile.locator('.drawer-left .drawer-btn').filter({hasText:'Your Connections'});
  await target.click();
  await mobile.waitForTimeout(100);
  if(!mobile.url().includes('#/hub/connections')){
    fail('mobile: room selection did not navigate');
  }
  if(await mobile.locator('.shell').getAttribute('data-drawer')){
    fail('mobile: drawer did not close after selection');
  }

  for(let i=1;i<rooms.length;i++){
    const [id,title]=rooms[i];
    await mobile.goto(base+'#/hub/'+id);
    await mobile.waitForSelector('.room-title');
    const actual=(await mobile.locator('.room-title').innerText()).trim();
    if(actual!==title) fail('mobile '+id+': title mismatch');
    await inspectPage(mobile,'mobile-'+id);
  }

  await mobile.screenshot({
    path:'HUB/app/test-artifacts/21-settings-mobile.png',
    fullPage:true
  });

  if(mobileErrors.length) fail('mobile runtime errors: '+mobileErrors.join(' | '));
  await mobile.close();
}finally{
  await browser.close();
}

if(failures.length){
  console.error('HUB BROWSER QA FAILED');
  for(const failure of failures) console.error(' -',failure);
  process.exit(1);
}

console.log('HUB BROWSER QA PASSED: Main Show + two-drawer shell + semantic color + governed action/search/evidence + type/target floor + 10 supporting rooms + mobile.');
