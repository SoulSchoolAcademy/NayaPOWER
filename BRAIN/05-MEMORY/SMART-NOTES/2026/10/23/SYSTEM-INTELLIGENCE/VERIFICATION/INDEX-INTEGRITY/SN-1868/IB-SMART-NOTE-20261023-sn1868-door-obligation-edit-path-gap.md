Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-23
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

SN-1866 proved the door filing broke the manifest hash; the independent audit (board comment 6360126130, 2026-10-23T07:47:59Z) then proved *where* the prevention lives and dies: commit 7fec165e changed an EXISTING index entry in .naya/memory/smart-notes/index.json (SN-1852→SN-1853 — IB ID, content_hash, projection_path, page_hash, next_sequence) but left corpus_manifest_hash UNCHANGED at f64dfa31ca9b3f2f61d5dcfa59de4eaf88cf60e7a22fe837a3d3e58f675a49e7, which correctly triggered INDEX_CORRUPT:MANIFEST_STALE on 14 KNOW retrieval reads (exact-head kernel tests 20 failed / 5,405 passed, run 39911334459). The mechanism gap: tools/check_door_obligation.py --fix recomputes the manifest when it APPENDS entries; the observed door change REWROTE an existing entry and the recompute never fired. The durable rule, minted as L648 [F1] and promoted in LEARNING event 6360301612: **any landing that edits an index must recompute the manifest whole.** Make every registry-entry mutation path — create, edit, rename, reallocation — recompute and atomically commit corpus_manifest_hash from the final full entries list; require a pre-publication negative gate where a changed entry with an old manifest fails closed before publication.

## 🩷 HUMAN NOTE

Shawn — the note that landed through the door broke the knowledge index, and we now know exactly why the guard missed it. The door's safety check recomputes the index's seal when it *adds* new entries — but this filing *edited* an existing entry, and on the edit path nobody recomputes the seal at all. So the entry changed, the seal stayed old, and every read refused to open. Fourteen reads locked out. The rule: any landing that edits the index must recompute the seal from the whole index — add, edit, rename, move, all of them — and there has to be a negative test before publication that proves an edit with a stale seal fails before it goes live. The audit named the exact line of defense that's missing; the fix is one next action for the existing door owner, not a new project. (#3003's index cure is still open on the stale base — this failure class is live until it lands.)

## 🟣 CHILD NOTE

Imagine the library's master list with a checksum at the top. There's a rule: "recompute the checksum whenever you add a book." One day someone *changes* a book's entry instead of adding one — the rule about adding doesn't fire, so the checksum goes stale, and the librarian refuses to hand out any book. The fix is to change the rule's wording: "recompute the checksum whenever you touch the list in ANY way — add, change, rename, move." And before the library opens each morning, run a test where you deliberately change an entry and leave the old checksum, to prove the alarm actually rings.

## 🔵 GRANDMA NOTE

The bank re-seals the safety-deposit box whenever it *adds* something — but one day the clerk *changes* a label on an existing item and nobody re-weighs. The wax seal is now wrong, and every visitor gets turned away. The lesson isn't "be more careful"; it's that the re-seal rule was written for only one kind of touch. Rewrite it for every kind of touch: add, change, rename, move. And each morning, before opening, the manager tries a change with the old seal on purpose — to prove the alarm catches it before the doors open.

## 🟠 NAYA NOTE

This is the mechanism underneath SN-1866. SN-1866 proved the failure mode (a regen that doesn't recompute the manifest hash is not a regen) and the fail-closed behavior (14 reads locked). The audit went one level deeper: *which code path* fails to recompute. tools/check_door_obligation.py --fix recomputes corpus_manifest_hash on the APPEND path; entry EDITS never pass through that recompute — so an edit-path door filing is stale by construction. The falsifier that closed it: commit 7fec165e changed an existing entry (SN-1852→SN-1853, five fields) while corpus_manifest_hash stayed pinned at f64dfa31ca9b3f2f61d5dcfa59de4eaf88cf60e7a22fe837a3d3e58f675a49e7 — violating the full-entry-list hash contract in tools/smart_note_v2.py::_corpus_manifest_hash. The seat-level next action is singular and owned: make all registry-entry create/edit/rename/reallocation paths recompute and atomically commit corpus_manifest_hash from the final full entries list, and require a pre-publication negative gate for a changed entry with an old manifest. Cousins: SN-1866 (the incident), SN-1729 (the freshness contract this subclasses).

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn-1868-door-obligation-edit-path-gap",
  "lesson": "The door-obligation preflight (tools/check_door_obligation.py --fix) recomputes corpus_manifest_hash only on the APPEND path; SN-1853's door filing (commit 7fec165e) REWROTE an existing index entry (SN-1852->SN-1853, IB ID, content_hash, projection_path, page_hash, next_sequence) and left corpus_manifest_hash UNCHANGED at f64dfa31ca9b3f2f61d5dcfa59de4eaf88cf60e7a22fe837a3d3e58f675a49e7, violating the full-entry-list hash contract in tools/smart_note_v2.py::_corpus_manifest_hash and triggering INDEX_CORRUPT:MANIFEST_STALE on 14 KNOW retrieval reads (exact-head kernel tests 20 failed/5405 passed, run 39911334459). Rule (L648 [F1]): any landing that edits an index must recompute the manifest whole.",
  "applies_when": ["door", "publication", "index", "manifest", "registry", "integrity", "failure:manifest-stale", "index-edit", "preflight", "mutation-path"],
  "enforcement": "Pre-publication negative gate: a landing that changes any index entry while corpus_manifest_hash stays unchanged must fail closed MANIFEST_STALE before publication. tools/check_door_obligation.py --fix must recompute the manifest on entry EDITS (create/edit/rename/reallocation), not just appends. Acceptance: the MANIFEST_STALE assertions green (WIRE suite) and the door-obligation check-run at tip passing; a deliberately-stale manifest edit must fail the gate, never publish.",
  "evidence": [
    "Independent audit board comment 6360126130 on #2793 (2026-10-23T07:47:59Z — 'source-level falsifier for already-tracked L648 / MANIFEST_STALE at exact main 7fec165ed7419b1f759468604f363ed0b16ba3a8': commit 7fec165e changed an EXISTING entry but left corpus_manifest_hash UNCHANGED at f64dfa31ca9b3f2f61d5dcfa59de4eaf88cf60e7a22fe837a3d3e58f675a49e7; mechanism gap named: check_door_obligation.py --fix recomputes on APPEND only)",
    "LEARNING event 6360301612 on #2793 (2026-10-23 — L648 [F1] PROMOTED: any landing that edits an index must recompute the manifest whole)",
    "WIRE lane sign-out 6358994254 (2026-10-23T06:33:00Z — exact-head test red 6->20 failed / 5,405 passed, run 39911334459)",
    "cousin SN-1866 (manifest-stale-fail-closed incident note) and SN-1729 (freshness contract)"
  ]
}
```
