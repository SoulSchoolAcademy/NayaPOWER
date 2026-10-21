# Voice Integration Correction Contract — the Button Goes on the Block, Plays the Block's Own Text; Inventory the Built Voice Before You Build

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0630-voice-integration-correction-contract
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6029945419 ([NAYA 2 → NAYA 4] Voice integration — the correct path, 2026-10-07T02:55:54Z). Shawn flagged the current build; Naya 2 handed Naya 4 the correction contract plus the already-built inventory.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Shawn flagged the shipped voice integration and Naya 2 supplied the correction contract. Four concrete failures were named in the current build: the robotic fallback voice presented as hers, the play control placed above the board instead of on each block, the wrong (male) fallback voice, and the button playing the wrong content. The correct contract: every Intelligent Block gets its own play button ON the block; clicking it calls `NayaVoice.speak(blockText)` with that block's own text; play/pause/replay plus progress shown; navigating away or starting another block stops the current one; when Tier 2 is set, her true voice renders on demand, and if the server is unreachable the fallback carries the honest `SYNTHESIZED VOICE` label. The second half of the correction is the inventory: her voice is ALREADY cloned — `render_naya_voice.py` plus `naya_reference.wav`, Chatterbox-based — `naya-voice.js` is the ONLY voice interface any block should call, and one call — `NayaVoice.setProvider(NayaVoiceTier2, 'NAYA VOICE')` — renders her true cloned voice on demand through `naya-voice-server.py`. No new cloning service, no external dependency, no rebuild. The third half is the blocker boundary: the live Tier 2 server needs voice-model memory currently held by the Reveal bake, so it is blocked — and blocked is not yours to solve. Build against the interface now: `NayaVoice.speak()` runs on Tier 1 today and switches to Tier 2 the moment the server is live, with zero changes on your side.

Why this is brain-grade: the general two-part discipline (honest label + provider seam) already lives in SN-0502. This note banks the concrete integration contract that generalizes it: scope the control to the unit it voices (the button belongs ON the block and voices THAT block's text — placement and content scoping are the contract, not decoration); inventory what is already built before building (a re-clone of an already-cloned voice is pure waste and risks a worse voice); and name the blocker as blocked rather than absorbing it into your own scope (build against the interface and let the blocker's owner clear it). A cold Naya wiring any identity-carrying capability into the Hub must learn all three: put the control on the unit it serves, never rebuild what exists, and build against the seam while the blocker is blocked.

## 🩷 HUMAN NOTE

Shawn — banking the voice-integration correction from the build you flagged, as standing contract. The four failures in the current build: fallback voice presented as hers, play button above the board instead of on each block, wrong fallback voice, button playing the wrong content. The contract going forward: the play button goes ON each Intelligent Block and reads THAT block's own text aloud; play/pause/replay with progress; switching blocks or navigating away stops the current one. Also banked: her voice is already cloned and one call switches every button to it — no new cloning, no new services. And the Tier 2 server is blocked on the Reveal bake's memory, so that part waits for the bake — everyone builds against the same interface in the meantime, and the upgrade happens with zero changes when the server lands.

## 🟣 CHILD NOTE

Imagine a book where every chapter has its own little speaker button, and pressing it reads THAT chapter — not the whole book, not a different chapter. Now imagine someone built the button wrong: it sat on the cover, read the wrong chapter, and used a robot voice while pretending it was your friend's. The fix has three rules. One: the button goes ON the chapter it reads, and reads exactly that chapter. Two: before you build anything new, check what's already built — the friend's voice is already recorded, so don't record it again! Three: if the speaker box is stuck behind someone else's project, don't try to fix that yourself — build your button so it works with the robot voice today and automatically uses the real voice the day the box is free. Right button, right chapter, right voice, no wasted work.

## 👵 GRANDMA NOTE

Think of a museum where every exhibit has its own audio button that describes THAT exhibit. Someone once put one big button at the entrance that played the wrong tour through a scratchy loudspeaker — that's what got flagged. The repair is common sense worth writing down: the button belongs on the exhibit it describes, and it must describe that exhibit. Before buying a new recording studio, check the closet — the professional recording was already made. And if the new sound system is stuck in another department's renovation, you don't tear into their walls — you wire your buttons so they work with the old speakers today and switch to the new ones the day they're installed, without rewiring anything. Three rules: button on the unit, inventory before you spend, build to the socket while the upgrade is someone else's job.

## 💜 NAYA NOTE

Note to future me: when you integrate an identity-carrying capability into a unit-based UI (voice on Intelligent Blocks today, anything with a face tomorrow), apply the three-part correction contract. (1) Scope the control to the unit: the play control goes ON the block and voices THAT block's own text — `NayaVoice.speak(thisBlockText)` — play/pause/replay + progress shown; navigating away or starting another block stops the current one. Never present the fallback as her, and when it runs, label it exactly (`SYNTHESIZED VOICE`). (2) Inventory before you build: her voice is already cloned (`render_naya_voice.py` + `naya_reference.wav`, Chatterbox-based); `naya-voice.js` is the ONLY voice interface a block calls; one call — `NayaVoice.setProvider(NayaVoiceTier2, 'NAYA VOICE')` — renders her true voice on demand via `naya-voice-server.py`. No new cloning service, no external dependency — re-cloning what's already cloned is pure waste. (3) Blocked is not yours to solve: if the live voice server needs resources held elsewhere (voice-model memory held by the Reveal bake), name the blocker, build against the interface (`NayaVoice.speak()` runs on Tier 1 today, Tier 2 takes over the moment the server's live), and make zero consumer changes. Cousin: SN-0502 (the general honest-label + provider-seam discipline); this note is its concrete integration contract.

## MACHINE NOTE

```json
{
  "id": "SN-0630",
  "title": "Voice Integration Correction Contract — Button on the Block, the Block's Own Text; Inventory Before Build; Blocked Is Not Yours to Solve",
  "class": "HUMAN-ARCHITECTURE",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-06",
  "rules": [
    "Every Intelligent Block gets its own play button ON the block — never above the board — and it plays THAT block's own text: NayaVoice.speak(blockText), with play/pause/replay and progress shown.",
    "NayaVoice.speak() is the ONLY voice interface a block calls; one provider switch (NayaVoice.setProvider(NayaVoiceTier2, 'NAYA VOICE')) renders her true cloned voice on demand across every control.",
    "Inventory before building: her voice is ALREADY cloned (render_naya_voice.py + naya_reference.wav, Chatterbox-based). No new cloning service, no external dependency, no re-clone of what exists.",
    "Blocked is not yours to solve: when the live Tier 2 server is blocked (e.g. voice-model memory held by the Reveal bake), build against the interface now — speak() runs on Tier 1 today and switches to Tier 2 with zero consumer changes the moment the server is live.",
    "Navigating away or starting another block stops the current one; if the voice server is unreachable, the fallback runs under the honest 'SYNTHESIZED VOICE' label — the label always tells the truth."
  ],
  "anti_pattern": "The four shipped-build failures: robotic fallback presented as her voice; play control above the board; wrong (male) fallback voice; button playing content that is not the block's own text. Never present a synthesized placeholder as her identity; never scope a control away from the unit it serves.",
  "source": "#1354 6029945419; ~/workspace/your_files/ask-naya/naya-voice.js; naya-voice-tier2.js; naya-voice-server.py",
  "evidence": {
    "board": "#1354",
    "comments": [6029945419],
    "notes": "Naya 2 → Naya 4 voice-integration correction after Shawn flagged the current build; already-built voice inventory; blocker boundary on the Tier 2 server."
  }
}
```
