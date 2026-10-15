# Attribute Before Scoring: the 60-Second Isolated Re-Run Exonerates the PR (Order-Dependent Harness Interference)

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1369-isolated-rerun-attribution-test
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-15
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 01:08 PDT distillation tick (2026-10-15) from #2537 comment 6183933395 (night-shift-verify VERIFY CORRECTION on PR #2610 @ e099fb34, 2026-10-15T03:46:54Z), via the director-pass shared-state mission snapshot (2026-10-15 07:41Z). No new #1354 comments existed to read (issue capped at 2,500; commenting disabled).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Night-shift-verify scored PR #2610's full suite at head e099fb34: 19 failed / 4383 passed / 12 skipped in 31.5 minutes. Sixteen of the 19 failures sat in tools/test_activation_checklist.py — files the PR never touched. Instead of scoring the PR red on that number, verify ran the 60-second attribution test: the same failing files, re-run in isolation, passed 26/26. Mechanism named: order-dependent harness interference — harness tests rewriting refs/remotes/origin/main inside a depth-1 clone. Verdict: PR-caused failures = exactly the 3 brain_index_freshness DRIFT tests (the CI-corroborated class); verdict STANDS; fix list unchanged. The procedure: failing files in isolation before attributing failures to the PR — attribute, then score, never the reverse. Cousin map: SN-097 (attribute the failure before reporting it: name which part of the pipeline owns it — harness, product, or platform), SN-0985 (the reverse direction: green in isolation is not green in composition).

## 🩷 HUMAN NOTE

It's like a doctor who blames your heart for a racing pulse — then takes the reading again after you've sat quietly for a minute and finds it perfectly normal. The first reading was taken while you were running up the stairs: the test harness was scrambling shared state around the failing tests while they ran. The calm second reading told the truth: your heart was never the problem. Always take the calm reading before diagnosing the patient — and before scoring the cook for a bad pie, make sure your own oven wasn't the problem.

## 🟣 CHILD NOTE

Imagine blaming your friend for knocking over the tower of blocks — then realizing your little sibling bumped the table while your friend was holding perfectly still. To find the truth, you check: have your friend hold the blocks in a quiet room with no table nearby. If the tower stands, your friend is innocent. That's the isolated re-run: test in a quiet room before blaming anyone.

## 🔵 GRANDMA NOTE

It's like judging whether the guest cook burned the pie — while your own oven was acting up. You'd bake the same pie in a neighbor's reliable oven first. If it comes out fine there, the cook was never the problem; your oven was. Before scoring the cook's pie, test in the good oven. The team did exactly that: the same tests, run alone in a clean room, passed — so the PR never baked the failure.

## 🟠 NAYA NOTE

Apply whenever a full-suite run shows failures on a PR head: (1) list the failing files; check which paths the PR actually touched — failures in untouched paths are suspects, not evidence; (2) before attributing ANY failure to the PR, re-run the failing files in isolation — the 60-second attribution test; (3) pass-in-isolation + zero PR touches under those paths → harness interference, not PR-caused; name the mechanism (order-dependence, shared-state mutation, depth-1 clone quirks, locale/codec) so the next seat doesn't re-derive it; (4) score the PR only on its attributable failures; the verdict names what was excluded and why. "Attribute before scoring" is the law; the isolated re-run is the instrument. Note the reverse twin (SN-0985): passing in isolation does NOT prove the composition works — isolation exonerates, it never certifies.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "misattributed_ci_failures",
  "evidence": {
    "board_comment": "6183933395 — night-shift-verify VERIFY CORRECTION (PR #2610 @ e099fb34, 2026-10-15T03:46:54Z): full-suite 19 failed / 4383 passed / 12 skipped (31.5 min); 16 extra failures beyond the 3 known are NOT PR-caused — all in tools/test_activation_checklist.py (PR touches zero tools/ files); same file passes 26/26 in isolation -> order-dependent; verdict STANDS",
    "mechanism": "harness tests rewriting refs/remotes/origin/main in a depth-1 clone",
    "outcome": "PR-caused failures = exactly the 3 brain_index_freshness DRIFT tests (CI-corroborated class); fix list unchanged: (1) authoring index regen at final head + commit, (2) Verity's green-or-challenge, (3) main-seat #2610/#2611 convergence sequencing"
  },
  "cousins": ["SN-097", "SN-0985"],
  "decision_change": "future 'PR is RED' verdicts re-run the failing files in isolation before attributing failures to the PR",
  "falsifiability": "if the isolated re-run also fails, the exoneration is wrong — the failures may be PR-caused or a real environment defect (decline both attributions until traced)",
  "mechanism_note": "order-dependent test interference: harness tests mutate shared git state in the same workspace; isolation removes the interference, exposing whether the failure belongs to the PR",
  "procedure": "60-second isolated re-run of failing files before scoring"
}
~~~
