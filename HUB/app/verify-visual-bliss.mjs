#!/usr/bin/env node
/**
 * NayaNET Visual Bliss / Law Zero guard.
 * This is a static acceptance check for the production-shell foundation.
 * It does not prove visual parity; it prevents obvious readability regressions.
 */
import { readFile } from 'node:fs/promises';

const root = new URL('./', import.meta.url);
const files = [
  'css/tokens.css',
  'css/base.css',
  'css/shell.css',
  'css/components.css',
  'css/views.css',
  'js/views/hub.js',
  'js/views/welcome.js',
];

const text = async (p) => readFile(new URL(p, root), 'utf8');

const tokens = await text('css/tokens.css');
const expectations = [
  ['--fs-body', /--fs-body:\s*17px\b/],
  ['--fs-control', /--fs-control:\s*16px\b/],
  ['--fs-small', /--fs-small:\s*14px\b/],
  ['--fs-meta', /--fs-meta:\s*13\.5px\b/],
  ['--fs-micro', /--fs-micro:\s*13px\b/],
];
const failures = [];
for (const [name, rx] of expectations) if (!rx.test(tokens)) failures.push('missing/readability token: '+name);

const combined = (await Promise.all(files.map(text))).join('\n');
for (const m of combined.matchAll(/font-size:\s*(\d+(?:\.\d+)?)px\b/g)) {
  const px = Number(m[1]);
  if (px < 13) failures.push('microtype remains in app source: '+px+'px');
}

const hub = await text('js/views/hub.js');
if (!hub.includes('PUBLIC BY DECISION')) failures.push('Hub privacy statement missing PUBLIC BY DECISION');

const welcome = await text('js/views/welcome.js');
if (!welcome.includes('PUBLIC BY DECISION')) failures.push('Welcome privacy statement missing PUBLIC BY DECISION');
if (!welcome.includes('Preview the Hub')) failures.push('preview route is not explicitly labeled');

if (failures.length) {
  console.error('LAW ZERO FAIL');
  for (const f of failures) console.error(' - '+f);
  process.exit(1);
}
console.log('LAW ZERO PASS — production-shell typography/privacy guard satisfied');
