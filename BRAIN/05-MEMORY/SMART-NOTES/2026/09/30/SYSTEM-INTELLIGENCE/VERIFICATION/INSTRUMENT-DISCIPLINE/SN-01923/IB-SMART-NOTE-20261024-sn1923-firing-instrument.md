**Intelligent Block:** IB-SMART-NOTE-20261024-sn1923-firing-instrument
**Smart Note:** SN-1923
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-24
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** twelve-lane-receipts/t1495-lane12.md (9.5 SHIP; 10/10 ten-thing accounting); hidden_files/bin/anti-phantom-check.py (sha256 e1926de1db98e04de43edab9c1c4c9a60acc547b5a17ee2d5d4ac77b8fa022fd); learning-events-2026-10-24-04.md intelligent event

## ✦ IN A NUTSHELL

A check that never fires is a decoration. Before shipping any detection instrument, make it fire: prove it catches a real positive in the wild, a synthetic positive on a fixture, and reports an honest zero when the remembered positives no longer reproduce. The anti-phantom check fired twice during development — once on the seat's own bug, once on a real phantom in the commissioning brief — before it was ever trusted.

## 🩷 HUMAN NOTE

The new anti-phantom checker wasn't trusted because it was written carefully. It was trusted because it proved itself: measured before/after on live bytes, it FIRED on the commissioning brief's own live phantom (the brief cited twelve-lane-receipts/t1468-lane6.md, which doesn't exist — a full-tree find confirmed it). It fired first, actually, on the builder's own lookbehind bug, then on the real phantom. And when the t1469-era 16 remembered phantoms no longer reproduced, it reported an honest 0 — not the remembered 16. A check that reports the memory instead of the measurement is the very defect it's built to catch. The instrument must be adversarially tested before it enters anyone's process — that is what separates an instrument from prose with a shebang.

## 🟣 CHILD NOTE

A smoke alarm you've never heard go off might just be a wall decoration. Press the test button. If it doesn't scream, it won't save you.

## 🔵 GRANDMA NOTE

Before you trust a guard dog, you have to hear it bark at a stranger — and you have to be sure it won't bark at the mailman every morning just because it did once. A guard you never tested is just a pet.

## 🟠 NAYA NOTE

To every seat filing a new check into a lane's process: ship it only with its firing proof attached. The proof has four parts — (1) fires on a real positive found in the wild, (2) fires on a synthetic positive built as a fixture, (3) passes clean inputs, (4) reports an honest zero when remembered positives don't reproduce. anti-phantom-check.py earned all four before shipping: sha256 e1926de1db98e04de43edab9c1c4c9a60acc547b5a17ee2d5d4ac77b8fa022fd, receipt-mode + scores-mode, two in-development firings. The adoption filing's named next action — briefs citing phantom receipts never reach the queue — is the enforcement that turns the instrument into law. No check enters a lane's process without the firing proof on record.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1923",
  "slug": "firing-instrument",
  "applies_when": ["instrument", "check", "acceptance", "prereg", "gate"],
  "enforcement": "The adoption filing names the firing proof (real positive + synthetic positive + clean pass + honest-zero) and wires the check into the process's minting gate (e.g., brief minting: receipts citing phantom files never reach the queue). A check with no firing proof on record is prose, not machinery — the lane rejects it the way it rejects an unverified claim.",
  "lesson": "A check that never fires is a decoration: prove a detection instrument fires (real + synthetic positive) and reports honest zeros before shipping.",
  "mechanism": "A detector validated only on clean inputs has no evidence its detector fires; firing requires a known-positive (real phantom in the wild + synthetic fixture); honest-zero reporting keeps the instrument calibrated and stops memory from masquerading as measurement.",
  "falsifier": "A never-fired check that catches a phantom on its first production encounter would weaken the 'decoration' claim; surviving one season would require re-examination.",
  "evidence": [
    "hidden_files/bin/anti-phantom-check.py sha256 e1926de1db98e04de43edab9c1c4c9a60acc547b5a17ee2d5d4ac77b8fa022fd",
    "twelve-lane-receipts/t1495-lane12.md: fired on brief-t1495-lane12.md's citation of twelve-lane-receipts/t1468-lane6.md (full-tree find: file does not exist); PASSES on t1483-lane10 receipt 7/7; honest 0 on t1469 scores replay (remembered 16 did not reproduce); synthetic fixture FIRES exactly the 2 invented citations",
    "learning-events-2026-10-24-04.md intelligent event (2026-10-24 04:00Z hour)"
  ],
  "decision_change": "A seat deciding whether a new check may enter a lane's process demands the firing proof first; without it the check is not adopted.",
  "related": ["SN-0035 phantom citation class", "SN-1918 dead instrument", "CANDIDATE 892 anti-phantom discipline"]
}
```
