# A Gate That Scans Zero Files and Prints PASS Is Worse Than a FAIL — Quote the Scanned Count With the Verdict

**Intelligent Block:** IB-SMART-NOTE-20261112-sn02701-quote-the-scanned-count-with-the-verdict
**Smart Note:** SN-2701
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

A gate that scans 0 files and prints PASS certifies nothing and looks like proof. In the 2026-11-12 distill-daily fix, the first post-edit gate run was executed from inside `BRAIN/00-ACTIVATION` with a relative path, scanned 0 files, and printed a vacuous PASS; the read-back caught it ("0 boot file(s)" versus "12 boot file(s)"), and the re-run from the repo root printed the real PASS over 12 files. Rule: always quote the scanned-count line with the verdict, never the verdict alone.

## 🩷 HUMAN NOTE

A check that looked at nothing and said "all good" is worse than a check that failed. A failure gets fixed; a false "all good" gets believed, filed, and built on. The verdict word — PASS or FAIL — says nothing by itself. What makes it proof is the count next to it: how many files, jobs, or cases the check actually examined. If a receipt claims a gate passed, the receipt must carry the line that says how much the gate saw. No count line, no proof — the claim gets bounced, not scored.

## 🟣 CHILD NOTE

Imagine a teacher who says "everyone passed the test" but never gave the test to anyone. The words sound good, but they mean nothing, because nobody was checked. A real pass means: this many papers were checked, and this many passed. Always ask "how many did you check?" before you believe "all good."

## 🔵 GRANDMA NOTE

If someone tells you the house is safe because they checked every room, ask how many rooms they checked. If the answer is none, the house is not proven safe — the checker just never looked. A green light only means something when you know what it looked at. Keep the number next to the verdict, every time.

## 🟠 NAYA NOTE

The operational rule: a gate PASS is accepted as proof only when the receipt quotes the scanned-count line with the verdict (for example, "PASS: no stale pointers in 12 boot file(s)"). A bare "PASS" verdict is bounced, not scored, and the seat re-runs the gate from the correct working directory and quotes the count.

Why it works: a verdict over an empty population is vacuously true — "all zero files are clean" is true of nothing, so the string PASS carries zero bits about the files. The count line is the population evidence that binds the verdict to something actually checked. The failure mode is silent: the wrong-directory run printed PASS in exactly the same format as the real run, so only the count line ("0 boot file(s)" versus "12 boot file(s)") distinguished proof from nothing.

Evidence: receipt `hidden_files/twelve-lane-receipts/distill-daily-20261112.md` (2026-11-12 13:49–14:05 UTC, Lane 0 distill-daily hat, 9.2/10 after three honest passes; independently scored 9.2/10). First post-edit run of `boot_pointer_check.py BRAIN/00-ACTIVATION` from inside `BRAIN/00-ACTIVATION` scanned 0 files and printed a vacuous PASS; caught on read-back; re-run from the repo root printed "PASS: no stale pointers in 12 boot file(s). Live board machine-read #3352 from snapshot." exit 0. Fix commit `1b31c827c3359060fb18d4be555a4bba4e05812f`, branch `distill-daily-20261112-boot-pointers`.

Cousins, distinct: SN-0421 (a CI run-level SUCCESS with skipped jobs is vacuous proof — read the job table, not the badge; CI-level, about skipped jobs, not a local gate's scanned population); SN-1285 (a proof that passes on everything is a rumor — the non-vacuous differential; about test design, not the count line); SN-0061 (prove negatives non-vacuous). None of them states the count-line prescription, and none of them would have caught this run: the gate can fail, it ran, and it printed PASS — it simply ran on nothing. Sibling near-miss in the same receipt (the twin edit that used list index 6 instead of 7, caught because the assertion fired before any write) is CANDIDATE 603's territory, already held — not re-filed here.

Falsifier: a gate that refuses empty input by construction (exits non-zero when it scans 0 files) makes the count line redundant for that gate; or a quoted count that matches the expected population while the verdict still proves nothing would show the rule insufficient. Honest scope: single-seat observation, one gate, one run; the rule's value is the prescription, not the incident's size.

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn_id": "SN-2701",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-11-12",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "applies_when": ["gate", "verification", "receipt"],
  "enforcement": "The verifier/scorecarder re-runs the gate from the repo root and requires the receipt to quote the scanned-count line (e.g. 'PASS: no stale pointers in 12 boot file(s)'); a gate PASS claimed without the count line is bounced, not scored.",
  "rule": "Always quote the scanned-count line with a gate verdict, never the verdict alone; a PASS over zero scanned files is vacuous proof.",
  "decision_change": "Whether a gate PASS counts as proof in a receipt or scorecard: a bare PASS verdict is not accepted; the receipt must carry the scanned-count line.",
  "falsifier": "A gate that refuses empty input by construction (exits non-zero on 0 scanned files) makes the count line redundant for that gate; a quoted count matching the expected population while the verdict still proves nothing would show the rule insufficient.",
  "mechanism": "A verdict over an empty population is vacuously true, so the PASS string carries zero bits about the files; the count line is the population evidence that binds the verdict to something actually checked.",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/distill-daily-20261112.md (2026-11-12 13:49-14:05 UTC, Lane 0 distill-daily hat, 9.2/10)",
    "gate": "boot_pointer_check.py BRAIN/00-ACTIVATION",
    "vacuous_run": "first post-edit run from inside BRAIN/00-ACTIVATION with a relative path scanned 0 files and printed PASS",
    "real_run": "re-run from the repo root: 'PASS: no stale pointers in 12 boot file(s). Live board machine-read #3352 from snapshot.' exit 0",
    "commit": "1b31c827c3359060fb18d4be555a4bba4e05812f",
    "branch": "distill-daily-20261112-boot-pointers"
  },
  "cousins": ["SN-0421", "SN-1285", "SN-0061"],
  "raw_source_separate_from_distillation": true,
  "automatic_truth_ceiling": "CANDIDATE",
  "authority_inheritance": false
}
```
