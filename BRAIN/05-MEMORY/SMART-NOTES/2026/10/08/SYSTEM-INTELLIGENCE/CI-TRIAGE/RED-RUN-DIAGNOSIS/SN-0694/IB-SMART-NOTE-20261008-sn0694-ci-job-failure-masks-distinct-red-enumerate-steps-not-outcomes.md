# A CI Job That Dies Before the Check Runs Hides a Distinct RED — Enumerate Steps, Not Job Outcomes

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0694-ci-job-failure-masks-distinct-red-enumerate-steps-not-outcomes
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Filed by:** distillation loop, #1354 6064045402 (2026-10-08).
**Provenance:** #1354 6064045402 ([NAYA 2][BRAIN-BUILD] Consolidation receipt — brain-index drift RED, 2026-10-08T16:08:41Z). Cousins SN-0421 (run-level SUCCESS with skipped behavioral jobs is vacuous), SN-0552 (fail-first CI topology converts secondary REDs), SN-0236 (one repair per RED class), SN-0438 (fail-closed gate firing is the design working).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The brain index was RED on the pristine tip `aacbcc9a` — 21 commits stale (basis `f52ffb96`, 806 files committed vs 811 in tree, 5 real files added since) — and CI never showed it: the `test` job died at the `test_engineering_gates.py` collection error **before the `--check` step ran**. An early-step failure masked a distinct, real drift RED. The repair discipline held: Naya 2 shipped PR #1900 (commit `26b76dae` on live tip `aacbcc9a`, 3 index files, remote blobs byte-verified, `--check` → OK, 37/37 index tests), then **HELD the merge** because the tip still carries the pre-existing collection RED (open repair #1840 owns that class — its mechanism proved: 17/17 pass with the path fix), closed #1845 as superseded by #1900 under the one-open-repair-per-class rule (SN-0236), and never touched another lane's branch. The lesson: a job-level RED verdict tells you only that the job stopped; read the step that stopped it, and enumerate which checks actually ran. A mask is not an absence — the `--check` didn't pass, it never executed.

## 🩷 HUMAN NOTE

Shawn — Naya 2 found the brain index was genuinely out of date on the current tip (21 commits behind, 5 real files missing from the committed index) — and CI was hiding it. The test job was failing, yes, but it was failing at a *collection error* that killed the job before the index-check step ever ran. So the dashboard said "red" for one reason while the real drift sat invisible underneath. She fixed the index (PR #1900, verified byte-for-byte) and then did the disciplined thing: she did NOT merge it, because the tip still has that pre-existing test-collection red owned by a different repair lane. No second repair, no touching anyone else's branch, no merge onto a red tip. The rule that survives: a CI failure only tells you where the job *stopped* — you have to read which steps actually ran. A check that never executed is not a check that passed.

## 🟣 CHILD NOTE

The team keeps a big list of all the files in the brain. That list fell 21 updates behind — but the robot that checks everything said "everything is fine"... because it broke down at step 2 and never got to the list-check at step 5. The dashboard was red, but for the wrong reason, and the real problem was hiding underneath. A team member rebuilt the list by hand, double-checked every byte, and then did NOT merge it yet — because the robot was still broken for a different reason, and merging onto broken tests is against the rules. Lesson: when the checker breaks early, the things it never checked don't become "fine" — they become "unknown." Read the steps, not just the red light.

## 👵 GRANDMA NOTE

Honey, the inventory list was 21 entries out of date, and the inspector's report looked like it had been filed — except the inspector's car broke down on the way, two blocks early. Nobody's fault, but nobody's checklist either. The team member who found it redid the inventory perfectly, proved every byte matched, and then — this is the disciplined part — she refused to file it until the broken-down car gets fixed too, because the rules say you don't stack new work on a broken lane. Two rules for the kitchen wall: (1) when the job fails, find out exactly which step died — everything after it is uninspected, not clean; (2) one broken thing gets one repair, owned by one person — you don't fix your neighbor's fence to get your own roof approved.

## 🧠 NAYA NOTE

Cold successor: this is the failure-masking sibling of SN-0421. SN-0421 says a run-level SUCCESS with skipped behavioral jobs is vacuous; this says a run-level FAIL whose job died before a downstream check ran is **masking** — the downstream verdict is not "passed" and not "failed", it is **unknown**. The procedure: when a CI job is RED, enumerate the steps and identify which one stopped the job; every check scheduled after it has no verdict. Reproduction belongs on pristine tip bytes, not on the repair environment (the battery ran on `aacbcc9a`). The ownership discipline around it: open repair #1840 owns the `test_engineering_gates.py` collection-error class (mechanism proved 17/17); #1845's stale regen on `027fceb0` was closed as superseded by #1900 under SN-0236; merge of #1900 HELD — no merge onto a tip whose tests are RED without an explicit scorecard accepting the pre-existing RED. Evidence: #1354 6064045402 — `--check` exits 1 (21 commits stale, 806 vs 811 files, 5 real files added: `BRAIN/01-GOVERNANCE/0000-OPERATING-CODE-V1.md`, `BRAIN/01-GOVERNANCE/TEAM-NAYA-OPERATING-PROTOCOL-V1.md`, 3× `BRAIN/06-PROOF/2026-10-07-SELF-IDENTITY-TRIAL-V1.*`); PR #1900 commit `26b76dae` (parent = live tip `aacbcc9a`), `--check` → OK (811 files), 37/37 index tests green.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-0694",
  "title": "A CI Job That Dies Before the Check Runs Hides a Distinct RED — Enumerate Steps, Not Job Outcomes",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "CI-TRIAGE", "RED-RUN-DIAGNOSIS"],
  "cousins": ["SN-0421", "SN-0552", "SN-0236", "SN-0438"],
  "evidence": {
    "comment": "#1354 6064045402 ([NAYA 2][BRAIN-BUILD] Consolidation receipt, 2026-10-08T16:08:41Z)",
    "drift": "brain index 21 commits stale on pristine tip aacbcc9a (basis f52ffb96): 806 files committed vs 811 in tree; 5 real files added since",
    "mask": "CI test job died at test_engineering_gates.py collection error before the --check step ran — the real drift RED was invisible at job level",
    "repair": "PR #1900 brain-build/brain-index-regen-tip-aacbcc9a commit 26b76dae (parent = live tip aacbcc9a); 3 index files; remote blobs byte-verified; --check OK (811); 37/37 index tests",
    "discipline": "#1845 closed as superseded by #1900 (SN-0236 one-repair-per-class); merge of #1900 HELD — tip carries pre-existing collection RED owned by #1840 (mechanism proved 17/17); no second repair; Naya 4's branch untouched"
  },
  "rule": "a job-level verdict only tells you where the job stopped — enumerate which steps actually ran; a check that never executed is unknown, not clean; reproduce on pristine tip; one class gets one repair; never merge onto a RED tip without an explicit scorecard accepting the pre-existing RED"
}
```
