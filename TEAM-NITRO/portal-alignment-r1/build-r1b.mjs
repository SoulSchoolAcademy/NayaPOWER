// ALIGNMENT R1b — fix the phone strip clipping found by my own eye on the
// R1 probe screenshot (r1-phone-front.png): the strip sat INSIDE the circular
// .core, where the circle's chord at that height is only ~182px, so it wrapped
// to 3 lines and the dial's bottom edge sliced through "2 Certificate" /
// "3 iPhones". Fix: move the strip OUT of .core to the bottom of the stage
// (a direct child of <section class="stage">, absolute, centred, one line),
// where the full 390px width is available. Desktop: one line on the floor
// below the dial. Nothing else changes.
import {readFileSync, writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
const sha = b => createHash('sha256').update(b).digest('hex');
const LANE = new URL('./', import.meta.url).pathname;
let asserts = 0;
const ok = (name, cond) => { asserts++; if (!cond) throw new Error('ASSERT FAIL: ' + name); console.log('PASS ' + name); };

const base = readFileSync(LANE + 'portal.html');
ok('R1 portal sha', sha(base) === '802c3dd226ffb4cc4429db35852acb79838a04c422415b0d0b0cee88b4925e43');
let html = base.toString('utf8');

const strip = '\n<nav class="fp-walk-strip" aria-label="Your three steps into NayaNET"><span>1 Portal</span><span class="fp-walk-arrow" aria-hidden="true">&rarr;</span><a href="/identity.html">2 Certificate</a><span class="fp-walk-arrow" aria-hidden="true">&rarr;</span><a href="https://portal-phone-v3-staging.nayapower.workers.dev/?walk=1">3 iPhones</a></nav>';
ok('strip present inside .core', html.includes(strip));
html = html.replace(strip, '');
ok('strip removed from .core', !html.includes('class="fp-walk-strip" aria-label'));

// Insert as a direct child of <section class="stage">, before its close.
// The stage contains no nested <section>, so its first </section> closes it.
const stageIdx = html.indexOf('<section class="stage">');
ok('stage section found', stageIdx !== -1);
const stageClose = html.indexOf('</section>', stageIdx);
ok('stage close found', stageClose !== -1);
html = html.slice(0, stageClose) + strip + '\n  ' + html.slice(stageClose);
ok('strip now a stage child', html.indexOf('class="fp-walk-strip"') > stageIdx && html.indexOf('class="fp-walk-strip"') < html.indexOf('</section>', stageIdx));

// CSS: absolute, centred, bottom of the stage, one line, capped to viewport.
const oldCss = '.fp-walk-strip{display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:4px 10px;max-width:560px;margin:16px auto 0;padding:10px 16px;';
ok('strip CSS present', html.includes(oldCss));
html = html.replace(oldCss,
  '.fp-walk-strip{position:absolute;left:50%;transform:translateX(-50%);bottom:8px;z-index:5;display:flex;flex-wrap:nowrap;align-items:center;justify-content:center;gap:4px 10px;max-width:calc(100vw - 16px);white-space:nowrap;margin:0;padding:10px 16px;');
ok('strip CSS absolute bottom one-line', html.includes('position:absolute;left:50%;transform:translateX(-50%);bottom:8px;') && html.includes('flex-wrap:nowrap'));

// Keepers re-asserted.
ok('nine eco-item anchors intact', (html.match(/class="eco-item"/g) || []).length === 9);
ok('labels still always visible', html.includes('.eco-item .eco-tip{position:static') && html.includes('opacity:1;'));
ok('phone grid still 3x3', html.includes('grid-template-columns:repeat(3,1fr)'));
ok('name entry still -> /identity.html', html.includes("window.location.href='/identity.html'"));
ok('sheen still 135deg', !html.includes('linear-gradient(105deg,transparent 42%'));
ok('top-left wash still in place', html.includes('radial-gradient(circle at 24% 12%'));

writeFileSync(LANE + 'portal.html', html);
const out = readFileSync(LANE + 'portal.html');
console.log('portal.html', out.length, 'B sha256', sha(out));
console.log('BUILD R1b DONE —', asserts, 'assertions PASS');
