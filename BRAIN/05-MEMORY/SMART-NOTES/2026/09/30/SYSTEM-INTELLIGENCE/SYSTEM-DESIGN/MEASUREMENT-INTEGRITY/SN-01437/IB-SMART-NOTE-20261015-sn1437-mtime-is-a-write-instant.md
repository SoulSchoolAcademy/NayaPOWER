# Intelligent Block
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-15 ~18:08 PDT (Smart Note distillation tick — staged by director completing timed-out worker run)
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**SN number:** SN-1437
**Provenance:** lane-executor standing task context (ORDERING root repair, 2026-10-15): "NEVER by file mtime (mtime changes on re-queue and lies about age)"; claim-brief.py mv+touch cure (root fix 2026-10-13): "mtime must mean claim time"; phantom-claim law claim-liveness audit (2026-10-13) 60-minute window.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## IN A NUTSHELL
File mtime records the last write instant — nothing more. Any protocol that reads mtime as an event timestamp is valid only if the write IS the event. The claim system works because the claim path does mv+touch at the claim instant (mtime = claim time by construction); the queue ORDERING rule refuses mtime because re-queues rewrite files and make mtime lie about age. Same attribute, opposite validity — the difference is whether the write and the event are the same act.

## HUMAN NOTE
On 2026-10-13 the team fixed a recurring failure class: briefs were being ordered and liveness-checked by file modification time, and the queue kept losing briefs. The root cause was embarrassingly simple — mtime doesn't record when a brief was *created* or *claimed*, it records when anything last *wrote* the file. Re-queue a brief and its mtime says "now," even though the brief is hours old. The cure had two halves that look contradictory until you see the principle: (1) the claim script does an explicit touch at claim instant, so mtime MEANS claim time — the write is the event, by construction; (2) queue ordering never trusts mtime and parses the timestamp embedded in the filename instead. The doctrine: mtime is a write instant. If you need it to mean an event, you must make the write be the event — deliberately, in code, every time. Anything else is reading a clock that isn't there.

## CHILD NOTE
Imagine a library book with a stamp that says when it was last touched — not when it was borrowed, just touched. If the librarian stamps it exactly when you borrow it, the stamp tells you the borrow time. But if anyone reshelving the book also stamps it, the stamp lies. Same stamp, different meaning — it only tells the truth when the stamp and the borrowing happen together, on purpose.

## GRANDMA NOTE
Darling, a file's timestamp is like the "last opened" date on a jar in the pantry — it tells you when someone last touched it, not when it was made or when it mattered. The team learned to only trust that date when they themselves put it there on purpose, at the exact moment that mattered. Any other time, they read the label instead. Simple rule: a timestamp only means what you made it mean.

## NAYA NOTE
Measurement-integrity doctrine, earned 2026-10-13–15: (1) The attribute: POSIX mtime = last write instant. It carries no event semantics on its own. (2) The valid use: claim-brief.py's mv+touch makes the claim write the file at the claim instant — mtime ≡ claim time by construction, and the phantom-claim liveness audit's 60-minute window is sound on that basis. (3) The invalid use: queue ORDERING by mtime — re-queues, hand-edits, and re-stagings rewrite files, so mtime lies about brief age; the ORDERING root repair (2026-10-15) mandates filename-embedded timestamps instead. (4) The doctrine: mtime is a write instant; treating it as an event timestamp requires the write to BE the event, enforced in code at the write site — never assumed at the read site. Evidence: lane-executor task context ORDERING §3 ("mtime changes on re-queue and lies about age"), claim-brief.py cure ("mtime must mean claim time", 2026-10-13), phantom-claim law claim-liveness audit (2026-10-13).

## MACHINE NOTE
```json
{
  "sn": "SN-1437",
  "slug": "mtime-is-a-write-instant",
  "category": "SYSTEM-DESIGN",
  "sub": "MEASUREMENT-INTEGRITY",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "lesson": "mtime records the last write instant, nothing more; reading it as an event timestamp is valid only when the write IS the event, enforced in code at the write site.",
  "mechanism": "POSIX mtime updates on any write. claim-brief.py's mv+touch binds the claim event to the write (mtime = claim time by construction). Queue re-queues rewrite files without any event occurring, so mtime diverges from brief age.",
  "decision_change": "Any future protocol that timestamps via mtime must either (a) perform an explicit touch at the event instant in code, or (b) use an embedded timestamp (e.g., filename) instead; assuming mtime means an event is a measurement-integrity violation.",
  "falsifiability": "A filesystem where mtime is set by the event source rather than the write path (e.g., content-addressed store with event-sourced timestamps) is outside this doctrine; checkable per measurement.",
  "evidence": ["lane-executor task context ORDERING §3 (2026-10-15)", "claim-brief.py mv+touch cure (2026-10-13)", "phantom-claim law claim-liveness audit (2026-10-13)"],
  "related": ["SN-1436 (prose-not-a-gate: enforcement must bind outside the actor's control — same class of misplaced trust)"]
}
```
