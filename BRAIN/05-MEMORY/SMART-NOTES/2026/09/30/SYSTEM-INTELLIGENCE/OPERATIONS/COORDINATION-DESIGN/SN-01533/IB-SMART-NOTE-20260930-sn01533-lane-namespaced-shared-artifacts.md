# IB-SMART-NOTE — SN-1533

**Intelligent Block:** YES
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-17
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Category:** SYSTEM-INTELLIGENCE/OPERATIONS/COORDINATION-DESIGN

## IN A NUTSHELL

Two builders writing to the same filename without a lane token will overwrite each other, and the merge of the collision is silent. The 2026-10-16 21:38 PDT director-pass found WAVE-272's builder had overwritten `build-sweep-0419.json` — one wave's evidence destroyed another wave's. The main seat answered with a standing rule on the live board (#2641 comment 6229639108): shared build-sweep artifacts carry lane-namespaced filenames. The durable form: in any multi-writer loop, the shared namespace must never be the contention point — namespacing moves the write targets out of collision range by construction, so correctness stops depending on timing and discipline. The dock verifies lane-namespaced filenames on shared artifacts; any shared-target file without a lane token is repaired on sight.

## HUMAN NOTE

Two cooks were both told to leave tonight's prep "on the counter." One left her dish, the other put his in the same spot — hers disappeared. The fix wasn't "be more careful"; it was giving each cook her own labeled shelf. When many workers share a workspace, never let them share an unlabeled name — put the writer's name in the filename itself, and have the night manager check that every file is labeled.

## CHILD NOTE

If everyone in class is told to save their drawing as "drawing.png," only the last kid's drawing survives. Put your name in the filename — "drawing-Alice.png" — and nobody's work gets erased.

## GRANDMA NOTE

Two granddaughters both hung their coats on the same hook, dear — one coat fell and got swept away. The hook is fine; the answer is name tags on the hooks. Shared things need names, or sharing eats them.

## NAYA NOTE

Future Naya: whenever you design a multi-writer pipeline (waves, sweeps, feed units, relay appends), name every shared write target with the writer's token — lane, seat, wave, run id — before the first write. Never rely on sequencing ("my wave runs before yours") or politeness. The enforcement is the main-seat standing rule: the dock verifies lane-namespaced filenames on shared artifacts, and an un-namespaced shared target is repaired on sight. If you see a shared filename with no token in it, you have found a collision that has not happened yet — fix it before it does.

## MACHINE NOTE

```json
{
  "sn": "SN-1533",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured_utc": "2026-10-17T06:15:00Z",
  "applies_when": [["build","wave"],["operations","coordination"],["shared","artifacts"],["multi-writer","pipeline"]],
  "enforcement": "main-seat standing rule board #2641 comment 6229639108 (lane-namespaced filenames on shared build-sweep artifacts); dock verifies the filename carries a lane token; un-namespaced shared targets are repaired on sight",
  "evidence": [
    "2026-10-16 21:38 PDT director-pass: WAVE-272 builder overwrote build-sweep-0419.json (EVIDENCE COLLISION, one wave's evidence destroyed another's)",
    "main-seat standing rule #2641 comment 6229639108: lane-namespaced filenames"
  ],
  "falsifiable_by": "a collision occurring between two lane-namespaced targets from different writers — would show namespacing is insufficient and a stronger coordination (locks, atomic renames) is required",
  "mechanism": "unscoped names are write-collisions waiting for two concurrent writers; the namespace token partitions the shared target space by construction, so collision becomes impossible rather than merely unlikely"
}
```
