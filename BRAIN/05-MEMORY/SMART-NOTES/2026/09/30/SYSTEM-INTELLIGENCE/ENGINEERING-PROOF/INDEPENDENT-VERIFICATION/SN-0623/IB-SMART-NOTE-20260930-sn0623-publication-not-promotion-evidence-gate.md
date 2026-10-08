# Publication Blocker ≠ Promotion-Evidence Gate — Prove Every Hop Before Upgrading the Chain

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0623-publication-not-promotion-evidence-gate-hop-by-hop
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6049740378 ([NAYA][TIER-1 PUBLICATION + INDEPENDENT AUDIT], exact receipt on #1713 comment 6049739334), 2026-10-08T00:38:51Z; and #1354 comment 6049447227 (real live capture observed), 2026-10-08T00:13:38Z — SoulSchoolAcademy.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Two evidence disciplines, one hour apart. First: five trial-derived Tier-1 packets were published on an exact branch — the publication blocker is **CLOSED** for those artifacts (exact hashes, exact branch, reproducible fetch). The independent audit's verdict was still **INCONCLUSIVE for production promotion**: the trial packet lacks a `learning_evidence.id`, live candidate-specific lineage/verdict, and matching dynamic-block authority; T11 stats and verification attribution were stale/mismatched versus the corrected #1786–#1789 review. So: **publication ≠ promotion evidence. The publication gate and the promotion-candidate evidence gate are different gates, and one does not close the other.** Second: a real live capture — idempotency key `coda1-capture-proof-20261007-003`, event `acc612d5-...`, VERIFIED receipt `5d89d7ca-...`, content hash `69df0519...` — proves REAL NOTE → CAPTURE → PERSIST → VERIFIED RECEIPT → HUB PROJECTION for that run (real row, not synthetic; outcome/learning remains UNKNOWN, as it should). But the auditor deliberately did **not** upgrade it to full-chain PROVEN: the last hop — independent retrieval/reread of the same object through the canonical retrieval path — was not yet independently proven from this evidence alone. The standing rule: **a proven chain is only as long as its proven hops; never upgrade partial-chain evidence, and never let one closed gate close another.**

## 🩷 HUMAN NOTE

Shawn, two sharp discipline moments tonight. First, the Tier-1 verification packets are now published with exact hashes — so that blocker is genuinely closed. But publishing is not the same as proving promotion-worthiness: the audit came back INCONCLUSIVE because the packet lacked live lineage and authority to promote, and some stats were stale. Second, we saw our first real live Smart Note capture go all the way NOTE → RECEIPT → HUB with a VERIFIED receipt — a real milestone — but the auditor refused to call the full chain proven until the last hop (independent retrieval of the same object) is independently re-read and hash-matched. Every hop proven, or the chain isn't proven. That's the standard holding.

## 👶 CHILD NOTE

Imagine you are building a paper chain with five links. You have glued four links shut and checked each one — but the fifth link is still open. The chain is NOT done, even though four-fifths of it is perfect. And there's another rule: handing someone the paper (publication) is not the same as proving the chain holds weight (promotion evidence) — two different tests, two different answers. Always test each link, and never let a pass on one test count as a pass on another.

## 👵 GRANDMA NOTE

Dear, this is about not jumping ahead. Two good things happened: we published the evidence packages so anyone can inspect them (that's one gate closed), and we watched a real note travel all the way through the system to the Hub (that's four hops proven). But in both cases we stopped exactly where the proof stopped — publishing is not promotion, and four proven hops is not a proven chain. You claim only what the evidence covers, link by link, gate by gate. Restraint in claiming is what makes the claims trustworthy.

## 🧠 NAYA NOTE

Cold successor: when you audit evidence, name each gate separately and close each only on its own proof. Publication gate = exact bytes available and hash-reproducible on the canonical surface (branch/PATH/commit). Promotion-candidate evidence gate = live candidate lineage (`learning_evidence.id`), candidate-specific verdict, matching dynamic-block authority, current attribution. A chain-proof (NOTE→CAPTURE→PERSIST→RECEIPT→HUB→RETRIEVE) is only complete when every hop is independently proven on the same object — hash/event/receipt match at each step; a hop proven on a different object or run does not transfer. If your audit returns INCONCLUSIVE, write the exact receipt (what was checked, what was missing) — an INCONCLUSIVE with a receipt is evidence; an INCONCLUSIVE without one is noise. Never upgrade; the next hop is always the next work.

## 🤖 MACHINE NOTE

```json
{
  "sn": "SN-0623",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INDEPENDENT-VERIFICATION",
  "doctrine": "Publication and promotion-evidence are different gates; a proven chain is only as long as its proven hops — never upgrade partial-chain evidence and never let one closed gate close another.",
  "family": "EVIDENCE-LAW / INDEPENDENT-VERIFICATION (SN-0518)",
  "evidence": ["#1354 comment 6049740378 (Tier-1 audit INCONCLUSIVE)", "#1713 comment 6049739334 (exact-hash receipt)", "#1354 comment 6049447227 (real live capture: event acc612d5, receipt 5d89d7ca, hash 69df0519)"],
  "falsifiers": [
    "A promotion claim based on published bytes that lack live candidate lineage/authority",
    "A full-chain PROVEN claim where any hop was proven on a different object/run",
    "A closed publication gate treated as closing the promotion-evidence gate"
  ],
  "applies_to": "all evidence-chain proofs and independent audits"
}
```
