/* NayaNET V11 — final 10/10 hierarchy and spatial polish.
   Surgical layer over V10. No new intelligence model; only authority, spacing,
   alignment, responsive ergonomics, and visual hierarchy are refined.
*/
(()=>{
'use strict';
if(window.__NAYANET_V11_FINAL_POLISH__) return;
window.__NAYANET_V11_FINAL_POLISH__=true;
const style=document.createElement('style');
style.textContent=`
:root{--n11-gold:#e8c766;--n11-line:#ffffff18}
/* CENTER = intelligence; RIGHT = intelligence operations. */
.n11-ready .main{margin-right:336px!important;padding-left:32px!important;padding-right:32px!important}
.n11-ready #nayanet-elite-feed{width:100%!important;max-width:1180px!important;margin-left:auto!important;margin-right:auto!important}
.n11-ready #nayanet-elite-feed .n3-tabs{margin-bottom:12px!important}
.n11-ready #nayanet-elite-feed .n3-body{margin-top:0!important;padding-top:0!important}
.n11-ready #nayanet-elite-feed .n3-bottom{margin-top:34px!important;padding-top:24px!important}
/* The rail starts beneath the global top bar and never competes with it. */
.n10-rail{top:88px!important;right:16px!important;width:304px!important;gap:12px!important;max-height:calc(100vh - 104px)!important}
.n10-report{border-radius:20px!important;padding:19px!important;border-color:#e8c76658!important;box-shadow:inset 0 1px #fff7,0 24px 60px #000e,0 0 34px #e8c76612!important}
.n10-report-icon{width:42px!important;height:42px!important;border-radius:13px!important;margin-bottom:12px!important}
.n10-report-copy span{font-size:7px!important;color:#e8c766!important}
.n10-report-copy strong{font-size:16px!important;color:#fff!important}
.n10-report-copy small{color:#d4cfda!important;font-size:9px!important}
.n10-report-btn{min-height:41px!important;border-radius:12px!important;background:#050505!important}
.n10-connect{border-radius:20px!important;padding:14px!important}
.n10-rail-label{color:#9b95a2!important;padding:2px 4px 8px!important}
.n10-connect-btn{min-height:60px!important;border-radius:13px!important;background:#020203!important}
.n10-connect-btn:hover,.n10-connect-btn:focus-visible{border-color:#ffffff42!important;background:#08080b!important;transform:translateY(-1px)}
.n10-connect-btn:focus-visible,.n10-report-btn:focus-visible{outline:2px solid #e8c766!important;outline-offset:2px}
/* Remove accidental competing authority if a legacy layer recreates these labels. */
.n11-ready .sidebar .n10-legacy-intelligence,.n11-ready .sidebar [data-intelligence-block],.n11-ready .sidebar [data-smart-note]{display:none!important}
@media(max-width:1120px){
 .n11-ready .main{margin-right:0!important;padding-left:24px!important;padding-right:24px!important}
 .n10-rail{position:relative!important;top:auto!important;right:auto!important;width:auto!important;margin:8px 24px 28px!important;max-height:none!important}
 .n11-ready #nayanet-elite-feed{max-width:1180px!important}
}
@media(max-width:820px){
 .n11-ready .main{padding-left:12px!important;padding-right:12px!important}
 .n10-rail{margin:8px 12px 22px!important}
 .n10-report{padding:16px!important}
 .n10-connect{padding:12px!important}
 .n10-connect-btn{min-height:56px!important}
}
@media(prefers-reduced-motion:reduce){.n10-connect-btn{transition:none!important}}
`;
document.head.appendChild(style);
function apply(){
 document.documentElement.classList.add('n11-ready');
 const feed=document.querySelector('#nayanet-elite-feed');
 if(!feed)return;
 const tabs=feed.querySelector('.n3-tabs');
 const body=feed.querySelector('.n3-body');
 const footer=feed.querySelector('.n3-bottom');
 if(tabs&&body){body.style.marginTop='0';body.style.paddingTop='0';}
 if(footer&&body&&footer.previousElementSibling!==body)feed.appendChild(footer);
}
apply();
new MutationObserver(apply).observe(document.body,{childList:true,subtree:true});
})();
