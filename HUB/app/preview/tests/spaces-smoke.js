/* Smart Spaces smoke suite — stub DOM, no layout. Covers the LIVING ROOM:
 * grid opens spaces, create-a-space, instant chat posting + persistence,
 * mail-to-space loop, add-people from the spine, demo honesty, no dead
 * MAIL button, modal focus traps, reduced-motion + depth CSS. */
'use strict';
const fs = require('fs');
const REPO = process.env.HOME + '/workspace/nayapower-room02';

/* ---------- stub DOM ---------- */
function makeStyle(){
  const s = { _p:{},
    setProperty(k,v){ this._p[k]=String(v); },
    getPropertyValue(k){ return this._p[k]||''; } };
  return s;
}
function makeEl(tag){
  const e = {
    tagName:(tag||'div').toUpperCase(), children:[], attrs:{}, handlers:{},
    className:'', textContent:'', _html:'', style:makeStyle(), value:'', name:'',
    parent:null, disabled:false, type:'', rows:0, placeholder:'',
    scrollTop:0, scrollHeight:0,
    setAttribute(k,v){ this.attrs[k]=String(v); },
    getAttribute(k){ return this.attrs[k]; },
    appendChild(c){ c.parent=this; this.children.push(c); return c; },
    removeChild(c){ const i=this.children.indexOf(c); if(i>=0)this.children.splice(i,1); c.parent=null; return c; },
    addEventListener(t,f){ (this.handlers[t]=this.handlers[t]||[]).push(f); },
    click(){ (this.handlers.click||[]).forEach(f=>f({preventDefault(){},target:this})); },
    input(){ (this.handlers.input||[]).forEach(f=>f({target:this})); },
    keydown(ev){ const e2 = typeof ev==='string' ? {key:ev,shiftKey:false,preventDefault(){}} : ev;
      (this.handlers.keydown||[]).forEach(f=>f(e2)); },
    focus(){ document.activeElement=this; },
    querySelector(sel){
      const all=[]; (function walk(n){ n.children.forEach(c=>{ all.push(c); walk(c); }); })(e);
      if(sel[0]==='.'){ const c=sel.slice(1); return all.find(x=>(x.className||'').split(' ').includes(c))||null; }
      if(sel[0]==='#'){ const id=sel.slice(1); return all.find(x=>x.attrs.id===id)||null; }
      return null;
    },
    querySelectorAll(sel){
      const all=[]; (function walk(n){ n.children.forEach(c=>{ all.push(c); walk(c); }); })(e);
      const parts = sel.split(',').map(s=>s.trim().toLowerCase()).filter(s=>s && s[0]!=='.' && s[0]!=='#' && s[0]!=='[');
      return all.filter(x=>parts.indexOf((x.tagName||'').toLowerCase())>=0);
    },
  };
  Object.defineProperty(e,'innerHTML',{
    get(){ return this._html; },
    set(v){ this._html=String(v); if(v==='') this.children=[]; }
  });
  Object.defineProperty(e,'parentNode',{ get(){ return this.parent; } });
  return e;
}
const document = {
  activeElement:null, body:makeEl('body'),
  createElement(t){ return makeEl(t); },
  addEventListener(){}, getElementById(){ return null; },
};
const store = {};
const localStorage = {
  getItem(k){ return k in store ? store[k] : null; },
  setItem(k,v){ store[k]=String(v); },
  removeItem(k){ delete store[k]; },
};
function el(tag,cls,text){ const e=document.createElement(tag);
  if(cls)e.className=cls; if(text!==undefined&&text!==null)e.textContent=text; return e; }

/* ---------- load ---------- */
const window = {};
global.window = window; global.document = document; global.localStorage = localStorage;
function inner(s){ const a=s.indexOf('(function(){'); const b=s.lastIndexOf('})();'); return s.slice(a+12,b); }
eval(inner(fs.readFileSync(REPO+'/HUB/app/js/people-registry.js','utf8')));
eval(inner(fs.readFileSync(REPO+'/HUB/app/js/rooms/spaces-adapter.js','utf8')));
eval(inner(fs.readFileSync(REPO+'/HUB/app/js/rooms/spaces.js','utf8')));

/* ---------- helpers ---------- */
let pass=0, fail=0;
function ok(c,name){ if(c){pass++;console.log('  PASS',name);} else {fail++;console.log('  FAIL',name);} }
function findAll(root,cls){ const out=[];
  (function walk(n){ n.children.forEach(c=>{ if((c.className||'').split(' ').includes(cls)) out.push(c); walk(c); }); })(root);
  return out; }
function find(root,cls){ return findAll(root,cls)[0]||null; }
function text(n){ return n? String(n.textContent) : ''; }
function btnByLabel(root,cls,label){
  return findAll(root,cls).filter(b=>text(b)===label)[0]||null;
}
function clearStore(){ for(const k in store) delete store[k]; }

/* ---------- fixtures ---------- */
const CONTACTS = [
  {id:'shawn', name:'Shawn Vibert', role:'Human Director', color:'#facc15'},
  {id:'naya1', name:'Naya 1', role:'Senior seat', color:'#a855f7'},
  {id:'naya2', name:'Naya 2', role:'Review lane', color:'#38bdf8'},
  {id:'naya3', name:'Naya 3', role:'Design intelligence', color:'#ec4899'},
  {id:'naya4', name:'Naya 4', role:'Builder seat', color:'#a3e635'},
];
const RAW = [
  {id:'team-naya', name:'Team Naya', color:'#a855f7', members:['shawn','naya1','naya2'],
   desc:'The build team.',
   activity:[
     {ts:'2026-10-01T10:00:00Z', author:'Naya 2', text:'oldest demo note', demo:true},
     {ts:'2026-10-02T10:00:00Z', author:'Shawn', text:'newest demo note', demo:true},
   ]},
  {id:'design-review', name:'Design Review', color:'#ec4899', members:['shawn','naya3'],
   desc:'Taste and QA.', activity:[]},
];
const SPACES = window.SpacesAdapter.parseSpaces(RAW, CONTACTS);

console.log('— grid: spaces open —');
clearStore();
window.NayaPeople.ensureSeeded(CONTACTS);
const stage = window.NayaRooms.smartSpaces(el, {spaces:SPACES, contacts:CONTACTS, me:'naya4'});
ok(findAll(stage,'sp-card').length===2, 'two space cards');
ok(!!find(stage,'sp-create'), 'CREATE A SPACE primary present');
const firstCard = findAll(stage,'sp-card')[0];
firstCard.click();
ok(!!find(stage,'sp-detail'), 'card opens the living room');
ok(text(find(stage,'sp-dname'))==='Team Naya', 'detail shows the space name');
ok(!!find(stage,'sp-topic'), 'topic block present');
ok(text(find(stage,'sp-topic-t'))==='The build team.', 'topic text correct');

console.log('— conversation: unified, oldest-first, demo-labeled —');
const msgs = findAll(stage,'sp-msg');
ok(msgs.length===2, 'two demo messages render');
ok(text(find(msgs[0],'sp-msg-text'))==='oldest demo note', 'oldest first');
ok(text(find(msgs[1],'sp-msg-text'))==='newest demo note', 'newest last');
ok(findAll(stage,'sp-msg').every(m=>!!find(m,'sp-demo-chip')), 'demo messages carry DEMO chips');
ok(findAll(stage,'sp-msg').every(m=>!(m.className||'').split(' ').includes('mine')), 'demo messages not mine-tinted');
ok(text(find(msgs[0],'sp-msg-author'))==='Naya 2', 'demo author shown');

console.log('— instant chat: post persists + renders —');
const ta = find(stage,'sp-ta');
const sendBtn = btnByLabel(stage,'sp-send','SEND');
ok(sendBtn.disabled===true, 'SEND disabled on empty');
ta.value = 'hello from the test';
ta.input();
ok(sendBtn.disabled===false, 'SEND enables with text');
sendBtn.click();
const msgs2 = findAll(stage,'sp-msg');
ok(msgs2.length===3, 'post appears instantly');
ok(text(find(msgs2[2],'sp-msg-text'))==='hello from the test', 'post is newest (chat order)');
ok((msgs2[2].className||'').split(' ').includes('mine'), 'my post is mine-tinted');
ok(!find(msgs2[2],'sp-demo-chip'), 'user content unlabeled');
const saved = JSON.parse(store['naya.smartspaces.posts']||'{}');
ok(saved['team-naya'] && saved['team-naya'].length===1 && saved['team-naya'][0].author==='Naya 4',
   'post persists with author name');
const stageR = window.NayaRooms.smartSpaces(el, {spaces:SPACES, contacts:CONTACTS, me:'naya4'});
findAll(stageR,'sp-card')[0].click();
ok(findAll(stageR,'sp-msg').length===3, 'post survives remount');

console.log('— mail-to-space loop: mailed message appears in the conversation —');
clearStore();
store['naya.smartspaces.posts'] = JSON.stringify({
  'design-review':[{ts:'2026-10-02T09:00:00Z', text:'mailed in from Smart Mail', author:'Naya 2'}]
});
const stageM = window.NayaRooms.smartSpaces(el, {spaces:SPACES, contacts:CONTACTS, me:'naya4'});
findAll(stageM,'sp-card').filter(c=>text(find(c,'sp-card-name'))==='Design Review')[0].click();
const mMsgs = findAll(stageM,'sp-msg');
ok(mMsgs.length===1 && text(find(mMsgs[0],'sp-msg-text'))==='mailed in from Smart Mail',
   'mailed-to-space post appears in the space conversation');
ok((mMsgs[0].className||'').split(' ').includes('mine'), 'mail-written post is mine (not demo)');
ok(text(find(mMsgs[0],'sp-msg-author'))==='Naya 2', 'carries the sender name');

console.log('— MAIL THIS SPACE: no dead button —');
ok(!find(stageM,'sp-mailspace'), 'no MAIL button without the hook');
let composed = null;
const stageC = window.NayaRooms.smartSpaces(el, {spaces:SPACES, contacts:CONTACTS, me:'naya4',
  onCompose:(req)=>{ composed = req; }});
findAll(stageC,'sp-card')[0].click();
const mailBtn = find(stageC,'sp-mailspace');
ok(!!mailBtn, 'MAIL THIS SPACE renders with the hook');
mailBtn.click();
ok(composed && composed.to==='team-naya' && composed.toKind==='space', 'hook called with {to, toKind:space}');

console.log('— add people from the spine —');
clearStore();
const stageP = window.NayaRooms.smartSpaces(el, {spaces:SPACES, contacts:CONTACTS, me:'naya4'});
findAll(stageP,'sp-card').filter(c=>text(find(c,'sp-card-name'))==='Design Review')[0].click();
ok(findAll(stageP,'sp-mchip').length===2, 'two seeded members shown');
btnByLabel(stageP,'sp-addppl','+ ADD PEOPLE').click();
const modal = find(stageP,'sp-modal');
ok(!!modal, 'add-people modal opens');
const rows = findAll(modal,'sp-prow');
ok(rows.length===3, 'lists spine contacts not yet in the space (5-2)');
const addN2 = rows.filter(r=>text(find(r,'sp-pname'))==='Naya 2')[0];
btnByLabel(addN2,'sp-padd','ADD').click();
ok(findAll(stageP,'sp-mchip').length===3, 'member added to the row');
const memSaved = JSON.parse(store['naya.smartspaces.members']||'{}');
ok((memSaved['design-review']||[]).indexOf('naya2')>=0, 'member id persists');
const stageP2 = window.NayaRooms.smartSpaces(el, {spaces:SPACES, contacts:CONTACTS, me:'naya4'});
findAll(stageP2,'sp-card').filter(c=>text(find(c,'sp-card-name'))==='Design Review')[0].click();
ok(findAll(stageP2,'sp-mchip').length===3, 'added member survives remount');

console.log('— create a space —');
clearStore();
const stageX = window.NayaRooms.smartSpaces(el, {spaces:SPACES, contacts:CONTACTS, me:'naya4'});
find(stageX,'sp-create').click();
const cm = find(stageX,'sp-modal');
ok(!!cm, 'create modal opens');
const inputs = findAll(cm,'sp-input');
const createBtn = btnByLabel(cm,'sp-btn','CREATE SPACE');
ok(createBtn.disabled===true, 'CREATE disabled until valid');
inputs[0].value = 'Launch crew'; inputs[0].input();
inputs[1].value = 'everything about the launch'; inputs[1].input();
ok(createBtn.disabled===false, 'CREATE enables with name+topic');
createBtn.click();
ok(findAll(stageX,'sp-card').length===0 || !!find(stageX,'sp-detail'), 'create leaves the modal');
btnByLabel(stageX,'sp-back','\u2190 ALL SPACES').click();
ok(findAll(stageX,'sp-card').length===3, 'new space appears in the grid');
const newCard = findAll(stageX,'sp-card').filter(c=>text(find(c,'sp-card-name'))==='Launch crew')[0];
ok(!!newCard && !find(newCard,'sp-demo-chip'), 'user space has no DEMO chip');
newCard.click();
ok(!!find(stageX,'sp-detail'), 'new space opens');
ok(text(find(stageX,'sp-dname'))==='Launch crew', 'new space named correctly');
const custom = JSON.parse(store['naya.smartspaces.custom']||'[]');
ok(custom.length===1 && custom[0].name==='Launch crew' && !custom[0].demo, 'custom space persists, unlabeled');

console.log('— modal focus trap + escape —');
const stageF = window.NayaRooms.smartSpaces(el, {spaces:SPACES, contacts:CONTACTS, me:'naya4'});
find(stageF,'sp-create').click();
const fmodal = find(stageF,'sp-modal');
const fels = fmodal.querySelectorAll('button, input, textarea, select').filter(x=>!x.disabled);
document.activeElement = fels[fels.length-1];
fmodal.keydown({key:'Tab', shiftKey:false, preventDefault(){}});
ok(document.activeElement===fels[0], 'Tab on last wraps to first');
document.activeElement = fels[0];
fmodal.keydown({key:'Tab', shiftKey:true, preventDefault(){}});
ok(document.activeElement===fels[fels.length-1], 'Shift+Tab on first wraps to last');
stageF.keydown({key:'Escape', preventDefault(){}});
ok(!find(stageF,'sp-modal'), 'Escape closes the modal');

console.log('— onMail hook fires on post —');
clearStore();
let mailed = null;
const stageO = window.NayaRooms.smartSpaces(el, {spaces:SPACES, contacts:CONTACTS, me:'naya4',
  onMail:(s,t)=>{ mailed = {id:s.id, text:t}; }});
findAll(stageO,'sp-card')[0].click();
const ota = find(stageO,'sp-ta');
ota.value = 'hook check'; ota.input();
btnByLabel(stageO,'sp-send','SEND').click();
ok(mailed && mailed.id==='team-naya' && mailed.text==='hook check', 'ctx.onMail(space, text) fires');

console.log('— CSS: living depth —');
const css = fs.readFileSync(REPO+'/HUB/app/css/spaces.css','utf8');
ok(css.indexOf('#0b0b0e')>=0, 'obsidian buttons — never grey');
ok(css.indexOf('radial-gradient(circle at 32% 28%')>=0, 'ball avatars (specular)');
ok(css.indexOf('prefers-reduced-motion')>=0, 'reduced-motion guard');
ok(css.indexOf('.sp-msg.mine')>=0, 'mine-tinted messages styled');
ok(css.indexOf('.sp-overlay')>=0 && css.indexOf('.sp-modal')>=0, 'modals styled');
ok(css.indexOf('font-size:16px')>=0, '16px type floor present');

console.log('\n'+pass+' pass, '+fail+' fail');
process.exit(fail?1:0);
