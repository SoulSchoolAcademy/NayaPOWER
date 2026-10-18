# When the Event-Snapshot Remedy Stales the Pin — Adjudicate, Don't Push

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01633-when-the-event-snapshot-remedy-stales-the-pin
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A re-run red can be a stale-payload artifact even when the body fix is correct — and the standard event-snapshot remedy (push an empty commit to fire `synchronize`, per SN-1072) can be circular when the receipt pins the exact head SHA. On #2757, the 13:28Z `Receipt pin — exact head SHA` FAILURE was a stale-payload re-run artifact: workflow run 39130819925 attempt 2 replayed the original `synchronize` event from 13:16:25Z, so the check evaluated the pre-pin body (MISSING → exit 1) even though the pin was cut at 13:17Z. Independent recomputation on live bytes passed both rungs (`check_scorecard_receipt_pin.py` → PASS; `auto_merge_gate.py --p12-only` → allowed, zero reasons). The temptation is to push a tree-identical empty commit — but that moves the head and stales the very pin the receipt certifies, regressing the receipt to fix the check. The fix is never a push: the gate owner re-wires the check to read the PR body live via the API at evaluation time, or the dock adjudicates the stale red with the evidence. Two disciplines (event-snapshot semantics, exact-head pins) collided; the way out is adjudication, not motion.

## 🩷 HUMAN NOTE

A security guard checks badges at the door using a photo taken at the start of the shift. An employee's badge gets corrected mid-shift, but the guard's photo is the old one — so the guard keeps turning the employee away, and "try the door again" changes nothing because the photo never updates. The obvious fix — walk through a different door so a new photo gets taken — breaks the attendance log, which records the exact door the employee used. The real fix isn't a different door; it's updating the guard's procedure to check the live badge roster, or having the supervisor override the stale photo with the evidence in hand. That's exactly the #2757 case: the CI check read a frozen photo of the PR body, the receipt pinned the exact door (head SHA), and walking through a new door would have voided the receipt. Don't break the log to satisfy the guard — fix the guard, or get the supervisor's word.

## 🟣 CHILD NOTE

If the test reads yesterday's answer sheet, re-taking the test won't help — it keeps seeing yesterday's answers. And you can't submit a new answer sheet, because your receipt says exactly which sheet you turned in. So don't submit a new sheet. Ask the teacher to read the real sheet, or have the principal say it's fine.

## 🔵 GRANDMA NOTE

When the inspector's clipboard has an old copy of the form and your receipt proves exactly which form you filed, you don't file a new form to make the clipboard right — that would break the receipt. You ask the office to read the real form, or the manager to sign off. Fixing a paper problem by making a new paper problem is just two problems.

## 🟠 NAYA NOTE

Event-snapshot collision case (2026-10-18 ~06:38 PDT, self-build-loop cycle, #2757): the `Receipt pin — exact head SHA` check failed at 13:28Z on re-run attempt 2 — but run 39130819925's event was frozen at 13:16:25Z (the `synchronize` that predated the 13:17Z pin edit), so the rung evaluated the pre-pin body. SN-1072's remedy (tree-identical empty commit → new `synchronize` event) is textbook-correct for body-only gate reds — and circular here, because the receipt's `SCORECARD-RECEIPT-PIN` certifies `merge_head_sha 23127acd…` byte-exact; any new commit moves the head and voids the pin. The loop deliberately did not push. Fix options named in the cycle file: (a) gate owner re-wires the check to fetch the PR body live via the API at evaluation time (Lane 9 / Code Health owns `receipt-gate.yml`), or (b) the dock adjudicates the stale red with this evidence. Cousins: SN-1072 (event-snapshot law — the remedy that breaks); SN-0200 (receipt pins must resolve live — the pin discipline that makes the remedy circular). The new content is the collision rule itself: when the snapshot remedy would move a pinned head, the remedy is void and the check is adjudicated or re-wired.

## 🟢 MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-01633",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-18",
  "applies_when": [
    ["gate", "receipt-pin-body-check"],
    ["event", "stale-payload-rerun"],
    ["pin", "exact-head-sha"],
    ["collision", "pin-vs-event-snapshot"]
  ],
  "enforcement": "When a receipt-pin body check fails on a RE-RUN of an event that predates the body fix (run created_at < pin/decided_at timestamp): (1) no re-run and no push until the collision is named — the failing run's event timestamp is read first, and a re-run of an event frozen before the body edit is classified STALE-PAYLOAD, not a PR defect; (2) the check's gate owner adjudicates: either re-wire the workflow to read the PR body live via the API at evaluation time (the mechanical fix — owner: whoever owns the gate file, here Lane 9 / Code Health for receipt-gate.yml), or the dock adjudicates the stale red on the PR with the recomputation evidence. A tree-identical empty commit is PROHIBITED when the receipt pins an exact head SHA — it stales the pin (regression), and the prohibition is checked by comparing the proposed remedy's head against the pinned head before acting.",
  "decision_change": "The question 'a body-gate check reds on re-run — re-run, fix the body, or push?' gains a collision check first: 'does the receipt pin an exact head, and is this run's event frozen before the body edit?' If both hold, re-running and pushing are both void moves — re-running replays the stale payload, pushing stales the pin. The decision becomes adjudication (gate owner re-wires to read live, or dock signs off the stale red with evidence). SN-1072's empty-commit remedy applies ONLY when no exact-head pin is at stake.",
  "falsifiability": "If the receipt's pin is re-cuttable (the receipt is amended and the new pin is published), the empty-commit remedy becomes legitimate again and this note's prohibition lifts — the collision is conditional, not absolute. If the gate is re-wired to read the body live, the entire stale-payload class vanishes for that gate and the note retires to documentation. A case where pushing fixed a pinned-head red without voiding the pin (pin survived the push, byte-verified) falsifies the circularity claim.",
  "mechanism": "GitHub Actions re-runs replay the triggering event's payload, not current state (SN-1072); a body-only edit after the event is invisible to the re-run. Receipt-pin checks anchor an exact head SHA (the SCORECARD-RECEIPT-PIN contract); any new commit — even tree-identical — produces a new SHA and moves the head the pin certifies. The two mechanics are individually correct and jointly circular: satisfying the check's freshness requirement (a new event) violates the receipt's immutability requirement (the same head). Circularity is resolved by authority (adjudication) or by redesign (the check reads live state), never by a third commit."
}
~~~

## 🧾 PROOF / PROVENANCE

~~~json
{
  "event": "2026-10-18 ~06:38 PDT, self-build-loop full cycle (Naya Clarity Narzan), #2757 builder-legs verification",
  "finding": "13:28Z 'Receipt pin — exact head SHA' FAILURE = stale-payload re-run artifact (run 39130819925, run_attempt 2, event frozen 2026-10-18T13:16:25Z pre-pin); independent recomputation on live bytes: rung 1 check_scorecard_receipt_pin.py @ main → PASS, rung 2 auto_merge_gate.py --p12-only → allowed:true",
  "deliberate_non_action": "no push — a new commit would stale the pinned head 23127acd2c7efe0c65105963d2ddfb8e4f757fb2",
  "routing": "fix = gate owner re-wires check to read body live (Lane 9 / Code Health, receipt-gate.yml) or dock adjudicates",
  "sources": ["goals/nayapower-self-build-loop/hidden_files/selfbuild-cycle-20261018-0638-full-2757-verify.md", "memory/2026-10-18.md (06:38 PDT intelligent-graph drive loop)", "#2721 Verity Kappa named-cure 6249944944"],
  "cousins": ["SN-1072 (event-snapshot law — the remedy that breaks)", "SN-0200 (receipt pins must resolve live — the pin discipline that makes the remedy circular)"]
}
~~~
