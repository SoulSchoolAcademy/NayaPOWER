/**
 * Ask Naya Knowledge API — router (SPEC.md §1).
 *   GET  /health  → {status, version, brainSha, indexVersion, voiceBackend, backend}
 *   POST /ask     → AskResponse (SPEC.md §3)
 *   POST /voice   → audio bytes (SPEC.md §4)
 *
 * Privacy (SPEC.md §6): logs carry only hashed session IDs + timings.
 * CORS: allowlist from ALLOWED_ORIGINS; default deny.
 */
import { loadIndex, search } from './retrieve.js';
import { composeAskResponse } from './compose.js';
import { renderVoice } from './voice.js';
import { getCtx, pushTurn, hashSession } from './session.js';

const VERSION = '0.1.0-scaffold';

function corsHeaders(env, req) {
  const origin = req.headers.get('Origin') || '';
  const allow = (env.ALLOWED_ORIGINS || '').split(',').map((s) => s.trim()).filter(Boolean);
  const ok = allow.includes(origin);
  return {
    ok,
    headers: {
      'Access-Control-Allow-Origin': ok ? origin : 'null',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
      'Vary': 'Origin',
    },
  };
}

function json(data, status = 200, cors) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json', ...cors.headers },
  });
}

function err(code, message, status = 400, cors, extra = {}) {
  // Error envelope: machine-readable code, human message, never a stack trace.
  return json({ error: code, message, ...extra }, status, cors);
}

async function handleHealth(env, cors) {
  const index = await loadIndex(env);
  return json({
    status: 'ok',
    version: VERSION,
    brainSha: index.manifest.brainSha,
    indexVersion: index.manifest.indexVersion,
    docCount: index.manifest.docCount,
    backend: index.backend,
    voiceBackend: env.VOICE_RENDER_URL ? 'render-service' : 'MOCK',
  }, 200, cors);
}

// Simple per-session throttle: 30 asks / rolling hour (MOCK in-memory).
const throttle = new Map();
function checkThrottle(sessionHash) {
  const now = Date.now();
  const e = throttle.get(sessionHash) || { count: 0, reset: now + 3600_000 };
  if (now > e.reset) { e.count = 0; e.reset = now + 3600_000; }
  e.count += 1;
  throttle.set(sessionHash, e);
  if (e.count > 30) return Math.ceil((e.reset - now) / 1000);
  return 0;
}

async function handleAsk(req, env, cors) {
  let body;
  try { body = await req.json(); }
  catch { return err('bad_request', 'body must be JSON', 400, cors); }
  const question = (body.question || '').toString().trim();
  if (!question || question.length > 500) {
    return err('bad_request', 'question required (1..500 chars)', 400, cors);
  }
  const sessionHash = body.sessionId ? await hashSession(body.sessionId) : 'anonymous';

  const retryAfter = checkThrottle(sessionHash);
  if (retryAfter) {
    return err('rate_limited', 'too many questions this hour — slow down', 429, cors, { retry_after: retryAfter });
  }

  const t0 = Date.now();
  const index = await loadIndex(env);
  const hits = search(index, question, 5);
  const sessionCtx = await getCtx(env, sessionHash).catch(() => null);
  const response = composeAskResponse({
    question, hits,
    manifest: index.manifest,
    backend: index.backend,
    sessionCtx,
  });
  await pushTurn(env, sessionHash, { q: question, a: response.keyText, id: response.id }).catch(() => {});
  // Privacy: hashed session only, timings only. Never question/answer text.
  console.log(JSON.stringify({
    route: 'ask', session: sessionHash, ms: Date.now() - t0,
    brainSha: response.brainSha, id: response.id, backend: response.backend,
  }));
  return json(response, 200, cors);
}

async function handleVoice(req, env, cors) {
  let body;
  try { body = await req.json(); }
  catch { return err('bad_request', 'body must be JSON', 400, cors); }
  const speakText = (body.speakText || '').toString().trim();
  if (!speakText || speakText.length > 2000) {
    return err('bad_request', 'speakText required (1..2000 chars)', 400, cors);
  }
  try {
    const out = await renderVoice(env, speakText, env.VOICE_PIN || 'chatterbox-naya-ref-v1');
    const headers = {
      'Content-Type': out.contentType,
      'X-Voice-Backend': out.backend,
      ...cors.headers,
    };
    if (out.mockLabel) headers['X-Mock-Audio'] = out.mockLabel;
    return new Response(out.audio, { status: 200, headers });
  } catch (e) {
    // Voice failure is honest, never silent: the page shows text + "voice unavailable".
    return err('voice_unavailable', 'voice render failed — text answer stands', 503, cors);
  }
}

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    const cors = corsHeaders(env, req);
    if (req.method === 'OPTIONS') return new Response(null, { status: 204, headers: cors.headers });
    if (!cors.ok && req.method !== 'OPTIONS') {
      return err('forbidden_origin', 'origin not allowlisted', 403, cors);
    }
    try {
      if (url.pathname === '/health' && req.method === 'GET') return handleHealth(env, cors);
      if (url.pathname === '/ask' && req.method === 'POST') return handleAsk(req, env, cors);
      if (url.pathname === '/voice' && req.method === 'POST') return handleVoice(req, env, cors);
      return err('not_found', 'unknown route', 404, cors);
    } catch (e) {
      return err('internal', 'unexpected error', 500, cors);
    }
  },
};
