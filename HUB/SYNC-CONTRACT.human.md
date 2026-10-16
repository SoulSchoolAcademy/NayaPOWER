# The Hub Contract — what needs to be completed, how, and why

**Status:** directive from Shawn, 2026-10-16. Research-backed — every claim below was verified against the live repo tip `e19a75d6` before writing. Wishes are labeled as wishes.

## The job in one sentence

A human says "smart note this" → within seconds it appears on the Hub page as a beautiful Smart Note → press play and Naya speaks it → save it → share it. That is the gasp test, and it is the acceptance test for everything below.

## The five pieces and who does what

### 1. The sender — ALREADY BUILT, reuse it, don't rebuild it

The capture bridge exists and is canonical. Shawn was right: the bridge is built.

- **Sender:** `.github/workflows/nayanet-agent-capture.yml` — takes `{ human_note: {subject, text}, naya_note: {text}, idempotency_key, source, invoking_seat }` and POSTs to the edge function.
- **Receiver:** `supabase/functions/v7-smart-note-canonical/index.ts` — builds the full Intelligent Block (`IB-######`): essence, human view, Naya view, machine view, plus provenance, truth, authority, lifecycle, and a receipt. It saves to the Supabase tables and writes the `smart-note.md` projection to GitHub, and returns a Smart Link.

**Why reuse:** there is exactly one capture bridge — no duplicates. Building a second one would be the duplicate-mechanism mistake. The sender side is done; the missing piece is the page reading what the sender writes.

### 2. The transport — the one open decision (teams scorecard it tonight)

Two real options, both viable:

- **A. Supabase-direct:** the page reads published notes straight from Supabase (`nayanet_intelligence_publications` — published notes are already readable without login). Fewest parts, fastest.
- **B. GitHub feed files:** an emitter writes `feeds/smart-notes.json`, the page reads it through the CDN. Matches the public-lane pattern.

**Why the scorecard decides:** both work; the math picks. Whoever scores it tonight, highest score wins, and the page is built against the winner.

**Blocked on Shawn:** nobody can verify the live Supabase state (are the tables really there? is Realtime on? are the secrets set?) without his authorization. That's a genuine human gate — the bridge can't be called "working" until the production side is verified.

### 3. The Hub page receiver — TO BUILD (this is the actual work)

The Hub page (`HUB/app/index.html`) currently mentions Supabase only in marketing copy — it has no data reader at all. This is what gets built:

- A **Smart Feed loader** that reads the published notes (from whichever transport wins) and renders each as the beautiful card: **essence** (the in-a-nutshell) → **human view** → **Naya view** → **machine view**.
- **Play** — uses the existing `naya-voice.js` playback module. Version 1 speaks with the browser's voice; Naya's true cloned voice arrives when Shawn's reference audio is baked in (his call which one the gasp test needs).
- **Save** — version 1 saves in the browser (localStorage). A server-side personal save is a later decision.
- **Share** — the Web Share button plus the Smart Link the pipeline already returns.

**Why this way:** the page renders exactly what the bridge writes — same vocabulary, no translation layer, no new mechanism. The four views on the card map one-to-one to fields the bridge already emits.

### 4. The GitHub output — projection exists, feed file to build

- Per-note `smart-note.md` projection in GitHub: **exists** (the bridge writes it).
- Per-page feed file (`feeds/smart-notes.json`): **to build** — the emitter that regenerates it whenever a note publishes. One feed per page, same pattern for all twelve rooms.

### 5. Alignment with the master directive and the compiler

- **Master directive #2601** is fresh and healthy (refreshes every 10 minutes) — the contract lands there as a work item so every worker sees it.
- **The compiler** (emitters → compiler → MAP-STATE.json) exists today only as prose — no code. So the contract does **not** wait for it: the v7 bridge already speaks the native vocabulary (intelligent block → event → receipt). A Smart Note *is* an intelligent block with a receipt. If Shawn later orders the MAP-STATE compiler built, it reads the same vocabulary — nothing is wasted.

## The decisions that are genuinely Shawn's

1. **Authorize production verification** — check the live Supabase tables, Realtime status, and confirm the capture secrets are set. Nothing else unblocks "it works."
2. **Voice for the gasp test** — browser voice now, or wait for Naya's true cloned voice from your reference audio?
3. **Save** — browser-only for v1, or server-side personal save now?

Everything else the teams decide tonight by scorecard — that's the operating order.

## Then every room, same pattern

The four majors (Hub, Reports, Today, Ledger) go first. Then the same contract shape — receiver-ready page, sender-ready emitter, one feed per room, done-only-when-it-renders — rolls out to all twelve rooms. The working tracker (`goal-1-working-tracker.md`) follows every room from "plumbing in" to "it flows."
