/* NayaNET Intelligent Feed V4 — Interior Evolution
 * Surgical additive layer. V3 remains the feed authority; this layer evolves the interior experience only.
 * Design intent: living intelligence library / black dimensional chambers / spectral outer identity / white nutshell / semantic perspective boards.
 */
(()=>{
'use strict';
const ROOT='nayanet-elite-feed';
const SPECTRUM=['#ff3b30','#ff8a00','#e8c766','#f4e94d','#b8e64c','#39b54a','#28b7a8','#3b82f6','#4f7cff','#7c3aed','#d946ef','#ffffff'];
const ICONS={
 human:'<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="7" r="3.2"/><path d="M5.5 20c.7-4 3-6 6.5-6s5.8 2 6.5 6"/></svg>',
 child:'<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="7.5"/><circle cx="9.2" cy="10.5" r=".8"/><circle cx="14.8" cy="10.5" r=".8"/><path d="M9 14.2c1.7 1.4 4.3 1.4 6 0"/></svg>',
 grandma:'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 18v-5a5 5 0 0 1 10 0v5"/><path d="M5.5 18h13M8 8.5c.7-2.2 2.1-3.5 4-3.5s3.3 1.3 4 3.5"/><circle cx="9" cy="14" r="1"/><circle cx="15" cy="14" r="1"/></svg>',
 naya:'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.8l1.5 6.2 5.7 1.5-5.7 1.5L12 18.2l-1.5-6.2-5.7-1.5 5.7-1.5L12 2.8z"/><path d="M18.2 16.2l.7 2.5 2.3.7-2.3.7-.7 2.5-.7-2.5-2.3-.7 2.3-.7.7-2.5z"/></svg>',
 machine:'<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="5" y="5" width="14" height="14" rx="3"/><path d="M9 9h6v6H9zM2.5 9h2.5M2.5 15h2.5M19 9h2.5M19 15h2.5M9 2.5V5M15 2.5V5M9 19v2.5M15 19v2.5"/></svg>',
 learning:'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3l7 3v5.5c0 4.4-2.9 7.4-7 9.5-4.1-2.1-7-5.1-7-9.5V6l7-3z"/><path d="M8.5 11.5l2.2 2.2 4.8-5"/></svg>'
};
function addStyle(){
 if(document.getElementById('n4-interior-style')) return;
 const s=document.createElement('style');s.id='n4-interior-style';
 s.textContent=`
#${ROOT}{--n4-radius:28px}
#${ROOT} .n3-body{gap:14px}
#${ROOT} .n3-block{border-radius:var(--n4-radius);border-color:color-mix(in srgb,var(--spectrum) 48%,#fff 5%);box-shadow:inset 0 1px #fff6,0 26px 70px #000e,0 0 34px color-mix(in srgb,var(--spectrum) 12%,transparent);isolation:isolate}
#${ROOT} .n3-block:hover{transform:translateY(-3px);border-color:color-mix(in srgb,var(--spectrum) 78%,#fff 8%);box-shadow:inset 0 1px #fff8,0 34px 80px #000e,0 0 55px color-mix(in srgb,var(--spectrum) 20%,transparent)}
#${ROOT} .n3-block:before{left:0;right:0;top:0;bottom:0;width:auto;height:auto;background:linear-gradient(90deg,color-mix(in srgb,var(--spectrum) 92%,#fff 8%),transparent 18%,transparent 82%,color-mix(in srgb,var(--spectrum) 72%,transparent));border:1px solid color-mix(in srgb,var(--spectrum) 70%,transparent);border-radius:inherit;box-shadow:0 0 24px color-mix(in srgb,var(--spectrum) 36%,transparent),inset 0 0 22px color-mix(in srgb,var(--spectrum) 7%,transparent);opacity:.9;pointer-events:none;z-index:0}
#${ROOT} .n3-block:after{z-index:0;opacity:.08;background:radial-gradient(circle at 12% 5%,var(--spectrum),transparent 54%)}
#${ROOT} .n3-head,#${ROOT} .n3-nutshell,#${ROOT} .n3-perspectives,#${ROOT} .n3-footer{position:relative;z-index:1}
#${ROOT} .n3-head{padding:24px 25px 18px}
#${ROOT} .n3-title{font-weight:850}
#${ROOT} .n3-nutshell{margin:18px 18px 14px;padding:23px 24px 25px;border-color:#ffffff70;background:linear-gradient(145deg,#0b0b0e,#030305);box-shadow:inset 0 1px #fff9,0 20px 44px #000c,0 0 36px #fff1;transform:translateY(-1px)}
#${ROOT} .n3-nutshell:after{content:"";position:absolute;left:10px;right:10px;bottom:-9px;height:9px;border-radius:0 0 16px 16px;background:#010102;box-shadow:0 10px 20px #000c}
#${ROOT} .n3-nutshell:before{width:3px;top:13px;bottom:13px;background:linear-gradient(#fff,#fff8,transparent);box-shadow:0 0 18px #fff}
#${ROOT} .n3-nutshell p{font-size:16px;line-height:1.6;max-width:1020px}
#${ROOT} .n3-perspectives{gap:10px;padding:8px 18px 5px}
#${ROOT} .n3-perspective{border-radius:19px;min-height:0;background:linear-gradient(145deg,#09090c,#020203);border-color:color-mix(in srgb,var(--p) 72%,#fff 5%);box-shadow:inset 0 1px #fff4,0 12px 28px #000b,0 0 28px color-mix(in srgb,var(--p) 11%,transparent);transition:transform .22s ease,box-shadow .22s ease,border-color .22s ease}
#${ROOT} .n3-perspective:hover{transform:translateX(2px);border-color:color-mix(in srgb,var(--p) 92%,#fff 10%);box-shadow:inset 0 1px #fff6,0 15px 32px #000c,0 0 34px color-mix(in srgb,var(--p) 17%,transparent)}
#${ROOT} .n3-perspective:before{width:3px;box-shadow:0 0 18px var(--p)}
#${ROOT} .n3-phead{padding:13px 15px 10px}
#${ROOT} .n3-picon{width:32px;height:32px;border-radius:10px;font-size:0;box-shadow:0 0 20px color-mix(in srgb,var(--p) 18%,transparent),inset 0 1px #fff3}
#${ROOT} .n3-picon svg{width:18px;height:18px;fill:none;stroke:#fff;stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round;filter:drop-shadow(0 0 6px var(--p))}
#${ROOT} .n3-phead b{font-size:8px;letter-spacing:.18em}
#${ROOT} .n3-pbody{padding:13px 15px 16px;font-size:12px;line-height:1.68;color:#fff}
#${ROOT} .n4-learning{border-color:#e8c76690!important;background:linear-gradient(145deg,#0d0c08,#030303)!important;box-shadow:inset 0 1px #fff5,0 14px 34px #000c,0 0 34px #e8c76619!important}
#${ROOT} .n4-learning .n3-picon{background:#e8c7660d;border-color:#e8c76680;box-shadow:0 0 22px #e8c76625,inset 0 1px #fff4}
#${ROOT} .n4-learning .n3-picon svg{filter:drop-shadow(0 0 7px #e8c766);stroke:#fff}
#${ROOT} .n4-learning .n3-phead b{color:#fff}
#${ROOT} .n4-learning .n3-pbody strong{color:#fff}
#${ROOT} .n3-footer{padding:15px 18px 20px}
@media(max-width:820px){#${ROOT} .n3-nutshell{margin:14px 12px 12px;padding:19px}#${ROOT} .n3-nutshell p{font-size:13.5px}#${ROOT} .n3-perspectives{padding:7px 12px 4px}#${ROOT} .n3-pbody{font-size:11.2px}}
`;
 document.head.appendChild(s);
}
function iconFor(type){return ICONS[type]||ICONS.naya}
function evolveBlock(block,index){
 const spectrum=SPECTRUM[index%SPECTRUM.length];
 block.style.setProperty('--spectrum',spectrum);
 block.dataset.n4Spectrum=String(index%SPECTRUM.length);
 const ps=[...block.querySelectorAll('.n3-perspective')];
 const types=['human','child','grandma','naya','machine','learning'];
 ps.slice(0,6).forEach((p,i)=>{
   const type=types[i];p.style.setProperty('--p',type==='human'?'#d86cff':type==='child'?'#7c3aed':type==='grandma'?'#6675ff':type==='naya'?'#3b82f6':type==='machine'?'#39d98a':'#e8c766');
   const icon=p.querySelector('.n3-picon');if(icon) icon.innerHTML=iconFor(type);
 });
 if(ps.length>=7){
   const lesson=ps[5], use=ps[6];
   const body=lesson.querySelector('.n3-pbody');
   const useBody=use.querySelector('.n3-pbody');
   const head=lesson.querySelector('.n3-phead b');
   const icon=lesson.querySelector('.n3-picon');
   if(head) head.textContent='WHAT WE LEARNED · WHAT IT MEANS';
   if(icon) icon.innerHTML=iconFor('learning');
   lesson.classList.add('n4-learning');lesson.style.setProperty('--p','#e8c766');
   if(body && useBody){
     const text=body.innerHTML;
     body.innerHTML='<strong>The lesson:</strong> '+text+'<br><br><strong>What it means:</strong> '+useBody.innerHTML;
   }
   use.remove();
 }
}
function run(){
 const root=document.getElementById(ROOT);if(!root) return false;
 addStyle();
 [...root.querySelectorAll('.n3-block')].forEach((b,i)=>evolveBlock(b,i));
 root.dataset.n4='INTERIOR_EVOLUTION_ACTIVE';
 return true;
}
let tries=0;const boot=()=>{if(run()||tries++>60)return;setTimeout(boot,120)};
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});else boot();
})();
