// Write fixed bytes to a local file (Node write, verified by size+sha) for pre-file browser testing.
const fs = require('fs');
const crypto = require('crypto');
const { transform, fetchBase } = require('./edit-fix6.js');
const out = transform(fetchBase());
const buf = Buffer.from(out, 'latin1');
const p = '/home/hatch/workspace/team-nitro/personal-frame-fix6-20261119/maker/personal-complete-fix6.html';
fs.writeFileSync(p, buf);
const back = fs.readFileSync(p);
console.log(JSON.stringify({ path: p, size: back.length, sha256: crypto.createHash('sha256').update(back).digest('hex'), matches: back.equals(buf) }));
