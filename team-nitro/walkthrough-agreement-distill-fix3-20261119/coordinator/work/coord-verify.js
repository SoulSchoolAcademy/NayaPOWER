// COORDINATOR verification — Agreement distill fix-3 (independent of the maker).
// My own scenarios, my own assertions, run against the DISK files (verified
// byte-identical to the filed blobs) and against the BASE bytes as a control.
// Uses the fix-1 checker's DOM engine (dom-harness3-dom.js) only as the engine;
// every scenario and assertion below is mine.
// Usage: node coord-verify.js  (exit 0 = all pass)
var fs = require('fs');
var path = require('path');
var H = require('/home/hatch/workspace/team-nitro/walkthrough-agreement-distill-fix3-20261119/maker/work/dom-harness3-dom.js');
var makeEnv = H.makeEnv, q = H.q, qa = H.qa, sleep = H.sleep;

var DIR = '/home/hatch/workspace/team-nitro';
var WKDIR = '/home/hatch/workspace/team-nitro/walkthrough-agreement-distill-fix3-20261119/coordinator/work';
var FIXED = {
  walk: fs.readFileSync(path.join(DIR, 'walk-v23-assembly-20261114/walk-beginning-fixed.html'), 'utf8'),
  identity: fs.readFileSync(path.join(DIR, 'walk-v23-assembly-20261114/identity-fixed.html'), 'utf8')
};
var BASE = {
  walk: fs.readFileSync(path.join(WKDIR, 'walk-base.html'), 'utf8'),
  identity: fs.readFileSync(path.join(WKDIR, 'identity-base.html'), 'utf8')
};

var pass = 0, fail = 0, failures = [];
function check(name, ok, detail) {
  if (ok) { pass++; console.log('  PASS ' + name); }
  else { fail++; failures.push(name); console.log('  FAIL ' + name + (detail ? ' — ' + detail : '')); }
}
function visibleSteps(doc) {
  return qa(doc, '[id^="step-"]').filter(function (el) { return !el.hidden; }).map(function (el) { return el.id; });
}
function identityParts(doc) {
  return {
    input: q(doc, '#aliasInput') || q(doc, 'input[placeholder*="lias"]'),
    nameEl: q(doc, '#displayName')
  };
}

async function main() {
  console.log('== C1: FIXED identity, paired ?name=Distill Eye Walk&alias=Distill ==');
  var e = makeEnv(FIXED.identity, '?name=Distill%20Eye%20Walk&alias=Distill');
  var doc = e.document;
  await sleep(50);
  var p = identityParts(doc);
  check('C1 input exists', !!p.input);
  if (p.input) check('C1 input holds paired alias (lowercased)', p.input.value === 'distill', 'value=' + JSON.stringify(p.input.value));
  check('C1 name line exists', !!p.nameEl);
  if (p.nameEl) {
    check('C1 hero text is the passed name', p.nameEl.textContent === 'Distill Eye Walk', 'text=' + JSON.stringify(p.nameEl.textContent));
    check('C1 hero data-text set', p.nameEl.getAttribute('data-text') === 'Distill Eye Walk', 'data-text=' + JSON.stringify(p.nameEl.getAttribute('data-text')));
    check('C1 hero unhidden', p.nameEl.hidden === false, 'hidden=' + p.nameEl.hidden);
  }
  check('C1 no script errors', e.errors.length === 0, e.errors.length + ' errors: ' + JSON.stringify(e.errors.slice(0, 2)));
  await sleep(2000);
  if (p.nameEl) check('C1 hero still painted after 2s', p.nameEl.textContent === 'Distill Eye Walk', 'text=' + JSON.stringify(p.nameEl.textContent));

  console.log('== C2: FIXED identity, name-only (unpaired — FIX3 never-pre-paint stands) ==');
  var e2 = makeEnv(FIXED.identity, '?name=Distill%20Eye%20Walk');
  var doc2 = e2.document;
  await sleep(50);
  var p2 = identityParts(doc2);
  if (p2.input) check('C2 input stays empty', p2.input.value === '', 'value=' + JSON.stringify(p2.input.value));
  if (p2.nameEl) {
    check('C2 hero stays blank', p2.nameEl.textContent === '', 'text=' + JSON.stringify(p2.nameEl.textContent));
    check('C2 hero stays hidden', p2.nameEl.hidden === true, 'hidden=' + p2.nameEl.hidden);
    check('C2 hero data-text unset', p2.nameEl.getAttribute('data-text') === null, 'data-text=' + JSON.stringify(p2.nameEl.getAttribute('data-text')));
  }
  check('C2 no script errors', e2.errors.length === 0, e2.errors.length + ' errors');

  console.log('== C3: FIXED walk door, paired — holds 5s, continue opens the walk ==');
  var e3 = makeEnv(FIXED.walk, '?name=Distill%20Eye%20Walk&alias=Distill');
  var doc3 = e3.document;
  await sleep(50);
  var door = q(doc3, '#step-door');
  check('C3 door exists', !!door);
  if (door) check('C3 door visible at boot', door.hidden === false, 'hidden=' + door.hidden);
  var before = visibleSteps(doc3);
  check('C3 only the door visible at boot', JSON.stringify(before) === JSON.stringify(['step-door']), 'visible=' + JSON.stringify(before));
  await sleep(5000);
  var after = visibleSteps(doc3);
  check('C3 door still the only visible step after 5s', JSON.stringify(after) === JSON.stringify(['step-door']), 'visible=' + JSON.stringify(after));
  var cont = q(doc3, '#doorContinue');
  check('C3 continue button exists', !!cont);
  if (cont) {
    check('C3 continue visible for certified citizen', cont.hidden === false, 'hidden=' + cont.hidden);
    check('C3 continue reads Continue to the walk', cont.textContent.indexOf('Continue to the walk') !== -1, JSON.stringify(cont.textContent));
    cont.click();
    await sleep(50);
    var afterClick = visibleSteps(doc3);
    check('C3 tap Continue: door gone, step-1 open', afterClick.indexOf('step-door') === -1 && afterClick.indexOf('step-1') !== -1, 'visible=' + JSON.stringify(afterClick));
  }
  check('C3 no script errors', e3.errors.length === 0, e3.errors.length + ' errors');

  console.log('== C4: FIXED walk door, no alias — continue hidden, cert link is the way ==');
  var e4 = makeEnv(FIXED.walk, '');
  var doc4 = e4.document;
  await sleep(50);
  var cont4 = q(doc4, '#doorContinue');
  check('C4 continue exists in markup', !!cont4);
  if (cont4) check('C4 continue hidden without alias', cont4.hidden === true, 'hidden=' + cont4.hidden);
  var link4 = q(doc4, '#step-door a[href*="/identity.html"]');
  check('C4 certificate link exists', !!link4);
  check('C4 no script errors', e4.errors.length === 0, e4.errors.length + ' errors');

  console.log('== C5: FIXED walk door, cert link navigates with name+alias (my own case) ==');
  var e5 = makeEnv(FIXED.walk, '?name=Distill%20Eye%20Walk&alias=Distill');
  var doc5 = e5.document;
  await sleep(50);
  var link5 = q(doc5, '#step-door a[href*="/identity.html"]');
  check('C5 cert link exists', !!link5);
  if (link5) {
    var href5 = link5.getAttribute('href');
    check('C5 cert link carries name+alias', href5.indexOf('name=Distill') !== -1 && href5.indexOf('alias=Distill') !== -1, 'href=' + JSON.stringify(href5));
    link5.click();
    await sleep(50);
    var navs = e5.navigations.filter(function (n) { return n.kind === 'href'; });
    check('C5 tapping cert link navigates to identity with the pair', navs.length >= 1 && navs[navs.length - 1].url.indexOf('/identity.html?name=Distill') === 0, JSON.stringify(navs));
    var stillDoor = visibleSteps(doc5);
    check('C5 door still visible after link tap (no auto-advance meanwhile)', stillDoor.indexOf('step-door') !== -1, 'visible=' + JSON.stringify(stillDoor));
  }
  check('C5 no script errors', e5.errors.length === 0, e5.errors.length + ' errors');

  console.log('== C6: CONTROL — BASE bytes must still fail all three (non-vacuity) ==');
  var b1 = makeEnv(BASE.identity, '?name=Distill%20Eye%20Walk&alias=Distill');
  await sleep(50);
  var bp = identityParts(b1.document);
  check('C6 base identity input is empty (the bug)', bp.input && bp.input.value === '', 'value=' + JSON.stringify(bp.input && bp.input.value));
  check('C6 base identity hero is blank+hidden (the bug)', bp.nameEl && bp.nameEl.textContent === '' && bp.nameEl.hidden === true, 'text=' + JSON.stringify(bp.nameEl && bp.nameEl.textContent) + ' hidden=' + (bp.nameEl && bp.nameEl.hidden));
  var b3 = makeEnv(BASE.walk, '?name=Distill%20Eye%20Walk&alias=Distill');
  await sleep(5000);
  var bAfter = visibleSteps(b3.document);
  check('C6 base walk auto-advances within 5s (the bug)', bAfter.indexOf('step-1') !== -1, 'visible=' + JSON.stringify(bAfter));

  console.log('\nCOORDINATOR-VERIFY: ' + pass + ' pass / ' + fail + ' fail');
  if (fail) { console.log('FAILURES: ' + failures.join(' | ')); process.exit(1); }
  process.exit(0);
}
main().catch(function (e) { console.error('FATAL', e); process.exit(2); });
