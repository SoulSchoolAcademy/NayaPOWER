**Intelligent Block:** IB-SMART-NOTE-20260930-sn2651-renumber-into-occupied-check-occupancy-first
**Smart Note:** SN-2651
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-09
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Main-seat window verification 2026-11-09 ~20:20/20:46 PST (memory 2026-11-10.md, windows BF/BG), re-verified first-hand this tick from the commit record at main tip 7b54c435 (git protocol; ls-remote + fetch 2026-11-10T07:38Z): six renumber commits each naming the first-filed occupant of its destination. Main-tree occupancy re-checked this tick: SN-2648 = 2 files, SN-2650 = 2 files (collisions #71/#73 still open); SN-2651 verified absent on main (0 matches) and on branch naya4/smart-notes-2026-09-30 (max SN-2294).

## ✦ IN A NUTSHELL

Every renumber in two verification windows landed in an occupied number — six out of six. World Masters SN-2640 → SN-2644 (notification-answers first-filed 03:16:40Z); master-manual SN-2644 → SN-2645 (D3 first-filed 03:38:32Z); master-manual SN-2645 → SN-2647 (Team Activation first-filed 03:46:10Z); Supabase SN-2645 → SN-2648 (Ultimate Team first-filed); master-manual SN-2647 → SN-2650 (Wake Flow first-filed 04:04:02Z); World Masters SN-2646 → SN-2650. Each renumber cured its source collision and opened a new one at the destination, and the last commit in the window (7b54c435) was still deleting a duplicate copy left behind at SN-2649. The rule: check destination occupancy in the live landing tree immediately before the renumber commit — a number picked from a stale estimate, a "next safe" guess, or the local counter is not a check. Post-hoc uniqueness verification catches the new collision, but it does not prevent it; the cure that is not occupancy-checked is a collision with a delay.

## 🩷 HUMAN NOTE

Shawn — this one is about moving house into a house someone already lives in. Six times in one night, a note was moved to fix a collision — and six times, the new number already had a note sitting in it, because nobody knocked on the door first. The mover picked a number that looked free from an old list, while the real tree had already filled it. The fix is one knock: before you move a note, look at the live tree and confirm the destination number is empty, right then, right before the move. An old list is not a look. The counter on disk is not a look. Only the live tree is a look — and the look has to happen at moving time, because another note can move in between your check and your commit.

## 🟣 CHILD NOTE

Imagine you have two toy boxes with the same number on them, and you fix it by moving one toy to a new box — but you do not look inside the new box first, and there is already a toy in there. Now you have two toys in the new box, and you have to move one again. That happened six times in a row. The fix is simple: always peek inside the new box before you put your toy in it. Peeking yesterday does not count, because someone might have put a toy in since then. Peek right before you move, every single time.

## 🔵 GRANDMA NOTE

Dear, this is the rule about not moving the furniture into a room that is already full. A note had the wrong number, so someone moved it to a new number — but they chose the new number from an old list instead of walking over and looking at the shelf. Six times the shelf already had a note on it, so the move made a second mess while fixing the first. The standing rule is plain: before any move, walk over and look at the shelf with your own eyes, at that very moment. An old list cannot tell you what is on the shelf now, and a guess is not a look. Look first, then move — and the mess stops making more mess.

## 🟠 NAYA NOTE

This is a failure-mode lesson about the cure, not about identity — keep it distinct from SN-0524, which prescribes renumbering as the collision cure ("retain both, renumber the non-owner, verify uniqueness"). SN-0524 is about which object keeps the number; this note is about how the new number is chosen, and the evidence is that SN-0524's post-hoc "verify uniqueness" did not prevent a single one of the six bad landings: every renumber in windows BF/BG (2026-11-10 03:38–04:30Z) was verified against the live tree afterwards and still needed another cure. The mechanism has two legs. First, staleness: the number is picked from a stale estimate — the local counter sat at SN-2539 while main had already run to SN-2650, and the staging branch sat at SN-2294 — so "next free" from any local record is fiction. Second, race: filings land through the direct-write door between number selection and the renumber commit (Wake Flow filed SN-2647 at 04:04:02Z; the master-manual renumber into SN-2650 and the World Masters renumber into SN-2650 both landed after occupants were already there). The guard therefore has to run against the live landing tree (main, not the branch — the staging script's claim check is branch-scoped and would not have caught any of these) and immediately before the commit; a check run minutes earlier is already stale. Honest holes, stated not hidden: the six instances are verified from commit messages and the live tree at tip 7b54c435, but no second seat has reviewed this distillation yet; the occupancy check itself is a named verification step, not yet a script — graduation to a pre-renumber gate script is still owed. Cousins, kept distinct: SN-0524 (renumber as cure + verify uniqueness — the what, not the how of target choice); the staging script's branch claim check (same idea, wrong tree — it guards the staging branch, not the landing tree).

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-2651",
  "slug": "renumber-into-occupied-check-occupancy-first",
  "title": "Renumber-into-occupied: every renumber in two windows landed in an occupied number — check destination occupancy in the live landing tree immediately before the renumber commit",
  "observation": false,
  "applies_when": ["collision", "renumber", "smart-note", "identity", "registry", "uniqueness"],
  "enforcement": "Before any renumber commit, run a live-tree occupancy check for the destination number against the LANDING tree (main: git ls-tree / tree lookup for /SN-<n>/ must return empty) immediately before the commit. A number taken from the local counter, a stale estimate, or 'next safe' guess is not a check and is refused. The staging script's claim check is branch-scoped only and does not satisfy this — the mover must check main itself. After landing, the collision sweep re-verifies uniqueness; any renumber whose pre-commit occupancy check is missing or stale is treated as an unproven cure and re-checked, not assumed good.",
  "evidence": "Main tip 7b54c435 (2026-11-10 04:30:17Z), verified first-hand this tick by git ls-remote + fetch. Six renumber commits, each naming the first-filed occupant of its destination: a16e4bdfcd World Masters SN-2640 -> SN-2644 (notification-answers first-filed 03:16:40Z); ed685e1198 master-manual SN-2644 -> SN-2645 (D3 first-filed 03:38:32Z); 5dcea7e570 master-manual SN-2645 -> SN-2647 (Team Activation first-filed 03:46:10Z); 68a6da2f26 Supabase SN-2645 -> SN-2648 (Ultimate Team first-filed); 885f9dbf53 master-manual SN-2647 -> SN-2650 (Wake Flow first-filed 04:04:02Z); 3a29bc286f World Masters SN-2646 -> SN-2650. Window-closing commit 7b54c435 deletes the duplicate master-manual copy at SN-2649 (Take It first-filed 04:17:30Z). Live-tree check this tick: SN-2648 = 2 files, SN-2650 = 2 files (collisions #71/#73 still open). Counter staleness measured this tick: local counter last line SN-2539, staging branch max SN-2294 (last commit 2026-11-08), main max SN-2650 — SN-2540 already exists on main (2026/11/09/DESIGN/SN-2540), so the counter number would itself have collided.",
  "decision_change": "Any future collision cure by renumber must run a live-tree occupancy check on the destination number against main immediately before the renumber commit; the renumber is not executed on a counter number, a stale estimate, or a branch-only check. A renumber proposed without that check is refused until the check is run.",
  "falsifier": "The lesson is refuted if a renumber executed with a live-tree occupancy check run immediately before the commit still lands in an occupied number (the check would then be shown insufficient, e.g. a race inside the check-to-commit window), or if the six instances are shown to have had their destinations verified empty at commit time (the occupancy, not the check, would then be the wrong mechanism). It weakens if a future renumber without the check lands cleanly by luck — a single clean landing does not refute the base rate, but a run of clean unchecked landings would.",
  "cousins": ["SN-0524 (renumber as collision cure + verify uniqueness — prescribes the cure, not how the target number is chosen)", "stage_smart_note.py branch claim check (same occupancy idea, branch-scoped — guards the staging branch, not the landing tree)"],
  "captured": "2026-11-09",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE"
}
```
