// transform-fix.js — agreement-distill FIX (2026-11-19, eye GOES BACK).
// Reads the distill outputs (transform-distill.js --emit unfold|welcome),
// applies the seven-fail fixes as COUNTED string replacements, and prints
// JSON {unfold_b64, welcome_b64} to stdout. Every replacement asserts its
// expected count; any miss throws and nothing is emitted. No disk writes.
// Usage: node transform-fix.js
var cp = require('child_process');
var path = require('path');
var t = path.join(__dirname, 'transform-distill.js');

function emit(mode) {
  var r = cp.spawnSync(process.execPath, [t, '--emit', mode], { encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 });
  if (r.status !== 0) throw new Error('transform --emit ' + mode + ' failed: ' + r.stderr);
  return r.stdout;
}

function rep(s, needle, replacement, expect, label) {
  var n = s.split(needle).length - 1;
  if (n !== expect) throw new Error('FIX-FAIL ' + label + ': expected ' + expect + ' found ' + n + ' :: ' + JSON.stringify(needle.slice(0, 100)));
  return s.split(needle).join(replacement);
}

function repRe(s, re, replacement, expect, label) {
  var m = s.match(re);
  var n = m ? m.length : 0;
  if (n !== expect) throw new Error('FIX-FAIL ' + label + ': expected ' + expect + ' found ' + n + ' :: ' + re);
  return s.replace(re, replacement);
}

// ---- shared board text (fails 3, 7) — identical strings in both files ----
function fixBoardText(s, file) {
  var u = file === 'unfold' ? 1 : 2; // unfold: 1 article; welcome: deck + letter
  s = rep(s, ' \u2014 and 99 out of 100 people fail on it.</p>', '.</p>', u, file + ' B1 99/100');
  s = rep(s, 'she\u2019s a Bugatti on a supercomputer.', 'she\u2019s a Bugatti on a superhighway.', u, file + ' B11 superhighway');
  s = rep(s, 'The work, done for you. And you\u2019re hired.', 'The work, done for you.', u, file + ' B15 title');
  s = rep(s, 'Why does it matter? Because the work gets done for you \u2014 and you\u2019re hired.', 'Why does it matter? Because the work gets done for you.', u, file + ' B15 line');
  s = rep(s, '<h2 class="ib-title">You\u2019re hired</h2>', '<h2 class="ib-title">Your card</h2>', u, file + ' B34 title');
  s = rep(s, 'This card is yours. You\u2019re hired \u2014 and when we get paid, you get paid.', 'This card is yours \u2014 and when we get paid, you get paid.', u, file + ' B34 line');
  return s;
}

function fixUnfold(U) {
  U = fixBoardText(U, 'unfold');
  // Fail 7 — board 1's internal note, in plain reader words (the anthem /
  // audio wiring itself stays unwired; the queued anthem round owns it).
  U = rep(U, 'Waiting on the captioned video \\u2014 the audio is cut from it', 'Naya\\u2019s reading arrives with her video', 1, 'U audio state');
  U = rep(U, 'Naya\\u2019s reading arrives with the captioned video \\u2014 the audio is cut from that video. Nothing is wired here yet; the reading starts when his video arrives.', 'Naya\\u2019s reading arrives with her video.', 1, 'U audio note');
  U = rep(U, 'The captioned anthem video arrives soon. These are its opening words, while the video is on its way.', 'These are the anthem\\u2019s opening words. The video is on its way.', 1, 'U anthem note');
  // Fail 1 — one board at a time. #deckBody .letter-beat{height:100%!important;
  // display:flex!important} (1,1,0) outranked .letter-beat:not(.frame-now)
  // {display:none!important} (0,2,0), so all 37 boards showed as one long
  // page while the pill moved. This rule (1,2,0) restores the hide.
  // Fail 6 — the showcase shows in talk view too (the fp-smart-talk hide
  // is vestigial on the unfold; the picture must never vanish).
  var style = '<style id="fpFixDistill">\n' +
    '/* FIX (2026-11-19, eye fail 1) — one board at a time: the frame-now hide lost to the later #deckBody rule, so all 37 boards stacked as one long scrollable page. This outranks it, so exactly one board shows and the pill tracks the board on screen. */\n' +
    '#deckBody .letter-beat:not(.frame-now){display:none!important}\n' +
    '#deckBody .letter-beat.frame-now{display:flex!important;flex-direction:column!important}\n' +
    '#deckBody{overflow-x:hidden}\n' +
    '/* FIX (2026-11-19, eye fail 6) — the showcase shows in talk view too. */\n' +
    '.letter-beat.fp-smart-talk .lb-showcase{display:block!important}\n' +
    '</style>\n';
  U = rep(U, '</head>', style + '</head>', 1, 'U head insert');
  // Fail 4 — /agreement honours ?stage=: the deck, the letter and the
  // bridge live on the welcome page, so hand the reader there with the
  // stage kept. Plain /agreement is untouched.
  var script = '<script>\n' +
    '/* FIX (2026-11-19, eye fail 4) — /agreement honours ?stage=: deck, letter and bridge live on the welcome page, so hand the reader there with the stage kept. */\n' +
    '(function(){try{var st=new URLSearchParams(window.location.search).get(\'stage\');if(st===\'deck\'||st===\'letter\'||st===\'bridge\'){window.location.replace(\'/?stage=\'+st);}}catch(e){}})();\n' +
    '</script>\n';
  U = rep(U, '\n</body>\n</html>', '\n' + script + '</body>\n</html>', 1, 'U body insert');
  return U;
}

function fixWelcome(W) {
  W = fixBoardText(W, 'welcome');
  // Fail 7 — the deck intro's count must be true: 37 boards, not nine pictures.
  W = rep(W, 'Nine pictures. One beautiful story.', 'Thirty-seven boards. One beautiful story.', 1, 'W nine pictures');
  // Fail 3 — one story: the deck carried 37 extra quote lines (ib-subtitle)
  // the letter and /agreement do not. Remove them; the words are the boards.
  W = repRe(W, /<p class="ib-subtitle">[^<]*<\/p>/g, '', 37, 'W deck subtitles');

  // ---- Fail 2 — one tap per board (the two-phase Smart Block is gone) ----
  W = rep(W, '      /* SMART BLOCK (2026-11-18) \u2014 one visual per block: a beat with a\n         showcase is TWO Smart Blocks. The first tap shows the visual\n         alone (16:9, locked to the viewport); the next tap moves on. */',
    '      /* FIX (2026-11-19, eye fail 2) \u2014 one tap per board: the visual and\n         the words are one board. Keep reading always moves to the next. */', 2, 'W keep-reading comment');
  W = rep(W, '      if (b.querySelector(\'.lb-showcase\') && !b.classList.contains(\'fp-smart-visual\')) {\n        b.classList.add(\'fp-smart-visual\');\n        b.classList.remove(\'fp-smart-talk\');\n        ensureBeatVisible(b);\n        return;\n      }',
    '      /* FIX (2026-11-19, eye fail 2) \u2014 one tap: the visual-first branch is gone; Keep reading always moves on. */', 2, 'W visual-first branch');
  W = rep(W, '      var cur = i + 1;\n      if (cur < beats.length) {\n        show(cur);\n        idx = cur + 1;\n        btn.hidden = true;\n        if (idx < beats.length) ensureBeatVisible(beats[cur]);\n      }',
    '      var cur = i + 1;\n      if (cur < beats.length) {\n        show(cur);\n        idx = cur + 1;\n        btn.hidden = true;\n        if (idx < beats.length) ensureBeatVisible(beats[cur]);\n      } else if (window.__fpStageEnd) {\n        /* FIX (2026-11-19, eye fail 5b) \u2014 the last board\'s Keep reading ends the story the same way the mirror button does. */\n        window.__fpStageEnd();\n      }', 2, 'W last-beat hook');
  W = rep(W, '  /* SMART BLOCK (2026-11-18) \u2014 always go back: every beat carries a\n     \u2039 Back button beside its Keep reading. It steps back one Smart\n     Block: visual -> talk on the same beat, else the previous beat\n     (its visual if it has a showcase, else its talk). */',
    '  /* FIX (2026-11-19, eye fail 2) \u2014 always go back: every beat carries a\n     \u2039 Back button beside its Keep reading. It steps back one board. */', 2, 'W back comment');
  W = rep(W, '      if (b.classList.contains(\'fp-smart-visual\')) {\n        b.classList.remove(\'fp-smart-visual\');\n        b.classList.add(\'fp-smart-talk\');\n        ensureBeatVisible(b);\n        return;\n      }', '', 2, 'W back visual branch');
  W = rep(W, '      if (prev.querySelector(\'.lb-showcase\')) {\n        prev.classList.add(\'fp-smart-visual\');\n        prev.classList.remove(\'fp-smart-talk\');\n      } else {\n        prev.classList.add(\'fp-smart-talk\');\n        prev.classList.remove(\'fp-smart-visual\');\n      }',
    '      prev.classList.add(\'fp-smart-talk\');\n      prev.classList.remove(\'fp-smart-visual\');', 2, 'W back prev branch');
  W = rep(W, '    /* SMART BLOCK (2026-11-18) \u2014 one visual per block (see wireDeck). */\n    var curBeat = beats[idx - 1];\n    if (curBeat && curBeat.querySelector(\'.lb-showcase\') && !curBeat.classList.contains(\'fp-smart-visual\')) {\n      curBeat.classList.add(\'fp-smart-visual\');\n      curBeat.classList.remove(\'fp-smart-talk\');\n      ensureBeatVisible(curBeat);\n      return;\n    }',
    '    /* FIX (2026-11-19, eye fail 2) \u2014 one tap per board: the visual-first branch is gone. */\n    var curBeat = beats[idx - 1];', 1, 'W wireLetter visual branch');
  W = rep(W, '        b.classList.toggle(\'fp-smart-visual\',sd&&S.phase===\'visual\');\n        b.classList.toggle(\'fp-smart-talk\',sd&&S.phase===\'talk\');',
    '        b.classList.remove(\'fp-smart-visual\');\n        b.classList.toggle(\'fp-smart-talk\',sd);', 1, 'W render deck');
  W = rep(W, '        else{b.classList.toggle(\'fp-smart-visual\',sl&&S.phase===\'visual\');b.classList.toggle(\'fp-smart-talk\',sl&&S.phase===\'talk\');}',
    '        else{b.classList.remove(\'fp-smart-visual\');b.classList.toggle(\'fp-smart-talk\',sl);}', 1, 'W render letter');
  W = rep(W, '        b.classList.toggle(\'fp-smart-visual\',slp&&S.phase===\'visual\');\n        b.classList.toggle(\'fp-smart-talk\',slp&&S.phase===\'talk\');',
    '        b.classList.remove(\'fp-smart-visual\');\n        b.classList.toggle(\'fp-smart-talk\',slp);', 1, 'W render letterPage');
  W = repRe(W, /S\.phase=\(\w+&&\w+\.classList\.contains\('fp-smart-visual'\)\)\?'visual':'talk';/g, 'S.phase=\'talk\';', 3, 'W derive phase');
  W = rep(W, 'function deckEnd(){return S.deck>=deckBeats.length-1&&(!hasShowcase(deckBeats[S.deck])||S.phase===\'visual\');}',
    'function deckEnd(){return S.deck>=deckBeats.length-1;}', 1, 'W deckEnd');
  W = rep(W, 'function letterEnd(){return S.letter>=letterBeats.length-1&&(!hasShowcase(letterBeats[S.letter])||S.phase===\'visual\');}',
    'function letterEnd(){return S.letter>=letterBeats.length-1;}', 1, 'W letterEnd');
  W = rep(W, '      /* FIX1 (2026-11-18) \u2014 deck beat 9 HAS a showcase like beats 1-8,\n         so its end button must show the visual first (talk, then\n         visual), not exit on the talk tap; and the exit goes through\n         the N hold, like deck-end Enter. S.phase is still \'talk\' on the\n         first tap (derive has not run since the phase handler added the\n         visual class), \'visual\' on the second \u2014 that is the tell. */',
    '      /* FIX (2026-11-19, eye fail 2) \u2014 one tap: the deck\'s end anchor exits through the N hold at once, like deck-end Enter. */', 1, 'W anchor comment');
  W = rep(W, '      if(S.view===\'deck\'&&S.phase!==\'visual\'){var _cb=currentBeatEl();if(_cb&&_cb.querySelector(\'.lb-showcase\')){if(!_cb.classList.contains(\'fp-smart-visual\')){_cb.classList.add(\'fp-smart-visual\');_cb.classList.remove(\'fp-smart-talk\');}derive(false);render();return;}}', '', 1, 'W anchor branch');

  // ---- Fail 2 — no void, nothing cut off: the showcase shows in talk view ----
  var style = '<style id="fpFixDistill">\n' +
    '/* FIX (2026-11-19, eye fail 2) \u2014 one phase, no void: the showcase shows in talk view too. The old rule hid it and left the grid\'s second column an empty black void on every text view; the plain-page deck hid its pictures the same way. */\n' +
    'body.fp-stage-on #fpAgreement .fp-now.fp-smart-talk .lb-showcase{display:block!important}\n' +
    '#fpAgreement .letter-beat.fp-smart-talk .lb-showcase{display:block!important}\n' +
    '/* FIX (2026-11-19, eye fail 2) \u2014 nothing cut off at the edges: the stage layer and every board clip horizontally. */\n' +
    'body.fp-stage-on #fpAgreement{overflow-x:hidden}\n' +
    'body.fp-stage-on #fpAgreement .letter-beat{overflow-x:hidden;max-width:100%}\n' +
    '</style>\n';
  W = rep(W, '</head>', style + '</head>', 1, 'W head insert');

  // ---- Fail 5a — hero "Read the collective agreement" goes to /agreement ----
  W = rep(W, '  /* EYE FOLLOW-ON #2 F4 (2026-11-18): the login\'s "Read the collective\n   agreement" link must open the CHOICE view, never resume the deck.\n   Deck-end "Enter NayaNET" sets window.__fpDeckEndReturn=true, and\n   enterStage() re-entered at deck 9/9 while the flag stood (the eye\n   proved it twice). The explicit read-link action clears the flag\n   first, so enterStage() lands on the intro (choice). goResume\n   ("Begin the visual story") still resumes where left off - that is\n   its stated job - and the deck-end exit itself is untouched. */',
    '  /* FIX (2026-11-19, eye fail 5a) \u2014 the hero "Read the collective agreement" goes to /agreement, not into the in-page stage. The in-page stage is entered only by ?stage= and the deck/letter flows. */', 1, 'W enterBtn comment');
  W = rep(W, 'if(enterBtn)enterBtn.addEventListener(\'click\',function(){window.__fpDeckEndReturn=false;enterStage();});',
    'if(enterBtn)enterBtn.addEventListener(\'click\',function(){window.location.href=\'/agreement\';});', 1, 'W enterBtn');

  // ---- Fail 5b — the last board's Keep reading ends the story (hook) ----
  W = rep(W, '  function enterLetterPage(){S.view=\'letterPage\';S.phase=\'talk\';S.all=null;render();}',
    '  function enterLetterPage(){S.view=\'letterPage\';S.phase=\'talk\';S.all=null;render();}\n' +
    '  /* FIX (2026-11-19, eye fail 5b) \u2014 the last board\'s Keep reading ends the story through this hook (the in-beat handler calls it when there is no next board). Deck: the N hold, then the bridge. Letter: the agree view, like the mirror button. Stage-only. */\n' +
    '  window.__fpStageEnd=function(){\n' +
    '    if(!body.classList.contains(\'fp-stage-on\'))return;\n' +
    '    if(S.view===\'deck\'){window.__fpDeckEndReturn=true;showNHold(function(){goBridgeAfterAgree();});}\n' +
    '    else if(S.view===\'letter\'||S.view===\'letterPage\'){agreeFromLetterPage();}\n' +
    '  };', 1, 'W stageEnd hook');

  // ---- Fail 5c — bridge Enter shows the N hold before identity ----
  W = rep(W, '  function releaseNHold(){',
    '  /* FIX (2026-11-19, eye fail 5c) \u2014 the name form lives outside the stage IIFE, so expose the hold for its submit: when the citizen agreed, Enter shows the N hold first, then goes to identity. */\n' +
    '  window.__fpHoldThen=function(done){showNHold(done);};\n' +
    '  function releaseNHold(){', 1, 'W holdThen expose');
  W = rep(W, '  f.addEventListener(\'submit\',function(e){\n    e.preventDefault();\n    var v=(n.value||\'\').trim();\n    window.location.href=\'/identity.html\'+(v?\'?name=\'+encodeURIComponent(v):\'\');\n  });',
    '  f.addEventListener(\'submit\',function(e){\n' +
    '    e.preventDefault();\n' +
    '    var v=(n.value||\'\').trim();\n' +
    '    var dest=\'/identity.html\'+(v?\'?name=\'+encodeURIComponent(v):\'\');\n' +
    '    /* FIX (2026-11-19, eye fail 5c/5d) \u2014 the citizen came through the agreement (agreed key, or the bridge\'s name-entry flag): show the N hold first, then go to identity. Otherwise go at once. */\n' +
    '    var _ag=false,_fb=false;\n' +
    '    try{_ag=localStorage.getItem(\'nayanet_fp_agreed\')===\'1\'||window.__fpAgreed===true;}catch(err){}\n' +
    '    try{_fb=window.__fpFromBridge===true||sessionStorage.getItem(\'nayanet_fp_from_bridge\')===\'1\';}catch(err2){}\n' +
    '    if((_ag||_fb)&&window.__fpHoldThen){\n' +
    '      try{sessionStorage.removeItem(\'nayanet_fp_from_bridge\');}catch(err3){}\n' +
    '      window.__fpFromBridge=false;\n' +
    '      window.__fpHoldThen(function(){window.location.href=dest;});\n' +
    '    }else{\n' +
    '      window.location.href=dest;\n' +
    '    }\n' +
    '  });', 1, 'W submit hold');

  // ---- Fail 5d — the name-entry state survives a reload ----
  W = rep(W, '    try{localStorage.removeItem(\'nayanet_fp_stage\');localStorage.removeItem(\'nayanet_fp_agreed\');}catch(e){}\n    window.__fpAgreed=false;\n    exitStage();',
    '    try{localStorage.removeItem(\'nayanet_fp_stage\');localStorage.removeItem(\'nayanet_fp_agreed\');}catch(e){}\n' +
    '    window.__fpAgreed=false;\n' +
    '    /* FIX (2026-11-19, eye fail 5c/5d) \u2014 the citizen is mid-name-entry after agreeing: remember it across a reload, so the name form re-opens instead of the login hero, and the submit shows the N hold. Cleared on submit and on Back-to-login. */\n' +
    '    window.__fpFromBridge=true;\n' +
    '    try{sessionStorage.setItem(\'nayanet_fp_from_bridge\',\'1\');}catch(e){}\n' +
    '    exitStage();', 1, 'W fromBridge set');
  W = rep(W, '  }catch(e){}\n    /* EYE FOLLOW-ON #2 F1 (2026-11-',
    '  }catch(e){}\n' +
    '  /* FIX (2026-11-19, eye fail 5d) \u2014 the name-entry state survives a reload: goBridgeToName set the flag, so re-open the name form instead of sitting on the login hero. Never runs while the stage is on. */\n' +
    '  try{\n' +
    '    var _fb2=false;try{_fb2=sessionStorage.getItem(\'nayanet_fp_from_bridge\')===\'1\';}catch(e){}\n' +
    '    if(_fb2&&!body.classList.contains(\'fp-stage-on\')){\n' +
    '      var _ff=document.getElementById(\'entryForm\'),_fv=document.getElementById(\'returningView\'),_fn=document.getElementById(\'userName\');\n' +
    '      if(_ff){_ff.hidden=false;if(_fv)_fv.hidden=true;if(_fn)_fn.focus();}\n' +
    '    }\n' +
    '  }catch(e){}\n' +
    '    /* EYE FOLLOW-ON #2 F1 (2026-11-', 1, 'W fromBridge restore');
  W = rep(W, 'bExit.addEventListener(\'click\',function(){cancelAgreeExit();exitStage();});',
    'bExit.addEventListener(\'click\',function(){cancelAgreeExit();exitStage();try{window.__fpFromBridge=false;sessionStorage.removeItem(\'nayanet_fp_from_bridge\');}catch(e){}});', 1, 'W bExit clear');
  W = rep(W, 'if(fExit){fExit.addEventListener(\'click\',function(){cancelAgreeExit();exitStage();});}',
    'if(fExit){fExit.addEventListener(\'click\',function(){cancelAgreeExit();exitStage();try{window.__fpFromBridge=false;sessionStorage.removeItem(\'nayanet_fp_from_bridge\');}catch(e){}});}', 1, 'W fExit clear');

  // ---- Fail 4 — the letter page gets progress (the jewel never updated) ----
  // updateChrome's letterPage branch set the button but never the jewel, so
  // ?stage=letter showed no progress at all. Mirror the letter branch.
  W = rep(W, '    else if(S.view===\'letterPage\'){\n      tone=toneOf(letterBeats[S.letter]);',
    '    else if(S.view===\'letterPage\'){\n      tone=toneOf(letterBeats[S.letter]);\n      jewelEl.classList.add(\'fp-on\');\n      jewelNum.textContent=(S.letter+1)+\' / \'+letterBeats.length;\n      jewelBar.style.width=Math.round(((S.letter+1)/letterBeats.length)*100)+\'%\';\n      jewelEl.style.setProperty(\'--tone\',tone);', 1, 'W letterPage jewel');

  // ---- Fail 1/2 — Back steps back one board in the stage too ----
  // The in-beat Back unhid the previous beat but never hid the current one,
  // so derive()'s lastShown landed on the current beat and render() re-hid
  // the previous: Back was a no-op in the stage. In the stage only, hide
  // this beat first; off-stage the beats stay stacked for scrolling.
  W = rep(W, '      if (i <= 0) return;\n      var prev = beats[i - 1];',
    '      if (i <= 0) return;\n      /* FIX (2026-11-19, eye fail 1/2) \u2014 in the stage, hide this beat so derive()\'s lastShown lands on the previous board; off-stage the beats stay stacked for scrolling. */\n      if (document.body.classList.contains(\'fp-stage-on\')) b.hidden = true;\n      var prev = beats[i - 1];', 2, 'W stage back hide');
  W = rep(W, 'try { var st = new URLSearchParams(window.location.search).get(\'stage\'); if (st === \'deck\') on(); } catch (e) {}',
    'try { var st = new URLSearchParams(window.location.search).get(\'stage\'); if (st === \'deck\' || st === \'letter\') on(); } catch (e) {}', 1, 'W frame boot');
  W = rep(W, 'if (l1) l1.addEventListener(\'click\', function(){ setTimeout(off, 0); });',
    'if (l1) l1.addEventListener(\'click\', function(){ setTimeout(on, 0); });', 1, 'W frame l1');
  W = rep(W, 'if (l2) l2.addEventListener(\'click\', function(){ setTimeout(off, 0); });',
    'if (l2) l2.addEventListener(\'click\', function(){ setTimeout(on, 0); });', 1, 'W frame l2');

  // ---- Fail 2 — Naya's photo top-right, pinned to the board's top ----
  W = rep(W, 'side: b.classList.contains(\'face-right\') ? \'right\' : \'left\'',
    'side: \'right\'', 1, 'W face side');
  W = rep(W, '      }\n      img.style.top = faceTop + \'px\';',
    '      }\n' +
    '      /* FIX (2026-11-19, eye fail 2) \u2014 deck/letter faces sit top-right, pinned to the board\'s top edge, never centred on a moving speaking line and never off the left edge. */\n' +
    '      if (f.key && (f.key.indexOf(\'deck:\') === 0 || f.key.indexOf(\'letter:\') === 0)) {\n' +
    '        var bbr2 = board.getBoundingClientRect();\n' +
    '        var bTop2 = bbr2.top - pr.top + parent.scrollTop;\n' +
    '        faceTop = Math.max(bTop2 + 4, Math.min(bTop2 + 12, bTop2 + bbr2.height - faceH - 4));\n' +
    '      }\n' +
    '      img.style.top = faceTop + \'px\';', 1, 'W face top');

  // ---- Fail 6 — pictures load reliably: retry once, then fall back ----
  var imgScript = '<script>\n' +
    '/* FIX (2026-11-19, eye fail 6) \u2014 a picture that fails to load retries once cache-busted, then falls back instead of showing a black circle or collapsing to 0 height. Faces fall back to the crystal N (the unfold\'s own fallback, harvested verbatim); showcases hide their frame so the words still read. Capture phase: the error never bubbles. */\n' +
    '(function(){\n' +
    '  var CRYSTAL=\'https://naya-proof-host.nayapower.workers.dev/?file=team-nitro/agreement-unfold-20261117/crystal-n.png&ref=walkthrough/chain-fix8-20261119&cb=ee4b627c0c254ed9165715308fa282010ce8cf3c\';\n' +
    '  document.addEventListener(\'error\',function(e){\n' +
    '    var t=e.target;\n' +
    '    if(!t||t.tagName!==\'IMG\')return;\n' +
    '    if(t.getAttribute(\'data-fp-retried\'))return;\n' +
    '    var src=t.getAttribute(\'src\')||\'\';\n' +
    '    if(!src)return;\n' +
    '    t.setAttribute(\'data-fp-retried\',\'1\');\n' +
    '    if(t.classList.contains(\'deal-beat-photo\')||t.classList.contains(\'fp-naya-portrait\')){\n' +
    '      t.addEventListener(\'error\',function(){t.style.display=\'none\';},{once:true});\n' +
    '      t.src=CRYSTAL;\n' +
    '      return;\n' +
    '    }\n' +
    '    if(t.closest&&t.closest(\'.lb-showcase\')){\n' +
    '      t.addEventListener(\'error\',function(){var f=t.closest(\'.lb-showcase\');if(f)f.style.display=\'none\';},{once:true});\n' +
    '      t.src=src+(src.indexOf(\'?\')===-1?\'?\':\'&\')+\'retry=1\';\n' +
    '    }\n' +
    '  },true);\n' +
    '})();\n' +
    '</script>\n';
  W = rep(W, '\n</body>\n</html>', '\n' + imgScript + '</body>\n</html>', 1, 'W body insert');

  // ---- Final guards: no visual phase can ever be entered again ----
  if (W.indexOf('S.phase=\'visual\'') !== -1) throw new Error('FIX-FAIL W guard: S.phase=\'visual\' remains');
  if ((W.match(/classList\.add\('fp-smart-visual'\)/g) || []).length !== 0) throw new Error('FIX-FAIL W guard: add fp-smart-visual remains');
  if ((W.match(/S\.phase==='visual'/g) || []).length !== 0) throw new Error('FIX-FAIL W guard: S.phase visual read remains');
  return W;
}

var U0 = emit('unfold');
var W0 = emit('welcome');
var U1 = fixUnfold(U0);
var W1 = fixWelcome(W0);
process.stdout.write(JSON.stringify({
  unfold_b64: Buffer.from(U1, 'utf8').toString('base64'),
  welcome_b64: Buffer.from(W1, 'utf8').toString('base64'),
  unfold_bytes: Buffer.byteLength(U1),
  welcome_bytes: Buffer.byteLength(W1)
}));
