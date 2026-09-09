(()=>{'use strict';
/* NayaNET Intelligent Feed V12 — LEGACY-FIRST SUPREME RECONSTRUCTION
   Preserve the proven board DOM. Remove the failed two-column renderer. Elevate the existing boards in place. */
if(window.__NAYA_INTELLIGENT_FEED_V12__)return;window.__NAYA_INTELLIGENT_FEED_V12__=true;
const ROOT='#homeIntelligentBlocks',STYLE='naya-intelligent-v12-style';
function css(){if(document.getElementById(STYLE))return;const s=document.createElement('style');s.id=STYLE;s.textContent=`
#homeIntelligentBlocks{position:relative;width:100%;max-width:1280px;margin:0 auto;padding:10px 0 100px;color:#f7f4fb;isolation:isolate}
#homeIntelligentBlocks:before{content:"";position:absolute;left:18px;top:0;bottom:40px;width:1px;background:linear-gradient(180deg,transparent,#d86cff55 8%,#9b72ff,#55b9ee,#e8c766 88%,transparent);box-shadow:0 0 22px #9b72ff44;pointer-events:none}
#homeIntelligentBlocks>*,#homeIntelligentBlocks .intelligentBlock{position:relative;margin:0 0 42px 42px!important;padding:0!important;display:block!important;width:calc(100% - 42px)!important;max-width:none!important;float:none!important;clear:both!important;box-sizing:border-box;border:1px solid #ffffff18!important;border-radius:32px!important;background:radial-gradient(900px 340px at 82% 0%,#9b72ff12,transparent 64%),linear-gradient(145deg,#14131a,#09090d 58%,#050507)!important;box-shadow:inset 0 1px #ffffff09,0 34px 90px #000c!important;overflow:hidden!important;transform:none!important}
#homeIntelligentBlocks>*:before,#homeIntelligentBlocks .intelligentBlock:before{content:"";position:absolute;left:-43px;top:28px;width:9px;height:9px;border-radius:50%;background:#d86cff;box-shadow:0 0 0 5px #d86cff12,0 0 28px #d86cff;z-index:5}
#homeIntelligentBlocks>*:after,#homeIntelligentBlocks .intelligentBlock:after{content:"";position:absolute;left:0;top:0;bottom:0;width:2px;background:linear-gradient(180deg,transparent,#d86cff 18%,#fff 48%,#9b72ff 76%,transparent);box-shadow:0 0 30px #9b72ff;opacity:.8;pointer-events:none}
#homeIntelligentBlocks>*>*{max-width:100%!important}
#homeIntelligentBlocks h1,#homeIntelligentBlocks h2,#homeIntelligentBlocks h3,#homeIntelligentBlocks h4{letter-spacing:-.055em;color:#fff;text-wrap:balance}
#homeIntelligentBlocks h1{font-size:clamp(34px,5vw,68px)!important;line-height:.92!important;margin:0 0 12px!important}
#homeIntelligentBlocks h2{font-size:clamp(25px,3vw,43px)!important;line-height:1!important;margin:0 0 12px!important}
#homeIntelligentBlocks h3{font-size:clamp(20px,2.3vw,32px)!important;line-height:1.05!important}
#homeIntelligentBlocks p,#homeIntelligentBlocks li{color:#d8d3de;font-size:clamp(12px,1.05vw,16px)!important;line-height:1.72!important}
#homeIntelligentBlocks>*>:first-child,#homeIntelligentBlocks .intelligentBlock>:first-child{padding-top:28px!important}
#homeIntelligentBlocks [class*="grid"],#homeIntelligentBlocks .grid2,#homeIntelligentBlocks .grid3,#homeIntelligentBlocks .two-column,#homeIntelligentBlocks .twoColumn{display:grid!important;grid-template-columns:1fr!important}
#homeIntelligentBlocks [style*="grid-template-columns"]{grid-template-columns:1fr!important}
#homeIntelligentBlocks [class*="column"],#homeIntelligentBlocks .columns{display:block!important;width:100%!important;max-width:none!important}
#homeIntelligentBlocks>*>*,#homeIntelligentBlocks .intelligentBlock>*{box-sizing:border-box}
#homeIntelligentBlocks button{border-radius:13px!important;border:1px solid #ffffff22!important;background:linear-gradient(145deg,#17151e,#08080c)!important;color:#fff!important;box-shadow:inset 0 1px #fff3,0 12px 28px #0009!important;transition:transform .25s ease,box-shadow .25s ease,border-color .25s ease!important}
#homeIntelligentBlocks button:hover,#homeIntelligentBlocks a:hover{transform:translateY(-2px)!important;border-color:#d86cff70!important}
#homeIntelligentBlocks img{max-width:100%;border-radius:20px;box-shadow:0 20px 50px #000b}
#homeIntelligentBlocks blockquote{position:relative;margin:24px 0!important;padding:24px 30px!important;border-left:2px solid #d86cff!important;border-top:1px solid #ffffff12!important;border-right:1px solid #ffffff12!important;border-bottom:1px solid #ffffff12!important;border-radius:4px 22px 22px 4px!important;background:linear-gradient(120deg,#d86cff09,#ffffff03,transparent)!important;color:#f7f3fb!important;font-size:clamp(20px,2vw,31px)!important;line-height:1.4!important;box-shadow:inset 0 1px #fff2,0 22px 45px #0009!important}
#homeIntelligentBlocks hr{height:1px;border:0;background:linear-gradient(90deg,#d86cff66,#ffffff15,transparent)!important;margin:25px 0!important}
#homeIntelligentBlocks [class*="card"],#homeIntelligentBlocks [class*="surface"],#homeIntelligentBlocks [class*="panel"]{border-radius:20px!important;background:linear-gradient(145deg,#111117,#07070a)!important;border-color:#ffffff15!important;box-shadow:inset 0 1px #fff2,0 20px 45px #0009!important}
@media(max-width:760px){#homeIntelligentBlocks{padding:5px 0 70px}#homeIntelligentBlocks:before{left:8px}#homeIntelligentBlocks>*,#homeIntelligentBlocks .intelligentBlock{margin-left:24px!important;width:calc(100% - 24px)!important;border-radius:24px!important}#homeIntelligentBlocks>*:before,#homeIntelligentBlocks .intelligentBlock:before{left:-25px}#homeIntelligentBlocks p,#homeIntelligentBlocks li{font-size:13px!important}#homeIntelligentBlocks blockquote{padding:19px 20px!important;font-size:20px!important}}
@media(prefers-reduced-motion:reduce){#homeIntelligentBlocks *{scroll-behavior:auto!important;transition:none!important;animation:none!important}}
`;document.head.appendChild(s)}
function restore(){const root=document.querySelector(ROOT);if(!root)return false;const old=document.getElementById('nayanet-supreme-feed');if(old)old.remove();const bad=document.getElementById('naya-supreme-v11-style');if(bad)bad.remove();root.hidden=false;root.removeAttribute('aria-hidden');root.style.display='block';css();root.dataset.nayaArchitecture='V12-LEGACY-FIRST-SUPREME';return true}
function boot(){if(restore())return;requestAnimationFrame(boot)}
boot();
})();