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

## 2. Transport [SCORED]

- Option A — Supabase-direct: page reads `nayanet_intelligence_publications` via REST (anon SELECT on published). Fewest parts, lowest latency.
- Option B — GitHub feed files: emitter regenerates `feeds/smart-notes.json` on publish; CDN serves; page reads via bridge. Matches public-lane pattern.
- Scorecard dimensions: latency, part count, auth surface, failure modes, public/private separation. Highest score wins; page built against winner.
- [HARD] Production verification requires Shawn's authorization: confirm migrations applied to live project, Realtime enabled on read tables, four repo secrets set. No `supabase` connector configured in this environment — cannot verify without his go-ahead.

## 3. Page receiver (TO BUILD)

- Target: `HUB/app/index.html` (510KB @ tip) — currently 3 Supabase mentions, all feature-card prose; zero data client; fetches only local JSONs.
- Build: Smart Feed loader module. Source: winning transport. Render mapping (exact):
  - essence → `meaning.in_a_nutshell` (fallback `meaning.summary`)
  - human view → `perspectives.human` (fallback `meaning.human`)
  - Naya view → `perspectives.naya` (fallback `meaning.naya`)
  - machine view → `perspectives.machine` (fallback `meaning.machine`)
- Play: `HUB/app/js/naya-voice.js` (exists: Web Speech API, voice cascade Google US English → Samantha → Zira → en-US female; architected for pre-baked MP3 swap). Page has 194 play-UI mentions, 0 speechSynthesis — wire module to UI. [HARD] True cloned voice needs Shawn's reference audio baked (Chatterbox spec PROPOSED; sample `BRAIN/10-INTERFACES/naya-voice-sample-v1.mp3`); browser TTS is fallback, not canonical.
- Save: v1 = localStorage (page already uses `naya.activity`, 50-item cap). [HARD] Server-side personal save needs Shawn's decision; D1 is NOT authorized — untouched.
- Share: `navigator.share` (×4 in app) + `clipboard` (×4) + Smart Link from capture response (OTP-gated viewer `nayanet-smart-note-viewer` exists).
- Required states: loading, empty, error, malformed-payload, offline.

## 4. GitHub output

- Per-note projection `.naya/.../IB-######/smart-note.md`: EXISTS (bridge writes it).
- Per-page feed file `feeds/<page>.json`: TO BUILD — emitter regenerates on publish. Pages: smart-notes, reports, today, ledger, then rooms 5–12.

## 5. Compiler/directive alignment

- Master directive #2601: open, fresh (compiled 2026-10-16 07:12:13Z, ≤60-min freshness contract, single writer dispatcher STEP 4b). Contract lands as a directive work item.
- Compiler (emitters → compiler → HUB/MAP-STATE.json → window.NayaPowerRuntime): NOT FOUND at tip — prose only, zero bytes. Contract uses v7 IB vocabulary directly (block/event/receipt native to the bridge output). MAP-STATE compiler, if later ordered, consumes the same vocabulary — no rework.

## 6. Acceptance (gasp test)

1. "smart note this" → 2. renders on Hub page within seconds → 3. play → Naya speaks → 4. save persists → 5. share produces a working link. Latency measured capture→render. Bridge-complete = this passes, not code existing.

## 7. Human gates ([HARD])

1. Authorize production Supabase verification + secrets confirmation.
2. Voice for gasp test: browser TTS v1 vs true cloned voice from Shawn's reference audio.
3. Save: localStorage v1 vs server-side personal save.
