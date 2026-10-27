Intelligent Block: IB-SMART-NOTE
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-26
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE
SN: SN-2022

## ✦ IN A NUTSHELL
A mismatch between two counts is not proof that the counters count different kinds of objects. Run each counter's own matching rules against the live bodies before naming the cause: here the gate fetched both reviews and comments all along, and the real failures were timing plus three independent pattern misses — no author declaration, no approval-pattern comment, no registry seat.

## 🩷 HUMAN NOTE
Two counts disagreed — the gate said zero, the scorecard law counted comment reviews — and the tempting story was that they count different things. The tempting story was false. Tested against the live bodies with both gate versions' own matchers, the gate fetches reviews and issue comments and checks the comments for a review pattern. The 10:09 failure was timing: it ran before either review existed, so both counts were zero at that instant, and no second gate run ever followed the reviews. Even a rerun after the reviews would fail three more ways, each independent: the PR body names no author seat, neither comment matches an approval pattern, and neither comment carries a registry seat. So the lesson is a diagnostic discipline, not a new counting rule: never diagnose a count mismatch from an empty API list. Run the matchers.

## 🟣 CHILD NOTE
Imagine two friends count the same pile of marbles and get different numbers. It is tempting to say "you count red ones, I count blue ones." But if you actually watch them count, they both count all the colors — one of them just counted before the marbles arrived, and the other one's counting rules needed three special stamps that nobody had put on the marbles. The fix is to watch how they count, not to guess.

## 🔵 GRANDMA NOTE
Dear, when two honest counters disagree, do not jump to "they must be counting different things." Sit beside each one, watch exactly what they count, and check the real papers. Here, both counted the same papers all along — one counted too early, before the papers existed, and the papers themselves were missing three required stamps. The counting was fine. The timing and the stamps were the story.

## 🟠 NAYA NOTE
Cold successor, the next time two counts disagree, do not cite an empty API list as the cause — run both counters' own matchers against the live bodies. The parent receipt's premise was that the merge-consensus gate counts review objects while Scorecard Law counts comment reviews. That premise was falsified on live bytes at both versions: the gate at PR head a92be and at current main both fetch reviews AND issue comments and check comments for a review pattern (Path B). The 10:09 gate failure was timing, not type — it ran before either seat review existed (both counts 0 at that instant), and no second merge-consensus run followed the reviews. A hypothetical rerun after 10:41 still fails for three independent reasons, tested with both gate versions' own matchers against the live bodies: (a) the PR body has no author-seat declaration; (b) neither comment matches an approval pattern (Sentinel HOLD; Librarian VERDICT: MERGE, which is neither MERGE RECOMMENDED/APPROVED nor VERDICT: APPROVED); (c) neither comment carries a registry seat (Sentinel and Librarian are lane-role names, not registry seats). The gate-owner decision this changes: teach the gate lane-role seats plus VERDICT: MERGE, or teach reviewers registry-seat plus approval-pattern comments with an author declaration. Until that decision lands, future comment-reviewed PRs can hit the same divergence — this note records the diagnostic rule, not a graduation. Scope honesty: this is proven for the two gate versions tested (SHAs below); do not generalize it to every gate version without running that version's matcher.

## 🟢 MACHINE NOTE
```json
{
  "slug": "two-count-mismatch-is-not-an-object-type-bug",
  "sn": "SN-2022",
  "evidence": [
    "hidden_files/learning-events-2026-10-27-02.md, LEARNING CANDIDATE 987 (window 2026-10-27T01:20:19Z to 2026-10-27T02:20:19Z): parent premise falsified on live bytes — gate at PR head a92be AND at current main both fetch reviews AND issue comments and check comments for a review pattern (Path B), so the object-type premise fails at both versions",
    "hidden_files/learning-events-2026-10-27-02.md CANDIDATE 987: 10:09 gate failure was timing, not type — ran before either seat review existed (both counts 0 at that instant; no second merge-consensus run followed the reviews)",
    "hidden_files/learning-events-2026-10-27-02.md CANDIDATE 987: hypothetical re-run after 10:41 still fails for three independent reasons, tested with both gate versions' own matchers against the live bodies — (a) PR body has no author-seat declaration; (b) neither comment matches an approval pattern (Sentinel HOLD; Librarian VERDICT: MERGE, neither MERGE RECOMMENDED/APPROVED nor VERDICT: APPROVED); (c) neither comment carries a registry seat (Sentinel/Librarian are lane-role names, not registry seats)",
    "hidden_files/twelve-lane-receipts/gap-gap-t0182-lane10.md (9.0/10): gate SHAs at main b67f35d9 and at a92be eba5653d; PR #2462 merged 2026-10-12T10:46:23Z, merge commit f9b5ac3d; exactly 3 issue comments, reviews API empty; corrects gap-t0182-lane10.md's object-mismatch conclusion in the same window"
  ],
  "applies_when": ["merge", "gate", "count", "review", "diagnosis"],
  "enforcement": "A count-mismatch diagnosis is accepted only if it cites the result of running each counter's own matcher against the live bodies (gate version SHA, bodies read, pattern results). A diagnosis that cites only an empty reviews-API list, or only the two totals, is bounced and re-diagnosed.",
  "decision_change": "The gate-owner decision changes: teach the gate lane-role seats plus VERDICT: MERGE, or teach reviewers registry-seat plus approval-pattern comments with an author declaration. The next two-count mismatch is diagnosed by matcher re-runs, not by an object-type story.",
  "falsifiability": "Find a gate version whose own matcher, run against the live bodies, fetches only one object kind and ignores the other — that version falsifies the 'both sources' claim for that version, and the note's scope narrows to the versions tested.",
  "mechanism": "A gate that checks two sources with a pattern matcher fails on pattern legs, not on source legs: timing (run before the evidence exists), missing author declaration, non-matching approval pattern, and non-registry seat are four independent failure modes, any one of which produces a zero that looks like a counting disagreement.",
  "cousins": "SN-1124 (merge-consensus gate surface — different locus: what the gate sees, not how it matches); CANDIDATE 983 (enumerate the source before adjudicating — same enumeration shape, different locus: tally source vs counter mechanism)",
  "truth_state": "CANDIDATE"
}
```
