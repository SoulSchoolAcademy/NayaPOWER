#!/usr/bin/env node
// Icon Library DATA build — Node renderer (2026-11-19).
// Node writes files (proven working); Python cannot write in this VM, so
// Python only supplied the 26x2 letter masks (letter-masks.json, rendered
// with PIL + Inter wght 900). This script does the gradient bases, the
// compositing, PNG encode/decode, logos, icons.json and the contact sheet.
// Gradient math mirrors render-orbs.py build_base exactly (float64, truncate).
const fs = require('fs');
const path = require('path');
const zlib = require('zlib');
const crypto = require('crypto');

const LIB = '/home/hatch/workspace/icon-library';
const GEM_NUM = {A:1,B:2,C:3,D:4,E:5,F:6,G:7,H:6,I:5,J:4,K:3,L:2,M:1,N:1,O:2,P:3,Q:4,R:5,S:6,T:7,U:6,V:5,W:4,X:3,Y:2,Z:1};
const GEM_COL = {1:'#c62828',2:'#c2410c',3:'#d4a017',4:'#07925f',5:'#0f52ba',6:'#3f51b5',7:'#8e24aa'};
const NAMES = {1:'red',2:'orange',3:'gold',4:'emerald',5:'sapphire',6:'indigo',7:'royal-purple'};
const DARK = [16, 16, 20];
const LETTERS = Object.keys(GEM_NUM);
const sleepSync = (ms) => Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, ms);

// ---------- CRC32 / PNG ----------
const CRC_TABLE = (() => {
  const t = new Int32Array(256);
  for (let n = 0; n < 256; n++) {
    let c = n;
    for (let k = 0; k < 8; k++) c = (c & 1) ? (0xEDB88320 ^ (c >>> 1)) : (c >>> 1);
    t[n] = c;
  }
  return t;
})();
function crc32(buf) {
  let c = 0xFFFFFFFF;
  for (let i = 0; i < buf.length; i++) c = CRC_TABLE[(c ^ buf[i]) & 0xFF] ^ (c >>> 8);
  return (c ^ 0xFFFFFFFF) >>> 0;
}
function chunk(type, data) {
  const len = Buffer.alloc(4); len.writeUInt32BE(data.length);
  const td = Buffer.concat([Buffer.from(type, 'ascii'), data]);
  const crc = Buffer.alloc(4); crc.writeUInt32BE(crc32(td));
  return Buffer.concat([len, td, crc]);
}
function pngEncode(w, h, rgba) { // rgba: Uint8Array w*h*4
  const raw = Buffer.alloc(h * (1 + w * 4));
  for (let y = 0; y < h; y++) {
    raw[y * (1 + w * 4)] = 0;
    raw.set(rgba.subarray(y * w * 4, (y + 1) * w * 4), y * (1 + w * 4) + 1);
  }
  const ihdr = Buffer.alloc(13);
  ihdr.writeUInt32BE(w, 0); ihdr.writeUInt32BE(h, 4);
  ihdr[8] = 8; ihdr[9] = 6; ihdr[10] = 0; ihdr[11] = 0; ihdr[12] = 0;
  return Buffer.concat([
    Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]),
    chunk('IHDR', ihdr),
    chunk('IDAT', zlib.deflateSync(raw, { level: 9 })),
    chunk('IEND', Buffer.alloc(0)),
  ]);
}
function paeth(a, b, c) {
  const p = a + b - c, pa = Math.abs(p - a), pb = Math.abs(p - b), pc = Math.abs(p - c);
  return (pa <= pb && pa <= pc) ? a : (pb <= pc ? b : c);
}
function pngDecode(buf) { // returns {w,h,rgba:Uint8Array} for 8-bit non-interlaced RGBA/RGB
  let pos = 8, w, h, bitDepth, colorType, idat = [];
  while (pos < buf.length) {
    const len = buf.readUInt32BE(pos);
    const type = buf.toString('ascii', pos + 4, pos + 8);
    const data = buf.subarray(pos + 8, pos + 8 + len);
    if (type === 'IHDR') { w = data.readUInt32BE(0); h = data.readUInt32BE(4); bitDepth = data[8]; colorType = data[9]; }
    else if (type === 'IDAT') idat.push(data);
    else if (type === 'IEND') break;
    pos += 12 + len;
  }
  if (bitDepth !== 8 || (colorType !== 6 && colorType !== 2)) throw new Error(`unsupported PNG ${bitDepth}/${colorType}`);
  const ch = colorType === 6 ? 4 : 3;
  const raw = zlib.inflateSync(Buffer.concat(idat));
  const stride = w * ch, rgba = new Uint8Array(w * h * 4);
  let p = 0;
  for (let y = 0; y < h; y++) {
    const f = raw[p++];
    for (let x = 0; x < stride; x++) {
      const v = raw[p++];
      const left = x >= ch ? rgba[y * w * 4 + x - ch] : 0;
      const up = y > 0 ? rgba[(y - 1) * w * 4 + x] : 0;
      const upLeft = (x >= ch && y > 0) ? rgba[(y - 1) * w * 4 + x - ch] : 0;
      let r;
      if (f === 0) r = v;
      else if (f === 1) r = (v + left) & 0xFF;
      else if (f === 2) r = (v + up) & 0xFF;
      else if (f === 3) r = (v + ((left + up) >> 1)) & 0xFF;
      else if (f === 4) r = (v + paeth(left, up, upLeft)) & 0xFF;
      else throw new Error('bad filter ' + f);
      const px = y * w + (x / ch | 0), c = x % ch;
      rgba[px * 4 + c] = r;
      if (ch === 3 && c === 2) rgba[px * 4 + 3] = 255;
    }
  }
  return { w, h, rgba };
}

// ---------- helpers ----------
function hx(h) { return [parseInt(h.slice(1, 3), 16), parseInt(h.slice(3, 5), 16), parseInt(h.slice(5, 7), 16)]; }
function sha(buf) { return crypto.createHash('sha256').update(buf).digest('hex'); }
function writeVerified(rel, buf) {
  const dest = path.join(LIB, rel);
  fs.mkdirSync(path.dirname(dest), { recursive: true });
  for (let i = 0; i < 30; i++) {
    try {
      fs.writeFileSync(dest, buf);
      const back = fs.readFileSync(dest);
      if (back.length === buf.length && sha(back) === sha(buf)) return back.length;
    } catch (e) { /* retry */ }
    sleepSync(1000);
  }
  throw new Error('could not write ' + rel);
}

// ---------- gradient base (mirrors render-orbs.py build_base) ----------
function buildBase(C, S) {
  const cx = S / 2, cy = S / 2, D = 0.88 * S, R = D / 2, u = D / 58, margin = (S - D) / 2;
  const N = S * S;
  const rgb = new Float64Array(N * 3), al = new Float64Array(N);
  const Rfar = D * Math.hypot(0.68, 0.72), hlCx = cx - 0.18 * D, hlCy = cy - 0.22 * D;
  const off = margin * 0.35, gBlur = margin * 0.6, sBlur = margin * 0.5;
  const rim = [0.8 * C[0] + 0.2 * 255, 0.8 * C[1] + 0.2 * 255, 0.8 * C[2] + 0.2 * 255];
  for (let y = 0; y < S; y++) {
    const dy = y - cy;
    for (let x = 0; x < S; x++) {
      const dx = x - cx, idx = y * S + x;
      const rPx = Math.hypot(dx, dy), r = rPx / R;
      const t = r < 0 ? 0 : (r > 1 ? 1 : r);
      const p = t <= 0.78 ? (55 - 27 * (t / 0.78)) / 100 : 0.28;
      let r0 = C[0] * p + DARK[0] * (1 - p);
      let g0 = C[1] * p + DARK[1] * (1 - p);
      let b0 = C[2] * p + DARK[2] * (1 - p);
      const dHl = Math.hypot(x - hlCx, y - hlCy);
      const hlA = 0.35 * Math.max(0, 1 - dHl / (0.42 * Rfar));
      r0 = r0 * (1 - hlA) + 255 * hlA; g0 = g0 * (1 - hlA) + 255 * hlA; b0 = b0 * (1 - hlA) + 255 * hlA;
      const dTop = y - (cy - R);
      const topA = dTop >= 0 ? 0.25 * Math.exp(-(((dTop - 2 * u) / (3 * u)) ** 2)) : 0;
      r0 = r0 * (1 - topA) + 255 * topA; g0 = g0 * (1 - topA) + 255 * topA; b0 = b0 * (1 - topA) + 255 * topA;
      const dBot = (cy + R) - y;
      const botA = dBot >= 0 ? 0.45 * Math.exp(-(((dBot - 6 * u) / (12 * u)) ** 2)) : 0;
      r0 *= (1 - botA); g0 *= (1 - botA); b0 *= (1 - botA);
      if (rPx >= R - 2 * u && rPx <= R) { r0 = rim[0]; g0 = rim[1]; b0 = rim[2]; }
      const edge = Math.max(0, Math.min(1, (R - rPx) / 1.5 + 0.5));
      const glowA = rPx > R ? 0.55 * Math.exp(-(((rPx - R) / gBlur) ** 2)) : 0;
      const dSh = Math.hypot(dx, dy - off);
      const shA = 0.55 * (dSh <= R ? 1 : Math.exp(-(((dSh - R) / sBlur) ** 2)));
      // composite: shadow (black), glow (colour), disc — "over", starting transparent
      let or_ = 0, og = 0, ob = 0, oa = 0;
      // shadow
      or_ = 0 * shA + or_ * (1 - shA); og = 0 * shA + og * (1 - shA); ob = 0 * shA + ob * (1 - shA); oa = shA + oa * (1 - shA);
      // glow
      or_ = C[0] * glowA + or_ * (1 - glowA); og = C[1] * glowA + og * (1 - glowA); ob = C[2] * glowA + ob * (1 - glowA); oa = glowA + oa * (1 - glowA);
      // disc
      or_ = r0 * edge + or_ * (1 - edge); og = g0 * edge + og * (1 - edge); ob = b0 * edge + ob * (1 - edge); oa = edge + oa * (1 - edge);
      rgb[idx * 3] = or_; rgb[idx * 3 + 1] = og; rgb[idx * 3 + 2] = ob; al[idx] = oa;
    }
  }
  return { rgb, al };
}

function main() {
  const masks = JSON.parse(fs.readFileSync(path.join(LIB, 'letter-masks.json'), 'utf8'));
  const fontSource = masks.font_source;
  console.log('font:', fontSource);
  // decode masks + verify alpha sums
  const decoded = {};
  for (const S of ['512', '192']) {
    decoded[S] = {};
    for (const L of LETTERS) {
      const m = masks.sizes[S][L];
      const png = Buffer.from(m.png_b64, 'base64');
      const dec = pngDecode(png);
      if (dec.w !== m.w || dec.h !== m.h) throw new Error(`mask size mismatch ${L} ${S}`);
      let asum = 0;
      for (let i = 3; i < dec.rgba.length; i += 4) asum += dec.rgba[i];
      if (asum !== m.alpha_sum) throw new Error(`mask alpha_sum mismatch ${L} ${S}: ${asum} vs ${m.alpha_sum}`);
      decoded[S][L] = { x: m.x, y: m.y, w: m.w, h: m.h, rgba: dec.rgba };
    }
  }
  console.log('masks decoded + alpha sums verified (52/52)');

  const recs = {};
  const keep512 = {};
  for (const S of [512, 192]) {
    for (let num = 1; num <= 7; num++) {
      const C = hx(GEM_COL[num]);
      const base = buildBase(C, S);
      for (const L of LETTERS) {
        const m = decoded[String(S)][L];
        // copy base floats, composite letter mask, truncate to uint8
        const out = new Uint8Array(S * S * 4);
        for (let i = 0; i < S * S; i++) {
          out[i * 4] = base.rgb[i * 3];
          out[i * 4 + 1] = base.rgb[i * 3 + 1];
          out[i * 4 + 2] = base.rgb[i * 3 + 2];
          out[i * 4 + 3] = base.al[i] * 255;
        }
        for (let my = 0; my < m.h; my++) {
          for (let mx = 0; mx < m.w; mx++) {
            const si = (my * m.w + mx) * 4;
            const sa = m.rgba[si + 3] / 255;
            if (sa === 0) continue;
            const dx = m.x + mx, dy = m.y + my, di = (dy * S + dx) * 4;
            out[di] = m.rgba[si] * sa + out[di] * (1 - sa);
            out[di + 1] = m.rgba[si + 1] * sa + out[di + 1] * (1 - sa);
            out[di + 2] = m.rgba[si + 2] * sa + out[di + 2] * (1 - sa);
            out[di + 3] = m.rgba[si + 3] * sa + out[di + 3] * (1 - sa);
          }
        }
        const buf = pngEncode(S, S, out);
        const rel = `orbs/${S}/${L}-${num}-${NAMES[num]}.png`;
        const n = writeVerified(rel, buf);
        const rec = recs[`${L}-${num}`] || (recs[`${L}-${num}`] = {});
        rec[`bytes${S}`] = n; rec[`sha${S}`] = sha(buf);
        if (S === 512 && (GEM_NUM[L] === num || (L === 'A' && num === 2) || (L === 'M' && num === 7) || (L === 'Z' && num === 3) || (L === 'T' && num === 1))) {
          keep512[`${L}-${num}`] = out;
        }
      }
      console.log(`  size ${S} colour ${num} ${NAMES[num]} done`);
    }
  }
  console.log('orbs written: 364');

  // logos (byte-identical copies)
  const logos = [];
  const trio = {
    'naya-icon-512.png': ['bb5728c0d075893ac6038c3a4081f20f7d878408bf3c5e354e7e6558f7213d58', 512],
    'naya-icon-192.png': ['b84ac3a14d5c7babbfac8d9a3414cbf80ddc5f4f4774f2e37c3395e1297f1308', 192],
    'apple-touch-icon.png': ['cb00859d0d1f167ec9cf460a30cb8b1a1d64df2006b2a556833fe7100db3cf5e', 180],
  };
  for (const [fname, [expSha, sizePx]] of Object.entries(trio)) {
    const src = `/home/hatch/workspace/user/files/icons/${fname}`;
    const data = fs.readFileSync(src);
    if (sha(data) !== expSha) throw new Error(`source logo hash mismatch ${fname}`);
    writeVerified(`logo/${fname}`, data);
    logos.push({ file: fname, size_px: sizePx, bytes: data.length, sha256: sha(data), source: `~/workspace/user/files/icons/${fname}` });
    console.log(`logo copied: ${fname} ${data.length} B sha256 ok`);
  }

  writeVerified('.font_source.txt', Buffer.from(fontSource + '\n'));

  const orbs = [];
  for (const L of LETTERS) for (let num = 1; num <= 7; num++) {
    const e = recs[`${L}-${num}`];
    orbs.push({
      id: `orb-${L}-${num}`, initial: L, gematria_number: num,
      colour_name: NAMES[num], colour_hex: GEM_COL[num],
      canonical: GEM_NUM[L] === num,
      file_512: `orbs/512/${L}-${num}-${NAMES[num]}.png`,
      file_192: `orbs/192/${L}-${num}-${NAMES[num]}.png`,
      bytes_512: e.bytes512, sha256_512: e.sha512,
      bytes_192: e.bytes192, sha256_192: e.sha192,
    });
  }
  const doc = {
    library: 'Naya Icon Library', version: '1.0.0', date: '2026-11-19',
    gematria_number: GEM_NUM, gematria_colour: GEM_COL, colour_names: NAMES,
    orb_recipe: {
      source: '.cx-ava from Personal mirror (branch personal/mirror-hub-20261119, blob 010dd56c) and Hub (blob 7a15413b), verbatim',
      shape: 'circle',
      letter: { colour: '#ffffff', weight: 900, size: '22px on a 58px orb (0.379 of diameter)',
        text_shadow: '0 1px 3px rgba(0,0,0,.6)',
        font: 'inherited sans (Inter / system sans) — NOT Marcellus (no 900 weight; certificate script face)' },
      body: 'radial-gradient(circle at 32% 28%, rgba(255,255,255,.35) 0%, rgba(255,255,255,0) 42%) over radial-gradient(circle at 50% 50%, color-mix(in srgb, COLOUR 55%, #101014) 0%, color-mix(in srgb, COLOUR 28%, #060607) 78%)',
      rim: 'border 2px solid color-mix(in srgb, COLOUR 80%, white) (2px on 58px orb; scales with diameter)',
      shadows: 'box-shadow 0 0 24px -4px COLOUR, inset 0 2px 3px rgba(255,255,255,.25), inset 0 -6px 12px rgba(0,0,0,.45), 0 8px 20px rgba(0,0,0,.55); all lengths scale with orb diameter',
      animation_note: 'The live page has a spinning sheen ring (osOrbFlow, 7s). It is ANIMATION, not part of the static icon file, and is not drawn.'
    },
    notes: [
      'TAB vs ORB colour for 5: the Hub TAB-colour table uses bright cyan #29b6f6 for 5 (verified from the fix-9 digit-5 tile). That is the TAB colour, NOT the orb colour. Orbs use the deep table: 5 = #0f52ba sapphire. #29b6f6 appears in NO orb file.',
      'SQUARE-FILE ADAPTATION (coordinator\'s call): on the page the glow/drop-shadow extend ~0.4x the disc diameter beyond the disc. A square icon file cannot hold that proportionally, so disc diameter = 88% of canvas (450px in 512, 169px in 192), centred; border, highlight, body gradient, inset light/shade and letter at EXACT CSS proportions relative to the disc; outer glow and drop shadow scaled to fit the remaining margin (glow blur ~ margin x 0.6 fading to ~0 at canvas edge; drop-shadow offset ~ margin x 0.35, blur ~ margin x 0.5). Disc, rim, highlight, letter and colours are exact; only the atmospheric shadows are contained to the square. No sheen ring, no extra decoration.',
      'Font: ' + fontSource,
      'Canonical orb for an initial is the one whose colour number equals GEM_NUM[initial].'
    ],
    orbs, logos,
  };
  writeVerified('icons.json', Buffer.from(JSON.stringify(doc, null, 2)));
  console.log(`icons.json written: ${orbs.length} orbs, ${logos.length} logos`);

  // contact sheet: 26 canonical (13x2) + 4 non-canonical samples (row 3)
  const thumb = 128, pad = 10, cols = 13, cell = thumb + pad;
  const W = cols * cell + pad, H = 3 * cell + pad;
  const sheet = new Uint8Array(W * H * 4);
  for (let i = 0; i < W * H; i++) { sheet[i * 4] = 10; sheet[i * 4 + 1] = 10; sheet[i * 4 + 2] = 15; sheet[i * 4 + 3] = 255; }
  const items = [];
  for (const L of LETTERS) items.push(`${L}-${GEM_NUM[L]}`);
  for (const k of ['A-2', 'M-7', 'Z-3', 'T-1']) items.push(k);
  items.forEach((key, i) => {
    const r = Math.floor(i / cols), c = i % cols;
    const src = keep512[key];
    const x0 = pad + c * cell, y0 = pad + r * cell;
    for (let ty = 0; ty < thumb; ty++) {
      for (let tx = 0; tx < thumb; tx++) {
        const sx = Math.floor(tx * 512 / thumb), sy = Math.floor(ty * 512 / thumb);
        const si = (sy * 512 + sx) * 4, di = ((y0 + ty) * W + (x0 + tx)) * 4;
        const sa = src[si + 3] / 255;
        sheet[di] = src[si] * sa + sheet[di] * (1 - sa);
        sheet[di + 1] = src[si + 1] * sa + sheet[di + 1] * (1 - sa);
        sheet[di + 2] = src[si + 2] * sa + sheet[di + 2] * (1 - sa);
        sheet[di + 3] = src[si + 3] * sa + sheet[di + 3] * (1 - sa);
      }
    }
  });
  writeVerified('contact-sheet.png', pngEncode(W, H, sheet));
  console.log(`contact sheet written: ${W}x${H}`);
  console.log('NODE-RENDER-DONE');
}

main();
