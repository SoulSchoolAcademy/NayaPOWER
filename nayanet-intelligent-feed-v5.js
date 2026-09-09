/* NayaNET Intelligent Feed V5 — Intelligence Canvas
   Surgical runtime layer for the existing Intelligent Feed DOM.
   It changes presentation, not the Hub/data/navigation architecture.
*/
(()=>{
'use strict';
if(window.__NAYA_INTELLIGENT_FEED_V5__)return;
window.__NAYA_INTELLIGENT_FEED_V5__=true;
const ROOT='#nayanet-elite-feed';
const $=(s,r=document)=>r.querySelector(s);
const $$=(s,r=document)=>[...r.querySelectorAll(s)];
const spectrum=['#8b5cf6','#6675ff','#55b9ee','#55e39a','#b7e65b','#f2d45c','#e8c766','#ff9b52','#ff5d78','#d86cff'];
const perspectiveColors=['#d86cff','#8b5cf6','#6675ff','#55b9ee','#55e39a','#f2d45c','#e8c766'];
const labels=['HUMAN NOTE','CHILD NOTE','GRANDMA NOTE','NAYA NOTE','MACHINE NOTE','WHAT WE LEARNED','WHAT IT MEANS'];
function css(){if($('#naya-v5-style'))return;const s=document.createElement('style');s.id='naya-v5-style';s.textContent=`
/* NAYANET INTELLIGENCE CANVAS */
#nayanet-elite-feed{--v5-bg:#050507;--v5-white:#f7f7f4;position:relative;isolation:isolate}
#nayanet-elite-feed .intelligentFeedHead{position:relative;padding:22px 8px 28px;margin-bottom:0}
#nayanet-elite-feed .intelligentFeedHead:after{content:"";position:absolute;left:0;right:0;bottom:0;height:1px;background:linear-gradient(90deg,#8b5cf640,#55b9ee20,#55e39a40,#e8c76640,#d86cff30,transparent)}
#nayanet-elite-feed .feedPulse{width:9px;height:9px;box-shadow:0 0 14px #d86cff,0 0 30px #d86cff33}
#nayanet-elite-feed .intelligentFeedHead h2{font-size:clamp(25px,3vw,38px);letter-spacing:-.055em}
#nayanet-elite-feed .intelligentFeedHead p{font-size:10px;color:#99939f;letter-spacing:.01em}
#nayanet-elite-feed .feedCount{border-color:#ffffff1c;background:#ffffff06;color:#d7d1dc}
#nayanet-elite-feed .intelligentBlocks{position:relative}
#nayanet-elite-feed .intelligentBlocks:before{content:"";position:absolute;top:30px;bottom:30px;left:7px;width:1px;background:linear-gradient(180deg,transparent,#8b5cf655 8%,#55b9ee44 32%,#55e39a44 52%,#e8c76644 75%,#d86cff55 92%,transparent);box-shadow:0 0 18px #8b5cf618;pointer-events:none}
#nayanet-elite-feed .intelligentBlock{position:relative;padding:76px 34px 78px;margin:0;overflow:visible;border-bottom:0}
#nayanet-elite-feed .intelligentBlock:after{content:"";position:absolute;left:34px;right:0;bottom:0;height:1px;background:linear-gradient(90deg,var(--tone),#ffffff12 45%,transparent);opacity:.5}
#nayanet-elite-feed .intelligentBlock:first-child{padding-top:60px}
#nayanet-elite-feed .intelligentBlock:last-child:after{display:none}
#nayanet-elite-feed .intelligentBlock:before{content:"";position:absolute;left:-1px;top:78px;width:17px;height:17px;border-radius:50%;background:var(--tone);box-shadow:0 0 0 5px #050507,0 0 22px var(--tone),0 0 45px color-mix(in srgb,var(--tone) 35%,transparent);z-index:3}
#nayanet-elite-feed .intelligentBlock:nth-child(1){--tone:#8b5cf6}.intelligentBlock:nth-child(2){--tone:#6675ff}.intelligentBlock:nth-child(3){--tone:#55b9ee}.intelligentBlock:nth-child(4){--tone:#55e39a}.intelligentBlock:nth-child(5){--tone:#b7e65b}.intelligentBlock:nth-child(6){--tone:#f2d45c}.intelligentBlock:nth-child(7){--tone:#e8c766}.intelligentBlock:nth-child(8){--tone:#ff9b52}.intelligentBlock:nth-child(9){--tone:#ff5d78}.intelligentBlock:nth-child(10){--tone:#d86cff}.intelligentBlock:nth-child(11){--tone:#8b5cf6}
#nayanet-elite-feed .intelligentBlock:global{--tone:#8b5cf6}
#nayanet-elite-feed .blockHeader{position:relative;display:flex;align-items:flex-start;gap:22px;margin:0 0 30px;padding:0;z-index:2}
#nayanet-elite-feed .blockGlyph{width:52px;height:52px;border-radius:16px;border-color:color-mix(in srgb,var(--tone) 52%,#fff 4%);background:radial-gradient(circle at 35% 25%,color-mix(in srgb,var(--tone) 30%,transparent),#09090d 72%);box-shadow:inset 0 1px #fff6,0 14px 34px #000b,0 0 30px color-mix(in srgb,var(--tone) 13%,transparent);color:var(--tone)}
#nayanet-elite-feed .blockTitle h3{font-size:clamp(32px,4vw,58px);line-height:.94;letter-spacing:-.065em;margin:0 0 11px;color:#fff;text-shadow:0 1px 0 #fff1}
#nayanet-elite-feed .blockMeta{font-size:7px;letter-spacing:.12em;color:#8f8996}
#nayanet-elite-feed .demoBadge{border-color:color-mix(in srgb,var(--tone) 42%,transparent);color:color-mix(in srgb,var(--tone) 75%,#fff);background:color-mix(in srgb,var(--tone) 7%,transparent)}
#nayanet-elite-feed .blockBody{position:relative;margin:0 0 34px;padding:27px 30px 30px;border:1px solid #ffffff14;border-radius:24px;background:linear-gradient(145deg,#111117,#08080c 72%);box-shadow:inset 0 1px #fff5,0 26px 60px #000b;overflow:hidden}
#nayanet-elite-feed .blockBody:before{content:"";position:absolute;left:0;top:0;width:180px;height:1px;background:#fff;box-shadow:0 0 25px var(--tone),0 0 55px var(--tone);opacity:.8}
#nayanet-elite-feed .blockBody:after{content:"";position:absolute;right:-100px;top:-100px;width:280px;height:280px;border-radius:50%;background:radial-gradient(circle,color-mix(in srgb,var(--tone) 12%,transparent),transparent 67%);pointer-events:none}
#nayanet-elite-feed .blockBody p{position:relative;z-index:1;font-size:clamp(18px,1.7vw,23px);line-height:1.65;color:#f4f1f6;letter-spacing:-.012em;max-width:920px}
#nayanet-elite-feed .blockBody p:first-child:before{content:"IN A NUTSHELL";display:block;margin-bottom:11px;font-size:7px;line-height:1;letter-spacing:.2em;font-weight:1000;color:#fff}
#nayanet-elite-feed .blockTagRow{position:relative;z-index:1;margin-top:20px}
#nayanet-elite-feed .blockTag{border-color:#ffffff16;background:#07070a;color:#aaa4b0}
#nayanet-elite-feed .perspectiveMap{position:relative;margin:0;padding:4px 0 0}
#nayanet-elite-feed .perspectiveMap:before{left:20px;top:0;bottom:28px;width:1px;background:linear-gradient(180deg,#d86cff,#6675ff,#55b9ee,#55e39a,#f2d45c,#e8c766,transparent);opacity:.38;box-shadow:0 0 16px #8b5cf633}
#nayanet-elite-feed .perspective{position:relative;display:block;padding:0 0 43px 68px;min-height:0;background:transparent;border:0;border-radius:0;box-shadow:none;transition:transform .25s cubic-bezier(.16,.84,.22,1)}
#nayanet-elite-feed .perspective:before{left:15px;top:5px;width:11px;height:11px;background:var(--perspective);box-shadow:0 0 15px var(--perspective),0 0 30px color-mix(in srgb,var(--perspective) 28%,transparent);border:3px solid #050507}
#nayanet-elite-feed .perspective:after{content:"";position:absolute;left:21px;top:11px;width:32px;height:1px;background:linear-gradient(90deg,var(--perspective),transparent);opacity:.45}
#nayanet-elite-feed .perspective:hover{transform:translateX(4px)}
#nayanet-elite-feed .perspectiveHead{display:flex;align-items:center;gap:10px;margin:0 0 12px}
#nayanet-elite-feed .perspectiveHead b{font-size:8px;letter-spacing:.17em;color:var(--perspective);font-weight:1000}
#nayanet-elite-feed .perspectiveState{font-size:6px;color:#6f6975;letter-spacing:.1em}
#nayanet-elite-feed .perspective p{font-size:14px;line-height:1.72;color:#cbc6d0;margin:0;max-width:900px}
#nayanet-elite-feed .perspective:nth-child(1){--perspective:#d86cff}.perspective:nth-child(2){--perspective:#8b5cf6}.perspective:nth-child(3){--perspective:#6675ff}.perspective:nth-child(4){--perspective:#55b9ee}.perspective:nth-child(5){--perspective:#55e39a}.perspective:nth-child(6){--perspective:#f2d45c}.perspective:nth-child(7){--perspective:#e8c766}
#nayanet-elite-feed .perspective:nth-child(6) p{color:#e6dfbf}.perspective:nth-child(7) p{color:#eee9d8}
#nayanet-elite-feed .perspective.naya{background:transparent;min-height:0;display:block}
#nayanet-elite-feed .blockFooter{margin-top:0;padding:18px 0 0;border-top:1px solid #ffffff10;color:#68616e}
#nayanet-elite-feed .blockFooter span:last-child{color:#aaa4b0}
#nayanet-elite-feed .v5-actions{display:flex;align-items:center;gap:7px;flex-wrap:wrap;margin-top:4px}
#nayanet-elite-feed .v5-actions button{min-height:34px;padding:0 10px;border:1px solid #ffffff17;border-radius:10px;background:#08080c;color:#a9a3af;font-size:7px;font-weight:1000;letter-spacing:.07em;box-shadow:inset 0 1px #fff3;transition:.2s}
#nayanet-elite-feed .v5-actions button:hover,#nayanet-elite-feed .v5-actions button.active{color:#fff;border-color:color-mix(in srgb,var(--tone) 65%,transparent);box-shadow:0 0 20px color-mix(in srgb,var(--tone) 14%,transparent)}
#nayanet-elite-feed .v5-reveal{display:none;margin-top:18px;padding:17px 18px;border:1px solid #ffffff12;border-radius:14px;background:#07070a;color:#aaa4b0;font-size:10px;line-height:1.6}
#nayanet-elite-feed .intelligentBlock.v5-open .v5-reveal{display:block;animation:v5In .3s ease both}@keyframes v5In{from{opacity:0;transform:translateY(-5px)}to{opacity:1;transform:none}}
@media(max-width:900px){#nayanet-elite-feed .intelligentBlocks:before{left:0}.intelligentBlock:before{left:-7px}.intelligentBlock:after{left:12px}.intelligentBlock{padding:54px 12px 62px}.intelligentBlock:first-child{padding-top:42px}.blockHeader{gap:13px}.blockGlyph{width:43px;height:43px;border-radius:13px}.blockTitle h3{font-size:32px}.blockBody{padding:22px 20px 24px;border-radius:20px}.blockBody p{font-size:17px}.perspective{padding-left:51px}.perspectiveMap:before{left:13px}.perspective:before{left:8px}.perspective:after{left:14px;width:27px}.perspective p{font-size:13px;line-height:1.68}}
`;document.head.appendChild(s)}
function enhanceBlock(block,i){if(block.dataset.v5==='1')return;block.dataset.v5='1';block.style.setProperty('--tone',spectrum[i%spectrum.length]);const ps=$$('.perspective',block);ps.forEach((p,j)=>{p.style.setProperty('--perspective',perspectiveColors[j]||'#fff');const h=$('.perspectiveHead b',p);if(h&&labels[j])h.textContent=labels[j]});const meta=$('.blockMeta',block);if(meta&&!meta.querySelector('.v5-semantic')){const x=document.createElement('span');x.className='v5-semantic';x.textContent='INTELLIGENCE EVENT';meta.appendChild(x)}const footer=$('.blockFooter',block);if(footer&&!footer.querySelector('.v5-actions')){const actions=document.createElement('div');actions.className='v5-actions';actions.innerHTML='<button data-v5="save">＋ SAVE</button><button data-v5="share">↗ SHARE</button><button data-v5="explore">↓ EXPLORE</button>';footer.prepend(actions);actions.querySelector('[data-v5="explore"]').onclick=()=>{block.classList.toggle('v5-open');actions.querySelector('[data-v5="explore"]').textContent=block.classList.contains('v5-open')?'↑ CLOSE':'↓ EXPLORE'};actions.querySelector('[data-v5="save"]').onclick=e=>e.currentTarget.classList.toggle('active');actions.querySelector('[data-v5="share']).onclick=()=>{const title=$('.blockTitle h3',block)?.textContent?.trim()||'NayaNET Intelligence';const body=$('.blockBody p',block)?.textContent?.trim()||'';const text=title+'\n\n'+body+'\n\nNayaNET — Create. Connect. Grow with US.';if(navigator.share)navigator.share({title,text,url:location.href}).catch(()=>{});else if(navigator.clipboard)navigator.clipboard.writeText(text).then(()=>{actions.querySelector('[data-v5="share"]').textContent='✓ COPIED';setTimeout(()=>actions.querySelector('[data-v5="share"]').textContent='↗ SHARE',1200)})};}}
function boot(){const feed=$(ROOT);if(!feed)return;css();const blocks=$$('.intelligentBlock',feed);blocks.forEach(enhanceBlock);feed.dataset.v5Ready='1'}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});else boot();
let tries=0;const timer=setInterval(()=>{if(!$(ROOT)){if(++tries>20)clearInterval(timer);return}boot();if(++tries>20)clearInterval(timer)},400);
})();
