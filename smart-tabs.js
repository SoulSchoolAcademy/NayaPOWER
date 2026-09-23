(()=>{'use strict';
/*
 * Legacy Smart Tabs compatibility entry point.
 * The old Smart Tabs / Your Navigation panel has no product value in the
 * canonical Hub. This entry point removes it and boots the real ten-surface
 * intelligence experience instead.
 */
function removeLegacy(){document.getElementById('naya-smart-tabs')?.remove()}
function boot(){
  removeLegacy();
  const src='/NAYANET/HUB/intelligence-surfaces-runtime.js';
  if(document.querySelector('script[data-naya-real-surfaces]'))return;
  const s=document.createElement('script');
  s.src=src;s.dataset.nayaRealSurfaces='1';s.async=false;
  document.head.append(s);
  setTimeout(removeLegacy,250);
  setTimeout(removeLegacy,1000);
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});else boot();
})();