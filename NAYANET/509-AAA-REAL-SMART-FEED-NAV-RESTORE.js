/* NayaNET 509 AAA — C4 FEED NAV RESTORE
 * Surgical repair: preserve the three sacred feed controls after real-content rendering.
 * Collective = purple, Personal = blue, Activity = green. Equal thirds, equal height.
 * Never removes or replaces feed navigation; never touches Smart Note content.
 */
(()=>{'use strict';
const LABELS=/^(PERSONAL\s+INTELLIGENCE|COLLECTIVE\s+INTELLIGENCE|ACTIVITY\s+FEED)$/i;
function norm(s){return String(s||'').replace(/\s+/g,' ').trim()}
function tone(t){t=t.toUpperCase();return t.startsWith('COLLECTIVE')?'purple':t.startsWith('PERSONAL')?'blue':'green'}
function find(){let nav=document.querySelector('.feedNav');if(!nav)return null;return nav}
function run(){const nav=find();if(!nav)return false;
 const controls=[...nav.querySelectorAll('button,a,[role="button"]')].filter(x=>LABELS.test(norm(x.textContent)));
 const unique=[];const seen=new Set();controls.forEach(x=>{const k=norm(x.textContent).toUpperCase();if(!seen.has(k)){seen.add(k);unique.push(x)}else{x.remove()}});
 unique.forEach(el=>{el.dataset.naya509FeedTone=tone(norm(el.textContent));el.style.setProperty('display','inline-flex','important');el.style.setProperty('visibility','visible','important');el.style.setProperty('opacity','1','important');el.style.setProperty('width','100%','important');el.style.setProperty('max-width','none','important');el.style.setProperty('height','52px','important');el.style.setProperty('min-height','52px','important');el.style.setProperty('align-items','center','important');el.style.setProperty('justify-content','center','important');el.style.setProperty('text-align','center','important');el.style.setProperty('box-sizing','border-box','important')});
 nav.style.setProperty('display','grid','important');nav.style.setProperty('grid-template-columns','repeat(3,minmax(0,1fr))','important');nav.style.setProperty('gap','12px','important');nav.style.setProperty('width','100%','important');nav.style.setProperty('padding','0 22px 15px','important');nav.style.setProperty('box-sizing','border-box','important');
 return unique.length===3}
function css(){if(document.getElementById('naya509-feed-nav-restore-css'))return;const s=document.createElement('style');s.id='naya509-feed-nav-restore-css';s.textContent=`
.feedNav{display:grid!important;grid-template-columns:repeat(3,minmax(0,1fr))!important;gap:12px!important;width:100%!important;align-items:stretch!important}
.feedNav button,.feedNav a,.feedNav [role="button"]{display:inline-flex!important;width:100%!important;max-width:none!important;height:52px!important;min-height:52px!important;align-items:center!important;justify-content:center!important;text-align:center!important;box-sizing:border-box!important;border-radius:15px!important;background:#09090e!important;color:#f4f0f7!important;font-size:15px!important;font-weight:850!important;line-height:1!important}
.feedNav [data-naya509-feed-tone="purple"]{border:2px solid #b06cff99!important;background:linear-gradient(180deg,#21122f,#0c0a12)!important;box-shadow:0 0 22px #a95cff20,0 7px 20px #00000066,inset 0 1px 0 #ffffff18!important}
.feedNav [data-naya509-feed-tone="blue"]{border:2px solid #55b9ee99!important;background:linear-gradient(180deg,#102333,#090c11)!important;box-shadow:0 0 22px #55b9ee20,0 7px 20px #00000066,inset 0 1px 0 #ffffff18!important}
.feedNav [data-naya509-feed-tone="green"]{border:2px solid #55e39a99!important;background:linear-gradient(180deg,#10271d,#090d0b)!important;box-shadow:0 0 22px #55e39a20,0 7px 20px #00000066,inset 0 1px 0 #ffffff18!important}
.feedNav [data-naya509-feed-tone="purple"].active{border-color:#c58aff!important;box-shadow:0 0 30px #b86cff55,0 8px 22px #00000077,inset 0 1px 0 #ffffff25!important}
.feedNav [data-naya509-feed-tone="blue"].active{border-color:#7bd4ff!important;box-shadow:0 0 30px #55b9ee55,0 8px 22px #00000077,inset 0 1px 0 #ffffff25!important}
.feedNav [data-naya509-feed-tone="green"].active{border-color:#79f4b1!important;box-shadow:0 0 30px #55e39a55,0 8px 22px #00000077,inset 0 1px 0 #ffffff25!important}
@media(max-width:760px){.feedNav{grid-template-columns:1fr!important;gap:8px!important;padding:0 14px 13px!important}.feedNav button,.feedNav a,.feedNav [role="button"]{height:50px!important;min-height:50px!important;font-size:14px!important}}
`;document.head.appendChild(s)}
function boot(){css();run();if(!window.__naya509FeedNavRestore){const mo=new MutationObserver(()=>{css();run()});mo.observe(document.body,{childList:true,subtree:true});window.__naya509FeedNavRestore=mo}}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});else boot();
})();