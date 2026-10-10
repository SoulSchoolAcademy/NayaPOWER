/**
 * Session rolling context (SPEC.md §5): last 6 Q&A pairs per session, 24h TTL.
 * Keyed by sha256(sessionId) — the raw session ID never touches storage or logs.
 * Interface: getCtx(hash) -> {turns:[{q,a,id}], lastId} | null
 *            pushTurn(hash, {q,a,id}) -> void
 * Production: Workers KV with expirationTtl: 86400.
 * MOCK (this scaffold): in-memory Map. Dies with the isolate — which is also
 * the honest v1 semantic: nothing persists beyond the session anyway.
 */
const mem = new Map(); // hash -> { turns: [], expires: ts }

function prune() {
  const now = Date.now();
  for (const [k, v] of mem) if (v.expires < now) mem.delete(k);
}

export async function getCtx(env, sessionHash) {
  if (env && env.SESSION_KV) {
    // TODO(deploy): const raw = await env.SESSION_KV.get('ctx:' + sessionHash, 'json');
    throw new Error('KV session path not yet implemented in scaffold');
  }
  prune();
  const e = mem.get(sessionHash);
  if (!e) return null;
  return { turns: e.turns, lastId: e.turns.length ? e.turns[e.turns.length - 1].id : null };
}

export async function pushTurn(env, sessionHash, turn) {
  if (env && env.SESSION_KV) {
    // TODO(deploy): await env.SESSION_KV.put('ctx:' + sessionHash, JSON.stringify({turns}), {expirationTtl: 86400});
    throw new Error('KV session path not yet implemented in scaffold');
  }
  prune();
  const e = mem.get(sessionHash) || { turns: [], expires: Date.now() + 86400_000 };
  e.turns.push({ q: turn.q, a: turn.a, id: turn.id });
  e.turns = e.turns.slice(-6);
  e.expires = Date.now() + 86400_000;
  mem.set(sessionHash, e);
}

export async function hashSession(sessionId) {
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(String(sessionId)));
  return [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, '0')).join('').slice(0, 16);
}
