# SUPER NOTE — Permission Dies When the World Moves

> **The essence layer: 71 distilled Super Notes.** Raw Smart Notes live in the archive; the Hub wall shows these essences. Nothing here deletes or replaces any raw note.

| Field | Value |
|---|---|
| Super Note ID | `SUPER-002` |
| Hub wall row | `public.hub_smart_notes` ib_id `SUPER-002` |
| Human title | Permission Dies When the World Moves |
| Layer | ESSENCE — distilled from raw Smart Notes, never a raw capture |
| Distilled | 2026-10-21 — corrective distillation drive (639 raw → 71 essences); REPAIRED 2026-10-21 after independent audit found 42 MISSING + 151 PARTIAL — lost lessons restored from the originals (see REPAIR-LOG); coverage map regenerated mechanically from these files |
| Sources | 12 raw notes (full list below) |
| Cluster file | `cluster-01-super.json` |
| Canonical machine object | Hub DB row `public.hub_smart_notes` + `distill/all-super-notes.json` |
| Human projection | This Markdown file |
| Sync note | NOT ingested by hub-sync (its watcher parses only `BRAIN/05-MEMORY/SMART-NOTES`); archive + queue untouched |

---

## ✦ IN A NUTSHELL

Permission is pinned to one exact version at one exact moment. The moment the work moves on, the permission, the decision, and the proof all expire together. Before you act, look again at what is actually there now — and judge only the exact bytes in front of you.

---

## 🩷 HUMAN NOTE

Approvals feel permanent, but they describe a snapshot. A director can approve one version on Monday; by Tuesday the team has added twelve more changes, and that approval simply does not describe what would ship anymore. The honest move is to stop, name the new version, and get the approval re-anchored — never to quietly substitute the old yes onto new work. The same rule protects reviewers: once a version is frozen for judging, later edits don't move the target, and a merged result must be proven by what actually landed, not by what was reviewed.

---

## 🟣 CHILD NOTE

If Mom says yes to the red bike, that yes is only for the red bike. If the shop swaps in a blue one, you have to ask again. And if someone already bought the bike while you were deciding, you say so out loud — you don't pretend it was your trip to the shop.

---

## 👵 GRANDMA NOTE

It's like a prescription, dear. The doctor wrote it for the medicine in front of her, on that day. If the bottle changes, the old prescription doesn't cover the new bottle — you go back and ask. Nobody sensible minds asking again; what matters is never guessing with someone's health.

---

## 🤖 NAYA NOTE

Bind every authorization, decision, and scorecard to the exact version it was measured on, and re-resolve the live state at the instant of action — between the decision and the act. If the target moved, the old permission is void: name the fresh version and stop for a re-anchor. Keep frozen review targets frozen. Prove merges by what landed on the main line, not by the branch that was reviewed. And when events overtake one of your receipts, publish a correction that says plainly what the record actually shows.

---

## WHAT IT MEANS

In a fast-moving system, most mistakes are not bad decisions — they are good decisions applied to a world that no longer exists. Pinning permission to exact bytes and exact moments turns every approval into something checkable, and forces the healthy pause exactly where the risk lives: in the gap between deciding and doing.

---

## WHAT'S IN IT FOR YOU

Nothing you approved in one form ever ships in another form behind your back. When you say yes, you know precisely what your yes covers — and if the work changes, you get asked again before anything irreversible happens. That is how you stay in real control without having to watch every keystroke.

---

## HOW IT APPLIES

Whenever you act on an approval: re-check the current state first; compare it to what was approved; if they differ, stop and re-anchor. Freeze what will be judged and judge only that. After anything lands, verify the landed result itself. If your own earlier statement turns out stale, correct it publicly and promptly — a corrected record is a strength, not a shame.

---

## ⟲ RESTORED BY REPAIR — 2026-10-21

> Restored by the distillation repair after the independent essence audit (distillation-audit-20261021) found the lessons below MISSING from, or only partially carried by, this Super Note. Each entry restores the named source note's own rule in checkable words, traced to that source. Nothing here is new doctrine.

### SN-0191 — The Repo Is the Demo — the Freeze-Point Protocol [audit: PARTIAL → lost element restored]

The demo protocol itself, four rules, mechanical: 1. Code lands in GitHub first — every shareable checkpoint is a pushed commit on a branch, and that commit SHA is the freeze point. 2. What the director views = the frozen SHA, via the Cloudflare-synced live version or by downloading the HTML from GitHub at that commit. 3. Nothing is shown outside GitHub that isn't pushed — if a preview appears in chat or the feed, it is rendered FROM the frozen commit, never a side copy, never a mockup that drifts. 4. The judge scores the same SHA the director viewed. One SHA, one review, one gate — the repo is the demo.

### SN-0328 — The Auto-Merge Gate Must Re-Verify on the Merge Commit — the Merge Itself Changes the Tree [audit: PARTIAL → lost element restored]

A merge itself produces a new tree, so pre-merge evidence does not transfer: every check and approval that qualified the pre-merge state proves nothing on the post-merge tree. The auto-merge gate's mechanical preconditions must include re-verification on the exact merge commit, re-running derived-layer checks (index `--check`, ledger, caches) on that commit — because only the merge commit is the tree the repo actually gets. (The instance: the #1438 auto-merge landed a `BRAIN/` file without regenerating the index layer, 188 → 189 files, `--check` RED on the merge commit.)

### SN-0415 — The Authorization Window Race — a SHA-Pinned Human Deploy Authorization Is Voided by Any Main Movement [audit: PARTIAL → lost element restored]

HOLD MAIN must precede the authorization request, not follow it: the freeze is the first step of the deploy sequence — asking for a SHA's deploy authorization while unrelated merges are free to land turns the authorization into a lottery ticket. The operating sequence: (1) establish HOLD MAIN first; (2) get the authorization for the exact frozen SHA; (3) re-verify main == SHA immediately before dispatch; (4) dispatch with the exact SHA. A human deploy authorization binds to the exact SHA, never to "current main" — if main moves at any point between authorization and dispatch acceptance, the authorization is void and must be re-requested for the new exact SHA. Record authorizations as facts, but never infer deployment from them; only a completed governed workflow run is deployment evidence.

### SN-0553 — The Overtaken Receipt — When the Tip Outruns Your Receipt, Publish a Temporal Correction [audit: PARTIAL → lost element restored]

When a pre-action receipt is overtaken by a moved tip, publish a temporal correction that: (1) quotes or cites the overtaken receipt; (2) states the live resolution with exact evidence — new main SHA, merge timestamp, which account GitHub records; (3) explicitly disclaims authorship of the action another hand completed ("I do not claim this seat performed or authorized that already-completed action"); and (4) reclassifies the receipt as a post-hoc record. Never let a stale receipt stand as authorization. GitHub recording a merge under an account does not establish which interaction caused it.

### SN-0563 — The PR Head Is Not the Merge Commit — Prove a Merge by Ancestry [audit: PARTIAL → lost element restored]

A merge is proven only by ancestry of the merge commit inside `refs/heads/main` (`git merge-base --is-ancestor <merge-sha> refs/heads/main`), never by PR head SHA equality or PR state labels. Squash merges and merge commits replace the head SHA entirely — the head ceases to exist as the identity of what landed. Verification receipts must record the merge commit, never the head, and the assertion must be ancestry, never equality; if the ancestry assertion fails, the claim is UNPROVEN.

## SOURCES (traceability — every raw note this essence was distilled from)

- `IB-SMART-NOTE-20260930-sn029-sha-bound-authorization`
- `IB-SMART-NOTE-20260930-sn0191-repo-is-the-demo-freeze-point-protocol`
- `IB-SMART-NOTE-20260930-sn0206-frozen-sha-judges-anchor`
- `IB-SMART-NOTE-20260930-sn0328-the-auto-merge-gate-must-re-verify-on-the-merge-commit`
- `IB-SMART-NOTE-20260930-sn0475-deployment-authorization-sha-expiry`
- `IB-SMART-NOTE-20261006-sn0473-review-head-stability`
- `IB-SMART-NOTE-20261007-sn0562-exact-sha-authorization-dies-when-tip-moves`
- `IB-SMART-NOTE-20261007-sn0563-pr-head-is-not-merge-commit-prove-by-ancestry`
- `IB-SMART-NOTE-20261007-sn0553-overtaken-receipt-temporal-correction`
- `IB-SMART-NOTE-20261007-sn0564-verification-packet-photograph-receiver-reanchors`
- `IB-SMART-NOTE-20261006-sn0493-decision-expires-when-tip-moves-reverify-at-action`
- `IB-SMART-NOTE-20261005-sn0415-authorization-window-race`
