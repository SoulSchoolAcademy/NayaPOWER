# Environment Failures Must Never Wear Product Clothing

**Intelligent Block:** IB-SMART-NOTE-20261005-sn0346-environment-failures-must-never-wear-product-clothing
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The adversarial brain-index harness scored 5/6, then 4/6, on a provably green tip (`240db9636`). The product was fine; the environment was not. Root cause: the harness clones the repo five times at ~117MB each into a 512MB `/tmp` tmpfs, and a `2>/dev/null` had been swallowing "No space left on device" — so dead clones were scored as index defects instead of what they were: the disk being full.

Two rules land from one repair (PR #1460): (1) measurement tooling must FAIL LOUD on environment shortage — a harness that cannot measure must announce it with a dedicated exit (here: FATAL exit 3) and abort the affected check as an environment failure, never silently convert it into a product score; `2>/dev/null` on anything that can carry a failure reason is a lie in the instrument. (2) When two lanes find the same RED class, consolidate — do not duplicate: the brain-build lane found an open PR #1263 on the same RED class, verified its fail-loud mechanism on exact bytes, carried it verbatim into #1460 (one mechanism, one env var), added only the missing disk-selection delta its `/tmp` default lacked, posted the receipt to #1263, and left closure to the owning lane. This is the positive form of the One-Repair-per-RED-Class law: scan first, verify on exact bytes, carry verbatim, extend minimally, receipt the owner, never close another lane's lane.

## 🩷 HUMAN NOTE

A measuring instrument that reports a broken product when its own battery died is worse than no instrument — it teaches you the wrong thing. When your test harness can't do its job because the disk is full, the harness must say "the disk is full" loudly, not quietly hand you a red score for the product. Never silence error output on a measuring tool: hiding "No space left on device" cost a real investigation into a phantom failure.

And when another team is already fixing the same problem, don't build a second fix: verify theirs works, carry it over exactly, add only what's genuinely missing, tell them, and let them finish their lane.

## 🟣 CHILD NOTE

If your ruler breaks while you measure, say "the ruler broke" — do not say "the table shrank." And if someone else already fixed the same problem, use their fix instead of building a second one.

## 🔵 GRANDMA NOTE

Tools must be honest about their own failures. A test that mistakes an empty tank for a broken engine will have you rebuilding the wrong thing. And never build a second ladder when someone is already climbing one — steady theirs instead.

## 🟠 NAYA NOTE

Treat every measurement harness as a two-failure-domain system: the subject's failure domain and the harness's own failure domain, and the harness must never attribute its own failures to the subject. Hard requirements: no silenced stderr on paths that carry failure reasons; a dedicated loud exit for environment shortage; a disk-selection chain for scratch workspaces ($BRAIN_ADVERSARIAL_TMPDIR → repo parent → /var/tmp → $HOME in this case). Pair this with the consolidation protocol for shared RED classes: scan the board for open work on the class first, verify the existing mechanism byte-for-byte, carry it verbatim (one mechanism, one knob), extend only the missing delta, post a receipt to the owning lane, and never close or duplicate their repair.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "rule_a_measurement_integrity": {
    "name": "environment failures must look like environment failures",
    "mechanism": "dedicated loud exit on environment shortage (FATAL exit 3); affected check aborts as environment failure, never scored as product defect",
    "prohibited": "2>/dev/null or any stderr suppression on paths that carry failure reasons",
    "root_cause": "5x~117MB clones into 512MB /tmp tmpfs; 'No space left on device' hidden by suppressed stderr; phantom 5/6 then 4/6 on green tip 240db9636",
    "disk_selection_chain": ["$BRAIN_ADVERSARIAL_TMPDIR", "repo parent", "/var/tmp", "$HOME"]
  },
  "rule_b_consolidation": {
    "name": "one repair per RED class — positive form",
    "steps": ["scan for open work on the RED class", "verify mechanism on exact bytes", "carry verbatim (one mechanism, one env var)", "extend only the missing delta", "post receipt to owning lane", "leave closure to the owning lane"],
    "observed": "open #1263 verified on exact bytes; carried verbatim into #1460; added only disk-selection delta its /tmp default lacked; pytest carried byte-identical (2/2 green)"
  },
  "evidence": {
    "board_comment": 5995511437,
    "pr": "#1460",
    "related": ["#1263", "SN-0236"]
  }
}
~~~
