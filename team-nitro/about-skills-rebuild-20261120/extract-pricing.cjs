// Extract the pricing slideshow presentation code, literally, from
// PRICING/pricing-live.html (fix-5 tip blob a2d06d5bb43199139f400e1688079f1b40a1b8fa,
// 11,350,562 B, sha256 7a0b837c...), local copy /tmp/pricing-live.html.
// Keeps ONLY the rules the Skills slideshow uses; everything kept is verbatim
// except the documented §2.3 adaptations (font-size <17px -> 17px) and any
// checker-FAIL color fixes. Prints a report; writes pricing-harvest.css.
const fs = require('fs');
const SRC = process.env.HOME + '/workspace/team-nitro/about-skills-rebuild-20261120/src-pricing-live.html';
const OUT = process.env.HOME + '/workspace/team-nitro/about-skills-rebuild-20261120/pricing-harvest.css';
const html = fs.readFileSync(SRC, 'utf8');
const css = html.match(/<style>([\s\S]*?)<\/style>/)[1];

// --- parse top-level rules (brace matching; keeps comments attached to rules) ---
function parseRules(text) {
  const rules = [];
  let i = 0, n = text.length;
  while (i < n) {
    while (i < n && /\s/.test(text[i])) i++;
    if (i >= n) break;
    // capture selector/prelude up to first '{' (skip comments)
    let start = i, depth = 0, j = i;
    while (j < n && text[j] !== '{') j++;
    if (j >= n) break;
    const prelude = text.slice(start, j).trim();
    depth = 1; j++;
    while (j < n && depth > 0) {
      if (text[j] === '{') depth++;
      else if (text[j] === '}') depth--;
      j++;
    }
    rules.push({ prelude, body: text.slice(start, j), start, end: j });
    i = j;
  }
  return rules;
}

const NEED = ['.ph-card', '.calc-story-card', '.has-face', '.face-left', '.face-right',
  '.ult-card', '.ult-sec', '.board-face', '.board-body', '.board-head', '.board-text',
  '.board-title', '.board-nut', '.board-sub',
  '.ult-part', '.ult-part-why', '.ult-part-sol', '.ult-part-nut', '.ult-part-head',
  '.ult-part-label', '.ult-bul', '.ult-jewel', '.ult-who', '.ult-orb',
  '.os-jewel', '.orb', '.ib-card-orb', '.orb-ring', '.orb-dot',
  '.primo', '.theme-purple',
  '.letter-beat', '.lb', '.lb-h', '.lb-big', '.letter-body', '.letter-controls',
  '.letter-dots', '.ldot', '.letter-next', '.letter-all', '.letter-sign'];
// NOTE: '.lb' as substring would match '.lb-showcase' etc.; handled by checking
// class tokens in the selector instead of raw substring for short names.
function selectorHas(sel, cls) {
  const re = new RegExp('(^|[^a-zA-Z0-9_-])' + cls.replace('.', '\\.') + '([^a-zA-Z0-9_-]|$)');
  return re.test(sel);
}
function barePrelude(prelude) {
  // Classification must ignore /* comments */: a comment mentioning .primo
  // is not a rule for .primo, and a comment before @media is not a selector.
  return prelude.replace(/\/\*[\s\S]*?\*\//g, '').trim();
}
function ruleNeeded(rawPrelude) {
  const prelude = barePrelude(rawPrelude);
  // Exclude pricing subsystems the Skills slideshow does not use: the
  // calculator, plan detail, popups, viewer and hired-views all mention
  // .primo/.os-jewel but are not the slideshow.
  if (/#calculator|\.plan-detail|\.pop-actions|\.viewer-|\.hired-view|\.calc-plan|\.calc-controls/.test(prelude)) return false;
  if (prelude.startsWith(':root')) return true;
  const sels = prelude.split(',');
  return sels.some(sel => NEED.some(cls => selectorHas(sel, cls)));
}

const adaptations = [];
function scopePrelude(prelude) {
  // Scope every harvested pricing rule under #skillsSlideshow so the pricing
  // classes (.letter-beat, .ldot, .letter-next, ...) can never restyle the
  // agreement deck above. :root and @keyframes stay global (tokens + motion).
  // A prelude may carry a leading /* comment */ (sometimes with commas) —
  // scope only the selector part after the last comment close.
  if (prelude.startsWith(':root') || prelude.startsWith('@')) return prelude;
  const ci = prelude.lastIndexOf('*/');
  const head = ci >= 0 ? prelude.slice(0, ci + 2) : '';
  const sel = ci >= 0 ? prelude.slice(ci + 2) : prelude;
  return head + sel.split(',').map(s => '#skillsSlideshow ' + s.trim()).join(', ');
}
function adapt(body, prelude) {
  // §3.1: the pricing --purple token is bright (#a06bff) -> deep royal #8e24aa
  // (the same bright->deep adaptation the agreement made). It feeds only the
  // .primo button glow.
  let out = body.replace(/--purple:#a06bff/, () => {
    adaptations.push(':root :: --purple #a06bff -> #8e24aa (§3.1 bright->deep)');
    return '--purple:#8e24aa';
  });
  // §3.1: remaining bright-purple fallbacks/defaults (never rendered — every
  // use sets --dc/--bc/--oc inline with deep tones — but the value must not
  // sit in the file): #a06bff -> #8e24aa, its rgb -> deep rgb, #d8ccff -> #8e24aa.
  if (/#a06bff|160,107,255|#d8ccff/.test(out)) {
    adaptations.push(prelude + ' :: bright-purple fallbacks -> deep #8e24aa (§3.1)');
    out = out.replace(/#a06bff/g, '#8e24aa').replace(/160,107,255/g, '142,36,170').replace(/#d8ccff/g, '#8e24aa');
  }
  // §2.3: font-size below 17px -> 17px
  out = out.replace(/font-size\s*:\s*([0-9.]+)px/g, (m, v) => {
    if (parseFloat(v) < 17) {
      adaptations.push(prelude + ' :: font-size ' + v + 'px -> 17px');
      return 'font-size:17px';
    }
    return m;
  });
  // clamp() with a minimum below 17px -> raise the minimum to 17px
  out = out.replace(/font-size\s*:\s*clamp\((\d+(?:\.\d+)?)px/g, (m, v) => {
    if (parseFloat(v) < 17) {
      adaptations.push(prelude + ' :: clamp min ' + v + 'px -> 17px');
      return 'font-size:clamp(17px';
    }
    return m;
  });
  return out;
}

const topRules = parseRules(css);
let kept = [];
let keyframesKept = new Set();
for (const r of topRules) {
  if (barePrelude(r.prelude).startsWith('@keyframes')) {
    const name = barePrelude(r.prelude).split(/\s+/)[1];
    if (name === 'letter-in' || name === 'orb-spin') { kept.push(r); keyframesKept.add(name); }
    continue;
  }
  if (barePrelude(r.prelude).startsWith('@media')) {
    const inner = parseRules(r.body.slice(r.body.indexOf('{') + 1, r.body.lastIndexOf('}')));
    const innerKept = inner.filter(ir => ruleNeeded(ir.prelude));
    if (innerKept.length) {
      const rebuilt = r.prelude + '{\n' + innerKept.map(ir => {
        const sc = scopePrelude(ir.prelude);
        return adapt(ir.body, sc).split(ir.prelude).join(sc);
      }).join('\n') + '\n}';
      kept.push({ prelude: r.prelude, body: rebuilt });
    }
    continue;
  }
  if (barePrelude(r.prelude).startsWith('@')) continue; // other at-rules: not needed
  if (ruleNeeded(r.prelude)) {
    const sc = scopePrelude(r.prelude);
    kept.push({ prelude: sc, body: adapt(r.body, sc).split(r.prelude).join(sc) });
  }
}

// collect animation names referenced by kept rules; keep those keyframes too
let anims = new Set();
for (const r of kept) {
  const m = r.body.match(/animation\s*:[^;}]*?([a-zA-Z][\w-]*)/g) || [];
  m.forEach(x => { const n = x.split(':')[1].trim().split(/\s+/)[0]; anims.add(n); });
}
for (const r of topRules) {
  if (barePrelude(r.prelude).startsWith('@keyframes')) {
    const name = barePrelude(r.prelude).split(/\s+/)[1];
    if (anims.has(name) && !keyframesKept.has(name)) { kept.push(r); keyframesKept.add(name); }
  }
}

const outCss = '/* PRICING HARVEST — the Skills slideshow presentation, taken literally from\n'
  + '   PRICING/pricing-live.html (blob a2d06d5bb43199139f400e1688079f1b40a1b8fa,\n'
  + '   11,350,562 B, sha256 7a0b837c481f5dfc...). Rules kept: ' + kept.length
  + ' of ' + topRules.length + ' top-level rules. Verbatim except the §2.3\n'
  + '   adaptations listed in the build log (font-size <17px -> 17px, the same\n'
  + '   adaptation the agreement made to this same grammar). Classes used by\n'
  + '   the Skills section only; no pricing body/chart/chooser code rides along. */\n'
  + kept.map(r => r.body).join('\n');
fs.writeFileSync(OUT, outCss);
console.log('top-level rules in pricing <style>:', topRules.length);
console.log('rules kept:', kept.length, '| keyframes:', [...keyframesKept].join(','));
console.log('bytes:', Buffer.byteLength(outCss));
console.log('--- adaptations (' + adaptations.length + ') ---');
adaptations.forEach(a => console.log(' *', a));
// check kept CSS for checker-FAIL patterns
const grayRes = [/#(?:888|999|aaa|bbb|ccc|8b8b9c|808080|777777|666666)\b/i, /\bgray\b/i, /\bgrey\b/i, /--dim\b/i, /color\s*:\s*rgba?\([^)]*,\s*0\.[0-6]\d*\)/i];
grayRes.forEach((re, i) => {
  const hits = outCss.match(new RegExp(re.source, 'gi')) || [];
  console.log('gray check', i, 'hits:', hits.length, hits.slice(0, 5));
});
const smallFonts = [...outCss.matchAll(/font-size\s*:\s*([0-9.]+)px/g)].filter(m => parseFloat(m[1]) < 17);
console.log('remaining sub-17px font-sizes:', smallFonts.length, smallFonts.slice(0, 5).map(m => m[0]));
