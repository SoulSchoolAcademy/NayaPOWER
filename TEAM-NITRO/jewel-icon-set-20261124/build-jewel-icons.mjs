// build-jewel-icons.mjs — NayaNET custom jewel icon set, maker round 2026-11-24
// Fix round 2026-11-24 (checker GOES BACK): emoji brought into the ONE
// construction, bar variants baked, think bubble moved inside the disc,
// wow mouth enlarged, emoji -sm variants added. Generates every SVG in
// icons/ from one construction, so all 55 speak one language.
// Construction (Design Laws §4, Real Object Law): obsidian disc (board black inside,
// no glow inside) · silver bezel (the emblem's silver frame, 135° metal) · white
// glyph as a real object (shadow copy down-right + metal-white body + top-left
// specular) · the icon's OWN deep colour as rim + outside halo + crown jewel
// (a faceted diamond set at 12 o'clock, the emblem's crown jewel) · slow orbit ring.
// Emoji faces ARE the white glyph on that same obsidian disc — no second
// construction, no coloured fill inside (laws §4 / §3 + §12.8).
// One light, top-left, always. Deep palette only. No flat fills of colour.
import { writeFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "icons");

// ---------- colour helpers ----------
function hexRgb(h) { const n = parseInt(h.slice(1), 16); return [n >> 16 & 255, n >> 8 & 255, n & 255]; }
function mix(h, target, t) { const a = hexRgb(h), b = hexRgb(target);
  return "#" + a.map((v, i) => Math.round(v + (b[i] - v) * t).toString(16).padStart(2, "0")).join(""); }
const light = (h, t = 0.55) => mix(h, "#ffffff", t);
const dark = (h, t = 0.55) => mix(h, "#000000", t);

// ---------- glyph library (24x24 grid) ----------
// mail / globe / pulse harvested verbatim from the Personal + Hub blobs
// (see smart-messenger-icons-20261119 MAKER-REPORT §2); the rest are the
// Feather-style stroke glyphs already in use across Personal/Hub.
const G = {
  mail: '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="M3 7l9 6 9-6"/>',
  chat: '<path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>',
  audio: '<path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><path d="M12 19v4"/><path d="M8 23h8"/>',
  video: '<polygon points="23 7 16 12 23 17 23 7"/><rect x="1" y="5" width="15" height="14" rx="2"/>',
  search: '<circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/>',
  compose: '<path d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"/>',
  send: '<path d="M22 2L11 13"/><path d="M22 2l-7 20-4-9-9-4 22-7z"/>',
  plus: '<path d="M12 5v14M5 12h14"/>',
  contacts: '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
  lists: '<path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01"/>',
  spaces: '<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3c2.6 2.6 4 5.7 4 9s-1.4 6.4-4 9c-2.6-2.6-4-5.7-4-9s1.4-6.4 4-9z"/>',
  settings: '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>',
  activity: '<path d="M3 12h4l2.5-6 4 12 2.5-6H21"/>',
  ecosystem: '<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/>',
  heart: '<path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>',
  star: '<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>',
  sparkle: '<path d="M12 2l2.4 7.6L22 12l-7.6 2.4L12 22l-2.4-7.6L2 12l7.6-2.4L12 2z"/>',
  thumbs: '<path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3z"/><path d="M7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3"/>',
  flame: '<path d="M12 23c-4.97 0-9-3.58-9-8 0-2.52 1.13-4.77 2.91-6.36.33 1.2.82 2.35 1.45 3.36C8.6 9.9 10.5 6 12 2c.5 2.5 1.5 4.5 3 6 .4-1 1-2 1.5-3C17.5 7 21 10 21 15c0 4.42-4.03 8-9 8z"/>',
};

// Filled glyphs (heart/star/sparkle/thumbs/flame) render as filled shapes;
// stroke glyphs render as strokes. Both get the same depth treatment.
const FILLED = new Set(["heart", "star", "sparkle", "thumbs", "flame"]);

// ---------- shared defs ----------
function defs(p, c) {
  return `<defs>
<radialGradient id="${p}disc" cx="35%" cy="28%" r="78%">
<stop offset="0%" stop-color="#26262e"/><stop offset="45%" stop-color="#0b0b0f"/><stop offset="100%" stop-color="#050607"/>
</radialGradient>
<linearGradient id="${p}silver" x1="0" y1="0" x2="1" y2="1">
<stop offset="0%" stop-color="#f2f3f5"/><stop offset="30%" stop-color="#b9bdc7"/><stop offset="50%" stop-color="#7d818c"/><stop offset="70%" stop-color="#a9adb8"/><stop offset="100%" stop-color="#d7d9de"/>
</linearGradient>
<linearGradient id="${p}glyph" x1="0" y1="0" x2="1" y2="1">
<stop offset="0%" stop-color="#ffffff"/><stop offset="55%" stop-color="#eef0f2"/><stop offset="100%" stop-color="#c2c6cd"/>
</linearGradient>
<linearGradient id="${p}gem" x1="0" y1="0" x2="1" y2="1">
<stop offset="0%" stop-color="${light(c, 0.6)}"/><stop offset="45%" stop-color="${c}"/><stop offset="100%" stop-color="${dark(c, 0.45)}"/>
</linearGradient>
<radialGradient id="${p}halo" cx="50%" cy="50%" r="50%">
<stop offset="0%" stop-color="${c}" stop-opacity=".5"/><stop offset="62%" stop-color="${c}" stop-opacity=".16"/><stop offset="100%" stop-color="${c}" stop-opacity="0"/>
</radialGradient>
</defs>`;
}

// Faceted crown jewel at 12 o'clock — the emblem's crown diamond, in the icon's colour.
function crownJewel(p, c, cx, cy, r) {
  const pts = `${cx},${cy - r} ${cx + r},${cy} ${cx},${cy + r} ${cx - r},${cy}`;
  return `<g>
<polygon points="${pts}" fill="url(#${p}gem)" stroke="url(#${p}silver)" stroke-width="1"/>
<path d="M${cx} ${cy - r}L${cx} ${cy + r}M${cx - r} ${cy}L${cx + r} ${cy}M${cx} ${cy - r}L${cx - r * 0.55} ${cy + r * 0.45}M${cx} ${cy - r}L${cx + r * 0.55} ${cy + r * 0.45}" fill="none" stroke="#ffffff" stroke-opacity=".55" stroke-width=".7"/>
<circle cx="${cx - r * 0.28}" cy="${cy - r * 0.3}" r="${(r * 0.16).toFixed(2)}" fill="#ffffff"/>
</g>`;
}

// Glyph with depth: dark cast copy down-right, metal-white body, top-left specular.
function glyph(p, name, tx, ty, scale, sw) {
  const inner = G[name];
  if (FILLED.has(name)) {
    return `<g transform="translate(${tx + 1.3},${ty + 1.6}) scale(${scale})" fill="#000000" fill-opacity=".45">${inner}</g>
<g transform="translate(${tx},${ty}) scale(${scale})" fill="url(#${p}glyph)" stroke="url(#${p}silver)" stroke-width="${(0.35 * scale).toFixed(2)}" stroke-linejoin="round">${inner}</g>
<g transform="translate(${tx},${ty}) scale(${scale})" fill="#ffffff" fill-opacity=".85"><circle cx="8.2" cy="7.4" r="1.1"/></g>`;
  }
  return `<g transform="translate(${tx + 1.3},${ty + 1.6}) scale(${scale})" fill="none" stroke="#000000" stroke-opacity=".5" stroke-width="${sw}" stroke-linecap="round" stroke-linejoin="round">${inner}</g>
<g transform="translate(${tx},${ty}) scale(${scale})" fill="none" stroke="url(#${p}glyph)" stroke-width="${sw}" stroke-linecap="round" stroke-linejoin="round">${inner}</g>
<g transform="translate(${tx},${ty}) scale(${scale})" fill="none" stroke="#ffffff" stroke-opacity=".9" stroke-width="${(sw * 0.42).toFixed(2)}" stroke-linecap="round"><path d="M7.5 5.5l1.6-1.1"/></g>`;
}

// ---------- FULL icon: 96x96, bezel + orbit + halo + crown jewel ----------
function fullIcon(name, label, color, glyphName, opts = {}) {
  const p = "j" + name.replace(/[^a-z0-9]/gi, "") + "-";
  const c = color;
  const orbitDur = opts.orbit || 120;
  const dir = opts.ccw ? "reverse" : "normal";
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 96" width="96" height="96" role="img" aria-label="${label} — NayaNET jewel icon">
<style>.jwl-orbit{transform-box:view-box;transform-origin:center;animation:jwl-spin linear infinite}@keyframes jwl-spin{to{transform:rotate(360deg)}}</style>
${defs(p, c)}
<circle cx="48" cy="48" r="47" fill="url(#${p}halo)"/>
<g class="jwl-orbit" style="animation-duration:${orbitDur}s;animation-direction:${dir}">
<circle cx="48" cy="48" r="44" fill="none" stroke="${c}" stroke-opacity=".5" stroke-width="1" stroke-dasharray="0.5 7" stroke-linecap="round"/>
<circle cx="48" cy="4" r="2.8" fill="url(#${p}gem)" stroke="#ffffff" stroke-opacity=".8" stroke-width=".7"/>
</g>
<circle cx="48" cy="48" r="38" fill="none" stroke="url(#${p}silver)" stroke-width="3"/>
<circle cx="48" cy="48" r="38" fill="none" stroke="${c}" stroke-opacity=".85" stroke-width="1.1"/>
<circle cx="48" cy="48" r="35.5" fill="url(#${p}disc)"/>
<circle cx="48" cy="48" r="35.5" fill="none" stroke="#ffffff" stroke-opacity=".13" stroke-width=".8"/>
${crownJewel(p, c, 48, 10, 6)}
${glyph(p, glyphName, 24, 24, 2, 2.6)}
</svg>
`;
  return svg;
}

// ---------- SMALL icon: 48x48, for 16–24px inside message bubbles ----------
// Bold glyph, thick rim, no bezel, no orbit — crisp and real at small sizes.
function smallIcon(name, label, color, glyphName) {
  const p = "s" + name.replace(/[^a-z0-9]/gi, "") + "-";
  const c = color;
  const sw = FILLED.has(glyphName) ? 0 : 3.1;
  const inner = G[glyphName];
  const glyphEl = FILLED.has(glyphName)
    ? `<g transform="translate(12.6,13) scale(0.95)" fill="#000000" fill-opacity=".45">${inner}</g>
<g transform="translate(12,12) scale(0.95)" fill="url(#${p}glyph)" stroke="url(#${p}silver)" stroke-width="0.4" stroke-linejoin="round">${inner}</g>`
    : `<g transform="translate(12.6,13) scale(0.95)" fill="none" stroke="#000000" stroke-opacity=".5" stroke-width="${sw}" stroke-linecap="round" stroke-linejoin="round">${inner}</g>
<g transform="translate(12,12) scale(0.95)" fill="none" stroke="url(#${p}glyph)" stroke-width="${sw}" stroke-linecap="round" stroke-linejoin="round">${inner}</g>`;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48" role="img" aria-label="${label} — NayaNET jewel icon, small">
${defs(p, c)}
<circle cx="24" cy="24" r="23" fill="url(#${p}halo)"/>
<circle cx="24" cy="24" r="21" fill="url(#${p}disc)"/>
<circle cx="24" cy="24" r="21" fill="none" stroke="${c}" stroke-width="2"/>
<circle cx="24" cy="24" r="21" fill="none" stroke="#ffffff" stroke-opacity=".35" stroke-width=".7"/>
${crownJewel(p, c, 24, 4.5, 3)}
${glyphEl}
</svg>
`;
}

// ---------- EMOJI: the ONE construction, faces as the white glyph ----------
// Identical anatomy to fullIcon: obsidian disc (board black inside, no glow
// inside) · silver bezel · own-colour rim + halo + crown jewel at 12 o'clock ·
// slow orbit ring. The face is the white glyph — a real object with a dark
// cast copy down-right and a top-left specular, in the glyph gradient.
// (Fix round: the first round's gem-orb fill was a second construction —
// coloured fill inside, no orbit, no crown — contradicting laws §4 / §3 +
// §12.8. That construction is gone; every emoji is built here now.)
function emojiIcon(name, label, color, face, orbitDur, ccw) {
  const p = "e" + name.replace(/[^a-z0-9]/gi, "") + "-";
  const c = color;
  const dir = ccw ? "reverse" : "normal";
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 96" width="96" height="96" role="img" aria-label="${label} — NayaNET jewel emoji">
<style>.jwl-orbit{transform-box:view-box;transform-origin:center;animation:jwl-spin linear infinite}@keyframes jwl-spin{to{transform:rotate(360deg)}}</style>
${defs(p, c)}
<circle cx="48" cy="48" r="47" fill="url(#${p}halo)"/>
<g class="jwl-orbit" style="animation-duration:${orbitDur}s;animation-direction:${dir}">
<circle cx="48" cy="48" r="44" fill="none" stroke="${c}" stroke-opacity=".5" stroke-width="1" stroke-dasharray="0.5 7" stroke-linecap="round"/>
<circle cx="48" cy="4" r="2.8" fill="url(#${p}gem)" stroke="#ffffff" stroke-opacity=".8" stroke-width=".7"/>
</g>
<circle cx="48" cy="48" r="38" fill="none" stroke="url(#${p}silver)" stroke-width="3"/>
<circle cx="48" cy="48" r="38" fill="none" stroke="${c}" stroke-opacity=".85" stroke-width="1.1"/>
<circle cx="48" cy="48" r="35.5" fill="url(#${p}disc)"/>
<circle cx="48" cy="48" r="35.5" fill="none" stroke="#ffffff" stroke-opacity=".13" stroke-width=".8"/>
${crownJewel(p, c, 48, 10, 6)}
${face(p)}
</svg>
`;
}

// ---------- EMOJI SMALL: 48x48, for 16–24px reaction rows ----------
// Same frame as smallIcon (obsidian disc, own-colour rim, crown jewel, no
// orbit — crisp at small sizes), the face scaled half into the disc.
function emojiSmallIcon(name, label, color, face) {
  const p = "f" + name.replace(/[^a-z0-9]/gi, "") + "-";
  const c = color;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48" role="img" aria-label="${label} — NayaNET jewel emoji, small">
${defs(p, c)}
<circle cx="24" cy="24" r="23" fill="url(#${p}halo)"/>
<circle cx="24" cy="24" r="21" fill="url(#${p}disc)"/>
<circle cx="24" cy="24" r="21" fill="none" stroke="${c}" stroke-width="2"/>
<circle cx="24" cy="24" r="21" fill="none" stroke="#ffffff" stroke-opacity=".35" stroke-width=".7"/>
${crownJewel(p, c, 24, 4.5, 3)}
<g transform="translate(24,24) scale(0.5) translate(-48,-48)">${face(p)}</g>
</svg>
`;
}

// Faces: white features with a dark cast copy down-right, stroke-width 3.
// Every feature sits inside the disc (r=35.5 about 48,48): the farthest
// point is the think outer bubble at (68,26) r=2.6 — centre distance 29.7,
// outer edge 32.3, clear of the disc edge and the bezel. (Fix round: the
// old outer bubble at (74,23) r=3.2 sat ON the bezel as a stray ring.)
function faceStroke(p, d, w = 3) {
  return `<path d="${d}" fill="none" stroke="#000000" stroke-opacity=".4" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round" transform="translate(1.2,1.6)"/>
<path d="${d}" fill="none" stroke="url(#${p}glyph)" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round"/>`;
}
function faceFill(p, d) {
  return `<path d="${d}" fill="#000000" fill-opacity=".4" transform="translate(1.2,1.6)"/>
<path d="${d}" fill="url(#${p}glyph)"/>`;
}
const FACES = {
  smile: (p) => faceStroke(p, "M36 56Q48 68 60 56") + `<circle cx="36" cy="42" r="3.4" fill="url(#${p}glyph)"/><circle cx="60" cy="42" r="3.4" fill="url(#${p}glyph)"/>`,
  laugh: (p) => faceStroke(p, "M31 44Q36 37 41 44M55 44Q60 37 65 44") + faceFill(p, "M35 53Q48 72 61 53Q48 61 35 53Z"),
  love: (p) => {
    const h = (cx, cy, s) => `<g transform="translate(${cx},${cy}) scale(${s})"><path d="M0 3.2C-1.8 1-4.5 1.4-5.4 3.4-6.2 5.2-5 7.4 0 11c5-3.6 6.2-5.8 5.4-7.6C4.5 1.4 1.8 1 0 3.2z" fill="url(#${p}glyph)"/></g>`;
    return h(36, 40, 1) + h(60, 40, 1) + faceStroke(p, "M36 56Q48 68 60 56");
  },
  // Wow mouth: an open oval (rx 5.5, ry 7), not the old r=4.8 dot — the dot
  // was a speck at 16px. (Fix round follow-on.)
  wow: (p) => `<circle cx="36" cy="42" r="3.6" fill="url(#${p}glyph)"/><circle cx="60" cy="42" r="3.6" fill="url(#${p}glyph)"/>` + `<ellipse cx="49.2" cy="60.6" rx="5.5" ry="7" fill="#000000" fill-opacity=".4"/><ellipse cx="48" cy="59" rx="5.5" ry="7" fill="url(#${p}glyph)"/>`,
  think: (p) => `<circle cx="36" cy="42" r="3.4" fill="url(#${p}glyph)"/><circle cx="60" cy="42" r="3.4" fill="url(#${p}glyph)"/>` + faceStroke(p, "M40 62H56", 2.6) + `<circle cx="63" cy="32" r="2" fill="url(#${p}glyph)"/><circle cx="68" cy="26" r="2.6" fill="none" stroke="url(#${p}glyph)" stroke-width="2"/>`,
  cool: (p) => faceFill(p, "M28 38h14a4 4 0 0 1 4 4v3a4 4 0 0 1-4 4H32a4 4 0 0 1-4-4v-3a4 4 0 0 1 0-4zM54 38h14a4 4 0 0 1 4 4v3a4 4 0 0 1-4 4H58a4 4 0 0 1-4-4v-3a4 4 0 0 1 0-4z") + faceStroke(p, "M42 42H54", 2.6) + faceStroke(p, "M38 58Q48 66 58 58", 2.6),
  sad: (p) => `<circle cx="36" cy="42" r="3.4" fill="url(#${p}glyph)"/><circle cx="60" cy="42" r="3.4" fill="url(#${p}glyph)"/>` + faceStroke(p, "M36 64Q48 56 60 64"),
  // Party hat pulled inside the disc (apex 22, clear of the crown jewel
  // at y 4–16) — the old apex at y 12 sat on the disc edge under the crown.
  party: (p) => faceFill(p, "M48 22l9 14H39z") + `<circle cx="48" cy="19" r="2.2" fill="url(#${p}glyph)"/>` + faceStroke(p, "M31 46Q36 39 41 46M55 46Q60 39 65 46") + faceStroke(p, "M36 56Q48 68 60 56"),
  peace: (p) => faceStroke(p, "M31 42Q36 47 41 42M55 42Q60 47 65 42") + faceStroke(p, "M38 57Q48 64 58 57") + `<ellipse cx="48" cy="22" rx="11" ry="3.2" fill="none" stroke="url(#${p}glyph)" stroke-width="2.4"/>`,
};

// ---------- the sets ----------
// Deep palette: purple #8e24aa · blue #0f52ba · green #07925f · gold #d4a017 ·
// orange #c2410c · red #c62828 · magenta #a21caf · indigo #3f51b5 · cyan #0e7490 · violet #6d28d9
const CORE = [
  ["mail", "Mail", "#0f52ba", "mail", 120, false],
  ["chat", "Chat", "#8e24aa", "chat", 75, true],
  ["audio", "Audio", "#07925f", "audio", 150, false],
  ["video", "Video", "#d4a017", "video", 90, true],
  ["search", "Search", "#c2410c", "search", 180, false],
  ["compose", "Compose", "#c62828", "compose", 60, true],
  ["send", "Send", "#a21caf", "send", 135, false],
  ["plus", "Add", "#3f51b5", "plus", 105, true],
  ["contacts", "Contacts", "#0e7490", "contacts", 165, false],
  ["lists", "Lists", "#6d28d9", "lists", 70, true],
  ["spaces", "Spaces", "#8e24aa", "spaces", 120, false],
  ["settings", "Settings", "#0f52ba", "settings", 85, true],
];
// Message-presentation jewels (Shawn's point 7): type colours per the dial —
// Chat purple, Mail gold, Post violet. Small variants ride inside bubbles.
const PRESENT = [
  ["naya-mark", "Naya mark", "#8e24aa", "diamond"],
  ["type-chat", "Message type — Chat", "#8e24aa", "chat"],
  ["type-mail", "Message type — Mail", "#d4a017", "mail"],
  ["type-post", "Message type — Post", "#6d28d9", "sparkle"],
  ["react-heart", "Reaction — Heart", "#c62828", "heart"],
  ["react-star", "Reaction — Star", "#d4a017", "star"],
  ["react-sparkle", "Reaction — Sparkle", "#6d28d9", "sparkle"],
];
// Bottom-bar extras for the showcase bar demo (the five + CONNECT).
// bar-add / bar-worlds are BAKED variants for the fixed bottom-bar colour
// flow (laws §3.2): ADD must render royal purple #8e24aa and WORLDS deep
// gold #d4a017. The core plus (indigo) and spaces (purple) keep their own
// spectrum slots — a --c wrapper cannot recolour a baked SVG, so the bar
// gets its own files. (Fix round, checker item 2.)
const BAR = [
  ["bar-activity", "Activity", "#07925f", "activity"],
  ["bar-ecosystem", "Ecosystem", "#c2410c", "ecosystem"],
  ["bar-connect", "Connect", "#c62828", "contacts"],
  ["bar-add", "Add", "#8e24aa", "plus"],
  ["bar-worlds", "Worlds", "#d4a017", "spaces"],
];
const EMOJI = [
  ["smile", "Smile", "#d4a017", "smile"],
  ["laugh", "Laugh", "#c2410c", "laugh"],
  ["love", "Love", "#c62828", "love"],
  ["wow", "Wow", "#8e24aa", "wow"],
  ["think", "Think", "#0f52ba", "think"],
  ["cool", "Cool", "#0e7490", "cool"],
  ["sad", "Sad", "#3f51b5", "sad"],
  ["party", "Party", "#a21caf", "party"],
  ["peace", "Peace", "#07925f", "peace"],
  ["fire", "Fire", "#c2410c", "flame"],
  ["thumbs-up", "Thumbs up", "#6d28d9", "thumbs"],
  ["star", "Star", "#d4a017", "star"],
];

// The Naya mark: the emblem's faceted diamond, drawn as the glyph itself.
function diamondGlyph(p, c) {
  return `<g transform="translate(24,24) scale(2)">
<polygon points="12,1.5 22.5,12 12,22.5 1.5,12" fill="url(#${p}gem)" stroke="url(#${p}silver)" stroke-width="1.1" stroke-linejoin="round"/>
<path d="M12 1.5L12 22.5M1.5 12L22.5 12M12 1.5L6.5 17.5M12 1.5L17.5 17.5" fill="none" stroke="#ffffff" stroke-opacity=".55" stroke-width=".8"/>
<circle cx="9" cy="8" r="1" fill="#ffffff"/>
</g>`;
}

function write(rel, content) {
  const full = join(ROOT, rel);
  mkdirSync(dirname(full), { recursive: true });
  writeFileSync(full, content);
  return content.length;
}

const report = [];
let n = 0;
for (const [slug, label, color, glyphName, dur, ccw] of CORE) {
  const svg = fullIcon(slug, label, color, glyphName, { orbit: dur, ccw });
  report.push([`core/${slug}.svg`, write(`core/${slug}.svg`, svg)]); n++;
}
for (const [slug, label, color, glyphName] of BAR) {
  const svg = fullIcon(slug, label, color, glyphName, { orbit: 95, ccw: false });
  report.push([`presentation/${slug}.svg`, write(`presentation/${slug}.svg`, svg)]); n++;
}
for (const [slug, label, color, glyphName] of PRESENT) {
  let svg;
  if (glyphName === "diamond") {
    const p = "j" + slug.replace(/[^a-z0-9]/gi, "") + "-";
    svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 96" width="96" height="96" role="img" aria-label="${label} — NayaNET jewel icon">
<style>.jwl-orbit{transform-box:view-box;transform-origin:center;animation:jwl-spin linear infinite}@keyframes jwl-spin{to{transform:rotate(360deg)}}</style>
${defs(p, color)}
<circle cx="48" cy="48" r="47" fill="url(#${p}halo)"/>
<g class="jwl-orbit" style="animation-duration:120s"><circle cx="48" cy="48" r="44" fill="none" stroke="${color}" stroke-opacity=".5" stroke-width="1" stroke-dasharray="0.5 7" stroke-linecap="round"/><circle cx="48" cy="4" r="2.8" fill="url(#${p}gem)" stroke="#ffffff" stroke-opacity=".8" stroke-width=".7"/></g>
<circle cx="48" cy="48" r="38" fill="none" stroke="url(#${p}silver)" stroke-width="3"/>
<circle cx="48" cy="48" r="38" fill="none" stroke="${color}" stroke-opacity=".85" stroke-width="1.1"/>
<circle cx="48" cy="48" r="35.5" fill="url(#${p}disc)"/>
<circle cx="48" cy="48" r="35.5" fill="none" stroke="#ffffff" stroke-opacity=".13" stroke-width=".8"/>
${crownJewel(p, color, 48, 10, 6)}
${diamondGlyph(p, color)}
</svg>
`;
  } else {
    svg = fullIcon(slug, label, color, glyphName, { orbit: 120, ccw: false });
  }
  report.push([`presentation/${slug}.svg`, write(`presentation/${slug}.svg`, svg)]); n++;
  const sm = smallIcon(slug, label, color, glyphName);
  report.push([`presentation/${slug}-sm.svg`, write(`presentation/${slug}-sm.svg`, sm)]); n++;
}
let ei = 0;
for (const [slug, label, color, kind] of EMOJI) {
  // Glyph emojis: the glyph itself, faceted in white, on the obsidian disc.
  // faceFn takes the id prefix as its argument, like FACES — the -sm file
  // uses a different prefix, so the gradient ids must follow the caller.
  let faceFn;
  if (kind === "flame" || kind === "thumbs" || kind === "star") {
    faceFn = (pp) => kind === "flame"
      ? `<g transform="translate(25.5,26) scale(1.9)"><path d="${G.flame.match(/d="([^"]+)"/)[1]}" fill="url(#${pp}glyph)"/></g>`
      : kind === "thumbs"
        ? `<g transform="translate(25,27) scale(1.9)" fill="url(#${pp}glyph)" stroke="url(#${pp}silver)" stroke-width=".5" stroke-linejoin="round">${G.thumbs}</g>`
        : `<g transform="translate(26,26) scale(1.85)" fill="url(#${pp}glyph)" stroke="url(#${pp}silver)" stroke-width=".6" stroke-linejoin="round">${G.star}</g>`;
  } else {
    faceFn = FACES[kind];
  }
  // Orbit 65–175s, alternating direction, same range as the core set.
  const svg = emojiIcon(slug, label, color, faceFn, 65 + ei * 10, ei % 2 === 1);
  report.push([`emoji/${slug}.svg`, write(`emoji/${slug}.svg`, svg)]); n++;
  const sm = emojiSmallIcon(slug, label, color, faceFn);
  report.push([`emoji/${slug}-sm.svg`, write(`emoji/${slug}-sm.svg`, sm)]); n++;
  ei++;
}

console.log(`icons written: ${n}`);
for (const [rel, size] of report) console.log(`  ${rel} ${size}B`);
