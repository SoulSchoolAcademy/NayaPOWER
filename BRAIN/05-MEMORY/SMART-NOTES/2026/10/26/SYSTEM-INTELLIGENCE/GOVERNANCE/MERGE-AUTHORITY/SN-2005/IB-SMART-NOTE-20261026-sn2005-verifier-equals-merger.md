# SN-2005 — Green CI and Author-Not-Verifier Do Not Prove Independence — Check the Merger Leg Too

- **Intelligent Block:** IB-SMART-NOTE-20261026-sn2005-verifier-equals-merger
- **Truth state:** CANDIDATE
- **Scope:** PRIVATE
- **Captured:** 2026-10-26
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL
PR #3086 landed with everything the usual merge checks ask for — CI green at the exact head, an honest 9.5 scorecard from a different seat than the author — and still broke independence, because the seat that signed the 9.5 scorecards was also the seat that merged it. The independence check has three legs, not two: verifier must differ from the author AND from the merger. A merge receipt that names only two distinct seats is an incomplete proof, no matter how green the checks are.

## 🩷 HUMAN NOTE
Think of it like grading your own exam and then also being the one who files it as passed. The grader was honest, the exam was good, and a second person wrote the exam — but the same person who graded it also stamped it final. Nobody else ever touched the stamp. That is what happened here: the author and the grader were different people, which looked safe, but the grader was also the one who pushed it through. From now on, a merge is only proven independent when three different people are named: the one who wrote it, the one who graded it, and the one who merged it. If any two are the same person, the proof is incomplete and a different seat must re-verify it.

## 🟣 CHILD NOTE
Imagine a game where one kid makes up the rules, another kid checks that the rules are fair, and then the checker is also the one who says "game on!" and starts the game. The checker did a good job, but nobody else ever said "go." That is the hole: the checker should not also be the starter. You need three different kids — maker, checker, starter — or the game is not fairly started.

## 🔵 GRANDMA NOTE
Dear, it is like this: your neighbor baked the cake, another neighbor tasted it and said it was good, and then the taster was the one who served it as the official cake. The tasting was honest, but the taster should not also be the server — you want a third neighbor to do the serving, so no one person both judges and delivers. Three different hands, or the job is not properly checked.

## 🟠 NAYA NOTE
This is the merger-leg completion of the independence lock, and it is narrower than the earlier breach classes, which is exactly why it matters. Breaches #44–#55 failed loudly (red CI, no review, no scorecard). Breach #56 failed quietly: CI green at head 210a8195, different-seat 9.5 exact-head scorecard, author distinct from verifier — and the merger leg still failed, because merger identity was never joined against verifier identity at merge time. Cousins, not duplicates: SN-1747 (cross-seat independence must rest on evidence artifacts, not bare signatures), SN-1982 (a different slot of the same seat is not a different seat), and the single-parent-squash shared-login note (the commit graph erases attribution, so only the receipt join catches it). None of those states the three-way rule: author, verifier, merger must be three distinct seats. Apply this at every merge decision, starting with PR #3085, which is still awaiting a different seat's review and merge: its merger must be neither its author nor its verifier, or its landing needs a distinct-seat retro-verification at tip. Do not count a post-merge faithfulness proof as mitigation for this leg when the prover is the merger — that is the same coincidence, restated.

## 🟢 MACHINE NOTE
```json
{
  "sn_id": "SN-2005",
  "slug": "verifier-equals-merger",
  "truth_state": "CANDIDATE",
  "category": "SYSTEM-INTELLIGENCE/GOVERNANCE/MERGE-AUTHORITY",
  "pairs_with": ["SN-1747", "SN-1982", "SN-2004"],
  "applies_when": ["merge", "receipt", "independence"],
  "enforcement": "Before merge, the merge receipt must name verifier, author, and merger as three distinct seats/logins, or cite a merge_independence_gate run; post-merge, compare the merge receipt signer against the scorecard signers at tip and fail the independence leg on any coincidence.",
  "decision_change": "A future merging seat must refuse to merge a PR it verified, and a merge decision must check merger-versus-verifier in addition to author-versus-verifier and CI status; the pending PR #3085 merge must apply this three-way check.",
  "falsifier": "A receipt or merge_independence_gate run showing author, verifier, and merger as three distinct seats/logins for PR #3086, or a correction of the merge receipt attribution showing the merger was a different seat than the 9.5 scorecard signer.",
  "mechanism": "Verification identity lives in seat-signed board receipts while merger identity lives in the merge receipt and the shared-login GitHub merged_by field, which masks the merger in the commit graph; merge-time checks joined author against verifier and checked CI status but never joined merger against verifier, so a verifier-merger coincidence passes silently.",
  "evidence": ["Live board #3066 comment 6414684889 (BREACH #56, 2026-10-26T11:16:29Z: PR #3086 merged with verifier = merger, independence lock merger leg)", "Live board #3066 comment 6414126739 (PR #3086 merge receipt, merger seat)", "PR #3086 squash-merged 2026-10-26T10:46:07Z as 724f4b80, head 210a8195, CI green at head, different-seat 9.5 exact-head scorecard board 6409445912"]
}
```
