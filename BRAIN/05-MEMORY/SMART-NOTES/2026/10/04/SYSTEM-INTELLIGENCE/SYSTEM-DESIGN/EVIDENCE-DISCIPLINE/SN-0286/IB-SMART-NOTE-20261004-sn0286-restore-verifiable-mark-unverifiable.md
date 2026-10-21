# Intelligent Block
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-04 ~16:15 PDT (Smart Note distillation tick)
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**SN number:** SN-0286
**Provenance:** #1354 comment 5985335215 (2026-10-04T22:53:43Z — "[NAYA 4] Hash Semantics Decision — WS-R11") and relay 5985364071 (2026-10-04T22:57:45Z — "[NAYA 2][RELAY] — WS-R11 hash-semantics receipt", live-verified PR #1414: OPEN, non-draft, mergeable=true, head `dfe1ccf9c388ee06fc5946e8de41884264e05a4a` on live main tip `94b39a53`, exactly 2 UNREPRODUCIBLE marks, 14-restored/2-marked split consistent with the patch).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## IN A NUTSHELL

**Decision: restore the verifiable, mark the unverifiable. Don't fake what you can't prove.** After #1401 removed all 16 content hashes from the registry on the rationale that they were "not verifiable from repo" — a rationale contradicting the owning function's own docstring (`tools/smart_note_v2.py::_canonical_content_hash` exists precisely for repo-side reconciliation) — Naya 4 recomputed every hash independently with the canonical formula `sha256(json.dumps(intelligence, sort_keys=True, separators=(",",":"), ensure_ascii=False))`. Result: **14 hashes reproduced exactly** from current capture files. SN-016: NOT reproducible — capture content changed after the hash was computed (checked both current and pre-merge versions; neither matches). SN-018: NOT reproducible — no capture file exists in the repo. Here is the sharp edge of this note: **Coda 3 reported 15/16 reproducible; Naya 4 found 14/16, and the delta was SN-016.** She could not reproduce SN-016 from any version in the repo. She wrote: "I'm going with what I verified, not what was claimed." PR #1414 restores the 14 verified hashes and explicitly marks SN-016 and SN-018 `UNREPRODUCIBLE` in provenance WITH REASONS — honest, not faked. Naya 2's relay independently verified the patch bytes at head (exactly 2 marks, reasons matching her record) and explicitly noted-but-did-not-adjudicate the 15/16-vs-14/16 discrepancy: "her lane's independent verification stands as recorded." Why this is the 9+ decision: **a verification system that cannot verify itself is the failure mode we're preventing.** Restoring the verifiable hashes closes the hole; marking the unverifiable ones — instead of inventing hashes or leaving them blank — preserves the integrity of the verification itself.

## HUMAN NOTE

Shawn — banking Naya 4's hash-semantics decision as standing evidence doctrine: "Restore the verifiable, mark the unverifiable." She independently recomputed all 16 content hashes: 14 reproduced byte-for-byte, SN-016 and SN-018 did not. Where Coda 3 claimed 15/16 and she proved 14/16, she went with her own verification — not the claim. PR #1414 restores the 14 and marks the two failures explicitly with reasons, rather than faking completeness or leaving blanks. The line I'm saving for every lane: "A verification system that cannot verify itself is the failure mode we're preventing. Don't fake what you can't prove." Naya 2 verified the patch bytes live without re-litigating the count dispute — corroborate the artifact, note the dispute, don't adjudicate another lane's verification. That's the relay pattern too: verify what you can see, record disagreements as-is.

## CHILD NOTE

Imagine a teacher checking 16 answers on a test. One classmate says "15 are right," but when you check yourself you can only prove 14 — one answer changed after the test was graded, and one page is missing entirely. The rule: write down the 14 you proved, and for the two you couldn't prove, write "couldn't verify" with WHY — never make up answers and never pretend the question wasn't asked. And when someone else's count disagrees with yours, trust your own checking, not their claim. A system whose whole job is checking answers must never pretend to check something it can't.

## GRANDMA NOTE

We've written down a rule about honesty in verification. A seat recomputed sixteen security fingerprints herself: fourteen matched exactly; one didn't match any version on record (the content was changed after the fingerprint was taken); one had no file to check against at all. She restored the fourteen proven ones and marked the two failures openly, with reasons — rather than inventing fingerprints or leaving them blank. When another seat's count disagreed with hers, she trusted her own verification over the claim. And a second seat verified the repair itself without re-arguing the disputed count — corroborate what you can see, record the disagreement as-is. The principle: a system whose purpose is verification must never fake what it cannot prove — the day it does, the whole system's trust is gone.

## NAYA NOTE

For me, months from now: this is the epistemic discipline behind every hash/registry repair. Rules: (1) Recompute with the canonical formula yourself — the owning code's docstring is the semantics, not a PR description's rationale (#1401's "not verifiable from repo" contradicted `smart_note_v2.py`'s own docstring). (2) When counts disagree across lanes (15/16 vs 14/16), the tie-breaker is your own independent verification, not the seniority of the claim. Say it plainly: "I'm going with what I verified, not what was claimed." (3) Mark the unverifiable explicitly WITH reasons — fabricated hashes are worse than missing ones; blanks hide the hole. (4) The corroboration lane pattern: verify the artifact's bytes at head (count of marks, reasons present, patch consistent), note-but-don't-adjudicate cross-lane disputes. Related: SN-0250 (green run ≠ sound registry — the structural problem this repairs), SN-0059 (attribute before blame), SN-0240 (classify before healing), SN-0247 (supersession identity).

## MACHINE NOTE
```json
{
  "sn": "SN-0286",
  "title": "Restore the Verifiable, Mark the Unverifiable: Never Fake What You Can't Prove",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-04",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "SYSTEM-DESIGN", "EVIDENCE-DISCIPLINE"],
  "cousins": ["SN-0250", "SN-0059", "SN-0240", "SN-0247"],
  "evidence": {
    "comments": "#1354 5985335215 (2026-10-04T22:53:43Z) / relay 5985364071 (2026-10-04T22:57:45Z)",
    "decision": "WS-R11 hash semantics: restore 14 verified hashes (PR #1414, head dfe1ccf9 on tip 94b39a53); mark SN-016 + SN-018 UNREPRODUCIBLE with reasons",
    "dispute": "Coda 3 claimed 15/16 reproducible; Naya 4 verified 14/16 — SN-016 the delta; went with own verification",
    "formula": "sha256(json.dumps(intelligence, sort_keys=True, separators=(',',':'), ensure_ascii=False))"
  },
  "rules": [
    "the owning code's docstring is the hash semantics, not a PR description's rationale",
    "when lane counts disagree, the tie-breaker is own independent verification, never claim seniority",
    "mark the unverifiable explicitly with reasons — fabricated hashes are worse than missing ones",
    "a verification system that cannot verify itself is the failure mode being prevented"
  ],
  "durable_test": "A cold Naya repairing registry hashes will (1) recompute every hash itself with the canonical formula, (2) restore only what it reproduced, (3) mark failures with reasons, (4) prefer its own verification over another lane's count claim."
}
```
