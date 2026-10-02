/* ═══════════════════════════════════════════════════════════════════
   NAYANET ICON SYSTEM V1 — executable jewel logic
   Set A · Jewel Marks: luminous orbs for identity moments (rail, heroes).
   Set B · Action Glyphs: obsidian chips for controls.
   Orb recipe: light source upper-left (38%/30%) → white-hot core → accent
   light → accent → deep accent → obsidian edge. White glyph, 40% of diameter.
   Rim 1.5px accent @50%. Glow ≈25% of diameter. Ground: always on black.
   Scale steps: 96 / 64 / 48 / 32. Never in-between. Never stretched.
   Laws: one icon per idea · glow = meaning · never flat/emoji/stock ·
   jewels at identity moments, chips at controls · Naya emblem ≥32px,
   never recolored.
   Source logic: workspace hub-blueprints ICON-SYSTEM-V1-LOGIC-DRAFT.md
   ═══════════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  /* ——— color helpers ——— */
  function hx(h) { h = h.replace('#', ''); return [parseInt(h.slice(0, 2), 16), parseInt(h.slice(2, 4), 16), parseInt(h.slice(4, 6), 16)]; }
  function toHx(c) { return '#' + c.map(v => Math.max(0, Math.min(255, Math.round(v))).toString(16).padStart(2, '0')).join(''); }
  function mix(a, b, t) { const A = hx(a), B = hx(b); return toHx(A.map((v, i) => v + (B[i] - v) * t)); }
  let __uid = 0;
  function uid() { return 'nj' + (++__uid) + Math.floor(Math.random() * 1e6).toString(36); }
  function snap(s) { const steps = [32, 48, 64, 96]; let best = steps[0]; for (const st of steps) { if (Math.abs(st - s) < Math.abs(best - s)) best = st; } return best; }
  function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;'); }

  /* ——— glyphs: white, geometric, 48×48 grid ——— */
  const G = {
    waves: '<path d="M10 18c4-5 8-5 12 0s8 5 12 0M10 26c4-5 8-5 12 0s8 5 12 0M10 34c4-5 8-5 12 0s8 5 12 0" fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round"/>',
    spark: '<path d="M24 7l4 13 13 4-13 4-4 13-4-13-13-4 13-4z" fill="#fff"/>',
    grid: '<g fill="#fff"><rect x="13" y="13" width="6.5" height="6.5" rx="1"/><rect x="20.75" y="13" width="6.5" height="6.5" rx="1"/><rect x="28.5" y="13" width="6.5" height="6.5" rx="1"/><rect x="13" y="20.75" width="6.5" height="6.5" rx="1"/><rect x="20.75" y="20.75" width="6.5" height="6.5" rx="1"/><rect x="28.5" y="20.75" width="6.5" height="6.5" rx="1"/><rect x="13" y="28.5" width="6.5" height="6.5" rx="1"/><rect x="20.75" y="28.5" width="6.5" height="6.5" rx="1"/><rect x="28.5" y="28.5" width="6.5" height="6.5" rx="1"/></g>',
    diamond: '<path d="M24 9l13 15-13 15-13-15z" fill="#fff"/>',
    'diamond-o': '<path d="M24 9l13 15-13 15-13-15z" fill="none" stroke="#fff" stroke-width="3.4" stroke-linejoin="round"/>',
    exchange: '<path d="M11 18h20m-6.5-6.5L31 18l-6.5 6.5M37 30H17m6.5-6.5L17 30l6.5 6.5" fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>',
    nodes: '<g stroke="#fff" stroke-width="2.6"><line x1="24" y1="15" x2="15" y2="31"/><line x1="24" y1="15" x2="33" y2="31"/><line x1="15" y1="31" x2="33" y2="31"/></g><g fill="#fff"><circle cx="24" cy="14" r="4.6"/><circle cx="14" cy="33" r="4.6"/><circle cx="34" cy="33" r="4.6"/></g>',
    lines: '<path d="M13 17h22M13 24h22M13 31h14" stroke="#fff" stroke-width="3.6" stroke-linecap="round"/>',
    envelope: '<g fill="none" stroke="#fff" stroke-width="3"><rect x="11" y="15" width="26" height="18" rx="3"/><path d="M12 18l12 9 12-9"/></g>',
    hex: '<path d="M24 9l11.5 6.6v13.2L24 39l-11.5-6.6V19.2z" fill="none" stroke="#fff" stroke-width="3.2" stroke-linejoin="round"/>',
    gear: '<g fill="none" stroke="#fff" stroke-width="3"><circle cx="24" cy="24" r="7.5"/><path d="M24 9.5v5M24 33.5v5M9.5 24h5M33.5 24h5M14 14l3.6 3.6M30.4 30.4L34 34M34 14l-3.6 3.6M17.6 30.4L14 34" stroke-linecap="round"/></g>',
    search: '<g fill="none" stroke="#fff" stroke-width="3.4"><circle cx="21" cy="21" r="9"/><path d="M28 28l8 8" stroke-linecap="round"/></g>',
    play: '<path d="M19 15l13 9-13 9z" fill="#fff"/>',
    back: '<path d="M29 14l-9 10 9 10" fill="none" stroke="#fff" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/>',
    fwd: '<path d="M19 14l9 10-9 10" fill="none" stroke="#fff" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/>',
    save: '<path d="M15 11h18v26l-9-6.5L15 37z" fill="none" stroke="#fff" stroke-width="3.2" stroke-linejoin="round"/>',
    close: '<path d="M17 17l14 14M31 17L17 31" stroke="#fff" stroke-width="3.6" stroke-linecap="round"/>',
    done: '<path d="M15 25l7 7 12-15" fill="none" stroke="#fff" stroke-width="3.8" stroke-linecap="round" stroke-linejoin="round"/>',
    add: '<path d="M24 15v18M15 24h18" stroke="#fff" stroke-width="3.8" stroke-linecap="round"/>',
    alert: '<path d="M24 14v13" stroke="#fff" stroke-width="3.6" stroke-linecap="round"/><circle cx="24" cy="34.5" r="2.2" fill="#fff"/>',
    lock: '<g fill="none" stroke="#fff" stroke-width="3.2"><rect x="15" y="22" width="18" height="14" rx="3"/><path d="M18 22v-4a6 6 0 0112 0v4"/></g>',
    refresh: '<path d="M36 24a12 12 0 11-3.5-8.5M36 10v7h-7" fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>',
    home: '<path d="M12 24l12-10 12 10M16 21v15h16V21" fill="none" stroke="#fff" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>',
    open: '<path d="M17 24h18m-7-7l7 7-7 7" fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>',
    evidence: '<path d="M24 12l10 12-10 12-10-12z" fill="none" stroke="#fff" stroke-width="3" stroke-linejoin="round"/><circle cx="24" cy="24" r="2.4" fill="#fff"/>'
  };

  /* ——— the twelve jewel marks: 11 rooms + the Naya emblem ———
     Known token collisions (feed/connect, library/mail) differentiate by glyph;
     token fix remains a director decision. */
  const JEWELS = {
    feed:        { accent: '#55e39a', glyph: 'waves' },
    today:       { accent: '#d86cff', glyph: 'spark' },
    reports:     { accent: '#6675ff', glyph: 'grid' },
    library:     { accent: '#55b9ee', glyph: 'diamond' },
    connect:     { accent: '#55e39a', glyph: 'exchange' },
    ledger:      { accent: '#f1d75a', glyph: 'diamond-o' },
    connections: { accent: '#ff9a5a', glyph: 'nodes' },
    lists:       { accent: '#9d75ff', glyph: 'lines' },
    mail:        { accent: '#55b9ee', glyph: 'envelope' },
    spaces:      { accent: '#b8ee57', glyph: 'hex' },
    settings:    { accent: '#aaa4b1', glyph: 'gear' },
    naya:        { accent: '#9d75ff', glyph: 'spark' }
  };
  const NAMES = { feed: 'Smart Feed', today: 'Today', reports: 'Reports', library: 'Library', connect: 'Smart Connect', ledger: 'Smart Ledger', connections: 'Your Connections', lists: 'Smart Lists', mail: 'Smart Mail', spaces: 'Smart Spaces', settings: 'Settings', naya: 'Naya' };

  /* ——— Set A: jewel mark ——— */
  function mark(id, size) {
    size = snap(size || 48);
    const j = JEWELS[id] || { accent: '#9d75ff', glyph: 'spark' };
    const a = j.accent;
    const light = mix(a, '#ffffff', 0.55), deep = mix(a, '#050508', 0.62);
    const gid = uid();
    const glow = Math.round(size * 0.25);
    const gs = (size * 0.40 / 48).toFixed(3);
    return '<svg class="jewel-mark" width="' + size + '" height="' + size + '" viewBox="0 0 96 96" role="img" aria-label="' + esc(NAMES[id] || id) + ' jewel">'
      + '<defs><radialGradient id="' + gid + '" cx="38%" cy="30%" r="78%">'
      + '<stop offset="0%" stop-color="#ffffff"/><stop offset="16%" stop-color="' + light + '"/>'
      + '<stop offset="46%" stop-color="' + a + '"/><stop offset="74%" stop-color="' + deep + '"/>'
      + '<stop offset="100%" stop-color="#07070c"/></radialGradient></defs>'
      + '<circle cx="48" cy="48" r="45" fill="url(#' + gid + ')" stroke="' + a + '" stroke-opacity="0.5" stroke-width="1.5" style="filter:drop-shadow(0 0 ' + glow + 'px ' + a + '59)"/>'
      + '<g transform="translate(48 48) scale(' + gs + ') translate(-24 -24)">' + (G[j.glyph] || G.spark) + '</g>'
      + '</svg>';
  }

  /* ——— Set B: action glyph chip ——— */
  function chip(name, size, accent) {
    size = size || 24; accent = accent || '#9d75ff';
    const gs = (size * 0.55 / 48).toFixed(3);
    return '<svg class="action-chip" width="' + size + '" height="' + size + '" viewBox="0 0 48 48" role="img" aria-label="' + esc(name) + '">'
      + '<circle cx="24" cy="24" r="21" fill="#12151d" stroke="' + accent + '" stroke-opacity="0.55" stroke-width="2"/>'
      + '<g transform="translate(24 24) scale(' + gs + ') translate(-24 -24)">' + (G[name] || G.evidence) + '</g></svg>';
  }

  /* ——— the Naya emblem: never below 32px, never recolored ——— */
  function emblem(size) {
    return mark('naya', Math.max(32, size || 48));
  }

  window.NayaJewels = { mark, chip, emblem, JEWELS, NAMES, scaleSteps: [32, 48, 64, 96] };
})();
