/* NayaNET 509 AAA — FINAL PRESENTATION FIX
 * Surgical final layer only. Preserve C4, feed controls, real Smart Notes,
 * and existing interaction nodes. Remove only the obsolete chrome explicitly
 * identified as non-functional; collapse unexplained bottom void; restore readable
 * mission/footer presentation; enforce the canonical perspective numbering.
 */
(()=>{'use strict';
const OBSOLETE=[
 /ACTIONS\s+ARE\s+REMEMBERED\s+ON\s+THIS\s+DEVICE/i,
 /RUNTIME\s+STATE\s+VISIBLE/i,
 /^INTELLIGENCE\s+CONTEXT$/i,
 /^INTELLIGENCE\s+COLLECTIVE$/i,
 /SHARED\s+INTELLIGENCE\s+WORTH\s+DISCOVERING[,.]?\s+UNDERSTANDING[,.]?\s+AND\s+USING\s+IT/i,
 /^FREE\s+BLOCK$/i
];
const PERSPECTIVES={
 'HUMAN':2,'HUMAN NOTE':2,
 'CHILD':3,'CHILD NOTE':3,
 'GRANDMA':4,'GRANDMA NOTE':4,
 'NAYA':5,'NAYA NOTE':5,
 'MACHINE':6,'MACHINE NOTE':6,
 'LEARNING':7,'ADAPTIVE LEARNING':7,
 'ULTIMATE MEANING':8,'WHAT IT MEANS':8,
 "WHAT'S IN IT FOR YOU?":9,"WHATS IN IT FOR YOU":9
};
const LABELS={2:'HUMAN NOTE',3:'CHILD NOTE',4:'GRANDMA NOTE',5:'NAYA NOTE',6:'MACHINE NOTE',7:'ADAPTIVE LEARNING',8:'WHAT IT MEANS',9:"WHAT'S IN IT FOR YOU?"};
function norm(s){return String(s||'').replace(/\s+/g,' ').trim()}
function protectedNode(e){return !!e.closest('.feedNav,.features,.mission,.blocks,[data-real-smart-note]')}
function removeObsolete(){
 document.querySelectorAll('body *').forEach(el=>{
   if(el===document.body||protectedNode(el)||el.children.length) return;
   const t=norm(el.textContent);if(!t||!OBSOLETE.some(r=>r.test(t)))return;
   let p=el.closest('.railCard,.contextBar,.collectiveBar,.statusBar,.feedStatus,.feedBanner,.runtimeBar');
   if(p&&!protectedNode(p)){p.remove();return}
   p=el.parentElement;
   for(let i=0;p&&i<6;i++,p=p.parentElement){
     if(protectedNode(p))return;
     const pt=norm(p.textContent);
     if(pt.length<=360&&!p.querySelector('button,input,textarea,a')){p.remove();return}
   }
 });
}
function fixPerspectives(){
 document.querySelectorAll('[data-real-smart-note] .layer').forEach(layer=>{
   const h=layer.querySelector('.layerHead b');if(!h)return;
   const raw=norm(h.textContent).toUpperCase();
   let key=raw;
   if(/^ADAPTIVE LEARNING$|^LEARNING$/.test(raw))key='ADAPTIVE LEARNING';
   if(/^WHAT IT MEANS$|^ULTIMATE MEANING$/.test(raw))key='WHAT IT MEANS';
   if(/^WHAT'S IN IT FOR YOU\??$|^WHATS IN IT FOR YOU\??$/.test(raw))key="WHAT'S IN IT FOR YOU?";
   const n=PERSPECTIVES[key];if(!n)return;
   h.textContent=LABELS[n];
   let badge=layer.querySelector('.perspectiveNo');
   if(!badge){badge=document.createElement('span');badge.className='perspectiveNo';const head=layer.querySelector('.layerHead');if(head)head.prepend(badge)}
   badge.textContent=String(n);
   layer.dataset.perspectiveNumber=String(n);
 });
 document.querySelectorAll('[data-real-smart-note]').forEach(board=>{
   const grid=board.querySelector('.naya509-perspectives');if(!grid)return;
   [...grid.children].sort((a,b)=>(+a.dataset.perspectiveNumber||99)-(+b.dataset.perspectiveNumber||99)).forEach(x=>grid.appendChild(x));
 });
}
function removeBottomInterveningNodes(){
 const main=document.querySelector('.main');if(!main)return;
 const blocks=main.querySelector('.blocks');const mission=main.querySelector('.mission');if(!blocks||!mission)return;
 // The user-facing contract is intentionally strict here: once the real feed ends,
 // the only content allowed before the mission statement is nothing. This removes
 // obsolete status/banner blocks AND anonymous spacer nodes that create the black void.
 let n=blocks.nextElementSibling;
 while(n&&n!==mission){const next=n.nextElementSibling;n.remove();n=next}
}
function fixBottom(){
 const main=document.querySelector('.main');if(!main)return;
 main.style.paddingBottom='0px';
 const blocks=main.querySelector('.blocks');if(blocks){blocks.style.marginBottom='0';const last=blocks.querySelector('[data-real-smart-note]:last-child');if(last){last.style.marginBottom='0';last.style.paddingBottom='24px'}}
 const mission=main.querySelector('.mission');
 if(mission){mission.style.position='static';mission.style.bottom='auto';mission.style.margin='0 22px 4px';mission.style.padding='0';mission.style.border='0';mission.style.background='transparent';mission.style.boxShadow='none';
   const b=mission.querySelector('b');const s=mission.querySelector('span');if(b){b.style.fontSize='40px';b.style.lineHeight='1.12'}if(s){s.style.fontSize='18px';s.style.lineHeight='1.45';s.style.fontWeight='650';s.style.marginTop='8px'}
 }
 const features=main.querySelector('.features');if(features){features.style.position='static';features.style.bottom='auto';features.style.left='auto';features.style.right='auto';features.style.justifyContent='center';features.style.margin='4px 22px 10px';features.style.padding='0';features.style.boxShadow='none';features.style.borderTop='0';features.style.background='transparent';features.style.overflow='visible'}
}
function style(){if(document.getElementById('naya509-final-presentation-css'))return;const s=document.createElement('style');s.id='naya509-final-presentation-css';s.textContent=`
.naya509-board .naya509-perspectives{order:initial!important}
.naya509-board .naya509-perspective{opacity:1!important;visibility:visible!important}
.naya509-board .naya509-perspective .perspectiveNo{width:34px!important;height:34px!important;font-size:15px!important;font-weight:900!important}
.naya509-board .naya509-perspective .layerBody{font-size:20px!important;line-height:1.62!important;color:#f0ebf4!important}
.naya509-board .naya509-for-you .layerBody{font-size:22px!important;line-height:1.6!important}
.mission{font-size:18px!important}
.mission b{font-size:40px!important;line-height:1.12!important}
.mission span{font-size:18px!important;line-height:1.45!important;font-weight:650!important}
.features{justify-content:center!important;position:static!important;margin:4px 22px 10px!important;padding:0!important;border:0!important;box-shadow:none!important;background:transparent!important}
.main{padding-bottom:0!important}
.blocks{margin-bottom:0!important}
@media(max-width:760px){.mission{margin:0 10px 4px!important}.mission b{font-size:29px!important}.mission span{font-size:18px!important}.features{margin:4px 10px 12px!important}.naya509-board .naya509-perspective .layerBody{font-size:19px!important}.naya509-board .naya509-for-you .layerBody{font-size:20px!important}}
`;
document.head.appendChild(s)}
function run(){style();removeObsolete();fixPerspectives();removeBottomInterveningNodes();fixBottom();document.documentElement.dataset.naya509FinalPresentationFix='true'}
let timer=0;function schedule(){clearTimeout(timer);timer=setTimeout(run,30)}
function boot(){run();if(!window.__naya509FinalPresentationObserver){const mo=new MutationObserver(schedule);mo.observe(document.body,{childList:true,subtree:true});window.__naya509FinalPresentationObserver=mo}}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});else boot();
})();
