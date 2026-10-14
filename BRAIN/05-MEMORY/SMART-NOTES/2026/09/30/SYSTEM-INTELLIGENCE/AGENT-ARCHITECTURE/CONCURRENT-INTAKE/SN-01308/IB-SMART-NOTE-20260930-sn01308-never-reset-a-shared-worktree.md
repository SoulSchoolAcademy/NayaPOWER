# IB-SMART-NOTE-20261014-sn1308

**Intelligent Block:** SN-1308
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

Never reset a shared worktree — build with git plumbing instead. At t0769 (t0762-lane5, DEMOTE branch-only wiring, 9.0/10) the verdict's own falsifier fired mid-build: the local worktree's smart_note_v2.py carried only a score<=0 floor while the verdict quoted a 40.0 relevance floor, so the stale-base commit was abandoned (kept for the record) and re-wired against the live tip. The worktree was shared and concurrently mutated by another seat — so instead of resetting it, the seat built with git plumbing plus the git-data API, writing objects without touching the checked-out files. The standing lesson: a shared checkout is another seat's live environment; `git reset --hard` on it is a destructive action against someone else's in-flight build. Object writes are race-free; checkout mutations are not.

## HUMAN NOTE

Shawn — this is the rule that keeps two seats from breaking each other's work when they share a workspace. This morning a seat found mid-build that her base had gone stale (the code she was building on didn't match the live tip) — on her own machine the fix is a simple reset. But this worktree was shared: another seat was building there at the same time. Resetting would have yanked the files out from under the other seat's running build. So she did the professional thing: abandoned the stale commit (kept it in the record, didn't hide it), and rebuilt against the live tip using git's low-level plumbing — writing objects directly, never touching the files the other seat was using. The rule is now standing: shared worktrees are never reset. If your base went stale, rebuild with plumbing against the live tip.

## CHILD NOTE

Imagine two kids sharing one desk to build their LEGO castles. One kid realizes she needs a different baseplate. She can't just flip the whole desk over — the other kid's castle is right there! So she builds her new baseplate next to the desk and moves her castle onto it, without touching anything on the desk. The other kid's castle never wobbles. That's the rule: never flip the shared desk; build beside it.

## GRANDMA NOTE

Dear, the girls share their workshop now, and they learned a good manners rule this morning: never clear someone else's bench while they're working. One of them found her project was built on an outdated foundation mid-way through. On her own bench she'd just sweep it off and start over. But the bench was shared — her sister was working there too. So she built the corrected version alongside, without touching anything on the bench. No one lost their work. The standing rule: a shared bench is never swept; you build the correction next to it.

## NAYA NOTE

For every seat building in a shared worktree: (1) know when the checkout is shared — if another seat's claim is live on it, the files are not yours to move; (2) when the base goes stale mid-run (live bytes don't match the verdict's quoted mechanism — a falsifier firing), abandon the stale commit, keep it for the record, and rebuild against the live tip (re-pinned via git ls-remote at action time); (3) never `git reset --hard` / `git checkout -f` / `git clean -fd` a shared checkout — those mutate the files another seat's in-flight build is reading and writing; (4) build with git plumbing (hash-object / write-tree / commit-tree) or the git-data API: object writes land in the object DB without touching the checkout, so they cannot race the other seat's files. Evidence: hidden_files/lesson-broadcast.md [t0769] Dispatcher mirror (t0762-lane5 DEMOTE branch-only wiring, 9.0/10): "the worktree was also shared and concurrently mutated — never reset it; built with git plumbing + git-data API instead"; the falsifier (40.0 relevance floor quoted vs score<=0 floor in the local worktree's smart_note_v2.py) forced the abandon-and-rewire. Standing principles applied: live bytes; the brief is a hypothesis. Note: this is distinct from SN-0697 (commit identity/signatures) — that was about WHO a commit claims; this is about HOW to build when the ground is shared.

## MACHINE NOTE

```json
{
  "lesson_id": "SN-1308",
  "title": "Never reset a shared worktree — abandon the stale commit and rebuild with git plumbing against the live tip",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-14",
  "category": "SYSTEM-INTELLIGENCE/AGENT-ARCHITECTURE/CONCURRENT-INTAKE",
  "evidence": [
    "hidden_files/lesson-broadcast.md [t0769] Dispatcher (mirror, t0762-lane5 DEMOTE branch-only wiring, 9.0/10): 'the verdict's own falsifier fired mid-build — the local worktree's smart_note_v2.py had only a score<=0 floor while the verdict quoted a 40.0 relevance floor, so the stale-base commit was abandoned (kept for the record) and re-wired against the live tip. The worktree was also shared and concurrently mutated — never reset it; built with git plumbing + git-data API instead.'"
  ],
  "rule": "when the base goes stale mid-run on a shared worktree: abandon the stale commit (keep it for the record), re-pin the live tip via git ls-remote at action time, rebuild with git plumbing / git-data API — never git reset --hard / checkout -f / clean -fd a shared checkout",
  "anti_pattern": "resetting a concurrently-mutated shared worktree because 'my base is stale' — the reset moves the checked-out files another seat's in-flight build is reading and writing (silent base corruption / lost work); hiding the abandoned stale commit instead of keeping it for the record",
  "related": ["SN-0697", "SN-1307", "SN-0527"],
  "falsifier": "a reset of a shared, concurrently-mutated worktree with ref-log proof that the concurrent seat's in-flight build reproduced byte-identical afterward (reset shown harmless); or a plumbing-built commit shown byte-different from an equivalent clean-worktree build (plumbing shown unfaithful)",
  "decision_changed": "the recovery move when a lane's worktree base goes stale mid-run on shared ground (plumbing rebuild against the live tip, not reset); how concurrent-build lanes share checkouts safely; what the falsifier firing in a verdict obligates (abandon-and-rewire, never force-through)",
  "mechanism": "git reset --hard moves the shared checkout's files; a second seat's in-flight build may be reading/writing those same files, so the mutation races their build (silent corruption, lost work, untraceable). git plumbing (hash-object/write-tree/commit-tree) and the git-data API write objects into the object DB without touching the checked-out files — object writes are race-free against the other seat's checkout"
}
```
