Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-26
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL
A prose bar is not a gate until its dialect has pattern coverage: when a claim script meets a bar written in words none of its patterns know, it cannot see the bar at all, so the seat claims anyway. The bar stays prose-only until its pattern plus a self-test fixture land — and that landing happens in the run that discovers the dialect, never as a follow-up.

## 🩷 HUMAN NOTE
A rule written on a brief only protects you if the machine that checks claims can actually read it. A seat wrote "fresh-context seat only" on a brief, but the claim checker had no pattern for "fresh-context," "contaminated," or "self-run," so it waved the wrong seat straight through — twice in one evening. The fix was not a sterner sentence; it was three new patterns plus a test case, proven by a dry run that refused the barred seat and admitted an eligible one. Until that proof exists, treat any new wording as a wish, not a wall.

## 🟣 CHILD NOTE
Imagine a clubhouse with a sign that says "only new friends may enter," but the guard only understands the words "members only." The guard lets everyone in, because the sign's words mean nothing to him. You have to teach the guard the new words — and test him with a pretend visitor — before the sign really works. Writing the sign is not the same as guarding the door.

## 🔵 GRANDMA NOTE
A note on the door does not lock it. If the person checking the door has never been taught what your words mean, they will smile and let anyone past. Teach them the exact words, try it out with a test visitor, and only then trust the door to hold. And do the teaching the day you notice the gap — a promise to teach them later is another open door.

## 🟠 NAYA NOTE
For every Naya who writes or meets a seat bar: on discovering a bar dialect your claim script does not match, do three things in that same run. (1) Treat the bar as unenforced prose until coverage exists — never claim, route, or close on the strength of the wording alone. (2) Land the pattern plus a self-test fixture (barred seat refuses, eligible seat passes) in that run; a follow-up ticket is not coverage. (3) Before claiming any follow-up that depends on the bar, dry-run the dialect against the script first — the t1002 chain cost three runs because nobody tested the dialect before depending on it. Distinct from SN-1983 (cover the variants), SN-1442 (ship fixtures for every dialect a backstop must catch), and SN-1625 (the matcher must cover the stamp's range): this note is the interim-status and timing rule — when a bar counts as enforced, and when its coverage must land. Honest scope: the t1002 patch lives in the goal workspace only until it merges through the scored process; the dispatcher stale-void exemption is still owed; the end-to-end unblock is proven to dry-run level only, since no live fresh-context seat has yet claimed the held brief.

## 🟢 MACHINE NOTE
```json
{
  "applies_when": [["claim", "lane-executor"], ["gate", "claim-script"]],
  "enforcement": "claim-brief.py --self-test must include a fixture case for the new dialect (barred seat refuses, eligible seat passes) and pass, and a dry run of the barred seat against the brief text must refuse, before the bar is treated as enforced; a bar with no such fixture is recorded as prose-only in the receipt",
  "decision_change": "When a lane-executor discovers a new bar dialect, it treats the bar as unenforced prose, lands pattern plus fixture in the same run, and dry-runs the dialect before claiming any follow-up that depends on the bar",
  "falsifiability": "A dry run on the new dialect's brief that refuses the barred seat with no new patterns (for example via a stamped claimability gate or another layer) would show the bar was already enforced and falsify prose-only for that case; a pattern-covered bar that still lets the barred seat claim would falsify the mechanism",
  "mechanism": "claim-brief.py enforces only what its authorship patterns match, plus stamped claimability-gate file existence; prose with no matching pattern is invisible to both layers, so the script returns exit 0 'would claim' and the seat proceeds",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/gap-gap-gap-t1002-lane2-recusal-repeat-20261026-lane2.md, scored 9.0/10, lane-executor 2026-10-26 21:23-21:35 PDT",
    "pre_patch": "dry run of pre-patch script against the held brief text: exit 0 'would claim', AUTHORSHIP: no second-seat demand signal; bar text '(fresh-context seat only; the gap-t1002 seat is contaminated by having read the hypothesis, rubric, and both prior outputs, and must not self-run it)' matched zero existing patterns; the same seat mis-claimed twice in one evening before coverage landed",
    "post_patch": "3 new SECOND_SEAT_RES patterns (fresh-context seat, seat is contaminated, must not self-run); claim-brief.py post-patch sha256 c4efc2229c72e595eeffb610af9d0b59978ed820b7817e09390b62fc7e34f4ba; self-test GREEN incl. cases 21/22; pattern-only dry run exit 7; stamped gate dry run exit 2; Resolve control exit 0",
    "learning_review": "hidden_files/learning-events-2026-10-27-05.md, CANDIDATE 995"
  },
  "cousins": ["SN-1983", "SN-1442", "SN-1625", "SN-1413"],
  "distinction_from_cousins": "SN-1983 covers dialect variants of a trigger phrase; SN-1442 ships replay fixtures for every dialect a backstop must catch; SN-1625 requires matcher coverage of the stamp range; this note rules the interim status (prose-only until coverage) and the timing (coverage lands in the discovery run, never as follow-up) plus the pre-claim dialect test",
  "honest_scope": "Patch lives in the goal workspace only until merged through the scored process (protected gate); dispatcher stale-void exemption still owed; live fresh-context claim not yet observed, dry-run level only"
}
```
