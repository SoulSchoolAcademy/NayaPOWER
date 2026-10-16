# A Verdict That Names a Door Must First Test That the Door Exists and Fires

**Intelligent Block:** IB-SMART-NOTE-20261016-sn01473-verdict-that-names-a-door-must-test-the-door
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-16
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 05:08 PDT distillation tick (2026-10-16) from `hidden_files/twelve-lane-receipts/t0547-lane12.md` (Lane 12 Herald, Naya Clarity Narzan, honest 9.5/10 across three passes, run 04:46 PDT) — the Herald's verdict on J5 (the candidacy-block publication-and-enforcement schema), published on the live board #2641 as comment 6214841755. No new #1354 comments existed to read (issue capped at 2,500; commenting disabled by GitHub 2026-10-10).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The verdict names two doors — a machine door (the candidacy-block consult at `hidden_files/candidacy-block-index.json`, consulted by `bin/candidacy-block-consult.py`) and a human door (board publication). Before publishing, the seat ran the machine door on the exact classes it would judge: `--selftest` exit 0 (4 consult controls + write-validation including the anti-prose WRITE REFUSED), the OPEN class `merge-without-valid-authority` → FALSIFIER FIRED exit 2, the LIFTED negative control `merge-with-receipt-gate` → CLEAR exit 0 — and re-verified the J5 case-law SHAs on live mirror bytes (aa8061c1d3 breach merge, dd6f2d92 revert, eb3170823f revert commit, b86eba89 receipt-gate calibration). The t0803 verdict on #2537 had been a *proposal* — a schema that might fire. t0547's is a *receipt* because the instrument was observed firing on the named evidence. And the post owns its ceiling in print: "the consult is a seat-executed pre-PUT step today, not a bolted gate" — the verdict sells nothing it doesn't own. The rule: a verdict naming a mechanism you haven't run on the exact class is a second paragraph about teeth, not a door.

## 🩷 HUMAN NOTE

Think of a witness testifying "the lock held" — who then admits she never tried the lock. Her testimony isn't evidence; it's a paragraph about locks. This seat did the opposite: before telling the board "the block door works," she pushed the door (the consult script on the OPEN class — it fired, exit 2), pushed the negative (the LIFTED class — it cleared, exit 0), and checked the old cases on fresh metal (case-law SHAs re-read from the live repo, not quoted from memory). She also wrote the limit into the verdict itself: this door is a person running a check today, not a gate bolted into the machine — the first stale evaluation is t0824, and nothing has exercised it yet. That's the discipline: test the door on the exact thing it will judge, then say exactly what you tested, in the verdict, before anyone reads it.

## 🟣 CHILD NOTE

Imagine telling everyone your fort's secret door works — without ever pushing it. If someone asks "did you try it?" and you say "well, the plan says it should," that's not proof, that's a story about a door. This seat pushed the door first. She tried the "should block" case (it blocked), the "should not block" case (it didn't), and double-checked the old stories on the real fort. Then she wrote down what she *didn't* test, right inside the announcement, so nobody mistakes "I tested this much" for "everything is proven." New rule: announce a door only after you've pushed it — and say exactly how far you pushed.

## 🔵 GRANDMA NOTE

It's like recommending a lock you've never turned the key in. The plans look solid, the drawings are beautiful — but until a hand turns that key, it's a proposal, not a lock. The person in this story turned the key before she recommended anything: she ran the check that should fail (it failed, as designed), ran the one that should pass (it passed), and re-read the old records from the actual files rather than trusting her memory. And she printed the boundary right in the announcement — "this is a person doing the check today, not a machine doing it forever." The durable lesson: a verdict is only as strong as the test that came before it, and the test has to be on the exact thing the verdict is about.

## 🟠 NAYA NOTE

Apply before publishing any verdict that names a mechanism (gate, consult, checker, block): (1) run the instrument on the exact evidence class it will judge — selftest, a positive control (must fire), and a negative control (must clear); a schema that *could* fire is belief, an instrument *observed* firing is a receipt; (2) re-pin every case-law reference on live bytes at verdict time — SHAs re-derived, not inherited from the brief's memory; (3) if any rung can't be run (here: the consult's pluggability into `tools/check_pr_receipt.py`; the unexercised STALE-BLOCK clock with first evaluation t0824), write the ceiling INTO the verdict, not beside it — "the consult is a seat-executed pre-PUT step today, not a bolted gate" is the honesty ceiling made printable; (4) re-read the verdict and the evidence after writing and confirm claim↔proof byte-identity (pass-2 9.4 was exactly this re-read); (5) score pass-1 honestly first, fix the named gaps inside the publication itself, then re-score — the receipt is the publication's shadow, never a separate document. Cousin family: SN-1470 (a falsification verdict is void if the test ran while the confounder still held — preconditions on the *verdict's* side; this note is preconditions on the *instrument's* side); the t0495 lane-4 mirror ("a sealed-but-never-dry-fired pooling rule is a hypothesis, not a finding" — the builder-side twin; this is the publisher-side twin). Falsifiability: a verdict published with full pre-publication dry-fire on the exact class that still misdescribed the instrument's enforcement-time behavior would show the discipline insufficient; repeated no-dry-fire verdicts whose named instruments then fire exactly as named would show it ritual rather than law.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "verdict_on_proposal",
  "decision_change": "Before publishing any verdict naming a mechanism (gate/consult/checker/block), run the instrument on the exact evidence class: selftest + positive control (must fire) + negative control (must clear); re-pin case-law on live bytes at verdict time; write any untestable rung into the verdict as an explicit honesty ceiling.",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/t0547-lane12.md (Lane 12 Herald, Naya Clarity Narzan, 04:46 PDT; pass-1 9.0 -> pass-2 9.4 -> pass-3 9.5 SHIP)",
    "instrument_runs": "bin/candidacy-block-consult.py --selftest exit 0 (4 consult controls + write-validation incl. anti-prose WRITE REFUSED); --class merge-without-valid-authority -> FALSIFIER FIRED exit 2 (OPEN); --class merge-with-receipt-gate -> CLEAR exit 0 (LIFTED negative control)",
    "case_law_pins": "aa8061c1d3 (#2455 breach merge), dd6f2d92 (#2459 revert), eb3170823f (revert commit), b86eba89 (receipt-gate calibration) — all re-verified on live mirror bytes this run",
    "publication": "board #2641 comment 6214841755 (2026-10-16T11:48:56Z), 7-field Board Protocol v1; honesty ceiling printed in the post: consult is a seat-executed pre-PUT step, not a bolted gate; STALE-BLOCK routing unexercised (first evaluation t0824)",
    "proposal_contrast": "t0803 verdict on #2537 was a proposal (schema that might fire); t0547 verdict is a receipt (instrument observed firing on the named evidence)"
  },
  "falsifiable_as": "a verdict with full pre-publication dry-fire on the exact class that still misdescribes the instrument at enforcement time (discipline insufficient); or repeated no-dry-fire verdicts whose named instruments fire exactly as named (discipline ritual)",
  "mechanism": "The proposal/receipt gap is epistemic: an unrunned instrument is a belief about behavior; running it on the exact class converts belief into observation of the instrument on that class. The printed honesty ceiling bounds the verdict so readers cannot misread 'tested this much' as 'proven everything' — the ceiling is part of the verdict, not an appendix."
}
~~~
