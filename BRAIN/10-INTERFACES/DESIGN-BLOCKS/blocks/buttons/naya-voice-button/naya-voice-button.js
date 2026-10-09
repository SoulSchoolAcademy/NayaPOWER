/* Smart Block: naya-voice-button — voice read-aloud control.
   Wires `.naya-button` to speech synthesis with honest states, and exposes the
   hooks the assessment needs: stop-on-navigate, Escape, and tab-hidden all
   stop playback. No framework required. */
(function () {
  'use strict';

  var RATE = 0.92;
  var PITCH = 1.02;

  function buttons() {
    return Array.prototype.slice.call(
      document.querySelectorAll('.naya-button')
    );
  }

  function setState(btn, mode) {
    // mode: 'idle' | 'playing' | 'paused'
    btn.classList.toggle('playing', mode === 'playing');
    btn.classList.toggle('paused', mode === 'paused');
    btn.setAttribute('aria-pressed', mode === 'playing' ? 'true' : 'false');
    var primary = btn.querySelector('.naya-primary');
    var secondary = btn.querySelector('.naya-secondary');
    var labels = {
      idle: ['Press Play', 'Listen to Naya'],
      playing: ['Pause Naya', 'Naya is speaking'],
      paused: ['Resume', 'Paused']
    }[mode] || ['Press Play', 'Listen to Naya'];
    if (primary) { primary.textContent = labels[0]; }
    if (secondary) { secondary.textContent = labels[1]; }
  }

  function isPlaying(btn) {
    return btn.classList.contains('playing');
  }

  function isPaused(btn) {
    return btn.classList.contains('paused');
  }

  function stopAll() {
    if ('speechSynthesis' in window) {
      try { window.speechSynthesis.cancel(); } catch (e) { /* noop */ }
    }
    buttons().forEach(function (btn) { setState(btn, 'idle'); });
  }

  function speak(text, btn) {
    if (!('speechSynthesis' in window)) { return false; }
    var target = btn || buttons()[0];
    if (!target || typeof text !== 'string' || !text) { return false; }
    stopAll();
    var utter = new SpeechSynthesisUtterance(text);
    utter.rate = RATE;
    utter.pitch = PITCH;
    utter.volume = 1;
    utter.onstart = function () { setState(target, 'playing'); };
    utter.onend = function () { setState(target, 'idle'); };
    utter.onerror = function () { setState(target, 'idle'); };
    try {
      window.speechSynthesis.speak(utter);
    } catch (e) {
      setState(target, 'idle');
      return false;
    }
    return true;
  }

  function toggle(btn) {
    var target = btn || buttons()[0];
    if (!target) { return; }
    if (!('speechSynthesis' in window)) { return; }
    if (isPlaying(target)) {
      // Pause: freeze mid-utterance, keep the orb in `.paused`.
      try { window.speechSynthesis.pause(); } catch (e) { /* noop */ }
      setState(target, 'paused');
      return;
    }
    if (isPaused(target)) {
      try { window.speechSynthesis.resume(); } catch (e) { /* noop */ }
      setState(target, 'playing');
      return;
    }
    // Idle: ask the host app what to read. The assessment answers by calling
    // NayaVoiceButton.speak(questionText) — this block never guesses content.
    var ev;
    if (typeof CustomEvent === 'function') {
      ev = new CustomEvent('naya-voice-request', { bubbles: true, cancelable: true });
    } else {
      ev = document.createEvent('CustomEvent');
      ev.initCustomEvent('naya-voice-request', true, true, null);
    }
    target.dispatchEvent(ev);
  }

  function setVoiceKind(btn, kind) {
    // kind: 'synthesized' (default, honest) or 'cloned' (Naya's real voice,
    // only when wired to the canonical voice service).
    var target = btn || buttons()[0];
    if (!target) { return; }
    var value = kind === 'cloned' ? 'cloned' : 'synthesized';
    target.setAttribute('data-voice-kind', value);
    var badge = target.querySelector('.naya-voice-kind');
    if (badge) {
      badge.textContent = value === 'cloned' ? "Naya's voice" : 'Synthesized voice';
    }
  }

  function wire() {
    buttons().forEach(function (btn) {
      if (btn._nvWired) { return; }
      btn._nvWired = true;
      if (!btn.hasAttribute('data-voice-kind')) {
        btn.setAttribute('data-voice-kind', 'synthesized');
      }
      btn.addEventListener('click', function () { toggle(btn); });
    });
  }

  // Stop-on-navigate hooks: question navigation dispatches `naya-voice-stop`
  // on window before rendering the next question; Escape and tab-hidden are
  // safety nets so audio never leaks across views.
  if (typeof window !== 'undefined') {
    window.addEventListener('naya-voice-stop', stopAll);
  }
  document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape') { stopAll(); }
  });
  if (typeof document.hidden !== 'undefined') {
    document.addEventListener('visibilitychange', function () {
      if (document.hidden) { stopAll(); }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', wire);
  } else {
    wire();
  }

  window.NayaVoiceButton = {
    speak: speak,
    stop: stopAll,
    toggle: toggle,
    setVoiceKind: setVoiceKind,
    rewire: wire
  };
})();
