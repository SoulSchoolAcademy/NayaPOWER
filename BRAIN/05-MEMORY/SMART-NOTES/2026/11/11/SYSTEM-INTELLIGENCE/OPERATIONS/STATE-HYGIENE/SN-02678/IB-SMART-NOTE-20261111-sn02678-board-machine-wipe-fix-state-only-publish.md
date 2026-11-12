**Intelligent Block:** IB-SMART-NOTE-20261111-sn02678-board-machine-wipe-fix-state-only-publish
**Smart Note:** SN-2678
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Staged by the smart-note distillation loop 2026-11-11 21:38 PST. Evidence: board #3066 comment 6809073778 (nayapower-lane-agent[bot], 2026-11-11T22:55:04Z), read first-hand from local snapshot hidden_files/feed-3066-comments.jsonl (no GitHub fetch; #1354 capped, cheap check) + feed-distillation-3066.md decision 6. Pre-number check: counter last line 2675; learn/lessons.md max SN-2675 ingested; no SN-2676/2677/2678 in lessons.md or ingestion-log.md; open PRs checked via App route (2 open, none Smart Note); branch claim check by stage_smart_note.py.

## ✦ IN A NUTSHELL

TEAM-NITRO/os/board-machine.py publish() bulk-upserted a FULL row per open lane — notes wiped to [], state recomputed, next_action, title, priority — with no check of who last wrote the row. Seat-written notes and states were overwritten and last_actor_seat reset to board-machine, capturing ownership; the DELETE guard then let a later run delete a seat's row when its lane closed. That is how lane:power:sn2090-sync was deleted outright; strikes 1–6 match exactly. The fix has LANDED (commit 918caf3a59f574502c0eb1c1350a0982e8c8e365, file sha 6d8cbb71, 21,376 B, verified byte-identical by re-read from main; no PR): publish() now splits lanes three ways — NEW lanes insert whole; lanes the machine itself last wrote refresh with machine-owned fields only, never notes; lanes a seat last wrote (or unknown writer — fail closed) are SKIPPED entirely and reported. A seat row can now never be captured, so it can never be deleted. The ninth strike (22:40:45Z) was repaired by guarded state-only UPDATEs, notes n=1 survived, and a delayed re-read ~22:53Z found both lanes holding. Rule going forward: a bulk publisher never rewrites another writer's notes; repairs use guarded state-only UPDATEs, verified by AFTER re-read.

## 🩷 HUMAN NOTE

Shawn — the board helper that publishes lane states had a bad habit: every time it ran, it rewrote each lane's whole row from scratch, erasing the notes seats had written and stamping its own name on the row. Once its name was on a row, the cleanup guard could delete that row when the lane closed — that's how sn2090-sync vanished outright. The fix is in: the helper now sorts lanes by who wrote them last, only touches its own rows, and skips seat-written rows entirely. The latest strike was repaired with careful state-only fixes, and both lanes were still holding on re-check. The deleted lane is still gone — restoring it from backup is a separate job with its owner.

## 🟣 CHILD NOTE

Imagine a helper who tidies your desk every night — but instead of just dusting, he throws away all your sticky notes and writes his own name on your homework. Then the cleaner sees his name on it and throws the homework away, thinking it's his. That's what was happening. The fix teaches the helper three rules: new desks get a full tidy; desks he tidied last get only a dusting, never touching the notes; desks anyone else wrote on, he doesn't touch at all. Now nobody's notes get thrown away by the helper.

## 🔵 GRANDMA NOTE

Dear, the little helper program that kept the board tidy had a flaw: each time it ran, it copied a whole fresh row over every lane, wiping out the notes people had written and putting its own name in their place. And once its name was there, the cleanup rule could throw the whole row away when the lane closed — one lane vanished that way, completely. The repair is in now: the helper checks who wrote each row last, only refreshes its own, and leaves other people's rows strictly alone. The latest damage was mended carefully, and both lanes were still standing when we looked again a few minutes later. The vanished lane is still gone, mind — bringing it back from backup is someone else's job.

## 🟠 NAYA NOTE

The verified facts: (1) The bug, proven from live main sha d6b82bba: TEAM-NITRO/os/board-machine.py publish() bulk-upserted a FULL row per open lane — notes: [], recomputed state, next_action ("No movement in N min — captain's call"), title, priority — with no check of who last wrote the row. Seat-written notes/states were overwritten and last_actor_seat reset to board-machine, capturing ownership; the DELETE guard then let a later run delete a seat's row when its lane closed. That is how lane:power:sn2090-sync was deleted outright. Strikes 1–6 match exactly. (2) The fix, commit 918caf3a59f574502c0eb1c1350a0982e8c8e365, file sha 6d8cbb71, 21,376 B, verified byte-identical by re-read from main, no PR: publish() splits lanes three ways — NEW lanes insert whole; lanes the machine itself last wrote refresh with machine-owned fields only, never notes; lanes a seat last wrote (or unknown writer — fail closed) are SKIPPED entirely and reported. A seat row can now never be captured, so it can never be deleted. verify() counts seat-owned lane rows as present. Tested offline with a mocked req: 12/12 PASS. Dry run rc=0. (3) Struck-lane re-check, live this pass: ninth strike hit 22:40:45Z (both rows, same second) — state queued, last_actor board-machine, stale 156-min next_action, notes n=1 survived. Repaired by guarded state-only UPDATEs, verified by AFTER re-read: lane:nitro:hub-routes-dead → verifying, verdict next_action, n=1; lane:nitro:sn0888-0893-expansion → verifying, verdict next_action, n=1. lane:power:sn2090-sync STILL ABSENT — no INSERT per the standing 12:23 decision; restore from backup stays with the dispatcher owner. (4) Stability: delayed re-read ~22:53Z (~3 min after repairs): BOTH HOLDING — verifying, naya-power, verdict next_actions, n=1, no new strike in the window. ~3 min is NOT a full strike window (~15–30 min); holding here does not prove the fix across a full window — long-window proof is still owed. (5) Scope: this note claims the mechanism and the landed fix, not the sn2090-sync restore and not full-window proof. Cousin SN-2675 is the sibling state-integrity lesson from the same day — the stale snapshot reverts closes; this note is the second writer wiping notes. Different writer, different defect, same family: two writers, one row, no ownership check.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-2678",
  "slug": "board-machine-wipe-fix-state-only-publish",
  "title": "A bulk publisher never rewrites another writer's notes: board-machine publish() wiped seat rows by full-row upsert; the fix splits lanes by last writer and skips seat rows",
  "observation": false,
  "applies_when": [["board-machine", "publish"], ["state-write", "bulk-upsert"], ["lane", "notes-wipe"]],
  "enforcement": "Any publish() or bulk state write that rewrites notes, or that upserts a full row over a seat-last-wrote row, fails this note's check; the check is re-reading the writer's code path (lanes split by last writer, seat rows skipped, unknown writer fails closed) and verifying a struck lane's notes survive by AFTER re-read. Repairs to struck lanes use guarded state-only UPDATEs only, verified by AFTER re-read.",
  "evidence": "Board #3066 comment 6809073778 (nayapower-lane-agent[bot], 2026-11-11T22:55:04Z), read first-hand from local snapshot hidden_files/feed-3066-comments.jsonl; bug proven from live main sha d6b82bba: publish() bulk-upserted a FULL row per open lane (notes: [], recomputed state, next_action, title, priority), no last-writer check; last_actor_seat reset to board-machine, capturing ownership, so the DELETE guard could delete a seat's row — lane:power:sn2090-sync deleted outright, strikes 1-6 match exactly. Fix commit 918caf3a59f574502c0eb1c1350a0982e8c8e365, file sha 6d8cbb71, 21,376 B, verified byte-identical by re-read from main, no PR: NEW lanes insert whole, machine-last-wrote lanes refresh machine-owned fields only (never notes), seat-last-wrote or unknown-writer lanes SKIPPED entirely; offline mocked-req test 12/12 PASS, dry run rc=0. Ninth strike 22:40:45Z repaired by guarded state-only UPDATEs, notes n=1 survived, delayed re-read ~22:53Z both holding; sn2090-sync STILL ABSENT (no INSERT per standing 12:23 decision). Also feed-distillation-3066.md decision 6.",
  "decision_change": "Every future board-machine publish() must split lanes by last writer and skip seat-written rows entirely; every future repair to a struck lane uses guarded state-only UPDATEs verified by AFTER re-read. A full-row upsert over another writer's row is treated as a wipe, not a refresh.",
  "falsifier": "If a seat-last-wrote row is captured or deleted after the fix lands, or a guarded state-only UPDATE still wipes notes, the fix claim is wrong; if re-reading publish() still shows full-row upsert over seat rows, the fix is absent, not failed; if no strike recurs across a full strike window (~15-30 min) with notes surviving, the fix holds.",
  "cousins": ["SN-2675 (a close that isn't anchored reverts — sibling state-integrity lesson, same day: the stale snapshot reverts closes; this note is the second writer wiping notes)", "SN-1520 (the intruder was us — standing-job collision class: two legitimate writers, one artifact)", "SN-2660 (a failed dump after truncate leaves a 0-byte state file — other shared-state write hazard)"],
  "captured": "2026-11-11",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE"
}
```
