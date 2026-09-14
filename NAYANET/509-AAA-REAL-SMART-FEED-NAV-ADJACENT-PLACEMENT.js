/* NayaNET 509 C4 — NAV-ADJACENT SMART NOTE CONTENT PLACEMENT
 * CONSTITUTIONAL SURGICAL LAYER.
 * Preserve the existing Hub, three-feed navigation, Smart Note structure,
 * typography, controls, spacing, and behavior. Do not invent a new card system.
 * The only content operation is source-derived distillation inside the existing
 * nine Smart Note cards. Each card remains content-responsive and may grow
 * vertically when its distilled text requires additional room.
 */
(()=>{'use strict';
 const KEY='naya509NavAdjacentPlacement';
 const TONES=['#35e69a','#b8ee57','#f4e45b','#e8c766','#ff9b4a','#ff5e6c','#ffffff','#ff9fda','#ff4fd8'];
 const SENTENCE_LIMIT=2;
 function text(el){return (el?.innerText||'').replace(/\s+/g,' ').trim()}
 function distill(value,max=520){
  let s=String(value||'').replace(/\s+/g,' ').trim();
  if(!s)return '';
  const sentences=s.match(/[^.!?]+[.!?]+(?:\s|$)/g)||[];
  if(sentences.length>SENTENCE_LIMIT)s=sentences.slice(0,SENTENCE_LIMIT).join(' ').trim();
  if(s.length>max)s=s.slice(0,max-1).replace(/\s+$/,'')+'…';
  return s;
 }
 function applyNoteContent(board,idx){
  board.style.setProperty('--tone',TONES[idx],'important');
  board.querySelectorAll('.layer').forEach(layer=>layer.style.setProperty('--layer',TONES[idx],'important'));
  const nutshell=board.querySelector('.nutshell p');
  if(nutshell){
   const source=text(nutshell);
   const short=distill(source,620);
   if(short)nutshell.textContent=short;
  }
  board.querySelectorAll('.layerBody').forEach(bodyEl=>{
   const source=text(bodyEl);
   const short=distill(source,430);
   if(short)bodyEl.textContent=short;
  });
  board.querySelectorAll('.naya509-distill').forEach(e=>e.remove());
  board.style.setProperty('min-height','0','important');
  board.style.setProperty('height','auto','important');
  board.style.setProperty('overflow','visible','important');
  board.dataset.naya509ContentDistilled='true';
  board.dataset.naya509Tone=String(idx+1);
 }
 function place(){
  const nav=document.querySelector('.feedNav');
  const blocks=document.querySelector('.blocks');
  if(!nav||!blocks)return false;
  if(nav.nextElementSibling!==blocks)nav.insertAdjacentElement('afterend',blocks);
  const notes=[...blocks.querySelectorAll('[data-real-smart-note]')].sort((a,b)=>Number(a.dataset.realSmartNote)-Number(b.dataset.realSmartNote));
  if(notes.length!==9)return false;
  notes.forEach((board,idx)=>applyNoteContent(board,idx));
  blocks.dataset.naya509NavAdjacent='true';
  blocks.dataset.naya509SmartNoteCount='9';
  return true;
 }
 function css(){
  if(document.getElementById('naya509-surgical-smart-note-content-css'))return;
  const s=document.createElement('style');s.id='naya509-surgical-smart-note-content-css';
  s.textContent=`
   .naya509-board{min-height:0!important;height:auto!important;overflow:visible!important}
   .naya509-board .nutshell p,.naya509-board .layerBody{white-space:normal!important;overflow:visible!important;text-overflow:clip!important;word-break:normal!important;overflow-wrap:anywhere!important}
   .naya509-board .layerBody{min-height:0!important;height:auto!important}
  `;
  document.head.appendChild(s);
 }
 function boot(){
  css();
  place();
  if(document.documentElement.dataset[KEY]==='1')return;
  document.documentElement.dataset[KEY]='1';
  const mo=new MutationObserver(()=>{if(document.documentElement.dataset.naya509PlacementBusy==='1')return;document.documentElement.dataset.naya509PlacementBusy='1';try{place()}finally{document.documentElement.dataset.naya509PlacementBusy='0'}});
  mo.observe(document.body,{childList:true,subtree:true});
 }
 window.Naya509NavAdjacentPlacement={boot,place,version:'c4-constitutional-smart-note-content-2'};
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});else boot();
})();
