/* NayaNET Intelligent Hub V13 — Surgical Sidebar Restoration
 * Purpose: restore the ORIGINAL operational controls into the EXISTING sidebar.
 * Never creates replacement controls. Moves the existing live DOM controls so their
 * original handlers/state remain authoritative. Removes duplicate rails/cards only.
 */
(()=>{
'use strict';
const SIDEBAR='.sidebar';
const OPS_CLASS='n13-original-ops';
const OPS_ID='n13-original-ops';
const LABELS={
 report:'YOUR DAILY INTELLIGENCE REPORT',
 github:'CONNECT GITHUB',
 sync:'SYNC INTELLIGENCE',
 connected:'GET CONNECTED'
};
const norm=s=>String(s||'').replace(/\s+/g,' ').trim().toUpperCase();
const isSidebar=el=>!!el?.closest?.(SIDEBAR);
function actionable(el){return el?.closest?.('button,a,[role="button"]')||el}
function findExact(label,exclude){
 const wanted=norm(label), all=[...document.querySelectorAll('button,a,[role="button"]')];
 for(const el of all){if(exclude?.has(el))continue; const t=norm(el.innerText||el.textContent); if(t===wanted||t.includes(wanted))return el;}
 return null;
}
function nearestControl(label,exclude){
 const el=findExact(label,exclude); if(!el)return null;
 return actionable(el);
}
function removeExtraRightRails(){
 const nodes=[...document.querySelectorAll('body *')];
 for(const el of nodes){
   if(isSidebar(el))continue;
   const cls=String(el.className||'').toLowerCase();
   const id=String(el.id||'').toLowerCase();
   const text=norm(el.innerText||el.textContent);
   const looksRail=/(^|[-_ ])(n10|n11|n12|right[-_ ]?rail|smart[-_ ]?notes[-_ ]?rail|intelligent[-_ ]?blocks[-_ ]?rail)/.test(cls+' '+id);
   const saysNotes=(text.includes('SMART NOTES')||text.includes('INTELLIGENT BLOCKS'));
   const fixed=(()=>{try{return getComputedStyle(el).position==='fixed'}catch{return false}})();
   if(looksRail || (fixed&&saysNotes&&text.length<1200)){
     if(el.parentElement)el.remove();
   }
 }
}
function removeNavDuplicates(){
 const sb=document.querySelector(SIDEBAR); if(!sb)return;
 for(const el of [...sb.querySelectorAll('button,a,[role="button"]')]){
   const t=norm(el.innerText||el.textContent);
   if(t==='SMART NOTES'||t==='INTELLIGENT BLOCKS'||t.includes('SMART NOTES /')||t.includes('INTELLIGENT BLOCKS /')){
     el.remove();
   }
 }
}
function ensureOps(){
 const sb=document.querySelector(SIDEBAR); if(!sb)return null;
 let ops=document.getElementById(OPS_ID);
 if(!ops){
   ops=document.createElement('section');
   ops.id=OPS_ID; ops.className=OPS_CLASS;
   ops.setAttribute('aria-label','Intelligence operations');
   const foot=sb.querySelector('.sidefoot');
   if(foot)sb.insertBefore(ops,foot); else sb.appendChild(ops);
 }
 return ops;
}
function moveOriginal(label,ops,seen){
 const control=nearestControl(label,seen);
 if(!control)return null;
 seen.add(control);
 // If a nested control is found, preserve the highest sensible original container,
 // but never lift an entire unrelated sidebar/page section.
 let node=control;
 const parent=node.parentElement;
 if(parent && parent.children.length===1 && !parent.matches('body,html,.sidebar')) node=parent;
 if(!isSidebar(node))ops.appendChild(node);
 else if(node.parentElement!==ops)ops.appendChild(node);
 return node;
}
function removeDuplicateControls(ops){
 const wanted=new Set(Object.values(LABELS));
 const kept=new Set();
 for(const el of [...document.querySelectorAll('button,a,[role="button"]')]){
   const t=norm(el.innerText||el.textContent);
   for(const label of wanted){
     if(t===label||t.includes(label)){
       const node=actionable(el);
       if(node===el && (el.parentElement===ops || ops.contains(el))){kept.add(label);continue;}
       if(kept.has(label)){
         const candidate=el.closest('.n10-connect,.n10-report,.n10-card,.n11-connect,.n11-report')||el;
         if(candidate && !isSidebar(candidate))candidate.remove();
       }
     }
   }
 }
}
function polish(ops){
 const style=document.createElement('style');
 style.id='n13-style';
 style.textContent=`
#${OPS_ID}{margin:14px 7px 0;padding:12px 0 0;border-top:1px solid #ffffff12;display:grid;gap:10px}
#${OPS_ID}::before{content:'INTELLIGENCE OPERATIONS';display:block;padding:0 4px 2px;color:#817c89;font-size:7px;font-weight:1000;letter-spacing:.18em}
#${OPS_ID} > *{box-sizing:border-box}
#${OPS_ID} .n13-report-wrap{display:block}
#${OPS_ID} button,#${OPS_ID} a,#${OPS_ID} [role="button"]{font:inherit}
#${OPS_ID} .n13-compact{min-height:70px!important;border-radius:16px!important}
#${OPS_ID} .n13-compact-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:7px}
#${OPS_ID} .n13-compact-grid > *{min-width:0}
#${OPS_ID} .n13-report{width:100%;min-height:64px!important;text-align:left!important;border-radius:16px!important}
#${OPS_ID} .n13-report *{max-width:100%}
#${OPS_ID} .n13-report{border-color:#e8c76658!important;box-shadow:inset 0 1px #fff4,0 10px 25px #0009,0 0 24px #e8c7660b!important}
#${OPS_ID} .n13-compact-grid button,#${OPS_ID} .n13-compact-grid a,#${OPS_ID} .n13-compact-grid [role="button"]{width:100%!important;min-height:72px!important;padding:8px 4px!important;display:flex!important;flex-direction:column!important;align-items:center!important;justify-content:center!important;gap:5px!important;text-align:center!important;border-radius:15px!important;background:linear-gradient(145deg,#101014,#050507)!important;border:1px solid #ffffff20!important;box-shadow:inset 0 1px #fff3,0 10px 23px #0009!important;transition:.22s cubic-bezier(.16,.84,.22,1)!important}
#${OPS_ID} .n13-compact-grid button:hover,#${OPS_ID} .n13-compact-grid a:hover,#${OPS_ID} .n13-compact-grid [role="button"]:hover{transform:translateY(-2px)!important;border-color:#ffffff55!important;box-shadow:inset 0 1px #fff5,0 15px 28px #000b,0 0 22px #ffffff0b!important}
#${OPS_ID} .n13-compact-grid > *:nth-child(1) button,#${OPS_ID} .n13-compact-grid > *:nth-child(1) a{border-color:#55e39a55!important}
#${OPS_ID} .n13-compact-grid > *:nth-child(2) button,#${OPS_ID} .n13-compact-grid > *:nth-child(2) a{border-color:#55b9ee55!important}
#${OPS_ID} .n13-compact-grid > *:nth-child(3) button,#${OPS_ID} .n13-compact-grid > *:nth-child(3) a{border-color:#55e39a55!important}
#${OPS_ID} .n13-compact-grid > *:nth-child(1) button:hover,#${OPS_ID} .n13-compact-grid > *:nth-child(1) a:hover{box-shadow:inset 0 1px #fff5,0 15px 28px #000b,0 0 25px #55e39a22!important}
#${OPS_ID} .n13-compact-grid > *:nth-child(2) button:hover,#${OPS_ID} .n13-compact-grid > *:nth-child(2) a:hover{box-shadow:inset 0 1px #fff5,0 15px 28px #000b,0 0 25px #55b9ee22!important}
#${OPS_ID} .n13-compact-grid > *:nth-child(3) button:hover,#${OPS_ID} .n13-compact-grid > *:nth-child(3) a:hover{box-shadow:inset 0 1px #fff5,0 15px 28px #000b,0 0 25px #55e39a22!important}
#${OPS_ID} .n13-compact-grid button span,#${OPS_ID} .n13-compact-grid a span{font-size:7px!important;line-height:1.2!important;letter-spacing:.04em!important}
@media(max-width:900px){#${OPS_ID}{margin-left:4px;margin-right:4px}}
`;
 document.head.appendChild(style);
}
function arrange(){
 const sb=document.querySelector(SIDEBAR); if(!sb)return false;
 removeExtraRightRails();
 removeNavDuplicates();
 const ops=ensureOps(); if(!ops)return false;
 const seen=new Set();
 const report=moveOriginal(LABELS.report,ops,seen);
 const gh=moveOriginal(LABELS.github,ops,seen);
 const sy=moveOriginal(LABELS.sync,ops,seen);
 const gc=moveOriginal(LABELS.connected,ops,seen);
 if(report)report.classList.add('n13-report');
 const controls=[gh,sy,gc].filter(Boolean);
 let grid=ops.querySelector('.n13-compact-grid');
 if(!grid && controls.length){grid=document.createElement('div');grid.className='n13-compact-grid';ops.appendChild(grid)}
 for(const c of controls){if(c.parentElement!==grid)grid.appendChild(c);c.classList.add('n13-compact')}
 removeDuplicateControls(ops);
 polishOnce();
 // Reclaim the center: V3 owns its feed width; no fixed right-rail reservation.
 const main=document.querySelector('.main'); if(main){main.style.marginRight='0';main.style.paddingRight='clamp(20px,3vw,40px)'}
 const root=document.getElementById('nayanet-elite-feed'); if(root){root.style.maxWidth='none';root.style.marginLeft='0';root.style.marginRight='0'}
 return !!(report||controls.length);
}
let polished=false; function polishOnce(){if(polished)return;polished=true;const ops=document.getElementById(OPS_ID);if(ops)polish(ops)}
function boot(){arrange()}
boot();
let ticks=0;const timer=setInterval(()=>{arrange();if(++ticks>18)clearInterval(timer)},400);
new MutationObserver(()=>{arrange()}).observe(document.body,{childList:true,subtree:true});
})();
