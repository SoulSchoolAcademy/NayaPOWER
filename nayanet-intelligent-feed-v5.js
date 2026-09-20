(()=>{
'use strict';
if(window.__NAYA_INTELLIGENT_FEED_V5_WORLD_CLASS__)return;
window.__NAYA_INTELLIGENT_FEED_V5_WORLD_CLASS__=true;

const ROOT='#nayanet-elite-feed';
const SPECTRUM=['#8B5CF6','#6675FF','#55B9EE','#20D6C7','#55E39A','#B7E65B','#F2D45C','#E8C766','#FF9B52','#FF5D78','#D86CFF'];
const LAYERS=[
  ['HUMAN NOTE','#FF2FB3'],
  ['CHILD NOTE','#7C3AED'],
  ['GRANDMA NOTE','#4F46E5'],
  ['NAYA NOTE','#2563EB'],
  ['MACHINE NOTE','#16A34A'],
  ['WHAT WE LEARNED','#FACC15'],
  ['WHAT IT MEANS','#D4AF37']
];
const $=(s,r=document)=>r.querySelector(s);
const $$=(s,r=document)=>[...r.querySelectorAll(s)];

function install(){
  if($('#naya-world-class-feed-style'))return;
  const s=document.createElement('style');s.id='naya-world-class-feed-style';
  s.textContent=`
${ROOT}{--naya-bg:#050507;--naya-panel:#09090d;--naya-ink:#fff;--naya-muted:#918c98;position:relative}
${ROOT} .intelligentBlocks{position:relative;display:grid;gap:0;padding:8px 0 50px}
${ROOT} .intelligentBlocks:before{content:"";position:absolute;left:9px;top:38px;bottom:65px;width:1px;background:linear-gradient(180deg,transparent,#8B5CF6 8%,#6675FF 22%,#55B9EE 35%,#20D6C7 45%,#55E39A 57%,#B7E65B 68%,#F2D45C 77%,#E8C766 85%,#D86CFF 94%,transparent);opacity:.42;box-shadow:0 0 22px #8B5CF633;pointer-events:none}
${ROOT} .intelligentBlock{--tone:#8B5CF6;position:relative;margin:0;padding:58px 0 72px 48px;border:0!important;border-radius:0!important;background:transparent!important;overflow:visible!important;box-shadow:none!important}
${ROOT} .intelligentBlock:before{content:"";position:absolute;left:1px;top:65px;width:17px;height:17px;border-radius:50%;background:var(--tone);border:4px solid #050507;box-shadow:0 0 0 1px color-mix(in srgb,var(--tone) 55%,transparent),0 0 22px var(--tone),0 0 55px color-mix(in srgb,var(--tone) 28%,transparent);z-index:4}
${ROOT} .intelligentBlock:after{content:"";position:absolute;left:48px;right:0;bottom:0;height:1px;background:linear-gradient(90deg,var(--tone),#ffffff14 48%,transparent);opacity:.45}
${ROOT} .intelligentBlock:nth-child(1){--tone:#8B5CF6}.intelligentBlock:nth-child(2){--tone:#6675FF}.intelligentBlock:nth-child(3){--tone:#55B9EE}.intelligentBlock:nth-child(4){--tone:#20D6C7}.intelligentBlock:nth-child(5){--tone:#55E39A}.intelligentBlock:nth-child(6){--tone:#B7E65B}.intelligentBlock:nth-child(7){--tone:#F2D45C}.intelligentBlock:nth-child(8){--tone:#E8C766}.intelligentBlock:nth-child(9){--tone:#FF9B52}.intelligentBlock:nth-child(10){--tone:#FF5D78}.intelligentBlock:nth-child(11){--tone:#D86CFF}
${ROOT} .blockHeader{position:relative;display:grid;grid-template-columns:auto 1fr;column-gap:16px;align-items:start;margin-bottom:20px}
${ROOT} .blockGlyph{width:54px!important;height:54px!important;border-radius:16px!important;border:1px solid color-mix(in srgb,var(--tone) 55%,#fff 4%)!important;background:radial-gradient(circle at 35% 25%,color-mix(in srgb,var(--tone) 24%,transparent),#09090d 72%)!important;color:var(--tone)!important;box-shadow:inset 0 1px #fff7,0 16px 38px #000c,0 0 34px color-mix(in srgb,var(--tone) 14%,transparent)!important}
${ROOT} .blockTitle{min-width:0}
${ROOT} .blockTitle h3{font-size:clamp(31px,3.8vw,57px)!important;line-height:.94!important;letter-spacing:-.067em!important;margin:0 0 12px!important;color:#fff!important;text-wrap:balance}
${ROOT} .blockMeta{font-size:7px!important;line-height:1.4!important;letter-spacing:.14em!important;color:#8F8996!important;text-transform:uppercase}
${ROOT} .blockBody{position:relative;margin:0 0 38px!important;padding:27px 31px 30px!important;border:1px solid #ffffff16!important;border-radius:24px!important;background:linear-gradient(145deg,#111117,#08080c 72%)!important;box-shadow:inset 0 1px #fff5,0 30px 70px #000c,0 0 0 1px color-mix(in srgb,var(--tone) 5%,transparent)!important;overflow:hidden!important}
${ROOT} .blockBody:before{content:"";position:absolute;left:0;top:0;width:190px;height:1px;background:#fff;box-shadow:0 0 25px var(--tone),0 0 65px var(--tone);opacity:.82}
${ROOT} .blockBody:after{content:"";position:absolute;right:-130px;top:-130px;width:330px;height:330px;border-radius:50%;background:radial-gradient(circle,color-mix(in srgb,var(--tone) 11%,transparent),transparent 68%);pointer-events:none}
${ROOT} .blockBody p{position:relative;z-index:1;max-width:980px!important;margin:0!important;font-size:clamp(18px,1.65vw,23px)!important;line-height:1.66!important;letter-spacing:-.012em!important;color:#F5F2F7!important}
${ROOT} .blockBody p:first-child:before{content:"IN A NUTSHELL";display:block;margin-bottom:12px;font-size:7px;line-height:1;letter-spacing:.22em;font-weight:1000;color:#fff}
${ROOT} .perspectiveMap{position:relative;margin:0!important;padding:8px 0 4px!important}
${ROOT} .perspectiveMap:before{left:19px!important;top:2px!important;bottom:30px!important;width:1px!important;background:linear-gradient(180deg,#FF2FB3,#7C3AED,#4F46E5,#2563EB,#16A34A,#FACC15,#D4AF37,transparent)!important;opacity:.42!important;box-shadow:0 0 18px #6675ff30!important}
${ROOT} .perspective{--perspective:#fff;position:relative!important;display:block!important;min-height:0!important;padding:0 0 42px 67px!important;margin:0!important;border:0!important;border-radius:0!important;background:transparent!important;box-shadow:none!important;transition:transform .24s cubic-bezier(.16,.84,.22,1),opacity .24s ease!important}
${ROOT} .perspective:before{left:14px!important;top:5px!important;width:11px!important;height:11px!important;background:var(--perspective)!important;border:3px solid #050507!important;box-shadow:0 0 15px var(--perspective),0 0 30px color-mix(in srgb,var(--perspective) 28%,transparent)!important}
${ROOT} .perspective:after{content:"";position:absolute;left:22px;top:10px;width:32px;height:1px;background:linear-gradient(90deg,var(--perspective),transparent);opacity:.45}
${ROOT} .perspectiveHead{position:relative;z-index:1;margin:0 0 7px!important}
${ROOT} .perspectiveHead b{font-size:8px!important;line-height:1!important;letter-spacing:.18em!important;color:var(--perspective)!important;font-weight:1000!important}
${ROOT} .perspective p{position:relative;z-index:1;max-width:910px!important;margin:0!important;font-size:14px!important;line-height:1.75!important;color:#CCC7D1!important}
${ROOT} .perspective:nth-child(1){--perspective:#FF2FB3}.perspective:nth-child(2){--perspective:#7C3AED}.perspective:nth-child(3){--perspective:#4F46E5}.perspective:nth-child(4){--perspective:#2563EB}.perspective:nth-child(5){--perspective:#16A34A}.perspective:nth-child(6){--perspective:#FACC15}.perspective:nth-child(7){--perspective:#D4AF37}
${ROOT} .perspective:nth-child(6){padding-top:9px!important}.perspective:nth-child(6) p{font-size:16px!important;color:#F1E9B9!important;line-height:1.65!important}.perspective:nth-child(7){padding-top:12px!important;padding-bottom:31px!important}.perspective:nth-child(7) p{font-size:17px!important;color:#F2EEE3!important;line-height:1.68!important}
${ROOT} .intelligentBlock:hover .blockBody{border-color:color-mix(in srgb,var(--tone) 18%,#fff 3%)!important;box-shadow:inset 0 1px #fff6,0 30px 70px #000c,0 0 34px color-mix(in srgb,var(--tone) 7%,transparent)!important}
${ROOT} .intelligentBlock:hover:before{box-shadow:0 0 0 1px color-mix(in srgb,var(--tone) 75%,transparent),0 0 26px var(--tone),0 0 62px color-mix(in srgb,var(--tone) 36%,transparent)}
${ROOT} .perspective:hover{transform:translateX(5px)!important}
${ROOT} .naya-v5-actionbar{display:flex;align-items:center;gap:6px;flex-wrap:wrap;margin-top:10px;padding-top:15px;border-top:1px solid #ffffff10}
${ROOT} .naya-v5-action{display:inline-flex;align-items:center;justify-content:center;gap:7px;min-height:35px;padding:0 11px;border:1px solid #ffffff18;border-radius:10px;background:linear-gradient(145deg,#0d0d12,#07070a);color:#A8A2AE;font-size:7px;font-weight:1000;letter-spacing:.08em;transition:.2s ease;box-shadow:inset 0 1px #fff3}
${ROOT} .naya-v5-action:hover{color:#fff;border-color:color-mix(in srgb,var(--tone) 58%,transparent);box-shadow:inset 0 1px #fff4,0 0 22px color-mix(in srgb,var(--tone) 13%,transparent);transform:translateY(-1px)}
${ROOT} .naya-v5-action.active{color:#fff;border-color:var(--tone);background:color-mix(in srgb,var(--tone) 12%,#07070a);box-shadow:0 0 20px color-mix(in srgb,var(--tone) 15%,transparent)}
${ROOT} .naya-v5-reveal{display:none;margin-top:15px;padding:15px 17px;border:1px solid #ffffff12;border-radius:14px;background:#060609;color:#AAA4B0;font-size:10px;line-height:1.65}.intelligentBlock.naya-v5-open .naya-v5-reveal{display:block}
@media(max-width:900px){${ROOT} .intelligentBlocks:before{left:4px}.intelligentBlock{padding:46px 0 58px 30px!important}.intelligentBlock:before{left:-4px!important;top:53px!important;width:14px!important;height:14px!important}.intelligentBlock:after{left:30px!important}.blockHeader{column-gap:12px}.blockGlyph{width:44px!important;height:44px!important;border-radius:13px!important}.blockTitle h3{font-size:31px!important}.blockBody{padding:22px 20px 24px!important;border-radius:20px!important}.blockBody p{font-size:17px!important}.perspectiveMap:before{left:12px!important}.perspective{padding-left:49px!important}.perspective:before{left:7px!important}.perspective:after{left:14px!important;width:25px!important}.perspective p{font-size:13px!important}.perspective:nth-child(6) p,.perspective:nth-child(7) p{font-size:14px!important}}
@media(max-width:560px){${ROOT} .intelligentBlock{padding-left:22px!important}.intelligentBlock:after{left:22px!important}.blockHeader{grid-template-columns:1fr}.blockGlyph{margin-bottom:13px}.blockTitle h3{font-size:29px!important}.blockBody{padding:20px 17px 21px!important}.perspective{padding-left:43px!important}.naya-v5-action{min-height:34px}}
`;
  document.head.appendChild(s);
}

function addActions(block){
  const footer=$('.blockFooter',block);if(!footer||$('.naya-v5-actionbar',footer))return;
  const bar=document.createElement('div');bar.className='naya-v5-actionbar';
  const make=(label,fn)=>{const b=document.createElement('button');b.type='button';b.className='naya-v5-action';b.textContent=label;b.onclick=fn;bar.appendChild(b);return b};
  const save=make('＋ SAVE',()=>save.classList.toggle('active'));
  const share=make('↗ SHARE INTEL',async()=>{
    const title=$('.blockTitle h3',block)?.textContent?.trim()||'NayaNET Intelligence';
    const nutshell=$('.blockBody p',block)?.textContent?.trim()||'';
    const text=title+'\n\n'+nutshell+'\n\nNayaNET — Create. Connect. Grow with US.';
    try{if(navigator.share)await navigator.share({title,text,url:location.href});else if(navigator.clipboard){await navigator.clipboard.writeText(text);share.textContent='✓ COPIED';setTimeout(()=>share.textContent='↗ SHARE INTEL',1400)}}catch(e){}
  });
  const explore=make('◉ EXPLORE',()=>{block.classList.toggle('naya-v5-open');explore.textContent=block.classList.contains('naya-v5-open')?'↑ CLOSE':'◉ EXPLORE'});
  const reveal=document.createElement('div');reveal.className='naya-v5-reveal';reveal.textContent='Explore the complete intelligence chain — Human → Child → Grandma → Naya → Machine → Learning → Meaning.';
  footer.prepend(reveal);footer.prepend(bar);
}

function enhance(block,i){
  if(block.dataset.nayaWorldClass==='1')return;
  block.dataset.nayaWorldClass='1';
  block.style.setProperty('--tone',SPECTRUM[i%SPECTRUM.length]);
  const ps=$$('.perspective',block);
  ps.forEach((p,j)=>{
    const [label,color]=LAYERS[j]||['INTELLIGENCE','#fff'];
    p.style.setProperty('--perspective',color);
    const h=$('.perspectiveHead b',p);if(h)h.textContent=label;
  });
  const meta=$('.blockMeta',block);
  if(meta&&!meta.querySelector('.naya-event-label')){const e=document.createElement('span');e.className='naya-event-label';e.textContent=' · INTELLIGENCE EVENT';meta.appendChild(e)}
  addActions(block);
}

function boot(){
  const root=$(ROOT);if(!root)return;
  install();
  const blocks=$$('.intelligentBlock',root);
  blocks.forEach(enhance);
  // Enforce the current product law: no permanent right rail.
  $$('.rightRail,.rightSidebar,.smartNotesRail,.operationsRail',document).forEach(el=>{el.style.display='none'});
  root.dataset.nayaWorldClassReady=blocks.length?'true':'false';
}

if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});else boot();
const observer=new MutationObserver(()=>boot());
observer.observe(document.documentElement,{childList:true,subtree:true});
})();
