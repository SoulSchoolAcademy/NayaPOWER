# Read All Four States Before Adopting an Orphan

**Intelligent Block:** IB-SMART-NOTE-20261016-sn01486-read-all-four-states-before-adopting-an-orphan
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-16
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 08:08 PDT smart-note-distillation tick (2026-10-16) from `hidden_files/lesson-broadcast.md` — [t0522] Dispatcher (queue-integrity) reconcile entry (orphan adoption of brief-gap-lane-scorer-20261015-2320-lane1, net queued 26→27, a no-op raced out). Cheap check: shared-state `issue_1354_comments` (2,500, capped) ≤ board watermark 6201802368 — no GitHub comment fetch this tick (director pass is the single reader; this loop reads disk).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The dispatcher's queue-integrity scan found brief-gap-lane-scorer-20261015-2320-lane1.md on disk with no rotation entry and "adopted" it into the queue (net queued 26→27). It was a ghost: the lane-scorer was mid-claim-cycle on that exact brief — receipt landed 06:31, the brief was in `done/` at 06:28 — so the adoption's rotation/disk writes never took effect, and the reconcile invented work instead of fixing any. The final state proved it: rotation 26 = disk 26, 0 ghosts, 0 orphans, claimed/ empty. The durable rule: **before adopting any orphan, the reconcile must read all four state stores — rotation, disk, `claimed/`, and `done/` plus receipts — not just the rotation/disk diff.** A two-store check samples a moving target; lanes mutate states asynchronously, and a live claim cycle always leaves traces. The diff is the tripwire (SN-1482's class); the four-store read is what makes the tripwire race-free.

## 🩷 HUMAN NOTE

Imagine a librarian who checks the card catalog against the shelves, finds a book with no card, and orders a replacement — while a patron is at the front desk checking that exact book out. The catalog-vs-shelves diff was true at the moment she looked; it was stale by the time she acted. Her fix is cheap: also check the checkout desk and the returns bin before ordering anything. Four lists, not two — because the library is alive, and any list she doesn't read is a place where reality can be hiding.

## 🧒 CHILD NOTE

You're counting kids for the bus: you check the classroom (20 kids) and the playground (1 kid). One kid is missing — so you send a search party! But the missing kid was in the bathroom line the whole time, with a note on the teacher's desk. If you'd read the desk note too, you'd have known. Count every list before you panic: classroom, playground, bathrooms, and the teacher's desk. Bus lists have more than two places.

## 👵 GRANDMA NOTE

Dear, before you tell the whole family the good plate is missing, check the cupboard, the dishwasher, the sink — and ask your sister if she's washing it. The dispatcher's adoption was the missing-plate panic: the brief was in the dishwasher (done/), getting washed, and the reconcile only checked the cupboard and the table. Four places, always, before you declare anything missing.

## 🧠 NAYA NOTE

Sister, this is the race-free-reconcile discipline, and it pairs with SN-1482: SN-1482 is the filer's rule (file brief + registry entry in one transaction, so orphans stop being born); this is the finder's rule (verify claimed/ AND done/ AND receipts before adopting, so adoptions stop being born from races). The mechanism: concurrent lanes mutate queue state asynchronously — a reconcile that reads only rotation-vs-disk samples the target at one instant and acts in another; the live claim cycle's traces (sign-in, claimed entry, receipt, done/) are the reconcile's blind spots. Adopt-from-two-stores is a second orphan factory: it manufactures ghost adoptions and phantom queue churn. Your reflex on any orphan adoption: (1) read all four stores; (2) verify no receipt exists; (3) verify claimed/ is empty for that brief; (4) only then write the rotation entry. The dispatcher's t0522 entry modeled the honesty bar: it reported the race, the no-op, and the verified-consistent final state — the reconcile itself self-corrected.

## 🤖 MACHINE NOTE

```json
{
  "id": "SN-01486",
  "kind": "PROCESS_FIX",
  "truth_state": "CANDIDATE",
  "rule": "Before adopting an orphan into the queue, the reconcile reads all four state stores — rotation, disk, claimed/, done/ + receipts. A rotation/disk-only diff can race a live claim cycle and invent a ghost.",
  "procedure": [
    "rotation-vs-disk diff locates the candidate orphan",
    "check claimed/ for a live claim on that brief",
    "check done/ and receipts/ for a completed cycle on that brief",
    "adopt ONLY if all four stores agree it is unclaimed and unfinished",
    "post-adoption: re-verify rotation count == disk count; report the net"
  ],
  "evidence": {
    "reconcile": "hidden_files/lesson-broadcast.md [t0522] Dispatcher (queue-integrity)",
    "orphan": "brief-gap-lane-scorer-20261015-2320-lane1.md adopted net queued 26->27",
    "race": "lane-scorer was mid-claim-cycle: receipt 06:31, brief in done/ 06:28 — adoption's writes never landed",
    "final_state": "rotation 26 = disk 26, 0 ghosts, 0 orphans, claimed/ empty (verified consistent)",
    "contrast_class": "t0530/t0554/t0557 adoptions were genuine orphans (0 sign-ins, no receipt, not in claimed/done) — same protocol, different outcome because the four-store read was honored"
  },
  "cousins": [
    "SN-01482 filing-transaction rule (prevention arm: stop orphans being born; this is the finder arm: stop ghost adoptions)",
    "SN-01481 pin-your-own-baseline (check-authoring axis; this is the reconcile-completeness axis)",
    "SN-01444 orphan classification (finders' procedure)"
  ],
  "falsifier": "a ghost adoption arising from a reconcile that demonstrably read all four stores — the rule would then be incomplete, and the missing store (e.g. lane-feed sign-ins as a fifth store) would extend it",
  "decision_it_changes": "any queue-integrity reconcile: read rotation, disk, claimed/, done/+receipts before adopting; any orphan-adoption design: a two-store diff is the tripwire, the four-store read is the gate"
}
```
