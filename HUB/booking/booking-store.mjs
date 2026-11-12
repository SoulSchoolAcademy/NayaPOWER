/*
 * booking-store.mjs — REST transport for the Booking block (element
 * #17), in the Hub bridge's pattern (transport injected; naya-notes.js
 * is the sibling). Two honesty rules, never broken here:
 *
 *   1. Public reads go through the migration's SECURITY DEFINER RPCs
 *      with the anon key — exactly the access the database grants a
 *      stranger: one page's shape, its windows, and taken TIME RANGES.
 *      Nothing here can read another booking's details, because the
 *      database offers no such path to this key.
 *   2. Owner operations require a session token; without one they
 *      refuse with { not_verified } and make ZERO network calls — the
 *      Hub never fakes owner data. Reminders ride the same rule: they
 *      are Smart Mail rows written under the owner's session; when no
 *      session exists the booking still succeeds and the result says
 *      { reminders: 'deferred_no_session' } instead of claiming mail
 *      that was never written.
 */

import { reminderRows } from './booking-core.mjs';

function base(opts) {
  return String(opts.supabaseUrl || '').replace(/\/$/, '') + '/rest/v1';
}

const KEY_HEADER = 'apikey';

function publicHeaders(opts) {
  const headers = { 'Content-Type': 'application/json' };
  headers[KEY_HEADER] = opts.anonKey;
  return headers;
}

function authHeaders(opts, token) {
  return { ...publicHeaders(opts), Authorization: `Bearer ${token}` };
}

function tokenOf(opts) {
  try {
    return typeof opts.getAccessToken === 'function' ? opts.getAccessToken() : null;
  } catch {
    return null;
  }
}

async function rpc(opts, name, args, token) {
  const fetchImpl = opts.fetchImpl || fetch;
  const res = await fetchImpl(`${base(opts)}/rpc/${name}`, {
    method: 'POST',
    headers: token ? authHeaders(opts, token) : publicHeaders(opts),
    body: JSON.stringify(args),
  });
  if (!res.ok) {
    const text = await res.text().catch(() => '');
    return { error: true, status: res.status, body: text };
  }
  return { data: await res.json() };
}

// Map a PostgREST error body to the migration's named refusals.
export function classifyInsertError(status, bodyText) {
  const text = String(bodyText || '');
  if (text.includes('booking_slot_taken') || text.includes('bookings_one_confirmed_per_slot')) {
    return { conflict: true, reason: 'slot_taken' };
  }
  if (text.includes('booking_outside_availability')) {
    return { invalid: true, reason: 'outside_availability' };
  }
  if (status === 409) return { conflict: true, reason: 'slot_taken' };
  return { error: true, status, reason: 'insert_failed' };
}

export function createBookingStore(opts) {
  const fetchImpl = opts.fetchImpl || fetch;
  const root = base(opts);
  return {
    // — Public (anon key, RPC-only by database design) —
    async getPage(slug) {
      const r = await rpc(opts, 'get_booking_page', { p_slug: slug });
      if (r.error) return r;
      return { page: Array.isArray(r.data) && r.data.length ? r.data[0] : null };
    },
    async getWindows(slug) {
      const r = await rpc(opts, 'get_booking_windows', { p_slug: slug });
      if (r.error) return r;
      return { windows: r.data || [] };
    },
    async getBookedStarts(slug, fromISO, toISO) {
      const r = await rpc(opts, 'get_booked_starts', {
        p_slug: slug, p_from: fromISO, p_to: toISO,
      });
      if (r.error) return r;
      // Times only, by database design — shaped as booked ranges here.
      return {
        booked: (r.data || []).map((row) => ({
          starts_at: row.starts_at, ends_at: row.ends_at, status: 'confirmed',
        })),
      };
    },
    async createBooking(row) {
      const res = await fetchImpl(`${root}/bookings`, {
        method: 'POST',
        headers: { ...publicHeaders(opts), Prefer: 'return=representation' },
        body: JSON.stringify(row),
      });
      if (!res.ok) return classifyInsertError(res.status, await res.text().catch(() => ''));
      const rows = await res.json();
      return { ok: true, booking: Array.isArray(rows) ? rows[0] : rows };
    },
    async cancelBooking(bookingId, cancelToken) {
      const r = await rpc(opts, 'cancel_booking', {
        p_booking_id: bookingId, p_cancel_token: cancelToken,
      });
      if (r.error) return r;
      return { ok: true, cancelled: r.data === true };
    },

    // — Owner (session required; refuses visibly without one) —
    async ownerListBookings() {
      const token = tokenOf(opts);
      if (!token) return { not_verified: true, reason: 'no_session' };
      const res = await fetchImpl(
        `${root}/bookings?select=*&order=starts_at.desc`,
        { headers: authHeaders(opts, token) },
      );
      if (!res.ok) return { not_verified: true, reason: `http_${res.status}` };
      return { bookings: await res.json() };
    },

    // Reminders: Smart Mail rows (thread + one message per planned
    // reminder) under the owner's session. Deferred — and SAY deferred —
    // when there is no session.
    async writeReminders(booking, page) {
      const token = tokenOf(opts);
      if (!token) return { reminders: 'deferred_no_session' };
      const { thread, messages } = reminderRows({ booking, page });
      const threadRes = await fetchImpl(`${root}/smart_mail_threads`, {
        method: 'POST',
        headers: { ...authHeaders(opts, token), Prefer: 'return=representation' },
        body: JSON.stringify(thread),
      });
      if (!threadRes.ok) return { reminders: 'failed', status: threadRes.status };
      for (const message of messages) {
        const msgRes = await fetchImpl(`${root}/smart_mail_messages`, {
          method: 'POST',
          headers: authHeaders(opts, token),
          body: JSON.stringify(message),
        });
        if (!msgRes.ok) return { reminders: 'failed', status: msgRes.status };
      }
      return { reminders: 'written', count: messages.length };
    },
  };
}
