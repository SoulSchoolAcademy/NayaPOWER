/* NayaNET 509 C4 — NAV-ADJACENT SMART NOTE CONTENT PLACEMENT
 * SURGICAL EXTENSION ONLY.
 * Preserve the existing Hub, three-feed navigation, existing Smart Note card,
 * typography, controls, spacing, and behavior. Do not redesign the card.
 * The source of truth for Smart Notes is the canonical GitHub file:
 * SMART FEED CONTENT. Missing cards are cloned from the existing card structure.
 */
(()=>{'use strict';
 const KEY='naya509NavAdjacentPlacement';
 const SOURCE='https://raw.githubusercontent.com/SoulSchoolAcademy/NayaPOWER/main/SMART%20FEED%20CONTENT';
 const TONES=['#35e69a','#b8ee57','#f4e45b','#e8c766','#ff9b4a','#ff5e6c','#ffffff','#ff9fda','#ff4fd8'];
 const names=['Nutshell','Human','Child','Grandma','Naya','Machine','Learning','Meaning','Connections','Apply','Benefits'];
 const norm=s=>String(s||'').replace(/\r/g,'').replace(/\s+/g,' ').trim();
 function parseNotes(raw){
  const text=String(raw||'').replace(/\\n/g,'\n').replace(/\u0026/g,'&');
  return text.split(/={20,}\s*/).map(x=>x.trim()).filter(x=>/SMART NOTE \d+/i.test(x)).slice(0,9).map((x,i)=>{
   const title=(x.match(/SMART NOTE \d+\s*\n([^\n]+)/i)||[])[1]||('Smart Note '+String(i+1).padStart(2,'0'));
   const sections={};
   const re=/(?:^|\n)(\d+)\.\s*([^\n]+)\n([\s\S]*?)(?=\n\d+\.\s|$)/g; let m;
   while((m=re.exec(x))) sections[norm(m[2]).toLowerCase()]=norm(m[3]);
   return {id:i+1,title:norm(title),sections};
  });
 }
 function shorten(v,max=760){
  let s=norm(v); if(!s)return '';
  const lines=s.split(/\n+/).map(norm).filter(Boolean);
  s=lines.slice(0,4).join(' ');
  if(s.length>max)s=s.slice(0,max-1).replace(/\s+$/,'')+'…';
  return s;
 }
 function setText(el,value){if(el&&value)el.textContent=value}
 function fill(board,n){
  board.style.setProperty('--tone',TONES[n.id-1],'important');
  board.querySelectorAll('.layer').forEach(x=>x.style.setProperty('--layer',TONES[n.id-1],'important'));
  board.dataset.realSmartNote=String(n.id);
  board.dataset.naya509Tone=String(n.id);
  const h=board.querySelector('.noteTop h3,.noteTop strong,.noteTop b,[data-note-title]');
  if(h)setText(h,n.title);
  const title=board.querySelector('.noteBody h3');
  if(title)setText(title,n.title);
  const map={
   'nutshell':['nutshell p','.nutshell'],
   'human':['.human .layerBody'],
   'child':['.child .layerBody'],
   'grandma':['.grandma .layerBody'],
   'naya':['.naya .layerBody'],
   'machine':['.machine .layerBody'],
   'learning':['.learning .layerBody'],
   'meaning':['.meaning .layerBody'],
   'connections':['.connections .layerBody'],
   'apply':['.apply .layerBody'],
   'benefits':['.benefits .layerBody']
  };
  Object.keys(map).forEach(k=>{const v=n.sections[k]; if(!v)return; const sels=map[k]; for(const sel of sels){const e=board.querySelector(sel);if(e){setText(e,shorten(v));break}}});
  const bodies=[...board.querySelectorAll('.layerBody')];
  const fallback=['human','child','grandma','naya','machine','learning'];
  fallback.forEach((k,i)=>{if(!n.sections[k]||!bodies[i])return;setText(bodies[i],shorten(n.sections[k],620))});
  board.querySelectorAll('.naya509-distill').forEach(e=>e.remove());
  board.style.setProperty('min-height','0','important');
  board.style.setProperty('height','auto','important');
  board.style.setProperty('overflow','visible','important');
  board.dataset.naya509ContentDistilled='true';
 }
 async function sourceNotes(){
  try{const r=await fetch(SOURCE,{cache:'no-store'});if(!r.ok)throw Error('source '+r.status);return parseNotes(await r.text())}catch(e){console.warn('Naya 509 source fetch failed',e);return []}}
 async function place(){
  const nav=document.querySelector('.feedNav'),blocks=document.querySelector('.blocks');
  if(!nav||!blocks)return false;
  if(nav.nextElementSibling!==blocks)nav.insertAdjacentElement('afterend',blocks);
  let notes=[...blocks.querySelectorAll('[data-real-smart-note]')].sort((a,b)=>Number(a.dataset.realSmartNote)-Number(b.dataset.realSmartNote));
  if(!notes.length)return false;
  while(notes.length<9){const clone=notes[notes.length-1].cloneNode(true);clone.removeAttribute('id');blocks.appendChild(clone);notes=[...blocks.querySelectorAll('[data-real-smart-note]')].sort((a,b)=>Number(a.dataset.realSmartNote)-Number(b.dataset.realSmartNote))}
  const data=await sourceNotes();
  if(data.length!==9)return false;
  notes.forEach((board,i)=>fill(board,data[i]));
  blocks.dataset.naya509NavAdjacent='true';blocks.dataset.naya509SmartNoteCount='9';
  return true;
 }
 function css(){if(document.getElementById('naya509-surgical-smart-note-content-css'))return;const s=document.createElement('style');s.id='naya509-surgical-smart-note-content-css';s.textContent=`.naya509-board{min-height:0!important;height:auto!important;overflow:visible!important}.naya509-board .nutshell p,.naya509-board .layerBody{white-space:normal!important;overflow:visible!important;text-overflow:clip!important;word-break:normal!important;overflow-wrap:anywhere!important}.naya509-board .layerBody{min-height:0!important;height:auto!important}`;document.head.appendChild(s)}
 let running=false;
 async function boot(){css();if(running)return;running=true;try{await place()}finally{running=false}if(document.documentElement.dataset[KEY]==='1')return;document.documentElement.dataset[KEY]='1';const mo=new MutationObserver(()=>{if(running)return;place()});mo.observe(document.body,{childList:true,subtree:true})}
 window.Naya509NavAdjacentPlacement={boot,place,version:'c4-canonical-smart-feed-content-nine-card'};
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});else boot();
})();

/* 2026-09-14 LIVE-DOM SNAPSHOT TRIGGER — no runtime behavior change. */
/* PR merge trigger for verified live DOM capture. */
/* Autosave workflow now verifies and saves the exact deployed standalone asset. */
