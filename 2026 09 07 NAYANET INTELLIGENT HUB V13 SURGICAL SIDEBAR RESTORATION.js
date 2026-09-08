/* NayaNET Intelligent Hub V15 — right-side operations + elite feed polish
 * Source of truth: authoritative 1:14 Hub + V3 feed.
 * Surgical only: preserve the original left navigation, original right operations controls,
 * existing handlers, three feeds, and bottom feature banner.
 */
(()=>{
'use strict';
const SIDEBAR='.sidebar';
const norm=s=>String(s||'').replace(/\s+/g,' ').trim().toUpperCase();

function removeOnlyDuplicateLayers(){
  for(const el of [...document.querySelectorAll('body *')]){
    if(el.matches(SIDEBAR)||el.closest(SIDEBAR)||el.matches('.activationRail')||el.closest('.activationRail')) continue;
    const cls=String(el.className||'').toLowerCase(), id=String(el.id||'').toLowerCase();
    if(/n10[-_]?rail|n11[-_]?rail|n12[-_]?rail|smart[-_]?notes[-_]?rail|intelligent[-_]?blocks[-_]?rail/.test(cls+' '+id)) el.remove();
  }
}

function removeDuplicateNavLabels(){
  const sb=document.querySelector(SIDEBAR); if(!sb) return;
  for(const el of [...sb.querySelectorAll('button,a,[role="button"]')]){
    const t=norm(el.innerText||el.textContent);
    if(t==='SMART NOTES'||t==='INTELLIGENT BLOCKS'||t.startsWith('SMART NOTES /')||t.startsWith('INTELLIGENT BLOCKS /')) el.remove();
  }
}

function style(){
  if(document.getElementById('n15-style')) return;
  const s=document.createElement('style');
  s.id='n15-style';
  s.textContent=`
/* ================================================================
   NAYANET V15 — CORRECT THREE-COLUMN HOME GEOMETRY
   LEFT = primary navigation | CENTER = intelligence | RIGHT = operations
   ================================================================ */
.homeWorkspace{
  display:grid!important;
  grid-template-columns:minmax(0,1fr) 250px!important;
  gap:28px!important;
  align-items:start!important;
}
.homeFeed{min-width:0!important;width:100%!important;max-width:none!important}
.main{min-width:0!important;margin-right:0!important;padding-left:clamp(20px,3vw,40px)!important;padding-right:clamp(20px,3vw,40px)!important}
#nayanet-elite-feed{width:100%!important;max-width:none!important;margin:0!important;padding-left:0!important;padding-right:0!important}
#nayanet-elite-feed .intelligentFeed,#nayanet-elite-feed .intelligentBlocks{width:100%!important;max-width:none!important}

/* ================================================================
   ORIGINAL RIGHT OPERATIONS RAIL — NEVER MOVE IT INTO LEFT NAV
   ================================================================ */
.activationRail{
  display:grid!important;
  grid-template-columns:1fr!important;
  gap:12px!important;
  position:sticky!important;
  top:96px!important;
  width:250px!important;
  min-width:250px!important;
  align-self:start!important;
  visibility:visible!important;
  opacity:1!important;
}
.activationRail .board{
  position:relative!important;
  padding:17px 16px!important;
  border:1px solid #ffffff18!important;
  border-radius:20px!important;
  background:linear-gradient(155deg,#101014,#050507)!important;
  box-shadow:inset 0 1px #fff3,0 18px 38px #000a!important;
  overflow:hidden!important;
  transition:transform .22s cubic-bezier(.16,.84,.22,1),border-color .22s,box-shadow .22s!important;
}
.activationRail .board:hover{
  transform:translateY(-3px)!important;
  border-color:#ffffff38!important;
  box-shadow:inset 0 1px #fff5,0 24px 44px #000b,0 0 28px color-mix(in srgb,var(--tone) 12%,transparent)!important;
}
.activationRail .boardTop{font-size:7px!important;letter-spacing:.14em!important}
.activationRail .boardTop span:last-child{color:var(--tone)!important}
.activationRail .orb{width:58px!important;height:58px!important;margin:13px auto!important}
.activationRail .board h3{font-size:17px!important;color:#fff!important}
.activationRail .board p{color:#d0cad5!important;font-size:9px!important;line-height:1.5!important}
.activationRail .why{margin:11px 0!important;padding:9px 5px!important;border-top:1px solid #ffffff10!important;border-bottom:1px solid #ffffff10!important}
.activationRail .why span{color:#aaa4b0!important}
.activationRail .btn{width:100%!important;min-height:40px!important;color:#fff!important}

/* Keep operational controls compact, luminous and unmistakably actionable. */
.activationRail .board:has(.btn.green){border-color:#55e39a42!important}
.activationRail .board:has(.btn.blue){border-color:#55b9ee42!important}
.activationRail .board:has(.btn.green):hover{box-shadow:inset 0 1px #fff5,0 24px 44px #000b,0 0 30px #55e39a18!important}
.activationRail .board:has(.btn.blue):hover{box-shadow:inset 0 1px #fff5,0 24px 44px #000b,0 0 30px #55b9ee18!important}

/* ================================================================
   ELITE INTELLIGENCE FEED — WIDE, BLACK, READABLE, DIMENSIONAL
   ================================================================ */
#nayanet-elite-feed .intelligentBlock{
  margin:0 0 28px!important;
  padding:46px clamp(26px,4vw,58px) 52px!important;
  border:1px solid #ffffff1c!important;
  border-radius:28px!important;
  background:linear-gradient(155deg,#050507 0%,#09090d 54%,#040406 100%)!important;
  box-shadow:inset 0 1px #fff3,0 28px 70px #000d,0 0 0 1px #ffffff05!important;
  overflow:hidden!important;
}
#nayanet-elite-feed .intelligentBlock:before{left:0!important;top:48px!important;bottom:48px!important;width:2px!important;opacity:.95!important}
#nayanet-elite-feed .blockHeader{margin-bottom:30px!important}
#nayanet-elite-feed .blockGlyph{width:50px!important;height:50px!important;border-radius:15px!important;font-size:20px!important}
#nayanet-elite-feed .blockTitle h3{font-size:clamp(32px,3.4vw,52px)!important;line-height:1.02!important;color:#fff!important;max-width:none!important}
#nayanet-elite-feed .blockMeta,#nayanet-elite-feed .demoBadge{color:#fff!important}
#nayanet-elite-feed .blockBody{margin-bottom:30px!important;padding-bottom:30px!important}
#nayanet-elite-feed .blockBody p{max-width:none!important;font-size:clamp(18px,1.35vw,21px)!important;line-height:1.8!important;color:#fff!important}
#nayanet-elite-feed .blockTag{color:#fff!important;background:#050507!important}
#nayanet-elite-feed .perspectiveMap:before{left:18px!important;opacity:.7!important}
#nayanet-elite-feed .perspective{
  margin:0 0 12px!important;
  padding:22px 26px 24px 56px!important;
  border:1px solid color-mix(in srgb,var(--perspective) 35%,#ffffff 7%)!important;
  border-radius:18px!important;
  background:linear-gradient(145deg,#07070a,#030304)!important;
  box-shadow:inset 0 1px #fff2,0 14px 30px #0009!important;
}
#nayanet-elite-feed .perspective:before{left:17px!important;top:25px!important;width:13px!important;height:13px!important;box-shadow:0 0 20px var(--perspective)!important}
#nayanet-elite-feed .perspectiveHead{margin-bottom:12px!important}
#nayanet-elite-feed .perspectiveHead b,#nayanet-elite-feed .perspectiveState{color:#fff!important}
#nayanet-elite-feed .perspective p{max-width:none!important;font-size:clamp(16px,1.18vw,19px)!important;line-height:1.78!important;color:#fff!important}
#nayanet-elite-feed .blockFooter{color:#fff!important}
#nayanet-elite-feed .blockFooter span:last-child{color:#fff!important}

/* Bottom feature banner remains the final visual anchor. */
.nayanet-feature-bar{left:250px!important;right:0!important;bottom:0!important}

@media(max-width:1100px){
  .homeWorkspace{grid-template-columns:minmax(0,1fr) 220px!important;gap:20px!important}
  .activationRail{width:220px!important;min-width:220px!important}
}
@media(max-width:900px){
  .homeWorkspace{grid-template-columns:1fr!important;gap:0!important}
  .activationRail{position:static!important;width:100%!important;min-width:0!important;grid-template-columns:repeat(2,minmax(0,1fr))!important;margin-top:8px!important}
  .activationRail .board{padding:15px 12px!important}
  .activationRail .board p,.activationRail .why{display:none!important}
  #nayanet-elite-feed .intelligentBlock{padding:34px 16px 40px!important;border-radius:22px!important}
  #nayanet-elite-feed .perspective{padding:19px 18px 21px 48px!important}
  #nayanet-elite-feed .perspective:before{left:14px!important}
  .main{padding-left:14px!important;padding-right:14px!important}
  .nayanet-feature-bar{left:0!important}
}
@media(prefers-reduced-motion:reduce){
  .activationRail .board{transition:none!important}
}
`;
  document.head.appendChild(s);
}

function enforce(){
  try{
    removeOnlyDuplicateLayers();
    removeDuplicateNavLabels();
    style();
    const ws=document.querySelector('.homeWorkspace');
    const rail=document.querySelector('.activationRail');
    if(ws){
      ws.style.setProperty('grid-template-columns','minmax(0,1fr) 250px','important');
      ws.style.setProperty('gap','28px','important');
    }
    if(rail){
      rail.style.setProperty('display','grid','important');
      rail.style.setProperty('visibility','visible','important');
      rail.style.setProperty('opacity','1','important');
    }
  }catch(e){console.warn('NayaNET V15 surgical layer',e)}
}

let timer=0;
function schedule(){clearTimeout(timer);timer=setTimeout(enforce,0)}
function boot(){enforce();let n=0;const t=setInterval(()=>{enforce();if(++n>20)clearInterval(t)},400);new MutationObserver(schedule).observe(document.body,{childList:true,subtree:true})}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});else boot();
})();