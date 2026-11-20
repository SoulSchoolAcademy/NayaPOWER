// Verify fix-6 bytes: script parse, fix-5 region intact, guard present, fallback untouched.
const vm = require('vm');
const crypto = require('crypto');
const { fetchBase, transform } = require('./edit-fix6.js');
const base = fetchBase();
const out = transform(base);
function scriptsOf(s) {
  const re = /<script(?:\s[^>]*)?>([\s\S]*?)<\/script\s*>/gi;
  const out = []; let m;
  while ((m = re.exec(s))) out.push(m[1]);
  return out;
}
const bScripts = scriptsOf(base), oScripts = scriptsOf(out);
console.log(JSON.stringify({ baseScripts: bScripts.length, outScripts: oScripts.length }));
let fails = 0;
oScripts.forEach((code, i) => { try { new vm.Script(code, { filename: 'script-' + i }); } catch (e) { fails++; console.log('PARSE FAIL script', i, e.message.slice(0, 200)); } });
console.log(JSON.stringify({ parseFails: fails }));
const checks = {
  guardPresent: out.includes("if (_h==='hub' || _h==='smart-notes' || _h==='notes' || _h==='note') return;"),
  f6comment: out.includes('FRAME-FIX6 2026-11-19 (F6)'),
  fix5RecoverPresent: out.includes('recoverFeedAfterBack'),
  fix5HookCount: (out.match(/recoverFeedAfterBack/g) || []).length,
  baseFix5HookCount: (base.match(/recoverFeedAfterBack/g) || []).length,
  fallbackUntouched: out.includes("Router.on('*', () => { var _h=(location.hash||'').replace(/^#\\/?/,'').split('?')[0].split('/')[0]; var _pv=['home','about','people','message','inbox','growth','lists','reports','settings','skills','scheduler','memberships','notes','dashboard','today','story','myworld'];"),
  askBtnUntouched: out.includes("askBtn.addEventListener('click', () => { if (window.NayaRouter) window.NayaRouter.navigate('/hub/ask'); else location.hash = '#/hub/ask'; });"),
  popstateSingle: (out.match(/addEventListener\('popstate'/g) || []).length,
};
console.log(JSON.stringify(checks, null, 2));
// diff must be exactly the one insertion
const bl = base.split('\n'), ol = out.split('\n');
let pre = 0; while (pre < bl.length && pre < ol.length && bl[pre] === ol[pre]) pre++;
let suf = 0; while (suf < bl.length - pre && suf < ol.length - pre && bl[bl.length - 1 - suf] === ol[ol.length - 1 - suf]) suf++;
console.log(JSON.stringify({ prefix: pre, suffix: suf, baseRemoved: bl.length - pre - suf, outAdded: ol.length - pre - suf }));
if (fails || !checks.guardPresent || checks.fix5HookCount !== checks.baseFix5HookCount || !checks.fallbackUntouched || bl.length - pre - suf !== 0 || ol.length - pre - suf !== 12) { console.error('VERIFY FAILED'); process.exit(1); }
console.log('VERIFY OK');
