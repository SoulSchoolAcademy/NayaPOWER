# INTELLIGENT BLOCK — SN-1145
- Truth state: CANDIDATE
- Scope: PRIVATE
- Captured date: 2026-10-12
- Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL
A revert closes with the same byte proof as a merge. "Revert landed" is a claim, not a close — the close requires the triad: (1) merge-faithfulness, (2) diff-inversion exactness, (3) no-clobber on overlapping files. The #2459 revert closed with all three.

## HUMAN NOTE
The #2459 merge hold was lifted tonight when the revert closed — and it closed properly: the Captain's merge-map sign-out records the triad. (1) Merge-faithfulness: the revert is a true merge against the live tip, not a direct push. (2) Diff-inversion exactness: all 8 reverted files are the exact inverse of #2455's diff — byte-verified. (3) No-clobber: #2469's files untouched. Any revert that can't show the triad hasn't closed; it has only been clicked. The discipline matters because reverts are the emergency path — and the emergency path is exactly where rigor gets skipped "for speed." Hold the same bar: a revert that silently re-inverts someone else's fix, or whose inversion is approximate, creates the next incident. The close criterion is mechanical: triad or it isn't closed.

## CHILD NOTE
When you undo something, you have to undo it completely and carefully — like untying a knot, not cutting the rope. Check that everything is back to exactly how it was, and that you didn't undo anyone else's work by accident.

## GRANDMA NOTE
If you borrow someone's kitchen and make a mess, "I put it back" isn't enough — the right check is: every dish exactly where it was, nothing of anyone else's moved. Undoing deserves the same care as doing.

## NAYA NOTE
I treat reverts as merges for proof purposes: exact tip pin, true merge structure, byte-exact inversion of the original diff, and a named no-clobber verification on overlapping files. If any leg of the triad is missing, the revert is open work, not a closed lane. Speed never outranks the close criterion on the emergency path.

## MACHINE NOTE
{
  "sn": "SN-1145",
  "lesson_id": "WP-21",
  "family": "F8",
  "rule": "REVERT_CLOSE requires TRIAD: {merge_faithfulness: true_merge_vs_live_tip, diff_inversion_exactness: byte_exact_inverse_of_original_diff, no_clobber: overlapping_files_untouched}; missing any leg => revert is OPEN_WORK",
  "cousins": ["SN-1059 invalid-authority-revert-by-default (authority angle)", "SN-0882 revert-first-own-wrong-repair (triage angle)"],
  "evidence": {
    "board_comment": 6136548769,
    "captain_signout": 6136329454,
    "pr_reverted": 2459,
    "reverted_pr": 2455,
    "window": "board-window-2026-10-13T0210Z.json"
  },
  "admission": {"durable": true, "new": true, "signal": true, "evidence_backed": true}
}
