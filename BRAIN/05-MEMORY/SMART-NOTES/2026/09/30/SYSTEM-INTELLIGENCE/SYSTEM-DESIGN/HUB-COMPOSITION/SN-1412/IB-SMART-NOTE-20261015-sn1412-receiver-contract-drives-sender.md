# The Receiver Contract Drives the Sender — Hub Render Schema Is the Engine's Emission Format

**Intelligent Block:** IB-SMART-NOTE-20261015-sn1412-receiver-contract-drives-sender
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-15
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #2641 comment 6197856402 (Clarity — the hub receiver contract, read from Shawn's 12 hub pages, 2026-10-15). Intelligence report nayapower-intelligence-report-2026-10-15.md confirms the wiring gap.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Read from Shawn's own 12 hub pages: the hub already renders a fixed Smart Note block contract — `{id, title, subtitle, topics[], topic, tone, icon, kind, layers[]}`, each layer `{name, key, color, tier, body}`, PRIMARY tier (IN A NUTSHELL / HUMAN / CHILD / GRANDMA / NAYA) and DEEPER tier (MACHINE, WHAT IT MEANS, HOW IT CONNECTS, WHATS IN IT FOR YOU, HOW TO APPLY, LEARNING LESSON, THE BIG IDEA, HOW IT WORKS, WHAT IT UNLOCKS), 12 rooms with `{id, name, kicker, accent, icon}`, dark theme `--bg #0B0D12`. **The engine's sender (converged-plan element 11, schema-first records) must emit exactly this shape — the receiver contract drives the sender's emission format.** Any record that cannot fill this schema cannot reach the human. The gap is measured, not guessed: the engine emits the 5 primary views but not the deeper tier; the hub renders deeper-tier layers the engine never sends. The rule: wire element 11 to emit exactly this — no competing schema design, no hub-side guessing of placement (every record carries its room id).

Rule for a cold successor: when building the engine↔hub pipe, start from the receiver's code, not the sender's wishes — the human-facing surface is the fixed law.

## 🩷 HUMAN NOTE

Shawn — one from the hub wiring work today that locks in an order-of-operations rule. I read the receiver contract out of the hub's own pages (all 12): there's a fixed, exact shape the hub already renders — a block schema with its layers, tiers, room ids, and the dark theme as law. The gap is concrete: the engine currently emits the five top views but never sends the deeper layers the hub renders — so the receiver would show an empty frame. The rule that follows: the receiver contract drives the sender's emission format. Element 11 (the schema-first records) gets wired to emit exactly what the hub already speaks — no inventing a second schema, no asking the hub to guess where things go. Every record carries its room id; the hub never guesses placement. Build the pipe from the human's side backward.

## 🟣 CHILD NOTE

Imagine a vending machine with exact-size slots, and someone building snacks for it. The smart move: measure the slots first, then shape the snacks to fit — not the other way around. The hub (the machine the human sees) already has its slots fixed: specific layers, tiers, rooms, colors. The engine (the snack maker) must shape its records to fit those slots exactly. Anything that doesn't fit can't reach the person. So: measure the slots, then build.

## 👵 GRANDMA NOTE

The team read the human-facing hub's code and wrote down exactly what shape of information it can display — its layers, rooms, and look. The finding: the engine that produces the intelligence sends only part of what the hub can show, so some sections would come up empty. The rule going forward: the thing the human sees sets the shape; the thing producing the content must match it exactly. Don't redesign the display to fit the producer — fit the producer to the display.

## 🟠 NAYA NOTE

Element-11 emission decisions from this rule: (1) Treat the hub's render contract as the fixed schema — PRIMARY tier (IN A NUTSHELL, HUMAN, CHILD, GRANDMA, NAYA) + DEEPER tier (MACHINE, WHAT IT MEANS, HOW IT CONNECTS, WHATS IN IT FOR YOU, HOW TO APPLY, LEARNING LESSON, THE BIG IDEA, HOW IT WORKS, WHAT IT UNLOCKS) + room id on every record + theme `--bg #0B0D12`. (2) Emit ALL layers, not just the primary five — partial emission is theater. (3) Never design a parallel schema; a competing sender format is a bug. (4) Staleness rides the spine: every block carries `verified_at`; stale never displays as fresh. If the hub's contract ever changes, the sender's emission changes with it — the contract is derived from receiver code, not invented, so re-read the receiver on every hub release.

## ⚙️ MACHINE NOTE

{
  "schema": "smart-note-v1",
  "sn": "SN-1412",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-15",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/HUB-COMPOSITION",
  "doctrine": "receiver-contract-drives-sender",
  "rule": "The receiver contract drives the sender's emission format. Element 11 (schema-first records) emits exactly the hub's rendered block schema; every record carries its room id; the hub never guesses placement. Any record that cannot fill the schema cannot reach the human.",
  "decision_change": "Element-11 and emit-pipe design decisions: no competing sender schema; full-layer emission (all PRIMARY + DEEPER tiers); room routing mandatory; verified_at on the spine.",
  "falsifiability": "The contract is derived from receiver code, so a hub re-release that changes the render schema supersedes this snapshot — re-read the receiver on every hub release; a hub that accepts server-driven schemas would invert the direction.",
  "mechanism": "The receiver is the human-facing fixed law (dark theme, 12 rooms, exact layer set); the hub renders whatever layers it receives, so an unfilled deeper tier renders as an empty frame, not a graceful omission. Wiring flows receiver->sender because the human surface is the constraint that cannot move — the sender is the variable side of the pipe.",
  "gap_measured": "engine emits the 5 primary views; the hub renders 9+ deeper-tier layers the engine never sends; zero fetch()/backend calls in all 13 hub files (seeded content + localStorage); repo search finds zero Python/JS talking to the hub",
  "related": ["SN-1409", "SN-1410"],
  "provenance": ["#2641 comment 6197856402", "nayapower-intelligence-report-2026-10-15.md"]
}
