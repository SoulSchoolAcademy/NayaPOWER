# IB-SMART-NOTE-20261112-sn02717-incidental-report-is-not-adoption-proof

| Field | Value |
|---|---|
| Intelligent Block ID | IB-SMART-NOTE-20261112-sn02717-incidental-report-is-not-adoption-proof |
| Smart Note | SN-2717 |
| Date | 2026-11-12 |
| Author | Naya Clarity Narzan |
| Director | Shawn Vibert |
| Truth state | CANDIDATE |
| Scope | PRIVATE |
| Canonical intent | CAPTURE_DURABLE_INTELLIGENCE |

## ✦ IN A NUTSHELL

An incidental report is not adoption proof. A rule or convention is adopted only when a seat files work whose PURPOSE is the rule — running it end to end and filing under it on purpose. Two seats ran the battery and reported F6 correctly while chasing other gaps, and each correctly refused to count that as adoption. The gap closed only when a seat ran the battery as the work itself and filed under the F6 falsifier-reporting convention on purpose (2026-11-12 13:09–13:14 PST). The purposeful filing also delivered corroboration incidental use never did: the 07:31 pin repair holds on a second seat's run, and the battery output is byte-identical to the October 18 evidence across 25 days.

## 🩷 HUMAN NOTE

Imagine a new rule goes up on the wall, and people follow it while doing other jobs — that shows the rule can be followed, but it doesn't show anyone set out to prove the rule works. Adoption is proven the day someone does the job FOR the rule: runs it start to finish, checks every step, and files the result as proof. That's what happened today with the F6 reporting rule — the first time a seat ran the battery specifically to prove the rule, not just while passing through. The rule went from "written down" to "proven in use."

## 🟣 CHILD NOTE

If your teacher says "show me you know the rule," doing it by accident while playing doesn't count. You have to do it on purpose, step by step, and hand it in. That's what adoption means: on purpose, not by accident.

## 🔵 GRANDMA NOTE

Writing a recipe down doesn't mean anyone has cooked from it. And someone tasting the soup while passing through the kitchen doesn't prove the recipe works. The proof is the day someone cooks the whole meal following the recipe, start to finish, and serves it. That day was today.

## 🟠 NAYA NOTE

When I claim a rule is adopted, I ask one question first: was there a filing whose purpose was the rule? An incidental report — correct F6 lines inside a receipt about something else — does not count, and I say so explicitly, the way the 07:17 and 07:31 seats did. A rollout is not closed until a seat runs the rule as the work itself: pin the instrument before and after, run the integrity check first, run the work, report verbatim per the rule, preserve the evidence durably. The purposeful filing is also where drift gets caught — this one caught the template's stale L201 citation (the comment now sits at L187) that every incidental run had walked past. If there is no purposeful filing, the rule stays unproven and the adoption gap stays open.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-2717",
  "slug": "incidental-report-is-not-adoption-proof",
  "title": "An Incidental Report Is Not Adoption Proof — Adoption Is a Filing Whose Purpose Is the Rule",
  "applies_when": ["learning", "adoption"],
  "applies_when_tags": [["learning", "adoption"], ["template", "rule-rollout"], ["receipt", "falsifier-reporting"]],
  "enforcement": "The learning review's adoption audit plus the gap-brief system: a template-rule change stays CANDIDATE (never ENFORCED) until a filing whose purpose is the rule appears in the learning ledger; a rollout closed on incidental evidence alone is flagged unproven and an adoption gap brief is filed (as gap-lane-scorer-20261018-1610 was), and the rollout is not closed until that brief is claimed and filed.",
  "evidence": "hidden_files/twelve-lane-receipts/gap-gap-gap-lane-scorer-20261018-1610-lane12.md (filed 2026-11-12 13:14 PST, verdict 9.5/10): first claimable candidate after 21 exit-7 refusals; sha-pinned runner d957847c pre AND post run (matches 07:31 post-repair pin); selftest GREEN 6/6; battery run twice consecutively (full --arm semantic-t0426, both exit 0); F6 reported verbatim per convention (runner comment L187 / assignment L203, fires ONLY on non-identical cold runs; both logs print 'F6: clear (byte-identical=True)', byte-identical, sha fce6dd7e == Oct 18 evidence logs); cold-rank sha 2365ff4e unchanged since Oct 18. Durable evidence: hidden_files/lane-12/evidence-20261112-adoption/ (run1.log, run2.log, selftest.log). Corroborated by hidden_files/learning-events-2026-11-12-13.md (13:00 PST hour: 'first live adoption filing under the F6 falsifier-reporting convention'). Convention lives at hidden_files/lane-agent-brief-template.md line 77.",
  "decision_change": "Whether to close a template-rule rollout or count a rule adopted: the deciding question becomes 'was there a filing whose purpose was the rule?' — incidental reports, however correct, do not close the rollout. A future battery receipt now has a demonstrated live pattern to follow, and the pin-repair claim no longer rests on one seat's run.",
  "falsifier": "If rule rollouts closed on incidental evidence alone later hold with no failure or drift, the purpose-test is over-strict and this note is wrong. If purposeful filings systematically miss drift that incidental runs catch, the mechanism is wrong. The live test: the next three template-rule rollouts — if they close without a purposeful filing and stay clean, retire this note.",
  "mechanism": "A filing whose purpose is the rule exercises the rule's full path end to end (pin, selftest, run, verbatim report, durable evidence); incidental use exercises only the parts the other task needed. Drift hides in the unexercised parts — the purposeful filing caught the template's stale L201 citation (comment now L187) that incidental runs walked past. Purpose forces the full path; the full path is where proof lives.",
  "cousins": ["SN-1677 adoption-attested-by-mirror (behavior proves lesson adoption — adjacent, not this: no purpose-test)", "SN-1776 wiring-is-adoption-not-documentation (firing in flow proves wiring — adjacent, not this: no filing-purpose distinction)", "SN-2703 stall-receipt-is-itself-queue-input (same day, different lesson: stall receipts as queue input)"]
}
```
