// CDP harness for the Reference Exemplars showcase — no playwright dependency.
import { spawn } from 'node:child_process';
import { writeFileSync } from 'node:fs';

const CHROME = process.env.HOME + '/.cache/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell';
const URL = 'file://' + process.env.HOME + '/workspace/smart-factory-contract/showcase/index.html';
const OUT = process.env.HOME + '/workspace/smart-factory-contract/showcase/';
const PORT = 9333;

const proc = spawn(CHROME, ['--headless', '--disable-gpu', '--no-sandbox',
  `--remote-debugging-port=${PORT}`, '--window-size=1280,1700', 'about:blank'],
  { stdio: 'ignore' });

const sleep = ms => new Promise(r => setTimeout(r, ms));
async function waitEndpoint() {
  for (let i = 0; i < 50; i++) {
    try { const r = await fetch(`http://127.0.0.1:${PORT}/json/version`); if (r.ok) return; } catch {}
    await sleep(200);
  }
  throw new Error('chrome did not start');
}
await waitEndpoint();
const targets = await (await fetch(`http://127.0.0.1:${PORT}/json`)).json();
const ws = new WebSocket(targets[0].webSocketDebuggerUrl);
await new Promise(res => ws.addEventListener('open', res, { once: true }));
let id = 0; const pending = new Map();
ws.addEventListener('message', ev => {
  const m = JSON.parse(ev.data);
  if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); }
});
function send(method, params = {}) {
  return new Promise(res => { const i = ++id; pending.set(i, res); ws.send(JSON.stringify({ id: i, method, params })); });
}
async function evaluate(expression) {
  const r = await send('Runtime.evaluate', { expression, returnByValue: true, awaitPromise: true });
  if (r.result?.exceptionDetails) throw new Error(JSON.stringify(r.result.exceptionDetails).slice(0, 400));
  return r.result?.result?.value;
}
async function shot(name, clip) {
  const p = { format: 'png', captureBeyondViewport: true };
  if (clip) p.clip = { ...clip, scale: 1 };
  const r = await send('Page.captureScreenshot', p);
  writeFileSync(OUT + name, Buffer.from(r.result.data, 'base64'));
}

await send('Page.enable'); await send('Runtime.enable');
await send('Emulation.setDeviceMetricsOverride', { width: 1280, height: 1700, deviceScaleFactor: 1, mobile: false });
await send('Page.navigate', { url: URL });
await sleep(2500);

const results = {};
// ---------- WELL ----------
results.well = await evaluate(`(() => {
  const box = document.querySelector('.ref-well-box');
  const input = box.querySelector('input');
  const cs = getComputedStyle(box);
  input.focus();
  const focused = getComputedStyle(box);
  const before = getComputedStyle(box, '::before');
  const ph = getComputedStyle(input, '::placeholder');
  return {
    shadowHasInset: cs.boxShadow.includes('inset'),
    shadowLayers: (cs.boxShadow.match(/inset/g) || []).length,
    borderColor: cs.borderColor,
    focusShadowDeepened: focused.boxShadow !== cs.boxShadow,
    focusRingAnimation: before.animationName,
    focusRingOpacity: before.opacity,
    placeholderColor: ph.color,
    inputColor: getComputedStyle(input).color,
  };
})()`);
// ---------- BUTTON ----------
results.button = await evaluate(`(() => {
  const b = document.querySelector('.living-btn');
  const cs = getComputedStyle(b);
  return {
    shadow: cs.boxShadow,
    activeSinkInCSS: [...document.styleSheets].some(s => { try { return [...s.cssRules].some(r => r.selectorText && r.selectorText.includes('.living-btn:active')); } catch { return false; } }),
  };
})()`);
// press it for real and read the transform mid-press
await evaluate(`document.querySelector('#ex-button').scrollIntoView()`);
await sleep(300);
const btnBox = await evaluate(`(() => { const r = document.querySelector('.living-btn').getBoundingClientRect(); return { x: r.x + r.width/2, y: r.y + r.height/2 }; })()`);
await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: btnBox.x, y: btnBox.y });
await send('Input.dispatchMouseEvent', { type: 'mousePressed', x: btnBox.x, y: btnBox.y, button: 'left', clickCount: 1 });
await sleep(120);
results.button.pressedTransform = await evaluate(`getComputedStyle(document.querySelector('.living-btn')).transform`);
await send('Input.dispatchMouseEvent', { type: 'mouseReleased', x: btnBox.x, y: btnBox.y, button: 'left', clickCount: 1 });
await sleep(300);
results.button.releasedTransform = await evaluate(`getComputedStyle(document.querySelector('.living-btn')).transform`);
// primo counter works?
await evaluate(`document.querySelector('[data-count]').click()`);
results.primoCounter = await evaluate(`document.querySelector('[data-count]').textContent.trim()`);
// ---------- SELECT ----------
await evaluate(`document.querySelector('#ex-select').scrollIntoView()`);
await sleep(300);
results.select = await evaluate(`(() => {
  const btn = document.querySelector('.ref-select-btn');
  const cs = getComputedStyle(btn);
  const out = { closedShadowHasInset: cs.boxShadow.includes('inset') };
  btn.click();
  const panel = document.querySelector('.ref-select-panel');
  out.opened = !panel.hidden;
  out.expanded = btn.getAttribute('aria-expanded');
  out.panelShadow = getComputedStyle(panel).boxShadow.includes('inset');
  out.openAnimation = getComputedStyle(panel).animationName;
  out.chevTransform = getComputedStyle(document.querySelector('.ref-select-chev')).transform;
  return out;
})()`);
await sleep(350);
await shot('shot-select-open-desktop.png');
// keyboard: ArrowDown + Enter should choose "Naya"
await send('Input.dispatchKeyEvent', { type: 'keyDown', key: 'ArrowDown', code: 'ArrowDown', windowsVirtualKeyCode: 40 });
await send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'ArrowDown', code: 'ArrowDown', windowsVirtualKeyCode: 40 });
await send('Input.dispatchKeyEvent', { type: 'keyDown', key: 'Enter', code: 'Enter', windowsVirtualKeyCode: 13 });
await send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'Enter', code: 'Enter', windowsVirtualKeyCode: 13 });
await sleep(200);
results.select.afterKeyboard = await evaluate(`(() => ({
  value: document.querySelector('.ref-select-value').textContent,
  panelHidden: document.querySelector('.ref-select-panel').hidden,
  selected: [...document.querySelectorAll('.ref-select-panel [role="option"]')].map(o => o.getAttribute('aria-selected')),
}))()`);
// ---------- BOARD ----------
results.board = await evaluate(`(() => {
  const p = document.querySelector('.board-h .bh-text p');
  const cs = getComputedStyle(p);
  return { color: cs.color, opacity: cs.opacity };
})()`);
// ---------- HERO ----------
results.hero = await evaluate(`(() => {
  const h = document.querySelector('.ref-hero');
  const cs = getComputedStyle(h);
  const mark = getComputedStyle(document.querySelector('.ref-hero-mark'));
  const title = getComputedStyle(document.querySelector('.ref-hero-title'));
  const before = getComputedStyle(h, '::before');
  return {
    bgHasGlossFall: cs.backgroundImage.includes('1b1b22') || cs.backgroundImage.includes('rgb(27, 27, 34)'),
    bgHasBurst: cs.backgroundImage.includes('conic'),
    borderColor: cs.borderColor,
    shadowHasGlow: cs.boxShadow.length > 40,
    markAnimation: mark.animationName,
    sheenAnimation: before.animationName,
    titleSize: title.fontSize, titleColor: title.color,
  };
})()`);
// ---------- SHOTS ----------
await evaluate(`window.scrollTo(0,0)`);
await sleep(400);
await shot('shot-desktop.png');
await send('Emulation.setDeviceMetricsOverride', { width: 390, height: 844, deviceScaleFactor: 2, mobile: true });
await send('Page.navigate', { url: URL });
await sleep(2200);
await shot('shot-phone.png');
console.log(JSON.stringify(results, null, 1));
ws.close(); proc.kill();
