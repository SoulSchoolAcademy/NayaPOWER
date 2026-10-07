# A Drift Count Without Its Counting Method Is Not a Number

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0165-drift-counts-carry-counting-method
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-02
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5945494828 (2026-10-02T04:15:36Z, [NAYA][DESIGN MASTERY LOCK-IN + NOT-RIGHT FINDING]) reports BRAIN index drift as actual `05-MEMORY = 27` vs expected ledger `05-MEMORY = 23`, and notes the old repair PR #1301 (closed/unmerged) was scoped to "the older 21→23 reality." #554 comment 5945708739 (2026-10-02T04:39:42Z, [NAYA 2] build-loop 21:36Z note) reports the same drift class as real count **25 (non-report)** vs ledger **21**, with repair PR #1314 (`brain-build/index-domain-count-05memory-25`, `7ec766a023e9d964101c9ba08304e450dadbdf65`, base frozen `ae2fd838`) as the deliberate ledger bump 21→25, byte-verified 4/4, `--check` clean, 546/546 on exact branch bytes. The two number pairs were produced by unstated/unstatedly-different counting methods; the repair-PR supersession question (does #1314 supersede #1301's scope?) cannot be answered until the methods reconcile. Open reconciliation item for the lanes: state raw vs non-report-excluded counts, the ledger pin, and the partition before comparing drift numbers.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Two lanes measured the same brain-index drift and produced two different number pairs: 27-actual/23-expected vs 25-(non-report)-actual/21-expected. The difference is not a disagreement about the world — it is unstated counting methods (raw file count vs non-report-excluded count; which ledger pin; which partition). Naya 2's #1314 is the canonical single repair green on the current tip (`ae2fd838`) with exact bytes proven; Naya 4's 27/23 pair was measured against a different counting method. Until the lanes state their methods side by side, the repairs cannot be compared and the "does #1314 supersede #1301" question cannot be answered. The rule: a drift number travels with its method — report actual vs expected **and** raw vs excluded, the ledger pin, the base SHA — or the number is not comparable, and incomparable numbers in two lanes' reports become phantom disagreements. Cousin map: SN-062 (the count ledger is part of the change) governs *updating* the ledger; SN-078 (regen + deliberate bump on merge) governs *keeping* the ledger; this governs *reading* the ledger — a count whose method is unstated cannot be compared across lanes.

## 🩷 HUMAN NOTE

Shawn — one measurement lesson from the brain-index drift work tonight. Two lanes both measured the same thing — how far the 05-MEMORY index has drifted from its ledger — and reported two different answers. One said the real count is 27 and the ledger expects 23. The other said the real count is 25 and the ledger says 21. Both are careful workers, so the gap isn't carelessness: it's that neither stated *how* they counted. One counted non-report files only, the other apparently counted raw; they were reading different ledger pins. A number without its counting method is like a score without saying what game was played — you can't compare two scores from two different games. The fix is mechanical: whenever a lane reports a drift count, it must also report the method — raw or excluded, which ledger pin, which base SHA. Until then, the lanes literally cannot answer "does this repair supersede that one?" because they're comparing apples to oranges. Naya 2's repair PR #1314 is the verified current-tip repair; the lane comparison just needs the methods written down first.

## 🟣 CHILD NOTE

Imagine two friends counting the cookies in a jar. One counts 27, the other counts 25. Are they disagreeing? No! One counted the cookies *and* the crumbs on the lid; the other counted only the cookies. If neither says how they counted, they argue forever about nothing. That's what happened with the brain-index count tonight: two lanes counted the "smart note" files and got different numbers because they counted differently (one excluded report files, the other didn't, and they looked at different "expected" numbers). The rule: always say HOW you counted when you give a number. "27 cookies including crumbs" and "25 cookies, crumbs not counted" — then both answers are true, and nobody argues.

## 🔵 GRANDMA NOTE

It's like two neighbors arguing about how many trees are on the street. One counted every sapling and stump; the other counted only the mature trees. Both counted honestly — they just counted different things, and neither said so. Two of the team's lanes did the same thing tonight with the brain's index ledger: one said the real count is 27, the other said 25 — because one included report files and the other excluded them, and they were reading different ledger numbers. The lesson for any record-keeper: a number is only useful if it carries its recipe. "25, excluding report files, against ledger pin 21, on base SHA ae2fd838" is a fact. "25" alone is a riddle. And two riddles from two lanes look like a disagreement when they're really just two recipes. Write the recipe with the number, every time.

## 🟠 NAYA NOTE

Apply this to every index-drift / count-ledger report: (1) report the method with the number — raw count vs exclusions (non-report files, partitions), the ledger pin (EXPECTED count), and the base SHA the count was taken on; (2) when two lanes produce different pairs, first check method-vs-method before treating it as a factual disagreement — unstated methods produce phantom conflicts; (3) a repair PR's scope (e.g., #1314's 21→25) is bound to its counting method — do not compare repair scopes across methods; (4) canonicalize the method lane-to-lane once (non-report-excluded, ledger pin, base tip) and write it into the merge checklist so every future count is comparable; (5) until methods reconcile, keep the repair with exact-byte evidence on the current tip (#1314: 7ec766a0, `--check` clean, 546/546) as the working repair and the other count as an unverified alternate, not a contradiction.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "method-unstated drift counts (two lanes report different actual/expected pairs for the same index drift; counting methods — raw vs non-report-excluded, ledger pin, base SHA — unstated, so repairs are not comparable and supersession cannot be decided)",
  "evidence": {
    "board": "#554 5945494828 (2026-10-02T04:15:36Z) — 05-MEMORY actual 27 vs expected ledger 23; old repair #1301 closed/unmerged, scoped to 'the older 21→23 reality'. #554 5945708739 (2026-10-02T04:39:42Z) — build-loop note: real count 25 (non-report) vs ledger 21; repair PR #1314 (brain-build/index-domain-count-05memory-25, 7ec766a023e9d964101c9ba08304e450dadbdf65, base frozen ae2fd838), deliberate ledger bump 21→25, byte-verified 4/4, --check clean, 546/546 on exact branch bytes; #1251 closed-unmerged on stale base 42c8f594; #1314 single canonical repair on current tip.",
    "open_item": "lanes have not yet reconciled counting methods; drift-count methodology (raw vs exclusions, ledger pin, base SHA) awaits lane-to-lane canonicalization"
  },
  "rule": [
    "a drift count must carry its counting method: exclusions (raw vs non-report-excluded), the ledger pin, and the base SHA — a bare number is not comparable across lanes",
    "treat differing number pairs as a method question first, a factual disagreement second — unstated methods manufacture phantom conflicts",
    "a repair PR's scope is bound to its counting method; never compare repair scopes across unstated methods; keep the exact-byte-verified current-tip repair as the working repair until methods reconcile",
    "canonicalize the counting method lane-to-lane once and write it into the merge checklist"
  ],
  "lesson_line": "A drift count without its counting method is not a number: report exclusions, ledger pin, and base SHA with every count, or two lanes' repairs become incomparable and supersession unanswerable."
}
~~~
