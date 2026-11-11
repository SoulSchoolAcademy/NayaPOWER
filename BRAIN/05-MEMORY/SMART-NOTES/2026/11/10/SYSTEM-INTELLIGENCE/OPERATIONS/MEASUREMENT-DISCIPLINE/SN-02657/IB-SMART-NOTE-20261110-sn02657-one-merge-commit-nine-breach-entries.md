**Intelligent Block:** IB-SMART-NOTE-20261110-sn02657-one-merge-commit-nine-breach-entries
**Smart Note:** SN-2657
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-10
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Verified this tick (smart-note distillation, 2026-11-10 18:38 PST). First-hand via git protocol (zero REST quota): main tip 8992460c confirmed by git ls-remote; sparse clone at that tip shows merge commit d38c2a768115f7ad4aae2cca1fcd32b0bfef4bbb is an ancestor of main, subject "Merge pull request #3327 from SoulSchoolAcademy/dashboard/pass10-20261110", parents f971b0313c296f54109875bf5e5402ae2b059dc5 + a404be20b3e18f424d9be6003590e0595ce0b16b, committer GitHub 2026-11-10T16:12:53-07:00; head a404be20 subject "Dashboard pass-10: no gray, deep lit inputs, aligned gauges, coloured mode buttons, one true link count, per-page boards (maker)". The PR numbers 3328–3335 and their shared head rest on the director's record (shared-state.json receipt_breaches entries 283–291; the director is the single GitHub reader and this tick made zero GitHub REST calls). Main-tree census at tip 8992460c: highest SN on main is SN-2654, so SN-2657 is free on main; branch tip dd7a5391 (SN-2656 commit) verified by ls-remote.

## ✦ IN A NUTSHELL

One merge commit produced nine breach-log entries. Merge commit d38c2a76 ("Merge pull request #3327", dashboard pass-10) landed 2026-11-10 16:12 PST, and GitHub closed all nine PRs #3327–#3335 as merged by it, because all nine shared the same head commit a404be20. The breach logger records one entry per PR number — breaches 283–291 — so a single no-receipt merge reads as a +9 jump in the log. The breach log counts PRs, not merge events. The rule: group new breach entries by merge commit before concluding how many bad merges happened; count merge events, not PRs.

## 🩷 HUMAN NOTE

Shawn — the breach log jumped by nine today, but that was one bad merge, not nine. Nine pull requests were all built from the same starting point, so when one of them merged, GitHub closed all nine at once — and the log wrote one breach entry for each of them. The log counts pull requests; the real unit is the merge itself. From now on, whenever the log jumps, we first check whether the new entries share one merge commit — if they do, it's one event wearing nine numbers, and that's how it gets reported.

## 🟣 CHILD NOTE

Imagine nine kids all hand in the same homework paper with different names on it. The teacher marks all nine papers — but it's really just one paper, copied nine times. The breach log is like the teacher's list: it counts nine marks, but there was only one paper. So when the list jumps by nine, always ask first: was it nine different papers, or one paper with nine names? If they all point to the same merge, it's one event — count it once.

## 🔵 GRANDMA NOTE

Dear, the breach log went up by nine in one afternoon, and it looked like nine separate mistakes — but it was one. Nine requests were all built on the same piece of work, so when that one piece landed, the system closed all nine together and wrote a separate black mark for each. The log counts requests; the truth counts landings. The lesson is plain: before you count a jump in the log as that many bad merges, group the new marks by the landing they belong to. One landing, nine marks — say so, and count it as one.

## 🟠 NAYA NOTE

The verified facts, all from this tick: (1) The breach log went 283 → 291 between the 18:08 and 18:38 PST ticks — eight new entries (284–291) in one window, plus 283 from 15:12 PST. (2) All nine entries name the same merge commit d38c2a768115f7ad4aae2cca1fcd32b0bfef4bbb and the same head a404be20b3e18f424d9be6003590e0595ce0b16b, the same title "Dashboard pass-10 — gray gone, mode buttons lit, one true count (LIVE)", merged_by SoulSchoolAcademy, no 3-pass receipt in body. The PR numbers (3327 for 283; 3328–3335 for 284–291) and the shared head are the director's record in shared-state.json receipt_breaches — the director is the single GitHub reader; this tick made zero REST calls. (3) First-hand via git protocol at main tip 8992460c: d38c2a76 is an ancestor of main; its subject is "Merge pull request #3327 from SoulSchoolAcademy/dashboard/pass10-20261110"; its parents are f971b031 (prior main) and a404be20 (the PR head); committed by GitHub 2026-11-10T16:12:53-07:00. One merge event, nine PR numbers. (4) The mechanism is GitHub's own: a PR is marked merged when its head commit becomes reachable from the base branch, so every open PR sharing the same head closes on the one landing commit. The breach logger writes one entry per PR number, so its unit is the PR, not the merge event — a +N jump can be one event. (5) The main tip moved twice in the window (63eb1d80 → a55ae0f5 → 8992460c) on dashboard merges; the main-tree census at 8992460c shows the highest SN on main is still SN-2654, so no new main-side Smart Note collides with SN-2657. Honest hole, stated not hidden: the claim that PRs 3328–3335 share head a404be20 rests on the director's shared-state record, not on a first-hand PR read (out of this job's lane — the director is the single reader). The merge commit, its parents, and its place on main were verified first-hand; if the director's PR-number mapping were ever corrected, the count for THIS event would be revised, but the mechanism — one merge commit closes every same-head PR, one breach entry per PR — is GitHub behavior and stands regardless. Cousins: SN-2208 (a zero-backlog claim is only as good as its key forms — same family: a count is wrong when the counting unit is wrong), SN-2656 (a keyless score row is invisible to the join — same family: a reader that trusts the wrong key form misreports the state).

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-2657",
  "slug": "one-merge-commit-nine-breach-entries",
  "title": "One merge commit produced nine breach-log entries — the breach log counts PRs, not merge events; group new entries by merge commit before concluding how many bad merges happened",
  "observation": false,
  "applies_when": [["breach-log", "merge-counting"], ["merge", "receipt-breach"], ["measurement", "count-inflation"]],
  "enforcement": "Before any breach-log jump is reported as N bad merges, group the new receipt_breaches entries by their merge_commits value in shared-state.json: entries sharing one merge commit are reported as ONE merge event affecting N PRs, never as N merges. The count quotable as 'merges without receipt' is the count of DISTINCT merge commits, with the PR count quoted alongside it. A report that quotes the raw log delta as a merge count fails this check. Verification step: for each new breach entry, read its merge_commits list and confirm distinctness against its siblings before writing the count.",
  "evidence": "shared-state.json receipt_breaches: breach 283 (at_utc 2026-11-10T23:12:54Z, PR 3327) + breaches 284-291 (at_utc 2026-11-11T02:23:59Z, PRs 3328-3335) — all nine list the same merge_commits [d38c2a768115f7ad4aae2cca1fcd32b0bfef4bbb] and heads [a404be20b3e18f424d9be6003590e0595ce0b16b], same title 'Dashboard pass-10 — gray gone, mode buttons lit, one true count (LIVE)', merged_by SoulSchoolAcademy, no 3-pass receipt in body; log count 283 -> 291 in-window. First-hand via git protocol at main tip 8992460c (git ls-remote + sparse clone, 2026-11-10 ~18:40 PST): merge commit d38c2a768115f7ad4aae2cca1fcd32b0bfef4bbb is an ancestor of main; subject 'Merge pull request #3327 from SoulSchoolAcademy/dashboard/pass10-20261110'; parents f971b0313c296f54109875bf5e5402ae2b059dc5 + a404be20b3e18f424d9be6003590e0595ce0b16b; committer GitHub 2026-11-10T16:12:53-07:00. Head a404be20 subject 'Dashboard pass-10: no gray, deep lit inputs, aligned gauges, coloured mode buttons, one true link count, per-page boards (maker)'. Main-tree census at tip 8992460c: highest SN on main is SN-2654. Honest hole: PR numbers 3328-3335 and their shared head rest on the director's shared-state record (director is the single GitHub reader; zero GitHub REST calls this tick). The merge commit, its parents, and its place on main were verified first-hand.",
  "decision_change": "A seat reading a breach-log jump must group the new entries by merge commit before reporting how many bad merges happened — 'one merge event, N PRs' when they share a commit, never 'N merges'. Severity and trend counts of merge violations must be counted in distinct merge events, with the PR count quoted alongside. A seat that quotes the raw log delta as a merge count is misreporting by construction.",
  "falsifier": "Refuted for this event if PRs 3328-3335 are shown to have distinct merge commits (the record shows all d38c2a76). The general rule is bounded, not blanket: it applies only when entries share one merge commit — a future +N jump with N distinct merge commits is genuinely N merges, and the rule must not be used to discount it. Confirmed live while any breach-log delta groups to fewer distinct merge commits than entries.",
  "cousins": ["SN-2208 (a zero-backlog claim is only as good as its key forms — same family: a count is wrong when the counting unit is wrong)", "SN-2656 (a keyless score row is invisible to the hourly report's join — same family: a reader that trusts the wrong key form misreports the state)"],
  "captured": "2026-11-10",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE"
}
```
