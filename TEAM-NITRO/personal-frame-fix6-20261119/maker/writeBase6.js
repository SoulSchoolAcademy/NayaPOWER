const fs = require('fs');
const crypto = require('crypto');
const { fetchBase } = require('./fetchBase6.js');
const base = fetchBase();
const buf = Buffer.from(base, 'latin1');
const p = '/home/hatch/workspace/team-nitro/personal-frame-fix6-20261119/maker/personal-complete-base5.html';
fs.writeFileSync(p, buf);
const back = fs.readFileSync(p);
console.log(JSON.stringify({ path: p, size: back.length, sha256: crypto.createHash('sha256').update(back).digest('hex'), matches: back.equals(buf) }));
