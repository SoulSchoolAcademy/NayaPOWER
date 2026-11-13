#!/usr/bin/env node
/* Parse-check every inline script block of built HTML from stdin.
   Usage: build-third-surface.py ... 2>/dev/null | node check-blocks.js */
const fs = require('fs'), vm = require('vm');
const html = fs.readFileSync(0, 'utf-8');
const re = /<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/g;
let m, i = 0, bad = 0;
while ((m = re.exec(html)) !== null) {
  i++;
  const code = m[1];
  if (!code.trim()) continue;
  try { new vm.Script(code, { filename: 'block' + i }); }
  catch (e) {
    bad++;
    const lines = code.split('\n');
    const lm = (e.stack || '').match(/block\d+:(\d+)/);
    const ln = lm ? parseInt(lm[1], 10) : null;
    console.log('BLOCK ' + i + ' FAIL: ' + e.message);
    if (ln) for (let k = Math.max(1, ln - 2); k <= Math.min(lines.length, ln + 1); k++)
      console.log('  ' + k + ': ' + lines[k - 1].slice(0, 220));
  }
}
console.log('script blocks: ' + i + ', parse failures: ' + bad);
console.log('literal tr(" leaks: ' + (html.match(/tr\("/g) || []).length);
console.log('mwTr guard uses: ' + (html.match(/window\.mwTr\?/g) || []).length);
console.log('mwLocale uses: ' + (html.match(/window\.mwLocale\?/g) || []).length);
