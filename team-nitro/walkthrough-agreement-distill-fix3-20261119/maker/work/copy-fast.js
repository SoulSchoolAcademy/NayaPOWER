#!/usr/bin/env node
// copy-fast.js — tight retry loop for EPERM-flake windows: the window opens for
// seconds at a time, so attempt a single writeFileSync + verify every ~100ms
// instead of sleeping seconds between tries. Usage: node copy-fast.js <src> <dest> [maxAttempts]
// Exits 0 only when dest re-reads byte-identical (size + sha256) to src.
const fs = require('fs');
const crypto = require('crypto');
const [src, dest, maxArg] = process.argv.slice(2);
if (!src || !dest) { console.error('usage: node copy-fast.js <src> <dest> [maxAttempts]'); process.exit(2); }
const max = parseInt(maxArg || '300', 10);
const data = fs.readFileSync(src);
const wantSha = crypto.createHash('sha256').update(data).digest('hex');
const wantBytes = data.length;
function sleep(ms) { return new Promise((r) => setTimeout(r, ms)); }
(async () => {
  for (let a = 1; a <= max; a++) {
    try {
      fs.writeFileSync(dest, data);
      const back = fs.readFileSync(dest);
      if (back.length === wantBytes && crypto.createHash('sha256').update(back).digest('hex') === wantSha) {
        console.log('COPY OK: ' + dest + ' ' + wantBytes + 'B sha ' + wantSha.slice(0, 16) + ' (attempt ' + a + ')');
        process.exit(0);
      }
      console.log('COPY VERIFY FAILED attempt ' + a + ': got ' + back.length + 'B');
    } catch (e) {
      if (a === 1 || a % 50 === 0) console.log('COPY attempt ' + a + ': ' + (e && e.code || e));
    }
    try { fs.unlinkSync(dest); } catch (e2) {}
    await sleep(100);
  }
  console.log('COPY ABORTED after ' + max + ' attempts: ' + dest + ' left absent');
  process.exit(1);
})();
