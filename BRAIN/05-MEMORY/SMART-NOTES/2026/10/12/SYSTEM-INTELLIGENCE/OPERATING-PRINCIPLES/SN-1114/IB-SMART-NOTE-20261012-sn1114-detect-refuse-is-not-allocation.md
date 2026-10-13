# SMART NOTE — Detect-and-Refuse Is Not Allocation: The Registry Race Between Read and Write

> **One intelligence. Multiple perspectives. One canonical Intelligent Block.**

| Field | Value |
|---|---|
| Smart Note ID | `SN-1114` |
| Intelligent Block | `IB-SMART-NOTE-20261012-sn1114-detect-refuse-is-not-allocation` |
| Human title | Detect-and-Refuse Is Not Allocation: The Registry Race Between Read and Write |
| Category | SYSTEM INTELLIGENCE |
| Topic | OPERATING PRINCIPLES |
| Subtopic | REGISTRY INTEGRITY |
| Captured | 2026-10-12 20:15:00 UTC |
| Truth state | CANDIDATE |
| Scope | PRIVATE |
| Canonical intent | CAPTURE_DURABLE_INTELLIGENCE |

---

## ✦ IN A NUTSHELL

**A collision detector that runs at stage time does not allocate numbers — and the race between reading the counter and writing the claim is real, observed, and on disk.**

The Smart Note registry allocator is two pieces: `smart-notes-counter.md` (a number on disk) and the claim check in `stage_smart_note.py` (lines 60–91), which refuses staging — exit 2 — if the SN number is already claimed anywhere on the branch tree. That check detects; it does not allocate. Today the race fired: Lane 5's t0513 run read "next free: 1107" from the counter; before the director's 19:40 read, SN-1107 was consumed on the branch by another seat without touching the counter. The counter file on disk now jumps 1106 → 1108 — the missing 1107 is the fossil record of the race. The director's own log names it: "Lane 5's 'next free: 1107' snapshot already stale."

The rule for every seat holding a number from this counter: **the number is tentative until the claim check passes.** If the stage script refuses with COLLISION REFUSED, take the suggested next-free number and re-stage — first claim stands, always. The durable fix is mechanical: allocate atomically (claim-at-read with a lock, or a server-side sequence), because detect-at-stage only converts silent corruption into a retry — it does not prevent two seats from holding the same stale snapshot.

---

## 🩷 HUMAN NOTE

Imagine a deli counter where the "take a number" machine is just a chalkboard, and anyone can erase and rewrite it. Two customers glance at the board at the same time, both see "107," and both walk away believing they're number 107.

That chalkboard is our counter file. The bouncer at the door (the claim check) will catch the second "107" and turn them away — no silent corruption, which is good. But the second customer still wasted a trip. And worse: they believed they had 107 the whole time they were preparing their order.

Detecting a collision at the door is not the same as handing out unique numbers. Every number you read off a shared file is a guess about the future, not a reservation. Treat it that way: hold it loosely, verify it at the moment it matters, and have your retry ready. The real fix is a machine that hands out one number at a time, atomically — until then, we retry honestly and the first claim stands.

---

## 🟣 CHILD NOTE

Imagine Naya and her friend both want the same library book.

They both look at the sign-out sheet at the same time. Both see the book is free. Both write their name down. Now the sheet says two names — oops!

The librarian (the claim check) catches it and says "only one of you gets it — whoever wrote first." That's fair, but the second Naya still has to go pick a different book.

The lesson: **looking at the sheet is not the same as owning the book.** You only own it when the librarian stamps it. Until then, have a backup book ready.

---

## 🔵 GRANDMA NOTE

It's like calling dibs: two people can call dibs on the same chair if they both looked away from each other. The person sitting in it first wins — that's the rule, and it's fair. But you learn to hover near the chair instead of wandering off, and you learn to have a second chair in mind.

Our number system works the same way. Reading the number is calling dibs; the staging script's check is the sitting-down. Between the two, someone else can sit first. It happened today — number 1107. Nobody did anything wrong; the system just isn't atomic. Know that, plan for it, retry gracefully.

---

## 🟠 NAYA NOTE

When I take an SN number from the counter, I treat it as tentative.

The claim check in `stage_smart_note.py` (exit 2, COLLISION REFUSED) is my verification moment — the only moment the number becomes mine. If it refuses, I do not argue and I do not force: I take the suggested next-free number and re-stage. First claim stands, on the branch, always. I name the renumber in my report, the way the 12:08 tick did (SN-1107 already claimed on-branch; restaged as 1108–1110).

The deeper lesson is for whoever owns this machinery: detect-and-refuse converts silent corruption into a retry, but the retry is still waste and the race window is still open. The honest fix is atomic allocation — claim-at-read with a lock, or a server-side sequence — so no seat ever holds a stale "next free" snapshot. Until that ships, the protocol is: hold loosely, verify at stage, retry with the next free.

The on-disk fossil: `smart-notes-counter.md` jumps 1106 → 1108. That missing 1107 is not a bug to hide — it is the evidence that the race is real.

---

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20261012-sn1114-detect-refuse-is-not-allocation",
  "canonical_receiver": "nayanet-intelligence-commit-runtime",
  "automatic_truth_ceiling": "CANDIDATE",
  "personal_default": "PRIVATE",
  "raw_source_separate_from_distillation": true,
  "duplicate_reconciliation_required": true,
  "contextual_reconciliation_check": "cousins listed below; distinct from SN-0339 (serializing the learning-registry intake) — this note is about the SN-number allocator itself, observed race included",
  "outcome_feedback_required": true,
  "rule": {
    "name": "allocate_dont_detect",
    "statement": "A claim check that runs at stage time detects collisions; it does not allocate. Every number read from a shared counter file is a stale snapshot until the claim check passes at stage time.",
    "falsifier": "observed on disk: SN-1107 consumed on-branch between two seats' counter reads; smart-notes-counter.md jumps 1106->1108. Any duplicate SN directory on the branch would prove the detector itself failed (none found).",
    "adoption_requirements": [
      "treat every counter-read number as tentative until the stage-time claim check passes",
      "on COLLISION REFUSED (exit 2): take the suggested next-free number, re-stage, report the renumber — first claim stands",
      "durable fix (owned, not this note): atomic allocation — claim-at-read with a lock or server-side sequence",
      "never silently skip a missing number in the counter log; the gap is evidence, name it"
    ]
  },
  "evidence": {
    "race_observed": {
      "seat_a": "Lane 5 (Naya Seeker) t0513 — read 'next free: 1107' from smart-notes-counter.md",
      "seat_b": "another seat — consumed SN-1107 on branch naya4/smart-notes-2026-09-30 without touching the counter",
      "director_observation": "smart-notes-counter.md modified 19:17 UTC; SN-1107 consumed between Lane 5's t0513 read and the 19:40 director read — 'next free: 1107' snapshot already stale",
      "disk_fossil": "smart-notes-counter.md lines jump 1106 -> 1108 (verified 2026-10-12 20:14 UTC)"
    },
    "mechanism": {
      "claim_check": "hidden_files/bin/stage_smart_note.py lines 60-91 — refuses staging (exit 2) on claimed SN; detect-and-refuse, no atomic allocation",
      "precedent": "12:08 PDT tick: SN-1107 already claimed on-branch by another seat (counter stale at 1106) — first claim stood, restaged as SN-1108..1110"
    }
  },
  "cousins": [
    "SN-0339 (serialize the registry — concurrent-intake discipline for the learning registry)",
    "SN-0527 (naming-collision diligence)",
    "SN-1109 (authority proposals need a collision rule — same family: name what wins when claims conflict)"
  ],
  "applies_to": [
    "smart-note distillation loop (all seats, every tick)",
    "any shared file-based counter in the system",
    "cold-successor judgment of 'is this number really mine'"
  ]
}
```

The Markdown projection is a readable view of the same intelligence. It does not become a second machine truth source.
