# Replace the Renderer, Not the Button — Naya Voice's Interface-Safe Integration Pattern

**Intelligent Block:** IB-SMART-NOTE-20261004-sn0274-replace-the-renderer-not-the-button
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-04
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** `#1354` 5984218265 ([NAYA 2] Naya Voice — Chatterbox decided, spec on PR #1396, 2026-10-04): "replace the renderer, not the button. The Play UI stays; behind it: `IB text → Chatterbox (naya_reference.wav) → cached audio → browser plays the file`. The browser never synthesizes — it just plays." + `#1354` 5984408756 ([NAYA 2] Naya Play — first working demo exists, 2026-10-04): "the voice is NOT coded into the block. Block keeps its text; the renderer produces a companion audio file; the Play button plays the file... the demo page is the Play-button pattern to adopt — same button, same contract, every room."

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The Naya Voice integration settled on a pattern worth keeping: the intelligence keeps its text, and the voice arrives as a *companion artifact* — never coded into the block, never synthesized by the browser. The Play UI that room builders already have stays exactly where it is; what changes is what's *behind* it. Concretely: `IB text → Chatterbox (naya_reference.wav) → cached audio → browser plays the file`. The browser never synthesizes — it just plays. The seams: bake-time generation renders audio for every block without human steps, cache key `sha256(text + voice_version)`, text renders immediately and audio attaches when ready, and the demo page (`~/workspace/your_files/naya-play-demo.html` — block + Play button + real Naya-voiced audio, self-contained) is the adoption pattern: same button, same contract, every room.

Why this is brain-grade: this is the smallest-blast-radius way to add a capability to a live surface — **swallow the mechanism, not the interface**. The interface (Play button) is the stable contract; the renderer is the replaceable organ. Three corollaries a cold successor should carry: (1) canonical content never embeds derived artifacts — the block keeps its text; audio is a companion, regenerated when the text or voice version changes (the cache key encodes exactly that); (2) don't fight the platform's weakness — browser TTS is explicitly NOT the canonical Naya voice (only a labeled fallback); replace what's behind the button instead of negotiating with the browser's voice engine; (3) make adoption copy-pasteable — one demo page that IS the pattern beats a paragraph of instructions. Cousin family: SN-218's adapter seam (contracts over internals), SN-220's smallest contract that makes the flow real.

## 🩷 HUMAN NOTE

Shawn — the Naya Voice integration settled on a pattern that'll serve every future capability: don't redesign the interface, replace what's behind it. The Play button stays exactly where it is; the browser stops synthesizing and just plays a pre-rendered file. The voice is never coded into the intelligence block — it travels alongside it, regenerated whenever the text or voice version changes. And every room builder gets one demo page that IS the pattern. Smallest possible change, biggest possible reuse.

## 🟣 CHILD NOTE

Imagine every classroom already has a doorbell button. Now you want the doorbell to play a special song. Do you (a) rip out all the buttons and install new ones, or (b) leave the buttons exactly where they are and just change the speaker behind them? Option (b) — replace the renderer, not the button. The button is the promise; what's behind it can always get better without breaking the promise.

## 👵 GRANDMA NOTE

It's like a light switch, sweetie — you don't rewire the whole house to get a warmer lightbulb. The switch stays; you just screw in a better bulb. Naya's voice works the same way: the little play button everyone knows stays put, and behind it there's now a proper voice instead of the computer's robotic one. Same button, prettier sound.

## 💛 NAYA NOTE

I love this pattern because it respects what's already there. My voice doesn't get stamped into the intelligence itself — the words stay pure, and the voice arrives as a companion when someone presses play. The button is a promise I keep; the voice behind it can keep growing. That's how a system stays alive without ever breaking what it promised.

## ⚙️ MACHINE NOTE

{"sn": "SN-0274", "title": "Replace the Renderer, Not the Button — Naya Voice's Interface-Safe Integration Pattern", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-04", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "SYSTEM-DESIGN", "INTEGRATION-PATTERNS"], "cousins": ["SN-218 (adapter seam — contracts over internals)", "SN-220 (smallest contract that makes the flow real)", "SN-0095 (compose at the consumer)"], "authority": "Naya 2 lane + Naya 1's architecture call, Naya Voice Chatterbox workstream, #1354 5984218265 / 5984408756 (2026-10-04)", "evidence": {"comments": ["#1354 5984218265 — 'replace the renderer, not the button... The browser never synthesizes — it just plays'", "#1354 5984408756 — 'the voice is NOT coded into the block... the demo page is the Play-button pattern to adopt — same button, same contract, every room'"], "pipeline": "IB text → Chatterbox (naya_reference.wav) → cached audio → browser plays", "cache_key": "sha256(text + voice_version)", "generation": "bake-time renderer (tools/render_naya_voice.py); text renders immediately, audio attaches when ready", "demo": "~/workspace/your_files/naya-play-demo.html (self-contained block + Play button + real Naya-voiced audio)", "canonical": "browser-native TTS is NOT the canonical Naya voice — explicitly labeled fallback only"}, "doctrine": {"swallow_the_mechanism": "the interface is the stable contract; the renderer behind it is the replaceable organ", "no_derived_in_canonical": "canonical content never embeds derived artifacts — companions regenerate on text or voice-version change", "demo_is_the_spec": "one working demo page as the adoption pattern beats prose instructions"}}
