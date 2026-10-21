# One Exact-Tip Battery Is Enough — Never Re-Run Evidence the Tip Already Produced

**Intelligent Block:** IB-SMART-NOTE-20261005-sn0440-one-exact-tip-battery-is-enough
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6010347808 ([Naya 2][overnight-sweep] 22:52 PDT gate report — tip `613133b6`, 2026-10-06T05:59:57Z / 2026-10-05 22:52 PDT).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The 22:52 PDT sweep ended with a scored decision: defer the cold-test re-run and the scorecard bump until PR #1588 merges. Reason: the tip (`613133b6`) is knowingly RED on the drift check, and the brain-build loop had already run the exact-tip battery 28 minutes earlier — re-running now would duplicate that evidence, not strengthen it. Re-verify on the post-merge tip.

Why this is brain-grade: evidence attaches to the tip, not to the sweep. A verification battery measures the exact bytes of one tip; running the identical battery again on the identical bytes produces a second copy of the same measurement, which looks like rigor and adds nothing. Rigor is not repetition — it is re-anchoring: re-run when the tip moves (here: after #1588 merges), because only new bytes can produce new evidence. This is the mirror image of SN-0233 (the Phantom Green — verify on virgin state, never on the repaired environment): virgin state makes a pass *about the subject*; unchanged state makes a re-run *not about anything new*. The failure mode it prevents is CI churn — overnight lanes each re-running the full battery "to be sure," each run green or red in the same places, each run billed against human attention and compute, each adding zero information. A cold Naya inheriting an un-verified tip must learn the question that precedes every battery: "has the tip moved since this battery last ran?" If no, don't run — cite the existing evidence. If yes, run fresh on virgin state.

## 🩷 HUMAN NOTE

Shawn — one clean discipline from the overnight sweep: the 22:52 sweep deliberately did NOT re-run the cold tests or bump the scorecard, because the brain-build loop had already run the full battery on the exact same tip 28 minutes earlier — re-running would duplicate evidence, not strengthen it. Banked rule: evidence attaches to the tip, not to the sweep — re-verify when the tip moves (after #1588 merges), never re-run just to feel more sure. Rigor is re-anchoring, not repetition.

## 🟣 CHILD NOTE

Imagine a scientist measures a rock and writes down "it weighs 5 pounds." Then her friend says "are you sure?" and she measures it again — still 5 pounds. Measuring it a third, fourth, fifth time doesn't make the answer more true; the rock didn't change. The only reason to measure again is if the rock changed — a different rock needs a new measurement. Tips are like rocks: once you've measured the exact tip, measure again only when the tip moves.

## 👵 GRANDMA NOTE

If you counted the eggs in the carton this morning and nobody has opened the fridge since, you don't count them again at noon — the count is still good. You count again when someone takes eggs out or buys a new carton. A verification battery is an egg count: it describes the tip exactly as it was. Re-running it on the same tip is counting the same eggs twice. Count again when the tip moves — a new tip is a new carton.

## 💜 NAYA NOTE

Note to future me: before running any verification battery, ask the one question: has the tip moved since this battery last ran? If no — don't run; cite the existing evidence, name the tip SHA it was measured on, and move on. A second run on identical bytes is duplicate evidence, not stronger evidence, and overnight lanes each re-running "to be sure" is CI churn billed against human attention. If yes — run fresh, and run on virgin state (SN-0233): the new tip deserves a genuine measurement, not a re-warmed one. The sweep's decision is the template: defer the cold-test re-run and scorecard bump until #1588 merges, because the post-merge tip is the next tip that can produce new evidence. Rigor is re-anchoring, not repetition.

## ⚙️ MACHINE NOTE

{"sn": "SN-0440", "title": "One Exact-Tip Battery Is Enough — Never Re-Run Evidence the Tip Already Produced", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-05", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "OPERATIONS", "EVIDENCE-PER-TIP"], "cousins": ["SN-0233", "SN-0421", "SN-0392"], "authority": "observed episode — Naya 2 overnight sweep scored decision, CANDIDATE (auto-capture, not ratified)", "evidence": {"board": "#1354 6010347808 ([Naya 2][overnight-sweep] 22:52 PDT gate report — tip 613133b6, 2026-10-06T05:59:57Z / 2026-10-05 22:52 PDT)", "decision": "cold-test re-run + scorecard bump deferred until PR #1588 merges — the tip is knowingly RED and the brain-build loop already ran the exact-tip battery 28 min ago; re-running now would duplicate that evidence; re-verify on the post-merge tip"}, "doctrine": {"evidence_attaches_to_the_tip": "a verification battery measures the exact bytes of one tip; a second run on identical bytes produces a duplicate measurement, not a stronger one", "the_one_question": "before any battery, ask: has the tip moved since this battery last ran? No → cite the existing evidence (name the tip SHA). Yes → run fresh.", "rigor_is_re_anchoring": "rigor is re-anchoring on new bytes, not repetition on old ones; overnight lanes re-running 'to be sure' is CI churn against human attention and compute", "mirror": "mirror of SN-0233 (verify on virgin state — virgin state makes a pass about the subject); unchanged state makes a re-run not about anything new", "family": "pairs with SN-0421 (a run-level SUCCESS with skipped behavioral jobs is vacuous — the inverse: a completed battery on the exact tip IS sufficient)"}}
