/* NayaNET 509 C4 — NAV-ADJACENT SMART NOTE PLACEMENT
 * Surgical presentation-only layer.
 * It does not invent, edit, delete, or reorder Smart Note content.
 * It only places the already-rendered canonical .blocks container directly
 * after the sacred three-control .feedNav, preserving all existing behavior.
 */
(()=>{'use strict';
 const KEY='naya509NavAdjacentPlacement';
 function place(){
  const nav=document.querySelector('.feedNav');
  const blocks=document.querySelector('.blocks');
  if(!nav||!blocks)return false;
  if(nav.nextElementSibling!==blocks)nav.insertAdjacentElement('afterend',blocks);
  blocks.dataset.naya509NavAdjacent='true';
  return blocks.querySelectorAll('[data-real-smart-note]').length===9;
 }
 function boot(){
  place();
  if(document.documentElement.dataset[KEY]==='1')return;
  document.documentElement.dataset[KEY]='1';
  const mo=new MutationObserver(()=>{place()});
  mo.observe(document.body,{childList:true,subtree:true});
 }
 window.Naya509NavAdjacentPlacement={boot,place,version:'c4-nav-adjacent-1'};
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});else boot();
})();
