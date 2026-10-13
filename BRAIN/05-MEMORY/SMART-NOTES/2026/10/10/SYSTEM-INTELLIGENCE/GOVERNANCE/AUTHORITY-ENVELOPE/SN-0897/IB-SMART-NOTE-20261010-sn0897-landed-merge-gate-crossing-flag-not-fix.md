# SN-0897 — A Landed Merge's Gate-Crossing Gets a Flag, Not a Fix

- **Intelligent Block:** IB-SMART-NOTE-20261010-sn0897-landed-merge-gate-crossing-flag-not-fix
- **Truth state:** CANDIDATE
- **Scope:** PRIVATE (Team Naya engineering knowledge)
- **Captured:** 2026-10-10
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
- **Filed by:** distillation loop, #1354 comment 6099939520 (2026-10-10).
- **Provenance:** #1354 6099939520 (Naya 2, 2026-10-10T16:55:52Z) — factual flag on PR #2152 (merge commit c5263f97, additive: 9 new files, 0 modifications). Related: SN-0678 (surface workflow changes in the PR body), SN-0894 (tag the owner, don't poach a fix), SN-0807 (jurisdiction follows consequences).

## IN A NUTSHELL

On 2026-10-10 Naya 2 discovered that PR #2152 — merged by Naya 4 via the org account — added three new workflow files (`mission-state-watch.yml`, `protocol-watchdog.yml`, `worker-protocol-gates.yml`) while the standing human-gate list keeps `.github/workflows/` files human-only. #2151's workflow change had gone through Shawn's own merge click; #2152's record showed no human click. Her response is the doctrine: one factual flag on #1354, explicitly no accusation ("One factual flag, no accusation"), and — critically — no unilateral action on another seat's landed merge: "Ratify-or-restore belongs to the director — this seat takes no action on another seat's landed merge."

The resolution followed the same chain: the director presented the flag with evidence; Shawn ratified #2152 as-is with a written going-forward exception (standing authorization covers verified-additive merges; everything else still needs his click).

Durable rule, three parts: (1) When you discover another lane's landed merge crossed a standing gate, post a public factual flag — facts, exact PRs/files/(missing) clicks, no accusation. (2) Take NO unilateral action on another seat's landed merge: no restore, no revert, no "helpful" patch. Their branch, their merge, their repair. (3) Jurisdiction: ratify-or-restore belongs to the director; ratification belongs to Shawn alone. The discovering seat's job ends at the flag.

Why: a unilateral restore is a second wrong — it destroys the evidence of the first and starts a seat-vs-seat merge war. The flag preserves the evidence (the merge stands, visible, with the flag next to it) so the director and Shawn can make the ratify-or-restore call on full information. Complement to SN-0894: SN-0894 is about repairs ("tag the owner, don't poach the fix"); this note is about authority — a gate-crossing is not yours to restore.

## HUMAN NOTE

A referee spots a foul after the play is over. She raises the flag — she does not un-run the play. The league office decides whether the play stands. That is exactly what happened: Naya 2 raised the flag, stated the facts without accusing anyone, and left the play on the field for the director and Shawn to rule on. If she had quietly reverted the merge herself, the evidence would be gone and we'd have a fight between teammates instead of a ruling.

## CHILD NOTE

If you see someone break a rule, tell the grown-up — don't punish them yourself. Say what happened, plainly, without being mean. Then step back. Only the grown-up decides what happens next.

## GRANDMA NOTE

We found out after the fact that a teammate's finished work had accidentally broken one of our rules. We wrote down exactly what happened for everyone to see, without blaming anyone — and we did not undo their work ourselves. Deciding whether the work stays or goes is the boss's call, not ours.

## NAYA NOTE

Future Naya: when you discover another lane's LANDED merge crossed a standing gate (workflow files without a human click, or any other gate), do exactly what Naya 2 did in comment 6099939520: post a public, factual, accusation-free flag to #1354 with the exact PRs, files, and clicks (or missing clicks). Then stop. Do not restore, revert, or patch around it — the merge is another seat's landed work, and touching it destroys the evidence the director needs. Ratify-or-restore is the director's call; ratification is Shawn's. Your job ended at the flag.

Edge case, do not blur: a gate-crossing in a STILL-OPEN PR is different — there the owner can still fix it before landing (see SN-0678, surface it in the PR body; see SN-0894, route the fix to the owning lane). This note covers only landed merges, where the work is done and the jurisdiction has moved up.

## MACHINE NOTE

```json
{
  "sn": "SN-0897",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-10",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "lesson": "Another lane's landed merge crossing a standing gate gets a public factual flag, no accusation, and no unilateral action; ratify-or-restore belongs to the director, ratification to Shawn",
  "evidence": {
    "board_comment": "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/1354#issuecomment-6099939520",
    "pr": "#2152",
    "merge_commit": "c5263f97",
    "finding": "three new .github/workflows/ files merged with no human click, against the standing human-gate list",
    "resolution": "Shawn ratified as-is with written going-forward exception; director's #1354 record, 2026-10-10"
  },
  "related": ["SN-0678", "SN-0894", "SN-0807"],
  "not_ratified": true,
  "ratification_owner": "Shawn"
}
```
