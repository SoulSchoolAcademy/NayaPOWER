#!/usr/bin/env node
// copy-chunked.js — EPERM-flake-safe file copy: chunked 8KB writes + hard
// verification (size + sha256). Usage: node copy-chunked.js <src> <dest> [retries]
// Exits 0 only when the dest re-reads byte-identical to the source.
// A failed attempt unlinks the partial dest; nothing is left half-written.
const fs = require('fs');
const crypto = require('crypto');
const [src, dest, retriesArg] = process.argv.slice(2);
if (!src || !dest) { console.error('usage: node copy-chunked.js <src> <dest> [retries]'); process.exit(2); }
const retries = parseInt(retriesArg || '5', 10);
const data = fs.readFileSync(src);
const wantSha = crypto.createHash('sha256').update(data).digest('hex');
const wantBytes = data.length;
const CHUNK = 8192;
function sleep(ms) { return new Promise((r) => setTimeout(r, ms)); }
(async () => {
  for (let attempt = 1; attempt <= retries; attempt++) {
    try {
      const fd = fs.openSync(dest, 'w');
      try {
        for (let off = 0; off < data.length; off += CHUNK) {
          const len = Math.min(CHUNK, data.length - off);
          fs.writeSync(fd, data, off, len);
        }
        fs.fsyncSync(fd);
      } finally { fs.closeSync(fd); }
      const back = fs.readFileSync(dest);
      const gotSha = crypto.createHash('sha256').update(back).digest('hex');
      if (back.length === wantBytes && gotSha === wantSha) {
        console.log('COPY OK: ' + dest + ' ' + wantBytes + 'B sha ' + wantSha.slice(0, 16) + ' (attempt ' + attempt + ')');
        process.exit(0);
      }
      console.log('COPY VERIFY FAILED attempt ' + attempt + ': got ' + back.length + 'B sha ' + gotSha.slice(0, 16) + ', want ' + wantBytes + 'B sha ' + wantSha.slice(0, 16));
    } catch (e) {
      console.log('COPY FAILED attempt ' + attempt + ': ' + (e && e.message || e));
    }
    try { fs.unlinkSync(dest); } catch (e2) {}
    if (attempt < retries) await sleep(2000 * attempt);
  }
  console.log('COPY ABORTED after ' + retries + ' attempts: ' + dest + ' left absent');
  process.exit(1);
})();
