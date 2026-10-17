# Dedup Keys Are Heuristics; Identity Is the Byte Hash

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01531-dedup-keys-are-heuristics
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-16
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** t0907-lane5 receipt (Lane 5, 2026-10-16 ~23:10 UTC) — first merge pass folded 4 spectrum buttons (different colors) + 6 checklist rows (different text) into 2 records on the "same demo_name + same classes" key; CORE-PRINCIPLES.md CANDIDATE 508; LEARNING event in learning-events-2026-10-16-16.md. Cousins: CANDIDATE 125 (spec-true vs code-true), CANDIDATE 504 (hash-before-place, the ingest side — this is the merge side). PR #2713 opened (unmerged, review-owned).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A merge rule keyed on "same demo_name + same classes" folded 4 spectrum buttons (different colors) and 6 checklist rows (different text) into 2 records — destroying real, distinct blocks, silently. The key was a heuristic wearing identity's clothes: it was many-to-one by construction, so folding on it folded distinct content. The root fix: hash the normalized content (byte-hash on normalized html + text-derived suffixes) and fold only on hash equality — near-dups (same key, different bytes) stay separate. Final tally: 457 records faithful, 11 true byte-dups folded, zero content destroyed. The durable rule: never fold on a key without hashing the content — the key is a guess about sameness; only the byte hash IS sameness. A dedup that destroys distinct records is not a merge, it is data loss with a clean log.

## 🩷 HUMAN NOTE

Imagine a librarian who merges "all the blue books by the same author" into one volume — because the catalog key said same author + same color. Four different blue books, six different pamphlets, all pulped into two Frankenstein volumes. The key was never identity; it was a guess that happened to collide. The fix: fingerprint the actual pages. Same fingerprint = same book, safe to merge. Different fingerprint = different book, hands off — no matter what the catalog key says. The discipline: the key narrows the search; only the fingerprint authorizes the fold. Anything else is shredding with extra steps.

## 🟣 CHILD NOTE

Imagine you have a box of crayons and you decide "all the red ones are the same crayon" — so you melt them together. But they were different reds: cherry, brick, rose! Now you have one muddy crayon instead of three pretty ones. The fix: look CLOSELY at each crayon first. If two crayons are exactly, exactly the same — same color, same size, same everything — then you can put them together. If they're even a tiny bit different, they stay separate. Names and labels are just guesses; the crayon itself is the truth.

## 🔵 GRANDMA NOTE

Dear, this one is about not throwing things away by mistake. We had a tidy-upper who put things in the same drawer because the labels matched — and threw out real treasures, because the labels were only guesses. Four buttons, six list rows, all different, all gone into two drawers. So we taught the tidy-upper a new rule: open the thing, look at what's actually inside, take its fingerprint — and only put two things together when the fingerprints match exactly. The wisdom, dear: a label tells you where to look; only the thing itself tells you what it is. Never melt the crayons on the strength of the label.

## 🟠 NAYA NOTE

Apply this to every dedup/merge/fold rule before it runs: (1) treat the identity key as a heuristic — a search-space narrow, never an identity; (2) hash the normalized content (normalize first: whitespace, attribute order, and other formatting noise, so formatting twins hash equal and true distincts hash different) and fold ONLY on hash equality; (3) near-dups — same key, different bytes — stay separate by construction; the 508 incident's 4 spectrum buttons and 6 checklist rows are the canonical near-dup shape; (4) report the fold honestly: N records in, M folded as true byte-dups, K near-dups kept separate — the 457/11/near-dup-kept accounting is the proof the rule didn't shred; (5) pair with CANDIDATE 514 (two-seed determinism before the pin) — the merge script's output hash must also be seed-stable, or the "11 true dups" number is itself a lottery draw. Cousin map: CANDIDATE 125 (spec-true vs code-true — the key was spec-true, the bytes were code-false); CANDIDATE 504 (hash-before-place — the ingest-side twin of this merge-side rule); SN-1528 (pins need addresses — the fold report is the address of the dedup decision).

## 🟢 MACHINE NOTE

~~~json
{
  "sn": 1531,
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "rule": "fold_only_on_byte_hash_of_normalized_content_never_on_heuristic_keys",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/t0907-lane5 (2026-10-16 ~23:10 UTC)",
    "violation": "first merge pass folded 4 spectrum buttons (different colors) + 6 checklist rows (different text) into 2 records on the 'same demo_name + same classes' key — real distinct blocks destroyed silently",
    "root_fix": "byte-hash on normalized html + text-derived suffixes; fold only on hash equality; near-dups (same key, different bytes) kept separate",
    "final_tally": "457 records faithful, 11 true byte-dups folded, zero content destroyed; PR #2713 opened (unmerged, review-owned)"
  },
  "procedure": [
    "treat every dedup identity key as a heuristic (search-space narrow), never as identity",
    "normalize the content (whitespace, attribute order, formatting noise), then hash; fold ONLY on hash equality",
    "keep near-dups (same key, different bytes) separate by construction",
    "report the fold accounting: records in / true byte-dups folded / near-dups kept separate",
    "pair with the two-seed determinism check so the fold report itself is reproducible"
  ],
  "applies_when": ["dedup", "merge", "catalog", "ingest", "block-extraction", "lane-executor"],
  "enforcement": "the merge/dedup script's fold key must be the sha of the normalized content (byte-hash on normalized html + text-derived suffixes in the 508 fix), not the heuristic key; the script's fold report must account records-in / true-byte-dups-folded / near-dups-kept-separate, and a fold with destroyed-but-distinct content is a data-loss defect — precedent: t0907-lane5's first pass shredded 10 distinct blocks on the demo_name+classes key; the fixed rule kept 457 faithful with 11 true folds",
  "cousins": ["CANDIDATE 125 (spec-true vs code-true — the key was spec-true)", "CANDIDATE 504 (hash-before-place — ingest-side twin)", "CANDIDATE 514 / SN-1529 (two-seed determinism — the fold report must be reproducible)", "SN-1528 (pins need addresses — the fold report is the dedup decision's address)"],
  "decision_change": "how merge/dedup rules are written and reviewed: key-on-hash is the bar; any rule folding on a bare heuristic key is rejected as a data-loss risk; fold reports must show the near-dup accounting",
  "falsifier": "a domain where the heuristic key is provably one-to-one with content (the key is itself a content hash, or a uniqueness constraint is mechanically enforced upstream) makes the extra hash redundant — the rule must name when the key is provably injective; or over-normalization shown to hash-distinct records equal, miscalibrating the rule",
  "mechanism": "heuristic keys (name + classes) are many-to-one by construction — distinct content routinely shares them; only the byte hash is one-to-one with the content. Folding on the key therefore folds on a collision class, and collisions destroy distinct records. Normalization removes formatting noise so formatting twins still fold; the hash then decides identity exactly",
  "admission_gates": {"durable": true, "new": true, "signal": true, "evidence_backed": true}
}
~~~
