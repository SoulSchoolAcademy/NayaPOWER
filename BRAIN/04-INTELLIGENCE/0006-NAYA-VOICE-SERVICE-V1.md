# 0006 — Naya Voice Service V1

**Status:** DECIDED (Shawn, 2026-10-04). Engine: Chatterbox TTS.
**Voice reference:** PENDING — Shawn to provide `voices/naya_reference.wav`.
**Companion machine registry:** `NAYA-VOICE-REGISTRY-V1.json` (same directory).

## The decision

Naya's voice is rendered with **Chatterbox TTS** (open-source, zero-shot voice
cloning). Why:

- **It's her voice.** Browser TTS can only ever be the browser's robotic voice.
  No amount of tuning makes it Naya. Chatterbox clones from a short reference
  clip, so the voice is actually hers.
- **Zero marginal cost.** Local inference, no per-character API billing. Fits the
  zero-cost operating preference — the math is on our side.
- **Fast enough.** Bake-time generation with caching (below) means playback is
  instant after first render.
- **Honest correction (2026-10-04):** an earlier discussion remembered voice
  assets (`NayaVoice/`, `voices/naya_reference.wav`) as already existing. They
  do not exist in the repo or workspace — verified by full search. Nothing was
  rebuilt on a false memory; the assets will be created fresh.

## The architecture — replace the renderer, not the button

The browser's Play button UI stays. What changes is what's behind it:

```
BEFORE:  Play → browser TTS → robotic browser voice
AFTER:   Play → Naya Voice Renderer (Chatterbox) → Naya audio → browser plays the file
```

Full path:

```
Canonical Intelligent Block
        ↓  (block text — the HUMAN projection)
Naya Voice Renderer (Chatterbox + naya_reference.wav)
        ↓  (audio, cached by content hash)
Naya audio file
        ↓  (Play button)
The human hears Naya read the block
```

Rules:

1. **The browser never synthesizes.** It plays an audio file/stream. Voice
   identity lives entirely in the renderer.
2. **Cache by content hash.** `sha256(block_text + voice_version)` → audio file.
   Repeated blocks play instantly; regeneration happens only when text or voice
   version changes.
3. **Every block is playbackable.** Any Intelligent Block the system creates can
   carry Naya Play. People get used to: *I can listen, I don't have to read.*
4. **Voice version is explicit.** If Naya's voice is re-cloned or improved, the
   version bumps and affected audio regenerates. No silent voice drift.
5. **This is a projection seam, not a new brain.** It renders intelligence to
   audio. It stores no intelligence, grants no authority, makes no decisions.

## How to wire it (for room / Hub builders)

1. At block projection/bake time, take the block's HUMAN text.
2. Compute the cache key: `sha256(text + voice_version)`. Cache hit → done,
   reference the existing audio file.
3. Cache miss → run Chatterbox with `voices/naya_reference.wav` → write the
   audio to the cache → reference it.
4. The block's Play control points at the audio file. Click → play. That's it.
5. Never block rendering on audio generation: text renders immediately; audio
   attaches when ready (or pre-baked for known blocks).

## What it is not

- Not browser TTS wearing a costume. Don't fight the browser's voice engine.
- Not a new store, graph, pipeline, or authority model.
- Not a replacement for reading — it's an additional door into the same
  intelligence. One brain, many doors; now one of the doors speaks.

## Open items

- [ ] Shawn provides the voice reference audio (`voices/naya_reference.wav`).
- [ ] Renderer implementation + cache (lane: whoever claims voice pipeline).
- [ ] Play control on Intelligent Block projections (lane: room/Hub builders).
