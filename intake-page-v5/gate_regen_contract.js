#!/usr/bin/env node
// gate_regen_contract.js — STANDING GATE on intake regen output (Naya Zeta w449).
// The contract blob only exists at user-interaction time, so regen-time cannot
// validate values. This gate validates the EMITTER: the generated page's
// draftContract() object-literal shape must exactly match contract-v1.schema.json.
// Any edit to the emitter that drifts from the spec makes the regen RED.
// Usage: node gate_regen_contract.js <generated.html>
// Exit 0 = emitter matches spec. Exit 2 = INVALID (reasons printed).
// Mirrors validate_contract.js's exit convention (0/2).
const fs = require('fs');
const path = require('path');

function fail(reasons) { reasons.forEach(r => console.log('GATE-FAIL: ' + r)); process.exit(2); }

const htmlFile = process.argv[2];
if (!htmlFile) { console.error('usage: node gate_regen_contract.js <generated.html>'); process.exit(1); }
let html;
try { html = fs.readFileSync(htmlFile, 'utf8'); } catch (e) { console.error('cannot read ' + htmlFile); process.exit(1); }

const schema = JSON.parse(fs.readFileSync(path.join(__dirname, 'contract-v1.schema.json'), 'utf8'));
const REQUIRED = schema.required.slice().sort();

const reasons = [];

// 1. locate the draftContract emitter
const fnIdx = html.indexOf('function draftContract(){');
if (fnIdx === -1) { fail(['draftContract() not found in regen output']); }
const fnSrc = html.slice(fnIdx, fnIdx + 6000); // emitter lives within 6KB of its start

// 2. extract the const jc={...} literal with brace balancing
const litStart = fnSrc.indexOf('const jc={');
if (litStart === -1) { fail(['contract emitter literal const jc={...} not found in draftContract()']); }
let depth = 0, end = -1;
for (let i = litStart + 'const jc='.length; i < fnSrc.length; i++) {
  const ch = fnSrc[i];
  if (ch === '{') depth++;
  else if (ch === '}') { depth--; if (depth === 0) { end = i + 1; break; } }
}
if (end === -1) { fail(['could not balance-brace the jc literal']); }
const lit = fnSrc.slice(litStart + 'const jc='.length, end);

// 3. top-level keys at depth 1, in order
const keys = [];
{
  let d = 0, inStr = false, q = '', esc = false, buf = '';
  for (let i = 0; i < lit.length; i++) {
    const ch = lit[i];
    if (inStr) { if (esc) esc = false; else if (ch === '\\') esc = true; else if (ch === q) inStr = false; continue; }
    if (ch === '"' || ch === "'") { inStr = true; q = ch; continue; }
    if (ch === '{') d++;
    else if (ch === '}') d--;
    else if (ch === ':' && d === 1) { const m = buf.match(/([A-Za-z_$][\w$]*)\s*$/); if (m) keys.push(m[1]); buf = ''; continue; }
    buf += ch;
  }
}
const got = keys.slice().sort();
if (JSON.stringify(got) !== JSON.stringify(REQUIRED)) {
  reasons.push('emitter keys [' + got.join(',') + '] != spec required [' + REQUIRED.join(',') + ']');
}

// 4. pieces mapping must emit exactly model/name/size/qty/note
const piecesMatch = lit.match(/pieces\s*:\s*cart\.map\(i\s*=>\s*\(\{/);
if (!piecesMatch) {
  reasons.push('pieces:cart.map(i=>({model,name,size,qty,note})) mapping not found');
} else {
  // key-anchored check: `k:i.k` must appear as an object-literal binding —
  // substring checks (e.g. 'i.qty' inside 'count:i.qty') are false-positive-proof holes (Zeta w456)
  const pm = fnSrc.slice(fnSrc.indexOf('cart.map(i=>({'), fnSrc.indexOf('cart.map(i=>({') + 300);
  for (const k of ['model', 'name', 'size', 'qty', 'note']) {
    const re = new RegExp('(?:^|[{,])' + k + ':i\\.' + k + '(?=[^\\w]|$)');
    if (!re.test(pm)) reasons.push('pieces mapping missing ' + k + ':i.' + k + ' binding');
  }
}

// 5. version pinned to contract-v1 in the emitter
if (!lit.includes('version:"contract-v1"')) reasons.push('emitter does not pin version:"contract-v1"');

// 6. handle sanitizer: the spec requires ^[a-z0-9]*$, the emitter must keep the guard
if (!fnSrc.includes(".replace(/[^a-z0-9]/g,'')")) reasons.push('handle sanitizer .replace(/[^a-z0-9]/g,\'\') missing — spec handle pattern ^[a-z0-9]*$ unenforced');

if (reasons.length) fail(reasons);
console.log('GATE-PASS: emitter matches contract-v1 (' + keys.length + ' keys, pieces mapping OK, version + handle guard OK)');
