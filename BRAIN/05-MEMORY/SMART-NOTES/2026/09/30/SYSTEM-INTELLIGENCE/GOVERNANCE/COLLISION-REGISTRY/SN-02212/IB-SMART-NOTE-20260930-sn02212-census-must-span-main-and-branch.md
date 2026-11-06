# A Number Census That Checks Only Main Is Blind to the Branch — Check Main and the Staging Branch Before Claiming a Number Free

**Intelligent Block:** IB-SMART-NOTE-20260930-sn02212-census-must-span-main-and-branch
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Main-seat breach verifications 2026-11-06 (memory log, breach #221 / #224 sections): PR #3260 and PR #3263 both collided with branch-staged notes their main-only censuses never saw. Smart-note distillation tick 2026-11-06 12:08 PST.

## ✦ IN A NUTSHELL

On 2026-11-06 two Smart Note numbers collided on the same day by the same mechanism. The #3260 census covered only main's commit graph, not the staging branch — but the branch already held a different SN-2203 (hourly-report-score-join, staged 2026-11-05 22:08, commit 31b15e16), so main's "exactly one SN-2203 entry, no collision" was true of main and false of the system. Hours later PR #3263 repeated it: main SN-2204 (Ten Learnings in Action) vs branch SN-2204 (wave-variable-typo-burn, staged 2026-11-05 23:08, commit edaf6ce9). A census confined to main is blind to exactly the numbers most likely to collide — the ones staged most recently, which live on the branch and have not landed yet. The rule: a number is free only when the census spans main AND the staging branch; a main-only "no collision" is an unproven claim, not a finding.

## 🩷 HUMAN NOTE

Shawn — imagine two people filing the same numbered folder, one in the main cabinet and one in the in-tray, and the checker only opens the main cabinet and reports "no duplicate." That is what happened twice today: the merge records claimed SN-2203 and SN-2204 were free because they checked only main, while the staging branch already held a different note under each number. The fix is one line in the check: always look in both places — main and the staging branch — before calling a number free. The branch is where the newest numbers live, so it is exactly where a collision hides.

## 🟣 CHILD NOTE

Think of two toy boxes: the big one in the living room and the small one by the door where new toys go first. If you only look in the big box and say "no toy like this one," you might miss the same toy sitting in the small box. Before you say a number is free, look in both boxes — the big one and the small one by the door.

## 🔵 GRANDMA NOTE

Dear, it is like checking whether a name is already taken by looking only in the phone book, when the newest names are still written on the notepad by the telephone. The phone book is last month; the notepad is today. You must check both, or you will give two grandchildren the same name. Main is the phone book; the staging branch is the notepad by the phone. Check both before you call a number free.

## 🟠 NAYA NOTE

For every seat that claims a Smart Note number is free, or that verifies such a claim: (1) run the census in BOTH scopes — main's registry (or commit graph) AND the staging branch tip (git ls-remote / branch log on naya4/smart-notes-2026-09-30); a census that names only one scope is incomplete and its "no collision" is unproven; (2) remember WHY the branch matters: staged notes land on the branch first and reach main later, so the freshest numbers — the ones a new claim is most likely to hit — exist only on the branch; (3) when a collision is found, first claim stands and the later note renumbers — never silently overwrite, never leave two notes sharing a number; (4) the branch SN-2204 (wave-variable-typo-burn, edaf6ce9) still needs renumbering after collision #23 — the renumber is owed, not optional; (5) this is the sibling of SN-1650 (pin the PR's state before pinning its head): a claim about state is only as good as the scope it was checked against.

## 🟢 MACHINE NOTE

```json
{
  "applies_when": [
    ["claim", "number-census"],
    ["collision", "smart-note-number"],
    ["merge", "receipt"]
  ],
  "canonical_object": "INTELLIGENT_BLOCK",
  "claim_boundary": "This note governs number-freedom claims for Smart Notes only: it does not claim main-only censuses are useless elsewhere, only that for Smart Note numbers the staging branch is a live claim scope. It does not retroactively void the collided landings — collisions #22/#23 stand as breach records; the cure is renumbering the branch note.",
  "decision_change": "Before claiming a Smart Note number free — or verifying such a claim — the seat censuses both main's registry and the staging branch tip; a main-only 'no collision' is treated as unproven and blocks the claim until the branch scope is checked.",
  "enforcement": "The distillation loop's pre-stage check (stage_smart_note.py claim check plus the loop's own branch-tip scan) fails closed when either scope is unreadable, and refuses a number already claimed on the branch; a PR-body census is rejected as evidence unless it names both scopes (main registry + staging branch tip).",
  "evidence": [
    "PR #3260 (SoulSchoolAcademy/NayaPOWER), merged 2026-11-06T16:49:12Z, 16s open, 0 reviews; its census covered only main's commit graph, not the branch; the twin's filing check at pin cb61c7d1 reported 'exactly one SN-2203 entry, no collision' — scoped to main's registry only — while the branch already held a different SN-2203 (hourly-report-score-join, staged 2026-11-05 22:08, commit 31b15e16). NUMBER COLLISION #22 (main-seat verification + correction, 2026-11-06 memory log, breach #221 section).",
    "PR #3263, merged 2026-11-06T19:44:12Z, 69s open, 0 reviews; body (1,607 chars) repeated the hole: main SN-2204 (Ten Learnings in Action) vs branch SN-2204 (wave-variable-typo-burn, staged 2026-11-05 23:08, commit edaf6ce9). NUMBER COLLISION #23 (main-seat verification, 2026-11-06 memory log, breach #224 section).",
    "Branch tip e952c1c9 (SN-2211) verified live this tick via git ls-remote; branch holds SN-2203 and SN-2204 under different lessons than main's SN-2203/SN-2204."
  ],
  "falsifier": "The rule is refuted if the staging branch stops being a live claim scope — i.e., if notes land on main the same instant they are staged, so no number can exist on the branch but not on main. Until then, any main-only census that misses a branch claim confirms it.",
  "intelligence_class": "LESSON",
  "mechanism": "Staged notes live on the branch before they land on main, so the newest numbers exist only on the branch; a census confined to main's commit graph cannot see them. The freshest numbers are the most likely collision targets, so a main-only census is blind precisely where collisions hide.",
  "related_notes": ["SN-1650", "SN-022", "SN-033", "SN-0189"],
  "truth_state": "CANDIDATE"
}
```
