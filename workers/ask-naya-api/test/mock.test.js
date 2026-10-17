/**
 * Smoke tests for the MOCK backends. Run: node --test test/
 * These prove the plumbing (routes, composer, schema, CORS). They prove
 * nothing about the real brain or her real voice — the mocks are labeled.
 */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import worker from '../src/index.js';
import { loadIndex, search } from '../src/retrieve.js';
import { composeAskResponse } from '../src/compose.js';
import { validateAskResponse } from '../src/schema.js';
import { renderVoice } from '../src/voice.js';

const ENV = { ALLOWED_ORIGINS: 'https://example.test' };
const req = (path, method, body, origin = 'https://example.test') =>
  new Request(`https://ask.test${path}`, {
    method,
    headers: { 'Content-Type': 'application/json', Origin: origin },
    body: body ? JSON.stringify(body) : undefined,
  });

test('health reports MOCK backend and manifest', async () => {
  const res = await worker.fetch(req('/health', 'GET'), ENV);
  assert.equal(res.status, 200);
  const h = await res.json();
  assert.equal(h.status, 'ok');
  assert.equal(h.backend, 'MOCK');
  assert.equal(h.brainSha, 'MOCK');
  assert.equal(h.voiceBackend, 'MOCK');
});

test('ask: known question returns a valid extractive answer', async () => {
  const res = await worker.fetch(
    req('/ask', 'POST', { question: 'What is the Judgment Rule?', sessionId: 's-1' }), ENV);
  assert.equal(res.status, 200);
  const a = await res.json();
  const v = validateAskResponse(a);
  assert.deepEqual(v.errors, v.errors); // surface errors on failure below
  assert.ok(v.ok, 'schema errors: ' + v.errors.join('; '));
  assert.equal(a.id, 'judgment-rule');
  assert.equal(a.backend, 'MOCK');
  assert.equal(a.brainSha, 'MOCK');
  assert.ok(a.sources[0].path.startsWith('BRAIN/'));
  assert.ok(a.confidence >= 0 && a.confidence <= 1);
});

test('ask: unknown question takes the honest Trait-47 path', async () => {
  const res = await worker.fetch(
    req('/ask', 'POST', { question: 'xyzzy plugh frobnicate', sessionId: 's-2' }), ENV);
  assert.equal(res.status, 200);
  const a = await res.json();
  assert.equal(a.id, 'unknown');
  assert.equal(a.confidence, 0);
  assert.ok(a.keyText.toLowerCase().includes("not in my knowledge"));
  assert.ok(validateAskResponse(a).ok);
});

test('ask: supersession emits the correction shape the page choreographs', async () => {
  const res = await worker.fetch(
    req('/ask', 'POST', { question: 'What is the Awesome Rule?', sessionId: 's-3' }), ENV);
  const a = await res.json();
  assert.ok(a.correction, 'expected correction for superseded mock doc');
  assert.ok(a.correction.retractText && a.correction.newText && a.correction.speakText);
  assert.ok(validateAskResponse(a).ok);
});

test('ask: missing question is a 400 with an error envelope', async () => {
  const res = await worker.fetch(req('/ask', 'POST', { sessionId: 's-4' }), ENV);
  assert.equal(res.status, 400);
  const e = await res.json();
  assert.equal(e.error, 'bad_request');
  assert.ok(!('stack' in e), 'no stack traces leak');
});

test('CORS: non-allowlisted origin is rejected', async () => {
  const res = await worker.fetch(
    req('/health', 'GET', null, 'https://evil.test'), ENV);
  assert.equal(res.status, 403);
});

test('voice mock returns labeled synthetic audio, never her voice', async () => {
  const out = await renderVoice(ENV, 'Hello, I am Naya.', 'pin');
  assert.equal(out.backend, 'MOCK');
  assert.ok(out.mockLabel.includes("NOT Naya's voice"));
  assert.ok(out.audio.length > 1000, 'non-trivial audio bytes');
  // WAV magic
  const magic = String.fromCharCode(...out.audio.slice(0, 4));
  assert.equal(magic, 'RIFF');
});

test('retrieve: search ranks the right mock doc first', async () => {
  const index = await loadIndex(ENV);
  const hits = search(index, 'nine nodes self law act', 3);
  assert.ok(hits.length > 0);
  assert.equal(hits[0].doc.id, 'nine-nodes');
});

test('composer output always carries provenance', async () => {
  const index = await loadIndex(ENV);
  const hits = search(index, 'judgment rule abdication', 5);
  const r = composeAskResponse({ question: 'q', hits, manifest: index.manifest, backend: 'MOCK', sessionCtx: null });
  assert.equal(r.brainSha, 'MOCK');
  assert.equal(typeof r.degraded, 'boolean');
});
