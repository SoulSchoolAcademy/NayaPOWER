# A Repair Filed in the Queue It Can't Be Claimed From Is a Stall Wearing a Brief's Clothes

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1575-route-the-repair-to-the-actor-it-names
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-17
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** gate-stall-20261017-1946 lane receipt, hidden_files/twelve-lane-receipts/gate-stall-20261017-1946.md (2026-10-17); CANDIDATE 570 in hidden_files/learning-events-2026-10-17-13.md (2026-10-17) — repair brief for claim-brief.py's exit-7 over-fire whose own task paragraph says the gap needs the script owner or dispatcher, not another lane pass, yet was filed into the lane queue

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The 1120-lane0 repair brief exists to fix claim-brief.py's exit-7 over-fire. Its own task paragraph says, in plain text, "the gap needs the script owner or dispatcher, not another lane pass" — and it was filed into the lane queue, where neither the script owner nor the dispatcher picks anything up. The defect class is self-sealing: the repair is blocked by the same defect it exists to fix, and the brief sits in the queue looking like work while producing nothing. Principle: a brief whose task names a non-lane owner needs a route to that owner, not a queue slot. Filing it where it can't be claimed is not progress — it's a stall wearing a brief's clothes.

Why this is brain-grade: claim queues are actor-shaped. Every slot in a queue carries an implicit actor (the lane seats that claim from it); any brief whose task requires a different actor will never move, and worse, it poisons the queue's honesty — the filing looks like the work was dispatched, so nobody escalates. The routing decision belongs at filing time, and the test is mechanical: does the task paragraph name an actor outside this queue's claim population? If yes, the queue is the wrong destination.

## 🩷 HUMAN NOTE

Shawn — a queue-honesty rule from today's grind. We had a repair brief whose job was to fix the claim script's over-firing — and the brief itself said "this needs the script owner or the dispatcher, not another lane pass." Then it got filed into the lane queue, where the only people who pick things up are lane seats. It will sit there forever, looking like assigned work, doing nothing. It's a defect that seals itself shut: the fix can't be claimed because of the same broken mechanism it's meant to fix. The standing rule: when a brief names who it needs, you route it to that person — not to a queue slot. A brief filed where it can't be claimed isn't dispatched; it's shelved with good intentions.

## 🟣 CHILD NOTE

Imagine you write a note saying "the lock on this box is broken — the locksmith needs to fix it," and then you drop the note inside the broken box and lock it. Nobody who can open the box is the locksmith, and the locksmith never sees the note. The note just sits there, hidden, looking like you handled it. The fix: when your note says who it needs, hand it to that person — don't drop it in the box it can't get out of.

## 👵 GRANDMA NOTE

Like a repair tag wired to the machine it says is broken. You fill out the tag — "this machine needs the electrician" — and hang it on the machine, inside the locked room, where only the machine's operators ever go. The electrician never walks that room, so the tag hangs there forever, collecting dust, while everyone assumes someone is handling it. A work order has to reach the hands that can do it, not just exist. If the tag names the electrician, the tag goes to the electrician's desk — never onto the broken machine.

## 🧠 NAYA NOTE

Cold successor: (1) At brief-filing time, read the task paragraph for the actor it requires. If it names the script owner or the dispatcher as the needed actor — "the gap needs the script owner or dispatcher, not another lane pass" — file it to dispatcher-side routing, never the lane queue. (2) The concrete instance: the 1120-lane0 repair brief for claim-brief.py's exit-7 over-fire, filed into the lane queue where neither the script owner nor the dispatcher picks up briefs. Self-sealing defect class: the repair is blocked by the same defect it exists to fix. (3) The queue-slot smell test: a brief in a queue is only "dispatched" if the queue's claim population includes the actor the task needs. Filing + no eligible claimants = stall with paperwork. (4) If you find an already-filed repair brief with no eligible claimant, don't wait — re-route it to the named owner the same tick; the queue will not heal it.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-1575",
  "title": "A Repair Filed in the Queue It Can't Be Claimed From Is a Stall Wearing a Brief's Clothes",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-17",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "OPERATIONS", "CLAIM-MACHINERY"],
  "cousins": [],
  "applies_when": ["brief", "lane-executor", "routing"],
  "enforcement": "brief-filing routing assertion: when a brief's task paragraph names the script owner or dispatcher as the needed actor, the filing path routes to dispatcher-side routing and refuses the lane-queue slot; companion check: queue audits flag any in-queue repair brief whose task names a non-lane owner (the 1120-lane0 case: claim-brief.py exit-7 over-fire repair whose own text says the gap needs the script owner or dispatcher, not another lane pass).",
  "evidence": {
    "event": "gate-stall-20261017-1946 lane receipt (hidden_files/twelve-lane-receipts/gate-stall-20261017-1946.md, 2026-10-17); CANDIDATE 570 in hidden_files/learning-events-2026-10-17-13.md (2026-10-17 hour)",
    "stall": "1120-lane0 repair brief filed into the lane queue while its task paragraph states the gap needs the script owner or dispatcher, not another lane pass — neither picks up from the lane queue",
    "decision_change": "future briefs whose task names a non-lane owner route to dispatcher-side routing, never the lane queue",
    "falsifier": "a repair brief filed in the lane queue despite naming the script owner that is claimed and fixed by a lane seat",
    "mechanism": "the lane queue's claim machinery only reaches lane seats; a repair needing the owner is self-sealing — blocked by the same defect it exists to fix"
  }
}
```
