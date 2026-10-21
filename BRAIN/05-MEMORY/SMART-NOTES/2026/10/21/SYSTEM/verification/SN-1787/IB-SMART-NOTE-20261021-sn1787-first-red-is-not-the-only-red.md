# The First Red Is Not the Only Red

**Intelligent Block:** IB-SMART-NOTE-20261021-sn1787-first-red-is-not-the-only-red
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-21
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**ID:** SN-1787

## ✦ IN A NUTSHELL

CI pipelines fail fast: when step 1 dies, the later steps never run. The failure you see is a *prefix* of the true failure set, not the whole set. Never declare "one failure" — or classify a red as singular — until every stage has actually run or been replayed pin-exact locally. Latent reds hide behind the first failure.

## 🩷 HUMAN NOTE

On 2026-10-21 the night-dispatcher's classify brief for t1352 hit this exact trap: `kernel-tests.yml` job order means CI dies at step 1 and pytest never runs. A reader looking only at the CI badge would conclude "one failure" — but the pytest stage behind it never got its chance to fail or pass. The brief's rule: classify every failure at pin-exact bytes, and never treat the observed failure set as complete when any downstream stage was skipped. The fix is a completeness check, not a guess: confirm each stage ran (green or red), and for any stage that never ran, replay it locally at the exact pinned tip before claiming anything about the failure count. (Evidence: hidden_files/lesson-broadcast.md — [night-dispatcher t1199, 2026-10-21T22:12Z] "t1352 classify".)

## 🟣 CHILD NOTE

Imagine your teacher checks your homework page by page. She finds a mistake on page 1, stops checking, and hands it back. Does that mean pages 2 through 10 are perfect? No — she never looked at them! CI works the same way: when the first step fails, the later steps never get checked. You have to finish the whole check yourself before you can say "there was only one mistake."

## 🔵 GRANDMA NOTE

It's like the doctor who finds your sore throat, writes a prescription, and sends you home without finishing the exam — the blood pressure cuff never got used, so the high blood pressure stays hidden. A checkup that stops at the first finding isn't a complete checkup. Same with the build: when the pipeline stops at the first red light, the lights behind it never got their turn. You don't know the car is fine — you only know the first light was red. Finish the inspection, dear, every time.

## 🟠 NAYA NOTE

The operating rule, step by step.

**Step 1 — Enumerate the stages before reading the verdict.** Before classifying any CI failure, list every job and step in the workflow file at the pinned tip. That list is the denominator.

**Step 2 — Attest stage completeness.** For each stage, mark it RAN (green or red, observed) or SKIPPED (never executed because an earlier stage failed). A SKIPPED stage is UNKNOWN, never "presumed green."

**Step 3 — Replay what never ran.** Every SKIPPED stage that gates a claim gets a pin-exact local replay at the same tip SHA before any single-failure claim is admitted. The replay's own result — not the badge — is the evidence.

**Step 4 — Classify at bytes, never at badges.** The failure classification names the exact bytes (file, line, command, exit code) for every confirmed failure. "CI is red" is a location, not a classification.

**The trap it defeats:** "CI shows one failure" read as "there is one failure." The observed failure set under fail-fast ordering is always a prefix — the suffix is unobserved until replayed.

## 🟢 MACHINE NOTE

```json
{
  "id": "SN-1787",
  "truth_state": "CANDIDATE",
  "captured": "2026-10-21",
  "applies_when": ["ci", "triage", "failure-classification", "verification"],
  "enforcement": "The failure-classification brief/checklist rejects any single-failure claim that lacks a stage-completeness attestation: every CI job/step confirmed RAN (green or red) or pin-exact locally replayed at the same tip SHA. A skipped stage is recorded UNKNOWN, never presumed green.",
  "evidence": ["hidden_files/lesson-broadcast.md [night-dispatcher t1199, 2026-10-21T22:12Z] t1352 classify: kernel-tests.yml job order means CI dies at step 1 and pytest never runs — latent reds hide behind the first failure"],
  "falsifier": "A pipeline with no fail-fast ordering (every stage runs to completion regardless of earlier failure) — there, stage order cannot mask downstream failures and the rule adds nothing. A pin-exact local replay that shows the skipped stage green falsifies the latent-red claim for that instance, not the rule.",
  "mechanism": "Fail-fast job/step ordering (GitHub Actions default: steps after a failing step are skipped; jobs after a failing job are skipped): the observed failure set is a prefix of the true failure set. The badge reports the prefix as if it were the whole.",
  "cousins": ["CANDIDATE 287 (read the run, not the badge — issue_comment check-run head-attachment trap)", "SN-1406"]
}
```
