/* NayaNET 509 C4 — FLOWING FOOTER + REAL BOARD VISIBILITY REPAIR */
(()=>{'use strict';
const REAL=()=>window.Naya509RealSmartFeed;
const links=[['▣ SMART NOTES','https://drive.google.com/file/d/19sRtp22aAn35wNoqqpNiZHkaFGmUOxoP/view?usp=sharing'],['▣ NO DEAD ENDS','https://drive.google.com/file/d/1LgRmYAQ85AB6mmu6Qp2ovghyd1lP-FNh/view?usp=sharing'],['▣ CONTEXT','https://drive.google.com/file/d/1N-XzV3_RCTHuLdp4leZNlOo7ITFwrICR/view?usp=sharing'],['▣ “10” STAR SERVICE','https://drive.google.com/file/d/1F9M66i5Av_oJcIa5dve-U0mMeAgYKczT/view?usp=sharing']];
function css(){if(document.getElementById('naya509-flow-repair-css'))return;const s=document.createElement('style');s.id='naya509-flow-repair-css';s.textContent=`
.naya509-mission{display:none!important}
.mission{display:block!important;position:static!important;inset:auto!important;z-index:auto!important;float:none!important;clear:both!important;margin:34px 22px 12px!important;padding:0!important;border:0!important;background:transparent!important;box-shadow:none!important;text-align:center!important}
.mission b{display:block!important;font-size:40px!important;line-height:1.15!important;font-weight:850!important;color:#fff!important}
.mission span{display:block!important;margin-top:7px!important;font-size:20px!important;line-height:1.4!important;font-weight:600!important;color:#d9d3df!important}
.features{display:flex!important;position:static!important;inset:auto!important;z-index:auto!important;float:none!important;clear:both!important;width:auto!important;margin:12px 22px 34px!important;flex-wrap:wrap!important;align-items:center!important;gap:10px!important}
.features .featureLabel{font-size:14px!important;font-weight:850!important;color:#fff!important}.features .featureBtn{font-size:14px!important;min-height:46px!important;padding:0 15px!important}
@media(max-width:760px){.mission{margin:26px 10px 10px!important}.mission b{font-size:29px!important}.mission span{font-size:18px!important}.features{margin:10px 10px 26px!important}}
`;
document.head.appendChild(s)}
function restoreFooter(){let m=document.querySelector('.mission');if(!m){m=document.createElement('div');m.className='mission';m.innerHTML='<b>Your life creates your intelligence every day.</b><span>Naya helps you capture it, understand it, remember it, compound it, and use it.</span>';const b=document.querySelector('.blocks');if(b&&b.parentElement)b.insertAdjacentElement('afterend',m);else document.body.appendChild(m)}let f=document.querySelector('.features');if(!f){f=document.createElement('nav');f.className='features';f.setAttribute('aria-label','Feature reports');f.innerHTML='<span class="featureLabel">FEATURE REPORTS</span>'+links.map(x=>`<a class="featureBtn" target="_blank" rel="noopener" href="${x[1]}">${x[0]}</a>`).join('');m.insertAdjacentElement('afterend',f)}m.style.position='static';f.style.position='static'}
function removeBanners(){document.querySelectorAll('body *').forEach(e=>{if(e.children.length)return;const t=(e.textContent||'').trim();if(/^INTELLIGENCE\s+(CONTEXT|COLLECTIVE)$/i.test(t)||/^COLLECTIVE\s+INTELLIGENCE/i.test(t)||/^ACTIONS\s+ARE\s+REMEMBERED\s+ON\s+THIS\s+DEVICE/i.test(t)||/^RUNTIME\s+STATE\s+VISIBLE/i.test(t)){const p=e.closest('.railCard,.contextBar,.collectiveBar,.statusBar,.feedStatus,.feedBanner,.runtimeBar');(p||e).remove()}})}
function forceReal(){const r=REAL();if(r&&typeof r.boot==='function')r.boot();if(r&&typeof r.run==='function')r.run();}
function boot(){css();forceReal();restoreFooter();removeBanners();document.documentElement.dataset.naya509FlowRepair='true'}
[0,50,150,350,750,1500,2500,4000].forEach(ms=>setTimeout(boot,ms));
const root=document.body||document.documentElement;if(root&&!window.__naya509FlowRepairObserver){const mo=new MutationObserver(()=>{css();restoreFooter();removeBanners()});mo.observe(root,{childList:true,subtree:true});window.__naya509FlowRepairObserver=mo}
})();