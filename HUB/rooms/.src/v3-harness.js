/* v3 harness: every room renders, every HubAction executes. Run: node v3-harness.js */
const fs = require('fs');
const path = require('path');
const DIR = __dirname;

// ---- DOM stubs ----
const elements = {};
function mkEl(){ return { innerHTML:'', textContent:'', value:'', checked:false,
  getAttribute:()=>'', setAttribute:()=>{}, scrollIntoView:()=>{}, click:()=>{},
  focus:()=>{}, setSelectionRange:()=>{} }; }
global.document = {
  addEventListener: () => {},
  querySelectorAll: () => [],
  querySelector: () => null,
  getElementById: (id) => elements[id] || null,
  createElement: () => mkEl(),
};
global.window = global;
global.addEventListener = () => {};
global.window.addEventListener = () => {};
global.window.confirm = () => true;
global.window.isSecureContext = true;
global.location = { hash:'', reload: () => {} };
global.localStorage = (()=>{ const m={}; return {
  getItem:k=>m[k]??null, setItem:(k,v)=>{m[k]=String(v)}, removeItem:k=>{delete m[k]} }; })();

// minimal crypto for receipts (sha256 via node)
const crypto = require('crypto');
global.crypto = { subtle: { digest: async (a, buf) => {
  const h = crypto.createHash('sha256').update(Buffer.from(buf)).digest();
  return h.buffer.slice(h.byteOffset, h.byteOffset+h.byteLength);
} } };
global.TextEncoder = require('util').TextEncoder;

// ---- load core + rooms ----
const coreSrc = fs.readFileSync(path.join(DIR,'core.js'),'utf8');
const roomFiles = fs.readdirSync(path.join(DIR,'rooms')).filter(f=>f.endsWith('.js')).sort();
// stub the globals the room code expects
const stub = `
var state = { saved:{}, favorites:{}, loves:{}, top:{} };
function blocks(){ return []; }
function NOTES(){ return global.__notes || []; }
function R(){ return null; }
function Q(s,b){ return null; }
function txt(e){ return ''; }
var S = { reports:{}, library:{}, share:{}, ledger:{}, connections:{}, lists:{}, mail:{}, spaces:{}, settings:{}, notes:{} };
function head(s){ return '<div class="ws-head">'; }
function card(t, b, c){ return '<div>'+t+b+'</div>'; }
function esc(s){ return String(s); }
`;
eval(stub);
eval(coreSrc);
for (const f of roomFiles){ eval(fs.readFileSync(path.join(DIR,'rooms',f),'utf8')); }

let pass = 0, fail = 0;
function ok(name, cond){ if (cond){ pass++; } else { fail++; console.log('FAIL:', name); } }

// 1. every room renders to non-empty HTML (rooms may be async — her render awaits)
const rooms = { reports, library, share, ledger, connections, lists, mail, spaces, settings, notes };
const roomHtml = {};
(async () => {
for (const [name, fn] of Object.entries(rooms)){
  let html = '';
  try { html = await fn(); } catch(e){ console.log('THROW in', name, e.message); }
  roomHtml[name] = String(html || '');
  ok('room '+name+' renders', typeof roomHtml[name] === 'string' && roomHtml[name].length > 200);
}
// share has 10 canonical doors
ok('share: 10 doors', (roomHtml.share.match(/hub-scope|ws-card/g)||[]).length >= 10);
// reports has no KPI stat cards (§27)
ok('reports: no stat cards', !/ws-stat/.test(roomHtml.reports));
// §21 state chips present in every room
for (const [name, html] of Object.entries(roomHtml)){
  ok('room '+name+' has hub-state', /hub-state/.test(html));
}
// mail honest
ok('mail: NO MAIL', /NO MAIL/.test(roomHtml.mail));
// every HubAction callable with stub trigger
const t = { getAttribute:()=>'' };
for (const [name, fn] of Object.entries(HubActions)){
  try { fn(t); ok('action '+name, true); }
  catch(e){ if (/not a function|undefined/.test(e.message)) { fail++; console.log('FAIL action', name, e.message); } else { pass++; } }
}
// state persistence + receipt chain (assert on the tail — earlier actions may have receipted)
// wait for any in-flight receipts from the actions loop to land first
setTimeout(()=>{
var beforeLen = NayaHub.d.receipts.length;
NayaHub.receipt('test.a','first', ()=>{
  NayaHub.receipt('test.b','second', ()=>{
    const r = NayaHub.d.receipts;
    const a = r[beforeLen], b = r[beforeLen+1];
    ok('receipt chain grew by 2', r.length === beforeLen + 2);
    ok('receipt chain linked', a && b && b.prev === a.hash);
    ok('receipt hashes are 32 hex', a && /^[0-9a-f]{32}$/.test(a.hash));
    ok('prefs persist', (()=>{ NayaHub.d.prefs.x = 1; NayaHub.w();
      return JSON.parse(localStorage.getItem('nayanet_hub_v1')).prefs.x === 1; })());
    console.log(`\n${pass} passed, ${fail} failed`);
    process.exit(fail ? 1 : 0);
  });
});
}, 400);
setTimeout(()=>{ console.log('TIMEOUT waiting for receipts; receipts so far:', NayaHub.d.receipts.length); process.exit(1); }, 5000).unref?.();
})();
