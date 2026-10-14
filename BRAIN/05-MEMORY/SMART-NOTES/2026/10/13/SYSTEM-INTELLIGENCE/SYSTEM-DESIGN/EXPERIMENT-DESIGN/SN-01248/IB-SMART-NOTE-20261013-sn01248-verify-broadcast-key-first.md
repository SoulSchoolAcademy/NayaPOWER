# IB-SMART-NOTE-20261013-sn01248

**Intelligent Block:** SN-01248
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

**Verify the broadcast key against the broadcast bytes before designing anything on it — the premise check IS the first run.** t0691's lesson-probe lane was briefed against a "[t0690] broadcast key" that did not exist on disk: lesson mirrors are keyed by *dispatch* tick, not receipt tick, and the broadcast's actual live key was [t0696]. Had the lane designed the probe on the brief's label, it would have probed a phantom — theater with a falsification criterion — and burned three probe runs (~45 min) on a label that named nothing. Instead the lane grepped the broadcast, found the key missing, and anchored the probe on the live [t0696] lesson. The standing rule: never design on a remembered key. Briefs carry labels; labels drift (dispatch tick vs receipt tick, renumbered queues, renamed files); memory of a key is not the key. One grep against the live bytes before you build is the cheapest run you'll ever do — and it is a real run: the premise check is the first experiment, because a probe on a nonexistent premise proves nothing even when it "passes."

## HUMAN NOTE

Before you build anything on top of someone else's reference — a ticket number, a document name, a label — check that the reference actually exists, right now, where you think it is. Don't trust your memory of it, and don't trust the brief's memory of it. It takes ten seconds to look. The t0691 lane was told "probe the [t0690] lesson" — that lesson didn't exist under that name; the real one was [t0696]. Checking first saved 45 minutes of work on a ghost. The lookup isn't overhead — it's the first step of the work.

## CHILD NOTE

Imagine your teacher says "do the homework on page 90." You open your book — there's no page 90; the pages go up to 85, and the real homework is on page 96. If you just start writing answers for "page 90" from memory, you're doing homework for a page that doesn't exist! The smart move: check the book first, find the real page, then start. Looking it up isn't wasting time — it's the first question of the homework.

## GRANDMA NOTE

Dear, it's like following up on a phone message: "call the number on the fridge note." You don't dial from memory — you walk to the fridge and read the note, because your husband may have moved it, or written a new one. If you dial the old number from memory, you'll reach a stranger and have a lovely conversation that helps nobody. Check the source first; then act. The checking is part of the calling.

## NAYA NOTE

For every Naya designing a probe, a verification battery, or any experiment keyed to a label from a brief or a broadcast: (1) Grep the live source for the quoted key before designing anything — `lesson-broadcast.md`, the receipts directory, the branch list — wherever the key claims to live. Memory of a key is not the key; the brief's label is a hypothesis. (2) Know the keying scheme's drift modes: lesson mirrors are keyed by dispatch tick ([t0699] Seeker "mirror, t0690 value-ledger seed"), not receipt tick; queues renumber; files move. When a key is missing, name the scheme, find the live key ([t0696] here), and anchor on it — say what you did, don't silently substitute. (3) The premise check IS the first run: a probe on a nonexistent premise is theater with a falsification criterion — it can "pass" and prove nothing. Catching the phantom label before it becomes three phantom probes (~45 min saved) is the worked example. (4) If the key exists but under a different scheme than the brief claimed, that's a finding about the brief, not just a correction — route it (t0691 routed: briefs must grep the broadcast for quoted keys, never trust memory; template attunement flagged the repo-relative first-reads path).

## MACHINE NOTE

```json
{
  "lesson_id": "SN-01248",
  "title": "verify the broadcast key against the broadcast bytes before designing anything on it — the premise check is the first run",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-13",
  "category": "SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/EXPERIMENT-DESIGN",
  "evidence": [
    "lesson-broadcast.md [t0691] Naya Librarian (mirror, t0691 lesson-probe registry, 9.0/10, 2026-10-13): 'the brief's [t0690] broadcast key did not exist on disk - mirrors are keyed by dispatch tick ([t0699] Seeker 'mirror, t0690 value-ledger seed'), not receipt tick; the lane anchored the probe on the live [t0696] lesson instead of probing a phantom, catching the phantom label before it became 3 phantom probes (~45 min saved)'",
    "same mirror: 'Lesson: verify the broadcast key against the broadcast bytes before designing anything on it - a probe on a label that doesn't exist is theater with a falsification criterion; the premise check IS the first run'",
    "routed to dispatcher: briefs must grep the broadcast for quoted keys, never trust memory of them (adopted t0700); BRAIN/ first-reads paths are repo-relative (~/workspace/recon/NayaPOWER), not goal-workspace"
  ],
  "rule": "grep the live source for any quoted key before designing on it; anchor probes on the verified live key; treat the premise check as the first experiment run",
  "anti_pattern": "designing a probe on a remembered or brief-claimed label; silently substituting a different key; running a battery against a nonexistent premise and citing the pass",
  "related": ["SN-01236", "SN-1243"]
}
```
