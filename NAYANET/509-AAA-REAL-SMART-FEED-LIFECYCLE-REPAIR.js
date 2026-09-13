/* NayaNET 509 AAA — REAL SMART FEED LIFECYCLE REPAIR */
(()=>{'use strict';
const REAL=()=>window.Naya509RealSmartFeed;
const tones={'1':'#ffffff','2':'#ff4fd8','3':'#d86cff','4':'#9d75ff','5':'#55b9ee','6':'#55e39a','7':'#b8ee57','8':'#e8c766','9':'#ff5e6c'};
function css(){if(document.getElementById('naya509-real-lifecycle-css'))return;const s=document.createElement('style');s.id='naya509-real-lifecycle-css';s.textContent=` .blocks{display:grid!important;visibility:visible!important;opacity:1!important} .block[data-real-smart-note],article[data-real-smart-note]{display:block!important;visibility:visible!important;opacity:1!important;--tone:#fff} ${Object.entries(tones).map(([n,c])=>`.block[data-real-smart-note="${n}"],article[data-real-smart-note="${n}"]{--tone:${c}!important}`).join('')}`;document.head.appendChild(s)}
function color(){document.querySelectorAll('[data-real-smart-note]').forEach(e=>{const c=tones[e.getAttribute('data-real-smart-note')];if(c)e.style.setProperty('--tone',c,'important')})}
let scheduled=false;
function boot(){if(scheduled)return;scheduled=true;requestAnimationFrame(()=>{scheduled=false;css();const r=REAL();if(r&&typeof r.boot==='function')r.boot();color()})}
function observe(){if(window.__naya509RealLifecycleObserver)return;const root=document.body||document.documentElement;if(!root)return;const mo=new MutationObserver(()=>boot());mo.observe(root,{childList:true,subtree:true});window.__naya509RealLifecycleObserver=mo;document.addEventListener('click',e=>{if(e.target.closest('.feedNav button'))[0,40,150,500,1000,2000].forEach(ms=>setTimeout(boot,ms))},true);boot();setInterval(boot,750)}
function start(){css();observe()}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start,{once:true});else start();
})();
