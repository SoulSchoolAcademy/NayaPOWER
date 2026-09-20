(() => {
  'use strict';

  const STORAGE_NAME = 'nayanetName';
  const STORAGE_NAME_LEGACY = 'nayanet_name';
  const INTELLIGENCE_KEY = 'nayanet:intelligence:v1';
  const FRONT_DOOR_STYLE = '/nayanet-front-door-overhaul.css';

  const loadStyle = () => {
    if (document.querySelector(`link[href="${FRONT_DOOR_STYLE}"]`)) return;
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = FRONT_DOOR_STYLE;
    document.head.appendChild(link);
  };

  const boot = () => {
    loadStyle();
    const form = document.getElementById('entryForm');
    const input = document.getElementById('nameInput');
    const frontDoor = document.getElementById('frontDoor');
    const hub = document.getElementById('hub');
    const greeting = document.getElementById('hubGreeting');
    const userName = document.getElementById('userName');
    if (!form || !input || !frontDoor || !hub) return;

    const readName = () => {
      try {
        const local = localStorage.getItem(STORAGE_NAME) || localStorage.getItem(STORAGE_NAME_LEGACY) || '';
        if (local.trim()) return local.trim();
        const state = JSON.parse(localStorage.getItem(INTELLIGENCE_KEY) || '{}');
        return String(state.name || '').trim();
      } catch (_) { return ''; }
    };

    const setName = (name) => {
      const clean = String(name || '').replace(/\s+/g, ' ').trim().slice(0, 80);
      if (!clean) return false;
      localStorage.setItem(STORAGE_NAME, clean);
      localStorage.setItem(STORAGE_NAME_LEGACY, clean);
      try {
        const state = JSON.parse(localStorage.getItem(INTELLIGENCE_KEY) || '{}');
        state.name = clean;
        state.lastSeen = Date.now();
        localStorage.setItem(INTELLIGENCE_KEY, JSON.stringify(state));
      } catch (_) {}
      return clean;
    };

    const existing = readName();
    if (existing) input.value = existing;

    const updateButton = () => {
      const button = form.querySelector('button[type="submit"]');
      if (!button) return;
      const ready = input.value.trim().length > 0;
      button.disabled = !ready;
      button.setAttribute('aria-disabled', String(!ready));
    };
    input.addEventListener('input', updateButton);
    input.addEventListener('keydown', (event) => {
      if (event.key === 'Escape') {
        input.value = '';
        updateButton();
      }
    });
    updateButton();

    const enter = (event) => {
      if (event) event.preventDefault();
      const name = setName(input.value);
      if (!name) {
        input.focus();
        input.setAttribute('aria-invalid', 'true');
        return;
      }
      input.setAttribute('aria-invalid', 'false');
      const submit = form.querySelector('button[type="submit"]');
      if (submit) {
        submit.setAttribute('data-state', 'entering');
        submit.setAttribute('aria-busy', 'true');
      }
      document.body.classList.add('nayanet-entering');
      frontDoor.setAttribute('aria-hidden', 'true');
      window.setTimeout(() => {
        frontDoor.hidden = true;
        frontDoor.style.display = 'none';
        hub.hidden = false;
        hub.style.removeProperty('display');
        hub.setAttribute('aria-hidden', 'false');
        if (greeting) greeting.textContent = `Welcome, ${name}. Your intelligence has a home.`;
        if (userName) userName.textContent = name.toUpperCase();
        document.body.classList.remove('nayanet-entering');
        document.body.classList.add('nayanet-inside');
        window.scrollTo({ top: 0, behavior: 'instant' });
        window.dispatchEvent(new CustomEvent('nayanet:entered', { detail: { name } }));
        try { window.dispatchEvent(new CustomEvent('naya:data-save')); } catch (_) {}
      }, 720);
    };

    form.addEventListener('submit', enter);

    document.querySelectorAll('.threshold-doors [data-preview]').forEach((button) => {
      button.addEventListener('click', () => {
        document.querySelectorAll('.threshold-doors [data-preview]').forEach((item) => item.classList.remove('is-selected'));
        button.classList.add('is-selected');
        const selectedText = button.querySelector('strong');
        if (selectedText) selectedText.style.color = '#fff';
        const key = button.dataset.preview;
        const messages = {
          naya: 'Naya is the intelligence partner at the center.',
          brain: 'Your context compounds instead of starting over.',
          identity: 'Your Smart Identity is your doorway into the network.',
          player: 'Power Player keeps the ideas moving with you.',
          network: 'Connection happens by permission, not exposure.'
        };
        const invitation = document.querySelector('.threshold-invitation');
        if (invitation && messages[key]) invitation.innerHTML = `Naya says: <span>${messages[key]}</span>`;
      });
    });
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot, { once: true });
  else boot();
})();
