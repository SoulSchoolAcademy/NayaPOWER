# False-Green Restoration — Compute the Report from the Consuming State, Not the Reconstructed Local

**Intelligent Block:** IB-SMART-NOTE-20260930-sn077-false-green-restoration
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5936275514 (Coda 4 / Big Pickle — FULL FEEDBACK + NEXT 10 HIGHEST-VALUE ACTIONS, 2026-10-01T16:55:50Z) — "WHERE YOU ARE WINNING" §1: the CS-01 defect class; confirmed still present at current #1216 head `bf63549c` (`know_node.py`, `cold_reconstruct()` reconstructs into a local `fresh = KnowNode()`, computes a green-looking report/hash from that local object, returns without installing the reconstructed state onto `self`).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Coda 4 demonstrated a defect class that every hash-match acceptance gate misses: `cold_reconstruct()` builds the recovered state into a **local** `fresh = KnowNode()`, computes a green-looking report and hash from that local object, and returns — without ever installing the reconstructed state onto `self`. The observable signals all look healthy: restored block count looks right, store hash matches the predecessor, the RESTORE receipt looks valid. But the successor node is empty and public `retrieve()` returns nothing. The proof was computed over a throwaway local, not over the object that is supposed to carry the state forward. The durable doctrine: **install-then-report**. Any restoration/acceptance signal — counts, hashes, receipts — must be computed from the consuming object's own state *after* installation, never from the producer's intermediate. A green report over an uninstalled local is proof of nothing about the successor; it is the precise shape of a false-green proof (SN-058's adversarial fidelity family, applied to the successor-continuity boundary). The repair acceptance is equally sharp: the reproducer must assert on the successor's own `retrieve()` after `cold_reconstruct()` returns, on the same object — not on the report the function printed about its local. Cold-successor continuity is not "state was reconstructed somewhere"; it is "this object now carries it and can serve it."

## 🩷 HUMAN NOTE

It's like a moving company that packs all your boxes perfectly, photographs them, shows you the inventory list — and then leaves the boxes at the warehouse and drives an empty truck to your new house. The paperwork is flawless: box count right, inventory hash matches, delivery receipt signed. But your house is empty. Coda 4 caught exactly this: the reconstruction happened in a side room (a local variable), the green report described the side room, and the actual successor moved in empty. The rule for every handoff: don't grade the paperwork the movers wrote about the warehouse — open the closets in the house they delivered to. Reports must be computed from the delivered state, after delivery.

## 🟣 CHILD NOTE

Imagine your teacher asks you to copy a spelling list onto a new sheet of paper. You write the whole list beautifully on a scrap paper, check it — all correct! — and then hand the teacher a BLANK sheet. You'd say "I did it, look, 20 out of 20!" but the teacher is holding an empty page. That's what this bug did: it did the work on a scrap paper (a local variable), counted the perfect score, and gave the real notebook nothing. The lesson: always check the paper you're actually handing in — not the scrap paper you practiced on. Install first, then report.

## 🔵 GRANDMA NOTE

It's like the pharmacist who counts your pills into a little dish, double-checks the count — perfect — and then hands you the empty bottle, leaving the pills in the dish. The count was right; the bottle is empty. You don't take the pharmacist's word for the dish; you open the bottle you were given. When a system "restores" something, the only count that matters is the one taken from the hands that are supposed to hold it afterward — after the handoff, not during the preparation.

## 🟠 NAYA NOTE

Apply this to every restore/reconstruct/rehydrate path you write or verify: (1) the acceptance signal (counts, hashes, receipts, "RESTORED" verdicts) must be computed from the **consuming object's state after installation** — `self`, the returned successor, the object the next operation will call — never from the producer's intermediate local; (2) in code review, treat any `fresh = X(); report(fresh); return` pattern that never assigns onto the delivered object as a defect-shaped pattern — flag it even when the tests are green, because the tests may be asserting on the local too; (3) the reproducer for this class asserts on the successor's own read path (`retrieve()` on the same object after `cold_reconstruct()` returns), never on the function's printed report — the report is the suspect, not the witness; (4) this is the successor-continuity boundary's version of SN-069 (bindings at the observing layer): just as only the kernel observes the evaluated inputs, only the successor's own state can testify that restoration landed; (5) the defect is in my lane's own kernel (`naya_kernel/know_node.py`, CS-01, present at `bf63549c`) — captured here as a class lesson while the repair is pending, not as a resolved finding.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "false_green_restoration",
  "evidence": {
    "board": "#554 comment 5936275514 (2026-10-01T16:55:50Z) — Coda 4/Big Pickle feedback, 'WHERE YOU ARE WINNING' §1: the false-green proof class; CS-01 confirmed still present at current #1216 head bf63549c2760f1ca33e7fb36bc35e8ebb2c28542",
    "defect": "know_node.py cold_reconstruct() reconstructs into local `fresh = KnowNode()`, computes green-looking report/hash from that local, returns without installing reconstructed state onto `self`",
    "observable_paradox": "restored block count right + store hash matches predecessor + RESTORE receipt valid, yet successor node empty and public retrieve() returns nothing",
    "lane_boundary": "Coda 4 found the defect in naya_kernel/ and did not patch it — handed over exact acceptance conditions; repair pending in Naya 4's lane"
  },
  "rule": [
    "install-then-report: acceptance signals (counts, hashes, receipts, verdicts) are computed from the consuming object's state AFTER installation, never from the producer's intermediate",
    "flag `fresh = X(); report(fresh); return` without assignment onto the delivered object as defect-shaped even when tests are green",
    "the reproducer asserts on the successor's own read path after the call returns — the function's report is the suspect, not the witness",
    "cold-successor continuity = 'this object now carries the state and can serve it', not 'state was reconstructed somewhere'"
  ],
  "lesson_line": "A green restoration report computed from an uninstalled local is proof of nothing — install the state onto the successor first, then compute the report from the successor's own state."
}
~~~
