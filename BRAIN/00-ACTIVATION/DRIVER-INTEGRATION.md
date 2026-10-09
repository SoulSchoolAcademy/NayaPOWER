# Checklist Driver Integration

**For all area drivers.** This is part of your run, not extra work.

## The one step

Add this to your run template, after your scoring step:

```
CHECKLIST UPDATE:
  python3 tools/checklist_update.py <ITEM-ID> --status <STATUS> --note "<one-line update>" --by "<your-seat>"
```

## Department → Item ID mapping

| Department | Feed | Item IDs |
|---|---|---|
| Learning | #1724 | L1, L2, L3, L4, L5 |
| Brain/Memory | Naya 5 lane | B1, B2, B3 |
| Law/Governance | #1718 | LW1, LW2, LW3 |
| Arch/Eng/Ops (ACT) | #1719 | A1, A2 |
| Evolution/Succession | #1725 | E1, E2, E3, E4 |
| Interfaces/Hub | #1722 | I1, I2, I3 |
| Knowledge/Intelligence | #1720 | K1, K2, K3 |
| Proving/Verifying | #1721 / #1723 | P1–P7 |
| Innovation | (unassigned) | IN1, IN2, IN3 |
| Cross-cutting | — | C1–C6 |

## When to update

- **Something changed:** PR merged, blocker hit, blocker cleared, score moved → update that item.
- **Nothing changed:** skip. The sync script handles PR-driven updates automatically. Don't add noise.
- **New blocker:** use `--blocker "description"` — this auto-sets status to BLOCKED.

## Examples

```bash
# Learning driver: battery progress
python3 tools/checklist_update.py L1 --note "Battery 8/14 seats done, avg 9.8" --by "naya4-learn-driver"

# Brain driver: unblocked!
python3 tools/checklist_update.py B2 --status "IN PROGRESS" --note "Rebased, CI green, awaiting review" --by "naya5"

# Prove driver: new blocker
python3 tools/checklist_update.py P4 --blocker "Rebase conflict in test_kernel.py, need author" --by "naya4-prove-driver"
```

## Rules

1. **One command per meaningful change.** Not every run needs an update.
2. **Be specific.** "Progressing" is not a note. "Rebased onto 7b8f8be8, 3/5 tests green" is.
3. **Never touch another department's items** without coordinating on #1354.
4. **Never clear a 🔒 SHAWN-GATED BLOCKED.** That's his word, not yours.
5. **The .md regenerates automatically.** You only touch JSON via this CLI.

## What the sync script does for you

Every 30 minutes, `tools/checklist_sync.py` checks all PR refs and auto-updates statuses. You don't need to manually flip IN PROGRESS → DONE when a PR merges — the script sees it. Your job is the human judgment: notes, blockers, context the API can't see.
