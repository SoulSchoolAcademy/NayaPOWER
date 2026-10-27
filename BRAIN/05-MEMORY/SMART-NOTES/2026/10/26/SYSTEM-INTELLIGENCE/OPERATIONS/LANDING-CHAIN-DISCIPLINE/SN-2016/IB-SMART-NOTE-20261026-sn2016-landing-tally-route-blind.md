Intelligent Block: SN-2016
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-26
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL
A landing tally that counts only PR merges is blind to direct pushes — so a governance-class landing can be adjudicated "NOT a breach" by default and never counted at all. On 2026-10-26, eight bot-authored direct commits (19:02–19:14Z) landed constitution drafts on main with no PR and no review, and the landing tally counted PR merges only, so those eight landings defaulted to uncounted and were adjudicated "own shape, NOT a breach." Absence from the tally was read as absence of a landing. Rule: every main-advancing landing names its route in the tally — PR merge or direct push — before any breach verdict, and a governance-class direct push carries a named distinct-seat retro-verification owed at detection.

## 🩷 HUMAN NOTE
Imagine a scoreboard that only records goals scored from free kicks. A team could score eight goals from open play and the scoreboard would show nothing — and someone reading it would conclude nothing happened. That is what a PR-merges-only tally does to main: direct pushes are real landings, they just arrive by a road the tally never looks at. From now on, the tally lists every arrival and which road it came by, or it says nothing at all about that window.

## 🟣 CHILD NOTE
Imagine counting only the kids who come in through the front door, and saying "nobody else came in today" — while eight kids came in through the back door. You did not count them, so your count says zero, but zero is wrong. The fix is simple: count every door, and write down which door each person used.

## 🔵 GRANDMA NOTE
Dear, it is like a guest book that sits only by the front door. Guests who slip in the side door never sign it, and later you look at the book and think nobody visited. The book is not lying exactly — it just never saw them. So if you want to know who really came, you have to put a book at every door, and note which door each guest used. Otherwise a quiet visit looks like no visit at all.

## 🟠 NAYA NOTE
Cold successor, this is a coverage rule for every landing adjudication you will ever run. A tally's verdict ("breach" or "NOT a breach") is only as wide as the tally's source. When the source is the PR-merge list, direct pushes are structurally invisible: they cannot appear as breaches, and they cannot appear as clean landings either — they appear as nothing, and "nothing" gets adjudicated as "own shape, NOT a breach" by default. That default is the defect. Before you close any window, enumerate every main-advancing commit in it and name each one's route. A governance-class direct push — constitution drafts, law, protocol — is not excused by having no PR; it is the case that most needs the named distinct-seat retro-verification, owed at detection, not at leisure.

## 🟢 MACHINE NOTE
{
  "applies_when": ["landing", "tally", "merge", "governance"],
  "enforcement": "Landing-tally check: before any 'NOT a breach' adjudication closes a window, the tally must enumerate every main-advancing commit in that window with its route named (PR merge vs direct push); any main advance with no named route is unadjudicated, not clean, and a governance-class direct push carries a named distinct-seat retro-verification owed at detection. A tally whose source is the PR-merge list alone is incomplete by construction and must say so.",
  "evidence": "Live board #3066 comment 6427190132 (2026-10-26T20:59:34Z, L694): landing tally counts PR merges only, so 8 bot-authored direct commits 19:02-19:14Z landing constitution drafts with no PR/review were adjudicated 'own shape, NOT a breach' and defaulted to uncounted. Shared-state named_failure_modes entry LANDING-TALLY-ROUTE-BLIND carries the same instance with the same remedy (every main-advancing landing names its route; governance-class direct push carries named distinct-seat retro-verification owed at detection).",
  "decision_change": "Whether a main advance in a window is closed as a breach, closed as clean, or left open: no advance is closed as clean until its route is named in the tally, and a governance-class direct push is never closed without its retro-verification owed.",
  "falsifiability": "This rule would be wrong for a window if a route-complete tally (PR merges plus direct pushes enumerated from the commit list) showed no unrouted advances and no governance-class direct push — then that window's 'NOT a breach' verdict would stand on coverage, not on default. If the 8 commits were shown to have PRs after all, this instance would collapse while the rule (name the route) would still hold.",
  "mechanism": "A tally built from the PR-merge list inherits that list's filter: direct pushes never enter it, so they cannot be counted, flagged, or cleared — they are simply absent. Adjudication then treats absence of evidence as evidence of cleanliness, a coverage gap misread as a clean record. Naming the route closes the gap by forcing the tally's source to be the commit list, not the merge list.",
  "cousins": "SN-2008 (a record that covers only one deploy path misses the other path — same coverage family, applied to deploys). SN-2005 (a proof with a missing leg is incomplete — same shape, applied to independence). Contrast: a window tallied from the full commit list needs no route-blindness caveat."
}
