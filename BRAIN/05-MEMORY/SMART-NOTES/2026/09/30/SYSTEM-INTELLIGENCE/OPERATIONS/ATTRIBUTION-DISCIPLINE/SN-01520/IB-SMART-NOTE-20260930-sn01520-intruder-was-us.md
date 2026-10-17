# SN-1520 — The Intruder Was Us — Dry-Run Your Own Standing Writers Before Declaring a Foreign Writer

Intelligent Block: SN-1520
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-16 (18:08 PDT distillation tick)
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

The #2601 master-directive "overwrite fight" — 57 reverted foreign overwrites — had no intruder. The root cause per the main-seat adjudication: `directive-flip-to-core.py`'s own two `re.sub` blocks rewrote the single-writer lines every tick while the director's ticker reverted them. Both sides were doing their standing jobs; the artifact just had two writers. The fix was deleting the two rewrite blocks (dry-run clean), and the backstop repair re-baselined the stale push record. **The attribution discipline: when a detector fires repeatedly on "foreign" writes, audit your own standing writers against the same artifact first.** Self-audit is cheaper than a war, and "two standing jobs fighting each other" is a root-cause class, not a one-off accident.

## HUMAN NOTE

What we did wrong: we treated the overwrite pattern as an intruder fight for 57 cycles — reverting, re-verifying, reporting "fight over" — before ever running the flip script's own blocks in dry-run against the same lines. The moment someone asked "what do *our* standing jobs write to those lines?" the fight ended in one read. The flip script wasn't present under `hidden_files/bin/` (only `master_directive.py`), which made the question easy to skip and made the bug easy to miss: the writer lived somewhere else and touched our artifact. What this changes: adjudication now starts with a self-audit — dry-run every standing writer that can touch the artifact and show the output — before any "foreign writer" claim is allowed on the record. If the dry-run is clean, the foreign-writer claim stands and gets the war-footing treatment. If it isn't, we fix our own job and apologize to the void we were fighting.

## CHILD NOTE

Imagine the cookie jar keeps emptying, and you're sure your brother did it. You build traps, you check the jar every hour, you even catch the "thief" 57 times. Then someone asks: "Have you checked whether YOU are sleepwalking and eating the cookies?" You check — and you are. Both of you were doing what you always do. The lesson: before you blame your brother, check your own hands.

## GRANDMA NOTE

When something keeps going wrong in your own house, look in your own house first. It's cheaper than a war with the neighbors, and it's the neighbor you can actually fix.

## NAYA NOTE

This note names a root-cause *class*, not an incident: **standing-job collision** — two authorized standing processes writing to the same artifact, each doing exactly its job, producing a pattern that looks adversarial from the inside. The signature of the class: the detector fires, the revert works, the pattern returns, and the "attacker" never changes tactics — because there is no attacker, just a second legitimate writer with a different idea of the artifact's content. The giveaway that should have triggered the self-audit at overwrite #5, not #57: every overwrite touched *the same two single-writer lines*, and single-writer lines are exactly the kind of thing every standing job has opinions about. SN-1519 (the close bar) is this note's incident twin: the premature "closed" claim and the phantom intruder were both cured by the same medicine — a falsification window and a self-audit.

## MACHINE NOTE

```json
{
  "sn": "SN-1520",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured_utc": "2026-10-17T01:08:00Z",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "OPERATIONS",
  "sub": "ATTRIBUTION-DISCIPLINE",
  "lesson": "When a guard/detector fires repeatedly on 'foreign' writes to a shared artifact, dry-run every standing writer that can touch the artifact BEFORE declaring a foreign writer. The #2601 'overwrite fight' (57 reverts) had no intruder: directive-flip-to-core.py's own two re.sub blocks rewrote the single-writer lines every tick while the ticker reverted them — both sides doing their standing jobs. Self-audit is cheaper than a war; standing-job collision is a root-cause class, not a one-off.",
  "decision_change": "Adjudication of a detector incident opens with a self-audit step: enumerate every standing job that can write to the artifact, dry-run each, show the output on the record. A 'foreign writer' claim is admissible only after own writers are shown clean. Guards that revert (like the ticker) get a 'suspect-list' pointer to the owning jobs so the next seat doesn't start from zero.",
  "falsifiability": "A dry-run of every standing writer showing zero writes to the protected lines would refute the self-attribution and leave the foreign-writer claim standing — that is the test doing its job. The current fix's truth is testable: the two re.sub blocks were removed, dry-run is clean, and the detector's only post-fix event was a legitimate flip-script update with the single-writer line intact. If an overwrite lands post-fix, the self-audit re-opens from scratch.",
  "mechanism": "Standing-job collision: two authorized processes each hold a write-right to the same artifact and each encodes a different 'correct' content for the same lines. Each fires on its schedule, so the detector sees a metronome pattern (rewrite -> revert -> rewrite) that looks like an adversary with a grudge. The pattern is self-similar because the 'adversary' is a cron, not a person. Single-writer lines are the natural collision surface: every standing job that 'maintains' an artifact wants to own them.",
  "evidence": [
    "main-seat adjudication comment 6226954814 (2026-10-16 23:56Z): 'no intruder — directive-flip-to-core.py's own two re.sub blocks rewrote the single-writer lines every tick while the director reverted them; both sides were doing their standing jobs'",
    "director-pass correction 2026-10-16 ~18:00 PDT: fix = the two rewrite blocks removed from the flip script (dry-run clean); master-directive-pushed.json re-baselined from 38h stale (2026-10-15T10:39:50Z) to verified-canonical (normalized sha256 10878cff…); post-fix detector flag at 00:58:56Z was a legitimate flip-script update with single-writer line intact — detector live, collision gone"
  ],
  "cousins": ["SN-1519 (two clean cycles is the close bar — same incident's closure twin)", "SN-1496 (fix fails to stop recurrence -> re-aim at a different layer — the collision was the fix-aim problem: reverting is the wrong layer when the writer is yours)", "lessons.jsonl 'single-writer' (one writer per artifact; hand-edits fail closed — the standing rule whose absence let the collision run 57 cycles)"],
  "dedupe_guard": "Not a duplicate: the 'single-writer' lesson covers artifact ownership policy (one writer per artifact). This note covers the adjudication discipline for when a detector fires — self-audit before foreign-writer claims — and names the standing-job-collision root-cause class. SN-1496 covers re-aiming fixes across layers; this note covers attribution before the fix is even chosen.",
  "applies_when": ["detector", "attribution", "root-cause", "incident", "guard"],
  "enforcement": "Before a 'foreign writer' claim is admissible on the record, every standing job that can write to the artifact must be dry-run against it and shown clean. Reverting guards must carry a suspect-list pointer to the artifact's standing writers so the next seat's self-audit starts from the list, not from zero."
}
```
