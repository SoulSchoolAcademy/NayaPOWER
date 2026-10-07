/* NayaVoice — Hub Intelligent Block play-button voice engine.
 * Contract (Naya 2 → Naya 4, #1354):
 *   NayaVoice.speak(text, hooks)  — hooks: {onstart, onboundary, onend, onerror}.
 *                                    New speech always cancels the old (no overlap).
 *   NayaVoice.stop()              — cancel immediately (call on navigation / block switch).
 *   NayaVoice.setProvider(p, label) — provider = {speak(text, hooks), stop()}.
 *                                    Tier 2 (her true cloned voice) swaps in here
 *                                    with zero control changes.
 *   NayaVoice.voiceLabel          — 'SYNTHESIZED VOICE' until Tier 2 lands.
 *                                    Display honestly. Never label Tier 1 as her voice.
 * Tier 1 = browser Web Speech API (dev fallback only). On-demand only.
 */
(function (global) {
  'use strict';

  var SYNTH_LABEL = 'SYNTHESIZED VOICE';

  // ---- Tier 1 provider: Web Speech API -------------------------------------
  var tier1 = {
    _utt: null,
    _paused: false,
    speak: function (text, hooks) {
      hooks = hooks || {};
      this.stop();
      if (!('speechSynthesis' in window)) {
        if (hooks.onerror) hooks.onerror(new Error('speechSynthesis unavailable'));
        if (hooks.onend) hooks.onend();
        return;
      }
      var u = new SpeechSynthesisUtterance(text);
      u.rate = 1.0; u.pitch = 1.0;
      // Prefer a natural en voice when the platform offers one.
      try {
        var vs = window.speechSynthesis.getVoices();
        var pick = vs.filter(function (v) { return v.lang && v.lang.toLowerCase().indexOf('en') === 0 && v.name.toLowerCase().indexOf('google') > -1; })[0]
          || vs.filter(function (v) { return v.lang && v.lang.toLowerCase().indexOf('en') === 0; })[0];
        if (pick) u.voice = pick;
      } catch (e) { /* voice pick is best-effort */ }
      u.onstart = function () { if (hooks.onstart) hooks.onstart(); };
      u.onboundary = function (ev) { if (hooks.onboundary) hooks.onboundary(ev); };
      u.onend = function () { tier1._utt = null; tier1._paused = false; if (hooks.onend) hooks.onend(); };
      u.onerror = function (ev) { tier1._utt = null; tier1._paused = false; if (hooks.onerror) hooks.onerror(ev.error || ev); };
      this._utt = u;
      window.speechSynthesis.speak(u);
    },
    stop: function () {
      if (!('speechSynthesis' in window)) return;
      window.speechSynthesis.cancel();
      this._utt = null;
      this._paused = false;
    },
    pause: function () {
      if (!('speechSynthesis' in window)) return;
      window.speechSynthesis.pause();
      this._paused = true;
    },
    resume: function () {
      if (!('speechSynthesis' in window)) return;
      window.speechSynthesis.resume();
      this._paused = false;
    },
    get paused() { return this._paused; },
    get speaking() { return !!this._utt; }
  };

  // ---- NayaVoice ------------------------------------------------------------
  var _provider = tier1;
  var _label = SYNTH_LABEL;
  var _state = 'idle'; // idle | speaking | paused
  var _stateListeners = [];

  function setState(s) {
    _state = s;
    _stateListeners.forEach(function (fn) { try { fn(s); } catch (e) {} });
  }

  var NayaVoice = {
    get voiceLabel() { return _label; },
    get state() { return _state; },
    get paused() { return _state === 'paused'; },
    get speaking() { return _state === 'speaking'; },

    onState: function (fn) {
      _stateListeners.push(fn);
      return function () {
        var i = _stateListeners.indexOf(fn);
        if (i > -1) _stateListeners.splice(i, 1);
      };
    },

    speak: function (text, hooks) {
      hooks = hooks || {};
      var wrapped = {
        onstart: function () { setState('speaking'); if (hooks.onstart) hooks.onstart(); },
        onboundary: hooks.onboundary,
        onend: function () { setState('idle'); if (hooks.onend) hooks.onend(); },
        onerror: function (e) { setState('idle'); if (hooks.onerror) hooks.onerror(e); }
      };
      _provider.speak(text, wrapped);
    },

    stop: function () {
      _provider.stop();
      setState('idle');
    },

    pause: function () {
      if (_provider.pause && _state === 'speaking') { _provider.pause(); setState('paused'); }
    },

    resume: function () {
      if (_provider.resume && _state === 'paused') { _provider.resume(); setState('speaking'); }
    },

    toggle: function () {
      if (_state === 'paused') this.resume();
      else if (_state === 'speaking') this.pause();
    },

    // Tier 2 seam: provider = {speak(text, hooks), stop()}.
    // Optional pause/resume pass through when supplied.
    setProvider: function (provider, label) {
      if (!provider || typeof provider.speak !== 'function' || typeof provider.stop !== 'function') {
        throw new Error('NayaVoice.setProvider: provider must supply speak(text, hooks) and stop()');
      }
      this.stop();
      _provider = provider;
      _label = label || SYNTH_LABEL;
    }
  };

  // Stop/reset on navigation — never let audio bleed across pages.
  window.addEventListener('pagehide', function () { NayaVoice.stop(); });
  document.addEventListener('visibilitychange', function () {
    if (document.hidden) NayaVoice.stop();
  });

  global.NayaVoice = NayaVoice;
})(window);
