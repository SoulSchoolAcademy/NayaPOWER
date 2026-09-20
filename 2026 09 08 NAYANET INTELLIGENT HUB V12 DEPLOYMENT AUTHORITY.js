/* NayaNET V12 — deployment authority layer.
   Surgical correction of the actual Hub hierarchy. Preserves existing nav controls,
   feed content, and connection handlers while enforcing the locked three-zone contract.
   Deployment verification trigger: 2026-09-07.
*/
(()=>{
'use strict';
if(window.__NAYANET_V12_DEPLOYMENT_AUTHORITY__) return;
window.__NAYANET_V12_DEPLOYMENT_AUTHORITY__=true;

const norm=s=>String(s||'').replace(/\s+/g,' ').trim().toUpperCase();
const desired=[
  {label:'YOUR INTELLIGENCE TODAY',aliases:['INTELLIGENCE TODAY','TODAY','SMART FEED','HOME']},
  {label:'YOUR REPORTS',aliases:['YOUR REPORTS','REPORTS','REPORT']},
  {label:'INTELLIGENT LIBRARY',aliases:['INTELLIGENT LIBRARY','LIBRARY']},
  {label:'SMART LISTS',aliases:['SMART LISTS','NIHILIST','LISTS','LIST']},
  {label:'SMART SHARE',aliases:['SMART SHARE','COLLECTIVE','SHARE']},
  {label:'YOUR EVIDENCE',aliases:['YOUR EVIDENCE','EVIDENCE']},
  {label:'YOUR CONNECTIONS',aliases:['YOUR CONNECTIONS','CONNECTIONS','CONNECTED']},
  {label:'SMART MAIL',aliases:['SMART MAIL','MAIL','EMAIL']},
  {label:'SMART SPACES',aliases:['SMART SPACES','SPACES','SPACE']}
];

const style=document.createElement('style');
style.textContent=`
.n12-ready .sidebar .nav{display:grid!important;gap:5px!important}
.n12-ready .sidebar .nav button,.n12-ready .sidebar .nav a,.n12-ready .sidebar .nav [role="button"]{min-height:46px!important}
.n12-ready .sidebar .n12-nav-label{display:block!important;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.n12-ready .sidebar [data-n12-extra="1"]{display:none!important}
.n12-ready #nayanet-elite-feed .n3-tabs{position:relative;z-index:2}
.n12-ready #nayanet-elite-feed .n3-body{position:relative;z-index:1}
.n12-ready .n10-rail{z-index:40!important}
`;
document.head.appendChild(style);

function navItems(){
 const nav=document.querySelector('.sidebar .nav');
 if(!nav) return [];
 return [...nav.querySelectorAll('button,a,[role="button"]')].filter(el=>!el.closest('.n10-rail'));
}
function visibleText(el){return norm(el.textContent);}
function removeLegacy(){
 navItems().forEach(el=>{
   const t=visibleText(el);
   if(t.includes('SMART NOTES')||t.includes('INTELLIGENT BLOCKS')) el.remove();
 });
}
function aliasesMatch(el,aliases){
 const t=visibleText(el);
 return aliases.some(a=>t===norm(a)||t.includes(norm(a)));
}
function setLabel(el,label){
 if(!el)return;
 el.setAttribute('aria-label',label);
 [...el.querySelectorAll('.n12-nav-label')].forEach(x=>x.remove());
 const walker=document.createTreeWalker(el,NodeFilter.SHOW_TEXT);
 const nodes=[];
 let n;
 while((n=walker.nextNode())){
   const p=n.parentElement;
   if(!p||p.closest('.ico')||p.closest('.badge')||p.closest('[aria-hidden="true"]'))continue;
   if(n.nodeValue.trim())nodes.push(n);
 }
 if(nodes.length){
   nodes[nodes.length-1].nodeValue=' '+label;
   return;
 }
 const span=document.createElement('span');span.className='n12-nav-label';span.textContent=label;el.appendChild(span);
}
function enforceSidebar(){
 removeLegacy();
 const items=navItems();
 if(!items.length)return;
 const used=new Set();
 const chosen=[];
 desired.forEach((spec)=>{
   let found=items.find(el=>!used.has(el)&&aliasesMatch(el,spec.aliases));
   if(!found)found=items.find(el=>!used.has(el));
   if(found){used.add(found);chosen.push(found);setLabel(found,spec.label);found.removeAttribute('data-n12-extra');}
 });
 items.forEach(el=>{if(!used.has(el))el.dataset.n12Extra='1';});
 const nav=document.querySelector('.sidebar .nav');
 if(nav){chosen.forEach(el=>nav.appendChild(el));}
}
function enforceCenter(){
 const feed=document.querySelector('#nayanet-elite-feed');
 if(!feed)return;
 const tabs=[...feed.querySelectorAll('.n3-tabs button,.n3-tabs a,[role="tab"]')];
 tabs.forEach(el=>{
   const t=visibleText(el);
   if(t.includes('COLLECTIVE INTELLIGENCE'))el.setAttribute('aria-label','Collective Intelligence');
   if(t.includes('PERSONAL INTELLIGENCE'))el.setAttribute('aria-label','Personal Intelligence');
   if(t.includes('ACTIVITY'))el.setAttribute('aria-label','Activity');
 });
}
function apply(){
 document.documentElement.classList.add('n12-ready');
 enforceSidebar();
 enforceCenter();
}
apply();
new MutationObserver(apply).observe(document.body,{childList:true,subtree:true});
})();
