Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-23
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

PR #3008 (activation-playbook procedures, merged 2026-10-23T15:50:59Z as merge 1ebcf8ae) changed a kernel-test threshold and landed WITHOUT its pinning test — kernel red grew by exactly one, caught only post-hoc by the hourly accountability tick (board #2793, comment 6370078929, 16:50Z: "a threshold fix landed WITHOUT its pinning test"). The lesson is structural, not personal: a test suite can only guard behavior it exercises. A threshold or behavior fix that lands without its pinning test in the same PR is not a fix — it is an unguarded edit. The next merge that touches that threshold re-breaks it silently, and no gate can fire because no test names the expected behavior. So the rule: the pinning test lands WITH the fix, in the same PR, or the fix does not land. The falsifier is coverage, not paperwork: a fix provably covered by an already-landed test (the regression battery already exercises the changed behavior at the new threshold) needs no new test — the bar is "the behavior is pinned," and a new test file is just the usual way to prove it. Sibling discipline: SN-1872 (cure must declare addressed failures) sets the claim bar for cures; this sets the proof bar for fixes.

## 🩷 HUMAN NOTE

Shawn — here's the simplest version. PR #3008 changed a threshold in the kernel tests and landed without any test pinning the new threshold. Kernel red grew by exactly one failure, and nobody knew until the hourly tick counted it. The tests are the only thing that keeps a fix fixed — if no test names the new expected behavior, the next merge can silently undo the fix and no gate will catch it. So the standing rule going forward: a fix and its pinning test arrive together, in the same PR. No test, no landing. The one exception is honest coverage: if an existing test already pins the changed behavior at the new threshold, the fix is already guarded — the bar is pinned behavior, not a new file.

## 🟣 CHILD NOTE

Imagine you fix a leaky faucet but you don't tell anyone how to check it's fixed. A week later someone "fixes" the pipes and the faucet leaks again — and nobody notices, because nobody wrote down what "fixed" looked like. The pinning test is the note that says "the faucet must stay dry for 10 minutes." You tape it to the fix. From now on: fix and note arrive together, or the fix doesn't go in.

## 🔵 GRANDMA NOTE

Honey, think of it like a prescription. The doctor changes your medicine, but nobody writes the new dosage on the chart. Next visit, the new nurse goes back to the old dosage — and nobody can say it was wrong, because the chart never named the new one. A pinning test is writing the new dosage on the chart, right there with the change. The fix lands with its chart note, always. That way any future change can be checked against what was decided.

## 🟠 NAYA NOTE

For the lanes: this is a landing-gate discipline, not a suggestion. Any PR that changes a threshold, a constant, a policy boundary, or observed behavior must cite its pinning test in the body — file and test id — or carry proof that an already-landed test pins the new behavior (quote the test, don't assert it). VERIFY exact-head cards must include a "pinning test" line for behavior-fix PRs. A fix PR with no named pinning test and no coverage proof is held at the gate: landing-gate breach, cure routed to the author lane. The WIRE red-watch names "fix landed without pinning test" as a breach-class delta every tick — the same way it names receipt breaches. This is the root repair of 6370078929: the red grew by one because the suite had no name for the new expectation.

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn-1882-fix-lands-with-pinning-test",
  "lesson": "A threshold or behavior fix that lands without its pinning test in the same PR is not a fix — it is an unguarded edit. The suite can only guard behavior it exercises; the next merge that touches that threshold re-breaks it silently because no test names the new expected behavior. PR #3008 (activation-playbook procedures, merged 2026-10-23T15:50:59Z as 1ebcf8ae) changed a kernel-test threshold without its pinning test; kernel red grew by exactly one, caught only post-hoc by the hourly accountability tick (board #2793, 6370078929, 16:50Z). The bar is pinned behavior, not paperwork: a fix provably covered by an already-landed test (regression battery already exercises the changed behavior at the new threshold) needs no new test. Sibling: SN-1872 (cure must declare addressed failures) sets the claim bar; this sets the proof bar.",
  "applies_when": ["fix", "threshold-change", "behavior-change", "pinning-test", "regression-guard", "landing-gate", "kernel", "pr-body"],
  "enforcement": "Any PR changing a threshold, constant, policy boundary, or observed behavior must cite its pinning test (file + test id) in the body, or quote the already-landed test that pins the new behavior — assertion is not proof. VERIFY exact-head cards carry a 'pinning test' line for behavior-fix PRs. A landing with no named pinning test and no coverage proof is a landing-gate breach: carded post-hoc at exact head and the cure routed to the author lane. The WIRE red-watch counts 'fix landed without pinning test' as a breach-class delta every tick, the same as receipt breaches.",
  "evidence": ["board #2793 comment 6370078929 (SoulSchoolAcademy hourly accountability 15:48-16:48 UTC, 2026-10-23T16:50:17Z): 'BLOCKER NOTE: kernel red grew by exactly one — a threshold fix landed WITHOUT its pinning test'", "PR #3008 merged 2026-10-23T15:50:59Z -> merge commit 1ebcf8ae (relay flagged both prongs: 0 reviews, no exact-head scorecard, 5 red gates; VERIFY carded STAND 8.5 post-hoc at exact head)", "board #2793 comment 6370261405 (learning event, 16:59Z): kernel failed at 1ebcf8ae"]
}
```

