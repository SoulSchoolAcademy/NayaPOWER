# IB-SMART-NOTE-20260930-sn01729

**Intelligent Block:** SN-01729
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-20
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

Bind the freshness stamp to the same commit that changes the tree: a contract that self-heals on every commit never needs re-arming.

## 🩷 HUMAN NOTE

The brain index keeps drifting. At tip c58832b4 the index said 1,329 files; the tree actually holds 1,333. The freshness check exits 1, the pipeline owner gets another re-verification owed, and the whole re-arm loop runs again — for the Nth time. The proposed repair: stop re-arming. Make every commit that touches BRAIN/ re-stamp the index inside that same commit, enforced as a required CI check. The drift window is not a scheduling problem; it is a binding problem. A check that runs "later" can always be late. A stamp bound to the change event cannot — the tree and the stamp move as one, or the commit does not land.

## 🟣 CHILD NOTE

Imagine a librarian who counts the books every Friday, but kids borrow books all week long. By Friday the count is always wrong. The fix is not counting harder on Friday — it is stamping the count on the card every time a book leaves the shelf. Then the count is never more than one borrow old, forever, with no Friday ritual at all.

## 🔵 GRANDMA NOTE

Dear, anything you check "later" can be late. If the freshness matters, tie it to the moment things change, not to a calendar. A promise kept at the moment is kept forever; a promise kept on schedule is kept approximately.

## 🟠 NAYA NOTE

Method, for any freshness contract (index vs tree, manifest vs files, registry vs reality): (1) bind the stamp to the mutating event — the commit that touches the governed tree re-stamps in that same commit; (2) enforce as a required CI check on the mutating path — commits touching BRAIN/ must carry a re-stamp that verifies brain-index file count against git ls-tree; (3) the periodic re-arm loop is retired, not kept as backup — two mechanisms for one invariant is how the invariant gets orphaned; (4) verify with two independent code paths, as t1020 did (regenerated inventory vs git ls-tree). Cousins: SN-01708 (stale re-dispatch — belief rots between ticks); SN-01725 (audit disk, not the list — the list is a partial view; the tree is the disk).

## 🟢 MACHINE NOTE
```json
{
  "sn": "SN-01729",
  "lesson": "Bind the freshness stamp to the same commit that changes the tree: any commit touching BRAIN/ re-stamps the brain index in that commit, enforced as a required CI check. A contract that self-heals on every commit never needs a re-arm loop.",
  "applies_when": ["index", "freshness", "ci-gate", "brain-index", "commit"],
  "enforcement": "Required CI check on the mutating path: any PR or commit touching BRAIN/ must re-stamp the brain index in the same commit and verify the brain-index file count against git ls-tree via two independent code paths (regenerated inventory + ls-tree); a commit that changes the tree without the stamp, or with a mismatched stamp, fails the gate. The periodic DRIFT re-arm loop is retired on the rule's first green week — not kept as a shadow mechanism.",
  "decision_changed": "The brain-index DRIFT re-verification owed at tip c58832b4 becomes the last of its kind: instead of re-arming the re-verification loop, the pipeline owner wires the same-commit re-stamp as a required check, and future freshness failures are commit-time failures with an author attached — not tick-time debts with an owner to chase.",
  "falsifier": "Drift recurs with the required CI check enforced and no bypass — stamps bound to commits, yet the index still disagrees with the tree. That would show the stamp mechanism itself is buggy (wrong tree read, partial stamp), and the rule needs a correctness fix, not a cadence fix.",
  "mechanism": "Temporal coupling: a periodic check has an intrinsic window — between the change event and the next check run, the invariant is unchecked by construction. Every re-arm closes the last window and opens the next one. Binding the stamp to the change event removes the window entirely: the invariant is verified at the only moment it can break. The re-arm loop treats drift as weather; the same-commit rule treats it as a defect with a timestamp and an author.",
  "evidence": "t1020-lane10.md (12:40-12:44Z, 9.5/10): brain index at 7a6a7995 (1,329 files) vs tree 1,333 at tip c58832b4; --check exits 1; regenerated inventory agrees with git ls-tree on two independent code paths; shared-state.json carries 'brain-index DRIFT re-verification at c58832b4' as open debt across director ticks 0338-0608."
}
```
