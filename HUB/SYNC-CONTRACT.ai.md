# Hub Contract — AI tongue (exact values, procedures, constraints)

Verified against tip `e19a75d6` (2026-10-16). Constraints marked [HARD] are human gates; [SCORED] are decided by team scorecard tonight.

## 1. Sender (BUILT — reuse, do not duplicate)

- Workflow: `.github/workflows/nayanet-agent-capture.yml` (6,222 bytes @ tip). `workflow_dispatch` input `payload_json`:
  `{ human_note: {subject: string, text: string}, naya_note: {text: string}, idempotency_key: string, source: string (must start with "nayanet-agent-capture"), invoking_seat: string }`
- Signs in as `naya-runtime` Supabase user; POSTs to edge function. Required repo secrets (Shawn's gate): `NAYA_SUPABASE_URL`, `NAYA_SUPABASE_ANON_KEY`, `NAYA_RUNTIME_EMAIL`, `NAYA_RUNTIME_PASSWORD`.
- Edge function: `supabase/functions/v7-smart-note-canonical/index.ts` (32,096 bytes @ tip). Allocates `IB-######`; builds `NAYANET_INTELLIGENT_BLOCK_V1`:
  `identity`, `type` ∈ {INTELLIGENT_EVENT, SMART_NOTE}, `meaning.{subject, content, summary, in_a_nutshell, interpretation, human, naya, machine, simple}`, `perspectives.{human, child, grandma, naya, machine, learning, meaning, connections, application, value}`, `provenance`, `truth`, `authority`, `lifecycle`, `projections`.
- Persists: `smart_note_events`, `nayanet_cognition_events`, `learning_evidence`, `nayanet_authority_grants`. Returns `{ ok, pipeline: "PROJECTION_VERIFIED" | "SMART_NOTE_CAPTURED_PROJECTION_DEFERRED", intelligent_block_id, transaction_id, smart_link (GitHub blob URL → smart-note.md), feed_verification }`.
- Public read surface: `nayanet_intelligence_publications` (migration `supabase/migrations/20260919155908_smart_feed_collective_publication_v1.sql`): published/revoked + explicit consent; RLS grants anon+authenticated SELECT on published rows.
- NOT the bridge: `tools/note_bridge.py` (note→behavior retrieval gate) and `orchestrator/ts_bridge.py` (TypeScript executor) are different mechanisms. Exactly one capture bridge exists.

## 1b. Bridge contents — exact spec (what must be IN the bridge)

**GitHub side (workflow `.github/workflows/nayanet-agent-capture.yml`):**
- Trigger: `workflow_dispatch` with `payload_json` (schema in §1). No schedule, no push trigger — capture is intentional, never ambient.
- `permissions: contents: read` — least privilege; the workflow never writes the repo.
- Secrets (repo settings → secrets, Shawn's gate): `NAYA_SUPABASE_URL`, `NAYA_SUPABASE_ANON_KEY`, `NAYA_RUNTIME_EMAIL`, `NAYA_RUNTIME_PASSWORD`. Fail-closed: missing secret → `AGENT_CAPTURE_FAILED` exit 1, zero partial writes.
- Behavior: sign in as `naya-runtime` Supabase user → real user JWT → POST to the UNCHANGED receiver → full pipeline (IB allocation, persistence, learning evidence, checkpoint, feed verification, GitHub projection, Smart Link). The workflow never modifies the receiver.

**Supabase side (edge function `v7-smart-note-canonical`):**
- Reads `SUPABASE_URL` / `SUPABASE_ANON_KEY` from function env (never hardcoded).
- `verify_jwt = false` in `supabase/config.toml` ONLY because the function implements its own governed GitHub OIDC verification (documented in-repo) — this is intentional, not a hole; changing it breaks the governed path.
- Writes (service role): `smart_note_events`, `nayanet_cognition_events`, `learning_evidence`, `nayanet_authority_grants`. Public read: `nayanet_intelligence_publications` (published/revoked + explicit consent; RLS: anon+authenticated SELECT on published only).
- **Voice bake (REQUIRED by contract):** at capture time, synthesize the note's essence+human text with Naya's true cloned voice → store MP3 → set `audio_url` on the published record. No note ships without `audio_url`.

**GitHub App / emitter side (to build — the send side):**
- Feed emitter: a workflow (or edge-function hook) triggered on publish that regenerates `feeds/<page>.json` (CDN-served). Needs `permissions: contents: write` scoped to `feeds/**` — nothing else.
- One feed per room (§4). Emitter is idempotent: re-running on the same publish set produces byte-identical output.

## 2. Transport [SCORED]

- Option A — Supabase-direct: page reads `nayanet_intelligence_publications` via REST (anon SELECT on published). Fewest parts, lowest latency.
- Option B — GitHub feed files: emitter regenerates `feeds/smart-notes.json` on publish; CDN serves; page reads via bridge. Matches public-lane pattern.
- Scorecard dimensions: latency, part count, auth surface, failure modes, public/private separation. Highest score wins; page built against winner.
- [VERIFIED LIVE 2026-10-16 ~07:30Z — Shawn authorized] Project `dahisasgpfvziswqvmvm.supabase.co` reachable; REST works. `smart_note_events`, `nayanet_cognition_events`, `nayanet_intelligence_lineage`, `learning_evidence` EXIST. **`nayanet_intelligence_publications` DOES NOT EXIST live** (PGRST205) — the Sep-2026 public-feed migration was never applied. `nayanet_cognition_events` shows 0 rows to anon (RLS or empty). So: before any page reads Supabase, apply the publications migration (or designate the read table) + set RLS + enable Realtime on the read tables. Realtime-enabled status: UNVERIFIED (needs dashboard/service check).
- Secrets: the 4 repo secrets (`NAYA_SUPABASE_URL`, `NAYA_SUPABASE_ANON_KEY`, `NAYA_RUNTIME_EMAIL`, `NAYA_RUNTIME_PASSWORD`) cannot be verified from here — whoever holds them confirms they are set, or the capture workflow fails closed at its first step.

## 3. Page receiver (TO BUILD)

- Target: `HUB/app/index.html` (510KB @ tip) — currently 3 Supabase mentions, all feature-card prose; zero data client; fetches only local JSONs.
- Build: Smart Feed loader module. Source: winning transport. Render mapping (exact):
  - essence → `meaning.in_a_nutshell` (fallback `meaning.summary`)
  - human view → `perspectives.human` (fallback `meaning.human`)
  - Naya view → `perspectives.naya` (fallback `meaning.naya`)
  - machine view → `perspectives.machine` (fallback `meaning.machine`)
- Play: `HUB/app/js/naya-voice.js` (exists: checks `_bakedAudioCache[blockId]` FIRST, then falls back to speechSynthesis). [DECIDED — Shawn 2026-10-16] **Her real voice, always. No browser voice.** The page's module already supports pre-baked Naya cloned-voice audio via `registerBakedAudio(blockId, audioUrl)` — so the contract REQUIRES: every published note carries `audio_url` (baked with her true cloned voice at capture time); the feed loader registers it; play uses it. The speechSynthesis fallback must never be hit in production.
- Save: v1 = localStorage (page already uses `naya.activity`, 50-item cap). [DECIDED — Naya 2026-10-16, Shawn: "I don't know what you're asking"] Browser V1 now — simplest, works today, zero new infrastructure. Server-side personal save later with the personal lane (D1 NOT authorized — untouched).
- Share: `navigator.share` (×4 in app) + `clipboard` (×4) + Smart Link from capture response (OTP-gated viewer `nayanet-smart-note-viewer` exists).
- Required states: loading, empty, error, malformed-payload, offline.

## 4. GitHub output + per-room receive spec

- Per-note projection `.naya/.../IB-######/smart-note.md`: EXISTS (bridge writes it).
- Per-page feed file `feeds/<page>.json`: TO BUILD — emitter regenerates on publish. Pages: smart-notes, reports, today, ledger, then library, connect, connections, lists, mail, spaces, settings.
- **What each room needs to receive (same pattern, all 11 rooms + home):** a loader that (a) fetches its feed (winning transport), (b) renders its cards, (c) handles loading/empty/error/malformed/offline. Room-specific: Reports renders `report` objects (type/date/nutshell/sections/body_url); Today renders `today_highlight` (nutshell + top-note essences); Ledger renders `action_receipt` stream (system activity); Hub renders full Smart Note cards + personal activity feed. **What GitHub needs to send:** the emitter from §1b writing each room's feed on every relevant publish — no room without its emitter, no emitter without its room.
- **What Supabase needs (setup checklist, in order):** 1. Apply the `nayanet_intelligence_publications` migration (missing live — verified). 2. RLS: anon+authenticated SELECT on published rows only; service-role write. 3. Enable Realtime on the read tables. 4. Confirm the 4 repo secrets set. 5. Voice-bake step emits `audio_url` per note. Until 1–4 are done, the page reads the GitHub feed-file lane (Option B) — the contract does not stall on Supabase.

## 5. Compiler/directive alignment

- Master directive #2601: open, fresh (compiled 2026-10-16 07:12:13Z, ≤60-min freshness contract, single writer dispatcher STEP 4b). Contract lands as a directive work item.
- Compiler (emitters → compiler → HUB/MAP-STATE.json → window.NayaPowerRuntime): NOT FOUND at tip — prose only, zero bytes. Contract uses v7 IB vocabulary directly (block/event/receipt native to the bridge output). MAP-STATE compiler, if later ordered, consumes the same vocabulary — no rework.

## 6. Acceptance (gasp test)

1. "smart note this" → 2. renders on Hub page within seconds → 3. play → Naya speaks → 4. save persists → 5. share produces a working link. Latency measured capture→render. Bridge-complete = this passes, not code existing.

## 7. Human gates ([HARD])

1. [CLEARED 2026-10-16 ~07:30Z] Production Supabase verification — Shawn authorized; verified live (see §2 findings).
2. [DECIDED — Shawn 2026-10-16] Voice: her real voice, always. Pre-baked per-note audio required; browser TTS never.
3. [DECIDED — Naya 2026-10-16] Save: browser V1 (localStorage) now; server-side with the personal lane later.
