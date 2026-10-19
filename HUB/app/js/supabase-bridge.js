/* HUB/app/js/supabase-bridge.js — Hub <-> Supabase persistence bridge (t0800)
 *
 * The "store" leg of the Smart Note flow, per
 * goals/smart-note-this-hub-the-one-flow-working-end-to-end/hidden_files/persistence-adapter-design.md
 *
 * Law of this module:
 *  1. It targets the adapter INTERFACE, never a hard-coded schema. The live
 *     Supabase mapping is a CONFIG (SUPABASE_MAP) — verified against the real
 *     database 2026-10-17, changeable without touching code.
 *  2. All three tongues (human / naya / machine) are stored, always.
 *  3. Every write gets a verify-read: sha256(canonical write) must equal
 *     sha256(canonical read-back), or the write is a hope and stored=false.
 *  4. Supabase unreachable -> local JSONL queue + replay. The Hub never sees
 *     an unexplained gap.
 *  5. The browser never ships a credential. The browser Supabase transport is
 *     a config slot the deployment fills (REST url + key from the Worker);
 *     when unconfigured it reports not-available honestly instead of faking.
 *
 * Dual runtime: browser (window.SupabaseBridge) and Node (module.exports).
 * Transports are injected so the module itself never touches fs/network:
 *   persist(sn, note, { supabase, queue }) -> PersistReceipt
 *   getNotes({ supabase, queue }, sinceUtc) -> [canonical records, newest first]
 */
(function (root, factory) {
  if (typeof module !== 'undefined' && module.exports) module.exports = factory();
  else root.SupabaseBridge = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  var ADAPTER_VERSION = 't0800-1';

  /* ——— Live Supabase mapping (CONFIG, not code) ———
     Verified 2026-10-17 against project dahisasgpfvziswqvmvm (supabase-red-cable):
     public.smart_note_events(id uuid, member_id uuid, subject text,
       event_type text, source_context jsonb, privacy_state text, status text,
       created_at timestamptz, verified_at timestamptz).
     30 rows live; the capture-inbox adapter already writes SMART_NOTE rows here. */
  var SUPABASE_MAP = {
    backend: 'supabase',
    table: 'public.smart_note_events',
    eventType: 'SMART_NOTE',
    // Identity MUST be supplied by an authenticated owner-scoped transport.
    // LIVE schema constraint (verified 2026-10-17): status IN ('INCOMPLETE','VERIFIED').
    // The canonical truth_state (CANDIDATE/...) is ALWAYS preserved verbatim in
    // the source_context envelope; the column carries the closest legal value.
    truthStateToStatus: { CANDIDATE: 'INCOMPLETE', VERIFIED: 'VERIFIED' },
    statusToTruthState: { INCOMPLETE: 'CANDIDATE', VERIFIED: 'VERIFIED' },
    columns: {
      subject: 'subject',            // <- nutshell
      eventType: 'event_type',       // <- 'SMART_NOTE'
      context: 'source_context',     // jsonb <- canonical record envelope
      privacy: 'privacy_state',      // <- scope
      status: 'status',              // <- truth_state
      member: 'member_id'
    }
  };

  /* ——— Canonical record (the design doc's canonical shape, exact) ——— */
  function canonicalRecord(sn, note, opts) {
    opts = opts || {};
    return {
      sn: String(sn),
      truth_state: note.truth_state || 'CANDIDATE',
      scope: note.scope || 'PRIVATE',
      captured_utc: note.captured_utc || new Date().toISOString(),
      nutshell: String(note.nutshell || ''),
      human_note: String(note.human_note || ''),
      naya_note: String(note.naya_note || ''),
      machine_note: note.machine_note || {},
      source_handle: note.source_handle || '',
      persisted_utc: opts.persisted_utc || new Date().toISOString(),
      adapter_version: ADAPTER_VERSION
    };
  }

  /* Stable stringify: fixed key order, so hashes are comparable byte-for-byte. */
  var CANON_KEYS = ['sn', 'truth_state', 'scope', 'captured_utc', 'nutshell',
    'human_note', 'naya_note', 'machine_note', 'source_handle', 'persisted_utc', 'adapter_version'];
  /* Stable stringify: fixed key order, so hashes are comparable byte-for-byte.
     DEEP: nested objects get their keys sorted recursively. This is the root
     fix for JSONB normalization — Postgres reorders object keys (by length)
     on write, so a shallow stringify would hash the write and the read-back
     differently even though the VALUES are identical. */
  function deepStable(v) {
    if (Array.isArray(v)) return '[' + v.map(deepStable).join(',') + ']';
    if (v && typeof v === 'object') {
      return '{' + Object.keys(v).sort().map(function (k) {
        return JSON.stringify(k) + ':' + deepStable(v[k]);
      }).join(',') + '}';
    }
    return JSON.stringify(v);
  }
  function stableStringify(rec) {
    var out = {};
    CANON_KEYS.forEach(function (k) { out[k] = rec[k] === undefined ? null : rec[k]; });
    return deepStable(out);
  }

  async function sha256Hex(str) {
    if (typeof crypto !== 'undefined' && crypto.subtle) {
      var buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(str));
      return Array.from(new Uint8Array(buf)).map(function (b) { return b.toString(16).padStart(2, '0'); }).join('');
    }
    // Node fallback
    var c = require('crypto');
    return c.createHash('sha256').update(str, 'utf8').digest('hex');
  }

  /* ——— Supabase transport (injected query fn: async (sql) -> rows) ——— */
  function sqlEscape(v) { return String(v).replace(/'/g, "''"); }

  function rowToCanonical(row) {
    var ctx = row.source_context || {};
    return {
      sn: ctx.sn || null,
      truth_state: ctx.truth_state || (SUPABASE_MAP.statusToTruthState[row.status] || row.status) || null,
      scope: row.privacy_state || ctx.scope || null,
      captured_utc: ctx.captured_utc || null,
      nutshell: row.subject || ctx.nutshell || '',
      human_note: ctx.human_note || '',
      naya_note: ctx.naya_note || '',
      machine_note: ctx.machine_note || {},
      source_handle: ctx.source_handle || '',
      persisted_utc: ctx.persisted_utc || row.created_at || null,
      adapter_version: ctx.adapter_version || null,
      _row_id: row.id || null,
      _created_at: row.created_at || null
    };
  }

  function requireMemberId(memberId) {
    if (typeof memberId !== 'string' || !/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(memberId)) {
      throw new Error('AUTHENTICATED_MEMBER_ID_REQUIRED');
    }
    return memberId;
  }

  /* REST: API key identifies the application; user JWT authorizes rows. */
  async function restCall(rest, method, path, body) {
    requireMemberId(rest && rest.memberId);
    if (!rest.key || !rest.accessToken) throw new Error('AUTHENTICATED_REST_SESSION_REQUIRED');
    var res = await fetch(rest.base + path, {
      method: method,
      headers: {
        'apikey': rest.key,
        'Authorization': 'Bearer ' + rest.accessToken,
        'Content-Type': 'application/json',
        'Prefer': 'return=representation'
      },
      body: body === undefined ? undefined : JSON.stringify(body)
    });
    if (!res.ok) throw new Error('supabase REST ' + res.status);
    return res.json();
  }

  async function supabasePersist(rec, transport) {
    if (transport.rest) return restPersist(rec, transport.rest);
    return sqlPersist(rec, transport.query, transport.memberId);
  }

  async function restPersist(rec, rest) {
    var c = SUPABASE_MAP.columns;
    var envelope = {
      sn: rec.sn, truth_state: rec.truth_state, scope: rec.scope,
      captured_utc: rec.captured_utc, human_note: rec.human_note,
      naya_note: rec.naya_note, machine_note: rec.machine_note,
      source_handle: rec.source_handle, persisted_utc: rec.persisted_utc,
      adapter_version: rec.adapter_version
    };
    var row = {};
    row[c.member] = requireMemberId(rest.memberId);
    row[c.subject] = rec.nutshell;
    row[c.eventType] = SUPABASE_MAP.eventType;
    row[c.context] = envelope;
    row[c.privacy] = rec.scope;
    row[c.status] = SUPABASE_MAP.truthStateToStatus[rec.truth_state] || 'INCOMPLETE';
    var rows = await restCall(rest, 'POST', '/smart_note_events', row);
    var rowId = rows && rows[0] && rows[0].id;
    if (!rowId) return { ok: false, reason: 'insert returned no id' };
    var back = await restCall(rest, 'GET', '/smart_note_events?id=eq.' + encodeURIComponent(rowId) + '&limit=1');
    if (!back || !back[0]) return { ok: false, reason: 'verify-read returned no row', rowId: rowId };
    var writeHash = await sha256Hex(stableStringify(rec));
    var readHash = await sha256Hex(stableStringify(rowToCanonical(back[0])));
    return {
      ok: writeHash === readHash, rowId: rowId,
      writeHash: writeHash, readHash: readHash,
      reason: writeHash === readHash ? null : 'read-back hash mismatch'
    };
  }

  async function sqlPersist(rec, query, memberId) {
    memberId = requireMemberId(memberId);
    var c = SUPABASE_MAP.columns;
    var envelope = {
      sn: rec.sn, truth_state: rec.truth_state, scope: rec.scope,
      captured_utc: rec.captured_utc, human_note: rec.human_note,
      naya_note: rec.naya_note, machine_note: rec.machine_note,
      source_handle: rec.source_handle, persisted_utc: rec.persisted_utc,
      adapter_version: rec.adapter_version
    };
    var sql =
      "INSERT INTO " + SUPABASE_MAP.table + " (" + c.member + ", " + c.subject + ", " +
      c.eventType + ", " + c.context + ", " + c.privacy + ", " + c.status + ") VALUES (" +
      "'" + sqlEscape(memberId) + "', " +
      "'" + sqlEscape(rec.nutshell) + "', " +
      "'" + sqlEscape(SUPABASE_MAP.eventType) + "', " +
      "'" + sqlEscape(JSON.stringify(envelope)) + "'::jsonb, " +
      "'" + sqlEscape(rec.scope) + "', " +
      "'" + sqlEscape(SUPABASE_MAP.truthStateToStatus[rec.truth_state] || 'INCOMPLETE') + "') " +
      "RETURNING id, created_at;";
    var rows = await query(sql);
    var rowId = rows && rows[0] && rows[0].id;
    if (!rowId) return { ok: false, reason: 'insert returned no id' };
    // VERIFY-READ: the write is a hope until the read-back hashes equal.
    var back = await query(
      "SELECT id, " + c.subject + ", " + c.eventType + ", " + c.context + ", " +
      c.privacy + ", " + c.status + ", created_at FROM " + SUPABASE_MAP.table +
      " WHERE id = '" + sqlEscape(rowId) + "' LIMIT 1;");
    if (!back || !back[0]) return { ok: false, reason: 'verify-read returned no row', rowId: rowId };
    var writeHash = await sha256Hex(stableStringify(rec));
    var readHash = await sha256Hex(stableStringify(rowToCanonical(back[0])));
    return {
      ok: writeHash === readHash, rowId: rowId,
      writeHash: writeHash, readHash: readHash,
      reason: writeHash === readHash ? null : 'read-back hash mismatch'
    };
  }

  async function supabaseGetNotes(transport, sinceUtc) {
    var memberId = requireMemberId(transport.rest ? transport.rest.memberId : transport.memberId);
    if (transport.rest) {
      var q = '/smart_note_events?event_type=eq.' + encodeURIComponent(SUPABASE_MAP.eventType) +
        '&member_id=eq.' + encodeURIComponent(memberId) + '&order=created_at.desc&limit=200' +
        (sinceUtc ? '&created_at=gte.' + encodeURIComponent(sinceUtc) : '');
      var rows = await restCall(transport.rest, 'GET', q);
      return (rows || []).map(rowToCanonical);
    }
    var c = SUPABASE_MAP.columns;
    var sql =
      "SELECT id, " + c.subject + ", " + c.eventType + ", " + c.context + ", " +
      c.privacy + ", " + c.status + ", created_at FROM " + SUPABASE_MAP.table +
      " WHERE " + c.eventType + " = '" + sqlEscape(SUPABASE_MAP.eventType) + "'" +
      " AND " + c.member + " = '" + sqlEscape(memberId) + "'" +
      (sinceUtc ? " AND created_at >= '" + sqlEscape(sinceUtc) + "'" : "") +
      " ORDER BY created_at DESC LIMIT 200;";
    var srows = await transport.query(sql);
    return (srows || []).map(rowToCanonical);
  }

  /* ——— Local JSONL transport (fallback + audit; injected {append, readAll}) ——— */
  async function queuePersist(rec, queue) {
    await queue.append(stableStringify(rec) + '\n');
    var all = await queue.readAll();
    var lines = all.split('\n').filter(function (l) { return l.trim(); });
    var last = JSON.parse(lines[lines.length - 1]);
    var writeHash = await sha256Hex(stableStringify(rec));
    var readHash = await sha256Hex(stableStringify(last));
    return { ok: writeHash === readHash, writeHash: writeHash, readHash: readHash };
  }

  async function queueGetNotes(queue, sinceUtc) {
    var all = await queue.readAll();
    var recs = all.split('\n').filter(function (l) { return l.trim(); }).map(function (l) {
      try { return JSON.parse(l); } catch (e) { return null; }
    }).filter(Boolean);
    if (sinceUtc) recs = recs.filter(function (r) { return (r.persisted_utc || '') >= sinceUtc; });
    recs.sort(function (a, b) { return (b.persisted_utc || '') < (a.persisted_utc || '') ? -1 : 1; });
    return recs;
  }

  /* ——— The adapter: persist() ——— */
  async function persist(sn, note, transports) {
    transports = transports || {};
    var rec = canonicalRecord(sn, note);
    var writeHash = await sha256Hex(stableStringify(rec));
    var receipt = {
      sn: rec.sn, stored: false, backend: null,
      read_back_ok: false, record_sha256: writeHash,
      persisted_utc: rec.persisted_utc, row_id: null, reason: null
    };
    // Audit trail: the JSONL is ALWAYS written, even when Supabase succeeds.
    if (transports.queue) {
      try { await queuePersist(rec, transports.queue); } catch (e) { /* audit best-effort */ }
    }
    if (transports.supabase && transports.supabase.available !== false) {
      try {
        var r = await supabasePersist(rec, transports.supabase);
        receipt.backend = 'supabase';
        receipt.stored = r.ok;
        receipt.read_back_ok = r.ok;
        receipt.row_id = r.rowId || null;
        receipt.reason = r.reason || null;
        if (r.ok) return receipt;
        // Supabase failed: fall through to the queue so no note is lost.
      } catch (e) {
        receipt.reason = 'supabase transport error: ' + (e && e.message);
      }
    }
    if (transports.queue) {
      receipt.backend = receipt.backend ? receipt.backend + '+local-queue' : 'local-queue';
      var q = await queuePersist(rec, transports.queue);
      receipt.stored = q.ok;
      receipt.read_back_ok = q.ok;
      if (!receipt.reason) receipt.reason = 'supabase unavailable — queued locally for replay';
    }
    return receipt;
  }

  /* ——— The adapter: replay queued notes into Supabase ——— */
  async function replay(transports) {
    if (!transports.queue || !transports.supabase || transports.supabase.available === false) {
      return { replayed: 0, reason: 'replay needs both queue and supabase transports' };
    }
    var queued = await queueGetNotes(transports.queue, null);
    var existing = await supabaseGetNotes(transports.supabase, null);
    var seen = {};
    existing.forEach(function (r) { if (r.sn) seen[r.sn + '|' + r.persisted_utc] = true; });
    var replayed = 0, failed = [];
    for (var i = 0; i < queued.length; i++) {
      var rec = queued[i];
      if (seen[rec.sn + '|' + rec.persisted_utc]) continue; // already in Supabase
      var note = {
        truth_state: rec.truth_state, scope: rec.scope, captured_utc: rec.captured_utc,
        nutshell: rec.nutshell, human_note: rec.human_note, naya_note: rec.naya_note,
        machine_note: rec.machine_note, source_handle: rec.source_handle
      };
      var r2 = await persist(rec.sn, note, { supabase: transports.supabase });
      if (r2.stored && r2.backend === 'supabase') replayed++;
      else failed.push(rec.sn);
    }
    return { replayed: replayed, failed: failed, scanned: queued.length };
  }

  /* ——— The bridge: getNotes() -> canonical records, newest first ——— */
  async function getNotes(transports, sinceUtc) {
    transports = transports || {};
    var remoteError = null;
    if (transports.supabase && transports.supabase.available !== false) {
      try { return { backend: 'supabase', records: await supabaseGetNotes(transports.supabase, sinceUtc) }; }
      catch (e) { remoteError = e && e.message ? e.message : 'remote read failed'; }
    }
    if (transports.queue) {
      return { backend: 'local-queue', records: await queueGetNotes(transports.queue, sinceUtc) };
    }
    return { backend: 'none', records: [], reason: remoteError ? 'supabase transport error: ' + remoteError : 'no transport available' };
  }

  /* ——— Card rendering (Hub feed rows; XSS-safe by construction) ——— */
  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }

  function cardHtml(rec) {
    return '<article class="smart-note-card" data-sn="' + esc(rec.sn) + '">' +
      '<div class="sn-kicker">SMART NOTE · ' + esc(rec.truth_state) + '</div>' +
      '<h3 class="sn-title">' + esc(rec.nutshell) + '</h3>' +
      '<p class="sn-human">' + esc((rec.human_note || '').slice(0, 280)) + '</p>' +
      '<div class="sn-meta"><span>' + esc(rec.scope) + '</span>' +
      '<span>' + esc(rec.captured_utc || '') + '</span>' +
      '<span>' + esc(rec.sn) + '</span></div></article>';
  }

  /* ——— Feed runtime: the injected governed runtime the Hub app picks up ———
     runtime-live.js's bridge() accepts window.NayaPowerRuntime; its METHOD_MAP
     calls smartFeed() for the feed room. We register only if no runtime is
     present — never clobber a deployment's own runtime. */
  function registerFeedRuntime(makeTransports) {
    if (typeof window === 'undefined') return false;
    if (window.NayaPowerRuntime || window.NayaAssistantRuntime || window.NayaRuntimeBridge) return false;
    window.NayaPowerRuntime = {
      smartFeed: async function (payload) {
        var t = makeTransports();
        var res = await getNotes(t, payload && payload.since_utc);
        if (res.backend === 'none') {
          return { ok: false, state: 'not_verified', message: res.reason || 'No persistence transport is available in this session.' };
        }
        var cards = res.records.map(function (r) {
          return {
            id: r._row_id || r.sn, type: 'SMART NOTE', title: r.nutshell,
            human: r.human_note, summary: r.human_note,
            truth_state: r.truth_state, scope: r.scope,
            created_at: r._created_at || r.persisted_utc,
            source: 'smart_note_events via bridge (' + res.backend + ')'
          };
        });
        return { ok: true, state: cards.length ? 'ready' : 'empty', data: cards, backend: res.backend };
      }
    };
    return true;
  }

  /* ——— Browser auto-registration ———
     On load in a browser, register the feed runtime with whatever the
     deployment injected via window.NayaBridgeConfig (the ONE config slot):
       { supabaseRest: { url, key, accessToken, memberId } } -> RLS-scoped rows
     accessToken/memberId MUST come from the authenticated session, not static HTML.
       { queueUrl: '...' }             -> live JSONL queue in the feed room
     Nothing injected -> transports absent -> smartFeed() reports not_verified
     honestly. The module NEVER ships a credential; deployment provides it. */
  if (typeof window !== 'undefined' && typeof document !== 'undefined') {
    try {
      var cfg = window.NayaBridgeConfig || {};
      registerFeedRuntime(function () {
        var t = {};
        if (cfg.supabaseRest && cfg.supabaseRest.url) {
          t.supabase = { available: true, query: null, rest: {
            base: String(cfg.supabaseRest.url).replace(/\/$/, ''),
            key: cfg.supabaseRest.key || '',
            accessToken: cfg.supabaseRest.accessToken || '',
            memberId: cfg.supabaseRest.memberId || ''
          } };
        }
        // A naked queueUrl is not an authenticated, owner-scoped source.
        // Browser queue fallback remains BLOCKED until a governed endpoint
        // proves viewer identity and note-level authorization server-side.
        return t;
      });
    } catch (e) { /* never break the app on bridge init */ }
  }

  return {
    ADAPTER_VERSION: ADAPTER_VERSION,
    SUPABASE_MAP: SUPABASE_MAP,
    canonicalRecord: canonicalRecord,
    stableStringify: stableStringify,
    sha256Hex: sha256Hex,
    persist: persist,
    replay: replay,
    getNotes: getNotes,
    cardHtml: cardHtml,
    esc: esc,
    rowToCanonical: rowToCanonical,
    registerFeedRuntime: registerFeedRuntime
  };
});
