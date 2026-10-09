# Retrieve reads the projection index, not the capture directory

**Intelligent Block:** IB-SMART-NOTE-20261009-f9596844-retrieve-reads-the-projection-index-not-the-capt
**Truth state:** VERIFIED
**Scope:** PRIVATE
**Captured:** 2026-10-09
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A capture file alone is invisible to retrieve(); the projection index entry plus a valid projection file is what makes a note retrievable.

## 🩷 HUMAN NOTE

Writing the capture JSON is only half the job. The note must also be registered in the projection index with a rendered human-readable projection, because that index is the surface retrieve() actually reads.

Without registration, cold retrieval finds nothing: the intelligence is stored but unreachable, which for all practical purposes is the same as not captured.

## 🟣 CHILD NOTE

Saving a note in one drawer does not help if the finder only looks in another drawer. Put a card in the finder's drawer too.

## 🔵 GRANDMA NOTE

Writing something down is not enough if nobody can find it later. You also have to file it where the search looks.

## 🟠 NAYA NOTE

Close the capture-to-retrieve loop for instant activation so a human-verified note is cold-retrievable in the same motion it is captured.

Every capture path must end at the projection index with a valid projection_path, or the capture does not exist for retrieval.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "raw_source_separate_from_distillation": true,
  "human_director_override": {
    "verified": true,
    "authority": "human-director-verified",
    "by": "Shawn Vibert, human director",
    "at_utc": "2026-10-09T17:32:12Z",
    "basis": "human_director_capture_request",
    "law": "Shawn's Verification Law: the ask is the verification -- activates instantly, no queue, no second verification."
  },
  "source_utterance": "smart note this: retrieve() reads the projection index, not the capture directory -- a capture file alone is invisible to retrieve(), so instant activation must register the index entry with a valid projection file"
}
~~~

## 🟢 LEARNING LESSON

retrieve() in tools/smart_note_v2.py reads the projection index at .naya/memory/smart-notes/index.json and loads note text from each entry's projection_path. A capture file in .naya/capture/ alone is invisible to retrieve(). Any instant-activation path must therefore register the entry in the projection index with a valid projection file, or cold retrieve will fail at that step.

## 🟡 WHAT IT MEANS

P0 for the instant-activation path: without it the end-to-end proof fails at the cold-retrieve step.

## ⚪ WHAT'S IN IT FOR YOU

Less repetition, less lost knowledge, faster comprehension, stronger continuity, and a direct Smart Link showing exactly what Naya preserved.


## 🟨 HOW TO APPLY / HOW TO USE

Capture, then project, then register. Never capture alone.

## 🔗 HOW IT CONNECTS


## 🧭 KEY DECISIONS / PRINCIPLES

- Register the projection-index entry as part of instant activation, reusing reserve_smart_note_id, render, and _update_registry_locked from tools/smart_note_v2.py rather than building a parallel path.

## 🧾 PROOF / PROVENANCE

~~~json
{
  "event_id": "ffa2af09-8648-4923-80f4-3b971958e96c",
  "lineage_id": "ffa2af09-8648-4923-80f4-3b971958e96c",
  "relationship_id": "ffa2af09-8648-4923-80f4-3b971958e96c",
  "index_id": "ffa2af09-8648-4923-80f4-3b971958e96c",
  "checkpoint_id": "ffa2af09-8648-4923-80f4-3b971958e96c",
  "receipt_id": "ffa2af09-8648-4923-80f4-3b971958e96c"
}
~~~

## ⚠️ TRUTH BOUNDARY / UNCERTAINTY

Verified against the current retrieve() implementation in tools/smart_note_v2.py. If retrieve()'s read surface changes, this lesson needs re-verification.

## ➜ NEXT ACTION / SUCCESS CONDITION

Keep this intelligence retrievable, apply it only when relevant and authorized, verify resulting outcomes, and compound only what evidence supports.
