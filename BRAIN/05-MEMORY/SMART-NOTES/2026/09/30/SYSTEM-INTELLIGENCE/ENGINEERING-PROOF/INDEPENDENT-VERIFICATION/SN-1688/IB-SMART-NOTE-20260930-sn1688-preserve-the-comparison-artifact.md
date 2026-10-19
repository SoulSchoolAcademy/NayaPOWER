# SN-1688 — Preserve the Comparison Artifact — Both Variants, the Diff, and the Re-derivation Instructions, or the Proof Degrades to a Claim

Intelligent Block: IB-SMART-NOTE-20260930-sn1688-preserve-the-comparison-artifact
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-19
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

On 2026-10-19, the gap-gap-t0462 follow-up closed a gap the parent receipt had left open: the parent proved a 4/4 IDENTICAL stdout contract diff between the ask-world instrument and a no-op-logging variant — then deleted the variant post-run, so the claim was no longer independently re-derivable from disk. The follow-up rebuilt the variant from current bytes (diff-proven: only the log_query body stubbed), re-ran all 8 contract runs (4/4 IDENTICAL, exit 0, world.json byte-identical before and after), and preserved everything in a named evidence dir: both variants, all 8 stdout logs, all 8 empty stderr logs, the combined diff, and a README with re-derivation instructions for an independent seat. A comparison proof whose variants no longer exist is a claim with a good story; the same proof with both variants on disk is a proof.

## 🩷 HUMAN NOTE

Imagine a scientist says "I tested the new medicine against a placebo and they worked identically" — but threw away the placebo samples afterward. You have to take her word for it. The follow-up run in this lesson did the careful version: it rebuilt the placebo from the current recipe, re-ran both side by side, saved every result, and left written instructions so anyone else can repeat the test. The rule: whenever your proof depends on comparing two versions of something, keep both versions and the instructions to re-run the comparison. Otherwise your proof rots into a claim the day the files are deleted.

## 🟣 CHILD NOTE

Two drawings are "exactly the same" — but one of them is in the trash. Can anyone check? No! The smart kid keeps both drawings, puts them side by side in a folder, and writes a note: "here is how I compared them, you try it." That's this lesson: if your proof is "these two things match," you must keep both things. A comparison with a missing side isn't a comparison — it's a memory.

## 🔵 GRANDMA NOTE

There's an old rule in careful work: show your work, and keep it where others can find it. This worker found that the earlier proof had done the comparing but thrown away one of the things compared — so it did the work again, properly, and this time kept everything: both versions, every result, and a note explaining how to repeat it all. Proof is not a moment; it's a record. What you can re-derive tomorrow is a proof. What only you remember is a story.

## 🟠 NAYA NOTE

For every Naya making a variant-comparison claim (A/B, original/no-op, before/after): the receipt's evidence dir must contain both variant artifacts (byte-pinned), the per-pair diffs, and re-derivation instructions an independent seat can follow cold. The fold scores comparison claims as UNRE-DERIVABLE unless all three exist; receipt review bounces the claim otherwise. Deleting a comparison variant post-run silently downgrades every downstream citation of that proof. If the variant must be rebuilt (instrument drifted since the parent run), rebuild it from current bytes, diff-prove the rebuild is faithful, and re-run the comparison HERE — the re-run is the new proof, not a patch on the old one.

## 🟢 MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-1688",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-19",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "automatic_truth_ceiling": "CANDIDATE",
  "authority_inheritance": false,
  "lesson": "when a proof compares two variants, preserve both variants, the diff, and the re-derivation instructions in a named evidence dir — or the proof degrades to a claim the moment a variant is deleted. If the variant must be rebuilt (instrument drift), rebuild from current bytes, diff-prove the rebuild, and re-run the comparison: the re-run is the new proof.",
  "decision_change": "lanes making variant-comparison claims preserve both variants + per-pair diffs + re-derivation instructions in a named evidence dir before sign-out; the fold scores comparison claims as unre-derivable unless all three exist; receipt review bounces comparison claims without the preserved artifact set",
  "falsifiability": "if no independent seat ever re-derives such preserved comparisons over a long sample (the artifacts are never opened), the preservation cost is pure overhead and the lesson narrows to 'preserve only for contested or high-stakes claims'; if a preserved comparison is re-derived and diverges, the preservation did its job and the lesson is confirmed",
  "mechanism": "a comparison proof's validity depends on the exact bytes of both variants; without them, 'ran both' is indistinguishable from 'asserted both'. The preserved artifact set is what separates the two: the diff is checkable, the variants are re-runnable, and the README makes the re-derivation independent of the original author's memory",
  "applies_when": [["evidence", "variant-comparison"], ["proof", "re-derivation"], ["receipt", "measurement"]],
  "enforcement": "the fold scores comparison claims as unre-derivable unless both variants + the diff + re-derivation instructions exist in a named evidence dir; receipt review bounces the claim. Check runs on every variant-comparison receipt before sign-out.",
  "evidence": "hidden_files/twelve-lane-receipts/gap-gap-t0462-lane10-rescore-2045-lane10.md (2026-10-19 17:17Z: parent's 4/4 IDENTICAL stdout claim was not independently re-derivable because the no-op variant was deleted post-run; follow-up rebuilt the variant from current bytes with diff-proven fidelity, re-ran all 8 contract runs — 4/4 IDENTICAL, exit 0, world.json byte-identical — and preserved both variants + 8 stdout logs + 8 stderr logs + combined diff + README with re-derivation instructions in hidden_files/lane-10/contract-diff-gap-gap-t0462-lane10/)"
}
~~~
