/* NayaNET 509 AAA — CANONICAL SMART NOTES 01–09 / SURGICAL TOP CLONE
 * Preserve the existing Hub, feed navigation, Smart Note board structure,
 * typography, controls, spacing, and behavior. Do not redesign the board.
 * Add nine new boards at the TOP by cloning the existing board structure.
 * Only the canonical Smart Note text and per-board border/tone change.
 */
(()=>{'use strict';
 const KEY='naya509CanonicalTopNine';
 const SOURCE='https://raw.githubusercontent.com/SoulSchoolAcademy/NayaPOWER/main/NAYANET/509-AAA-SMART-NOTES-01-09-CANONICAL.md';
 const TONES=['#ff4fd8','#9d75ff','#6675ff','#55b9ee','#55e39a','#b8ee57','#f1d75a','#ff9b4a','#ff5e6c'];
 const SECTION_ALIASES={
  nutshell:['nutshell'],
  human:['human note','human'],
  child:['child'],
  grandma:['grandma note','grandma'],
  naya:['naya note','naya'],
  machine:['machine note','machine'],
  learning:['adaptive learning','learning'],
  meaning:["what it means",'meaning'],
  benefits:["what's in it for you?","what's in it for you",'benefits']
 };
 const norm=s=>String(s||'').replace(/\r/g,'').replace(/[ \t]+/g,' ').trim();
 function parseNotes(raw){
  const text=String(raw||'').replace(/^#.*?\n/,'');
  const chunks=text.split(/(?=^## SMART NOTE \d+\s+—\s+)/gim).map(x=>x.trim()).filter(Boolean).slice(0,9);
  return chunks.map((chunk,i)=>{
   const title=(chunk.match(/^## SMART NOTE \d+\s+—\s+([^\n]+)$/im)||[])[1]||('SMART NOTE '+String(i+1).padStart(2,'0'));
   const sections={};
   const re=/^###\s+([^\n]+)\n([\s\S]*?)(?=^###\s+|^##\s+|$)/gim; let m;
   while((m=re.exec(chunk))) sections[norm(m[1]).toLowerCase()]=norm(m[2]);
   return {id:i+1,title:norm(title),sections};
  });
 }
 function getSection(note,key){
  for(const alias of (SECTION_ALIASES[key]||[])){const v=note.sections[alias];if(v)return v}
  return '';
 }
 function setText(el,value){if(el&&value)el.textContent=value}
 function fill(board,n){
  const tone=TONES[n.id-1];
  board.style.setProperty('--tone',tone,'important');
  board.style.setProperty('border-color',tone+'55','important');
  board.querySelectorAll('.layer').forEach(x=>{x.style.setProperty('--layer',tone,'important');x.style.setProperty('border-color',tone+'55','important')});
  board.querySelectorAll('.glyph').forEach(x=>x.style.setProperty('border-color',tone+'78','important'));
  board.dataset.naya509CanonicalTop='true';
  board.dataset.naya509CanonicalNote=String(n.id);
  const h=board.querySelector('.blockTop h3,.noteTop h3,.noteTop strong,.noteTop b,[data-note-title]');
  if(h)setText(h,n.title);
  const bodyTitle=board.querySelector('.noteBody h3');
  if(bodyTitle)setText(bodyTitle,n.title);
  const nutshell=board.querySelector('.nutshell p');
  setText(nutshell,getSection(n,'nutshell'));
  const bodies=[...board.querySelectorAll('.layerBody')];
  const keys=['human','child','grandma','naya','machine','learning','meaning','benefits'];
  const heads=[...board.querySelectorAll('.layerHead b')].map(x=>norm(x.textContent).toLowerCase());
  keys.forEach((key,i)=>{
   const value=getSection(n,key);if(!value)return;
   let target=null;
   const aliases=SECTION_ALIASES[key]||[];
   for(let j=0;j<heads.length;j++){if(aliases.includes(heads[j])){target=bodies[j];break}}
   if(!target)target=bodies[i];
   setText(target,value);
  });
 }
 async function sourceNotes(){
  const r=await fetch(SOURCE,{cache:'no-store'});
  if(!r.ok)throw Error('canonical smart notes source '+r.status);
  const notes=parseNotes(await r.text());
  if(notes.length!==9)throw Error('expected 9 canonical Smart Notes, got '+notes.length);
  for(const n of notes){for(const k of Object.keys(SECTION_ALIASES)){if(!getSection(n,k))throw Error('missing '+k+' in Smart Note '+n.id)}}
  return notes;
 }
 function css(){
  if(document.getElementById('naya509-canonical-top-nine-css'))return;
  const s=document.createElement('style');s.id='naya509-canonical-top-nine-css';
  s.textContent=`[data-naya509-canonical-top="true"] .nutshell p,[data-naya509-canonical-top="true"] .layerBody{white-space:normal!important;overflow:visible!important;text-overflow:clip!important;word-break:normal!important;overflow-wrap:anywhere!important}[data-naya509-canonical-top="true"] .layerBody{min-height:0!important;height:auto!important}`;
  document.head.appendChild(s);
 }
 async function place(){
  const blocks=document.querySelector('.blocks');
  if(!blocks)return false;
  if(blocks.querySelectorAll('[data-naya509-canonical-top="true"]').length===9)return true;
  const template=blocks.querySelector('.block');
  if(!template)return false;
  const notes=await sourceNotes();
  const frag=document.createDocumentFragment();
  notes.forEach(n=>{
   const clone=template.cloneNode(true);
   clone.removeAttribute('id');
   clone.querySelectorAll('[id]').forEach(el=>el.removeAttribute('id'));
   fill(clone,n);
   frag.appendChild(clone);
  });
  blocks.insertBefore(frag,blocks.firstElementChild||null);
  blocks.dataset.naya509CanonicalTopCount='9';
  return true;
 }
 async function boot(){
  css();
  if(document.documentElement.dataset[KEY]==='1')return;
  document.documentElement.dataset[KEY]='1';
  try{await place()}catch(e){console.error('Naya 509 canonical Smart Notes failed',e)}
 }
 window.Naya509NavAdjacentPlacement={boot,place,version:'509-aaa-canonical-smart-notes-top-nine-v1'};
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});else boot();
})();
