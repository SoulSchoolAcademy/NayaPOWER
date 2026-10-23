Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-23
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

#2746 was merged 2026-10-21 on red CI with no repair blocks present — and the landing stood until the director's Kappa adjudication (comment 6360287869) classified it: it fails condition 1 of the five-rule merge conditions, making it a BYPASS, not a pass. The ruling names the failure class **RED-CI LANDING**: a landing that reaches main while the CI verdict surface says red and no repair blocks carry it. The landing path read its own instruction stream but never re-checked the gate's verdict surface at the moment of landing — the W704 family root (SN-1829) in CI-verdict form. The durable rule: **a red-CI landing with repair blocks absent is classified RED-CI LANDING and routed to dock remediation, never re-litigated.** The dock owes remediation, and the bypass is relay-appended to the PR's record so the class accumulates evidence instead of excuses. Cousin SN-0578 names the consequence (a red-CI merge converts the red into a base defect); this note names the classification and the standing remediation duty.

## 🩷 HUMAN NOTE

Shawn — a pull request landed on red CI with no repair work covering the red, and it looked like a normal merge until Kappa's verdict and the director's adjudication confirmed it: it fails the first merge rule, so it's a bypass, not a pass. The landing was never authorized on that basis — the merge machinery just never re-checked the CI verdict before landing. We've named the class RED-CI LANDING so the next one is classified on sight and the merge dock owns the remediation — relayed onto the record, fixed by the dock, no fresh debate each time.

## 🟣 CHILD NOTE

Imagine a school race where you can only finish if the judges' flag is green — red flag means a judge has to walk the track with you (a repair). One runner crossed the line on a red flag with no judge, and everyone wrote it down as a normal finish. Later someone checked the flag book: red flag + no judge = not a finish. The rule: red-flag finishes without a judge get a special name, and the race committee has to fix the record — we don't argue about it every time.

## 🔵 GRANDMA NOTE

It's like a building that passes inspection only with a green tag — or a red tag with the repairs signed off. A tenant moved in with a red tag and no signed repairs, and the front desk logged it as a normal move-in. Weeks later the inspector checked: red tag, no sign-off, so the move-in was never authorized. From now on that situation has a name — RED-CI LANDING — and when it happens the front desk is responsible for fixing the record, not for deciding whether it really counts.

## 🟠 NAYA NOTE

This is SN-1829's root wearing the CI verdict's face. SN-1829 said a bot merge must consult the hold registry because the merge path reads only its own instruction stream. #2746's landing did the same thing one surface over: it read its own landing instructions and never re-consulted the CI verdict surface at the moment of landing — red CI, repair blocks absent, landed anyway. The adjudication (Kappa lane-5 W704-class verdict 6360287869, confirmed in the director pass) closed the loop the landing skipped: condition 1 of the five-rule fails, so the landing is a bypass. The classification is load-bearing because it settles two things without re-litigation: (1) the landing never satisfied the merge conditions, so it is not a pass with an asterisk — it is a bypass; (2) the merge dock owes remediation, relay-appended to the PR record, so evidence accumulates in one place. The machine truth: verdict surfaces (CI state, hold records) must be consulted AT LANDING, not at briefing time — anything consulted earlier has rotted by merge time. Cousins: SN-1829 (hold-registry consultation), SN-0578 (consequence classification of red-CI merges — the base-defect conversion); this note is the classification-and-remediation-routing member of the family.

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn-1867-red-ci-landing-bypass",
  "lesson": "A landing that reaches main on red CI with repair blocks absent is classified RED-CI LANDING: it fails five-rule merge condition 1, so it is a bypass, not a pass. #2746 merged 2026-10-21 on red CI with no repair blocks; Kappa lane-5 W704-class adjudication 6360287869 confirmed the bypass. The landing path read only its own instruction stream and never re-checked the CI verdict surface at landing (W704-family root, cf SN-1829). The classification routes remediation: the merge dock owes remediation, relay-appended to the PR record, instead of re-litigating the landing each time.",
  "applies_when": ["merge", "landing", "ci-verdict", "red-ci", "bypass", "five-rule"],
  "enforcement": "Landing verification's five-rule merge-condition check (condition 1: CI green OR repair blocks present) re-verified AT LANDING against the live CI verdict surface — not at briefing/claim time. A red-CI landing with repair blocks absent is classified RED-CI LANDING, relay-appended to the PR record, and routed to the merge dock for remediation (dock bypass register). Observed instance: #2746 adjudication 6360287869 (2026-10-21 landing, confirmed 2026-10-23 director pass).",
  "evidence": [
    "Kappa lane-5 W704-class adjudication 6360287869 on board #2793: #2746 merged 2026-10-21 on red CI with repair blocks absent, fails five-rule condition 1 -> BYPASS CONFIRMED",
    "director pass t20261023-0908 (2026-10-23 02:08-02:15 PDT): bypass relay-appended, merge dock owes remediation; new named failure mode RED-CI LANDING",
    "memory log ~/memory/2026-10-23.md director-pass entry (02:08-02:15 PDT window)",
    "cousins: SN-0578 (red-CI consequence classification), SN-1829 (hold-registry consultation root)"
  ]
}
```
