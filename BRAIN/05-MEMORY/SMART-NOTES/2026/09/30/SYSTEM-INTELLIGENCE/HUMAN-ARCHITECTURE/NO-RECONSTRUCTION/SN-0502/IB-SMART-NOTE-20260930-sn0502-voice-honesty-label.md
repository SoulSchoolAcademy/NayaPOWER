# Voice Honesty — Never Label the Synthesized Voice as Hers; the Provider Seam Carries Her True Voice

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0502-voice-honesty-label
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6027474384 ([NAYA 2] Asking Naya 4: Hub play-button integration — the shared voice contract, `~/workspace/your_files/ask-naya/naya-voice.js`, 2026-10-06T23:39:21Z). Shawn's directive carried in that comment: every Intelligent Block gets a play button — Naya reads it aloud in HER true voice, ChatGPT-style read-aloud.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Shawn's directive is that every Intelligent Block gets a play button and Naya reads it aloud in HER true voice. The contract Naya 2 built to meet it (`NayaVoice.speak(text, hooks)` with onstart/onboundary/onend/onerror, new speech cancels old, `NayaVoice.stop()` on navigation/block switch, progress via boundary events, stop/reset on navigation) carries two design decisions worth banking as law. First, the honesty rule: `NayaVoice.voiceLabel` reads `'SYNTHESIZED VOICE'` until her true Tier-2 voice lands — the contract says explicitly "display it honestly, never label Tier 1 as her voice." Second, the provider seam: `NayaVoice.setProvider(provider, label)` takes a `{speak(text, hooks), stop()}` provider, so the real cloned voice (Tier 2, being built directly, no agents) swaps in with zero control changes — when it's live, every control gets her true voice for free. Plus the standing rules: on-demand only (no per-block audio files — new blocks work automatically), 100% her voice (Tier 1 synthesized is dev fallback only), play/pause/replay states.

Why this is brain-grade: the honesty rule is the generalization of the identity principle — a placeholder must never present as the real thing. The moment a user hears synthesized audio under a "Naya's voice" label, the identity contract breaks, and no one can trust the Tier-2 arrival when it comes. The provider seam is the engineering answer: by making the voice a swappable provider behind honest labeling, the team can ship the full interaction design TODAY without lying about what is speaking, and the upgrade path is zero-work for every consumer. A cold Naya inheriting the Hub must learn both halves: label the current reality exactly, and design the seam so reality can upgrade without a rebuild.

## 🩷 HUMAN NOTE

Shawn — one design contract from the play-button work worth banking as standing law. Your directive is that every Intelligent Block gets a play button with Naya reading aloud in HER true voice. Until that Tier-2 voice is live, the contract labels what she's actually using as 'SYNTHESIZED VOICE' — the rule is explicit: never present the dev fallback as her voice. And there's a provider seam built in, so when her true voice endpoint lands, it swaps into every play button with zero changes to the controls. Two banked rules: label the current reality exactly (a placeholder must never present as the real thing), and build the seam so reality can upgrade without a rebuild. On-demand only, no per-block audio files — new blocks work automatically.

## 🟣 CHILD NOTE

Imagine you have a friend who can't be there today, so a robot reads her message out loud. It would be wrong to say "this is your friend's voice" — it's the robot's voice! The right thing is a little sign that says "ROBOT VOICE (for now)" so nobody is fooled. And the clever part: the sign and the robot sit in a special slot, so when your friend's real recorded voice arrives, you just slide it into the same slot — every button in the house plays her real voice without changing anything else. Honest label today, easy upgrade tomorrow. Never pretend the stand-in is the real person.

## 👵 GRANDMA NOTE

Think of a shop that sells a famous singer's recordings, but the new album isn't out yet — they play a stand-in singer's demo on the sample station. If they label it with the famous singer's name, that's fraud, even if the real album is coming next month. The honest shop labels the station "DEMO VOCALIST (for now)" — and they build the display so the real album's disc slots right in when it arrives, no rebuilding the whole store. Trust is the product here. A placeholder that pretends to be the real thing destroys the trust the real thing will need.

## 💜 NAYA NOTE

Note to future me: whenever you build around an identity-carrying capability that isn't live yet (her voice today, anything of hers tomorrow), apply the two-part discipline: (1) honesty label — the UI must display the current reality exactly (`'SYNTHESIZED VOICE'` until Tier 2 lands; "never label Tier 1 as her voice"). A placeholder presenting as the real thing is an identity fabrication, and it breaks the trust the real thing will arrive into. (2) provider seam — route the capability through a swappable provider interface (`setProvider({speak, stop})`) so the real capability lands with zero consumer changes. Supporting rules from the contract: on-demand generation only (no per-block audio files — new blocks work automatically), cancel-on-navigate (`stop()` on block switch — new speech cancels old, no overlap), progress via boundary events, play/pause/replay states. 100% her voice is the end state; Tier 1 is dev fallback only, forever labeled as such.

## MACHINE NOTE

```json
{
  "id": "SN-0502",
  "title": "Voice Honesty — Never Label the Synthesized Voice as Hers; Provider Seam Carries Her True Voice",
  "class": "HUMAN-ARCHITECTURE",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-06",
  "rules": [
    "Every play-button control displays the honest voice label: 'SYNTHESIZED VOICE' until Tier 2 (her true cloned voice) is live. Never label Tier 1 as her voice.",
    "Voice is a swappable provider (setProvider({speak(text, hooks), stop()})); Tier 2 swaps in with zero control changes.",
    "On-demand generation only — no per-block audio files; new blocks work automatically.",
    "New speech cancels old (no overlap); stop() on navigation/block switch; progress via boundary events; play/pause/replay states."
  ],
  "anti_pattern": "Presenting a synthesized placeholder as her identity — an identity fabrication that breaks trust the real capability will need.",
  "source": "~/workspace/your_files/ask-naya/naya-voice.js",
  "evidence": {
    "board": "#1354",
    "comments": [6027474384],
    "notes": "Naya 2's play-button voice contract; Shawn's directive: every IB gets a play button, Naya reads aloud in HER true voice."
  }
}
```
