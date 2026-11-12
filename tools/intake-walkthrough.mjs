// intake-walkthrough.mjs — the scripted old-vs-new comparison for
// Conversational Intake v1 (element #13). Run: node tools/intake-walkthrough.mjs
//
// WHAT IS MEASURED (countable mechanics, from the engine itself):
//   screens shown · fields demanded per screen · where a bad answer is
//   caught · whether a review exists before the write · events emitted.
// WHAT IS *NOT* MEASURED: human completion rates — those come from
// intake_events once the migration applies (the instrumentation this
// build ships). The OLD model is the one-screen form demanding the same
// answer set at once (the pattern the map's Part 2 verified in every
// intake surface: "forms are multi-field everywhere except Ask Naya").
// Typeform's published 2.5–3× completion advantage is the evidence the
// DESIGN follows; this script proves the mechanics that produce it.

import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const NI = require('../HUB/app/js/naya-intake.js');

function oldModel(flowId) {
  const n = NI.FLOWS[flowId].steps.length;
  return {
    screens: 1,
    fieldsPerScreen: n, // the whole answer set demanded on one screen
    totalFields: n,
    mistakesCaughtAtStep: 0, // a bad email surfaces only at submit, form-wide
    reviewBeforeWrite: false,
    events: [], // the old forms emit nothing: completion was unmeasured
  };
}

// The scripted persona answers name → email (deliberately mistyped once;
// the engine catches it AT that step and the persona corrects it on the
// same screen) → intent → note, then reaches the review screen.
const newWelcome = (() => {
  const events = [];
  const s = NI.createSession('welcome', { ownerAlias: 'walkthrough', onEvent: (e) => events.push(e) });
  s.start();
  let screens = 0, caught = 0;
  const answers = ['Maria', 'maria@exampl', 'build', 'I run a bakery'];
  for (const raw of answers) {
    screens++;
    const r = s.answer(raw);
    if (!r.ok) { caught++; screens++; s.answer('maria@example.com'); }
  }
  return {
    screens: screens + 1, // + the review screen
    fieldsPerScreen: 1,
    totalFields: NI.FLOWS.welcome.steps.length,
    mistakesCaughtAtStep: caught,
    reviewBeforeWrite: s.state().status === 'ready',
    events: events.map((e) => e.event),
  };
})();

const oldWelcome = oldModel('welcome');

console.log('CONVERSATIONAL INTAKE v1 — SCRIPTED WALKTHROUGH (welcome flow)');
console.log('metric                        OLD one-screen form   NEW conversation');
const rows = [
  ['screens to finish', oldWelcome.screens, newWelcome.screens],
  ['fields demanded per screen', oldWelcome.fieldsPerScreen, newWelcome.fieldsPerScreen],
  ['total fields', oldWelcome.totalFields, newWelcome.totalFields],
  ['bad answer caught at its step', oldWelcome.mistakesCaughtAtStep, newWelcome.mistakesCaughtAtStep],
  ['review before the write', oldWelcome.reviewBeforeWrite, newWelcome.reviewBeforeWrite],
  ['events emitted (measurement)', oldWelcome.events.length, newWelcome.events.length],
];
for (const [label, a, b] of rows) {
  console.log(String(label).padEnd(30), String(a).padEnd(22), String(b));
}
console.log('new-flow event stream:', newWelcome.events.join(' → '));

// ── Instrumentation proof: a scripted cohort through completionStats ──
const cohort = [];
function cohortSession(id, answers) {
  const s = NI.createSession('welcome', {
    ownerAlias: 'walkthrough', sessionId: id, onEvent: (e) => cohort.push(e),
  });
  s.start();
  for (const a of answers) {
    if (a === 'ABANDON') { s.abandon(); return; }
    s.answer(a);
  }
  if (s.state().status === 'ready') s.finish({ cohort: true });
}
for (let i = 0; i < 6; i++) cohortSession('fin-' + i, ['A', 'a@b.co', 'learn', 'x']);
for (let i = 0; i < 4; i++) cohortSession('ab-email-' + i, ['A', 'ABANDON']);
for (let i = 0; i < 2; i++) cohortSession('ab-intent-' + i, ['A', 'a@b.co', 'ABANDON']);
const stats = NI.completionStats(cohort);
console.log('\nSCRIPTED COHORT (12 sessions: 6 finish, 4 leave at email, 2 at intent):');
console.log(JSON.stringify(stats, null, 2));
