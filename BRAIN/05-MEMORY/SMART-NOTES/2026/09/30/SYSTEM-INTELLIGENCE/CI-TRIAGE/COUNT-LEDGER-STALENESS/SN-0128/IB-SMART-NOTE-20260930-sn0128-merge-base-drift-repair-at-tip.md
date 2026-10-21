# Intelligent Block — SN-128

- **Intelligent Block:** SN-128 — Verify the Repair at the Merge Tip: Merge-Base Drift Defeats Correct Repairs
- **Truth state:** CANDIDATE (proactive auto-capture; only Shawn ratifies)
- **Scope:** PRIVATE
- **Captured date:** 2026-10-02
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

A repair PR that is provably correct against its base can still be insufficient at the merge tip, because the baseline moved under it. PR #1301 fixes the 05-MEMORY brain-index drift correctly for its base `43e74d30` (raw baseline 21→23 covering the two SN-018 files) — but main then moved to `a67fc180` (SN-019 capture + projection publish), making git=26 vs #1301's expected 25. The CI check stays RED by +1 after the merge. Lesson: recompute the expected value at the actual merge tip before merging a drift repair, and park a one-commit follow-up for the delta; correct-at-base ≠ sufficient-at-tip.

## HUMAN NOTE

Shawn: the brain-index count fix (PR #1301) works — for the commit it was written against. Since then main advanced with SN-019's capture, so the count the fix produces (25) is still one behind the real count (26). Merging it as-is leaves the same red check. The battery lane needs a tiny follow-up (23→24 bump + artifact regen at the pin) before a loop re-run can close the check green. The takeaway for the team: never merge a count/drift repair without re-pinning it to current main first.

## CHILD NOTE

Imagine you fixed a leak in a bucket — counted the holes, patched exactly 2. But while you were patching, someone poured 1 more hole in (okay, holes don't work that way, but pretend). Your patch is perfect for the old bucket and still one hole short for the new bucket. Always count the holes again right before you say "done."

## GRANDMA NOTE

It's like balancing the checkbook: you reconcile everything to Tuesday's statement, then Wednesday's mail arrives with one more check. The math was right — just right for yesterday. Always do one last look at today's mail before you close the book.

## NAYA NOTE

Sisters: this is the count-ledger family's newest wrinkle — SN-062 taught us the ledger is part of the change, SN-078 taught us merges must regen the index, and now SN-128 teaches us the repair's base must be re-verified at the tip. Main moved `43e74d30` → `a67fc180` between #1301's authoring and its review window; two commits (SN-019 capture + projection publish) added +1 to the 05-MEMORY file count. Naya 4 verified this independently at the pin (169 BRAIN files, git ls-tree + server-side object sizes, immune to the shallow-checkout 0-byte class) and opened no competing PR — #1301 is the battery lane's in-flight repair, and the follow-up spec is parked in `human-director-package-e84b5565.md` §16 for the battery lane to apply. The crisp discipline: a drift-repair merge requires a tip-recompute as the last step before merge, not just base-correctness at authoring time. Watch also: #1301's regenerated artifacts stamp basis `5885459af8` while the branch claims base `43e74d30` — one confirming look before merge.

## MACHINE NOTE

```json
{
  "sn": "SN-128",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-02",
  "taxonomy": "SYSTEM-INTELLIGENCE/CI-TRIAGE/COUNT-LEDGER-STALENESS",
  "extends": ["SN-062", "SN-078"],
  "lesson": "A drift repair must be re-pinned and recomputed at the actual merge tip; base-correctness at authoring time is not sufficiency at merge time.",
  "evidence": {
    "board": "#554 comment 5944290497 (Naya 4 self-build sign-out, 2026-10-02T02:09:19Z)",
    "pr": "SoulSchoolAcademy/NayaPOWER#1301 (head c0407250, base 43e74d30, basis-stamp note: artifacts stamp 5885459af8)",
    "main_pins": {"repair_base": "43e74d30", "current_main": "a67fc180"},
    "counts": {"05_memory_git_at_tip": 26, "pr1301_expected": 25, "shortfall": 1}
  },
  "mechanism": {
    "independent_verification": "pin a67fc180; tools/regenerate_brain_index.py functions against git ls-tree of the pin; 169 BRAIN files; server-side object sizes (shallow-checkout 0-byte immune)",
    "follow_up": "23->24 one-commit bump + artifact regeneration at pin, spec parked in human-director-package-e84b5565.md §16",
    "full_reconciliation": "~/workspace/goals/nayapower-self-build-loop/hidden_files/05memory-drift-reconcile-a67fc180-2026-10-01.md"
  },
  "gate": "Before merging any count/drift repair: re-run the count at the CURRENT merge tip and confirm expected == actual. If not, apply the delta as a follow-up commit before or immediately with the merge.",
  "ratification": "NOT_RATIFIED — only Shawn ratifies"
}
```
