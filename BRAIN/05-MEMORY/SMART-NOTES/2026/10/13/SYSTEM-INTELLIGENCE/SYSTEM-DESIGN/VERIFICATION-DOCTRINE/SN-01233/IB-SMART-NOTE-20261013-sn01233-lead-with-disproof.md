# IB-SMART-NOTE-20261013-sn1233

**Intelligent Block:** SN-1233
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

Lead with disproof, not sides. t-converge (Naya Conductor, lane 7, convergence provenance map, 9.0/10): the enforcement map byte-checks the Judge's ruling's premises BEFORE listing any questions — two of the ruling's premises are byte-disproven at exact commits (a) Naya 2's "written, signed, live" contract is worker-local-only, no repo presence; (b) "machine-enforced via naya-contract.py" — the only naya-contract.py in the repo lives on Naya 5's unmerged branch. The map also distinguishes what claims SAY from what bytes DO: Naya 5's set has a gate + red-team tests in bytes; Naya 2's set has text only; Naya 4's set has a gate but tests uncommitted. The key move: when a brief says "verified via git log --all" by another seat, re-run it or name the residual explicitly — the map flags its own "never in any repo branch/commit" as resting on Naya 4's git-log verification, "not re-run with a full clone this turn; flagged as read-not-reproven." For constitutional inputs, re-run. Drift line: facts only, no synthesis, no winner-picking — the map does not overturn the ruling (that is Shawn's word), it supplies the byte-proof the decision needs.

## HUMAN NOTE

Two seats disagreed about which contract is real. The third seat didn't pick a side — she built a table of every claimed file: exact repo path, branch, commit, blob SHA, size. Two of the ruling's premises failed against the bytes: one file was never in the repo at all; the enforcement script lives on a different seat's unmerged branch. And where she couldn't prove something herself (relying on another seat's git-log check), she said so explicitly — "read-not-reproven" — instead of inheriting the certainty. The discipline: disprove first, question second, and never let someone else's "verified" become your "verified" on constitutional questions without either re-running it or labeling the residual.

## CHILD NOTE

Two friends argue about whose rule is real. A wise third friend doesn't take sides — she checks: where is the rule? Can you show me the exact paper? She finds out one rule was never written down, and the other rule lives in someone else's notebook. And when she uses someone else's checking work, she says so honestly: "I didn't check this one myself." Check the thing, not the side. And say what you didn't check.

## GRANDMA NOTE

Dear, it's like two people arguing over whose name is on the deed. You don't take a side — you go look at the deed yourself. If one person can't show you the paper, that's the end of their side. And if someone tells you "I already checked," on an important matter you check again yourself — or you say plainly that you're trusting their word. Honest checking, not taking sides.

## NAYA NOTE

For every Naya asked to adjudicate or map a disputed claim: (1) build the provenance table first — artifact, exact repo path, branch, commit SHA, blob SHA, size; (2) byte-check each premise of any ruling BEFORE listing questions — the map leads with disproof, never with sides; (3) distinguish 'has a gate' from 'is enforced' — a gate with no red-team tests in bytes is text, not enforcement; (4) when your input says "verified via <command>" by another seat: for constitutional inputs, RE-RUN it; if you cannot, name the residual explicitly ("read-not-reproven") — never inherit certainty silently. (5) Drift line: facts only — no winner-picking; the map supplies byte-proof for Shawn's decision, it does not make it. Evidence: t-converge-lane7.md §§1,4,5 — two premises disproven at exact commits; §5 open question on ratification header ("Ratified by Shawn's word" with no ratification on record) remains Shawn's to answer.

## MACHINE NOTE

```json
{
  "lesson_id": "SN-1233",
  "title": "lead with disproof, not sides — re-run inherited verifications on constitutional inputs",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-13",
  "category": "SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/VERIFICATION-DOCTRINE",
  "evidence": [
    "twelve-lane-receipts/t-converge-lane7.md (Naya Conductor, lane 7, 9.0/10): provenance table artifact/path/branch/commit/blob/size; §4 ruling premise check — (a) Naya 2 'written, signed, live' worker-local-only, (b) 'machine-enforced via naya-contract.py' disproven (only copy on Naya 5's unmerged branch); enforcement distinction gate+tests vs text-only vs gate-without-tests; §5 'read-not-reproven' residual flag on inherited git-log verification",
    "lesson-broadcast.md t0679 entry: map leads with disproof, not sides; drift line facts-only"
  ],
  "rule": "byte-check a ruling's premises before listing questions; inherited 'verified' claims are re-run or explicitly residual; provenance tables precede adjudication",
  "anti_pattern": "side-taking without byte-proof; silently inheriting another seat's verification; confusing 'has a gate' with 'is enforced'",
  "related": ["SN-01228", "SN-01231"]
}
```
