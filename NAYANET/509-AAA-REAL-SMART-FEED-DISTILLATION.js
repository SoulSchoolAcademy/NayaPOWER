/* NayaNET 509 AAA — REAL SMART FEED DISTILLATION
 * Surgical presentation layer only. It distills the already-rendered canonical
 * Smart Note perspectives into a fast-skim "WHAT MATTERS" block without replacing
 * C4 architecture, source content, or interaction nodes.
 */
(()=>{'use strict';
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function text(el){return (el?.innerText||'').replace(/\s+/g,' ').trim()}
function findLayer(board,name){return [...board.querySelectorAll('.layer')].find(x=>new RegExp(`^${name}$`,'i').test(text(x.querySelector('.layerHead b'))))}
function distill(board){
 if(board.querySelector('.naya509-distill'))return;
 const nutshell=text(board.querySelector('.nutshell p'));
 const meaning=text(findLayer(board,'ULTIMATE MEANING')?.querySelector('.layerBody'));
 const value=text(findLayer(board,"WHAT'S IN IT FOR YOU\?",)?.querySelector('.layerBody'));
 const points=[nutshell,meaning,value].filter(Boolean).map(x=>x.replace(/^In a nutshell\s*/i,''));
 if(!points.length)return;
 const short=points.map(x=>x.length>300?x.slice(0,297).replace(/\s+$/,'')+'…':x);
 const d=document.createElement('section');d.className='naya509-distill';d.setAttribute('aria-label','Distilled intelligence');
 d.innerHTML=`<div class="naya509-distill-label">WHAT MATTERS</div><div class="naya509-distill-title">${esc(short[0]||'')}</div>${short.slice(1).map(x=>`<p>${esc(x)}</p>`).join('')}`;
 const top=board.querySelector('.blockTop');if(top)top.after(d);else board.prepend(d);
}
function style(){if(document.getElementById('naya509-distill-style'))return;const s=document.createElement('style');s.id='naya509-distill-style';s.textContent=`
.naya509-distill{margin:22px 0 28px;padding:18px 22px 20px;border:1px solid color-mix(in srgb,var(--tone,#ffffff) 72%,#ffffff 18%);border-left:5px solid var(--tone,#ffffff);border-radius:18px;background:linear-gradient(135deg,#ffffff0d,#ffffff04);box-shadow:inset 0 1px #ffffff12,0 12px 32px #0007;}
.naya509-distill-label{font-size:13px!important;letter-spacing:.16em;font-weight:800;color:var(--tone,#fff);margin-bottom:7px}
.naya509-distill-title{font-size:21px!important;line-height:1.42!important;font-weight:750;color:#fff;}
.naya509-distill p{margin:7px 0 0;font-size:18px!important;line-height:1.48!important;color:#e9e4ed;font-weight:560}
@media(max-width:760px){.naya509-distill{margin:16px 0 22px;padding:16px 17px}.naya509-distill-title{font-size:19px!important}.naya509-distill p{font-size:17px!important}}
`;document.head.appendChild(s)}
function run(){const boards=[...document.querySelectorAll('.naya509-board[data-real-smart-note]')];if(!boards.length)return;boards.forEach(distill);document.documentElement.dataset.nayaRealSmartFeedDistilled=String(boards.length)}
function boot(){style();run();const b=document.querySelector('.blocks');if(b&&!b.dataset.nayaRealDistillObserver){new MutationObserver(()=>run()).observe(b,{childList:true,subtree:true});b.dataset.nayaRealDistillObserver='1'}}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});else boot();
})();
