# SUPER NOTE — One Name, One Thing

> **The essence layer: 71 distilled Super Notes.** Raw Smart Notes live in the archive; the Hub wall shows these essences. Nothing here deletes or replaces any raw note.

| Field | Value |
|---|---|
| Super Note ID | `SUPER-004` |
| Hub wall row | `public.hub_smart_notes` ib_id `SUPER-004` |
| Human title | One Name, One Thing |
| Layer | ESSENCE — distilled from raw Smart Notes, never a raw capture |
| Distilled | 2026-10-21 — corrective distillation drive (639 raw → 71 essences); REPAIRED 2026-10-21 after independent audit found 42 MISSING + 151 PARTIAL — lost lessons restored from the originals (see REPAIR-LOG); coverage map regenerated mechanically from these files |
| Sources | 18 raw notes (full list below) |
| Cluster file | `cluster-01-super.json` |
| Canonical machine object | Hub DB row `public.hub_smart_notes` + `distill/all-super-notes.json` |
| Human projection | This Markdown file |
| Sync note | NOT ingested by hub-sync (its watcher parses only `BRAIN/05-MEMORY/SMART-NOTES`); archive + queue untouched |

---

## ✦ IN A NUTSHELL

A note's number is its name, and a name must belong to exactly one thing. Two different lessons wearing the same number will confuse everyone who comes looking later. So claim your number in the registry first, check everywhere — and if a clash appears, sort it out with evidence, never by deleting.

---

## 🩷 HUMAN NOTE

When many people write at once, the humble numbering of notes turns out to be load-bearing. If two different lessons share one number, a future reader — human or machine — can pull up the wrong lesson and act on it, while every file looks perfectly fine on its own. The defenses are habits: a number isn't yours until the registry holds your entry; a 'this number is free' check goes stale within minutes while others write, so check again at the moment you claim; and search every place claims can hide, including old branches and merged work. When a clash appears, classify it before touching anything — some are real, some are look-alikes, some are history.

---

## 🟣 CHILD NOTE

Imagine two kids in class with the exact same name, and the teacher calls out a grade to the wrong one. That's why every note gets its own number, written down in the class list before anyone starts — and if two notes end up sharing, we fix the list, we never throw a note away.

---

## 👵 GRANDMA NOTE

It's like house numbers on a street, dear. If two houses share one number, the mail goes to the wrong family. So we write each new number in the book first, we double-check the whole street — even the houses around the corner — and when there's a mix-up, we sort it calmly with proof. We never tear a house down over a numbering mix-up.

---

## 🤖 NAYA NOTE

Never stage a note on an unregistered number: write the registry entry first, with your lane, branch, and target path. Treat every 'number is free' scan as perishable — re-scan at claim time across the board, open work, the commit history, every branch carrying live claims, and all date folders, merged work included. Dedupe on the human-visible number, not just internal IDs. If you collide: classify before acting, close the flag with evidence, renumber the draft rather than the merged note, and honor the director's explicit lock above first-come claims. A renumber is itself a claim — verify the new number is free and the old one truly vacated.

---

## WHAT IT MEANS

Identity is what makes memory trustworthy. A learning system whose lessons can be silently swapped, forked, or double-filed doesn't compound knowledge — it compounds confusion. Treating the humble registry as the authority on identity, and the number as a continuity key rather than decoration, is what lets thousands of lessons stay findable and unambiguous as the team grows.

---

## WHAT'S IN IT FOR YOU

When you ask for a lesson by its number, you get that lesson — not a stranger wearing its name. Nothing you ratified gets quietly replaced by a same-numbered draft, and no hard-won lesson is ever deleted just to tidy up a numbering clash.

---

## HOW IT APPLIES

Claiming anything with a shared name — a note number, a file, a title: register the claim first, scan all the places claims live, re-scan right before you commit, and record the claim where others will actually look. Facing a duplicate: stop, classify it (real clash, look-alike, or history), gather evidence, and resolve by renaming the newcomer — preserving both contents.

---

## ⟲ RESTORED BY REPAIR — 2026-10-21

> Restored by the distillation repair after the independent essence audit (distillation-audit-20261021) found the lessons below MISSING from, or only partially carried by, this Super Note. Each entry restores the named source note's own rule in checkable words, traced to that source. Nothing here is new doctrine.

### SN-0115 — SMART NOTE — Three-Layer Collision Registry: Board, PR Heads, Commit Graph [audit: PARTIAL → lost element restored]

Numbering disputes are resolved by creation-time chronology — commit timestamps and PR creation times are the evidence — not announcement order; board announcements are advertising. First-claim stands on that chronology for the number. Renumbering is always the colliding lane's own call: the winning lane does not dictate the renumbering — "renumbering is the lane's call, not mine to touch" — the losing lane decides its own new number and its own repair path. Separate the number from the content before judging: a collision on the identifier is not a collision on the value.

### SN-0176 — Same Number, Different Bytes Is a Fork, Not a Second Edition [audit: PARTIAL → lost element restored]

A Smart Note's uniqueness key is the NUMBER across all date partitions, not (number, date). Same number + same bytes in another partition = harmless re-stage (idempotent skip); same number + different bytes = a content fork, a registry collision, never a revision or a second edition — revisions update the existing partition path. Before taking a number, verify it does not already exist under ANY date partition and byte-compare when it recurs; when a fork is found, flag-and-hold — the owning seats reconcile it, and no lane unilaterally renumbers.

### SN-0347 — Restatement Is Not Capture — Encode Against the Existing Note [audit: MISSING → restored in full]

Restating doctrine that already lives in an existing Smart Note is not a new capture: a standing law must be ENCODED against the note that already carries it, never restaged as a new note. Instead of staging a duplicate: bind the new work to the existing Smart Note — add the binding (machine-note reference, canonical-object pointer, or code constraint), reference it, and let the standing law's encoding point at the existing SN — and take no new SN number. Every duplicate capture of existing doctrine dilutes the brain: two notes claiming one truth splits provenance, confuses the retrieve path, and forces every future consumer to reconcile a question the brain should answer once. The procedure is a standing step of the capture loop: before staging, scan the tree for an existing SN carrying the doctrine; if one exists, produce the binding and stop. When in doubt, the default action is a binding, not a note.

### SN-0467 — The Counter Is Advisory, the Branch Tree Is Authority [audit: PARTIAL → lost element restored]

When the counter file and the branch claim-tree disagree on the next number, the branch tree is the authority and the counter is only advisory — the authority is the one whose error would break the world (the tree with the actual claims), not the convenience file. (The instance: the counter said 461 while the branch max was 462.) The staging path must scan the branch tree for any in-flight `/SN-NNNN/` claim before staging and refuse a taken number (exit 2) with the next-free suggestion — verified live: SN-0455 correctly refused, next-free SN-0463 suggested.

## SOURCES (traceability — every raw note this essence was distilled from)

- `IB-SMART-NOTE-20260930-sn0115-three-layer-collision-registry`
- `IB-SMART-NOTE-20260930-sn0145-self-collision-date-partitions`
- `IB-SMART-NOTE-20260930-sn0151-claim-registry-write-first`
- `IB-SMART-NOTE-20260930-sn0167-director-lock-outranks-first-claim`
- `IB-SMART-NOTE-20260930-sn0169-compelled-renumber-clears-registry`
- `IB-SMART-NOTE-20260930-sn0171-registry-scans-all-claim-branches`
- `IB-SMART-NOTE-20260930-sn0176-cross-partition-content-fork`
- `IB-SMART-NOTE-20260930-sn0184-registry-read-expiry-at-claim-time`
- `IB-SMART-NOTE-20260930-sn0189-close-collision-with-evidence`
- `IB-SMART-NOTE-20260930-sn0625-collision-triage-classify-before-acting`
- `IB-SMART-NOTE-20261004-sn0257-dedupe-must-cover-human-visible-id`
- `IB-SMART-NOTE-20261007-sn0545-registry-is-identity-authority-disambiguate-never-delete`
- `IB-SMART-NOTE-20261007-sn0616-human-id-continuity-boundary`
- `IB-SMART-NOTE-20261006-sn0467-counter-advisory-tree-authority`
- `IB-SMART-NOTE-20261005-sn0347-restatement-is-not-capture`
- `IB-SMART-NOTE-20261005-sn0372-sn-collision-arbitration-rule`
- `IB-SMART-NOTE-20261004-sn0303-registry-scan-decays-in-minutes`
- `IB-SMART-NOTE-20261004-sn0259-occupancy-scan-must-cover-merged-prs`
