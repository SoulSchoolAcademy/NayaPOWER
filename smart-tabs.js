(()=>{'use strict';
/*
 * Smart Tabs is intentionally not rendered in the canonical Hub.
 * The Hub's ten fixed intelligence surfaces are the navigation model.
 * This compatibility shim removes any legacy Smart Tabs DOM if an older
 * bundle or cached deployment creates it.
 */
function removeLegacySmartTabs(){
  document.getElementById('naya-smart-tabs')?.remove();
}
if(document.readyState==='loading'){
  document.addEventListener('DOMContentLoaded',removeLegacySmartTabs,{once:true});
}else{
  removeLegacySmartTabs();
}
setTimeout(removeLegacySmartTabs,500);
setTimeout(removeLegacySmartTabs,1500);
})();