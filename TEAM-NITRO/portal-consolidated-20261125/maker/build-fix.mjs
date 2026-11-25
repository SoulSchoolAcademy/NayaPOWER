// PORTAL CONSOLIDATED — FIX ROUND 2026-11-25 (checker GOES BACK, 2 defects).
// Phase "identity": patch identity.html (the claim) — run BEFORE
// build-consolidated.mjs, which regenerates identity-consolidated.html.
// Phase "portal": patch portal.html (the walk complete + end screen) — run
// AFTER build-consolidated.mjs, which regenerates portal.html.
// Node only. Every replacement is asserted exactly-once; any miss fails loudly.
import {readFileSync, writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
const sha = b => createHash('sha256').update(b).digest('hex');
const LANE = new URL('./', import.meta.url).pathname;
const phase = process.argv[2];
const assert = (c, m) => { if (!c) { console.error('ASSERT FAIL:', m); process.exit(1); } };
const count = (s, sub) => s.split(sub).length - 1;
const rep = (s, oldS, newS, m) => { assert(count(s, oldS) === 1, m + ' (found ' + count(s, oldS) + ')'); return s.replace(oldS, newS); };

if (phase === 'identity') {
  let ident = readFileSync(LANE + 'identity.html', 'utf8');

  // I1 — the claim comment: fire-and-forget is gone; verify before proceed.
  ident = rep(ident,
    "Fire-and-verify:\n         the network never blocks a device-local identity — except\n         when the alias is already claimed by ANOTHER device. */",
    "Verify-before-proceed (fix 2026-11-25): only a registry answer of\n         200/201 — or a 409 the same device can re-prove — counts as\n         claimed. ANY other outcome (network error, timeout, other status,\n         empty 409 read-back) is 'unconfirmed': the page says so plainly\n         and offers retry, and never sails into the walk on an\n         unconfirmed claim. */",
    'I1 claim comment');

  // I2 — 409 read-back with no rows is unconfirmed, not ok.
  ident = rep(ident,
    "                if (rows && rows.length && rows[0].device_key !== deviceKey) return { status: 'taken', createdAt: null };",
    "                if (!rows || !rows.length) return { status: 'unconfirmed', createdAt: null };\n                if (rows[0].device_key !== deviceKey) return { status: 'taken', createdAt: null };",
    'I2 409 empty read-back');

  // I3 — 409 inner catch: silent ok -> unconfirmed (14-space indent, unique).
  ident = rep(ident,
    "              .catch(function () { return { status: 'ok', createdAt: null }; });",
    "              .catch(function () { return { status: 'unconfirmed', createdAt: null }; });",
    'I3 409 inner catch');

  // I4 — non-200/201/409 fallthrough: silent ok -> unconfirmed.
  ident = rep(ident,
    "          return { status: 'ok', createdAt: null };",
    "          return { status: 'unconfirmed', createdAt: null };",
    'I4 fallthrough status');

  // I5 — outer network catch: silent ok -> unconfirmed (8-space indent, unique).
  ident = rep(ident,
    "        }).catch(function () { return { status: 'ok', createdAt: null }; });",
    "        }).catch(function () { return { status: 'unconfirmed', createdAt: null }; });",
    'I5 outer catch');

  // I6 — the 2.5 s timeout race: resolving 'ok' was the silence. Unconfirmed now.
  ident = rep(ident,
    "          setTimeout(function () { resolve({ status: 'ok', createdAt: null }); }, 2500);",
    "          setTimeout(function () { resolve({ status: 'unconfirmed', createdAt: null }); }, 2500);",
    'I6 timeout race');

  // I7 — named result handler + the unconfirmed branch (plain words + retry).
  // The 200/201 row IS the registry confirmation: the POST returns the row
  // (return=representation), so 'ok' still means the claim landed.
  ident = rep(ident,
    "      claimAlias().then(function (result) {\n        var status = (result && typeof result === 'object') ? result.status : result;",
    "      /* FIX 2026-11-25 — the claim result handler. 'unconfirmed' means\n         the registry never answered that the claim landed: say so in plain\n         words, offer retry, and do NOT proceed into the walk. */\n      function onClaimResult(result) {\n        var status = (result && typeof result === 'object') ? result.status : result;\n        if (status === 'unconfirmed') {\n          var noteU = document.getElementById('hubNote');\n          if (_hubNoteHTML === null) _hubNoteHTML = noteU.innerHTML;\n          noteU.textContent = 'We couldn\\u2019t certify your name just now \\u2014 the connection dropped. Nothing is lost: your name is saved on this device. Please try again.';\n          noteU.hidden = false;\n          noteU.appendChild(document.createElement('br'));\n          var _try = document.createElement('button');\n          _try.id = 'fpClaimRetry'; _try.type = 'button';\n          _try.className = 'fp-this-is-me';\n          _try.textContent = 'Try again \\u2192';\n          _try.addEventListener('click', function(){\n            try { noteU.innerHTML = _hubNoteHTML; noteU.classList.remove('fp-taken-green'); } catch(e){}\n            noteU.hidden = true;\n            claimAlias().then(onClaimResult);\n          });\n          noteU.appendChild(_try);\n          _unclaim();\n          try { noteU.scrollIntoView({block:'center'}); } catch(e){}\n          return;\n        }",
    'I7 unconfirmed branch');

  // I8 — close the named handler and call it.
  ident = rep(ident,
    "        setTimeout(function(){ window.location.href = walkthroughEntryUrl(rawName || prettyName(finalAlias), finalAlias); }, 800);\n      });\n    };",
    "        setTimeout(function(){ window.location.href = walkthroughEntryUrl(rawName || prettyName(finalAlias), finalAlias); }, 800);\n      }\n      claimAlias().then(onClaimResult);\n    };",
    'I8 handler close');

  writeFileSync(LANE + 'identity.html', ident);
  const b = Buffer.from(ident);
  console.log('identity.html', b.length, 'B sha256', sha(b));
  assert(count(ident, "status: 'unconfirmed'") === 5, 'I: five unconfirmed resolutions');
  assert(count(ident, "status: 'ok'") === 3, 'I: three ok resolutions left (201 row, 201 parse, 409 same-device)');
  assert(ident.includes('fpClaimRetry') && ident.includes('onClaimResult'), 'I: retry handler present');
  console.log('IDENTITY PHASE PASS');
}

if (phase === 'portal') {
  let portal = readFileSync(LANE + 'portal.html', 'utf8');

  // P1 — end-screen markup: id the ready line + link row, add the fail line.
  portal = rep(portal,
    "      <p class=\"fp-walk-linkrow\"><span class=\"fp-walk-link\" id=\"fpWalkLink\"></span> <button class=\"fp-walk-copy\" id=\"fpWalkCopy\" type=\"button\">Copy</button></p>\n      <p class=\"fp-walk-endline\">Your answers are saved on this device. Your world is ready &mdash; go see it, then choose your plan.</p>",
    "      <p class=\"fp-walk-linkrow\" id=\"fpWalkLinkRow\"><span class=\"fp-walk-link\" id=\"fpWalkLink\"></span> <button class=\"fp-walk-copy\" id=\"fpWalkCopy\" type=\"button\">Copy</button></p>\n      <p class=\"fp-walk-endline\" id=\"fpWalkReadyLine\">Your answers are saved on this device. Your world is ready &mdash; go see it, then choose your plan.</p>\n      <p class=\"fp-walk-endline\" id=\"fpWalkFailLine\" hidden></p>",
    'P1 end lines');

  // P2 — retry button row after the world/pricing row.
  portal = rep(portal,
    "      <div class=\"fp-walk-nav\">\n        <button class=\"fp-walk-enter\" id=\"fpWalkWorld\" type=\"button\">See my world &rarr;</button>\n        <button class=\"fp-walk-navbtn\" id=\"fpWalkPricing\" type=\"button\">Choose your plan &rarr;</button>\n      </div>",
    "      <div class=\"fp-walk-nav\">\n        <button class=\"fp-walk-enter\" id=\"fpWalkWorld\" type=\"button\">See my world &rarr;</button>\n        <button class=\"fp-walk-navbtn\" id=\"fpWalkPricing\" type=\"button\">Choose your plan &rarr;</button>\n      </div>\n      <div class=\"fp-walk-nav\">\n        <button class=\"fp-walk-enter\" id=\"fpWalkRetry\" type=\"button\" hidden>Try again &rarr;</button>\n      </div>",
    'P2 retry row');

  // P3 — CSS: the [hidden] attribute lost to display:block (the Skip-on-end-screen
  // bug), and the two-button rows overflowed 390 px. Wrap the rows; honour hidden.
  portal = rep(portal,
    ".fp-walk-nav{display:flex;align-items:center;justify-content:center;gap:14px;margin-top:6px}",
    ".fp-walk-nav{display:flex;align-items:center;justify-content:center;gap:14px;margin-top:6px;flex-wrap:wrap}",
    'P3 nav wrap');
  portal = rep(portal,
    ".fp-walk-enter{display:block;min-width:179px;height:48px;padding:0 24px;white-space:nowrap;border-radius:30px;border:1.5px solid rgba(47,232,158,.65);color:#fff;background:radial-gradient(circle at 50% 0%,#0b2e21,#05060a);font:inherit;font-size:17px;font-weight:800;cursor:pointer}",
    ".fp-walk-enter{display:block;min-width:179px;height:48px;padding:0 24px;white-space:nowrap;border-radius:30px;border:1.5px solid rgba(47,232,158,.65);color:#fff;background:radial-gradient(circle at 50% 0%,#0b2e21,#05060a);font:inherit;font-size:17px;font-weight:800;cursor:pointer}\n.fp-walk-enter[hidden]{display:none!important}\n.fp-walk-skip[hidden]{display:none!important}\n.fp-walk-enter{max-width:100%;box-sizing:border-box}\n.fp-walk-navbtn{max-width:100%;box-sizing:border-box}",
    'P3 hidden + fit');

  // P4 — the walk header comment: best-effort is gone.
  portal = rep(portal,
    "   State key + shape identical to the live walk: naya_welcome_right_v1\n   {alias, answers, topics, reveal}. The complete POST is best-effort and\n   never blocks: the end renders locally regardless. */",
    "   State key + shape identical to the live walk: naya_welcome_right_v1\n   {alias, answers, topics, reveal}. Verify-before-declare (fix 2026-11-25):\n   complete() must succeed AND the created world must answer 200 before\n   the end screen says \"Your world is ready\" or shows the \"See my world\"\n   door. On any failure the end screen says so plainly (\"your world isn't\n   ready yet\"), hides the world door and the Smart Link row, and offers\n   retry. The end line also says plainly how many of the 15 were answered. */",
    'P4 header comment');

  // P5 — complete(): verify before declaring. Replace the whole function.
  const start = portal.indexOf('  function complete(){');
  const endMark = "  document.getElementById('fpWalkCopy').addEventListener('click', function(){";
  const end = portal.indexOf(endMark);
  assert(start !== -1 && end !== -1 && end > start, 'P5 complete() bounds');
  const oldFn = portal.slice(start, end);
  assert(oldFn.includes('var to = setTimeout(finish, 3000);'), 'P5 old 3s fallback present');
  assert(count(oldFn, 'finish()') === 4, 'P5 old finish calls (def + 3)');
  const newFn = `  function complete(){
    /* FIX 2026-11-25 — verify before declaring: the 3 s "finish anyway"
       fallback is gone. complete() must return ok, and the world it just
       created must answer 200, before the end screen claims readiness. */
    var done = false;
    function finish(state){
      if (done) return; done = true;
      try {
        if (pname) localStorage.setItem('nayanet_smart_name', pname);
        if (S.alias) localStorage.setItem('nayanet_smart_alias', S.alias);
      } catch(e){}
      var a = S.alias || 'yourname';
      var link = (S.reveal && S.reveal.ambassador_link) || ('https://nayanet.app/joinus?ref=' + a);
      document.getElementById('fpWalkLink').textContent = a + '.nayanet.app';
      document.getElementById('fpWalkLink').setAttribute('data-real', link);
      var answered = 0;
      QUESTIONS.forEach(function(q){ if (S.answers && S.answers[q.key]) answered++; });
      var readyLine = document.getElementById('fpWalkReadyLine');
      var failLine = document.getElementById('fpWalkFailLine');
      var retryBtn = document.getElementById('fpWalkRetry');
      var worldBtn = document.getElementById('fpWalkWorld');
      var linkRow = document.getElementById('fpWalkLinkRow');
      if (state === 'ready') {
        qEl.textContent = 'Welcome home.';
        progEl.textContent = 'Welcome complete';
        readyLine.textContent = 'Your answers are saved on this device \\u2014 ' + answered + ' of ' + QUESTIONS.length + ' questions answered. Your world is ready \\u2014 go see it, then choose your plan.';
        readyLine.hidden = false;
        failLine.hidden = true;
        retryBtn.hidden = true;
        worldBtn.hidden = false;
        linkRow.hidden = false;
      } else {
        qEl.textContent = 'Almost there.';
        progEl.textContent = 'Your world is not ready yet';
        readyLine.hidden = true;
        failLine.textContent = 'Your answers are saved on this device \\u2014 ' + answered + ' of ' + QUESTIONS.length + ' questions answered \\u2014 but your world isn\\u2019t ready yet. The connection dropped before we could finish it. Tap Try again and we\\u2019ll finish it now.';
        failLine.hidden = false;
        retryBtn.hidden = false;
        worldBtn.hidden = true;
        linkRow.hidden = true;
      }
      ansEl.hidden = true;
      backBtn.hidden = true;
      enterBtn.hidden = true;
      skipBtn.hidden = true;
      document.querySelector('.fp-walk-hint').hidden = true;
      endEl.hidden = false;
      try { walk.scrollIntoView({block:'start'}); } catch(e){}
    }
    function verifyWorld(){
      /* The world page (/world/<alias>) is a navigation, not a CORS API —
         a cross-origin fetch of it is blocked by the walk worker. The
         registry read /api/welcome/me serves CORS and reports has_world:
         that is the proof the world exists. */
      return fetch('https://naya-walkthrough-15-staging.nayapower.workers.dev/api/welcome/me', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({alias: S.alias, name: pname})})
        .then(function(r){ return r.ok ? r.json() : null; })
        .then(function(d){ return !!(d && d.has_world === true); })
        .catch(function(){ return false; });
    }
    function run(){
      done = false;
      var timer = new Promise(function(resolve){ setTimeout(function(){ resolve({failed:true}); }, 10000); });
      var post = fetch('https://naya-walkthrough-15-staging.nayapower.workers.dev/api/welcome/complete', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({alias: S.alias, name: pname, answers: S.answers, topics: S.topics})})
        .then(function(r){ return r.ok ? r.json().then(function(d){ return {failed:false, reveal:d}; }).catch(function(){ return {failed:false, reveal:null}; }) : {failed:true}; })
        .then(function(out){
          if (out.failed) return out;
          if (out.reveal) { S.reveal = out.reveal; save(); }
          return verifyWorld().then(function(worldOk){ return {failed: !worldOk}; });
        })
        .catch(function(){ return {failed:true}; });
      Promise.race([post, timer]).then(function(out){ finish(out && out.failed ? 'failed' : 'ready'); });
    }
    try { run(); } catch(e){ finish('failed'); }
  }
  document.getElementById('fpWalkRetry').addEventListener('click', function(){ complete(); });
`;
  portal = portal.slice(0, start) + newFn + portal.slice(end);

  writeFileSync(LANE + 'portal.html', portal);
  const b = Buffer.from(portal);
  console.log('portal.html', b.length, 'B sha256', sha(b));
  assert(!portal.includes('var to = setTimeout(finish, 3000);'), 'P5 old fallback gone');
  assert(portal.includes("finish(out && out.failed ? 'failed' : 'ready')"), 'P5 race verdict present');
  assert(portal.includes('verifyWorld'), 'P5 world verify present');
  assert(portal.includes('fpWalkRetry') && portal.includes('fpWalkFailLine'), 'P5 retry + fail line present');
  assert(count(portal, '"key": "') === 15, 'P5 still 15 questions');
  console.log('PORTAL PHASE PASS');
}

if (phase !== 'identity' && phase !== 'portal') {
  console.error('usage: node build-fix.mjs <identity|portal>');
  process.exit(1);
}
