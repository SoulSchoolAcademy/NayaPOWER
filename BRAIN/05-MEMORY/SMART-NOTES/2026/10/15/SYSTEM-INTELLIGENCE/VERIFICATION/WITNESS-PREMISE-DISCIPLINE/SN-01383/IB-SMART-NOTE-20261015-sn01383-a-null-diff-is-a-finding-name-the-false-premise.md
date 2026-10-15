# A Null-Diff Is a Finding, Not an Absence — Name the False Premise with Proof

**Intelligent Block:** IB-SMART-NOTE-20261015-sn01383-a-null-diff-is-a-finding-name-the-false-premise
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-15
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 04:38 PDT smart-note-distillation tick (2026-10-15) from `hidden_files/twelve-lane-receipts/gap-scorer-20261015-0040-lane10.md` (Naya Clarity Narzan, Lane 10 Verity hat, 2026-10-15 11:29–11:31 UTC), Half 2 — the mirror lesson of a requested byte-diff that had no wire to diff.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The gap asked for a byte-level diff showing consult path (2) — the `candidacy-block-consult` script — plugs into the receipt-gate machinery. The seat did the byte work: `hidden_files/enforcement/check_pr_receipt.py` (sha `e1436de3…`) contains ZERO mentions of "candidacy" — no import, no subprocess call, no exit-code check — and a workspace-wide sweep of the canonical dirs (`hidden_files/bin/`, `hidden_files/enforcement/`) found the ONLY file referencing `candidacy-block-consult` is the consult script itself. So the requested "diff" is a null-diff on both sides: pluggability cannot be byte-diffed because pluggability was never built.

The honest close was not another round of greps. It was naming the false premise with proof: path (2) is a contract statement ("a merge attempt whose class matches an OPEN entry fails the consult with the verdict pin attached"), not a wiring. The consult runs as a seat's pre-PUT step; nothing in the receipt-gate check calls it. Actual pluggability — a call site inside `check_pr_receipt.py`, or a required check that fails on a fired consult — is an adoption/wiring gap owned by governance (Shawn's word + a merge), not a byte gap. "Not byte-diffed for pluggability" assumed a wire existed to diff; the bytes said no wire was ever built. A null-diff is a finding, not an absence.

## 🩷 HUMAN NOTE

Imagine asking a mechanic to "show me where the new brake line connects to the pedal." He looks, looks again, then tells you: there's no connection to show — the brake line was never installed. The useful answer isn't "I couldn't find it" (that sends you back to search the car), it's "it was never installed — here's the proof, and installing it is a garage job, not a search job." That's what happened: the empty result was the answer, not the failure to find one.

## 🟣 CHILD NOTE

Imagine your teacher asks you to compare your drawing to the class mural to show how your drawing hangs on the wall. But your drawing was never hung — it's still in your backpack. Comparing it to the wall would take forever and prove nothing. The smart answer is: "There's nothing to compare — it was never hung. Hanging it is a separate job." An empty comparison is the finding, not a missing answer.

## 🔵 GRANDMA NOTE

It's like calling the phone company to ask why your new phone line sounds bad, and they check and tell you: "There's no line connected to your house at all." That's not them failing to find the problem — that IS the problem. You don't keep testing the silent handset; you book an installation. When the evidence says "never built," the next step is building, not more checking.

## 🟠 NAYA NOTE

Apply this every time a byte-verification returns empty: (1) before re-running the check, state the check's premise explicitly — "this diff assumes a wire exists at <location>"; (2) sweep the canonical locations for the wire's endpoints (imports, call sites, references) — if none exist, the premise is false; (3) close the gap with the false-premise finding and its proof (pins, zero-mention counts, sweep scope) — not with another round of greps; (4) route the underlying desire to the right owner — here, actual pluggability is a governance/adoption question (needs Shawn's word + a merge), not a byte question; (5) keep the honest boundary: the null-diff finding closes the premise, not the desire — name both, and name who owns the desire.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "byte_check_on_a_never_built_wire",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/gap-scorer-20261015-0040-lane10.md (Naya Clarity Narzan, Lane 10, 2026-10-15 11:29-11:31 UTC), Half 2",
    "zero_mentions": "hidden_files/enforcement/check_pr_receipt.py sha e1436de3ba9d8d058b87a3db5199152d28a700a51afe2e4623f93de6438b — 0 mentions of 'candidacy' (no import, no subprocess call, no exit-code check)",
    "sweep": "workspace-wide sweep of canonical dirs (hidden_files/bin/, hidden_files/enforcement/): ONLY the consult script itself references candidacy-block-consult",
    "design_doc": "hidden_files/candidacy-block-index-design-t0818.md §3 — path (2) names tools/checks without claiming pluggability; pass-1 narrowing confirmed the consult works standalone as a seat's pre-PUT step",
    "parent_pins": "consult script b375bb9d…, index d3e1b234…, design doc 732c921a… — all re-derived byte-exact, unmodified"
  },
  "rule": "a_null_diff_is_a_finding_name_the_false_premise_with_proof",
  "procedure": [
    "when a byte-verification returns empty, state the check's premise explicitly before re-running it",
    "sweep the canonical locations for the premise's endpoints (imports, call sites, references); if none exist, the premise is false",
    "close with the false-premise finding plus proof (pins, zero-mention counts, sweep scope) — never with another round of greps",
    "route the underlying desire to its true owner (here: governance — Shawn's word + a merge), and name who owns the desire"
  ],
  "decision_change": "the next time a byte-level 'show me the wiring' check comes back empty, the default close becomes 'premise false with proof' instead of 're-run the check' — and the report names the adoption/wiring owner, not the absence",
  "falsifiability": "if a call site is later found that the canonical-dir sweep missed (e.g., a wrapper script outside hidden_files/bin/ or hidden_files/enforcement/), the premise-false verdict is falsified and the diff must be produced",
  "mechanism": "a diff needs two endpoints; an unbuilt integration has no call site, so an empty result is structural — the sweep measured the absence of the object, not a failure to measure. Re-running the measurement cannot change the structure",
  "related": ["SN-01381 (premise shift — reconstruct the author's rule before correcting)", "SN-01380 (absent is a value — name the absence rule in bytes)"]
}
~~~
