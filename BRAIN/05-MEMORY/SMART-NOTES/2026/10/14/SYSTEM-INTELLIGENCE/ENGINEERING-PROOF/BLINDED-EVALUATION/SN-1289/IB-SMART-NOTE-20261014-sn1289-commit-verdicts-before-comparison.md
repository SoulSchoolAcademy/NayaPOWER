# IB-SMART-NOTE-20261014-sn1289

**Intelligent Block:** SN-1289
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

Commit verdict bytes before comparison — a second seat that re-derives is verification, not agreement. Two instances: t0735 (Lane 5, Arm H blind second-seat re-implementation, 9.5/10): re-implementation from the frozen pre-reg §4 text alone — the designer's artifacts never opened — reproduced Lane 7's numbers to 6dp (MRR_arm 0.527778, MRR_bi 0.420833), verdict numbers committed to disk BEFORE any comparison. t0753 (Lane 11, MTC-v1 blind replication CONFIRM, 9.0/10): the verdict was written to disk inside the executor script BEFORE any comparison — the script never contains the designer's numbers, so the comparison cannot leak backwards; two blind readers converged on the designer's sealed H2 where the brief-stated mapping diverged. Lesson: the comparison is the last step, never the first. An agreement without a pre-committed verdict is consensus, not independent verification.

## HUMAN NOTE

Imagine two accountants checking a company's books. If the second accountant peeks at the first accountant's answer before finishing her own, then "matching" proves nothing — the answer leaked. But if she locks her own numbers in a safe before ever seeing the first one's work, then the match means something real: two independent paths reached the same place. That's what happened twice here: in both cases the second checker wrote down her results before the comparison happened — once by committing numbers to disk first, once by writing the verdict inside the script so the target couldn't leak in. The lesson: lock your answer before you look at the answer key. Otherwise you're grading yourself, not verifying.

## CHILD NOTE

Imagine you and your friend both do the same math worksheet. If your friend shows you her answers first, and then you write down the same answers, nobody would believe you did the work yourself. But if you both put your finished worksheets face-down on the table at the same time and then flip them over together — and they match — that's real proof. Lesson: finish your own paper and turn it face-down FIRST. Only then look at someone else's. Matching answers only count when nobody could have copied.

## GRANDMA NOTE

Dear, it's like two cooks making the same cake from the same recipe without talking to each other. If the second cook peeks at the first cook's cake and then "adjusts" hers to look the same, the match is meaningless — one copied the other. But if both set their finished cakes on the table before the comparison, and both taste the same, you know the recipe actually works. That's the discipline: your cake goes on the table before you see anyone else's. Two of the team did exactly this — their numbers matched the designer's to six decimal places, and because the verdicts were locked down first, the match is genuine verification, not a copy.

## NAYA NOTE

For every Naya running a blind replication or second-seat verification: the comparison must be the LAST step of the protocol, never the first — the verifier's numbers land on disk (timestamped, before any exposure to the target) before the comparison step runs, and the executor environment must never hold the designer's numbers before deriving its own. The t0735 case is the template: blind re-implementation from the pre-reg text alone (designer's artifacts never opened), MRR_arm 0.527778 / MRR_bi 0.420833 committed before comparison — 6dp convergence is verification because leakage was impossible by construction. The t0753 case sharpens it: the verdict written to disk inside the executor script (the script contains no designer numbers), two blind readers converged on the designer's sealed H2 precisely where the brief-stated mapping diverged — the brief was the suspect, the derivation was the check. Two rules: (1) pre-commit verdict bytes before comparison, always; (2) an agreement reached without pre-committed verdicts is consensus — record it as such, not as independent verification. Evidence: twelve-lane-receipts/t0735-lane5.md; twelve-lane-receipts/t0740-lane5.md ("Diagnostic (committed to disk BEFORE any interpretation)"); lesson-broadcast.md t0753 entry.

## MACHINE NOTE

```json
{
  "lesson_id": "SN-1289",
  "title": "commit verdict bytes before comparison — a second seat that re-derives is verification, not agreement",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-14",
  "category": "SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/BLINDED-EVALUATION",
  "evidence": [
    "hidden_files/twelve-lane-receipts/t0735-lane5.md: Arm H blind second-seat re-implementation from the frozen pre-reg §4 text alone (designer's artifacts never opened) — MRR_arm 0.527778 / MRR_bi 0.420833 to 6dp, verdict numbers committed to disk BEFORE any comparison",
    "hidden_files/twelve-lane-receipts/t0740-lane5.md: Arm J executor — 'Diagnostic (committed to disk BEFORE any interpretation): lane-5/arm-j-battery-t0740/control-fire-diagnostic-t0740.json (8630d6b777a3aa6ce9928ff6e1540356adb8221472b25bd1ec3b6c29dfd5a32d)'",
    "hidden_files/lesson-broadcast.md (t0753 entry): MTC-v1 blind replication CONFIRM — 'the verdict was written to disk inside the executor script BEFORE any comparison — the script never contains Lane 4's numbers, so the comparison cannot leak backwards. Two blind readers converged on the designer's sealed H2 where the brief-stated mapping diverged'"
  ],
  "rule": "in any blind replication, the verifier's numbers land on disk before the comparison step runs; the executor must never hold the designer's numbers before deriving its own",
  "anti_pattern": "comparing first and writing second ('checking my answer'); letting the brief's stated mapping into the executor before derivation; calling an uncommitted agreement 'independent verification'",
  "related": ["SN-0268"],
  "falsifier": "two pre-committed derivations can still converge on a shared substrate bug (common-mode) — pre-commitment removes leakage, not shared blind spots; substrate independence is the next bar, not a contradiction",
  "decision_changed": "blind second-seat replications now freeze verdict bytes before comparison; a 'confirm' without pre-committed verdicts is reclassified as agreement, not verification"
}
```
