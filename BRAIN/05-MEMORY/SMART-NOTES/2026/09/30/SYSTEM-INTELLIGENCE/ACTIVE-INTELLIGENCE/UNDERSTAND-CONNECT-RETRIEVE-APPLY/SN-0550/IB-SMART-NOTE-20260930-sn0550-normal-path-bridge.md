# The Normal-Path Bridge: Learning Reaches Behavior Through the Ordinary Decision Path, Never a Special Learning Step

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0550-normal-path-bridge
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-07
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6042435676 ([NAYA] P0 learning activation seam — PR #1743 published and bounded, 2026-10-07T16:40:53Z); PR #1743, seam head `85102798286cd2288d6a158c5d384f649c4284ee`, main `e561beaab72f846b54f3aebf113641cab6d3283d`; #1724 cold-successor receipt

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

PR #1743 closed the P0 learning activation seam by implementing the missing normal-path bridge in canonical `nayanet-act-runtime` source: persisted KNOW/CONNECT receipt → ACT.PLAN → LAW re-resolution on consequential scope delta → exact PLAN + fresh LAW → ACT.EXECUTE → independent VERIFY handoff. The retained learning is not invoked by a special step, a caller-provided lesson ID, or a block reference — it flows through the ordinary decision path. The same task with the same authority change goes from baseline behavior to `PRESERVE_PROVENANCE_BEFORE_APPLY` **only when the normal KNOW selector returns the applicable retained learning**. The falsifier is built into the design: remove the seam and the delta disappears entirely; the caller never names the lesson, so the retrieval is provably the selector's work, not the harness's.

Why this is brain-grade: it defines what "learning is active" means mechanically. A learning loop where the caller must say "apply lesson X" is not retained intelligence — it is manual invocation wearing learning's clothes, and it fails the cold-successor test by construction (a cold agent cannot know what it never retained). The normal-path bridge is the only activation pattern that survives the cold-start boundary: the selector must return the applicable learning unprompted, or the system has not learned. The two-sided proof is the discipline: (1) presence — behavior changes only when the normal selector returns the applicable learning; (2) absence — removing the seam kills the delta, proving the path carried it and no side channel did.

## 🩷 HUMAN NOTE

Shawn — the big one from this tick, and it answers "how do we know she actually learned?" PR #1743 wires retained learning through the normal decision path: receipt → plan → law re-resolution → execute → verify, with the learning picked up by the ordinary selector — nobody tells the system which lesson to use. The proof is elegant: the same task changes behavior from baseline to provenance-preserving only when the selector itself finds the right lesson, and if you remove the bridge the change vanishes completely. That two-sided proof is now our definition of real learning: if the caller has to name the lesson, it isn't learned — it's just manual recall.

## 🟣 CHILD NOTE

Imagine a student who only answers the teacher's question when the teacher also hands her the answer sheet. Did she learn anything? No — she just read aloud. Real learning is when the student hears the question, searches her own memory, and answers from what she kept inside. That's what this bridge does: no answer sheet is handed over. The system reads its own memory, finds the right lesson by itself, and changes what it does. And we proved it by taking the bridge away — without it, the answer goes back to the old one.

## 👵 GRANDMA NOTE

A cook followed a recipe card handed to her each time — then one day the card was gone and she cooked from memory, adding the trick her grandmother taught her. Nobody told her to use the trick; she remembered it on her own. That's the difference between being handed the answer and having truly learned. Our system now cooks from memory: the lesson comes from inside, not from a card, and we verified it by taking the kitchen's recipe rail away and watching the dish still come out right.

## 🧠 NAYA NOTE

Cold successor: any learning-activation claim must pass the normal-path bridge test. (1) The caller provides the task and the authority context ONLY — no lesson ID, no block ID, no "apply this." (2) Run with and without the retained learning present; the behavior delta must appear only when the normal KNOW selector returns the applicable learning (presence proof). (3) Remove the seam and re-run: the delta must vanish completely (absence proof — no side channel carried it). (4) The full chain is receipt → PLAN → LAW re-resolution on consequential scope delta → exact PLAN + fresh LAW → EXECUTE → independent VERIFY handoff. A "learning" that requires the caller to name the lesson fails (1) and is manual invocation, not retained intelligence. Keep the falsifier live: PR #1743's gates are 48/48 Node, 6/6 Python, 12/12 typecheck/guard; kernel REDs are the inherited CONNECT `_shared` coverage pair owned by #1739 — do not duplicate that repair.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-0550",
  "title": "The Normal-Path Bridge: Learning Reaches Behavior Through the Ordinary Decision Path, Never a Special Learning Step",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-07",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "ACTIVE-INTELLIGENCE", "UNDERSTAND-CONNECT-RETRIEVE-APPLY"],
  "cousins": ["SN-0526", "SN-015"],
  "evidence": {
    "board": ["#1354 6042435676 ([NAYA] P0 learning activation seam — PR #1743 published and bounded, 2026-10-07T16:40:53Z)"],
    "pr": "PR #1743 (canonical nayanet-act-runtime source), seam head 85102798286cd2288d6a158c5d384f649c4284ee, main e561beaab72f846b54f3aebf113641cab6d3283d",
    "receipt": "#1724 cold-successor receipt — full handoff",
    "gates": "focused gates/falsifiers green: 48/48 Node, 6/6 Python, 12/12 typecheck/guard; guard firing coverage 76.1% (73.5% floor held); Ratified Guard, Spec Integrity, Collective Chain CI green",
    "key_result": "same task + authority change: baseline -> PRESERVE_PROVENANCE_BEFORE_APPLY ONLY when the normal KNOW selector returns the applicable retained learning; remove the seam and the delta disappears; caller provides no lesson or block ID",
    "kernel_red": "inherited CONNECT _shared execution-coverage pair (547/549); same two failures on current main; #1739 owns the repair — not duplicated"
  },
  "doctrine": {
    "normal_path_bridge": "persisted KNOW/CONNECT receipt -> ACT.PLAN -> LAW re-resolution on consequential scope delta -> exact PLAN + fresh LAW -> ACT.EXECUTE -> independent VERIFY handoff; the learning is picked up by the ordinary selector, never named by the caller",
    "presence_proof": "behavior changes only when the normal selector returns the applicable retained learning",
    "absence_proof": "removing the seam kills the delta completely — the path carried it, no side channel",
    "cold_start_test": "learning that requires the caller to name the lesson is manual invocation, not retained intelligence — it cannot survive the cold-successor boundary",
    "not_proven": "production learning activation and independent outcome verification remain NOT PROVEN (claimed as such in the board comment, not inflated)"
  },
  "rule": "learning is active only when it flows through the ordinary decision path unprompted; prove it two-sided — presence with the selector's retrieval, absence with the seam removed"
}
```
