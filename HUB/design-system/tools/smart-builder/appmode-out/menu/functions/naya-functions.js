/* NayaFunctions — the loader. v1.0.0 (Item 26, INFRA/Tau)
   What: registry + boot for all NayaFunction units. Every unit activates through this file.
   Activation: <script src="naya-functions.js"></script> BEFORE any f-*.js unit file.
   Boot: on DOMContentLoaded, every [data-fn] element is activated by its registered unit.
   Contract: <div data-fn="<id>" data-fn-config='{...}'></div>
     - data-fn-config parsed as JSON, fail-soft (bad JSON -> warn + defaults, never crash)
     - unregistered id -> console.warn + skip (fail-closed: never pretend a missing function works)
   API: NayaFunctions.register(id, def) | NayaFunctions.get(id) | NayaFunctions.boot(scope)
   Lessons: L-2026-10-17-004 (fail-soft everywhere), L-2026-10-16-005 (real behavior, no staging)
*/
(function(){
'use strict';
var NF = window.NayaFunctions = window.NayaFunctions || {};
NF._r = NF._r || {};
NF.version = '1.0.0';

NF.register = NF.register || function(id, def){
  if (!id || typeof id !== 'string') return;
  if (NF._r[id]) return; // one function, one implementation — never double-register
  NF._r[id] = def || {};
};

NF.get = function(id){ return NF._r[id] || null; };

NF.parseConfig = function(el){
  var raw = el.getAttribute('data-fn-config');
  if (raw == null || raw === '') return {};
  try {
    var c = JSON.parse(raw);
    return (c && typeof c === 'object') ? c : {};
  } catch (e) {
    console.warn('[NayaFunctions] data-fn-config is not valid JSON on <' +
      el.tagName.toLowerCase() + ' data-fn="' + el.getAttribute('data-fn') + '"> — using defaults (fail-soft)');
    return {};
  }
};

NF.boot = function(scope){
  scope = scope || document;
  var booted = [];
  var els = scope.querySelectorAll('[data-fn]');
  for (var i = 0; i < els.length; i++) {
    var el = els[i];
    if (el._nayaFn) continue; // idempotent — already booted
    var id = el.getAttribute('data-fn');
    if (!id) continue;
    var def = NF._r[id];
    if (!def || typeof def.activate !== 'function') {
      console.warn('[NayaFunctions] unregistered function id "' + id + '" — skipped (fail-closed)');
      continue;
    }
    var config = NF.parseConfig(el);
    try {
      var inst = def.activate(el, config);
      el._nayaFn = { id: id, instance: inst || null, version: def.version || '?' };
      booted.push(id);
    } catch (err) {
      console.error('[NayaFunctions] activate("' + id + '") threw — element left untouched (fail-soft)', err);
    }
  }
  return booted;
};

function bootNow(){ NF.boot(document); }
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', bootNow);
} else {
  bootNow();
}
})();
