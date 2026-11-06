# INTELLIGENT BLOCK — SN-2209

**Intelligent Block:** IB-SMART-NOTE-20261106-sn02209-twin-run-shared-scratch-collision
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Drive-loop record 2026-11-06 03:38 PST (goals/nayapower-self-build-loop/hidden_files/drive-loop-2026-11-06.md, "03:38 PST tick — TIP MOVED, #212 retro-verified (TWIN RUN)"): a parallel worker ran the same 03:38 job (same stamp, same pin, same #212 item); its fetch.py (11:40:01Z) overwrote the first worker's fetch.py, its pincheck.py landed first while the first worker's write was refused; both workers' numbers agree everywhere they overlap, so the record survived by convergence, not by design. Duplication check this tick: branch naya4/smart-notes-2026-09-30 tip 5541bf9 (SN-02208) — git grep for "twin run / parallel worker / double dispatch / two workers" across BRAIN/05-MEMORY/SMART-NOTES/ on branch and main found 10 files; the three substantively nearest (SN-1091, SN-1749, SN-01992) were read in full and are distinct cousins (see MACHINE NOTE); no file states the per-run scratch-isolation rule. Counter ends at 2208; branch max SN-02208.

## ✦ IN A NUTSHELL

At 03:38 PST on 2026-11-06 two workers ran the same drive-loop tick — same stamp, same pin, same breach-#212 item. The twin's fetch script overwrote the first worker's fetch.py (11:40:01Z) and its pincheck landed first while the first worker's write was refused. Both workers converged on identical numbers, so nothing was lost from the record — but a worker's output WAS destroyed, and the record survived by luck, not by design. The lesson: **twin detection cannot serialize a simultaneous start.** Both workers legitimately started on an open slot, and the collision happened at the first write — before either could detect the other. The drive loop's own twin check ("no twin files exist yet") is a check-then-act race: both workers run it before either has written, both pass, both write. The fix is structural, not detective: **every run writes scratch files only under a per-run directory keyed by its unique run id**, so two twins can never share a filename. A check can tell you a twin exists; only isolation makes twins harmless.

## 🩷 HUMAN NOTE

Shawn — two workers got sent the same job at the same time this morning, and one overwrote the other's working file before either knew the other was there. Both reached the same answer, so the record survived — but that's luck, not design: the first worker's file was destroyed and its write was refused. The fix is simple and now standing: give every run its own folder to work in, so two copies of the same job can never step on each other's files. Checking "is anyone else here?" doesn't help when both arrive at the same second — separate folders do. Filed as Smart Note candidate SN-2209.

## 🟣 CHILD NOTE

Imagine you and your friend are both told to draw the same picture, and you both sit down at the same table with the same sheet of paper at the same time. You both start drawing — and your friend's crayon scribbles right over your lines. Neither of you did anything wrong; you just shared one sheet. The fix is easy: give each kid their own sheet of paper. Then it doesn't matter if two kids get the same job — they can never ruin each other's drawing.

## 🔵 GRANDMA NOTE

Dear, it is like sending two cooks to the same kitchen to make the same soup, both reaching for the same pot at the same moment — one pours over the other's work before either knows the other is there. Looking around first doesn't help when you both walk in together. The rule is simple: every cook gets their own pot. Then two cooks on the same recipe can never spoil each other's soup, and whichever finishes first, the meal is safe.

## 🟠 NAYA NOTE

For every seat that runs a job whose workers write scratch files: (1) never write scratch files to a fixed shared filename when a job can be dispatched twice — always write under a per-run directory keyed by the unique run id (tick stamp + run id); (2) the twin check ("are there files from another run?") is necessary but not sufficient — it races, because both twins run it before either writes, so both pass and both write; treat detection as a courtesy signal, never as the serialization mechanism; (3) if you find a same-stamp file you did not create, stop writing at once and reconcile read-only, letting the twin own the item — the duplicate's silence rule (SN-1091) applies to the loser; (4) the scheduler double-fires — twins happened on Nov 5 for breaches #196, #199, #200, #201 and again Nov 6 at 03:38 for #212, so treat twins as a recurring condition, not a one-off; (5) the 03:38 case is the first recorded one where detection failed and a write was actually destroyed — the earlier twins were detected in time and stood down without racing, which is why this failure mode stayed invisible until now.

## 🟢 MACHINE NOTE

```json
{
  "slug": "twin-run-shared-scratch-collision",
  "sn": "SN-2209",
  "title": "Twin Runs Collide on Shared Scratch — Detection Can't Serialize a Simultaneous Start",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-11-06",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "kind": "lesson",
  "applies_when": [["dispatch", "twin-run"], ["execution", "scratch-files"], ["coordination", "parallel-workers"]],
  "enforcement": "Worker scripts write scratch files only under a per-run directory keyed by the unique run id (tick stamp + run id); a pre-run check greps the job's scripts for writes to fixed shared scratch filenames and fails the run if any are found. A worker that finds a same-stamp file it did not create stops writing and reconciles read-only. Regression test: the next twin run must produce zero overwritten or refused files — any overwrite reopens this note.",
  "falsifier": "If two workers run the same tick with per-run scratch directories and a file is still overwritten or a write still refused, shared filenames were not the mechanism and this note is wrong. If the scheduler is proven to deliver exactly one worker per tick (dispatch log shows a single delivery per tick for 30 days), twins stop occurring and this note retires to OBSERVATION.",
  "decision_changed": "How parallel-capable jobs are built: scratch writes go to per-run directories keyed by run id instead of fixed shared filenames, and twin detection is treated as a courtesy signal rather than the serialization mechanism — so the next twin run is harmless by construction instead of lucky by convergence.",
  "mechanism": "The same tick stamp produces the same scratch filenames for both workers, and no lock or claim precedes the first write — both workers write within seconds of starting. Last-writer-wins destroys the loser's file (03:38: twin fetch.py 11:40:01Z overwrote the first worker's fetch.py; the first worker's pincheck write was refused). Detection ('do twin files exist?') cannot serialize this because it is itself a check-then-act race: both workers run the check before either has written, both pass, both write. Only isolating the write path — distinct directories per run — removes the shared mutable state the race needs.",
  "cousins": ["SN-1091 (duplicate dispatch of a closed slot writes nothing — the behavior rule once a duplicate is detected; this note is the concurrent open-slot case, where detection itself races)", "SN-1749 (check the claim registry before dispatching a row — works when a claim exists; cannot help when two starts are simultaneous and no claim exists yet)", "SN-01992 (a rebuild landing mid-sync is a race to re-check — the re-check remedy fits stale reads; here the loss is a destroyed write, so the remedy is isolation, not re-check)"],
  "provenance": "Drive-loop record 2026-11-06 03:38 PST (goals/nayapower-self-build-loop/hidden_files/drive-loop-2026-11-06.md, '03:38 PST tick — TIP MOVED, #212 retro-verified (TWIN RUN)'): parallel worker ran the same 03:38 job (same stamp, pin, #212 item); its fetch.py (11:40:01Z) overwrote the first worker's, its pincheck.py landed first (first worker's write refused), its pincheck.log (11:42:07) + followup.py/log (11:42:30/32) ran alongside the first worker's reads; both workers' numbers agree everywhere they overlap; 'no coordination channel exists between the two workers.' Second worker's sign-out entry (~/memory/2026-11-06.md, '03:38 PST — self-build sign-out + two record corrections'): 'both workers did the full verification independently and converged; no duplicated board posts... The shared-filename collision (fetch.py overwritten, record write refused) is the same process defect.' Prior twins (same handling, no file loss): Nov 5 20:08 breach #196, 21:08 #199, 21:38 #200, 22:08 #201 — detected and stood down without racing; 03:38 is the first recorded case where detection failed and a write was destroyed. Duplication check this tick: branch naya4/smart-notes-2026-09-30 tip 5541bf9 (SN-02208) — git grep 0 files stating the per-run scratch-isolation rule; nearest cousins SN-1091/SN-1749/SN-01992 read in full, distinct mechanisms above. Counter ends at 2208; branch max SN-02208; open-PR census 03:38 (6 open, none a Smart Note carrier; carrier PRs all closed, intelligence door is direct-write) + staging script's mechanical branch-tree claim check as backstop."
}
```
