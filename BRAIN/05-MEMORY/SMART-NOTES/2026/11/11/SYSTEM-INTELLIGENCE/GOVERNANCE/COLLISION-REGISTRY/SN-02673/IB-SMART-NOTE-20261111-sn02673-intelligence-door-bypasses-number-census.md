**Intelligent Block:** IB-SMART-NOTE-20261111-sn02673-intelligence-door-bypasses-number-census
**Smart Note:** SN-2673
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Staged by the smart-note distillation loop 2026-11-11 16:08 PST. Evidence: main tip 786acf83 (git ls-remote + live-main tree census this tick: max SN 2671, 1,619 SN paths) — door filings ecb95bf8e (SN-2670 "The Discipline Is the Machine", 2026-11-11T23:23:47Z) and 786acf83e (SN-2671 "Daily Intelligence Report 2026-11-11", 23:26:25Z), no PR, no board comment; branch stagings SN-2670 (retrieval-format lesson, 10:38) and SN-2671 (rubric-change lesson, commit 65f30e4d, 15:38) under the same numbers; LEARN ingest run 20261112T000827Z ingested branch SN-2671 into lessons.md, so the learn ledger now holds SN-2671 = rubric lesson while main holds SN-2671 = daily report. Number census this tick: live main max SN-2671, branch counter max SN-2672; next free number SN-2673 verified on both.

## ✦ IN A NUTSHELL

The intelligence door is a fourth claim channel for Smart Note numbers, and the census every staging run is told to use cannot see it. Door filings land straight on main with no pull request and no board comment — so a board-plus-open-PR check, and stage_smart_note.py's CLAIM CHECK, which reads only the branch tree, are both structurally blind to them. On 2026-11-11 it bit twice in one day: main took SN-2670 and SN-2671 by door filing while the branch already held SN-2670 and SN-2671 with different content, and the branch SN-2671 was even ingested into lessons.md after main took the number — so the learn ledger now holds a conflicting SN-2671. The fix is mechanical, not social: before taking a number, read live main's tree (git ls-remote HEAD plus ls-tree — zero REST quota). A number check that cannot see the door will keep colliding with it.

## 🩷 HUMAN NOTE

Shawn — two Smart Notes collided today, twice, and it's not carelessness — it's a blind spot in the checker. Notes filed through the fast door go straight onto main with no pull request and no board post, so the usual check (look at the board, look at open pull requests) literally cannot see them. The branch took numbers 2670 and 2671 for its own notes, and main took the same two numbers for different notes through the door — and one of the branch notes was already copied into the learning record under the taken number. From now on, before any note takes a number, we read main itself — the live tree, not the board — because main is the only place all four roads meet. First claim stands: main's numbers stand, the branch renumbers.

## 🟣 CHILD NOTE

Imagine four doors into the same classroom, and the teacher only watches three of them when handing out seat numbers. Two kids walk in through the fourth door and sit in seats that already have name tags — same seat, different kid. That's what happened today: the fast door onto main doesn't leave a note on the board or open a pull request, so the checker that only looks at those two places never saw the seats get taken. The fix is simple: before handing out a seat number, look at the classroom itself — count the seats that are actually taken — instead of only checking the sign-up sheets by the other doors.

## 🔵 GRANDMA NOTE

Dear, two of our notes ended up sharing the same number today, and it's nobody's fault — it's a hole in how we check. There's a fast lane that puts notes straight onto the main record without any announcement, no pull request, no board post. The checker only looks at the announcements, so it never saw those two numbers get used. One of the branch notes even got copied into the learning book under a number the main record already owned for a different note. The cure is plain: before giving a note its number, look at the main record itself — the real list of what's taken — every single time. The board and the pull requests are not the whole story.

## 🟠 NAYA NOTE

The verified facts: (1) Live main tip 786acf83 (verified this tick by git ls-remote, matching the 16:08 main-tip-watchdog): the main tree holds 1,619 SN paths, max SN-2671. (2) The two door filings: commit ecb95bf8e, 2026-11-11T23:23:47Z, SN-2670 "The Discipline Is the Machine", page +50; commit 786acf83e, 23:26:25Z, SN-2671 "Daily Intelligence Report 2026-11-11", page +63. Both single-parent nayapower-lane-agent[bot], zero associated PRs, zero board comments — the door channel by design. (3) The branch held SN-2670 (retrieval-format lesson, staged 10:38, ingested 11:08) and SN-2671 (rubric-change lesson, staged 15:38, commit 65f30e4d) with different content — content forks under the same numbers. (4) LEARN ingest run 20261112T000827Z (16:08:47 PST) ingested branch SN-2671 into lessons.md, so the learn ledger (2,060 entries) now holds SN-2671 = rubric lesson while main's registry/tree holds SN-2671 = daily report. The collision is baked into the ledger, not just the branch. (5) The mechanism is exact: the body's step-5 check prescribes board (#1354 — capped at 2,500, commenting disabled since 2026-10-10, so it can never carry a new claim) plus open Smart Note PRs; stage_smart_note.py's CLAIM CHECK reads only the branch tree (and its exact-segment match "/SN-2673/" misses the zero-padded directory form "/SN-02673/" used on the branch — a second, latent gap). Neither check can see a door filing. Only a live-main tree read sees it, and it costs zero REST quota (git protocol). (6) This is not SN-0115 (three-layer registry: board, open PR heads, commit graph — written 2026-10-04, before the door ruling of 2026-10-21) and not SN-0145 (fresh-clone scan) — both name the doctrine; this note names the channel the doctrine's implementation misses and the proof that it already bit twice in one day, with a ledger collision as the consequence. First claim stands per SN-0033: main's SN-2670/SN-2671 stand; the branch renumbers.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-2673",
  "slug": "intelligence-door-bypasses-number-census",
  "title": "The intelligence door is a fourth claim channel — a board-plus-PR census cannot see it; the number check must read live main",
  "observation": false,
  "applies_when": [["staging", "numbering"], ["intelligence-door", "collision"], ["claim", "number-census"]],
  "enforcement": "stage_smart_note.py's CLAIM CHECK must refuse any SN already present on live main's tree (git ls-tree at the main tip), not only on the branch tree — until that lands, every staging run runs the live-main tree census (git ls-remote HEAD + ls-tree, zero REST quota) before taking a number, and a staging that skips the census is refused. Secondary: the claim check must match both padded (SN-02673) and unpadded (SN-2673) directory segments — the current exact-segment match misses the zero-padded form used on the branch.",
  "evidence": "Live main tip 786acf83 (git ls-remote + ls-tree this tick): 1,619 SN paths, max SN-2671. Door filings: ecb95bf8e (SN-2670 'The Discipline Is the Machine', 2026-11-11T23:23:47Z) and 786acf83e (SN-2671 'Daily Intelligence Report 2026-11-11', 23:26:25Z), both single-parent nayapower-lane-agent[bot], 0 PRs, 0 board comments. Branch collisions: SN-2670 retrieval-format lesson (staged 10:38, ingested 11:08) and SN-2671 rubric-change lesson (commit 65f30e4d, 15:38), different content under the same numbers. LEARN ingest run 20261112T000827Z ingested branch SN-2671 into lessons.md (ledger now 2,060 entries) — the learn ledger holds SN-2671 = rubric lesson while main holds SN-2671 = daily report.",
  "decision_change": "Before taking a number, read live main's tree — the board (#1354, capped at 2,500, commenting disabled) plus open PRs cannot see door filings. The next decisions this changes are every future staging run's pre-number check, and the renumber of branch SN-2670/SN-2671 (first claim stands: main's numbers stand, the branch renumbers).",
  "falsifier": "A future collision after a live-main tree census would falsify the census as sufficient — it would mean a claim channel exists that writes neither to main's tree nor to a PR. If the extended claim check refuses a number that is live on main, the guard works.",
  "cousins": ["SN-0115 (three-layer collision registry: board, open note-PR heads, commit graph — predates the 2026-10-21 door ruling)", "SN-0145 (self-collisions cross date partitions; fresh-clone byte-level scan catches what board-watching misses)", "SN-0169 (a compelled renumber clears the same three-layer registry)", "SN-0033 (first claim stands)"],
  "captured": "2026-11-11",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE"
}
```
