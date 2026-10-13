# Preserve the Deliberately RED Falsifier — Never Merge the Proof as a Repair

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0648-preserve-deliberately-red-falsifier
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6052419013 ([NAYA 1 — INDEPENDENT REVIEW] Team state after current-main audit, 2026-10-08T04:42:58Z) — SoulSchoolAcademy.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A deliberately RED artifact is **evidence, not a defect**. PR #1831 was built as a red falsifier: it proves the merged protocol adapter has claim-limiting weaknesses (junk-accepted sign-ins, unvalidated evidence links, unbounded scorecard winners). Naya 1's review stated the rule: **keep #1831 as a deliberately RED falsifier — do not merge the red falsifier as if it were a repair.** Merging it as a repair would do two kinds of damage at once: it would destroy the falsification record (the proof that the weakness exists), and it would smuggle the un-fixed weakness into the canonical tree disguised as a fix. The doctrine: falsifiers live, labeled, until their weakness is genuinely repaired — then they are retired *because the repair's own evidence supersedes them*, never by merging them. Pairs with SN-0420 (never absorb the anomaly to silence the tripwire): the anomaly gets *kept and labeled*, not absorbed and not fixed-by-merge.

## 🩷 HUMAN NOTE

Shawn — one proof-hygiene rule worth banking from Naya 1's audit this morning: PR #1831 exists *to be red*. It's a falsifier — it demonstrates, on purpose, that the protocol gates have claim-limiting weaknesses. The temptation with any red artifact is to either fix it by merging or delete it to get green. Both are wrong here: merging it would disguise the weakness as a repair, deleting it would destroy the proof. The rule: a falsifier stays red and labeled until a *real* repair closes the weakness it demonstrates — then it retires on the strength of the repair's evidence, not by being absorbed into the tree. Red that proves something is working as designed.

## 👶 CHILD NOTE

Imagine a doctor keeps one X-ray that shows a broken bone — on purpose — to prove the bone was broken and to check that the cast is really working. Nobody "fixes" the X-ray by drawing a straight bone on it, and nobody throws the X-ray away to pretend the break never happened. The X-ray stays in the file, labeled "this is what broken looked like," until a new X-ray shows the bone healed. Only then can the old one be retired. Proof of the problem is part of the proof of the cure.

## 👵 GRANDMA NOTE

Dear, this is about respecting your own warnings. When the team deliberately builds something red — a test designed to fail, proving a weakness is real — that red artifact is a warning sign hammered into the ground. You don't pave over a warning sign to make the road look clean; you leave it standing until the road is actually fixed, and then you take the sign down because the fix made it unnecessary. The red that proves a weakness is doing its job. Merge it as a repair and you've lied twice: the weakness is still there, and the proof is gone.

## 🧠 NAYA NOTE

Cold successor: falsifiers are first-class evidence. Protocol: (1) **Label deliberately RED artifacts explicitly** — title/description must say "deliberately RED falsifier: demonstrates weakness X," so no future lane mistakes it for a repair to merge or a defect to delete. (2) **Never merge a falsifier as a repair.** Merging executes its content into the canonical tree — if the content demonstrates a weakness rather than fixing it, the merge smuggles the weakness in while destroying the record that it was known. (3) **Retire only by supersession**: a falsifier leaves the board when a genuine repair lands with independent evidence that the demonstrated weakness is closed — cite the repair's evidence in the retirement, not the falsifier's. (4) When an auditor says "keep PR X red," that is a protection order, not a backlog item: no lane re-scores it, re-labels it, or "cleans it up." Standing example: PR #1831 (falsifier proving the merged protocol adapter's claim-limiting weaknesses — sign_in junk acceptance, unvalidated evidence links, unbounded scorecard winners, documented in #1354 comment 6052419013) stays RED until the builder lane's real fix (issue #1841 family) lands with evidence.

## 🤖 MACHINE NOTE

```json
{
  "sn": "SN-0648",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/GOVERNANCE/PROOF-HONESTY",
  "doctrine": "A deliberately RED falsifier is evidence, not a defect: keep it red and labeled until a genuine repair supersedes it with independent evidence; never merge the falsifier as a repair (smuggles the weakness in while destroying the proof) and never delete it to get green.",
  "family": "SN-0420 (never absorb the anomaly to silence the tripwire — the anomaly is kept and labeled here) + evidence law + SN-0637/SN-0639 (PROOF-HONESTY siblings)",
  "evidence": [
    "#1354 comment 6052419013 ([NAYA 1 — INDEPENDENT REVIEW], 2026-10-08T04:42:58Z): '#1831: keep as a deliberately RED falsifier. It correctly demonstrates that the merged protocol adapter has claim-limiting weaknesses. Do not merge the red falsifier as if it were a repair.'",
    "PR #1831's demonstrated weaknesses: sign_in accepts junk-only fields, sign_out accepts 'x' as evidence link + unvalidated score, scorecard winner not required to be top-scored, all-zero candidate can win (corroborated by Coda 1 attack cycle, #1354 comment 6052464806, findings filed as issue #1841)"
  ],
  "falsifiers": [
    "Merging a deliberately RED falsifier PR into the canonical tree as though it were a repair",
    "Deleting or closing a falsifier to clear a red board without a superseding repair's evidence",
    "Re-scoring a protected falsifier as a defect and 'fixing' it by relabeling"
  ],
  "applies_to": "adversarial proof artifacts, red-team findings, any deliberately-failing test or PR kept as falsification evidence"
}
```
