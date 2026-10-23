// Booking block (element #17) — module tests, node --test.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import {
  validatePageInput, validateWindow, computeSlots, fitsAvailability,
  validateBookingRequest, planReminders, reminderRows, reminderThreadKey,
  pluginStates, rangesOverlap,
} from '../HUB/booking/booking-core.mjs';
import { createBookingStore, classifyInsertError } from '../HUB/booking/booking-store.mjs';

// Monday 2026-10-26, window 09:00–12:00 UTC, 60-minute bookings.
const PAGE = {
  id: 'page-1', page_id: 'page-1', owner_alias: 'shawn',
  title: 'Intro call', duration_minutes: 60, calendar_sync_state: 'not_connected',
};
const WINDOWS = [{ weekday: 1, start_time: '09:00', end_time: '12:00', timezone: 'UTC' }];
const MON = '2026-10-26';
const at = (hm) => `${MON}T${hm}:00.000Z`;

test('page + window validation: shape grammar mirrors smart_links', () => {
  assert.equal(validatePageInput({ slug: 'Intro Call', title: 'x', duration_minutes: 30 }).reason, 'slug_shape');
  assert.equal(validatePageInput({ slug: 'intro-call', title: ' ', duration_minutes: 30 }).reason, 'title_required');
  assert.equal(validatePageInput({ slug: 'intro-call', title: 'Intro', duration_minutes: 3 }).reason, 'duration_range');
  assert.deepEqual(
    validatePageInput({ slug: 'Intro-Call', title: ' Intro ', duration_minutes: 30 }).page,
    { slug: 'intro-call', title: 'Intro', duration_minutes: 30, active: true },
  );
  assert.equal(validateWindow({ weekday: 7, start_time: '09:00', end_time: '10:00' }).reason, 'weekday_range');
  assert.equal(validateWindow({ weekday: 1, start_time: '10:00', end_time: '09:00' }).reason, 'window_inverted');
  assert.equal(validateWindow({ weekday: 1, start_time: '09:00', end_time: '12:00' }).ok, true);
});

test('slots: generated inside the window, taken slot greyed, none invented', () => {
  const booked = [{ starts_at: at('10:00'), ends_at: at('11:00'), status: 'confirmed' }];
  const slots = computeSlots({
    windows: WINDOWS, booked, dateStr: MON, durationMinutes: 60,
    nowISO: '2026-10-25T00:00:00.000Z',
  });
  assert.deepEqual(slots.map((s) => s.starts_at), [at('09:00'), at('10:00'), at('11:00')]);
  assert.deepEqual(slots.map((s) => s.available), [true, false, true]);
  assert.equal(slots[1].taken, true);
  // A day with no window offers nothing.
  assert.deepEqual(computeSlots({
    windows: WINDOWS, booked: [], dateStr: '2026-10-27', durationMinutes: 60,
    nowISO: '2026-10-25T00:00:00.000Z',
  }), []);
});

test('slots: timezone is real — a New York 09:00 is 13:00Z in October', () => {
  const slots = computeSlots({
    windows: [{ weekday: 1, start_time: '09:00', end_time: '10:00', timezone: 'America/New_York' }],
    booked: [], dateStr: MON, durationMinutes: 60,
    nowISO: '2026-10-25T00:00:00.000Z',
  });
  assert.equal(slots.length, 1);
  assert.equal(slots[0].starts_at, '2026-10-26T13:00:00.000Z');
});

test('DOUBLE-BOOKING refused: same slot and partial overlap both refused', () => {
  const booked = [{ id: 'b1', starts_at: at('10:00'), ends_at: at('11:00'), status: 'confirmed' }];
  const same = validateBookingRequest({
    page: PAGE, windows: WINDOWS, booked,
    request: { visitor_name: 'Ana', starts_at: at('10:00'), ends_at: at('11:00') },
  });
  assert.deepEqual(same, { ok: false, reason: 'slot_taken' });
  const page30 = { ...PAGE, duration_minutes: 30 };
  const partial = validateBookingRequest({
    page: page30, windows: WINDOWS, booked,
    request: { visitor_name: 'Ana', starts_at: at('10:15'), ends_at: at('10:45') },
  });
  assert.equal(partial.reason, 'slot_taken');
  assert.equal(rangesOverlap(at('10:00'), at('11:00'), at('11:00'), at('12:00')), false); // back-to-back is fine
});

test('OUTSIDE AVAILABILITY refused: wrong day, before the window, overrun', () => {
  const tue = validateBookingRequest({
    page: PAGE, windows: WINDOWS, booked: [],
    request: { visitor_name: 'Ana', starts_at: '2026-10-27T10:00:00.000Z', ends_at: '2026-10-27T11:00:00.000Z' },
  });
  assert.equal(tue.reason, 'outside_availability');
  const early = validateBookingRequest({
    page: PAGE, windows: WINDOWS, booked: [],
    request: { visitor_name: 'Ana', starts_at: at('08:00'), ends_at: at('09:00') },
  });
  assert.equal(early.reason, 'outside_availability');
  const overrun = validateBookingRequest({
    page: PAGE, windows: WINDOWS, booked: [],
    request: { visitor_name: 'Ana', starts_at: at('11:30'), ends_at: at('12:30') },
  });
  assert.equal(overrun.reason, 'outside_availability');
  assert.equal(fitsAvailability(WINDOWS, at('09:00'), at('10:00')), true);
});

test('CANCELLING FREES THE SLOT: a cancelled row blocks nothing', () => {
  const cancelled = [{ id: 'b1', starts_at: at('10:00'), ends_at: at('11:00'), status: 'cancelled' }];
  const verdict = validateBookingRequest({
    page: PAGE, windows: WINDOWS, booked: cancelled,
    request: { visitor_name: 'Ana', starts_at: at('10:00'), ends_at: at('11:00') },
  });
  assert.equal(verdict.ok, true);
  const slots = computeSlots({
    windows: WINDOWS, booked: cancelled, dateStr: MON, durationMinutes: 60,
    nowISO: '2026-10-25T00:00:00.000Z',
  });
  assert.deepEqual(slots.map((s) => s.available), [true, true, true]);
});

test('reminders: both sides, owner hears twice, rows use evidenced columns only', () => {
  const booking = {
    id: 'bk-9', visitor_name: 'Ana', starts_at: at('10:00'),
    ends_at: at('11:00'), created_at: '2026-10-24T10:00:00.000Z', status: 'confirmed',
  };
  const plan = planReminders({ booking, page: PAGE });
  assert.deepEqual(plan.map((r) => [r.side, r.kind]), [
    ['owner', 'new_booking'], ['owner', 'reminder'], ['visitor', 'reminder'],
  ]);
  assert.equal(plan[1].at, '2026-10-25T10:00:00.000Z'); // a day ahead
  const { thread, messages } = reminderRows({ booking, page: PAGE });
  assert.equal(reminderThreadKey('bk-9'), 'booking-bk-9');
  assert.equal(thread.thread_key, 'booking-bk-9');
  assert.equal(thread.owner_alias, 'shawn');
  assert.deepEqual(Object.keys(thread).sort(),
    ['direction', 'owner_alias', 'participants', 'status', 'subject', 'thread_key']);
  for (const m of messages) {
    assert.deepEqual(Object.keys(m).sort(),
      ['body', 'created_at', 'direction', 'sender', 'sender_name', 'thread_key']);
  }
  assert.equal(messages.length, 3);
});

test('calendar sync: the placeholder is honest — not_connected, never dressed up', () => {
  const states = pluginStates(PAGE);
  assert.equal(states.length, 1);
  assert.equal(states[0].id, 'calendar');
  assert.equal(states[0].state, 'not_connected');
  assert.equal(pluginStates({})[0].state, 'not_connected');
});

test('insert-error classification maps the migration\u2019s named refusals', () => {
  assert.deepEqual(classifyInsertError(400, 'booking_slot_taken'),
    { conflict: true, reason: 'slot_taken' });
  assert.deepEqual(classifyInsertError(409, 'duplicate key bookings_one_confirmed_per_slot'),
    { conflict: true, reason: 'slot_taken' });
  assert.deepEqual(classifyInsertError(400, 'booking_outside_availability'),
    { invalid: true, reason: 'outside_availability' });
});

// ——— Store, with a fake transport ———

function fakeFetch(handler) {
  const calls = [];
  const impl = async (url, init) => {
    calls.push({ url, init });
    return handler(url, init);
  };
  impl.calls = calls;
  return impl;
}
const jsonRes = (status, data) => ({
  ok: status >= 200 && status < 300, status,
  json: async () => data, text: async () => JSON.stringify(data),
});

test('store: public reads ride the RPCs and shape times-only booked ranges', async () => {
  const fetchImpl = fakeFetch(async (url) => {
    if (url.includes('/rpc/get_booking_page')) {
      return jsonRes(200, [{
        page_id: 'page-1', owner_alias: 'shawn', title: 'Intro call',
        duration_minutes: 60, calendar_sync_state: 'not_connected',
      }]);
    }
    if (url.includes('/rpc/get_booked_starts')) {
      return jsonRes(200, [{ starts_at: at('10:00'), ends_at: at('11:00') }]);
    }
    throw new Error(`unexpected ${url}`);
  });
  const store = createBookingStore({
    supabaseUrl: 'https://example.supabase.co', anonKey: 'anon', fetchImpl,
  });
  const { page } = await store.getPage('intro-call');
  assert.equal(page.title, 'Intro call');
  const { booked } = await store.getBookedStarts('intro-call', at('00:00'), at('23:59'));
  assert.deepEqual(booked, [{ starts_at: at('10:00'), ends_at: at('11:00'), status: 'confirmed' }]);
  // Times only: no name, no note, no visitor field exists to leak.
  assert.deepEqual(Object.keys(booked[0]).sort(), ['ends_at', 'starts_at', 'status']);
});

test('store: createBooking maps a database refusal to slot_taken', async () => {
  const dupe = createBookingStore({
    supabaseUrl: 'https://example.supabase.co', anonKey: 'anon',
    fetchImpl: fakeFetch(async () => jsonRes(400, { message: 'booking_slot_taken' })),
  });
  assert.deepEqual(await dupe.createBooking({ page_id: 'page-1' }),
    { conflict: true, reason: 'slot_taken' });
  const good = createBookingStore({
    supabaseUrl: 'https://example.supabase.co', anonKey: 'anon',
    fetchImpl: fakeFetch(async () => jsonRes(201, [{ id: 'bk-1', cancel_token: 'tok-1' }])),
  });
  const created = await good.createBooking({ page_id: 'page-1' });
  assert.equal(created.ok, true);
  assert.equal(created.booking.cancel_token, 'tok-1');
});

test('NEGATIVE CONTROL — owner ops without a session: refuse, zero network', async () => {
  const fetchImpl = fakeFetch(async () => jsonRes(200, []));
  const store = createBookingStore({
    supabaseUrl: 'https://example.supabase.co', anonKey: 'anon',
    getAccessToken: () => null, fetchImpl,
  });
  assert.deepEqual(await store.ownerListBookings(),
    { not_verified: true, reason: 'no_session' });
  assert.deepEqual(await store.writeReminders({ id: 'bk-1' }, PAGE),
    { reminders: 'deferred_no_session' });
  assert.equal(fetchImpl.calls.length, 0);
});

test('store: reminders written under a session — one thread, three messages', async () => {
  const fetchImpl = fakeFetch(async () => jsonRes(201, [{}]));
  const store = createBookingStore({
    supabaseUrl: 'https://example.supabase.co', anonKey: 'anon',
    getAccessToken: () => 'jwt-1', fetchImpl,
  });
  const booking = {
    id: 'bk-9', visitor_name: 'Ana', starts_at: at('10:00'),
    ends_at: at('11:00'), created_at: '2026-10-24T10:00:00.000Z', status: 'confirmed',
  };
  assert.deepEqual(await store.writeReminders(booking, PAGE),
    { reminders: 'written', count: 3 });
  const urls = fetchImpl.calls.map((c) => c.url);
  assert.equal(urls.filter((u) => u.includes('smart_mail_threads')).length, 1);
  assert.equal(urls.filter((u) => u.includes('smart_mail_messages')).length, 3);
  const threadBody = JSON.parse(
    fetchImpl.calls.find((c) => c.url.includes('smart_mail_threads')).init.body);
  assert.equal(threadBody.thread_key, 'booking-bk-9');
});
