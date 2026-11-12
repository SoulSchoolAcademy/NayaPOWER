**Intelligent Block:** IB-SMART-NOTE-20261112-sn02696-fault-that-fires-it
**Smart Note:** SN-2696
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Staged by the smart-note distillation loop 2026-11-12 01:08 PST. Evidence read first-hand from the Lane 12 gap receipts + scripts on disk (no GitHub fetch — #1354 capped at 2500). Pre-number check (this tick, full-domain, fresh main tip 6f38cba5): SN-2696 free in every domain (no capture, no BRAIN page, no registry entry, not on branch, not in ledger); 2693–2695 left clear for the owed renumber of branch SN-2685/2686/2691; registry next_sequence 2692.

## ✦ IN A NUTSHELL

A safety net nobody has ever seen catch anything is a promise, not a mechanism. `safe-edit.py` tells every seat "the edit either lands verified or the file is restored, never half-applied" — but until this run, the restore half of that sentence rested on reading the code. Two lane runs fired it for real: a fault injected at the exact boundary the script defines (between the apply write and the verify read) tripped exit 3 and restored the file byte-identical, and the manual recovery the CRITICAL branch names was then performed by hand — `cp` exit 0, sha back to the pre-edit value exactly. Reading a defensive branch proves the author wrote it; firing it proves the machine runs it. Before calling any defensive path "done", fire it — with a fault injected at the boundary the code itself defines, and a diff proving the code that ran is the code that ships.

## 🩷 HUMAN NOTE

Shawn — the edit tool promises that a failed edit always puts the file back exactly as it was. That promise was only words on a page until this morning, when two runs proved it by breaking things on purpose: they corrupted a test file mid-edit, the tool caught it, and the file came back byte-for-byte identical. Then they ran the manual rescue the tool's own error message describes, and that worked too. A safety net is only real once something has fallen into it — now this one has, twice, with the receipts to show it.

## 🟣 CHILD NOTE

Imagine a net under a trapeze. Everyone says the net will catch you — but nobody has ever fallen into it. Is it a real net, or just a drawing of one? The helpers tested it the honest way: they dropped something into it on purpose, watched it catch, and then practiced the rescue the net's own instructions describe. Now they know the net is real — because something fell, and the net held.

## 🔵 GRANDMA NOTE

Dear, there was a safety promise in the little edit tool — if anything goes wrong, your file comes back just as it was. Pretty words, love, but nobody had ever seen it happen. So this morning the helpers broke a test file on purpose, right in the middle of an edit, and watched the tool catch it and put everything back exactly — and then they walked through the rescue steps the tool itself tells you to do, and those worked too. A promise is only proven when it is kept, and now it has been kept twice.

## 🟠 NAYA NOTE

The verified facts: (1) The unproven branch: `safe-edit.py`'s exit-3 auto-restore path was defensive code never triggered in testing — named as honest scope in the 00:00 learning review and in SN-2692 ("the exit-3 auto-restore path is defensive code never triggered in testing"). (2) F1 — the fault fired: the 5-gap receipt (Lane 12, 2026-11-12 08:25–08:34Z, self 9.4, scorer 9.4) copied the shipped script to /tmp and injected exactly one 6-line corruption block after the APPLY write (diff vs shipped exactly `178a179,184`; the VERIFY + restore code byte-identical to shipped). Ran on a fresh fixture: exit 3, `SAFE-EDIT FAIL: post-edit verification failed -- backup restored byte-identical`, fixture post sha == pre sha == backup sha == `970a886d…`, FAULT-INJECTED count 0. The 6-test battery A–E2 was independently re-run against the shipped script, 6/6, each exit code and sha confirmed. (3) F2 — the CRITICAL branch fired: same run, exit 3, `SAFE-EDIT CRITICAL: restore sha mismatch -- file may not be byte-identical to pre-edit; manual recovery from <backup> required`, backup sha == pre (recovery available). (4) The recovery performed: the 6-gap receipt (Lane 12, 2026-11-12 08:44–08:47Z, self 9.5) executed the F2 manual recovery end-to-end on the brief-named pair — `cp` exit 0, fixture sha returned exactly to the brief-named pre-edit sha `970a886db9379f6bb830025a6026e1679e94c04d21aa24d703a08977b8c2c1ce`, diff vs the shipped template empty, fault markers 0; the corrupted fixture's pre-recovery sha `f9b0649b…` matched the parent's recorded F2 post sha byte-for-byte, so the recovery is provably on the parent's exact case. The parent's original corrupted fixture was preserved untouched as scorer evidence. (5) Mechanism: verification compares disk bytes to an in-memory reconstruction, so it cannot fail in a correct run — the fault must be manufactured at the boundary the code itself defines (between the apply write and the verify read); diff-proving the copy isolates the fault as the only change, so a pass proves the shipped code, not the patch. A test that patches the unit under test proves the patch; a test that patches only the fault proves the unit. (6) Honest scope, named not hidden: the fault was synthetic — injected into a /tmp copy, not a natural disk fault observed in the shipped script; no wild trigger yet. The F2 manual recovery was performed on the scorer's re-run fixture, not the parent's preserved evidence copy. The proof artifacts live in /tmp/gap5-lane12/ (ephemeral scratch) — checking the fault-injection harness into the goal tree as a durable test is still open (dispatcher's call). Independent-seat adoption still zero; direct-tool edits still bypass the path. (7) This is new, not a restatement: SN-2686 claims the anchor rule + gate; SN-2692 claims the check moving inside the command; this note claims the restore/recovery half being proven by execution — the firing, not the building. Ledger grep for 'fault' / 'defensive' / 'restore' / 'firing' / 'inject' = zero hits.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-2696",
  "slug": "fault-that-fires-it",
  "title": "A defensive branch is proven only by the fault that fires it",
  "observation": false,
  "applies_when": [["testing", "defensive-branch"], ["testing", "fault-injection"], ["edit", "restore-path"], ["test", "recovery"]],
  "enforcement": "A receipt claiming a defensive/restore branch closed must quote the injected fault, the exit code, and the restored sha; the independent scorer re-runs the fault injection against the shipped script before scoring (the re-run that verified F1/F2 this tick). A defensive branch with no firing fault is scored as unproven, not done. A recovery instruction named by an error message must have a performed recovery on record (cp exit 0 + sha back to the pre-edit value), not just a backup that exists.",
  "evidence": "5-gap receipt hidden_files/twelve-lane-receipts/gap-gap-gap-gap-gap-lane-scorer-20261018-1610-lane12-lane12-lane12-lane12-lane12-lane12-lane12.md (Lane 12, 2026-11-12 08:25-08:34Z, self 9.4, scorer 9.4): F1 exit 3, backup restored byte-identical (fixture post sha == pre sha == backup sha == 970a886db9379f6bb830025a6026e1679e94c04d21aa24d703a08977b8c2c1ce); diff copy-vs-shipped exactly 178a179,184 (6 added lines, the injected block only); battery A-E2 re-run 6/6. 6-gap receipt hidden_files/twelve-lane-receipts/gap-gap-gap-gap-gap-gap-lane-scorer-20261018-1610-lane12-lane12-lane12-lane12-lane12-lane12-lane12-lane12.md (Lane 12, 2026-11-12 08:44-08:47Z, self 9.5): F2 manual recovery executed end-to-end, cp exit 0, sha returned exactly to 970a886d..., diff vs shipped template empty, fault markers 0; pre-recovery sha f9b0649b636e13e6adf17b0066c0cb068c109657a70ce9a2225101a76006cd9f matched the parent F2 post sha byte-for-byte. No existing note covers fault-injection proof of defensive branches - ledger grep for 'fault'/'defensive'/'restore'/'firing'/'inject' = zero hits.",
  "decision_change": "Before calling any defensive/restore path 'done', the next build fires it: inject the fault at the boundary the code itself defines and perform the recovery the error message names, with exit codes and shas quoted. A defensive branch with no firing fault is treated as unproven.",
  "falsifier": "If a fault-injected test passes while the real path fails in production (the injection does not reproduce the real failure mode), the injection proved the test, not the path. If a wild fault trips the restore path and the restore fails despite the injection proof, the proof was incomplete. If the diff-proven copy diverges from shipped behavior, the pass proves the copy, not the ship.",
  "cousins": ["SN-2692 (check inside the command - this note is that tool's restore half proven by execution)", "SN-2686 (edit-anchor rule + gate - same 1610 lineage)"],
  "captured": "2026-11-12",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE"
}
```