(()=>{'use strict';
/*
 * Canonical Hub runtime loader.
 * Smart Tabs is no longer a destination; this entry point loads the governed
 * intelligence-surface runtime and then the 58-domain Library experience.
 */
function removeLegacy(){document.getElementById('naya-smart-tabs')?.remove()}
function loadLibrary(){
  if(document.querySelector('script[data-naya-library-58]'))return;
  const s=document.createElement('script');
  s.src='/NAYANET/HUB/intelligent-library-58.js';
  s.dataset.nayaLibrary58='1';
  s.async=false;
  document.head.append(s);
}
function boot(){
  removeLegacy();
  const src='/NAYANET/HUB/intelligence-surfaces-runtime.js';
  const existing=document.querySelector('script[data-naya-real-surfaces]');
  if(existing){
    existing.addEventListener('load',loadLibrary,{once:true});
    if(window.NayaAssistantRuntime) loadLibrary();
    return;
  }
  const s=document.createElement('script');
  s.src=src;s.dataset.nayaRealSurfaces='1';s.async=false;
  s.addEventListener('load',loadLibrary,{once:true});
  document.head.append(s);
  setTimeout(removeLegacy,250);
  setTimeout(removeLegacy,1000);
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});else boot();
})();