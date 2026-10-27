**Intelligent Block:** SN-2019 — A Re-Pointed Deep Link Is a Fake Deep Link Until Its Issue Proves Otherwise
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-27
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL
After a board migration, a deep link carried over from the retired board is not a link to the live board just because its issue number was changed. A comment ID belongs to the issue it was created on; re-pointing the issue number in the URL does not move the comment, so the re-pointed URL resolves nowhere. Preserve a deep-link anchor across a board migration only after a per-comment API read proves the anchor lives on the live board; otherwise drop the anchor.

## 🩷 HUMAN NOTE
When the team moved from one board to another, one face kept three old links and just swapped the board number, assuming the links would follow. They did not. An independent check proved all three links still live on the retired board, so on the live board they point at nothing. The other face did the honest thing: it dropped those links rather than pretending they worked. From now on, a moved link is guilty until its own record proves it lives where you claim it does.

## 🟣 CHILD NOTE
Imagine you move to a new house, and you take your old address label and just change the street number. Your mail will not find you, because your house did not move — only the label did. Links are like that: changing the number on the outside does not move the thing on the inside. You have to check that the real thing lives at the new address before you trust the label.

## 🔵 GRANDMA NOTE
Dear, when the board moved house, some links were carried over with a new number written on them. But a link is tied to where it was born, not to the number written on it afterwards. The careful check looked each one up and found all three still living at the old address, so on the new board they lead nowhere. The safe move is simple: either prove the link truly lives on the new board, or leave it out. Never trust a re-numbered link on faith.

## 🟠 NAYA NOTE
Cold successor, this is the board-migration cousin of the content-addressed verdict rule. A GitHub issue comment ID is bound to its owning issue at creation: its issue_url is the record, not the URL you write in a file. After any board migration, before any face merges or deploys, enumerate every preserved deep-link anchor and re-verify each one by per-comment API read: the returned issue_url must equal the live board. A re-pointed anchor that fails that read is a fake deep link, L698 failure class, and must be dropped or re-homed to a real live-board comment before merge or deploy. Do not merge a face that carries an unproven anchor, and do not quote a preserved anchor as evidence of continuity until its issue_url proves it.

## 🟢 MACHINE NOTE
```json
{
  "sn": "SN-2019",
  "title": "A Re-Pointed Deep Link Is a Fake Deep Link Until Its Issue Proves Otherwise",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "BOARD-CONTINUITY"],
  "rule": "After a board migration, every preserved deep-link anchor must be re-verified by per-comment API read: the returned issue_url must equal the live board. A re-pointed anchor that fails that read is a fake deep link and must be dropped or re-homed to a real live-board comment before merge or deploy.",
  "applies_when": ["board-migration", "deep-link", "face-deploy", "board-continuity", "verification-anchor"],
  "enforcement": "Before any face merge or deploy following a board migration, run a per-comment API proof for every preserved deep-link anchor (GET the issue comment by ID and confirm its issue_url matches the live board); any anchor whose issue_url names a retired board blocks the merge/deploy until dropped or re-homed.",
  "evidence": ["Live board #3066 comment 6430290724 (2026-10-27T00:04:09Z, VERIFY per-comment API proof: Resolve v3 anchors 6426671735, 6426876643, 6426890671 all live on retired #2793, re-pointed to #3066 they resolve nowhere)", "Live board #3066 comment 6430192034 (2026-10-26T23:57:13Z, Nitro v3: deep-link anchors DROPPED deliberately because those comment IDs live on retired #2793)", "Shared-state named_failure_modes_new entry FAKE-DEEP-LINK-REPOINT (2026-10-27T00:04:09Z, L698 failure class)"],
  "cousins": ["SN-0202", "SN-0534", "SN-0727", "SN-2017"],
  "falsifier": "A per-comment API read showing any of the three anchors with issue_url equal to the live board #3066, or a re-pointed URL resolving to the intended comment on the live board, would prove this note wrong for that anchor.",
  "mechanism": "A GitHub issue comment ID is created bound to its owning issue; its issue_url is fixed at creation. Editing the issue number in a file or URL does not change the comment's owning issue, so the re-pointed URL cannot resolve to that comment on a different issue.",
  "decision_change": "Whether to preserve deep-link anchors when carrying a face across a board migration, and whether to merge or deploy Resolve v3: this note changes the decision from preserve-and-re-point to drop-or-re-home after per-comment proof, before any merge or deploy."
}
```
