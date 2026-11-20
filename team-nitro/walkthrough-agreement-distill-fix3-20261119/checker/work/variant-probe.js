#!/usr/bin/env node
// variant-probe.js — CHECKER: try to identify the 25 bytes between the maker's
// claimed walk sha (b068d1da, 4,363,239 B) and the reproducible bytes
// (ef982267, 4,363,264 B). Tests plausible earlier-variant surgeries on the
// checker's fixed walk; prints the sha of each. A hit identifies the stale
// version; no hit means the claimed bytes survive nowhere.
const runFix2 = require('/home/hatch/workspace/team-nitro/walkthrough-agreement-distill-fix3-20261119/maker/work/run-fix2-export.js');
const checker = require('./check-fix3.js');
const crypto = require('crypto');
const sha = (s) => crypto.createHash('sha256').update(s, 'utf8').digest('hex');
const TARGET = 'b068d1da38403878eb0b4a552ea92efec2fe77724d6a12fdef04f98fb8f8089b';
(async () => {
  const R = await runFix2();
  const F2 = { U: R.U, W: R.W, WK: R.WK, I: R.I };
  const C = checker.applyFix3(F2);
  const W = C.WK;
  console.log('current: ' + Buffer.byteLength(W) + 'B ' + sha(W) + ' (target ' + TARGET.slice(0, 16) + ')');
  const variants = {};
  const btnLine = '\n<button type="button" class="p3-enter" id="doorContinue" style="font-family:inherit">Continue to the walk ◆</button>';
  variants['no-button'] = W.split(btnLine).join('');
  variants['no-button-style-attr'] = W.split(' style="font-family:inherit"').join('');
  variants['no-button-diamond'] = W.split(' ◆</button>').join('</button>');
  variants['no-wiring'] = W.split(C._ins.W_WIRE.slice(0, C._ins.W_WIRE.length - C._ins.W_WIRE.indexOf('  if (!ID.alias)'))).join('') && W; // placeholder, replaced below
  // wiring block alone (comment + IIFE + \n), anchor kept:
  const wireBlock = "  /* FIX3 (distill fix-3, F9b) — the door's explicit continue: a certified citizen dismisses the door by tapping Continue; the door hides, then proceed() opens the walk. No alias, no continue — the walk opens after the certificate. */\n  (function(){ var c = document.getElementById('doorContinue'); if (!c) return; if (!ID.alias) { c.hidden = true; return; } c.addEventListener('click', function(){ var d = document.getElementById('step-door'); if (d) d.hidden = true; proceed(); }); })();\n";
  variants['no-wiring'] = W.split(wireBlock).join('');
  variants['no-wiring-comment-only'] = W.split("  /* FIX3 (distill fix-3, F9b) — the door's explicit continue: a certified citizen dismisses the door by tapping Continue; the door hides, then proceed() opens the walk. No alias, no continue — the walk opens after the certificate. */\n").join('');
  variants['no-guard-comment-only'] = W.split("  /* FIX3 (distill fix-3, F9b) — the door is the gate: while #step-door is visible, NOTHING advances the walk. Only the user's own action on the door (the certificate link or the explicit continue) dismisses it, never a timer. */\n").join('');
  variants['guard-nospaces'] = W.split("if (document.getElementById('step-door') && !document.getElementById('step-door').hidden) return;").join("if(document.getElementById('step-door')&&!document.getElementById('step-door').hidden)return;");
  variants['no-never-a-timer'] = W.split(', never a timer.').join('.');
  variants['emdash-to-hyphen'] = W.split('—').join('-');
  variants['no-wiring-noalias-clause'] = W.split('No alias, no continue — the walk opens after the certificate. ').join('');
  for (const [name, s] of Object.entries(variants)) {
    const b = Buffer.byteLength(s), h = sha(s);
    console.log(name + ': ' + b + 'B sha ' + h.slice(0, 16) + (h === TARGET ? '  <=== MATCHES CLAIM' : '') + (b === 4363239 ? '  <=== SIZE MATCHES CLAIM' : ''));
  }
  process.exit(0);
})().catch((e) => { console.error('FATAL', e); process.exit(1); });
