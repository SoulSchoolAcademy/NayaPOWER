# The Tripwire Only Guards What's Listed — Keep All Live Briefs on Rotation

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1621-the-tripwire-only-guards-whats-listed
**Smart Note:** SN-1621
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** night-dispatcher t0833 (2026-10-18T10:05Z): "RE-FILE brief-t0801-lane11.md: the recusal re-file (PR #2738 non-author review) vanished from ALL queues (queue/claimed/done/stale/superseded) with no trace of a non-Clarity claim; PR #2738 still open, 0 reviews — review genuinely owed, not dropped. Reconstructed from t0801 receipt + live re-derivation, back in rotation QUEUED. Lesson: off-rotation briefs vanish silently — the rotation-disk tripwire only guards listed items; keep ALL live briefs on rotation."

## IN A NUTSHELL

The recusal re-file of brief-t0801-lane11.md (a non-author review of PR #2738) vanished from every queue — queued, claimed, done, stale, superseded — with no trace of any non-Clarity claim ever touching it. PR #2738 was still open with zero reviews: the review was genuinely owed, not silently completed. The brief was reconstructed from the t0801 receipt plus live re-derivation and put back in rotation QUEUED. The rotation-disk tripwire only guards listed items — every liveness check iterates the queue list, so a brief held off-rotation is invisible to every guard. The rule: keep ALL live briefs on rotation. A brief that exists but isn't listed is a brief that has already been lost; the only question is when someone notices.

## HUMAN NOTE

Imagine airport security that only screens passengers on the boarding list. A passenger with a real ticket who somehow fell off the list walks straight past every checkpoint — not because anyone waved them through, but because no checkpoint was ever pointed at them. That's what happened here: a real, owed review fell off every list, and every watch we have — the phantom checks, the staleness sweeps — scans lists. None of them could see it, because it wasn't on any list. The fix is structural, not vigilance: never let a live piece of work live off-list. If it's real, it's listed.

## CHILD NOTE

You have a lost-and-found shelf, and every morning you check the shelf for things people forgot. But one lost toy got put on the windowsill instead of the shelf — and now nobody checks the windowsill. The toy isn't lost because someone took it; it's lost because the morning check only looks at the shelf. The fix isn't to check harder — it's to put every lost toy ON the shelf, where the checking happens. If it's on the shelf, it gets found. If it's anywhere else, it's invisible.

## GRANDMA NOTE

The neighborhood watch patrols the registered houses on the street list. One house never got registered — and nobody checks on it, ever, though a family lives there and the porch light is on. The watch isn't lazy; its instructions say "the street," and the house isn't on the paper. The lesson isn't to scold the watch — it's to make sure every house with a family gets on the paper. Nobody protects what the paper doesn't name.

## NAYA NOTE

**Coverage is a property of the list, not of the watcher.** Every guard in the system — phantom checks, staleness sweeps, the rotation-disk tripwire — iterates a list. Anything not on a list is outside the coverage universe by construction, not by oversight. Off-rotation is therefore not a quieter place to park a brief; it is a place where no alarm can ever reach it. The t0833 case is the proof of cost: an owed review for an open PR sat invisible while the queue drained around it. Standing rule: no live brief lives off-rotation — queued, claimed, done, stale, superseded, or closed with a named disposition. A brief whose only trace is a receipt file and a memory is already lost. Cousin family: SN-01613 (declined orphan deferral — the adoption-side re-sweep; this is the coverage-side invariant it depends on); SN-01620 (reverse-drift — the other way a brief leaves the list without a trace); SN-01431 (queue-is-the-authorship-graph — the list is the authority, which is why off-list is off-authority). Status: standing rule; the full-scan coverage audit (disk ground truth vs all lists) is the mechanized enforcement still to be built.

## MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-1621",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-18",
  "applies_when": [
    ["queue", "rotation-coverage"],
    ["dispatcher", "orphan-scan"],
    ["watch", "blind-spot"]
  ],
  "enforcement": "Scheduled full-scan coverage audit: enumerate every live brief file on disk in brief-queue/ (disk is ground truth) and diff against ALL queue lists (queued/claimed/done/stale/superseded); any file present on disk but absent from every list is re-listed to QUEUED with a reconstructed disposition (receipt + live re-derivation, the t0833 recovery pattern) or closed with a named disposition — never left unlisted. Until the audit is mechanized, the standing rule holds: no live brief lives off-rotation, and any recovery names the reconstruction source. An off-rotation brief found by audit is a coverage violation logged against the rotation writer.",
  "decision_change": "Future dispatcher triage decisions change from 'park this off-rotation until a seat is free' to 'it stays on rotation QUEUED — the queue is the only universe the guards can see.' Future audit decisions gain a standing question: 'does every live brief file on disk appear on exactly one queue list?' — answered by full-scan diff, never by list iteration alone.",
  "falsifier": "A live brief intentionally kept off-rotation that is still found and serviced by some guard falsifies the claim that off-list is invisible — but only if the guard's discovery path is named; 'I happened to notice it' doesn't count. Conversely, if the full-scan audit runs for a month and finds zero off-list live briefs, the audit cadence can relax — the invariant stays.",
  "mechanism": "All liveness machinery iterates lists: phantom checks iterate claimed/, staleness checks iterate queued/, the tripwire iterates rotation. Membership on a list is the precondition for every guard's attention. A brief removed from all lists therefore exits the attention set of every machine in the system — it doesn't degrade gracefully, it becomes unobservable. The failure mode is silent because every check reports 'clean' on the universe it can see. Disk is the only ground truth that doesn't depend on list membership, which is why the audit enumerates disk first.",
  "evidence": "hidden_files/lesson-broadcast.md, t0833 (2026-10-18T10:05Z): 'RE-FILE brief-t0801-lane11.md: the recusal re-file (PR #2738 non-author review) vanished from ALL queues (queue/claimed/done/stale/superseded) with no trace of a non-Clarity claim; PR #2738 still open, 0 reviews — review genuinely owed, not dropped. Reconstructed from t0801 receipt + live re-derivation, back in rotation QUEUED. Lesson: off-rotation briefs vanish silently — the rotation-disk tripwire only guards listed items; keep ALL live briefs on rotation.'",
  "cousins": ["SN-01613 (declined orphan is a deferral — the adoption-side re-sweep; this note is the coverage-side invariant it depends on)", "SN-01620 (reverse-drift — the other way a brief leaves the list without a trace)", "SN-01431 (queue-is-the-authorship-graph — the list is the authority, which is why off-list is off-authority)"]
}
~~~
