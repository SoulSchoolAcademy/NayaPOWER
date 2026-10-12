# Audit the Evidence Artifacts, Not Just the Pipeline — The Leak Audit Caught a Real Identity Leak

**Intelligent Block:** IB-SMART-NOTE-20261011-sn1048-audit-evidence-artifacts-not-just-pipeline
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** [LANE VERITY] Naya Verity (Lane 1) tick t1282 receipt 2026-10-11 22:01 PDT, hidden_files/twelve-lane-receipts/t1282-lane1.md §4; Blinded-Scoring Protocol v1 hidden_files/blinded-scoring/SPEC.md + mechanism/leak_audit.py; packet hidden_files/blinded-scoring/demo/ (seal-log.json sealed 2026-10-12T04:59:44Z, leak-audit.json verdict=PASS, score-sheet.md). Related: SN-1028 (calibrate probes), SN-1029 (correct refutation), SN-1030 (never score a void).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Naya Verity built Blinded-Scoring Protocol v1 — six ceremonies (C1–C6) with a leak-audit step that scans the sealed packet before any scorer sees it. On the very first demo run the audit **fired honestly**: two probe outputs had self-named their probes (`probe-a1`, `probe-a2`) inside their headers — a genuine identity leak sitting inside the evidence. The pipeline was blinding correctly (neutral IDs from os.urandom, arm key escrowed); the contamination came from the producers' own output headers. Verity added evidence normalization to the assembler, re-ran the audit — PASS (0 exclusion hits, 0 unexpected files, 0 arm-specific pointers) — and only then unblinded. Three independent scorings (t1262 unblinded provisional, t1272 partial-blind, this fully blinded run) agree exactly: Δ=+0.67, so the normalization did not move the score; it only removed the leak.

The durable rule: **in blinded evaluation, audit the evidence artifacts themselves, not just the pipeline.** Producers leak identity in headers, filenames, timestamps, and phrasing — the blinding layer cannot sanitize what the evidence already says. The leak-audit ceremony must run on the actual bytes the scorer will read, and any fire must block scoring until normalization re-passes. A second lesson rides along: the audit's credibility came from firing on a real leak, not on a synthetic test — the same "first red is the proof" law as SN-1026. And the protocol captured a failure-transport detail worth keeping: the t1262 scorer failure (subagent bootstrap unauthorized ×2) happened at the SPAWN layer before packet transmission — zero integrity impact — and is now encoded as an idempotent-retry checkpoint (scorer ACKs packet receipt before scoring), so a retry can never double-count.

## 🩷 HUMAN NOTE

Shawn — a good one from Naya Verity tonight. She built the blinded-scoring protocol (so judges can't tell which answers they're grading) with a mandatory leak-check before scoring. On the first real run, the check caught an actual leak: two answers had the experiment's codenames in their headers — the blinding was fine, but the answers themselves gave it away. She stripped the leaked names out, re-ran the check (clean), and only then scored. Three separate scorings agree to the digit, so the cleanup changed nothing but the leak. The brain rule: when you run a blind test, audit the actual test materials — not just the blinding machine — because leaks hide in the content, not the plumbing.

## 🟣 CHILD NOTE

Imagine a taste test where two chefs' cookies must be judged without knowing who baked them. The helper put the cookies in plain bags — but one chef wrote her name on the bag in tiny letters! A judge who spots the name can't be fair anymore. So before judging, a helper checks every bag for secret names. Tonight, the checker found two names, erased them, checked again (all clean), and THEN the judges tasted. Rule: check the actual bags, not just the bag-filling machine — because names hide in the bags.

## 👵 GRANDMA NOTE

It's like blind wine tasting. You can pour the wines into identical glasses all day long — but if one bottle's label fell into a glass, the taster isn't blind anymore. The pour was done perfectly; the leak was in the glass itself. So the smart move isn't to improve the pouring — it's to check every glass for labels before anyone sips. And one honesty habit: when the tasting got interrupted (the taster couldn't start, twice), the team recorded that the interruption happened before any wine was poured — so it couldn't have changed the result — and built a "start over cleanly" rule for next time.

## 💜 NAYA NOTE

Blinding is a promise to the scorer: "nothing you read can tell you who wrote it." I kept that promise at the pipeline — but the evidence broke it in the headers. The leak was never in my machinery; it was in the words themselves, which no pipeline can launder. So the audit must read what the scorer reads, byte for byte, and any leak blocks scoring until the evidence is clean. A leak-check that has never fired is a wish — mine fired on the first real packet, and that is why it is now a gate I trust.

## 🤖 MACHINE NOTE
```json
{
  "sn": "SN-1048",
  "lesson": "audit-evidence-artifacts-not-just-pipeline",
  "rule": "In blinded evaluation, run the leak audit on the actual bytes the scorer will read; producer-side artifacts (headers, names, timestamps) leak identity where the blinding pipeline is clean. A fire blocks scoring until normalization re-passes.",
  "failure_found": "probe outputs self-named probes (probe-a1, probe-a2) in headers — FAIL-IDENTITY-LEAK",
  "fix": "evidence normalization in assembler; re-audit PASS (0 exclusion hits, 0 unexpected files, 0 arm-specific pointers)",
  "triangulation": "t1262 unblinded (provisional) × t1272 partial-blind × fully-blinded run agree exactly: delta=+0.67",
  "evidence": {
    "protocol": "hidden_files/blinded-scoring/SPEC.md (C1–C6), mechanism/leak_audit.py",
    "packet": "hidden_files/blinded-scoring/demo/ (seal-log.json 2026-10-12T04:59:44Z, leak-audit.json verdict PASS)",
    "receipt": "hidden_files/twelve-lane-receipts/t1282-lane1.md"
  },
  "also_captured": "t1262 scorer failure at SPAWN layer (pre-transmission, zero integrity impact) → idempotent-retry checkpoint: scorer ACKs packet receipt before scoring",
  "related": ["SN-1026", "SN-1028", "SN-1029", "SN-1030"]
}
```
