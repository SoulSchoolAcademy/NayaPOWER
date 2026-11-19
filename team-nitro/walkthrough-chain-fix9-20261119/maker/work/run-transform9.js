#!/usr/bin/env node
/* FIX9 transform runner: run transform-fix9.js, capture its stdout bytes
   in memory, write them to the unfold file path via node (python writes
   are untrusted in this flake window), sha-verify the write. Usage:
   node run-transform9.js <out-path> */
const fs = require('fs');
const crypto = require('crypto');
const { spawnSync } = require('child_process');
const outPath = process.argv[2];
if (!outPath) { console.error('usage: run-transform9.js <out-path>'); process.exit(2); }
const r = spawnSync('node', ['/home/hatch/workspace/team-nitro/walkthrough-chain-fix9-20261119/maker/work/transform-fix9.js'],
  { maxBuffer: 64 * 1024 * 1024 });
process.stderr.write(r.stderr);
if (r.status !== 0) { console.error('transform failed rc=' + r.status); process.exit(1); }
const bytes = r.stdout;
const sha = crypto.createHash('sha256').update(bytes).digest('hex');
console.error('transform bytes: ' + bytes.length + ' sha ' + sha);
// Chunked write: a single large write EPERMs in this flake window while
// small writes land (proven fix-8 pattern: 8KB chunks + fsync + verify,
// retried). Never leave a partial file as the truth — verify by size+sha.
let lastErr = null;
for (let attempt = 0; attempt < 40; attempt++) {
  try {
    const fd = fs.openSync(outPath, 'w');
    try {
      for (let off = 0; off < bytes.length; off += 8192) {
        fs.writeSync(fd, bytes, off, Math.min(8192, bytes.length - off));
      }
      fs.fsyncSync(fd);
    } finally { fs.closeSync(fd); }
    const back = fs.readFileSync(outPath);
    const sha2 = crypto.createHash('sha256').update(back).digest('hex');
    if (back.length === bytes.length && sha2 === sha) {
      console.error('wrote ' + outPath + ' ' + back.length + ' B sha ' + sha2 + ' (attempt ' + (attempt + 1) + ')');
      console.log(sha);
      process.exit(0);
    }
    lastErr = new Error('verify mismatch: ' + back.length + ' B sha ' + sha2);
  } catch (e) { lastErr = e; }
  Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, 2000);
}
console.error('CHUNKED WRITE FAILED: ' + String(lastErr && lastErr.message || lastErr));
process.exit(1);
