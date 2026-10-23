Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-23
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

SN-1853's 06:24:54Z door filing (direct commit 7fec165e, tip 23a4aa5d→7fec165e) touched the smart-notes corpus and carried in-landing regen — but the committed corpus_manifest_hash no longer matched the entries, so every KNOW retrieval read failed closed INDEX_CORRUPT:MANIFEST_STALE, fourteen of them (red 6→20 failed / 5,405 passed, run 39911334459). Brain-index freshness x3 re-fired anyway; the regen ran and cured nothing. The durable rule: **a regen that does not recompute the committed manifest hash is not a regen.** The manifest hash is a precomputed commitment of corpus contents; KNOW retrieval verifies it before reading, and any corpus write that skips the recompute turns every read into a closed door. The door filing must include the corpus_manifest_hash recompute (tools/regenerate_brain_index.py) in the same contents-write — and the proof is the MANIFEST_STALE assertions passing, never "regen ran."

## 🩷 HUMAN NOTE

Shawn — a Smart Note landed through the intelligence door and broke the knowledge index: fourteen reads failing closed, all saying the manifest hash doesn't match the entries. The filing even ran its regen step — but the regen rebuilt entries without recomputing the hash the readers check first. So the note is live and the library is locked. The rule going forward: the door write has to recompute the manifest hash in the same write, and "the index is fine" is proven by the hash-match checks passing, not by "regen ran." (#3003's index cure is still open on the stale base, so this failure class is live until it lands.)

## 🟣 CHILD NOTE

Imagine you update every book in a library, and the librarian's master list has a checksum at the top. You reshelved all the books — but you forgot to update the checksum on the master list. Now every time someone asks for a book, the librarian checks the checksum first, sees it doesn't match, and refuses to hand out ANY book — even though all the books are right there on the shelves. The fix: update the checksum every time you touch the shelves, in the same trip.

## 🔵 GRANDMA NOTE

It's like a safety-deposit box where the bank keeps a wax seal with the exact weight of the box's contents. You add a coin — a proper, authorized addition — but nobody re-weighs and re-seals. Now every visit, the bank weighs the box, finds the seal wrong, and won't open it for anyone. The addition was fine; the missing re-weigh is what locked everyone out. Re-seal every time you touch the box, as part of touching it.

## 🟠 NAYA NOTE

This is SN-1729's freshness contract meeting its sharp edge. SN-1729 said: bind the re-stamp to the mutating commit. The 06:24Z door filing obeyed the letter — in-landing regen ran — and violated the spirit: the regen rebuilt entries but never recomputed the committed corpus_manifest_hash, so the invariant the readers actually enforce stayed broken. The lesson is the failure of a ritual: "regen ran" became a claim that substitutes for the proof. The machine truth: KNOW retrieval verifies corpus_manifest_hash before reading; a mismatch fails closed INDEX_CORRUPT on every read. The seat-level fix is in the door workflow, not in a new gate: the contents-write that mutates the corpus must include the hash recompute in the same write, and the acceptance proof is the MANIFEST_STALE assertions green — fourteen failures named it louder than any checklist. Cousin: SN-1729 (the general freshness contract); this is the first instance of its regen-without-recompute subclass.

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn-1866-manifest-stale-fail-closed",
  "lesson": "A regen that does not recompute the committed manifest hash is not a regen: SN-1853's 06:24:54Z door filing (7fec165e) carried in-landing regen but left corpus_manifest_hash mismatched, so every KNOW retrieval read failed closed INDEX_CORRUPT:MANIFEST_STALE (14 failures, red 6->20, run 39911334459) while freshness x3 re-fired. The door's contents-write must include the corpus_manifest_hash recompute (tools/regenerate_brain_index.py) in the same write; the proof is the MANIFEST_STALE assertions passing, never 'regen ran'.",
  "applies_when": ["door", "index-regen", "knowledge", "retrieval", "intelligence", "failure:manifest-stale", "manifest-hash"],
  "enforcement": "WIRE suite MANIFEST_STALE assertions + the door-obligation check-run at tip fail closed INDEX_CORRUPT on manifest-hash mismatch (observed: 14 failures at run 39911334459, door-obligation check-run 120274796930 failing at tip 7fec165e). Door-filing workflow must run the corpus_manifest_hash recompute (tools/regenerate_brain_index.py) in the same contents-write that mutates the corpus; the acceptance proof is the MANIFEST_STALE assertions green — 'regen ran' is not proof.",
  "evidence": [
    "board comment 6358994254 (WIRE sign-out 06:30Z, created 2026-10-23T06:33:00Z — 'NEW failure class MANIFEST_STALE cascade x14 — smart-notes index committed corpus_manifest_hash no longer matches entries, every KNOW retrieval read fails closed INDEX_CORRUPT:MANIFEST_STALE; brain-index freshness x3 STILL re-fired (filing carried in-landing regen, did not cure); test red 6->20 failed / 5,405 passed (run 39911334459)')",
    "shared-state.json merge_watch_latest (tick_utc 2026-10-23T06:38:00Z — 'tip moved by single door-filing direct commit 06:24:54Z; door-obligation workflow at this tip = failure (check-run 120274796930); #3003 did NOT land, base stale')",
    "cousin SN-1729 (same-commit re-stamp rule) — this is the first instance of its regen-without-recompute subclass"
  ]
}
```
