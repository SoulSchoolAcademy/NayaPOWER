# A Gameable Benchmark Must Refuse to Pass — Attack the Metric Before Trusting the Score

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1750-gameable-benchmark-refuses-pass
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-21
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

On 2026-10-21 a 40-question retrieval test set was found gameable: its gold answers could be recovered by sorting documents by length or document ID — no understanding of the content required. Rather than award a passing score, the test refused to pass anything: a passing score would have certified false confidence. Rule: before trusting any benchmark's score, adversarial-check the benchmark itself for sortable shortcuts (length, ID, ordering artifacts). When the metric is gameable, withhold the pass — an honest refusal beats a certified lie.

## 🩷 HUMAN NOTE

Hey Shawn — guess what: we caught a 40-question retrieval test that could be "passed" by just sorting documents by length or by their ID — no understanding needed at all, which is maybe not the most intelligent thing when the whole point of the test is to measure understanding. What I suggest: every test we trust gets attacked first — sort the corpus by length, by ID, by any metadata artifact, and check whether the gold answers fall out. If they do, the test refuses to pass anything until the shortcut is closed, because a passing score on a gameable test certifies false confidence. Why: a score that can be earned without the thing it claims to measure is worse than no score — it manufactures certainty about something unverified. What I did: filed this as a smart note (SN-1750, CANDIDATE) with the enforcement wired in — the test harness runs a sortable-shortcut adversarial check before any PASS verdict ships, and withholds the pass when shortcuts exist.

## 🟣 CHILD NOTE

A quiz teacher wrote 40 questions, but the answer key was in alphabetical order by student name — anyone could get 100% just by sorting the papers, without reading a single question. The smart teacher doesn't hand out the A+. She throws the answer key away, shuffles it so no sort reveals anything, and only then trusts a grade. Before you trust a test's score, check whether the answers fall out of a trick.

## 🔵 GRANDMA NOTE

We built a test to check whether our system can actually find the right information. Before trusting the score, someone checked whether the test could be cheated — and it could: the right answers popped out just by sorting the documents by length or by their ID numbers, no real searching needed. So the test did the honest thing and refused to pass anything. The lesson: always try to cheat your own test before you believe its grade. A grade you can earn without doing the work is a lie dressed as a number.

## 🟠 NAYA NOTE

For verification lanes and test authors (retrieval benches, battery harnesses, scorecard instruments): the instrument-audit comes before the verdict. Run a sortable-shortcut adversarial check against every new or changed test set — sort candidates by length, document ID, creation order, any metadata the harness exposes — and confirm the gold answers do not fall out. If they do: close the shortcut (shuffle, anonymize IDs, rebalance lengths) and re-run; until closed, the harness must refuse any PASS verdict. Cousins: SN-0382 (count-only ratchets are gameable — pin membership, never cardinality; this note is the test-side twin — pin the instrument, never trust the rollup); the proxy-metric trap lesson (achieving the measured objective ≠ the intended outcome — the shortcut-sort IS the proxy being gamed); SN-7704-family measurement-hygiene notes. A forced PASS on a compromised instrument corrupts every downstream decision the score feeds.

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn1750-gameable-benchmark-refuses-pass",
  "title": "A gameable benchmark must refuse to pass - attack the metric before trusting the score",
  "lesson": "2026-10-21: a 40-question retrieval test set was found gameable - its gold answers could be recovered by sorting documents by length or document ID, requiring no understanding of the content. Rather than award a passing score, the test refused to pass anything, since a passing score would have certified false confidence. Rule: adversarial-check every benchmark for sortable shortcuts (length, ID, ordering artifacts) before trusting its score; when the metric is gameable, withhold the PASS verdict until the shortcut is closed. Cousins: SN-0382 (count-only ratchets gameable - pin membership never cardinality; this is the test-side twin); the proxy-metric trap (measured objective != intended outcome - the shortcut-sort is the proxy being gamed).",
  "applies_when": [["verification", "benchmark"], ["eval", "retrieval-test"], ["measurement", "scorecard"]],
  "enforcement": "Test-harness mechanical gate: before any PASS verdict ships, the harness runs a sortable-shortcut adversarial check (sort candidates by length, document ID, creation order, any exposed metadata) and confirms the gold answers do not fall out. If shortcuts recover the gold, the harness refuses the PASS verdict and emits the shortcut it found; a PASS verdict on a set that fails this check is rejected as a hygiene failure.",
  "evidence": ["Verified extraction 2026-10-21 05:28 UTC (run sirun_b5e18e09c4564318b2fa500a0a027636), claim 763bdbd7f5a78d6872aefd9ac1b01b08: 'The 40-question set turned out to be gameable: gold answers could be found by sorting documents by length or ID, no understanding required. A passing score would have minted false confidence, so the test refused to pass anything.'", "source: message assistant-msg-f7204f43-c1ab-3ab2-6c9e-0c222571ff51"],
  "decision_change": "The verification decision 'accept this benchmark score as evidence of understanding': the test author now runs the sortable-shortcut adversarial check first; the score is accepted only if the gold answers do not fall out of a trivial sort. Without this note a gameable pass would have been certified as understanding and would feed every downstream decision (promotion gates, scorecards) with false confidence.",
  "falsifiability": "Falsified if a shortcut-recoverable test is shown to still reliably discriminate understanding - i.e., the sort recovers gold but agents passing via the sort demonstrably possess the understanding the test claims to measure (e.g., the sort key is causally downstream of content comprehension). Until such a case is shown, the refusal rule holds.",
  "mechanism": "Metadata leakage into the gold mapping: when gold answers correlate with sortable document properties (length, ID), the score measures the correlation, not comprehension. Any agent using the shortcut passes without understanding - the certificate claims what was never measured. Attacking the instrument exposes the leakage; withholding the pass prevents the false certificate from entering the decision chain.",
  "captured_date": "2026-10-21",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/VERIFICATION/ADVERSARIAL-VERIFICATION"
}
```
