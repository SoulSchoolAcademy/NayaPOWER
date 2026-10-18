# Name the Hash Flavor at the Comparison Site — Cross-Flavor Comparisons Produce False Drift

**Intelligent Block:** IB-SMART-NOTE-20261018-sn01656-name-the-hash-flavor-at-the-comparison-site
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** hidden_files/shared-state.json (director_tick_2026_10_18_1438, 2026-10-18 21:38Z): L527 [F1] (board comment 6255392239) — byte-identity comparison names hash flavor (contents-API sha256 vs git blob-sha1 cross-flavor false-drift on the #2753 gate blob, resolved via git/trees which speaks the blob flavor; promoted to AGENTS.md).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A "SHA match" claim is meaningless until both hash flavors are named. The #2753 gate blob produced a false drift signal because the comparison crossed flavors — a contents-API sha256 against a git blob-sha1 — and inequality-of-flavors was read as drift-of-content. The fix: at every byte-identity comparison site, name each digest's algorithm and the exact bytes hashed; when the flavors differ, normalize through one source (git/trees) before comparing. Identical-looking hex is the trap; the comparison site, not the digest, must disambiguate.

## 🩷 HUMAN NOTE

Shawn — a byte-check cried "drift" on the #2753 gate blob, and the drift was fake. The check was comparing a SHA from one system (the contents API, sha256) against a SHA from another system (git blobs, sha1) — two different hash recipes, so they could never match even on identical bytes. The standing rule this earned: any identity comparison has to name the hash flavor on both sides — algorithm AND the exact bytes hashed — before it compares. If the flavors differ, normalize first (git/trees speaks the blob flavor) and compare after. A bare "SHAs don't match" is never the verdict until the flavors are named.

## 🟣 CHILD NOTE

Imagine comparing two secret codes to see if two boxes hold the same treasure. But one code was written in red ink and the other in blue ink — and you compare the ink, not the treasure. They'll never match, even if the treasure inside is identical. The rule: before comparing, check you're comparing the same thing — same code style, same treasure. If they're not the same style, convert one first, then compare.

## 🔵 GRANDMA NOTE

It's like weighing two parcels to prove they hold the same cake. One scale reads in pounds, the other in kilograms — and the numbers never match, so you conclude someone ate a slice. Nobody ate anything; you compared pounds to kilograms. The rule: say which scale you're using, convert to one, then compare. Name the measure, or the measure lies.

## 🟠 NAYA NOTE

Cold successor: the byte-identity comparison procedure.

1. At the comparison site, name BOTH flavors: algorithm (sha1 / sha256) and the exact bytes hashed (response payload vs git blob bytes vs tree entry). No flavor named = the comparison is not evidence.
2. If the flavors match: compare directly, cite the flavors in the receipt.
3. If the flavors differ: normalize through ONE source before comparing — for blob identity, git/trees speaks the blob flavor; or re-hash the same bytes with the same algorithm. Never compare across flavors.
4. Failure signature to watch: a CONSTANT mismatch on bytes you believe identical is the fingerprint of a flavor mismatch, not drift. When you see it, check flavors before declaring drift.
5. The receipt line reads: "blob identity: git blob-sha1 <h1> == contents-API sha256→normalized-via-git/trees <h2>" — the flavor annotation is load-bearing, not decorative.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1656",
  "title": "Name the Hash Flavor at the Comparison Site — Cross-Flavor Comparisons Produce False Drift",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-18",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "ENGINEERING-PROOF", "EVIDENCE-IDENTITY"],
  "applies_when": ["verification", "byte-identity", "evidence", "git", "blob-sha", "ledger-sync", "pin-to-live"],
  "enforcement": "A shared comparison helper used by all byte-identity checks declares both hash flavors in its call signature and refuses to compare across flavors without normalization (route through git/trees, or re-hash the same bytes with the same algorithm). The scorer bounces any byte-identity proof that cites a bare 'SHA match' without naming flavors on both sides.",
  "cousins": ["SN-0861 (verify by blob-sha — same anchored-measurement family: this note adds the missing rung, that a blob-SHA from one source and a hash from another are comparable only when both flavors are named)", "SN-0200 (receipt pins must resolve live — the identity half: a pin that resolves to a cross-flavor comparison is not a resolution)"],
  "evidence": {
    "l527_f1": "hidden_files/shared-state.json, director_tick_2026_10_18_1438: 'L527 [F1] (6255392239): byte-identity comparison names hash flavor (contents-API sha256 vs git blob-sha1 cross-flavor false-drift on #2753 gate blob, resolved via git/trees; promoted to AGENTS.md)'",
    "failure_signature": "constant mismatch on believed-identical bytes = the fingerprint of a flavor mismatch, resolved by normalizing through git/trees before comparing"
  },
  "decision_change": "when writing or reviewing any byte-identity verification — blob-SHA vs API SHA, hash comparisons across stores — the author names both hash flavors at the comparison site and normalizes before comparing; a bare 'SHA match' is treated as an unverified claim until the flavors are on the record.",
  "falsifier": "for any pair of digests where both flavors are proven identical, the naming requirement is vacuous (the rule does not fire there). If a cross-flavor comparison is ever proven order- and encoding-safe for a specific pair, the normalization step drops for that pair — the naming requirement stands regardless.",
  "mechanism": "SHA hex strings are indistinguishable by eye — a 40-hex sha1 and a 64-hex sha256 both 'look like hashes,' and comparing across flavors yields deterministic inequality that masquerades as content drift. The failure signature (constant mismatch) is identical to real drift, so disambiguation must happen at the comparison site, where the flavors can be named — the digest alone can never say what recipe made it."
}
```
