import { spawn } from 'node:child_process';
const CHROME = process.env.HOME + '/.cache/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell';
const URL = 'file://' + process.env.HOME + '/workspace/smart-factory-contract/showcase/index.html';
const PORT = 9335;
const proc = spawn(CHROME, ['--headless','--disable-gpu','--no-sandbox',`--remote-debugging-port=${PORT}`,'--window-size=1280,1000','about:blank'], { stdio:'ignore' });
const sleep = ms => new Promise(r => setTimeout(r, ms));
for (let i=0;i<50;i++){ try{ const r=await fetch(`http://127.0.0.1:${PORT}/json/version`); if(r.ok) break; }catch{} await sleep(200); }
const targets = await (await fetch(`http://127.0.0.1:${PORT}/json`)).json();
const ws = new WebSocket(targets[0].webSocketDebuggerUrl);
await new Promise(res => ws.addEventListener('open', res, { once:true }));
let id=0; const pending=new Map();
ws.addEventListener('message', ev => { const m=JSON.parse(ev.data); if(m.id&&pending.has(m.id)){pending.get(m.id)(m);pending.delete(m.id);} });
const send=(m,p={})=>new Promise(res=>{const i=++id;pending.set(i,res);ws.send(JSON.stringify({id:i,method:m,params:p}));});
async function evaluate(e){ const r=await send('Runtime.evaluate',{expression:e,returnByValue:true}); return r.result?.result?.value; }
await send('Page.enable'); await send('Runtime.enable');
await send('Page.navigate',{url:URL}); await sleep(2000);
console.log(await evaluate(`(() => {
  const bodyBg = getComputedStyle(document.body).backgroundColor + ' / ' + getComputedStyle(document.body).backgroundImage.slice(0,60);
  const htmlBg = getComputedStyle(document.documentElement).backgroundColor;
  // find first element (in paint order candidates) with opaque light background covering width
  const hits = [];
  document.querySelectorAll('*').forEach(el => {
    const cs = getComputedStyle(el); const r = el.getBoundingClientRect();
    const bg = cs.backgroundColor;
    const m = bg.match(/rgba?\\((\\d+), (\\d+), (\\d+)(?:, ([\\d.]+))?\\)/);
    if (m && +m[1] > 200 && +m[2] > 200 && +m[3] > 200 && (m[4] === undefined || +m[4] > 0.5) && r.width > 600 && r.height > 100) {
      hits.push(el.tagName + '.' + el.className.toString().slice(0,50) + ' bg=' + bg + ' pos=' + cs.position + ' rect=' + Math.round(r.top+scrollY) + 'x' + Math.round(r.height));
    }
  });
  return { bodyBg, htmlBg, docHeight: document.documentElement.scrollHeight, hits: hits.slice(0,8) };
})()`));
ws.close(); proc.kill();
