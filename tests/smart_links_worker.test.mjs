// Smart Links redirect worker — behavior tests (node --test).
// Covers the map element #3 acceptance shape: reserved-name refusal,
// count recorded, redirect target correct — plus the negative controls:
// reserved/unknown names record ZERO clicks, and counting never blocks.
import { test } from 'node:test';
import assert from 'node:assert/strict';

import { handleRequest, classifyReferrer, buildRedirectTarget } from '../HUB/smart-links/worker.js';
import { readAttribution, ATTRIBUTION_COOKIE } from '../HUB/smart-links/attribution.mjs';
import { validateLinkName, isReservedName } from '../HUB/smart-links/reserved-names.mjs';

const LINK = { id: 'link-1', target_url: 'https://example.com/landing?x=1' };

function fakeEnv(overrides = {}) {
  const clicks = [];
  const env = {
    clicks,
    lookupLink: async (name) => (name === 'morning-crumb' ? LINK : null),
    recordClick: async (row) => { clicks.push(row); },
    newAttributionId: () => 'attr-123',
    ...overrides,
  };
  return env;
}

function fakeCtx() {
  const pending = [];
  return { pending, waitUntil(p) { pending.push(p); } };
}

const req = (path, headers = {}) =>
  new Request('https://nayanet.live' + path, { headers });

test('happy path: 302 to target with carrier param, cookie set, click recorded', async () => {
  const env = fakeEnv();
  const ctx = fakeCtx();
  const res = await handleRequest(req('/morning-crumb', { Referer: 'https://www.facebook.com/post/1' }), env, ctx);
  assert.equal(res.status, 302);
  const loc = res.headers.get('Location');
  assert.ok(loc.startsWith('https://example.com/landing?x=1'), loc);
  assert.ok(loc.includes('nl_ref=morning-crumb'), loc);
  const cookie = res.headers.get('Set-Cookie');
  assert.ok(cookie.includes(ATTRIBUTION_COOKIE + '=morning-crumb.attr-123'), cookie);
  await Promise.all(ctx.pending);
  assert.equal(env.clicks.length, 1);
  assert.equal(env.clicks[0].link_id, 'link-1');
  assert.equal(env.clicks[0].referrer_class, 'social');
  assert.equal(env.clicks[0].referrer_host, 'www.facebook.com');
  assert.equal(env.clicks[0].attribution_id, 'attr-123');
});

test('counting never blocks: redirect returns while the count is still pending', async () => {
  let release;
  const gate = new Promise((r) => { release = r; });
  const env = fakeEnv({ recordClick: () => gate });
  const ctx = fakeCtx();
  const res = await handleRequest(req('/morning-crumb'), env, ctx);
  assert.equal(res.status, 302); // arrived without releasing the count
  release();
  await Promise.all(ctx.pending);
});

test('counting failure is swallowed: redirect still succeeds', async () => {
  const env = fakeEnv({ recordClick: async () => { throw new Error('db down'); } });
  const ctx = fakeCtx();
  const res = await handleRequest(req('/morning-crumb'), env, ctx);
  assert.equal(res.status, 302);
  await Promise.all(ctx.pending); // must not reject
});

test('NEGATIVE CONTROL — reserved names: 404 and zero clicks recorded', async () => {
  for (const name of ['rooms', 's', 'identity.html', 'settings', 'sn', 'feed']) {
    const env = fakeEnv({ lookupLink: async () => LINK }); // even if a row existed
    const ctx = fakeCtx();
    const res = await handleRequest(req('/' + name), env, ctx);
    assert.equal(res.status, 404, name);
    await Promise.all(ctx.pending);
    assert.equal(env.clicks.length, 0, name);
  }
});

test('NEGATIVE CONTROL — unknown name: 404 and zero clicks', async () => {
  const env = fakeEnv();
  const ctx = fakeCtx();
  const res = await handleRequest(req('/no-such-link'), env, ctx);
  assert.equal(res.status, 404);
  await Promise.all(ctx.pending);
  assert.equal(env.clicks.length, 0);
});

test('multi-segment paths are never links', async () => {
  const env = fakeEnv();
  const res = await handleRequest(req('/rooms/reports'), env, fakeCtx());
  assert.equal(res.status, 404);
  assert.equal(env.clicks.length, 0);
});

test('referrer classes: direct / internal / search / email / other', () => {
  assert.equal(classifyReferrer(null, 'nayanet.live').referrer_class, 'direct');
  assert.equal(classifyReferrer('https://nayanet.live/feed', 'nayanet.live').referrer_class, 'internal');
  assert.equal(classifyReferrer('https://www.google.com/search?q=x', 'nayanet.live').referrer_class, 'search');
  assert.equal(classifyReferrer('https://mail.google.com/mail/u/0/', 'nayanet.live').referrer_class, 'email');
  assert.equal(classifyReferrer('https://some-blog.example/post', 'nayanet.live').referrer_class, 'other');
  // raw referrer path is never stored — host only
  assert.equal(classifyReferrer('https://some-blog.example/secret-path', 'nayanet.live').referrer_host, 'some-blog.example');
});

test('redirect target: nl_ref appended once, never duplicated', () => {
  const once = buildRedirectTarget('https://example.com/a', 'morning-crumb');
  assert.ok(once.includes('nl_ref=morning-crumb'));
  const twice = buildRedirectTarget(once, 'morning-crumb');
  assert.equal(twice, once);
});

test('attribution carrier: the join side reads what the worker wrote', () => {
  const fromCookie = readAttribution({ cookieHeader: 'other=1; nl_attr=morning-crumb.attr-123; x=2' });
  assert.deepEqual(fromCookie, { link_name: 'morning-crumb', attribution_id: 'attr-123', source: 'cookie' });
  const fromParam = readAttribution({ url: 'https://nayanet.live/join?nl_ref=morning-crumb' });
  assert.deepEqual(fromParam, { link_name: 'morning-crumb', attribution_id: null, source: 'param' });
  assert.equal(readAttribution({ cookieHeader: 'a=1', url: 'https://nayanet.live/join' }), null);
  assert.equal(readAttribution({}), null);
});

test('name validation: shape + reserved, case-insensitive', () => {
  assert.deepEqual(validateLinkName('Morning-Crumb'), { ok: true, name: 'morning-crumb' });
  assert.equal(validateLinkName('rooms').reason, 'reserved');
  assert.equal(validateLinkName('ROOMS').reason, 'reserved');
  assert.equal(validateLinkName('a').reason, 'bad_shape');
  assert.equal(validateLinkName('has space').reason, 'bad_shape');
  assert.equal(validateLinkName('under_score').reason, 'bad_shape');
  assert.equal(validateLinkName('').reason, 'empty');
  assert.ok(isReservedName('Identity.HTML'));
});
