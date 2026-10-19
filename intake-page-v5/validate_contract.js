#!/usr/bin/env node
// validate_contract.js — machine validator for draftContract() contract-v1 blobs.
// Reads a JSON file (argv[2]), validates against contract-v1.schema.json (same dir).
// Exit 0 = valid. Exit 2 = invalid, reasons printed. Exit 1 = unreadable input.
// Naya Zeta w447, gr-w444 gapclose — spec-first; nothing validated this blob before.
const fs = require('fs');
const path = require('path');

function fail(msg) { console.log('INVALID: ' + msg); process.exit(2); }

const file = process.argv[2];
if (!file) { console.error('usage: node validate_contract.js <contract.json>'); process.exit(1); }
let raw;
try { raw = fs.readFileSync(file, 'utf8'); } catch (e) { console.error('cannot read ' + file); process.exit(1); }
let c;
try { c = JSON.parse(raw); } catch (e) { fail('not valid JSON: ' + e.message); }

const REQUIRED = ['version','handle','idea','vision','do','behave','template','functions','pieces','rules'];
if (typeof c !== 'object' || c === null || Array.isArray(c)) fail('top level must be an object');
for (const k of REQUIRED) if (!(k in c)) fail('missing required key: ' + k);
for (const k of Object.keys(c)) if (!REQUIRED.includes(k)) fail('unexpected key: ' + k);
if (c.version !== 'contract-v1') fail('version must be "contract-v1", got ' + JSON.stringify(c.version));
if (typeof c.handle !== 'string' || !/^[a-z0-9]*$/.test(c.handle)) fail('handle must be lowercase-alnum string');
for (const k of ['idea','vision','do','behave','template','rules'])
  if (typeof c[k] !== 'string') fail(k + ' must be a string');
if (typeof c.functions !== 'object' || c.functions === null || Array.isArray(c.functions)) fail('functions must be an object');
for (const [k, v] of Object.entries(c.functions))
  if (typeof v !== 'boolean') fail('functions[' + k + '] must be boolean');
if (!Array.isArray(c.pieces)) fail('pieces must be an array');
c.pieces.forEach((p, i) => {
  if (typeof p !== 'object' || p === null) fail('pieces[' + i + '] must be an object');
  for (const k of ['model','name','size','qty','note']) if (!(k in p)) fail('pieces[' + i + '] missing ' + k);
  if (typeof p.model !== 'string' || typeof p.name !== 'string' || typeof p.size !== 'string' || typeof p.note !== 'string')
    fail('pieces[' + i + '] model/name/size/note must be strings');
  if (!Number.isInteger(p.qty) || p.qty < 0) fail('pieces[' + i + '] qty must be a non-negative integer');
});
console.log('VALID: contract-v1, ' + c.pieces.length + ' pieces, ' + Object.keys(c.functions).length + ' function states');
