#!/usr/bin/env node
/**
 * Dashboard FIRST SCREEN acceptance audit (read-only).
 * This does not judge aesthetic excellence, authenticate users, or certify live data.
 * It catches first-viewport composition defects before a human is asked to score.
 *
 * Usage:
 *   node tools/dashboard_first_viewport_audit.mjs --url=https://nayanet.live/dashboard
 *   CHROME_BIN=/usr/bin/google-chrome node tools/dashboard_first_viewport_audit.mjs --url=file:///.../fixture.html
 *
 * Exit 0: automated first-viewport checks pass for both sizes.
 * Exit 1: a check fails. Exit 2: setup/browser/instrumentation failed (UNKNOWN).
 */
import {spawn} from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {pathToFileURL} from 'node:url';

const args=process.argv.slice(2);
const urlArg=args.find(a=>a.startsWith('--url='));
const screenshotDirArg=args.find(a=>a.startsWith('--screenshots='));
if (!urlArg) { console.error('Require --url=... (no implicit production browsing)'); process.exit(2); }
const url=urlArg.slice(6);
try { const u=new URL(url); if (!['https:','http:','file:'].includes(u.protocol)) throw Error('protocol'); }
catch { console.error('Invalid URL'); process.exit(2); }
const variants=[{name:'compact-phone',width:320,height:700,mobile:true},{name:'phone',width:390,height:844,mobile:true},{name:'tablet',width:768,height:1024,mobile:true},{name:'desktop',width:1440,height:900,mobile:false}];
const chromeBins=process.platform==='win32'
 ? ['C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe','C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe']
 : ['/usr/bin/google-chrome','/usr/bin/chromium','/usr/bin/chromium-browser'];
const chrome=[process.env.CHROME_BIN,...chromeBins].find(x=>x && fs.existsSync(x));
if(!chrome){console.error('No Chrome/Chromium binary found; result UNKNOWN');process.exit(2)}
const profile=fs.mkdtempSync(path.join(os.tmpdir(),'naya-first-screen-'));
const port=Number(process.env.CHROME_CDP_PORT || 9438);
const proc=spawn(chrome,['--headless=new','--no-first-run','--disable-gpu','--disable-extensions','--no-default-browser-check',
  '--remote-debugging-port='+port,'--user-data-dir='+profile,'about:blank'],{stdio:'ignore'});
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
let socket;
async function browser(){
 let pages;
 for(let i=0;i<45;i++){try{pages=await(await fetch('http://127.0.0.1:'+port+'/json/list')).json();break}catch{await sleep(180)}}
 if(!pages)throw Error('Chrome CDP did not become ready');
 socket=new WebSocket((pages.find(x=>x.type==='page')||pages[0]).webSocketDebuggerUrl);
 await new Promise((ok,no)=>{socket.onopen=ok;socket.onerror=no});
 let id=0;const promises=new Map();
 socket.onmessage=e=>{const m=JSON.parse(e.data);const entry=promises.get(m.id);
   if(entry){promises.delete(m.id);m.error?entry.reject(Error(JSON.stringify(m.error))):entry.resolve(m.result)}};
 const send=(method,params={})=>new Promise((resolve,reject)=>{
   const n=++id;promises.set(n,{resolve,reject});socket.send(JSON.stringify({id:n,method,params}))});
 await send('Page.enable');await send('Runtime.enable');await send('Page.navigate',{url});
 await sleep(3100);
 return send;
}
function inspect(){
 const viewport=document.documentElement.clientWidth;
 const nodes={heading:[...document.querySelectorAll('#os-points-board h3')].find(x=>/Your points/i.test(x.textContent)),
   gauge:document.querySelector('.tn-tacho'),next:document.querySelector('#os-v6-next'),
   bar:document.querySelector('#nsbBottom')};
 const dimensions=el=>{if(!el)return null;const r=el.getBoundingClientRect(),style=getComputedStyle(el);
   return {top:Math.round(r.top),bottom:Math.round(r.bottom),left:Math.round(r.left),right:Math.round(r.right),
     width:Math.round(r.width),height:Math.round(r.height),display:style.display,visibility:style.visibility,
     hidden:el.hidden}};
 const obj=Object.fromEntries(Object.entries(nodes).map(([k,v])=>[k,dimensions(v)]));
 const bar=obj.bar;
 const safeBottom=bar&&bar.display!=='none'&&bar.top>0&&bar.top<innerHeight?bar.top:innerHeight;
 const visible=o=>o&&o.display!=='none'&&o.visibility!=='hidden'&&!o.hidden&&o.height>0&&o.width>0;
 const inside=(o)=>visible(o)&&o.top>=0&&o.bottom<=safeBottom-8;
 const controls=[...document.querySelectorAll('button,a,[role="button"]')].filter(el=>!el.closest('[aria-hidden="true"],[hidden]') && el.checkVisibility({checkOpacity:true,checkVisibilityCSS:true})).map(el=>{
   const o=dimensions(el);return {name:(el.getAttribute('aria-label')||el.textContent||'').trim().slice(0,45),...o,
   viewportCenter:o?o.top+o.height/2>=0&&o.top+o.height/2<safeBottom&&o.left+o.width/2>=0&&o.left+o.width/2<=viewport:false}});
 const underMin=controls.filter(x=>x.viewportCenter&&visible(x)&&(x.width<44||x.height<44));
 const checks={
   hero_heading_first_view:inside(obj.heading),
   gauge_fully_readable_first_view:inside(obj.gauge),
   useful_action_first_view:inside(obj.next),
   no_document_horizontal_overflow:document.documentElement.scrollWidth<=viewport+2,
   first_view_tap_targets_at_least_44px:underMin.length===0
 };
 return {title:document.title,viewportWidth:viewport,viewportHeight:innerHeight,documentWidth:document.documentElement.scrollWidth,
   firstScreenContentBottom:safeBottom,rects:obj,checks,undersizedControls:underMin.slice(0,20).map(x=>({name:x.name,width:x.width,height:x.height,top:x.top}))};
}
async function main(){
 const send=await browser();const results=[];
 for(const v of variants){
   await send('Emulation.setDeviceMetricsOverride',{width:v.width,height:v.height,deviceScaleFactor:1,mobile:v.mobile});
   await sleep(1100);
   const result=await send('Runtime.evaluate',{expression:'('+inspect.toString()+')()',returnByValue:true,awaitPromise:true});
   if(result.exceptionDetails||!result.result?.value)throw Error('Cannot inspect '+v.name+': '+JSON.stringify(result.exceptionDetails));
   const data={view:v.name,...result.result.value};results.push(data);
   if(screenshotDirArg){
     const dir=screenshotDirArg.slice(14);fs.mkdirSync(dir,{recursive:true});
     const photo=await send('Page.captureScreenshot',{format:'png',fromSurface:true,captureBeyondViewport:false});
     fs.writeFileSync(path.join(dir,'dashboard-first-screen-'+v.name+'.png'),Buffer.from(photo.data,'base64'));
   }
 }
 const result={audit:'naya-dashboard-first-viewport-v1',url,checkedAt:new Date().toISOString(),
   sourceOfProof:'rendered unprivileged Chrome DOM, not data/backend verification',
   viewportResults:results,passed:results.every(r=>Object.values(r.checks).every(Boolean))};
 console.log(JSON.stringify(result,null,2));
 process.exitCode=result.passed?0:1;
}
try{await main()}catch(e){console.error('AUDIT UNKNOWN: '+e.stack);process.exitCode=2}
finally{try{socket?.close()}catch{}proc.kill();try{fs.rmSync(profile,{recursive:true,force:true})}catch{}}

[executed on device: DESKTOP-OJ712N5 (97813f8c-e057-47af-82b6-89e3bc067f5c)]