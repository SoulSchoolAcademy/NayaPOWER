# Naya Hub GitHub App — Full Functional Spec (Deep Dive, 2026-10-16)

Shawn's directive: think through ALL levels, ALL pages, how everything
functions, and what the app must do. Nothing missing. Done right.

## 1. The one idea

The GitHub App is the Hub's connection to GitHub. Every function of the app
— every room, every flow — communicates through it: GitHub ↔ app ↔ Hub.
A user joins NayaNET, clicks "Connect GitHub," their forked repo connects,
and from then on the Hub and the repo talk both ways. "Smart note this" →
shows up in the Hub. "Design me a page" → the page gets built. "My daily
intelligence report" → it's in the Reports room. Every action anywhere shows
up in the ledger. One connection, the whole system alive.

## 2. Joining: the Connect GitHub flow

1. User joins NayaNET and opens the Hub.
2. They click **Connect GitHub** (Identity room).
3. GitHub asks them to install the Naya Hub app — on their **fork** of the
   Hub repo (forked automatically if they don't have one).
4. The Hub backend stores the installation (tokens in the Secure Vault —
   never in the page, never in chat).
5. Now the Hub can read and write their fork: their pages, their reports,
   their library customizations. Their repo is their mind's home on the
   network; the app is the door.

Multi-user shape: every user has a fork; the app is installed on each fork;
the Hub network operates across them through the shared protocol.

## 3. The data split: Supabase vs GitHub (open question flagged)

Two stores, two jobs. This is the honest architecture:

- **Supabase = live user data.** High-frequency, private, real-time:
  smart notes, lists, mail messages, connections, space membership and
  messages, feed state. Supabase realtime is what makes pages feel alive.
- **GitHub = governed archive + library + pages.** The design library, the
  built pages, intelligence reports as artifacts, the ledger archive, the
  design-law source of truth. Versioned, reviewable, permanent.

The bridge keeps them in sync both ways:
- Supabase event → repo artifact (a smart note saved → archived as a file).
- Repo event (webhook) → Supabase row (a merge lands → ledger activity).

**OPEN (Shawn, 2026-10-16 — his call):** one shared Supabase project with
strict row-level scoping per user (one-click onboarding), or each user
brings their own Supabase project (more setup, more ownership)?
Recommendation: shared with strict scoping — onboarding must stay one click.
The privacy model (what's collective vs private) needs his explicit word
before anything ships — standing rule.

## 4. Room by room: data, and what the app does

**Today / Smart Feed** — Data: smart notes (Supabase). App: the emitter
writes `HUB/FEEDS/smart-feed.json` to the repo through the app; the page
loads it. Supabase → emitter → repo → page. (Being built now.)

**Reports (daily intelligence report room)** — Data: generated reports.
Flow: Naya generates the daily intelligence report → the app writes it as
a versioned artifact to the repo → the Reports room renders it. Every past
report stays browsable; nothing is a screenshot.

**Smart Mail** — Data: messages (Supabase, realtime). App role: thin —
new-mail events can surface as Hub notifications; threads archive to the
repo as governed records. Mail itself is a Supabase realtime concern.

**Smart Lists** — Data: saved smart notes in user groupings/categories
(Supabase). App role: a list can be published/shared as a repo artifact
(a shareable list is a file); importing a shared list reads it back.

**Connections** — Data: contacts gained from Smart Spaces (Supabase). App
role: thin — export/import as artifacts; the live graph is Supabase.

**Spaces** — Data: membership, messages, presence (Supabase realtime).
App role: shared space artifacts (docs, boards) persist to the repo so they
are versioned and forkable.

**Living Intel / Ledger** — Data: the ledger (repo, `LEDGER/`). App role:
CORE. GitHub webhooks (push, PR, issues, checks) flow through the app into
the bridge, which writes ledger entries. Every action anywhere shows up
here. This is "all the actions that happen, shown."

**Intelligent Library** — Data: the design library (repo,
`HUB/design-system/`). App role: read — the Hub always pulls the current
canonical library. No stale copies.

**Naya Design (new room)** — Data: library (read), new pages (write). App
role: CORE. User picks pieces → the Hub composes the page → the app puts
it on a branch as a PR → preview → approve → live.

**Identity** — Data: the user's connection. App role: CORE. Hosts the
"Connect GitHub" flow, shows connection state, which fork, what the app
can touch.

**Get Started** — Data: static guidance (repo). App role: read.

**PowerCast (12th room)** — Data: media + metadata. App role: read/write
for published episodes as repo artifacts (exact shape TBD with the room).

## 5. The core flows, end to end

**"Smart note this."** User says it (in chat with Naya, or to Muse/ChatGPT
through the bridge): the note is captured → written to Supabase (live) →
archived to the repo through the app (governed) → appears as a card in
Today/Smart Feed within a minute. Say it, see it.

**"Design me a page."** User picks pieces in the Naya Design room (or
describes the page): the composer assembles it from the library, applying
the design laws automatically → the app opens a PR with the page → the
design-law check runs on the PR → user previews → approves → live.

**"My daily intelligence report."** On schedule (or on ask), Naya compiles
the report → the app writes it versioned to the repo → it appears in the
Reports room, and the user is notified. Every edition kept.

**Ledger activity.** Anything happens anywhere — a note saved, a page
built, a merge landed, a report issued — webhooks + bridge write it to the
ledger → the Ledger room shows it live.

**Talking to AI (Muse, ChatGPT, etc.).** The bridge exposes the Hub as
tools the assistants can call: `smart_note_this`, `build_page`,
`get_daily_report`, `show_ledger`. The user talks naturally; the assistant
acts through the bridge; the app carries it to the repo; the Hub shows it.
The AI never touches GitHub directly — it goes through the Hub's front
door, governed the whole way.

## 6. The app's complete feature list

A. **Connection & identity** — install flow ("Connect GitHub"), fork setup,
   installation-token handling (backend only, vault-stored).
B. **Read paths** — design library, built pages, feed JSON, reports,
   ledger, library catalog. Always current, never baked.
C. **Write paths** — new pages (branch → PR), feed files, intelligence
   reports, smart-note artifacts, list/space exports.
D. **Event intake** — webhooks (push, PR, issues, check_run) → bridge →
   ledger + live Hub updates.
E. **Review & verification** — PRs as the approval step; design-law checks
   reported on the PR; receipts posted back.
F. **AI tool surface** — the bridge's tool endpoints that assistants call
   (`smart_note_this`, `build_page`, `get_daily_report`, …).
G. **Notifications** — report ready, page approved, note arrived (through
   the Hub; channels TBD).

## 7. Permissions — final, each justified

- **Contents: read & write.** Read: library, pages, feeds, reports. Write:
  pages, feed files, reports, artifacts. The core. (Write switches on in
  phase 2.)
- **Pull requests: read & write.** The approval step for every Naya-built
  page: the diff, the approval, the proof — one place. Your rule is that
  done requires proof; the PR is the proof.
- **Issues: read & write.** The work-request channel: a user asks "design
  me a page" → the Hub tracks it as an issue → Naya builds → the PR closes
  the issue. Requests in, delivery out, all linked.
- **Checks: read & write.** The design-law verification reports on the
  page PR ("this page passes the laws") — machine enforcement, visible at
  the review.
- **Actions: read only.** So the Hub can show deploy/pipeline state
  honestly. (Write never — deploys stay behind your word.)
- **Metadata: read.** Mandatory.
- Events: `push`, `pull_request`, `issues`, `check_run`.

Phase 1 needs only Contents-read + Metadata + events. Everything else
switches on when its feature does.

## 8. What's still open / not ready (honest)

- The **composer** (pieces + page type → finished page, laws enforced).
- The **bridge backend service** (holds the app key, runs the tool
  endpoints, syncs Supabase ↔ GitHub).
- The **Hub's hosting target** (where the Hub actually lives).
- The **Naya Design room UI** (the picker).
- The **Supabase model decision** (shared-with-scoping vs bring-your-own)
  and the **privacy model** — both need Shawn's word; nothing ships
  without it.
- Smart Mail / Lists / Connections / Spaces realtime wiring (Supabase
  side) — designed above, not built.

## 9. Phased rollout

- **Phase 1 — prove the connection (now):** app created, test scope.
  Bridge reads the repo, webhooks arrive. Zero writes.
- **Phase 2 — first flows:** write on; "smart note this" and the first
  composed page go through the app end to end, PR-reviewed.
- **Phase 3 — self-building (Shawn's word):** users connect forks, request
  pages and reports in the Hub, AI assistants build through the bridge,
  the Hub ships itself.
