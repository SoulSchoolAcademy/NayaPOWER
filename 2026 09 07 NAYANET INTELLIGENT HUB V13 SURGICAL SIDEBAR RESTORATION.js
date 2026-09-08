/* NayaNET Intelligent Hub V14 — recovery + elite feed polish
 * Source of truth: authoritative 1:14 Hub + V3 feed.
 * Surgical only: preserve existing controls/handlers; remove duplicate presentation layers.
 */
(()=>{
'use strict';
const SIDEBAR='.sidebar', OPS_ID='n13-original-ops';
const LABELS={report:'YOUR DAILY INTELLIGENCE REPORT',github:'CONNECT GITHUB',sync:'SYNC INTELLIGENCE',connected:'GET CONNECTED'};
const norm=s=>String(s||'').replace(/\s+/g,' ').trim().toUpperCase();
const contains=(el,label)=>norm(el?.innerText||el?.textContent).includes(norm(label));
const actionable=el=>el?.closest?.('button,a,[role="button"]')||el;
function findControl(label){
  const all=[...document.querySelectorAll('button,a,[role="button"]')];
  const rail=all.find(el=>el.closest('.activationRail')&&contains(el,label));
  const sb=all.find(el=>el.closest(SIDEBAR)&&contains(el,label));
  const any=all.find(el=>contains(el,label));
  return actionable(rail||sb||any);
}
function nodeFor(control){
  if(!control)return null;
  const rail=control.closest('.activationRail');
  if(rail){
    const board=control.closest('.board');
    if(board&&Object.values(LABELS).some(x=>contains(board,x)))return board;
  }
  const wrap=control.parentElement;
  if(wrap&&wrap.children.length===1&&!wrap.matches('body,html,.sidebar'))return wrap;
  return control;
}
function removeDuplicateRails(){
  for(const el of [...document.querySelectorAll('body *')]){
    if(el.matches(SIDEBAR)||el.closest(SIDEBAR))continue;
    const cls=String(el.className||'').toLowerCase(), id=String(el.id||'').toLowerCase();
    if(/n10[-_]?rail|n11[-_]?rail|n12[-_]?rail|right[-_]?rail|smart[-_]?notes[-_]?rail|intelligent[-_]?blocks[-_]?rail/.test(cls+' '+id)){el.remove();continue}
    try{if(getComputedStyle(el).position==='fixed'&&/(SMART NOTES|INTELLIGENT BLOCKS)/.test(norm(el.innerText||el.textContent)))el.remove()}catch{}
  }
}
function removeBadNav(){
 const sb=document.querySelector(SIDEBAR); if(!sb)return;
 for(const el of [...sb.querySelectorAll('button,a,[role="button"]')]){
   const t=norm(el.innerText||el.textContent);
   if(t==='SMART NOTES'||t==='INTELLIGENT BLOCKS'||t.includes('SMART NOTES /')||t.includes('INTELLIGENT BLOCKS /'))el.remove();
 }
}
function ensureOps(){
 const sb=document.querySelector(SIDEBAR); if(!sb)return null;
 let ops=document.getElementById(OPS_ID);
 if(!ops){ops=document.createElement('section');ops.id=OPS_ID;ops.setAttribute('aria-label','Intelligence operations');const foot=sb.querySelector('.sidefoot');foot?sb.insertBefore(ops,foot):sb.appendChild(ops)}
 return ops;
}
function move(label,ops,used){
 const c=findControl(label); if(!c)return null;
 const n=nodeFor(c); if(!n||used.has(n))return null; used.add(n);
 if(!ops.contains(n))ops.appendChild(n);
 return n;
}
function dedupeOutside(ops){
 for(const label of Object.values(LABELS)){
   const matches=[...document.querySelectorAll('button,a,[role="button"]')].filter(x=>contains(x,label));
   let kept=false;
   for(const c of matches){
     const n=nodeFor(c);
     if(ops.contains(n)){kept=true;continue}
     if(kept&&n&&!n.closest(SIDEBAR))n.remove();
   }
 }
}
function style(){
 if(document.getElementById('n14-style'))return;
 const s=document.createElement('style');s.id='n14-style';s.textContent=`
/* STRUCTURAL RECOVERY */
.homeWorkspace{grid-template-columns:minmax(0,1fr)!important;gap:0!important}
.homeFeed{width:100%!important;max-width:none!important}
.activationRail{display:none!important}
.main{margin-right:0!important;padding-left:clamp(18px,3vw,40px)!important;padding-right:clamp(18px,3vw,40px)!important}
#nayanet-elite-feed{width:100%!important;max-width:none!important;margin:0!important;padding-left:0!important;padding-right:0!important}
#nayanet-elite-feed .intelligentFeed,#nayanet-elite-feed .intelligentBlocks{width:100%!important;max-width:none!important}
/* OPERATIONS — original controls, compact luminous treatment */
#${OPS_ID}{margin:12px 7px 0;padding:12px 0 0;border-top:1px solid #ffffff14;display:grid;gap:9px}
#${OPS_ID}::before{content:'INTELLIGENCE OPERATIONS';padding:0 4px 2px;color:#fff;font-size:7px;font-weight:1000;letter-spacing:.18em}
#${OPS_ID} .n13-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:7px}
#${OPS_ID} .n13-report{width:100%!important;min-height:64px!important;border:1px solid #e8c76665!important;border-radius:15px!important;background:linear-gradient(145deg,#12100b,#050507)!important;box-shadow:inset 0 1px #fff4,0 10px 24px #0009,0 0 22px #e8c76610!important}
#${OPS_ID} .n13-grid>*{min-width:0}
#${OPS_ID} .n13-grid>*{min-height:72px!important;border:1px solid #ffffff22!important;border-radius:15px!important;background:linear-gradient(145deg,#101014,#050507)!important;box-shadow:inset 0 1px #fff3,0 10px 22px #0009!important;display:flex!important;align-items:center!important;justify-content:center!important;text-align:center!important;transition:transform .22s cubic-bezier(.16,.84,.22,1),box-shadow .22s,border-color .22s!important}
#${OPS_ID} .n13-grid>*:nth-child(1){border-color:#55e39a55!important}
#${OPS_ID} .n13-grid>*:nth-child(2){border-color:#55b9ee55!important}
#${OPS_ID} .n13-grid>*:nth-child(3){border-color:#55e39a55!important}
#${OPS_ID} .n13-grid>*:hover{transform:translateY(-2px)!important;border-color:#fff8!important;box-shadow:inset 0 1px #fff5,0 15px 28px #000b,0 0 24px #fff1!important}
#${OPS_ID} .n13-grid>*:nth-child(1):hover{box-shadow:inset 0 1px #fff5,0 15px 28px #000b,0 0 25px #55e39a22!important}
#${OPS_ID} .n13-grid>*:nth-child(2):hover{box-shadow:inset 0 1px #fff5,0 15px 28px #000b,0 0 25px #55b9ee22!important}
#${OPS_ID} .n13-grid>*:nth-child(3):hover{box-shadow:inset 0 1px #fff5,0 15px 28px #000b,0 0 25px #55e39a22!important}
/* ELITE INTELLIGENCE BOARDS */
#nayanet-elite-feed .intelligentBlock{margin:0 0 28px!important;padding:46px clamp(24px,4vw,56px) 50px!important;border:1px solid #ffffff1c!important;border-radius:28px!important;background:linear-gradient(155deg,#050507 0%,#09090d 54%,#040406 100%)!important;box-shadow:inset 0 1px #fff3,0 28px 70px #000d,0 0 0 1px #ffffff05!important;overflow:hidden!important}
#nayanet-elite-feed .intelligentBlock:before{left:0!important;top:48px!important;bottom:48px!important;width:2px!important;opacity:.95!important;box-shadow:0 0 20px color-mix(in srgb,var(--tone) 30%,transparent)!important}
#nayanet-elite-feed .blockHeader{margin-bottom:30px!important}
#nayanet-elite-feed .blockGlyph{width:48px!important;height:48px!important;border-radius:15px!important;font-size:19px!important}
#nayanet-elite-feed .blockTitle h3{font-size:clamp(32px,3.4vw,52px)!important;line-height:1.02!important;color:#fff!important;max-width:none!important}
#nayanet-elite-feed .blockMeta,#nayanet-elite-feed .demoBadge{color:#fff!important}
#nayanet-elite-feed .blockBody{margin-bottom:30px!important;padding-bottom:30px!important}
#nayanet-elite-feed .blockBody p{max-width:none!important;font-size:clamp(18px,1.35vw,21px)!important;line-height:1.78!important;color:#fff!important}
#nayanet-elite-feed .blockTag{color:#fff!important;background:#050507!important}
#nayanet-elite-feed .perspectiveMap:before{left:18px!important;opacity:.7!important}
#nayanet-elite-feed .perspective{margin:0 0 12px!important;padding:22px 26px 24px 56px!important;border:1px solid color-mix(in srgb,var(--perspective) 35%,#ffffff 7%)!important;border-radius:18px!important;background:linear-gradient(145deg,#07070a,#030304)!important;box-shadow:inset 0 1px #fff2,0 14px 30px #0009!important}
#nayanet-elite-feed .perspective:last-child{margin-bottom:0!important}
#nayanet-elite-feed .perspective:before{left:17px!important;top:25px!important;width:13px!important;height:13px!important;box-shadow:0 0 20px var(--perspective)!important}
#nayanet-elite-feed .perspectiveHead{margin-bottom:12px!important}
#nayanet-elite-feed .perspectiveHead b,#nayanet-elite-feed .perspectiveState{color:#fff!important}
#nayanet-elite-feed .perspective p{max-width:none!important;font-size:clamp(16px,1.18vw,19px)!important;line-height:1.78!important;color:#fff!important}
#nayanet-elite-feed .blockFooter{color:#fff!important}
#nayanet-elite-feed .blockFooter span:last-child{color:#fff!important}
@media(max-width:900px){#nayanet-elite-feed .intelligentBlock{padding:34px 16px 38px!important;border-radius:22px!important}#nayanet-elite-feed .perspective{padding:19px 18px 21px 48px!important}#nayanet-elite-feed .perspective:before{left:14px!important}.main{padding-left:14px!important;padding-right:14px!important}#${OPS_ID} .n13-grid{gap:5px}}
@media(prefers-reduced-motion:reduce){#${OPS_ID} .n13-grid>*{transition:none!important}}
`;
 document.head.appendChild(s);
}
function arrange(){
 removeDuplicateRails();removeBadNav();
 const sb=document.querySelector(SIDEBAR),ops=ensureOps();if(!sb||!ops)return false;
 const used=new Set();
 const report=move(LABELS.report,ops,used), gh=move(LABELS.github,ops,used), sy=move(LABELS.sync,ops,used), gc=move(LABELS.connected,ops,used);
 if(report)report.classList.add('n13-report');
 const controls=[gh,sy,gc].filter(Boolean);
 let grid=ops.querySelector('.n13-grid');
 if(controls.length){if(!grid){grid=document.createElement('div');grid.className='n13-grid';ops.appendChild(grid)}for(const c of controls)if(c.parentElement!==grid)grid.appendChild(c)}
 dedupeOutside(ops);
 const rail=document.querySelector('.activationRail');if(rail&&controls.length+(report?1:0)>0)rail.style.setProperty('display','none','important');
 style();
 return !!(report||controls.length);
}
let scheduled=false;
function run(){scheduled=false;try{arrange()}catch(e){console.warn('NayaNET V14 surgical layer',e)}}
function schedule(){if(scheduled)return;scheduled=true;queueMicrotask(run)}
function boot(){run();let n=0;const t=setInterval(()=>{run();if(++n>30)clearInterval(t)},350);new MutationObserver(schedule).observe(document.body,{childList:true,subtree:true})}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});else boot();
})();