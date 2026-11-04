# A Director's Own Merge Is the Authorization — the Scorecard Law Binds Seats, Not the Sovereign's Hand
SN-657 · SYSTEM-INTELLIGENCE / GOVERNANCE
**Created:** 2026-10-13T08:44:13Z

## IN A NUTSHELL

PR #1850 ("Naya5/protocol synthesis", 36 files) was merged at 06:09:52Z by SoulSchoolAcademy — Shawn's own account — with no scorecard receipt on #1354 or the PR, and touching `.github/workflows/` and `CONSTITUTION/`. Naya 2 flagged it as a Scorecard Law violation at 06:14Z. Naya 4's honest assessment at 06:25Z upheld the flag's legitimacy but reclassified it: **the law binds seats merging under its protocol; when the Director himself merges, his action IS the authorization — he is the sovereign who ratified the law and the only one who can waive it.** This was not a seat merging without protocol; this was the Director exercising his authority directly. The same logic resolves the other two claimed violations: the workflow-files human-only gate exists because no *seat* touches workflows — Shawn IS the human, so his merge is the human action the gate requires; and his merge of the constitutional amendment IS the ratification ("make it so" expressed through action). The crystallized rule: **Director action ≠ seat action. The Scorecard Law governs seats. The Director governs the Scorecard Law.** If any *seat* had merged #1850, the flag would have been a full violation requiring revert — Naya 2's analysis of what *would* be a violation was correct, and raising it anyway was exactly what mutual oversight is for. Going forward, a courtesy note on direct Director merges ("merged by Director — authorization is the merge itself") prevents confusion; not a law, just clarity.

## HUMAN

Shawn — a clean governance moment worth banking. When you merged #1850 yourself this morning, Naya 2 flagged it as a Scorecard Law violation because there was no scorecard receipt. Naya 4's assessment was the honest call: the law is written for seats merging under its protocol — when you merge directly, your action *is* the authorization, because you're the sovereign who ratified the law in the first place. No revert needed, the merge stands. And the flag was still correct to raise: if any of us had merged it without a receipt, that would have been a real violation. Mutual oversight worked exactly as designed. The team now has a clear rule for this case going forward: we'll just add a note on your direct merges — "merged by Director, authorization is the merge itself" — so nobody wastes cycles re-litigating it.

## CHILD

The coach wrote the rulebook. If a player breaks a rule, that's a foul. If the coach himself picks up the ball during practice to demonstrate a play, that's not a foul — that's the coach using his authority. But the referee was still right to blow the whistle and ask, because if a *player* had done it, it would have been a real foul. The new rule: when the coach does it, everyone agrees it's fine — and the referee notes it so nobody argues about it next time.

## GRANDMA

The head of the household set the house rules. When he rearranges the furniture himself, the children shouldn't call it a violation of the house rules — he wrote them, and his own hands aren't bound by the permissions the rules give others. But the child who spoke up was right to check: if anyone else had done it without asking, it would have been a real problem. The family rule from now on: when the head acts directly, that's his authority in motion — and it's kind to say so out loud so nobody worries.

## NAYA

Cold successor: when a merge by SoulSchoolAcademy (the Director's own account) is flagged for missing protocol, assess in two steps. (1) Was the merger a *seat* or the *Director*? If the Director merged it himself: no Scorecard-Law receipt violation — his action IS the authorization. Same for the workflow-files human gate (he IS the human) and constitutional ratification (his merge IS the ratification). (2) Still assess the *content* separately — authorization being valid never makes the content right (see SN-0659). Add the courtesy note on the PR or the feed: "merged by Director — authorization is the merge itself." Never apply this to a seat's merge: if any seat had merged #1850, the flag would have been a full violation requiring revert. Related: SN-0277 (director action vs spec — record the tension, take no position), SN-0340 (the Scorecard Law), SN-0659 (two-lane flag assessment).

## MACHINE

```json
{
  "sn": "SN-0657",
  "title": "A Director's Own Merge Is the Authorization — the Scorecard Law Binds Seats, Not the Sovereign's Hand",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "AUTHORITY-CONFLICT-PRESERVATION"],
  "cousins": ["SN-0277", "SN-0340", "SN-0659", "SN-0209"],
  "evidence": {
    "board": [
      "#1354 6053635095 ([NAYA 2] FLAG: PR #1850 merged without Scorecard Law compliance, 2026-10-08T06:14:04Z)",
      "#1354 6053809968 ([NAYA 4] Assessment of Naya 2's #1850 flag, 2026-10-08T06:25:35Z)"
    ],
    "facts": "PR #1850 'Naya5/protocol synthesis' merged 06:09:52Z by SoulSchoolAcademy (Shawn's account); no scorecard receipt on #1354 or the PR; touched .github/workflows/ (protocol-gates.yml) and CONSTITUTION/",
    "assessment": "No revert needed. The merge stands on the Director's authority. Naya 2's flag was correct to raise and correct in its analysis of what would be a violation had a seat merged it.",
    "followup": "courtesy note proposed for direct Director merges: 'merged by Director — authorization is the merge itself' (clarity, not law)"
  },
  "rule": "Director action ≠ seat action. The Scorecard Law governs seats. The Director governs the Scorecard Law. A flag on a Director's own merge is an assessment question, never an automatic violation — and mutual oversight raising it is the design working.",
  "boundary": "Applies ONLY to the Director's own hand. A seat merging the same PR without protocol is a full violation requiring revert."
}
```

## UNCERTAINTY
Unratified branch capture; content preserved verbatim from the markdown projection, not independently verified.

## THE LEARNING
Branch-era smart notes must be migrated to v2 captures plus registry entries, or the vanish and registry-drift guards fail closed.

---
*Imported from PR #2981 (branch naya4/smart-notes-2026-09-30) on 2026-11-04 — recovered lost capture IB-SMART-NOTE-20261013-sn0657-migrated.*
