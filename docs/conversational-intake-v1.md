# Conversational Intake v1 — contract (Best-of-Best element #13, step 12)

Typeform's lesson, applied: one question at a time completes at multiples
of a wall-of-boxes form. This build replaces the intake *shape* — the
writes underneath are the writes the current forms already make.

## The engine — `HUB/app/js/naya-intake.js`

One module, dual runtime (browser `window.NayaIntake` / Node exports),
transport injected everywhere. Two flows, one engine:

| Flow | Steps (one screen each) | The write at the end |
|---|---|---|
| `welcome` | name → email → intent (choice) → note (optional, skippable) → review | INSERT `public.invites` `{owner_alias, invitee_email_hash, status: 'joined'}` |
| `invite_accept` | email → name → intent (choice) → review | SELECT the recorded invite by `(owner_alias, invitee_email_hash)`, PATCH `status → 'joined'` |

Rules the engine enforces (all unit-tested in `tests/naya_intake.test.mjs`):

- **One question per screen**, progress shown, **Back always works** and
  keeps answers; the review screen lists every answer with tap-to-change
  (the raw email is shown masked — it is never displayed back in full,
  and never stored anywhere but as its hash).
- **A voice answer counts at every step** — dictation (Web Speech API
  where present, honestly absent where not); spoken choice labels resolve
  to the same values a tap gives. Voice-path and tap-path records are
  byte-identical (proven by test).
- **Nothing writes before review.** The join record is built only from a
  session that reached the review screen complete; a half-finished
  intake creates **no** record (negative control, tested, zero network
  traffic).
- **Abandonment loses nothing already answered** — the session snapshot
  persists on the device and the next visit offers resume where they
  left off.
- **Hash-only emails, everywhere** (the invites canon: "never email").
  The raw address exists only in the form field and on its way into
  SHA-256; no payload, event, or server row carries it.

## The measurement — `public.intake_events`

Migration `20261022213000_conversational_intake_v1.sql` (registered
PENDING in the production migration ledger; applies at the human gate).

Every session emits `started` / `step_completed` / `abandoned` /
`finished` (the finished event carries the hash-only join record as its
summary). `completionStats()` turns events into the only numbers a
completion claim may use: started, finished, abandoned,
completion_rate, abandon_by_step. Rows are anonymous
write-but-never-delete (intake happens before sign-in), owner-read for
the authenticated role; per-table RLS fitting rides the GT-039 gate like
the other visitor-write tables. A local on-device journal mirrors the
events so the panel can show "on this device" stats with zero server.

## The surface

The Hub's `#/welcome` route is the Welcome door (it previously
neutralized straight to the Hub). It renders the intake; an invite
context arrives as `#/welcome?invite=<ownerAlias>` and starts the
invite-accept flow. A finished join writes the remembered-name key the
Hub's boot seam reads, so the device knows the person immediately.

**The frozen remainder, stated plainly:** the flagship template's own
Welcome door and invite-accept surfaces live in the factory sources
under another lane's freeze and are NOT edited here. This build ships
the engine (which the flagship adopts unchanged — it is surface-free)
plus the Hub's reachable surface. Flagship adoption is a follow-on the
moment the freeze lifts.

## The evidence bar

`tools/intake-walkthrough.mjs` runs the scripted old-vs-new comparison:
fields demanded per screen 4 → 1; a mistyped email caught at its own
step instead of at submit; a review beat exists before the write; 5
measurement events emitted where the old forms emitted 0. Human
completion rates are *not* claimed from the walkthrough — they become
claimable from `intake_events` once the migration applies, which is the
point of instrumenting first.
