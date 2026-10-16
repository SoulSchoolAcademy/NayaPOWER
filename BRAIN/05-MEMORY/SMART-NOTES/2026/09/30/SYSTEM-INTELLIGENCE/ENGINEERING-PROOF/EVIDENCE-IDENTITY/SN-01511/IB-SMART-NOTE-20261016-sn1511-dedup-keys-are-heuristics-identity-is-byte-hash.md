# Dedup Keys Are Heuristics — Identity Is the Byte Hash: Never Fold on a Key Without Hashing the Content

**Intelligent Block:** IB-SMART-NOTE-20261016-sn1511-dedup-keys-are-heuristics-identity-is-byte-hash
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-16
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 16:38 PDT distillation tick (2026-10-16) from `hidden_files/learning-events-2026-10-16-16.md` — CANDIDATE 508 (t0907-lane5, 2026-10-16 ~23:10 UTC, Naya Clarity Narzan; appended to `hidden_files/CORE-PRINCIPLES.md` as candidate 508).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A merge pass folded records on an identity key — "same demo_name + same classes" — and silently destroyed real data: 4 spectrum buttons with different colors and 6 checklist rows with different text shared keys, so 10 distinct records collapsed into 2. The key was a heuristic wearing an identity costume. The fix was at the root: hash the normalized content (byte-hash on normalized html + text-derived suffixes) before folding — near-dups with the same key but different bytes stayed separate; the final 457 records were faithful and only 11 true byte-dups folded. The lesson: a merge rule's identity key is a heuristic, not identity — never fold on a key without hashing the content. Identity is the byte hash; everything else is a guess that can eat your records.

## 🩷 HUMAN NOTE

Imagine sorting a mailroom by last name and throwing away "duplicates" — two letters to different people named Smith get merged into one, and one person's mail is gone. That's what happened: the sorter used a rough label (name + category) instead of checking the actual contents, and ten different items got crushed into two. The fix: open the envelope and compare the letters themselves before declaring two the same. The lesson: a label is a shortcut, not an identity — before you throw anything away as a duplicate, compare the actual bytes. Shortcuts destroy real things when they guess wrong.

## 🟣 CHILD NOTE

Imagine you have two toy boxes, and you decide to merge them by keeping only one of every "red car." But the two red cars are different — one's a race car, one's a fire truck. If you only look at the color label, you throw away a real toy. A worker did exactly this with computer records: the labels matched, so she merged them — and ten different things became two. Then she learned to look at the *actual toys* (the bytes) before merging. The lesson: labels can lie by accident. Always check the real thing underneath before you say "these are the same."

## 🔵 GRANDMA NOTE

It's like a librarian who throws away "duplicate" books based on the spine label — but two books with the same title can have different stories inside. A worker's cleanup pass did just that: ten genuinely different records got folded into two because their labels matched, and the differences were lost for good. The fix was simple and permanent: compare the actual contents, word for word, before calling anything a duplicate. The lesson: a name tag is not the thing itself. When you're deciding two things are identical, look at what's inside, not what's written on the outside.

## 🟠 NAYA NOTE

Cold successor: any merge/dedup rule keyed on a heuristic ("same demo_name + same classes") is a projection — it discards information by design, and two different contents can share a projection while never sharing bytes. The t0907 damage is worked evidence: 10 real records (4 spectrum buttons, different colors; 6 checklist rows, different text) folded into 2 by a key that "matched." Rule: hash the normalized content before folding — byte-hash on normalized html + text-derived suffixes — and treat the hash as identity; near-dups (same key, different bytes) stay separate. What falsifies this lesson: a worked case where byte-hash identity folded two records a cold reader genuinely needed separate (a collision of meaning, not of bytes — the hash would then be the wrong identity), or a heuristic key provably non-colliding over its full domain (then the hash is redundant cost). The mechanism: a key is a lossy projection of content; folding on a projection identifies the projection, not the content — only the byte hash is a lossless identity, so only the hash can authorize a fold. Cousins: CANDIDATE 125 (spec-true ≠ code-true), CANDIDATE 504 (hash-before-place, the ingest side — this is the merge side). Filed against the t0907 catalog merge (457 final records, PR #2713 opened, unmerged).

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "heuristic_identity_key_record_destruction",
  "evidence": {
    "events": "hidden_files/learning-events-2026-10-16-16.md — CANDIDATE 508 (t0907-lane5, 2026-10-16 ~23:10 UTC)",
    "damage": "first pass folded 4 spectrum buttons (different colors) + 6 checklist rows (different text) into 2 records — same key, different bytes; real records destroyed",
    "root_fix": "byte-hash on normalized html + text-derived suffixes before folding; near-dups (same key, different bytes) stay separate",
    "result": "final 457 records faithful, 11 true byte-dups folded; PR #2713 opened (unmerged)",
    "core_principles": "hidden_files/CORE-PRINCIPLES.md candidate 508",
    "cousins": ["CANDIDATE 125 (spec-true ≠ code-true)", "CANDIDATE 504 (hash-before-place, ingest side)"]
  },
  "decision_change": "merge/dedup rules key on content hashes, never bare heuristics — never fold on a key without hashing the content",
  "falsifier": "a worked case where byte-hash identity folded two records a cold reader genuinely needed separate (meaning-collision, not byte-collision), or a heuristic key provably non-colliding over its full domain",
  "mechanism": "an identity key is a lossy projection of content; folding on a projection identifies the projection, not the content — only the byte hash is a lossless identity, so only the hash can authorize a fold"
}
~~~
