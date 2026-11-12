# Memberships Run on Smart Mail — The Six Directives
SN-0881 · MEMBERSHIPS / DIRECTIVES
**Created:** 2026-11-04T03:10:00Z

## The Hook
Six locked directives for the membership system — including the big one: login codes go through Smart Mail, not email.

## What Shawn Directed (2026-11-04 02:47Z)
1. **Login codes via Smart Mail, NOT email.** The membership system syncs with Smart Mail. Email is opt-in only: the user enters their email and chooses notifications (e.g. "send my login codes to email"). The simplest path never touches email at all.
2. **"Create membership" buttons = the most beautiful buttons ever.** They are the doorway to the citizen's income — they must feel like it.
3. **Gating:** membership creation requires Pro or Max tier. A non-Pro/Max citizen who clicks "Create membership" goes to the upgrade flow; once Pro/Max, creation unlocks.
4. **Payments stay simple:** Stripe/PayPal, automatic on Power/Pro/Max upgrade.
5. **Smart Scheduler on every page:** must be built, aligned with the booking app — one shared calendar system, different scheduling functions (appointments, posts, mail, messages, reminders, journal).
6. **Sync engine MUST be completed:** Smart Lists + Smart Connections + Messenger all talk to each other. Lists feed the messenger, the messenger feeds the scheduler.

## Why It Matters
Each directive removes a dependency on the old internet: no email for login, no ugly buttons for the money doorway, no paywall confusion, no separate scheduler app, no disconnected lists. One system, one source, everything synced.

## Status
Directives locked 2026-11-04 02:47Z. Gap-closer build in progress: Smart Mail OTP, Pro/Max gating, scheduler mount, sync engine deploy.
