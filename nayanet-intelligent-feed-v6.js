(()=>{'use strict';
/* NayaNET Intelligent Feed V12.1 — TRUE LEGACY BOARD RECONSTRUCTION
   The existing intelligent boards remain the source of truth. The rejected renderer is removed.
   This layer transforms the proven board content into one premium vertical intelligence object. */
if(window.__NAYA_INTELLIGENT_FEED_V121__)return;window.__NAYA_INTELLIGENT_FEED_V121__=true;
const ROOT='#homeIntelligentBlocks',STYLE='naya-intelligent-v121-style';
const BAD_IDS=['nayanet-supreme-feed','naya-supreme-v11-style','naya-supreme-v12-style'];
const BAD_SELECTORS=['#nayanet-supreme-feed','.naya-supreme-v11','.naya-v11','.naya-v12','.supreme-v11'];
function css(){if(document.getElementById(STYLE))return;const s=document.createElement('style');s.id=STYLE;s.textContent=`
#homeIntelligentBlocks{position:relative;width:100%;max-width:1380px;margin:0 auto;padding:18px 0 110px;color:#f7f4fb;isolation:isolate}
#homeIntelligentBlocks:before{content:"";position:absolute;left:22px;top:0;bottom:70px;width:1px;background:linear-gradient(180deg,transparent 0%,#d86cff55 7%,#d86cff 22%,#8c70ff 52%,#55b9ee 72%,#e8c766 91%,transparent 100%);box-shadow:0 0 28px #9b72ff44;pointer-events:none}
#homeIntelligentBlocks>*,#homeIntelligentBlocks .intelligentBlock{position:relative;display:block!important;float:none!important;clear:both!important;width:calc(100% - 52px)!important;max-width:none!important;margin:0 0 54px 52px!important;padding:0!important;box-sizing:border-box;overflow:hidden;border:1px solid #ffffff18!important;border-radius:30px!important;background:radial-gradient(900px 420px at 85% -5%,#9b72ff16,transparent 62%),radial-gradient(600px 350px at 5% 100%,#55b9ee09,transparent 68%),linear-gradient(145deg,#15131b 0%,#0b0a0f 54%,#060609 100%)!important;box-shadow:inset 0 1px #ffffff0b,0 34px 90px #000d!important;transform:none!important}
#homeIntelligentBlocks>*>*,#homeIntelligentBlocks .intelligentBlock>*{box-sizing:border-box;max-width:100%!important;float:none!important;clear:both!important}
#homeIntelligentBlocks>*>*{width:100%!important}
#homeIntelligentBlocks>*>:first-child,#homeIntelligentBlocks .intelligentBlock>:first-child{padding-top:34px!important}
#homeIntelligentBlocks>*>:last-child,#homeIntelligentBlocks .intelligentBlock>:last-child{padding-bottom:34px!important}
#homeIntelligentBlocks>*>:before,#homeIntelligentBlocks .intelligentBlock:before{content:"";position:absolute;left:-53px;top:32px;width:10px;height:10px;border-radius:50%;background:#d86cff;box-shadow:0 0 0 6px #d86cff10,0 0 30px #d86cff;z-index:8}
#homeIntelligentBlocks>*>:after,#homeIntelligentBlocks .intelligentBlock:after{content:"";position:absolute;left:0;top:0;bottom:0;width:2px;background:linear-gradient(180deg,transparent,#d86cff 14%,#ffffff 45%,#8c70ff 70%,#e8c766 90%,transparent);box-shadow:0 0 34px #9b72ff;opacity:.9;pointer-events:none}
#homeIntelligentBlocks [class*="grid"],#homeIntelligentBlocks .grid2,#homeIntelligentBlocks .grid3,#homeIntelligentBlocks .grid4,#homeIntelligentBlocks .two-column,#homeIntelligentBlocks .twoColumn,#homeIntelligentBlocks .columns,#homeIntelligentBlocks [style*="grid-template-columns"],#homeIntelligentBlocks [style*="display:grid"]{display:block!important;grid-template-columns:none!important;grid-template-rows:none!important;columns:1!important;width:100%!important}
#homeIntelligentBlocks [class*="column"],#homeIntelligentBlocks .column,#homeIntelligentBlocks .col{display:block!important;width:100%!important;max-width:none!important;min-width:0!important;float:none!important}
#homeIntelligentBlocks [class*="row"],#homeIntelligentBlocks .row{display:block!important;width:100%!important;max-width:none!important}
#homeIntelligentBlocks [class*="card"],#homeIntelligentBlocks [class*="panel"],#homeIntelligentBlocks [class*="surface"]{width:100%!important;max-width:none!important;margin:0 0 16px!important;border:1px solid #ffffff14!important;border-radius:22px!important;background:linear-gradient(145deg,#14131a,#08080c)!important;box-shadow:inset 0 1px #ffffff08,0 22px 48px #000a!important}
#homeIntelligentBlocks h1,#homeIntelligentBlocks h2,#homeIntelligentBlocks h3,#homeIntelligentBlocks h4{color:#fff!important;letter-spacing:-.055em!important;text-wrap:balance}
#homeIntelligentBlocks h1{font-size:clamp(42px,6vw,78px)!important;line-height:.9!important;margin:0 0 14px!important}
#homeIntelligentBlocks h2{font-size:clamp(28px,3.6vw,48px)!important;line-height:.98!important;margin:0 0 13px!important}
#homeIntelligentBlocks h3{font-size:clamp(20px,2.5vw,34px)!important;line-height:1.03!important;margin:0 0 9px!important}
#homeIntelligentBlocks h4{font-size:clamp(14px,1.5vw,20px)!important;line-height:1.15!important}
#homeIntelligentBlocks p,#homeIntelligentBlocks li{color:#d9d5df!important;font-size:clamp(13px,1.08vw,17px)!important;line-height:1.72!important}
#homeIntelligentBlocks blockquote{position:relative;margin:28px 0!important;padding:28px 34px!important;border:1px solid #ffffff16!important;border-left:3px solid #d86cff!important;border-radius:5px 24px 24px 5px!important;background:linear-gradient(120deg,#d86cff0c,#ffffff03,transparent)!important;color:#faf7ff!important;font-size:clamp(21px,2.3vw,34px)!important;line-height:1.4!important;box-shadow:inset 0 1px #fff2,0 25px 55px #000a!important}
#homeIntelligentBlocks hr{height:1px!important;border:0!important;margin:30px 0!important;background:linear-gradient(90deg,#d86cff77,#ffffff18,transparent)!important}
#homeIntelligentBlocks img{max-width:100%!important;border-radius:20px!important;box-shadow:0 25px 60px #000b!important}
#homeIntelligentBlocks button{border-radius:14px!important;border:1px solid #ffffff22!important;background:linear-gradient(145deg,#191720,#08080c)!important;color:#fff!important;box-shadow:inset 0 1px #fff3,0 12px 30px #000a!important;transition:transform .25s ease,box-shadow .25s ease,border-color .25s ease!important}
#homeIntelligentBlocks button:hover{transform:translateY(-2px)!important;border-color:#d86cff70!important;box-shadow:inset 0 1px #fff5,0 18px 38px #000b,0 0 28px #d86cff14!important}
#homeIntelligentBlocks a{color:#e7cfff!important}
#homeIntelligentBlocks pre,#homeIntelligentBlocks code,#homeIntelligentBlocks kbd,#homeIntelligentBlocks samp{display:none!important}
#homeIntelligentBlocks .code,.codeBlock,.debug,.debug-output,.debugOutput,.implementation,.implementation-artifact{display:none!important}
#homeIntelligentBlocks [data-debug],#homeIntelligentBlocks [data-code],#homeIntelligentBlocks [data-implementation]{display:none!important}
#homeIntelligentBlocks .metricGrid,#homeIntelligentBlocks .flow{display:block!important}
#homeIntelligentBlocks .metric,#homeIntelligentBlocks .flow>div{display:flex!important;align-items:baseline!important;justify-content:space-between!important;gap:18px!important;margin:0 0 10px!important;padding:18px 20px!important;border:1px solid #ffffff15!important;border-radius:16px!important;background:#09090d!important}
@media(max-width:760px){#homeIntelligentBlocks{padding:5px 0 80px}#homeIntelligentBlocks:before{left:9px}#homeIntelligentBlocks>*,#homeIntelligentBlocks .intelligentBlock{width:calc(100% - 30px)!important;margin-left:30px!important;margin-bottom:34px!important;border-radius:24px!important}#homeIntelligentBlocks>*>:before,#homeIntelligentBlocks .intelligentBlock:before{left:-31px;top:26px;width:9px;height:9px}#homeIntelligentBlocks p,#homeIntelligentBlocks li{font-size:13px!important}#homeIntelligentBlocks blockquote{padding:21px 22px!important;font-size:20px!important}}
@media(prefers-reduced-motion:reduce){#homeIntelligentBlocks *{transition:none!important;animation:none!important;scroll-behavior:auto!important}}
`;document.head.appendChild(s)}
function removeRejected(){BAD_IDS.forEach(id=>{const n=document.getElementById(id);if(n)n.remove()});BAD_SELECTORS.forEach(sel=>document.querySelectorAll(sel).forEach(n=>n.remove())}
function cleanNode(root){root.querySelectorAll('pre,code,kbd,samp,.code,.codeBlock,.debug,.debug-output,.debugOutput,.implementation,.implementation-artifact,[data-debug],[data-code],[data-implementation]').forEach(n=>n.remove());root.querySelectorAll('[style]').forEach(n=>{const v=(n.getAttribute('style')||'').toLowerCase();if(v.includes('grid-template-columns')||v.includes('display:grid'))n.style.setProperty('display','block','important');if(v.includes('float:'))n.style.setProperty('float','none','important')});root.querySelectorAll('[class]').forEach(n=>{const c=String(n.className||'').toLowerCase();if(/(^|[-_])(debug|code|implementation)([-_]|$)/.test(c))n.remove()})}
function restore(){removeRejected();const root=document.querySelector(ROOT);if(!root)return false;root.hidden=false;root.removeAttribute('aria-hidden');root.style.display='block';css();cleanNode(root);root.dataset.nayaArchitecture='V12.1-TRUE-LEGACY-RECONSTRUCTION';return true}
let last=0;function boot(){const now=Date.now();if(now-last>500){last=now;restore()}requestAnimationFrame(boot)}boot();
})();