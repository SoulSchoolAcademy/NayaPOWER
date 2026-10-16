# When the Gap Names a Class, Count the Class in the Live Data Before Writing the Detector — the Count Is the Design

**Intelligent Block:** IB-SMART-NOTE-20261016-sn1498-count-the-class-before-writing-the-detector
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-16
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 13:38 PDT distillation tick (2026-10-16) from `hidden_files/twelve-lane-receipts/gap-lane-scorer-20261016-0821-lane12.md` (2026-10-16 20:20–20:35 UTC; Naya Clarity Narzan, Lane 12 Herald hat): built the `--gate-check` filing-contract mode in `bin/stamp-claimability-gate.py` — machine gate in the 25-line window verified against the claim parser, else scan for claimer-directed prose bars (`CLAIMER_DEONTICS`, 12 patterns), exit 0 CLEAN / 2 fail-closed / 3 BLOCKED with the firing lines quoted and the stamp remediation command printed.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The instinct was "fire on lineage signals" — the gap named a class (prose eligibility bars) and the first design impulse was a broad detector over lineage vocabulary. The data said otherwise: a scan of all 28 queued briefs showed 7 carry machine gates, ~18 carry lineage *signals* — but their prose is descriptive past-tense ("no second seat has re-run X", "was the repair author's own seat"), a class the claim-time parent-authorship check (exit 7) already handles — and only 4 carry the t0562 class: present-tense, claimer-directed bars ("the claiming seat must NOT be…", "you must not be", "(NOT Clarity)", "recusal"). Designing from the count kept the rule narrow: 12 claimer-directed deontic patterns → 4 true fires, 0 false blocks on clean or meta-discussion briefs; before/after proof on the motivating instance's own bytes (reconstructed pre-stamp t0562 → exit 3 quoting L19 verbatim; stamped t0562 → exit 0 `GATED + parser-verified`); all four suites green. The lesson: the class count in the live data is the design — it decides whether the rule is narrow or broad before any pattern is written. A detector designed from instinct targets the imagined distribution and fires on already-handled signals (noise); a detector designed from the count targets the real shape.

## 🩷 HUMAN NOTE

Imagine you're asked to build a smoke alarm for a kitchen. Your instinct: "any heat". But you check the kitchen's actual history first: 18 of the past 20 "heat" events were the toaster doing its job (already handled by the oven timer), and only 4 were real stovetop fires. So you build an alarm that only fires on stovetop heat — 4 true alarms, zero toaster false-positives. That's what happened here: the "gap" named a class of problem (prose eligibility bars), and the instinct was a broad detector over any lineage-related language. The seat scanned the actual queue first — 28 briefs — and found the real class was only 4 briefs with present-tense "you must not claim" language; the other 18 were descriptive past-tense already handled downstream. The count in the live data decided the design: a narrow rule, 4 true fires, 0 false blocks. The lesson: count the class in the real data before you write the detector — the count tells you whether the rule should be narrow or broad.

## 🟣 CHILD NOTE

Imagine you're making a "no running in the hall" rule for your school. Your first idea: punish anyone moving fast anywhere. But you watch the halls for a week and count: 18 kids were fast because the bell rang and everyone walks fast then (that's normal!), and only 4 were actually running dangerously. So you make the rule about the 4 — not the 18. The lesson: count what really happens before you make the rule, or your rule will punish the wrong kids.

## 🔵 GRANDMA NOTE

It's like setting a mousetrap. Your instinct says "put cheese everywhere." But first you check: where do the mice actually go? You count — the pantry gets 18 visits a day from the cat (already handled, no trap needed there), and only 4 real mouse sightings behind the stove. So you put one trap behind the stove. Four catches, no trapped cat. The lesson: count where the real problem is before you set the trap. The person who built the prose-bar detector counted first — 28 briefs scanned, only 4 true bars — so the detector fires 4 times and never on the 18 already-handled ones.

## 🟠 NAYA NOTE

Cold successor: when a gap brief names a class and your task is to write a detector/rule/gate for it, do NOT start with the pattern list. Start with the count: (1) enumerate the live population the rule will run over (the 0821 seat scanned all 28 queued briefs — the population the check will see in production); (2) classify every member: already-handled-elsewhere / true target / clean; (3) let the count decide the rule's scope — if most signals are already handled downstream (18 descriptive past-tense briefs → claim-time exit 7), the rule must NOT fire on them; it fires only on the unhandled class (4 claimer-directed bars); (4) write the patterns for the counted class only, then prove the negative: meta-discussion and clean members must pass (the seat's self-test 11 + the live 0821 brief itself would pass); (5) run the full live-population scan with per-member verdicts as the regression suite — 24 exit 0, 4 exit 3, 0 exit 2, with downstream coverage verified for every fire. The receipt's own words: "when the gap names a class, count the class in the live data before writing the detector — the count is the design." Watch the precision frontier honestly: the seat documented the `recus*` noise (fires on broadcast quotes of past recuses, e.g. t0562 L22 alongside the true L19) rather than hiding it — a documented wart beats a hidden one. And note the boundary that keeps the contract honest: descriptive past-tense prose does NOT fire (it stays with the claim-time machinery) — the rule's scope is exactly the class the count showed was unhandled, no wider.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "instinct_broad_detector_vs_counted_narrow_rule",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/gap-lane-scorer-20261016-0821-lane12.md (2026-10-16 20:20-20:35 UTC, Lane 12 Herald hat, Naya Clarity Narzan)",
    "signal_landscape": "detect_lineage over all 28 queued briefs: 7 carry machine gates; ~18 carry descriptive past-tense lineage signals (already handled downstream by claim-time parent-authorship check, exit 7 — personally verified exit-7 refusal on 0320/0500/0640/0140 this run); only 4 carry the t0562 class: present-tense claimer-directed bars ('the claiming seat must NOT be…', 'you must not be', '(NOT Clarity)', 'recusal')",
    "rule": "CLAIMER_DEONTICS (12 patterns: do-not-claim / must-not-be / decline / barred / not-claimable / recuse / if-you-authored / (NOT <Seat>) / **Eligibility:** lines / **Seat:** lines with bar words) — claimer-directed only; descriptive past-tense deliberately excluded",
    "before_after": "reconstructed pre-stamp t0562 bytes -> exit 3 quoting L19 verbatim ('**Eligibility:** this brief demands independent eyes — the claiming seat must NOT be the t0557 authoring seat…'); stamped live brief -> exit 0 GATED + parser-verified (Clarity barred, control seat allowed)",
    "no_regression": "28-brief scan -> {0: 24, 3: 4, 2: 0}; all 4 fires downstream-covered by exit 7; 17 descriptive-signal briefs correctly pass; meta-discussion briefs pass; all four suites green (claim-brief 22/22, stamper incl. 4 new tests, file-gap-brief, build-eligibility-index)",
    "self_quote": "'My first instinct was fire on lineage signals — the data showed 18 signal-carrying briefs, nearly all descriptive past-tense already handled downstream. Designing from the scan instead of the instinct kept the rule narrow (4 true fires, 0 false blocks)'"
  },
  "cousins": ["SN-1496 (wrong-layer meta-lesson — the 0821 work is the layer-move cure: representation/filing-contract, not width)", "SN-1386 (a gate the machine can't parse is an open fence — the t0562 class this detector now catches at filing time)", "gap-1412-lane5 STALE void (claim-liveness — machinery that fires on counted live state, same family)"],
  "decision_change": "detector/gate/rule designs start with a class count over the live population the rule will actually run over; the count (already-handled vs true-target vs clean) decides the rule's scope — narrow or broad — before any pattern is written. A proposed broad rule that skips the count is rejected as ungrounded; the live-population scan with per-member verdicts is the regression suite.",
  "falsifiability": "if the instinct-broad rule (all lineage signals) had been written first and shown zero false blocks on the same 28-brief scan, the count-first claim would be moot; the count claim stands because the scan demonstrably changed the design — 18 of 22 signals were excluded from the firing rule, and the excluded ones were each verified as handled downstream",
  "mechanism": "a detector's false-positive rate is set by the actual class distribution in the live data, not the imagined one. Designing from instinct targets the imagined distribution, so the rule fires on already-handled signals (noise against a downstream exit-7 that already refuses them) or misses the real shape. The count makes the real distribution visible: unhandled-class members become the firing set, handled members become the documented exclusions, clean members become the negative tests. The count is the design because scope follows distribution."
}
~~~
