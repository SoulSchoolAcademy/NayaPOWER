# INTELLIGENT BLOCK — SN-2215

**Intelligent Block:** IB-SMART-NOTE-20261106-sn02215-cap-crossed-compaction-cannot-archive-what-it-does-not-cover
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Main-seat verification ~14:06 PST 2026-11-06 (memory log ~/memory/2026-11-06.md): shared-state.json stat 208,831 bytes — over the 200,000-byte cap; was 199,575 at ~13:35 (425 below the cap), crossed within ~30 min at ~5KB/tick (night-dispatcher t2852, 2026-11-06T22:02Z). Director pass 13:38 PST (22:06:18Z): 209,308 bytes after compaction + re-adds — above the bar by 9,308; bloat class named: breach_* keys, 71,757 bytes across 65 keys, never archived by the compactor; the compactor writes compact JSON while tick scripts re-add with indent=1 (~7KB re-expansion). twelve-lane-rotation.json 1,789,731 bytes (main seat verified), mostly dispatcher_note_* keys — the same never-archived per-tick-key class. TIME-BOX LAW names >200KB a failure mode to fix, not work around. Duplication check this tick: main registry index at live tip 594a7b54 (1,258 entries) 0 hits for 200kb / 200,000 / compactor / shared-state / bloat; branch tree at tip 10f4c605 (9,166 entries) 0 'bloat' paths; cousins SN-2207 (indent-whitespace cost — different mechanism) and SN-1964 (compactor tick-sort timezone normalization — different subject); lessons.jsonl 0 hits for 200KB / compactor / shared-state / bloat / breach_ (single 'cap' hit is prepend-not-overwrite, unrelated). Number census: SN-02215 absent from the branch tree; counter 2214 → 2215; open PRs #3262, #3178, #3089 (App route this tick) claim no SN file; #1354 capped at 2,500 comments, commenting disabled 2026-10-10.

## ✦ IN A NUTSHELL

shared-state.json crossed its 200,000-byte cap today: 208,831 bytes at ~14:06 PST, up from 199,575 at ~13:35 — a ~30-minute crossing at ~5KB per tick. Compaction ran and could not stop it, because the bloat is breach_* keys (71,757 bytes across 65 keys) that the compactor's archive set never covers, and tick scripts re-add with indent=1, re-expanding ~7KB per write. A compactor that cannot archive the class that is growing is not holding the cap — it is watching it be crossed. The fix is a root repair, not another compaction run: extend the compactor's archive set to breach_* keys older than the newest 6, cap the relay list by bytes, and stop indent=1 re-adds.

## 🩷 HUMAN NOTE

Shawn — the file that holds the whole system's shared state has a hard size limit of 200,000 bytes, and today it went over it: 208,831 bytes, crossed in about half an hour. The cleanup tool ran and didn't help, because the growth isn't clutter it knows how to remove — it's 65 breach-record entries, 71,757 bytes, that the cleanup tool's list simply doesn't include, and every tick's rewrite adds the file back in pretty-printed form, which re-expands it by about 7KB. Running the same cleanup again won't fix this; the cleanup tool itself has to be taught to archive the breach records, and the relay list has to be capped by size instead of count. The same pattern is already at 1.79MB in the rotation file, which grows one entry per tick with nothing ever archiving it.

## 🟣 CHILD NOTE

Imagine a toy box with a rule: it can only hold so much, and someone is supposed to tidy it every day. But the tidier only ever puts away the red toys — and the box is filling up with blue toys nobody ever puts away. No matter how many times the tidier tidies, the box keeps overflowing, because the blue toys are never on the tidy list. The fix isn't tidying harder — it's adding blue toys to the tidy list. And there's a second box filling up the same way, one toy per day, that nobody has tidied at all.

## 🔵 GRANDMA NOTE

Dear, it is like a pantry with a strict shelf limit, and the housekeeper sweeps it every morning — but she only ever clears the top shelf. The bottom shelf keeps filling with jars nobody touches, until the whole pantry overflows. Sweeping the top shelf again won't help; the housekeeper has to be told the bottom shelf counts too. The lesson is simple: a cleanup that doesn't cover what's actually growing isn't a cleanup — it's a ritual. Check what the broom reaches before you trust the floor is clean.

## 🟠 NAYA NOTE

For every seat that reads or writes shared-state.json: (1) the file is OVER its 200,000-byte cap — 208,831 bytes verified ~14:06 PST 2026-11-06, crossed from 199,575 in ~30 minutes at ~5KB/tick — and every job's STEP 0 read now operates on an over-cap file; (2) do NOT treat another compaction run as the fix — the compactor ran and the file still crossed, because its archive set excludes breach_* keys (71,757 bytes, 65 keys, never archived) and tick scripts re-add with indent=1 (~7KB re-expansion per write, the SN-2207 mechanism); (3) the root repair is: extend compact-shared-state.py's archive set to breach_* keys older than the newest 6 (same pattern as director_tick_*), cap the naya2_to_builder relay list by bytes not count, and stop indent=1 re-adds; (4) verify the repair by a compactor run that drops the file by ≥50KB and holds it below 200,000 across subsequent ticks — if it does not shrink while breach_* keys grow, the coverage gap is still open; (5) the same class is already at 1,789,731 bytes in twelve-lane-rotation.json (dispatcher_note_* keys, one per tick, no archival) — the archival need covers both files, and any state file with a per-tick key class needs its archiver to cover that class, or it will cross its cap the same way.

## 🟢 MACHINE NOTE

```json
{
  "slug": "cap-crossed-compaction-cannot-archive-what-it-does-not-cover",
  "sn": "SN-2215",
  "title": "The Cap Is Crossed — Compaction Can't Archive What It Doesn't Cover",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-11-06",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "kind": "lesson",
  "applies_when": ["state", "shared-state", "budget", "cap", "compaction", "archival"],
  "enforcement": "Post-write size check on shared-state.json after every write — fail/flag the tick if it exceeds 200,000 bytes. Compactor coverage test: the archive set must include breach_* keys older than the newest 6, verified by a compactor run dropping the file by >=50KB and holding it below 200,000 across subsequent ticks; the relay list is capped by bytes, not count. Regression check: run the compactor and assert shared-state shrinks; if it does not shrink while breach_* keys grow, the coverage gap is still open.",
  "falsifier": "A compactor run that archives breach_* keys drops shared-state by ~70KB and it holds below 200,000 bytes across subsequent ticks; or the file stays under 200,000 for a full day with no archival (growth stopped). Either would show the crossing was a transient spike, not a coverage gap, and collapse this note.",
  "decision_changed": "When shared-state crosses 200,000 bytes, run the root repair — extend the compactor's archive set to breach_* keys older than the newest 6 and cap the relay list by bytes — instead of re-running a compaction that cannot touch the bloat class; and stop tick scripts re-adding with indent=1. A cap breach is now diagnosed by which key class is growing and whether the archiver covers it, not by whether compaction ran.",
  "mechanism": "breach_* keys accumulate ~3-5KB per tick and the compactor's archive set excludes them, so compaction removes only the classes it covers while the breach class grows unchecked; tick scripts re-add with indent=1, re-expanding ~7KB per write (the SN-2207 mechanism). Net growth outruns compaction, so the file crosses the 200,000-byte cap even though compaction 'ran'. The same mechanism is visible in twelve-lane-rotation.json at 1,789,731 bytes: dispatcher_note_* keys, one per tick, with no archival at all.",
  "provenance": "Main-seat verification ~14:06 PST 2026-11-06 (memory log ~/memory/2026-11-06.md): shared-state.json stat 208,831 bytes — over the 200,000-byte cap; was 199,575 at ~13:35 (425 below the cap), crossed within ~30 min at ~5KB/tick (night-dispatcher t2852, 2026-11-06T22:02Z). Director pass 13:38 PST (22:06:18Z): 209,308 bytes after compaction + re-adds — above the bar by 9,308; bloat class named: breach_* keys, 71,757 bytes across 65 keys, never archived by the compactor; the compactor writes compact JSON while tick scripts re-add with indent=1 (~7KB re-expansion). twelve-lane-rotation.json 1,789,731 bytes (main seat verified), mostly dispatcher_note_* keys. TIME-BOX LAW names >200KB a failure mode to fix, not work around. Duplication check this tick: main registry index at live tip 594a7b54 (1,258 entries) 0 hits for 200kb / 200,000 / compactor / shared-state / bloat; branch tree at tip 10f4c605 (9,166 entries) 0 'bloat' paths; cousins SN-2207 (indent-whitespace cost — different mechanism) and SN-1964 (compactor tick-sort timezone normalization — different subject); lessons.jsonl 0 hits for 200KB / compactor / shared-state / bloat / breach_ (single 'cap' hit is prepend-not-overwrite, unrelated). Number census: SN-02215 absent from the branch tree; counter 2214 → 2215; open PRs #3262, #3178, #3089 (App route this tick) claim no SN file; #1354 capped at 2,500 comments, commenting disabled 2026-10-10."
}
```
