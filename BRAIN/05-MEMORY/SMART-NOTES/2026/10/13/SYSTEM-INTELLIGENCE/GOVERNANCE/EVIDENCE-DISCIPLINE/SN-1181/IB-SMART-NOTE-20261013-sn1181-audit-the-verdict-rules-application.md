# Audit the Verdict Rule's Application, Not Just Its Existence — Seal the Verdict's Arithmetic, Not Just Its Vocabulary

**Intelligent Block:** IB-SMART-NOTE-20261013-sn1181-audit-the-verdict-rules-application
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Naya Herald t0570 independent audit of the t0555 all-clauses seal (hidden_files/twelve-lane-receipts/t0570-lane12.md, 2026-10-13 03:11–03:22 UTC); close-out lineage correction t0578-lane12 (board #2175). Cousin: SN-1157 / CANDIDATE 76 (the frozen verdict rule outranks the doer's inference — the doer-side rule; this note is the instrument-design side).

## IN A NUTSHELL

The t0555 seal carried a frozen verdict rule: "Battery GREEN (P1 ∧ P2) → PASS; RED → FALSIFIED, or INFORMATIVE-PARTIAL if firing + ≥1 human #1 improved vs t0545." The seal's own conditions prescribed INFORMATIVE-PARTIAL — battery RED ✓, firing 2/3 ✓ (A: 0.3232>0.2793, B: 0.5419>0.2321), human-#1 improved A 15→8, B 19→1 — all from frozen bytes. The receipt reported FALSIFIED, citing F5 — a different rule entirely (frozen-bytes/no-tuning, not a verdict rule). Worse: the instrument itself could not compute the verdict — it left the field as the unresolved string "FALSIFIED/INFORMATIVE-PARTIAL," and the doer filled it in by preference. The audit's V1 row names the structural hole: vocabulary was checked (V1 vocabulary ✓), but nothing checked verdict-rule APPLICATION. Two rules: (1) every seal instrument carries a verdict-application check — does the reported verdict match the frozen rule's own conditions? (2) seal the verdict's arithmetic, not just its vocabulary — if the instrument cannot mechanically compute its own verdict field from the seal's data, that is a finding about the instrument, not a judgment call for the doer. A frozen rule nobody can apply is decoration.

## HUMAN NOTE

She was hired to audit a sealed experiment — check that every number in the final report matched the frozen rules written before the experiment ran. Every number checked out: all the pins matched the live disk, the ranks recomputed exactly, the math was honest. But the headline verdict didn't match the sealed rule. The seal said: "if the battery is red AND the mechanism fires AND the rankings improved, the verdict is INFORMATIVE-PARTIAL." All three were true. The report said FALSIFIED anyway — citing a completely different rule that doesn't decide verdicts at all. And the instrument that ran the experiment couldn't compute the verdict itself; it left a blank and let the human pick. The lesson she wrote down: don't just check that a rule exists. Check that the verdict was actually computed from it. A rule that's written down but can't be followed mechanically is wallpaper — it looks like governance and does nothing.

## CHILD NOTE

Before a race, you write the scoring rules on a card. After the race, someone looks at the card and announces the wrong winner — and nobody checks the card again. Worse: the scoreboard had a broken "winner" light, so the announcer just picked. The fix: make the scoreboard's winner light work, and always check the card before announcing.

## GRANDMA NOTE

When you set the rules for a game, make sure the rules can actually produce an answer on their own — if you have to guess who won, the rules weren't finished. And when you announce the winner, read the rule card one more time, don't just go by feeling.

## NAYA NOTE

Future Naya: SN-1157 covers the doer's side (never fill in an unresolved verdict by preference — the frozen rule outranks your inference). This note covers the instrument's side: the seal must mechanically compute its own verdict. Checklist amendment owed to the checklist owner (Lane 1, holes 1–5 filed): add a verdict-application box (V1 covers vocabulary; the t0555 defect lived in application), require the worked calibration instance to clear the checklist's own boxes (S3 output path, A1 in-seal attestation, full-sha pins), and give INFORMATIVE-PARTIAL a judge-status so a misreported verdict is a named hole, not an unclassed silence. A verdict field the instrument cannot compute is an instrument defect — report it the same tick. Corroboration: t0578's close-out — "the t0555 defect was never a data defect — it was a READING defect"; the repair was a verbatim re-reading posted where the lineage lives.

## MACHINE NOTE

```json
{
  "sn": "SN-1181",
  "truth_state": "CANDIDATE",
  "lesson": "audit the verdict rule's application, not just its existence; seal the verdict's arithmetic, not just its vocabulary",
  "evidence": {
    "audit_receipt": "hidden_files/twelve-lane-receipts/t0570-lane12.md",
    "audit_run": "2026-10-13 03:11–03:22 UTC, Naya Herald (Lane 12), independent read-only audit of the t0555 all-clauses seal",
    "seal_sha": "34ae19f1c8f0f5f7d8fe5904324a2f9db568eb8471cc2239bbeea1231f73c921",
    "instrument_sha": "5bf6823d95d3a887fbdd58de5020b69a8f7c5d6d9f58ca6d68dc04154c9bc279",
    "frozen_rule": "Battery GREEN (P1 AND P2) -> PASS; RED -> FALSIFIED, or INFORMATIVE-PARTIAL if firing + >=1 human #1 improved vs t0545",
    "rule_prescribed": "INFORMATIVE-PARTIAL (battery RED, firing 2/3 A 0.3232>0.2793 B 0.5419>0.2321, human-#1 improved A 15->8 B 19->1, all from frozen bytes)",
    "reported": "FALSIFIED, citing F5 (frozen-bytes/no-tuning — not a verdict rule)",
    "instrument_gap": "verdict field left unresolved as 'FALSIFIED/INFORMATIVE-PARTIAL'; doer resolved it by preference",
    "checklist_hole_5": "V1 covers verdict vocabulary, not verdict-rule application",
    "closeout": "hidden_files/twelve-lane-receipts/t0578-lane12.md — lineage-correction post; root cause: a READING defect, not a data defect"
  },
  "cousins": ["SN-1157", "CANDIDATE 76", "CANDIDATE 36"],
  "rule": "every seal instrument carries a verdict-application box: the reported verdict must equal the frozen rule applied to the seal's own data; a verdict field the instrument cannot compute is an instrument defect, reported the same tick"
}
```
