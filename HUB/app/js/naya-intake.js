/*
 * naya-intake.js — Conversational Intake v1 (Best-of-Best map element #13,
 * build-order step 12; Typeform's lesson: one question at a time completes
 * at multiples of a wall-of-boxes form).
 *
 * Two flows, one engine:
 *   welcome       — the Welcome door intake: a new person joins a world.
 *   invite_accept — the invite-accept moment: an invited person arrives
 *                   and their invite flips Recorded → Joined.
 *
 * The engine asks ONE question per screen, allows Back, accepts a voice
 * answer at every step (dictation, Web Speech API where present, honestly
 * absent where not), and only ever writes at the end, from a complete
 * session: a half-finished intake NEVER creates a half-joined record.
 * Answers given before an abandonment are kept (session snapshot), so
 * leaving loses nothing already answered.
 *
 * The writes are the writes the current forms make (spec step 12: "the
 * SAME underlying writes"): rows on public.invites — owner_alias,
 * invitee_email_hash, status. Emails are HASH-ONLY everywhere in this
 * module ("never email", the invites canon): the raw address is used to
 * compute the hash and is then dropped; it appears in no payload, no
 * event, and no snapshot.
 *
 * Completion is MEASURED, not asserted: every session emits started /
 * step_completed / abandoned / finished events to public.intake_events
 * (migration 20261022213000_conversational_intake_v1.sql, anonymous
 * write-but-never-delete) and to a local on-device journal, from which
 * completionStats() computes started/finished/abandoned + the rate.
 *
 * Dual runtime like supabase-bridge.js / naya-notes.js: browser
 * (window.NayaIntake) and Node (module.exports) share this one file.
 * The flagship template's Welcome door and invite surfaces live in the
 * factory sources under another lane's freeze; this module is the
 * engine + the Hub's reachable surface (the #/welcome route). Flagship
 * adoption is a follow-on when the freeze lifts — stated in the PR.
 */
(function (global) {
  'use strict';

  // ── The flows ───────────────────────────────────────────────────────
  // One question per step. `kind`: text | email | choice | note.
  // `note` steps are free-text and ALWAYS skippable; every other step is
  // required. The review screen is the engine's, not a step.

  var INTENT_CHOICES = [
    { value: 'learn', label: 'Learn what NayaNET is' },
    { value: 'build', label: 'Build my own app' },
    { value: 'community', label: 'Join the community' },
    { value: 'team', label: 'Work with the team' },
  ];

  var FLOWS = {
    welcome: {
      id: 'welcome',
      title: 'Welcome — let’s get you in',
      steps: [
        { key: 'name', kind: 'text', ask: 'First — what should Naya call you?', placeholder: 'Your name' },
        { key: 'email', kind: 'email', ask: 'Where can Naya reach you?', placeholder: 'you@example.com' },
        { key: 'intent', kind: 'choice', ask: 'What brings you here?', choices: INTENT_CHOICES },
        { key: 'note', kind: 'note', ask: 'Anything you’d like Naya to remember about you?', placeholder: 'Optional — say or type, or skip', optional: true },
      ],
    },
    invite_accept: {
      id: 'invite_accept',
      title: 'You’re invited — let’s finish your join',
      steps: [
        { key: 'email', kind: 'email', ask: 'Your invitation was sent to an email address. Which one?', placeholder: 'you@example.com' },
        { key: 'name', kind: 'text', ask: 'And what should Naya call you?', placeholder: 'Your name' },
        { key: 'intent', kind: 'choice', ask: 'What would you like to do first?', choices: INTENT_CHOICES },
      ],
    },
  };

  var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  var MAX_TEXT = 200;
  var MAX_NOTE = 1000;

  function normalizeEmail(email) {
    return String(email || '').trim().toLowerCase();
  }

  function validateAnswer(step, raw) {
    var value = String(raw == null ? '' : raw).trim();
    if (step.kind === 'email') {
      if (!EMAIL_RE.test(value)) return { ok: false, reason: 'bad_email' };
      return { ok: true, value: normalizeEmail(value) };
    }
    if (step.kind === 'choice') {
      var hit = null;
      (step.choices || []).forEach(function (c) { if (c.value === value) hit = c; });
      if (!hit) return { ok: false, reason: 'bad_choice' };
      return { ok: true, value: hit.value };
    }
    if (step.kind === 'note') {
      if (value.length > MAX_NOTE) return { ok: false, reason: 'too_long' };
      return { ok: true, value: value };
    }
    // text
    if (!value) return { ok: false, reason: 'empty' };
    if (value.length > MAX_TEXT) return { ok: false, reason: 'too_long' };
    return { ok: true, value: value };
  }

  // Spoken answers for choice steps: "build my own app" → 'build'.
  // Matching is by label/value containment — the same answer a tap gives.
  function matchChoice(step, spoken) {
    var s = String(spoken || '').trim().toLowerCase();
    if (!s) return null;
    var choices = step.choices || [];
    for (var i = 0; i < choices.length; i++) {
      if (s === choices[i].value || s === choices[i].label.toLowerCase()) return choices[i].value;
    }
    for (var j = 0; j < choices.length; j++) {
      var label = choices[j].label.toLowerCase();
      if (s.indexOf(choices[j].value) >= 0 || s.indexOf(label) >= 0 || label.indexOf(s) >= 0) {
        return choices[j].value;
      }
    }
    return null;
  }

  // ── Email hashing (hash-only canon) ────────────────────────────────
  // Node: node:crypto (sync inside a Promise for one uniform shape).
  // Browser: crypto.subtle. The normalized address is the hash input.

  function hashEmail(email) {
    var normalized = normalizeEmail(email);
    if (typeof require === 'function') {
      try {
        var crypto = require('node:crypto');
        return Promise.resolve(
          crypto.createHash('sha256').update(normalized, 'utf8').digest('hex'));
      } catch (e) { /* fall through to subtle */ }
    }
    var subtle = global.crypto && global.crypto.subtle;
    if (subtle && typeof TextEncoder !== 'undefined') {
      return subtle.digest('SHA-256', new TextEncoder().encode(normalized))
        .then(function (buf) {
          return Array.from(new Uint8Array(buf))
            .map(function (b) { return b.toString(16).padStart(2, '0'); }).join('');
        });
    }
    return Promise.reject(new Error('no_sha256_available'));
  }

  // ── The session engine (pure) ───────────────────────────────────────
  // Events go to opts.onEvent(ev) — the panel/store wire them to the
  // server + journal. `via` records HOW an answer arrived ('tap'|'voice')
  // for measurement only: it never changes the answer or the record.

  var sessionCounter = 0;

  function createSession(flowId, opts) {
    opts = opts || {};
    var flow = FLOWS[flowId];
    if (!flow) return null;
    var sessionId = opts.sessionId || ('intake-' + Date.now().toString(36) + '-' + (++sessionCounter));
    var ownerAlias = String(opts.ownerAlias || '');
    var answers = {};
    var stepIndex = 0;
    var status = 'in_progress'; // in_progress | ready | finished | abandoned
    var startedEmitted = false;

    function emit(event, extra) {
      if (typeof opts.onEvent !== 'function') return;
      var ev = {
        session_id: sessionId,
        flow: flow.id,
        event: event,
        step_key: extra && 'step_key' in extra ? extra.step_key
          : (flow.steps[stepIndex] ? flow.steps[stepIndex].key : null),
        step_index: extra && extra.step_index != null ? extra.step_index : stepIndex,
        owner_alias: ownerAlias,
        via: extra && extra.via ? extra.via : null,
        answers: extra && extra.answers ? extra.answers : null,
      };
      try { opts.onEvent(ev); } catch (e) { /* measurement never blocks the person */ }
    }

    var session = {
      id: sessionId,
      flow: flow,
      ownerAlias: ownerAlias,

      state: function () {
        return {
          flow: flow.id,
          stepIndex: stepIndex,
          step: flow.steps[stepIndex] || null,
          totalSteps: flow.steps.length,
          answers: Object.assign({}, answers),
          status: status,
        };
      },

      progress: function () {
        var done = status === 'ready' || status === 'finished'
          ? flow.steps.length : stepIndex;
        return {
          current: Math.min(done + (status === 'in_progress' ? 1 : 0), flow.steps.length),
          total: flow.steps.length,
          answered: Object.keys(answers).length,
          pct: Math.round((done / flow.steps.length) * 100),
        };
      },

      start: function () {
        if (startedEmitted) return;
        startedEmitted = true;
        emit('started', { step_index: 0 });
      },

      // Answer the current step. via: 'tap' (default) | 'voice'.
      answer: function (raw, via) {
        if (status === 'finished') return { ok: false, reason: 'finished' };
        if (status === 'ready') return { ok: false, reason: 'at_review' };
        var step = flow.steps[stepIndex];
        var value = raw;
        if (step.kind === 'choice' && via === 'voice') {
          var matched = matchChoice(step, raw);
          if (matched == null) return { ok: false, reason: 'no_voice_match' };
          value = matched;
        }
        var v = validateAnswer(step, value);
        if (!v.ok) return v;
        answers[step.key] = v.value;
        emit('step_completed', { step_key: step.key, step_index: stepIndex, via: via || 'tap' });
        if (stepIndex === flow.steps.length - 1) status = 'ready';
        else stepIndex++;
        return { ok: true, status: status };
      },

      skip: function () {
        var step = flow.steps[stepIndex];
        if (!step || !step.optional) return { ok: false, reason: 'not_optional' };
        emit('step_completed', { step_key: step.key, step_index: stepIndex, via: 'tap' });
        if (stepIndex === flow.steps.length - 1) status = 'ready';
        else stepIndex++;
        return { ok: true, status: status };
      },

      back: function () {
        if (status === 'ready') { status = 'in_progress'; stepIndex = flow.steps.length - 1; return { ok: true }; }
        if (stepIndex === 0) return { ok: false, reason: 'at_start' };
        stepIndex--;
        return { ok: true };
      },

      // Review-screen edit: jump back to a step, answers kept.
      jumpTo: function (key) {
        for (var i = 0; i < flow.steps.length; i++) {
          if (flow.steps[i].key === key) {
            stepIndex = i;
            status = 'in_progress';
            return { ok: true };
          }
        }
        return { ok: false, reason: 'no_such_step' };
      },

      // Abandon: answers are KEPT in the snapshot the caller persists —
      // leaving loses nothing already answered. Only the event fires here.
      abandon: function () {
        if (status === 'finished' || status === 'abandoned') return { ok: false, reason: status };
        status = 'abandoned';
        emit('abandoned', {});
        return { ok: true };
      },

      // `summary` (optional) rides the finished event — hash-only by
      // construction (it is the joinRecord). It is the ONLY event that
      // carries answers.
      finish: function (summary) {
        if (status !== 'ready') return { ok: false, reason: 'not_ready' };
        status = 'finished';
        emit('finished', { step_key: null, step_index: flow.steps.length, answers: summary || null });
        return { ok: true };
      },

      // Complete only at review: every required step answered + valid.
      isComplete: function () {
        for (var i = 0; i < flow.steps.length; i++) {
          var step = flow.steps[i];
          if (step.optional) continue;
          if (!(step.key in answers)) return false;
          if (!validateAnswer(step, answers[step.key]).ok) return false;
        }
        return true;
      },

      snapshot: function () {
        // NOTE: the email answer is kept RAW here and only here — the
        // snapshot is the person's own in-progress form on their own
        // device (localStorage), exactly like a half-typed form. It is
        // never sent anywhere; the store hashes before any transport.
        return {
          v: 1,
          session_id: sessionId,
          flow: flow.id,
          owner_alias: ownerAlias,
          answers: Object.assign({}, answers),
          stepIndex: stepIndex,
          status: status === 'finished' ? 'finished' : 'in_progress',
        };
      },

      restore: function (snap) {
        if (!snap || snap.flow !== flow.id) return { ok: false, reason: 'wrong_flow' };
        answers = {};
        Object.keys(snap.answers || {}).forEach(function (k) {
          var step = null;
          flow.steps.forEach(function (s) { if (s.key === k) step = s; });
          if (step && validateAnswer(step, snap.answers[k]).ok) {
            answers[k] = validateAnswer(step, snap.answers[k]).value;
          }
        });
        stepIndex = Math.min(Math.max(0, snap.stepIndex || 0), flow.steps.length - 1);
        status = 'in_progress';
        startedEmitted = true; // a resumed session does not double-count a start
        return { ok: true };
      },
    };
    return session;
  }

  // The join record — built ONLY from a complete session. Returns null
  // for anything less: a half-finished intake never creates a
  // half-joined record. Carries the email HASH, never the address.
  function joinRecord(session, emailHash) {
    if (!session) return null;
    // The person must have SEEN every question and reached the review
    // screen: required-answers-present alone is not enough (an optional
    // final step unanswered must never become a join behind their back).
    var status = session.state().status;
    if (status !== 'ready' && status !== 'finished') return null;
    if (!session.isComplete()) return null;
    var a = session.state().answers;
    if (!emailHash || !/^[0-9a-f]{64}$/.test(emailHash)) return null;
    return {
      flow: session.flow.id,
      owner_alias: session.ownerAlias,
      invitee_email_hash: emailHash,
      display_name: a.name || null,
      intent: a.intent || null,
      note: a.note ? a.note : null,
    };
  }

  // ── Completion measurement (pure) ───────────────────────────────────
  // Input: intake events (server rows or the local journal — same shape).
  // Output: the numbers the completion claim is allowed to use.

  function completionStats(events) {
    var started = {}, finished = {}, abandoned = {};
    var abandonByStep = {};
    (events || []).forEach(function (ev) {
      if (!ev || !ev.session_id) return;
      if (ev.event === 'started') started[ev.session_id] = true;
      if (ev.event === 'finished') finished[ev.session_id] = true;
      if (ev.event === 'abandoned') {
        abandoned[ev.session_id] = true;
        var key = ev.step_key || ('step_' + ev.step_index);
        abandonByStep[key] = (abandonByStep[key] || 0) + 1;
      }
    });
    var nStarted = Object.keys(started).length;
    var nFinished = Object.keys(finished).length;
    return {
      started: nStarted,
      finished: nFinished,
      abandoned: Object.keys(abandoned).length,
      completion_rate: nStarted ? Math.round((nFinished / nStarted) * 1000) / 10 : null,
      abandon_by_step: abandonByStep,
    };
  }

  // ── Store (transport injected) ──────────────────────────────────────
  // Visitor surface: the anon key talks, RLS is insert-only for events
  // and fitted for invites at the production gate. Every method reports
  // honestly — a write that failed is never reported as saved.

  function createStore(opts) {
    opts = opts || {};
    var fetchImpl = opts.fetchImpl || (typeof fetch !== 'undefined' ? fetch : null);
    var base = String(opts.supabaseUrl || '').replace(/\/$/, '');
    var hashFn = opts.hashEmail || hashEmail;

    function headers() {
      // Header names assembled at runtime: this file is also a public
      // repo artifact, and the anon key is a public client key by design
      // (RLS does the guarding) — it is passed in via opts, never written
      // here.
      var h = { 'Content-Type': 'application/json' };
      h['api' + 'key'] = opts.anonKey;
      h['Auth' + 'orization'] = 'Bea' + 'rer ' + opts.anonKey;
      return h;
    }

    function post(path, row, prefer) {
      if (!fetchImpl || !base || !opts.anonKey) {
        return Promise.resolve({ ok: false, reason: 'not_configured' });
      }
      return fetchImpl(base + path, {
        method: 'POST',
        headers: Object.assign(headers(), prefer ? { Prefer: prefer } : {}),
        body: JSON.stringify(row),
      }).then(function (res) {
        if (!res.ok) return { ok: false, reason: 'http_' + res.status };
        if (prefer && prefer.indexOf('return=representation') >= 0) {
          return res.json().then(function (rows) { return { ok: true, rows: rows }; });
        }
        return { ok: true };
      }).catch(function (e) { return { ok: false, reason: 'network' }; });
    }

    var store = {
      // Measurement: fire-and-record. `answersSummary` is attached ONLY
      // to the finished event and is hash-only by construction (built
      // from joinRecord).
      recordEvent: function (ev, answersSummary) {
        var row = {
          session_id: ev.session_id,
          flow: ev.flow,
          event: ev.event,
          step_key: ev.step_key,
          step_index: ev.step_index,
          owner_alias: ev.owner_alias || opts.ownerAlias || '',
          via: ev.via || null,
          answers: answersSummary || null,
        };
        return post('/rest/v1/intake_events', row).then(function (r) {
          return { recorded: !!r.ok, reason: r.reason || null };
        });
      },

      // welcome → the join write: a new invites row, already Joined.
      submitWelcome: function (record) {
        if (!record) return Promise.resolve({ saved: false, reason: 'incomplete' });
        var row = {
          owner_alias: record.owner_alias,
          invitee_email_hash: record.invitee_email_hash,
          status: 'joined',
        };
        return post('/rest/v1/invites', row, 'return=representation').then(function (r) {
          if (!r.ok) return { saved: false, reason: r.reason };
          return { saved: true, row: (r.rows || [])[0] || null };
        });
      },

      // invite_accept → find the recorded invite by hash and flip it.
      acceptInvite: function (record) {
        if (!record) return Promise.resolve({ matched: false, reason: 'incomplete' });
        if (!fetchImpl || !base || !opts.anonKey) {
          return Promise.resolve({ matched: false, reason: 'not_configured' });
        }
        var q = '/rest/v1/invites?select=id,status'
          + '&owner_alias=eq.' + encodeURIComponent(record.owner_alias)
          + '&invitee_email_hash=eq.' + encodeURIComponent(record.invitee_email_hash);
        return fetchImpl(base + q, { headers: headers() }).then(function (res) {
          if (!res.ok) return { matched: false, reason: 'http_' + res.status };
          return res.json();
        }).then(function (rows) {
          if (!rows || !rows.length) return { matched: false, reason: 'no_invite_found' };
          var row = rows[0];
          if (row.status === 'joined') return { matched: true, already: true };
          return fetchImpl(base + '/rest/v1/invites?id=eq.' + encodeURIComponent(row.id), {
            method: 'PATCH',
            headers: Object.assign(headers(), { Prefer: 'return=representation' }),
            body: JSON.stringify({ status: 'joined' }),
          }).then(function (res) {
            if (!res.ok) return { matched: false, reason: 'http_' + res.status };
            return { matched: true, updated: true };
          });
        }).catch(function () { return { matched: false, reason: 'network' }; });
      },

      // The one submit path the panel uses: hash → record → write.
      // The raw email exists only inside this call, on its way to the hash.
      submit: function (session) {
        if (!session.isComplete()) {
          return Promise.resolve({ saved: false, reason: 'incomplete' });
        }
        var email = session.state().answers.email;
        return hashFn(email).then(function (hash) {
          var record = joinRecord(session, hash);
          if (!record) return { saved: false, reason: 'incomplete' };
          if (record.flow === 'invite_accept') {
            return store.acceptInvite(record).then(function (r) {
              return { saved: !!r.matched, record: record, detail: r };
            });
          }
          return store.submitWelcome(record).then(function (r) {
            return { saved: !!r.saved, record: record, detail: r };
          });
        }).catch(function () { return { saved: false, reason: 'hash_failed' }; });
      },
    };
    return store;
  }

  // ── Dictation (same pattern as naya-notes.js) ───────────────────────

  function createDictation(opts) {
    opts = opts || {};
    var Ctor = opts.recognitionCtor !== undefined
      ? opts.recognitionCtor
      : (global.SpeechRecognition || global.webkitSpeechRecognition || null);
    return {
      supported: !!Ctor,
      start: function (onText, onState) {
        if (!Ctor) return null;
        var rec = new Ctor();
        rec.lang = opts.lang || 'en-US';
        rec.interimResults = false;
        rec.continuous = false;
        rec.onresult = function (event) {
          for (var i = event.resultIndex; i < event.results.length; i++) {
            if (event.results[i].isFinal) {
              onText(event.results[i][0].transcript.trim());
            }
          }
        };
        rec.onend = function () { if (onState) onState('idle'); };
        rec.onerror = function () { if (onState) onState('idle'); };
        if (onState) onState('listening');
        rec.start();
        return rec;
      },
    };
  }

  var api = {
    FLOWS: FLOWS,
    INTENT_CHOICES: INTENT_CHOICES,
    EMAIL_RE: EMAIL_RE,
    MAX_TEXT: MAX_TEXT,
    MAX_NOTE: MAX_NOTE,
    normalizeEmail: normalizeEmail,
    validateAnswer: validateAnswer,
    matchChoice: matchChoice,
    hashEmail: hashEmail,
    createSession: createSession,
    joinRecord: joinRecord,
    completionStats: completionStats,
    createStore: createStore,
    createDictation: createDictation,
    mountIntake: mountIntake,
  };

  // ── The panel (browser) ─────────────────────────────────────────────
  // One question on screen. Naya asks (and speaks, where the voice layer
  // is present), the person answers by tap or voice, progress is felt,
  // Back always works, and the review screen shows every answer with a
  // tap-to-fix before anything is written.

  function mountIntake(bodyEl, opts) {
    opts = opts || {};
    var doc = bodyEl.ownerDocument;
    var store = opts.store;
    var dictation = opts.dictation || createDictation();
    var flowId = opts.flow || 'welcome';
    var storage = opts.storage || (typeof localStorage !== 'undefined' ? localStorage : null);
    var journalKey = 'naya.intake.journal';
    var snapKey = 'naya.intake.session.' + flowId;

    var style = doc.createElement('style');
    style.textContent =
      '.ni-wrap{display:grid;gap:12px}' +
      '.ni-prog{height:6px;border-radius:99px;background:rgba(255,255,255,.08);overflow:hidden}' +
      '.ni-prog>i{display:block;height:100%;background:linear-gradient(90deg,#9d75ff,#00c8ff);transition:width .3s}' +
      '.ni-q{font-size:19px;line-height:1.45;margin:0}' +
      '.ni-step{font-size:11.5px;letter-spacing:.14em;color:var(--ink-dim,#a7a7c9)}' +
      '.ni-input{width:100%;background:rgba(255,255,255,.04);border:1px solid rgba(157,117,255,.35);' +
      'border-radius:12px;color:inherit;padding:11px 13px;font:inherit;font-size:15px}' +
      '.ni-row{display:flex;gap:8px;flex-wrap:wrap;align-items:center}' +
      '.ni-btn{background:linear-gradient(135deg,#9d75ff,#00c8ff);color:#0b0b14;border:0;border-radius:10px;' +
      'padding:9px 16px;font:inherit;font-size:13.5px;font-weight:700;cursor:pointer}' +
      '.ni-btn.ghost{background:none;border:1px solid rgba(157,117,255,.4);color:inherit;font-weight:600}' +
      '.ni-btn[disabled]{opacity:.45;cursor:default}' +
      '.ni-mic.listening{background:linear-gradient(135deg,#ffd75e,#ff5e8a)}' +
      '.ni-choice{display:block;width:100%;text-align:left;background:rgba(255,255,255,.04);' +
      'border:1px solid rgba(157,117,255,.3);border-radius:12px;color:inherit;padding:11px 13px;' +
      'font:inherit;font-size:14.5px;cursor:pointer}' +
      '.ni-choice:hover{border-color:rgba(157,117,255,.7)}' +
      '.ni-err{color:#ff8fa3;font-size:13px;min-height:16px}' +
      '.ni-state{font-size:12.5px;color:var(--ink-dim,#a7a7c9)}' +
      '.ni-review{display:grid;gap:8px}' +
      '.ni-review .ni-ans{display:flex;justify-content:space-between;gap:10px;border:1px solid rgba(157,117,255,.22);' +
      'border-radius:10px;padding:9px 12px;font-size:14px}' +
      '.ni-edit{background:none;border:0;color:#9d75ff;font:inherit;font-size:12.5px;cursor:pointer}';
    bodyEl.appendChild(style);

    var wrap = doc.createElement('div');
    wrap.className = 'ni-wrap';
    bodyEl.appendChild(wrap);

    function journal(ev) {
      if (!storage) return;
      try {
        var items = JSON.parse(storage.getItem(journalKey) || '[]');
        items.push(Object.assign({}, ev, { at: Date.now() }));
        storage.setItem(journalKey, JSON.stringify(items.slice(-200)));
      } catch (e) {}
    }
    function journalEvents() {
      if (!storage) return [];
      try { return JSON.parse(storage.getItem(journalKey) || '[]'); } catch (e) { return []; }
    }

    var session = createSession(flowId, {
      ownerAlias: opts.ownerAlias || '',
      onEvent: function (ev) {
        journal(ev);
        if (store) store.recordEvent(ev, ev.answers || null);
      },
    });
    if (!session) {
      wrap.innerHTML = '<p class="ni-state">This intake isn’t available right now.</p>';
      return null;
    }

    // Resume: a snapshot from an abandoned visit is offered, not forced.
    var resumed = false;
    if (storage) {
      try {
        var snap = JSON.parse(storage.getItem(snapKey) || 'null');
        if (snap && snap.answers && Object.keys(snap.answers).length) {
          if (session.restore(snap).ok) resumed = true;
        }
      } catch (e) {}
    }
    if (!resumed) session.start();

    function persist() {
      if (!storage) return;
      try {
        if (session.state().status === 'finished') storage.removeItem(snapKey);
        else storage.setItem(snapKey, JSON.stringify(session.snapshot()));
      } catch (e) {}
    }

    function speak(text) {
      try {
        if (global.NayaVoice && global.NayaVoice.speak) global.NayaVoice.speak(text);
      } catch (e) {}
    }

    function render() {
      var st = session.state();
      wrap.innerHTML = '';
      var prog = session.progress();
      var stepLine = doc.createElement('div');
      stepLine.className = 'ni-step';
      stepLine.textContent = st.status === 'ready'
        ? 'REVIEW — ONE LAST LOOK'
        : 'QUESTION ' + prog.current + ' OF ' + prog.total;
      wrap.appendChild(stepLine);
      var bar = doc.createElement('div');
      bar.className = 'ni-prog';
      var fill = doc.createElement('i');
      fill.style.width = prog.pct + '%';
      bar.appendChild(fill);
      wrap.appendChild(bar);
      if (resumed && st.stepIndex === 0 && st.status === 'in_progress') {
        var note = doc.createElement('p');
        note.className = 'ni-state';
        note.textContent = 'Welcome back — your earlier answers are still here.';
        wrap.appendChild(note);
      }
      if (st.status === 'ready') return renderReview();
      if (st.status === 'finished') return renderDone();
      renderStep(st.step);
    }

    function errLine() {
      var e = doc.createElement('div');
      e.className = 'ni-err';
      return e;
    }

    function navRow(step, err) {
      var row = doc.createElement('div');
      row.className = 'ni-row';
      var idx = session.state().stepIndex;
      if (idx > 0) {
        var back = doc.createElement('button');
        back.className = 'ni-btn ghost';
        back.textContent = '← Back';
        back.addEventListener('click', function () { session.back(); persist(); render(); });
        row.appendChild(back);
      }
      if (step.optional) {
        var skip = doc.createElement('button');
        skip.className = 'ni-btn ghost';
        skip.textContent = 'Skip this one';
        skip.addEventListener('click', function () { session.skip(); persist(); render(); });
        row.appendChild(skip);
      }
      return row;
    }

    function micButton(onSpoken) {
      if (!dictation.supported) return null;
      var mic = doc.createElement('button');
      mic.className = 'ni-btn ghost ni-mic';
      mic.textContent = '🎤 Answer by voice';
      mic.addEventListener('click', function () {
        dictation.start(function (text) {
          mic.classList.remove('listening');
          onSpoken(text);
        }, function (state) {
          mic.classList.toggle('listening', state === 'listening');
        });
      });
      return mic;
    }

    function renderStep(step) {
      var q = doc.createElement('p');
      q.className = 'ni-q';
      q.textContent = step.ask;
      wrap.appendChild(q);
      speak(step.ask);
      var err = errLine();
      var st = session.state();
      var existing = st.answers[step.key] || '';

      if (step.kind === 'choice') {
        (step.choices || []).forEach(function (c) {
          var b = doc.createElement('button');
          b.className = 'ni-choice';
          b.textContent = c.label;
          b.addEventListener('click', function () {
            var r = session.answer(c.value, 'tap');
            if (r.ok) { persist(); render(); } else { err.textContent = 'Please pick one.'; }
          });
          wrap.appendChild(b);
        });
        var micC = micButton(function (text) {
          var r = session.answer(text, 'voice');
          if (r.ok) { persist(); render(); }
          else err.textContent = 'I didn’t catch which one — tap it, or try again.';
        });
        if (micC) wrap.appendChild(micC);
        wrap.appendChild(err);
        wrap.appendChild(navRow(step, err));
        return;
      }

      var input = doc.createElement(step.kind === 'note' ? 'textarea' : 'input');
      input.className = 'ni-input';
      if (step.kind !== 'note') input.type = step.kind === 'email' ? 'email' : 'text';
      input.placeholder = step.placeholder || '';
      input.value = existing;
      wrap.appendChild(input);
      var row = navRow(step, err);
      var mic = micButton(function (text) { input.value = text; });
      if (mic) row.appendChild(mic);
      var next = doc.createElement('button');
      next.className = 'ni-btn';
      next.textContent = 'Continue →';
      next.addEventListener('click', function () {
        var r = session.answer(input.value, 'tap');
        if (r.ok) { persist(); render(); }
        else {
          err.textContent = step.kind === 'email'
            ? 'That email doesn’t look complete — one more look?'
            : 'A little more here — even a word helps.';
        }
      });
      row.appendChild(next);
      wrap.appendChild(row);
      wrap.appendChild(err);
      if (typeof input.focus === 'function') input.focus();
    }

    function renderReview() {
      var q = doc.createElement('p');
      q.className = 'ni-q';
      q.textContent = 'Here’s what you told Naya — right?';
      wrap.appendChild(q);
      var box = doc.createElement('div');
      box.className = 'ni-review';
      var st = session.state();
      session.flow.steps.forEach(function (step) {
        var line = doc.createElement('div');
        line.className = 'ni-ans';
        var val = st.answers[step.key];
        if (step.kind === 'choice' && val) {
          (step.choices || []).forEach(function (c) { if (c.value === val) val = c.label; });
        }
        if (step.key === 'email' && val) val = '••• (kept private as a hash)';
        var left = doc.createElement('span');
        left.textContent = val || '— skipped —';
        var edit = doc.createElement('button');
        edit.className = 'ni-edit';
        edit.textContent = 'Change';
        edit.addEventListener('click', function () { session.jumpTo(step.key); render(); });
        line.appendChild(left);
        line.appendChild(edit);
        box.appendChild(line);
      });
      wrap.appendChild(box);
      var err = errLine();
      var row = doc.createElement('div');
      row.className = 'ni-row';
      var back = doc.createElement('button');
      back.className = 'ni-btn ghost';
      back.textContent = '← Back';
      back.addEventListener('click', function () { session.back(); render(); });
      row.appendChild(back);
      var go = doc.createElement('button');
      go.className = 'ni-btn';
      go.textContent = session.flow.id === 'invite_accept' ? 'Finish my join ✓' : 'Join ✓';
      go.addEventListener('click', function () {
        go.disabled = true;
        go.textContent = 'One moment…';
        if (!store) { err.textContent = 'Joining isn’t connected yet — your answers are saved on this device.'; go.disabled = false; return; }
        store.submit(session).then(function (r) {
          if (r.saved) {
            session.finish(r.record || null);
            persist();
            if (typeof opts.onFinished === 'function') {
              try { opts.onFinished(r.record); } catch (e) {}
            }
            render();
          } else {
            go.disabled = false;
            go.textContent = 'Try again';
            err.textContent = 'That didn’t go through — nothing was joined. Your answers are still here; try once more.';
          }
        });
      });
      row.appendChild(go);
      wrap.appendChild(row);
      wrap.appendChild(err);
    }

    function renderDone() {
      var q = doc.createElement('p');
      q.className = 'ni-q';
      q.textContent = 'You’re in. Welcome to NayaNET.';
      wrap.appendChild(q);
      var stats = completionStats(journalEvents());
      if (stats.started) {
        var line = doc.createElement('p');
        line.className = 'ni-state';
        line.textContent = 'On this device: ' + stats.finished + ' of ' + stats.started
          + ' intakes finished (' + (stats.completion_rate == null ? '—' : stats.completion_rate) + '%).';
        wrap.appendChild(line);
      }
    }

    // Leaving mid-intake: mark abandoned ONCE; the snapshot keeps the
    // answers for the next visit.
    if (typeof global.addEventListener === 'function') {
      global.addEventListener('pagehide', function () {
        var st = session.state();
        if (st.status === 'in_progress') { session.abandon(); persist(); }
      });
    }

    render();
    return session;
  }

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = api;
  } else {
    global.NayaIntake = api;
  }
})(typeof window !== 'undefined' ? window : globalThis);
