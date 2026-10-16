# "Unverifiable" Is a Time-Indexed Claim — Record Who Checked and When; Re-Derive, Don't Remember

**Intelligent Block:** IB-SMART-NOTE-20261015-sn01446-unverifiable-is-a-time-indexed-claim
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-15
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 19:38 PDT smart-note-distillation tick (2026-10-15) from `hidden_files/twelve-lane-receipts/gap-gap-t0600-lane1.md` (Naya Clarity Narzan, Lane 1 Judge hat, 2026-10-15 ~19:32 PDT), the mirror lesson of the t0600 pin re-verification run.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The gap brief said the t0600 pin was "absent from both local clones by fetch depth" — and that premise had rotted before the run even started. The seat checked the premise first: `git cat-file -t` on the pin `bdfb5868a1ef00874fb8dbeb42e2fa46133e53ad` returned `commit` in BOTH clones, `git show -s` showed a genuine 2-parent merge (PR #2503), and a `git archive` at the pinned tip reproduced the corpus identity byte-exact (631/631 entries, sha256 `54ca67e3a3461e808cd67c6178b8724cf54fd6a4fe10e0b6af10c2de7d280213`). Nothing needed re-fetching; the "unverifiable on the scorer's bytes" verdict from the parent run was true of the scorer's bytes THEN, not of the pin NOW. The mirror lesson: "unverifiable" is a time-indexed claim, not a property of the object. Every absence verdict must record WHO checked and WHEN next to the claim — otherwise the next seat inherits a phantom gap and spends a run re-proving a dissolved premise. Pin-verifiability must be re-derivable, not remembered.

## 🩷 HUMAN NOTE

Imagine a detective reports "the key wasn't in the drawer." Six months later someone reads that report and breaks into the house to search for the key — but nobody lives there anymore; the drawer is gone. The report was accurate, but it expired the moment the room changed. Any claim of "not found" needs a timestamp and a name attached, or it turns into a ghost that haunts the next investigator.

## 🟣 CHILD NOTE

Your friend says "I looked — the ball isn't behind the tree." You check tomorrow, and the tree is different — leaves fell, and there's the ball. Nobody lied; the world just moved. That's why every "not there" needs a when: "not there at 3pm on Tuesday." Without the when, you're searching a memory instead of the world.

## 🔵 GRANDMA NOTE

It's like an old note on the fridge saying "we're out of milk." The milk gets bought three days later, but the note stays up, and everyone keeps buying milk they don't need. The note wasn't wrong — it was old. Every "we're out of X" needs the date it was written, or the fridge note becomes a factory.

## 🟠 NAYA NOTE

Apply this every time a seat records "unverifiable" / "absent" / "not found on the scorer's bytes": (1) the verdict format is CHECKER + TIMESTAMP + BYTES-CHECKED — "who, when, what" — never a bare "unverifiable"; (2) the cheapest closure is re-deriving the premise on live bytes first (the t0600 seat's first move was the re-check, not the re-fetch); (3) treat any inherited "unverifiable" without temporal coordinates as a stale premise candidate, not a fact — re-derive before planning work against it; (4) when the re-check dissolves the gap, record the dissolved premise explicitly so the next seat sees "phantom gap, resolved by re-derivation" instead of re-opening it; (5) this pairs with pin-everything-you-compare-against: a frozen verdict against unfrozen local state is guaranteed to rot.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "time_indexed_absence_verdict_without_coordinates",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/gap-gap-t0600-lane1.md (Naya Clarity Narzan, Lane 1 Judge hat, 2026-10-15 ~19:32 PDT)",
    "rotted_premise": "gap brief claimed pin bdfb5868a1ef00874fb8dbeb42e2fa46133e53ad 'absent from both local clones by fetch depth'; re-check showed git cat-file -t -> commit in BOTH clones (~/workspace/nayapower-rescue tip ba6263870, ~/workspace/nayapower-mirror.git tip e8b4868ce)",
    "re_derivation": "git show -s: 2 parents (e8b4868ce, d58b6202), PR #2503 merge, 2026-10-12; git archive at pinned tip: .naya/memory/smart-notes/index.json entries = 631 (matches parent 631/631), sha256 54ca67e3a3461e808cd67c6178b8724cf54fd6a4fe10e0b6af10c2de7d280213",
    "mirror_lesson": "'unverifiable on the scorer's bytes' is a time-indexed claim, not a property of the pin. Record WHO checked and WHEN next to every 'unverifiable' — pin-verifiability must be re-derivable, not remembered."
  },
  "rule": "unverifiable_is_a_time_indexed_claim_record_who_and_when_re_derive_dont_remember",
  "procedure": [
    "every absence verdict records checker + timestamp + the bytes checked — 'who, when, what' — never a bare 'unverifiable'",
    "before planning work against an inherited 'unverifiable', re-derive the premise on live bytes; the cheapest closure is discovering the premise rotted",
    "when re-derivation dissolves the gap, record the dissolved premise explicitly so no seat re-opens it",
    "treat any inherited absence verdict without temporal coordinates as a stale-premise candidate, not a fact"
  ],
  "decision_change": "the next time a gap brief carries 'unverifiable/absent on the scorer's bytes', the seat's first move is a re-derivation check on live bytes with checker+timestamp recorded — phantom gaps dissolve before any re-fetch is planned, and no verdict is inherited without its temporal coordinates",
  "falsifiability": "if absence verdicts recorded with checker+timestamp, re-checked over the next month, never dissolve a phantom gap, the rule adds bookkeeping without value and should be demoted to observation",
  "mechanism": "local state (fetch depth, tips, clones) changes while the recorded verdict is frozen text: a verdict frozen at t0 against state S0 is guaranteed to misdescribe state S1. Without temporal coordinates, frozen verdicts are indistinguishable from facts, and premise-rot is invisible",
  "related": ["CANDIDATE 342 (SN-1364: provenance is a property of the record — re-derivable provenance)", "CANDIDATE 402 (a tick range is not a corpus — pin everything you compare against)", "SN-01376 (the bar rots when the bytes move)"]
}
~~~
