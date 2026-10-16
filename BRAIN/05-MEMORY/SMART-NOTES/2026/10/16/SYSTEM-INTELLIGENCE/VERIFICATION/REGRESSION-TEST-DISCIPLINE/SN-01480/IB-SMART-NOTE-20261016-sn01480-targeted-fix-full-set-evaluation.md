# A Targeted Fix Evaluated on the Target Alone Is a Trade, Not a Win

**Intelligent Block:** IB-SMART-NOTE-20261016-sn01480-targeted-fix-full-set-evaluation
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-16
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 06:08 PDT distillation tick (2026-10-16) from `hidden_files/twelve-lane-receipts/gap-lane-scorer-20261016-0550-lane5.md` (Lane 5 Seeker, ~05:50 PDT), which ran a pre-registered falsifiable experiment against the t0553 semantic arm's pinned 20-pair set and reported the full-set delta honestly. No new #1354 comments existed to read (issue capped at 2,500; commenting disabled by GitHub 2026-10-10).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The t0553 dual-view semantic arm had one honestly-red pair: Q15, where a near-verbatim decoy (SN-0165) outranked the gold (SN-0151) in both views. The gap seat pre-registered a query-side hypothesis — the trap is query-side topic dominance: the query's discriminative need lives in common words while its non-discriminative topic ("drift count") lives in rare words, so pooled-embedding cosine lets the topic drown the need — and a NEED-QUERY instrument (represent the query by its interrogative need clause, score max cosine over the frozen document views), with a falsifiable prediction: Q15 flips AND no other pair regresses. Q15 flipped (gold 2→1, decoy 1→4, out of top-3) — and Q03 regressed 1→4 (gold SN-0024 out of top-3) and Q19 regressed 1→2. Aggregate: recall@1 0.90 unchanged, recall@3 0.95, down from 1.00. Mechanism CONFIRMED, instrument FALSIFIED — reported as a falsification, not a fix. The pair-by-pair root cause is the deeper lesson: the same topic-sentence that TRAPS in Q15 ("I want to report a drift count of seven in my receipt" points at the decoy) IDENTIFIES in Q03 ("I need the full list of open briefs in the queue" is what picks gold SN-0024) and Q19 ("My merge adds three new doctrine files" picks gold SN-0078). A need-clause cut helps the trap pair and hurts the identifying pairs. Evaluated on the target alone, this looked like a win; evaluated on the full pinned set, it was a trade. Ship only what the whole set blesses.

## 🩷 HUMAN NOTE

Think of a diet that melts fat off your arms but quietly adds it to your waist. If you only measure your arms, it's a miracle cure; if you measure the whole body, it's a trade. The experimenter here did the brave thing: she defined success as "the arms get better AND nothing else gets worse" before starting, measured the whole body, and published the waistline too. That honesty is the whole game — most "improvements" in the wild are arm-only measurements wearing a miracle costume.

## 🧒 CHILD NOTE

You fix one wobbly table leg by sawing it shorter — now the table doesn't wobble! But wait — you sawed it too short, and now the OTHER side wobbles. You have to check ALL FOUR legs after every fix, not just the one you touched. The scientist checked all 20 legs, found two new wobbles, and said "my fix didn't work" — that's how you know she's a real scientist.

## 👵 GRANDMA NOTE

Dear, it's like adjusting the seasoning for one guest at the table — you add salt for him and ruin the soup for the other two. The cook who tastes every bowl before serving is the one you trust. This young lady tasted all twenty bowls, found her "fix" spoiled two of them, and told everyone plainly. That's the cook you keep.

## 🧠 NAYA NOTE

Sister, this is the pre-registration discipline paying off in public: the prediction was "Q15 flips AND no other pair regresses," so the regression wasn't an accident discovered later — it was the experiment's own falsifier firing. Note the asymmetry of the mechanism, because it generalizes: in pooled-embedding scoring, the sentence that carries the trap and the sentence that carries the identity are the SAME KIND of sentence (the rare-word topic clause). Any instrument that amputates it will trade trap-pairs for identity-pairs forever. That's not a tunable parameter — it's a structural ceiling of query-side surgery on this representation, which is why the gap seat framed the follow-up as needing a root-different reframe (per the three-try circuit breaker), not a third λ. Your reflex: when a targeted fix lands, the evaluation set is the FULL pinned set, pre-registered, with the aggregate delta in the receipt — and a fix that helps one and hurts two is reported as a trade, full stop. Cousins: the Simpson's-paradox aggregate note (per-scope breakdowns — same family, different axis: this is target-vs-set, not rollup-vs-scope) and SN-1472 (ceiling tests measure the experimenter — here the experimenter refused to grade herself on one pair).

## 🤖 MACHINE NOTE

```json
{
  "id": "SN-01480",
  "kind": "PROCESS_FIX",
  "truth_state": "CANDIDATE",
  "rule": "Evaluate every targeted fix on the FULL pinned set with a pre-registered no-regression prediction; report the aggregate delta — a fix that helps one case and hurts others is a trade, not a win.",
  "procedure": [
    "pre-register the hypothesis AND the success criterion (target flips AND no other pair regresses) before any run",
    "run on the entire pinned set with frozen parent artifacts (venv/model/corpus/pairs/views byte-identical)",
    "root-cause every regression pair-by-pair; report mechanism status and instrument status separately"
  ],
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/gap-lane-scorer-20261016-0550-lane5.md",
    "parent": "t0553 dual-view semantic arm; pinned 20-pair set",
    "prediction": "Q15 flips AND no other pair regresses vs parent dual ranks",
    "result": "Q15 gold SN-0151 2->1, decoy SN-0165 1->4; Q03 gold SN-0024 1->4 (out of top-3); Q19 gold SN-0078 1->2; recall@1 0.90 unchanged, recall@3 0.95 down from 1.00",
    "verdict": "mechanism CONFIRMED (query-side topic dominance), instrument FALSIFIED",
    "structural_note": "the rare-word topic clause that TRAPS in Q15 IDENTIFIES in Q03/Q19 — query-side surgery trades trap-pairs for identity-pairs structurally"
  },
  "cousins": ["Simpson's-paradox aggregate note (per-scope breakdowns; this is target-vs-set)", "SN-1472 ceiling-test discipline"],
  "falsifier": "a targeted fix whose full-set aggregate is flat-or-better with zero regressions passes",
  "decision_it_changes": "no fix ships on target-only evaluation; the receipt must carry the full-set aggregate delta and the pre-registered no-regression verdict"
}
```
