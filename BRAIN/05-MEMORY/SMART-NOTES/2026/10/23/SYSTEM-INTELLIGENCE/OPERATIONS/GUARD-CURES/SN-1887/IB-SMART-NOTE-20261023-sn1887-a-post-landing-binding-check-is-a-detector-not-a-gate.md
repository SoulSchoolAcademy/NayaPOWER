Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-23
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL
A binding check that runs only after landing is a detector, not a gate: the door's hash-binding check must run on the final filing bytes BEFORE the filing lands.

## 🩷 HUMAN NOTE
On 2026-10-23 the sanctioned SN-1854 Smart Note door filing landed with a broken link: the registry entry's content_hash matched no capture on disk. The Door Obligation check caught it 56 minutes later, in CI, after it was already on the tip — so the team had to reconcile a corrupted binding under pressure instead of never letting it land. The check existed; it just ran in the wrong place. From now on the door runs the same hash-binding check on the final bytes before publication, not only after. A detector tells you what broke. A gate keeps it out.

## 🟣 CHILD NOTE
Imagine a factory that builds toys and checks every toy for broken parts — but only checks AFTER the toy is already in the store's window. The broken toy still got to the store, and someone has to rush over and take it down. The smart move: check the toy one more time right before it goes into the window. Same toy, same check — just earlier. That's what the door now does with Smart Notes.

## 🔵 GRANDMA NOTE
It's like mailing a letter with the wrong address on the envelope. The post office does notice — but only after the letter is already gone, so you have to chase it down. Checking the address before you drop it in the mailbox is the same check, done in time to matter. The filing system now checks its envelopes before posting.

## 🟠 NAYA NOTE
For the door lane and the KNOW/registry lane: this is the per-entry sibling of L648/MANIFEST_STALE (the whole-index seal broken by a one-sided re-stamp, audit 6365670544). There the binding was corpus_manifest_hash vs the full entry list; here it is a single registry entry's content_hash vs its capture bytes. Same failure family — the seal is re-stamped while the referenced bytes are not recomputed together — but a different binding and, until now, only a post-landing check. The standing rule: every content-addressed binding the door publishes gets its negative check in the prepublication path, on the final bytes. Post-landing CI keeps the identical check as the backstop witness, never as the gate.

## 🟢 MACHINE NOTE
{
  "id": "SN-1887",
  "slug": "a-post-landing-binding-check-is-a-detector-not-a-gate",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-23",
  "lesson": "A content-addressed binding check that runs only in post-landing CI is a detector, not a gate: the corrupted binding still reaches the tip and must be reconciled under pressure. The door's hash-binding check must run on the final filing bytes in the prepublication path; post-landing CI remains the backstop witness, never the gate.",
  "evidence": [
    "board #2793 comment 6371339622 (independent read-only continuity audit, 2026-10-23T17:56:50Z): Door Obligation job 120543963091 FAILED 'MISSING: hash binding for SN-1854 - no capture on disk hashes to the registry entry's content_hash'; Kernel Tests job corroborates captures_unregistered_by_hash 20->21 naming SN-1854; exact tip c60ff22c",
    "director tick 2026-10-23 11:08 PDT (live-plan.md): SN-1854 door filing landed 17:00:09Z; mismatch discovered ~56 minutes later by CI, not pre-publication",
    "sibling class L648/MANIFEST_STALE (audit 6365670544, 2026-10-23): whole-index seal re-stamped without recomputing the entry list - same one-sided re-stamp family, different binding"
  ],
  "decision_change": "Whether a door filing lands without a prepublication hash-binding pass. Future door filings run the negative binding check on the final bytes before landing; a filing whose capture does not hash to its registry content_hash fails closed pre-publication instead of being discovered by CI 56 minutes later.",
  "falsifier": "If the SN-1854 door filing already ran a prepublication hash-binding check that passed while post-landing CI failed, the check is broken rather than absent, and this lesson misdiagnoses the placement.",
  "mechanism": "Content-addressed bindings break in one direction: the seal (registry content_hash) is re-stamped while the referenced bytes (capture on disk) are not recomputed/committed together, or vice versa. A post-landing check observes the break after the fact; only a prepublication check on the final bytes closes the land-to-CI-green window during which downstream jobs trip on the corrupted state.",
  "applies_when": ["door", "publication", "hash-binding", "filing"],
  "enforcement": "The Door Obligation 'MISSING: hash binding' check runs on the final filing bytes in the door's prepublication path; a filing whose capture does not hash to its registry content_hash fails closed before landing. Door Obligation CI keeps the identical check as the backstop witness, not the gate."
}
