# Fetch the Evidence, Not the Repository — Single-Ref Fetch + Hash Proof for Remote-Branch Verification

**Intelligent Block:** IB-SMART-NOTE-20261015-sn01398-fetch-the-evidence-not-the-repository
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-15
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Category:** SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INDEPENDENT-VERIFICATION
**Provenance:** Captured on the 07:08 PDT smart-note-distillation tick (2026-10-15) from lesson-broadcast [t0818] (Naya Verity, lane-executor, independent branch verification).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Verity's independent branch verification replaced a full clone with a bare single-ref fetch — minutes → 2 seconds — with byte-identical proof: 9 blob hashes verified plus an orphan check. The proof statement was about blob *content*, and git objects are content-addressed: the proof needed only the objects it hashed, never the DAG. The durable rule: **match the fetch to the proof's needs.** Single-ref fetch when the claim is about content hashes; full history when the claim is about history (the opposite direction lives in SN-1000, where receipt gates anchoring artifact handles needed `fetch-depth: 0`). Fetch depth is a decision variable, not a habit. This is the standard fetch pattern for remote-branch proofs.

## 🩷 HUMAN NOTE

Shawn — verifying a remote branch used to mean downloading the whole repository, which took minutes. It turns out you only need the exact pieces you're checking: a targeted fetch of just those pieces, plus fingerprint verification, finishes in 2 seconds with proof byte-for-byte identical to the slow way. The flip side also holds: when the proof needs history (our receipt gates do), you fetch the full history. Lesson banked: fetch what the proof needs — nothing more, nothing less.

## 🟣 CHILD NOTE

To check one page of a book, she didn't copy the whole library — she asked the librarian to send just that page, then checked its fingerprint against the one on file. Same answer, seconds instead of hours. But if the question were "what did page 5 look like last year," she'd need the older editions too. The fetch matches the question.

## 🔵 GRANDMA NOTE

It's like asking for one recipe page instead of photocopying the whole cookbook to check a single ingredient. You get the page, you check the ingredients, you're done in seconds. But if the question is how the recipe *changed* over the years, you need the old editions — then you copy the whole book. Right-sized fetching.

## 🟠 NAYA NOTE

Apply to every remote verification you run: (1) name the proof's object set BEFORE fetching — blob SHAs → `git fetch origin <ref>` single-ref; history-anchored claims (receipt-gate artifact handles, merge-base arguments) → full fetch; (2) the hash check is the verdict, not the fetch method — the proof is byte-identical or it fails loudly, and a loud failure on a minimal fetch tells you the fetch was wrong, not the claim; (3) include the orphan check: verify no unlisted objects beyond the fetched set, so a minimal fetch can't silently pass on a partial tree; (4) record the standard: single-ref fetch + SHA verification is the default pattern for remote-branch content proofs — a full clone for a blob-hash proof is budget burned for nothing (budget law: ~2,500 actions/month).

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "category": "SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INDEPENDENT-VERIFICATION",
  "sibling_notes": ["SN-1000 (receipt-gate-fetch-depth-zero — opposite direction: proof needs history → fetch-depth: 0)", "SN-086 (qualify-only-the-fetchable-subject)"],
  "learning_refs": ["lesson-broadcast [t0818] (independent branch verification)"],
  "evidence": {
    "before": "full clone, minutes",
    "after": "bare single-ref fetch, ~2 seconds",
    "proof": "9 blob hashes verified byte-identical + orphan check",
    "source": "lesson-broadcast [t0818]: Naya Verity (lane-executor, independent branch verification)"
  },
  "rule": "match the fetch to the proof's needs — single-ref fetch + SHA verification for content-hash claims; full history for history-anchored claims",
  "decision_change": "the next seat verifying a remote branch's content claims defaults to single-ref fetch + blob-hash proof instead of a full clone",
  "falsifier": "a minimal fetch that cannot verify the required hashes (proof needs history traversal) shows the pattern misapplied — the fetch-then-verify either reproduces the hashes or fails loudly, so misapplication is self-detecting",
  "mechanism": "git objects are content-addressed — a proof statement about blob SHAs needs only those objects; a full clone additionally transfers the whole DAG (history the proof never touches), which is why the proof is byte-identical at a fraction of the transfer"
}
~~~
