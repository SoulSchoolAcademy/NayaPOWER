/*
 * booking-core.mjs — the Booking block's pure logic (Best-of-Best map
 * element #17, build step 17). No I/O, no DOM: every rule the database
 * enforces (migration 20261022210000_booking_v1.sql) is mirrored here so
 * the Hub page can refuse kindly and instantly, and the database refuses
 * identically when a client skips the page. The contract test
 * (tests/test_booking_contract.py) fails if the two ever drift.
 *
 * The rules, in plain words:
 *   - A booking page is a named link (Smart Links name grammar), owned.
 *   - Availability is windows: weekday + local time range + timezone.
 *   - A booking must fit inside ONE window on ONE local day, last exactly
 *     the page's duration, and never overlap a confirmed booking.
 *   - Cancelling frees the slot: cancelled rows block nothing.
 *   - Both sides get reminded through the Smart Mail store: the owner
 *     hears at once and again a day ahead; the visitor a day ahead.
 *   - Calendar sync is element #21's first plug-in and is NOT built
 *     here: the only honest state this block reports is the page's own
 *     calendar_sync_state, which ships 'not_connected'.
 */

export const SLUG_SHAPE = /^[a-z0-9][a-z0-9-]{1,62}$/;
export const REMINDER_LEAD_MS = 24 * 60 * 60 * 1000;
export const WEEKDAY_NAMES = [
  'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday',
];

// ——— Validation ————————————————————————————————————————————————

export function validatePageInput(input) {
  const slug = String((input && input.slug) || '').trim().toLowerCase();
  const title = String((input && input.title) || '').trim();
  const duration = Number(input && input.duration_minutes);
  if (!SLUG_SHAPE.test(slug)) return { ok: false, reason: 'slug_shape' };
  if (!title) return { ok: false, reason: 'title_required' };
  if (!Number.isInteger(duration) || duration < 5 || duration > 480) {
    return { ok: false, reason: 'duration_range' };
  }
  return {
    ok: true,
    page: { slug, title, duration_minutes: duration, active: true },
  };
}

export function validateWindow(input) {
  const weekday = Number(input && input.weekday);
  const start = String((input && input.start_time) || '');
  const end = String((input && input.end_time) || '');
  const timezone = String((input && input.timezone) || 'UTC').trim() || 'UTC';
  if (!Number.isInteger(weekday) || weekday < 0 || weekday > 6) {
    return { ok: false, reason: 'weekday_range' };
  }
  if (!/^\d{2}:\d{2}(:\d{2})?$/.test(start) || !/^\d{2}:\d{2}(:\d{2})?$/.test(end)) {
    return { ok: false, reason: 'time_shape' };
  }
  if (end <= start) return { ok: false, reason: 'window_inverted' };
  return {
    ok: true,
    window: {
      weekday,
      start_time: start.slice(0, 5),
      end_time: end.slice(0, 5),
      timezone,
    },
  };
}

// ——— Timezone helpers (Intl is the only dependency) —————————————

function partsInTz(instant, timeZone) {
  const dtf = new Intl.DateTimeFormat('en-US', {
    timeZone,
    weekday: 'short',
    year: 'numeric', month: '2-digit', day: '2-digit',
    hour: '2-digit', minute: '2-digit', second: '2-digit',
    hour12: false,
  });
  const parts = {};
  for (const p of dtf.formatToParts(instant)) parts[p.type] = p.value;
  const weekday = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    .indexOf(parts.weekday);
  return {
    dateStr: `${parts.year}-${parts.month}-${parts.day}`,
    timeStr: `${String(parts.hour % 24).padStart(2, '0')}:${parts.minute}`,
    weekday,
  };
}

function tzOffsetMs(timeZone, instant) {
  const p = partsInTz(instant, timeZone);
  const [hh, mm] = p.timeStr.split(':').map(Number);
  const asUtc = Date.UTC(
    Number(p.dateStr.slice(0, 4)), Number(p.dateStr.slice(5, 7)) - 1,
    Number(p.dateStr.slice(8, 10)), hh, mm, 0,
  );
  return asUtc - Math.floor(instant.getTime() / 1000) * 1000;
}

// A local (date, time) in a timezone → the UTC instant it names.
export function zonedTimeToUtc(dateStr, timeStr, timeZone) {
  const [y, m, d] = dateStr.split('-').map(Number);
  const [hh, mm] = timeStr.split(':').map(Number);
  const guess = Date.UTC(y, m - 1, d, hh, mm);
  let utc = guess - tzOffsetMs(timeZone, new Date(guess));
  const second = guess - tzOffsetMs(timeZone, new Date(utc));
  if (second !== utc) utc = second;
  return new Date(utc);
}

export function weekdayOfLocalDate(dateStr, timeZone) {
  // Noon UTC on the date is safely inside the local day for every zone.
  const [y, m, d] = dateStr.split('-').map(Number);
  return partsInTz(new Date(Date.UTC(y, m - 1, d, 12)), timeZone).weekday;
}

// ——— The slot rules (mirror bookings_guard_slot in the migration) ————

export function rangesOverlap(aStart, aEnd, bStart, bEnd) {
  return aStart < bEnd && bStart < aEnd; // half-open [start, end)
}

// True when [startsAt, endsAt] fits inside ONE window on ONE local day.
export function fitsAvailability(windows, startsAtISO, endsAtISO) {
  const starts = new Date(startsAtISO);
  const ends = new Date(endsAtISO);
  if (!(ends > starts)) return false;
  return (windows || []).some((w) => {
    const s = partsInTz(starts, w.timezone);
    const e = partsInTz(ends, w.timezone);
    return s.weekday === w.weekday
      && s.dateStr === e.dateStr
      && s.timeStr >= w.start_time
      && e.timeStr <= w.end_time;
  });
}

export function computeSlots({ windows, booked, dateStr, durationMinutes, nowISO }) {
  const now = nowISO ? new Date(nowISO).getTime() : 0;
  const taken = (booked || []).filter((b) => b.status !== 'cancelled');
  const slots = [];
  for (const w of windows || []) {
    if (weekdayOfLocalDate(dateStr, w.timezone) !== w.weekday) continue;
    let cursor = w.start_time;
    while (true) {
      const start = zonedTimeToUtc(dateStr, cursor, w.timezone);
      const end = new Date(start.getTime() + durationMinutes * 60000);
      const endLocal = partsInTz(end, w.timezone);
      if (endLocal.dateStr !== dateStr || endLocal.timeStr > w.end_time) break;
      const isTaken = taken.some((b) => rangesOverlap(
        start.toISOString(), end.toISOString(), b.starts_at, b.ends_at,
      ));
      slots.push({
        starts_at: start.toISOString(),
        ends_at: end.toISOString(),
        taken: isTaken,
        past: start.getTime() < now,
        available: !isTaken && start.getTime() >= now,
      });
      cursor = endLocal.timeStr;
      if (cursor <= w.start_time) break; // safety: never loop a day away
    }
  }
  return slots.sort((a, b) => a.starts_at.localeCompare(b.starts_at));
}

// The whole request judged at once — the page's pre-flight of the same
// verdicts the database trigger gives ('outside_availability',
// 'slot_taken'). Reasons are the migration's error names, verbatim.
export function validateBookingRequest({ page, windows, booked, request }) {
  const name = String((request && request.visitor_name) || '').trim();
  if (!name) return { ok: false, reason: 'visitor_name_required' };
  const starts = new Date(request.starts_at);
  const ends = new Date(request.ends_at);
  if (Number.isNaN(starts.getTime()) || Number.isNaN(ends.getTime()) || ends <= starts) {
    return { ok: false, reason: 'span_invalid' };
  }
  if ((ends - starts) / 60000 !== page.duration_minutes) {
    return { ok: false, reason: 'duration_mismatch' };
  }
  if (!fitsAvailability(windows, request.starts_at, request.ends_at)) {
    return { ok: false, reason: 'outside_availability' };
  }
  const clash = (booked || [])
    .filter((b) => b.status !== 'cancelled' && b.id !== request.id)
    .some((b) => rangesOverlap(
      request.starts_at, request.ends_at, b.starts_at, b.ends_at,
    ));
  if (clash) return { ok: false, reason: 'slot_taken' };
  return {
    ok: true,
    booking: {
      page_id: page.id || page.page_id,
      visitor_name: name,
      visitor_email_hash: request.visitor_email_hash || null,
      starts_at: starts.toISOString(),
      ends_at: ends.toISOString(),
      note: request.note ? String(request.note).slice(0, 1000) : null,
      status: 'confirmed',
    },
  };
}

// ——— Reminders (Smart Mail store: one thread per booking) ——————————

export function reminderThreadKey(bookingId) {
  return `booking-${bookingId}`;
}

export function planReminders({ booking, page }) {
  const startMs = new Date(booking.starts_at).getTime();
  const createdMs = new Date(booking.created_at || booking.starts_at).getTime();
  const dayAhead = new Date(Math.max(createdMs, startMs - REMINDER_LEAD_MS));
  const when = new Date(booking.starts_at).toISOString();
  return [
    {
      side: 'owner', kind: 'new_booking',
      at: new Date(createdMs).toISOString(),
      body: `${booking.visitor_name} booked "${page.title}" for ${when}.`,
    },
    {
      side: 'owner', kind: 'reminder',
      at: dayAhead.toISOString(),
      body: `Reminder: "${page.title}" with ${booking.visitor_name} is at ${when}.`,
    },
    {
      side: 'visitor', kind: 'reminder',
      at: dayAhead.toISOString(),
      body: `Reminder: your booking "${page.title}" is at ${when}.`,
    },
  ];
}

// The Smart Mail rows for a plan — ONLY the columns the flagship store
// evidences (thread: owner_alias, subject, participants, status,
// direction, thread_key; message: thread_key, sender, sender_name, body,
// direction, created_at). The thread lives in the PAGE OWNER's inbox;
// the visitor's reminder is the same thread's record for their side.
export function reminderRows({ booking, page }) {
  const threadKey = reminderThreadKey(booking.id);
  const thread = {
    owner_alias: page.owner_alias,
    subject: `Booking: ${page.title} with ${booking.visitor_name}`,
    participants: booking.visitor_name,
    status: 'open',
    direction: 'inbound',
    thread_key: threadKey,
  };
  const messages = planReminders({ booking, page }).map((r) => ({
    thread_key: threadKey,
    sender: 'booking',
    sender_name: r.side === 'owner' ? booking.visitor_name : page.owner_alias,
    body: r.body,
    direction: r.side === 'owner' ? 'inbound' : 'outbound',
    created_at: r.at,
  }));
  return { thread, messages };
}

// ——— Plug-ins: the honest placeholder (element #21 owns the build) ———

export function pluginStates(page) {
  return [{
    id: 'calendar',
    label: 'Calendar sync',
    state: (page && page.calendar_sync_state) || 'not_connected',
    note: 'Bookings live in NayaNET only until calendar sync connects.',
  }];
}
