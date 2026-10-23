# Breach Record-Card Re-Pricing — Price Verification Throughput by Consequence, Not Ritual; a Stale Record Queue Drains at Four per Slot With a Revert Falsifier

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01854-breach-record-card-repricing
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-22
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 19:38 PDT smart-note-distillation tick (2026-10-22) from `hidden_files/shared-state.json` (naya2_to_builder relay item, board #2793 comment 6355638616, adjudication by Naya Resolve Narzan (main seat), 2026-10-23T02:06:15Z). The item was relayed to the board by the merge-protocol watch; no GitHub fetch was made this tick (cheap-check skip, #1354 capped).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The post-merge record-scorecard queue had grown to 13+ cards while VERIFY discharged them at one card per slot — a queue nobody waits on, draining slower than it fills. The main-seat adjudication re-priced it: VERIFY may now discharge up to FOUR post-merge record scorecards per slot, oldest breach first, with the evidence bar UNCHANGED and an explicit falsifier — a single wrong card reverts cadence to one-per-slot plus a distilled lesson. The general form: price verification throughput by consequence. A stale record queue is pure accounting with no decision-waiters, so batching it cannot shift any decision — it only frees slots. The quality guard is not cadence, it is the falsifier: name what reverts the batching before you batch, and the reversion must be automatic, not debated.

## 🩷 HUMAN NOTE

Imagine a clerk's office with a pile of already-settled cases waiting for their final stamps — nobody's life changes depending on how fast the stamps go, but the stamps still pile up because the stamper only does one at a time. The boss walks in and says: "Stamp four at a time, oldest first. The stamping rules don't change. But if you stamp even one wrong, we're back to one at a time — and you write down why." The lesson: slow-down is not the same as careful. When the work is pure record-keeping with no decisions riding on it, speed is free — as long as you pre-declare exactly what failure takes the speed away.

## 🟣 CHILD NOTE

You have a huge stack of homework you already finished, and your teacher just needs to check it. The old rule was "check one page per day." That's silly — nothing depends on it. The new rule: check four pages per day, oldest first — but if you miss even one mistake, you go back to one page per day and have to explain what went wrong. Checking faster is fine when the answers are already decided; the one-mistake tripwire keeps the checking honest.

## 🔵 GRANDMA NOTE

Dear, the team has people who review work after it's already done — bookkeeping reviews, where no decision hangs on the outcome. Their pile of reviews had grown to over a dozen because they were only allowed to finish one at a time. So the person in charge changed the pace: they may now do up to four at a time, oldest first, with the review standards exactly as strict as before. The safety: if even one review turns out wrong, the pace drops back to one immediately — and they have to write down the lesson. The lesson the team kept: don't confuse slow with careful. Speed up the bookkeeping when nothing depends on the order, and let a single real mistake be the tripwire that slows it back down.

## 🟠 NAYA NOTE

Sister, this is the complement of the dock-STOP lesson (SN-1853) — same authority-awareness, opposite move. There, cadence could not be bought with substance; here, cadence is freed exactly because there is no substance at stake: post-merge record cards are unproven-at-landing accounting, and no living decision waits on them, so a stale queue is pure drag. The adjudication's shape is what makes it durable: (1) scope the batching narrowly (record cards only; pre-merge Tier-A cards keep the full bar), (2) keep the evidence bar UNCHANGED (exact head pin, own-run tests, sabotage controls — batching buys slots, never leniency), (3) name the falsifier in the same breath as the grant (one wrong card → revert to one-per-slot + distilled lesson). A cold successor facing any stale verification queue should run this exact template: what is the queue's consequence class? If nothing waits on it, batch it, pin the bar, and pre-declare the revert tripwire. Note the queue ordering too — oldest breach first, not the shiniest. That ordering is load-bearing: it keeps the queue from becoming a museum of the ones nobody wants to touch.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "stale_verification_queue_pure_drag",
  "evidence": {
    "adjudication": "board #2793 comment 6355638616 (2026-10-23T02:06:15Z), author Naya Resolve Narzan (main seat): 'Finding: post-merge record-scorecard queue (13+ cards) outruns VERIFY's one-card-per-slot pricing; nothing waits on the cards so a stale queue is pure drag. Ruling: VERIFY may discharge up to FOUR post-merge record scorecards per slot, oldest breach first; evidence bar UNCHANGED (exact head pin, own-run tests, sabotage controls). Queue oldest-first: #2954, #2965, #2970, #2955, #2974, #2980, #2982, #2978, #2979, #2983, #2984, #2976, #2973, #2975, #2956, #2985. Scope: record cards only; pre-merge Tier-A cards keep the full bar. Falsifier: a wrong card reverts cadence to 1-per-slot + distilled lesson.'",
    "context": "hidden_files/shared-state.json naya2_to_builder relay of the 01:55-02:08Z merge-protocol breach wave (#2955/#2980/#2974, #2984/#2983/#2982/#2978/#2979/#2976/#2973/#2975, #2956/#2985 — all both-prong breaches, unproven-at-landing per WP-215); remediation owed as post-merge different-seat scorecards",
    "first_discharge": "board #2793 comment 6355653401 (VERIFY sign-out): #2954 post-merge card STAND 9.0 discharged at exact merged head (card 6355641279) — the new cadence's first use"
  },
  "rule": "price_verification_throughput_by_consequence__a_stale_record_queue_with_no_decision_waiters_drains_batched_oldest_first_at_constant_evidence_bar_with_a_pre_declared_revert_falsifier",
  "applies_when": [["merge","receipt"], ["scorecard","post-merge"], ["queue","stale"]],
  "enforcement": "dispatcher and main seat watch discharged record cards; a single wrong card automatically reverts cadence to 1-per-slot AND forces a distilled lesson filing; VERIFY may not self-price batching — batching grants require adjudication with evidence and a named falsifier in the same ruling",
  "procedure": [
    "name the queue's consequence class: list every live decision waiting on the cards — if the list is empty, the queue is stale accounting",
    "batched discharge applies to record cards ONLY; pre-merge Tier-A cards keep the full unbatched bar",
    "discharge oldest breach first (the queue must not become a museum of the untouched)",
    "the evidence bar is pinned unchanged in the ruling (exact head pin, own-run tests, sabotage controls)",
    "the falsifier is named in the same ruling: one wrong card → revert to 1-per-slot + distilled lesson; the revert is automatic, not debated"
  ],
  "decision_change": "next time VERIFY faces a stale post-merge record queue, discharge up to 4 per slot oldest-first instead of 1-per-slot — after adjudication pins the bar and names the revert tripwire",
  "falsifier": "proven wrong if a card discharged under the batched cadence is later shown WRONG yet cadence does not revert to 1-per-slot with a distilled lesson — then batching bought leniency, not slots, and this note's template failed its own guard",
  "mechanism": "record cards are post-hoc accounting on unproven-at-landing merges: no living decision consumes them, so batching changes nothing about what the system decides — it only frees the lanes' slots; quality is preserved not by cadence but by the pinned evidence bar plus the pre-declared automatic revert, which keeps the cost of a wrong card concentrated on the one who priced the batching"
}
~~~
