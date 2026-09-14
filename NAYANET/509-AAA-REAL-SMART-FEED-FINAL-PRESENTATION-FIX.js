/* NayaNET 509 AAA — FINAL PRESENTATION FIX v3
 * Surgical presentation correction. Functional feed navigation is sacred.
 * Never remove or resize it into oblivion. Obsolete Collective/Context chrome
 * is removable only when it is demonstrably outside the real feed navigation.
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
const FEED_LABELS=/^(PERSONAL\s+INTELLIGENCE|COLLECTIVE\s+INTELLIGENCE|ACTIVITY\s+FEED)$/i;
const PERSPECTIVES={HUMAN:2,'HUMAN NOTE':2,CHILD:3,'CHILD NOTE':3,GRANDMA:4,'GRANDMA NOTE':4,NAYA:5,'NAYA NOTE':5,MACHINE:6,'MACHINE NOTE':6,LEARNING:7,'ADAPTIVE LEARNING':7,'ULTIMATE MEANING':8,'WHAT IT MEANS':8,"WHAT'S IN IT FOR YOU?":9,"WHATS IN IT FOR YOU":9};
const LABELS={2:'HUMAN NOTE',3:'CHILD NOTE',4:'GRANDMA NOTE',5:'NAYA NOTE',6:'MACHINE NOTE',7:'ADAPTIVE LEARNING',8:'WHAT IT MEANS',9:"WHAT'S IN IT FOR YOU?"};
function norm(s){return String(s||'').replace(/\s+/g,' ').trim()}
function inFeedNav(e){return !!e.closest?.('.feedNav')}
function protectedNode(e){return !!e.closest?.('.features,.mission,.blocks,[data-real-smart-note]')||inFeedNav(e)}
function preserveFeedNavigation(){
 let nav=document.querySelector('.feedNav');
 if(!nav){
   const candidates=[...document.querySelectorAll('button,a,[role="button"]')].filter(el=>FEED_LABELS.test(norm(el.textContent)));
   if(candidates.length){nav=document.createElement('nav');nav.className='feedNav';nav.setAttribute('aria-label','Intelligence feed views');const anchor=document.querySelector('.feedHead')||document.querySelector('.blocks');if(anchor)anchor.parentNode.insertBefore(nav,anchor);candidates.forEach(el=>nav.appendChild(el));}
 }
 if(!nav)return;
 const wanted=[...nav.querySelectorAll('button,a,[role="button"]')].filter(el=>FEED_LABELS.test(norm(el.textContent)));
 wanted.forEach(el=>{el.style.setProperty('display','inline-flex','important');el.style.setProperty('visibility','visible','important');el.style.setProperty('opacity','1','important');el.style.setProperty('min-height','52px','important');el.style.setProperty('height','52px','important');el.style.setProperty('padding','0 20px','important');el.style.setProperty('font-size','15px','important');el.style.setProperty('font-weight','850','important');el.style.setProperty('line-height','1.15','important');el.style.setProperty('width','auto','important');el.style.setProperty('max-width','none','important');el.style.setProperty('flex','0 0 auto','important');});
}
function removeObsolete(){
 preserveFeedNavigation();
 document.querySelectorAll('body *').forEach(el=>{
   if(el===document.body||protectedNode(el)||el.children.length)return;
   const t=norm(el.textContent);if(!t||!OBSOLETE.some(r=>r.test(t)))return;
   let p=el.closest('.railCard,.contextBar,.collectiveBar,.statusBar,.feedStatus,.feedBanner,.runtimeBar');
   if(p&&!protectedNode(p)){p.remove();return}
   p=el.parentElement;
   for(let i=0;p&&i<6;i++,p=p.parentElement){
     if(protectedNode(p))return;
     const pt=norm(p.textContent);
     if(pt.length<=360&&!p.querySelector('.feedNav button,.features .featureBtn')){p.remove();return}
   }
 });
 document.querySelectorAll('button,a,[role="button"]').forEach(el=>{
   if(inFeedNav(el))return;
   const t=norm(el.textContent);
   if(!FEED_LABELS.test(t))return;
   // A duplicate is obsolete only if the real feed navigation exists and has the same label.
   const nav=document.querySelector('.feedNav');if(!nav)return;
   const duplicate=[...nav.querySelectorAll('button,a,[role="button"]')].some(x=>norm(x.textContent).toUpperCase()===t.toUpperCase());
   if(!duplicate)return;
   const p=el.closest('.collectiveBar,.contextBar,.railCard,.statusBar,.feedStatus,.feedBanner,.runtimeBar')||el.parentElement;
   if(p&&!inFeedNav(p))p.remove();
 });
}
function fixPerspectives(){
 document.querySelectorAll('[data-real-smart-note] .layer').forEach(layer=>{
   const h=layer.querySelector('.layerHead b');if(!h)return;const raw=norm(h.textContent).toUpperCase();let key=raw;
   if(/^ADAPTIVE LEARNING$|^LEARNING$/.test(raw))key='ADAPTIVE LEARNING';if(/^WHAT IT MEANS$|^ULTIMATE MEANING$/.test(raw))key='WHAT IT MEANS';if(/^WHAT'S IN IT FOR YOU\??$|^WHATS IN IT FOR YOU\??$/.test(raw))key="WHAT'S IN IT FOR YOU?";
   const n=PERSPECTIVES[key];if(!n)return;h.textContent=LABELS[n];let badge=layer.querySelector('.perspectiveNo');if(!badge){badge=document.createElement('span');badge.className='perspectiveNo';const head=layer.querySelector('.layerHead');if(head)head.prepend(badge)}badge.textContent=String(n);layer.dataset.perspectiveNumber=String(n);
 });
 document.querySelectorAll('[data-real-smart-note]').forEach(board=>{const grid=board.querySelector('.naya509-perspectives');if(!grid)return;[...grid.children].sort((a,b)=>(+a.dataset.perspectiveNumber||99)-(+b.dataset.perspectiveNumber||99)).forEach(x=>grid.appendChild(x))});
}
function removeBottomInterveningNodes(){const main=document.querySelector('.main');if(!main)return;const blocks=main.querySelector('.blocks');const mission=main.querySelector('.mission');if(!blocks||!mission)return;let n=blocks.nextElementSibling;while(n&&n!==mission){const next=n.nextElementSibling;if(n.matches('.feedNav,.features')||n.querySelector?.('.feedNav,.features')){n=next;continue}n.remove();n=next}}
function fixBottom(){const main=document.querySelector('.main');if(!main)return;main.style.setProperty('padding-bottom','0px','important');const blocks=main.querySelector('.blocks');if(blocks){blocks.style.setProperty('margin-bottom','0','important');const last=blocks.querySelector('[data-real-smart-note]:last-child');if(last){last.style.marginBottom='0';last.style.paddingBottom='24px'}}const mission=main.querySelector('.mission');if(mission){mission.style.position='static';mission.style.bottom='auto';mission.style.margin='0 22px 8px';mission.style.padding='0';mission.style.border='0';mission.style.background='transparent';mission.style.boxShadow='none';const b=mission.querySelector('b'),s=mission.querySelector('span');if(b){b.style.setProperty('font-size','40px','important');b.style.setProperty('line-height','1.12','important');b.style.setProperty('font-weight','850','important')}if(s){s.style.setProperty('font-size','26px','important');s.style.setProperty('line-height','1.45','important');s.style.setProperty('font-weight','650','important');s.style.setProperty('margin-top','10px','important')}}const features=main.querySelector('.features');if(features){features.style.position='static';features.style.bottom='auto';features.style.left='auto';features.style.right='auto';features.style.justifyContent='center';features.style.margin='4px 22px 10px';features.style.padding='0';features.style.boxShadow='none';features.style.borderTop='0';features.style.background='transparent';features.style.overflow='visible'}}
function style(){if(document.getElementById('naya509-final-presentation-css'))document.getElementById('naya509-final-presentation-css').remove();const s=document.createElement('style');s.id='naya509-final-presentation-css';s.textContent=`
.naya509-board .naya509-perspectives{order:initial!important}.naya509-board .naya509-perspective{opacity:1!important;visibility:visible!important}.naya509-board .naya509-perspective .perspectiveNo{width:34px!important;height:34px!important;font-size:15px!important;font-weight:900!important}.naya509-board .naya509-perspective .layerBody{font-size:20px!important;line-height:1.62!important;color:#f0ebf4!important}.naya509-board .naya509-for-you .layerBody{font-size:22px!important;line-height:1.6!important}
.feedNav{display:flex!important;visibility:visible!important;opacity:1!important;position:relative!important;z-index:60!important;gap:9px!important;padding:0 22px 15px!important;overflow:auto!important}.feedNav button,.feedNav a,.feedNav [role="button"]{display:inline-flex!important;visibility:visible!important;opacity:1!important;position:relative!important;flex:0 0 auto!important;width:auto!important;max-width:none!important;height:52px!important;min-height:52px!important;padding:0 20px!important;font-size:15px!important;line-height:1.15!important;font-weight:850!important;letter-spacing:.01em!important;border:2px solid #8b63ff66!important;border-radius:13px!important;background:#09090e!important;color:#e7e2eb!important}.feedNav button.active,.feedNav a.active,.feedNav [role="button"].active{color:#fff!important;border-color:#55e39a!important;background:#0b1711!important;box-shadow:0 0 20px #55e39a18!important}
.mission{font-size:26px!important}.mission b{font-size:40px!important;line-height:1.12!important}.mission span{font-size:26px!important;line-height:1.45!important;font-weight:650!important;margin-top:10px!important}.features{justify-content:center!important;position:static!important;margin:4px 22px 10px!important;padding:0!important;border:0!important;box-shadow:none!important;background:transparent!important}.main{padding-bottom:0!important}.blocks{margin-bottom:0!important}
@media(max-width:760px){.feedNav{padding:0 14px 13px!important;gap:7px!important}.feedNav button,.feedNav a,.feedNav [role="button"]{height:50px!important;min-height:50px!important;padding:0 16px!important;font-size:14px!important}.mission{margin:0 10px 8px!important}.mission b{font-size:29px!important}.mission span{font-size:21px!important}.features{margin:4px 10px 12px!important}.naya509-board .naya509-perspective .layerBody{font-size:19px!important}.naya509-board .naya509-for-you .layerBody{font-size:20px!important}}
`;document.head.appendChild(s)}
function run(){style();preserveFeedNavigation();removeObsolete();fixPerspectives();removeBottomInterveningNodes();fixBottom();preserveFeedNavigation();document.documentElement.dataset.naya509FinalPresentationFix='true'}
let timer=0;function schedule(){clearTimeout(timer);timer=setTimeout(run,30)}
function boot(){run();if(!window.__naya509FinalPresentationObserver){const mo=new MutationObserver(schedule);mo.observe(document.body,{childList:true,subtree:true});window.__naya509FinalPresentationObserver=mo}}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});else boot();
})();