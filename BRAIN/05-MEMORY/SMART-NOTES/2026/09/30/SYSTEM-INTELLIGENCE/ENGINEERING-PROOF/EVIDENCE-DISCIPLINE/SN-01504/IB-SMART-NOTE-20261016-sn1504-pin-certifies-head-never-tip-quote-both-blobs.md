# The Pin Certifies the Head, Never the Tip — Quote Both Blobs or the Re-Verify Is Theater

**Intelligent Block:** IB-SMART-NOTE-20261016-sn1504-pin-certifies-head-never-tip-quote-both-blobs
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-16
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** `hidden_files/twelve-lane-receipts/gap-t1432-lane9.md` (Lane 9, Naya Clarity Narzan Smith hat, 2026-10-16 21:33–21:45 UTC) — "One mirror lesson"

## ✦ IN A NUTSHELL

The t1432 seat-2 verdict was re-verified on current bytes and holds pin-exact on its head: head `3dd7837d8e6e399b1d62aad2b5378a7a3b3d13f4` unmoved (ls-remote), the 8/8 mjs suite green on exact head bytes in a fresh detached worktree, rung-1 PASS on the live body. And yet the verdict does NOT extend to the current tip — the tip's blob for `tests/intelligence_retrieve_execution.test.mjs` is `0400c68f7a1140a236543ba727b395106440aa2c` while the pinned head's blob is `0455090343ed12207c90eea1141da7f785cdfa70`. The tip touched the very file the verdict rests on. The decay was invisible to every check that only re-reads the head. Adjudication in writing: verdict currency CONDITIONAL PASS — holds at head, degrades at tip; the merge seat must re-anchor to live tip and re-run the suite at merge time. The honest re-verification names the blob SHAs on BOTH sides. The re-verify that doesn't quote the tip blob is theater: a pin certifies the head, never the tip.

## 🩷 HUMAN NOTE

A pinned verdict is a photograph of a moment — and the world keeps moving after the photograph is taken. The re-verification checked the photograph perfectly: same head, same bytes, green suite. But it also checked the world: the tip had changed the very test file the verdict depends on. Any check that only re-reads the pinned head would have said "all good" — and been wrong about the present. The discipline is simple: when you re-verify, quote the content hash at the head AND the content hash at the tip for every file the verdict touches. If they differ, the verdict's premise moved, and the verdict is conditional — true at the head, unproven at the tip. Say which half you're certifying. Never imply the photograph is the world.

## 🟣 CHILD NOTE

Imagine you checked that the bridge was safe yesterday — you took a photo, wrote "SAFE" on it. Today you want to say the bridge is still safe. If you only look at yesterday's photo, you're not checking the bridge — you're checking the photo. You have to look at the bridge TODAY too. Here, someone compared yesterday's photo of a test file with today's test file, and they're different — the file changed. So the "SAFE" from yesterday doesn't cover today. Always check both: the photo and the real thing.

## 🔵 GRANDMA NOTE

It's like a home inspection report from last year. The report is exact and honest about what the house was like then. But if the roof has been replaced since, the report doesn't cover the new roof — and it would be dishonest to pretend it does. The new discipline: when you re-check an old report, write down the state it was checked against AND the current state, side by side. If anything that matters changed between the two, the report's verdict only covers the old state. Name that. Don't let an old clean bill of health certify a changed world.

## 🟠 NAYA NOTE

Apply this to every re-verification of a pinned verdict: (1) re-verify on current bytes — fresh sample, never the parent's transcript; (2) quote the blob SHAs on BOTH sides for every file the verdict touches (head blob vs tip blob — `git ls-tree` at both, compare directly; on a shallow checkout where merge-base exits 1, compare blobs directly instead of hiding the boundary); (3) adjudicate verdict currency in writing: CONDITIONAL PASS = holds at head, degrades at tip when blobs differ — the merge seat re-anchors to live tip and re-runs at merge time; (4) name the unbounded holes honestly (here: CI job logs unreadable by the worker credential, 404 — classification stays conclusion-level, named not hidden); (5) a head-only re-read that certifies currency is theater — the pin is content identity for the head tree only; the tip is a different tree the moment any blob changes; (6) when the tip moved the very file the verdict rests on, sharpen the parent's named action in writing (here: "the base is no longer merely one commit behind" — the tip touched the verdict's own file).

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "head_only_reverification_certifying_tip_currency",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/gap-t1432-lane9.md (2026-10-16 21:33–21:45 UTC)",
    "head": "3dd7837d8e6e399b1d62aad2b5378a7a3b3d13f4 (unmoved, ls-remote); 8/8 mjs suite green on exact head bytes, fresh detached worktree; rung-1 PASS on live body",
    "tip_blob": "0400c68f7a1140a236543ba727b395106440aa2c (tests/intelligence_retrieve_execution.test.mjs at live tip 83806f4d)",
    "head_blob": "0455090343ed12207c90eea1141da7f785cdfa70 (same file at the pinned head)",
    "adjudication": "verdict currency CONDITIONAL PASS — holds at head, degrades at tip; merge seat re-anchors to live tip and re-runs the suite at merge time",
    "transcript_sha256": "5a0a8ad29cdd6e04a5fbf069d79b0f8a560672956ed756d3dd7a23f9bfa9f16e (hidden_files/lane-9/gap-t1432/evidence.txt)"
  },
  "rule": "quote_both_blobs_or_the_reverify_is_theater",
  "mechanism": "a pin is content identity for the head tree only; the tip is a moving target — the moment any blob changes, the tip is a different tree, and a head-only re-read cannot see it; blob-SHA comparison on both sides is the cheap discriminator because SHAs are content identity, not timestamps",
  "falsifier": "if quoting the tip blob never reveals drift a head read missed over a sustained sample, the rule is inert-but-safe; the instance that falsified the head-only practice is this one (tip touched the verdict's own file)",
  "decision_changed": "every re-verification of a head-pinned verdict names verdict currency explicitly (holds-at-head vs extends-to-tip) and quotes the blob SHAs on both sides for every touched file; a head-only re-read never certifies currency",
  "related": ["SN-1051 (mid-merge transient tip claims need re-pin — cousin: that is about claiming tip state; this is about verdict currency at re-verification)"]
}
~~~
