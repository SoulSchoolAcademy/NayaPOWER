# Ask Naya Knowledge API — scaffold

**Status: SCAFFOLD — UNMERGED, NOT deployed.** Retrieval, voice, and session are
**MOCK** backends. This proves the plumbing (routes, schema, CORS, error
envelope, privacy logging). It proves nothing about the real brain or her real
voice — the mocks are labeled on every surface.

Full design: `~/workspace/goals/bring-naya-to-life/hidden_files/ask-api/SPEC.md`
(in Shawn's workspace; the canonical spec lives with the goal, not the repo).

## Layout

```
workers/ask-naya-api/
  wrangler.toml   # Worker config; R2/KV bindings are placeholders until deploy
  src/index.js    # router: GET /health, POST /ask, POST /voice
  src/schema.js   # AskResponse validation — the page's render contract
  src/retrieve.js # RetrievalBackend: loadIndex() + BM25-lite search (MOCK default)
  src/compose.js  # extractive composer: chunks → AskResponse; Trait-47 unknown path
  src/voice.js    # voice proxy; MOCK returns a labeled synthetic tone
  src/session.js  # rolling context (MOCK in-memory; KV in production)
  src/mock-data.js# 3 mock brain docs — "MOCK — not the brain"
  test/mock.test.js
```

## Run locally

```bash
cd workers/ask-naya-api
node --test test/        # smoke tests, no dependencies
npx wrangler dev         # local Worker (needs wrangler login only for remote)
```

## What's mock vs real

| Piece | Scaffold | Production (needs Shawn's deploy word) |
|---|---|---|
| Retrieval | keyword BM25-lite over 3 mock docs | R2 versioned `brain-index/<sha>.json` (SPEC §2) |
| Answering | extractive over mock claims | extractive over real index (SPEC §3) |
| Voice | 1.2s synthetic tone, `X-Mock-Audio` labeled | serverless-GPU Chatterbox service + R2 cache (SPEC §4) |
| Session | in-memory Map | Workers KV, 24h TTL (SPEC §5) |

## Deploy checklist (mirrors SPEC.md §8 — all need Shawn's explicit word)

1. `wrangler login` (his account) → fill R2 bucket + KV IDs in `wrangler.toml`
2. `wrangler secret put VOICE_RENDER_URL` (never in the repo)
3. Build the real brain index at a pinned SHA → publish to R2
4. Implement the three `TODO(deploy)` stubs (R2 index load, voice proxy, KV session)
5. `wrangler deploy --dry-run` must pass with zero secrets
6. Deploy, then point the v9 page's bank at `POST /ask`
