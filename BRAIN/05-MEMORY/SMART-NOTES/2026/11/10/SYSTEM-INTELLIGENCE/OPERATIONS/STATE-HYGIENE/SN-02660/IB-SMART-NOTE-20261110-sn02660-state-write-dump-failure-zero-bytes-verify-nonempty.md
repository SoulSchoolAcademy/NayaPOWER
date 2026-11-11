**Intelligent Block:** IB-SMART-NOTE-20261110-sn02660-state-write-dump-failure-zero-bytes-verify-nonempty
**Smart Note:** SN-2660
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-10
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Staged by the smart-note distillation loop 2026-11-10 23:38 PST. Evidence: director tick 2026-11-11T06:38Z (shared-state.json key director_tick_20261111_0638z on disk); compactor backup shared-state-backup-20261111-0640.json verified present on disk this tick; memory log ~/memory/2026-11-10.md "Director pass 22:38 PST" entry records the same self-repair. Zero GitHub REST calls this tick for #1354 (capped at 2500 comments, commenting disabled 2026-10-10); App route used only by the staging script.

## ✦ IN A NUTSHELL

An inline script truncated shared-state.json — the single file every seat coordinates through — to 0 bytes. A bad json.dump kwarg raised after open(f, 'w') had already truncated the file, and the dump is not atomic: any failure between the open and a completed dump leaves a 0-byte file. The director caught it, restored the file byte-identical from the compactor backup (shared-state-backup-20261111-0640.json), re-compacted, and verified valid JSON with all tick updates intact. The durable rule: state writes go through script files only, never inline, and every state write is verified non-empty afterward — fail the tick if the file is 0 bytes or smaller than before the write, and restore from the compactor backup, never re-derive by hand. SN-2207's "check the file size after every write" does not catch this: it is cap-oriented (fail if over 200,000 bytes), and a 0-byte file passes it. The non-empty check is a separate, mandatory gate.

## 🩷 HUMAN NOTE

Shawn — the shared-state file, the one every seat coordinates through, was wiped to zero bytes this evening by a script error: the write opened the file, which emptied it at once, and then the write itself failed before putting anything back. It was caught and restored exactly from the automatic backup, with nothing lost. The lesson that stays: a file that is opened for writing is empty from that instant, so a failed write is silent destruction, not a harmless error. From here on, state writes go through proper script files only, and every write gets checked afterward — the file must still be there, full and valid, or the tick fails and the backup is restored. A size check that only looks for "too big" would have waved a zero-byte file straight through.

## 🟣 CHILD NOTE

Imagine you erase your whole homework page before you start writing the new answers — and then your pencil breaks. The page is blank, and the old answers are gone. That is what happened to the shared-state file: opening it for writing erased it first, and the write broke before it could put anything back. The fix is simple — always write on a practice sheet first, then check the real page is still full and correct afterward, and keep a photocopy of the page so a blank page can always be restored.

## 🔵 GRANDMA NOTE

Dear, the recipe book was opened to rewrite a page, and the moment it opened the old page was gone — the pen ran dry before a single word was written back. We were lucky: a photocopy of the book sat in the drawer, and the page came back word for word. The rule for every rewrite from now on: never write straight into the book without a copy in the drawer, and always read the page back afterward to make sure it is still there and still full. Checking only that the book isn't too thick would never catch an empty page.

## 🟠 NAYA NOTE

The verified facts: (1) Director tick 2026-11-10 22:38 PST (executed 2026-11-11T06:38:06Z), shared-state.json key director_tick_20261111_0638z on disk: "SELF-REPAIR: my inline script truncated shared-state.json to 0 bytes (bad json.dump kwarg); restored byte-identical from compactor backup shared-state-backup-20261111-0640.json and re-compacted — verified valid JSON, all tick updates intact. Lesson: script files only for state writes; verify non-empty after write." (2) The backup file shared-state-backup-20261111-0640.json is present on disk, verified this tick. (3) The mechanism: open(f, 'w') truncates immediately; json.dump raising afterward leaves the 0-byte file — the write is not atomic, and the failure mode is silent unless the writer checks afterward. (4) Why this is not a repeat of SN-1905 or SN-2207: SN-1905 (prepend-write truncation) rules on reading before opening for write — this incident had the bytes in hand; the dump itself failed. SN-2207 (shared-state stays compact) rules on checking size against the 200,000-byte cap — a 0-byte file passes that check. Neither rule would have prevented or caught this incident; the non-empty-after-write rule closes the hole. (5) Honest hole, stated not hidden: the exact bad kwarg is not recorded in the tick text — the mechanism (open-truncate, then dump raises) is the director's own diagnosis, quoted in the tick, and this note adopts it as diagnosed, not as independently re-derived. The byte-identical restoration was verified by the director, not re-verified by this tick. Cousins: SN-1905 (prepend-write truncation — open(f, 'w') before read destroys the file; same silent-truncation family, different trigger), SN-2207 (shared-state stays compact — check size after every write; cap-oriented, does not catch a 0-byte file), SN-2652 (shared-state concurrent-writer clobber — the other shared-state write hazard).

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-2660",
  "slug": "state-write-dump-failure-zero-bytes-verify-nonempty",
  "title": "A failed dump after truncate leaves a 0-byte state file — verify non-empty after every state write",
  "observation": false,
  "applies_when": [["state-write", "shared-state"], ["state-write", "json-dump"], ["state-write", "zero-byte-truncation"]],
  "enforcement": "After every shared-state.json write: (1) assert the file is non-empty and its byte size is at least the pre-write size — a 0-byte or shrunken result fails the tick immediately; (2) state writes run only from script files, never inline — the bad-kwarg truncation happened in an inline script; (3) a 0-byte result is restored byte-identical from the latest compactor backup (shared-state-backup-*.json), never re-derived by hand, and the restore is re-verified with json.load before the tick continues. SN-2207's size check (fail if over 200,000 bytes) does NOT catch this — a 0-byte file passes it — so the non-empty check is a separate, mandatory gate.",
  "evidence": "Director tick 2026-11-10 22:38 PST (executed 2026-11-11T06:38:06Z), shared-state.json key director_tick_20261111_0638z on disk: inline script truncated shared-state.json to 0 bytes (bad json.dump kwarg); restored byte-identical from compactor backup shared-state-backup-20261111-0640.json and re-compacted; verified valid JSON, all tick updates intact. Backup file verified present on disk this tick. Memory log ~/memory/2026-11-10.md 'Director pass 22:38 PST' entry records the same self-repair and the lesson 'script files only for state writes; verify non-empty after write.'",
  "decision_change": "Any seat writing shared-state.json (or any state file) must verify the file is non-empty after the write and fail the tick on 0 bytes; a write verified only against the 200KB cap is unverified. On a 0-byte result, the seat restores from the compactor backup instead of rewriting from memory.",
  "falsifier": "Refuted if a 0-byte shared-state.json is shown to have been produced by a cause other than open-truncate-then-dump-failure (e.g. an external process truncating the file), or if a dump failure after truncate is shown to leave the previous bytes intact on this host. Bounded: the rule fires only for writes through open(f, 'w') + json.dump; a write-temp-then-atomic-rename path is immune by construction and the rule must not be used to demand post-write checks on an atomic path.",
  "cousins": ["SN-1905 (prepend-write truncation — open(f, 'w') before read destroys the file; same silent-truncation family, different trigger)", "SN-2207 (shared-state stays compact — check size after every write; cap-oriented, does not catch a 0-byte file)", "SN-2652 (shared-state concurrent-writer clobber — the other shared-state write hazard)"],
  "captured": "2026-11-10",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE"
}
```
