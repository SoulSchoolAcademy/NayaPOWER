(() => {
  'use strict';
  const KEY = 'nayanet:e01:v2';
  const $ = (s) => document.querySelector(s);
  const sections = { arrival: $('#arrival'), identity: $('#identity'), reveal: $('#reveal'), naya: $('#nayaRoom'), home: $('#toolbox') };
  const sun = $('#sun'), sunState = $('#sunState'), sunMessage = $('#sunMessage'), toast = $('#toast');
  let state = { stage: 'arrival', name: '', smartName: '', smartLink: '' };
  let lastStage = 'arrival';

  function load() {
    try {
      const saved = JSON.parse(localStorage.getItem(KEY) || '{}');
      state = { ...state, ...saved };
      if (state.name && state.stage === 'home') show('home', false);
      else if (state.name && state.stage === 'identityCreated') show('reveal', false);
      else show('arrival', false);
    } catch (_) { show('arrival', false); }
  }

  function save() {
    try { localStorage.setItem(KEY, JSON.stringify(state)); }
    catch (_) { toastMsg('Storage is unavailable. You can keep going, but this identity will not persist.'); }
  }

  function slug(name) {
    return (name || 'friend').toLowerCase().trim().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') || 'friend';
  }

  function setSun(mode, message) {
    const labels = {
      RESTING: 'Naya is here when you\'re ready.', ATTENTION: 'Naya is paying attention.', LISTENING: 'Naya is listening.',
      SUCCESS: 'Your first connection is ready.', WARNING: 'This part is coming next.', ERROR: 'Something needs your attention.'
    };
    sun.dataset.state = mode;
    sunState.textContent = mode;
    sunMessage.textContent = message || labels[mode] || labels.RESTING;
    sun.setAttribute('aria-label', `Naya is ${mode.toLowerCase()}. ${sunMessage.textContent}`);
  }

  function toastMsg(message) {
    toast.textContent = message;
    toast.classList.add('show');
    clearTimeout(toast.t);
    toast.t = setTimeout(() => toast.classList.remove('show'), 3200);
  }

  function show(which, remember = true) {
    Object.entries(sections).forEach(([key, section]) => { section.hidden = key !== which; });
    if (remember) lastStage = state.stage || lastStage;
    state.stage = which === 'home' ? 'home' : which === 'reveal' ? 'identityCreated' : which;
    if (which === 'arrival') { setSun('RESTING'); window.scrollTo({ top: 0, behavior: motion() ? 'smooth' : 'auto' }); }
    if (which === 'identity') {
      setSun('LISTENING');
      window.scrollTo({ top: 0, behavior: motion() ? 'smooth' : 'auto' });
      setTimeout(() => $('#nameInput')?.focus(), 80);
    }
    if (which === 'reveal') {
      $('#revealedName').textContent = state.name;
      $('#smartName').textContent = state.smartName;
      $('#smartLink').textContent = state.smartLink;
      setSun('SUCCESS');
      window.scrollTo({ top: 0, behavior: motion() ? 'smooth' : 'auto' });
    }
    if (which === 'home') {
      $('#toolName').textContent = state.name.toUpperCase();
      setSun('ATTENTION', `Welcome, ${state.name}. Your toolbox is ready.`);
      window.scrollTo({ top: 0, behavior: motion() ? 'smooth' : 'auto' });
    }
    if (which === 'naya') {
      setSun('ATTENTION', state.name ? `Good to meet you, ${state.name}.` : 'Naya is here. Start wherever you are.');
      window.scrollTo({ top: 0, behavior: motion() ? 'smooth' : 'auto' });
    }
  }

  function motion() { return !window.matchMedia('(prefers-reduced-motion: reduce)').matches; }

  function future(label) {
    setSun('WARNING', `${label} is coming next. Nothing is being simulated here.`);
    toastMsg(`${label} is coming next. This E01 room will not pretend it is already live.`);
  }

  $('#createCta').onclick = () => show('identity');
  $('#meetCta').onclick = () => show('naya');
  $('#identityBack').onclick = () => show('arrival');

  $('#identityForm').onsubmit = (event) => {
    event.preventDefault();
    const input = $('#nameInput');
    const name = input.value.trim();
    if (name.length < 2) { $('#nameError').textContent = 'Please enter at least two characters.'; setSun('ERROR', 'Please add a little more to your name.'); input.focus(); return; }
    if (name.length > 80) { $('#nameError').textContent = 'Please use a shorter name.'; setSun('ERROR', 'That name is longer than this first step needs.'); input.focus(); return; }
    $('#nameError').textContent = '';
    const normalized = slug(name);
    state.name = name;
    state.smartName = `naya/${normalized}`;
    state.smartLink = `nayanet.xyz/${normalized}`;
    save();
    show('reveal');
  };

  $('#copyLink').onclick = async () => {
    const value = state.smartLink;
    try {
      if (!navigator.clipboard?.writeText) throw new Error('clipboard unavailable');
      await navigator.clipboard.writeText(value);
      toastMsg('Smart Link copied.');
    } catch (_) {
      const code = $('#smartLink');
      const range = document.createRange();
      range.selectNodeContents(code);
      const sel = window.getSelection();
      sel.removeAllRanges(); sel.addRange(range);
      toastMsg('Clipboard is unavailable. The Smart Link is selected for you.');
    }
  };

  $('#toolboxCta').onclick = () => show('home');
  $('#revealMeet').onclick = () => show('naya');
  $('#nayaStart').onclick = () => state.name ? show('reveal') : show('identity');
  $('#nayaBack').onclick = () => show(state.name ? 'reveal' : 'arrival');
  $('#sun').onclick = () => { setSun('ATTENTION', 'Naya is paying attention.'); toastMsg('Naya is paying attention.'); };
  $('#brandHome').onclick = () => show(state.name ? 'home' : 'arrival');

  $('#toolNaya').onclick = () => show('naya');
  $('#toolChallenge').onclick = () => future('The Five-Day Challenge');
  $('#toolPower').onclick = () => future('Naya Power');
  $('#toolAsk').onclick = () => future('Ask Naya');
  $('#toolIntelligence').onclick = () => future('My Intelligence');
  $('#toolNotes').onclick = () => future('My Notes');
  $('#toolReport').onclick = () => future('Daily Report');
  $('#toolConnect').onclick = () => future('Connect');
  $('#nextAction').onclick = () => future('The Five-Day Challenge');
  $('#nextPower').onclick = () => future('Naya Power');
  $('#nextExplore').onclick = () => show('home');

  $('#resetIdentity').onclick = () => {
    if (!window.confirm('Reset only this local E01 identity?')) return;
    state = { stage: 'arrival', name: '', smartName: '', smartLink: '' };
    try { localStorage.removeItem(KEY); localStorage.removeItem('nayanet:e01:v1'); } catch (_) {}
    show('arrival');
    toastMsg('Local E01 identity reset.');
  };

  load();
})();
