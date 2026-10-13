# Never Close What You Cannot Prove Superseded — the Byte-Level Close Bar

**Intelligent Block:** IB-SMART-NOTE-20261012-sn1085-never-close-what-you-cannot-prove-superseded
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Lane 1 (Naya Verity) ran the t0302 close batch against the byte-level bar: the 10 oldest PRs three-dot-compared vs the live tip, the 6 smallest-diff candidates blob-compared head-vs-tip, 200 branch refs verified present on origin, 300 PRs draft-scanned. Zero met the supersession bar. She closed 0 — and that was the correct result, reported as a completed batch. Closing is an irreversible write; age and appearance are not proof. The bar for closing is byte-level proof that the work is superseded, never "it looks old."

## 🩷 HUMAN NOTE

Imagine a librarian clearing the shelves who throws out every book with a worn cover. The shelf looks tidy — and three months later someone needs the exact book she tossed, the one that was still the only copy. The fix isn't "never clean"; it's "prove the book is elsewhere before you bin it." Lane 1 did exactly that: she checked every candidate against the live shelf, found none provably duplicated, and closed nothing. A tidy-looking zero closed beats a tidy-looking ten destroyed.

## 🟣 CHILD NOTE

Don't throw it away unless you can prove nobody needs it. "It looks old" is not proof.

## 🔵 GRANDMA NOTE

A clean desk is nice. An empty drawer where the rent money used to be is not. Throw away only what you can prove is a copy.

## 🟠 NAYA NOTE

Closing composes with the "writes are real" family: a close is a write, and like every write it needs evidence before it happens. It also bounds the no-bottleneck law's 5-minute test — doing it yourself beats waiting, but closing wrong destroys work that cost someone days; the cost of a wrong close always exceeds the cost of closing later. The honest close-0 is the mechanism working: the bar exists to protect the queue's contents, not to pad the queue's stats. Lane 1's batch is the reference procedure: three-dot vs tip (divergence check), blob comparison head-vs-tip (at least one differing file = not superseded), ref presence on origin, draft scan with the one protected exception (#1130, awaiting Shawn) named explicitly.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "close_bar": "byte-level proof of supersession: three-dot compare vs live tip + blob comparison head-vs-tip + branch-ref presence on origin",
  "anti_pattern": "closing on age, appearance, smallness of diff, or 'probably merged'",
  "rule": "close-0 with evidence is a completed batch; close-N without proof is data loss",
  "protected_exceptions": "name them explicitly (e.g. awaiting the director's word) — never silently skipped, never silently closed",
  "canonical_object": "INTELLIGENT_BLOCK"
}
~~~

## 🟢 LEARNING LESSON

The temptation in queue discipline is to measure progress by closures. The correct measure is closures that were provably safe. A batch that closes nothing because nothing was provable is not a wasted batch — it is the discipline holding under pressure to "just clean it up."

## 🟡 WHAT IT MEANS

Every close is a judgment call with irreversible consequences, so the evidence bar must match the irreversibility. Age, small diffs, and "someone probably merged this" are guesses — and the Judgment Rule says intelligence never guesses. The byte-level bar turns closing from opinion into measurement.

## ⚪ WHAT'S IN IT FOR YOU

A queue that shrinks without losing work. When every close carries its byte-level proof, a cold successor can audit any closure and confirm it was safe — or reopen it with the evidence still attached.

## 🟨 HOW TO APPLY / HOW TO USE

When clearing stale PRs or branches: (1) three-dot-compare each candidate vs the live tip; (2) blob-compare head-vs-tip for the smallest diffs (any differing file = not superseded); (3) verify branch refs exist on origin; (4) name protected exceptions explicitly; (5) close only what passes all checks — and report the close-0 honestly when nothing does.

## 🔗 HOW IT CONNECTS

- **COMPOSES WITH** → SN-0484 — writes are real; a close is a write and needs evidence first
- **BOUNDS** → the no-bottleneck 5-minute test — speed never outranks the cost of a wrong close
- **PREVENTS** → silent data loss from age-based cleanup

## 🧭 KEY DECISIONS / PRINCIPLES

- Never close what you cannot prove superseded.
- Byte-level proof or it stays open: three-dot + blob comparison + ref presence.
- A correct close-0 is a completed batch, not a failed one.
- Protected exceptions are named, never silently skipped or closed.

## 🧾 PROOF / PROVENANCE

~~~json
{
  "board": "SoulSchoolAcademy/NayaPOWER#2175",
  "comment_id": 6124655144,
  "comment_kind": "lane-verdict/verification",
  "event": "Naya Verity (Lane 1, Verification) t0302 close batch: 10 oldest PRs three-dot-compared vs tip f9b5ac3de34d3cafa0718b20458289539e11b685 (all diverged), 6 smallest-diff candidates blob-compared head-vs-tip (every one differs in >=1 file), 200 branch refs all present on origin, 300 PRs draft-scanned (only #1130 awaiting Shawn + 2 recent active) — zero met the byte-level supersession bar, closed 0",
  "owner": "Naya 1 (Lane 1, Verification)"
}
~~~

## ⚠️ TRUTH BOUNDARY / UNCERTAINTY

The finding is Lane 1's t0302 verdict on the live tip at 2026-10-12 ~12:53 UTC, using her stated byte-level procedure. The doctrine is the general lesson (close bar = byte-level proof), independent of this batch's specific candidates.

## ➜ NEXT ACTION / SUCCESS CONDITION

Use the byte-level bar on every future close batch. Never let closure count become the metric — provable safety is the metric.
