# The Compare API Contradicts Itself on the Identical SHA Pair — Never Quote Its Counts as Verified

**Intelligent Block:** IB-SMART-NOTE-20261021-sn1794-compare-api-contradiction
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-22
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** board #2793 comment 6330914275 (Shawn's word surfaced by the 19:08 PDT director pass 2026-10-21); hidden_files/snapshot-content-20261021-1908.md

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

On 2026-10-21 the GitHub compare API returned contradictory commit counts for the identical SHA pair — the same call, the same two SHAs, different numbers. Shawn's word surfaced the incident the same hour (board #2793 comment 6330914275): the production-parity compare counts were WITHDRAWN as unverified. What stands is only what was verified two other ways: production `acf57082f5` stamps source `00f50bb32c1c`. The named failure mode is COMPARE-API-CONTRADICTION. The rule from here on: a compare-API "N commits ahead/behind" number is a computed artifact, not a measurement — it is never quoted as a verified count. If a count matters, re-derive it from terminal output read in full, or mark it UNVERIFIED and omit it.

## 🩷 HUMAN NOTE

Shawn — one banking-worthy catch from tonight's director pass: the GitHub compare API gave two different commit counts for the exact same SHA pair. Same call, same SHAs, different answers. That's not a number we can ever quote as fact, so your call the same hour stood: the production-parity compare counts were withdrawn, and what counts is only the two-ways-verified stamp (production `acf57082f5` ↔ source `00f50bb32c1c`). The lesson now in the brain: compare-API numbers are computed, not measured — any report that needs a commit count re-derives it from the terminal output read in full, or leaves the number out. Nothing verified ever rests on a number that changes when you ask twice.

## 🟣 CHILD NOTE

Imagine a scale that shows a different weight every time you step on it. Would you write that weight down as a fact? Of course not. The compare tool is that scale — it answered the same question with two different numbers. So the rule is simple: never write down the number from that scale as a fact. If you really need a number, count it yourself and read the whole answer before you write anything down.

## 🔵 GRANDMA NOTE

A surveyor measured the same fence twice and got two different lengths. The wise answer isn't to pick one — it's to throw both away and measure again yourself, carefully, reading the full tape. The compare tool gave two different counts for the same two points, so we retired it as a source of counts. When a number matters, we count it by hand and read the whole result before writing it down.

## 🟠 NAYA NOTE

Cold successor: COMPARE-API-CONTRADICTION is a named failure mode — never quote a GitHub compare-API ahead/behind count as a verified number in a board post, merge receipt, or snapshot. The mechanism: the endpoint resolves branch heads and merge bases, not a frozen pair, so identical-looking calls can route through different resolutions and return different numbers. The enforcement is the receipt checklist: (1) if a count is needed, re-derive it from terminal output read in full; (2) otherwise mark any compare-API count UNVERIFIED or omit it. Incident evidence: board #2793 comment 6330914275 (withdrawal), hidden_files/snapshot-content-20261021-1908.md (19:08 PDT director pass). What stands in its place: production `acf57082f5` stamps source `00f50bb32c1c`, verified two ways. Cousin: SN-1788 (count-equality promises on growing sets), SN-0035 (phantom citations — different class).

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1794",
  "title": "The Compare API Contradicts Itself on the Identical SHA Pair — Never Quote Its Counts as Verified",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-22",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "VERIFICATION", "EVIDENCE-DISCIPLINE"],
  "cousins": ["SN-1788", "SN-0035"],
  "evidence": {
    "board": ["#2793 comment 6330914275 — Shawn's word surfaced by the 19:08 PDT director pass: production-parity compare counts WITHDRAWN as unverified"],
    "incident": "compare API returned contradictory commit counts for the identical SHA pair (2026-10-21) — new named failure mode COMPARE-API-CONTRADICTION",
    "what_stands": "production acf57082f5 stamps source 00f50bb32c1c, verified two ways",
    "source": "hidden_files/snapshot-content-20261021-1908.md"
  },
  "applies_when": ["claim", "compare-api", "merge", "receipt", "board", "report"],
  "enforcement": "merge receipt checklist: never publish a compare-API ahead/behind count as verified; re-derive any needed count from terminal output read in full, else mark UNVERIFIED or omit",
  "decision_change": "whether a board post or merge report may quote compare-API commit counts as verified numbers — it may not",
  "falsifiability": "repeat the identical-SHA-pair compare call N times; consistent counts would demote the incident to a one-off and revise the lesson",
  "mechanism": "the compare endpoint resolves branch heads and merge bases, not a frozen pair — identical-looking calls can route through different resolutions, so the number is a computed artifact, not a measurement",
  "rule": "a number that changes when you ask twice is never quoted as verified — re-derive from terminal output read in full, or omit"
}
```
