(() => {
  'use strict';

  /* NayaNET — Legendary Threshold Controller
     One deterministic state machine drives the entrance:
     IDLE -> ACTIVE -> READY -> ENTERING.
     Visual intensity is a response to real human interaction, not randomness.
     Identity remains browser-local until authenticated server capabilities exist.
  */

  const NAME = 'nayanetName';
  const LEGACY = 'nayanet_name';
  const STATE = 'nayanet:intelligence:v1';
  const TRANSITION_MS = 1080;

  const frontDoor = document.getElementById('frontDoor');
  const form = document.getElementById('entryForm');
  const input = document.getElementById('nameInput');
  if (!frontDoor || !form || !input) return;

  const portal = form.querySelector('.portal-input');
  const button = form.querySelector('button[type="submit"]');
  const chamber = frontDoor.querySelector('.threshold-chamber');
  const ring = frontDoor.querySelector('.jewel-ring');
  const doors = [...frontDoor.querySelectorAll('.threshold-doors button')];
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

  const clean = value => String(value || '').replace(/\s+/g, ' ').trim().slice(0, 80);

  const setState = state => {
    frontDoor.dataset.nnState = state;
    frontDoor.dataset.state = state;
  };

  const setEnergy = value => {
    const n = Math.max(0, Math.min(1, Number(value) || 0));
    frontDoor.style.setProperty('--nn-energy', n.toFixed(3));
  };

  const setPointer = (x, y) => {
    frontDoor.style.setProperty('--nn-pointer-x', `${x}%`);
    frontDoor.style.setProperty('--nn-pointer-y', `${y}%`);
  };

  const readSavedName = () => {
    try { return clean(localStorage.getItem(NAME) || localStorage.getItem(LEGACY)); }
    catch (_) { return ''; }
  };

  const saveIdentity = name => {
    try {
      localStorage.setItem(NAME, name);
      localStorage.setItem(LEGACY, name);
      const state = JSON.parse(localStorage.getItem(STATE) || '{}');
      state.name = name;
      state.lastSeen = Date.now();
      localStorage.setItem(STATE, JSON.stringify(state));
    } catch (_) {}
  };

  const sync = () => {
    const name = clean(input.value);
    const ready = name.length > 0;
    if (portal) portal.dataset.state = ready ? 'ready' : 'idle';
    if (button) {
      button.disabled = !ready;
      button.setAttribute('aria-disabled', String(!ready));
    }
    if (frontDoor.dataset.state !== 'entering') {
      setState(document.activeElement === input ? 'active' : (ready ? 'ready' : 'idle'));
    }
    setEnergy(!ready ? .18 : (document.activeElement === input ? .66 : .48));
  };

  const awaken = amount => {
    setEnergy(Math.max(.18, Math.min(.92, amount)));
    if (!reducedMotion.matches) {
      frontDoor.style.setProperty('--nn-ring-scale', amount > .7 ? '1.018' : '1.006');
    }
  };

  const activatePresence = () => {
    if (frontDoor.dataset.state === 'entering') return;
    setState('active');
    awaken(.68);
  };

  const resetPresence = () => {
    if (frontDoor.dataset.state === 'entering') return;
    sync();
  };

  const handlePointer = event => {
    if (frontDoor.dataset.state === 'entering') return;
    const rect = frontDoor.getBoundingClientRect();
    const x = ((event.clientX - rect.left) / rect.width) * 100;
    const y = ((event.clientY - rect.top) / rect.height) * 100;
    setPointer(Math.max(0, Math.min(100, x)), Math.max(0, Math.min(100, y)));
    if (chamber) {
      const dx = event.clientX - (rect.left + rect.width / 2);
      const dy = event.clientY - (rect.top + rect.height / 2);
      const distance = Math.sqrt(dx * dx + dy * dy) / (rect.width / 2);
      const proximity = Math.max(0, 1 - Math.min(1.5, distance));
      awaken(.18 + proximity * .34 + (input === document.activeElement ? .18 : 0));
    }
  };

  const selectDoor = door => {
    doors.forEach(item => {
      const selected = item === door;
      item.classList.toggle('is-selected', selected);
      item.setAttribute('aria-pressed', String(selected));
    });
    activatePresence();
    awaken(.76);
  };

  const beginEntry = () => {
    if (frontDoor.dataset.state === 'entering') return;
    const name = clean(input.value);
    if (!name) {
      input.focus();
      activatePresence();
      return;
    }

    saveIdentity(name);
    setState('entering');
    setEnergy(1);
    if (portal) portal.dataset.state = 'entering';
    if (button) {
      button.disabled = true;
      button.setAttribute('aria-disabled', 'true');
      button.setAttribute('aria-busy', 'true');
      button.dataset.state = 'entering';
    }
    doors.forEach(item => item.setAttribute('aria-disabled', 'true'));
    document.body.classList.add('nayanet-entering');
    frontDoor.setAttribute('aria-busy', 'true');
    if (ring) ring.setAttribute('data-entry', 'charging');

    window.setTimeout(() => { window.location.assign('/hub.html'); }, reducedMotion.matches ? 80 : TRANSITION_MS);
  };

  const saved = readSavedName();
  if (saved) input.value = saved;
  setPointer(50, 50);
  sync();

  frontDoor.addEventListener('pointermove', handlePointer, { passive: true });
  frontDoor.addEventListener('pointerleave', resetPresence, { passive: true });
  frontDoor.addEventListener('pointerenter', activatePresence, { passive: true });

  input.addEventListener('focus', () => { activatePresence(); awaken(.72); });
  input.addEventListener('input', () => {
    const name = clean(input.value);
    if (portal) portal.dataset.state = name ? 'active' : 'idle';
    setState('active');
    awaken(name ? Math.min(.92, .52 + name.length / 100) : .52);
    sync();
    if (name) setState('active');
  });
  input.addEventListener('blur', sync);
  input.addEventListener('keydown', event => {
    if (event.key === 'Enter' && !button?.disabled) {
      event.preventDefault();
      form.requestSubmit();
    }
  });

  doors.forEach(door => door.addEventListener('click', () => selectDoor(door)));

  form.addEventListener('submit', event => {
    event.preventDefault();
    beginEntry();
  });

  window.addEventListener('pageshow', () => {
    if (frontDoor.dataset.state === 'entering') {
      setState('ready');
      document.body.classList.remove('nayanet-entering');
      doors.forEach(item => item.setAttribute('aria-disabled', 'false'));
      sync();
    }
  });

  window.NayaNETThreshold = Object.freeze({
    version: '2.1.0',
    state: () => frontDoor.dataset.state || 'idle',
    enter: beginEntry,
    refresh: sync
  });
})();
