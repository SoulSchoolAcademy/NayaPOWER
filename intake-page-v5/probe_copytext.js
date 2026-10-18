// w453 Zeta probe (v2): copyText from the generated HTML, executed at module scope.
const fs = require('fs');
const html = fs.readFileSync(process.argv[2], 'utf8');
const srcLine = html.split('\n')[1767];
if (!srcLine.includes("function copyText(t,done)")) { console.error('EXTRACT-FAIL'); process.exit(2); }
const state = { calls: [] };
function resetShims({ secure, clipboard, execCommand }) {
  state.calls = [];
  const ta = { value: '', style: {}, focus() {}, select() {}, remove() { state.calls.push('removed'); } };
  global.document = {
    createElement(tag) { state.calls.push('createElement:' + tag); return ta; },
    body: { appendChild() { state.calls.push('appended'); } },
    execCommand(cmd) { state.calls.push('execCommand:' + cmd); return execCommand(cmd); },
  };
  global.window = { isSecureContext: secure };
  navigator = clipboard
    ? { clipboard: { writeText(t) { state.calls.push('writeText:' + t.length + 'B'); return Promise.resolve(); } } }
    : {};
}
let navigator = {};
eval(srcLine); // defines module-scope copyText
async function run() {
  const out = {};
  resetShims({ secure: false, clipboard: false, execCommand: () => true });
  out.caseA_nonsecure_execCommand_true = await new Promise(res => copyText('hello', v => res({ done: v, calls: state.calls })));
  resetShims({ secure: false, clipboard: false, execCommand: () => { throw new Error('denied'); } });
  out.caseB_nonsecure_execCommand_throws = await new Promise(res => copyText('hello', v => res({ done: v, calls: state.calls })));
  resetShims({ secure: true, clipboard: true, execCommand: () => { throw new Error('must-not-run'); } });
  out.caseC_secure_clipboard_api = await new Promise(res => copyText('hello', v => res({ done: v, calls: state.calls })));
  resetShims({ secure: false, clipboard: true, execCommand: () => true });
  out.caseD_nonsecure_clipboard_present = await new Promise(res => copyText('hello', v => res({ done: v, calls: state.calls })));
  console.log(JSON.stringify(out, null, 1));
}
run().catch(e => { console.error('PROBE-ERROR', e.message); process.exit(2); });
