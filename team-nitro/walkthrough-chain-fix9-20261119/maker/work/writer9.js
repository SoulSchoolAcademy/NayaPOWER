#!/usr/bin/env node
/* FIX9 stdin writer (proven fix-8 shape): read the transform bytes from
   stdin, chunked-write them to the out path, sha-verify. This process
   never spawns children and never reads the worker file — the transform
   runs as a separate process upstream of the pipe, so no taint carries
   over. Usage: node transform-fix9.js 2>/dev/null | node writer9.js <out-path> */
const fs = require('fs');
const crypto = require('crypto');
const outPath = process.argv[2];
const maxAttempts = parseInt(process.argv[3] || '40', 10);
if (!outPath) { console.error('usage: writer9.js <out-path> [max-attempts]'); process.exit(2); }
const chunks = [];
process.stdin.on('data', c => chunks.push(c));
process.stdin.on('end', () => {
  const bytes = Buffer.concat(chunks);
  const sha = crypto.createHash('sha256').update(bytes).digest('hex');
  console.error('writer got ' + bytes.length + ' B sha ' + sha);
  // NEVER truncate the live file first: write a temp in the same directory,
  // verify size+sha, and only then replace. A failed write leaves a
  // 0-byte TEMP, never a 0-byte live file (the fix-8 unfold was truncated
  // exactly this way once — recovered from its filed blob).
  const tmpPath = outPath + '.tmp9';
  let lastErr = null;
  for (let attempt = 0; attempt < maxAttempts; attempt++) {
    try {
      const fd = fs.openSync(tmpPath, 'w');
      try {
        for (let off = 0; off < bytes.length; off += 8192) {
          fs.writeSync(fd, bytes, off, Math.min(8192, bytes.length - off));
        }
        fs.fsyncSync(fd);
      } finally { fs.closeSync(fd); }
      const back = fs.readFileSync(tmpPath);
      const sha2 = crypto.createHash('sha256').update(back).digest('hex');
      if (back.length === bytes.length && sha2 === sha) {
        fs.renameSync(tmpPath, outPath);
        const back2 = fs.readFileSync(outPath);
        const sha3 = crypto.createHash('sha256').update(back2).digest('hex');
        if (back2.length !== bytes.length || sha3 !== sha) throw new Error('verify after replace failed');
        console.error('wrote ' + outPath + ' ' + back.length + ' B sha ' + sha2 + ' (attempt ' + (attempt + 1) + ')');
        console.log(sha);
        process.exit(0);
      }
      lastErr = new Error('verify mismatch: ' + back.length + ' B sha ' + sha2);
    } catch (e) { lastErr = e; }
    Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, 2000);
  }
  console.error('WRITER FAILED: ' + String(lastErr && lastErr.message || lastErr));
  process.exit(1);
});
