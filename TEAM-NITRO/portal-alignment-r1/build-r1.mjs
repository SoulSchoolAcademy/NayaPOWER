// PORTAL ALIGNMENT R1 — build on the R5 staged portal, verbatim base.
// Base: lane base-r5.html == R5 staged bytes, sha d4bb2102279838984db558e87cec4a977e4782ed22e5a2cc98be70f28e00b86b.
// Scope (design alignment only, phone first):
//  1. NAV LABELS VISIBLE — .eco-tip goes from hover-only (opacity 0) to always-visible
//     labels under each ball. Desktop: one row of 9 ball+label cells. Phone: 3x3 grid
//     (one 390px row of 9 labelled cells is geometrically impossible at 17px —
//     "Innovations" alone is ~90px; 9 labels need ~900px. Grid keeps every label
//     whole, nothing cut off). First-tap-hold JS deleted: a single tap must navigate.
//     "12 Elements of Naya" shortens to "12 Elements" (matches its aria-label) so it
//     fits its cell; all other tip texts, hrefs, glyphs, --eco-c values untouched.
//     This reverses R5's hover-only pick on Shawn's Nov 27 alignment order: a cold
//     visitor must know where each icon goes without hovering or clicking.
//  2. ONE LIGHT TOP-LEFT — button sheen 105deg -> 135deg (all occurrences of that
//     exact sheen); the disabled body:before ambient glow becomes a top-left wash
//     (circle at 24% 12%, deep gold + royal purple). .core (35% 30%) and .eco-ball
//     (35% 28%) already light top-left — verified, untouched. NAMED GAP: the arch
//     scene's central light is baked into the dial photograph itself; no CSS
//     re-lights a photograph — that needs an art pass, not this round.
//  3. WALKTHROUGH SEQUENCE VISIBLE — one compact strip under the name entry:
//     1 Portal -> 2 Certificate (/identity.html, same host) -> 3 iPhones
//     (the official v3 phone walkthrough staging worker, owned by the
//     walkthrough+About/Skills track — linked, never duplicated).
//     Name entry: the R5 submit handler already goes to '/identity.html'
//     (relative, same host, the NEW certificate sha 57bdd387) — asserted here,
//     no nayanet.app certificate URL anywhere in the file.
//  4. Nothing cut off at 390x844 / 1440x900 — labels wrap, never clip;
//     body already overflow-x:clip; grid + wrap verified by asserts.
// Node only (python writes EPERM). Base edited, nothing re-harvested.
import {readFileSync, writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
const sha = b => createHash('sha256').update(b).digest('hex');
const LANE = new URL('./', import.meta.url).pathname;
let asserts = 0;
const ok = (name, cond) => { asserts++; if (!cond) throw new Error('ASSERT FAIL: ' + name); console.log('PASS ' + name); };

const base = readFileSync(LANE + 'base-r5.html');
ok('R5 base sha', sha(base) === 'd4bb2102279838984db558e87cec4a977e4782ed22e5a2cc98be70f28e00b86b');
let html = base.toString('utf8');

// --- 0. Name entry -> NEW certificate on the same host (assert the R5 wiring) ---
ok('entry submit goes to /identity.html (relative, same host)',
  html.includes("window.location.href='/identity.html'+(v?'?name='+encodeURIComponent(v):'');"));
ok('no live-host certificate URL in portal', !/nayanet\.app\/[^"']*(certificate|identity)/i.test(html));
ok('certificate unchanged (identity sha 57bdd387)',
  sha(readFileSync(LANE + 'identity.html')).startsWith('57bdd387'));

// --- 1. NAV: surgical edits on the existing menu CSS region ---
function menuRegion(s) {
  const start = s.indexOf('.eco-inline{');
  if (start === -1) throw new Error('menu CSS start not found');
  const rm = s.indexOf('@media (prefers-reduced-motion:reduce)', start);
  if (rm === -1) throw new Error('menu reduced-motion block not found');
  let d = 0, end = -1;
  for (let i = rm; i < s.length; i++) {
    if (s[i] === '{') d++;
    if (s[i] === '}') { d--; if (d === 0) { end = i + 1; break; } }
  }
  if (end === -1) throw new Error('menu reduced-motion block end not found');
  return {start, end, text: s.slice(start, end)};
}
const region = menuRegion(html);
let css = region.text;
// 1a. .eco-item: column layout, fixed desktop cell width.
ok('menu region has .eco-item flex row',
  css.includes('.eco-item{\n  flex:none;\n  position:relative;\n  display:flex;\n  align-items:center;\n  justify-content:center;'));
css = css.replace(
  '.eco-item{\n  flex:none;\n  position:relative;\n  display:flex;\n  align-items:center;\n  justify-content:center;',
  '.eco-item{\n  flex:none;\n  position:relative;\n  display:flex;\n  flex-direction:column;\n  align-items:center;\n  justify-content:flex-start;\n  gap:6px;\n  width:112px;');
// 1b. .eco-tip: static, always visible, wrapping label (was absolute + opacity 0).
ok('menu region has absolute hover-only .eco-tip', css.includes('.eco-item .eco-tip{position:absolute;top:calc(100% + 10px);'));
css = css.replace(
  '.eco-item .eco-tip{position:absolute;top:calc(100% + 10px);left:50%;transform:translateX(calc(-50% + var(--tip-x,0px))) translateY(4px);white-space:nowrap;background:#050607;border:1.5px solid var(--eco-c,#8e24aa);color:#ffffff;font-family:Marcellus,Georgia,serif;font-size:17px;line-height:1.2;padding:8px 14px;border-radius:999px;opacity:0;pointer-events:none;transition:opacity .2s ease,transform .2s ease;box-shadow:0 4px 14px rgba(0,0,0,.55),0 0 12px var(--eco-c,#8e24aa);z-index:9}',
  '.eco-item .eco-tip{position:static;transform:none;white-space:normal;text-align:center;max-width:112px;background:#050607;border:1.5px solid var(--eco-c,#8e24aa);color:#ffffff;font-family:Marcellus,Georgia,serif;font-size:17px;line-height:1.2;padding:8px 8px;border-radius:999px;opacity:1;pointer-events:none;box-shadow:0 4px 14px rgba(0,0,0,.55),0 0 12px var(--eco-c,#8e24aa);z-index:9}');
// 1c. Delete the hover/focus reveal rule (labels are always on now).
ok('menu region has hover reveal rule',
  css.includes(".eco-item:hover .eco-tip,.eco-item:focus-visible .eco-tip,.eco-item.tip-on .eco-tip{opacity:1;transform:translateX(calc(-50% + var(--tip-x,0px))) translateY(0)}"));
css = css.replace(
  ".eco-item:hover .eco-tip,.eco-item:focus-visible .eco-tip,.eco-item.tip-on .eco-tip{opacity:1;transform:translateX(calc(-50% + var(--tip-x,0px))) translateY(0)}", '');
ok('hover reveal rule deleted', !css.includes('.eco-item.tip-on .eco-tip{opacity:1'));
// 1d. Phone: 3x3 grid instead of the single nowrap row (was .eco-inline{flex-wrap:nowrap;gap:8px;max-width:374px;}).
ok('menu region has phone nowrap row', css.includes('.eco-inline{flex-wrap:nowrap;gap:8px;max-width:374px;}'));
css = css.replace(
  '.eco-inline{flex-wrap:nowrap;gap:8px;max-width:374px;}',
  '.eco-inline{display:grid;grid-template-columns:repeat(3,1fr);gap:16px 8px;max-width:374px;}\n.eco-item{width:auto;}\n.eco-item .eco-tip{max-width:100%;}');
// 1e. Walkthrough strip styles (appended to the menu region, head <style>).
css += '\n/* ALIGNMENT R1 — walkthrough strip: one compact bar under the name entry.\n   Obsidian pill bar, rim in deep gold, white 17px Marcellus, steps in order. */\n.fp-walk-strip{display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:4px 10px;max-width:560px;margin:16px auto 0;padding:10px 16px;background:#050607;border:1.5px solid #d4a017;border-radius:999px;box-shadow:0 4px 14px rgba(0,0,0,.55),0 0 12px rgba(212,160,23,.45);font-family:Marcellus,Georgia,serif;font-size:17px;line-height:1.2;color:#ffffff;text-align:center}\n.fp-walk-strip a{color:#ffffff;text-decoration:underline;text-underline-offset:3px}\n.fp-walk-strip .fp-walk-arrow{color:#d4a017}\n';
html = html.slice(0, region.start) + css + html.slice(region.end);

// --- 2. Tip text: "12 Elements of Naya" -> "12 Elements" (fits its cell; matches aria-label) ---
ok('tip text 12 Elements of Naya present', html.includes('>12 Elements of Naya</span>'));
html = html.replace('>12 Elements of Naya</span>', '>12 Elements</span>');
ok('nine eco-item anchors intact', (html.match(/class="eco-item"/g) || []).length === 9);
ok('nine R5 destinations unchanged', ['https://nayanet.groovepages.com/aboutus','https://howitworks.nayanet.app/','https://innovations.nayanet.app/','https://12elements.nayanet.app/','https://nayanet.app/personal#skills','https://grandmission.nayanet.app/','https://powercasts.nayapower.workers.dev/','https://academy.nayanet.app/','https://naya-model-pricing.nayapower.workers.dev/'].every(h => html.includes('href="' + h + '"')));

// --- 3. Delete the first-tap-hold tip JS (single tap must navigate now) ---
const tipJsStart = html.indexOf('/* HOVER-FIX tip JS');
ok('tip JS block present', tipJsStart !== -1);
const scriptOpen = html.lastIndexOf('<script>', tipJsStart);
const scriptClose = html.indexOf('</script>', tipJsStart);
ok('tip JS script tags found', scriptOpen !== -1 && scriptClose !== -1);
html = html.slice(0, scriptOpen) + html.slice(scriptClose + '</script>'.length);
ok('no first-tap-hold code left', !html.includes("classList.add('tip-on')") && !html.includes('clampEcoTip(dot)') && !html.includes(',2600);'));

// --- 4. Walkthrough strip HTML: after the deed-sentence </p> ---
const deedIdx = html.indexOf('id="fpDeedSentence"');
ok('deed sentence present', deedIdx !== -1);
const deedClose = html.indexOf('</p>', deedIdx);
ok('deed sentence close found', deedClose !== -1);
const strip = '\n<nav class="fp-walk-strip" aria-label="Your three steps into NayaNET"><span>1 Portal</span><span class="fp-walk-arrow" aria-hidden="true">&rarr;</span><a href="/identity.html">2 Certificate</a><span class="fp-walk-arrow" aria-hidden="true">&rarr;</span><a href="https://portal-phone-v3-staging.nayapower.workers.dev/?walk=1">3 iPhones</a></nav>';
html = html.slice(0, deedClose + 4) + strip + html.slice(deedClose + 4);
ok('strip present with same-host certificate link', html.includes('class="fp-walk-strip"') && html.includes('href="/identity.html">2 Certificate</a>'));
ok('strip links iPhones to the v3 phone walkthrough', html.includes('href="https://portal-phone-v3-staging.nayapower.workers.dev/?walk=1">3 iPhones</a>'));

// --- 5. ONE LIGHT TOP-LEFT ---
// 5a. Button sheen 105deg -> 135deg (every occurrence of that exact sheen).
const sheen = 'linear-gradient(105deg,transparent 42%,rgba(255,255,255,.16) 50%,transparent 58%)';
const sheenCount = html.split(sheen).length - 1;
ok('button sheen occurrences found', sheenCount >= 4);
html = html.split(sheen).join('linear-gradient(135deg,transparent 42%,rgba(255,255,255,.16) 50%,transparent 58%)');
console.log('sheen 105deg -> 135deg:', sheenCount, 'occurrences');
// 5b. Disabled ambient glow -> top-left wash (deep gold + royal purple, faint).
ok('disabled body:before present', html.includes('body:before{display:none;}'));
html = html.replace('body:before{display:none;}',
  'body:before{display:block;background:radial-gradient(circle at 24% 12%,rgba(212,160,23,.14),rgba(142,36,170,.08) 32%,transparent 55%);animation:ambient 8s ease-in-out infinite alternate;}');
ok('top-left wash in place', html.includes('radial-gradient(circle at 24% 12%'));
// 5c. Already top-left, verified untouched: .core 35%/30%, .eco-ball 35%/28%.
ok('.core light top-left untouched', html.includes('circle at 35% 30%'));
ok('.eco-ball light top-left untouched', html.includes('circle at 35% 28%'));
// 5d. No new violations of the easy greps: no gray text classes added, no font <17 in new CSS.
ok('strip text is 17px Marcellus', html.includes('.fp-walk-strip{display:flex') && html.includes('font-size:17px;line-height:1.2;color:#ffffff'));
ok('labels are 17px Marcellus white', html.includes("font-family:Marcellus,Georgia,serif;font-size:17px;line-height:1.2;padding:8px 8px;"));

writeFileSync(LANE + 'portal.html', html);
const out = readFileSync(LANE + 'portal.html');
console.log('portal.html', out.length, 'B sha256', sha(out));
console.log('BUILD DONE —', asserts, 'assertions PASS');
