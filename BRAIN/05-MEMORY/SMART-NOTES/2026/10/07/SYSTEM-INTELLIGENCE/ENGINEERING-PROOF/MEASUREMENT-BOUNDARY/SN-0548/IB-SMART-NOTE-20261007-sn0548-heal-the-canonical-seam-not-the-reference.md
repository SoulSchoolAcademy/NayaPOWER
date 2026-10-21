# Heal the Canonical Seam, Not the Reference — a Reference-Engine Fix Never Establishes the Production Path

**Intelligent Block:** IB-SMART-NOTE-20261007-sn0548-heal-the-canonical-seam-not-the-reference
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-07 ~09:15 PDT
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6041724313 ([NAYA] P0 learning activation seam — deconflicted, no duplicate build, 2026-10-07 16:01 UTC); handoff on #1724 comment 6041722141; tip `75f6e225481bc0e8753cadd644e2b5b6f67d4173`.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The P0 learning-activation investigation found the exact seam: the canonical runtime ACT binding is `supabase/functions/nayanet-act-runtime`, and it **hardcodes one Intelligent Block and reads it directly after LAW — it does not consume the normal persisted KNOW/CONNECT selection**. The reference `KernelBehaviorEngine` shares the same conceptual hole (ACT before KNOW; no KNOW/CONNECT → ACT feedback). The tempting move is to fix the reference engine and claim the seam closed. The seat refused: **fixing only the reference engine would not establish the canonical production seam.** The reference is a measurement instrument, not the machine — a fix in the instrument proves nothing about the machine's behavior.

**The rule:** when a reference/test-double and the canonical runtime share a conceptual hole, the repair must land on the canonical authority path — the binding that actually runs in production. A reference-engine fix is admissible only as an experiment, never as seam closure. Current-main selector authority on this tip is KNOW `selectKnowContext()` + CONNECT `selectableConnections()`; `note_bridge_live.py` is tooling, and open #1665 is not merged current-main authority — so the repair surface is the ACT binding under LAW/KNOW/CONNECT authority, not the reference engine. This is SN-0523's repair-side twin: SN-0523 says *proof scope is part of the proof* (name the measured engine); this says *the fix belongs on the named engine's canonical counterpart, not on the engine you measured*.

## 🩷 HUMAN NOTE

If the test version of a machine has the same flaw as the real machine, fixing the test version doesn't fix the real one. You have to open the real machine and repair the actual part — the exact component that runs in production.

## 👶 CHILD NOTE

If your toy car and the real car both have a wobbly wheel, fixing the toy car's wheel doesn't fix the real car. You have to fix the real car.

## 👵 GRANDMA NOTE

You can't mend the Sunday dress by sewing the practice cloth, dear. Same hole, yes — but the dress is the dress. Work on the garment that gets worn.

## 🧠 NAYA NOTE

For a cold successor arriving at any learning-activation seam: first map the canonical authority on current main (selector functions, runtime bindings, merged vs open PRs), then ask "does my fix land where production runs, or only where the reference runs?" If the answer is the reference, you have an experiment, not a repair — say so in the receipt. The proving instance here is concrete: `nayanet-act-runtime` hardcodes one IB after LAW, bypassing KNOW `selectKnowContext()` and CONNECT `selectableConnections()`; the minimal design (ACT.PLAN → optional LAW re-resolution → ACT.EXECUTE) was handed to the claiming lane (#1724 comment 6041722141) precisely so the fix could land on the canonical seam. The anti-pattern to never repeat: closing a seam by green-ing the reference engine and letting the receipt imply production behavior changed.

## 🤖 MACHINE NOTE

```json
{
  "sn": "SN-0548",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-07",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/MEASUREMENT-BOUNDARY",
  "doctrine": "When a reference engine and the canonical runtime share a conceptual hole, the repair must land on the canonical authority path — the binding that actually runs in production. A reference-engine fix is an experiment, never seam closure.",
  "evidence": [
    "#1354 comment 6041724313 (P0 learning activation seam, tip 75f6e225481bc0e8753cadd644e2b5b6f67d4173, 2026-10-07)",
    "Canonical ACT binding supabase/functions/nayanet-act-runtime hardcodes one Intelligent Block, reads directly after LAW, does not consume persisted KNOW/CONNECT selection",
    "Reference KernelBehaviorEngine shares the conceptual hole (ACT before KNOW; no KNOW/CONNECT->ACT feedback); fixing only it would not establish the canonical production seam",
    "Current-main selector authority: KNOW selectKnowContext() + CONNECT selectableConnections(); note_bridge_live.py is tooling; open #1665 not merged = not authority",
    "Handoff design preserved on #1724 comment 6041722141 (ACT.PLAN -> optional LAW re-resolution -> ACT.EXECUTE)"
  ],
  "falsifiers": [
    "Closing a seam by green-ing the reference engine while the canonical binding is untouched",
    "Letting a receipt imply production behavior changed from a reference-only fix",
    "Routing a repair through note_bridge_live.py (tooling) or an unmerged PR (#1665) as if it were current-main authority"
  ],
  "applies_to": "learning-activation repairs; reference-engine vs production-runtime seams; proof receipts",
  "sibling": "SN-0523 (proof scope is part of the proof — name the measured engine); SN-0388 (deployed URL is not the deployed product); SN-0350 (deploy stamp is not behavioral evidence)"
}
```
