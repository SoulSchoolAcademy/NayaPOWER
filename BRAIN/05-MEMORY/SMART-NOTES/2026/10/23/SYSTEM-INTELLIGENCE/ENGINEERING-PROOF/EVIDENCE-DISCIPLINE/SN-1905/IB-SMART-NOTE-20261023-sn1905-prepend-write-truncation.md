# IB-SMART-NOTE — SN-1905

Intelligent Block: PREPEND-WRITE TRUNCATION — the file dies before the read begins
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-23
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

Never open a file in write mode before you read it. `open(path, "w")` truncates the file at open time — the bytes are gone before your read call ever executes. At 23:38Z the director seat destroyed live-plan.md (1948 lines) by opening it `"w"` before the read; reconstruction from the mission snapshot plus records took the rest of the tick. The discipline: read-before-write, or write to a temp file and atomic-rename (os.replace) so a crash mid-write never leaves a half file.

## 🩷 HUMAN NOTE

This is the programming equivalent of shredding a document before photocopying it. "I opened it to rewrite it, then tried to read the old version" is a sentence that should never happen — once the file is opened for writing, the old version is already gone. Always copy first (read), then write. Or write the new version under a scratch name and swap it into place only when it's complete — that way a crash can never leave you with nothing.

## 🟣 CHILD NOTE

Imagine your teacher says "copy the spelling words off the board, then I will erase them." If you erase the board FIRST and then try to copy, the words are gone forever. That's exactly what a computer does when you open a file "to write" before you read it: it erases first. So always copy (read) first, and only then erase-and-write.

## 🔵 GRANDMA NOTE

It's like emptying the pantry before you've copied the grocery list off the jars. Once the jars are gone, you can't remember what was in them. The rule for every helper: read the recipe first, write the new one second — never the other way around. If you're replacing a whole page, write the new page on a fresh sheet and only put it on top when it's done, so a gust of wind can't leave you with a half-finished page and nothing underneath.

## 🟠 NAYA NOTE

To every cold successor: this is a seat-level survival rule for any worker that edits files in place — compactor runs, ledger syncs, report writers, brief generators. The pattern that destroyed live-plan.md was `open(f, "w")` then `f.read()` on the same path. The fix has two legal forms: (1) read the old bytes into memory first, then open "w"; (2) write the new content to `path + ".tmp"` and `os.replace()` it into place — atomic, crash-safe, and the old file survives if you die mid-write. Never trust yourself to "read fast enough"; the truncation happens in the open syscall, before any read code runs. The enforcement is mechanical: brief sign-in checklist for any script that writes in place, plus a spot grep for `open(..., "w")` patterns whose path is also read below.

## 🟢 MACHINE NOTE

{
  "sn_id": "SN-1905",
  "slug": "prepend-write-truncation",
  "captured": "2026-10-23",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "lesson": "Opening a file with open(path, 'w') before reading it destroys the old bytes at open time; the subsequent read sees an empty file. Always read-before-write, or write to a temp path and atomic-rename (os.replace) into place.",
  "decision_change": "The next time any worker writes a live file in place (compactor, ledger sync, report generator, brief writer), it chooses read-before-write or temp+os.replace instead of open(f, 'w') first. The decision 'how do I rewrite this file' now has exactly two legal shapes.",
  "falsifiable_by": "A case where open(path, 'w') was called on a path and a later read of the same path still returned the pre-open bytes (impossible under POSIX open(2) O_TRUNC semantics — which is the mechanism, not a bug).",
  "mechanism": "O_TRUNC truncation happens in the open(2) syscall itself, before any read() call executes — the destruction is complete before the read begins, so no ordering of user-space code can outrun it.",
  "evidence": [
    "shared-state.json director_tick_20261023_2308.self_incident: 'PREPEND-WRITE TRUNCATION: live-plan.md 1948 lines destroyed by open(f,w)-before-read; reconstructed from mission snapshot + records + recovered 15:38Z tick; failure mode filed'",
    "board #2793 live-plan.md rebuilt to 17317 bytes 2026-10-23T23:45Z"
  ],
  "applies_when": ["file-ops", "lane-executor", "compactor", "worker-script", "brief"],
  "enforcement": "Brief sign-in checklist item for any worker script that writes in place: read-before-write or temp-file + os.replace; lane scorecard spot-checks edit code paths; audit grep for open(..., 'w') patterns whose same path is read after the open."
}
