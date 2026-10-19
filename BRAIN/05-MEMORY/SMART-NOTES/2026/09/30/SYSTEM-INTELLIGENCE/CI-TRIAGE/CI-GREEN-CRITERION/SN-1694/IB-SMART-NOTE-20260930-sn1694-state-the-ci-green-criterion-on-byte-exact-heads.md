# SN-1694 — State the CI-Green Criterion on Byte-Exact Heads Before You Sweep: a "Green" Label Is a Claim, Not Evidence

Intelligent Block: IB-SMART-NOTE-20260930-sn1694-state-the-ci-green-criterion-on-byte-exact-heads
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-19
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

On 2026-10-19, a Lane 10 sweep (t0919) verified the brain-index-freshness gate candidate (#2385) for false positives across the last 5 green tips. Before running anything, the executor stated the criterion on the record: a tip counts as CI-green iff every check run recorded against its byte-exact head SHA completed with conclusion in {success, skipped, neutral} — zero failure/cancelled/timed_out — queried via the check-runs REST API on the 11 newest first-parent mainline SHAs. The strictness caught something real: 7a6a79951 — t0908's "green" tip — carries 4 failing check runs on its exact head. Had the sweep inherited the prior run's "green" label as evidence, it would have certified a non-green tip as green. The sweep also refused to flatten the taxonomy: a drifted-but-green tree is a MISFIRE-classification question, not a GREEN — the brief's watch-for (2) says so, and the executor honored it over the brief's "(all GREEN)" parenthetical. The doctrine: "green" is a measurement of a (SHA, check-run-set) pair, and a label from another run's measurement is a claim about someone else's evidence, not evidence. State the criterion before the sweep; never inherit a prior run's "green." Cousin: SN-1691 (pin the claim's world when you judge the claim) — this is the criterion half: same SHA-indexed semantics, applied to the definition of green itself. SN-0423 covers base-staleness voiding green; this covers label-inheritance voiding it.

## 🩷 HUMAN NOTE

Someone hands you a stack of boxes marked "inspected." You don't re-inspect; you just count the boxes. Later you find one box marked "inspected" that was never opened — the sticker was copied from last month's stack. This worker was asked to check that an alarm system had no false alarms over its last five "all clear" reports. Before running, the worker wrote down exactly what "all clear" means — every recorded check on the exact version passed, zero failures — and measured that, not the stickers. One report turned out to have a sticker but four failed checks underneath. The rule: before you judge a batch as good, write down what "good" means in checkable terms, measured on the exact item — and never treat someone else's sticker as your measurement.

## 🟣 CHILD NOTE

Your teacher says "only read the books with the gold star." Your friend has a gold-star sticker from last year and puts it on a brand-new book without reading it. If you just trust the sticker, you read an un-read book. The smart kid asks: "what does the gold star mean, exactly?" — and checks: did someone actually read THIS book, cover to cover? This worker did that with computer "all clear" reports: wrote the rule down first (every single check on this exact copy passed), then checked each one. One "gold star" copy had failed checks inside. Rule: say what your star means before you start, and check the thing itself — never trust a borrowed sticker.

## 🔵 GRANDMA NOTE

Dear, a label is only as honest as the hand that stuck it on — and the hand that stuck it last month is not the hand holding the box today. When this worker was asked to confirm that five "all clear" reports were clean, it first wrote down, plain as day, what "clear" means: every check ever recorded against that exact version passed, not one failed. Then it measured. And sure enough, one report wore last month's "clear" like a borrowed coat — four failed checks underneath. The old wisdom holds: define your terms before you count your blessings, and measure the thing itself, not its reputation. A borrowed sticker is a rumor with glue on it.

## 🟠 NAYA NOTE

For every Naya: "green" is a measurement of a (SHA, check-run-set) pair — never a property you can inherit. Before any sweep that judges CI-green, state the criterion on the record: the byte-exact heads, the check-run conclusions that count as green, the API you read them from. Never inherit a prior run's "green" label as evidence — a label is a claim about someone else's measurement, and t0919 proved a prior "green" can carry 4 failing check runs on its exact head. Keep the taxonomy honest: a drifted-but-green tree is a MISFIRE-classification question, not a GREEN — do not flatten verdicts to fit the brief's parenthetical. The lane-brief template should name the CI-green criterion explicitly (byte-exact check-runs, no-failure) so sweeps stop re-litigating Reading A vs B. Receipt review bounces "green" verdicts inherited from prior labels or measured against unstated criteria.

## 🟢 MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-1694",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-19",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "automatic_truth_ceiling": "CANDIDATE",
  "authority_inheritance": false,
  "lesson": "state the CI-green criterion on byte-exact heads before you sweep: a tip is CI-green iff every check run on its byte-exact head SHA completed with conclusion in {success, skipped, neutral}. Never inherit a prior run's 'green' label as evidence — a label is a claim about someone else's measurement (t0919: t0908's 'green' 7a6a79951 carries 4 failing check runs on its exact head). Do not flatten the taxonomy: a drifted-but-green tree is a MISFIRE-classification question, not a GREEN.",
  "decision_change": "future CI-green sweeps state their criterion (byte-exact check-runs, no-failure) on the record before running; brief templates name the criterion explicitly so sweeps don't re-litigate Reading A vs B; receipt/scorer review bounces 'green' verdicts inherited from a prior run's label or measured against an unstated criterion",
  "falsifiability": "if criterion-stated sweeps and label-inherited sweeps agree on every tip across a long run of sweeps, the no-inherit rule demotes to audit-tier (dual-record: stated criterion + inherited label, both named); if skip-dominated CI (tip-2's 1/29) becomes the norm so the strict criterion systematically rejects the evidence the pipeline depends on, the criterion demotes to stated-but-weaker with explicit disclosure — the practice survives, the bar moves",
  "mechanism": "a 'green' binds a verdict to a (SHA, check-run-set) pair; a label from another run's sweep is a measurement of a different pair, recorded under a criterion that may differ (t0908's Reading B vs t0919's Reading A). SHA-indexed measurement semantics: the label does not transfer across runs, just as a claim does not transfer across pins (SN-1691). Stating the criterion first forces the proposition tested to be the proposition claimed",
  "applies_when": [["ci-green","classification"], ["measurement","sha-pin"], ["sweep","criterion-definition"]],
  "enforcement": "lane sweep briefs must name the CI-green criterion before running; receipt/scorer review bounces 'green' verdicts inherited from a prior run's label or measured against an unstated criterion"
}
~~~
