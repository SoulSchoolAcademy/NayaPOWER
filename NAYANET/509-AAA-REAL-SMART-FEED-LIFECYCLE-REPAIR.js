/* NayaNET 509 AAA — REAL SMART FEED LIFECYCLE + PRESENTATION REPAIR */
(()=>{'use strict';
const REAL=()=>window.Naya509RealSmartFeed;
const tones={'1':'#ffffff','2':'#ff4fd8','3':'#d86cff','4':'#9d75ff','5':'#55b9ee','6':'#55e39a','7':'#b8ee57','8':'#e8c766','9':'#ff5e6c'};
const labels={HUMAN:'HUMAN NOTE',CHILD:'CHILD NOTE',GRANDMA:'GRANDMA NOTE',NAYA:'NAYA NOTE',MACHINE:'MACHINE NOTE',LEARNING:'ADAPTIVE LEARNING','ULTIMATE MEANING':'WHAT IT MEANS',"WHAT'S IN IT FOR YOU?":"WHAT'S IN IT FOR YOU?"};
function css(){if(document.getElementById('naya509-real-lifecycle-css'))return;const s=document.createElement('style');s.id='naya509-real-lifecycle-css';s.textContent=`
.blocks{display:grid!important;visibility:visible!important;opacity:1!important}
.block[data-real-smart-note],article[data-real-smart-note]{display:block!important;visibility:visible!important;opacity:1!important;--tone:#fff}
${Object.entries(tones).map(([n,c])=>`.block[data-real-smart-note="${n}"],article[data-real-smart-note="${n}"]{--tone:${c}!important}`).join('')}
.naya509-perspectives{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px;margin:22px 0 28px}
.naya509-perspective{display:block!important;min-height:0!important;margin:0!important;padding:24px 26px!important;border:1px solid color-mix(in srgb,var(--tone,#fff) 68%,transparent)!important;border-radius:18px!important;background:linear-gradient(145deg,#15121b,#09080d)!important;box-shadow:0 12px 32px #0008,0 0 24px color-mix(in srgb,var(--tone,#fff) 14%,transparent)!important}
.naya509-perspective .layerHead{display:flex!important;align-items:center!important;gap:10px!important;margin-bottom:12px!important}
.naya509-perspective .layerHead b{font-size:20px!important;line-height:1.2!important;letter-spacing:.01em!important}
.naya509-perspective .layerHead .state{font-size:12px!important;margin-left:auto!important;opacity:.72!important}
.naya509-perspective .layerBody{font-size:20px!important;line-height:1.58!important;color:#f0ebf4!important}
.naya509-perspective.naya509-for-you{grid-column:1/-1;border-width:2px!important;padding:28px 32px!important;background:linear-gradient(145deg,#17121d,#08070b)!important}
.naya509-perspective.naya509-for-you .layerHead b{font-size:24px!important}
.naya509-perspective.naya509-for-you .layerBody{font-size:22px!important;line-height:1.6!important}
.naya509-detailLayers{display:grid;gap:16px;margin-top:8px}
/* Mission is the original source element: one quiet text line above the preserved feature-report footer. */
.mission{display:block!important;position:fixed!important;left:230px;right:250px;bottom:64px;z-index:40;text-align:center;padding:10px 18px!important;border:0!important;background:transparent!important;backdrop-filter:none!important;color:#d9d3df!important;font-size:20px!important;line-height:1.4!important;letter-spacing:.01em!important}
.mission b{display:block!important;color:#fff!important;font-size:40px!important;line-height:1.15!important;font-weight:850!important}
.mission:not(:has(b)){font-size:20px!important}
.mission span{font-size:20px!important;line-height:1.4!important;font-weight:600!important}
.features{display:flex!important;position:fixed!important;left:230px;right:0;bottom:0;z-index:45!important}
/* If the original source already contains the mission, never manufacture a second mission banner. */
.naya509-mission{display:none!important}
@media(max-width:1180px){.mission{right:0!important}.features{left:210px!important}}
@media(max-width:820px){.mission{left:0!important;right:0!important;bottom:70px!important;font-size:18px!important;padding:8px 10px!important}.mission b{font-size:29px!important}.mission span{font-size:18px!important}.features{left:0!important;bottom:0!important}}
@media(max-width:520px){.mission b{font-size:29px!important}.mission span{font-size:18px!important}}
`;
document.head.appendChild(s)}
function textOf(e){return(e.querySelector('.layerHead b')?.textContent||'').trim().replace(/\s+/g,' ').toUpperCase()}
function perspectiveKey(e){const t=textOf(e);if(t==='HUMAN'||t==='HUMAN NOTE')return'HUMAN';if(t==='CHILD'||t==='CHILD NOTE')return'CHILD';if(t==='GRANDMA'||t==='GRANDMA NOTE')return'GRANDMA';if(t==='NAYA'||t==='NAYA NOTE')return'NAYA';if(t==='MACHINE'||t==='MACHINE NOTE')return'MACHINE';if(/^LEARNING|ADAPTIVE LEARNING/.test(t))return'LEARNING';if(/^ULTIMATE MEANING|WHAT IT MEANS/.test(t))return'ULTIMATE MEANING';if(/^WHAT'S IN IT FOR YOU|WHATS IN IT FOR YOU|WHAT IS IN IT FOR YOU/.test(t))return"WHAT'S IN IT FOR YOU?";return null}
function removeContextBars(){document.querySelectorAll('body *').forEach(e=>{if(e.children.length===0&&/^INTELLIGENCE\s+(CONTEXT|COLLECTIVE)$/i.test((e.textContent||'').trim())){const p=e.closest('.railCard,.featureBtn,.contextBar,.collectiveBar');if(p)p.remove();else e.remove()}})}
function elevate(){document.querySelectorAll('[data-real-smart-note]').forEach(board=>{const nutshell=board.querySelector('.nutshell');const layers=[...board.querySelectorAll(':scope .layers > .layer')];if(!layers.length)return;let grid=board.querySelector(':scope .naya509-perspectives');let detail=board.querySelector(':scope .naya509-detailLayers');if(!grid){grid=document.createElement('section');grid.className='naya509-perspectives';grid.setAttribute('aria-label','Intelligence perspectives');if(nutshell)nutshell.insertAdjacentElement('afterend',grid);else board.querySelector('.blockInner')?.prepend(grid)}if(!detail){detail=document.createElement('section');detail.className='naya509-detailLayers';detail.setAttribute('aria-label','Intelligence detail');const actions=board.querySelector('.actions');if(actions)actions.insertAdjacentElement('beforebegin',detail);else board.querySelector('.blockInner')?.appendChild(detail)}layers.forEach(layer=>{const key=perspectiveKey(layer);if(key){const heading=layer.querySelector('.layerHead b');if(heading)heading.textContent=labels[key]||key;if(key==="WHAT'S IN IT FOR YOU?")layer.classList.add('naya509-for-you');layer.classList.add('naya509-perspective');grid.appendChild(layer)}else{detail.appendChild(layer)}});const old=board.querySelector(':scope .layers');if(old&&!old.querySelector('.layer'))old.remove()})}
function mission(){document.querySelectorAll('.naya509-mission').forEach(e=>e.remove())}
let scheduled=false;function boot(){if(scheduled)return;scheduled=true;requestAnimationFrame(()=>{scheduled=false;css();const r=REAL();if(r&&typeof r.boot==='function')r.boot();removeContextBars();elevate();mission();document.documentElement.dataset.nayaRealSmartFeed='true'})}
function observe(){if(window.__naya509RealLifecycleObserver)return;const root=document.body||document.documentElement;if(!root)return;const mo=new MutationObserver(()=>boot());mo.observe(root,{childList:true,subtree:true});window.__naya509RealLifecycleObserver=mo;document.addEventListener('click',e=>{if(e.target.closest('.feedNav button'))[0,40,150,500,1000,2000].forEach(ms=>setTimeout(boot,ms))},true);boot();setInterval(boot,750)}
function start(){css();observe()}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start,{once:true});else start();
})();
