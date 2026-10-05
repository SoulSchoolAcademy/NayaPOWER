# Naya Voice — Chatterbox Voice Playback Specification V1

**Status:** PROPOSED — implementation target; not a claim of runtime completion.  
**Purpose:** Define the canonical architecture for optional Naya voice playback across Intelligent Blocks and other approved intelligence projections.

## 1. Decision

Naya Voice playback will use **Chatterbox TTS** as the initial voice-rendering technology, subject to repository/runtime verification and licensing/quality review before production adoption.

The simplest target path is:

**Canonical Intelligent Block text → Naya Voice renderer (Chatterbox) → audio artifact/stream → standard browser audio player**

The browser remains responsible for playback/UI, but **browser-native speech synthesis is not the canonical Naya voice**. It may remain as a fallback only if explicitly labeled as fallback.

## 2. Core architecture

Naya Voice is a presentation capability, not a second intelligence store or authority.

- Canonical content remains the Intelligent Block.
- The voice renderer consumes canonical text.
- The renderer produces audio; it does not create or alter the intelligence.
- Audio may be cached by a deterministic content/voice/version key.
- The player exposes simple **Play / Pause / progress** controls.
- A user should not need to configure TTS to hear an approved block.

Conceptual flow:

**INTELLIGENT BLOCK → TEXT PROJECTION → VOICE RENDERER → AUDIO → PLAYBACK**

## 3. Voice identity

The intended voice is the approved Naya voice, using the canonical voice reference/model asset once located and verified.

Do not guess the location of the voice asset. Search the current repository/runtime and record the exact source, model/version, provenance, license, and hash where available.

If the previously used voice asset cannot be recovered, the system must say **UNKNOWN** rather than silently substituting a different voice and calling it Naya.

## 4. Intelligent Block requirement

Naya Play is an Intelligent Block capability.

Every block eligible for audio should expose a clear playback affordance, for example:

**▶ Naya Play**

Playback should read the canonical human-readable content in a sensible order. The UI must not create a second copy of the intelligence solely for audio.

## 5. Simplicity target

Do not wait for the GitHub app to establish the architecture.

The GitHub app/door is one possible interface. Naya Voice should be implemented behind the canonical capability so that Hub, GitHub, future web/API/MCP/A2A doors, and other authorized interfaces can reuse the same voice service.

**One Brain. Many Doors. One voice capability.**

## 6. Initial implementation path

1. Locate and verify the existing Naya voice reference/model asset.
2. Confirm the current Chatterbox version/runtime and license.
3. Build the smallest local/service renderer that accepts canonical text and returns playable audio.
4. Add deterministic caching keyed by content identity + voice identity + renderer/version.
5. Add the existing/simple browser audio player as the presentation layer.
6. Add Naya Play to Intelligent Blocks.
7. Test empty/very long text, punctuation, Unicode, failure, retry, cache hit, and fallback behavior.
8. Verify latency, audio quality, accessibility, and mobile playback.
9. Only then consider production hosting/optimization.

## 7. Truth and governance requirements

- Voice playback must never imply that spoken content is more authoritative than its source block.
- Unverified/candidate content must retain its source status in the UI.
- No hidden voice service may become a second Brain.
- Do not store credentials or private voice assets in source control.
- Fail clearly if the renderer or voice asset is unavailable.
- Browser-native fallback must be visibly distinguishable from canonical Naya Voice.
- Production use requires verified licensing/rights for the voice model and reference material.

## 8. Quality gate

Naya Voice is not “done” because audio plays once.

Minimum target:

- **≥9/10** overall before birth-ready acceptance.
- **≥9.5/10 (AAA)** preferred.
- Proven on the actual current runtime, not just a local mock.
- Proven with the actual approved Naya voice.
- Proven through an Intelligent Block.
- Proven across supported browser/device paths.
- Proven failure behavior.
- No material accessibility regression.
- No privacy/security regression.

## 9. Open verification items

These remain UNKNOWN until evidence is found:

- Exact existing Naya voice asset location.
- Exact prior voice-cloning workflow/model version.
- Current Chatterbox version used or intended.
- Runtime hosting location.
- Production licensing/rights.
- Final audio caching/storage policy.
- Current Intelligent Block UI insertion point.

These are investigation targets, not assumptions.

## 10. Success

A user opens an Intelligent Block, presses **Naya Play**, and Naya's approved voice reads the canonical block content naturally, reliably, accessibly, and efficiently—without the user needing to understand the underlying voice technology.

That is the experience target.
