// Build the Black Diamond phone portal from the R5 base — surgical splice only.
// Reads portal-r5-base.html (byte-identical R5 copy, sha d4bb2102...), applies
// the phone transplant + walk-JS patches, writes portal.html. Node only.
// Every replacement is asserted exactly-once; a miss fails loudly, no write.
import {readFileSync, writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
const sha = b => createHash('sha256').update(b).digest('hex');
const LANE = new URL('./', import.meta.url).pathname;
const base = readFileSync(LANE + 'portal-r5-base.html');
console.log('base', base.length, 'B sha256', sha(base));
if (sha(base) !== 'd4bb2102279838984db558e87cec4a977e4782ed22e5a2cc98be70f28e00b86b') throw new Error('R5 base sha mismatch — refusing to build');
let s = base.toString('utf8');
const once = (name, from, to) => {
  const n = s.split(from).length - 1;
  if (n !== 1) throw new Error('PATCH ' + name + ': expected 1 occurrence, found ' + n);
  s = s.replace(from, to);
  console.log('patched', name);
};
// 1. Walk section -> phone markup (whole section, markers verified).
const secStart = '<section id="fpWalk" hidden>';
const secEnd = '</section>';
const a = s.indexOf(secStart);
const b = s.indexOf(secEnd, a);
if (a < 0 || b < 0) throw new Error('walk section not found');
const section = readFileSync(LANE + 'phone-section.html', 'utf8');
s = s.slice(0, a) + section + s.slice(b + secEnd.length);
console.log('patched section: walk -> Black Diamond phone');
// 2. Phone script BEFORE the harvested walk script (walk IIFE calls window.bdPhone).
const walkScriptAnchor = "<script>\n/* WHOLE-SYSTEM CONNECTION 2026-11-24 (items 65/67/68/72)";
once('phone-script-insert', walkScriptAnchor, readFileSync(LANE + 'phone-script.html', 'utf8') + '\n' + walkScriptAnchor);
// 3. Phone style BEFORE the walk script (after the walk <style>).
once('phone-style-insert', walkScriptAnchor, readFileSync(LANE + 'phone-style.html', 'utf8') + '\n' + walkScriptAnchor);
// 4. Walk JS: prepend country / province / city screens to QUESTIONS.
once('questions-prepend', 'var QUESTIONS = [',
  'var QUESTIONS = [{"key": "country", "q": "What country are you in?", "def": "", "ph": "e.g. Canada"}, {"key": "province", "q": "What province or state are you in?", "def": "", "ph": "e.g. Ontario"}, {"key": "city", "q": "What city are you in?", "def": "", "ph": "e.g. Toronto"}, ');
// 5. render(): placeholder from q.ph (was: Enter-button label swap — the ball has no label to swap).
once('render-placeholder',
  "enterBtn.textContent = idx === QUESTIONS.length - 1 ? 'Finish \\u25C6' : 'Enter';",
  "ansEl.placeholder = q.ph || '';");
// 6. render(): reset to input mode after focus.
once('render-showInput', 'ansEl.focus();',
  "ansEl.focus();\n    if (window.bdPhone) window.bdPhone.showInput();");
// 7. Ball IS Enter: reveal in place, never navigate.
once('ball-reveal',
  "enterBtn.addEventListener('click', function(){\n    S.answers[QUESTIONS[idx].key] = ansEl.value;\n    save();\n    if (idx < QUESTIONS.length - 1) { idx++; render(); return; }\n    complete();\n  });",
  "enterBtn.addEventListener('click', function(){\n    if (!endEl.hidden) return; /* the ball is Enter: it reveals, it never navigates */\n    var q = QUESTIONS[idx];\n    S.answers[q.key] = ansEl.value;\n    save();\n    if (window.bdPhone) window.bdPhone.reveal(q.q, ansEl.value, q.def);\n  });");
// 8. Next arrow moves forward (or completes on the last screen).
once('next-arrow',
  "backBtn.addEventListener('click', function(){\n    if (idx > 0) { idx--; render(); }\n  });",
  "backBtn.addEventListener('click', function(){\n    if (idx > 0) { idx--; render(); }\n  });\n  var nextBtn = document.getElementById('fpWalkNext');\n  if (nextBtn) nextBtn.addEventListener('click', function(){\n    if (idx < QUESTIONS.length - 1) { idx++; render(); return; }\n    complete();\n  });");
// 9. finish(): hide the phone nav + input/reveal, show the end screen inside the phone.
once('finish-showEnd',
  "document.querySelector('.fp-walk-hint').hidden = true;\n      endEl.hidden = false;",
  "document.querySelector('.fp-walk-hint').hidden = true;\n      endEl.hidden = false;\n      if (window.bdPhone) window.bdPhone.showEnd();");
// ---- assertions on the built file (R5 keepers + phone markers) ----
const assert = (name, ok) => { console.log((ok ? 'PASS ' : 'FAIL ') + name); if (!ok) process.exitCode = 1; };
assert('phone present (bd-phone, bd-ball, fpWalkNext)', s.includes('class="bd-phone"') && s.includes('bd-ball') && s.includes('id="fpWalkNext"'));
assert('no separate Enter button (ball is the only Enter)', !s.includes('>Enter</button>') && s.includes('id="fpWalkEnter"'));
assert('no Finish label swap left', !s.includes("enterBtn.textContent"));
assert('18 screens: 3 location + 15 harvested', s.includes('"key": "country"') && s.includes('"key": "province"') && s.includes('"key": "city"') && s.includes('"key": "motto"') && s.includes('"key": "start"'));
assert('live clock + battery present', s.includes('id="bdClock"') && s.includes('id="bdBattFill"'));
assert('copy-out on review screen', s.includes('id="fpWalkCopyAll"'));
assert('8 style elements (7 R5 + 1 phone)', (s.match(/<style>/g) || []).length === 8);
assert('10 script elements (9 R5 + 1 phone)', (s.match(/<script/g) || []).length === 10);
assert('R5: hover-only menu intact', s.includes('.eco-item .eco-tip{') && !s.includes('eco-label'));
assert('R5: ring intact (nayaSpectrum 78s)', s.includes('animation:nayaSpectrum 78s linear infinite'));
assert('R5: story intact, 27 slides', s.includes('id="fpStory"') && s.includes('FP_SLIDES'));
assert('R5: nine eco-item destinations intact', (s.match(/class="eco-item"/g) || []).length === 9);
assert('R5: walk gating intact (?walk=1)', s.includes("params.get('walk') !== '1'"));
assert('R5: complete() verify-before-declare intact', s.includes("api/welcome/complete") && s.includes("api/welcome/me"));
assert('R5: certificate link intact', s.includes('identity.html'));
assert('walk=1 scroll-into-view intact', s.includes('walk.scrollIntoView'));
const out = Buffer.from(s, 'utf8');
writeFileSync(LANE + 'portal.html', out);
console.log('portal.html', out.length, 'B sha256', sha(out), '(base +', out.length - base.length, 'B)');
console.log('BUILD DONE');
